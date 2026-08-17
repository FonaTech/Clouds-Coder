# Code_Structure Framework

## Overview

- Source snapshot: `Clouds_Coder.py` (969 top-level statements)
- Generated source modules: 58
- Unclassified statements: 0
- Execution model: real source fragments initialized in original top-level order
- Runtime dependency on original monolith: none

The generated modules contain the actual Python source. `_runtime.py` only preserves the original
global initialization order and shared-global semantics required by this legacy monolith's circular
dependency graph; it does not import or read `Clouds_Coder.py`.

## Package Tree

```text
Code_Structure/
├── admin
│   ├── auth.py
│   ├── config.py
│   └── constants.py
├── agent
│   ├── background.py
│   ├── bus.py
│   ├── errors.py
│   ├── events.py
│   ├── tasks.py
│   ├── todo.py
│   ├── tools.py
│   └── worktree.py
├── app
│   ├── context.py
│   ├── main.py
│   └── services.py
├── config
│   ├── constants.py
│   ├── paths.py
│   └── settings.py
├── ide
│   ├── assets.py
│   ├── auth.py
│   ├── errors.py
│   ├── events.py
│   ├── handler.py
│   ├── preview.py
│   └── sandbox.py
├── llm
│   ├── client.py
│   ├── constants.py
│   └── utils.py
├── mcp
│   ├── constants.py
│   ├── driver.py
│   └── service.py
├── rag
│   ├── assets.py
│   ├── constants.py
│   ├── index.py
│   ├── ingestion.py
│   ├── parsers.py
│   ├── store.py
│   └── web_search.py
├── server
│   ├── http.py
│   ├── rag_admin.py
│   └── skills.py
├── session
│   ├── manager.py
│   └── state.py
├── skills
│   ├── embedded.py
│   ├── provisioning.py
│   └── store.py
├── utils
│   ├── compress.py
│   ├── crypto.py
│   ├── errors.py
│   ├── files.py
│   ├── http.py
│   ├── json_utils.py
│   ├── media.py
│   ├── misc.py
│   └── text.py
├── web
│   ├── admin_assets.py
│   ├── assets.py
│   └── skills_assets.py
├── __init__.py
├── __main__.py
├── _imports.py
└── _runtime.py
```

## Module Summary

| Module | Statements | Exported names | Dependencies | Original line span |
| --- | ---: | ---: | --- | --- |
| `_imports.py` | 60 | 75 | — | 1–78 |
| `admin/auth.py` | 3 | 3 | `admin/constants.py`, `utils/misc.py` | 8085–8786 |
| `admin/config.py` | 8 | 8 | `config/constants.py`, `config/paths.py`, `config/settings.py`, `llm/constants.py`, `utils/http.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` | 9511–9924 |
| `admin/constants.py` | 13 | 13 | — | 85–143 |
| `agent/background.py` | 1 | 1 | `ide/sandbox.py`, `utils/misc.py`, `utils/text.py` | 16376–16485 |
| `agent/bus.py` | 1 | 1 | `config/constants.py`, `utils/crypto.py`, `utils/misc.py` | 16486–16551 |
| `agent/errors.py` | 1 | 1 | — | 6674–6677 |
| `agent/events.py` | 1 | 1 | — | 10616–10662 |
| `agent/tasks.py` | 1 | 1 | `utils/crypto.py`, `utils/json_utils.py`, `utils/misc.py` | 16241–16375 |
| `agent/todo.py` | 1 | 1 | `config/constants.py`, `config/settings.py`, `utils/misc.py`, `utils/text.py` | 10663–11023 |
| `agent/tools.py` | 15 | 19 | `config/constants.py`, `utils/text.py` | 10495–21148 |
| `agent/worktree.py` | 1 | 1 | `agent/tasks.py`, `config/constants.py`, `utils/crypto.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` | 16552–16768 |
| `app/context.py` | 1 | 1 | `admin/auth.py`, `admin/config.py`, `admin/constants.py`, `agent/tools.py`, `app/services.py`, `config/constants.py`, `config/paths.py`, `config/settings.py`, `ide/assets.py`, `ide/auth.py`, `ide/errors.py`, `ide/events.py`, `ide/preview.py`, `ide/sandbox.py`, `llm/client.py`, `llm/constants.py`, `llm/utils.py`, `mcp/driver.py`, `rag/assets.py`, `rag/constants.py`, `rag/ingestion.py`, `rag/parsers.py`, `rag/store.py`, `session/manager.py`, `session/state.py`, `skills/provisioning.py`, `skills/store.py`, `utils/crypto.py`, `utils/files.py`, `utils/http.py`, `utils/json_utils.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py`, `web/assets.py`, `web/skills_assets.py` | 98138–106413 |
| `app/main.py` | 2 | 1 | `admin/config.py`, `admin/constants.py`, `agent/tools.py`, `app/context.py`, `config/constants.py`, `config/paths.py`, `config/settings.py`, `ide/handler.py`, `llm/constants.py`, `llm/utils.py`, `mcp/constants.py`, `mcp/service.py`, `rag/constants.py`, `server/http.py`, `server/rag_admin.py`, `server/skills.py`, `skills/provisioning.py`, `utils/files.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` | 110937–112604 |
| `app/services.py` | 2 | 2 | `admin/constants.py`, `config/settings.py`, `skills/embedded.py`, `skills/store.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` | 106454–107572 |
| `config/constants.py` | 381 | 377 | `rag/constants.py` | 81–10240 |
| `config/paths.py` | 8 | 8 | `utils/text.py` | 84–3864 |
| `config/settings.py` | 63 | 63 | `agent/tools.py`, `config/constants.py`, `config/paths.py`, `llm/constants.py`, `llm/utils.py`, `rag/constants.py`, `skills/provisioning.py`, `utils/http.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` | 1993–8425 |
| `ide/assets.py` | 7 | 3 | — | 97278–98137 |
| `ide/auth.py` | 2 | 2 | `admin/auth.py`, `admin/constants.py`, `config/constants.py`, `utils/misc.py`, `utils/text.py` | 8787–9495 |
| `ide/errors.py` | 2 | 2 | — | 9496–9510 |
| `ide/events.py` | 1 | 1 | `config/constants.py`, `utils/text.py` | 4472–4518 |
| `ide/handler.py` | 1 | 1 | `admin/auth.py`, `app/context.py`, `config/constants.py`, `config/settings.py`, `ide/auth.py`, `ide/errors.py`, `ide/events.py`, `session/manager.py`, `session/state.py`, `utils/http.py`, `utils/json_utils.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py` | 109564–110719 |
| `ide/preview.py` | 12 | 12 | `config/constants.py`, `utils/text.py` | 10210–10615 |
| `ide/sandbox.py` | 18 | 18 | `utils/misc.py` | 21149–21631 |
| `llm/client.py` | 2 | 2 | `agent/tools.py`, `config/constants.py`, `config/settings.py`, `llm/utils.py`, `utils/http.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` | 18151–20488 |
| `llm/constants.py` | 17 | 17 | — | 82–7117 |
| `llm/utils.py` | 22 | 22 | `config/settings.py`, `llm/constants.py`, `utils/http.py`, `utils/json_utils.py`, `utils/text.py` | 6648–7331 |
| `mcp/constants.py` | 8 | 8 | — | 235–16804 |
| `mcp/driver.py` | 13 | 13 | `mcp/constants.py`, `utils/files.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` | 16805–18150 |
| `mcp/service.py` | 1 | 1 | `app/context.py`, `config/constants.py`, `utils/files.py`, `utils/http.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` | 110720–110936 |
| `rag/assets.py` | 6 | 6 | — | 94870–97277 |
| `rag/constants.py` | 74 | 74 | — | 231–88012 |
| `rag/index.py` | 5 | 5 | `rag/constants.py`, `rag/ingestion.py`, `rag/parsers.py`, `utils/misc.py`, `utils/text.py` | 88037–94515 |
| `rag/ingestion.py` | 13 | 13 | `config/constants.py`, `config/settings.py`, `rag/constants.py`, `rag/parsers.py`, `rag/store.py`, `session/state.py`, `utils/files.py`, `utils/json_utils.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py` | 87405–94869 |
| `rag/parsers.py` | 24 | 24 | `config/constants.py`, `rag/constants.py`, `rag/ingestion.py`, `utils/files.py`, `utils/json_utils.py`, `utils/media.py`, `utils/text.py` | 87195–89145 |
| `rag/store.py` | 7 | 7 | `config/constants.py`, `config/settings.py`, `ide/preview.py`, `rag/constants.py`, `rag/index.py`, `rag/ingestion.py`, `rag/parsers.py`, `skills/provisioning.py`, `utils/files.py`, `utils/json_utils.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py` | 90823–94781 |
| `rag/web_search.py` | 15 | 15 | `config/constants.py`, `config/paths.py`, `rag/constants.py`, `utils/http.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` | 4553–6000 |
| `server/http.py` | 2 | 2 | `admin/auth.py`, `admin/config.py`, `app/context.py`, `config/constants.py`, `config/paths.py`, `config/settings.py`, `ide/preview.py`, `llm/utils.py`, `session/manager.py`, `session/state.py`, `utils/files.py`, `utils/http.py`, `utils/json_utils.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py`, `web/admin_assets.py` | 106414–108942 |
| `server/rag_admin.py` | 2 | 2 | `admin/auth.py`, `app/context.py`, `config/constants.py`, `rag/constants.py`, `utils/http.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py` | 109169–109563 |
| `server/skills.py` | 1 | 1 | `admin/auth.py`, `app/context.py`, `config/constants.py`, `config/paths.py`, `config/settings.py`, `session/manager.py`, `skills/provisioning.py`, `utils/http.py`, `utils/misc.py`, `utils/text.py` | 108943–109168 |
| `session/manager.py` | 2 | 2 | `config/constants.py`, `config/paths.py`, `config/settings.py`, `llm/client.py`, `llm/utils.py`, `rag/store.py`, `session/state.py`, `utils/crypto.py`, `utils/files.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` | 3131–76029 |
| `session/state.py` | 1 | 1 | `admin/constants.py`, `agent/background.py`, `agent/bus.py`, `agent/errors.py`, `agent/events.py`, `agent/tasks.py`, `agent/todo.py`, `agent/tools.py`, `agent/worktree.py`, `config/constants.py`, `config/paths.py`, `config/settings.py`, `ide/preview.py`, `ide/sandbox.py`, `llm/client.py`, `llm/constants.py`, `llm/utils.py`, `mcp/constants.py`, `mcp/driver.py`, `rag/constants.py`, `rag/parsers.py`, `rag/web_search.py`, `skills/provisioning.py`, `skills/store.py`, `utils/compress.py`, `utils/crypto.py`, `utils/errors.py`, `utils/files.py`, `utils/http.py`, `utils/json_utils.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py` | 21632–74717 |
| `skills/embedded.py` | 10 | 10 | — | 11024–14823 |
| `skills/provisioning.py` | 26 | 26 | `config/paths.py`, `skills/embedded.py`, `utils/files.py`, `utils/json_utils.py`, `utils/misc.py` | 11050–14786 |
| `skills/store.py` | 2 | 2 | `config/constants.py`, `config/settings.py`, `llm/utils.py`, `skills/embedded.py`, `utils/files.py`, `utils/http.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` | 14824–16240 |
| `utils/compress.py` | 2 | 2 | — | 6165–6181 |
| `utils/crypto.py` | 1 | 1 | `utils/json_utils.py` | 8118–8236 |
| `utils/errors.py` | 1 | 1 | — | 6670–6673 |
| `utils/files.py` | 27 | 27 | `config/constants.py`, `config/paths.py`, `utils/http.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` | 1912–8449 |
| `utils/http.py` | 7 | 7 | `utils/json_utils.py`, `utils/text.py` | 79–3839 |
| `utils/json_utils.py` | 13 | 13 | `utils/text.py` | 230–8507 |
| `utils/media.py` | 3 | 3 | — | 3479–3512 |
| `utils/misc.py` | 16 | 16 | `config/constants.py` | 3513–11125 |
| `utils/text.py` | 30 | 30 | `config/constants.py` | 218–10209 |
| `web/admin_assets.py` | 3 | 3 | — | 81905–82260 |
| `web/assets.py` | 4 | 4 | — | 76030–81505 |
| `web/skills_assets.py` | 3 | 3 | — | 81506–81904 |

## Source Mapping

### `_imports.py`

- order 0: `_import_3` (import), lines 1-3, exports `annotations`
- order 1: `_import_5` (import), lines 4-5, exports `argparse`
- order 2: `_import_6` (import), lines 6-6, exports `ast`
- order 3: `_import_7` (import), lines 7-7, exports `base64`
- order 4: `_import_8` (import), lines 8-8, exports `concurrent`
- order 5: `_import_9` (import), lines 9-9, exports `csv`
- order 6: `_import_10` (import), lines 10-10, exports `ctypes`
- order 7: `_import_11` (import), lines 11-11, exports `difflib`
- order 8: `_import_12` (import), lines 12-12, exports `errno`
- order 9: `_import_13` (import), lines 13-13, exports `fnmatch`
- order 10: `_import_14` (import), lines 14-14, exports `hashlib`
- order 11: `_import_15` (import), lines 15-15, exports `hmac`
- order 12: `_import_16` (import), lines 16-16, exports `html`
- order 13: `_import_17` (import), lines 17-17, exports `importlib`
- order 14: `_import_18` (import), lines 18-18, exports `io`
- order 15: `_import_19` (import), lines 19-19, exports `ipaddress`
- order 16: `_import_20` (import), lines 20-20, exports `json`
- order 17: `_import_21` (import), lines 21-21, exports `locale`
- order 18: `_import_22` (import), lines 22-22, exports `math`
- order 19: `_import_23` (import), lines 23-23, exports `mimetypes`
- order 20: `_import_24` (import), lines 24-24, exports `multiprocessing`
- order 21: `_import_25` (import), lines 25-25, exports `os`
- order 22: `_import_26` (import), lines 26-26, exports `queue`
- order 23: `_import_27` (import), lines 27-27, exports `re`
- order 24: `_import_28` (import), lines 28-28, exports `select`
- order 25: `_import_29` (import), lines 29-29, exports `selectors`
- order 26: `_import_30` (import), lines 30-30, exports `shlex`
- order 27: `_import_31` (import), lines 31-31, exports `shutil`
- order 28: `_import_32` (import), lines 32-32, exports `signal`
- order 29: `_import_33` (import), lines 33-33, exports `socket`
- order 30: `_import_34` (import), lines 34-34, exports `sqlite3`
- order 31: `_import_35` (import), lines 35-35, exports `ssl`
- order 32: `_import_36` (import), lines 36-36, exports `struct`
- order 33: `_import_37` (import), lines 37-37, exports `subprocess`
- order 34: `_import_38` (import), lines 38-38, exports `sys`
- order 35: `_import_39` (import), lines 39-39, exports `tarfile`
- order 36: `_import_40` (import), lines 40-40, exports `tempfile`
- order 37: `_import_41` (import), lines 41-41, exports `threading`
- order 38: `_import_42` (import), lines 42-42, exports `time`
- order 39: `_import_43` (import), lines 43-43, exports `traceback`
- order 40: `_import_44` (import), lines 44-44, exports `unicodedata`
- order 41: `_import_45` (import), lines 45-45, exports `robotparser`
- order 42: `_import_46` (import), lines 46-46, exports `uuid`
- order 43: `_import_47` (import), lines 47-47, exports `ET`
- order 44: `_import_48` (import), lines 48-48, exports `zipfile`
- order 45: `_import_49` (import), lines 49-49, exports `zlib`
- order 46: `_import_50` (import), lines 50-50, exports `Counter`, `defaultdict`, `deque`
- order 47: `_import_51` (import), lines 51-51, exports `datetime`, `timedelta`, `timezone`
- order 48: `_import_52` (import), lines 52-52, exports `parsedate_to_datetime`
- order 49: `_import_53` (import), lines 53-53, exports `HTMLParser`
- order 50: `_import_54` (import), lines 54-54, exports `HTTPStatus`
- order 51: `_import_55` (import), lines 55-55, exports `IncompleteRead`
- order 52: `_import_56` (import), lines 56-56, exports `BaseHTTPRequestHandler`, `ThreadingHTTPServer`
- order 53: `_import_57` (import), lines 57-57, exports `Path`, `PurePosixPath`
- order 54: `_import_58` (import), lines 58-58, exports `HTTPError`, `URLError`
- order 55: `_import_59` (import), lines 59-59, exports `parse_qs`, `quote`, `unquote`, `urljoin`, `urlparse`, `urlunparse`
- order 56: `_import_60` (import), lines 60-60, exports `Request`, `urlopen`
- order 57: `_try_import_62` (import), lines 61-69, exports `_fcntl`, `_pty`, `_termios`
- order 58: `_try_import_71` (import), lines 70-74, exports `_certifi`
- order 59: `_try_import_75` (import), lines 75-78, exports `_yaml`

### `admin/auth.py`

- order 725: `trusted_client_ip` (function), lines 8085-8117, exports `trusted_client_ip`
- order 733: `AdminAuthError` (class), lines 8508-8515, exports `AdminAuthError`
- order 734: `AdminAuthStore` (class), lines 8516-8786, exports `AdminAuthStore`

### `admin/config.py`

- order 739: `_admin_config_schema` (function), lines 9511-9619, exports `_admin_config_schema`
- order 740: `_admin_factory_config` (function), lines 9620-9623, exports `_admin_factory_config`
- order 741: `_admin_coerce_config` (function), lines 9624-9744, exports `_admin_coerce_config`
- order 742: `_admin_config_to_argv` (function), lines 9745-9781, exports `_admin_config_to_argv`
- order 743: `_admin_restart_probe_url` (function), lines 9782-9797, exports `_admin_restart_probe_url`
- order 744: `_admin_supervised_restart` (function), lines 9798-9884, exports `_admin_supervised_restart`
- order 745: `_admin_argparse_defaults` (function), lines 9885-9904, exports `_admin_argparse_defaults`
- order 746: `_admin_config_from_namespace` (function), lines 9905-9924, exports `_admin_config_from_namespace`

### `admin/constants.py`

- order 66: `ADMIN_STATE_DIRNAME` (constant), lines 85-85, exports `ADMIN_STATE_DIRNAME`
- order 67: `ADMIN_CONFIG_FILENAME` (constant), lines 86-86, exports `ADMIN_CONFIG_FILENAME`
- order 68: `ADMIN_APPS_FILENAME` (constant), lines 87-87, exports `ADMIN_APPS_FILENAME`
- order 69: `ADMIN_TELEMETRY_FILENAME` (constant), lines 88-88, exports `ADMIN_TELEMETRY_FILENAME`
- order 70: `ADMIN_AUTH_FILENAME` (constant), lines 89-89, exports `ADMIN_AUTH_FILENAME`
- order 80: `ADMIN_MAX_APP_SKILLS` (constant), lines 136-136, exports `ADMIN_MAX_APP_SKILLS`
- order 81: `ADMIN_MAX_APP_CAPSULE_CHARS` (constant), lines 137-137, exports `ADMIN_MAX_APP_CAPSULE_CHARS`
- order 82: `ADMIN_MAX_APP_RESOURCE_FILES` (constant), lines 138-138, exports `ADMIN_MAX_APP_RESOURCE_FILES`
- order 83: `ADMIN_MAX_APP_RESOURCE_BYTES` (constant), lines 139-139, exports `ADMIN_MAX_APP_RESOURCE_BYTES`
- order 84: `ADMIN_APP_INLINE_BLOB_BYTES` (constant), lines 140-140, exports `ADMIN_APP_INLINE_BLOB_BYTES`
- order 85: `ADMIN_AUTH_SESSION_TTL_SECONDS` (constant), lines 141-141, exports `ADMIN_AUTH_SESSION_TTL_SECONDS`
- order 86: `ADMIN_AUTH_PASSWORD_ITERATIONS` (constant), lines 142-142, exports `ADMIN_AUTH_PASSWORD_ITERATIONS`
- order 87: `ADMIN_AUTH_MAX_ACTIVE_SESSIONS` (constant), lines 143-143, exports `ADMIN_AUTH_MAX_ACTIVE_SESSIONS`

### `agent/background.py`

- order 815: `BackgroundManager` (class), lines 16376-16485, exports `BackgroundManager`

### `agent/bus.py`

- order 816: `MessageBus` (class), lines 16486-16551, exports `MessageBus`

### `agent/errors.py`

- order 674: `CircuitBreakerTriggered` (class), lines 6674-6677, exports `CircuitBreakerTriggered`

### `agent/events.py`

- order 773: `EventHub` (class), lines 10616-10662, exports `EventHub`

### `agent/tasks.py`

- order 814: `TaskManager` (class), lines 16241-16375, exports `TaskManager`

### `agent/todo.py`

- order 774: `TodoManager` (class), lines 10663-11023, exports `TodoManager`

### `agent/tools.py`

- order 768: `_ask_user_option_rows` (function), lines 10495-10528, exports `_ask_user_option_rows`
- order 769: `_ask_user_option_value` (function), lines 10529-10534, exports `_ask_user_option_value`
- order 840: `tool_def` (function), lines 20489-20502, exports `tool_def`
- order 841: `TOOLS` (constant), lines 20503-20987, exports `TOOLS`
- order 842: `TOOL_REQUIRED_ARGS` (constant), lines 20988-20989, exports `TOOL_REQUIRED_ARGS`
- order 843: `TOOL_SPEC_BY_NAME` (constant), lines 20990-20990, exports `TOOL_SPEC_BY_NAME`
- order 844: `_for_20991` (statement), lines 20991-21000, exports `_tool`, `_fn`, `_name`, `_required`
- order 845: `TOOL_NAME_FUZZY_MAP` (constant), lines 21001-21002, exports `TOOL_NAME_FUZZY_MAP`
- order 846: `_for_21003` (statement), lines 21003-21006, exports `_name`, `_key`
- order 847: `_for_21008` (statement), lines 21007-21024, exports `_alias`, `_target`
- order 848: `is_todo_resume_tool_name` (function), lines 21025-21041, exports `is_todo_resume_tool_name`
- order 849: `canonicalize_tool_name` (function), lines 21042-21060, exports `canonicalize_tool_name`
- order 850: `filter_tool_specs_for_runtime` (function), lines 21061-21076, exports `filter_tool_specs_for_runtime`
- order 851: `DEVELOPER_TOOL_DROP` (constant), lines 21077-21087, exports `DEVELOPER_TOOL_DROP`
- order 852: `AGENT_TOOL_ALLOWLIST` (constant), lines 21088-21148, exports `AGENT_TOOL_ALLOWLIST`

### `agent/worktree.py`

- order 817: `WorktreeManager` (class), lines 16552-16768, exports `WorktreeManager`

### `app/context.py`

- order 957: `AppContext` (class), lines 98138-106413, exports `AppContext`

### `app/main.py`

- order 967: `main` (function), lines 110937-112601, exports `main`
- order 968: `_main_guard_112603` (main_guard), lines 112602-112604, exports —

### `app/services.py`

- order 959: `TelemetryStore` (class), lines 106454-106829, exports `TelemetryStore`
- order 960: `ApplicationRegistry` (class), lines 106830-107572, exports `ApplicationRegistry`

### `config/constants.py`

- order 62: `APP_VERSION` (constant), lines 81-81, exports `APP_VERSION`
- order 71: `IDE_AUTH_FILENAME` (constant), lines 90-90, exports `IDE_AUTH_FILENAME`
- order 72: `IDE_AUTH_SESSION_TTL_SECONDS` (constant), lines 91-91, exports `IDE_AUTH_SESSION_TTL_SECONDS`
- order 73: `IDE_AUTH_MAX_ACTIVE_SESSIONS` (constant), lines 92-92, exports `IDE_AUTH_MAX_ACTIVE_SESSIONS`
- order 74: `IDE_DEVICE_SECRET_MIN_BYTES` (constant), lines 93-93, exports `IDE_DEVICE_SECRET_MIN_BYTES`
- order 75: `IDE_DEVICE_LABEL_MAX_CHARS` (constant), lines 94-94, exports `IDE_DEVICE_LABEL_MAX_CHARS`
- order 76: `IDE_DEVICE_PAIRING_TTL_SECONDS` (constant), lines 95-95, exports `IDE_DEVICE_PAIRING_TTL_SECONDS`
- order 77: `IDE_WORKBENCH_STATE_FILENAME` (constant), lines 96-96, exports `IDE_WORKBENCH_STATE_FILENAME`
- order 78: `IDE_PROMPT_ENHANCEMENT_BUDGETS` (constant), lines 97-134, exports `IDE_PROMPT_ENHANCEMENT_BUDGETS`
- order 79: `IDE_EXTENSIONS_DIRNAME` (constant), lines 135-135, exports `IDE_EXTENSIONS_DIRNAME`
- order 96: `LONG_OUTPUT_MODEL_PAGE_CHARS` (constant), lines 219-219, exports `LONG_OUTPUT_MODEL_PAGE_CHARS`
- order 97: `LONG_OUTPUT_UI_PAGE_CHARS` (constant), lines 220-220, exports `LONG_OUTPUT_UI_PAGE_CHARS`
- order 98: `LONG_OUTPUT_UI_PREVIEW_MAX_PAGES` (constant), lines 221-221, exports `LONG_OUTPUT_UI_PREVIEW_MAX_PAGES`
- order 99: `LONG_OUTPUT_LISTING_OFFLOAD_CHARS` (constant), lines 222-222, exports `LONG_OUTPUT_LISTING_OFFLOAD_CHARS`
- order 100: `LONG_OUTPUT_READ_PAGE_LINES` (constant), lines 223-223, exports `LONG_OUTPUT_READ_PAGE_LINES`
- order 101: `LONG_OUTPUT_READ_PAGE_MAX_CHARS` (constant), lines 224-224, exports `LONG_OUTPUT_READ_PAGE_MAX_CHARS`
- order 102: `LONG_OUTPUT_TEMP_MAX_FILES` (constant), lines 225-225, exports `LONG_OUTPUT_TEMP_MAX_FILES`
- order 103: `READ_FILE_DEFAULT_MAX_CHARS` (constant), lines 226-226, exports `READ_FILE_DEFAULT_MAX_CHARS`
- order 104: `READ_FILE_HARD_MAX_CHARS` (constant), lines 227-227, exports `READ_FILE_HARD_MAX_CHARS`
- order 105: `READ_FILE_OVERVIEW_HEAD_LINES` (constant), lines 228-228, exports `READ_FILE_OVERVIEW_HEAD_LINES`
- order 106: `READ_FILE_SEARCH_MAX_MATCHES` (constant), lines 229-229, exports `READ_FILE_SEARCH_MAX_MATCHES`
- order 111: `CODE_ADMIN_PORT_OFFSET` (constant), lines 234-234, exports `CODE_ADMIN_PORT_OFFSET`
- order 113: `IDE_PORT_OFFSET` (constant), lines 236-239, exports `IDE_PORT_OFFSET`
- order 114: `IDE_DEFAULT_PORT` (constant), lines 240-240, exports `IDE_DEFAULT_PORT`
- order 116: `DEFAULT_WEB_SEARCH_ENABLED` (constant), lines 242-242, exports `DEFAULT_WEB_SEARCH_ENABLED`
- order 121: `DEFAULT_USER_MEMORY_MODE` (constant), lines 247-247, exports `DEFAULT_USER_MEMORY_MODE`
- order 129: `AGENT_WEB_SEARCH_USER_AGENT` (constant), lines 258-258, exports `AGENT_WEB_SEARCH_USER_AGENT`
- order 130: `AGENT_WEB_SEARCH_DEFAULT_MAX_RESULTS` (constant), lines 259-259, exports `AGENT_WEB_SEARCH_DEFAULT_MAX_RESULTS`
- order 131: `AGENT_WEB_SEARCH_DEFAULT_MAX_PAGES` (constant), lines 260-260, exports `AGENT_WEB_SEARCH_DEFAULT_MAX_PAGES`
- order 132: `AGENT_WEB_SEARCH_HARD_MAX_PAGES` (constant), lines 261-261, exports `AGENT_WEB_SEARCH_HARD_MAX_PAGES`
- order 133: `AGENT_WEB_SEARCH_DEFAULT_DEPTH` (constant), lines 262-262, exports `AGENT_WEB_SEARCH_DEFAULT_DEPTH`
- order 134: `AGENT_WEB_SEARCH_HARD_DEPTH` (constant), lines 263-263, exports `AGENT_WEB_SEARCH_HARD_DEPTH`
- order 135: `AGENT_WEB_SEARCH_FETCH_TIMEOUT` (constant), lines 264-264, exports `AGENT_WEB_SEARCH_FETCH_TIMEOUT`
- order 136: `AGENT_WEB_SEARCH_TOOL_SOFT_TIMEOUT` (constant), lines 265-265, exports `AGENT_WEB_SEARCH_TOOL_SOFT_TIMEOUT`
- order 137: `AGENT_WEB_SEARCH_MAX_PAGE_BYTES` (constant), lines 266-266, exports `AGENT_WEB_SEARCH_MAX_PAGE_BYTES`
- order 138: `AGENT_WEB_SEARCH_MAX_TEXT_CHARS` (constant), lines 267-267, exports `AGENT_WEB_SEARCH_MAX_TEXT_CHARS`
- order 148: `CODE_CHUNK_CHARS` (constant), lines 289-289, exports `CODE_CHUNK_CHARS`
- order 149: `CODE_CHUNK_OVERLAP` (constant), lines 290-290, exports `CODE_CHUNK_OVERLAP`
- order 150: `CODE_MAX_CHUNKS_PER_DOC` (constant), lines 291-291, exports `CODE_MAX_CHUNKS_PER_DOC`
- order 188: `CODE_IMPORT_WORKER_COUNT` (constant), lines 351-354, exports `CODE_IMPORT_WORKER_COUNT`
- order 190: `CODE_PARSE_TIMEOUT_SECONDS` (constant), lines 359-362, exports `CODE_PARSE_TIMEOUT_SECONDS`
- order 191: `DEFAULT_CONTEXT_TOKEN_LIMIT` (constant), lines 363-363, exports `DEFAULT_CONTEXT_TOKEN_LIMIT`
- order 192: `TOKEN_THRESHOLD` (constant), lines 364-364, exports `TOKEN_THRESHOLD`
- order 193: `CONTEXT_AUTO_COMPACT_RESERVE_RATIO` (constant), lines 365-368, exports `CONTEXT_AUTO_COMPACT_RESERVE_RATIO`
- order 194: `CONTEXT_ESTIMATE_SAFETY_MULTIPLIER` (constant), lines 369-372, exports `CONTEXT_ESTIMATE_SAFETY_MULTIPLIER`
- order 195: `CONTEXT_USAGE_CALIBRATION_MAX` (constant), lines 373-376, exports `CONTEXT_USAGE_CALIBRATION_MAX`
- order 196: `CONTEXT_ACTUAL_USAGE_RECENT_SECONDS` (constant), lines 377-380, exports `CONTEXT_ACTUAL_USAGE_RECENT_SECONDS`
- order 197: `LARGE_FILE_AUTO_PAGE_BYTES` (constant), lines 381-384, exports `LARGE_FILE_AUTO_PAGE_BYTES`
- order 198: `LARGE_FILE_AUTO_PAGE_LINES` (constant), lines 385-388, exports `LARGE_FILE_AUTO_PAGE_LINES`
- order 199: `LARGE_SOURCE_UPLOAD_EXCERPT_CHARS` (constant), lines 389-392, exports `LARGE_SOURCE_UPLOAD_EXCERPT_CHARS`
- order 200: `CHAT_UPLOAD_PARSE_QUEUE_MAX` (constant), lines 393-396, exports `CHAT_UPLOAD_PARSE_QUEUE_MAX`
- order 201: `CHAT_UPLOAD_PARSE_TIMEOUT_SECONDS` (constant), lines 397-400, exports `CHAT_UPLOAD_PARSE_TIMEOUT_SECONDS`
- order 202: `CHAT_UPLOAD_INLINE_TEXT_BYTES` (constant), lines 401-404, exports `CHAT_UPLOAD_INLINE_TEXT_BYTES`
- order 203: `CHAT_UPLOAD_PARSE_MAX_BYTES` (constant), lines 405-411, exports `CHAT_UPLOAD_PARSE_MAX_BYTES`
- order 204: `CHAT_UPLOAD_ZIP_ENTRY_MAX_BYTES` (constant), lines 412-418, exports `CHAT_UPLOAD_ZIP_ENTRY_MAX_BYTES`
- order 205: `CHAT_UPLOAD_TEXT_CONTEXT_CHARS` (constant), lines 419-422, exports `CHAT_UPLOAD_TEXT_CONTEXT_CHARS`
- order 206: `CHAT_UPLOAD_PROMPT_MAX_FILES` (constant), lines 423-426, exports `CHAT_UPLOAD_PROMPT_MAX_FILES`
- order 207: `CHAT_UPLOAD_PROMPT_MAX_CHARS` (constant), lines 427-430, exports `CHAT_UPLOAD_PROMPT_MAX_CHARS`
- order 208: `CHAT_UPLOAD_PROMPT_PER_FILE_CHARS` (constant), lines 431-434, exports `CHAT_UPLOAD_PROMPT_PER_FILE_CHARS`
- order 209: `CHAT_UPLOAD_FRONTEND_WAIT_MS` (constant), lines 435-438, exports `CHAT_UPLOAD_FRONTEND_WAIT_MS`
- order 210: `CHAT_UPLOAD_AUTO_LIBRARY_INGEST` (constant), lines 439-442, exports `CHAT_UPLOAD_AUTO_LIBRARY_INGEST`
- order 211: `CHAT_UPLOAD_INGEST_QUEUE_MAX` (constant), lines 443-446, exports `CHAT_UPLOAD_INGEST_QUEUE_MAX`
- order 212: `SESSION_SUBMIT_LOCK_TIMEOUT_SECONDS` (constant), lines 447-450, exports `SESSION_SUBMIT_LOCK_TIMEOUT_SECONDS`
- order 213: `SESSION_DEFERRED_START_QUEUE_MAX` (constant), lines 451-454, exports `SESSION_DEFERRED_START_QUEUE_MAX`
- order 214: `SESSION_WATCHDOG_INTERVAL_SECONDS` (constant), lines 455-458, exports `SESSION_WATCHDOG_INTERVAL_SECONDS`
- order 215: `SESSION_HEARTBEAT_STALE_SECONDS` (constant), lines 459-462, exports `SESSION_HEARTBEAT_STALE_SECONDS`
- order 216: `SESSION_LIST_DEFAULT_LIMIT` (constant), lines 463-466, exports `SESSION_LIST_DEFAULT_LIMIT`
- order 217: `IDLE_TIMEOUT` (constant), lines 467-467, exports `IDLE_TIMEOUT`
- order 218: `POLL_INTERVAL` (constant), lines 468-468, exports `POLL_INTERVAL`
- order 219: `SSE_HEARTBEAT_SECONDS` (constant), lines 469-469, exports `SSE_HEARTBEAT_SECONDS`
- order 220: `MODEL_CALL_PROGRESS_DELAY` (constant), lines 470-470, exports `MODEL_CALL_PROGRESS_DELAY`
- order 221: `MODEL_CALL_PROGRESS_INTERVAL` (constant), lines 471-471, exports `MODEL_CALL_PROGRESS_INTERVAL`
- order 222: `RUN_COMPLETION_SUMMARY_ENABLED` (constant), lines 472-475, exports `RUN_COMPLETION_SUMMARY_ENABLED`
- order 223: `LLM_HTTP_RETRY_MAX_ATTEMPTS` (constant), lines 476-479, exports `LLM_HTTP_RETRY_MAX_ATTEMPTS`
- order 224: `LLM_HTTP_RETRY_DELAY_SECONDS` (constant), lines 480-483, exports `LLM_HTTP_RETRY_DELAY_SECONDS`
- order 225: `LLM_HTTP_RETRY_MAX_SECONDS` (constant), lines 484-487, exports `LLM_HTTP_RETRY_MAX_SECONDS`
- order 226: `LLM_HTTP_RETRY_404_ON_VLLM` (constant), lines 488-491, exports `LLM_HTTP_RETRY_404_ON_VLLM`
- order 227: `LLM_HTTP_RETRY_STATUSES` (constant), lines 492-492, exports `LLM_HTTP_RETRY_STATUSES`
- order 228: `MAX_AGENT_ROUNDS` (constant), lines 493-493, exports `MAX_AGENT_ROUNDS`
- order 229: `MIN_AGENT_ROUNDS` (constant), lines 494-494, exports `MIN_AGENT_ROUNDS`
- order 230: `MAX_AGENT_ROUNDS_CAP` (constant), lines 495-495, exports `MAX_AGENT_ROUNDS_CAP`
- order 231: `REPEATED_TOOL_LOOP_THRESHOLD` (constant), lines 496-496, exports `REPEATED_TOOL_LOOP_THRESHOLD`
- order 232: `BASH_READ_LOOP_THRESHOLD` (constant), lines 497-497, exports `BASH_READ_LOOP_THRESHOLD`
- order 233: `READ_FILE_LOOP_THRESHOLD` (constant), lines 498-498, exports `READ_FILE_LOOP_THRESHOLD`
- order 234: `READ_FILE_LOOP_DISTINCT_SOFT_LIMIT` (constant), lines 499-499, exports `READ_FILE_LOOP_DISTINCT_SOFT_LIMIT`
- order 235: `READ_FILE_COMPACT_PIN_DISTINCT` (constant), lines 500-500, exports `READ_FILE_COMPACT_PIN_DISTINCT`
- order 236: `READ_FILE_COMPACT_PIN_MAX_CHARS` (constant), lines 501-501, exports `READ_FILE_COMPACT_PIN_MAX_CHARS`
- order 237: `READ_CONTEXT_REGISTRY_MAX` (constant), lines 502-502, exports `READ_CONTEXT_REGISTRY_MAX`
- order 238: `READ_CONTEXT_PROMPT_MAX_ITEMS` (constant), lines 503-503, exports `READ_CONTEXT_PROMPT_MAX_ITEMS`
- order 239: `READ_CONTEXT_PROMPT_MAX_CHARS` (constant), lines 504-504, exports `READ_CONTEXT_PROMPT_MAX_CHARS`
- order 240: `READ_CONTEXT_SUMMARY_MAX_CHARS` (constant), lines 505-505, exports `READ_CONTEXT_SUMMARY_MAX_CHARS`
- order 241: `READ_CONTEXT_SHARED_MAX_ITEMS` (constant), lines 506-506, exports `READ_CONTEXT_SHARED_MAX_ITEMS`
- order 242: `READ_CONTEXT_POLICY_CHOICES` (constant), lines 507-507, exports `READ_CONTEXT_POLICY_CHOICES`
- order 243: `DEFAULT_READ_CONTEXT_POLICY` (constant), lines 508-508, exports `DEFAULT_READ_CONTEXT_POLICY`
- order 244: `TOOL_MEMORY_REGISTRY_MAX` (constant), lines 509-509, exports `TOOL_MEMORY_REGISTRY_MAX`
- order 245: `TOOL_MEMORY_PROMPT_MAX_ITEMS` (constant), lines 510-510, exports `TOOL_MEMORY_PROMPT_MAX_ITEMS`
- order 246: `TOOL_MEMORY_PROMPT_MAX_CHARS` (constant), lines 511-511, exports `TOOL_MEMORY_PROMPT_MAX_CHARS`
- order 247: `TOOL_MEMORY_SUMMARY_MAX_CHARS` (constant), lines 512-512, exports `TOOL_MEMORY_SUMMARY_MAX_CHARS`
- order 248: `TOOL_MEMORY_SHARED_MAX_ITEMS` (constant), lines 513-513, exports `TOOL_MEMORY_SHARED_MAX_ITEMS`
- order 249: `TOOL_MEMORY_COMPACT_PIN_DISTINCT` (constant), lines 514-514, exports `TOOL_MEMORY_COMPACT_PIN_DISTINCT`
- order 250: `TOOL_MEMORY_COMPACT_PIN_MAX_CHARS` (constant), lines 515-515, exports `TOOL_MEMORY_COMPACT_PIN_MAX_CHARS`
- order 251: `TOOL_MEMORY_POLICY_CHOICES` (constant), lines 516-516, exports `TOOL_MEMORY_POLICY_CHOICES`
- order 252: `DEFAULT_TOOL_MEMORY_POLICY` (constant), lines 517-517, exports `DEFAULT_TOOL_MEMORY_POLICY`
- order 253: `DEFAULT_AUTO_TASK_LEVEL_CEILING` (constant), lines 518-518, exports `DEFAULT_AUTO_TASK_LEVEL_CEILING`
- order 254: `HARD_BREAK_TOOL_ERROR_THRESHOLD` (constant), lines 519-519, exports `HARD_BREAK_TOOL_ERROR_THRESHOLD`
- order 255: `HARD_BREAK_RECOVERY_ROUND_THRESHOLD` (constant), lines 520-522, exports `HARD_BREAK_RECOVERY_ROUND_THRESHOLD`
- order 256: `FUSED_FAULT_BREAK_THRESHOLD` (constant), lines 523-523, exports `FUSED_FAULT_BREAK_THRESHOLD`
- order 257: `STALL_SEVERITY_ESCALATION_THRESHOLD` (constant), lines 524-524, exports `STALL_SEVERITY_ESCALATION_THRESHOLD`
- order 258: `STALL_SEVERITY_WEIGHT_BASH_READ_LOOP` (constant), lines 525-525, exports `STALL_SEVERITY_WEIGHT_BASH_READ_LOOP`
- order 259: `STALL_SEVERITY_WEIGHT_REPEATED_TOOL` (constant), lines 526-526, exports `STALL_SEVERITY_WEIGHT_REPEATED_TOOL`
- order 260: `STALL_SEVERITY_WEIGHT_FAULT` (constant), lines 527-527, exports `STALL_SEVERITY_WEIGHT_FAULT`
- order 261: `STALL_SEVERITY_WEIGHT_RECOVERY_RETRY` (constant), lines 528-528, exports `STALL_SEVERITY_WEIGHT_RECOVERY_RETRY`
- order 262: `STALL_SEVERITY_WEIGHT_WATCHDOG` (constant), lines 529-529, exports `STALL_SEVERITY_WEIGHT_WATCHDOG`
- order 263: `STALL_SEVERITY_DECAY_ON_SUCCESS` (constant), lines 530-530, exports `STALL_SEVERITY_DECAY_ON_SUCCESS`
- order 264: `STALL_ESCALATION_MIN_LEVEL` (constant), lines 531-531, exports `STALL_ESCALATION_MIN_LEVEL`
- order 265: `STALL_PLAN_SYNTHESIS_MAX_TOKENS` (constant), lines 532-532, exports `STALL_PLAN_SYNTHESIS_MAX_TOKENS`
- order 266: `STALL_ESCALATION_CONTEXT_MAX_CHARS` (constant), lines 533-533, exports `STALL_ESCALATION_CONTEXT_MAX_CHARS`
- order 267: `MAX_RUN_SECONDS` (constant), lines 534-534, exports `MAX_RUN_SECONDS`
- order 268: `MIN_RUN_TIMEOUT_SECONDS` (constant), lines 535-535, exports `MIN_RUN_TIMEOUT_SECONDS`
- order 269: `MAX_RUN_TIMEOUT_SECONDS` (constant), lines 536-536, exports `MAX_RUN_TIMEOUT_SECONDS`
- order 270: `MIN_TIMEOUT_SECONDS` (constant), lines 537-537, exports `MIN_TIMEOUT_SECONDS`
- order 271: `MAX_TIMEOUT_SECONDS` (constant), lines 538-538, exports `MAX_TIMEOUT_SECONDS`
- order 272: `DEFAULT_TIMEOUT_SECONDS` (constant), lines 539-545, exports `DEFAULT_TIMEOUT_SECONDS`
- order 273: `DEFAULT_REQUEST_TIMEOUT` (constant), lines 546-546, exports `DEFAULT_REQUEST_TIMEOUT`
- order 274: `_SHELL_AUTO_CONFIRM_PATTERNS` (assignment), lines 547-562, exports `_SHELL_AUTO_CONFIRM_PATTERNS`
- order 275: `MIN_SHELL_COMMAND_TIMEOUT_SECONDS` (constant), lines 563-563, exports `MIN_SHELL_COMMAND_TIMEOUT_SECONDS`
- order 276: `MAX_SHELL_COMMAND_TIMEOUT_SECONDS` (constant), lines 564-564, exports `MAX_SHELL_COMMAND_TIMEOUT_SECONDS`
- order 277: `DEFAULT_SHELL_COMMAND_TIMEOUT_SECONDS` (constant), lines 565-579, exports `DEFAULT_SHELL_COMMAND_TIMEOUT_SECONDS`
- order 278: `DEFAULT_SINGLE_NO_PLAN_TODO_PROMPT` (constant), lines 580-594, exports `DEFAULT_SINGLE_NO_PLAN_TODO_PROMPT`
- order 279: `SINGLE_NO_PLAN_TODO_BOOTSTRAP_MAX_ATTEMPTS` (constant), lines 595-595, exports `SINGLE_NO_PLAN_TODO_BOOTSTRAP_MAX_ATTEMPTS`
- order 280: `AUTO_CONTINUE_BUDGET_DEFAULT` (constant), lines 596-596, exports `AUTO_CONTINUE_BUDGET_DEFAULT`
- order 281: `AGENT_MAX_OUTPUT_TOKENS` (constant), lines 597-597, exports `AGENT_MAX_OUTPUT_TOKENS`
- order 282: `OLLAMA_THINKING_TOOL_BUFFER` (constant), lines 598-598, exports `OLLAMA_THINKING_TOOL_BUFFER`
- order 283: `WATCHDOG_INTENT_NO_TOOL_THRESHOLD` (constant), lines 599-599, exports `WATCHDOG_INTENT_NO_TOOL_THRESHOLD`
- order 284: `WATCHDOG_REPEAT_NO_TOOL_THRESHOLD` (constant), lines 600-600, exports `WATCHDOG_REPEAT_NO_TOOL_THRESHOLD`
- order 285: `WATCHDOG_INTENT_NO_TOOL_THRESHOLD_SINGLE` (constant), lines 601-601, exports `WATCHDOG_INTENT_NO_TOOL_THRESHOLD_SINGLE`
- order 286: `WATCHDOG_REPEAT_NO_TOOL_THRESHOLD_SINGLE` (constant), lines 602-602, exports `WATCHDOG_REPEAT_NO_TOOL_THRESHOLD_SINGLE`
- order 287: `WATCHDOG_STATE_STALL_THRESHOLD` (constant), lines 603-603, exports `WATCHDOG_STATE_STALL_THRESHOLD`
- order 288: `WATCHDOG_CONTEXT_STALL_THRESHOLD` (constant), lines 604-604, exports `WATCHDOG_CONTEXT_STALL_THRESHOLD`
- order 289: `WATCHDOG_REPEAT_SIMILARITY_THRESHOLD` (constant), lines 605-605, exports `WATCHDOG_REPEAT_SIMILARITY_THRESHOLD`
- order 290: `WATCHDOG_CONTEXT_NEAR_RATIO` (constant), lines 606-606, exports `WATCHDOG_CONTEXT_NEAR_RATIO`
- order 291: `WATCHDOG_MAX_DECOMPOSE_STEPS` (constant), lines 607-607, exports `WATCHDOG_MAX_DECOMPOSE_STEPS`
- order 292: `WATCHDOG_STEP_MAX_ATTEMPTS` (constant), lines 608-608, exports `WATCHDOG_STEP_MAX_ATTEMPTS`
- order 293: `EMPTY_ACTION_MIN_CONTENT_CHARS` (constant), lines 609-609, exports `EMPTY_ACTION_MIN_CONTENT_CHARS`
- order 294: `EMPTY_ACTION_WAKEUP_RETRY_LIMIT` (constant), lines 610-610, exports `EMPTY_ACTION_WAKEUP_RETRY_LIMIT`
- order 295: `THINKING_BUDGET_FORCE_RATIO` (constant), lines 611-611, exports `THINKING_BUDGET_FORCE_RATIO`
- order 296: `_TOOL_TIMEOUT_MAP` (assignment), lines 612-630, exports `_TOOL_TIMEOUT_MAP`
- order 297: `_DEFAULT_TOOL_TIMEOUT` (assignment), lines 631-631, exports `_DEFAULT_TOOL_TIMEOUT`
- order 298: `CONVERSATION_VISIBLE_TOOL_EVENTS` (constant), lines 632-642, exports `CONVERSATION_VISIBLE_TOOL_EVENTS`
- order 299: `PERSIST_ON_EVENT_TYPES` (constant), lines 643-658, exports `PERSIST_ON_EVENT_TYPES`
- order 300: `PERSIST_EVENT_MIN_INTERVAL_SECONDS` (constant), lines 659-659, exports `PERSIST_EVENT_MIN_INTERVAL_SECONDS`
- order 301: `TRUNCATION_CONTINUATION_MAX_PASSES` (constant), lines 660-660, exports `TRUNCATION_CONTINUATION_MAX_PASSES`
- order 302: `TRUNCATION_CONTINUATION_MAX_TOKENS` (constant), lines 661-661, exports `TRUNCATION_CONTINUATION_MAX_TOKENS`
- order 303: `TRUNCATION_CONTINUATION_TAIL_CHARS` (constant), lines 662-662, exports `TRUNCATION_CONTINUATION_TAIL_CHARS`
- order 304: `TRUNCATION_CONTINUATION_ECHO_CHARS` (constant), lines 663-663, exports `TRUNCATION_CONTINUATION_ECHO_CHARS`
- order 305: `TRUNCATION_OVERLAP_SCAN_CHARS` (constant), lines 664-664, exports `TRUNCATION_OVERLAP_SCAN_CHARS`
- order 306: `TRUNCATION_PAIR_SCAN_CHARS` (constant), lines 665-665, exports `TRUNCATION_PAIR_SCAN_CHARS`
- order 307: `TRUNCATION_LIVE_BUFFER_MAX_CHARS` (constant), lines 666-666, exports `TRUNCATION_LIVE_BUFFER_MAX_CHARS`
- order 308: `MIN_CONTEXT_TOKEN_LIMIT` (constant), lines 667-667, exports `MIN_CONTEXT_TOKEN_LIMIT`
- order 309: `COMPACT_TIER1_PCT` (constant), lines 668-669, exports `COMPACT_TIER1_PCT`
- order 310: `COMPACT_TIER2_PCT` (constant), lines 670-670, exports `COMPACT_TIER2_PCT`
- order 311: `COMPACT_TIER3_PCT` (constant), lines 671-671, exports `COMPACT_TIER3_PCT`
- order 312: `COMPACT_TIER1_ABS` (constant), lines 672-673, exports `COMPACT_TIER1_ABS`
- order 313: `COMPACT_TIER2_ABS` (constant), lines 674-674, exports `COMPACT_TIER2_ABS`
- order 314: `CONTEXT_COMPACT_INEFFECTIVE_COOLDOWN_SECONDS` (constant), lines 675-681, exports `CONTEXT_COMPACT_INEFFECTIVE_COOLDOWN_SECONDS`
- order 315: `FILE_BUFFER_CONTENT_THRESHOLD` (constant), lines 682-683, exports `FILE_BUFFER_CONTENT_THRESHOLD`
- order 316: `FILE_BUFFER_MAX_FILES` (constant), lines 684-684, exports `FILE_BUFFER_MAX_FILES`
- order 317: `AUTHORITATIVE_USER_GOAL_OPEN` (constant), lines 685-685, exports `AUTHORITATIVE_USER_GOAL_OPEN`
- order 318: `AUTHORITATIVE_USER_GOAL_CLOSE` (constant), lines 686-686, exports `AUTHORITATIVE_USER_GOAL_CLOSE`
- order 319: `AGENT_MSG_LIMIT_TIER0` (constant), lines 687-688, exports `AGENT_MSG_LIMIT_TIER0`
- order 320: `AGENT_MSG_LIMIT_TIER1` (constant), lines 689-689, exports `AGENT_MSG_LIMIT_TIER1`
- order 321: `AGENT_MSG_LIMIT_TIER2` (constant), lines 690-690, exports `AGENT_MSG_LIMIT_TIER2`
- order 322: `AGENT_MSG_LIMIT_TIER3` (constant), lines 691-691, exports `AGENT_MSG_LIMIT_TIER3`
- order 323: `AGENT_CTX_LIMIT_TIER0` (constant), lines 692-692, exports `AGENT_CTX_LIMIT_TIER0`
- order 324: `AGENT_CTX_LIMIT_TIER1` (constant), lines 693-693, exports `AGENT_CTX_LIMIT_TIER1`
- order 325: `AGENT_CTX_LIMIT_TIER2` (constant), lines 694-694, exports `AGENT_CTX_LIMIT_TIER2`
- order 326: `AGENT_CTX_LIMIT_TIER3` (constant), lines 695-695, exports `AGENT_CTX_LIMIT_TIER3`
- order 327: `MANAGER_CTX_LIMIT_TIER0` (constant), lines 696-696, exports `MANAGER_CTX_LIMIT_TIER0`
- order 328: `MANAGER_CTX_LIMIT_TIER1` (constant), lines 697-697, exports `MANAGER_CTX_LIMIT_TIER1`
- order 329: `MANAGER_CTX_LIMIT_TIER2` (constant), lines 698-698, exports `MANAGER_CTX_LIMIT_TIER2`
- order 330: `MANAGER_CTX_LIMIT_TIER3` (constant), lines 699-699, exports `MANAGER_CTX_LIMIT_TIER3`
- order 331: `MAX_CONTEXT_ARCHIVE_SEGMENTS` (constant), lines 700-700, exports `MAX_CONTEXT_ARCHIVE_SEGMENTS`
- order 332: `MAX_USER_BUBBLE_LOG` (constant), lines 701-702, exports `MAX_USER_BUBBLE_LOG`
- order 333: `MANAGER_INSTRUCTION_MAX_CHARS` (constant), lines 703-707, exports `MANAGER_INSTRUCTION_MAX_CHARS`
- order 334: `MANAGER_MOMENTUM_MAX_SKIPS` (constant), lines 708-713, exports `MANAGER_MOMENTUM_MAX_SKIPS`
- order 335: `MODEL_OUTPUT_RETRY_TIMES` (constant), lines 714-718, exports `MODEL_OUTPUT_RETRY_TIMES`
- order 336: `ARBITER_TRIGGER_MIN_CONTENT_CHARS` (constant), lines 719-719, exports `ARBITER_TRIGGER_MIN_CONTENT_CHARS`
- order 337: `ARBITER_VALID_PLANNING_STREAK_LIMIT` (constant), lines 720-720, exports `ARBITER_VALID_PLANNING_STREAK_LIMIT`
- order 338: `ARBITER_DEFAULT_TIMEOUT_SECONDS` (constant), lines 721-721, exports `ARBITER_DEFAULT_TIMEOUT_SECONDS`
- order 339: `ARBITER_DEFAULT_MAX_TOKENS` (constant), lines 722-722, exports `ARBITER_DEFAULT_MAX_TOKENS`
- order 340: `ARBITER_DEFAULT_TEMPERATURE` (constant), lines 723-723, exports `ARBITER_DEFAULT_TEMPERATURE`
- order 341: `LIVE_INPUT_DELAY_WRITE_ROUNDS` (constant), lines 724-724, exports `LIVE_INPUT_DELAY_WRITE_ROUNDS`
- order 342: `LIVE_INPUT_DELAY_TOOL_ROUNDS` (constant), lines 725-725, exports `LIVE_INPUT_DELAY_TOOL_ROUNDS`
- order 343: `LIVE_INPUT_DELAY_NORMAL_ROUNDS` (constant), lines 726-726, exports `LIVE_INPUT_DELAY_NORMAL_ROUNDS`
- order 344: `LIVE_INPUT_MAX_INJECTIONS` (constant), lines 727-727, exports `LIVE_INPUT_MAX_INJECTIONS`
- order 345: `LIVE_INPUT_REINJECT_INTERVAL` (constant), lines 728-728, exports `LIVE_INPUT_REINJECT_INTERVAL`
- order 346: `LIVE_INPUT_WEIGHT_BASE_DELAYED` (constant), lines 729-729, exports `LIVE_INPUT_WEIGHT_BASE_DELAYED`
- order 347: `LIVE_INPUT_WEIGHT_BASE_NORMAL` (constant), lines 730-730, exports `LIVE_INPUT_WEIGHT_BASE_NORMAL`
- order 348: `LIVE_INPUT_WEIGHT_STEP_DELAYED` (constant), lines 731-731, exports `LIVE_INPUT_WEIGHT_STEP_DELAYED`
- order 349: `LIVE_INPUT_WEIGHT_STEP_NORMAL` (constant), lines 732-732, exports `LIVE_INPUT_WEIGHT_STEP_NORMAL`
- order 351: `BENIGN_SOCKET_DEBUG_LOG_ENABLED` (constant), lines 739-745, exports `BENIGN_SOCKET_DEBUG_LOG_ENABLED`
- order 352: `BENIGN_SOCKET_LOG_INTERVAL_SECONDS` (constant), lines 746-746, exports `BENIGN_SOCKET_LOG_INTERVAL_SECONDS`
- order 353: `FINAL_SUMMARY_MIN_CHARS` (constant), lines 747-747, exports `FINAL_SUMMARY_MIN_CHARS`
- order 354: `FINAL_SUMMARY_STRICT_MIN_CHARS` (constant), lines 748-748, exports `FINAL_SUMMARY_STRICT_MIN_CHARS`
- order 355: `RUNTIME_CONTROL_HINT_PREFIXES` (constant), lines 749-768, exports `RUNTIME_CONTROL_HINT_PREFIXES`
- order 356: `RETRY_RUNTIME_HINT_PREFIXES` (constant), lines 769-783, exports `RETRY_RUNTIME_HINT_PREFIXES`
- order 357: `EXECUTION_MODE_SINGLE` (constant), lines 784-784, exports `EXECUTION_MODE_SINGLE`
- order 358: `EXECUTION_MODE_SEQUENTIAL` (constant), lines 785-785, exports `EXECUTION_MODE_SEQUENTIAL`
- order 359: `EXECUTION_MODE_SYNC` (constant), lines 786-786, exports `EXECUTION_MODE_SYNC`
- order 360: `EXECUTION_MODE_CHOICES` (constant), lines 787-791, exports `EXECUTION_MODE_CHOICES`
- order 361: `AGENT_ROLES` (constant), lines 792-792, exports `AGENT_ROLES`
- order 362: `AGENT_BUBBLE_ROLES` (constant), lines 793-793, exports `AGENT_BUBBLE_ROLES`
- order 363: `AGENT_ROLE_LABELS` (constant), lines 794-800, exports `AGENT_ROLE_LABELS`
- order 364: `AGENT_ROLE_BUBBLE_COLORS` (constant), lines 801-807, exports `AGENT_ROLE_BUBBLE_COLORS`
- order 365: `BLACKBOARD_STATUSES` (constant), lines 808-817, exports `BLACKBOARD_STATUSES`
- order 366: `TASK_COMPLEXITY_LEVELS` (constant), lines 818-818, exports `TASK_COMPLEXITY_LEVELS`
- order 367: `TASK_COMPLEXITY_RANKS` (constant), lines 819-824, exports `TASK_COMPLEXITY_RANKS`
- order 368: `TASK_PROFILE_TYPES` (constant), lines 825-831, exports `TASK_PROFILE_TYPES`
- order 369: `TASK_LEVEL_CHOICES` (constant), lines 832-832, exports `TASK_LEVEL_CHOICES`
- order 370: `TASK_SCALE_PREFERENCES` (constant), lines 833-833, exports `TASK_SCALE_PREFERENCES`
- order 371: `SEMANTIC_CONFIDENCE_CHOICES` (constant), lines 834-834, exports `SEMANTIC_CONFIDENCE_CHOICES`
- order 372: `L2_TODO_POLICY_CHOICES` (constant), lines 835-839, exports `L2_TODO_POLICY_CHOICES`
- order 373: `DEFAULT_L2_TODO_POLICY` (constant), lines 840-840, exports `DEFAULT_L2_TODO_POLICY`
- order 374: `TASK_LEVEL_POLICIES` (constant), lines 841-894, exports `TASK_LEVEL_POLICIES`
- order 375: `MANAGER_ROUTE_TARGETS` (constant), lines 895-895, exports `MANAGER_ROUTE_TARGETS`
- order 376: `BLACKBOARD_MAX_LOG_ENTRIES` (constant), lines 896-896, exports `BLACKBOARD_MAX_LOG_ENTRIES`
- order 377: `BLACKBOARD_MAX_TEXT` (constant), lines 897-897, exports `BLACKBOARD_MAX_TEXT`
- order 378: `BLACKBOARD_MEMORY_SHORT_MAX` (constant), lines 898-898, exports `BLACKBOARD_MEMORY_SHORT_MAX`
- order 379: `BLACKBOARD_MEMORY_MID_MAX_STEPS` (constant), lines 899-899, exports `BLACKBOARD_MEMORY_MID_MAX_STEPS`
- order 380: `BLACKBOARD_MEMORY_MID_ITEMS_PER_STEP` (constant), lines 900-900, exports `BLACKBOARD_MEMORY_MID_ITEMS_PER_STEP`
- order 381: `BLACKBOARD_MEMORY_LONG_MAX` (constant), lines 901-901, exports `BLACKBOARD_MEMORY_LONG_MAX`
- order 382: `BLACKBOARD_MEMORY_INDEX_MAX` (constant), lines 902-902, exports `BLACKBOARD_MEMORY_INDEX_MAX`
- order 383: `SKILL_REFRESH_MIN_INTERVAL_SECONDS` (constant), lines 903-903, exports `SKILL_REFRESH_MIN_INTERVAL_SECONDS`
- order 384: `SKILL_PROMPT_MAX_ITEMS` (constant), lines 904-904, exports `SKILL_PROMPT_MAX_ITEMS`
- order 385: `SKILL_PROMPT_MAX_CHARS` (constant), lines 905-905, exports `SKILL_PROMPT_MAX_CHARS`
- order 386: `SKILL_RUNTIME_CACHE_MAX_ENTRIES` (constant), lines 906-906, exports `SKILL_RUNTIME_CACHE_MAX_ENTRIES`
- order 387: `SKILL_RUNTIME_CACHE_MAX_BYTES` (constant), lines 907-907, exports `SKILL_RUNTIME_CACHE_MAX_BYTES`
- order 388: `AUTO_SKILLS_ROOT_CANDIDATES` (constant), lines 908-908, exports `AUTO_SKILLS_ROOT_CANDIDATES`
- order 389: `SKILL_DEFAULT_ATTACHMENT_GLOBS` (constant), lines 909-939, exports `SKILL_DEFAULT_ATTACHMENT_GLOBS`
- order 390: `SKILL_INLINE_ATTACHMENT_MAX_FILES` (constant), lines 940-940, exports `SKILL_INLINE_ATTACHMENT_MAX_FILES`
- order 391: `SKILL_INLINE_ATTACHMENT_MAX_CHARS` (constant), lines 941-941, exports `SKILL_INLINE_ATTACHMENT_MAX_CHARS`
- order 392: `SKILL_RESOURCE_MANIFEST_MAX_ITEMS` (constant), lines 942-942, exports `SKILL_RESOURCE_MANIFEST_MAX_ITEMS`
- order 393: `SKILL_BODY_COMPACT_THRESHOLD_CHARS` (constant), lines 943-943, exports `SKILL_BODY_COMPACT_THRESHOLD_CHARS`
- order 394: `SKILL_BODY_PREVIEW_CHARS` (constant), lines 944-944, exports `SKILL_BODY_PREVIEW_CHARS`
- order 395: `SKILLS_VIRTUAL_PREFIX` (constant), lines 945-945, exports `SKILLS_VIRTUAL_PREFIX`
- order 396: `SKILLS_EXTERNAL_MOUNT` (constant), lines 946-946, exports `SKILLS_EXTERNAL_MOUNT`
- order 397: `PLAN_MODE_ENABLED_LEVELS` (constant), lines 947-947, exports `PLAN_MODE_ENABLED_LEVELS`
- order 398: `PLAN_MODE_FORCED_LEVELS` (constant), lines 948-948, exports `PLAN_MODE_FORCED_LEVELS`
- order 399: `PLAN_MODE_USER_CHOICES` (constant), lines 949-949, exports `PLAN_MODE_USER_CHOICES`
- order 400: `TASK_PHASES` (constant), lines 950-951, exports `TASK_PHASES`
- order 401: `TASK_PHASE_ROUTING` (constant), lines 952-959, exports `TASK_PHASE_ROUTING`
- order 402: `COMPLEXITY_KEYWORDS` (constant), lines 960-966, exports `COMPLEXITY_KEYWORDS`
- order 403: `USER_COMPLEXITY_SIMPLE_TOKENS` (constant), lines 967-971, exports `USER_COMPLEXITY_SIMPLE_TOKENS`
- order 404: `USER_COMPLEXITY_MODERATE_TOKENS` (constant), lines 972-976, exports `USER_COMPLEXITY_MODERATE_TOKENS`
- order 405: `USER_COMPLEXITY_COMPLEX_TOKENS` (constant), lines 977-981, exports `USER_COMPLEXITY_COMPLEX_TOKENS`
- order 406: `USER_COMPLEXITY_EXPERT_TOKENS` (constant), lines 982-986, exports `USER_COMPLEXITY_EXPERT_TOKENS`
- order 407: `PLAN_MODE_EXPLORER_MAX_ROUNDS` (constant), lines 987-990, exports `PLAN_MODE_EXPLORER_MAX_ROUNDS`
- order 408: `PLAN_MODE_EXPLORER_PRODUCTIVE_ROUNDS` (constant), lines 991-991, exports `PLAN_MODE_EXPLORER_PRODUCTIVE_ROUNDS`
- order 409: `PLAN_MODE_EXPLORER_STALE_ROUNDS` (constant), lines 992-992, exports `PLAN_MODE_EXPLORER_STALE_ROUNDS`
- order 410: `PLAN_MODE_SYNTHESIS_MAX_ATTEMPTS` (constant), lines 993-993, exports `PLAN_MODE_SYNTHESIS_MAX_ATTEMPTS`
- order 411: `REVIEWER_DEBUG_MODE_MAX_ROUNDS` (constant), lines 994-995, exports `REVIEWER_DEBUG_MODE_MAX_ROUNDS`
- order 412: `REVIEWER_DEBUG_TOOL_ALLOWLIST` (constant), lines 996-1000, exports `REVIEWER_DEBUG_TOOL_ALLOWLIST`
- order 413: `EXPLORER_STALL_THRESHOLD` (constant), lines 1001-1001, exports `EXPLORER_STALL_THRESHOLD`
- order 414: `DEVELOPER_EDIT_STALL_THRESHOLD` (constant), lines 1002-1002, exports `DEVELOPER_EDIT_STALL_THRESHOLD`
- order 415: `ACCEPTANCE_GATE_STALL_THRESHOLD` (constant), lines 1003-1006, exports `ACCEPTANCE_GATE_STALL_THRESHOLD`
- order 416: `ACCEPTANCE_GATE_HARD_CEILING` (constant), lines 1007-1010, exports `ACCEPTANCE_GATE_HARD_CEILING`
- order 417: `ACCEPTANCE_GATE_TOTAL_ROUND_CEILING` (constant), lines 1011-1011, exports `ACCEPTANCE_GATE_TOTAL_ROUND_CEILING`
- order 418: `PLAN_MODE_MANAGER_SYNTHESIS_MAX_TOKENS` (constant), lines 1012-1012, exports `PLAN_MODE_MANAGER_SYNTHESIS_MAX_TOKENS`
- order 419: `PLAN_MODE_MAX_OPTIONS` (constant), lines 1013-1013, exports `PLAN_MODE_MAX_OPTIONS`
- order 420: `PLAN_FILE_RELATIVE_PATH` (constant), lines 1014-1014, exports `PLAN_FILE_RELATIVE_PATH`
- order 421: `PLAN_BUBBLE_MAX_CHARS` (constant), lines 1015-1015, exports `PLAN_BUBBLE_MAX_CHARS`
- order 422: `PLAN_NOTICE_BODY_MAX_CHARS` (constant), lines 1016-1016, exports `PLAN_NOTICE_BODY_MAX_CHARS`
- order 423: `PLAN_MESSAGE_EVENT_MAX_CHARS` (constant), lines 1017-1017, exports `PLAN_MESSAGE_EVENT_MAX_CHARS`
- order 424: `PLAN_STEP_FULL_CONTENT_MAX_CHARS` (constant), lines 1018-1018, exports `PLAN_STEP_FULL_CONTENT_MAX_CHARS`
- order 425: `PLAN_MODE_RESEARCH_TOOL_ALLOWLIST` (constant), lines 1019-1026, exports `PLAN_MODE_RESEARCH_TOOL_ALLOWLIST`
- order 426: `FAILURE_LEDGER_MAX_FIXES` (constant), lines 1027-1027, exports `FAILURE_LEDGER_MAX_FIXES`
- order 427: `FAILURE_LEDGER_MAX_COMPILE_ERRORS` (constant), lines 1028-1028, exports `FAILURE_LEDGER_MAX_COMPILE_ERRORS`
- order 428: `FAILURE_LEDGER_MAX_DELEGATIONS` (constant), lines 1029-1029, exports `FAILURE_LEDGER_MAX_DELEGATIONS`
- order 429: `FAILURE_LEDGER_MAX_STALLS` (constant), lines 1030-1030, exports `FAILURE_LEDGER_MAX_STALLS`
- order 430: `FAILURE_LEDGER_MAX_TOOL_FPS` (constant), lines 1031-1031, exports `FAILURE_LEDGER_MAX_TOOL_FPS`
- order 431: `FAILURE_LEDGER_MAX_ERRORS` (constant), lines 1032-1032, exports `FAILURE_LEDGER_MAX_ERRORS`
- order 432: `ERROR_CATEGORY_DEFS` (constant), lines 1033-1072, exports `ERROR_CATEGORY_DEFS`
- order 433: `CHECKPOINT_MAX_COUNT` (constant), lines 1073-1073, exports `CHECKPOINT_MAX_COUNT`
- order 434: `CHECKPOINT_INTERVAL_ROUNDS` (constant), lines 1074-1074, exports `CHECKPOINT_INTERVAL_ROUNDS`
- order 435: `PERSISTED_ROUTES_MAX` (constant), lines 1075-1075, exports `PERSISTED_ROUTES_MAX`
- order 436: `HTML_FRONTEND_REQUEST_KEYWORDS` (constant), lines 1076-1115, exports `HTML_FRONTEND_REQUEST_KEYWORDS`
- order 437: `DEEP_RESEARCH_REQUEST_KEYWORDS` (constant), lines 1116-1138, exports `DEEP_RESEARCH_REQUEST_KEYWORDS`
- order 438: `DEEP_RESEARCH_RETRIEVAL_KEYWORDS` (constant), lines 1139-1158, exports `DEEP_RESEARCH_RETRIEVAL_KEYWORDS`
- order 439: `DEEP_RESEARCH_TEXT_ONLY_HINT_KEYWORDS` (constant), lines 1159-1176, exports `DEEP_RESEARCH_TEXT_ONLY_HINT_KEYWORDS`
- order 440: `DANGEROUS_PATTERNS` (constant), lines 1177-1178, exports `DANGEROUS_PATTERNS`
- order 441: `VALID_MSG_TYPES` (constant), lines 1179-1185, exports `VALID_MSG_TYPES`
- order 442: `SUPPORTED_UI_LANGUAGES` (constant), lines 1186-1192, exports `SUPPORTED_UI_LANGUAGES`
- order 443: `UI_LANGUAGE_LABELS` (constant), lines 1193-1193, exports `UI_LANGUAGE_LABELS`
- order 444: `DEFAULT_UI_LANGUAGE` (constant), lines 1194-1194, exports `DEFAULT_UI_LANGUAGE`
- order 445: `PUBLIC_TOOL_PROGRESS_SUMMARY_ENABLED` (constant), lines 1195-1197, exports `PUBLIC_TOOL_PROGRESS_SUMMARY_ENABLED`
- order 446: `AGENT_LANGUAGE_PREFERENCES` (constant), lines 1198-1239, exports `AGENT_LANGUAGE_PREFERENCES`
- order 447: `UI_STYLE_CHOICES` (constant), lines 1240-1240, exports `UI_STYLE_CHOICES`
- order 448: `UI_STYLE_LABELS` (constant), lines 1241-1241, exports `UI_STYLE_LABELS`
- order 449: `DEFAULT_UI_STYLE` (constant), lines 1242-1242, exports `DEFAULT_UI_STYLE`
- order 450: `DEFAULT_WEB_UI_DIR` (constant), lines 1243-1243, exports `DEFAULT_WEB_UI_DIR`
- order 451: `DEFAULT_WEB_UI_CONFIG` (constant), lines 1244-1244, exports `DEFAULT_WEB_UI_CONFIG`
- order 452: `WEB_UI_REQUIRED_FILES` (constant), lines 1245-1252, exports `WEB_UI_REQUIRED_FILES`
- order 453: `WEB_UI_OPTIONAL_FILES` (constant), lines 1253-1253, exports `WEB_UI_OPTIONAL_FILES`
- order 454: `WEB_UI_APPLICATION_CONTRACT_VERSION` (constant), lines 1254-1254, exports `WEB_UI_APPLICATION_CONTRACT_VERSION`
- order 455: `WEB_UI_APPLICATION_FEATURE_MARKERS` (constant), lines 1255-1274, exports `WEB_UI_APPLICATION_FEATURE_MARKERS`
- order 456: `IMAGE_EXTS` (constant), lines 1275-1289, exports `IMAGE_EXTS`
- order 457: `IMAGE_FORMATS_NEED_CONVERSION` (constant), lines 1290-1290, exports `IMAGE_FORMATS_NEED_CONVERSION`
- order 458: `IMAGE_SAFE_FORMATS` (constant), lines 1291-1291, exports `IMAGE_SAFE_FORMATS`
- order 459: `AUDIO_EXTS` (constant), lines 1292-1302, exports `AUDIO_EXTS`
- order 460: `VIDEO_EXTS` (constant), lines 1303-1313, exports `VIDEO_EXTS`
- order 461: `CODE_PREVIEW_STAGE_MAX_BYTES` (constant), lines 1314-1314, exports `CODE_PREVIEW_STAGE_MAX_BYTES`
- order 462: `CODE_PREVIEW_STAGE_MAX_ROWS` (constant), lines 1315-1315, exports `CODE_PREVIEW_STAGE_MAX_ROWS`
- order 463: `CODE_PREVIEW_STAGE_MAX_PER_FILE` (constant), lines 1316-1316, exports `CODE_PREVIEW_STAGE_MAX_PER_FILE`
- order 464: `CODE_PREVIEW_STAGE_MAX_TOTAL` (constant), lines 1317-1317, exports `CODE_PREVIEW_STAGE_MAX_TOTAL`
- order 465: `CODE_PREVIEW_DIFF_CONTEXT_LINES` (constant), lines 1318-1318, exports `CODE_PREVIEW_DIFF_CONTEXT_LINES`
- order 466: `CODE_PREVIEW_DIFF_MERGE_GAP` (constant), lines 1319-1319, exports `CODE_PREVIEW_DIFF_MERGE_GAP`
- order 467: `PREVIEW_DOWNLOAD_MAX_FILES` (constant), lines 1320-1320, exports `PREVIEW_DOWNLOAD_MAX_FILES`
- order 468: `PREVIEW_DOWNLOAD_MAX_BYTES` (constant), lines 1321-1321, exports `PREVIEW_DOWNLOAD_MAX_BYTES`
- order 469: `FILES_TREE_DEFAULT_MAX_NODES` (constant), lines 1322-1322, exports `FILES_TREE_DEFAULT_MAX_NODES`
- order 470: `FILES_TREE_DEFAULT_MAX_DEPTH` (constant), lines 1323-1323, exports `FILES_TREE_DEFAULT_MAX_DEPTH`
- order 471: `FILES_TREE_SKIP_DIRS` (constant), lines 1324-1332, exports `FILES_TREE_SKIP_DIRS`
- order 472: `FILES_TREE_SKIP_REL_DIRS` (constant), lines 1333-1335, exports `FILES_TREE_SKIP_REL_DIRS`
- order 473: `IDE_FILE_MAX_BYTES` (constant), lines 1336-1336, exports `IDE_FILE_MAX_BYTES`
- order 474: `IDE_UPLOAD_MAX_BYTES` (constant), lines 1337-1337, exports `IDE_UPLOAD_MAX_BYTES`
- order 475: `IDE_UPLOAD_TOTAL_MAX_BYTES` (constant), lines 1338-1338, exports `IDE_UPLOAD_TOTAL_MAX_BYTES`
- order 476: `IDE_UPLOAD_MAX_ITEMS` (constant), lines 1339-1339, exports `IDE_UPLOAD_MAX_ITEMS`
- order 477: `IDE_UPLOAD_CHUNK_MAX_BYTES` (constant), lines 1340-1340, exports `IDE_UPLOAD_CHUNK_MAX_BYTES`
- order 478: `IDE_UPLOAD_STREAM_MAX_BYTES` (constant), lines 1341-1341, exports `IDE_UPLOAD_STREAM_MAX_BYTES`
- order 479: `IDE_TEXT_PREVIEW_MAX_BYTES` (constant), lines 1342-1342, exports `IDE_TEXT_PREVIEW_MAX_BYTES`
- order 480: `IDE_MARKDOWN_PREVIEW_MAX_LINES` (constant), lines 1343-1343, exports `IDE_MARKDOWN_PREVIEW_MAX_LINES`
- order 481: `IDE_IMAGE_PREVIEW_MAX_EDGE` (constant), lines 1344-1344, exports `IDE_IMAGE_PREVIEW_MAX_EDGE`
- order 482: `IDE_IMAGE_PREVIEW_MAX_PIXELS` (constant), lines 1345-1345, exports `IDE_IMAGE_PREVIEW_MAX_PIXELS`
- order 483: `IDE_IMAGE_PREVIEW_SOURCE_MAX_PIXELS` (constant), lines 1346-1346, exports `IDE_IMAGE_PREVIEW_SOURCE_MAX_PIXELS`
- order 484: `IDE_VECTOR_PREVIEW_MAX_BYTES` (constant), lines 1347-1347, exports `IDE_VECTOR_PREVIEW_MAX_BYTES`
- order 485: `IDE_TABLE_PREVIEW_SOURCE_MAX_BYTES` (constant), lines 1348-1348, exports `IDE_TABLE_PREVIEW_SOURCE_MAX_BYTES`
- order 486: `IDE_TABLE_PREVIEW_CELL_MAX_CHARS` (constant), lines 1349-1349, exports `IDE_TABLE_PREVIEW_CELL_MAX_CHARS`
- order 487: `IDE_TABLE_PREVIEW_TOTAL_CHARS` (constant), lines 1350-1350, exports `IDE_TABLE_PREVIEW_TOTAL_CHARS`
- order 488: `IDE_OFFICE_PREVIEW_MAX_ENTRIES` (constant), lines 1351-1351, exports `IDE_OFFICE_PREVIEW_MAX_ENTRIES`
- order 489: `IDE_OFFICE_PREVIEW_MAX_EXPANDED_BYTES` (constant), lines 1352-1352, exports `IDE_OFFICE_PREVIEW_MAX_EXPANDED_BYTES`
- order 490: `IDE_OFFICE_PREVIEW_MAX_ENTRY_BYTES` (constant), lines 1353-1353, exports `IDE_OFFICE_PREVIEW_MAX_ENTRY_BYTES`
- order 491: `IDE_COMMAND_TIMEOUT_DEFAULT` (constant), lines 1354-1354, exports `IDE_COMMAND_TIMEOUT_DEFAULT`
- order 492: `IDE_TREE_DEFAULT_MAX_NODES` (constant), lines 1355-1355, exports `IDE_TREE_DEFAULT_MAX_NODES`
- order 493: `IDE_TREE_MAX_NODES` (constant), lines 1356-1356, exports `IDE_TREE_MAX_NODES`
- order 494: `IDE_SEARCH_MAX_RESULTS` (constant), lines 1357-1357, exports `IDE_SEARCH_MAX_RESULTS`
- order 495: `IDE_SEARCH_MAX_FILE_BYTES` (constant), lines 1358-1358, exports `IDE_SEARCH_MAX_FILE_BYTES`
- order 496: `IDE_TERMINAL_SCROLLBACK_BYTES` (constant), lines 1359-1359, exports `IDE_TERMINAL_SCROLLBACK_BYTES`
- order 497: `IDE_TERMINAL_IDLE_SECONDS` (constant), lines 1360-1360, exports `IDE_TERMINAL_IDLE_SECONDS`
- order 498: `IDE_DEBUG_ADAPTER_START_ATTEMPTS` (constant), lines 1361-1361, exports `IDE_DEBUG_ADAPTER_START_ATTEMPTS`
- order 499: `IDE_DEBUG_ADAPTER_START_TIMEOUT_SECONDS` (constant), lines 1362-1362, exports `IDE_DEBUG_ADAPTER_START_TIMEOUT_SECONDS`
- order 500: `IDE_VSIX_MAX_BYTES` (constant), lines 1363-1363, exports `IDE_VSIX_MAX_BYTES`
- order 501: `IDE_VSIX_MAX_EXPANDED_BYTES` (constant), lines 1364-1364, exports `IDE_VSIX_MAX_EXPANDED_BYTES`
- order 502: `IDE_VSIX_MAX_FILES` (constant), lines 1365-1365, exports `IDE_VSIX_MAX_FILES`
- order 503: `IDE_VSIX_MAX_FILE_BYTES` (constant), lines 1366-1366, exports `IDE_VSIX_MAX_FILE_BYTES`
- order 504: `IDE_TREE_SKIP_DIRS` (constant), lines 1367-1375, exports `IDE_TREE_SKIP_DIRS`
- order 505: `RENDER_FRAME_MAX_B64_CHARS` (constant), lines 1376-1376, exports `RENDER_FRAME_MAX_B64_CHARS`
- order 506: `RENDER_FRAME_MAX_POINTS` (constant), lines 1377-1377, exports `RENDER_FRAME_MAX_POINTS`
- order 507: `RENDER_FRAME_MAX_LINES` (constant), lines 1378-1378, exports `RENDER_FRAME_MAX_LINES`
- order 508: `RENDER_FRAME_MAX_LINE_POINTS` (constant), lines 1379-1379, exports `RENDER_FRAME_MAX_LINE_POINTS`
- order 509: `RENDER_FRAME_ACTIVITY_INTERVAL_SECONDS` (constant), lines 1380-1380, exports `RENDER_FRAME_ACTIVITY_INTERVAL_SECONDS`
- order 510: `RAW_TOOLCALL_TEXT_FILTER_THRESHOLD` (constant), lines 1381-1381, exports `RAW_TOOLCALL_TEXT_FILTER_THRESHOLD`
- order 511: `ASSISTANT_TEXT_PERSIST_MAX_CHARS` (constant), lines 1382-1382, exports `ASSISTANT_TEXT_PERSIST_MAX_CHARS`
- order 512: `ASSISTANT_MESSAGE_EVENT_MAX_CHARS` (constant), lines 1383-1383, exports `ASSISTANT_MESSAGE_EVENT_MAX_CHARS`
- order 513: `CODE_PREVIEW_EXTS` (constant), lines 1384-1511, exports `CODE_PREVIEW_EXTS`
- order 514: `CODE_PREVIEW_FILENAMES` (constant), lines 1512-1563, exports `CODE_PREVIEW_FILENAMES`
- order 515: `MEDIA_CAPABILITY_KEYS` (constant), lines 1564-1571, exports `MEDIA_CAPABILITY_KEYS`
- order 516: `SAMPLE_IMAGE_PNG_B64` (constant), lines 1572-1575, exports `SAMPLE_IMAGE_PNG_B64`
- order 517: `SAMPLE_AUDIO_WAV_B64` (constant), lines 1576-1578, exports `SAMPLE_AUDIO_WAV_B64`
- order 518: `SAMPLE_VIDEO_MP4_B64` (constant), lines 1579-1581, exports `SAMPLE_VIDEO_MP4_B64`
- order 519: `OFFLINE_JS_LIB_CATALOG` (constant), lines 1582-1908, exports `OFFLINE_JS_LIB_CATALOG`
- order 520: `OFFLINE_JS_ASSET_LOCK` (constant), lines 1909-1909, exports `OFFLINE_JS_ASSET_LOCK`
- order 521: `OFFLINE_JS_LIB_INDEX_FILE` (constant), lines 1910-1910, exports `OFFLINE_JS_LIB_INDEX_FILE`
- order 522: `OFFLINE_JS_LIB_README_FILE` (constant), lines 1911-1911, exports `OFFLINE_JS_LIB_README_FILE`
- order 532: `BACKEND_I18N` (constant), lines 2105-2176, exports `BACKEND_I18N`
- order 533: `_call_backend_i18n_en_update_2178` (expression), lines 2177-2278, exports —
- order 534: `_call_backend_i18n_zh_cn_update_2279` (expression), lines 2279-2379, exports —
- order 535: `_call_backend_i18n_zh_tw_update_2380` (expression), lines 2380-2480, exports —
- order 536: `_call_backend_i18n_ja_update_2481` (expression), lines 2481-2581, exports —
- order 757: `TABULAR_PREVIEW_EXTS` (constant), lines 10235-10237, exports `TABULAR_PREVIEW_EXTS`
- order 758: `EXCEL_PREVIEW_EXTS` (constant), lines 10238-10238, exports `EXCEL_PREVIEW_EXTS`
- order 759: `PRESENTATION_PREVIEW_EXTS` (constant), lines 10239-10239, exports `PRESENTATION_PREVIEW_EXTS`
- order 760: `DOCUMENT_PREVIEW_EXTS` (constant), lines 10240-10240, exports `DOCUMENT_PREVIEW_EXTS`

### `config/paths.py`

- order 65: `SCRIPT_DIR` (constant), lines 84-84, exports `SCRIPT_DIR`
- order 90: `_resolve_default_agent_workdir` (function), lines 178-183, exports `_resolve_default_agent_workdir`
- order 91: `_migrate_legacy_runtime_roots` (function), lines 184-213, exports `_migrate_legacy_runtime_roots`
- order 92: `WORKDIR` (constant), lines 214-215, exports `WORKDIR`
- order 93: `CODES_ROOT` (constant), lines 216-216, exports `CODES_ROOT`
- order 94: `LLM_CONFIG_PATH` (constant), lines 217-217, exports `LLM_CONFIG_PATH`
- order 604: `detect_repo_root` (function), lines 3847-3862, exports `detect_repo_root`
- order 605: `REPO_ROOT` (constant), lines 3863-3864, exports `REPO_ROOT`

### `config/settings.py`

- order 526: `normalize_ui_language` (function), lines 1993-2017, exports `normalize_ui_language`
- order 527: `normalize_ui_style` (function), lines 2018-2037, exports `normalize_ui_style`
- order 528: `supported_ui_languages_payload` (function), lines 2038-2041, exports `supported_ui_languages_payload`
- order 529: `agent_language_preference_payload` (function), lines 2042-2051, exports `agent_language_preference_payload`
- order 530: `normalize_execution_mode` (function), lines 2052-2073, exports `normalize_execution_mode`
- order 531: `model_language_instruction` (function), lines 2074-2104, exports `model_language_instruction`
- order 537: `backend_i18n_text` (function), lines 2582-2594, exports `backend_i18n_text`
- order 538: `backend_role_label` (function), lines 2595-2601, exports `backend_role_label`
- order 539: `_detect_os_shell_instruction` (function), lines 2602-2643, exports `_detect_os_shell_instruction`
- order 540: `resolve_web_ui_dir_path` (function), lines 2644-2652, exports `resolve_web_ui_dir_path`
- order 541: `resolve_optional_file_path` (function), lines 2653-2662, exports `resolve_optional_file_path`
- order 542: `resolve_skills_root_path` (function), lines 2663-2672, exports `resolve_skills_root_path`
- order 543: `_count_skill_markdown_files` (function), lines 2673-2686, exports `_count_skill_markdown_files`
- order 544: `select_preferred_skills_root` (function), lines 2687-2723, exports `select_preferred_skills_root`
- order 545: `load_web_ui_config_file` (function), lines 2724-2740, exports `load_web_ui_config_file`
- order 546: `extract_show_upload_list_setting` (function), lines 2741-2757, exports `extract_show_upload_list_setting`
- order 547: `extract_ui_style_setting` (function), lines 2758-2774, exports `extract_ui_style_setting`
- order 548: `extract_js_lib_download_setting` (function), lines 2775-2796, exports `extract_js_lib_download_setting`
- order 549: `extract_daily_session_limit_setting` (function), lines 2797-2842, exports `extract_daily_session_limit_setting`
- order 550: `extract_shell_command_timeout_setting` (function), lines 2843-2891, exports `extract_shell_command_timeout_setting`
- order 551: `extract_context_token_limit_setting` (function), lines 2892-2926, exports `extract_context_token_limit_setting`
- order 552: `normalize_auto_task_level_ceiling` (function), lines 2927-2948, exports `normalize_auto_task_level_ceiling`
- order 553: `normalize_l2_todo_policy` (function), lines 2949-2984, exports `normalize_l2_todo_policy`
- order 554: `extract_l2_todo_policy_setting` (function), lines 2985-3027, exports `extract_l2_todo_policy_setting`
- order 555: `extract_auto_task_level_ceiling_setting` (function), lines 3028-3057, exports `extract_auto_task_level_ceiling_setting`
- order 556: `normalize_read_context_policy` (function), lines 3058-3078, exports `normalize_read_context_policy`
- order 557: `normalize_tool_memory_policy` (function), lines 3079-3082, exports `normalize_tool_memory_policy`
- order 558: `extract_read_context_policy_setting` (function), lines 3083-3106, exports `extract_read_context_policy_setting`
- order 559: `extract_tool_memory_policy_setting` (function), lines 3107-3130, exports `extract_tool_memory_policy_setting`
- order 561: `default_multimodal_capabilities` (function), lines 3137-3147, exports `default_multimodal_capabilities`
- order 562: `_to_bool_like` (function), lines 3148-3160, exports `_to_bool_like`
- order 563: `extract_web_search_enabled_setting` (function), lines 3161-3173, exports `extract_web_search_enabled_setting`
- order 564: `_single_no_plan_todo_setting_sections` (function), lines 3174-3200, exports `_single_no_plan_todo_setting_sections`
- order 565: `_single_no_plan_todo_setting_present` (function), lines 3201-3226, exports `_single_no_plan_todo_setting_present`
- order 566: `extract_single_no_plan_todo_settings` (function), lines 3227-3273, exports `extract_single_no_plan_todo_settings`
- order 567: `normalize_user_memory_mode` (function), lines 3274-3304, exports `normalize_user_memory_mode`
- order 568: `user_memory_enabled_from_mode` (function), lines 3305-3308, exports `user_memory_enabled_from_mode`
- order 569: `extract_user_memory_mode_setting` (function), lines 3309-3348, exports `extract_user_memory_mode_setting`
- order 570: `set_web_search_enabled_on_runtime` (function), lines 3349-3364, exports `set_web_search_enabled_on_runtime`
- order 571: `infer_model_multimodal_capabilities` (function), lines 3365-3411, exports `infer_model_multimodal_capabilities`
- order 572: `parse_capability_overrides` (function), lines 3412-3451, exports `parse_capability_overrides`
- order 573: `merge_multimodal_capabilities` (function), lines 3452-3461, exports `merge_multimodal_capabilities`
- order 574: `parse_media_endpoints` (function), lines 3462-3478, exports `parse_media_endpoints`
- order 590: `extract_runtime_region_hint_setting` (function), lines 3656-3681, exports `extract_runtime_region_hint_setting`
- order 591: `extract_runtime_timezone_hint_setting` (function), lines 3682-3699, exports `extract_runtime_timezone_hint_setting`
- order 592: `runtime_environment_context_snapshot` (function), lines 3700-3749, exports `runtime_environment_context_snapshot`
- order 593: `runtime_environment_context_block` (function), lines 3750-3779, exports `runtime_environment_context_block`
- order 622: `load_offline_js_lib_index` (function), lines 4135-4145, exports `load_offline_js_lib_index`
- order 676: `resolve_ollama_model` (function), lines 6717-6728, exports `resolve_ollama_model`
- order 677: `infer_thinking_model` (function), lines 6729-6732, exports `infer_thinking_model`
- order 688: `extract_base_url` (function), lines 6943-6952, exports `extract_base_url`
- order 690: `infer_user_complexity_value` (function), lines 6964-6981, exports `infer_user_complexity_value`
- order 691: `normalize_task_complexity` (function), lines 6982-7011, exports `normalize_task_complexity`
- order 692: `task_complexity_rank` (function), lines 7012-7014, exports `task_complexity_rank`
- order 693: `task_complexity_at_least` (function), lines 7015-7017, exports `task_complexity_at_least`
- order 694: `max_task_complexity` (function), lines 7018-7028, exports `max_task_complexity`
- order 695: `normalize_openai_compat_provider_name` (function), lines 7029-7045, exports `normalize_openai_compat_provider_name`
- order 715: `resolve_reasoning_payload` (function), lines 7167-7217, exports `resolve_reasoning_payload`
- order 718: `extract_openai_compat_model_ids` (function), lines 7265-7299, exports `extract_openai_compat_model_ids`
- order 721: `load_llm_config_from_source` (function), lines 7332-7367, exports `load_llm_config_from_source`
- order 722: `parse_llm_config_profiles` (function), lines 7368-7998, exports `parse_llm_config_profiles`
- order 723: `looks_like_llm_config` (function), lines 7999-8076, exports `looks_like_llm_config`
- order 727: `parse_front_matter` (function), lines 8237-8425, exports `parse_front_matter`

### `ide/assets.py`

- order 950: `IDE_INDEX_HTML` (constant), lines 97278-97400, exports `IDE_INDEX_HTML`
- order 951: `IDE_CSS` (constant), lines 97401-97437, exports `IDE_CSS`
- order 952: `IDE_JS` (constant), lines 97438-97631, exports `IDE_JS`
- order 953: `IDE_JS` (constant), lines 97632-97866, exports `IDE_JS`
- order 954: `IDE_JS` (constant), lines 97867-97930, exports `IDE_JS`
- order 955: `IDE_JS` (constant), lines 97931-98102, exports `IDE_JS`
- order 956: `IDE_JS` (constant), lines 98103-98137, exports `IDE_JS`

### `ide/auth.py`

- order 735: `IDEAuthError` (class), lines 8787-8794, exports `IDEAuthError`
- order 736: `IDEAuthStore` (class), lines 8795-9495, exports `IDEAuthStore`

### `ide/errors.py`

- order 737: `IDECapabilityError` (class), lines 9496-9502, exports `IDECapabilityError`
- order 738: `IDEFileConflict` (class), lines 9503-9510, exports `IDEFileConflict`

### `ide/events.py`

- order 632: `ide_public_operation_data` (function), lines 4472-4518, exports `ide_public_operation_data`

### `ide/handler.py`

- order 965: `IdeHandler` (class), lines 109564-110719, exports `IdeHandler`

### `ide/preview.py`

- order 755: `normalize_rel_preview_path` (function), lines 10210-10223, exports `normalize_rel_preview_path`
- order 756: `is_code_preview_candidate` (function), lines 10224-10234, exports `is_code_preview_candidate`
- order 761: `preview_kind_for_path` (function), lines 10241-10270, exports `preview_kind_for_path`
- order 762: `normalize_markdown_preview_text` (function), lines 10271-10304, exports `normalize_markdown_preview_text`
- order 763: `_preview_markdown_value_html` (function), lines 10305-10325, exports `_preview_markdown_value_html`
- order 764: `_preview_markdown_frontmatter_html` (function), lines 10326-10341, exports `_preview_markdown_frontmatter_html`
- order 765: `_preview_markdown_task_lists` (function), lines 10342-10355, exports `_preview_markdown_task_lists`
- order 766: `_preview_markdown_fallback_inline` (function), lines 10356-10397, exports `_preview_markdown_fallback_inline`
- order 767: `_preview_markdown_fallback_html` (function), lines 10398-10494, exports `_preview_markdown_fallback_html`
- order 770: `workspace_file_revision_map` (function), lines 10535-10559, exports `workspace_file_revision_map`
- order 771: `workspace_revision_delta` (function), lines 10560-10566, exports `workspace_revision_delta`
- order 772: `build_code_preview_rows` (function), lines 10567-10615, exports `build_code_preview_rows`

### `ide/sandbox.py`

- order 853: `_IDE_SANDBOX_BACKEND_CACHE` (assignment), lines 21149-21157, exports `_IDE_SANDBOX_BACKEND_CACHE`
- order 854: `_IDE_SANDBOX_BACKEND_LOCK` (assignment), lines 21158-21158, exports `_IDE_SANDBOX_BACKEND_LOCK`
- order 855: `WINDOWS_JOB_SANDBOX_MARKER` (constant), lines 21159-21159, exports `WINDOWS_JOB_SANDBOX_MARKER`
- order 856: `_WINDOWS_LOW_INTEGRITY_ROOTS` (assignment), lines 21160-21160, exports `_WINDOWS_LOW_INTEGRITY_ROOTS`
- order 857: `_WINDOWS_LOW_INTEGRITY_FAILED_ROOTS` (assignment), lines 21161-21161, exports `_WINDOWS_LOW_INTEGRITY_FAILED_ROOTS`
- order 858: `_WINDOWS_LOW_INTEGRITY_LOCK` (assignment), lines 21162-21162, exports `_WINDOWS_LOW_INTEGRITY_LOCK`
- order 859: `_is_windows_job_sandbox_prefix` (function), lines 21163-21169, exports `_is_windows_job_sandbox_prefix`
- order 860: `_windows_builtin_sandbox_probe` (function), lines 21170-21193, exports `_windows_builtin_sandbox_probe`
- order 861: `_windows_last_error` (function), lines 21194-21201, exports `_windows_last_error`
- order 862: `_windows_set_low_integrity_label` (function), lines 21202-21255, exports `_windows_set_low_integrity_label`
- order 863: `_windows_prepare_low_integrity_workspace` (function), lines 21256-21290, exports `_windows_prepare_low_integrity_workspace`
- order 864: `_windows_job_memory_limit` (function), lines 21291-21298, exports `_windows_job_memory_limit`
- order 865: `_windows_lower_process_integrity` (function), lines 21299-21346, exports `_windows_lower_process_integrity`
- order 866: `_windows_attach_sandbox_job` (function), lines 21347-21439, exports `_windows_attach_sandbox_job`
- order 867: `_windows_close_sandbox_job` (function), lines 21440-21456, exports `_windows_close_sandbox_job`
- order 868: `_popen_windows_sandboxed` (function), lines 21457-21488, exports `_popen_windows_sandboxed`
- order 869: `_run_windows_sandboxed_command` (function), lines 21489-21526, exports `_run_windows_sandboxed_command`
- order 870: `_detect_ide_sandbox_backend` (function), lines 21527-21631, exports `_detect_ide_sandbox_backend`

### `llm/client.py`

- order 838: `OllamaError` (class), lines 18151-18173, exports `OllamaError`
- order 839: `OllamaClient` (class), lines 18174-20488, exports `OllamaClient`

### `llm/constants.py`

- order 63: `DEFAULT_OLLAMA_BASE_URL` (constant), lines 82-82, exports `DEFAULT_OLLAMA_BASE_URL`
- order 64: `DEFAULT_OLLAMA_MODEL` (constant), lines 83-83, exports `DEFAULT_OLLAMA_MODEL`
- order 696: `OPENAI_COMPAT_PROVIDER_NAMES` (constant), lines 7046-7055, exports `OPENAI_COMPAT_PROVIDER_NAMES`
- order 697: `OPENAI_LIKE_PROVIDER_NAMES` (constant), lines 7056-7057, exports `OPENAI_LIKE_PROVIDER_NAMES`
- order 700: `EFFORT_OFF` (constant), lines 7064-7075, exports `EFFORT_OFF`
- order 701: `EFFORT_LOW` (constant), lines 7076-7076, exports `EFFORT_LOW`
- order 702: `EFFORT_MEDIUM` (constant), lines 7077-7077, exports `EFFORT_MEDIUM`
- order 703: `EFFORT_HIGH` (constant), lines 7078-7078, exports `EFFORT_HIGH`
- order 704: `EFFORT_MAX` (constant), lines 7079-7079, exports `EFFORT_MAX`
- order 705: `EFFORT_LEVELS` (constant), lines 7080-7080, exports `EFFORT_LEVELS`
- order 706: `EFFORT_ORDER` (constant), lines 7081-7081, exports `EFFORT_ORDER`
- order 707: `EFFORT_DEFAULT` (constant), lines 7082-7082, exports `EFFORT_DEFAULT`
- order 708: `EFFORT_ANTHROPIC_BUDGET` (constant), lines 7083-7090, exports `EFFORT_ANTHROPIC_BUDGET`
- order 709: `EFFORT_OPENAI_REASONING` (constant), lines 7091-7097, exports `EFFORT_OPENAI_REASONING`
- order 710: `TASK_LEVEL_EFFORT` (constant), lines 7098-7107, exports `TASK_LEVEL_EFFORT`
- order 711: `ROLE_EFFORT_FLOOR` (constant), lines 7108-7113, exports `ROLE_EFFORT_FLOOR`
- order 712: `COORDINATION_EFFORT` (constant), lines 7114-7117, exports `COORDINATION_EFFORT`

### `llm/utils.py`

- order 669: `probe_ollama_environment` (function), lines 6648-6662, exports `probe_ollama_environment`
- order 670: `list_ollama_models` (function), lines 6663-6666, exports `list_ollama_models`
- order 671: `_OLLAMA_TAG_CACHE_LOCK` (assignment), lines 6667-6668, exports `_OLLAMA_TAG_CACHE_LOCK`
- order 672: `_OLLAMA_TAG_CACHE` (assignment), lines 6669-6669, exports `_OLLAMA_TAG_CACHE`
- order 675: `list_ollama_models_cached` (function), lines 6678-6716, exports `list_ollama_models_cached`
- order 678: `split_thinking_content` (function), lines 6733-6777, exports `split_thinking_content`
- order 679: `strip_thinking_content` (function), lines 6778-6780, exports `strip_thinking_content`
- order 680: `check_ollama_model_ready` (function), lines 6781-6806, exports `check_ollama_model_ready`
- order 681: `list_loaded_ollama_models` (function), lines 6807-6821, exports `list_loaded_ollama_models`
- order 682: `wake_ollama_model` (function), lines 6822-6853, exports `wake_ollama_model`
- order 683: `try_pull_ollama_model` (function), lines 6854-6873, exports `try_pull_ollama_model`
- order 684: `ordered_model_candidates` (function), lines 6874-6893, exports `ordered_model_candidates`
- order 685: `pick_working_ollama_model` (function), lines 6894-6911, exports `pick_working_ollama_model`
- order 689: `complete_chat_endpoint` (function), lines 6953-6963, exports `complete_chat_endpoint`
- order 698: `is_openai_compat_provider` (function), lines 7058-7060, exports `is_openai_compat_provider`
- order 699: `is_openai_like_provider` (function), lines 7061-7063, exports `is_openai_like_provider`
- order 713: `clamp_effort` (function), lines 7118-7129, exports `clamp_effort`
- order 714: `model_reasoning_style` (function), lines 7130-7166, exports `model_reasoning_style`
- order 716: `openai_compat_probe_headers` (function), lines 7218-7230, exports `openai_compat_probe_headers`
- order 717: `openai_compat_model_list_urls` (function), lines 7231-7264, exports `openai_compat_model_list_urls`
- order 719: `_is_http_url` (function), lines 7300-7313, exports `_is_http_url`
- order 720: `_resolve_local_path` (function), lines 7314-7331, exports `_resolve_local_path`

### `mcp/constants.py`

- order 112: `MCP_SERVICE_PORT_OFFSET` (constant), lines 235-235, exports `MCP_SERVICE_PORT_OFFSET`
- order 818: `MCP_PROTOCOL_VERSION` (constant), lines 16769-16798, exports `MCP_PROTOCOL_VERSION`
- order 819: `MCP_NAME_RE` (constant), lines 16799-16799, exports `MCP_NAME_RE`
- order 820: `MCP_TOOL_PREFIX` (constant), lines 16800-16800, exports `MCP_TOOL_PREFIX`
- order 821: `_MCP_DEFAULT_HANDSHAKE_TIMEOUT` (assignment), lines 16801-16801, exports `_MCP_DEFAULT_HANDSHAKE_TIMEOUT`
- order 822: `_MCP_DEFAULT_CALL_TIMEOUT` (assignment), lines 16802-16802, exports `_MCP_DEFAULT_CALL_TIMEOUT`
- order 823: `_MCP_MAX_RESULT_CHARS` (assignment), lines 16803-16803, exports `_MCP_MAX_RESULT_CHARS`
- order 824: `_MCP_TRUST_STORE_VERSION` (assignment), lines 16804-16804, exports `_MCP_TRUST_STORE_VERSION`

### `mcp/driver.py`

- order 825: `mcp_normalize_name` (function), lines 16805-16814, exports `mcp_normalize_name`
- order 826: `mcp_normalize_server_configs` (function), lines 16815-16899, exports `mcp_normalize_server_configs`
- order 827: `mcp_extract_server_configs` (function), lines 16900-16919, exports `mcp_extract_server_configs`
- order 828: `_mcp_sha256_file` (function), lines 16920-16930, exports `_mcp_sha256_file`
- order 829: `_mcp_file_identity` (function), lines 16931-16948, exports `_mcp_file_identity`
- order 830: `mcp_workspace_identity` (function), lines 16949-16967, exports `mcp_workspace_identity`
- order 831: `mcp_config_file_digest` (function), lines 16968-16975, exports `mcp_config_file_digest`
- order 832: `mcp_default_trust_store_path` (function), lines 16976-17010, exports `mcp_default_trust_store_path`
- order 833: `mcp_record_definition_fingerprint` (function), lines 17011-17025, exports `mcp_record_definition_fingerprint`
- order 834: `_mcp_effective_spawn` (function), lines 17026-17113, exports `_mcp_effective_spawn`
- order 835: `MCPWorkspaceTrustStore` (class), lines 17114-17175, exports `MCPWorkspaceTrustStore`
- order 836: `MCPServerProcess` (class), lines 17176-17531, exports `MCPServerProcess`
- order 837: `MCPManager` (class), lines 17532-18150, exports `MCPManager`

### `mcp/service.py`

- order 966: `McpServiceHandler` (class), lines 110720-110936, exports `McpServiceHandler`

### `rag/assets.py`

- order 944: `RAG_ADMIN_INDEX_HTML` (constant), lines 94870-95044, exports `RAG_ADMIN_INDEX_HTML`
- order 945: `RAG_ADMIN_CSS` (constant), lines 95045-95136, exports `RAG_ADMIN_CSS`
- order 946: `RAG_ADMIN_JS` (constant), lines 95137-97228, exports `RAG_ADMIN_JS`
- order 947: `CODE_ADMIN_INDEX_HTML` (constant), lines 97229-97241, exports `CODE_ADMIN_INDEX_HTML`
- order 948: `CODE_ADMIN_CSS` (constant), lines 97242-97272, exports `CODE_ADMIN_CSS`
- order 949: `CODE_ADMIN_JS` (constant), lines 97273-97277, exports `CODE_ADMIN_JS`

### `rag/constants.py`

- order 108: `RAG_LIBRARY_DIRNAME` (constant), lines 231-231, exports `RAG_LIBRARY_DIRNAME`
- order 109: `RAG_ADMIN_PORT_OFFSET` (constant), lines 232-232, exports `RAG_ADMIN_PORT_OFFSET`
- order 110: `CODE_LIBRARY_DIRNAME` (constant), lines 233-233, exports `CODE_LIBRARY_DIRNAME`
- order 115: `WEB_SEARCH_INDEX_DIRNAME` (constant), lines 241-241, exports `WEB_SEARCH_INDEX_DIRNAME`
- order 117: `USER_MEMORY_DIRNAME` (constant), lines 243-243, exports `USER_MEMORY_DIRNAME`
- order 118: `USER_MEMORY_DB_FILENAME` (constant), lines 244-244, exports `USER_MEMORY_DB_FILENAME`
- order 119: `USER_MEMORY_PROFILE_FILENAME` (constant), lines 245-245, exports `USER_MEMORY_PROFILE_FILENAME`
- order 120: `USER_MEMORY_MODE_CHOICES` (constant), lines 246-246, exports `USER_MEMORY_MODE_CHOICES`
- order 122: `USER_MEMORY_WEAK_CAPSULE_CHARS` (constant), lines 248-248, exports `USER_MEMORY_WEAK_CAPSULE_CHARS`
- order 123: `USER_MEMORY_ON_CAPSULE_CHARS` (constant), lines 249-249, exports `USER_MEMORY_ON_CAPSULE_CHARS`
- order 124: `USER_MEMORY_CAPSULE_INJECT_CHARS` (constant), lines 250-253, exports `USER_MEMORY_CAPSULE_INJECT_CHARS`
- order 125: `USER_MEMORY_MAX_SUMMARY_CHARS` (constant), lines 254-254, exports `USER_MEMORY_MAX_SUMMARY_CHARS`
- order 126: `USER_MEMORY_QUERY_LIMIT` (constant), lines 255-255, exports `USER_MEMORY_QUERY_LIMIT`
- order 127: `USER_MEMORY_DECAY_HALFLIFE_DAYS` (constant), lines 256-256, exports `USER_MEMORY_DECAY_HALFLIFE_DAYS`
- order 128: `USER_MEMORY_PROFILE_SCHEMA_VERSION` (constant), lines 257-257, exports `USER_MEMORY_PROFILE_SCHEMA_VERSION`
- order 139: `WEB_SEARCH_CONTEXT_REGISTRY_MAX` (constant), lines 268-268, exports `WEB_SEARCH_CONTEXT_REGISTRY_MAX`
- order 140: `WEB_SEARCH_CONTEXT_PROMPT_MAX_ITEMS` (constant), lines 269-269, exports `WEB_SEARCH_CONTEXT_PROMPT_MAX_ITEMS`
- order 141: `WEB_SEARCH_CONTEXT_PROMPT_MAX_CHARS` (constant), lines 270-270, exports `WEB_SEARCH_CONTEXT_PROMPT_MAX_CHARS`
- order 142: `WEB_SEARCH_CONTEXT_NODE_MAX` (constant), lines 271-271, exports `WEB_SEARCH_CONTEXT_NODE_MAX`
- order 143: `WEB_SEARCH_CONTEXT_URL_MAX` (constant), lines 272-272, exports `WEB_SEARCH_CONTEXT_URL_MAX`
- order 144: `RAG_CHUNK_CHARS` (constant), lines 273-273, exports `RAG_CHUNK_CHARS`
- order 145: `RAG_CHUNK_OVERLAP` (constant), lines 274-274, exports `RAG_CHUNK_OVERLAP`
- order 146: `RAG_MAX_CHUNKS_PER_DOC` (constant), lines 275-277, exports `RAG_MAX_CHUNKS_PER_DOC`
- order 147: `RAG_MAX_DOCUMENT_CHARS` (constant), lines 278-288, exports `RAG_MAX_DOCUMENT_CHARS`
- order 151: `RAG_MAX_QUERY_RESULTS` (constant), lines 292-292, exports `RAG_MAX_QUERY_RESULTS`
- order 152: `RAG_HIGH_RECALL_POOL_MULTIPLIER` (constant), lines 293-293, exports `RAG_HIGH_RECALL_POOL_MULTIPLIER`
- order 153: `RAG_HIGH_RECALL_MIN_POOL` (constant), lines 294-294, exports `RAG_HIGH_RECALL_MIN_POOL`
- order 154: `RAG_RETRIEVAL_MAX_PER_DOC` (constant), lines 295-295, exports `RAG_RETRIEVAL_MAX_PER_DOC`
- order 155: `RAG_BM25_K1` (constant), lines 296-299, exports `RAG_BM25_K1`
- order 156: `RAG_BM25_B` (constant), lines 300-300, exports `RAG_BM25_B`
- order 157: `RAG_BM25_SATURATION` (constant), lines 301-307, exports `RAG_BM25_SATURATION`
- order 158: `RAG_SYMBOL_EXACT_BOOST` (constant), lines 308-311, exports `RAG_SYMBOL_EXACT_BOOST`
- order 159: `RAG_INDEX_SNAPSHOT_FORMAT` (constant), lines 312-315, exports `RAG_INDEX_SNAPSHOT_FORMAT`
- order 160: `RAG_GRAPH_MAX_NODES` (constant), lines 316-316, exports `RAG_GRAPH_MAX_NODES`
- order 161: `RAG_TASK_HISTORY_LIMIT` (constant), lines 317-317, exports `RAG_TASK_HISTORY_LIMIT`
- order 162: `RAG_MODEL_MEDIA_MAX_BYTES` (constant), lines 318-318, exports `RAG_MODEL_MEDIA_MAX_BYTES`
- order 163: `RAG_MAX_IMPORT_FILES` (constant), lines 319-319, exports `RAG_MAX_IMPORT_FILES`
- order 164: `RAG_MAX_IMPORT_BATCH_ITEMS` (constant), lines 320-320, exports `RAG_MAX_IMPORT_BATCH_ITEMS`
- order 165: `RAG_MAX_IMPORT_BATCH_BYTES` (constant), lines 321-321, exports `RAG_MAX_IMPORT_BATCH_BYTES`
- order 166: `RAG_PDF_IMAGE_LIMIT` (constant), lines 322-322, exports `RAG_PDF_IMAGE_LIMIT`
- order 167: `RAG_QUERY_CONTEXT_CHARS` (constant), lines 323-323, exports `RAG_QUERY_CONTEXT_CHARS`
- order 168: `RAG_MAX_GLOBAL_COMMUNITIES` (constant), lines 324-324, exports `RAG_MAX_GLOBAL_COMMUNITIES`
- order 169: `RAG_MAX_COMMUNITY_MAP_SUPPORT` (constant), lines 325-325, exports `RAG_MAX_COMMUNITY_MAP_SUPPORT`
- order 170: `RAG_INCLUDE_FILENAME_ENTITIES_DEFAULT` (constant), lines 326-326, exports `RAG_INCLUDE_FILENAME_ENTITIES_DEFAULT`
- order 171: `RAG_DYNAMIC_NOISE_MIN_DOC_FREQ` (constant), lines 327-327, exports `RAG_DYNAMIC_NOISE_MIN_DOC_FREQ`
- order 172: `RAG_DYNAMIC_NOISE_MIN_COMMUNITY_FREQ` (constant), lines 328-328, exports `RAG_DYNAMIC_NOISE_MIN_COMMUNITY_FREQ`
- order 173: `RAG_DYNAMIC_NOISE_SOFT_DOC_RATIO` (constant), lines 329-329, exports `RAG_DYNAMIC_NOISE_SOFT_DOC_RATIO`
- order 174: `RAG_DYNAMIC_NOISE_HARD_DOC_RATIO` (constant), lines 330-330, exports `RAG_DYNAMIC_NOISE_HARD_DOC_RATIO`
- order 175: `RAG_DYNAMIC_NOISE_SOFT_COMMUNITY_RATIO` (constant), lines 331-331, exports `RAG_DYNAMIC_NOISE_SOFT_COMMUNITY_RATIO`
- order 176: `RAG_DYNAMIC_NOISE_HARD_COMMUNITY_RATIO` (constant), lines 332-332, exports `RAG_DYNAMIC_NOISE_HARD_COMMUNITY_RATIO`
- order 177: `RAG_MIN_SYNTHESIS_SCORE` (constant), lines 333-333, exports `RAG_MIN_SYNTHESIS_SCORE`
- order 178: `RAG_NO_EVIDENCE_THRESHOLD` (constant), lines 334-334, exports `RAG_NO_EVIDENCE_THRESHOLD`
- order 179: `RAG_WEAK_MATCH_SCORE_CAP` (constant), lines 335-335, exports `RAG_WEAK_MATCH_SCORE_CAP`
- order 180: `RAG_SYNTHESIS_MAX_PER_DOC` (constant), lines 336-336, exports `RAG_SYNTHESIS_MAX_PER_DOC`
- order 181: `RAG_WORKFLOW_ACCEPT_SCORE` (constant), lines 337-337, exports `RAG_WORKFLOW_ACCEPT_SCORE`
- order 182: `RAG_NO_EVIDENCE_MESSAGE` (constant), lines 338-338, exports `RAG_NO_EVIDENCE_MESSAGE`
- order 183: `RAG_CONTEXT_BUDGETS` (constant), lines 339-343, exports `RAG_CONTEXT_BUDGETS`
- order 184: `RAG_WEAK_EVIDENCE_MESSAGE` (constant), lines 344-344, exports `RAG_WEAK_EVIDENCE_MESSAGE`
- order 185: `RAG_DENSE_DEFAULT_ENABLED` (constant), lines 345-345, exports `RAG_DENSE_DEFAULT_ENABLED`
- order 186: `RAG_EMBEDDING_MODE_VALUES` (constant), lines 346-346, exports `RAG_EMBEDDING_MODE_VALUES`
- order 187: `RAG_IMPORT_WORKER_COUNT` (constant), lines 347-350, exports `RAG_IMPORT_WORKER_COUNT`
- order 189: `RAG_PARSE_TIMEOUT_SECONDS` (constant), lines 355-358, exports `RAG_PARSE_TIMEOUT_SECONDS`
- order 883: `RAG_TERM_GROUPS` (constant), lines 82261-86894, exports `RAG_TERM_GROUPS`
- order 884: `RAG_RESEARCH_HINTS` (constant), lines 86895-86916, exports `RAG_RESEARCH_HINTS`
- order 885: `RAG_CODE_HINTS` (constant), lines 86917-86927, exports `RAG_CODE_HINTS`
- order 886: `RAG_SHORT_TOKEN_ALLOWLIST` (constant), lines 86928-86943, exports `RAG_SHORT_TOKEN_ALLOWLIST`
- order 887: `RAG_EN_STOPWORDS` (constant), lines 86944-87016, exports `RAG_EN_STOPWORDS`
- order 888: `RAG_ZH_STOPWORDS` (constant), lines 87017-87053, exports `RAG_ZH_STOPWORDS`
- order 889: `RAG_GENERIC_ENTITY_TERMS_EN` (constant), lines 87054-87132, exports `RAG_GENERIC_ENTITY_TERMS_EN`
- order 890: `RAG_GENERIC_ENTITY_TERMS_ZH` (constant), lines 87133-87175, exports `RAG_GENERIC_ENTITY_TERMS_ZH`
- order 891: `RAG_STRUCTURAL_ENTITY_PATTERNS` (constant), lines 87176-87194, exports `RAG_STRUCTURAL_ENTITY_PATTERNS`
- order 916: `CODE_LIBRARY_IGNORED_DIRS` (constant), lines 87939-87948, exports `CODE_LIBRARY_IGNORED_DIRS`
- order 917: `CODE_LIBRARY_LANGUAGE_BY_EXT` (constant), lines 87949-88005, exports `CODE_LIBRARY_LANGUAGE_BY_EXT`
- order 918: `CODE_LIBRARY_SPECIAL_FILENAMES` (constant), lines 88006-88012, exports `CODE_LIBRARY_SPECIAL_FILENAMES`

### `rag/index.py`

- order 921: `_code_module_name` (function), lines 88037-88053, exports `_code_module_name`
- order 922: `_code_choose_community` (function), lines 88054-88063, exports `_code_choose_community`
- order 923: `_code_query_terms` (function), lines 88064-88078, exports `_code_query_terms`
- order 932: `TFGraphIDFIndex` (class), lines 89146-90822, exports `TFGraphIDFIndex`
- order 941: `CodeGraphIndex` (class), lines 94030-94515, exports `CodeGraphIndex`

### `rag/ingestion.py`

- order 901: `_rag_trigram_set` (function), lines 87405-87412, exports `_rag_trigram_set`
- order 902: `_rag_jaccard_sim` (function), lines 87413-87422, exports `_rag_jaccard_sim`
- order 903: `_rag_mmr_select` (function), lines 87423-87472, exports `_rag_mmr_select`
- order 908: `_rag_embed_text` (function), lines 87607-87630, exports `_rag_embed_text`
- order 909: `_rag_embed_batch` (function), lines 87631-87639, exports `_rag_embed_batch`
- order 910: `_rag_window_for_query` (function), lines 87640-87654, exports `_rag_window_for_query`
- order 911: `_rag_focused_excerpt` (function), lines 87655-87697, exports `_rag_focused_excerpt`
- order 912: `_rag_query_variants` (function), lines 87698-87737, exports `_rag_query_variants`
- order 913: `_rag_parse_segments` (function), lines 87738-87800, exports `_rag_parse_segments`
- order 914: `_rag_boundary_split` (function), lines 87801-87858, exports `_rag_boundary_split`
- order 939: `_rag_parse_file_worker` (function), lines 93131-93147, exports `_rag_parse_file_worker`
- order 940: `RAGIngestionService` (class), lines 93148-94029, exports `RAGIngestionService`
- order 943: `CodeIngestionService` (class), lines 94782-94869, exports `CodeIngestionService`

### `rag/parsers.py`

- order 892: `_rag_safe_name` (function), lines 87195-87209, exports `_rag_safe_name`
- order 893: `_rag_detect_language` (function), lines 87210-87226, exports `_rag_detect_language`
- order 894: `_rag_cjk_ngrams` (function), lines 87227-87241, exports `_rag_cjk_ngrams`
- order 895: `_rag_is_noise_token` (function), lines 87242-87263, exports `_rag_is_noise_token`
- order 896: `_rag_entity_allowed` (function), lines 87264-87278, exports `_rag_entity_allowed`
- order 897: `_rag_filter_entities` (function), lines 87279-87295, exports `_rag_filter_entities`
- order 898: `_rag_filename_entity_aliases` (function), lines 87296-87331, exports `_rag_filename_entity_aliases`
- order 899: `_rag_apply_filename_entity_policy` (function), lines 87332-87364, exports `_rag_apply_filename_entity_policy`
- order 900: `_rag_choose_community` (function), lines 87365-87404, exports `_rag_choose_community`
- order 904: `_rag_tokenize` (function), lines 87473-87526, exports `_rag_tokenize`
- order 905: `_rag_expand_tokens` (function), lines 87527-87550, exports `_rag_expand_tokens`
- order 906: `_rag_extract_entities` (function), lines 87551-87569, exports `_rag_extract_entities`
- order 907: `_rag_classify_document` (function), lines 87570-87606, exports `_rag_classify_document`
- order 915: `_rag_chunk_text` (function), lines 87859-87938, exports `_rag_chunk_text`
- order 919: `_code_language_from_name` (function), lines 88013-88031, exports `_code_language_from_name`
- order 920: `_code_is_test_path` (function), lines 88032-88036, exports `_code_is_test_path`
- order 924: `_CallCollector` (class), lines 88079-88093, exports `_CallCollector`
- order 925: `_ALGO_COMPLEXITY_RE` (assignment), lines 88094-88096, exports `_ALGO_COMPLEXITY_RE`
- order 926: `_ALGO_STEP_RE` (assignment), lines 88097-88097, exports `_ALGO_STEP_RE`
- order 927: `_ALGO_MATH_VARS` (assignment), lines 88098-88098, exports `_ALGO_MATH_VARS`
- order 928: `_ALGO_DOC_KEYWORDS` (assignment), lines 88099-88099, exports `_ALGO_DOC_KEYWORDS`
- order 929: `_detect_algo_chunk` (function), lines 88100-88125, exports `_detect_algo_chunk`
- order 930: `CodeContentParser` (class), lines 88126-88635, exports `CodeContentParser`
- order 931: `RAGContentParser` (class), lines 88636-89145, exports `RAGContentParser`

### `rag/store.py`

- order 933: `RAGLibraryStore` (class), lines 90823-91408, exports `RAGLibraryStore`
- order 934: `WikiStore` (class), lines 91409-91940, exports `WikiStore`
- order 935: `UserMemoryStore` (class), lines 91941-92618, exports `UserMemoryStore`
- order 936: `UserInteractionOptimizer` (class), lines 92619-92687, exports `UserInteractionOptimizer`
- order 937: `UserIntentProfiler` (class), lines 92688-92729, exports `UserIntentProfiler`
- order 938: `WorkflowMemoryStore` (class), lines 92730-93130, exports `WorkflowMemoryStore`
- order 942: `CodeLibraryStore` (class), lines 94516-94781, exports `CodeLibraryStore`

### `rag/web_search.py`

- order 635: `_agent_web_bool` (function), lines 4553-4560, exports `_agent_web_bool`
- order 636: `_agent_web_int` (function), lines 4561-4568, exports `_agent_web_int`
- order 637: `_agent_web_host_is_local_name` (function), lines 4569-4575, exports `_agent_web_host_is_local_name`
- order 638: `_agent_web_ip_is_blocked` (function), lines 4576-4590, exports `_agent_web_ip_is_blocked`
- order 639: `_agent_web_canonical_url` (function), lines 4591-4620, exports `_agent_web_canonical_url`
- order 640: `_agent_web_domain_to_seed` (function), lines 4621-4632, exports `_agent_web_domain_to_seed`
- order 641: `_agent_web_query_terms` (function), lines 4633-4650, exports `_agent_web_query_terms`
- order 642: `_agent_web_query_domain_hints` (function), lines 4651-4691, exports `_agent_web_query_domain_hints`
- order 643: `_agent_web_query_needs_fresh_network` (function), lines 4692-4714, exports `_agent_web_query_needs_fresh_network`
- order 644: `_agent_web_extract_text_snippet` (function), lines 4715-4732, exports `_agent_web_extract_text_snippet`
- order 645: `AgentWebHTMLParser` (class), lines 4733-4812, exports `AgentWebHTMLParser`
- order 646: `_agent_web_decompress_bytes` (function), lines 4813-4836, exports `_agent_web_decompress_bytes`
- order 647: `_agent_web_charset_candidates` (function), lines 4837-4895, exports `_agent_web_charset_candidates`
- order 648: `_agent_web_decode_text_bytes` (function), lines 4896-4930, exports `_agent_web_decode_text_bytes`
- order 649: `AgentWebSearchEngine` (class), lines 4931-6000, exports `AgentWebSearchEngine`

### `server/http.py`

- order 958: `AgentHTTPServer` (class), lines 106414-106453, exports `AgentHTTPServer`
- order 961: `Handler` (class), lines 107573-108942, exports `Handler`

### `server/rag_admin.py`

- order 963: `RagAdminHandler` (class), lines 109169-109360, exports `RagAdminHandler`
- order 964: `CodeAdminHandler` (class), lines 109361-109563, exports `CodeAdminHandler`

### `server/skills.py`

- order 962: `SkillsHandler` (class), lines 108943-109168, exports `SkillsHandler`

### `session/manager.py`

- order 560: `SessionCreationLimitExceeded` (class), lines 3131-3136, exports `SessionCreationLimitExceeded`
- order 872: `SessionManager` (class), lines 74718-76029, exports `SessionManager`

### `session/state.py`

- order 871: `SessionState` (class), lines 21632-74717, exports `SessionState`

### `skills/embedded.py`

- order 775: `EMBEDDED_SKILLS_ARCHIVE_B64` (constant), lines 11024-11025, exports `EMBEDDED_SKILLS_ARCHIVE_B64`
- order 776: `EMBEDDED_SKILLS_ARCHIVE_SHA256` (constant), lines 11026-11026, exports `EMBEDDED_SKILLS_ARCHIVE_SHA256`
- order 777: `EMBEDDED_SKILLS_ARCHIVE_FILES` (constant), lines 11027-11049, exports `EMBEDDED_SKILLS_ARCHIVE_FILES`
- order 802: `BUILTIN_CLAWHUB_SKILLS_VERSION` (constant), lines 14285-14287, exports `BUILTIN_CLAWHUB_SKILLS_VERSION`
- order 803: `EMBEDDED_CLAWHUB_SKILLS_ARCHIVE_B64` (constant), lines 14288-14533, exports `EMBEDDED_CLAWHUB_SKILLS_ARCHIVE_B64`
- order 805: `MCP_BUILDER_SKILL_MD` (constant), lines 14581-14755, exports `MCP_BUILDER_SKILL_MD`
- order 808: `SKILL_PROTOCOL_LOCAL` (constant), lines 14787-14788, exports `SKILL_PROTOCOL_LOCAL`
- order 809: `SKILL_PROTOCOL_CLAWHUB` (constant), lines 14789-14789, exports `SKILL_PROTOCOL_CLAWHUB`
- order 810: `SKILL_PROTOCOL_HTTP_JSON` (constant), lines 14790-14790, exports `SKILL_PROTOCOL_HTTP_JSON`
- order 811: `SKILL_PROTOCOL_SPECS` (constant), lines 14791-14823, exports `SKILL_PROTOCOL_SPECS`

### `skills/provisioning.py`

- order 778: `ensure_embedded_skills_at_root` (function), lines 11050-11115, exports `ensure_embedded_skills_at_root`
- order 779: `ensure_embedded_skills` (function), lines 11116-11119, exports `ensure_embedded_skills`
- order 781: `detect_upload_parser_capabilities` (function), lines 11126-11142, exports `detect_upload_parser_capabilities`
- order 782: `_render_cap_markdown` (function), lines 11143-11158, exports `_render_cap_markdown`
- order 783: `_write_text_if_changed` (function), lines 11159-11165, exports `_write_text_if_changed`
- order 784: `ensure_generated_document_skills` (function), lines 11166-11255, exports `ensure_generated_document_skills`
- order 785: `ensure_generated_image_coding_feedback_skill` (function), lines 11256-11356, exports `ensure_generated_image_coding_feedback_skill`
- order 786: `_skill_knowledge_files` (function), lines 11357-11377, exports `_skill_knowledge_files`
- order 787: `analyze_skill_building_knowledge` (function), lines 11378-11433, exports `analyze_skill_building_knowledge`
- order 788: `_sanitize_skill_slug` (function), lines 11434-11437, exports `_sanitize_skill_slug`
- order 789: `_build_skills_gen_skill_content` (function), lines 11438-11470, exports `_build_skills_gen_skill_content`
- order 790: `ensure_generated_skills_gen_skill` (function), lines 11471-11476, exports `ensure_generated_skills_gen_skill`
- order 791: `ensure_generated_execution_recovery_skill` (function), lines 11477-11561, exports `ensure_generated_execution_recovery_skill`
- order 792: `ensure_generated_systematic_debugging_skill` (function), lines 11562-11835, exports `ensure_generated_systematic_debugging_skill`
- order 793: `ensure_generated_code_engineering_mastery_skill` (function), lines 11836-11955, exports `ensure_generated_code_engineering_mastery_skill`
- order 794: `ensure_generated_smart_file_navigation_skill` (function), lines 11956-12072, exports `ensure_generated_smart_file_navigation_skill`
- order 795: `ensure_generated_html_frontend_report_skills` (function), lines 12073-12281, exports `ensure_generated_html_frontend_report_skills`
- order 796: `ensure_generated_deep_research_skills` (function), lines 12282-12551, exports `ensure_generated_deep_research_skills`
- order 797: `ensure_generated_research_scientific_skills` (function), lines 12552-13189, exports `ensure_generated_research_scientific_skills`
- order 798: `ensure_generated_rag_mastery_skills` (function), lines 13190-13491, exports `ensure_generated_rag_mastery_skills`
- order 799: `ensure_generated_multimodal_comprehension_skills` (function), lines 13492-14186, exports `ensure_generated_multimodal_comprehension_skills`
- order 800: `ensure_generated_runtime_skills_manifest` (function), lines 14187-14221, exports `ensure_generated_runtime_skills_manifest`
- order 801: `ensure_generated_agent_web_search_skill` (function), lines 14222-14284, exports `ensure_generated_agent_web_search_skill`
- order 804: `ensure_embedded_clawhub_skills` (function), lines 14534-14580, exports `ensure_embedded_clawhub_skills`
- order 806: `ensure_generated_mcp_builder_skill` (function), lines 14756-14767, exports `ensure_generated_mcp_builder_skill`
- order 807: `ensure_runtime_skills` (function), lines 14768-14786, exports `ensure_runtime_skills`

### `skills/store.py`

- order 812: `_BUILTIN_SKILLS` (assignment), lines 14824-14932, exports `_BUILTIN_SKILLS`
- order 813: `SkillStore` (class), lines 14933-16240, exports `SkillStore`

### `utils/compress.py`

- order 653: `compress_text_blob` (function), lines 6165-6171, exports `compress_text_blob`
- order 654: `decompress_text_blob` (function), lines 6172-6181, exports `decompress_text_blob`

### `utils/crypto.py`

- order 726: `CryptoBox` (class), lines 8118-8236, exports `CryptoBox`

### `utils/errors.py`

- order 673: `EmptyActionError` (class), lines 6670-6673, exports `EmptyActionError`

### `utils/files.py`

- order 523: `_normalize_js_lib_asset_ref` (function), lines 1912-1927, exports `_normalize_js_lib_asset_ref`
- order 524: `_resolve_js_lib_asset_path` (function), lines 1928-1959, exports `_resolve_js_lib_asset_path`
- order 525: `_discover_extra_js_lib_files` (function), lines 1960-1992, exports `_discover_extra_js_lib_files`
- order 606: `safe_path` (function), lines 3865-3875, exports `safe_path`
- order 607: `_safe_js_filename` (function), lines 3876-3884, exports `_safe_js_filename`
- order 608: `_sha256_bytes` (function), lines 3885-3887, exports `_sha256_bytes`
- order 609: `_sha256_file` (function), lines 3888-3897, exports `_sha256_file`
- order 610: `_download_http_bytes` (function), lines 3898-3907, exports `_download_http_bytes`
- order 611: `offline_js_lib_root` (function), lines 3908-3910, exports `offline_js_lib_root`
- order 612: `_offline_js_entry_relative_path` (function), lines 3911-3916, exports `_offline_js_entry_relative_path`
- order 613: `_archive_member_relative_path` (function), lines 3917-3927, exports `_archive_member_relative_path`
- order 614: `_path_size_bytes` (function), lines 3928-3944, exports `_path_size_bytes`
- order 615: `_extract_archive_to_dir` (function), lines 3945-3986, exports `_extract_archive_to_dir`
- order 616: `_package_required_paths` (function), lines 3987-3994, exports `_package_required_paths`
- order 617: `_package_required_globs` (function), lines 3995-4011, exports `_package_required_globs`
- order 618: `_package_install_ready` (function), lines 4012-4034, exports `_package_install_ready`
- order 619: `_postprocess_offline_js_package` (function), lines 4035-4071, exports `_postprocess_offline_js_package`
- order 620: `_ensure_offline_js_package` (function), lines 4072-4116, exports `_ensure_offline_js_package`
- order 621: `_render_offline_js_catalog_md` (function), lines 4117-4134, exports `_render_offline_js_catalog_md`
- order 623: `ensure_offline_js_libs` (function), lines 4146-4304, exports `ensure_offline_js_libs`
- order 624: `_offline_js_catalog_entry_for_asset` (function), lines 4305-4325, exports `_offline_js_catalog_entry_for_asset`
- order 625: `ensure_offline_js_asset` (function), lines 4326-4383, exports `ensure_offline_js_asset`
- order 626: `_normalize_external_js_url` (function), lines 4384-4389, exports `_normalize_external_js_url`
- order 627: `is_external_js_src` (function), lines 4390-4393, exports `is_external_js_src`
- order 628: `match_offline_js_catalog_by_url` (function), lines 4394-4411, exports `match_offline_js_catalog_by_url`
- order 629: `cache_external_js_url` (function), lines 4412-4447, exports `cache_external_js_url`
- order 729: `try_read_text` (function), lines 8440-8449, exports `try_read_text`

### `utils/http.py`

- order 60: `_URL_OPEN_ORIGINAL` (assignment), lines 79-79, exports `_URL_OPEN_ORIGINAL`
- order 61: `_HTTP_SSL_CONTEXT` (assignment), lines 80-80, exports `_HTTP_SSL_CONTEXT`
- order 88: `_shared_http_ssl_context` (function), lines 144-167, exports `_shared_http_ssl_context`
- order 89: `urlopen` (function), lines 168-177, exports `urlopen`
- order 599: `json_response_bytes` (function), lines 3809-3811, exports `json_response_bytes`
- order 600: `read_http_json_body` (function), lines 3812-3825, exports `read_http_json_body`
- order 601: `close_if_http_request_body_unread` (function), lines 3826-3839, exports `close_if_http_request_body_unread`

### `utils/json_utils.py`

- order 107: `JSON_FSYNC_ENABLED` (constant), lines 230-230, exports `JSON_FSYNC_ENABLED`
- order 598: `json_dumps` (function), lines 3805-3808, exports `json_dumps`
- order 663: `parse_tool_arguments` (function), lines 6475-6485, exports `parse_tool_arguments`
- order 664: `repair_truncated_json_object` (function), lines 6486-6540, exports `repair_truncated_json_object`
- order 665: `parse_tool_arguments_with_error` (function), lines 6541-6572, exports `parse_tool_arguments_with_error`
- order 666: `_is_valid_json_object` (function), lines 6573-6578, exports `_is_valid_json_object`
- order 667: `_scan_top_level_json_objects` (function), lines 6579-6602, exports `_scan_top_level_json_objects`
- order 668: `reconstruct_streamed_tool_args` (function), lines 6603-6647, exports `reconstruct_streamed_tool_args`
- order 686: `parse_json_object` (function), lines 6912-6918, exports `parse_json_object`
- order 687: `extract_json_object_from_text` (function), lines 6919-6942, exports `extract_json_object_from_text`
- order 730: `_json_default_copy` (function), lines 8450-8456, exports `_json_default_copy`
- order 731: `_read_json_file` (function), lines 8457-8478, exports `_read_json_file`
- order 732: `_write_json_file` (function), lines 8479-8507, exports `_write_json_file`

### `utils/media.py`

- order 575: `guess_mime_from_name` (function), lines 3479-3483, exports `guess_mime_from_name`
- order 576: `_convert_image_to_safe_format` (function), lines 3484-3503, exports `_convert_image_to_safe_format`
- order 577: `guess_ext_from_mime` (function), lines 3504-3512, exports `guess_ext_from_mime`

### `utils/misc.py`

- order 578: `now_ts` (function), lines 3513-3515, exports `now_ts`
- order 579: `_benign_socket_log_lock` (assignment), lines 3516-3518, exports `_benign_socket_log_lock`
- order 580: `_benign_socket_log_state` (assignment), lines 3519-3519, exports `_benign_socket_log_state`
- order 582: `is_benign_socket_error` (function), lines 3535-3555, exports `is_benign_socket_error`
- order 583: `_socket_error_code` (function), lines 3556-3567, exports `_socket_error_code`
- order 584: `_log_benign_socket_error_limited` (function), lines 3568-3604, exports `_log_benign_socket_error_limited`
- order 585: `swallow_benign_socket_error` (function), lines 3605-3611, exports `swallow_benign_socket_error`
- order 586: `normalize_timeout_seconds` (function), lines 3612-3627, exports `normalize_timeout_seconds`
- order 587: `detect_local_lan_ip` (function), lines 3628-3639, exports `detect_local_lan_ip`
- order 588: `_LOCAL_LAN_IP_CACHE` (assignment), lines 3640-3641, exports `_LOCAL_LAN_IP_CACHE`
- order 589: `detect_local_lan_ip_cached` (function), lines 3642-3655, exports `detect_local_lan_ip_cached`
- order 602: `make_id` (function), lines 3840-3842, exports `make_id`
- order 603: `sanitize_profile_id` (function), lines 3843-3846, exports `sanitize_profile_id`
- order 724: `user_id_from_ip` (function), lines 8077-8084, exports `user_id_from_ip`
- order 728: `_meta_string_list` (function), lines 8426-8439, exports `_meta_string_list`
- order 780: `_module_exists` (function), lines 11120-11125, exports `_module_exists`

### `utils/text.py`

- order 95: `MAX_TOOL_OUTPUT` (constant), lines 218-218, exports `MAX_TOOL_OUTPUT`
- order 350: `SOCKET_NOISE_LINE_PATTERNS` (constant), lines 733-738, exports `SOCKET_NOISE_LINE_PATTERNS`
- order 581: `filter_runtime_noise_lines` (function), lines 3520-3534, exports `filter_runtime_noise_lines`
- order 594: `safe_utf8_bytes` (function), lines 3780-3782, exports `safe_utf8_bytes`
- order 595: `escape_invalid_utf8_text` (function), lines 3783-3785, exports `escape_invalid_utf8_text`
- order 596: `sanitize_utf8_surrogates` (function), lines 3786-3799, exports `sanitize_utf8_surrogates`
- order 597: `decode_utf8_replace` (function), lines 3800-3804, exports `decode_utf8_replace`
- order 630: `trim` (function), lines 4448-4451, exports `trim`
- order 631: `is_synthetic_public_progress` (function), lines 4452-4471, exports `is_synthetic_public_progress`
- order 633: `display_clean` (function), lines 4519-4533, exports `display_clean`
- order 634: `short_title_from` (function), lines 4534-4552, exports `short_title_from`
- order 650: `_fmt_export_ts` (function), lines 6001-6011, exports `_fmt_export_ts`
- order 651: `_html_esc` (function), lines 6012-6015, exports `_html_esc`
- order 652: `_text_to_minimal_pdf` (function), lines 6016-6164, exports `_text_to_minimal_pdf`
- order 655: `normalize_embedded_newlines` (function), lines 6182-6191, exports `normalize_embedded_newlines`
- order 656: `_map_todo_status_token` (function), lines 6192-6230, exports `_map_todo_status_token`
- order 657: `split_todo_status_text` (function), lines 6231-6290, exports `split_todo_status_text`
- order 658: `extract_todo_rows_from_text` (function), lines 6291-6360, exports `extract_todo_rows_from_text`
- order 659: `decode_structured_todo_container` (function), lines 6361-6379, exports `decode_structured_todo_container`
- order 660: `infer_todo_status_from_text` (function), lines 6380-6388, exports `infer_todo_status_from_text`
- order 661: `split_structured_todo_content` (function), lines 6389-6444, exports `split_structured_todo_content`
- order 662: `normalize_work_text` (function), lines 6445-6474, exports `normalize_work_text`
- order 747: `make_unified_diff` (function), lines 9925-9943, exports `make_unified_diff`
- order 748: `_skip_row` (function), lines 9944-9949, exports `_skip_row`
- order 749: `_row_is_hot` (function), lines 9950-9953, exports `_row_is_hot`
- order 750: `_hotspot_index` (function), lines 9954-9977, exports `_hotspot_index`
- order 751: `_compress_rows_keep_hotspot` (function), lines 9978-10027, exports `_compress_rows_keep_hotspot`
- order 752: `_focused_diff_rows_from_opcodes` (function), lines 10028-10162, exports `_focused_diff_rows_from_opcodes`
- order 753: `make_numbered_diff` (function), lines 10163-10195, exports `make_numbered_diff`
- order 754: `render_numbered_diff_text` (function), lines 10196-10209, exports `render_numbered_diff_text`

### `web/admin_assets.py`

- order 880: `ADMIN_INDEX_HTML` (constant), lines 81905-82067, exports `ADMIN_INDEX_HTML`
- order 881: `ADMIN_CSS` (constant), lines 82068-82195, exports `ADMIN_CSS`
- order 882: `ADMIN_JS` (constant), lines 82196-82260, exports `ADMIN_JS`

### `web/assets.py`

- order 873: `INDEX_HTML` (constant), lines 76030-76276, exports `INDEX_HTML`
- order 874: `APP_CSS` (constant), lines 76277-76812, exports `APP_CSS`
- order 875: `APP_JS` (constant), lines 76813-81465, exports `APP_JS`
- order 876: `APP_TS` (constant), lines 81466-81505, exports `APP_TS`

### `web/skills_assets.py`

- order 877: `SKILLS_INDEX_HTML` (constant), lines 81506-81661, exports `SKILLS_INDEX_HTML`
- order 878: `SKILLS_EXTRA_CSS` (constant), lines 81662-81758, exports `SKILLS_EXTRA_CSS`
- order 879: `SKILLS_APP_JS` (constant), lines 81759-81904, exports `SKILLS_APP_JS`
