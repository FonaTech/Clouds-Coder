# Code_Structure Framework

## Overview

- Source snapshot: `Clouds_Coder.py` (874 top-level statements)
- Generated source modules: 53
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
│   └── handler.py
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
| `_imports.py` | 53 | 66 | — | 1–60 |
| `admin/auth.py` | 3 | 3 | `admin/constants.py`, `utils/misc.py` | 7676–8377 |
| `admin/config.py` | 8 | 8 | `config/constants.py`, `config/paths.py`, `config/settings.py`, `llm/constants.py`, `utils/http.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` | 8378–8790 |
| `admin/constants.py` | 13 | 13 | — | 67–79 |
| `agent/background.py` | 1 | 1 | `utils/misc.py`, `utils/text.py` | 14948–15044 |
| `agent/bus.py` | 1 | 1 | `config/constants.py`, `utils/crypto.py`, `utils/misc.py` | 15045–15110 |
| `agent/errors.py` | 1 | 1 | — | 6260–6263 |
| `agent/events.py` | 1 | 1 | — | 9188–9234 |
| `agent/tasks.py` | 1 | 1 | `utils/crypto.py`, `utils/json_utils.py`, `utils/misc.py` | 14813–14947 |
| `agent/todo.py` | 1 | 1 | `config/constants.py`, `config/settings.py`, `utils/misc.py`, `utils/text.py` | 9235–9595 |
| `agent/tools.py` | 13 | 17 | `config/constants.py` | 18524–19181 |
| `agent/worktree.py` | 1 | 1 | `agent/tasks.py`, `config/constants.py`, `utils/crypto.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` | 15111–15327 |
| `app/context.py` | 1 | 1 | `admin/auth.py`, `admin/config.py`, `admin/constants.py`, `agent/tools.py`, `app/services.py`, `config/constants.py`, `config/paths.py`, `config/settings.py`, `ide/assets.py`, `llm/client.py`, `llm/constants.py`, `llm/utils.py`, `mcp/driver.py`, `rag/assets.py`, `rag/constants.py`, `rag/ingestion.py`, `rag/parsers.py`, `rag/store.py`, `session/manager.py`, `session/state.py`, `skills/provisioning.py`, `skills/store.py`, `utils/crypto.py`, `utils/files.py`, `utils/json_utils.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py`, `web/assets.py`, `web/skills_assets.py` | 93037–97884 |
| `app/main.py` | 2 | 1 | `admin/config.py`, `admin/constants.py`, `agent/tools.py`, `app/context.py`, `config/constants.py`, `config/paths.py`, `config/settings.py`, `ide/handler.py`, `llm/constants.py`, `llm/utils.py`, `mcp/constants.py`, `mcp/service.py`, `rag/constants.py`, `server/http.py`, `server/rag_admin.py`, `server/skills.py`, `skills/provisioning.py`, `utils/files.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` | 101469–103112 |
| `app/services.py` | 2 | 2 | `admin/constants.py`, `config/settings.py`, `skills/embedded.py`, `skills/store.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` | 97925–99043 |
| `config/constants.py` | 344 | 340 | `rag/constants.py` | 63–9106 |
| `config/paths.py` | 8 | 8 | `utils/text.py` | 66–3645 |
| `config/settings.py` | 62 | 62 | `agent/tools.py`, `config/constants.py`, `config/paths.py`, `llm/constants.py`, `llm/utils.py`, `rag/constants.py`, `skills/provisioning.py`, `utils/http.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` | 1784–8016 |
| `ide/assets.py` | 3 | 3 | — | 92693–93036 |
| `ide/handler.py` | 1 | 1 | `admin/auth.py`, `app/context.py`, `config/constants.py`, `session/manager.py`, `utils/http.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py` | 101021–101304 |
| `llm/client.py` | 2 | 2 | `agent/tools.py`, `config/constants.py`, `config/settings.py`, `llm/utils.py`, `utils/http.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` | 16206–18523 |
| `llm/constants.py` | 17 | 17 | — | 64–6708 |
| `llm/utils.py` | 22 | 22 | `config/settings.py`, `llm/constants.py`, `utils/http.py`, `utils/json_utils.py`, `utils/text.py` | 6234–6922 |
| `mcp/constants.py` | 7 | 7 | — | 171–15362 |
| `mcp/driver.py` | 5 | 5 | `mcp/constants.py`, `utils/files.py`, `utils/json_utils.py`, `utils/text.py` | 15363–16205 |
| `mcp/service.py` | 1 | 1 | `config/constants.py`, `utils/files.py`, `utils/http.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` | 101305–101468 |
| `rag/assets.py` | 6 | 6 | — | 90285–92692 |
| `rag/constants.py` | 74 | 74 | — | 167–83427 |
| `rag/index.py` | 5 | 5 | `rag/constants.py`, `rag/ingestion.py`, `rag/parsers.py`, `utils/misc.py`, `utils/text.py` | 83452–89930 |
| `rag/ingestion.py` | 13 | 13 | `config/constants.py`, `config/settings.py`, `rag/constants.py`, `rag/parsers.py`, `rag/store.py`, `session/state.py`, `utils/files.py`, `utils/json_utils.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py` | 82820–90284 |
| `rag/parsers.py` | 28 | 28 | `config/constants.py`, `rag/constants.py`, `rag/ingestion.py`, `utils/files.py`, `utils/json_utils.py`, `utils/media.py`, `utils/text.py` | 9076–84560 |
| `rag/store.py` | 7 | 7 | `config/constants.py`, `config/settings.py`, `rag/constants.py`, `rag/index.py`, `rag/ingestion.py`, `rag/parsers.py`, `skills/provisioning.py`, `utils/files.py`, `utils/json_utils.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py` | 86238–90196 |
| `rag/web_search.py` | 15 | 15 | `config/constants.py`, `config/paths.py`, `rag/constants.py`, `utils/http.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` | 4139–5586 |
| `server/http.py` | 2 | 2 | `admin/auth.py`, `admin/config.py`, `app/context.py`, `config/constants.py`, `config/paths.py`, `config/settings.py`, `llm/utils.py`, `rag/parsers.py`, `session/manager.py`, `session/state.py`, `utils/files.py`, `utils/http.py`, `utils/json_utils.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py`, `web/admin_assets.py` | 97885–100407 |
| `server/rag_admin.py` | 2 | 2 | `admin/auth.py`, `app/context.py`, `config/constants.py`, `rag/constants.py`, `utils/http.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py` | 100634–101020 |
| `server/skills.py` | 1 | 1 | `admin/auth.py`, `app/context.py`, `config/constants.py`, `config/paths.py`, `config/settings.py`, `session/manager.py`, `skills/provisioning.py`, `utils/http.py`, `utils/misc.py`, `utils/text.py` | 100408–100633 |
| `session/manager.py` | 2 | 2 | `config/constants.py`, `config/paths.py`, `config/settings.py`, `llm/client.py`, `llm/utils.py`, `rag/store.py`, `session/state.py`, `utils/crypto.py`, `utils/files.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` | 2912–71455 |
| `session/state.py` | 1 | 1 | `admin/constants.py`, `agent/background.py`, `agent/bus.py`, `agent/errors.py`, `agent/events.py`, `agent/tasks.py`, `agent/todo.py`, `agent/tools.py`, `agent/worktree.py`, `config/constants.py`, `config/paths.py`, `config/settings.py`, `llm/client.py`, `llm/constants.py`, `llm/utils.py`, `mcp/constants.py`, `mcp/driver.py`, `rag/constants.py`, `rag/parsers.py`, `rag/web_search.py`, `skills/provisioning.py`, `skills/store.py`, `utils/compress.py`, `utils/crypto.py`, `utils/errors.py`, `utils/files.py`, `utils/http.py`, `utils/json_utils.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py` | 19182–70133 |
| `skills/embedded.py` | 10 | 10 | — | 9596–13395 |
| `skills/provisioning.py` | 26 | 26 | `config/paths.py`, `skills/embedded.py`, `utils/files.py`, `utils/json_utils.py`, `utils/misc.py` | 9622–13358 |
| `skills/store.py` | 2 | 2 | `config/constants.py`, `config/settings.py`, `llm/utils.py`, `skills/embedded.py`, `utils/files.py`, `utils/http.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` | 13396–14812 |
| `utils/compress.py` | 2 | 2 | — | 5751–5767 |
| `utils/crypto.py` | 1 | 1 | `utils/json_utils.py` | 7709–7827 |
| `utils/errors.py` | 1 | 1 | — | 6256–6259 |
| `utils/files.py` | 24 | 24 | `config/constants.py`, `config/paths.py`, `utils/http.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` | 1703–8040 |
| `utils/http.py` | 7 | 7 | `utils/json_utils.py`, `utils/text.py` | 61–3620 |
| `utils/json_utils.py` | 13 | 13 | `utils/text.py` | 166–8098 |
| `utils/media.py` | 3 | 3 | — | 3260–3293 |
| `utils/misc.py` | 16 | 16 | `config/constants.py` | 3294–9697 |
| `utils/text.py` | 29 | 29 | `config/constants.py` | 154–9075 |
| `web/admin_assets.py` | 3 | 3 | — | 77320–77675 |
| `web/assets.py` | 4 | 4 | — | 71456–76920 |
| `web/skills_assets.py` | 3 | 3 | — | 76921–77319 |

## Source Mapping

### `_imports.py`

- order 0: `_import_2` (import), lines 1-2, exports `annotations`
- order 1: `_import_3` (import), lines 3-3, exports `argparse`
- order 2: `_import_4` (import), lines 4-4, exports `ast`
- order 3: `_import_5` (import), lines 5-5, exports `base64`
- order 4: `_import_6` (import), lines 6-6, exports `Counter`, `defaultdict`, `deque`
- order 5: `_import_7` (import), lines 7-7, exports `concurrent`
- order 6: `_import_8` (import), lines 8-8, exports `csv`
- order 7: `_import_9` (import), lines 9-9, exports `difflib`
- order 8: `_import_10` (import), lines 10-10, exports `errno`
- order 9: `_import_11` (import), lines 11-11, exports `parsedate_to_datetime`
- order 10: `_import_12` (import), lines 12-12, exports `html`
- order 11: `_import_13` (import), lines 13-13, exports `HTMLParser`
- order 12: `_import_14` (import), lines 14-14, exports `hashlib`
- order 13: `_import_15` (import), lines 15-15, exports `hmac`
- order 14: `_import_16` (import), lines 16-16, exports `io`
- order 15: `_import_17` (import), lines 17-17, exports `ipaddress`
- order 16: `_import_18` (import), lines 18-18, exports `importlib`
- order 17: `_import_19` (import), lines 19-19, exports `json`
- order 18: `_import_20` (import), lines 20-20, exports `locale`
- order 19: `_import_21` (import), lines 21-21, exports `math`
- order 20: `_import_22` (import), lines 22-22, exports `multiprocessing`
- order 21: `_import_23` (import), lines 23-23, exports `mimetypes`
- order 22: `_import_24` (import), lines 24-24, exports `os`
- order 23: `_import_25` (import), lines 25-25, exports `queue`
- order 24: `_import_26` (import), lines 26-26, exports `re`
- order 25: `_import_27` (import), lines 27-27, exports `selectors`
- order 26: `_import_28` (import), lines 28-28, exports `signal`
- order 27: `_import_29` (import), lines 29-29, exports `shutil`
- order 28: `_import_30` (import), lines 30-30, exports `shlex`
- order 29: `_import_31` (import), lines 31-31, exports `ssl`
- order 30: `_import_32` (import), lines 32-32, exports `socket`
- order 31: `_import_33` (import), lines 33-33, exports `sqlite3`
- order 32: `_import_34` (import), lines 34-34, exports `subprocess`
- order 33: `_import_35` (import), lines 35-35, exports `sys`
- order 34: `_import_36` (import), lines 36-36, exports `tarfile`
- order 35: `_import_37` (import), lines 37-37, exports `threading`
- order 36: `_import_38` (import), lines 38-38, exports `time`
- order 37: `_import_39` (import), lines 39-39, exports `traceback`
- order 38: `_import_40` (import), lines 40-40, exports `unicodedata`
- order 39: `_import_41` (import), lines 41-41, exports `uuid`
- order 40: `_import_42` (import), lines 42-42, exports `zipfile`
- order 41: `_import_43` (import), lines 43-43, exports `zlib`
- order 42: `_import_44` (import), lines 44-44, exports `ET`
- order 43: `_import_45` (import), lines 45-45, exports `datetime`, `timedelta`, `timezone`
- order 44: `_import_46` (import), lines 46-46, exports `HTTPStatus`
- order 45: `_import_47` (import), lines 47-47, exports `BaseHTTPRequestHandler`, `ThreadingHTTPServer`
- order 46: `_import_48` (import), lines 48-48, exports `Path`, `PurePosixPath`
- order 47: `_import_49` (import), lines 49-49, exports `HTTPError`, `URLError`
- order 48: `_import_50` (import), lines 50-50, exports `parse_qs`, `quote`, `unquote`, `urljoin`, `urlparse`, `urlunparse`
- order 49: `_import_51` (import), lines 51-51, exports `Request`, `urlopen`
- order 50: `_import_52` (import), lines 52-52, exports `robotparser`
- order 51: `_try_import_53` (import), lines 53-56, exports `_certifi`
- order 52: `_try_import_57` (import), lines 57-60, exports `_yaml`

### `admin/auth.py`

- order 675: `trusted_client_ip` (function), lines 7676-7708, exports `trusted_client_ip`
- order 683: `AdminAuthError` (class), lines 8099-8106, exports `AdminAuthError`
- order 684: `AdminAuthStore` (class), lines 8107-8377, exports `AdminAuthStore`

### `admin/config.py`

- order 685: `_admin_config_schema` (function), lines 8378-8485, exports `_admin_config_schema`
- order 686: `_admin_factory_config` (function), lines 8486-8489, exports `_admin_factory_config`
- order 687: `_admin_coerce_config` (function), lines 8490-8610, exports `_admin_coerce_config`
- order 688: `_admin_config_to_argv` (function), lines 8611-8647, exports `_admin_config_to_argv`
- order 689: `_admin_restart_probe_url` (function), lines 8648-8663, exports `_admin_restart_probe_url`
- order 690: `_admin_supervised_restart` (function), lines 8664-8750, exports `_admin_supervised_restart`
- order 691: `_admin_argparse_defaults` (function), lines 8751-8770, exports `_admin_argparse_defaults`
- order 692: `_admin_config_from_namespace` (function), lines 8771-8790, exports `_admin_config_from_namespace`

### `admin/constants.py`

- order 59: `ADMIN_STATE_DIRNAME` (constant), lines 67-67, exports `ADMIN_STATE_DIRNAME`
- order 60: `ADMIN_CONFIG_FILENAME` (constant), lines 68-68, exports `ADMIN_CONFIG_FILENAME`
- order 61: `ADMIN_APPS_FILENAME` (constant), lines 69-69, exports `ADMIN_APPS_FILENAME`
- order 62: `ADMIN_TELEMETRY_FILENAME` (constant), lines 70-70, exports `ADMIN_TELEMETRY_FILENAME`
- order 63: `ADMIN_AUTH_FILENAME` (constant), lines 71-71, exports `ADMIN_AUTH_FILENAME`
- order 64: `ADMIN_MAX_APP_SKILLS` (constant), lines 72-72, exports `ADMIN_MAX_APP_SKILLS`
- order 65: `ADMIN_MAX_APP_CAPSULE_CHARS` (constant), lines 73-73, exports `ADMIN_MAX_APP_CAPSULE_CHARS`
- order 66: `ADMIN_MAX_APP_RESOURCE_FILES` (constant), lines 74-74, exports `ADMIN_MAX_APP_RESOURCE_FILES`
- order 67: `ADMIN_MAX_APP_RESOURCE_BYTES` (constant), lines 75-75, exports `ADMIN_MAX_APP_RESOURCE_BYTES`
- order 68: `ADMIN_APP_INLINE_BLOB_BYTES` (constant), lines 76-76, exports `ADMIN_APP_INLINE_BLOB_BYTES`
- order 69: `ADMIN_AUTH_SESSION_TTL_SECONDS` (constant), lines 77-77, exports `ADMIN_AUTH_SESSION_TTL_SECONDS`
- order 70: `ADMIN_AUTH_PASSWORD_ITERATIONS` (constant), lines 78-78, exports `ADMIN_AUTH_PASSWORD_ITERATIONS`
- order 71: `ADMIN_AUTH_MAX_ACTIVE_SESSIONS` (constant), lines 79-79, exports `ADMIN_AUTH_MAX_ACTIVE_SESSIONS`

### `agent/background.py`

- order 751: `BackgroundManager` (class), lines 14948-15044, exports `BackgroundManager`

### `agent/bus.py`

- order 752: `MessageBus` (class), lines 15045-15110, exports `MessageBus`

### `agent/errors.py`

- order 624: `CircuitBreakerTriggered` (class), lines 6260-6263, exports `CircuitBreakerTriggered`

### `agent/events.py`

- order 709: `EventHub` (class), lines 9188-9234, exports `EventHub`

### `agent/tasks.py`

- order 750: `TaskManager` (class), lines 14813-14947, exports `TaskManager`

### `agent/todo.py`

- order 710: `TodoManager` (class), lines 9235-9595, exports `TodoManager`

### `agent/tools.py`

- order 767: `tool_def` (function), lines 18524-18537, exports `tool_def`
- order 768: `TOOLS` (constant), lines 18538-19020, exports `TOOLS`
- order 769: `TOOL_REQUIRED_ARGS` (constant), lines 19021-19022, exports `TOOL_REQUIRED_ARGS`
- order 770: `TOOL_SPEC_BY_NAME` (constant), lines 19023-19023, exports `TOOL_SPEC_BY_NAME`
- order 771: `_for_19024` (statement), lines 19024-19033, exports `_tool`, `_fn`, `_name`, `_required`
- order 772: `TOOL_NAME_FUZZY_MAP` (constant), lines 19034-19035, exports `TOOL_NAME_FUZZY_MAP`
- order 773: `_for_19036` (statement), lines 19036-19039, exports `_name`, `_key`
- order 774: `_for_19041` (statement), lines 19040-19057, exports `_alias`, `_target`
- order 775: `is_todo_resume_tool_name` (function), lines 19058-19074, exports `is_todo_resume_tool_name`
- order 776: `canonicalize_tool_name` (function), lines 19075-19093, exports `canonicalize_tool_name`
- order 777: `filter_tool_specs_for_runtime` (function), lines 19094-19109, exports `filter_tool_specs_for_runtime`
- order 778: `DEVELOPER_TOOL_DROP` (constant), lines 19110-19120, exports `DEVELOPER_TOOL_DROP`
- order 779: `AGENT_TOOL_ALLOWLIST` (constant), lines 19121-19181, exports `AGENT_TOOL_ALLOWLIST`

### `agent/worktree.py`

- order 753: `WorktreeManager` (class), lines 15111-15327, exports `WorktreeManager`

### `app/context.py`

- order 862: `AppContext` (class), lines 93037-97884, exports `AppContext`

### `app/main.py`

- order 872: `main` (function), lines 101469-103109, exports `main`
- order 873: `_main_guard_103111` (main_guard), lines 103110-103112, exports —

### `app/services.py`

- order 864: `TelemetryStore` (class), lines 97925-98300, exports `TelemetryStore`
- order 865: `ApplicationRegistry` (class), lines 98301-99043, exports `ApplicationRegistry`

### `config/constants.py`

- order 55: `APP_VERSION` (constant), lines 63-63, exports `APP_VERSION`
- order 80: `LONG_OUTPUT_MODEL_PAGE_CHARS` (constant), lines 155-155, exports `LONG_OUTPUT_MODEL_PAGE_CHARS`
- order 81: `LONG_OUTPUT_UI_PAGE_CHARS` (constant), lines 156-156, exports `LONG_OUTPUT_UI_PAGE_CHARS`
- order 82: `LONG_OUTPUT_UI_PREVIEW_MAX_PAGES` (constant), lines 157-157, exports `LONG_OUTPUT_UI_PREVIEW_MAX_PAGES`
- order 83: `LONG_OUTPUT_LISTING_OFFLOAD_CHARS` (constant), lines 158-158, exports `LONG_OUTPUT_LISTING_OFFLOAD_CHARS`
- order 84: `LONG_OUTPUT_READ_PAGE_LINES` (constant), lines 159-159, exports `LONG_OUTPUT_READ_PAGE_LINES`
- order 85: `LONG_OUTPUT_READ_PAGE_MAX_CHARS` (constant), lines 160-160, exports `LONG_OUTPUT_READ_PAGE_MAX_CHARS`
- order 86: `LONG_OUTPUT_TEMP_MAX_FILES` (constant), lines 161-161, exports `LONG_OUTPUT_TEMP_MAX_FILES`
- order 87: `READ_FILE_DEFAULT_MAX_CHARS` (constant), lines 162-162, exports `READ_FILE_DEFAULT_MAX_CHARS`
- order 88: `READ_FILE_HARD_MAX_CHARS` (constant), lines 163-163, exports `READ_FILE_HARD_MAX_CHARS`
- order 89: `READ_FILE_OVERVIEW_HEAD_LINES` (constant), lines 164-164, exports `READ_FILE_OVERVIEW_HEAD_LINES`
- order 90: `READ_FILE_SEARCH_MAX_MATCHES` (constant), lines 165-165, exports `READ_FILE_SEARCH_MAX_MATCHES`
- order 95: `CODE_ADMIN_PORT_OFFSET` (constant), lines 170-170, exports `CODE_ADMIN_PORT_OFFSET`
- order 97: `IDE_PORT_OFFSET` (constant), lines 172-175, exports `IDE_PORT_OFFSET`
- order 98: `IDE_DEFAULT_PORT` (constant), lines 176-176, exports `IDE_DEFAULT_PORT`
- order 100: `DEFAULT_WEB_SEARCH_ENABLED` (constant), lines 178-178, exports `DEFAULT_WEB_SEARCH_ENABLED`
- order 105: `DEFAULT_USER_MEMORY_MODE` (constant), lines 183-183, exports `DEFAULT_USER_MEMORY_MODE`
- order 113: `AGENT_WEB_SEARCH_USER_AGENT` (constant), lines 194-194, exports `AGENT_WEB_SEARCH_USER_AGENT`
- order 114: `AGENT_WEB_SEARCH_DEFAULT_MAX_RESULTS` (constant), lines 195-195, exports `AGENT_WEB_SEARCH_DEFAULT_MAX_RESULTS`
- order 115: `AGENT_WEB_SEARCH_DEFAULT_MAX_PAGES` (constant), lines 196-196, exports `AGENT_WEB_SEARCH_DEFAULT_MAX_PAGES`
- order 116: `AGENT_WEB_SEARCH_HARD_MAX_PAGES` (constant), lines 197-197, exports `AGENT_WEB_SEARCH_HARD_MAX_PAGES`
- order 117: `AGENT_WEB_SEARCH_DEFAULT_DEPTH` (constant), lines 198-198, exports `AGENT_WEB_SEARCH_DEFAULT_DEPTH`
- order 118: `AGENT_WEB_SEARCH_HARD_DEPTH` (constant), lines 199-199, exports `AGENT_WEB_SEARCH_HARD_DEPTH`
- order 119: `AGENT_WEB_SEARCH_FETCH_TIMEOUT` (constant), lines 200-200, exports `AGENT_WEB_SEARCH_FETCH_TIMEOUT`
- order 120: `AGENT_WEB_SEARCH_TOOL_SOFT_TIMEOUT` (constant), lines 201-201, exports `AGENT_WEB_SEARCH_TOOL_SOFT_TIMEOUT`
- order 121: `AGENT_WEB_SEARCH_MAX_PAGE_BYTES` (constant), lines 202-202, exports `AGENT_WEB_SEARCH_MAX_PAGE_BYTES`
- order 122: `AGENT_WEB_SEARCH_MAX_TEXT_CHARS` (constant), lines 203-203, exports `AGENT_WEB_SEARCH_MAX_TEXT_CHARS`
- order 132: `CODE_CHUNK_CHARS` (constant), lines 225-225, exports `CODE_CHUNK_CHARS`
- order 133: `CODE_CHUNK_OVERLAP` (constant), lines 226-226, exports `CODE_CHUNK_OVERLAP`
- order 134: `CODE_MAX_CHUNKS_PER_DOC` (constant), lines 227-227, exports `CODE_MAX_CHUNKS_PER_DOC`
- order 172: `CODE_IMPORT_WORKER_COUNT` (constant), lines 287-290, exports `CODE_IMPORT_WORKER_COUNT`
- order 174: `CODE_PARSE_TIMEOUT_SECONDS` (constant), lines 295-298, exports `CODE_PARSE_TIMEOUT_SECONDS`
- order 175: `DEFAULT_CONTEXT_TOKEN_LIMIT` (constant), lines 299-299, exports `DEFAULT_CONTEXT_TOKEN_LIMIT`
- order 176: `TOKEN_THRESHOLD` (constant), lines 300-300, exports `TOKEN_THRESHOLD`
- order 177: `CONTEXT_AUTO_COMPACT_RESERVE_RATIO` (constant), lines 301-304, exports `CONTEXT_AUTO_COMPACT_RESERVE_RATIO`
- order 178: `CONTEXT_ESTIMATE_SAFETY_MULTIPLIER` (constant), lines 305-308, exports `CONTEXT_ESTIMATE_SAFETY_MULTIPLIER`
- order 179: `CONTEXT_USAGE_CALIBRATION_MAX` (constant), lines 309-312, exports `CONTEXT_USAGE_CALIBRATION_MAX`
- order 180: `CONTEXT_ACTUAL_USAGE_RECENT_SECONDS` (constant), lines 313-316, exports `CONTEXT_ACTUAL_USAGE_RECENT_SECONDS`
- order 181: `LARGE_FILE_AUTO_PAGE_BYTES` (constant), lines 317-320, exports `LARGE_FILE_AUTO_PAGE_BYTES`
- order 182: `LARGE_FILE_AUTO_PAGE_LINES` (constant), lines 321-324, exports `LARGE_FILE_AUTO_PAGE_LINES`
- order 183: `LARGE_SOURCE_UPLOAD_EXCERPT_CHARS` (constant), lines 325-328, exports `LARGE_SOURCE_UPLOAD_EXCERPT_CHARS`
- order 184: `CHAT_UPLOAD_PARSE_QUEUE_MAX` (constant), lines 329-332, exports `CHAT_UPLOAD_PARSE_QUEUE_MAX`
- order 185: `CHAT_UPLOAD_PARSE_TIMEOUT_SECONDS` (constant), lines 333-336, exports `CHAT_UPLOAD_PARSE_TIMEOUT_SECONDS`
- order 186: `CHAT_UPLOAD_INLINE_TEXT_BYTES` (constant), lines 337-340, exports `CHAT_UPLOAD_INLINE_TEXT_BYTES`
- order 187: `CHAT_UPLOAD_PARSE_MAX_BYTES` (constant), lines 341-347, exports `CHAT_UPLOAD_PARSE_MAX_BYTES`
- order 188: `CHAT_UPLOAD_ZIP_ENTRY_MAX_BYTES` (constant), lines 348-354, exports `CHAT_UPLOAD_ZIP_ENTRY_MAX_BYTES`
- order 189: `CHAT_UPLOAD_TEXT_CONTEXT_CHARS` (constant), lines 355-358, exports `CHAT_UPLOAD_TEXT_CONTEXT_CHARS`
- order 190: `CHAT_UPLOAD_PROMPT_MAX_FILES` (constant), lines 359-362, exports `CHAT_UPLOAD_PROMPT_MAX_FILES`
- order 191: `CHAT_UPLOAD_PROMPT_MAX_CHARS` (constant), lines 363-366, exports `CHAT_UPLOAD_PROMPT_MAX_CHARS`
- order 192: `CHAT_UPLOAD_PROMPT_PER_FILE_CHARS` (constant), lines 367-370, exports `CHAT_UPLOAD_PROMPT_PER_FILE_CHARS`
- order 193: `CHAT_UPLOAD_FRONTEND_WAIT_MS` (constant), lines 371-374, exports `CHAT_UPLOAD_FRONTEND_WAIT_MS`
- order 194: `CHAT_UPLOAD_AUTO_LIBRARY_INGEST` (constant), lines 375-378, exports `CHAT_UPLOAD_AUTO_LIBRARY_INGEST`
- order 195: `CHAT_UPLOAD_INGEST_QUEUE_MAX` (constant), lines 379-382, exports `CHAT_UPLOAD_INGEST_QUEUE_MAX`
- order 196: `SESSION_SUBMIT_LOCK_TIMEOUT_SECONDS` (constant), lines 383-386, exports `SESSION_SUBMIT_LOCK_TIMEOUT_SECONDS`
- order 197: `SESSION_DEFERRED_START_QUEUE_MAX` (constant), lines 387-390, exports `SESSION_DEFERRED_START_QUEUE_MAX`
- order 198: `SESSION_WATCHDOG_INTERVAL_SECONDS` (constant), lines 391-394, exports `SESSION_WATCHDOG_INTERVAL_SECONDS`
- order 199: `SESSION_HEARTBEAT_STALE_SECONDS` (constant), lines 395-398, exports `SESSION_HEARTBEAT_STALE_SECONDS`
- order 200: `SESSION_LIST_DEFAULT_LIMIT` (constant), lines 399-402, exports `SESSION_LIST_DEFAULT_LIMIT`
- order 201: `IDLE_TIMEOUT` (constant), lines 403-403, exports `IDLE_TIMEOUT`
- order 202: `POLL_INTERVAL` (constant), lines 404-404, exports `POLL_INTERVAL`
- order 203: `SSE_HEARTBEAT_SECONDS` (constant), lines 405-405, exports `SSE_HEARTBEAT_SECONDS`
- order 204: `MODEL_CALL_PROGRESS_DELAY` (constant), lines 406-406, exports `MODEL_CALL_PROGRESS_DELAY`
- order 205: `MODEL_CALL_PROGRESS_INTERVAL` (constant), lines 407-407, exports `MODEL_CALL_PROGRESS_INTERVAL`
- order 206: `RUN_COMPLETION_SUMMARY_ENABLED` (constant), lines 408-411, exports `RUN_COMPLETION_SUMMARY_ENABLED`
- order 207: `LLM_HTTP_RETRY_MAX_ATTEMPTS` (constant), lines 412-415, exports `LLM_HTTP_RETRY_MAX_ATTEMPTS`
- order 208: `LLM_HTTP_RETRY_DELAY_SECONDS` (constant), lines 416-419, exports `LLM_HTTP_RETRY_DELAY_SECONDS`
- order 209: `LLM_HTTP_RETRY_MAX_SECONDS` (constant), lines 420-423, exports `LLM_HTTP_RETRY_MAX_SECONDS`
- order 210: `LLM_HTTP_RETRY_404_ON_VLLM` (constant), lines 424-427, exports `LLM_HTTP_RETRY_404_ON_VLLM`
- order 211: `LLM_HTTP_RETRY_STATUSES` (constant), lines 428-428, exports `LLM_HTTP_RETRY_STATUSES`
- order 212: `MAX_AGENT_ROUNDS` (constant), lines 429-429, exports `MAX_AGENT_ROUNDS`
- order 213: `MIN_AGENT_ROUNDS` (constant), lines 430-430, exports `MIN_AGENT_ROUNDS`
- order 214: `MAX_AGENT_ROUNDS_CAP` (constant), lines 431-431, exports `MAX_AGENT_ROUNDS_CAP`
- order 215: `REPEATED_TOOL_LOOP_THRESHOLD` (constant), lines 432-432, exports `REPEATED_TOOL_LOOP_THRESHOLD`
- order 216: `BASH_READ_LOOP_THRESHOLD` (constant), lines 433-433, exports `BASH_READ_LOOP_THRESHOLD`
- order 217: `READ_FILE_LOOP_THRESHOLD` (constant), lines 434-434, exports `READ_FILE_LOOP_THRESHOLD`
- order 218: `READ_FILE_LOOP_DISTINCT_SOFT_LIMIT` (constant), lines 435-435, exports `READ_FILE_LOOP_DISTINCT_SOFT_LIMIT`
- order 219: `READ_FILE_COMPACT_PIN_DISTINCT` (constant), lines 436-436, exports `READ_FILE_COMPACT_PIN_DISTINCT`
- order 220: `READ_FILE_COMPACT_PIN_MAX_CHARS` (constant), lines 437-437, exports `READ_FILE_COMPACT_PIN_MAX_CHARS`
- order 221: `READ_CONTEXT_REGISTRY_MAX` (constant), lines 438-438, exports `READ_CONTEXT_REGISTRY_MAX`
- order 222: `READ_CONTEXT_PROMPT_MAX_ITEMS` (constant), lines 439-439, exports `READ_CONTEXT_PROMPT_MAX_ITEMS`
- order 223: `READ_CONTEXT_PROMPT_MAX_CHARS` (constant), lines 440-440, exports `READ_CONTEXT_PROMPT_MAX_CHARS`
- order 224: `READ_CONTEXT_SUMMARY_MAX_CHARS` (constant), lines 441-441, exports `READ_CONTEXT_SUMMARY_MAX_CHARS`
- order 225: `READ_CONTEXT_SHARED_MAX_ITEMS` (constant), lines 442-442, exports `READ_CONTEXT_SHARED_MAX_ITEMS`
- order 226: `READ_CONTEXT_POLICY_CHOICES` (constant), lines 443-443, exports `READ_CONTEXT_POLICY_CHOICES`
- order 227: `DEFAULT_READ_CONTEXT_POLICY` (constant), lines 444-444, exports `DEFAULT_READ_CONTEXT_POLICY`
- order 228: `TOOL_MEMORY_REGISTRY_MAX` (constant), lines 445-445, exports `TOOL_MEMORY_REGISTRY_MAX`
- order 229: `TOOL_MEMORY_PROMPT_MAX_ITEMS` (constant), lines 446-446, exports `TOOL_MEMORY_PROMPT_MAX_ITEMS`
- order 230: `TOOL_MEMORY_PROMPT_MAX_CHARS` (constant), lines 447-447, exports `TOOL_MEMORY_PROMPT_MAX_CHARS`
- order 231: `TOOL_MEMORY_SUMMARY_MAX_CHARS` (constant), lines 448-448, exports `TOOL_MEMORY_SUMMARY_MAX_CHARS`
- order 232: `TOOL_MEMORY_SHARED_MAX_ITEMS` (constant), lines 449-449, exports `TOOL_MEMORY_SHARED_MAX_ITEMS`
- order 233: `TOOL_MEMORY_COMPACT_PIN_DISTINCT` (constant), lines 450-450, exports `TOOL_MEMORY_COMPACT_PIN_DISTINCT`
- order 234: `TOOL_MEMORY_COMPACT_PIN_MAX_CHARS` (constant), lines 451-451, exports `TOOL_MEMORY_COMPACT_PIN_MAX_CHARS`
- order 235: `TOOL_MEMORY_POLICY_CHOICES` (constant), lines 452-452, exports `TOOL_MEMORY_POLICY_CHOICES`
- order 236: `DEFAULT_TOOL_MEMORY_POLICY` (constant), lines 453-453, exports `DEFAULT_TOOL_MEMORY_POLICY`
- order 237: `DEFAULT_AUTO_TASK_LEVEL_CEILING` (constant), lines 454-454, exports `DEFAULT_AUTO_TASK_LEVEL_CEILING`
- order 238: `HARD_BREAK_TOOL_ERROR_THRESHOLD` (constant), lines 455-455, exports `HARD_BREAK_TOOL_ERROR_THRESHOLD`
- order 239: `HARD_BREAK_RECOVERY_ROUND_THRESHOLD` (constant), lines 456-456, exports `HARD_BREAK_RECOVERY_ROUND_THRESHOLD`
- order 240: `FUSED_FAULT_BREAK_THRESHOLD` (constant), lines 457-457, exports `FUSED_FAULT_BREAK_THRESHOLD`
- order 241: `STALL_SEVERITY_ESCALATION_THRESHOLD` (constant), lines 458-458, exports `STALL_SEVERITY_ESCALATION_THRESHOLD`
- order 242: `STALL_SEVERITY_WEIGHT_BASH_READ_LOOP` (constant), lines 459-459, exports `STALL_SEVERITY_WEIGHT_BASH_READ_LOOP`
- order 243: `STALL_SEVERITY_WEIGHT_REPEATED_TOOL` (constant), lines 460-460, exports `STALL_SEVERITY_WEIGHT_REPEATED_TOOL`
- order 244: `STALL_SEVERITY_WEIGHT_FAULT` (constant), lines 461-461, exports `STALL_SEVERITY_WEIGHT_FAULT`
- order 245: `STALL_SEVERITY_WEIGHT_RECOVERY_RETRY` (constant), lines 462-462, exports `STALL_SEVERITY_WEIGHT_RECOVERY_RETRY`
- order 246: `STALL_SEVERITY_WEIGHT_WATCHDOG` (constant), lines 463-463, exports `STALL_SEVERITY_WEIGHT_WATCHDOG`
- order 247: `STALL_SEVERITY_DECAY_ON_SUCCESS` (constant), lines 464-464, exports `STALL_SEVERITY_DECAY_ON_SUCCESS`
- order 248: `STALL_ESCALATION_MIN_LEVEL` (constant), lines 465-465, exports `STALL_ESCALATION_MIN_LEVEL`
- order 249: `STALL_PLAN_SYNTHESIS_MAX_TOKENS` (constant), lines 466-466, exports `STALL_PLAN_SYNTHESIS_MAX_TOKENS`
- order 250: `STALL_ESCALATION_CONTEXT_MAX_CHARS` (constant), lines 467-467, exports `STALL_ESCALATION_CONTEXT_MAX_CHARS`
- order 251: `MAX_RUN_SECONDS` (constant), lines 468-468, exports `MAX_RUN_SECONDS`
- order 252: `MIN_RUN_TIMEOUT_SECONDS` (constant), lines 469-469, exports `MIN_RUN_TIMEOUT_SECONDS`
- order 253: `MAX_RUN_TIMEOUT_SECONDS` (constant), lines 470-470, exports `MAX_RUN_TIMEOUT_SECONDS`
- order 254: `MIN_TIMEOUT_SECONDS` (constant), lines 471-471, exports `MIN_TIMEOUT_SECONDS`
- order 255: `MAX_TIMEOUT_SECONDS` (constant), lines 472-472, exports `MAX_TIMEOUT_SECONDS`
- order 256: `DEFAULT_TIMEOUT_SECONDS` (constant), lines 473-479, exports `DEFAULT_TIMEOUT_SECONDS`
- order 257: `DEFAULT_REQUEST_TIMEOUT` (constant), lines 480-480, exports `DEFAULT_REQUEST_TIMEOUT`
- order 258: `_SHELL_AUTO_CONFIRM_PATTERNS` (assignment), lines 481-496, exports `_SHELL_AUTO_CONFIRM_PATTERNS`
- order 259: `MIN_SHELL_COMMAND_TIMEOUT_SECONDS` (constant), lines 497-497, exports `MIN_SHELL_COMMAND_TIMEOUT_SECONDS`
- order 260: `MAX_SHELL_COMMAND_TIMEOUT_SECONDS` (constant), lines 498-498, exports `MAX_SHELL_COMMAND_TIMEOUT_SECONDS`
- order 261: `DEFAULT_SHELL_COMMAND_TIMEOUT_SECONDS` (constant), lines 499-513, exports `DEFAULT_SHELL_COMMAND_TIMEOUT_SECONDS`
- order 262: `DEFAULT_SINGLE_NO_PLAN_TODO_PROMPT` (constant), lines 514-526, exports `DEFAULT_SINGLE_NO_PLAN_TODO_PROMPT`
- order 263: `SINGLE_NO_PLAN_TODO_BOOTSTRAP_MAX_ATTEMPTS` (constant), lines 527-527, exports `SINGLE_NO_PLAN_TODO_BOOTSTRAP_MAX_ATTEMPTS`
- order 264: `AUTO_CONTINUE_BUDGET_DEFAULT` (constant), lines 528-528, exports `AUTO_CONTINUE_BUDGET_DEFAULT`
- order 265: `AGENT_MAX_OUTPUT_TOKENS` (constant), lines 529-529, exports `AGENT_MAX_OUTPUT_TOKENS`
- order 266: `OLLAMA_THINKING_TOOL_BUFFER` (constant), lines 530-530, exports `OLLAMA_THINKING_TOOL_BUFFER`
- order 267: `WATCHDOG_INTENT_NO_TOOL_THRESHOLD` (constant), lines 531-531, exports `WATCHDOG_INTENT_NO_TOOL_THRESHOLD`
- order 268: `WATCHDOG_REPEAT_NO_TOOL_THRESHOLD` (constant), lines 532-532, exports `WATCHDOG_REPEAT_NO_TOOL_THRESHOLD`
- order 269: `WATCHDOG_INTENT_NO_TOOL_THRESHOLD_SINGLE` (constant), lines 533-533, exports `WATCHDOG_INTENT_NO_TOOL_THRESHOLD_SINGLE`
- order 270: `WATCHDOG_REPEAT_NO_TOOL_THRESHOLD_SINGLE` (constant), lines 534-534, exports `WATCHDOG_REPEAT_NO_TOOL_THRESHOLD_SINGLE`
- order 271: `WATCHDOG_STATE_STALL_THRESHOLD` (constant), lines 535-535, exports `WATCHDOG_STATE_STALL_THRESHOLD`
- order 272: `WATCHDOG_CONTEXT_STALL_THRESHOLD` (constant), lines 536-536, exports `WATCHDOG_CONTEXT_STALL_THRESHOLD`
- order 273: `WATCHDOG_REPEAT_SIMILARITY_THRESHOLD` (constant), lines 537-537, exports `WATCHDOG_REPEAT_SIMILARITY_THRESHOLD`
- order 274: `WATCHDOG_CONTEXT_NEAR_RATIO` (constant), lines 538-538, exports `WATCHDOG_CONTEXT_NEAR_RATIO`
- order 275: `WATCHDOG_MAX_DECOMPOSE_STEPS` (constant), lines 539-539, exports `WATCHDOG_MAX_DECOMPOSE_STEPS`
- order 276: `WATCHDOG_STEP_MAX_ATTEMPTS` (constant), lines 540-540, exports `WATCHDOG_STEP_MAX_ATTEMPTS`
- order 277: `EMPTY_ACTION_MIN_CONTENT_CHARS` (constant), lines 541-541, exports `EMPTY_ACTION_MIN_CONTENT_CHARS`
- order 278: `EMPTY_ACTION_WAKEUP_RETRY_LIMIT` (constant), lines 542-542, exports `EMPTY_ACTION_WAKEUP_RETRY_LIMIT`
- order 279: `THINKING_BUDGET_FORCE_RATIO` (constant), lines 543-543, exports `THINKING_BUDGET_FORCE_RATIO`
- order 280: `_TOOL_TIMEOUT_MAP` (assignment), lines 544-562, exports `_TOOL_TIMEOUT_MAP`
- order 281: `_DEFAULT_TOOL_TIMEOUT` (assignment), lines 563-563, exports `_DEFAULT_TOOL_TIMEOUT`
- order 282: `CONVERSATION_VISIBLE_TOOL_EVENTS` (constant), lines 564-574, exports `CONVERSATION_VISIBLE_TOOL_EVENTS`
- order 283: `PERSIST_ON_EVENT_TYPES` (constant), lines 575-589, exports `PERSIST_ON_EVENT_TYPES`
- order 284: `PERSIST_EVENT_MIN_INTERVAL_SECONDS` (constant), lines 590-590, exports `PERSIST_EVENT_MIN_INTERVAL_SECONDS`
- order 285: `TRUNCATION_CONTINUATION_MAX_PASSES` (constant), lines 591-591, exports `TRUNCATION_CONTINUATION_MAX_PASSES`
- order 286: `TRUNCATION_CONTINUATION_MAX_TOKENS` (constant), lines 592-592, exports `TRUNCATION_CONTINUATION_MAX_TOKENS`
- order 287: `TRUNCATION_CONTINUATION_TAIL_CHARS` (constant), lines 593-593, exports `TRUNCATION_CONTINUATION_TAIL_CHARS`
- order 288: `TRUNCATION_CONTINUATION_ECHO_CHARS` (constant), lines 594-594, exports `TRUNCATION_CONTINUATION_ECHO_CHARS`
- order 289: `TRUNCATION_OVERLAP_SCAN_CHARS` (constant), lines 595-595, exports `TRUNCATION_OVERLAP_SCAN_CHARS`
- order 290: `TRUNCATION_PAIR_SCAN_CHARS` (constant), lines 596-596, exports `TRUNCATION_PAIR_SCAN_CHARS`
- order 291: `TRUNCATION_LIVE_BUFFER_MAX_CHARS` (constant), lines 597-597, exports `TRUNCATION_LIVE_BUFFER_MAX_CHARS`
- order 292: `MIN_CONTEXT_TOKEN_LIMIT` (constant), lines 598-598, exports `MIN_CONTEXT_TOKEN_LIMIT`
- order 293: `COMPACT_TIER1_PCT` (constant), lines 599-600, exports `COMPACT_TIER1_PCT`
- order 294: `COMPACT_TIER2_PCT` (constant), lines 601-601, exports `COMPACT_TIER2_PCT`
- order 295: `COMPACT_TIER3_PCT` (constant), lines 602-602, exports `COMPACT_TIER3_PCT`
- order 296: `COMPACT_TIER1_ABS` (constant), lines 603-604, exports `COMPACT_TIER1_ABS`
- order 297: `COMPACT_TIER2_ABS` (constant), lines 605-605, exports `COMPACT_TIER2_ABS`
- order 298: `CONTEXT_COMPACT_INEFFECTIVE_COOLDOWN_SECONDS` (constant), lines 606-612, exports `CONTEXT_COMPACT_INEFFECTIVE_COOLDOWN_SECONDS`
- order 299: `FILE_BUFFER_CONTENT_THRESHOLD` (constant), lines 613-614, exports `FILE_BUFFER_CONTENT_THRESHOLD`
- order 300: `FILE_BUFFER_MAX_FILES` (constant), lines 615-615, exports `FILE_BUFFER_MAX_FILES`
- order 301: `AGENT_MSG_LIMIT_TIER0` (constant), lines 616-617, exports `AGENT_MSG_LIMIT_TIER0`
- order 302: `AGENT_MSG_LIMIT_TIER1` (constant), lines 618-618, exports `AGENT_MSG_LIMIT_TIER1`
- order 303: `AGENT_MSG_LIMIT_TIER2` (constant), lines 619-619, exports `AGENT_MSG_LIMIT_TIER2`
- order 304: `AGENT_MSG_LIMIT_TIER3` (constant), lines 620-620, exports `AGENT_MSG_LIMIT_TIER3`
- order 305: `AGENT_CTX_LIMIT_TIER0` (constant), lines 621-621, exports `AGENT_CTX_LIMIT_TIER0`
- order 306: `AGENT_CTX_LIMIT_TIER1` (constant), lines 622-622, exports `AGENT_CTX_LIMIT_TIER1`
- order 307: `AGENT_CTX_LIMIT_TIER2` (constant), lines 623-623, exports `AGENT_CTX_LIMIT_TIER2`
- order 308: `AGENT_CTX_LIMIT_TIER3` (constant), lines 624-624, exports `AGENT_CTX_LIMIT_TIER3`
- order 309: `MANAGER_CTX_LIMIT_TIER0` (constant), lines 625-625, exports `MANAGER_CTX_LIMIT_TIER0`
- order 310: `MANAGER_CTX_LIMIT_TIER1` (constant), lines 626-626, exports `MANAGER_CTX_LIMIT_TIER1`
- order 311: `MANAGER_CTX_LIMIT_TIER2` (constant), lines 627-627, exports `MANAGER_CTX_LIMIT_TIER2`
- order 312: `MANAGER_CTX_LIMIT_TIER3` (constant), lines 628-628, exports `MANAGER_CTX_LIMIT_TIER3`
- order 313: `MAX_CONTEXT_ARCHIVE_SEGMENTS` (constant), lines 629-629, exports `MAX_CONTEXT_ARCHIVE_SEGMENTS`
- order 314: `MAX_USER_BUBBLE_LOG` (constant), lines 630-631, exports `MAX_USER_BUBBLE_LOG`
- order 315: `MANAGER_INSTRUCTION_MAX_CHARS` (constant), lines 632-636, exports `MANAGER_INSTRUCTION_MAX_CHARS`
- order 316: `MANAGER_MOMENTUM_MAX_SKIPS` (constant), lines 637-642, exports `MANAGER_MOMENTUM_MAX_SKIPS`
- order 317: `EXPLORER_CODING_CAP` (constant), lines 643-647, exports `EXPLORER_CODING_CAP`
- order 318: `MODEL_OUTPUT_RETRY_TIMES` (constant), lines 648-648, exports `MODEL_OUTPUT_RETRY_TIMES`
- order 319: `ARBITER_TRIGGER_MIN_CONTENT_CHARS` (constant), lines 649-649, exports `ARBITER_TRIGGER_MIN_CONTENT_CHARS`
- order 320: `ARBITER_VALID_PLANNING_STREAK_LIMIT` (constant), lines 650-650, exports `ARBITER_VALID_PLANNING_STREAK_LIMIT`
- order 321: `ARBITER_DEFAULT_TIMEOUT_SECONDS` (constant), lines 651-651, exports `ARBITER_DEFAULT_TIMEOUT_SECONDS`
- order 322: `ARBITER_DEFAULT_MAX_TOKENS` (constant), lines 652-652, exports `ARBITER_DEFAULT_MAX_TOKENS`
- order 323: `ARBITER_DEFAULT_TEMPERATURE` (constant), lines 653-653, exports `ARBITER_DEFAULT_TEMPERATURE`
- order 324: `LIVE_INPUT_DELAY_WRITE_ROUNDS` (constant), lines 654-654, exports `LIVE_INPUT_DELAY_WRITE_ROUNDS`
- order 325: `LIVE_INPUT_DELAY_TOOL_ROUNDS` (constant), lines 655-655, exports `LIVE_INPUT_DELAY_TOOL_ROUNDS`
- order 326: `LIVE_INPUT_DELAY_NORMAL_ROUNDS` (constant), lines 656-656, exports `LIVE_INPUT_DELAY_NORMAL_ROUNDS`
- order 327: `LIVE_INPUT_MAX_INJECTIONS` (constant), lines 657-657, exports `LIVE_INPUT_MAX_INJECTIONS`
- order 328: `LIVE_INPUT_REINJECT_INTERVAL` (constant), lines 658-658, exports `LIVE_INPUT_REINJECT_INTERVAL`
- order 329: `LIVE_INPUT_WEIGHT_BASE_DELAYED` (constant), lines 659-659, exports `LIVE_INPUT_WEIGHT_BASE_DELAYED`
- order 330: `LIVE_INPUT_WEIGHT_BASE_NORMAL` (constant), lines 660-660, exports `LIVE_INPUT_WEIGHT_BASE_NORMAL`
- order 331: `LIVE_INPUT_WEIGHT_STEP_DELAYED` (constant), lines 661-661, exports `LIVE_INPUT_WEIGHT_STEP_DELAYED`
- order 332: `LIVE_INPUT_WEIGHT_STEP_NORMAL` (constant), lines 662-662, exports `LIVE_INPUT_WEIGHT_STEP_NORMAL`
- order 334: `BENIGN_SOCKET_DEBUG_LOG_ENABLED` (constant), lines 669-675, exports `BENIGN_SOCKET_DEBUG_LOG_ENABLED`
- order 335: `BENIGN_SOCKET_LOG_INTERVAL_SECONDS` (constant), lines 676-676, exports `BENIGN_SOCKET_LOG_INTERVAL_SECONDS`
- order 336: `FINAL_SUMMARY_MIN_CHARS` (constant), lines 677-677, exports `FINAL_SUMMARY_MIN_CHARS`
- order 337: `FINAL_SUMMARY_STRICT_MIN_CHARS` (constant), lines 678-678, exports `FINAL_SUMMARY_STRICT_MIN_CHARS`
- order 338: `RUNTIME_CONTROL_HINT_PREFIXES` (constant), lines 679-698, exports `RUNTIME_CONTROL_HINT_PREFIXES`
- order 339: `RETRY_RUNTIME_HINT_PREFIXES` (constant), lines 699-713, exports `RETRY_RUNTIME_HINT_PREFIXES`
- order 340: `EXECUTION_MODE_SINGLE` (constant), lines 714-714, exports `EXECUTION_MODE_SINGLE`
- order 341: `EXECUTION_MODE_SEQUENTIAL` (constant), lines 715-715, exports `EXECUTION_MODE_SEQUENTIAL`
- order 342: `EXECUTION_MODE_SYNC` (constant), lines 716-716, exports `EXECUTION_MODE_SYNC`
- order 343: `EXECUTION_MODE_CHOICES` (constant), lines 717-721, exports `EXECUTION_MODE_CHOICES`
- order 344: `AGENT_ROLES` (constant), lines 722-722, exports `AGENT_ROLES`
- order 345: `AGENT_BUBBLE_ROLES` (constant), lines 723-723, exports `AGENT_BUBBLE_ROLES`
- order 346: `AGENT_ROLE_LABELS` (constant), lines 724-730, exports `AGENT_ROLE_LABELS`
- order 347: `AGENT_ROLE_BUBBLE_COLORS` (constant), lines 731-737, exports `AGENT_ROLE_BUBBLE_COLORS`
- order 348: `BLACKBOARD_STATUSES` (constant), lines 738-747, exports `BLACKBOARD_STATUSES`
- order 349: `TASK_COMPLEXITY_LEVELS` (constant), lines 748-748, exports `TASK_COMPLEXITY_LEVELS`
- order 350: `TASK_COMPLEXITY_RANKS` (constant), lines 749-754, exports `TASK_COMPLEXITY_RANKS`
- order 351: `TASK_PROFILE_TYPES` (constant), lines 755-761, exports `TASK_PROFILE_TYPES`
- order 352: `TASK_LEVEL_CHOICES` (constant), lines 762-762, exports `TASK_LEVEL_CHOICES`
- order 353: `TASK_SCALE_PREFERENCES` (constant), lines 763-763, exports `TASK_SCALE_PREFERENCES`
- order 354: `SEMANTIC_CONFIDENCE_CHOICES` (constant), lines 764-764, exports `SEMANTIC_CONFIDENCE_CHOICES`
- order 355: `L2_TODO_POLICY_CHOICES` (constant), lines 765-769, exports `L2_TODO_POLICY_CHOICES`
- order 356: `DEFAULT_L2_TODO_POLICY` (constant), lines 770-770, exports `DEFAULT_L2_TODO_POLICY`
- order 357: `TASK_LEVEL_POLICIES` (constant), lines 771-824, exports `TASK_LEVEL_POLICIES`
- order 358: `MANAGER_ROUTE_TARGETS` (constant), lines 825-825, exports `MANAGER_ROUTE_TARGETS`
- order 359: `BLACKBOARD_MAX_LOG_ENTRIES` (constant), lines 826-826, exports `BLACKBOARD_MAX_LOG_ENTRIES`
- order 360: `BLACKBOARD_MAX_TEXT` (constant), lines 827-827, exports `BLACKBOARD_MAX_TEXT`
- order 361: `BLACKBOARD_MEMORY_SHORT_MAX` (constant), lines 828-828, exports `BLACKBOARD_MEMORY_SHORT_MAX`
- order 362: `BLACKBOARD_MEMORY_MID_MAX_STEPS` (constant), lines 829-829, exports `BLACKBOARD_MEMORY_MID_MAX_STEPS`
- order 363: `BLACKBOARD_MEMORY_MID_ITEMS_PER_STEP` (constant), lines 830-830, exports `BLACKBOARD_MEMORY_MID_ITEMS_PER_STEP`
- order 364: `BLACKBOARD_MEMORY_LONG_MAX` (constant), lines 831-831, exports `BLACKBOARD_MEMORY_LONG_MAX`
- order 365: `BLACKBOARD_MEMORY_INDEX_MAX` (constant), lines 832-832, exports `BLACKBOARD_MEMORY_INDEX_MAX`
- order 366: `SKILL_REFRESH_MIN_INTERVAL_SECONDS` (constant), lines 833-833, exports `SKILL_REFRESH_MIN_INTERVAL_SECONDS`
- order 367: `SKILL_PROMPT_MAX_ITEMS` (constant), lines 834-834, exports `SKILL_PROMPT_MAX_ITEMS`
- order 368: `SKILL_PROMPT_MAX_CHARS` (constant), lines 835-835, exports `SKILL_PROMPT_MAX_CHARS`
- order 369: `SKILL_RUNTIME_CACHE_MAX_ENTRIES` (constant), lines 836-836, exports `SKILL_RUNTIME_CACHE_MAX_ENTRIES`
- order 370: `SKILL_RUNTIME_CACHE_MAX_BYTES` (constant), lines 837-837, exports `SKILL_RUNTIME_CACHE_MAX_BYTES`
- order 371: `AUTO_SKILLS_ROOT_CANDIDATES` (constant), lines 838-838, exports `AUTO_SKILLS_ROOT_CANDIDATES`
- order 372: `SKILL_DEFAULT_ATTACHMENT_GLOBS` (constant), lines 839-869, exports `SKILL_DEFAULT_ATTACHMENT_GLOBS`
- order 373: `SKILL_INLINE_ATTACHMENT_MAX_FILES` (constant), lines 870-870, exports `SKILL_INLINE_ATTACHMENT_MAX_FILES`
- order 374: `SKILL_INLINE_ATTACHMENT_MAX_CHARS` (constant), lines 871-871, exports `SKILL_INLINE_ATTACHMENT_MAX_CHARS`
- order 375: `SKILL_RESOURCE_MANIFEST_MAX_ITEMS` (constant), lines 872-872, exports `SKILL_RESOURCE_MANIFEST_MAX_ITEMS`
- order 376: `SKILL_BODY_COMPACT_THRESHOLD_CHARS` (constant), lines 873-873, exports `SKILL_BODY_COMPACT_THRESHOLD_CHARS`
- order 377: `SKILL_BODY_PREVIEW_CHARS` (constant), lines 874-874, exports `SKILL_BODY_PREVIEW_CHARS`
- order 378: `SKILLS_VIRTUAL_PREFIX` (constant), lines 875-875, exports `SKILLS_VIRTUAL_PREFIX`
- order 379: `SKILLS_EXTERNAL_MOUNT` (constant), lines 876-876, exports `SKILLS_EXTERNAL_MOUNT`
- order 380: `PLAN_MODE_ENABLED_LEVELS` (constant), lines 877-877, exports `PLAN_MODE_ENABLED_LEVELS`
- order 381: `PLAN_MODE_FORCED_LEVELS` (constant), lines 878-878, exports `PLAN_MODE_FORCED_LEVELS`
- order 382: `PLAN_MODE_USER_CHOICES` (constant), lines 879-879, exports `PLAN_MODE_USER_CHOICES`
- order 383: `TASK_PHASES` (constant), lines 880-881, exports `TASK_PHASES`
- order 384: `TASK_PHASE_ROUTING` (constant), lines 882-889, exports `TASK_PHASE_ROUTING`
- order 385: `COMPLEXITY_KEYWORDS` (constant), lines 890-896, exports `COMPLEXITY_KEYWORDS`
- order 386: `USER_COMPLEXITY_SIMPLE_TOKENS` (constant), lines 897-901, exports `USER_COMPLEXITY_SIMPLE_TOKENS`
- order 387: `USER_COMPLEXITY_MODERATE_TOKENS` (constant), lines 902-906, exports `USER_COMPLEXITY_MODERATE_TOKENS`
- order 388: `USER_COMPLEXITY_COMPLEX_TOKENS` (constant), lines 907-911, exports `USER_COMPLEXITY_COMPLEX_TOKENS`
- order 389: `USER_COMPLEXITY_EXPERT_TOKENS` (constant), lines 912-916, exports `USER_COMPLEXITY_EXPERT_TOKENS`
- order 390: `PLAN_MODE_EXPLORER_MAX_ROUNDS` (constant), lines 917-920, exports `PLAN_MODE_EXPLORER_MAX_ROUNDS`
- order 391: `PLAN_MODE_EXPLORER_PRODUCTIVE_ROUNDS` (constant), lines 921-921, exports `PLAN_MODE_EXPLORER_PRODUCTIVE_ROUNDS`
- order 392: `PLAN_MODE_EXPLORER_STALE_ROUNDS` (constant), lines 922-922, exports `PLAN_MODE_EXPLORER_STALE_ROUNDS`
- order 393: `PLAN_MODE_SYNTHESIS_MAX_ATTEMPTS` (constant), lines 923-923, exports `PLAN_MODE_SYNTHESIS_MAX_ATTEMPTS`
- order 394: `REVIEWER_DEBUG_MODE_MAX_ROUNDS` (constant), lines 924-925, exports `REVIEWER_DEBUG_MODE_MAX_ROUNDS`
- order 395: `REVIEWER_DEBUG_TOOL_ALLOWLIST` (constant), lines 926-930, exports `REVIEWER_DEBUG_TOOL_ALLOWLIST`
- order 396: `EXPLORER_STALL_THRESHOLD` (constant), lines 931-931, exports `EXPLORER_STALL_THRESHOLD`
- order 397: `DEVELOPER_EDIT_STALL_THRESHOLD` (constant), lines 932-932, exports `DEVELOPER_EDIT_STALL_THRESHOLD`
- order 398: `ACCEPTANCE_GATE_STALL_THRESHOLD` (constant), lines 933-936, exports `ACCEPTANCE_GATE_STALL_THRESHOLD`
- order 399: `ACCEPTANCE_GATE_HARD_CEILING` (constant), lines 937-940, exports `ACCEPTANCE_GATE_HARD_CEILING`
- order 400: `ACCEPTANCE_GATE_TOTAL_ROUND_CEILING` (constant), lines 941-941, exports `ACCEPTANCE_GATE_TOTAL_ROUND_CEILING`
- order 401: `PLAN_MODE_MANAGER_SYNTHESIS_MAX_TOKENS` (constant), lines 942-942, exports `PLAN_MODE_MANAGER_SYNTHESIS_MAX_TOKENS`
- order 402: `PLAN_MODE_MAX_OPTIONS` (constant), lines 943-943, exports `PLAN_MODE_MAX_OPTIONS`
- order 403: `PLAN_FILE_RELATIVE_PATH` (constant), lines 944-944, exports `PLAN_FILE_RELATIVE_PATH`
- order 404: `PLAN_BUBBLE_MAX_CHARS` (constant), lines 945-945, exports `PLAN_BUBBLE_MAX_CHARS`
- order 405: `PLAN_NOTICE_BODY_MAX_CHARS` (constant), lines 946-946, exports `PLAN_NOTICE_BODY_MAX_CHARS`
- order 406: `PLAN_MESSAGE_EVENT_MAX_CHARS` (constant), lines 947-947, exports `PLAN_MESSAGE_EVENT_MAX_CHARS`
- order 407: `PLAN_STEP_FULL_CONTENT_MAX_CHARS` (constant), lines 948-948, exports `PLAN_STEP_FULL_CONTENT_MAX_CHARS`
- order 408: `PLAN_MODE_RESEARCH_TOOL_ALLOWLIST` (constant), lines 949-956, exports `PLAN_MODE_RESEARCH_TOOL_ALLOWLIST`
- order 409: `FAILURE_LEDGER_MAX_FIXES` (constant), lines 957-957, exports `FAILURE_LEDGER_MAX_FIXES`
- order 410: `FAILURE_LEDGER_MAX_COMPILE_ERRORS` (constant), lines 958-958, exports `FAILURE_LEDGER_MAX_COMPILE_ERRORS`
- order 411: `FAILURE_LEDGER_MAX_DELEGATIONS` (constant), lines 959-959, exports `FAILURE_LEDGER_MAX_DELEGATIONS`
- order 412: `FAILURE_LEDGER_MAX_STALLS` (constant), lines 960-960, exports `FAILURE_LEDGER_MAX_STALLS`
- order 413: `FAILURE_LEDGER_MAX_TOOL_FPS` (constant), lines 961-961, exports `FAILURE_LEDGER_MAX_TOOL_FPS`
- order 414: `FAILURE_LEDGER_MAX_ERRORS` (constant), lines 962-962, exports `FAILURE_LEDGER_MAX_ERRORS`
- order 415: `ERROR_CATEGORY_DEFS` (constant), lines 963-1002, exports `ERROR_CATEGORY_DEFS`
- order 416: `CHECKPOINT_MAX_COUNT` (constant), lines 1003-1003, exports `CHECKPOINT_MAX_COUNT`
- order 417: `CHECKPOINT_INTERVAL_ROUNDS` (constant), lines 1004-1004, exports `CHECKPOINT_INTERVAL_ROUNDS`
- order 418: `PERSISTED_ROUTES_MAX` (constant), lines 1005-1005, exports `PERSISTED_ROUTES_MAX`
- order 419: `HTML_FRONTEND_REQUEST_KEYWORDS` (constant), lines 1006-1045, exports `HTML_FRONTEND_REQUEST_KEYWORDS`
- order 420: `DEEP_RESEARCH_REQUEST_KEYWORDS` (constant), lines 1046-1068, exports `DEEP_RESEARCH_REQUEST_KEYWORDS`
- order 421: `DEEP_RESEARCH_RETRIEVAL_KEYWORDS` (constant), lines 1069-1088, exports `DEEP_RESEARCH_RETRIEVAL_KEYWORDS`
- order 422: `DEEP_RESEARCH_TEXT_ONLY_HINT_KEYWORDS` (constant), lines 1089-1106, exports `DEEP_RESEARCH_TEXT_ONLY_HINT_KEYWORDS`
- order 423: `DANGEROUS_PATTERNS` (constant), lines 1107-1108, exports `DANGEROUS_PATTERNS`
- order 424: `VALID_MSG_TYPES` (constant), lines 1109-1115, exports `VALID_MSG_TYPES`
- order 425: `SUPPORTED_UI_LANGUAGES` (constant), lines 1116-1122, exports `SUPPORTED_UI_LANGUAGES`
- order 426: `UI_LANGUAGE_LABELS` (constant), lines 1123-1123, exports `UI_LANGUAGE_LABELS`
- order 427: `DEFAULT_UI_LANGUAGE` (constant), lines 1124-1124, exports `DEFAULT_UI_LANGUAGE`
- order 428: `UI_STYLE_CHOICES` (constant), lines 1125-1125, exports `UI_STYLE_CHOICES`
- order 429: `UI_STYLE_LABELS` (constant), lines 1126-1126, exports `UI_STYLE_LABELS`
- order 430: `DEFAULT_UI_STYLE` (constant), lines 1127-1127, exports `DEFAULT_UI_STYLE`
- order 431: `DEFAULT_WEB_UI_DIR` (constant), lines 1128-1128, exports `DEFAULT_WEB_UI_DIR`
- order 432: `DEFAULT_WEB_UI_CONFIG` (constant), lines 1129-1129, exports `DEFAULT_WEB_UI_CONFIG`
- order 433: `WEB_UI_REQUIRED_FILES` (constant), lines 1130-1137, exports `WEB_UI_REQUIRED_FILES`
- order 434: `WEB_UI_OPTIONAL_FILES` (constant), lines 1138-1138, exports `WEB_UI_OPTIONAL_FILES`
- order 435: `WEB_UI_APPLICATION_CONTRACT_VERSION` (constant), lines 1139-1139, exports `WEB_UI_APPLICATION_CONTRACT_VERSION`
- order 436: `WEB_UI_APPLICATION_FEATURE_MARKERS` (constant), lines 1140-1159, exports `WEB_UI_APPLICATION_FEATURE_MARKERS`
- order 437: `IMAGE_EXTS` (constant), lines 1160-1174, exports `IMAGE_EXTS`
- order 438: `IMAGE_FORMATS_NEED_CONVERSION` (constant), lines 1175-1175, exports `IMAGE_FORMATS_NEED_CONVERSION`
- order 439: `IMAGE_SAFE_FORMATS` (constant), lines 1176-1176, exports `IMAGE_SAFE_FORMATS`
- order 440: `AUDIO_EXTS` (constant), lines 1177-1187, exports `AUDIO_EXTS`
- order 441: `VIDEO_EXTS` (constant), lines 1188-1198, exports `VIDEO_EXTS`
- order 442: `CODE_PREVIEW_STAGE_MAX_BYTES` (constant), lines 1199-1199, exports `CODE_PREVIEW_STAGE_MAX_BYTES`
- order 443: `CODE_PREVIEW_STAGE_MAX_ROWS` (constant), lines 1200-1200, exports `CODE_PREVIEW_STAGE_MAX_ROWS`
- order 444: `CODE_PREVIEW_STAGE_MAX_PER_FILE` (constant), lines 1201-1201, exports `CODE_PREVIEW_STAGE_MAX_PER_FILE`
- order 445: `CODE_PREVIEW_STAGE_MAX_TOTAL` (constant), lines 1202-1202, exports `CODE_PREVIEW_STAGE_MAX_TOTAL`
- order 446: `CODE_PREVIEW_DIFF_CONTEXT_LINES` (constant), lines 1203-1203, exports `CODE_PREVIEW_DIFF_CONTEXT_LINES`
- order 447: `CODE_PREVIEW_DIFF_MERGE_GAP` (constant), lines 1204-1204, exports `CODE_PREVIEW_DIFF_MERGE_GAP`
- order 448: `PREVIEW_DOWNLOAD_MAX_FILES` (constant), lines 1205-1205, exports `PREVIEW_DOWNLOAD_MAX_FILES`
- order 449: `PREVIEW_DOWNLOAD_MAX_BYTES` (constant), lines 1206-1206, exports `PREVIEW_DOWNLOAD_MAX_BYTES`
- order 450: `FILES_TREE_DEFAULT_MAX_NODES` (constant), lines 1207-1207, exports `FILES_TREE_DEFAULT_MAX_NODES`
- order 451: `FILES_TREE_DEFAULT_MAX_DEPTH` (constant), lines 1208-1208, exports `FILES_TREE_DEFAULT_MAX_DEPTH`
- order 452: `FILES_TREE_SKIP_DIRS` (constant), lines 1209-1217, exports `FILES_TREE_SKIP_DIRS`
- order 453: `FILES_TREE_SKIP_REL_DIRS` (constant), lines 1218-1220, exports `FILES_TREE_SKIP_REL_DIRS`
- order 454: `IDE_FILE_MAX_BYTES` (constant), lines 1221-1221, exports `IDE_FILE_MAX_BYTES`
- order 455: `IDE_UPLOAD_MAX_BYTES` (constant), lines 1222-1222, exports `IDE_UPLOAD_MAX_BYTES`
- order 456: `IDE_UPLOAD_TOTAL_MAX_BYTES` (constant), lines 1223-1223, exports `IDE_UPLOAD_TOTAL_MAX_BYTES`
- order 457: `IDE_UPLOAD_MAX_ITEMS` (constant), lines 1224-1224, exports `IDE_UPLOAD_MAX_ITEMS`
- order 458: `IDE_COMMAND_TIMEOUT_DEFAULT` (constant), lines 1225-1225, exports `IDE_COMMAND_TIMEOUT_DEFAULT`
- order 459: `IDE_TREE_DEFAULT_MAX_NODES` (constant), lines 1226-1226, exports `IDE_TREE_DEFAULT_MAX_NODES`
- order 460: `IDE_TREE_MAX_NODES` (constant), lines 1227-1227, exports `IDE_TREE_MAX_NODES`
- order 461: `IDE_TREE_SKIP_DIRS` (constant), lines 1228-1236, exports `IDE_TREE_SKIP_DIRS`
- order 462: `RENDER_FRAME_MAX_B64_CHARS` (constant), lines 1237-1237, exports `RENDER_FRAME_MAX_B64_CHARS`
- order 463: `RENDER_FRAME_MAX_POINTS` (constant), lines 1238-1238, exports `RENDER_FRAME_MAX_POINTS`
- order 464: `RENDER_FRAME_MAX_LINES` (constant), lines 1239-1239, exports `RENDER_FRAME_MAX_LINES`
- order 465: `RENDER_FRAME_MAX_LINE_POINTS` (constant), lines 1240-1240, exports `RENDER_FRAME_MAX_LINE_POINTS`
- order 466: `RENDER_FRAME_ACTIVITY_INTERVAL_SECONDS` (constant), lines 1241-1241, exports `RENDER_FRAME_ACTIVITY_INTERVAL_SECONDS`
- order 467: `RAW_TOOLCALL_TEXT_FILTER_THRESHOLD` (constant), lines 1242-1242, exports `RAW_TOOLCALL_TEXT_FILTER_THRESHOLD`
- order 468: `ASSISTANT_TEXT_PERSIST_MAX_CHARS` (constant), lines 1243-1243, exports `ASSISTANT_TEXT_PERSIST_MAX_CHARS`
- order 469: `ASSISTANT_MESSAGE_EVENT_MAX_CHARS` (constant), lines 1244-1244, exports `ASSISTANT_MESSAGE_EVENT_MAX_CHARS`
- order 470: `CODE_PREVIEW_EXTS` (constant), lines 1245-1370, exports `CODE_PREVIEW_EXTS`
- order 471: `CODE_PREVIEW_FILENAMES` (constant), lines 1371-1422, exports `CODE_PREVIEW_FILENAMES`
- order 472: `MEDIA_CAPABILITY_KEYS` (constant), lines 1423-1430, exports `MEDIA_CAPABILITY_KEYS`
- order 473: `SAMPLE_IMAGE_PNG_B64` (constant), lines 1431-1434, exports `SAMPLE_IMAGE_PNG_B64`
- order 474: `SAMPLE_AUDIO_WAV_B64` (constant), lines 1435-1437, exports `SAMPLE_AUDIO_WAV_B64`
- order 475: `SAMPLE_VIDEO_MP4_B64` (constant), lines 1438-1440, exports `SAMPLE_VIDEO_MP4_B64`
- order 476: `OFFLINE_JS_LIB_CATALOG` (constant), lines 1441-1700, exports `OFFLINE_JS_LIB_CATALOG`
- order 477: `OFFLINE_JS_LIB_INDEX_FILE` (constant), lines 1701-1701, exports `OFFLINE_JS_LIB_INDEX_FILE`
- order 478: `OFFLINE_JS_LIB_README_FILE` (constant), lines 1702-1702, exports `OFFLINE_JS_LIB_README_FILE`
- order 487: `BACKEND_I18N` (constant), lines 1886-1957, exports `BACKEND_I18N`
- order 488: `_call_backend_i18n_en_update_1959` (expression), lines 1958-2059, exports —
- order 489: `_call_backend_i18n_zh_cn_update_2060` (expression), lines 2060-2160, exports —
- order 490: `_call_backend_i18n_zh_tw_update_2161` (expression), lines 2161-2261, exports —
- order 491: `_call_backend_i18n_ja_update_2262` (expression), lines 2262-2362, exports —
- order 703: `TABULAR_PREVIEW_EXTS` (constant), lines 9101-9103, exports `TABULAR_PREVIEW_EXTS`
- order 704: `EXCEL_PREVIEW_EXTS` (constant), lines 9104-9104, exports `EXCEL_PREVIEW_EXTS`
- order 705: `PRESENTATION_PREVIEW_EXTS` (constant), lines 9105-9105, exports `PRESENTATION_PREVIEW_EXTS`
- order 706: `DOCUMENT_PREVIEW_EXTS` (constant), lines 9106-9106, exports `DOCUMENT_PREVIEW_EXTS`

### `config/paths.py`

- order 58: `SCRIPT_DIR` (constant), lines 66-66, exports `SCRIPT_DIR`
- order 74: `_resolve_default_agent_workdir` (function), lines 114-119, exports `_resolve_default_agent_workdir`
- order 75: `_migrate_legacy_runtime_roots` (function), lines 120-149, exports `_migrate_legacy_runtime_roots`
- order 76: `WORKDIR` (constant), lines 150-151, exports `WORKDIR`
- order 77: `CODES_ROOT` (constant), lines 152-152, exports `CODES_ROOT`
- order 78: `LLM_CONFIG_PATH` (constant), lines 153-153, exports `LLM_CONFIG_PATH`
- order 559: `detect_repo_root` (function), lines 3628-3643, exports `detect_repo_root`
- order 560: `REPO_ROOT` (constant), lines 3644-3645, exports `REPO_ROOT`

### `config/settings.py`

- order 482: `normalize_ui_language` (function), lines 1784-1808, exports `normalize_ui_language`
- order 483: `normalize_ui_style` (function), lines 1809-1828, exports `normalize_ui_style`
- order 484: `supported_ui_languages_payload` (function), lines 1829-1832, exports `supported_ui_languages_payload`
- order 485: `normalize_execution_mode` (function), lines 1833-1854, exports `normalize_execution_mode`
- order 486: `model_language_instruction` (function), lines 1855-1885, exports `model_language_instruction`
- order 492: `backend_i18n_text` (function), lines 2363-2375, exports `backend_i18n_text`
- order 493: `backend_role_label` (function), lines 2376-2382, exports `backend_role_label`
- order 494: `_detect_os_shell_instruction` (function), lines 2383-2424, exports `_detect_os_shell_instruction`
- order 495: `resolve_web_ui_dir_path` (function), lines 2425-2433, exports `resolve_web_ui_dir_path`
- order 496: `resolve_optional_file_path` (function), lines 2434-2443, exports `resolve_optional_file_path`
- order 497: `resolve_skills_root_path` (function), lines 2444-2453, exports `resolve_skills_root_path`
- order 498: `_count_skill_markdown_files` (function), lines 2454-2467, exports `_count_skill_markdown_files`
- order 499: `select_preferred_skills_root` (function), lines 2468-2504, exports `select_preferred_skills_root`
- order 500: `load_web_ui_config_file` (function), lines 2505-2521, exports `load_web_ui_config_file`
- order 501: `extract_show_upload_list_setting` (function), lines 2522-2538, exports `extract_show_upload_list_setting`
- order 502: `extract_ui_style_setting` (function), lines 2539-2555, exports `extract_ui_style_setting`
- order 503: `extract_js_lib_download_setting` (function), lines 2556-2577, exports `extract_js_lib_download_setting`
- order 504: `extract_daily_session_limit_setting` (function), lines 2578-2623, exports `extract_daily_session_limit_setting`
- order 505: `extract_shell_command_timeout_setting` (function), lines 2624-2672, exports `extract_shell_command_timeout_setting`
- order 506: `extract_context_token_limit_setting` (function), lines 2673-2707, exports `extract_context_token_limit_setting`
- order 507: `normalize_auto_task_level_ceiling` (function), lines 2708-2729, exports `normalize_auto_task_level_ceiling`
- order 508: `normalize_l2_todo_policy` (function), lines 2730-2765, exports `normalize_l2_todo_policy`
- order 509: `extract_l2_todo_policy_setting` (function), lines 2766-2808, exports `extract_l2_todo_policy_setting`
- order 510: `extract_auto_task_level_ceiling_setting` (function), lines 2809-2838, exports `extract_auto_task_level_ceiling_setting`
- order 511: `normalize_read_context_policy` (function), lines 2839-2859, exports `normalize_read_context_policy`
- order 512: `normalize_tool_memory_policy` (function), lines 2860-2863, exports `normalize_tool_memory_policy`
- order 513: `extract_read_context_policy_setting` (function), lines 2864-2887, exports `extract_read_context_policy_setting`
- order 514: `extract_tool_memory_policy_setting` (function), lines 2888-2911, exports `extract_tool_memory_policy_setting`
- order 516: `default_multimodal_capabilities` (function), lines 2918-2928, exports `default_multimodal_capabilities`
- order 517: `_to_bool_like` (function), lines 2929-2941, exports `_to_bool_like`
- order 518: `extract_web_search_enabled_setting` (function), lines 2942-2954, exports `extract_web_search_enabled_setting`
- order 519: `_single_no_plan_todo_setting_sections` (function), lines 2955-2981, exports `_single_no_plan_todo_setting_sections`
- order 520: `_single_no_plan_todo_setting_present` (function), lines 2982-3007, exports `_single_no_plan_todo_setting_present`
- order 521: `extract_single_no_plan_todo_settings` (function), lines 3008-3054, exports `extract_single_no_plan_todo_settings`
- order 522: `normalize_user_memory_mode` (function), lines 3055-3085, exports `normalize_user_memory_mode`
- order 523: `user_memory_enabled_from_mode` (function), lines 3086-3089, exports `user_memory_enabled_from_mode`
- order 524: `extract_user_memory_mode_setting` (function), lines 3090-3129, exports `extract_user_memory_mode_setting`
- order 525: `set_web_search_enabled_on_runtime` (function), lines 3130-3145, exports `set_web_search_enabled_on_runtime`
- order 526: `infer_model_multimodal_capabilities` (function), lines 3146-3192, exports `infer_model_multimodal_capabilities`
- order 527: `parse_capability_overrides` (function), lines 3193-3232, exports `parse_capability_overrides`
- order 528: `merge_multimodal_capabilities` (function), lines 3233-3242, exports `merge_multimodal_capabilities`
- order 529: `parse_media_endpoints` (function), lines 3243-3259, exports `parse_media_endpoints`
- order 545: `extract_runtime_region_hint_setting` (function), lines 3437-3462, exports `extract_runtime_region_hint_setting`
- order 546: `extract_runtime_timezone_hint_setting` (function), lines 3463-3480, exports `extract_runtime_timezone_hint_setting`
- order 547: `runtime_environment_context_snapshot` (function), lines 3481-3530, exports `runtime_environment_context_snapshot`
- order 548: `runtime_environment_context_block` (function), lines 3531-3560, exports `runtime_environment_context_block`
- order 576: `load_offline_js_lib_index` (function), lines 3882-3892, exports `load_offline_js_lib_index`
- order 626: `resolve_ollama_model` (function), lines 6303-6314, exports `resolve_ollama_model`
- order 627: `infer_thinking_model` (function), lines 6315-6318, exports `infer_thinking_model`
- order 638: `extract_base_url` (function), lines 6529-6538, exports `extract_base_url`
- order 640: `infer_user_complexity_value` (function), lines 6550-6567, exports `infer_user_complexity_value`
- order 641: `normalize_task_complexity` (function), lines 6568-6597, exports `normalize_task_complexity`
- order 642: `task_complexity_rank` (function), lines 6598-6600, exports `task_complexity_rank`
- order 643: `task_complexity_at_least` (function), lines 6601-6603, exports `task_complexity_at_least`
- order 644: `max_task_complexity` (function), lines 6604-6614, exports `max_task_complexity`
- order 645: `normalize_openai_compat_provider_name` (function), lines 6615-6631, exports `normalize_openai_compat_provider_name`
- order 665: `resolve_reasoning_payload` (function), lines 6758-6808, exports `resolve_reasoning_payload`
- order 668: `extract_openai_compat_model_ids` (function), lines 6856-6890, exports `extract_openai_compat_model_ids`
- order 671: `load_llm_config_from_source` (function), lines 6923-6958, exports `load_llm_config_from_source`
- order 672: `parse_llm_config_profiles` (function), lines 6959-7589, exports `parse_llm_config_profiles`
- order 673: `looks_like_llm_config` (function), lines 7590-7667, exports `looks_like_llm_config`
- order 677: `parse_front_matter` (function), lines 7828-8016, exports `parse_front_matter`

### `ide/assets.py`

- order 859: `IDE_INDEX_HTML` (constant), lines 92693-92773, exports `IDE_INDEX_HTML`
- order 860: `IDE_CSS` (constant), lines 92774-92841, exports `IDE_CSS`
- order 861: `IDE_JS` (constant), lines 92842-93036, exports `IDE_JS`

### `ide/handler.py`

- order 870: `IdeHandler` (class), lines 101021-101304, exports `IdeHandler`

### `llm/client.py`

- order 765: `OllamaError` (class), lines 16206-16228, exports `OllamaError`
- order 766: `OllamaClient` (class), lines 16229-18523, exports `OllamaClient`

### `llm/constants.py`

- order 56: `DEFAULT_OLLAMA_BASE_URL` (constant), lines 64-64, exports `DEFAULT_OLLAMA_BASE_URL`
- order 57: `DEFAULT_OLLAMA_MODEL` (constant), lines 65-65, exports `DEFAULT_OLLAMA_MODEL`
- order 646: `OPENAI_COMPAT_PROVIDER_NAMES` (constant), lines 6632-6641, exports `OPENAI_COMPAT_PROVIDER_NAMES`
- order 647: `OPENAI_LIKE_PROVIDER_NAMES` (constant), lines 6642-6643, exports `OPENAI_LIKE_PROVIDER_NAMES`
- order 650: `EFFORT_OFF` (constant), lines 6650-6661, exports `EFFORT_OFF`
- order 651: `EFFORT_LOW` (constant), lines 6662-6662, exports `EFFORT_LOW`
- order 652: `EFFORT_MEDIUM` (constant), lines 6663-6663, exports `EFFORT_MEDIUM`
- order 653: `EFFORT_HIGH` (constant), lines 6664-6664, exports `EFFORT_HIGH`
- order 654: `EFFORT_MAX` (constant), lines 6665-6665, exports `EFFORT_MAX`
- order 655: `EFFORT_LEVELS` (constant), lines 6666-6666, exports `EFFORT_LEVELS`
- order 656: `EFFORT_ORDER` (constant), lines 6667-6667, exports `EFFORT_ORDER`
- order 657: `EFFORT_DEFAULT` (constant), lines 6668-6668, exports `EFFORT_DEFAULT`
- order 658: `EFFORT_ANTHROPIC_BUDGET` (constant), lines 6669-6676, exports `EFFORT_ANTHROPIC_BUDGET`
- order 659: `EFFORT_OPENAI_REASONING` (constant), lines 6677-6683, exports `EFFORT_OPENAI_REASONING`
- order 660: `TASK_LEVEL_EFFORT` (constant), lines 6684-6693, exports `TASK_LEVEL_EFFORT`
- order 661: `ROLE_EFFORT_FLOOR` (constant), lines 6694-6699, exports `ROLE_EFFORT_FLOOR`
- order 662: `COORDINATION_EFFORT` (constant), lines 6700-6708, exports `COORDINATION_EFFORT`

### `llm/utils.py`

- order 619: `probe_ollama_environment` (function), lines 6234-6248, exports `probe_ollama_environment`
- order 620: `list_ollama_models` (function), lines 6249-6252, exports `list_ollama_models`
- order 621: `_OLLAMA_TAG_CACHE_LOCK` (assignment), lines 6253-6254, exports `_OLLAMA_TAG_CACHE_LOCK`
- order 622: `_OLLAMA_TAG_CACHE` (assignment), lines 6255-6255, exports `_OLLAMA_TAG_CACHE`
- order 625: `list_ollama_models_cached` (function), lines 6264-6302, exports `list_ollama_models_cached`
- order 628: `split_thinking_content` (function), lines 6319-6363, exports `split_thinking_content`
- order 629: `strip_thinking_content` (function), lines 6364-6366, exports `strip_thinking_content`
- order 630: `check_ollama_model_ready` (function), lines 6367-6392, exports `check_ollama_model_ready`
- order 631: `list_loaded_ollama_models` (function), lines 6393-6407, exports `list_loaded_ollama_models`
- order 632: `wake_ollama_model` (function), lines 6408-6439, exports `wake_ollama_model`
- order 633: `try_pull_ollama_model` (function), lines 6440-6459, exports `try_pull_ollama_model`
- order 634: `ordered_model_candidates` (function), lines 6460-6479, exports `ordered_model_candidates`
- order 635: `pick_working_ollama_model` (function), lines 6480-6497, exports `pick_working_ollama_model`
- order 639: `complete_chat_endpoint` (function), lines 6539-6549, exports `complete_chat_endpoint`
- order 648: `is_openai_compat_provider` (function), lines 6644-6646, exports `is_openai_compat_provider`
- order 649: `is_openai_like_provider` (function), lines 6647-6649, exports `is_openai_like_provider`
- order 663: `clamp_effort` (function), lines 6709-6720, exports `clamp_effort`
- order 664: `model_reasoning_style` (function), lines 6721-6757, exports `model_reasoning_style`
- order 666: `openai_compat_probe_headers` (function), lines 6809-6821, exports `openai_compat_probe_headers`
- order 667: `openai_compat_model_list_urls` (function), lines 6822-6855, exports `openai_compat_model_list_urls`
- order 669: `_is_http_url` (function), lines 6891-6904, exports `_is_http_url`
- order 670: `_resolve_local_path` (function), lines 6905-6922, exports `_resolve_local_path`

### `mcp/constants.py`

- order 96: `MCP_SERVICE_PORT_OFFSET` (constant), lines 171-171, exports `MCP_SERVICE_PORT_OFFSET`
- order 754: `MCP_PROTOCOL_VERSION` (constant), lines 15328-15357, exports `MCP_PROTOCOL_VERSION`
- order 755: `MCP_NAME_RE` (constant), lines 15358-15358, exports `MCP_NAME_RE`
- order 756: `MCP_TOOL_PREFIX` (constant), lines 15359-15359, exports `MCP_TOOL_PREFIX`
- order 757: `_MCP_DEFAULT_HANDSHAKE_TIMEOUT` (assignment), lines 15360-15360, exports `_MCP_DEFAULT_HANDSHAKE_TIMEOUT`
- order 758: `_MCP_DEFAULT_CALL_TIMEOUT` (assignment), lines 15361-15361, exports `_MCP_DEFAULT_CALL_TIMEOUT`
- order 759: `_MCP_MAX_RESULT_CHARS` (assignment), lines 15362-15362, exports `_MCP_MAX_RESULT_CHARS`

### `mcp/driver.py`

- order 760: `mcp_normalize_name` (function), lines 15363-15372, exports `mcp_normalize_name`
- order 761: `mcp_normalize_server_configs` (function), lines 15373-15457, exports `mcp_normalize_server_configs`
- order 762: `mcp_extract_server_configs` (function), lines 15458-15477, exports `mcp_extract_server_configs`
- order 763: `MCPServerProcess` (class), lines 15478-15813, exports `MCPServerProcess`
- order 764: `MCPManager` (class), lines 15814-16205, exports `MCPManager`

### `mcp/service.py`

- order 871: `McpServiceHandler` (class), lines 101305-101468, exports `McpServiceHandler`

### `rag/assets.py`

- order 853: `RAG_ADMIN_INDEX_HTML` (constant), lines 90285-90459, exports `RAG_ADMIN_INDEX_HTML`
- order 854: `RAG_ADMIN_CSS` (constant), lines 90460-90551, exports `RAG_ADMIN_CSS`
- order 855: `RAG_ADMIN_JS` (constant), lines 90552-92643, exports `RAG_ADMIN_JS`
- order 856: `CODE_ADMIN_INDEX_HTML` (constant), lines 92644-92656, exports `CODE_ADMIN_INDEX_HTML`
- order 857: `CODE_ADMIN_CSS` (constant), lines 92657-92687, exports `CODE_ADMIN_CSS`
- order 858: `CODE_ADMIN_JS` (constant), lines 92688-92692, exports `CODE_ADMIN_JS`

### `rag/constants.py`

- order 92: `RAG_LIBRARY_DIRNAME` (constant), lines 167-167, exports `RAG_LIBRARY_DIRNAME`
- order 93: `RAG_ADMIN_PORT_OFFSET` (constant), lines 168-168, exports `RAG_ADMIN_PORT_OFFSET`
- order 94: `CODE_LIBRARY_DIRNAME` (constant), lines 169-169, exports `CODE_LIBRARY_DIRNAME`
- order 99: `WEB_SEARCH_INDEX_DIRNAME` (constant), lines 177-177, exports `WEB_SEARCH_INDEX_DIRNAME`
- order 101: `USER_MEMORY_DIRNAME` (constant), lines 179-179, exports `USER_MEMORY_DIRNAME`
- order 102: `USER_MEMORY_DB_FILENAME` (constant), lines 180-180, exports `USER_MEMORY_DB_FILENAME`
- order 103: `USER_MEMORY_PROFILE_FILENAME` (constant), lines 181-181, exports `USER_MEMORY_PROFILE_FILENAME`
- order 104: `USER_MEMORY_MODE_CHOICES` (constant), lines 182-182, exports `USER_MEMORY_MODE_CHOICES`
- order 106: `USER_MEMORY_WEAK_CAPSULE_CHARS` (constant), lines 184-184, exports `USER_MEMORY_WEAK_CAPSULE_CHARS`
- order 107: `USER_MEMORY_ON_CAPSULE_CHARS` (constant), lines 185-185, exports `USER_MEMORY_ON_CAPSULE_CHARS`
- order 108: `USER_MEMORY_CAPSULE_INJECT_CHARS` (constant), lines 186-189, exports `USER_MEMORY_CAPSULE_INJECT_CHARS`
- order 109: `USER_MEMORY_MAX_SUMMARY_CHARS` (constant), lines 190-190, exports `USER_MEMORY_MAX_SUMMARY_CHARS`
- order 110: `USER_MEMORY_QUERY_LIMIT` (constant), lines 191-191, exports `USER_MEMORY_QUERY_LIMIT`
- order 111: `USER_MEMORY_DECAY_HALFLIFE_DAYS` (constant), lines 192-192, exports `USER_MEMORY_DECAY_HALFLIFE_DAYS`
- order 112: `USER_MEMORY_PROFILE_SCHEMA_VERSION` (constant), lines 193-193, exports `USER_MEMORY_PROFILE_SCHEMA_VERSION`
- order 123: `WEB_SEARCH_CONTEXT_REGISTRY_MAX` (constant), lines 204-204, exports `WEB_SEARCH_CONTEXT_REGISTRY_MAX`
- order 124: `WEB_SEARCH_CONTEXT_PROMPT_MAX_ITEMS` (constant), lines 205-205, exports `WEB_SEARCH_CONTEXT_PROMPT_MAX_ITEMS`
- order 125: `WEB_SEARCH_CONTEXT_PROMPT_MAX_CHARS` (constant), lines 206-206, exports `WEB_SEARCH_CONTEXT_PROMPT_MAX_CHARS`
- order 126: `WEB_SEARCH_CONTEXT_NODE_MAX` (constant), lines 207-207, exports `WEB_SEARCH_CONTEXT_NODE_MAX`
- order 127: `WEB_SEARCH_CONTEXT_URL_MAX` (constant), lines 208-208, exports `WEB_SEARCH_CONTEXT_URL_MAX`
- order 128: `RAG_CHUNK_CHARS` (constant), lines 209-209, exports `RAG_CHUNK_CHARS`
- order 129: `RAG_CHUNK_OVERLAP` (constant), lines 210-210, exports `RAG_CHUNK_OVERLAP`
- order 130: `RAG_MAX_CHUNKS_PER_DOC` (constant), lines 211-213, exports `RAG_MAX_CHUNKS_PER_DOC`
- order 131: `RAG_MAX_DOCUMENT_CHARS` (constant), lines 214-224, exports `RAG_MAX_DOCUMENT_CHARS`
- order 135: `RAG_MAX_QUERY_RESULTS` (constant), lines 228-228, exports `RAG_MAX_QUERY_RESULTS`
- order 136: `RAG_HIGH_RECALL_POOL_MULTIPLIER` (constant), lines 229-229, exports `RAG_HIGH_RECALL_POOL_MULTIPLIER`
- order 137: `RAG_HIGH_RECALL_MIN_POOL` (constant), lines 230-230, exports `RAG_HIGH_RECALL_MIN_POOL`
- order 138: `RAG_RETRIEVAL_MAX_PER_DOC` (constant), lines 231-231, exports `RAG_RETRIEVAL_MAX_PER_DOC`
- order 139: `RAG_BM25_K1` (constant), lines 232-235, exports `RAG_BM25_K1`
- order 140: `RAG_BM25_B` (constant), lines 236-236, exports `RAG_BM25_B`
- order 141: `RAG_BM25_SATURATION` (constant), lines 237-243, exports `RAG_BM25_SATURATION`
- order 142: `RAG_SYMBOL_EXACT_BOOST` (constant), lines 244-247, exports `RAG_SYMBOL_EXACT_BOOST`
- order 143: `RAG_INDEX_SNAPSHOT_FORMAT` (constant), lines 248-251, exports `RAG_INDEX_SNAPSHOT_FORMAT`
- order 144: `RAG_GRAPH_MAX_NODES` (constant), lines 252-252, exports `RAG_GRAPH_MAX_NODES`
- order 145: `RAG_TASK_HISTORY_LIMIT` (constant), lines 253-253, exports `RAG_TASK_HISTORY_LIMIT`
- order 146: `RAG_MODEL_MEDIA_MAX_BYTES` (constant), lines 254-254, exports `RAG_MODEL_MEDIA_MAX_BYTES`
- order 147: `RAG_MAX_IMPORT_FILES` (constant), lines 255-255, exports `RAG_MAX_IMPORT_FILES`
- order 148: `RAG_MAX_IMPORT_BATCH_ITEMS` (constant), lines 256-256, exports `RAG_MAX_IMPORT_BATCH_ITEMS`
- order 149: `RAG_MAX_IMPORT_BATCH_BYTES` (constant), lines 257-257, exports `RAG_MAX_IMPORT_BATCH_BYTES`
- order 150: `RAG_PDF_IMAGE_LIMIT` (constant), lines 258-258, exports `RAG_PDF_IMAGE_LIMIT`
- order 151: `RAG_QUERY_CONTEXT_CHARS` (constant), lines 259-259, exports `RAG_QUERY_CONTEXT_CHARS`
- order 152: `RAG_MAX_GLOBAL_COMMUNITIES` (constant), lines 260-260, exports `RAG_MAX_GLOBAL_COMMUNITIES`
- order 153: `RAG_MAX_COMMUNITY_MAP_SUPPORT` (constant), lines 261-261, exports `RAG_MAX_COMMUNITY_MAP_SUPPORT`
- order 154: `RAG_INCLUDE_FILENAME_ENTITIES_DEFAULT` (constant), lines 262-262, exports `RAG_INCLUDE_FILENAME_ENTITIES_DEFAULT`
- order 155: `RAG_DYNAMIC_NOISE_MIN_DOC_FREQ` (constant), lines 263-263, exports `RAG_DYNAMIC_NOISE_MIN_DOC_FREQ`
- order 156: `RAG_DYNAMIC_NOISE_MIN_COMMUNITY_FREQ` (constant), lines 264-264, exports `RAG_DYNAMIC_NOISE_MIN_COMMUNITY_FREQ`
- order 157: `RAG_DYNAMIC_NOISE_SOFT_DOC_RATIO` (constant), lines 265-265, exports `RAG_DYNAMIC_NOISE_SOFT_DOC_RATIO`
- order 158: `RAG_DYNAMIC_NOISE_HARD_DOC_RATIO` (constant), lines 266-266, exports `RAG_DYNAMIC_NOISE_HARD_DOC_RATIO`
- order 159: `RAG_DYNAMIC_NOISE_SOFT_COMMUNITY_RATIO` (constant), lines 267-267, exports `RAG_DYNAMIC_NOISE_SOFT_COMMUNITY_RATIO`
- order 160: `RAG_DYNAMIC_NOISE_HARD_COMMUNITY_RATIO` (constant), lines 268-268, exports `RAG_DYNAMIC_NOISE_HARD_COMMUNITY_RATIO`
- order 161: `RAG_MIN_SYNTHESIS_SCORE` (constant), lines 269-269, exports `RAG_MIN_SYNTHESIS_SCORE`
- order 162: `RAG_NO_EVIDENCE_THRESHOLD` (constant), lines 270-270, exports `RAG_NO_EVIDENCE_THRESHOLD`
- order 163: `RAG_WEAK_MATCH_SCORE_CAP` (constant), lines 271-271, exports `RAG_WEAK_MATCH_SCORE_CAP`
- order 164: `RAG_SYNTHESIS_MAX_PER_DOC` (constant), lines 272-272, exports `RAG_SYNTHESIS_MAX_PER_DOC`
- order 165: `RAG_WORKFLOW_ACCEPT_SCORE` (constant), lines 273-273, exports `RAG_WORKFLOW_ACCEPT_SCORE`
- order 166: `RAG_NO_EVIDENCE_MESSAGE` (constant), lines 274-274, exports `RAG_NO_EVIDENCE_MESSAGE`
- order 167: `RAG_CONTEXT_BUDGETS` (constant), lines 275-279, exports `RAG_CONTEXT_BUDGETS`
- order 168: `RAG_WEAK_EVIDENCE_MESSAGE` (constant), lines 280-280, exports `RAG_WEAK_EVIDENCE_MESSAGE`
- order 169: `RAG_DENSE_DEFAULT_ENABLED` (constant), lines 281-281, exports `RAG_DENSE_DEFAULT_ENABLED`
- order 170: `RAG_EMBEDDING_MODE_VALUES` (constant), lines 282-282, exports `RAG_EMBEDDING_MODE_VALUES`
- order 171: `RAG_IMPORT_WORKER_COUNT` (constant), lines 283-286, exports `RAG_IMPORT_WORKER_COUNT`
- order 173: `RAG_PARSE_TIMEOUT_SECONDS` (constant), lines 291-294, exports `RAG_PARSE_TIMEOUT_SECONDS`
- order 792: `RAG_TERM_GROUPS` (constant), lines 77676-82309, exports `RAG_TERM_GROUPS`
- order 793: `RAG_RESEARCH_HINTS` (constant), lines 82310-82331, exports `RAG_RESEARCH_HINTS`
- order 794: `RAG_CODE_HINTS` (constant), lines 82332-82342, exports `RAG_CODE_HINTS`
- order 795: `RAG_SHORT_TOKEN_ALLOWLIST` (constant), lines 82343-82358, exports `RAG_SHORT_TOKEN_ALLOWLIST`
- order 796: `RAG_EN_STOPWORDS` (constant), lines 82359-82431, exports `RAG_EN_STOPWORDS`
- order 797: `RAG_ZH_STOPWORDS` (constant), lines 82432-82468, exports `RAG_ZH_STOPWORDS`
- order 798: `RAG_GENERIC_ENTITY_TERMS_EN` (constant), lines 82469-82547, exports `RAG_GENERIC_ENTITY_TERMS_EN`
- order 799: `RAG_GENERIC_ENTITY_TERMS_ZH` (constant), lines 82548-82590, exports `RAG_GENERIC_ENTITY_TERMS_ZH`
- order 800: `RAG_STRUCTURAL_ENTITY_PATTERNS` (constant), lines 82591-82609, exports `RAG_STRUCTURAL_ENTITY_PATTERNS`
- order 825: `CODE_LIBRARY_IGNORED_DIRS` (constant), lines 83354-83363, exports `CODE_LIBRARY_IGNORED_DIRS`
- order 826: `CODE_LIBRARY_LANGUAGE_BY_EXT` (constant), lines 83364-83420, exports `CODE_LIBRARY_LANGUAGE_BY_EXT`
- order 827: `CODE_LIBRARY_SPECIAL_FILENAMES` (constant), lines 83421-83427, exports `CODE_LIBRARY_SPECIAL_FILENAMES`

### `rag/index.py`

- order 830: `_code_module_name` (function), lines 83452-83468, exports `_code_module_name`
- order 831: `_code_choose_community` (function), lines 83469-83478, exports `_code_choose_community`
- order 832: `_code_query_terms` (function), lines 83479-83493, exports `_code_query_terms`
- order 841: `TFGraphIDFIndex` (class), lines 84561-86237, exports `TFGraphIDFIndex`
- order 850: `CodeGraphIndex` (class), lines 89445-89930, exports `CodeGraphIndex`

### `rag/ingestion.py`

- order 810: `_rag_trigram_set` (function), lines 82820-82827, exports `_rag_trigram_set`
- order 811: `_rag_jaccard_sim` (function), lines 82828-82837, exports `_rag_jaccard_sim`
- order 812: `_rag_mmr_select` (function), lines 82838-82887, exports `_rag_mmr_select`
- order 817: `_rag_embed_text` (function), lines 83022-83045, exports `_rag_embed_text`
- order 818: `_rag_embed_batch` (function), lines 83046-83054, exports `_rag_embed_batch`
- order 819: `_rag_window_for_query` (function), lines 83055-83069, exports `_rag_window_for_query`
- order 820: `_rag_focused_excerpt` (function), lines 83070-83112, exports `_rag_focused_excerpt`
- order 821: `_rag_query_variants` (function), lines 83113-83152, exports `_rag_query_variants`
- order 822: `_rag_parse_segments` (function), lines 83153-83215, exports `_rag_parse_segments`
- order 823: `_rag_boundary_split` (function), lines 83216-83273, exports `_rag_boundary_split`
- order 848: `_rag_parse_file_worker` (function), lines 88546-88562, exports `_rag_parse_file_worker`
- order 849: `RAGIngestionService` (class), lines 88563-89444, exports `RAGIngestionService`
- order 852: `CodeIngestionService` (class), lines 90197-90284, exports `CodeIngestionService`

### `rag/parsers.py`

- order 701: `normalize_rel_preview_path` (function), lines 9076-9089, exports `normalize_rel_preview_path`
- order 702: `is_code_preview_candidate` (function), lines 9090-9100, exports `is_code_preview_candidate`
- order 707: `preview_kind_for_path` (function), lines 9107-9138, exports `preview_kind_for_path`
- order 708: `build_code_preview_rows` (function), lines 9139-9187, exports `build_code_preview_rows`
- order 801: `_rag_safe_name` (function), lines 82610-82624, exports `_rag_safe_name`
- order 802: `_rag_detect_language` (function), lines 82625-82641, exports `_rag_detect_language`
- order 803: `_rag_cjk_ngrams` (function), lines 82642-82656, exports `_rag_cjk_ngrams`
- order 804: `_rag_is_noise_token` (function), lines 82657-82678, exports `_rag_is_noise_token`
- order 805: `_rag_entity_allowed` (function), lines 82679-82693, exports `_rag_entity_allowed`
- order 806: `_rag_filter_entities` (function), lines 82694-82710, exports `_rag_filter_entities`
- order 807: `_rag_filename_entity_aliases` (function), lines 82711-82746, exports `_rag_filename_entity_aliases`
- order 808: `_rag_apply_filename_entity_policy` (function), lines 82747-82779, exports `_rag_apply_filename_entity_policy`
- order 809: `_rag_choose_community` (function), lines 82780-82819, exports `_rag_choose_community`
- order 813: `_rag_tokenize` (function), lines 82888-82941, exports `_rag_tokenize`
- order 814: `_rag_expand_tokens` (function), lines 82942-82965, exports `_rag_expand_tokens`
- order 815: `_rag_extract_entities` (function), lines 82966-82984, exports `_rag_extract_entities`
- order 816: `_rag_classify_document` (function), lines 82985-83021, exports `_rag_classify_document`
- order 824: `_rag_chunk_text` (function), lines 83274-83353, exports `_rag_chunk_text`
- order 828: `_code_language_from_name` (function), lines 83428-83446, exports `_code_language_from_name`
- order 829: `_code_is_test_path` (function), lines 83447-83451, exports `_code_is_test_path`
- order 833: `_CallCollector` (class), lines 83494-83508, exports `_CallCollector`
- order 834: `_ALGO_COMPLEXITY_RE` (assignment), lines 83509-83511, exports `_ALGO_COMPLEXITY_RE`
- order 835: `_ALGO_STEP_RE` (assignment), lines 83512-83512, exports `_ALGO_STEP_RE`
- order 836: `_ALGO_MATH_VARS` (assignment), lines 83513-83513, exports `_ALGO_MATH_VARS`
- order 837: `_ALGO_DOC_KEYWORDS` (assignment), lines 83514-83514, exports `_ALGO_DOC_KEYWORDS`
- order 838: `_detect_algo_chunk` (function), lines 83515-83540, exports `_detect_algo_chunk`
- order 839: `CodeContentParser` (class), lines 83541-84050, exports `CodeContentParser`
- order 840: `RAGContentParser` (class), lines 84051-84560, exports `RAGContentParser`

### `rag/store.py`

- order 842: `RAGLibraryStore` (class), lines 86238-86823, exports `RAGLibraryStore`
- order 843: `WikiStore` (class), lines 86824-87355, exports `WikiStore`
- order 844: `UserMemoryStore` (class), lines 87356-88033, exports `UserMemoryStore`
- order 845: `UserInteractionOptimizer` (class), lines 88034-88102, exports `UserInteractionOptimizer`
- order 846: `UserIntentProfiler` (class), lines 88103-88144, exports `UserIntentProfiler`
- order 847: `WorkflowMemoryStore` (class), lines 88145-88545, exports `WorkflowMemoryStore`
- order 851: `CodeLibraryStore` (class), lines 89931-90196, exports `CodeLibraryStore`

### `rag/web_search.py`

- order 585: `_agent_web_bool` (function), lines 4139-4146, exports `_agent_web_bool`
- order 586: `_agent_web_int` (function), lines 4147-4154, exports `_agent_web_int`
- order 587: `_agent_web_host_is_local_name` (function), lines 4155-4161, exports `_agent_web_host_is_local_name`
- order 588: `_agent_web_ip_is_blocked` (function), lines 4162-4176, exports `_agent_web_ip_is_blocked`
- order 589: `_agent_web_canonical_url` (function), lines 4177-4206, exports `_agent_web_canonical_url`
- order 590: `_agent_web_domain_to_seed` (function), lines 4207-4218, exports `_agent_web_domain_to_seed`
- order 591: `_agent_web_query_terms` (function), lines 4219-4236, exports `_agent_web_query_terms`
- order 592: `_agent_web_query_domain_hints` (function), lines 4237-4277, exports `_agent_web_query_domain_hints`
- order 593: `_agent_web_query_needs_fresh_network` (function), lines 4278-4300, exports `_agent_web_query_needs_fresh_network`
- order 594: `_agent_web_extract_text_snippet` (function), lines 4301-4318, exports `_agent_web_extract_text_snippet`
- order 595: `AgentWebHTMLParser` (class), lines 4319-4398, exports `AgentWebHTMLParser`
- order 596: `_agent_web_decompress_bytes` (function), lines 4399-4422, exports `_agent_web_decompress_bytes`
- order 597: `_agent_web_charset_candidates` (function), lines 4423-4481, exports `_agent_web_charset_candidates`
- order 598: `_agent_web_decode_text_bytes` (function), lines 4482-4516, exports `_agent_web_decode_text_bytes`
- order 599: `AgentWebSearchEngine` (class), lines 4517-5586, exports `AgentWebSearchEngine`

### `server/http.py`

- order 863: `AgentHTTPServer` (class), lines 97885-97924, exports `AgentHTTPServer`
- order 866: `Handler` (class), lines 99044-100407, exports `Handler`

### `server/rag_admin.py`

- order 868: `RagAdminHandler` (class), lines 100634-100817, exports `RagAdminHandler`
- order 869: `CodeAdminHandler` (class), lines 100818-101020, exports `CodeAdminHandler`

### `server/skills.py`

- order 867: `SkillsHandler` (class), lines 100408-100633, exports `SkillsHandler`

### `session/manager.py`

- order 515: `SessionCreationLimitExceeded` (class), lines 2912-2917, exports `SessionCreationLimitExceeded`
- order 781: `SessionManager` (class), lines 70134-71455, exports `SessionManager`

### `session/state.py`

- order 780: `SessionState` (class), lines 19182-70133, exports `SessionState`

### `skills/embedded.py`

- order 711: `EMBEDDED_SKILLS_ARCHIVE_B64` (constant), lines 9596-9597, exports `EMBEDDED_SKILLS_ARCHIVE_B64`
- order 712: `EMBEDDED_SKILLS_ARCHIVE_SHA256` (constant), lines 9598-9598, exports `EMBEDDED_SKILLS_ARCHIVE_SHA256`
- order 713: `EMBEDDED_SKILLS_ARCHIVE_FILES` (constant), lines 9599-9621, exports `EMBEDDED_SKILLS_ARCHIVE_FILES`
- order 738: `BUILTIN_CLAWHUB_SKILLS_VERSION` (constant), lines 12857-12859, exports `BUILTIN_CLAWHUB_SKILLS_VERSION`
- order 739: `EMBEDDED_CLAWHUB_SKILLS_ARCHIVE_B64` (constant), lines 12860-13105, exports `EMBEDDED_CLAWHUB_SKILLS_ARCHIVE_B64`
- order 741: `MCP_BUILDER_SKILL_MD` (constant), lines 13153-13327, exports `MCP_BUILDER_SKILL_MD`
- order 744: `SKILL_PROTOCOL_LOCAL` (constant), lines 13359-13360, exports `SKILL_PROTOCOL_LOCAL`
- order 745: `SKILL_PROTOCOL_CLAWHUB` (constant), lines 13361-13361, exports `SKILL_PROTOCOL_CLAWHUB`
- order 746: `SKILL_PROTOCOL_HTTP_JSON` (constant), lines 13362-13362, exports `SKILL_PROTOCOL_HTTP_JSON`
- order 747: `SKILL_PROTOCOL_SPECS` (constant), lines 13363-13395, exports `SKILL_PROTOCOL_SPECS`

### `skills/provisioning.py`

- order 714: `ensure_embedded_skills_at_root` (function), lines 9622-9687, exports `ensure_embedded_skills_at_root`
- order 715: `ensure_embedded_skills` (function), lines 9688-9691, exports `ensure_embedded_skills`
- order 717: `detect_upload_parser_capabilities` (function), lines 9698-9714, exports `detect_upload_parser_capabilities`
- order 718: `_render_cap_markdown` (function), lines 9715-9730, exports `_render_cap_markdown`
- order 719: `_write_text_if_changed` (function), lines 9731-9737, exports `_write_text_if_changed`
- order 720: `ensure_generated_document_skills` (function), lines 9738-9827, exports `ensure_generated_document_skills`
- order 721: `ensure_generated_image_coding_feedback_skill` (function), lines 9828-9928, exports `ensure_generated_image_coding_feedback_skill`
- order 722: `_skill_knowledge_files` (function), lines 9929-9949, exports `_skill_knowledge_files`
- order 723: `analyze_skill_building_knowledge` (function), lines 9950-10005, exports `analyze_skill_building_knowledge`
- order 724: `_sanitize_skill_slug` (function), lines 10006-10009, exports `_sanitize_skill_slug`
- order 725: `_build_skills_gen_skill_content` (function), lines 10010-10042, exports `_build_skills_gen_skill_content`
- order 726: `ensure_generated_skills_gen_skill` (function), lines 10043-10048, exports `ensure_generated_skills_gen_skill`
- order 727: `ensure_generated_execution_recovery_skill` (function), lines 10049-10133, exports `ensure_generated_execution_recovery_skill`
- order 728: `ensure_generated_systematic_debugging_skill` (function), lines 10134-10407, exports `ensure_generated_systematic_debugging_skill`
- order 729: `ensure_generated_code_engineering_mastery_skill` (function), lines 10408-10527, exports `ensure_generated_code_engineering_mastery_skill`
- order 730: `ensure_generated_smart_file_navigation_skill` (function), lines 10528-10644, exports `ensure_generated_smart_file_navigation_skill`
- order 731: `ensure_generated_html_frontend_report_skills` (function), lines 10645-10853, exports `ensure_generated_html_frontend_report_skills`
- order 732: `ensure_generated_deep_research_skills` (function), lines 10854-11123, exports `ensure_generated_deep_research_skills`
- order 733: `ensure_generated_research_scientific_skills` (function), lines 11124-11761, exports `ensure_generated_research_scientific_skills`
- order 734: `ensure_generated_rag_mastery_skills` (function), lines 11762-12063, exports `ensure_generated_rag_mastery_skills`
- order 735: `ensure_generated_multimodal_comprehension_skills` (function), lines 12064-12758, exports `ensure_generated_multimodal_comprehension_skills`
- order 736: `ensure_generated_runtime_skills_manifest` (function), lines 12759-12793, exports `ensure_generated_runtime_skills_manifest`
- order 737: `ensure_generated_agent_web_search_skill` (function), lines 12794-12856, exports `ensure_generated_agent_web_search_skill`
- order 740: `ensure_embedded_clawhub_skills` (function), lines 13106-13152, exports `ensure_embedded_clawhub_skills`
- order 742: `ensure_generated_mcp_builder_skill` (function), lines 13328-13339, exports `ensure_generated_mcp_builder_skill`
- order 743: `ensure_runtime_skills` (function), lines 13340-13358, exports `ensure_runtime_skills`

### `skills/store.py`

- order 748: `_BUILTIN_SKILLS` (assignment), lines 13396-13504, exports `_BUILTIN_SKILLS`
- order 749: `SkillStore` (class), lines 13505-14812, exports `SkillStore`

### `utils/compress.py`

- order 603: `compress_text_blob` (function), lines 5751-5757, exports `compress_text_blob`
- order 604: `decompress_text_blob` (function), lines 5758-5767, exports `decompress_text_blob`

### `utils/crypto.py`

- order 676: `CryptoBox` (class), lines 7709-7827, exports `CryptoBox`

### `utils/errors.py`

- order 623: `EmptyActionError` (class), lines 6256-6259, exports `EmptyActionError`

### `utils/files.py`

- order 479: `_normalize_js_lib_asset_ref` (function), lines 1703-1718, exports `_normalize_js_lib_asset_ref`
- order 480: `_resolve_js_lib_asset_path` (function), lines 1719-1750, exports `_resolve_js_lib_asset_path`
- order 481: `_discover_extra_js_lib_files` (function), lines 1751-1783, exports `_discover_extra_js_lib_files`
- order 561: `safe_path` (function), lines 3646-3656, exports `safe_path`
- order 562: `_safe_js_filename` (function), lines 3657-3665, exports `_safe_js_filename`
- order 563: `_sha256_bytes` (function), lines 3666-3668, exports `_sha256_bytes`
- order 564: `_sha256_file` (function), lines 3669-3678, exports `_sha256_file`
- order 565: `_download_http_bytes` (function), lines 3679-3688, exports `_download_http_bytes`
- order 566: `offline_js_lib_root` (function), lines 3689-3691, exports `offline_js_lib_root`
- order 567: `_offline_js_entry_relative_path` (function), lines 3692-3697, exports `_offline_js_entry_relative_path`
- order 568: `_archive_member_relative_path` (function), lines 3698-3708, exports `_archive_member_relative_path`
- order 569: `_path_size_bytes` (function), lines 3709-3725, exports `_path_size_bytes`
- order 570: `_extract_archive_to_dir` (function), lines 3726-3767, exports `_extract_archive_to_dir`
- order 571: `_package_required_paths` (function), lines 3768-3775, exports `_package_required_paths`
- order 572: `_package_install_ready` (function), lines 3776-3785, exports `_package_install_ready`
- order 573: `_postprocess_offline_js_package` (function), lines 3786-3822, exports `_postprocess_offline_js_package`
- order 574: `_ensure_offline_js_package` (function), lines 3823-3863, exports `_ensure_offline_js_package`
- order 575: `_render_offline_js_catalog_md` (function), lines 3864-3881, exports `_render_offline_js_catalog_md`
- order 577: `ensure_offline_js_libs` (function), lines 3893-4038, exports `ensure_offline_js_libs`
- order 578: `_normalize_external_js_url` (function), lines 4039-4044, exports `_normalize_external_js_url`
- order 579: `is_external_js_src` (function), lines 4045-4048, exports `is_external_js_src`
- order 580: `match_offline_js_catalog_by_url` (function), lines 4049-4066, exports `match_offline_js_catalog_by_url`
- order 581: `cache_external_js_url` (function), lines 4067-4100, exports `cache_external_js_url`
- order 679: `try_read_text` (function), lines 8031-8040, exports `try_read_text`

### `utils/http.py`

- order 53: `_URL_OPEN_ORIGINAL` (assignment), lines 61-61, exports `_URL_OPEN_ORIGINAL`
- order 54: `_HTTP_SSL_CONTEXT` (assignment), lines 62-62, exports `_HTTP_SSL_CONTEXT`
- order 72: `_shared_http_ssl_context` (function), lines 80-103, exports `_shared_http_ssl_context`
- order 73: `urlopen` (function), lines 104-113, exports `urlopen`
- order 554: `json_response_bytes` (function), lines 3590-3592, exports `json_response_bytes`
- order 555: `read_http_json_body` (function), lines 3593-3606, exports `read_http_json_body`
- order 556: `close_if_http_request_body_unread` (function), lines 3607-3620, exports `close_if_http_request_body_unread`

### `utils/json_utils.py`

- order 91: `JSON_FSYNC_ENABLED` (constant), lines 166-166, exports `JSON_FSYNC_ENABLED`
- order 553: `json_dumps` (function), lines 3586-3589, exports `json_dumps`
- order 613: `parse_tool_arguments` (function), lines 6061-6071, exports `parse_tool_arguments`
- order 614: `repair_truncated_json_object` (function), lines 6072-6126, exports `repair_truncated_json_object`
- order 615: `parse_tool_arguments_with_error` (function), lines 6127-6158, exports `parse_tool_arguments_with_error`
- order 616: `_is_valid_json_object` (function), lines 6159-6164, exports `_is_valid_json_object`
- order 617: `_scan_top_level_json_objects` (function), lines 6165-6188, exports `_scan_top_level_json_objects`
- order 618: `reconstruct_streamed_tool_args` (function), lines 6189-6233, exports `reconstruct_streamed_tool_args`
- order 636: `parse_json_object` (function), lines 6498-6504, exports `parse_json_object`
- order 637: `extract_json_object_from_text` (function), lines 6505-6528, exports `extract_json_object_from_text`
- order 680: `_json_default_copy` (function), lines 8041-8047, exports `_json_default_copy`
- order 681: `_read_json_file` (function), lines 8048-8069, exports `_read_json_file`
- order 682: `_write_json_file` (function), lines 8070-8098, exports `_write_json_file`

### `utils/media.py`

- order 530: `guess_mime_from_name` (function), lines 3260-3264, exports `guess_mime_from_name`
- order 531: `_convert_image_to_safe_format` (function), lines 3265-3284, exports `_convert_image_to_safe_format`
- order 532: `guess_ext_from_mime` (function), lines 3285-3293, exports `guess_ext_from_mime`

### `utils/misc.py`

- order 533: `now_ts` (function), lines 3294-3296, exports `now_ts`
- order 534: `_benign_socket_log_lock` (assignment), lines 3297-3299, exports `_benign_socket_log_lock`
- order 535: `_benign_socket_log_state` (assignment), lines 3300-3300, exports `_benign_socket_log_state`
- order 537: `is_benign_socket_error` (function), lines 3316-3336, exports `is_benign_socket_error`
- order 538: `_socket_error_code` (function), lines 3337-3348, exports `_socket_error_code`
- order 539: `_log_benign_socket_error_limited` (function), lines 3349-3385, exports `_log_benign_socket_error_limited`
- order 540: `swallow_benign_socket_error` (function), lines 3386-3392, exports `swallow_benign_socket_error`
- order 541: `normalize_timeout_seconds` (function), lines 3393-3408, exports `normalize_timeout_seconds`
- order 542: `detect_local_lan_ip` (function), lines 3409-3420, exports `detect_local_lan_ip`
- order 543: `_LOCAL_LAN_IP_CACHE` (assignment), lines 3421-3422, exports `_LOCAL_LAN_IP_CACHE`
- order 544: `detect_local_lan_ip_cached` (function), lines 3423-3436, exports `detect_local_lan_ip_cached`
- order 557: `make_id` (function), lines 3621-3623, exports `make_id`
- order 558: `sanitize_profile_id` (function), lines 3624-3627, exports `sanitize_profile_id`
- order 674: `user_id_from_ip` (function), lines 7668-7675, exports `user_id_from_ip`
- order 678: `_meta_string_list` (function), lines 8017-8030, exports `_meta_string_list`
- order 716: `_module_exists` (function), lines 9692-9697, exports `_module_exists`

### `utils/text.py`

- order 79: `MAX_TOOL_OUTPUT` (constant), lines 154-154, exports `MAX_TOOL_OUTPUT`
- order 333: `SOCKET_NOISE_LINE_PATTERNS` (constant), lines 663-668, exports `SOCKET_NOISE_LINE_PATTERNS`
- order 536: `filter_runtime_noise_lines` (function), lines 3301-3315, exports `filter_runtime_noise_lines`
- order 549: `safe_utf8_bytes` (function), lines 3561-3563, exports `safe_utf8_bytes`
- order 550: `escape_invalid_utf8_text` (function), lines 3564-3566, exports `escape_invalid_utf8_text`
- order 551: `sanitize_utf8_surrogates` (function), lines 3567-3580, exports `sanitize_utf8_surrogates`
- order 552: `decode_utf8_replace` (function), lines 3581-3585, exports `decode_utf8_replace`
- order 582: `trim` (function), lines 4101-4104, exports `trim`
- order 583: `display_clean` (function), lines 4105-4119, exports `display_clean`
- order 584: `short_title_from` (function), lines 4120-4138, exports `short_title_from`
- order 600: `_fmt_export_ts` (function), lines 5587-5597, exports `_fmt_export_ts`
- order 601: `_html_esc` (function), lines 5598-5601, exports `_html_esc`
- order 602: `_text_to_minimal_pdf` (function), lines 5602-5750, exports `_text_to_minimal_pdf`
- order 605: `normalize_embedded_newlines` (function), lines 5768-5777, exports `normalize_embedded_newlines`
- order 606: `_map_todo_status_token` (function), lines 5778-5816, exports `_map_todo_status_token`
- order 607: `split_todo_status_text` (function), lines 5817-5876, exports `split_todo_status_text`
- order 608: `extract_todo_rows_from_text` (function), lines 5877-5946, exports `extract_todo_rows_from_text`
- order 609: `decode_structured_todo_container` (function), lines 5947-5965, exports `decode_structured_todo_container`
- order 610: `infer_todo_status_from_text` (function), lines 5966-5974, exports `infer_todo_status_from_text`
- order 611: `split_structured_todo_content` (function), lines 5975-6030, exports `split_structured_todo_content`
- order 612: `normalize_work_text` (function), lines 6031-6060, exports `normalize_work_text`
- order 693: `make_unified_diff` (function), lines 8791-8809, exports `make_unified_diff`
- order 694: `_skip_row` (function), lines 8810-8815, exports `_skip_row`
- order 695: `_row_is_hot` (function), lines 8816-8819, exports `_row_is_hot`
- order 696: `_hotspot_index` (function), lines 8820-8843, exports `_hotspot_index`
- order 697: `_compress_rows_keep_hotspot` (function), lines 8844-8893, exports `_compress_rows_keep_hotspot`
- order 698: `_focused_diff_rows_from_opcodes` (function), lines 8894-9028, exports `_focused_diff_rows_from_opcodes`
- order 699: `make_numbered_diff` (function), lines 9029-9061, exports `make_numbered_diff`
- order 700: `render_numbered_diff_text` (function), lines 9062-9075, exports `render_numbered_diff_text`

### `web/admin_assets.py`

- order 789: `ADMIN_INDEX_HTML` (constant), lines 77320-77482, exports `ADMIN_INDEX_HTML`
- order 790: `ADMIN_CSS` (constant), lines 77483-77610, exports `ADMIN_CSS`
- order 791: `ADMIN_JS` (constant), lines 77611-77675, exports `ADMIN_JS`

### `web/assets.py`

- order 782: `INDEX_HTML` (constant), lines 71456-71701, exports `INDEX_HTML`
- order 783: `APP_CSS` (constant), lines 71702-72237, exports `APP_CSS`
- order 784: `APP_JS` (constant), lines 72238-76880, exports `APP_JS`
- order 785: `APP_TS` (constant), lines 76881-76920, exports `APP_TS`

### `web/skills_assets.py`

- order 786: `SKILLS_INDEX_HTML` (constant), lines 76921-77076, exports `SKILLS_INDEX_HTML`
- order 787: `SKILLS_EXTRA_CSS` (constant), lines 77077-77173, exports `SKILLS_EXTRA_CSS`
- order 788: `SKILLS_APP_JS` (constant), lines 77174-77319, exports `SKILLS_APP_JS`
