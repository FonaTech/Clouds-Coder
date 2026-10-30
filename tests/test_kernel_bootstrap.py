"""A single-file checkout must collect kernel-first tests without local state."""
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class SingleFileKernelCollectionTests(unittest.TestCase):
    def test_reported_regressions_run_without_tools_or_fixture_directories(self):
        with tempfile.TemporaryDirectory(prefix='ci-no-extras-中文-') as directory:
            checkout = Path(directory)
            (checkout/'tests').mkdir()
            shutil.copy2(ROOT/'Clouds_Coder.py', checkout/'Clouds_Coder.py')
            shutil.copy2(ROOT/'pyproject.toml', checkout/'pyproject.toml')
            for name in ('conftest.py', 'test_agentic_evolution.py',
                         'test_screenshot_regressions.py', 'test_skill_selection.py'):
                shutil.copy2(ROOT/'tests'/name, checkout/'tests'/name)
            for relative in ('tools', 'tests/fixtures', 'skills', 'liquid_kernel'):
                self.assertFalse((checkout/relative).exists(), relative)
            env = {**os.environ, 'PYTHONIOENCODING': 'utf-8', 'PYTHONUTF8': '1'}
            env.pop('PYTHONPATH', None)
            result = subprocess.run(
                [sys.executable, '-I', '-c', 'import pytest,sys; sys.exit(pytest.main(sys.argv[1:]))',
                 '-q',
                 'tests/test_screenshot_regressions.py::ScreenshotRegressionTests::test_bundle_sync_reads_and_writes_utf8_under_gbk_defaults',
                 'tests/test_skill_selection.py::SkillSelectionTests::test_cfd_metadata_recalls_shader_dev_without_loading_body'],
                cwd=checkout, env=env, capture_output=True, text=True,
                encoding='utf-8', errors='replace', timeout=120,
            )
            self.assertEqual(result.returncode, 0, result.stdout+result.stderr)
            self.assertIn('2 passed', result.stdout)
            self.assertFalse((checkout/'tools').exists())
            self.assertFalse((checkout/'tests/fixtures').exists())

    def test_kernel_first_collection_bootstraps_a_clean_checkout(self):
        for project_config in (True, False):
            with self.subTest(pyproject_pytest_config=project_config), tempfile.TemporaryDirectory(prefix='kernel-中文-') as directory:
                checkout = Path(directory)
                (checkout/'tests').mkdir()
                shutil.copy2(ROOT/'Clouds_Coder.py', checkout/'Clouds_Coder.py')
                for name in ('conftest.py', 'test_acceptance_portability.py', 'test_agentic_evolution.py'):
                    shutil.copy2(ROOT/'tests'/name, checkout/'tests'/name)
                if project_config:
                    shutil.copy2(ROOT/'pyproject.toml', checkout/'pyproject.toml')
                else:
                    (checkout/'pyproject.toml').write_text('[tool.ruff]\n', encoding='utf-8')
                self.assertFalse((checkout/'liquid_kernel').exists())
                self.assertFalse((checkout/'pytest.ini').exists())
                env = {**os.environ, 'PYTHONIOENCODING': 'utf-8', 'PYTHONUTF8': '1'}
                env.pop('PYTHONPATH', None)
                # Isolated Python has no checkout path: this also covers the
                # console-script pytest path, not only `python -m pytest`.
                result = subprocess.run(
                    [sys.executable, '-I', '-c', 'import pytest,sys; sys.exit(pytest.main(sys.argv[1:]))',
                     '--collect-only', '-q', 'tests/test_acceptance_portability.py'],
                    cwd=checkout, env=env, capture_output=True, text=True,
                    encoding='utf-8', errors='replace', timeout=120,
                )
                self.assertEqual(result.returncode, 0, result.stdout+result.stderr)
                self.assertIn('test_windows_runtime_hints', result.stdout)
                for name in ('__init__.py', 'agentic.py', 'control.py', 'context.py', 'execution.py'):
                    self.assertTrue((checkout/'liquid_kernel'/name).is_file(), name)
