#!/usr/bin/env python3
"""
split_coder.py — Architecture-aware Python file splitter with incremental update support.

Analyzes a large monolithic Python file using AST, automatically identifies
architectural components, and splits it into a proper Python package structure.

Usage:
    python split_coder.py <source.py>
    python split_coder.py <source.py> --output-dir ./my_package
    python split_coder.py <source.py> --dry-run          # preview without writing
    python split_coder.py <source.py> --update            # incremental update
    python split_coder.py <source.py> --show-tree         # print tree after split
    python split_coder.py <source.py> --dump-layout       # print detected layout as JSON
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import py_compile
import re
import shutil
import subprocess
import symtable
import sys
import textwrap
import unicodedata
from collections import defaultdict
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple


# ─── Data Structures ─────────────────────────────────────────────────────────

@dataclass
class NodeInfo:
    """Metadata for one top-level AST node."""
    name: str                     # Symbol name (class/function name, or synthetic expression label)
    kind: str                     # "class" | "function" | "constant" | "assignment" | "expression" | "other"
    lineno: int                   # Start line (1-based)
    end_lineno: int               # End line (1-based)
    source_hash: str = ""         # SHA256 of the source lines
    target_module: str = ""       # Output module path (relative to package root)
    bases: List[str] = field(default_factory=list)  # For classes: base class names


@dataclass
class ManifestEntry:
    """Per-node record stored in the manifest."""
    name: str
    kind: str
    lineno: int
    end_lineno: int
    source_hash: str
    target_module: str


@dataclass
class SplitManifest:
    """Tracks the state of a split for incremental updates."""
    source_path: str
    source_hash: str
    output_dir: str
    package_name: str
    nodes: List[ManifestEntry] = field(default_factory=list)
    layout_config: str = ""       # Path to custom layout config, if any

    FILENAME = ".split_manifest.json"

    def save(self, output_dir: Path) -> None:
        path = output_dir / self.FILENAME
        path.write_text(json.dumps(asdict(self), indent=2), encoding="utf-8")

    @classmethod
    def load(cls, output_dir: Path) -> Optional["SplitManifest"]:
        path = output_dir / cls.FILENAME
        if not path.exists():
            return None
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            data["nodes"] = [ManifestEntry(**n) for n in data.get("nodes", [])]
            return cls(**data)
        except Exception:
            return None


@dataclass(frozen=True)
class ImportAlias:
    """One imported alias from an import statement."""

    name: str
    asname: Optional[str] = None

    @property
    def bound_name(self) -> str:
        return self.asname or self.name.split(".")[0]

    def render(self) -> str:
        if self.asname:
            return f"{self.name} as {self.asname}"
        return self.name


@dataclass
class ImportStatement:
    """Metadata for one top-level import statement or try-import block."""

    kind: str
    lineno: int
    end_lineno: int
    aliases: List[ImportAlias] = field(default_factory=list)
    module: Optional[str] = None
    level: int = 0
    source: str = ""
    bound_names: Set[str] = field(default_factory=set)
    always_include: bool = False


# ─── Default Layout Rules ────────────────────────────────────────────────────
#
# Each key is a relative module path within the output package.
# Values are lists of symbol names or regex patterns (prefix with "~").
#
# The layout is tried in order; the FIRST match wins.
# Special rules:
#   "~^[A-Z][A-Z0-9_]{3,}$"  → matches ALL_CAPS constants
#   "_unclassified.py"        → fallback for unmatched symbols

DEFAULT_LAYOUT: Dict[str, List[str]] = {
    # ── Package root ──────────────────────────────────────────────────────
    "__init__.py": [],
    "__main__.py": ["main", "~^_main_guard_"],

    # ── Configuration & constants ─────────────────────────────────────────
    "config/__init__.py": [],
    "config/constants.py": [
        # UPPER_CASE constants
        "~^[A-Z][A-Z0-9_]{3,}$",
        "APP_VERSION",
        "_TOOL_TIMEOUT_MAP",
        "_DEFAULT_TOOL_TIMEOUT",
        "RUNTIME_CONTROL_HINT_PREFIXES",
        "RETRY_RUNTIME_HINT_PREFIXES",
    ],
    "config/paths.py": [
        "_resolve_default_agent_workdir", "_migrate_legacy_runtime_roots",
        "WORKDIR", "CODES_ROOT", "LLM_CONFIG_PATH", "SCRIPT_DIR",
        "REPO_ROOT", "detect_repo_root",
    ],
    "config/settings.py": [
        "normalize_ui_language", "normalize_ui_style", "supported_ui_languages_payload",
        "backend_i18n_text", "backend_role_label",
        "infer_user_complexity_value", "normalize_task_complexity",
        "task_complexity_rank", "task_complexity_at_least", "max_task_complexity",
        "normalize_execution_mode", "model_language_instruction", "_detect_os_shell_instruction",
        "resolve_web_ui_dir_path", "resolve_optional_file_path", "resolve_skills_root_path",
        "_count_skill_markdown_files", "select_preferred_skills_root",
        "load_web_ui_config_file", "extract_show_upload_list_setting",
        "extract_ui_style_setting", "default_multimodal_capabilities", "_to_bool_like",
        "infer_model_multimodal_capabilities", "parse_capability_overrides",
        "merge_multimodal_capabilities", "parse_media_endpoints",
        "load_llm_config_from_source", "~^load_llm_config",
        "looks_like_llm_config", "parse_llm_config_profiles",
    ],

    # ── Utilities ─────────────────────────────────────────────────────────
    "utils/__init__.py": [],
    "utils/errors.py": [
        "EmptyActionError", "CircuitBreakerTriggered", "~Error$", "~Exception$",
    ],
    "utils/text.py": [
        "MAX_TOOL_OUTPUT", "SOCKET_NOISE_LINE_PATTERNS",
        "trim", "_fmt_export_ts", "_html_esc", "_text_to_minimal_pdf",
        "normalize_embedded_newlines", "_map_todo_status_token",
        "split_todo_status_text", "extract_todo_rows_from_text",
        "infer_todo_status_from_text", "split_structured_todo_content",
        "normalize_work_text", "filter_runtime_noise_lines",
        "parse_front_matter", "make_numbered_diff", "make_unified_diff", "render_numbered_diff_text",
        "_compress_rows_keep_hotspot", "_hotspot_index", "_row_is_hot", "_skip_row",
    ],
    "utils/http.py": [
        "_URL_OPEN_ORIGINAL",
        "_HTTP_SSL_CONTEXT",
        "_shared_http_ssl_context",
        "urlopen",
    ],
    "utils/media.py": [
        "guess_mime_from_name", "_convert_image_to_safe_format", "guess_ext_from_mime",
    ],
    "utils/compress.py": ["compress_text_blob", "decompress_text_blob"],
    "utils/json_utils.py": [
        "JSON_FSYNC_ENABLED",
        "json_dumps", "parse_json_object", "extract_json_object_from_text",
        "repair_truncated_json_object", "parse_tool_arguments", "parse_tool_arguments_with_error",
        "_json_default_copy", "_read_json_file", "_write_json_file",
        "tool_def", "canonicalize_tool_name",
        "TOOLS", "TOOL_REQUIRED_ARGS", "TOOL_SPEC_BY_NAME", "TOOL_NAME_FUZZY_MAP",
    ],
    "utils/files.py": [
        "safe_path", "_safe_js_filename", "_sha256_bytes", "_sha256_file",
        "_normalize_js_lib_asset_ref", "_resolve_js_lib_asset_path",
        "_discover_extra_js_lib_files", "_download_http_bytes",
        "_offline_js_entry_relative_path", "_archive_member_relative_path",
        "_path_size_bytes", "_extract_archive_to_dir",
        "_package_required_paths", "_package_install_ready",
        "_postprocess_offline_js_package", "_ensure_offline_js_package",
        "offline_js_lib_root", "_render_offline_js_catalog_md",
        "load_offline_js_lib_index", "ensure_offline_js_libs",
        "_normalize_external_js_url", "is_external_js_src",
        "match_offline_js_catalog_by_url", "cache_external_js_url",
        "try_read_text",
    ],
    "utils/misc.py": [
        "DEFAULT_TIMEOUT_SECONDS", "MIN_TIMEOUT_SECONDS", "MAX_TIMEOUT_SECONDS",
        "BENIGN_SOCKET_DEBUG_LOG_ENABLED", "BENIGN_SOCKET_LOG_INTERVAL_SECONDS",
        "now_ts", "make_id", "sanitize_profile_id", "detect_repo_root",
        "detect_local_lan_ip", "is_benign_socket_error", "_socket_error_code",
        "_log_benign_socket_error_limited", "swallow_benign_socket_error",
        "normalize_timeout_seconds", "BENIGN_SOCKET_DEBUG_LOG_ENABLED",
        "BENIGN_SOCKET_LOG_INTERVAL_SECONDS",
        "_benign_socket_log_lock", "_benign_socket_log_state",
        "_module_exists", "_meta_string_list", "user_id_from_ip",
    ],
    "utils/crypto.py": ["CryptoBox"],

    # ── LLM / Ollama ──────────────────────────────────────────────────────
    "llm/__init__.py": [],
    "llm/client.py": ["OllamaError", "OllamaClient"],
    "llm/utils.py": [
        "probe_ollama_environment", "list_ollama_models", "list_ollama_models_cached",
        "resolve_ollama_model", "infer_thinking_model", "split_thinking_content",
        "strip_thinking_content", "check_ollama_model_ready", "list_loaded_ollama_models",
        "wake_ollama_model", "try_pull_ollama_model", "ordered_model_candidates",
        "pick_working_ollama_model", "extract_base_url", "complete_chat_endpoint",
        "normalize_openai_compat_provider_name", "is_openai_compat_provider",
        "is_openai_like_provider", "openai_compat_probe_headers",
        "openai_compat_model_list_urls", "extract_openai_compat_model_ids",
        "_is_http_url", "_resolve_local_path",
        "_OLLAMA_TAG_CACHE", "_OLLAMA_TAG_CACHE_LOCK",
    ],

    # ── Agent subsystems ──────────────────────────────────────────────────
    "agent/__init__.py": [],
    "agent/events.py": ["EventHub"],
    "agent/todo.py": ["TodoManager"],
    "agent/tasks.py": ["TaskManager"],
    "agent/background.py": ["BackgroundManager"],
    "agent/bus.py": ["MessageBus"],
    "agent/worktree.py": ["WorktreeManager"],

    # ── Skills ────────────────────────────────────────────────────────────
    "skills/__init__.py": [],
    "skills/store.py": [
        "SkillStore",
        "_BUILTIN_SKILLS",
        "_build_skills_gen_skill_content",
        "_sanitize_skill_slug",
        "_skill_knowledge_files",
        "analyze_skill_building_knowledge",
        "ensure_embedded_clawhub_skills",
        "ensure_embedded_skills",
        "ensure_embedded_skills_at_root",
        "detect_upload_parser_capabilities",
        "_render_cap_markdown",
        "ensure_runtime_skills",
        "~^ensure_generated_",
        "~^_write_text_if_changed",
    ],

    # ── Session ───────────────────────────────────────────────────────────
    "session/__init__.py": [],
    "session/state.py": ["SessionState"],
    "session/manager.py": ["SessionManager"],

    # ── RAG / Knowledge ───────────────────────────────────────────────────
    "rag/__init__.py": [],
    "rag/parsers.py": [
        "CodeContentParser", "RAGContentParser",
        "_rag_safe_name", "_rag_detect_language", "_rag_cjk_ngrams", "_rag_is_noise_token",
        "_rag_entity_allowed", "_rag_filter_entities", "_rag_filename_entity_aliases",
        "_rag_apply_filename_entity_policy", "_rag_choose_community", "_rag_tokenize",
        "_rag_expand_tokens", "_rag_extract_entities", "_rag_classify_document", "_rag_chunk_text",
        "_code_language_from_name", "_code_is_test_path",
        "build_code_preview_rows", "is_code_preview_candidate",
        "normalize_rel_preview_path", "preview_kind_for_path",
    ],
    "rag/index.py": [
        "TFGraphIDFIndex", "CodeGraphIndex",
        "_code_choose_community", "_code_is_test_path", "_code_language_from_name",
        "_code_module_name", "_code_query_terms",
    ],
    "rag/store.py": ["RAGLibraryStore", "CodeLibraryStore"],
    "rag/ingestion.py": [
        "RAGIngestionService", "CodeIngestionService",
        "~^_rag_",
    ],

    # ── App ───────────────────────────────────────────────────────────────
    "app/__init__.py": [],
    "app/context.py": ["AppContext"],

    # ── HTTP Server ───────────────────────────────────────────────────────
    "server/__init__.py": [],
    "server/handlers.py": [
        "AgentHTTPServer", "Handler", "SkillsHandler",
        "RagAdminHandler", "CodeAdminHandler", "user_id_from_ip",
    ],

    # ── Catch-all ─────────────────────────────────────────────────────────
    "_unclassified.py": [],
}


# ─── Architecture Analyzer ───────────────────────────────────────────────────

class ArchitectureAnalyzer:
    """Parses the source file with AST and extracts top-level node metadata."""

    def __init__(self, source_path: Path) -> None:
        self.source_path = source_path
        self.source_lines: List[str] = []
        self.tree: ast.Module | None = None
        self.nodes: List[NodeInfo] = []
        self.import_statements: List[ImportStatement] = []

    def analyze(self) -> List[NodeInfo]:
        """Parse and classify all top-level nodes."""
        text = self.source_path.read_text(encoding="utf-8")
        self.source_lines = text.splitlines(keepends=True)
        print(f"  Parsing {len(self.source_lines):,} lines with AST...")
        self.tree = ast.parse(text, filename=str(self.source_path))
        self.nodes = []
        self.import_statements = []

        for node in self.tree.body:
            self._register_top_level_import(node)
            infos = self._extract_node_info(node)
            self.nodes.extend(infos)

        return self.nodes

    def _extract_node_info(self, node: ast.AST) -> List[NodeInfo]:
        """Convert one AST body node into NodeInfo records."""
        results: List[NodeInfo] = []

        if isinstance(node, (ast.ClassDef,)):
            bases = [self._name_of(b) for b in node.bases]
            info = NodeInfo(
                name=node.name,
                kind="class",
                lineno=node.lineno,
                end_lineno=node.end_lineno or node.lineno,
                bases=bases,
            )
            info.source_hash = self._hash_lines(info.lineno, info.end_lineno)
            results.append(info)

        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            info = NodeInfo(
                name=node.name,
                kind="function",
                lineno=node.lineno,
                end_lineno=node.end_lineno or node.lineno,
            )
            info.source_hash = self._hash_lines(info.lineno, info.end_lineno)
            results.append(info)

        elif isinstance(node, ast.Assign):
            # Capture top-level assignments (constants, config dicts, etc.)
            for target in node.targets:
                name = self._name_of(target)
                if name:
                    end = node.end_lineno or node.lineno
                    kind = "constant" if re.match(r"^[A-Z][A-Z0-9_]{2,}$", name) else "assignment"
                    info = NodeInfo(
                        name=name,
                        kind=kind,
                        lineno=node.lineno,
                        end_lineno=end,
                    )
                    info.source_hash = self._hash_lines(info.lineno, info.end_lineno)
                    results.append(info)

        elif isinstance(node, ast.AnnAssign):
            name = self._name_of(node.target)
            if name:
                end = node.end_lineno or node.lineno
                kind = "constant" if re.match(r"^[A-Z][A-Z0-9_]{2,}$", name) else "assignment"
                info = NodeInfo(
                    name=name,
                    kind=kind,
                    lineno=node.lineno,
                    end_lineno=end,
                )
                info.source_hash = self._hash_lines(info.lineno, info.end_lineno)
                results.append(info)

        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            # Track the first import block as a special node
            info = NodeInfo(
                name=f"_import_{node.lineno}",
                kind="import",
                lineno=node.lineno,
                end_lineno=node.end_lineno or node.lineno,
            )
            info.source_hash = self._hash_lines(info.lineno, info.end_lineno)
            results.append(info)

        elif isinstance(node, ast.If):
            # Handle `if __name__ == "__main__":` blocks
            if self._is_main_guard(node):
                info = NodeInfo(
                    name=f"_main_guard_{node.lineno}",
                    kind="main_guard",
                    lineno=node.lineno,
                    end_lineno=node.end_lineno or node.lineno,
                )
                info.source_hash = self._hash_lines(info.lineno, info.end_lineno)
                results.append(info)

        elif isinstance(node, ast.Expr):
            # Top-level expression statements: dict updates, docstrings, registry calls, etc.
            end = node.end_lineno or node.lineno
            info = NodeInfo(
                name=self._expression_node_name(node),
                kind="expression",
                lineno=node.lineno,
                end_lineno=end,
            )
            info.source_hash = self._hash_lines(info.lineno, info.end_lineno)
            results.append(info)

        elif isinstance(node, ast.Try):
            # top-level try (e.g. `try: import yaml`)
            end = node.end_lineno or node.lineno
            # Collect names assigned in except handlers
            names = []
            for handler in node.handlers:
                if handler.name:
                    names.append(handler.name)
            for child in ast.walk(node):
                if isinstance(child, (ast.Import, ast.ImportFrom)):
                    for alias in child.names:
                        names.append(alias.asname or alias.name.split(".")[0])
            name = "_try_import_" + "_".join(names) if names else f"_try_{node.lineno}"
            info = NodeInfo(
                name=name,
                kind="import",
                lineno=node.lineno,
                end_lineno=end,
            )
            info.source_hash = self._hash_lines(info.lineno, info.end_lineno)
            results.append(info)

        return results

    @staticmethod
    def _name_of(node: ast.AST) -> str:
        if isinstance(node, ast.Name):
            return node.id
        if isinstance(node, ast.Attribute):
            return node.attr
        return ""

    def _expression_node_name(self, node: ast.Expr) -> str:
        base = self._expression_anchor_label(node)
        return f"{base}_l{node.lineno}"

    def _expression_anchor_label(self, node: ast.Expr) -> str:
        value = node.value
        if (
            self.tree is not None
            and self.tree.body
            and self.tree.body[0] is node
            and isinstance(value, ast.Constant)
            and isinstance(value.value, str)
        ):
            return "module_docstring"
        if isinstance(value, ast.Call):
            tokens = self._anchor_tokens(value.func)
            return "call_" + "_".join(tokens or ["anonymous"])
        if isinstance(value, ast.Constant):
            return self._literal_expression_label(value.value)
        if isinstance(value, ast.Dict):
            return "dict_literal"
        if isinstance(value, ast.List):
            return "list_literal"
        if isinstance(value, ast.Tuple):
            return "tuple_literal"
        if isinstance(value, ast.Set):
            return "set_literal"
        if isinstance(value, ast.JoinedStr):
            return "formatted_string"
        if isinstance(value, ast.Compare):
            return "comparison"
        if isinstance(value, ast.BoolOp):
            return "boolean_operation"
        if isinstance(value, ast.BinOp):
            return "binary_operation"
        if isinstance(value, ast.UnaryOp):
            return "unary_operation"
        return f"{self._slugify_fragment(type(value).__name__) or 'value'}_expression"

    def _anchor_tokens(self, node: ast.AST, depth: int = 0) -> List[str]:
        if depth > 6:
            return []
        if isinstance(node, ast.Name):
            token = self._slugify_fragment(node.id)
            return [token] if token else []
        if isinstance(node, ast.Attribute):
            return self._merge_anchor_tokens(
                self._anchor_tokens(node.value, depth + 1),
                self._slugify_fragment(node.attr),
            )
        if isinstance(node, ast.Subscript):
            return self._merge_anchor_tokens(
                self._anchor_tokens(node.value, depth + 1),
                self._anchor_tokens(node.slice, depth + 1),
            )
        if isinstance(node, ast.Call):
            return self._merge_anchor_tokens(self._anchor_tokens(node.func, depth + 1), "result")
        if isinstance(node, ast.Constant):
            token = self._constant_anchor_token(node.value)
            return [token] if token else []
        if isinstance(node, (ast.Tuple, ast.List)):
            tokens: List[str] = []
            for elt in node.elts[:2]:
                tokens = self._merge_anchor_tokens(tokens, self._anchor_tokens(elt, depth + 1))
            return tokens
        if isinstance(node, ast.Dict):
            return ["dict"]
        if isinstance(node, ast.Slice):
            return ["slice"]
        return []

    @staticmethod
    def _merge_anchor_tokens(*parts: object) -> List[str]:
        merged: List[str] = []
        for part in parts:
            if not part:
                continue
            if isinstance(part, list):
                items = part
            else:
                items = [part]
            for item in items:
                token = str(item or "").strip("_")
                if not token:
                    continue
                if merged and merged[-1] == token:
                    continue
                merged.append(token)
                if len(merged) >= 6:
                    return merged
        return merged

    @staticmethod
    def _literal_expression_label(value: object) -> str:
        if isinstance(value, str):
            return "string_literal"
        if isinstance(value, bytes):
            return "bytes_literal"
        if isinstance(value, bool):
            return "boolean_literal"
        if isinstance(value, (int, float, complex)):
            return "numeric_literal"
        if value is None:
            return "none_literal"
        return "literal_value"

    def _constant_anchor_token(self, value: object) -> str:
        if isinstance(value, str):
            token = self._slugify_fragment(value)
            return token if token and token != "value" else "string"
        if isinstance(value, bytes):
            return "bytes"
        if isinstance(value, bool):
            return "true" if value else "false"
        if isinstance(value, (int, float)):
            return self._slugify_fragment(value)
        if value is None:
            return "none"
        return self._slugify_fragment(type(value).__name__) or "value"

    @staticmethod
    def _slugify_fragment(value: object) -> str:
        text = str(value or "").strip()
        if not text:
            return ""
        normalized = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
        normalized = normalized.lower()
        normalized = re.sub(r"[^a-z0-9_]+", "_", normalized)
        normalized = re.sub(r"_+", "_", normalized).strip("_")
        if not normalized:
            digest = hashlib.sha1(text.encode("utf-8")).hexdigest()[:8]
            return f"u_{digest}"
        if normalized[0].isdigit():
            normalized = f"n_{normalized}"
        return normalized[:48]

    @staticmethod
    def _is_main_guard(node: ast.If) -> bool:
        test = node.test
        if isinstance(test, ast.Compare):
            if (isinstance(test.left, ast.Name) and test.left.id == "__name__"
                    and len(test.ops) == 1 and isinstance(test.ops[0], ast.Eq)
                    and len(test.comparators) == 1
                    and isinstance(test.comparators[0], ast.Constant)
                    and test.comparators[0].value == "__main__"):
                return True
        return False

    def _hash_lines(self, start: int, end: int) -> str:
        chunk = "".join(self.source_lines[start - 1:end])
        return hashlib.sha256(chunk.encode()).hexdigest()[:16]

    def get_source_lines(self, start: int, end: int) -> str:
        """Extract source lines (1-based, inclusive)."""
        return "".join(self.source_lines[start - 1:end])

    def get_all_import_lines(self) -> str:
        """Return all top-level import statements as a block."""
        lines = []
        for node in self.nodes:
            if node.kind == "import":
                lines.append(self.get_source_lines(node.lineno, node.end_lineno))
        return "\n".join(lines)

    def select_import_lines(self, referenced_names: Set[str]) -> List[str]:
        """Return only the import lines required by the given referenced names."""
        lines: List[str] = []
        for stmt in self.import_statements:
            if stmt.always_include:
                lines.append(self._render_import_statement(stmt))
                continue

            if stmt.kind == "try":
                if stmt.bound_names & referenced_names:
                    lines.append(stmt.source.rstrip("\n"))
                continue

            aliases = [alias for alias in stmt.aliases if alias.bound_name in referenced_names]
            if aliases:
                lines.append(self._render_import_statement(stmt, aliases))
        return lines

    def _register_top_level_import(self, node: ast.AST) -> None:
        if isinstance(node, ast.Import):
            aliases = [ImportAlias(alias.name, alias.asname) for alias in node.names]
            self.import_statements.append(
                ImportStatement(
                    kind="import",
                    lineno=node.lineno,
                    end_lineno=node.end_lineno or node.lineno,
                    aliases=aliases,
                    source=self.get_source_lines(node.lineno, node.end_lineno or node.lineno),
                    bound_names={alias.bound_name for alias in aliases},
                )
            )
            return

        if isinstance(node, ast.ImportFrom):
            aliases = [ImportAlias(alias.name, alias.asname) for alias in node.names]
            self.import_statements.append(
                ImportStatement(
                    kind="from",
                    lineno=node.lineno,
                    end_lineno=node.end_lineno or node.lineno,
                    aliases=aliases,
                    module=node.module,
                    level=node.level,
                    source=self.get_source_lines(node.lineno, node.end_lineno or node.lineno),
                    bound_names={alias.bound_name for alias in aliases},
                    always_include=node.module == "__future__",
                )
            )
            return

        if isinstance(node, ast.Try):
            bound_names: Set[str] = set()
            for child in ast.walk(node):
                if isinstance(child, (ast.Import, ast.ImportFrom)):
                    for alias in child.names:
                        bound_names.add(alias.asname or alias.name.split(".")[0])
            if bound_names:
                self.import_statements.append(
                    ImportStatement(
                        kind="try",
                        lineno=node.lineno,
                        end_lineno=node.end_lineno or node.lineno,
                        source=self.get_source_lines(node.lineno, node.end_lineno or node.lineno),
                        bound_names=bound_names,
                    )
                )

    @staticmethod
    def _render_import_statement(
        stmt: ImportStatement,
        aliases: Optional[List[ImportAlias]] = None,
    ) -> str:
        selected = aliases or stmt.aliases
        if stmt.kind == "import":
            return "import " + ", ".join(alias.render() for alias in selected)
        if stmt.kind == "from":
            dots = "." * stmt.level
            module = stmt.module or ""
            origin = f"{dots}{module}" if module else dots
            return f"from {origin} import " + ", ".join(alias.render() for alias in selected)
        return stmt.source.rstrip("\n")


# ─── Module Router ────────────────────────────────────────────────────────────

class ModuleRouter:
    """Routes each NodeInfo to an output module path using layout rules."""

    def __init__(self, layout: Dict[str, List[str]]) -> None:
        self.layout = layout
        self._fallback_classifier = AutoLayoutGenerator()
        # Pre-compile: list of (module_path, list_of_matchers)
        self._rules: List[Tuple[str, List[Tuple[str, object]]]] = []
        for mod_path, patterns in layout.items():
            matchers: List[Tuple[str, object]] = []
            for pat in patterns:
                if pat.startswith("~"):
                    matchers.append(("regex", re.compile(pat[1:])))
                else:
                    matchers.append(("exact", pat))
            self._rules.append((mod_path, matchers))

    def route(self, node: NodeInfo) -> str:
        """Return the target module path for a node."""
        # Import nodes always go to a special _imports collector
        if node.kind == "import":
            return "_imports"

        name = node.name
        for mod_path, matchers in self._rules:
            for kind, matcher in matchers:
                if kind == "exact" and name == matcher:
                    return mod_path

        # Broad regex buckets only apply after exact-name routing.
        for mod_path, matchers in self._rules:
            if not matchers:
                continue
            for kind, matcher in matchers:
                if kind == "regex" and matcher.search(name):
                    return mod_path

        fallback_module = self._fallback_classifier._classify(node)
        if fallback_module != "_unclassified.py":
            return fallback_module

        return "_unclassified.py"

    def assign_all(self, nodes: List[NodeInfo]) -> None:
        """Assign target_module to all nodes in-place."""
        for node in nodes:
            node.target_module = self.route(node)
        self._adopt_contextual_expression_nodes(nodes)

    def _adopt_contextual_expression_nodes(self, nodes: List[NodeInfo]) -> None:
        """Attach anonymous top-level expressions to the nearest classified neighbor."""
        for index, node in enumerate(nodes):
            if node.target_module != "_unclassified.py":
                continue
            if node.kind != "expression":
                continue
            contextual_module = self._nearest_contextual_module(nodes, index)
            if contextual_module:
                node.target_module = contextual_module

    def _nearest_contextual_module(self, nodes: List[NodeInfo], index: int) -> str:
        current = nodes[index]
        prev_node = self._nearest_classified_neighbor(nodes, index, -1)
        next_node = self._nearest_classified_neighbor(nodes, index, 1)

        if prev_node and next_node and prev_node.target_module == next_node.target_module:
            return prev_node.target_module

        candidates: List[Tuple[int, int, str]] = []
        if prev_node and prev_node.target_module:
            gap = max(0, current.lineno - prev_node.end_lineno)
            candidates.append((gap, 0, prev_node.target_module))
        if next_node and next_node.target_module:
            gap = max(0, next_node.lineno - current.end_lineno)
            candidates.append((gap, 1, next_node.target_module))
        if not candidates:
            return ""

        candidates.sort()
        closest_gap, _, module = candidates[0]
        return module if closest_gap <= 240 or len(candidates) == 1 else ""

    @staticmethod
    def _nearest_classified_neighbor(
        nodes: List[NodeInfo],
        index: int,
        direction: int,
    ) -> Optional[NodeInfo]:
        cursor = index + direction
        while 0 <= cursor < len(nodes):
            candidate = nodes[cursor]
            if candidate.kind == "import":
                cursor += direction
                continue
            if candidate.target_module and candidate.target_module != "_unclassified.py":
                return candidate
            cursor += direction
        return None


# ─── Dependency Analyzer ──────────────────────────────────────────────────────

class DependencyAnalyzer:
    """Analyzes cross-module name dependencies with scope awareness."""

    def __init__(self, analyzer: ArchitectureAnalyzer, nodes: List[NodeInfo]) -> None:
        self.analyzer = analyzer
        self.nodes = nodes
        # Build symbol → module map (only non-import nodes)
        self.symbol_to_module: Dict[str, str] = {}
        for n in nodes:
            if n.kind not in ("import",) and not n.name.startswith("_import_") and not n.name.startswith("_try_"):
                self.symbol_to_module[n.name] = n.target_module

    def compute_dependency_map(self, module_path: str, module_nodes: List[NodeInfo]) -> Dict[str, Set[str]]:
        """Return dependency module -> symbols for one generated module."""
        deps: Dict[str, Set[str]] = defaultdict(set)
        for node in module_nodes:
            if node.kind == "import":
                continue
            for name in self._node_referenced_symbols(node):
                source_mod = self.symbol_to_module.get(name)
                if source_mod and source_mod != module_path and source_mod != "_imports":
                    deps[source_mod].add(name)
        return deps

    def compute_imports(self, module_path: str, module_nodes: List[NodeInfo]) -> List[str]:
        """
        For a given output module, compute the correct relative `from .X import Y`
        statements needed to satisfy cross-module references.
        Returns sorted list of import lines.
        """
        deps = self.compute_dependency_map(module_path, module_nodes)

        import_lines = []
        for dep_mod, names in sorted(deps.items()):
            if not names:
                continue
            rel = self._relative_import(module_path, dep_mod)
            names_str = ", ".join(sorted(names))
            import_lines.append(f"from {rel} import {names_str}")

        return import_lines

    def compute_referenced_names(self, module_nodes: List[NodeInfo]) -> Set[str]:
        """Return all referenced names across nodes in one generated module."""
        referenced: Set[str] = set()
        for node in module_nodes:
            if node.kind == "import":
                continue
            referenced.update(self._node_referenced_symbols(node))
        return referenced

    def _node_referenced_symbols(self, node: NodeInfo) -> Set[str]:
        source = self.analyzer.get_source_lines(node.lineno, node.end_lineno)
        if not source.strip():
            return set()
        try:
            table = symtable.symtable(source, str(self.analyzer.source_path), "exec")
        except SyntaxError:
            return set()

        referenced: Set[str] = set()
        self._collect_referenced_symbols(table, referenced)
        return referenced

    def _collect_referenced_symbols(self, table: symtable.SymbolTable, out: Set[str]) -> None:
        table_type = table.get_type()
        for symbol in table.get_symbols():
            if not symbol.is_referenced() or symbol.is_imported() or symbol.is_parameter():
                continue
            if table_type == "module":
                out.add(symbol.get_name())
                continue
            if symbol.is_global() or symbol.is_free() or symbol.is_nonlocal():
                out.add(symbol.get_name())
        for child in table.get_children():
            self._collect_referenced_symbols(child, out)

    @staticmethod
    def _relative_import(current_module: str, dep_module: str) -> str:
        """
        Compute the correct relative import prefix.

        Examples:
          config/constants.py → config/paths.py   =>  .paths
          session/state.py    → agent/events.py   =>  ..agent.events
          rag/store.py        → config/constants.py => ..config.constants
        """
        cur_parts = current_module.replace(".py", "").split("/")
        dep_parts = dep_module.replace(".py", "").split("/")

        cur_pkg = cur_parts[:-1]   # directory parts only
        dep_pkg = dep_parts[:-1]
        dep_file = dep_parts[-1]

        # Find common ancestor package depth
        common = 0
        for a, b in zip(cur_pkg, dep_pkg):
            if a == b:
                common += 1
            else:
                break

        # Number of levels to go up from current package
        levels_up = len(cur_pkg) - common
        dots = "." * (levels_up + 1)   # "." = same pkg, ".." = parent, etc.

        remaining = dep_pkg[common:]
        if remaining:
            path = ".".join(remaining) + "." + dep_file
        else:
            path = dep_file

        return f"{dots}{path}"


# ─── Code Generator ───────────────────────────────────────────────────────────

class CodeGenerator:
    """Generates the content of each output module file."""

    HEADER_TEMPLATE = '''\
# Auto-generated by split_coder.py — do not edit manually.
# Re-run split_coder.py to regenerate.
'''

    def __init__(
        self,
        analyzer: ArchitectureAnalyzer,
        dep_analyzer: DependencyAnalyzer,
        package_name: str,
        source_path: str,
    ) -> None:
        self.analyzer = analyzer
        self.dep_analyzer = dep_analyzer
        self.package_name = package_name
        self.source_path = str(Path(source_path).resolve())
        self.source_dir = str(Path(self.source_path).parent.resolve())

    @staticmethod
    def _compact_imports(raw: str) -> str:
        """Strip blank lines between import statements."""
        out = []
        for line in raw.splitlines():
            stripped = line.rstrip()
            # Skip blank lines that appear between import lines
            if stripped == "" and out and out[-1].startswith(("import ", "from ")):
                continue
            out.append(stripped)
        # Also collapse consecutive blank lines at the end of the import block
        while out and out[-1] == "":
            out.pop()
        return "\n".join(out)

    def generate_module(
        self,
        module_path: str,
        module_nodes: List[NodeInfo],
    ) -> str:
        """Generate complete file content for one output module."""
        if module_path.endswith("__init__.py") and not module_nodes:
            return self._generate_init(module_path)

        parts: List[str] = []
        parts.append(self.HEADER_TEMPLATE)

        referenced_names = self.dep_analyzer.compute_referenced_names(module_nodes)
        dep_map = self.dep_analyzer.compute_dependency_map(module_path, module_nodes)
        cross_imported_names: Set[str] = set()
        for names in dep_map.values():
            cross_imported_names.update(names)
        import_lines = self.analyzer.select_import_lines(referenced_names - cross_imported_names)
        compact = self._compact_imports("\n".join(import_lines))
        if compact:
            parts.append(compact)
            parts.append("")

        # Cross-module imports
        cross_imports = []
        for dep_mod, names in sorted(dep_map.items()):
            if not names:
                continue
            rel = self.dep_analyzer._relative_import(module_path, dep_mod)
            names_str = ", ".join(sorted(names))
            cross_imports.append(f"from {rel} import {names_str}")
        if cross_imports:
            parts.append("# ── cross-module imports ─────────────────────────────────────────────────")
            parts.extend(cross_imports)
            parts.append("")

        # Actual code bodies
        for node in module_nodes:
            if node.kind == "import":
                continue
            src = self.analyzer.get_source_lines(node.lineno, node.end_lineno)
            src = self._rewrite_context_sensitive_source(node, src)
            parts.append(src)

        return "\n".join(parts) + "\n"

    def _generate_init(self, module_path: str) -> str:
        """Generate a minimal __init__.py."""
        pkg = module_path.replace("/__init__.py", "").replace("/", ".") or self.package_name
        return f"# {pkg}\n"

    def generate_root_init(self, all_modules: List[str]) -> str:
        sub_modules = sorted(
            m.split("/")[0]
            for m in all_modules
            if "/" in m and not m.startswith("_")
        )
        seen: Set[str] = set()
        unique = [x for x in sub_modules if not (x in seen or seen.add(x))]  # type: ignore
        lines = ["# Auto-generated package root.", ""]
        for mod in unique:
            lines.append(f"from . import {mod} as {mod}")
        return "\n".join(lines) + "\n"

    def _rewrite_context_sensitive_source(self, node: NodeInfo, src: str) -> str:
        """Patch a small set of known context-sensitive snippets after relocation."""
        if node.name == "SCRIPT_DIR" and "Path(__file__).resolve().parent" in src:
            return f"SCRIPT_DIR = Path({self.source_dir!r}).resolve()\n"
        if "Path(__file__).read_text(encoding=\"utf-8\")" in src:
            return src.replace(
                'Path(__file__).read_text(encoding="utf-8")',
                f'Path({self.source_path!r}).read_text(encoding="utf-8")',
            )
        return src


class FrameworkReportGenerator:
    """Builds a Markdown report describing the generated package framework."""

    def __init__(
        self,
        source_path: Path,
        output_dir: Path,
        modules: Dict[str, List[NodeInfo]],
        dep_analyzer: DependencyAnalyzer,
    ) -> None:
        self.source_path = source_path
        self.output_dir = output_dir
        self.modules = modules
        self.dep_analyzer = dep_analyzer

    def generate(self) -> str:
        module_paths = sorted(m for m in self.modules.keys() if m != "_imports")
        total_symbols = sum(
            1
            for nodes in self.modules.values()
            for node in nodes
            if node.kind != "import"
        )
        unclassified = [n for n in self.modules.get("_unclassified.py", []) if n.kind != "import"]

        lines: List[str] = [
            f"# {self.output_dir.name} Framework",
            "",
            "## Overview",
            "",
            f"- Source file: `{self.source_path}`",
            f"- Output directory: `{self.output_dir}`",
            f"- Generated modules: {len(module_paths)}",
            f"- Top-level symbols: {total_symbols}",
            f"- Entry point present: {'yes' if '__main__.py' in self.modules else 'no'}",
            f"- Unclassified symbols: {len(unclassified)}",
            "",
            "## Package Tree",
            "",
            "```text",
        ]
        lines.extend(self._tree_lines(module_paths))
        lines.extend([
            "```",
            "",
            "## Module Summary",
            "",
            "| Module | Symbols | Cross-module deps |",
            "| --- | ---: | --- |",
        ])

        for module_path in module_paths:
            module_nodes = [n for n in self.modules.get(module_path, []) if n.kind != "import"]
            deps = self.dep_analyzer.compute_dependency_map(module_path, module_nodes)
            dep_list = ", ".join(f"`{mod}`" for mod in sorted(deps.keys())) or "—"
            lines.append(f"| `{module_path}` | {len(module_nodes)} | {dep_list} |")

        if unclassified:
            lines.extend([
                "",
                "## Unclassified Symbols",
                "",
            ])
            for node in unclassified:
                lines.append(f"- `{node.name}` ({node.kind}, lines {node.lineno}-{node.end_lineno})")

        lines.extend([
            "",
            "## Module Details",
            "",
        ])
        for module_path in module_paths:
            module_nodes = [n for n in self.modules.get(module_path, []) if n.kind != "import"]
            deps = self.dep_analyzer.compute_dependency_map(module_path, module_nodes)
            lines.append(f"### `{module_path}`")
            lines.append("")
            if not module_nodes:
                lines.append("- Package initializer with no routed symbols.")
            else:
                lines.append(f"- Routed symbols: {len(module_nodes)}")
                if deps:
                    dep_summary = "; ".join(
                        f"`{mod}`: {', '.join(f'`{name}`' for name in sorted(names))}"
                        for mod, names in sorted(deps.items())
                    )
                    lines.append(f"- Cross-module imports: {dep_summary}")
                else:
                    lines.append("- Cross-module imports: none")
                lines.append("- Symbols:")
                for node in module_nodes:
                    lines.append(
                        f"  - `{node.name}` ({node.kind}, lines {node.lineno}-{node.end_lineno})"
                    )
            lines.append("")

        return "\n".join(lines).rstrip() + "\n"

    def _tree_lines(self, module_paths: List[str]) -> List[str]:
        tree: Dict[str, dict] = {}
        for rel_path in sorted(set(module_paths + ["__init__.py"])):
            cursor = tree
            for part in rel_path.split("/"):
                cursor = cursor.setdefault(part, {})
        lines = [f"{self.output_dir.name}/"]
        lines.extend(self._render_tree(tree, prefix=""))
        return lines

    def _render_tree(self, tree: Dict[str, dict], prefix: str) -> List[str]:
        lines: List[str] = []
        items = sorted(tree.items(), key=lambda item: (item[0].endswith(".py"), item[0]))
        for idx, (name, child) in enumerate(items):
            is_last = idx == len(items) - 1
            connector = "└── " if is_last else "├── "
            lines.append(f"{prefix}{connector}{name}")
            if child:
                child_prefix = prefix + ("    " if is_last else "│   ")
                lines.extend(self._render_tree(child, child_prefix))
        return lines


# ─── File Writer ─────────────────────────────────────────────────────────────

class FileWriter:
    """Writes generated module files to disk with change detection."""

    def __init__(self, output_dir: Path, dry_run: bool = False) -> None:
        self.output_dir = output_dir
        self.dry_run = dry_run
        self.written: List[str] = []
        self.skipped: List[str] = []

    def write(self, rel_path: str, content: str) -> bool:
        """Write file if content changed. Returns True if written."""
        full_path = self.output_dir / rel_path
        if self.dry_run:
            print(f"  [DRY-RUN] Would write: {rel_path} ({len(content):,} bytes)")
            self.written.append(rel_path)
            return True

        full_path.parent.mkdir(parents=True, exist_ok=True)

        # Skip if content unchanged
        if full_path.exists():
            existing = full_path.read_text(encoding="utf-8")
            if existing == content:
                self.skipped.append(rel_path)
                return False

        full_path.write_text(content, encoding="utf-8")
        self.written.append(rel_path)
        return True

    def ensure_init_files(self, all_module_paths: List[str]) -> None:
        """Ensure every package directory has an __init__.py."""
        dirs_seen: Set[str] = set()
        for mp in all_module_paths:
            parts = mp.split("/")
            for i in range(1, len(parts)):
                d = "/".join(parts[:i])
                if d not in dirs_seen:
                    dirs_seen.add(d)
                    init_path = f"{d}/__init__.py"
                    if not (self.output_dir / init_path).exists():
                        self.write(init_path, f"# {init_path}\n")


def _iter_python_files(root: Path) -> List[Path]:
    return sorted(
        p for p in root.rglob("*.py")
        if "__pycache__" not in p.parts
    )


def _collect_top_level_names(path: Path) -> Set[str]:
    names: Set[str] = set()
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            names.add(node.name)
        elif isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            for target in targets:
                if isinstance(target, ast.Name):
                    names.add(target.id)
    return names


def _is_split_coder_generated_python_file(path: Path) -> bool:
    if path.suffix != ".py" or not path.is_file():
        return False
    try:
        with path.open("r", encoding="utf-8") as fh:
            first_line = fh.readline()
    except Exception:
        return False
    return first_line.startswith("# Auto-generated by split_coder.py")


def _expected_python_output_paths(module_paths: List[str]) -> Set[str]:
    expected: Set[str] = {"__init__.py"}
    for rel_path in module_paths:
        if rel_path == "_imports":
            continue
        expected.add(rel_path)
        parts = rel_path.split("/")
        for i in range(1, len(parts)):
            expected.add("/".join(parts[:i]) + "/__init__.py")
    return expected


def _remove_stale_generated_python_files(output_dir: Path, keep_paths: Set[str]) -> List[str]:
    removed: List[str] = []
    if not output_dir.exists():
        return removed

    for path in sorted(
        (p for p in output_dir.rglob("*.py") if "__pycache__" not in p.parts),
        key=lambda p: (len(p.parts), p.as_posix()),
        reverse=True,
    ):
        rel = path.relative_to(output_dir).as_posix()
        if rel in keep_paths or not _is_split_coder_generated_python_file(path):
            continue
        try:
            path.unlink()
            removed.append(rel)
        except FileNotFoundError:
            continue

    for path in sorted(
        (p for p in output_dir.rglob("*") if p.is_dir() and "__pycache__" not in p.parts),
        key=lambda p: len(p.parts),
        reverse=True,
    ):
        if path == output_dir:
            continue
        try:
            next(path.iterdir())
        except StopIteration:
            try:
                path.rmdir()
            except OSError:
                pass
        except Exception:
            continue

    return sorted(removed)


def _clear_pycache_dirs(root: Path) -> List[str]:
    removed: List[str] = []
    if not root.exists():
        return removed
    for path in sorted((p for p in root.rglob("__pycache__") if p.is_dir()), key=lambda p: len(p.parts), reverse=True):
        rel = path.relative_to(root).as_posix()
        shutil.rmtree(path, ignore_errors=True)
        removed.append(rel)
    return removed


def run_self_check(source_path: Path, output_dir: Path, *, expect_report: bool = True, report_name: str = "FRAMEWORK.md") -> bool:
    print("\n[SELF-CHECK] Running post-split validation...")
    ok = True
    py_files = _iter_python_files(output_dir)
    package_name = output_dir.name

    try:
        source_names = _collect_top_level_names(source_path)
        output_names: Set[str] = set()
        for path in py_files:
            output_names.update(_collect_top_level_names(path))
        missing = sorted(source_names - output_names)
        extra = sorted(output_names - source_names)
        if missing or extra:
            ok = False
            print(f"  [FAIL] top-level symbol coverage mismatch: missing={len(missing)} extra={len(extra)}")
            if missing:
                print(f"         missing sample: {missing[:12]}")
            if extra:
                print(f"         extra sample: {extra[:12]}")
        else:
            print(f"  [OK] top-level symbols match ({len(source_names)} names)")

        compile_errors: List[str] = []
        for path in py_files:
            try:
                py_compile.compile(str(path), doraise=True)
            except py_compile.PyCompileError as exc:
                compile_errors.append(f"{path.relative_to(output_dir).as_posix()}: {exc.msg}")
            except Exception as exc:
                compile_errors.append(f"{path.relative_to(output_dir).as_posix()}: {exc}")
        if compile_errors:
            ok = False
            print(f"  [FAIL] py_compile failed for {len(compile_errors)} files")
            print(f"         first error: {compile_errors[0]}")
        else:
            print(f"  [OK] py_compile passed for {len(py_files)} files")

        manifest = SplitManifest.load(output_dir)
        if manifest:
            expected_non_init = {
                entry.target_module
                for entry in manifest.nodes
                if entry.target_module not in {"_imports", "__init__.py"}
                and not entry.target_module.endswith("/__init__.py")
            }
            stale_generated = [
                path.relative_to(output_dir).as_posix()
                for path in py_files
                if path.name != "__init__.py"
                and path.relative_to(output_dir).as_posix() not in expected_non_init
                and _is_split_coder_generated_python_file(path)
            ]
            if stale_generated:
                ok = False
                print(f"  [FAIL] stale generated python files detected ({len(stale_generated)})")
                print(f"         sample: {stale_generated[:5]}")
            else:
                print("  [OK] no stale generated python files detected")

        if expect_report:
            report_path = output_dir / report_name
            if report_path.exists() and report_path.is_file():
                print(f"  [OK] report exists: {report_path.name}")
            else:
                ok = False
                print(f"  [FAIL] missing report: {report_path.name}")

        if not package_name.isidentifier():
            ok = False
            print(f"  [FAIL] output directory name is not importable as a package: {package_name!r}")
        else:
            parent = output_dir.parent
            import_snippet = textwrap.dedent(
                f"""
                import importlib
                import pkgutil
                import sys

                sys.path.insert(0, {str(parent)!r})
                importlib.invalidate_caches()
                pkg = importlib.import_module({package_name!r})
                mods = [m.name for m in pkgutil.walk_packages(pkg.__path__, pkg.__name__ + '.')]
                errors = []
                for name in mods:
                    try:
                        importlib.import_module(name)
                    except Exception as exc:
                        errors.append((name, type(exc).__name__, str(exc)))
                if errors:
                    raise SystemExit("module import failures: " + repr(errors))
                print("ok", len(mods))
                """
            ).strip()
            proc = subprocess.run(
                [sys.executable, "-c", import_snippet],
                cwd=str(parent),
                text=True,
                capture_output=True,
                timeout=120,
            )
            if proc.returncode != 0:
                ok = False
                detail = (proc.stderr or proc.stdout or "").strip()
                print("  [FAIL] package import walk failed")
                if detail:
                    print(f"         {detail.splitlines()[-1]}")
            else:
                detail = (proc.stdout or "").strip().splitlines()
                imported = detail[-1] if detail else "ok"
                print(f"  [OK] package import walk passed ({imported})")

            help_proc = subprocess.run(
                [sys.executable, "-m", package_name, "--help"],
                cwd=str(parent),
                text=True,
                capture_output=True,
                timeout=120,
            )
            if help_proc.returncode != 0:
                ok = False
                detail = (help_proc.stderr or help_proc.stdout or "").strip()
                print("  [FAIL] entry point help check failed")
                if detail:
                    print(f"         {detail.splitlines()[-1]}")
            else:
                first = next((line.strip() for line in (help_proc.stdout or "").splitlines() if line.strip()), "help ok")
                print(f"  [OK] entry point help check passed ({first})")
    finally:
        removed = _clear_pycache_dirs(output_dir)
        if removed:
            print(f"  [CLEAN] removed {len(removed)} __pycache__ directories")
        else:
            print("  [CLEAN] no __pycache__ directories found")

    print(f"[SELF-CHECK] {'PASSED' if ok else 'FAILED'}")
    return ok


# ─── Main Splitter Orchestrator ───────────────────────────────────────────────

class Splitter:
    """Orchestrates the full split workflow."""

    def __init__(
        self,
        source_path: Path,
        output_dir: Path,
        layout: Dict[str, List[str]],
        dry_run: bool = False,
        update_mode: bool = False,
        show_tree: bool = False,
        dump_layout: bool = False,
        report_name: str = "FRAMEWORK.md",
        generate_report: bool = True,
    ) -> None:
        self.source_path = source_path
        self.output_dir = output_dir
        self.layout = layout
        self.dry_run = dry_run
        self.update_mode = update_mode
        self.show_tree = show_tree
        self.dump_layout_flag = dump_layout
        self.report_name = str(report_name or "FRAMEWORK.md").strip() or "FRAMEWORK.md"
        self.generate_report = bool(generate_report)
        self.package_name = source_path.stem.lower().replace(" ", "_").replace("-", "_")

    def run(self) -> None:
        print(f"\n{'─'*60}")
        print(f"  split_coder.py  —  splitting {self.source_path.name}")
        print(f"  Output: {self.output_dir}")
        print(f"{'─'*60}\n")

        # ── Step 1: Analyze source ─────────────────────────────────────────
        print("[1/7] Analyzing source architecture...")
        analyzer = ArchitectureAnalyzer(self.source_path)
        nodes = analyzer.analyze()
        print(f"  Found {len(nodes)} top-level nodes")

        # ── Step 2: Load existing manifest (for update mode) ───────────────
        old_manifest = SplitManifest.load(self.output_dir) if self.update_mode else None
        if self.update_mode and old_manifest:
            print(f"[2/7] Loaded existing manifest ({len(old_manifest.nodes)} nodes)")
        else:
            print("[2/7] Starting fresh split")

        # ── Step 3: Route nodes to modules ────────────────────────────────
        print("[3/7] Routing symbols to modules...")
        router = ModuleRouter(self.layout)
        router.assign_all(nodes)
        # Group by target module
        modules: Dict[str, List[NodeInfo]] = defaultdict(list)
        for node in nodes:
            modules[node.target_module].append(node)

        unclassified = modules.get("_unclassified.py", [])
        classified_count = len(nodes) - len(unclassified) - len(modules.get("_imports", []))
        print(f"  Classified {classified_count} symbols into {len(modules)} modules")
        if unclassified:
            print(f"  ⚠ Unclassified: {[n.name for n in unclassified[:10]]}"
                  + ("..." if len(unclassified) > 10 else ""))

        if self.dump_layout_flag:
            layout_out = {mod: [n.name for n in ns] for mod, ns in sorted(modules.items())}
            print("\n── Detected Layout ──")
            print(json.dumps(layout_out, indent=2))
            print()

        # ── Step 4: Analyze cross-module dependencies ─────────────────────
        print("[4/7] Analyzing cross-module dependencies...")
        dep_analyzer = DependencyAnalyzer(analyzer, nodes)
        gen = CodeGenerator(analyzer, dep_analyzer, self.package_name, str(self.source_path))
        # ── Step 5: Generate and write files ──────────────────────────────
        print("[5/7] Generating output files...")
        writer = FileWriter(self.output_dir, dry_run=self.dry_run)

        # Determine which modules to (re)generate
        old_node_map: Dict[str, str] = {}  # name → source_hash
        if old_manifest:
            old_node_map = {e.name: e.source_hash for e in old_manifest.nodes}

        # Collect all non-empty target modules
        all_target_modules = [m for m in modules.keys() if m != "_imports"]
        # Add empty __init__.py entries from layout
        for mp in self.layout:
            if mp.endswith("__init__.py") and mp not in modules:
                all_target_modules.append(mp)
        expected_python_paths = _expected_python_output_paths(sorted(set(all_target_modules)))

        for mod_path in sorted(set(all_target_modules)):
            if mod_path == "_imports":
                continue

            mod_nodes = modules.get(mod_path, [])

            # In update mode, skip unchanged modules
            if self.update_mode and old_manifest:
                changed = any(
                    old_node_map.get(n.name) != n.source_hash
                    for n in mod_nodes
                )
                if not changed and mod_nodes:
                    writer.skipped.append(mod_path)
                    continue

            content = gen.generate_module(mod_path, mod_nodes)
            writer.write(mod_path, content)

        # Ensure __init__.py in every sub-package + write root __init__.py
        writer.ensure_init_files(list(modules.keys()))
        writer.write("__init__.py", gen.generate_root_init(list(modules.keys())))

        if self.generate_report:
            print("[6/7] Generating framework markdown report...")
            report = FrameworkReportGenerator(
                source_path=self.source_path,
                output_dir=self.output_dir,
                modules=modules,
                dep_analyzer=dep_analyzer,
            ).generate()
            writer.write(self.report_name, report)
        else:
            print("[6/7] Framework markdown report disabled")

        # ── Step 6: Save manifest ──────────────────────────────────────────
        print("[7/7] Saving manifest...")
        source_hash = hashlib.sha256(
            self.source_path.read_bytes()
        ).hexdigest()[:16]

        manifest = SplitManifest(
            source_path=str(self.source_path),
            source_hash=source_hash,
            output_dir=str(self.output_dir),
            package_name=self.package_name,
            nodes=[
                ManifestEntry(
                    name=n.name,
                    kind=n.kind,
                    lineno=n.lineno,
                    end_lineno=n.end_lineno,
                    source_hash=n.source_hash,
                    target_module=n.target_module,
                )
                for n in nodes
            ],
        )
        if not self.dry_run:
            manifest.save(self.output_dir)

        removed_stale: List[str] = []
        if not self.dry_run:
            removed_stale = _remove_stale_generated_python_files(self.output_dir, expected_python_paths)

        # ── Summary ────────────────────────────────────────────────────────
        print(f"\n{'─'*60}")
        print(f"  Written : {len(writer.written)} files")
        print(f"  Skipped : {len(writer.skipped)} unchanged files")
        if removed_stale:
            print(f"  Removed : {len(removed_stale)} stale generated files")
        print(f"  Output  : {self.output_dir}")
        print(f"{'─'*60}")

        if self.show_tree and not self.dry_run:
            self._print_tree(self.output_dir)

    @staticmethod
    def _print_tree(root: Path, prefix: str = "", is_last: bool = True) -> None:
        """Print a directory tree."""
        if prefix == "":
            print(f"\n{root.name}/")
        items = sorted(root.iterdir(), key=lambda p: (p.is_file(), p.name))
        for i, item in enumerate(items):
            last = i == len(items) - 1
            connector = "└── " if last else "├── "
            print(f"{prefix}{connector}{item.name}")
            if item.is_dir():
                extension = "    " if last else "│   "
                Splitter._print_tree(item, prefix + extension, last)


# ─── Auto-Layout Generator ────────────────────────────────────────────────────

class AutoLayoutGenerator:
    """
    Generates a layout config by heuristic analysis of the source file.
    Used when no custom layout is provided.
    """

    EXACT_NAME_MODULES: Dict[str, str] = {
        "SCRIPT_DIR": "config/paths.py",
        "WORKDIR": "config/paths.py",
        "CODES_ROOT": "config/paths.py",
        "LLM_CONFIG_PATH": "config/paths.py",
        "REPO_ROOT": "config/paths.py",
        "detect_repo_root": "config/paths.py",
        "MAX_TOOL_OUTPUT": "utils/text.py",
        "SOCKET_NOISE_LINE_PATTERNS": "utils/text.py",
        "normalize_embedded_newlines": "utils/text.py",
        "_map_todo_status_token": "utils/text.py",
        "split_todo_status_text": "utils/text.py",
        "extract_todo_rows_from_text": "utils/text.py",
        "infer_todo_status_from_text": "utils/text.py",
        "split_structured_todo_content": "utils/text.py",
        "_compress_rows_keep_hotspot": "utils/text.py",
        "_hotspot_index": "utils/text.py",
        "_row_is_hot": "utils/text.py",
        "_skip_row": "utils/text.py",
        "JSON_FSYNC_ENABLED": "utils/json_utils.py",
        "tool_def": "utils/json_utils.py",
        "canonicalize_tool_name": "utils/json_utils.py",
        "TOOLS": "utils/json_utils.py",
        "TOOL_REQUIRED_ARGS": "utils/json_utils.py",
        "TOOL_SPEC_BY_NAME": "utils/json_utils.py",
        "TOOL_NAME_FUZZY_MAP": "utils/json_utils.py",
        "MIN_TIMEOUT_SECONDS": "utils/misc.py",
        "MAX_TIMEOUT_SECONDS": "utils/misc.py",
        "DEFAULT_TIMEOUT_SECONDS": "utils/misc.py",
        "BENIGN_SOCKET_DEBUG_LOG_ENABLED": "utils/misc.py",
        "BENIGN_SOCKET_LOG_INTERVAL_SECONDS": "utils/misc.py",
        "_normalize_js_lib_asset_ref": "utils/files.py",
        "_resolve_js_lib_asset_path": "utils/files.py",
        "_discover_extra_js_lib_files": "utils/files.py",
        "_offline_js_entry_relative_path": "utils/files.py",
        "_archive_member_relative_path": "utils/files.py",
        "_path_size_bytes": "utils/files.py",
        "_extract_archive_to_dir": "utils/files.py",
        "_package_required_paths": "utils/files.py",
        "_package_install_ready": "utils/files.py",
        "_postprocess_offline_js_package": "utils/files.py",
        "_ensure_offline_js_package": "utils/files.py",
        "detect_upload_parser_capabilities": "skills/store.py",
        "_render_cap_markdown": "skills/store.py",
        "_rag_safe_name": "rag/parsers.py",
        "_rag_detect_language": "rag/parsers.py",
        "_rag_cjk_ngrams": "rag/parsers.py",
        "_rag_is_noise_token": "rag/parsers.py",
        "_rag_entity_allowed": "rag/parsers.py",
        "_rag_filter_entities": "rag/parsers.py",
        "_rag_filename_entity_aliases": "rag/parsers.py",
        "_rag_apply_filename_entity_policy": "rag/parsers.py",
        "_rag_choose_community": "rag/parsers.py",
        "_rag_tokenize": "rag/parsers.py",
        "_rag_expand_tokens": "rag/parsers.py",
        "_rag_extract_entities": "rag/parsers.py",
        "_rag_classify_document": "rag/parsers.py",
        "_rag_chunk_text": "rag/parsers.py",
        "_code_language_from_name": "rag/parsers.py",
        "_code_is_test_path": "rag/parsers.py",
        "backend_i18n_text": "config/settings.py",
        "backend_role_label": "config/settings.py",
        "infer_user_complexity_value": "config/settings.py",
        "normalize_openai_compat_provider_name": "llm/utils.py",
        "is_openai_compat_provider": "llm/utils.py",
        "is_openai_like_provider": "llm/utils.py",
        "openai_compat_probe_headers": "llm/utils.py",
        "openai_compat_model_list_urls": "llm/utils.py",
        "extract_openai_compat_model_ids": "llm/utils.py",
    }

    # Name prefix/suffix → module path
    NAME_PATTERNS: List[Tuple[str, str, str]] = [
        # (pattern_type, pattern, module_path)
        ("prefix", "RAGContent",       "rag/parsers.py"),
        ("prefix", "RAGLibrary",       "rag/store.py"),
        ("prefix", "RAGIngestion",     "rag/ingestion.py"),
        ("prefix", "CodeContent",      "rag/parsers.py"),
        ("prefix", "CodeGraph",        "rag/index.py"),
        ("prefix", "CodeLibrary",      "rag/store.py"),
        ("prefix", "CodeIngestion",    "rag/ingestion.py"),
        ("prefix", "TFGraph",          "rag/index.py"),
        ("prefix", "Ollama",           "llm/client.py"),
        ("exact",  "SessionState",     "session/state.py"),
        ("prefix", "Session",          "session/manager.py"),
        ("exact",  "EventHub",         "agent/events.py"),
        ("exact",  "TodoManager",      "agent/todo.py"),
        ("exact",  "TaskManager",      "agent/tasks.py"),
        ("exact",  "BackgroundManager","agent/background.py"),
        ("exact",  "MessageBus",       "agent/bus.py"),
        ("prefix", "Worktree",         "agent/worktree.py"),
        ("prefix", "Skill",            "skills/store.py"),
        ("exact",  "AppContext",       "app/context.py"),
        ("prefix", "CryptoBox",        "utils/crypto.py"),
        ("suffix", "Error",            "utils/errors.py"),
        ("suffix", "Exception",        "utils/errors.py"),
        ("prefix", "AgentHTTP",        "server/handlers.py"),
        ("suffix", "Handler",          "server/handlers.py"),
        ("exact",  "main",             "__main__.py"),
    ]

    FUNCTION_PREFIXES: List[Tuple[str, str]] = [
        ("probe_ollama",           "llm/utils.py"),
        ("list_ollama",            "llm/utils.py"),
        ("resolve_ollama",         "llm/utils.py"),
        ("check_ollama",           "llm/utils.py"),
        ("wake_ollama",            "llm/utils.py"),
        ("try_pull_ollama",        "llm/utils.py"),
        ("list_loaded_ollama",     "llm/utils.py"),
        ("pick_working_ollama",    "llm/utils.py"),
        ("ordered_model_",         "llm/utils.py"),
        ("infer_thinking",         "llm/utils.py"),
        ("split_thinking",         "llm/utils.py"),
        ("strip_thinking",         "llm/utils.py"),
        ("extract_base_url",       "llm/utils.py"),
        ("complete_chat_endpoint", "llm/utils.py"),
        ("compress_",              "utils/compress.py"),
        ("decompress_",            "utils/compress.py"),
        ("guess_mime",             "utils/media.py"),
        ("guess_ext",              "utils/media.py"),
        ("_convert_image",         "utils/media.py"),
        ("json_dumps",             "utils/json_utils.py"),
        ("parse_json",             "utils/json_utils.py"),
        ("extract_json",           "utils/json_utils.py"),
        ("repair_truncated",       "utils/json_utils.py"),
        ("parse_tool_",            "utils/json_utils.py"),
        ("safe_path",              "utils/files.py"),
        ("_sha256",                "utils/files.py"),
        ("_download_http",         "utils/files.py"),
        ("offline_js",             "utils/files.py"),
        ("load_offline_js",        "utils/files.py"),
        ("ensure_offline_js",      "utils/files.py"),
        ("cache_external_js",      "utils/files.py"),
        ("is_external_js",         "utils/files.py"),
        ("match_offline_js",       "utils/files.py"),
        ("normalize_ui",           "config/settings.py"),
        ("normalize_execution",    "config/settings.py"),
        ("model_language",         "config/settings.py"),
        ("resolve_web_ui",         "config/settings.py"),
        ("resolve_optional_file",  "config/settings.py"),
        ("resolve_skills",         "config/settings.py"),
        ("select_preferred_skills","config/settings.py"),
        ("load_web_ui",            "config/settings.py"),
        ("extract_show_upload",    "config/settings.py"),
        ("extract_ui_style",       "config/settings.py"),
        ("infer_model_multimodal", "config/settings.py"),
        ("parse_capability",       "config/settings.py"),
        ("merge_multimodal",       "config/settings.py"),
        ("parse_media_endpoints",  "config/settings.py"),
        ("load_llm_config",        "config/settings.py"),
        ("infer_user_complexity",  "config/settings.py"),
        ("normalize_openai_compat","llm/utils.py"),
        ("is_openai_compat",       "llm/utils.py"),
        ("is_openai_like",         "llm/utils.py"),
        ("openai_compat_",         "llm/utils.py"),
        ("extract_openai_compat",  "llm/utils.py"),
        ("_resolve_default_agent", "config/paths.py"),
        ("_migrate_legacy",        "config/paths.py"),
        ("now_ts",                 "utils/misc.py"),
        ("make_id",                "utils/misc.py"),
        ("sanitize_",              "utils/misc.py"),
        ("detect_",                "utils/misc.py"),
        ("is_benign_socket",       "utils/misc.py"),
        ("swallow_benign",         "utils/misc.py"),
        ("normalize_timeout",      "utils/misc.py"),
        ("filter_runtime_noise",   "utils/misc.py"),
        ("trim",                   "utils/text.py"),
        ("_html_esc",              "utils/text.py"),
        ("_text_to_minimal",       "utils/text.py"),
        ("normalize_embedded_newlines", "utils/text.py"),
        ("split_todo_status_text", "utils/text.py"),
        ("extract_todo_rows_from_text", "utils/text.py"),
        ("infer_todo_status_from_text", "utils/text.py"),
        ("split_structured_todo_content", "utils/text.py"),
        ("normalize_work_text",    "utils/text.py"),
        ("ensure_generated_",      "skills/store.py"),
    ]

    FUNCTION_REGEX_RULES: List[Tuple[str, str]] = [
        (r"^extract_.*_setting$", "config/settings.py"),
        (r"^(?:load|parse)_.*config(?:_from_.*)?$", "config/settings.py"),
        (r"^backend_(?:i18n|role)_.*$", "config/settings.py"),
        (r"^resolve_.*(?:path|dir|root)$", "config/paths.py"),
        (r"^(?:load|ensure|match|cache|offline|download|extract|resolve)_.*(?:js_lib|offline_js|external_js).*$", "utils/files.py"),
    ]

    def generate(self, nodes: List[NodeInfo]) -> Dict[str, List[str]]:
        """Generate a layout config from node analysis."""
        layout: Dict[str, List[str]] = defaultdict(list)
        layout["__init__.py"] = []
        layout["config/__init__.py"] = []
        layout["utils/__init__.py"] = []
        layout["llm/__init__.py"] = []
        layout["agent/__init__.py"] = []
        layout["skills/__init__.py"] = []
        layout["session/__init__.py"] = []
        layout["rag/__init__.py"] = []
        layout["app/__init__.py"] = []
        layout["server/__init__.py"] = []

        for node in nodes:
            if node.kind == "import":
                continue
            module = self._classify(node)
            layout[module].append(node.name)

        return dict(layout)

    def _classify(self, node: NodeInfo) -> str:
        name = node.name

        if name in self.EXACT_NAME_MODULES:
            return self.EXACT_NAME_MODULES[name]

        # Constants go to config/constants.py
        if node.kind == "constant" or re.match(r"^[A-Z][A-Z0-9_]{3,}$", name):
            return "config/constants.py"

        # Check class/exact patterns
        for pat_type, pattern, module in self.NAME_PATTERNS:
            if pat_type == "exact" and name == pattern:
                return module
            if pat_type == "prefix" and name.startswith(pattern):
                return module
            if pat_type == "suffix" and name.endswith(pattern):
                return module

        # Check function prefixes
        if node.kind in ("function", "assignment"):
            for pattern, module in self.FUNCTION_REGEX_RULES:
                if re.match(pattern, name):
                    return module
            for prefix, module in self.FUNCTION_PREFIXES:
                if name.startswith(prefix) or name == prefix.rstrip("_"):
                    return module

        # Proximity-based: functions near a class likely belong to it
        # (handled by the proximity pass in a future version)

        return "_unclassified.py"


# ─── CLI ─────────────────────────────────────────────────────────────────────

def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Intelligent Python file splitter with architecture analysis.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""\
            Examples:
              python split_coder.py Clouds_Coder.py
              python split_coder.py Clouds_Coder.py --output-dir ./clouds_split
              python split_coder.py Clouds_Coder.py --dry-run
              python split_coder.py Clouds_Coder.py --update
              python split_coder.py Clouds_Coder.py --show-tree
              python split_coder.py Clouds_Coder.py --dump-layout
              python split_coder.py Clouds_Coder.py --self-check
              python split_coder.py Clouds_Coder.py --auto-layout  # ignore built-in rules
        """),
    )
    p.add_argument("source", help="Source Python file to split")
    p.add_argument(
        "--output-dir", "-o",
        help="Output directory (default: <source_stem>_split/ next to source)",
    )
    p.add_argument(
        "--dry-run", "-n",
        action="store_true",
        help="Preview without writing any files",
    )
    p.add_argument(
        "--update", "-u",
        action="store_true",
        help="Incremental update: only regenerate changed modules",
    )
    p.add_argument(
        "--show-tree",
        action="store_true",
        help="Print directory tree after split",
    )
    p.add_argument(
        "--dump-layout",
        action="store_true",
        help="Print the symbol→module layout as JSON (useful for debugging)",
    )
    p.add_argument(
        "--auto-layout",
        action="store_true",
        help="Use auto-generated layout instead of built-in rules",
    )
    p.add_argument(
        "--layout-file",
        help="Path to a custom layout JSON file (overrides built-in rules)",
    )
    p.add_argument(
        "--report-name",
        default="FRAMEWORK.md",
        help="Markdown framework report filename written inside the output directory.",
    )
    p.add_argument(
        "--no-report",
        action="store_true",
        help="Skip framework Markdown report generation.",
    )
    p.add_argument(
        "--self-check",
        action="store_true",
        help="Run post-split validation and then clear generated __pycache__ directories.",
    )
    return p


def load_layout(args) -> Dict[str, List[str]]:
    """Load layout config from file, auto-generate, or use default."""
    if args.layout_file:
        path = Path(args.layout_file)
        if not path.exists():
            raise SystemExit(f"Layout file not found: {path}")
        return json.loads(path.read_text(encoding="utf-8"))
    if args.auto_layout:
        # Will be filled in after analysis
        return None  # type: ignore
    return DEFAULT_LAYOUT


def main() -> int:
    parser = build_arg_parser()
    args = parser.parse_args()

    source_path = Path(args.source).expanduser().resolve()
    if not source_path.exists():
        print(f"Error: Source file not found: {source_path}", file=sys.stderr)
        return 1

    if args.output_dir:
        output_dir = Path(args.output_dir).expanduser().resolve()
    else:
        output_dir = source_path.parent / "Code_Structure"

    if args.self_check and args.dry_run:
        print("Error: --self-check cannot be used with --dry-run", file=sys.stderr)
        return 2

    layout = load_layout(args)

    # If auto-layout requested, do a first-pass analysis to generate layout
    if layout is None:
        print("[AUTO] Running first-pass analysis to generate layout...")
        analyzer = ArchitectureAnalyzer(source_path)
        nodes = analyzer.analyze()
        auto_gen = AutoLayoutGenerator()
        layout = auto_gen.generate(nodes)
        print(f"[AUTO] Generated layout with {len(layout)} modules")

    splitter = Splitter(
        source_path=source_path,
        output_dir=output_dir,
        layout=layout,
        dry_run=args.dry_run,
        update_mode=args.update,
        show_tree=args.show_tree,
        dump_layout=args.dump_layout,
        report_name=args.report_name,
        generate_report=not args.no_report,
    )
    splitter.run()

    if args.self_check:
        passed = run_self_check(
            source_path,
            output_dir,
            expect_report=not args.no_report,
            report_name=args.report_name,
        )
        return 0 if passed else 2

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
