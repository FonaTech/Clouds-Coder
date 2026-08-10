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
| `_imports.py` | 53 | 66 | — | 1–62 |
| `admin/auth.py` | 3 | 3 | `admin/constants.py`, `utils/misc.py` | 7678–8379 |
| `admin/config.py` | 8 | 8 | `config/constants.py`, `config/paths.py`, `config/settings.py`, `llm/constants.py`, `utils/http.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` | 8380–8792 |
| `admin/constants.py` | 13 | 13 | — | 69–81 |
| `agent/background.py` | 1 | 1 | `utils/misc.py`, `utils/text.py` | 14950–15046 |
| `agent/bus.py` | 1 | 1 | `config/constants.py`, `utils/crypto.py`, `utils/misc.py` | 15047–15112 |
| `agent/errors.py` | 1 | 1 | — | 6262–6265 |
| `agent/events.py` | 1 | 1 | — | 9190–9236 |
| `agent/tasks.py` | 1 | 1 | `utils/crypto.py`, `utils/json_utils.py`, `utils/misc.py` | 14815–14949 |
| `agent/todo.py` | 1 | 1 | `config/constants.py`, `config/settings.py`, `utils/misc.py`, `utils/text.py` | 9237–9597 |
| `agent/tools.py` | 13 | 17 | `config/constants.py` | 18526–19183 |
| `agent/worktree.py` | 1 | 1 | `agent/tasks.py`, `config/constants.py`, `utils/crypto.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` | 15113–15329 |
| `app/context.py` | 1 | 1 | `admin/auth.py`, `admin/config.py`, `admin/constants.py`, `agent/tools.py`, `app/services.py`, `config/constants.py`, `config/paths.py`, `config/settings.py`, `ide/assets.py`, `llm/client.py`, `llm/constants.py`, `llm/utils.py`, `mcp/driver.py`, `rag/assets.py`, `rag/constants.py`, `rag/ingestion.py`, `rag/parsers.py`, `rag/store.py`, `session/manager.py`, `session/state.py`, `skills/provisioning.py`, `skills/store.py`, `utils/crypto.py`, `utils/files.py`, `utils/json_utils.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py`, `web/assets.py`, `web/skills_assets.py` | 93039–97886 |
| `app/main.py` | 2 | 1 | `admin/config.py`, `admin/constants.py`, `agent/tools.py`, `app/context.py`, `config/constants.py`, `config/paths.py`, `config/settings.py`, `ide/handler.py`, `llm/constants.py`, `llm/utils.py`, `mcp/constants.py`, `mcp/service.py`, `rag/constants.py`, `server/http.py`, `server/rag_admin.py`, `server/skills.py`, `skills/provisioning.py`, `utils/files.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` | 101471–103114 |
| `app/services.py` | 2 | 2 | `admin/constants.py`, `config/settings.py`, `skills/embedded.py`, `skills/store.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` | 97927–99045 |
| `config/constants.py` | 344 | 340 | `rag/constants.py` | 65–9108 |
| `config/paths.py` | 8 | 8 | `utils/text.py` | 68–3647 |
| `config/settings.py` | 62 | 62 | `agent/tools.py`, `config/constants.py`, `config/paths.py`, `llm/constants.py`, `llm/utils.py`, `rag/constants.py`, `skills/provisioning.py`, `utils/http.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` | 1786–8018 |
| `ide/assets.py` | 3 | 3 | — | 92695–93038 |
| `ide/handler.py` | 1 | 1 | `admin/auth.py`, `app/context.py`, `config/constants.py`, `session/manager.py`, `utils/http.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py` | 101023–101306 |
| `llm/client.py` | 2 | 2 | `agent/tools.py`, `config/constants.py`, `config/settings.py`, `llm/utils.py`, `utils/http.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` | 16208–18525 |
| `llm/constants.py` | 17 | 17 | — | 66–6710 |
| `llm/utils.py` | 22 | 22 | `config/settings.py`, `llm/constants.py`, `utils/http.py`, `utils/json_utils.py`, `utils/text.py` | 6236–6924 |
| `mcp/constants.py` | 7 | 7 | — | 173–15364 |
| `mcp/driver.py` | 5 | 5 | `mcp/constants.py`, `utils/files.py`, `utils/json_utils.py`, `utils/text.py` | 15365–16207 |
| `mcp/service.py` | 1 | 1 | `app/context.py`, `config/constants.py`, `utils/files.py`, `utils/http.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` | 101307–101470 |
| `rag/assets.py` | 6 | 6 | — | 90287–92694 |
| `rag/constants.py` | 74 | 74 | — | 169–83429 |
| `rag/index.py` | 5 | 5 | `rag/constants.py`, `rag/ingestion.py`, `rag/parsers.py`, `utils/misc.py`, `utils/text.py` | 83454–89932 |
| `rag/ingestion.py` | 13 | 13 | `config/constants.py`, `config/settings.py`, `rag/constants.py`, `rag/parsers.py`, `rag/store.py`, `session/state.py`, `utils/files.py`, `utils/json_utils.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py` | 82822–90286 |
| `rag/parsers.py` | 28 | 28 | `config/constants.py`, `rag/constants.py`, `rag/ingestion.py`, `utils/files.py`, `utils/json_utils.py`, `utils/media.py`, `utils/text.py` | 9078–84562 |
| `rag/store.py` | 7 | 7 | `config/constants.py`, `config/settings.py`, `rag/constants.py`, `rag/index.py`, `rag/ingestion.py`, `rag/parsers.py`, `skills/provisioning.py`, `utils/files.py`, `utils/json_utils.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py` | 86240–90198 |
| `rag/web_search.py` | 15 | 15 | `config/constants.py`, `config/paths.py`, `rag/constants.py`, `utils/http.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` | 4141–5588 |
| `server/http.py` | 2 | 2 | `admin/auth.py`, `admin/config.py`, `app/context.py`, `config/constants.py`, `config/paths.py`, `config/settings.py`, `llm/utils.py`, `rag/parsers.py`, `session/manager.py`, `session/state.py`, `utils/files.py`, `utils/http.py`, `utils/json_utils.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py`, `web/admin_assets.py` | 97887–100409 |
| `server/rag_admin.py` | 2 | 2 | `admin/auth.py`, `app/context.py`, `config/constants.py`, `rag/constants.py`, `utils/http.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py` | 100636–101022 |
| `server/skills.py` | 1 | 1 | `admin/auth.py`, `app/context.py`, `config/constants.py`, `config/paths.py`, `config/settings.py`, `session/manager.py`, `skills/provisioning.py`, `utils/http.py`, `utils/misc.py`, `utils/text.py` | 100410–100635 |
| `session/manager.py` | 2 | 2 | `config/constants.py`, `config/paths.py`, `config/settings.py`, `llm/client.py`, `llm/utils.py`, `rag/store.py`, `session/state.py`, `utils/crypto.py`, `utils/files.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` | 2914–71457 |
| `session/state.py` | 1 | 1 | `admin/constants.py`, `agent/background.py`, `agent/bus.py`, `agent/errors.py`, `agent/events.py`, `agent/tasks.py`, `agent/todo.py`, `agent/tools.py`, `agent/worktree.py`, `config/constants.py`, `config/paths.py`, `config/settings.py`, `llm/client.py`, `llm/constants.py`, `llm/utils.py`, `mcp/constants.py`, `mcp/driver.py`, `rag/constants.py`, `rag/parsers.py`, `rag/web_search.py`, `skills/provisioning.py`, `skills/store.py`, `utils/compress.py`, `utils/crypto.py`, `utils/errors.py`, `utils/files.py`, `utils/http.py`, `utils/json_utils.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py` | 19184–70135 |
| `skills/embedded.py` | 10 | 10 | — | 9598–13397 |
| `skills/provisioning.py` | 26 | 26 | `config/paths.py`, `skills/embedded.py`, `utils/files.py`, `utils/json_utils.py`, `utils/misc.py` | 9624–13360 |
| `skills/store.py` | 2 | 2 | `config/constants.py`, `config/settings.py`, `llm/utils.py`, `skills/embedded.py`, `utils/files.py`, `utils/http.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` | 13398–14814 |
| `utils/compress.py` | 2 | 2 | — | 5753–5769 |
| `utils/crypto.py` | 1 | 1 | `utils/json_utils.py` | 7711–7829 |
| `utils/errors.py` | 1 | 1 | — | 6258–6261 |
| `utils/files.py` | 24 | 24 | `config/constants.py`, `config/paths.py`, `utils/http.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` | 1705–8042 |
| `utils/http.py` | 7 | 7 | `utils/json_utils.py`, `utils/text.py` | 63–3622 |
| `utils/json_utils.py` | 13 | 13 | `utils/text.py` | 168–8100 |
| `utils/media.py` | 3 | 3 | — | 3262–3295 |
| `utils/misc.py` | 16 | 16 | `config/constants.py` | 3296–9699 |
| `utils/text.py` | 29 | 29 | `config/constants.py` | 156–9077 |
| `web/admin_assets.py` | 3 | 3 | — | 77322–77677 |
| `web/assets.py` | 4 | 4 | — | 71458–76922 |
| `web/skills_assets.py` | 3 | 3 | — | 76923–77321 |

## Source Mapping

### `_imports.py`

- order 0: `_import_2` (import), lines 1-2, exports `annotations`
- order 1: `_import_4` (import), lines 3-4, exports `argparse`
- order 2: `_import_5` (import), lines 5-5, exports `ast`
- order 3: `_import_6` (import), lines 6-6, exports `base64`
- order 4: `_import_7` (import), lines 7-7, exports `concurrent`
- order 5: `_import_8` (import), lines 8-8, exports `csv`
- order 6: `_import_9` (import), lines 9-9, exports `difflib`
- order 7: `_import_10` (import), lines 10-10, exports `errno`
- order 8: `_import_11` (import), lines 11-11, exports `hashlib`
- order 9: `_import_12` (import), lines 12-12, exports `hmac`
- order 10: `_import_13` (import), lines 13-13, exports `html`
- order 11: `_import_14` (import), lines 14-14, exports `importlib`
- order 12: `_import_15` (import), lines 15-15, exports `io`
- order 13: `_import_16` (import), lines 16-16, exports `ipaddress`
- order 14: `_import_17` (import), lines 17-17, exports `json`
- order 15: `_import_18` (import), lines 18-18, exports `locale`
- order 16: `_import_19` (import), lines 19-19, exports `math`
- order 17: `_import_20` (import), lines 20-20, exports `mimetypes`
- order 18: `_import_21` (import), lines 21-21, exports `multiprocessing`
- order 19: `_import_22` (import), lines 22-22, exports `os`
- order 20: `_import_23` (import), lines 23-23, exports `queue`
- order 21: `_import_24` (import), lines 24-24, exports `re`
- order 22: `_import_25` (import), lines 25-25, exports `selectors`
- order 23: `_import_26` (import), lines 26-26, exports `shlex`
- order 24: `_import_27` (import), lines 27-27, exports `shutil`
- order 25: `_import_28` (import), lines 28-28, exports `signal`
- order 26: `_import_29` (import), lines 29-29, exports `socket`
- order 27: `_import_30` (import), lines 30-30, exports `sqlite3`
- order 28: `_import_31` (import), lines 31-31, exports `ssl`
- order 29: `_import_32` (import), lines 32-32, exports `subprocess`
- order 30: `_import_33` (import), lines 33-33, exports `sys`
- order 31: `_import_34` (import), lines 34-34, exports `tarfile`
- order 32: `_import_35` (import), lines 35-35, exports `threading`
- order 33: `_import_36` (import), lines 36-36, exports `time`
- order 34: `_import_37` (import), lines 37-37, exports `traceback`
- order 35: `_import_38` (import), lines 38-38, exports `unicodedata`
- order 36: `_import_39` (import), lines 39-39, exports `robotparser`
- order 37: `_import_40` (import), lines 40-40, exports `uuid`
- order 38: `_import_41` (import), lines 41-41, exports `ET`
- order 39: `_import_42` (import), lines 42-42, exports `zipfile`
- order 40: `_import_43` (import), lines 43-43, exports `zlib`
- order 41: `_import_44` (import), lines 44-44, exports `Counter`, `defaultdict`, `deque`
- order 42: `_import_45` (import), lines 45-45, exports `datetime`, `timedelta`, `timezone`
- order 43: `_import_46` (import), lines 46-46, exports `parsedate_to_datetime`
- order 44: `_import_47` (import), lines 47-47, exports `HTMLParser`
- order 45: `_import_48` (import), lines 48-48, exports `HTTPStatus`
- order 46: `_import_49` (import), lines 49-49, exports `BaseHTTPRequestHandler`, `ThreadingHTTPServer`
- order 47: `_import_50` (import), lines 50-50, exports `Path`, `PurePosixPath`
- order 48: `_import_51` (import), lines 51-51, exports `HTTPError`, `URLError`
- order 49: `_import_52` (import), lines 52-52, exports `parse_qs`, `quote`, `unquote`, `urljoin`, `urlparse`, `urlunparse`
- order 50: `_import_53` (import), lines 53-53, exports `Request`, `urlopen`
- order 51: `_try_import_55` (import), lines 54-58, exports `_certifi`
- order 52: `_try_import_59` (import), lines 59-62, exports `_yaml`

### `admin/auth.py`

- order 675: `trusted_client_ip` (function), lines 7678-7710, exports `trusted_client_ip`
- order 683: `AdminAuthError` (class), lines 8101-8108, exports `AdminAuthError`
- order 684: `AdminAuthStore` (class), lines 8109-8379, exports `AdminAuthStore`

### `admin/config.py`

- order 685: `_admin_config_schema` (function), lines 8380-8487, exports `_admin_config_schema`
- order 686: `_admin_factory_config` (function), lines 8488-8491, exports `_admin_factory_config`
- order 687: `_admin_coerce_config` (function), lines 8492-8612, exports `_admin_coerce_config`
- order 688: `_admin_config_to_argv` (function), lines 8613-8649, exports `_admin_config_to_argv`
- order 689: `_admin_restart_probe_url` (function), lines 8650-8665, exports `_admin_restart_probe_url`
- order 690: `_admin_supervised_restart` (function), lines 8666-8752, exports `_admin_supervised_restart`
- order 691: `_admin_argparse_defaults` (function), lines 8753-8772, exports `_admin_argparse_defaults`
- order 692: `_admin_config_from_namespace` (function), lines 8773-8792, exports `_admin_config_from_namespace`

### `admin/constants.py`

- order 59: `ADMIN_STATE_DIRNAME` (constant), lines 69-69, exports `ADMIN_STATE_DIRNAME`
- order 60: `ADMIN_CONFIG_FILENAME` (constant), lines 70-70, exports `ADMIN_CONFIG_FILENAME`
- order 61: `ADMIN_APPS_FILENAME` (constant), lines 71-71, exports `ADMIN_APPS_FILENAME`
- order 62: `ADMIN_TELEMETRY_FILENAME` (constant), lines 72-72, exports `ADMIN_TELEMETRY_FILENAME`
- order 63: `ADMIN_AUTH_FILENAME` (constant), lines 73-73, exports `ADMIN_AUTH_FILENAME`
- order 64: `ADMIN_MAX_APP_SKILLS` (constant), lines 74-74, exports `ADMIN_MAX_APP_SKILLS`
- order 65: `ADMIN_MAX_APP_CAPSULE_CHARS` (constant), lines 75-75, exports `ADMIN_MAX_APP_CAPSULE_CHARS`
- order 66: `ADMIN_MAX_APP_RESOURCE_FILES` (constant), lines 76-76, exports `ADMIN_MAX_APP_RESOURCE_FILES`
- order 67: `ADMIN_MAX_APP_RESOURCE_BYTES` (constant), lines 77-77, exports `ADMIN_MAX_APP_RESOURCE_BYTES`
- order 68: `ADMIN_APP_INLINE_BLOB_BYTES` (constant), lines 78-78, exports `ADMIN_APP_INLINE_BLOB_BYTES`
- order 69: `ADMIN_AUTH_SESSION_TTL_SECONDS` (constant), lines 79-79, exports `ADMIN_AUTH_SESSION_TTL_SECONDS`
- order 70: `ADMIN_AUTH_PASSWORD_ITERATIONS` (constant), lines 80-80, exports `ADMIN_AUTH_PASSWORD_ITERATIONS`
- order 71: `ADMIN_AUTH_MAX_ACTIVE_SESSIONS` (constant), lines 81-81, exports `ADMIN_AUTH_MAX_ACTIVE_SESSIONS`

### `agent/background.py`

- order 751: `BackgroundManager` (class), lines 14950-15046, exports `BackgroundManager`

### `agent/bus.py`

- order 752: `MessageBus` (class), lines 15047-15112, exports `MessageBus`

### `agent/errors.py`

- order 624: `CircuitBreakerTriggered` (class), lines 6262-6265, exports `CircuitBreakerTriggered`

### `agent/events.py`

- order 709: `EventHub` (class), lines 9190-9236, exports `EventHub`

### `agent/tasks.py`

- order 750: `TaskManager` (class), lines 14815-14949, exports `TaskManager`

### `agent/todo.py`

- order 710: `TodoManager` (class), lines 9237-9597, exports `TodoManager`

### `agent/tools.py`

- order 767: `tool_def` (function), lines 18526-18539, exports `tool_def`
- order 768: `TOOLS` (constant), lines 18540-19022, exports `TOOLS`
- order 769: `TOOL_REQUIRED_ARGS` (constant), lines 19023-19024, exports `TOOL_REQUIRED_ARGS`
- order 770: `TOOL_SPEC_BY_NAME` (constant), lines 19025-19025, exports `TOOL_SPEC_BY_NAME`
- order 771: `_for_19026` (statement), lines 19026-19035, exports `_tool`, `_fn`, `_name`, `_required`
- order 772: `TOOL_NAME_FUZZY_MAP` (constant), lines 19036-19037, exports `TOOL_NAME_FUZZY_MAP`
- order 773: `_for_19038` (statement), lines 19038-19041, exports `_name`, `_key`
- order 774: `_for_19043` (statement), lines 19042-19059, exports `_alias`, `_target`
- order 775: `is_todo_resume_tool_name` (function), lines 19060-19076, exports `is_todo_resume_tool_name`
- order 776: `canonicalize_tool_name` (function), lines 19077-19095, exports `canonicalize_tool_name`
- order 777: `filter_tool_specs_for_runtime` (function), lines 19096-19111, exports `filter_tool_specs_for_runtime`
- order 778: `DEVELOPER_TOOL_DROP` (constant), lines 19112-19122, exports `DEVELOPER_TOOL_DROP`
- order 779: `AGENT_TOOL_ALLOWLIST` (constant), lines 19123-19183, exports `AGENT_TOOL_ALLOWLIST`

### `agent/worktree.py`

- order 753: `WorktreeManager` (class), lines 15113-15329, exports `WorktreeManager`

### `app/context.py`

- order 862: `AppContext` (class), lines 93039-97886, exports `AppContext`

### `app/main.py`

- order 872: `main` (function), lines 101471-103111, exports `main`
- order 873: `_main_guard_103113` (main_guard), lines 103112-103114, exports —

### `app/services.py`

- order 864: `TelemetryStore` (class), lines 97927-98302, exports `TelemetryStore`
- order 865: `ApplicationRegistry` (class), lines 98303-99045, exports `ApplicationRegistry`

### `config/constants.py`

- order 55: `APP_VERSION` (constant), lines 65-65, exports `APP_VERSION`
- order 80: `LONG_OUTPUT_MODEL_PAGE_CHARS` (constant), lines 157-157, exports `LONG_OUTPUT_MODEL_PAGE_CHARS`
- order 81: `LONG_OUTPUT_UI_PAGE_CHARS` (constant), lines 158-158, exports `LONG_OUTPUT_UI_PAGE_CHARS`
- order 82: `LONG_OUTPUT_UI_PREVIEW_MAX_PAGES` (constant), lines 159-159, exports `LONG_OUTPUT_UI_PREVIEW_MAX_PAGES`
- order 83: `LONG_OUTPUT_LISTING_OFFLOAD_CHARS` (constant), lines 160-160, exports `LONG_OUTPUT_LISTING_OFFLOAD_CHARS`
- order 84: `LONG_OUTPUT_READ_PAGE_LINES` (constant), lines 161-161, exports `LONG_OUTPUT_READ_PAGE_LINES`
- order 85: `LONG_OUTPUT_READ_PAGE_MAX_CHARS` (constant), lines 162-162, exports `LONG_OUTPUT_READ_PAGE_MAX_CHARS`
- order 86: `LONG_OUTPUT_TEMP_MAX_FILES` (constant), lines 163-163, exports `LONG_OUTPUT_TEMP_MAX_FILES`
- order 87: `READ_FILE_DEFAULT_MAX_CHARS` (constant), lines 164-164, exports `READ_FILE_DEFAULT_MAX_CHARS`
- order 88: `READ_FILE_HARD_MAX_CHARS` (constant), lines 165-165, exports `READ_FILE_HARD_MAX_CHARS`
- order 89: `READ_FILE_OVERVIEW_HEAD_LINES` (constant), lines 166-166, exports `READ_FILE_OVERVIEW_HEAD_LINES`
- order 90: `READ_FILE_SEARCH_MAX_MATCHES` (constant), lines 167-167, exports `READ_FILE_SEARCH_MAX_MATCHES`
- order 95: `CODE_ADMIN_PORT_OFFSET` (constant), lines 172-172, exports `CODE_ADMIN_PORT_OFFSET`
- order 97: `IDE_PORT_OFFSET` (constant), lines 174-177, exports `IDE_PORT_OFFSET`
- order 98: `IDE_DEFAULT_PORT` (constant), lines 178-178, exports `IDE_DEFAULT_PORT`
- order 100: `DEFAULT_WEB_SEARCH_ENABLED` (constant), lines 180-180, exports `DEFAULT_WEB_SEARCH_ENABLED`
- order 105: `DEFAULT_USER_MEMORY_MODE` (constant), lines 185-185, exports `DEFAULT_USER_MEMORY_MODE`
- order 113: `AGENT_WEB_SEARCH_USER_AGENT` (constant), lines 196-196, exports `AGENT_WEB_SEARCH_USER_AGENT`
- order 114: `AGENT_WEB_SEARCH_DEFAULT_MAX_RESULTS` (constant), lines 197-197, exports `AGENT_WEB_SEARCH_DEFAULT_MAX_RESULTS`
- order 115: `AGENT_WEB_SEARCH_DEFAULT_MAX_PAGES` (constant), lines 198-198, exports `AGENT_WEB_SEARCH_DEFAULT_MAX_PAGES`
- order 116: `AGENT_WEB_SEARCH_HARD_MAX_PAGES` (constant), lines 199-199, exports `AGENT_WEB_SEARCH_HARD_MAX_PAGES`
- order 117: `AGENT_WEB_SEARCH_DEFAULT_DEPTH` (constant), lines 200-200, exports `AGENT_WEB_SEARCH_DEFAULT_DEPTH`
- order 118: `AGENT_WEB_SEARCH_HARD_DEPTH` (constant), lines 201-201, exports `AGENT_WEB_SEARCH_HARD_DEPTH`
- order 119: `AGENT_WEB_SEARCH_FETCH_TIMEOUT` (constant), lines 202-202, exports `AGENT_WEB_SEARCH_FETCH_TIMEOUT`
- order 120: `AGENT_WEB_SEARCH_TOOL_SOFT_TIMEOUT` (constant), lines 203-203, exports `AGENT_WEB_SEARCH_TOOL_SOFT_TIMEOUT`
- order 121: `AGENT_WEB_SEARCH_MAX_PAGE_BYTES` (constant), lines 204-204, exports `AGENT_WEB_SEARCH_MAX_PAGE_BYTES`
- order 122: `AGENT_WEB_SEARCH_MAX_TEXT_CHARS` (constant), lines 205-205, exports `AGENT_WEB_SEARCH_MAX_TEXT_CHARS`
- order 132: `CODE_CHUNK_CHARS` (constant), lines 227-227, exports `CODE_CHUNK_CHARS`
- order 133: `CODE_CHUNK_OVERLAP` (constant), lines 228-228, exports `CODE_CHUNK_OVERLAP`
- order 134: `CODE_MAX_CHUNKS_PER_DOC` (constant), lines 229-229, exports `CODE_MAX_CHUNKS_PER_DOC`
- order 172: `CODE_IMPORT_WORKER_COUNT` (constant), lines 289-292, exports `CODE_IMPORT_WORKER_COUNT`
- order 174: `CODE_PARSE_TIMEOUT_SECONDS` (constant), lines 297-300, exports `CODE_PARSE_TIMEOUT_SECONDS`
- order 175: `DEFAULT_CONTEXT_TOKEN_LIMIT` (constant), lines 301-301, exports `DEFAULT_CONTEXT_TOKEN_LIMIT`
- order 176: `TOKEN_THRESHOLD` (constant), lines 302-302, exports `TOKEN_THRESHOLD`
- order 177: `CONTEXT_AUTO_COMPACT_RESERVE_RATIO` (constant), lines 303-306, exports `CONTEXT_AUTO_COMPACT_RESERVE_RATIO`
- order 178: `CONTEXT_ESTIMATE_SAFETY_MULTIPLIER` (constant), lines 307-310, exports `CONTEXT_ESTIMATE_SAFETY_MULTIPLIER`
- order 179: `CONTEXT_USAGE_CALIBRATION_MAX` (constant), lines 311-314, exports `CONTEXT_USAGE_CALIBRATION_MAX`
- order 180: `CONTEXT_ACTUAL_USAGE_RECENT_SECONDS` (constant), lines 315-318, exports `CONTEXT_ACTUAL_USAGE_RECENT_SECONDS`
- order 181: `LARGE_FILE_AUTO_PAGE_BYTES` (constant), lines 319-322, exports `LARGE_FILE_AUTO_PAGE_BYTES`
- order 182: `LARGE_FILE_AUTO_PAGE_LINES` (constant), lines 323-326, exports `LARGE_FILE_AUTO_PAGE_LINES`
- order 183: `LARGE_SOURCE_UPLOAD_EXCERPT_CHARS` (constant), lines 327-330, exports `LARGE_SOURCE_UPLOAD_EXCERPT_CHARS`
- order 184: `CHAT_UPLOAD_PARSE_QUEUE_MAX` (constant), lines 331-334, exports `CHAT_UPLOAD_PARSE_QUEUE_MAX`
- order 185: `CHAT_UPLOAD_PARSE_TIMEOUT_SECONDS` (constant), lines 335-338, exports `CHAT_UPLOAD_PARSE_TIMEOUT_SECONDS`
- order 186: `CHAT_UPLOAD_INLINE_TEXT_BYTES` (constant), lines 339-342, exports `CHAT_UPLOAD_INLINE_TEXT_BYTES`
- order 187: `CHAT_UPLOAD_PARSE_MAX_BYTES` (constant), lines 343-349, exports `CHAT_UPLOAD_PARSE_MAX_BYTES`
- order 188: `CHAT_UPLOAD_ZIP_ENTRY_MAX_BYTES` (constant), lines 350-356, exports `CHAT_UPLOAD_ZIP_ENTRY_MAX_BYTES`
- order 189: `CHAT_UPLOAD_TEXT_CONTEXT_CHARS` (constant), lines 357-360, exports `CHAT_UPLOAD_TEXT_CONTEXT_CHARS`
- order 190: `CHAT_UPLOAD_PROMPT_MAX_FILES` (constant), lines 361-364, exports `CHAT_UPLOAD_PROMPT_MAX_FILES`
- order 191: `CHAT_UPLOAD_PROMPT_MAX_CHARS` (constant), lines 365-368, exports `CHAT_UPLOAD_PROMPT_MAX_CHARS`
- order 192: `CHAT_UPLOAD_PROMPT_PER_FILE_CHARS` (constant), lines 369-372, exports `CHAT_UPLOAD_PROMPT_PER_FILE_CHARS`
- order 193: `CHAT_UPLOAD_FRONTEND_WAIT_MS` (constant), lines 373-376, exports `CHAT_UPLOAD_FRONTEND_WAIT_MS`
- order 194: `CHAT_UPLOAD_AUTO_LIBRARY_INGEST` (constant), lines 377-380, exports `CHAT_UPLOAD_AUTO_LIBRARY_INGEST`
- order 195: `CHAT_UPLOAD_INGEST_QUEUE_MAX` (constant), lines 381-384, exports `CHAT_UPLOAD_INGEST_QUEUE_MAX`
- order 196: `SESSION_SUBMIT_LOCK_TIMEOUT_SECONDS` (constant), lines 385-388, exports `SESSION_SUBMIT_LOCK_TIMEOUT_SECONDS`
- order 197: `SESSION_DEFERRED_START_QUEUE_MAX` (constant), lines 389-392, exports `SESSION_DEFERRED_START_QUEUE_MAX`
- order 198: `SESSION_WATCHDOG_INTERVAL_SECONDS` (constant), lines 393-396, exports `SESSION_WATCHDOG_INTERVAL_SECONDS`
- order 199: `SESSION_HEARTBEAT_STALE_SECONDS` (constant), lines 397-400, exports `SESSION_HEARTBEAT_STALE_SECONDS`
- order 200: `SESSION_LIST_DEFAULT_LIMIT` (constant), lines 401-404, exports `SESSION_LIST_DEFAULT_LIMIT`
- order 201: `IDLE_TIMEOUT` (constant), lines 405-405, exports `IDLE_TIMEOUT`
- order 202: `POLL_INTERVAL` (constant), lines 406-406, exports `POLL_INTERVAL`
- order 203: `SSE_HEARTBEAT_SECONDS` (constant), lines 407-407, exports `SSE_HEARTBEAT_SECONDS`
- order 204: `MODEL_CALL_PROGRESS_DELAY` (constant), lines 408-408, exports `MODEL_CALL_PROGRESS_DELAY`
- order 205: `MODEL_CALL_PROGRESS_INTERVAL` (constant), lines 409-409, exports `MODEL_CALL_PROGRESS_INTERVAL`
- order 206: `RUN_COMPLETION_SUMMARY_ENABLED` (constant), lines 410-413, exports `RUN_COMPLETION_SUMMARY_ENABLED`
- order 207: `LLM_HTTP_RETRY_MAX_ATTEMPTS` (constant), lines 414-417, exports `LLM_HTTP_RETRY_MAX_ATTEMPTS`
- order 208: `LLM_HTTP_RETRY_DELAY_SECONDS` (constant), lines 418-421, exports `LLM_HTTP_RETRY_DELAY_SECONDS`
- order 209: `LLM_HTTP_RETRY_MAX_SECONDS` (constant), lines 422-425, exports `LLM_HTTP_RETRY_MAX_SECONDS`
- order 210: `LLM_HTTP_RETRY_404_ON_VLLM` (constant), lines 426-429, exports `LLM_HTTP_RETRY_404_ON_VLLM`
- order 211: `LLM_HTTP_RETRY_STATUSES` (constant), lines 430-430, exports `LLM_HTTP_RETRY_STATUSES`
- order 212: `MAX_AGENT_ROUNDS` (constant), lines 431-431, exports `MAX_AGENT_ROUNDS`
- order 213: `MIN_AGENT_ROUNDS` (constant), lines 432-432, exports `MIN_AGENT_ROUNDS`
- order 214: `MAX_AGENT_ROUNDS_CAP` (constant), lines 433-433, exports `MAX_AGENT_ROUNDS_CAP`
- order 215: `REPEATED_TOOL_LOOP_THRESHOLD` (constant), lines 434-434, exports `REPEATED_TOOL_LOOP_THRESHOLD`
- order 216: `BASH_READ_LOOP_THRESHOLD` (constant), lines 435-435, exports `BASH_READ_LOOP_THRESHOLD`
- order 217: `READ_FILE_LOOP_THRESHOLD` (constant), lines 436-436, exports `READ_FILE_LOOP_THRESHOLD`
- order 218: `READ_FILE_LOOP_DISTINCT_SOFT_LIMIT` (constant), lines 437-437, exports `READ_FILE_LOOP_DISTINCT_SOFT_LIMIT`
- order 219: `READ_FILE_COMPACT_PIN_DISTINCT` (constant), lines 438-438, exports `READ_FILE_COMPACT_PIN_DISTINCT`
- order 220: `READ_FILE_COMPACT_PIN_MAX_CHARS` (constant), lines 439-439, exports `READ_FILE_COMPACT_PIN_MAX_CHARS`
- order 221: `READ_CONTEXT_REGISTRY_MAX` (constant), lines 440-440, exports `READ_CONTEXT_REGISTRY_MAX`
- order 222: `READ_CONTEXT_PROMPT_MAX_ITEMS` (constant), lines 441-441, exports `READ_CONTEXT_PROMPT_MAX_ITEMS`
- order 223: `READ_CONTEXT_PROMPT_MAX_CHARS` (constant), lines 442-442, exports `READ_CONTEXT_PROMPT_MAX_CHARS`
- order 224: `READ_CONTEXT_SUMMARY_MAX_CHARS` (constant), lines 443-443, exports `READ_CONTEXT_SUMMARY_MAX_CHARS`
- order 225: `READ_CONTEXT_SHARED_MAX_ITEMS` (constant), lines 444-444, exports `READ_CONTEXT_SHARED_MAX_ITEMS`
- order 226: `READ_CONTEXT_POLICY_CHOICES` (constant), lines 445-445, exports `READ_CONTEXT_POLICY_CHOICES`
- order 227: `DEFAULT_READ_CONTEXT_POLICY` (constant), lines 446-446, exports `DEFAULT_READ_CONTEXT_POLICY`
- order 228: `TOOL_MEMORY_REGISTRY_MAX` (constant), lines 447-447, exports `TOOL_MEMORY_REGISTRY_MAX`
- order 229: `TOOL_MEMORY_PROMPT_MAX_ITEMS` (constant), lines 448-448, exports `TOOL_MEMORY_PROMPT_MAX_ITEMS`
- order 230: `TOOL_MEMORY_PROMPT_MAX_CHARS` (constant), lines 449-449, exports `TOOL_MEMORY_PROMPT_MAX_CHARS`
- order 231: `TOOL_MEMORY_SUMMARY_MAX_CHARS` (constant), lines 450-450, exports `TOOL_MEMORY_SUMMARY_MAX_CHARS`
- order 232: `TOOL_MEMORY_SHARED_MAX_ITEMS` (constant), lines 451-451, exports `TOOL_MEMORY_SHARED_MAX_ITEMS`
- order 233: `TOOL_MEMORY_COMPACT_PIN_DISTINCT` (constant), lines 452-452, exports `TOOL_MEMORY_COMPACT_PIN_DISTINCT`
- order 234: `TOOL_MEMORY_COMPACT_PIN_MAX_CHARS` (constant), lines 453-453, exports `TOOL_MEMORY_COMPACT_PIN_MAX_CHARS`
- order 235: `TOOL_MEMORY_POLICY_CHOICES` (constant), lines 454-454, exports `TOOL_MEMORY_POLICY_CHOICES`
- order 236: `DEFAULT_TOOL_MEMORY_POLICY` (constant), lines 455-455, exports `DEFAULT_TOOL_MEMORY_POLICY`
- order 237: `DEFAULT_AUTO_TASK_LEVEL_CEILING` (constant), lines 456-456, exports `DEFAULT_AUTO_TASK_LEVEL_CEILING`
- order 238: `HARD_BREAK_TOOL_ERROR_THRESHOLD` (constant), lines 457-457, exports `HARD_BREAK_TOOL_ERROR_THRESHOLD`
- order 239: `HARD_BREAK_RECOVERY_ROUND_THRESHOLD` (constant), lines 458-458, exports `HARD_BREAK_RECOVERY_ROUND_THRESHOLD`
- order 240: `FUSED_FAULT_BREAK_THRESHOLD` (constant), lines 459-459, exports `FUSED_FAULT_BREAK_THRESHOLD`
- order 241: `STALL_SEVERITY_ESCALATION_THRESHOLD` (constant), lines 460-460, exports `STALL_SEVERITY_ESCALATION_THRESHOLD`
- order 242: `STALL_SEVERITY_WEIGHT_BASH_READ_LOOP` (constant), lines 461-461, exports `STALL_SEVERITY_WEIGHT_BASH_READ_LOOP`
- order 243: `STALL_SEVERITY_WEIGHT_REPEATED_TOOL` (constant), lines 462-462, exports `STALL_SEVERITY_WEIGHT_REPEATED_TOOL`
- order 244: `STALL_SEVERITY_WEIGHT_FAULT` (constant), lines 463-463, exports `STALL_SEVERITY_WEIGHT_FAULT`
- order 245: `STALL_SEVERITY_WEIGHT_RECOVERY_RETRY` (constant), lines 464-464, exports `STALL_SEVERITY_WEIGHT_RECOVERY_RETRY`
- order 246: `STALL_SEVERITY_WEIGHT_WATCHDOG` (constant), lines 465-465, exports `STALL_SEVERITY_WEIGHT_WATCHDOG`
- order 247: `STALL_SEVERITY_DECAY_ON_SUCCESS` (constant), lines 466-466, exports `STALL_SEVERITY_DECAY_ON_SUCCESS`
- order 248: `STALL_ESCALATION_MIN_LEVEL` (constant), lines 467-467, exports `STALL_ESCALATION_MIN_LEVEL`
- order 249: `STALL_PLAN_SYNTHESIS_MAX_TOKENS` (constant), lines 468-468, exports `STALL_PLAN_SYNTHESIS_MAX_TOKENS`
- order 250: `STALL_ESCALATION_CONTEXT_MAX_CHARS` (constant), lines 469-469, exports `STALL_ESCALATION_CONTEXT_MAX_CHARS`
- order 251: `MAX_RUN_SECONDS` (constant), lines 470-470, exports `MAX_RUN_SECONDS`
- order 252: `MIN_RUN_TIMEOUT_SECONDS` (constant), lines 471-471, exports `MIN_RUN_TIMEOUT_SECONDS`
- order 253: `MAX_RUN_TIMEOUT_SECONDS` (constant), lines 472-472, exports `MAX_RUN_TIMEOUT_SECONDS`
- order 254: `MIN_TIMEOUT_SECONDS` (constant), lines 473-473, exports `MIN_TIMEOUT_SECONDS`
- order 255: `MAX_TIMEOUT_SECONDS` (constant), lines 474-474, exports `MAX_TIMEOUT_SECONDS`
- order 256: `DEFAULT_TIMEOUT_SECONDS` (constant), lines 475-481, exports `DEFAULT_TIMEOUT_SECONDS`
- order 257: `DEFAULT_REQUEST_TIMEOUT` (constant), lines 482-482, exports `DEFAULT_REQUEST_TIMEOUT`
- order 258: `_SHELL_AUTO_CONFIRM_PATTERNS` (assignment), lines 483-498, exports `_SHELL_AUTO_CONFIRM_PATTERNS`
- order 259: `MIN_SHELL_COMMAND_TIMEOUT_SECONDS` (constant), lines 499-499, exports `MIN_SHELL_COMMAND_TIMEOUT_SECONDS`
- order 260: `MAX_SHELL_COMMAND_TIMEOUT_SECONDS` (constant), lines 500-500, exports `MAX_SHELL_COMMAND_TIMEOUT_SECONDS`
- order 261: `DEFAULT_SHELL_COMMAND_TIMEOUT_SECONDS` (constant), lines 501-515, exports `DEFAULT_SHELL_COMMAND_TIMEOUT_SECONDS`
- order 262: `DEFAULT_SINGLE_NO_PLAN_TODO_PROMPT` (constant), lines 516-528, exports `DEFAULT_SINGLE_NO_PLAN_TODO_PROMPT`
- order 263: `SINGLE_NO_PLAN_TODO_BOOTSTRAP_MAX_ATTEMPTS` (constant), lines 529-529, exports `SINGLE_NO_PLAN_TODO_BOOTSTRAP_MAX_ATTEMPTS`
- order 264: `AUTO_CONTINUE_BUDGET_DEFAULT` (constant), lines 530-530, exports `AUTO_CONTINUE_BUDGET_DEFAULT`
- order 265: `AGENT_MAX_OUTPUT_TOKENS` (constant), lines 531-531, exports `AGENT_MAX_OUTPUT_TOKENS`
- order 266: `OLLAMA_THINKING_TOOL_BUFFER` (constant), lines 532-532, exports `OLLAMA_THINKING_TOOL_BUFFER`
- order 267: `WATCHDOG_INTENT_NO_TOOL_THRESHOLD` (constant), lines 533-533, exports `WATCHDOG_INTENT_NO_TOOL_THRESHOLD`
- order 268: `WATCHDOG_REPEAT_NO_TOOL_THRESHOLD` (constant), lines 534-534, exports `WATCHDOG_REPEAT_NO_TOOL_THRESHOLD`
- order 269: `WATCHDOG_INTENT_NO_TOOL_THRESHOLD_SINGLE` (constant), lines 535-535, exports `WATCHDOG_INTENT_NO_TOOL_THRESHOLD_SINGLE`
- order 270: `WATCHDOG_REPEAT_NO_TOOL_THRESHOLD_SINGLE` (constant), lines 536-536, exports `WATCHDOG_REPEAT_NO_TOOL_THRESHOLD_SINGLE`
- order 271: `WATCHDOG_STATE_STALL_THRESHOLD` (constant), lines 537-537, exports `WATCHDOG_STATE_STALL_THRESHOLD`
- order 272: `WATCHDOG_CONTEXT_STALL_THRESHOLD` (constant), lines 538-538, exports `WATCHDOG_CONTEXT_STALL_THRESHOLD`
- order 273: `WATCHDOG_REPEAT_SIMILARITY_THRESHOLD` (constant), lines 539-539, exports `WATCHDOG_REPEAT_SIMILARITY_THRESHOLD`
- order 274: `WATCHDOG_CONTEXT_NEAR_RATIO` (constant), lines 540-540, exports `WATCHDOG_CONTEXT_NEAR_RATIO`
- order 275: `WATCHDOG_MAX_DECOMPOSE_STEPS` (constant), lines 541-541, exports `WATCHDOG_MAX_DECOMPOSE_STEPS`
- order 276: `WATCHDOG_STEP_MAX_ATTEMPTS` (constant), lines 542-542, exports `WATCHDOG_STEP_MAX_ATTEMPTS`
- order 277: `EMPTY_ACTION_MIN_CONTENT_CHARS` (constant), lines 543-543, exports `EMPTY_ACTION_MIN_CONTENT_CHARS`
- order 278: `EMPTY_ACTION_WAKEUP_RETRY_LIMIT` (constant), lines 544-544, exports `EMPTY_ACTION_WAKEUP_RETRY_LIMIT`
- order 279: `THINKING_BUDGET_FORCE_RATIO` (constant), lines 545-545, exports `THINKING_BUDGET_FORCE_RATIO`
- order 280: `_TOOL_TIMEOUT_MAP` (assignment), lines 546-564, exports `_TOOL_TIMEOUT_MAP`
- order 281: `_DEFAULT_TOOL_TIMEOUT` (assignment), lines 565-565, exports `_DEFAULT_TOOL_TIMEOUT`
- order 282: `CONVERSATION_VISIBLE_TOOL_EVENTS` (constant), lines 566-576, exports `CONVERSATION_VISIBLE_TOOL_EVENTS`
- order 283: `PERSIST_ON_EVENT_TYPES` (constant), lines 577-591, exports `PERSIST_ON_EVENT_TYPES`
- order 284: `PERSIST_EVENT_MIN_INTERVAL_SECONDS` (constant), lines 592-592, exports `PERSIST_EVENT_MIN_INTERVAL_SECONDS`
- order 285: `TRUNCATION_CONTINUATION_MAX_PASSES` (constant), lines 593-593, exports `TRUNCATION_CONTINUATION_MAX_PASSES`
- order 286: `TRUNCATION_CONTINUATION_MAX_TOKENS` (constant), lines 594-594, exports `TRUNCATION_CONTINUATION_MAX_TOKENS`
- order 287: `TRUNCATION_CONTINUATION_TAIL_CHARS` (constant), lines 595-595, exports `TRUNCATION_CONTINUATION_TAIL_CHARS`
- order 288: `TRUNCATION_CONTINUATION_ECHO_CHARS` (constant), lines 596-596, exports `TRUNCATION_CONTINUATION_ECHO_CHARS`
- order 289: `TRUNCATION_OVERLAP_SCAN_CHARS` (constant), lines 597-597, exports `TRUNCATION_OVERLAP_SCAN_CHARS`
- order 290: `TRUNCATION_PAIR_SCAN_CHARS` (constant), lines 598-598, exports `TRUNCATION_PAIR_SCAN_CHARS`
- order 291: `TRUNCATION_LIVE_BUFFER_MAX_CHARS` (constant), lines 599-599, exports `TRUNCATION_LIVE_BUFFER_MAX_CHARS`
- order 292: `MIN_CONTEXT_TOKEN_LIMIT` (constant), lines 600-600, exports `MIN_CONTEXT_TOKEN_LIMIT`
- order 293: `COMPACT_TIER1_PCT` (constant), lines 601-602, exports `COMPACT_TIER1_PCT`
- order 294: `COMPACT_TIER2_PCT` (constant), lines 603-603, exports `COMPACT_TIER2_PCT`
- order 295: `COMPACT_TIER3_PCT` (constant), lines 604-604, exports `COMPACT_TIER3_PCT`
- order 296: `COMPACT_TIER1_ABS` (constant), lines 605-606, exports `COMPACT_TIER1_ABS`
- order 297: `COMPACT_TIER2_ABS` (constant), lines 607-607, exports `COMPACT_TIER2_ABS`
- order 298: `CONTEXT_COMPACT_INEFFECTIVE_COOLDOWN_SECONDS` (constant), lines 608-614, exports `CONTEXT_COMPACT_INEFFECTIVE_COOLDOWN_SECONDS`
- order 299: `FILE_BUFFER_CONTENT_THRESHOLD` (constant), lines 615-616, exports `FILE_BUFFER_CONTENT_THRESHOLD`
- order 300: `FILE_BUFFER_MAX_FILES` (constant), lines 617-617, exports `FILE_BUFFER_MAX_FILES`
- order 301: `AGENT_MSG_LIMIT_TIER0` (constant), lines 618-619, exports `AGENT_MSG_LIMIT_TIER0`
- order 302: `AGENT_MSG_LIMIT_TIER1` (constant), lines 620-620, exports `AGENT_MSG_LIMIT_TIER1`
- order 303: `AGENT_MSG_LIMIT_TIER2` (constant), lines 621-621, exports `AGENT_MSG_LIMIT_TIER2`
- order 304: `AGENT_MSG_LIMIT_TIER3` (constant), lines 622-622, exports `AGENT_MSG_LIMIT_TIER3`
- order 305: `AGENT_CTX_LIMIT_TIER0` (constant), lines 623-623, exports `AGENT_CTX_LIMIT_TIER0`
- order 306: `AGENT_CTX_LIMIT_TIER1` (constant), lines 624-624, exports `AGENT_CTX_LIMIT_TIER1`
- order 307: `AGENT_CTX_LIMIT_TIER2` (constant), lines 625-625, exports `AGENT_CTX_LIMIT_TIER2`
- order 308: `AGENT_CTX_LIMIT_TIER3` (constant), lines 626-626, exports `AGENT_CTX_LIMIT_TIER3`
- order 309: `MANAGER_CTX_LIMIT_TIER0` (constant), lines 627-627, exports `MANAGER_CTX_LIMIT_TIER0`
- order 310: `MANAGER_CTX_LIMIT_TIER1` (constant), lines 628-628, exports `MANAGER_CTX_LIMIT_TIER1`
- order 311: `MANAGER_CTX_LIMIT_TIER2` (constant), lines 629-629, exports `MANAGER_CTX_LIMIT_TIER2`
- order 312: `MANAGER_CTX_LIMIT_TIER3` (constant), lines 630-630, exports `MANAGER_CTX_LIMIT_TIER3`
- order 313: `MAX_CONTEXT_ARCHIVE_SEGMENTS` (constant), lines 631-631, exports `MAX_CONTEXT_ARCHIVE_SEGMENTS`
- order 314: `MAX_USER_BUBBLE_LOG` (constant), lines 632-633, exports `MAX_USER_BUBBLE_LOG`
- order 315: `MANAGER_INSTRUCTION_MAX_CHARS` (constant), lines 634-638, exports `MANAGER_INSTRUCTION_MAX_CHARS`
- order 316: `MANAGER_MOMENTUM_MAX_SKIPS` (constant), lines 639-644, exports `MANAGER_MOMENTUM_MAX_SKIPS`
- order 317: `EXPLORER_CODING_CAP` (constant), lines 645-649, exports `EXPLORER_CODING_CAP`
- order 318: `MODEL_OUTPUT_RETRY_TIMES` (constant), lines 650-650, exports `MODEL_OUTPUT_RETRY_TIMES`
- order 319: `ARBITER_TRIGGER_MIN_CONTENT_CHARS` (constant), lines 651-651, exports `ARBITER_TRIGGER_MIN_CONTENT_CHARS`
- order 320: `ARBITER_VALID_PLANNING_STREAK_LIMIT` (constant), lines 652-652, exports `ARBITER_VALID_PLANNING_STREAK_LIMIT`
- order 321: `ARBITER_DEFAULT_TIMEOUT_SECONDS` (constant), lines 653-653, exports `ARBITER_DEFAULT_TIMEOUT_SECONDS`
- order 322: `ARBITER_DEFAULT_MAX_TOKENS` (constant), lines 654-654, exports `ARBITER_DEFAULT_MAX_TOKENS`
- order 323: `ARBITER_DEFAULT_TEMPERATURE` (constant), lines 655-655, exports `ARBITER_DEFAULT_TEMPERATURE`
- order 324: `LIVE_INPUT_DELAY_WRITE_ROUNDS` (constant), lines 656-656, exports `LIVE_INPUT_DELAY_WRITE_ROUNDS`
- order 325: `LIVE_INPUT_DELAY_TOOL_ROUNDS` (constant), lines 657-657, exports `LIVE_INPUT_DELAY_TOOL_ROUNDS`
- order 326: `LIVE_INPUT_DELAY_NORMAL_ROUNDS` (constant), lines 658-658, exports `LIVE_INPUT_DELAY_NORMAL_ROUNDS`
- order 327: `LIVE_INPUT_MAX_INJECTIONS` (constant), lines 659-659, exports `LIVE_INPUT_MAX_INJECTIONS`
- order 328: `LIVE_INPUT_REINJECT_INTERVAL` (constant), lines 660-660, exports `LIVE_INPUT_REINJECT_INTERVAL`
- order 329: `LIVE_INPUT_WEIGHT_BASE_DELAYED` (constant), lines 661-661, exports `LIVE_INPUT_WEIGHT_BASE_DELAYED`
- order 330: `LIVE_INPUT_WEIGHT_BASE_NORMAL` (constant), lines 662-662, exports `LIVE_INPUT_WEIGHT_BASE_NORMAL`
- order 331: `LIVE_INPUT_WEIGHT_STEP_DELAYED` (constant), lines 663-663, exports `LIVE_INPUT_WEIGHT_STEP_DELAYED`
- order 332: `LIVE_INPUT_WEIGHT_STEP_NORMAL` (constant), lines 664-664, exports `LIVE_INPUT_WEIGHT_STEP_NORMAL`
- order 334: `BENIGN_SOCKET_DEBUG_LOG_ENABLED` (constant), lines 671-677, exports `BENIGN_SOCKET_DEBUG_LOG_ENABLED`
- order 335: `BENIGN_SOCKET_LOG_INTERVAL_SECONDS` (constant), lines 678-678, exports `BENIGN_SOCKET_LOG_INTERVAL_SECONDS`
- order 336: `FINAL_SUMMARY_MIN_CHARS` (constant), lines 679-679, exports `FINAL_SUMMARY_MIN_CHARS`
- order 337: `FINAL_SUMMARY_STRICT_MIN_CHARS` (constant), lines 680-680, exports `FINAL_SUMMARY_STRICT_MIN_CHARS`
- order 338: `RUNTIME_CONTROL_HINT_PREFIXES` (constant), lines 681-700, exports `RUNTIME_CONTROL_HINT_PREFIXES`
- order 339: `RETRY_RUNTIME_HINT_PREFIXES` (constant), lines 701-715, exports `RETRY_RUNTIME_HINT_PREFIXES`
- order 340: `EXECUTION_MODE_SINGLE` (constant), lines 716-716, exports `EXECUTION_MODE_SINGLE`
- order 341: `EXECUTION_MODE_SEQUENTIAL` (constant), lines 717-717, exports `EXECUTION_MODE_SEQUENTIAL`
- order 342: `EXECUTION_MODE_SYNC` (constant), lines 718-718, exports `EXECUTION_MODE_SYNC`
- order 343: `EXECUTION_MODE_CHOICES` (constant), lines 719-723, exports `EXECUTION_MODE_CHOICES`
- order 344: `AGENT_ROLES` (constant), lines 724-724, exports `AGENT_ROLES`
- order 345: `AGENT_BUBBLE_ROLES` (constant), lines 725-725, exports `AGENT_BUBBLE_ROLES`
- order 346: `AGENT_ROLE_LABELS` (constant), lines 726-732, exports `AGENT_ROLE_LABELS`
- order 347: `AGENT_ROLE_BUBBLE_COLORS` (constant), lines 733-739, exports `AGENT_ROLE_BUBBLE_COLORS`
- order 348: `BLACKBOARD_STATUSES` (constant), lines 740-749, exports `BLACKBOARD_STATUSES`
- order 349: `TASK_COMPLEXITY_LEVELS` (constant), lines 750-750, exports `TASK_COMPLEXITY_LEVELS`
- order 350: `TASK_COMPLEXITY_RANKS` (constant), lines 751-756, exports `TASK_COMPLEXITY_RANKS`
- order 351: `TASK_PROFILE_TYPES` (constant), lines 757-763, exports `TASK_PROFILE_TYPES`
- order 352: `TASK_LEVEL_CHOICES` (constant), lines 764-764, exports `TASK_LEVEL_CHOICES`
- order 353: `TASK_SCALE_PREFERENCES` (constant), lines 765-765, exports `TASK_SCALE_PREFERENCES`
- order 354: `SEMANTIC_CONFIDENCE_CHOICES` (constant), lines 766-766, exports `SEMANTIC_CONFIDENCE_CHOICES`
- order 355: `L2_TODO_POLICY_CHOICES` (constant), lines 767-771, exports `L2_TODO_POLICY_CHOICES`
- order 356: `DEFAULT_L2_TODO_POLICY` (constant), lines 772-772, exports `DEFAULT_L2_TODO_POLICY`
- order 357: `TASK_LEVEL_POLICIES` (constant), lines 773-826, exports `TASK_LEVEL_POLICIES`
- order 358: `MANAGER_ROUTE_TARGETS` (constant), lines 827-827, exports `MANAGER_ROUTE_TARGETS`
- order 359: `BLACKBOARD_MAX_LOG_ENTRIES` (constant), lines 828-828, exports `BLACKBOARD_MAX_LOG_ENTRIES`
- order 360: `BLACKBOARD_MAX_TEXT` (constant), lines 829-829, exports `BLACKBOARD_MAX_TEXT`
- order 361: `BLACKBOARD_MEMORY_SHORT_MAX` (constant), lines 830-830, exports `BLACKBOARD_MEMORY_SHORT_MAX`
- order 362: `BLACKBOARD_MEMORY_MID_MAX_STEPS` (constant), lines 831-831, exports `BLACKBOARD_MEMORY_MID_MAX_STEPS`
- order 363: `BLACKBOARD_MEMORY_MID_ITEMS_PER_STEP` (constant), lines 832-832, exports `BLACKBOARD_MEMORY_MID_ITEMS_PER_STEP`
- order 364: `BLACKBOARD_MEMORY_LONG_MAX` (constant), lines 833-833, exports `BLACKBOARD_MEMORY_LONG_MAX`
- order 365: `BLACKBOARD_MEMORY_INDEX_MAX` (constant), lines 834-834, exports `BLACKBOARD_MEMORY_INDEX_MAX`
- order 366: `SKILL_REFRESH_MIN_INTERVAL_SECONDS` (constant), lines 835-835, exports `SKILL_REFRESH_MIN_INTERVAL_SECONDS`
- order 367: `SKILL_PROMPT_MAX_ITEMS` (constant), lines 836-836, exports `SKILL_PROMPT_MAX_ITEMS`
- order 368: `SKILL_PROMPT_MAX_CHARS` (constant), lines 837-837, exports `SKILL_PROMPT_MAX_CHARS`
- order 369: `SKILL_RUNTIME_CACHE_MAX_ENTRIES` (constant), lines 838-838, exports `SKILL_RUNTIME_CACHE_MAX_ENTRIES`
- order 370: `SKILL_RUNTIME_CACHE_MAX_BYTES` (constant), lines 839-839, exports `SKILL_RUNTIME_CACHE_MAX_BYTES`
- order 371: `AUTO_SKILLS_ROOT_CANDIDATES` (constant), lines 840-840, exports `AUTO_SKILLS_ROOT_CANDIDATES`
- order 372: `SKILL_DEFAULT_ATTACHMENT_GLOBS` (constant), lines 841-871, exports `SKILL_DEFAULT_ATTACHMENT_GLOBS`
- order 373: `SKILL_INLINE_ATTACHMENT_MAX_FILES` (constant), lines 872-872, exports `SKILL_INLINE_ATTACHMENT_MAX_FILES`
- order 374: `SKILL_INLINE_ATTACHMENT_MAX_CHARS` (constant), lines 873-873, exports `SKILL_INLINE_ATTACHMENT_MAX_CHARS`
- order 375: `SKILL_RESOURCE_MANIFEST_MAX_ITEMS` (constant), lines 874-874, exports `SKILL_RESOURCE_MANIFEST_MAX_ITEMS`
- order 376: `SKILL_BODY_COMPACT_THRESHOLD_CHARS` (constant), lines 875-875, exports `SKILL_BODY_COMPACT_THRESHOLD_CHARS`
- order 377: `SKILL_BODY_PREVIEW_CHARS` (constant), lines 876-876, exports `SKILL_BODY_PREVIEW_CHARS`
- order 378: `SKILLS_VIRTUAL_PREFIX` (constant), lines 877-877, exports `SKILLS_VIRTUAL_PREFIX`
- order 379: `SKILLS_EXTERNAL_MOUNT` (constant), lines 878-878, exports `SKILLS_EXTERNAL_MOUNT`
- order 380: `PLAN_MODE_ENABLED_LEVELS` (constant), lines 879-879, exports `PLAN_MODE_ENABLED_LEVELS`
- order 381: `PLAN_MODE_FORCED_LEVELS` (constant), lines 880-880, exports `PLAN_MODE_FORCED_LEVELS`
- order 382: `PLAN_MODE_USER_CHOICES` (constant), lines 881-881, exports `PLAN_MODE_USER_CHOICES`
- order 383: `TASK_PHASES` (constant), lines 882-883, exports `TASK_PHASES`
- order 384: `TASK_PHASE_ROUTING` (constant), lines 884-891, exports `TASK_PHASE_ROUTING`
- order 385: `COMPLEXITY_KEYWORDS` (constant), lines 892-898, exports `COMPLEXITY_KEYWORDS`
- order 386: `USER_COMPLEXITY_SIMPLE_TOKENS` (constant), lines 899-903, exports `USER_COMPLEXITY_SIMPLE_TOKENS`
- order 387: `USER_COMPLEXITY_MODERATE_TOKENS` (constant), lines 904-908, exports `USER_COMPLEXITY_MODERATE_TOKENS`
- order 388: `USER_COMPLEXITY_COMPLEX_TOKENS` (constant), lines 909-913, exports `USER_COMPLEXITY_COMPLEX_TOKENS`
- order 389: `USER_COMPLEXITY_EXPERT_TOKENS` (constant), lines 914-918, exports `USER_COMPLEXITY_EXPERT_TOKENS`
- order 390: `PLAN_MODE_EXPLORER_MAX_ROUNDS` (constant), lines 919-922, exports `PLAN_MODE_EXPLORER_MAX_ROUNDS`
- order 391: `PLAN_MODE_EXPLORER_PRODUCTIVE_ROUNDS` (constant), lines 923-923, exports `PLAN_MODE_EXPLORER_PRODUCTIVE_ROUNDS`
- order 392: `PLAN_MODE_EXPLORER_STALE_ROUNDS` (constant), lines 924-924, exports `PLAN_MODE_EXPLORER_STALE_ROUNDS`
- order 393: `PLAN_MODE_SYNTHESIS_MAX_ATTEMPTS` (constant), lines 925-925, exports `PLAN_MODE_SYNTHESIS_MAX_ATTEMPTS`
- order 394: `REVIEWER_DEBUG_MODE_MAX_ROUNDS` (constant), lines 926-927, exports `REVIEWER_DEBUG_MODE_MAX_ROUNDS`
- order 395: `REVIEWER_DEBUG_TOOL_ALLOWLIST` (constant), lines 928-932, exports `REVIEWER_DEBUG_TOOL_ALLOWLIST`
- order 396: `EXPLORER_STALL_THRESHOLD` (constant), lines 933-933, exports `EXPLORER_STALL_THRESHOLD`
- order 397: `DEVELOPER_EDIT_STALL_THRESHOLD` (constant), lines 934-934, exports `DEVELOPER_EDIT_STALL_THRESHOLD`
- order 398: `ACCEPTANCE_GATE_STALL_THRESHOLD` (constant), lines 935-938, exports `ACCEPTANCE_GATE_STALL_THRESHOLD`
- order 399: `ACCEPTANCE_GATE_HARD_CEILING` (constant), lines 939-942, exports `ACCEPTANCE_GATE_HARD_CEILING`
- order 400: `ACCEPTANCE_GATE_TOTAL_ROUND_CEILING` (constant), lines 943-943, exports `ACCEPTANCE_GATE_TOTAL_ROUND_CEILING`
- order 401: `PLAN_MODE_MANAGER_SYNTHESIS_MAX_TOKENS` (constant), lines 944-944, exports `PLAN_MODE_MANAGER_SYNTHESIS_MAX_TOKENS`
- order 402: `PLAN_MODE_MAX_OPTIONS` (constant), lines 945-945, exports `PLAN_MODE_MAX_OPTIONS`
- order 403: `PLAN_FILE_RELATIVE_PATH` (constant), lines 946-946, exports `PLAN_FILE_RELATIVE_PATH`
- order 404: `PLAN_BUBBLE_MAX_CHARS` (constant), lines 947-947, exports `PLAN_BUBBLE_MAX_CHARS`
- order 405: `PLAN_NOTICE_BODY_MAX_CHARS` (constant), lines 948-948, exports `PLAN_NOTICE_BODY_MAX_CHARS`
- order 406: `PLAN_MESSAGE_EVENT_MAX_CHARS` (constant), lines 949-949, exports `PLAN_MESSAGE_EVENT_MAX_CHARS`
- order 407: `PLAN_STEP_FULL_CONTENT_MAX_CHARS` (constant), lines 950-950, exports `PLAN_STEP_FULL_CONTENT_MAX_CHARS`
- order 408: `PLAN_MODE_RESEARCH_TOOL_ALLOWLIST` (constant), lines 951-958, exports `PLAN_MODE_RESEARCH_TOOL_ALLOWLIST`
- order 409: `FAILURE_LEDGER_MAX_FIXES` (constant), lines 959-959, exports `FAILURE_LEDGER_MAX_FIXES`
- order 410: `FAILURE_LEDGER_MAX_COMPILE_ERRORS` (constant), lines 960-960, exports `FAILURE_LEDGER_MAX_COMPILE_ERRORS`
- order 411: `FAILURE_LEDGER_MAX_DELEGATIONS` (constant), lines 961-961, exports `FAILURE_LEDGER_MAX_DELEGATIONS`
- order 412: `FAILURE_LEDGER_MAX_STALLS` (constant), lines 962-962, exports `FAILURE_LEDGER_MAX_STALLS`
- order 413: `FAILURE_LEDGER_MAX_TOOL_FPS` (constant), lines 963-963, exports `FAILURE_LEDGER_MAX_TOOL_FPS`
- order 414: `FAILURE_LEDGER_MAX_ERRORS` (constant), lines 964-964, exports `FAILURE_LEDGER_MAX_ERRORS`
- order 415: `ERROR_CATEGORY_DEFS` (constant), lines 965-1004, exports `ERROR_CATEGORY_DEFS`
- order 416: `CHECKPOINT_MAX_COUNT` (constant), lines 1005-1005, exports `CHECKPOINT_MAX_COUNT`
- order 417: `CHECKPOINT_INTERVAL_ROUNDS` (constant), lines 1006-1006, exports `CHECKPOINT_INTERVAL_ROUNDS`
- order 418: `PERSISTED_ROUTES_MAX` (constant), lines 1007-1007, exports `PERSISTED_ROUTES_MAX`
- order 419: `HTML_FRONTEND_REQUEST_KEYWORDS` (constant), lines 1008-1047, exports `HTML_FRONTEND_REQUEST_KEYWORDS`
- order 420: `DEEP_RESEARCH_REQUEST_KEYWORDS` (constant), lines 1048-1070, exports `DEEP_RESEARCH_REQUEST_KEYWORDS`
- order 421: `DEEP_RESEARCH_RETRIEVAL_KEYWORDS` (constant), lines 1071-1090, exports `DEEP_RESEARCH_RETRIEVAL_KEYWORDS`
- order 422: `DEEP_RESEARCH_TEXT_ONLY_HINT_KEYWORDS` (constant), lines 1091-1108, exports `DEEP_RESEARCH_TEXT_ONLY_HINT_KEYWORDS`
- order 423: `DANGEROUS_PATTERNS` (constant), lines 1109-1110, exports `DANGEROUS_PATTERNS`
- order 424: `VALID_MSG_TYPES` (constant), lines 1111-1117, exports `VALID_MSG_TYPES`
- order 425: `SUPPORTED_UI_LANGUAGES` (constant), lines 1118-1124, exports `SUPPORTED_UI_LANGUAGES`
- order 426: `UI_LANGUAGE_LABELS` (constant), lines 1125-1125, exports `UI_LANGUAGE_LABELS`
- order 427: `DEFAULT_UI_LANGUAGE` (constant), lines 1126-1126, exports `DEFAULT_UI_LANGUAGE`
- order 428: `UI_STYLE_CHOICES` (constant), lines 1127-1127, exports `UI_STYLE_CHOICES`
- order 429: `UI_STYLE_LABELS` (constant), lines 1128-1128, exports `UI_STYLE_LABELS`
- order 430: `DEFAULT_UI_STYLE` (constant), lines 1129-1129, exports `DEFAULT_UI_STYLE`
- order 431: `DEFAULT_WEB_UI_DIR` (constant), lines 1130-1130, exports `DEFAULT_WEB_UI_DIR`
- order 432: `DEFAULT_WEB_UI_CONFIG` (constant), lines 1131-1131, exports `DEFAULT_WEB_UI_CONFIG`
- order 433: `WEB_UI_REQUIRED_FILES` (constant), lines 1132-1139, exports `WEB_UI_REQUIRED_FILES`
- order 434: `WEB_UI_OPTIONAL_FILES` (constant), lines 1140-1140, exports `WEB_UI_OPTIONAL_FILES`
- order 435: `WEB_UI_APPLICATION_CONTRACT_VERSION` (constant), lines 1141-1141, exports `WEB_UI_APPLICATION_CONTRACT_VERSION`
- order 436: `WEB_UI_APPLICATION_FEATURE_MARKERS` (constant), lines 1142-1161, exports `WEB_UI_APPLICATION_FEATURE_MARKERS`
- order 437: `IMAGE_EXTS` (constant), lines 1162-1176, exports `IMAGE_EXTS`
- order 438: `IMAGE_FORMATS_NEED_CONVERSION` (constant), lines 1177-1177, exports `IMAGE_FORMATS_NEED_CONVERSION`
- order 439: `IMAGE_SAFE_FORMATS` (constant), lines 1178-1178, exports `IMAGE_SAFE_FORMATS`
- order 440: `AUDIO_EXTS` (constant), lines 1179-1189, exports `AUDIO_EXTS`
- order 441: `VIDEO_EXTS` (constant), lines 1190-1200, exports `VIDEO_EXTS`
- order 442: `CODE_PREVIEW_STAGE_MAX_BYTES` (constant), lines 1201-1201, exports `CODE_PREVIEW_STAGE_MAX_BYTES`
- order 443: `CODE_PREVIEW_STAGE_MAX_ROWS` (constant), lines 1202-1202, exports `CODE_PREVIEW_STAGE_MAX_ROWS`
- order 444: `CODE_PREVIEW_STAGE_MAX_PER_FILE` (constant), lines 1203-1203, exports `CODE_PREVIEW_STAGE_MAX_PER_FILE`
- order 445: `CODE_PREVIEW_STAGE_MAX_TOTAL` (constant), lines 1204-1204, exports `CODE_PREVIEW_STAGE_MAX_TOTAL`
- order 446: `CODE_PREVIEW_DIFF_CONTEXT_LINES` (constant), lines 1205-1205, exports `CODE_PREVIEW_DIFF_CONTEXT_LINES`
- order 447: `CODE_PREVIEW_DIFF_MERGE_GAP` (constant), lines 1206-1206, exports `CODE_PREVIEW_DIFF_MERGE_GAP`
- order 448: `PREVIEW_DOWNLOAD_MAX_FILES` (constant), lines 1207-1207, exports `PREVIEW_DOWNLOAD_MAX_FILES`
- order 449: `PREVIEW_DOWNLOAD_MAX_BYTES` (constant), lines 1208-1208, exports `PREVIEW_DOWNLOAD_MAX_BYTES`
- order 450: `FILES_TREE_DEFAULT_MAX_NODES` (constant), lines 1209-1209, exports `FILES_TREE_DEFAULT_MAX_NODES`
- order 451: `FILES_TREE_DEFAULT_MAX_DEPTH` (constant), lines 1210-1210, exports `FILES_TREE_DEFAULT_MAX_DEPTH`
- order 452: `FILES_TREE_SKIP_DIRS` (constant), lines 1211-1219, exports `FILES_TREE_SKIP_DIRS`
- order 453: `FILES_TREE_SKIP_REL_DIRS` (constant), lines 1220-1222, exports `FILES_TREE_SKIP_REL_DIRS`
- order 454: `IDE_FILE_MAX_BYTES` (constant), lines 1223-1223, exports `IDE_FILE_MAX_BYTES`
- order 455: `IDE_UPLOAD_MAX_BYTES` (constant), lines 1224-1224, exports `IDE_UPLOAD_MAX_BYTES`
- order 456: `IDE_UPLOAD_TOTAL_MAX_BYTES` (constant), lines 1225-1225, exports `IDE_UPLOAD_TOTAL_MAX_BYTES`
- order 457: `IDE_UPLOAD_MAX_ITEMS` (constant), lines 1226-1226, exports `IDE_UPLOAD_MAX_ITEMS`
- order 458: `IDE_COMMAND_TIMEOUT_DEFAULT` (constant), lines 1227-1227, exports `IDE_COMMAND_TIMEOUT_DEFAULT`
- order 459: `IDE_TREE_DEFAULT_MAX_NODES` (constant), lines 1228-1228, exports `IDE_TREE_DEFAULT_MAX_NODES`
- order 460: `IDE_TREE_MAX_NODES` (constant), lines 1229-1229, exports `IDE_TREE_MAX_NODES`
- order 461: `IDE_TREE_SKIP_DIRS` (constant), lines 1230-1238, exports `IDE_TREE_SKIP_DIRS`
- order 462: `RENDER_FRAME_MAX_B64_CHARS` (constant), lines 1239-1239, exports `RENDER_FRAME_MAX_B64_CHARS`
- order 463: `RENDER_FRAME_MAX_POINTS` (constant), lines 1240-1240, exports `RENDER_FRAME_MAX_POINTS`
- order 464: `RENDER_FRAME_MAX_LINES` (constant), lines 1241-1241, exports `RENDER_FRAME_MAX_LINES`
- order 465: `RENDER_FRAME_MAX_LINE_POINTS` (constant), lines 1242-1242, exports `RENDER_FRAME_MAX_LINE_POINTS`
- order 466: `RENDER_FRAME_ACTIVITY_INTERVAL_SECONDS` (constant), lines 1243-1243, exports `RENDER_FRAME_ACTIVITY_INTERVAL_SECONDS`
- order 467: `RAW_TOOLCALL_TEXT_FILTER_THRESHOLD` (constant), lines 1244-1244, exports `RAW_TOOLCALL_TEXT_FILTER_THRESHOLD`
- order 468: `ASSISTANT_TEXT_PERSIST_MAX_CHARS` (constant), lines 1245-1245, exports `ASSISTANT_TEXT_PERSIST_MAX_CHARS`
- order 469: `ASSISTANT_MESSAGE_EVENT_MAX_CHARS` (constant), lines 1246-1246, exports `ASSISTANT_MESSAGE_EVENT_MAX_CHARS`
- order 470: `CODE_PREVIEW_EXTS` (constant), lines 1247-1372, exports `CODE_PREVIEW_EXTS`
- order 471: `CODE_PREVIEW_FILENAMES` (constant), lines 1373-1424, exports `CODE_PREVIEW_FILENAMES`
- order 472: `MEDIA_CAPABILITY_KEYS` (constant), lines 1425-1432, exports `MEDIA_CAPABILITY_KEYS`
- order 473: `SAMPLE_IMAGE_PNG_B64` (constant), lines 1433-1436, exports `SAMPLE_IMAGE_PNG_B64`
- order 474: `SAMPLE_AUDIO_WAV_B64` (constant), lines 1437-1439, exports `SAMPLE_AUDIO_WAV_B64`
- order 475: `SAMPLE_VIDEO_MP4_B64` (constant), lines 1440-1442, exports `SAMPLE_VIDEO_MP4_B64`
- order 476: `OFFLINE_JS_LIB_CATALOG` (constant), lines 1443-1702, exports `OFFLINE_JS_LIB_CATALOG`
- order 477: `OFFLINE_JS_LIB_INDEX_FILE` (constant), lines 1703-1703, exports `OFFLINE_JS_LIB_INDEX_FILE`
- order 478: `OFFLINE_JS_LIB_README_FILE` (constant), lines 1704-1704, exports `OFFLINE_JS_LIB_README_FILE`
- order 487: `BACKEND_I18N` (constant), lines 1888-1959, exports `BACKEND_I18N`
- order 488: `_call_backend_i18n_en_update_1961` (expression), lines 1960-2061, exports —
- order 489: `_call_backend_i18n_zh_cn_update_2062` (expression), lines 2062-2162, exports —
- order 490: `_call_backend_i18n_zh_tw_update_2163` (expression), lines 2163-2263, exports —
- order 491: `_call_backend_i18n_ja_update_2264` (expression), lines 2264-2364, exports —
- order 703: `TABULAR_PREVIEW_EXTS` (constant), lines 9103-9105, exports `TABULAR_PREVIEW_EXTS`
- order 704: `EXCEL_PREVIEW_EXTS` (constant), lines 9106-9106, exports `EXCEL_PREVIEW_EXTS`
- order 705: `PRESENTATION_PREVIEW_EXTS` (constant), lines 9107-9107, exports `PRESENTATION_PREVIEW_EXTS`
- order 706: `DOCUMENT_PREVIEW_EXTS` (constant), lines 9108-9108, exports `DOCUMENT_PREVIEW_EXTS`

### `config/paths.py`

- order 58: `SCRIPT_DIR` (constant), lines 68-68, exports `SCRIPT_DIR`
- order 74: `_resolve_default_agent_workdir` (function), lines 116-121, exports `_resolve_default_agent_workdir`
- order 75: `_migrate_legacy_runtime_roots` (function), lines 122-151, exports `_migrate_legacy_runtime_roots`
- order 76: `WORKDIR` (constant), lines 152-153, exports `WORKDIR`
- order 77: `CODES_ROOT` (constant), lines 154-154, exports `CODES_ROOT`
- order 78: `LLM_CONFIG_PATH` (constant), lines 155-155, exports `LLM_CONFIG_PATH`
- order 559: `detect_repo_root` (function), lines 3630-3645, exports `detect_repo_root`
- order 560: `REPO_ROOT` (constant), lines 3646-3647, exports `REPO_ROOT`

### `config/settings.py`

- order 482: `normalize_ui_language` (function), lines 1786-1810, exports `normalize_ui_language`
- order 483: `normalize_ui_style` (function), lines 1811-1830, exports `normalize_ui_style`
- order 484: `supported_ui_languages_payload` (function), lines 1831-1834, exports `supported_ui_languages_payload`
- order 485: `normalize_execution_mode` (function), lines 1835-1856, exports `normalize_execution_mode`
- order 486: `model_language_instruction` (function), lines 1857-1887, exports `model_language_instruction`
- order 492: `backend_i18n_text` (function), lines 2365-2377, exports `backend_i18n_text`
- order 493: `backend_role_label` (function), lines 2378-2384, exports `backend_role_label`
- order 494: `_detect_os_shell_instruction` (function), lines 2385-2426, exports `_detect_os_shell_instruction`
- order 495: `resolve_web_ui_dir_path` (function), lines 2427-2435, exports `resolve_web_ui_dir_path`
- order 496: `resolve_optional_file_path` (function), lines 2436-2445, exports `resolve_optional_file_path`
- order 497: `resolve_skills_root_path` (function), lines 2446-2455, exports `resolve_skills_root_path`
- order 498: `_count_skill_markdown_files` (function), lines 2456-2469, exports `_count_skill_markdown_files`
- order 499: `select_preferred_skills_root` (function), lines 2470-2506, exports `select_preferred_skills_root`
- order 500: `load_web_ui_config_file` (function), lines 2507-2523, exports `load_web_ui_config_file`
- order 501: `extract_show_upload_list_setting` (function), lines 2524-2540, exports `extract_show_upload_list_setting`
- order 502: `extract_ui_style_setting` (function), lines 2541-2557, exports `extract_ui_style_setting`
- order 503: `extract_js_lib_download_setting` (function), lines 2558-2579, exports `extract_js_lib_download_setting`
- order 504: `extract_daily_session_limit_setting` (function), lines 2580-2625, exports `extract_daily_session_limit_setting`
- order 505: `extract_shell_command_timeout_setting` (function), lines 2626-2674, exports `extract_shell_command_timeout_setting`
- order 506: `extract_context_token_limit_setting` (function), lines 2675-2709, exports `extract_context_token_limit_setting`
- order 507: `normalize_auto_task_level_ceiling` (function), lines 2710-2731, exports `normalize_auto_task_level_ceiling`
- order 508: `normalize_l2_todo_policy` (function), lines 2732-2767, exports `normalize_l2_todo_policy`
- order 509: `extract_l2_todo_policy_setting` (function), lines 2768-2810, exports `extract_l2_todo_policy_setting`
- order 510: `extract_auto_task_level_ceiling_setting` (function), lines 2811-2840, exports `extract_auto_task_level_ceiling_setting`
- order 511: `normalize_read_context_policy` (function), lines 2841-2861, exports `normalize_read_context_policy`
- order 512: `normalize_tool_memory_policy` (function), lines 2862-2865, exports `normalize_tool_memory_policy`
- order 513: `extract_read_context_policy_setting` (function), lines 2866-2889, exports `extract_read_context_policy_setting`
- order 514: `extract_tool_memory_policy_setting` (function), lines 2890-2913, exports `extract_tool_memory_policy_setting`
- order 516: `default_multimodal_capabilities` (function), lines 2920-2930, exports `default_multimodal_capabilities`
- order 517: `_to_bool_like` (function), lines 2931-2943, exports `_to_bool_like`
- order 518: `extract_web_search_enabled_setting` (function), lines 2944-2956, exports `extract_web_search_enabled_setting`
- order 519: `_single_no_plan_todo_setting_sections` (function), lines 2957-2983, exports `_single_no_plan_todo_setting_sections`
- order 520: `_single_no_plan_todo_setting_present` (function), lines 2984-3009, exports `_single_no_plan_todo_setting_present`
- order 521: `extract_single_no_plan_todo_settings` (function), lines 3010-3056, exports `extract_single_no_plan_todo_settings`
- order 522: `normalize_user_memory_mode` (function), lines 3057-3087, exports `normalize_user_memory_mode`
- order 523: `user_memory_enabled_from_mode` (function), lines 3088-3091, exports `user_memory_enabled_from_mode`
- order 524: `extract_user_memory_mode_setting` (function), lines 3092-3131, exports `extract_user_memory_mode_setting`
- order 525: `set_web_search_enabled_on_runtime` (function), lines 3132-3147, exports `set_web_search_enabled_on_runtime`
- order 526: `infer_model_multimodal_capabilities` (function), lines 3148-3194, exports `infer_model_multimodal_capabilities`
- order 527: `parse_capability_overrides` (function), lines 3195-3234, exports `parse_capability_overrides`
- order 528: `merge_multimodal_capabilities` (function), lines 3235-3244, exports `merge_multimodal_capabilities`
- order 529: `parse_media_endpoints` (function), lines 3245-3261, exports `parse_media_endpoints`
- order 545: `extract_runtime_region_hint_setting` (function), lines 3439-3464, exports `extract_runtime_region_hint_setting`
- order 546: `extract_runtime_timezone_hint_setting` (function), lines 3465-3482, exports `extract_runtime_timezone_hint_setting`
- order 547: `runtime_environment_context_snapshot` (function), lines 3483-3532, exports `runtime_environment_context_snapshot`
- order 548: `runtime_environment_context_block` (function), lines 3533-3562, exports `runtime_environment_context_block`
- order 576: `load_offline_js_lib_index` (function), lines 3884-3894, exports `load_offline_js_lib_index`
- order 626: `resolve_ollama_model` (function), lines 6305-6316, exports `resolve_ollama_model`
- order 627: `infer_thinking_model` (function), lines 6317-6320, exports `infer_thinking_model`
- order 638: `extract_base_url` (function), lines 6531-6540, exports `extract_base_url`
- order 640: `infer_user_complexity_value` (function), lines 6552-6569, exports `infer_user_complexity_value`
- order 641: `normalize_task_complexity` (function), lines 6570-6599, exports `normalize_task_complexity`
- order 642: `task_complexity_rank` (function), lines 6600-6602, exports `task_complexity_rank`
- order 643: `task_complexity_at_least` (function), lines 6603-6605, exports `task_complexity_at_least`
- order 644: `max_task_complexity` (function), lines 6606-6616, exports `max_task_complexity`
- order 645: `normalize_openai_compat_provider_name` (function), lines 6617-6633, exports `normalize_openai_compat_provider_name`
- order 665: `resolve_reasoning_payload` (function), lines 6760-6810, exports `resolve_reasoning_payload`
- order 668: `extract_openai_compat_model_ids` (function), lines 6858-6892, exports `extract_openai_compat_model_ids`
- order 671: `load_llm_config_from_source` (function), lines 6925-6960, exports `load_llm_config_from_source`
- order 672: `parse_llm_config_profiles` (function), lines 6961-7591, exports `parse_llm_config_profiles`
- order 673: `looks_like_llm_config` (function), lines 7592-7669, exports `looks_like_llm_config`
- order 677: `parse_front_matter` (function), lines 7830-8018, exports `parse_front_matter`

### `ide/assets.py`

- order 859: `IDE_INDEX_HTML` (constant), lines 92695-92775, exports `IDE_INDEX_HTML`
- order 860: `IDE_CSS` (constant), lines 92776-92843, exports `IDE_CSS`
- order 861: `IDE_JS` (constant), lines 92844-93038, exports `IDE_JS`

### `ide/handler.py`

- order 870: `IdeHandler` (class), lines 101023-101306, exports `IdeHandler`

### `llm/client.py`

- order 765: `OllamaError` (class), lines 16208-16230, exports `OllamaError`
- order 766: `OllamaClient` (class), lines 16231-18525, exports `OllamaClient`

### `llm/constants.py`

- order 56: `DEFAULT_OLLAMA_BASE_URL` (constant), lines 66-66, exports `DEFAULT_OLLAMA_BASE_URL`
- order 57: `DEFAULT_OLLAMA_MODEL` (constant), lines 67-67, exports `DEFAULT_OLLAMA_MODEL`
- order 646: `OPENAI_COMPAT_PROVIDER_NAMES` (constant), lines 6634-6643, exports `OPENAI_COMPAT_PROVIDER_NAMES`
- order 647: `OPENAI_LIKE_PROVIDER_NAMES` (constant), lines 6644-6645, exports `OPENAI_LIKE_PROVIDER_NAMES`
- order 650: `EFFORT_OFF` (constant), lines 6652-6663, exports `EFFORT_OFF`
- order 651: `EFFORT_LOW` (constant), lines 6664-6664, exports `EFFORT_LOW`
- order 652: `EFFORT_MEDIUM` (constant), lines 6665-6665, exports `EFFORT_MEDIUM`
- order 653: `EFFORT_HIGH` (constant), lines 6666-6666, exports `EFFORT_HIGH`
- order 654: `EFFORT_MAX` (constant), lines 6667-6667, exports `EFFORT_MAX`
- order 655: `EFFORT_LEVELS` (constant), lines 6668-6668, exports `EFFORT_LEVELS`
- order 656: `EFFORT_ORDER` (constant), lines 6669-6669, exports `EFFORT_ORDER`
- order 657: `EFFORT_DEFAULT` (constant), lines 6670-6670, exports `EFFORT_DEFAULT`
- order 658: `EFFORT_ANTHROPIC_BUDGET` (constant), lines 6671-6678, exports `EFFORT_ANTHROPIC_BUDGET`
- order 659: `EFFORT_OPENAI_REASONING` (constant), lines 6679-6685, exports `EFFORT_OPENAI_REASONING`
- order 660: `TASK_LEVEL_EFFORT` (constant), lines 6686-6695, exports `TASK_LEVEL_EFFORT`
- order 661: `ROLE_EFFORT_FLOOR` (constant), lines 6696-6701, exports `ROLE_EFFORT_FLOOR`
- order 662: `COORDINATION_EFFORT` (constant), lines 6702-6710, exports `COORDINATION_EFFORT`

### `llm/utils.py`

- order 619: `probe_ollama_environment` (function), lines 6236-6250, exports `probe_ollama_environment`
- order 620: `list_ollama_models` (function), lines 6251-6254, exports `list_ollama_models`
- order 621: `_OLLAMA_TAG_CACHE_LOCK` (assignment), lines 6255-6256, exports `_OLLAMA_TAG_CACHE_LOCK`
- order 622: `_OLLAMA_TAG_CACHE` (assignment), lines 6257-6257, exports `_OLLAMA_TAG_CACHE`
- order 625: `list_ollama_models_cached` (function), lines 6266-6304, exports `list_ollama_models_cached`
- order 628: `split_thinking_content` (function), lines 6321-6365, exports `split_thinking_content`
- order 629: `strip_thinking_content` (function), lines 6366-6368, exports `strip_thinking_content`
- order 630: `check_ollama_model_ready` (function), lines 6369-6394, exports `check_ollama_model_ready`
- order 631: `list_loaded_ollama_models` (function), lines 6395-6409, exports `list_loaded_ollama_models`
- order 632: `wake_ollama_model` (function), lines 6410-6441, exports `wake_ollama_model`
- order 633: `try_pull_ollama_model` (function), lines 6442-6461, exports `try_pull_ollama_model`
- order 634: `ordered_model_candidates` (function), lines 6462-6481, exports `ordered_model_candidates`
- order 635: `pick_working_ollama_model` (function), lines 6482-6499, exports `pick_working_ollama_model`
- order 639: `complete_chat_endpoint` (function), lines 6541-6551, exports `complete_chat_endpoint`
- order 648: `is_openai_compat_provider` (function), lines 6646-6648, exports `is_openai_compat_provider`
- order 649: `is_openai_like_provider` (function), lines 6649-6651, exports `is_openai_like_provider`
- order 663: `clamp_effort` (function), lines 6711-6722, exports `clamp_effort`
- order 664: `model_reasoning_style` (function), lines 6723-6759, exports `model_reasoning_style`
- order 666: `openai_compat_probe_headers` (function), lines 6811-6823, exports `openai_compat_probe_headers`
- order 667: `openai_compat_model_list_urls` (function), lines 6824-6857, exports `openai_compat_model_list_urls`
- order 669: `_is_http_url` (function), lines 6893-6906, exports `_is_http_url`
- order 670: `_resolve_local_path` (function), lines 6907-6924, exports `_resolve_local_path`

### `mcp/constants.py`

- order 96: `MCP_SERVICE_PORT_OFFSET` (constant), lines 173-173, exports `MCP_SERVICE_PORT_OFFSET`
- order 754: `MCP_PROTOCOL_VERSION` (constant), lines 15330-15359, exports `MCP_PROTOCOL_VERSION`
- order 755: `MCP_NAME_RE` (constant), lines 15360-15360, exports `MCP_NAME_RE`
- order 756: `MCP_TOOL_PREFIX` (constant), lines 15361-15361, exports `MCP_TOOL_PREFIX`
- order 757: `_MCP_DEFAULT_HANDSHAKE_TIMEOUT` (assignment), lines 15362-15362, exports `_MCP_DEFAULT_HANDSHAKE_TIMEOUT`
- order 758: `_MCP_DEFAULT_CALL_TIMEOUT` (assignment), lines 15363-15363, exports `_MCP_DEFAULT_CALL_TIMEOUT`
- order 759: `_MCP_MAX_RESULT_CHARS` (assignment), lines 15364-15364, exports `_MCP_MAX_RESULT_CHARS`

### `mcp/driver.py`

- order 760: `mcp_normalize_name` (function), lines 15365-15374, exports `mcp_normalize_name`
- order 761: `mcp_normalize_server_configs` (function), lines 15375-15459, exports `mcp_normalize_server_configs`
- order 762: `mcp_extract_server_configs` (function), lines 15460-15479, exports `mcp_extract_server_configs`
- order 763: `MCPServerProcess` (class), lines 15480-15815, exports `MCPServerProcess`
- order 764: `MCPManager` (class), lines 15816-16207, exports `MCPManager`

### `mcp/service.py`

- order 871: `McpServiceHandler` (class), lines 101307-101470, exports `McpServiceHandler`

### `rag/assets.py`

- order 853: `RAG_ADMIN_INDEX_HTML` (constant), lines 90287-90461, exports `RAG_ADMIN_INDEX_HTML`
- order 854: `RAG_ADMIN_CSS` (constant), lines 90462-90553, exports `RAG_ADMIN_CSS`
- order 855: `RAG_ADMIN_JS` (constant), lines 90554-92645, exports `RAG_ADMIN_JS`
- order 856: `CODE_ADMIN_INDEX_HTML` (constant), lines 92646-92658, exports `CODE_ADMIN_INDEX_HTML`
- order 857: `CODE_ADMIN_CSS` (constant), lines 92659-92689, exports `CODE_ADMIN_CSS`
- order 858: `CODE_ADMIN_JS` (constant), lines 92690-92694, exports `CODE_ADMIN_JS`

### `rag/constants.py`

- order 92: `RAG_LIBRARY_DIRNAME` (constant), lines 169-169, exports `RAG_LIBRARY_DIRNAME`
- order 93: `RAG_ADMIN_PORT_OFFSET` (constant), lines 170-170, exports `RAG_ADMIN_PORT_OFFSET`
- order 94: `CODE_LIBRARY_DIRNAME` (constant), lines 171-171, exports `CODE_LIBRARY_DIRNAME`
- order 99: `WEB_SEARCH_INDEX_DIRNAME` (constant), lines 179-179, exports `WEB_SEARCH_INDEX_DIRNAME`
- order 101: `USER_MEMORY_DIRNAME` (constant), lines 181-181, exports `USER_MEMORY_DIRNAME`
- order 102: `USER_MEMORY_DB_FILENAME` (constant), lines 182-182, exports `USER_MEMORY_DB_FILENAME`
- order 103: `USER_MEMORY_PROFILE_FILENAME` (constant), lines 183-183, exports `USER_MEMORY_PROFILE_FILENAME`
- order 104: `USER_MEMORY_MODE_CHOICES` (constant), lines 184-184, exports `USER_MEMORY_MODE_CHOICES`
- order 106: `USER_MEMORY_WEAK_CAPSULE_CHARS` (constant), lines 186-186, exports `USER_MEMORY_WEAK_CAPSULE_CHARS`
- order 107: `USER_MEMORY_ON_CAPSULE_CHARS` (constant), lines 187-187, exports `USER_MEMORY_ON_CAPSULE_CHARS`
- order 108: `USER_MEMORY_CAPSULE_INJECT_CHARS` (constant), lines 188-191, exports `USER_MEMORY_CAPSULE_INJECT_CHARS`
- order 109: `USER_MEMORY_MAX_SUMMARY_CHARS` (constant), lines 192-192, exports `USER_MEMORY_MAX_SUMMARY_CHARS`
- order 110: `USER_MEMORY_QUERY_LIMIT` (constant), lines 193-193, exports `USER_MEMORY_QUERY_LIMIT`
- order 111: `USER_MEMORY_DECAY_HALFLIFE_DAYS` (constant), lines 194-194, exports `USER_MEMORY_DECAY_HALFLIFE_DAYS`
- order 112: `USER_MEMORY_PROFILE_SCHEMA_VERSION` (constant), lines 195-195, exports `USER_MEMORY_PROFILE_SCHEMA_VERSION`
- order 123: `WEB_SEARCH_CONTEXT_REGISTRY_MAX` (constant), lines 206-206, exports `WEB_SEARCH_CONTEXT_REGISTRY_MAX`
- order 124: `WEB_SEARCH_CONTEXT_PROMPT_MAX_ITEMS` (constant), lines 207-207, exports `WEB_SEARCH_CONTEXT_PROMPT_MAX_ITEMS`
- order 125: `WEB_SEARCH_CONTEXT_PROMPT_MAX_CHARS` (constant), lines 208-208, exports `WEB_SEARCH_CONTEXT_PROMPT_MAX_CHARS`
- order 126: `WEB_SEARCH_CONTEXT_NODE_MAX` (constant), lines 209-209, exports `WEB_SEARCH_CONTEXT_NODE_MAX`
- order 127: `WEB_SEARCH_CONTEXT_URL_MAX` (constant), lines 210-210, exports `WEB_SEARCH_CONTEXT_URL_MAX`
- order 128: `RAG_CHUNK_CHARS` (constant), lines 211-211, exports `RAG_CHUNK_CHARS`
- order 129: `RAG_CHUNK_OVERLAP` (constant), lines 212-212, exports `RAG_CHUNK_OVERLAP`
- order 130: `RAG_MAX_CHUNKS_PER_DOC` (constant), lines 213-215, exports `RAG_MAX_CHUNKS_PER_DOC`
- order 131: `RAG_MAX_DOCUMENT_CHARS` (constant), lines 216-226, exports `RAG_MAX_DOCUMENT_CHARS`
- order 135: `RAG_MAX_QUERY_RESULTS` (constant), lines 230-230, exports `RAG_MAX_QUERY_RESULTS`
- order 136: `RAG_HIGH_RECALL_POOL_MULTIPLIER` (constant), lines 231-231, exports `RAG_HIGH_RECALL_POOL_MULTIPLIER`
- order 137: `RAG_HIGH_RECALL_MIN_POOL` (constant), lines 232-232, exports `RAG_HIGH_RECALL_MIN_POOL`
- order 138: `RAG_RETRIEVAL_MAX_PER_DOC` (constant), lines 233-233, exports `RAG_RETRIEVAL_MAX_PER_DOC`
- order 139: `RAG_BM25_K1` (constant), lines 234-237, exports `RAG_BM25_K1`
- order 140: `RAG_BM25_B` (constant), lines 238-238, exports `RAG_BM25_B`
- order 141: `RAG_BM25_SATURATION` (constant), lines 239-245, exports `RAG_BM25_SATURATION`
- order 142: `RAG_SYMBOL_EXACT_BOOST` (constant), lines 246-249, exports `RAG_SYMBOL_EXACT_BOOST`
- order 143: `RAG_INDEX_SNAPSHOT_FORMAT` (constant), lines 250-253, exports `RAG_INDEX_SNAPSHOT_FORMAT`
- order 144: `RAG_GRAPH_MAX_NODES` (constant), lines 254-254, exports `RAG_GRAPH_MAX_NODES`
- order 145: `RAG_TASK_HISTORY_LIMIT` (constant), lines 255-255, exports `RAG_TASK_HISTORY_LIMIT`
- order 146: `RAG_MODEL_MEDIA_MAX_BYTES` (constant), lines 256-256, exports `RAG_MODEL_MEDIA_MAX_BYTES`
- order 147: `RAG_MAX_IMPORT_FILES` (constant), lines 257-257, exports `RAG_MAX_IMPORT_FILES`
- order 148: `RAG_MAX_IMPORT_BATCH_ITEMS` (constant), lines 258-258, exports `RAG_MAX_IMPORT_BATCH_ITEMS`
- order 149: `RAG_MAX_IMPORT_BATCH_BYTES` (constant), lines 259-259, exports `RAG_MAX_IMPORT_BATCH_BYTES`
- order 150: `RAG_PDF_IMAGE_LIMIT` (constant), lines 260-260, exports `RAG_PDF_IMAGE_LIMIT`
- order 151: `RAG_QUERY_CONTEXT_CHARS` (constant), lines 261-261, exports `RAG_QUERY_CONTEXT_CHARS`
- order 152: `RAG_MAX_GLOBAL_COMMUNITIES` (constant), lines 262-262, exports `RAG_MAX_GLOBAL_COMMUNITIES`
- order 153: `RAG_MAX_COMMUNITY_MAP_SUPPORT` (constant), lines 263-263, exports `RAG_MAX_COMMUNITY_MAP_SUPPORT`
- order 154: `RAG_INCLUDE_FILENAME_ENTITIES_DEFAULT` (constant), lines 264-264, exports `RAG_INCLUDE_FILENAME_ENTITIES_DEFAULT`
- order 155: `RAG_DYNAMIC_NOISE_MIN_DOC_FREQ` (constant), lines 265-265, exports `RAG_DYNAMIC_NOISE_MIN_DOC_FREQ`
- order 156: `RAG_DYNAMIC_NOISE_MIN_COMMUNITY_FREQ` (constant), lines 266-266, exports `RAG_DYNAMIC_NOISE_MIN_COMMUNITY_FREQ`
- order 157: `RAG_DYNAMIC_NOISE_SOFT_DOC_RATIO` (constant), lines 267-267, exports `RAG_DYNAMIC_NOISE_SOFT_DOC_RATIO`
- order 158: `RAG_DYNAMIC_NOISE_HARD_DOC_RATIO` (constant), lines 268-268, exports `RAG_DYNAMIC_NOISE_HARD_DOC_RATIO`
- order 159: `RAG_DYNAMIC_NOISE_SOFT_COMMUNITY_RATIO` (constant), lines 269-269, exports `RAG_DYNAMIC_NOISE_SOFT_COMMUNITY_RATIO`
- order 160: `RAG_DYNAMIC_NOISE_HARD_COMMUNITY_RATIO` (constant), lines 270-270, exports `RAG_DYNAMIC_NOISE_HARD_COMMUNITY_RATIO`
- order 161: `RAG_MIN_SYNTHESIS_SCORE` (constant), lines 271-271, exports `RAG_MIN_SYNTHESIS_SCORE`
- order 162: `RAG_NO_EVIDENCE_THRESHOLD` (constant), lines 272-272, exports `RAG_NO_EVIDENCE_THRESHOLD`
- order 163: `RAG_WEAK_MATCH_SCORE_CAP` (constant), lines 273-273, exports `RAG_WEAK_MATCH_SCORE_CAP`
- order 164: `RAG_SYNTHESIS_MAX_PER_DOC` (constant), lines 274-274, exports `RAG_SYNTHESIS_MAX_PER_DOC`
- order 165: `RAG_WORKFLOW_ACCEPT_SCORE` (constant), lines 275-275, exports `RAG_WORKFLOW_ACCEPT_SCORE`
- order 166: `RAG_NO_EVIDENCE_MESSAGE` (constant), lines 276-276, exports `RAG_NO_EVIDENCE_MESSAGE`
- order 167: `RAG_CONTEXT_BUDGETS` (constant), lines 277-281, exports `RAG_CONTEXT_BUDGETS`
- order 168: `RAG_WEAK_EVIDENCE_MESSAGE` (constant), lines 282-282, exports `RAG_WEAK_EVIDENCE_MESSAGE`
- order 169: `RAG_DENSE_DEFAULT_ENABLED` (constant), lines 283-283, exports `RAG_DENSE_DEFAULT_ENABLED`
- order 170: `RAG_EMBEDDING_MODE_VALUES` (constant), lines 284-284, exports `RAG_EMBEDDING_MODE_VALUES`
- order 171: `RAG_IMPORT_WORKER_COUNT` (constant), lines 285-288, exports `RAG_IMPORT_WORKER_COUNT`
- order 173: `RAG_PARSE_TIMEOUT_SECONDS` (constant), lines 293-296, exports `RAG_PARSE_TIMEOUT_SECONDS`
- order 792: `RAG_TERM_GROUPS` (constant), lines 77678-82311, exports `RAG_TERM_GROUPS`
- order 793: `RAG_RESEARCH_HINTS` (constant), lines 82312-82333, exports `RAG_RESEARCH_HINTS`
- order 794: `RAG_CODE_HINTS` (constant), lines 82334-82344, exports `RAG_CODE_HINTS`
- order 795: `RAG_SHORT_TOKEN_ALLOWLIST` (constant), lines 82345-82360, exports `RAG_SHORT_TOKEN_ALLOWLIST`
- order 796: `RAG_EN_STOPWORDS` (constant), lines 82361-82433, exports `RAG_EN_STOPWORDS`
- order 797: `RAG_ZH_STOPWORDS` (constant), lines 82434-82470, exports `RAG_ZH_STOPWORDS`
- order 798: `RAG_GENERIC_ENTITY_TERMS_EN` (constant), lines 82471-82549, exports `RAG_GENERIC_ENTITY_TERMS_EN`
- order 799: `RAG_GENERIC_ENTITY_TERMS_ZH` (constant), lines 82550-82592, exports `RAG_GENERIC_ENTITY_TERMS_ZH`
- order 800: `RAG_STRUCTURAL_ENTITY_PATTERNS` (constant), lines 82593-82611, exports `RAG_STRUCTURAL_ENTITY_PATTERNS`
- order 825: `CODE_LIBRARY_IGNORED_DIRS` (constant), lines 83356-83365, exports `CODE_LIBRARY_IGNORED_DIRS`
- order 826: `CODE_LIBRARY_LANGUAGE_BY_EXT` (constant), lines 83366-83422, exports `CODE_LIBRARY_LANGUAGE_BY_EXT`
- order 827: `CODE_LIBRARY_SPECIAL_FILENAMES` (constant), lines 83423-83429, exports `CODE_LIBRARY_SPECIAL_FILENAMES`

### `rag/index.py`

- order 830: `_code_module_name` (function), lines 83454-83470, exports `_code_module_name`
- order 831: `_code_choose_community` (function), lines 83471-83480, exports `_code_choose_community`
- order 832: `_code_query_terms` (function), lines 83481-83495, exports `_code_query_terms`
- order 841: `TFGraphIDFIndex` (class), lines 84563-86239, exports `TFGraphIDFIndex`
- order 850: `CodeGraphIndex` (class), lines 89447-89932, exports `CodeGraphIndex`

### `rag/ingestion.py`

- order 810: `_rag_trigram_set` (function), lines 82822-82829, exports `_rag_trigram_set`
- order 811: `_rag_jaccard_sim` (function), lines 82830-82839, exports `_rag_jaccard_sim`
- order 812: `_rag_mmr_select` (function), lines 82840-82889, exports `_rag_mmr_select`
- order 817: `_rag_embed_text` (function), lines 83024-83047, exports `_rag_embed_text`
- order 818: `_rag_embed_batch` (function), lines 83048-83056, exports `_rag_embed_batch`
- order 819: `_rag_window_for_query` (function), lines 83057-83071, exports `_rag_window_for_query`
- order 820: `_rag_focused_excerpt` (function), lines 83072-83114, exports `_rag_focused_excerpt`
- order 821: `_rag_query_variants` (function), lines 83115-83154, exports `_rag_query_variants`
- order 822: `_rag_parse_segments` (function), lines 83155-83217, exports `_rag_parse_segments`
- order 823: `_rag_boundary_split` (function), lines 83218-83275, exports `_rag_boundary_split`
- order 848: `_rag_parse_file_worker` (function), lines 88548-88564, exports `_rag_parse_file_worker`
- order 849: `RAGIngestionService` (class), lines 88565-89446, exports `RAGIngestionService`
- order 852: `CodeIngestionService` (class), lines 90199-90286, exports `CodeIngestionService`

### `rag/parsers.py`

- order 701: `normalize_rel_preview_path` (function), lines 9078-9091, exports `normalize_rel_preview_path`
- order 702: `is_code_preview_candidate` (function), lines 9092-9102, exports `is_code_preview_candidate`
- order 707: `preview_kind_for_path` (function), lines 9109-9140, exports `preview_kind_for_path`
- order 708: `build_code_preview_rows` (function), lines 9141-9189, exports `build_code_preview_rows`
- order 801: `_rag_safe_name` (function), lines 82612-82626, exports `_rag_safe_name`
- order 802: `_rag_detect_language` (function), lines 82627-82643, exports `_rag_detect_language`
- order 803: `_rag_cjk_ngrams` (function), lines 82644-82658, exports `_rag_cjk_ngrams`
- order 804: `_rag_is_noise_token` (function), lines 82659-82680, exports `_rag_is_noise_token`
- order 805: `_rag_entity_allowed` (function), lines 82681-82695, exports `_rag_entity_allowed`
- order 806: `_rag_filter_entities` (function), lines 82696-82712, exports `_rag_filter_entities`
- order 807: `_rag_filename_entity_aliases` (function), lines 82713-82748, exports `_rag_filename_entity_aliases`
- order 808: `_rag_apply_filename_entity_policy` (function), lines 82749-82781, exports `_rag_apply_filename_entity_policy`
- order 809: `_rag_choose_community` (function), lines 82782-82821, exports `_rag_choose_community`
- order 813: `_rag_tokenize` (function), lines 82890-82943, exports `_rag_tokenize`
- order 814: `_rag_expand_tokens` (function), lines 82944-82967, exports `_rag_expand_tokens`
- order 815: `_rag_extract_entities` (function), lines 82968-82986, exports `_rag_extract_entities`
- order 816: `_rag_classify_document` (function), lines 82987-83023, exports `_rag_classify_document`
- order 824: `_rag_chunk_text` (function), lines 83276-83355, exports `_rag_chunk_text`
- order 828: `_code_language_from_name` (function), lines 83430-83448, exports `_code_language_from_name`
- order 829: `_code_is_test_path` (function), lines 83449-83453, exports `_code_is_test_path`
- order 833: `_CallCollector` (class), lines 83496-83510, exports `_CallCollector`
- order 834: `_ALGO_COMPLEXITY_RE` (assignment), lines 83511-83513, exports `_ALGO_COMPLEXITY_RE`
- order 835: `_ALGO_STEP_RE` (assignment), lines 83514-83514, exports `_ALGO_STEP_RE`
- order 836: `_ALGO_MATH_VARS` (assignment), lines 83515-83515, exports `_ALGO_MATH_VARS`
- order 837: `_ALGO_DOC_KEYWORDS` (assignment), lines 83516-83516, exports `_ALGO_DOC_KEYWORDS`
- order 838: `_detect_algo_chunk` (function), lines 83517-83542, exports `_detect_algo_chunk`
- order 839: `CodeContentParser` (class), lines 83543-84052, exports `CodeContentParser`
- order 840: `RAGContentParser` (class), lines 84053-84562, exports `RAGContentParser`

### `rag/store.py`

- order 842: `RAGLibraryStore` (class), lines 86240-86825, exports `RAGLibraryStore`
- order 843: `WikiStore` (class), lines 86826-87357, exports `WikiStore`
- order 844: `UserMemoryStore` (class), lines 87358-88035, exports `UserMemoryStore`
- order 845: `UserInteractionOptimizer` (class), lines 88036-88104, exports `UserInteractionOptimizer`
- order 846: `UserIntentProfiler` (class), lines 88105-88146, exports `UserIntentProfiler`
- order 847: `WorkflowMemoryStore` (class), lines 88147-88547, exports `WorkflowMemoryStore`
- order 851: `CodeLibraryStore` (class), lines 89933-90198, exports `CodeLibraryStore`

### `rag/web_search.py`

- order 585: `_agent_web_bool` (function), lines 4141-4148, exports `_agent_web_bool`
- order 586: `_agent_web_int` (function), lines 4149-4156, exports `_agent_web_int`
- order 587: `_agent_web_host_is_local_name` (function), lines 4157-4163, exports `_agent_web_host_is_local_name`
- order 588: `_agent_web_ip_is_blocked` (function), lines 4164-4178, exports `_agent_web_ip_is_blocked`
- order 589: `_agent_web_canonical_url` (function), lines 4179-4208, exports `_agent_web_canonical_url`
- order 590: `_agent_web_domain_to_seed` (function), lines 4209-4220, exports `_agent_web_domain_to_seed`
- order 591: `_agent_web_query_terms` (function), lines 4221-4238, exports `_agent_web_query_terms`
- order 592: `_agent_web_query_domain_hints` (function), lines 4239-4279, exports `_agent_web_query_domain_hints`
- order 593: `_agent_web_query_needs_fresh_network` (function), lines 4280-4302, exports `_agent_web_query_needs_fresh_network`
- order 594: `_agent_web_extract_text_snippet` (function), lines 4303-4320, exports `_agent_web_extract_text_snippet`
- order 595: `AgentWebHTMLParser` (class), lines 4321-4400, exports `AgentWebHTMLParser`
- order 596: `_agent_web_decompress_bytes` (function), lines 4401-4424, exports `_agent_web_decompress_bytes`
- order 597: `_agent_web_charset_candidates` (function), lines 4425-4483, exports `_agent_web_charset_candidates`
- order 598: `_agent_web_decode_text_bytes` (function), lines 4484-4518, exports `_agent_web_decode_text_bytes`
- order 599: `AgentWebSearchEngine` (class), lines 4519-5588, exports `AgentWebSearchEngine`

### `server/http.py`

- order 863: `AgentHTTPServer` (class), lines 97887-97926, exports `AgentHTTPServer`
- order 866: `Handler` (class), lines 99046-100409, exports `Handler`

### `server/rag_admin.py`

- order 868: `RagAdminHandler` (class), lines 100636-100819, exports `RagAdminHandler`
- order 869: `CodeAdminHandler` (class), lines 100820-101022, exports `CodeAdminHandler`

### `server/skills.py`

- order 867: `SkillsHandler` (class), lines 100410-100635, exports `SkillsHandler`

### `session/manager.py`

- order 515: `SessionCreationLimitExceeded` (class), lines 2914-2919, exports `SessionCreationLimitExceeded`
- order 781: `SessionManager` (class), lines 70136-71457, exports `SessionManager`

### `session/state.py`

- order 780: `SessionState` (class), lines 19184-70135, exports `SessionState`

### `skills/embedded.py`

- order 711: `EMBEDDED_SKILLS_ARCHIVE_B64` (constant), lines 9598-9599, exports `EMBEDDED_SKILLS_ARCHIVE_B64`
- order 712: `EMBEDDED_SKILLS_ARCHIVE_SHA256` (constant), lines 9600-9600, exports `EMBEDDED_SKILLS_ARCHIVE_SHA256`
- order 713: `EMBEDDED_SKILLS_ARCHIVE_FILES` (constant), lines 9601-9623, exports `EMBEDDED_SKILLS_ARCHIVE_FILES`
- order 738: `BUILTIN_CLAWHUB_SKILLS_VERSION` (constant), lines 12859-12861, exports `BUILTIN_CLAWHUB_SKILLS_VERSION`
- order 739: `EMBEDDED_CLAWHUB_SKILLS_ARCHIVE_B64` (constant), lines 12862-13107, exports `EMBEDDED_CLAWHUB_SKILLS_ARCHIVE_B64`
- order 741: `MCP_BUILDER_SKILL_MD` (constant), lines 13155-13329, exports `MCP_BUILDER_SKILL_MD`
- order 744: `SKILL_PROTOCOL_LOCAL` (constant), lines 13361-13362, exports `SKILL_PROTOCOL_LOCAL`
- order 745: `SKILL_PROTOCOL_CLAWHUB` (constant), lines 13363-13363, exports `SKILL_PROTOCOL_CLAWHUB`
- order 746: `SKILL_PROTOCOL_HTTP_JSON` (constant), lines 13364-13364, exports `SKILL_PROTOCOL_HTTP_JSON`
- order 747: `SKILL_PROTOCOL_SPECS` (constant), lines 13365-13397, exports `SKILL_PROTOCOL_SPECS`

### `skills/provisioning.py`

- order 714: `ensure_embedded_skills_at_root` (function), lines 9624-9689, exports `ensure_embedded_skills_at_root`
- order 715: `ensure_embedded_skills` (function), lines 9690-9693, exports `ensure_embedded_skills`
- order 717: `detect_upload_parser_capabilities` (function), lines 9700-9716, exports `detect_upload_parser_capabilities`
- order 718: `_render_cap_markdown` (function), lines 9717-9732, exports `_render_cap_markdown`
- order 719: `_write_text_if_changed` (function), lines 9733-9739, exports `_write_text_if_changed`
- order 720: `ensure_generated_document_skills` (function), lines 9740-9829, exports `ensure_generated_document_skills`
- order 721: `ensure_generated_image_coding_feedback_skill` (function), lines 9830-9930, exports `ensure_generated_image_coding_feedback_skill`
- order 722: `_skill_knowledge_files` (function), lines 9931-9951, exports `_skill_knowledge_files`
- order 723: `analyze_skill_building_knowledge` (function), lines 9952-10007, exports `analyze_skill_building_knowledge`
- order 724: `_sanitize_skill_slug` (function), lines 10008-10011, exports `_sanitize_skill_slug`
- order 725: `_build_skills_gen_skill_content` (function), lines 10012-10044, exports `_build_skills_gen_skill_content`
- order 726: `ensure_generated_skills_gen_skill` (function), lines 10045-10050, exports `ensure_generated_skills_gen_skill`
- order 727: `ensure_generated_execution_recovery_skill` (function), lines 10051-10135, exports `ensure_generated_execution_recovery_skill`
- order 728: `ensure_generated_systematic_debugging_skill` (function), lines 10136-10409, exports `ensure_generated_systematic_debugging_skill`
- order 729: `ensure_generated_code_engineering_mastery_skill` (function), lines 10410-10529, exports `ensure_generated_code_engineering_mastery_skill`
- order 730: `ensure_generated_smart_file_navigation_skill` (function), lines 10530-10646, exports `ensure_generated_smart_file_navigation_skill`
- order 731: `ensure_generated_html_frontend_report_skills` (function), lines 10647-10855, exports `ensure_generated_html_frontend_report_skills`
- order 732: `ensure_generated_deep_research_skills` (function), lines 10856-11125, exports `ensure_generated_deep_research_skills`
- order 733: `ensure_generated_research_scientific_skills` (function), lines 11126-11763, exports `ensure_generated_research_scientific_skills`
- order 734: `ensure_generated_rag_mastery_skills` (function), lines 11764-12065, exports `ensure_generated_rag_mastery_skills`
- order 735: `ensure_generated_multimodal_comprehension_skills` (function), lines 12066-12760, exports `ensure_generated_multimodal_comprehension_skills`
- order 736: `ensure_generated_runtime_skills_manifest` (function), lines 12761-12795, exports `ensure_generated_runtime_skills_manifest`
- order 737: `ensure_generated_agent_web_search_skill` (function), lines 12796-12858, exports `ensure_generated_agent_web_search_skill`
- order 740: `ensure_embedded_clawhub_skills` (function), lines 13108-13154, exports `ensure_embedded_clawhub_skills`
- order 742: `ensure_generated_mcp_builder_skill` (function), lines 13330-13341, exports `ensure_generated_mcp_builder_skill`
- order 743: `ensure_runtime_skills` (function), lines 13342-13360, exports `ensure_runtime_skills`

### `skills/store.py`

- order 748: `_BUILTIN_SKILLS` (assignment), lines 13398-13506, exports `_BUILTIN_SKILLS`
- order 749: `SkillStore` (class), lines 13507-14814, exports `SkillStore`

### `utils/compress.py`

- order 603: `compress_text_blob` (function), lines 5753-5759, exports `compress_text_blob`
- order 604: `decompress_text_blob` (function), lines 5760-5769, exports `decompress_text_blob`

### `utils/crypto.py`

- order 676: `CryptoBox` (class), lines 7711-7829, exports `CryptoBox`

### `utils/errors.py`

- order 623: `EmptyActionError` (class), lines 6258-6261, exports `EmptyActionError`

### `utils/files.py`

- order 479: `_normalize_js_lib_asset_ref` (function), lines 1705-1720, exports `_normalize_js_lib_asset_ref`
- order 480: `_resolve_js_lib_asset_path` (function), lines 1721-1752, exports `_resolve_js_lib_asset_path`
- order 481: `_discover_extra_js_lib_files` (function), lines 1753-1785, exports `_discover_extra_js_lib_files`
- order 561: `safe_path` (function), lines 3648-3658, exports `safe_path`
- order 562: `_safe_js_filename` (function), lines 3659-3667, exports `_safe_js_filename`
- order 563: `_sha256_bytes` (function), lines 3668-3670, exports `_sha256_bytes`
- order 564: `_sha256_file` (function), lines 3671-3680, exports `_sha256_file`
- order 565: `_download_http_bytes` (function), lines 3681-3690, exports `_download_http_bytes`
- order 566: `offline_js_lib_root` (function), lines 3691-3693, exports `offline_js_lib_root`
- order 567: `_offline_js_entry_relative_path` (function), lines 3694-3699, exports `_offline_js_entry_relative_path`
- order 568: `_archive_member_relative_path` (function), lines 3700-3710, exports `_archive_member_relative_path`
- order 569: `_path_size_bytes` (function), lines 3711-3727, exports `_path_size_bytes`
- order 570: `_extract_archive_to_dir` (function), lines 3728-3769, exports `_extract_archive_to_dir`
- order 571: `_package_required_paths` (function), lines 3770-3777, exports `_package_required_paths`
- order 572: `_package_install_ready` (function), lines 3778-3787, exports `_package_install_ready`
- order 573: `_postprocess_offline_js_package` (function), lines 3788-3824, exports `_postprocess_offline_js_package`
- order 574: `_ensure_offline_js_package` (function), lines 3825-3865, exports `_ensure_offline_js_package`
- order 575: `_render_offline_js_catalog_md` (function), lines 3866-3883, exports `_render_offline_js_catalog_md`
- order 577: `ensure_offline_js_libs` (function), lines 3895-4040, exports `ensure_offline_js_libs`
- order 578: `_normalize_external_js_url` (function), lines 4041-4046, exports `_normalize_external_js_url`
- order 579: `is_external_js_src` (function), lines 4047-4050, exports `is_external_js_src`
- order 580: `match_offline_js_catalog_by_url` (function), lines 4051-4068, exports `match_offline_js_catalog_by_url`
- order 581: `cache_external_js_url` (function), lines 4069-4102, exports `cache_external_js_url`
- order 679: `try_read_text` (function), lines 8033-8042, exports `try_read_text`

### `utils/http.py`

- order 53: `_URL_OPEN_ORIGINAL` (assignment), lines 63-63, exports `_URL_OPEN_ORIGINAL`
- order 54: `_HTTP_SSL_CONTEXT` (assignment), lines 64-64, exports `_HTTP_SSL_CONTEXT`
- order 72: `_shared_http_ssl_context` (function), lines 82-105, exports `_shared_http_ssl_context`
- order 73: `urlopen` (function), lines 106-115, exports `urlopen`
- order 554: `json_response_bytes` (function), lines 3592-3594, exports `json_response_bytes`
- order 555: `read_http_json_body` (function), lines 3595-3608, exports `read_http_json_body`
- order 556: `close_if_http_request_body_unread` (function), lines 3609-3622, exports `close_if_http_request_body_unread`

### `utils/json_utils.py`

- order 91: `JSON_FSYNC_ENABLED` (constant), lines 168-168, exports `JSON_FSYNC_ENABLED`
- order 553: `json_dumps` (function), lines 3588-3591, exports `json_dumps`
- order 613: `parse_tool_arguments` (function), lines 6063-6073, exports `parse_tool_arguments`
- order 614: `repair_truncated_json_object` (function), lines 6074-6128, exports `repair_truncated_json_object`
- order 615: `parse_tool_arguments_with_error` (function), lines 6129-6160, exports `parse_tool_arguments_with_error`
- order 616: `_is_valid_json_object` (function), lines 6161-6166, exports `_is_valid_json_object`
- order 617: `_scan_top_level_json_objects` (function), lines 6167-6190, exports `_scan_top_level_json_objects`
- order 618: `reconstruct_streamed_tool_args` (function), lines 6191-6235, exports `reconstruct_streamed_tool_args`
- order 636: `parse_json_object` (function), lines 6500-6506, exports `parse_json_object`
- order 637: `extract_json_object_from_text` (function), lines 6507-6530, exports `extract_json_object_from_text`
- order 680: `_json_default_copy` (function), lines 8043-8049, exports `_json_default_copy`
- order 681: `_read_json_file` (function), lines 8050-8071, exports `_read_json_file`
- order 682: `_write_json_file` (function), lines 8072-8100, exports `_write_json_file`

### `utils/media.py`

- order 530: `guess_mime_from_name` (function), lines 3262-3266, exports `guess_mime_from_name`
- order 531: `_convert_image_to_safe_format` (function), lines 3267-3286, exports `_convert_image_to_safe_format`
- order 532: `guess_ext_from_mime` (function), lines 3287-3295, exports `guess_ext_from_mime`

### `utils/misc.py`

- order 533: `now_ts` (function), lines 3296-3298, exports `now_ts`
- order 534: `_benign_socket_log_lock` (assignment), lines 3299-3301, exports `_benign_socket_log_lock`
- order 535: `_benign_socket_log_state` (assignment), lines 3302-3302, exports `_benign_socket_log_state`
- order 537: `is_benign_socket_error` (function), lines 3318-3338, exports `is_benign_socket_error`
- order 538: `_socket_error_code` (function), lines 3339-3350, exports `_socket_error_code`
- order 539: `_log_benign_socket_error_limited` (function), lines 3351-3387, exports `_log_benign_socket_error_limited`
- order 540: `swallow_benign_socket_error` (function), lines 3388-3394, exports `swallow_benign_socket_error`
- order 541: `normalize_timeout_seconds` (function), lines 3395-3410, exports `normalize_timeout_seconds`
- order 542: `detect_local_lan_ip` (function), lines 3411-3422, exports `detect_local_lan_ip`
- order 543: `_LOCAL_LAN_IP_CACHE` (assignment), lines 3423-3424, exports `_LOCAL_LAN_IP_CACHE`
- order 544: `detect_local_lan_ip_cached` (function), lines 3425-3438, exports `detect_local_lan_ip_cached`
- order 557: `make_id` (function), lines 3623-3625, exports `make_id`
- order 558: `sanitize_profile_id` (function), lines 3626-3629, exports `sanitize_profile_id`
- order 674: `user_id_from_ip` (function), lines 7670-7677, exports `user_id_from_ip`
- order 678: `_meta_string_list` (function), lines 8019-8032, exports `_meta_string_list`
- order 716: `_module_exists` (function), lines 9694-9699, exports `_module_exists`

### `utils/text.py`

- order 79: `MAX_TOOL_OUTPUT` (constant), lines 156-156, exports `MAX_TOOL_OUTPUT`
- order 333: `SOCKET_NOISE_LINE_PATTERNS` (constant), lines 665-670, exports `SOCKET_NOISE_LINE_PATTERNS`
- order 536: `filter_runtime_noise_lines` (function), lines 3303-3317, exports `filter_runtime_noise_lines`
- order 549: `safe_utf8_bytes` (function), lines 3563-3565, exports `safe_utf8_bytes`
- order 550: `escape_invalid_utf8_text` (function), lines 3566-3568, exports `escape_invalid_utf8_text`
- order 551: `sanitize_utf8_surrogates` (function), lines 3569-3582, exports `sanitize_utf8_surrogates`
- order 552: `decode_utf8_replace` (function), lines 3583-3587, exports `decode_utf8_replace`
- order 582: `trim` (function), lines 4103-4106, exports `trim`
- order 583: `display_clean` (function), lines 4107-4121, exports `display_clean`
- order 584: `short_title_from` (function), lines 4122-4140, exports `short_title_from`
- order 600: `_fmt_export_ts` (function), lines 5589-5599, exports `_fmt_export_ts`
- order 601: `_html_esc` (function), lines 5600-5603, exports `_html_esc`
- order 602: `_text_to_minimal_pdf` (function), lines 5604-5752, exports `_text_to_minimal_pdf`
- order 605: `normalize_embedded_newlines` (function), lines 5770-5779, exports `normalize_embedded_newlines`
- order 606: `_map_todo_status_token` (function), lines 5780-5818, exports `_map_todo_status_token`
- order 607: `split_todo_status_text` (function), lines 5819-5878, exports `split_todo_status_text`
- order 608: `extract_todo_rows_from_text` (function), lines 5879-5948, exports `extract_todo_rows_from_text`
- order 609: `decode_structured_todo_container` (function), lines 5949-5967, exports `decode_structured_todo_container`
- order 610: `infer_todo_status_from_text` (function), lines 5968-5976, exports `infer_todo_status_from_text`
- order 611: `split_structured_todo_content` (function), lines 5977-6032, exports `split_structured_todo_content`
- order 612: `normalize_work_text` (function), lines 6033-6062, exports `normalize_work_text`
- order 693: `make_unified_diff` (function), lines 8793-8811, exports `make_unified_diff`
- order 694: `_skip_row` (function), lines 8812-8817, exports `_skip_row`
- order 695: `_row_is_hot` (function), lines 8818-8821, exports `_row_is_hot`
- order 696: `_hotspot_index` (function), lines 8822-8845, exports `_hotspot_index`
- order 697: `_compress_rows_keep_hotspot` (function), lines 8846-8895, exports `_compress_rows_keep_hotspot`
- order 698: `_focused_diff_rows_from_opcodes` (function), lines 8896-9030, exports `_focused_diff_rows_from_opcodes`
- order 699: `make_numbered_diff` (function), lines 9031-9063, exports `make_numbered_diff`
- order 700: `render_numbered_diff_text` (function), lines 9064-9077, exports `render_numbered_diff_text`

### `web/admin_assets.py`

- order 789: `ADMIN_INDEX_HTML` (constant), lines 77322-77484, exports `ADMIN_INDEX_HTML`
- order 790: `ADMIN_CSS` (constant), lines 77485-77612, exports `ADMIN_CSS`
- order 791: `ADMIN_JS` (constant), lines 77613-77677, exports `ADMIN_JS`

### `web/assets.py`

- order 782: `INDEX_HTML` (constant), lines 71458-71703, exports `INDEX_HTML`
- order 783: `APP_CSS` (constant), lines 71704-72239, exports `APP_CSS`
- order 784: `APP_JS` (constant), lines 72240-76882, exports `APP_JS`
- order 785: `APP_TS` (constant), lines 76883-76922, exports `APP_TS`

### `web/skills_assets.py`

- order 786: `SKILLS_INDEX_HTML` (constant), lines 76923-77078, exports `SKILLS_INDEX_HTML`
- order 787: `SKILLS_EXTRA_CSS` (constant), lines 77079-77175, exports `SKILLS_EXTRA_CSS`
- order 788: `SKILLS_APP_JS` (constant), lines 77176-77321, exports `SKILLS_APP_JS`
