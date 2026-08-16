import ast
import builtins
import pkgutil
import re
import sys
import sysconfig
import unittest
from io import BytesIO
from pathlib import Path
from unittest.mock import patch

import Clouds_Coder as cc

ROOT = Path(__file__).resolve().parents[1]
SOURCE_PATH = ROOT / "Clouds_Coder.py"
REQUIREMENTS_PATH = ROOT / "requirements.txt"

# Import names and PyPI distribution names are not always identical. Keep this
# mapping explicit so newly introduced host dependencies cannot silently rely
# on a fallback simply because requirements.txt was not updated.
IMPORT_TO_DISTRIBUTION = {
    "PIL": "Pillow",
    "bleach": "bleach",
    "brotli": "brotli",
    "certifi": "certifi",
    "chardet": "chardet",
    "charset_normalizer": "charset-normalizer",
    "debugpy": "debugpy",
    "docx": "python-docx",
    "fitz": "PyMuPDF",
    "imgkit": "imgkit",
    "jedi": "jedi",
    "markdown": "Markdown",
    "numpy": "numpy",
    "openpyxl": "openpyxl",
    "pdfminer": "pdfminer.six",
    "playwright": "playwright",
    "pptx": "python-pptx",
    "watchfiles": "watchfiles",
    "xlrd": "xlrd",
    "yaml": "PyYAML",
}

# Loaded through ``python -m`` / ``find_spec`` rather than an import statement.
DYNAMIC_RUNTIME_MODULES = {"debugpy"}


def stdlib_module_names() -> set[str]:
    """Return stdlib top-level names on old and new supported Pythons."""
    current = getattr(sys, "stdlib_module_names", None)
    if current is not None:
        return set(current)

    names = set(sys.builtin_module_names)
    search_paths = {
        path
        for path in (
            sysconfig.get_paths().get("stdlib"),
            sysconfig.get_paths().get("platstdlib"),
            sysconfig.get_config_var("DESTSHARED"),
        )
        if path
    }
    names.update(module.name for module in pkgutil.iter_modules(sorted(search_paths)))
    return names


def canonical_distribution(value: str) -> str:
    return re.sub(r"[-_.]+", "-", str(value or "").strip()).lower()


def declared_distributions() -> set[str]:
    declared = set()
    for raw_line in REQUIREMENTS_PATH.read_text(encoding="utf-8").splitlines():
        line = raw_line.split("#", 1)[0].strip()
        if not line or line.startswith(("-r", "--requirement", "-e", "--editable")):
            continue
        name = re.split(r"[<>=!~;\[]", line, maxsplit=1)[0].strip()
        if name:
            declared.add(canonical_distribution(name))
    return declared


class RequirementsCoverageTests(unittest.TestCase):
    def test_all_host_third_party_imports_are_declared(self):
        source = SOURCE_PATH.read_text(encoding="utf-8")
        tree = ast.parse(source)
        imported = set(DYNAMIC_RUNTIME_MODULES)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.update(alias.name.split(".", 1)[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module.split(".", 1)[0])

        third_party = imported - stdlib_module_names() - {"__future__"}
        unmapped = sorted(third_party - set(IMPORT_TO_DISTRIBUTION))
        self.assertEqual(unmapped, [], f"Map new third-party imports: {unmapped}")

        declared = declared_distributions()
        missing = sorted(
            distribution
            for module, distribution in IMPORT_TO_DISTRIBUTION.items()
            if module in third_party
            and canonical_distribution(distribution) not in declared
        )
        self.assertEqual(
            missing, [], f"Add host dependencies to requirements.txt: {missing}"
        )

    def test_debug_adapter_dependency_is_explicit(self):
        source = SOURCE_PATH.read_text(encoding="utf-8")
        self.assertIn('find_spec("debugpy")', source)
        self.assertIn(canonical_distribution("debugpy"), declared_distributions())

    @staticmethod
    def conversation_session():
        session = cc.SessionState.__new__(cc.SessionState)
        session.snapshot = lambda: {
            "id": "dependency-test",
            "title": "依赖回退验证",
            "model": "test-model",
            "conversation_feed": [
                {"role": "user", "ts": 0, "text": "中文与 English 均应可见。"},
                {
                    "role": "assistant",
                    "ts": 0,
                    "text": "Pillow fallback rendered successfully.",
                },
            ],
        }
        return session

    def test_conversation_png_uses_pillow_without_external_browser_binaries(self):
        try:
            from PIL import Image
        except ImportError:
            self.skipTest("Pillow is not installed")

        real_import = builtins.__import__

        def import_without_external_renderers(name, *args, **kwargs):
            if name.startswith("playwright") or name == "imgkit":
                raise ImportError(name)
            return real_import(name, *args, **kwargs)

        with patch(
            "builtins.__import__", side_effect=import_without_external_renderers
        ):
            data = self.conversation_session().export_conversation_image()

        image = Image.open(BytesIO(data))
        self.assertEqual(image.format, "PNG")
        self.assertGreaterEqual(image.width, 800)
        self.assertGreaterEqual(image.height, 180)

    def test_conversation_png_endpoint_stays_valid_without_any_image_package(self):
        real_import = builtins.__import__

        def import_without_renderers(name, *args, **kwargs):
            if name.startswith("playwright") or name in {"imgkit", "PIL"}:
                raise ImportError(name)
            return real_import(name, *args, **kwargs)

        with patch("builtins.__import__", side_effect=import_without_renderers):
            data = self.conversation_session().export_conversation_image()

        self.assertTrue(data.startswith(b"\x89PNG\r\n\x1a\n"))


if __name__ == "__main__":
    unittest.main()
