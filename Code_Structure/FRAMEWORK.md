# Code_Structure Framework

## Overview

- Source snapshot: `Clouds_Coder.py` (1212 top-level statements)
- Generated source modules: 64
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
│   ├── process.py
│   ├── tasks.py
│   ├── todo.py
│   ├── tools.py
│   └── worktree.py
├── app
│   ├── context.py
│   ├── main.py
│   └── services.py
├── collaboration
│   ├── core.py
│   └── watcher.py
├── config
│   ├── bootstrap.py
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
│   ├── store.py
│   └── studio.py
├── utils
│   ├── compress.py
│   ├── crypto.py
│   ├── errors.py
│   ├── files.py
│   ├── http.py
│   ├── json_utils.py
│   ├── media.py
│   ├── misc.py
│   ├── sqlite.py
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
| `_imports.py` | 76 | 94 | — | 1–3912 |
| `admin/auth.py` | 3 | 3 | `admin/constants.py`, `utils/misc.py`, `utils/sqlite.py` | 14429–15271 |
| `admin/config.py` | 8 | 8 | `config/constants.py`, `config/paths.py`, `config/settings.py`, `llm/constants.py`, `utils/http.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` | 16019–16482 |
| `admin/constants.py` | 16 | 16 | — | 3919–118748 |
| `agent/background.py` | 1 | 1 | `agent/process.py`, `config/constants.py`, `ide/sandbox.py`, `utils/misc.py`, `utils/text.py` | 23929–24554 |
| `agent/bus.py` | 1 | 1 | `config/constants.py`, `utils/crypto.py`, `utils/misc.py` | 24555–24620 |
| `agent/errors.py` | 1 | 1 | — | 12316–12319 |
| `agent/events.py` | 1 | 1 | — | 17209–17263 |
| `agent/process.py` | 7 | 7 | `ide/sandbox.py`, `utils/errors.py`, `utils/misc.py`, `utils/text.py` | 8298–23928 |
| `agent/tasks.py` | 1 | 1 | `utils/crypto.py`, `utils/json_utils.py`, `utils/misc.py` | 23428–23562 |
| `agent/todo.py` | 1 | 1 | `config/constants.py`, `config/settings.py`, `utils/misc.py`, `utils/text.py` | 17264–17624 |
| `agent/tools.py` | 15 | 19 | `config/constants.py`, `utils/text.py` | 17088–29482 |
| `agent/worktree.py` | 1 | 1 | `agent/process.py`, `agent/tasks.py`, `config/constants.py`, `utils/crypto.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` | 24621–24833 |
| `app/context.py` | 1 | 1 | `admin/auth.py`, `admin/config.py`, `admin/constants.py`, `agent/process.py`, `agent/tools.py`, `app/services.py`, `collaboration/core.py`, `config/bootstrap.py`, `config/constants.py`, `config/paths.py`, `config/settings.py`, `ide/assets.py`, `ide/auth.py`, `ide/errors.py`, `ide/events.py`, `ide/preview.py`, `ide/sandbox.py`, `llm/client.py`, `llm/constants.py`, `llm/utils.py`, `mcp/driver.py`, `rag/assets.py`, `rag/constants.py`, `rag/ingestion.py`, `rag/parsers.py`, `rag/store.py`, `server/http.py`, `session/manager.py`, `session/state.py`, `skills/provisioning.py`, `skills/store.py`, `skills/studio.py`, `utils/crypto.py`, `utils/files.py`, `utils/http.py`, `utils/json_utils.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py`, `web/assets.py`, `web/skills_assets.py` | 118749–129628 |
| `app/main.py` | 2 | 1 | `admin/config.py`, `admin/constants.py`, `agent/tools.py`, `app/context.py`, `collaboration/watcher.py`, `config/constants.py`, `config/paths.py`, `config/settings.py`, `ide/handler.py`, `llm/constants.py`, `llm/utils.py`, `mcp/constants.py`, `mcp/service.py`, `rag/constants.py`, `server/http.py`, `server/rag_admin.py`, `server/skills.py`, `skills/provisioning.py`, `utils/files.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` | 136610–138561 |
| `app/services.py` | 2 | 2 | `admin/constants.py`, `config/settings.py`, `skills/embedded.py`, `skills/store.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/sqlite.py`, `utils/text.py` | 129669–130854 |
| `collaboration/core.py` | 23 | 23 | `config/constants.py`, `utils/sqlite.py` | 531–3772 |
| `collaboration/watcher.py` | 2 | 2 | `utils/misc.py`, `utils/sqlite.py`, `utils/text.py` | 136517–136609 |
| `config/bootstrap.py` | 6 | 6 | `config/constants.py`, `config/settings.py`, `utils/json_utils.py`, `utils/misc.py` | 123–14984 |
| `config/constants.py` | 504 | 499 | `config/bootstrap.py`, `rag/constants.py` | 482–118744 |
| `config/paths.py` | 13 | 13 | `agent/process.py`, `utils/crypto.py`, `utils/text.py` | 3918–8458 |
| `config/settings.py` | 76 | 76 | `agent/tools.py`, `config/constants.py`, `config/paths.py`, `ide/preview.py`, `llm/constants.py`, `llm/utils.py`, `rag/constants.py`, `skills/provisioning.py`, `utils/http.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` | 6397–16816 |
| `ide/assets.py` | 8 | 3 | — | 115688–116816 |
| `ide/auth.py` | 2 | 2 | `admin/auth.py`, `admin/constants.py`, `config/constants.py`, `utils/misc.py`, `utils/sqlite.py`, `utils/text.py` | 15272–16003 |
| `ide/errors.py` | 2 | 2 | — | 16004–16018 |
| `ide/events.py` | 1 | 1 | `config/constants.py`, `utils/text.py` | 9341–9392 |
| `ide/handler.py` | 1 | 1 | `admin/auth.py`, `app/context.py`, `collaboration/core.py`, `config/constants.py`, `config/settings.py`, `ide/auth.py`, `ide/errors.py`, `ide/events.py`, `session/manager.py`, `session/state.py`, `utils/http.py`, `utils/json_utils.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py` | 134086–135742 |
| `ide/preview.py` | 12 | 12 | `config/constants.py`, `utils/text.py` | 16768–17208 |
| `ide/sandbox.py` | 21 | 21 | `agent/process.py`, `utils/misc.py` | 8280–30011 |
| `llm/client.py` | 2 | 2 | `agent/tools.py`, `config/constants.py`, `config/settings.py`, `llm/utils.py`, `utils/http.py`, `utils/json_utils.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py` | 26216–28756 |
| `llm/constants.py` | 17 | 17 | — | 3916–12791 |
| `llm/utils.py` | 29 | 29 | `agent/process.py`, `config/settings.py`, `llm/constants.py`, `utils/http.py`, `utils/json_utils.py`, `utils/text.py` | 12233–13433 |
| `mcp/constants.py` | 8 | 8 | — | 4288–24869 |
| `mcp/driver.py` | 13 | 13 | `mcp/constants.py`, `utils/files.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` | 24870–26215 |
| `mcp/service.py` | 1 | 1 | `app/context.py`, `config/constants.py`, `utils/files.py`, `utils/http.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` | 136214–136431 |
| `rag/assets.py` | 6 | 6 | — | 113081–115687 |
| `rag/constants.py` | 77 | 77 | — | 4284–106039 |
| `rag/index.py` | 5 | 5 | `config/constants.py`, `rag/constants.py`, `rag/ingestion.py`, `rag/parsers.py`, `utils/misc.py`, `utils/text.py` | 106064–112701 |
| `rag/ingestion.py` | 13 | 13 | `config/constants.py`, `config/settings.py`, `rag/constants.py`, `rag/parsers.py`, `rag/store.py`, `session/state.py`, `utils/files.py`, `utils/json_utils.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py` | 105386–113080 |
| `rag/parsers.py` | 31 | 31 | `agent/process.py`, `config/constants.py`, `rag/constants.py`, `rag/ingestion.py`, `utils/files.py`, `utils/json_utils.py`, `utils/media.py`, `utils/text.py` | 105009–107235 |
| `rag/store.py` | 7 | 7 | `config/constants.py`, `config/settings.py`, `ide/preview.py`, `rag/constants.py`, `rag/index.py`, `rag/ingestion.py`, `rag/parsers.py`, `skills/provisioning.py`, `utils/files.py`, `utils/json_utils.py`, `utils/media.py`, `utils/misc.py`, `utils/sqlite.py`, `utils/text.py` | 108931–112992 |
| `rag/web_search.py` | 15 | 15 | `config/constants.py`, `config/paths.py`, `rag/constants.py`, `utils/http.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/sqlite.py`, `utils/text.py` | 9427–11585 |
| `server/http.py` | 12 | 12 | `admin/auth.py`, `admin/config.py`, `admin/constants.py`, `agent/process.py`, `app/context.py`, `collaboration/core.py`, `collaboration/watcher.py`, `config/constants.py`, `config/paths.py`, `config/settings.py`, `ide/auth.py`, `ide/handler.py`, `ide/preview.py`, `llm/utils.py`, `server/rag_admin.py`, `session/manager.py`, `session/state.py`, `skills/studio.py`, `utils/errors.py`, `utils/files.py`, `utils/http.py`, `utils/json_utils.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py`, `web/admin_assets.py` | 6446–136213 |
| `server/rag_admin.py` | 3 | 3 | `admin/auth.py`, `app/context.py`, `config/constants.py`, `rag/constants.py`, `utils/http.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py` | 133414–134085 |
| `server/skills.py` | 1 | 1 | `admin/auth.py`, `app/context.py`, `config/constants.py`, `config/paths.py`, `config/settings.py`, `session/manager.py`, `skills/provisioning.py`, `skills/studio.py`, `utils/http.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py` | 132771–133413 |
| `session/manager.py` | 2 | 2 | `agent/process.py`, `config/constants.py`, `config/paths.py`, `config/settings.py`, `llm/client.py`, `llm/utils.py`, `rag/store.py`, `session/state.py`, `skills/store.py`, `utils/crypto.py`, `utils/files.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` | 7606–93165 |
| `session/state.py` | 1 | 1 | `admin/constants.py`, `agent/background.py`, `agent/bus.py`, `agent/errors.py`, `agent/events.py`, `agent/process.py`, `agent/tasks.py`, `agent/todo.py`, `agent/tools.py`, `agent/worktree.py`, `collaboration/core.py`, `config/constants.py`, `config/paths.py`, `config/settings.py`, `ide/events.py`, `ide/preview.py`, `ide/sandbox.py`, `llm/client.py`, `llm/constants.py`, `llm/utils.py`, `mcp/constants.py`, `mcp/driver.py`, `rag/constants.py`, `rag/parsers.py`, `rag/web_search.py`, `server/http.py`, `skills/provisioning.py`, `skills/store.py`, `utils/compress.py`, `utils/crypto.py`, `utils/errors.py`, `utils/files.py`, `utils/http.py`, `utils/json_utils.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py` | 30012–90660 |
| `skills/embedded.py` | 10 | 10 | — | 17625–21424 |
| `skills/provisioning.py` | 26 | 26 | `config/paths.py`, `skills/embedded.py`, `utils/files.py`, `utils/json_utils.py`, `utils/misc.py` | 17651–21387 |
| `skills/store.py` | 2 | 2 | `config/constants.py`, `config/settings.py`, `llm/utils.py`, `skills/embedded.py`, `utils/files.py`, `utils/http.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` | 21425–23427 |
| `skills/studio.py` | 5 | 5 | `agent/process.py`, `collaboration/core.py`, `config/constants.py`, `config/settings.py`, `ide/sandbox.py`, `llm/client.py`, `llm/constants.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/sqlite.py`, `utils/text.py` | 116842–118739 |
| `utils/compress.py` | 2 | 2 | — | 11750–11766 |
| `utils/crypto.py` | 1 | 1 | `utils/json_utils.py` | 14462–14615 |
| `utils/errors.py` | 2 | 2 | — | 12312–23568 |
| `utils/files.py` | 27 | 27 | `config/constants.py`, `config/paths.py`, `utils/http.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` | 6316–14868 |
| `utils/http.py` | 7 | 7 | `utils/json_utils.py`, `utils/text.py` | 3913–8434 |
| `utils/json_utils.py` | 13 | 13 | `utils/text.py` | 4283–14926 |
| `utils/media.py` | 6 | 6 | — | 5954–7987 |
| `utils/misc.py` | 16 | 16 | `config/constants.py` | 7988–17726 |
| `utils/sqlite.py` | 3 | 3 | — | 73–136516 |
| `utils/text.py` | 30 | 30 | `config/constants.py` | 4271–16767 |
| `web/admin_assets.py` | 3 | 3 | — | 99192–100074 |
| `web/assets.py` | 5 | 4 | — | 93166–98789 |
| `web/skills_assets.py` | 3 | 3 | — | 98790–99191 |

## Source Mapping

### `_imports.py`

- order 0: `_import_2` (import), lines 1-2, exports `annotations`
- order 1: `_import_4` (import), lines 3-4, exports `argparse`
- order 2: `_import_5` (import), lines 5-5, exports `ast`
- order 3: `_import_6` (import), lines 6-6, exports `base64`
- order 4: `_import_7` (import), lines 7-7, exports `concurrent`
- order 5: `_import_8` (import), lines 8-8, exports `contextlib`
- order 6: `_import_9` (import), lines 9-9, exports `copy`
- order 7: `_import_10` (import), lines 10-10, exports `csv`
- order 8: `_import_11` (import), lines 11-11, exports `ctypes`
- order 9: `_import_12` (import), lines 12-12, exports `difflib`
- order 10: `_import_13` (import), lines 13-13, exports `errno`
- order 11: `_import_14` (import), lines 14-14, exports `fnmatch`
- order 12: `_import_15` (import), lines 15-15, exports `hashlib`
- order 13: `_import_16` (import), lines 16-16, exports `hmac`
- order 14: `_import_17` (import), lines 17-17, exports `html`
- order 15: `_import_18` (import), lines 18-18, exports `importlib`
- order 16: `_import_19` (import), lines 19-19, exports `io`
- order 17: `_import_20` (import), lines 20-20, exports `ipaddress`
- order 18: `_import_21` (import), lines 21-21, exports `json`
- order 19: `_import_22` (import), lines 22-22, exports `locale`
- order 20: `_import_23` (import), lines 23-23, exports `math`
- order 21: `_import_24` (import), lines 24-24, exports `mimetypes`
- order 22: `_import_25` (import), lines 25-25, exports `multiprocessing`
- order 23: `_import_26` (import), lines 26-26, exports `os`
- order 24: `_import_27` (import), lines 27-27, exports `platform`
- order 25: `_import_28` (import), lines 28-28, exports `posixpath`
- order 26: `_import_29` (import), lines 29-29, exports `queue`
- order 27: `_import_30` (import), lines 30-30, exports `random`
- order 28: `_import_31` (import), lines 31-31, exports `re`
- order 29: `_import_32` (import), lines 32-32, exports `secrets`
- order 30: `_import_33` (import), lines 33-33, exports `select`
- order 31: `_import_34` (import), lines 34-34, exports `selectors`
- order 32: `_import_35` (import), lines 35-35, exports `shlex`
- order 33: `_import_36` (import), lines 36-36, exports `shutil`
- order 34: `_import_37` (import), lines 37-37, exports `signal`
- order 35: `_import_38` (import), lines 38-38, exports `socket`
- order 36: `_import_39` (import), lines 39-39, exports `sqlite3`
- order 37: `_import_40` (import), lines 40-40, exports `ssl`
- order 38: `_import_41` (import), lines 41-41, exports `stat`
- order 39: `_import_42` (import), lines 42-42, exports `struct`
- order 40: `_import_43` (import), lines 43-43, exports `subprocess`
- order 41: `_import_44` (import), lines 44-44, exports `sys`
- order 42: `_import_45` (import), lines 45-45, exports `tarfile`
- order 43: `_import_46` (import), lines 46-46, exports `tempfile`
- order 44: `_import_47` (import), lines 47-47, exports `threading`
- order 45: `_import_48` (import), lines 48-48, exports `time`
- order 46: `_import_49` (import), lines 49-49, exports `traceback`
- order 47: `_import_50` (import), lines 50-50, exports `unicodedata`
- order 48: `_import_51` (import), lines 51-51, exports `robotparser`
- order 49: `_import_52` (import), lines 52-52, exports `uuid`
- order 50: `_import_53` (import), lines 53-53, exports `ET`
- order 51: `_import_54` (import), lines 54-54, exports `zipfile`
- order 52: `_import_55` (import), lines 55-55, exports `zlib`
- order 53: `_import_56` (import), lines 56-56, exports `Counter`, `defaultdict`, `deque`
- order 54: `_import_57` (import), lines 57-57, exports `Iterable`
- order 55: `_import_58` (import), lines 58-58, exports `asdict`, `dataclass`
- order 56: `_import_59` (import), lines 59-59, exports `dataclass_field`
- order 57: `_import_60` (import), lines 60-60, exports `datetime`, `timedelta`, `timezone`
- order 58: `_import_61` (import), lines 61-61, exports `parsedate_to_datetime`
- order 59: `_import_62` (import), lines 62-62, exports `HTMLParser`
- order 60: `_import_63` (import), lines 63-63, exports `HTTPStatus`
- order 61: `_import_64` (import), lines 64-64, exports `IncompleteRead`
- order 62: `_import_65` (import), lines 65-65, exports `SimpleCookie`
- order 63: `_import_66` (import), lines 66-66, exports `BaseHTTPRequestHandler`, `ThreadingHTTPServer`
- order 64: `_import_67` (import), lines 67-67, exports `Path`, `PurePosixPath`
- order 65: `_import_68` (import), lines 68-68, exports `Any`
- order 66: `_import_69` (import), lines 69-69, exports `HTTPError`, `URLError`
- order 67: `_import_70` (import), lines 70-70, exports `parse_qs`, `quote`, `unquote`, `urljoin`, `urlparse`, `urlunparse`
- order 68: `_import_71` (import), lines 71-71, exports `Request`, `urlopen`
- order 69: `_import_72` (import), lines 72-72, exports `ZoneInfo`
- order 72: `_try_import_119` (import), lines 117-122, exports `_AESGCM`
- order 76: `_import_485` (import), lines 484-489, exports `EVOLUTION_MODES`, `LiquidKernelControlPlane`, `LiquidKernelError`
- order 78: `_import_510` (import), lines 506-512, exports `_LiquidKernelRegistry`
- order 119: `_try_import_3896` (import), lines 3894-3903, exports `_fcntl`, `_pty`, `_termios`
- order 120: `_try_import_3905` (import), lines 3904-3908, exports `_certifi`
- order 121: `_try_import_3909` (import), lines 3909-3912, exports `_yaml`

### `admin/auth.py`

- order 923: `trusted_client_ip` (function), lines 14429-14461, exports `trusted_client_ip`
- order 937: `AdminAuthError` (class), lines 14985-14992, exports `AdminAuthError`
- order 938: `AdminAuthStore` (class), lines 14993-15271, exports `AdminAuthStore`

### `admin/config.py`

- order 943: `_admin_config_schema` (function), lines 16019-16139, exports `_admin_config_schema`
- order 944: `_admin_factory_config` (function), lines 16140-16143, exports `_admin_factory_config`
- order 945: `_admin_coerce_config` (function), lines 16144-16299, exports `_admin_coerce_config`
- order 946: `_admin_config_to_argv` (function), lines 16300-16336, exports `_admin_config_to_argv`
- order 947: `_admin_restart_probe_url` (function), lines 16337-16352, exports `_admin_restart_probe_url`
- order 948: `_admin_supervised_restart` (function), lines 16353-16439, exports `_admin_supervised_restart`
- order 949: `_admin_argparse_defaults` (function), lines 16440-16461, exports `_admin_argparse_defaults`
- order 950: `_admin_config_from_namespace` (function), lines 16462-16482, exports `_admin_config_from_namespace`

### `admin/constants.py`

- order 128: `ADMIN_STATE_DIRNAME` (constant), lines 3919-3919, exports `ADMIN_STATE_DIRNAME`
- order 129: `ADMIN_CONFIG_FILENAME` (constant), lines 3920-3920, exports `ADMIN_CONFIG_FILENAME`
- order 130: `ADMIN_APPS_FILENAME` (constant), lines 3921-3921, exports `ADMIN_APPS_FILENAME`
- order 131: `ADMIN_TELEMETRY_FILENAME` (constant), lines 3922-3922, exports `ADMIN_TELEMETRY_FILENAME`
- order 132: `ADMIN_AUTH_FILENAME` (constant), lines 3923-3923, exports `ADMIN_AUTH_FILENAME`
- order 142: `ADMIN_MAX_APP_SKILLS` (constant), lines 3970-3970, exports `ADMIN_MAX_APP_SKILLS`
- order 143: `ADMIN_MAX_APP_CAPSULE_CHARS` (constant), lines 3971-3971, exports `ADMIN_MAX_APP_CAPSULE_CHARS`
- order 144: `ADMIN_MAX_APP_RESOURCE_FILES` (constant), lines 3972-3972, exports `ADMIN_MAX_APP_RESOURCE_FILES`
- order 145: `ADMIN_MAX_APP_RESOURCE_BYTES` (constant), lines 3973-3973, exports `ADMIN_MAX_APP_RESOURCE_BYTES`
- order 146: `ADMIN_APP_INLINE_BLOB_BYTES` (constant), lines 3974-3974, exports `ADMIN_APP_INLINE_BLOB_BYTES`
- order 147: `ADMIN_AUTH_SESSION_TTL_SECONDS` (constant), lines 3975-3975, exports `ADMIN_AUTH_SESSION_TTL_SECONDS`
- order 148: `ADMIN_AUTH_PASSWORD_ITERATIONS` (constant), lines 3976-3976, exports `ADMIN_AUTH_PASSWORD_ITERATIONS`
- order 149: `ADMIN_AUTH_MAX_ACTIVE_SESSIONS` (constant), lines 3977-3977, exports `ADMIN_AUTH_MAX_ACTIVE_SESSIONS`
- order 1191: `ADMIN_SKILLS_REVIEW_HTML` (constant), lines 118745-118746, exports `ADMIN_SKILLS_REVIEW_HTML`
- order 1192: `ADMIN_SKILLS_REVIEW_CSS` (constant), lines 118747-118747, exports `ADMIN_SKILLS_REVIEW_CSS`
- order 1193: `ADMIN_SKILLS_REVIEW_JS` (constant), lines 118748-118748, exports `ADMIN_SKILLS_REVIEW_JS`

### `agent/background.py`

- order 1022: `BackgroundManager` (class), lines 23929-24554, exports `BackgroundManager`

### `agent/bus.py`

- order 1023: `MessageBus` (class), lines 24555-24620, exports `MessageBus`

### `agent/errors.py`

- order 858: `CircuitBreakerTriggered` (class), lines 12316-12319, exports `CircuitBreakerTriggered`

### `agent/events.py`

- order 978: `EventHub` (class), lines 17209-17263, exports `EventHub`

### `agent/process.py`

- order 767: `subprocess_text_encodings` (function), lines 8298-8319, exports `subprocess_text_encodings`
- order 768: `decode_subprocess_bytes` (function), lines 8320-8346, exports `decode_subprocess_bytes`
- order 769: `run_subprocess_text` (function), lines 8347-8369, exports `run_subprocess_text`
- order 770: `windows_utf8_shell_command` (function), lines 8370-8376, exports `windows_utf8_shell_command`
- order 771: `shell_process_invocation` (function), lines 8377-8387, exports `shell_process_invocation`
- order 772: `join_shell_task_command` (function), lines 8388-8399, exports `join_shell_task_command`
- order 1021: `UserProcessManager` (class), lines 23569-23928, exports `UserProcessManager`

### `agent/tasks.py`

- order 1019: `TaskManager` (class), lines 23428-23562, exports `TaskManager`

### `agent/todo.py`

- order 979: `TodoManager` (class), lines 17264-17624, exports `TodoManager`

### `agent/tools.py`

- order 973: `_ask_user_option_rows` (function), lines 17088-17121, exports `_ask_user_option_rows`
- order 974: `_ask_user_option_value` (function), lines 17122-17127, exports `_ask_user_option_value`
- order 1047: `tool_def` (function), lines 28757-28770, exports `tool_def`
- order 1048: `TOOLS` (constant), lines 28771-29318, exports `TOOLS`
- order 1049: `TOOL_REQUIRED_ARGS` (constant), lines 29319-29320, exports `TOOL_REQUIRED_ARGS`
- order 1050: `TOOL_SPEC_BY_NAME` (constant), lines 29321-29321, exports `TOOL_SPEC_BY_NAME`
- order 1051: `_for_29322` (statement), lines 29322-29331, exports `_tool`, `_fn`, `_name`, `_required`
- order 1052: `TOOL_NAME_FUZZY_MAP` (constant), lines 29332-29333, exports `TOOL_NAME_FUZZY_MAP`
- order 1053: `_for_29334` (statement), lines 29334-29337, exports `_name`, `_key`
- order 1054: `_for_29339` (statement), lines 29338-29355, exports `_alias`, `_target`
- order 1055: `is_todo_resume_tool_name` (function), lines 29356-29372, exports `is_todo_resume_tool_name`
- order 1056: `canonicalize_tool_name` (function), lines 29373-29391, exports `canonicalize_tool_name`
- order 1057: `filter_tool_specs_for_runtime` (function), lines 29392-29407, exports `filter_tool_specs_for_runtime`
- order 1058: `DEVELOPER_TOOL_DROP` (constant), lines 29408-29418, exports `DEVELOPER_TOOL_DROP`
- order 1059: `AGENT_TOOL_ALLOWLIST` (constant), lines 29419-29482, exports `AGENT_TOOL_ALLOWLIST`

### `agent/worktree.py`

- order 1024: `WorktreeManager` (class), lines 24621-24833, exports `WorktreeManager`

### `app/context.py`

- order 1194: `AppContext` (class), lines 118749-129628, exports `AppContext`

### `app/main.py`

- order 1210: `main` (function), lines 136610-138558, exports `main`
- order 1211: `_main_guard_138560` (main_guard), lines 138559-138561, exports —

### `app/services.py`

- order 1196: `TelemetryStore` (class), lines 129669-130044, exports `TelemetryStore`
- order 1197: `ApplicationRegistry` (class), lines 130045-130854, exports `ApplicationRegistry`

### `collaboration/core.py`

- order 93: `_now` (function), lines 531-534, exports `_now`
- order 94: `_json` (function), lines 535-538, exports `_json`
- order 95: `_load_json` (function), lines 539-545, exports `_load_json`
- order 96: `_b64_token` (function), lines 546-549, exports `_b64_token`
- order 97: `_branch_label` (function), lines 550-558, exports `_branch_label`
- order 98: `_digest` (function), lines 559-562, exports `_digest`
- order 99: `_password_hash` (function), lines 563-566, exports `_password_hash`
- order 100: `_normalize_ip` (function), lines 567-576, exports `_normalize_ip`
- order 101: `_normalize_name` (function), lines 577-583, exports `_normalize_name`
- order 102: `_COLLAB_PUBLIC_SECRET_PATTERNS` (assignment), lines 584-595, exports `_COLLAB_PUBLIC_SECRET_PATTERNS`
- order 103: `_collaboration_public_text` (function), lines 596-626, exports `_collaboration_public_text`
- order 104: `_collaboration_task_objective` (function), lines 627-651, exports `_collaboration_task_objective`
- order 105: `_collaboration_task_title` (function), lines 652-659, exports `_collaboration_task_title`
- order 106: `_collaboration_task_key` (function), lines 660-666, exports `_collaboration_task_key`
- order 107: `_collaboration_plan_steps` (function), lines 667-685, exports `_collaboration_plan_steps`
- order 108: `CollaborationError` (class), lines 686-693, exports `CollaborationError`
- order 109: `CollaborationPrincipal` (class), lines 694-704, exports `CollaborationPrincipal`
- order 110: `_normalize_operation` (function), lines 705-738, exports `_normalize_operation`
- order 111: `operation_input_length` (function), lines 739-742, exports `operation_input_length`
- order 112: `apply_text_operation` (function), lines 743-765, exports `apply_text_operation`
- order 113: `transform_text_operation` (function), lines 766-842, exports `transform_text_operation`
- order 114: `CollaborationStore` (class), lines 843-3558, exports `CollaborationStore`
- order 115: `CollaborationWriteCoordinator` (class), lines 3559-3772, exports `CollaborationWriteCoordinator`

### `collaboration/watcher.py`

- order 1208: `collaboration_file_watcher_loop` (function), lines 136517-136591, exports `collaboration_file_watcher_loop`
- order 1209: `collaboration_watcher_health` (function), lines 136592-136609, exports `collaboration_watcher_health`

### `config/bootstrap.py`

- order 73: `_EMBEDDED_LIQUID_KERNEL_PACKAGE_B64` (assignment), lines 123-434, exports `_EMBEDDED_LIQUID_KERNEL_PACKAGE_B64`
- order 74: `_ensure_embedded_liquid_kernel_package` (function), lines 435-481, exports `_ensure_embedded_liquid_kernel_package`
- order 77: `_ensure_liquid_kernel_sqlite_lifecycle` (function), lines 490-505, exports `_ensure_liquid_kernel_sqlite_lifecycle`
- order 934: `_liquid_kernel_history_present` (function), lines 14936-14940, exports `_liquid_kernel_history_present`
- order 935: `prepare_liquid_kernel_runtime` (function), lines 14941-14970, exports `prepare_liquid_kernel_runtime`
- order 936: `_persist_liquid_kernel_bootstrap` (function), lines 14971-14984, exports `_persist_liquid_kernel_bootstrap`

### `config/constants.py`

- order 75: `LIQUID_KERNEL_PACKAGE_STATUS` (constant), lines 482-483, exports `LIQUID_KERNEL_PACKAGE_STATUS`
- order 79: `_call_ensure_liquid_kernel_sqlite_lifecycle_514` (expression), lines 513-514, exports —
- order 80: `COLLAB_DB_FILENAME` (constant), lines 515-518, exports `COLLAB_DB_FILENAME`
- order 81: `COLLAB_SESSION_TTL_SECONDS` (constant), lines 519-519, exports `COLLAB_SESSION_TTL_SECONDS`
- order 82: `COLLAB_PRESENCE_TTL_SECONDS` (constant), lines 520-520, exports `COLLAB_PRESENCE_TTL_SECONDS`
- order 83: `COLLAB_PASSWORD_ITERATIONS` (constant), lines 521-521, exports `COLLAB_PASSWORD_ITERATIONS`
- order 84: `COLLAB_MAX_AVATAR_BYTES` (constant), lines 522-522, exports `COLLAB_MAX_AVATAR_BYTES`
- order 85: `COLLAB_MAX_TEXT_BYTES` (constant), lines 523-523, exports `COLLAB_MAX_TEXT_BYTES`
- order 86: `COLLAB_DELETE_RETENTION_DAYS` (constant), lines 524-524, exports `COLLAB_DELETE_RETENTION_DAYS`
- order 87: `COLLAB_EVENT_RETENTION` (constant), lines 525-525, exports `COLLAB_EVENT_RETENTION`
- order 88: `COLLAB_AGENT_STALE_SECONDS` (constant), lines 526-526, exports `COLLAB_AGENT_STALE_SECONDS`
- order 89: `COLLAB_AGENT_HEARTBEAT_INTERVAL_SECONDS` (constant), lines 527-527, exports `COLLAB_AGENT_HEARTBEAT_INTERVAL_SECONDS`
- order 90: `COLLAB_EXTERNAL_WRITE_SETTLE_SECONDS` (constant), lines 528-528, exports `COLLAB_EXTERNAL_WRITE_SETTLE_SECONDS`
- order 91: `COLLAB_EXTERNAL_WRITE_CONFIRMATIONS` (constant), lines 529-529, exports `COLLAB_EXTERNAL_WRITE_CONFIRMATIONS`
- order 92: `COLLAB_SCHEMA_VERSION` (constant), lines 530-530, exports `COLLAB_SCHEMA_VERSION`
- order 116: `COLLAB_INDEX_HTML` (constant), lines 3773-3844, exports `COLLAB_INDEX_HTML`
- order 117: `COLLAB_CSS` (constant), lines 3845-3852, exports `COLLAB_CSS`
- order 118: `COLLAB_JS` (constant), lines 3853-3893, exports `COLLAB_JS`
- order 124: `APP_VERSION` (constant), lines 3915-3915, exports `APP_VERSION`
- order 133: `IDE_AUTH_FILENAME` (constant), lines 3924-3924, exports `IDE_AUTH_FILENAME`
- order 134: `IDE_AUTH_SESSION_TTL_SECONDS` (constant), lines 3925-3925, exports `IDE_AUTH_SESSION_TTL_SECONDS`
- order 135: `IDE_AUTH_MAX_ACTIVE_SESSIONS` (constant), lines 3926-3926, exports `IDE_AUTH_MAX_ACTIVE_SESSIONS`
- order 136: `IDE_DEVICE_SECRET_MIN_BYTES` (constant), lines 3927-3927, exports `IDE_DEVICE_SECRET_MIN_BYTES`
- order 137: `IDE_DEVICE_LABEL_MAX_CHARS` (constant), lines 3928-3928, exports `IDE_DEVICE_LABEL_MAX_CHARS`
- order 138: `IDE_DEVICE_PAIRING_TTL_SECONDS` (constant), lines 3929-3929, exports `IDE_DEVICE_PAIRING_TTL_SECONDS`
- order 139: `IDE_WORKBENCH_STATE_FILENAME` (constant), lines 3930-3930, exports `IDE_WORKBENCH_STATE_FILENAME`
- order 140: `IDE_PROMPT_ENHANCEMENT_BUDGETS` (constant), lines 3931-3968, exports `IDE_PROMPT_ENHANCEMENT_BUDGETS`
- order 141: `IDE_EXTENSIONS_DIRNAME` (constant), lines 3969-3969, exports `IDE_EXTENSIONS_DIRNAME`
- order 163: `LONG_OUTPUT_MODEL_PAGE_CHARS` (constant), lines 4272-4272, exports `LONG_OUTPUT_MODEL_PAGE_CHARS`
- order 164: `LONG_OUTPUT_UI_PAGE_CHARS` (constant), lines 4273-4273, exports `LONG_OUTPUT_UI_PAGE_CHARS`
- order 165: `LONG_OUTPUT_UI_PREVIEW_MAX_PAGES` (constant), lines 4274-4274, exports `LONG_OUTPUT_UI_PREVIEW_MAX_PAGES`
- order 166: `LONG_OUTPUT_LISTING_OFFLOAD_CHARS` (constant), lines 4275-4275, exports `LONG_OUTPUT_LISTING_OFFLOAD_CHARS`
- order 167: `LONG_OUTPUT_READ_PAGE_LINES` (constant), lines 4276-4276, exports `LONG_OUTPUT_READ_PAGE_LINES`
- order 168: `LONG_OUTPUT_READ_PAGE_MAX_CHARS` (constant), lines 4277-4277, exports `LONG_OUTPUT_READ_PAGE_MAX_CHARS`
- order 169: `LONG_OUTPUT_TEMP_MAX_FILES` (constant), lines 4278-4278, exports `LONG_OUTPUT_TEMP_MAX_FILES`
- order 170: `READ_FILE_DEFAULT_MAX_CHARS` (constant), lines 4279-4279, exports `READ_FILE_DEFAULT_MAX_CHARS`
- order 171: `READ_FILE_HARD_MAX_CHARS` (constant), lines 4280-4280, exports `READ_FILE_HARD_MAX_CHARS`
- order 172: `READ_FILE_OVERVIEW_HEAD_LINES` (constant), lines 4281-4281, exports `READ_FILE_OVERVIEW_HEAD_LINES`
- order 173: `READ_FILE_SEARCH_MAX_MATCHES` (constant), lines 4282-4282, exports `READ_FILE_SEARCH_MAX_MATCHES`
- order 178: `CODE_ADMIN_PORT_OFFSET` (constant), lines 4287-4287, exports `CODE_ADMIN_PORT_OFFSET`
- order 180: `IDE_PORT_OFFSET` (constant), lines 4289-4292, exports `IDE_PORT_OFFSET`
- order 181: `IDE_DEFAULT_PORT` (constant), lines 4293-4293, exports `IDE_DEFAULT_PORT`
- order 182: `COLLAB_PORT_OFFSET` (constant), lines 4294-4294, exports `COLLAB_PORT_OFFSET`
- order 184: `DEFAULT_WEB_SEARCH_ENABLED` (constant), lines 4296-4296, exports `DEFAULT_WEB_SEARCH_ENABLED`
- order 189: `DEFAULT_USER_MEMORY_MODE` (constant), lines 4301-4301, exports `DEFAULT_USER_MEMORY_MODE`
- order 197: `AGENT_WEB_SEARCH_USER_AGENT` (constant), lines 4312-4312, exports `AGENT_WEB_SEARCH_USER_AGENT`
- order 198: `AGENT_WEB_SEARCH_DEFAULT_MAX_RESULTS` (constant), lines 4313-4313, exports `AGENT_WEB_SEARCH_DEFAULT_MAX_RESULTS`
- order 199: `AGENT_WEB_SEARCH_DEFAULT_MAX_PAGES` (constant), lines 4314-4314, exports `AGENT_WEB_SEARCH_DEFAULT_MAX_PAGES`
- order 200: `AGENT_WEB_SEARCH_HARD_MAX_PAGES` (constant), lines 4315-4315, exports `AGENT_WEB_SEARCH_HARD_MAX_PAGES`
- order 201: `AGENT_WEB_SEARCH_DEFAULT_DEPTH` (constant), lines 4316-4316, exports `AGENT_WEB_SEARCH_DEFAULT_DEPTH`
- order 202: `AGENT_WEB_SEARCH_HARD_DEPTH` (constant), lines 4317-4317, exports `AGENT_WEB_SEARCH_HARD_DEPTH`
- order 203: `AGENT_WEB_SEARCH_FETCH_TIMEOUT` (constant), lines 4318-4318, exports `AGENT_WEB_SEARCH_FETCH_TIMEOUT`
- order 204: `AGENT_WEB_SEARCH_TOOL_SOFT_TIMEOUT` (constant), lines 4319-4319, exports `AGENT_WEB_SEARCH_TOOL_SOFT_TIMEOUT`
- order 205: `AGENT_WEB_SEARCH_MAX_PAGE_BYTES` (constant), lines 4320-4320, exports `AGENT_WEB_SEARCH_MAX_PAGE_BYTES`
- order 206: `AGENT_WEB_SEARCH_MAX_TEXT_CHARS` (constant), lines 4321-4321, exports `AGENT_WEB_SEARCH_MAX_TEXT_CHARS`
- order 207: `AGENT_WEB_SEARCH_PUBLIC_DISCOVERY_ENABLED` (constant), lines 4322-4324, exports `AGENT_WEB_SEARCH_PUBLIC_DISCOVERY_ENABLED`
- order 208: `AGENT_WEB_SEARCH_PUBLIC_FEED_URL` (constant), lines 4325-4325, exports `AGENT_WEB_SEARCH_PUBLIC_FEED_URL`
- order 209: `AGENT_WEB_SEARCH_PUBLIC_FEED_MAX_BYTES` (constant), lines 4326-4326, exports `AGENT_WEB_SEARCH_PUBLIC_FEED_MAX_BYTES`
- order 210: `AGENT_WEB_SEARCH_LOCAL_GRAPH_MAX_NODES` (constant), lines 4327-4327, exports `AGENT_WEB_SEARCH_LOCAL_GRAPH_MAX_NODES`
- order 211: `AGENT_WEB_SEARCH_LOCAL_GRAPH_MAX_EDGES` (constant), lines 4328-4328, exports `AGENT_WEB_SEARCH_LOCAL_GRAPH_MAX_EDGES`
- order 212: `AGENT_WEB_SEARCH_LOCAL_GRAPH_EDGE_SCAN_MULTIPLIER` (constant), lines 4329-4329, exports `AGENT_WEB_SEARCH_LOCAL_GRAPH_EDGE_SCAN_MULTIPLIER`
- order 213: `AGENT_WEB_SEARCH_LOCAL_GRAPH_PAGERANK_ITERATIONS` (constant), lines 4330-4330, exports `AGENT_WEB_SEARCH_LOCAL_GRAPH_PAGERANK_ITERATIONS`
- order 214: `AGENT_WEB_SEARCH_LOCAL_GRAPH_PAGERANK_DAMPING` (constant), lines 4331-4331, exports `AGENT_WEB_SEARCH_LOCAL_GRAPH_PAGERANK_DAMPING`
- order 215: `AGENT_WEB_SEARCH_LOCAL_GRAPH_AUTHORITY_BONUS_MAX` (constant), lines 4332-4332, exports `AGENT_WEB_SEARCH_LOCAL_GRAPH_AUTHORITY_BONUS_MAX`
- order 225: `CODE_CHUNK_CHARS` (constant), lines 4354-4354, exports `CODE_CHUNK_CHARS`
- order 226: `CODE_CHUNK_OVERLAP` (constant), lines 4355-4355, exports `CODE_CHUNK_OVERLAP`
- order 227: `CODE_MAX_CHUNKS_PER_DOC` (constant), lines 4356-4356, exports `CODE_MAX_CHUNKS_PER_DOC`
- order 228: `CODE_SOURCE_ANALYSIS_MAX_CHARS` (constant), lines 4357-4366, exports `CODE_SOURCE_ANALYSIS_MAX_CHARS`
- order 269: `CODE_IMPORT_WORKER_COUNT` (constant), lines 4435-4438, exports `CODE_IMPORT_WORKER_COUNT`
- order 271: `CODE_PARSE_TIMEOUT_SECONDS` (constant), lines 4443-4446, exports `CODE_PARSE_TIMEOUT_SECONDS`
- order 272: `DEFAULT_CONTEXT_TOKEN_LIMIT` (constant), lines 4447-4447, exports `DEFAULT_CONTEXT_TOKEN_LIMIT`
- order 273: `TOKEN_THRESHOLD` (constant), lines 4448-4448, exports `TOKEN_THRESHOLD`
- order 274: `CONTEXT_AUTO_COMPACT_RESERVE_RATIO` (constant), lines 4449-4452, exports `CONTEXT_AUTO_COMPACT_RESERVE_RATIO`
- order 275: `CONTEXT_ESTIMATE_SAFETY_MULTIPLIER` (constant), lines 4453-4456, exports `CONTEXT_ESTIMATE_SAFETY_MULTIPLIER`
- order 276: `CONTEXT_USAGE_CALIBRATION_MAX` (constant), lines 4457-4460, exports `CONTEXT_USAGE_CALIBRATION_MAX`
- order 277: `CONTEXT_ACTUAL_USAGE_RECENT_SECONDS` (constant), lines 4461-4464, exports `CONTEXT_ACTUAL_USAGE_RECENT_SECONDS`
- order 278: `LARGE_FILE_AUTO_PAGE_BYTES` (constant), lines 4465-4468, exports `LARGE_FILE_AUTO_PAGE_BYTES`
- order 279: `LARGE_FILE_AUTO_PAGE_LINES` (constant), lines 4469-4472, exports `LARGE_FILE_AUTO_PAGE_LINES`
- order 280: `LARGE_SOURCE_UPLOAD_EXCERPT_CHARS` (constant), lines 4473-4476, exports `LARGE_SOURCE_UPLOAD_EXCERPT_CHARS`
- order 281: `CHAT_UPLOAD_PARSE_QUEUE_MAX` (constant), lines 4477-4480, exports `CHAT_UPLOAD_PARSE_QUEUE_MAX`
- order 282: `CHAT_UPLOAD_PARSE_TIMEOUT_SECONDS` (constant), lines 4481-4484, exports `CHAT_UPLOAD_PARSE_TIMEOUT_SECONDS`
- order 283: `CHAT_UPLOAD_INLINE_TEXT_BYTES` (constant), lines 4485-4488, exports `CHAT_UPLOAD_INLINE_TEXT_BYTES`
- order 284: `CHAT_UPLOAD_PARSE_MAX_BYTES` (constant), lines 4489-4495, exports `CHAT_UPLOAD_PARSE_MAX_BYTES`
- order 285: `CHAT_UPLOAD_ZIP_ENTRY_MAX_BYTES` (constant), lines 4496-4502, exports `CHAT_UPLOAD_ZIP_ENTRY_MAX_BYTES`
- order 286: `CHAT_UPLOAD_TEXT_CONTEXT_CHARS` (constant), lines 4503-4506, exports `CHAT_UPLOAD_TEXT_CONTEXT_CHARS`
- order 287: `CHAT_UPLOAD_PROMPT_MAX_FILES` (constant), lines 4507-4510, exports `CHAT_UPLOAD_PROMPT_MAX_FILES`
- order 288: `CHAT_UPLOAD_PROMPT_MAX_CHARS` (constant), lines 4511-4514, exports `CHAT_UPLOAD_PROMPT_MAX_CHARS`
- order 289: `CHAT_UPLOAD_PROMPT_PER_FILE_CHARS` (constant), lines 4515-4518, exports `CHAT_UPLOAD_PROMPT_PER_FILE_CHARS`
- order 290: `CHAT_UPLOAD_FRONTEND_WAIT_MS` (constant), lines 4519-4522, exports `CHAT_UPLOAD_FRONTEND_WAIT_MS`
- order 291: `CHAT_UPLOAD_AUTO_LIBRARY_INGEST` (constant), lines 4523-4526, exports `CHAT_UPLOAD_AUTO_LIBRARY_INGEST`
- order 292: `CHAT_UPLOAD_INGEST_QUEUE_MAX` (constant), lines 4527-4530, exports `CHAT_UPLOAD_INGEST_QUEUE_MAX`
- order 293: `SESSION_SUBMIT_LOCK_TIMEOUT_SECONDS` (constant), lines 4531-4534, exports `SESSION_SUBMIT_LOCK_TIMEOUT_SECONDS`
- order 294: `SESSION_DEFERRED_START_QUEUE_MAX` (constant), lines 4535-4538, exports `SESSION_DEFERRED_START_QUEUE_MAX`
- order 295: `SESSION_SUBMISSION_DEDUPE_MAX` (constant), lines 4539-4539, exports `SESSION_SUBMISSION_DEDUPE_MAX`
- order 296: `SESSION_SUBMISSION_DEDUPE_SECONDS` (constant), lines 4540-4540, exports `SESSION_SUBMISSION_DEDUPE_SECONDS`
- order 297: `SCHEDULER_SUBMISSION_DEDUPE_MAX` (constant), lines 4541-4541, exports `SCHEDULER_SUBMISSION_DEDUPE_MAX`
- order 298: `FAST_START_LOCAL_CLASSIFICATION` (constant), lines 4542-4544, exports `FAST_START_LOCAL_CLASSIFICATION`
- order 299: `FAST_START_LOCAL_TITLE` (constant), lines 4545-4547, exports `FAST_START_LOCAL_TITLE`
- order 300: `AUTO_TITLE_MODEL_REFINE` (constant), lines 4548-4550, exports `AUTO_TITLE_MODEL_REFINE`
- order 301: `AUTO_TITLE_MODEL_TIMEOUT_SECONDS` (constant), lines 4551-4554, exports `AUTO_TITLE_MODEL_TIMEOUT_SECONDS`
- order 302: `AUTO_TITLE_MODEL_RETRY_COOLDOWN_SECONDS` (constant), lines 4555-4561, exports `AUTO_TITLE_MODEL_RETRY_COOLDOWN_SECONDS`
- order 303: `FAST_START_DEFER_CAPABILITY_PROBE` (constant), lines 4562-4564, exports `FAST_START_DEFER_CAPABILITY_PROBE`
- order 304: `SESSION_RUNTIME_MESSAGE_WINDOW` (constant), lines 4565-4565, exports `SESSION_RUNTIME_MESSAGE_WINDOW`
- order 305: `SESSION_RUNTIME_ACTIVITY_WINDOW` (constant), lines 4566-4566, exports `SESSION_RUNTIME_ACTIVITY_WINDOW`
- order 306: `SESSION_RUNTIME_OPERATION_WINDOW` (constant), lines 4567-4567, exports `SESSION_RUNTIME_OPERATION_WINDOW`
- order 307: `SESSION_RUNTIME_UPLOAD_WINDOW` (constant), lines 4568-4568, exports `SESSION_RUNTIME_UPLOAD_WINDOW`
- order 308: `LITE_SNAPSHOT_MAX_BYTES` (constant), lines 4569-4572, exports `LITE_SNAPSHOT_MAX_BYTES`
- order 309: `LITE_SNAPSHOT_MESSAGES_BYTES` (constant), lines 4573-4573, exports `LITE_SNAPSHOT_MESSAGES_BYTES`
- order 310: `LITE_SNAPSHOT_FEED_BYTES` (constant), lines 4574-4574, exports `LITE_SNAPSHOT_FEED_BYTES`
- order 311: `LITE_SNAPSHOT_OPERATIONS_BYTES` (constant), lines 4575-4575, exports `LITE_SNAPSHOT_OPERATIONS_BYTES`
- order 312: `IDE_AGENT_STATE_MAX_BYTES` (constant), lines 4576-4579, exports `IDE_AGENT_STATE_MAX_BYTES`
- order 313: `IDE_AGENT_FEED_BYTES` (constant), lines 4580-4580, exports `IDE_AGENT_FEED_BYTES`
- order 314: `IDE_AGENT_OPERATIONS_BYTES` (constant), lines 4581-4581, exports `IDE_AGENT_OPERATIONS_BYTES`
- order 315: `SESSION_WATCHDOG_INTERVAL_SECONDS` (constant), lines 4582-4585, exports `SESSION_WATCHDOG_INTERVAL_SECONDS`
- order 316: `SESSION_HEARTBEAT_STALE_SECONDS` (constant), lines 4586-4589, exports `SESSION_HEARTBEAT_STALE_SECONDS`
- order 317: `SESSION_LIST_DEFAULT_LIMIT` (constant), lines 4590-4593, exports `SESSION_LIST_DEFAULT_LIMIT`
- order 318: `SESSION_INDEX_SYNC_SNAPSHOT_MAX` (constant), lines 4594-4597, exports `SESSION_INDEX_SYNC_SNAPSHOT_MAX`
- order 319: `SESSION_INDEX_JOURNAL_COMPACT_RECORDS` (constant), lines 4598-4601, exports `SESSION_INDEX_JOURNAL_COMPACT_RECORDS`
- order 320: `SESSION_INDEX_JOURNAL_COMPACT_BYTES` (constant), lines 4602-4605, exports `SESSION_INDEX_JOURNAL_COMPACT_BYTES`
- order 321: `SESSION_CATALOG_RECENT_MAX` (constant), lines 4606-4609, exports `SESSION_CATALOG_RECENT_MAX`
- order 322: `IDE_SESSION_LIST_DEFAULT_LIMIT` (constant), lines 4610-4613, exports `IDE_SESSION_LIST_DEFAULT_LIMIT`
- order 323: `IDLE_TIMEOUT` (constant), lines 4614-4614, exports `IDLE_TIMEOUT`
- order 324: `POLL_INTERVAL` (constant), lines 4615-4615, exports `POLL_INTERVAL`
- order 325: `SSE_HEARTBEAT_SECONDS` (constant), lines 4616-4616, exports `SSE_HEARTBEAT_SECONDS`
- order 326: `MODEL_CALL_PROGRESS_DELAY` (constant), lines 4617-4617, exports `MODEL_CALL_PROGRESS_DELAY`
- order 327: `MODEL_CALL_PROGRESS_INTERVAL` (constant), lines 4618-4618, exports `MODEL_CALL_PROGRESS_INTERVAL`
- order 328: `RUN_COMPLETION_SUMMARY_ENABLED` (constant), lines 4619-4622, exports `RUN_COMPLETION_SUMMARY_ENABLED`
- order 329: `LLM_HTTP_RETRY_MAX_ATTEMPTS` (constant), lines 4623-4626, exports `LLM_HTTP_RETRY_MAX_ATTEMPTS`
- order 330: `LLM_HTTP_RETRY_DELAY_SECONDS` (constant), lines 4627-4630, exports `LLM_HTTP_RETRY_DELAY_SECONDS`
- order 331: `LLM_HTTP_RETRY_MAX_SECONDS` (constant), lines 4631-4634, exports `LLM_HTTP_RETRY_MAX_SECONDS`
- order 332: `LLM_HTTP_RETRY_404_ON_VLLM` (constant), lines 4635-4638, exports `LLM_HTTP_RETRY_404_ON_VLLM`
- order 333: `LLM_HTTP_RETRY_STATUSES` (constant), lines 4639-4639, exports `LLM_HTTP_RETRY_STATUSES`
- order 334: `MAX_AGENT_ROUNDS` (constant), lines 4640-4640, exports `MAX_AGENT_ROUNDS`
- order 335: `MIN_AGENT_ROUNDS` (constant), lines 4641-4641, exports `MIN_AGENT_ROUNDS`
- order 336: `MAX_AGENT_ROUNDS_CAP` (constant), lines 4642-4642, exports `MAX_AGENT_ROUNDS_CAP`
- order 337: `REPEATED_TOOL_LOOP_THRESHOLD` (constant), lines 4643-4643, exports `REPEATED_TOOL_LOOP_THRESHOLD`
- order 338: `BASH_READ_LOOP_THRESHOLD` (constant), lines 4644-4644, exports `BASH_READ_LOOP_THRESHOLD`
- order 339: `READ_FILE_LOOP_THRESHOLD` (constant), lines 4645-4645, exports `READ_FILE_LOOP_THRESHOLD`
- order 340: `READ_FILE_LOOP_DISTINCT_SOFT_LIMIT` (constant), lines 4646-4646, exports `READ_FILE_LOOP_DISTINCT_SOFT_LIMIT`
- order 341: `READ_FILE_COMPACT_PIN_DISTINCT` (constant), lines 4647-4647, exports `READ_FILE_COMPACT_PIN_DISTINCT`
- order 342: `READ_FILE_COMPACT_PIN_MAX_CHARS` (constant), lines 4648-4648, exports `READ_FILE_COMPACT_PIN_MAX_CHARS`
- order 343: `READ_CONTEXT_REGISTRY_MAX` (constant), lines 4649-4649, exports `READ_CONTEXT_REGISTRY_MAX`
- order 344: `READ_CONTEXT_PROMPT_MAX_ITEMS` (constant), lines 4650-4650, exports `READ_CONTEXT_PROMPT_MAX_ITEMS`
- order 345: `READ_CONTEXT_PROMPT_MAX_CHARS` (constant), lines 4651-4651, exports `READ_CONTEXT_PROMPT_MAX_CHARS`
- order 346: `READ_CONTEXT_SUMMARY_MAX_CHARS` (constant), lines 4652-4652, exports `READ_CONTEXT_SUMMARY_MAX_CHARS`
- order 347: `READ_CONTEXT_SHARED_MAX_ITEMS` (constant), lines 4653-4653, exports `READ_CONTEXT_SHARED_MAX_ITEMS`
- order 348: `READ_CONTEXT_POLICY_CHOICES` (constant), lines 4654-4654, exports `READ_CONTEXT_POLICY_CHOICES`
- order 349: `DEFAULT_READ_CONTEXT_POLICY` (constant), lines 4655-4655, exports `DEFAULT_READ_CONTEXT_POLICY`
- order 350: `READ_CONTEXT_CACHE_SEARCH_MAX_BYTES` (constant), lines 4656-4662, exports `READ_CONTEXT_CACHE_SEARCH_MAX_BYTES`
- order 351: `READ_CONTEXT_CACHE_SEARCH_MAX_MATCHES` (constant), lines 4663-4663, exports `READ_CONTEXT_CACHE_SEARCH_MAX_MATCHES`
- order 352: `READ_CONTEXT_CACHE_SNIPPET_CHARS` (constant), lines 4664-4664, exports `READ_CONTEXT_CACHE_SNIPPET_CHARS`
- order 353: `READ_CONTEXT_CACHE_LINE_CONTEXT` (constant), lines 4665-4665, exports `READ_CONTEXT_CACHE_LINE_CONTEXT`
- order 354: `LONG_CONTENT_SOURCE_CACHE_MAX_BYTES` (constant), lines 4666-4672, exports `LONG_CONTENT_SOURCE_CACHE_MAX_BYTES`
- order 355: `LONG_CONTENT_SOURCE_CACHE_MAX_FILES` (constant), lines 4673-4676, exports `LONG_CONTENT_SOURCE_CACHE_MAX_FILES`
- order 356: `LONG_CONTENT_SYMBOL_MEMORY_MAX` (constant), lines 4677-4680, exports `LONG_CONTENT_SYMBOL_MEMORY_MAX`
- order 357: `TOOL_MEMORY_REGISTRY_MAX` (constant), lines 4681-4681, exports `TOOL_MEMORY_REGISTRY_MAX`
- order 358: `TOOL_MEMORY_PROMPT_MAX_ITEMS` (constant), lines 4682-4682, exports `TOOL_MEMORY_PROMPT_MAX_ITEMS`
- order 359: `TOOL_MEMORY_PROMPT_MAX_CHARS` (constant), lines 4683-4683, exports `TOOL_MEMORY_PROMPT_MAX_CHARS`
- order 360: `TOOL_MEMORY_SUMMARY_MAX_CHARS` (constant), lines 4684-4684, exports `TOOL_MEMORY_SUMMARY_MAX_CHARS`
- order 361: `TOOL_MEMORY_SHARED_MAX_ITEMS` (constant), lines 4685-4685, exports `TOOL_MEMORY_SHARED_MAX_ITEMS`
- order 362: `TOOL_MEMORY_COMPACT_PIN_DISTINCT` (constant), lines 4686-4686, exports `TOOL_MEMORY_COMPACT_PIN_DISTINCT`
- order 363: `TOOL_MEMORY_COMPACT_PIN_MAX_CHARS` (constant), lines 4687-4687, exports `TOOL_MEMORY_COMPACT_PIN_MAX_CHARS`
- order 364: `TOOL_MEMORY_POLICY_CHOICES` (constant), lines 4688-4688, exports `TOOL_MEMORY_POLICY_CHOICES`
- order 365: `DEFAULT_TOOL_MEMORY_POLICY` (constant), lines 4689-4689, exports `DEFAULT_TOOL_MEMORY_POLICY`
- order 366: `LONG_CONTENT_MEMORY_VERSION` (constant), lines 4690-4702, exports `LONG_CONTENT_MEMORY_VERSION`
- order 367: `LONG_CONTENT_MEMORY_MAX_ITEMS` (constant), lines 4703-4706, exports `LONG_CONTENT_MEMORY_MAX_ITEMS`
- order 368: `LONG_CONTENT_MEMORY_MAX_SEGMENTS` (constant), lines 4707-4710, exports `LONG_CONTENT_MEMORY_MAX_SEGMENTS`
- order 369: `LONG_CONTENT_TEXT_SEGMENT_LINES` (constant), lines 4711-4714, exports `LONG_CONTENT_TEXT_SEGMENT_LINES`
- order 370: `LONG_CONTENT_CODE_SEGMENT_LINES` (constant), lines 4715-4718, exports `LONG_CONTENT_CODE_SEGMENT_LINES`
- order 371: `LONG_CONTENT_CARD_CHARS` (constant), lines 4719-4722, exports `LONG_CONTENT_CARD_CHARS`
- order 372: `LONG_CONTENT_STRUCTURE_MAX_CHARS` (constant), lines 4723-4726, exports `LONG_CONTENT_STRUCTURE_MAX_CHARS`
- order 373: `LONG_CONTENT_SEMANTIC_ENABLED` (constant), lines 4727-4734, exports `LONG_CONTENT_SEMANTIC_ENABLED`
- order 374: `LONG_CONTENT_SEMANTIC_TIMEOUT_SECONDS` (constant), lines 4735-4738, exports `LONG_CONTENT_SEMANTIC_TIMEOUT_SECONDS`
- order 375: `LONG_CONTENT_SEMANTIC_MAX_INPUT_CHARS` (constant), lines 4739-4742, exports `LONG_CONTENT_SEMANTIC_MAX_INPUT_CHARS`
- order 376: `LONG_CONTENT_SEMANTIC_MAX_OUTPUT_TOKENS` (constant), lines 4743-4746, exports `LONG_CONTENT_SEMANTIC_MAX_OUTPUT_TOKENS`
- order 377: `LONG_CONTENT_SEMANTIC_MAX_KEY_POINTS` (constant), lines 4747-4747, exports `LONG_CONTENT_SEMANTIC_MAX_KEY_POINTS`
- order 378: `LONG_CONTENT_SEMANTIC_MAX_DEFINITIONS` (constant), lines 4748-4748, exports `LONG_CONTENT_SEMANTIC_MAX_DEFINITIONS`
- order 379: `LONG_CONTENT_SEMANTIC_MAX_RELATIONS` (constant), lines 4749-4749, exports `LONG_CONTENT_SEMANTIC_MAX_RELATIONS`
- order 380: `LONG_CONTENT_SEMANTIC_MAX_UNCERTAINTIES` (constant), lines 4750-4750, exports `LONG_CONTENT_SEMANTIC_MAX_UNCERTAINTIES`
- order 381: `LONG_CONTENT_SEMANTIC_MAX_EVIDENCE` (constant), lines 4751-4751, exports `LONG_CONTENT_SEMANTIC_MAX_EVIDENCE`
- order 382: `LONG_CONTENT_SEMANTIC_MAX_NEXT_SEGMENTS` (constant), lines 4752-4752, exports `LONG_CONTENT_SEMANTIC_MAX_NEXT_SEGMENTS`
- order 383: `LONG_CONTENT_SEMANTIC_MAX_COVERED` (constant), lines 4753-4753, exports `LONG_CONTENT_SEMANTIC_MAX_COVERED`
- order 384: `LONG_CONTENT_SEMANTIC_MAX_OPEN_QUESTIONS` (constant), lines 4754-4754, exports `LONG_CONTENT_SEMANTIC_MAX_OPEN_QUESTIONS`
- order 385: `LONG_CONTENT_SEMANTIC_MAX_REFRESHES` (constant), lines 4755-4758, exports `LONG_CONTENT_SEMANTIC_MAX_REFRESHES`
- order 386: `LONG_CONTENT_OBSERVATION_MAX` (constant), lines 4759-4762, exports `LONG_CONTENT_OBSERVATION_MAX`
- order 387: `LONG_CONTENT_OBSERVATION_MAX_RANGES` (constant), lines 4763-4763, exports `LONG_CONTENT_OBSERVATION_MAX_RANGES`
- order 388: `LONG_CONTENT_OBSERVATION_MAX_EXCERPTS` (constant), lines 4764-4764, exports `LONG_CONTENT_OBSERVATION_MAX_EXCERPTS`
- order 389: `LONG_CONTENT_OBSERVATION_EXCERPT_CHARS` (constant), lines 4765-4765, exports `LONG_CONTENT_OBSERVATION_EXCERPT_CHARS`
- order 390: `LONG_CONTENT_RELATED_SOURCE_MAX` (constant), lines 4766-4766, exports `LONG_CONTENT_RELATED_SOURCE_MAX`
- order 391: `SHELL_SOURCE_CANDIDATE_MAX` (constant), lines 4767-4767, exports `SHELL_SOURCE_CANDIDATE_MAX`
- order 392: `LONG_CONTENT_TEXT_EXTS` (constant), lines 4768-4770, exports `LONG_CONTENT_TEXT_EXTS`
- order 393: `LONG_CONTENT_DATA_EXTS` (constant), lines 4771-4775, exports `LONG_CONTENT_DATA_EXTS`
- order 394: `DEFAULT_AUTO_TASK_LEVEL_CEILING` (constant), lines 4776-4776, exports `DEFAULT_AUTO_TASK_LEVEL_CEILING`
- order 395: `HARD_BREAK_TOOL_ERROR_THRESHOLD` (constant), lines 4777-4777, exports `HARD_BREAK_TOOL_ERROR_THRESHOLD`
- order 396: `HARD_BREAK_RECOVERY_ROUND_THRESHOLD` (constant), lines 4778-4780, exports `HARD_BREAK_RECOVERY_ROUND_THRESHOLD`
- order 397: `FUSED_FAULT_BREAK_THRESHOLD` (constant), lines 4781-4781, exports `FUSED_FAULT_BREAK_THRESHOLD`
- order 398: `STALL_SEVERITY_ESCALATION_THRESHOLD` (constant), lines 4782-4782, exports `STALL_SEVERITY_ESCALATION_THRESHOLD`
- order 399: `STALL_SEVERITY_WEIGHT_BASH_READ_LOOP` (constant), lines 4783-4783, exports `STALL_SEVERITY_WEIGHT_BASH_READ_LOOP`
- order 400: `STALL_SEVERITY_WEIGHT_REPEATED_TOOL` (constant), lines 4784-4784, exports `STALL_SEVERITY_WEIGHT_REPEATED_TOOL`
- order 401: `STALL_SEVERITY_WEIGHT_FAULT` (constant), lines 4785-4785, exports `STALL_SEVERITY_WEIGHT_FAULT`
- order 402: `STALL_SEVERITY_WEIGHT_RECOVERY_RETRY` (constant), lines 4786-4786, exports `STALL_SEVERITY_WEIGHT_RECOVERY_RETRY`
- order 403: `STALL_SEVERITY_WEIGHT_WATCHDOG` (constant), lines 4787-4787, exports `STALL_SEVERITY_WEIGHT_WATCHDOG`
- order 404: `STALL_SEVERITY_DECAY_ON_SUCCESS` (constant), lines 4788-4788, exports `STALL_SEVERITY_DECAY_ON_SUCCESS`
- order 405: `STALL_ESCALATION_MIN_LEVEL` (constant), lines 4789-4789, exports `STALL_ESCALATION_MIN_LEVEL`
- order 406: `STALL_PLAN_SYNTHESIS_MAX_TOKENS` (constant), lines 4790-4790, exports `STALL_PLAN_SYNTHESIS_MAX_TOKENS`
- order 407: `STALL_ESCALATION_CONTEXT_MAX_CHARS` (constant), lines 4791-4791, exports `STALL_ESCALATION_CONTEXT_MAX_CHARS`
- order 408: `MAX_RUN_SECONDS` (constant), lines 4792-4792, exports `MAX_RUN_SECONDS`
- order 409: `MIN_RUN_TIMEOUT_SECONDS` (constant), lines 4793-4793, exports `MIN_RUN_TIMEOUT_SECONDS`
- order 410: `MAX_RUN_TIMEOUT_SECONDS` (constant), lines 4794-4794, exports `MAX_RUN_TIMEOUT_SECONDS`
- order 411: `MIN_TIMEOUT_SECONDS` (constant), lines 4795-4795, exports `MIN_TIMEOUT_SECONDS`
- order 412: `MAX_TIMEOUT_SECONDS` (constant), lines 4796-4796, exports `MAX_TIMEOUT_SECONDS`
- order 413: `DEFAULT_TIMEOUT_SECONDS` (constant), lines 4797-4803, exports `DEFAULT_TIMEOUT_SECONDS`
- order 414: `DEFAULT_REQUEST_TIMEOUT` (constant), lines 4804-4804, exports `DEFAULT_REQUEST_TIMEOUT`
- order 415: `_SHELL_AUTO_CONFIRM_PATTERNS` (assignment), lines 4805-4820, exports `_SHELL_AUTO_CONFIRM_PATTERNS`
- order 416: `MIN_SHELL_COMMAND_TIMEOUT_SECONDS` (constant), lines 4821-4821, exports `MIN_SHELL_COMMAND_TIMEOUT_SECONDS`
- order 417: `MAX_SHELL_COMMAND_TIMEOUT_SECONDS` (constant), lines 4822-4822, exports `MAX_SHELL_COMMAND_TIMEOUT_SECONDS`
- order 418: `SHELL_TIMEOUT_MODES` (constant), lines 4823-4823, exports `SHELL_TIMEOUT_MODES`
- order 419: `_DEFAULT_SHELL_TIMEOUT_MODE_RAW` (assignment), lines 4824-4827, exports `_DEFAULT_SHELL_TIMEOUT_MODE_RAW`
- order 420: `DEFAULT_SHELL_TIMEOUT_MODE` (constant), lines 4828-4832, exports `DEFAULT_SHELL_TIMEOUT_MODE`
- order 421: `MIN_SHELL_ASYNC_HANDOFF_SECONDS` (constant), lines 4833-4833, exports `MIN_SHELL_ASYNC_HANDOFF_SECONDS`
- order 422: `MAX_SHELL_ASYNC_HANDOFF_SECONDS` (constant), lines 4834-4834, exports `MAX_SHELL_ASYNC_HANDOFF_SECONDS`
- order 423: `SHELL_FAILURE_GUIDANCE_SECONDS` (constant), lines 4835-4837, exports `SHELL_FAILURE_GUIDANCE_SECONDS`
- order 424: `DEFAULT_SHELL_ASYNC_HANDOFF_SECONDS` (constant), lines 4838-4852, exports `DEFAULT_SHELL_ASYNC_HANDOFF_SECONDS`
- order 425: `DEFAULT_SHELL_COMMAND_TIMEOUT_SECONDS` (constant), lines 4853-4867, exports `DEFAULT_SHELL_COMMAND_TIMEOUT_SECONDS`
- order 426: `DEFAULT_SINGLE_NO_PLAN_TODO_PROMPT` (constant), lines 4868-4882, exports `DEFAULT_SINGLE_NO_PLAN_TODO_PROMPT`
- order 427: `SINGLE_NO_PLAN_TODO_BOOTSTRAP_MAX_ATTEMPTS` (constant), lines 4883-4883, exports `SINGLE_NO_PLAN_TODO_BOOTSTRAP_MAX_ATTEMPTS`
- order 428: `AUTO_CONTINUE_BUDGET_DEFAULT` (constant), lines 4884-4884, exports `AUTO_CONTINUE_BUDGET_DEFAULT`
- order 429: `AGENT_MAX_OUTPUT_TOKENS` (constant), lines 4885-4885, exports `AGENT_MAX_OUTPUT_TOKENS`
- order 430: `OLLAMA_THINKING_TOOL_BUFFER` (constant), lines 4886-4886, exports `OLLAMA_THINKING_TOOL_BUFFER`
- order 431: `WATCHDOG_INTENT_NO_TOOL_THRESHOLD` (constant), lines 4887-4887, exports `WATCHDOG_INTENT_NO_TOOL_THRESHOLD`
- order 432: `WATCHDOG_REPEAT_NO_TOOL_THRESHOLD` (constant), lines 4888-4888, exports `WATCHDOG_REPEAT_NO_TOOL_THRESHOLD`
- order 433: `WATCHDOG_INTENT_NO_TOOL_THRESHOLD_SINGLE` (constant), lines 4889-4889, exports `WATCHDOG_INTENT_NO_TOOL_THRESHOLD_SINGLE`
- order 434: `WATCHDOG_REPEAT_NO_TOOL_THRESHOLD_SINGLE` (constant), lines 4890-4890, exports `WATCHDOG_REPEAT_NO_TOOL_THRESHOLD_SINGLE`
- order 435: `WATCHDOG_STATE_STALL_THRESHOLD` (constant), lines 4891-4891, exports `WATCHDOG_STATE_STALL_THRESHOLD`
- order 436: `WATCHDOG_CONTEXT_STALL_THRESHOLD` (constant), lines 4892-4892, exports `WATCHDOG_CONTEXT_STALL_THRESHOLD`
- order 437: `WATCHDOG_REPEAT_SIMILARITY_THRESHOLD` (constant), lines 4893-4893, exports `WATCHDOG_REPEAT_SIMILARITY_THRESHOLD`
- order 438: `WATCHDOG_CONTEXT_NEAR_RATIO` (constant), lines 4894-4894, exports `WATCHDOG_CONTEXT_NEAR_RATIO`
- order 439: `WATCHDOG_MAX_DECOMPOSE_STEPS` (constant), lines 4895-4895, exports `WATCHDOG_MAX_DECOMPOSE_STEPS`
- order 440: `WATCHDOG_STEP_MAX_ATTEMPTS` (constant), lines 4896-4896, exports `WATCHDOG_STEP_MAX_ATTEMPTS`
- order 441: `EMPTY_ACTION_MIN_CONTENT_CHARS` (constant), lines 4897-4897, exports `EMPTY_ACTION_MIN_CONTENT_CHARS`
- order 442: `EMPTY_ACTION_WAKEUP_RETRY_LIMIT` (constant), lines 4898-4898, exports `EMPTY_ACTION_WAKEUP_RETRY_LIMIT`
- order 443: `EMPTY_ACTION_INTERVENTION_THRESHOLD` (constant), lines 4899-4905, exports `EMPTY_ACTION_INTERVENTION_THRESHOLD`
- order 444: `EMPTY_ACTION_BOOTSTRAP_THINKING_GRACE_ROUNDS` (constant), lines 4906-4910, exports `EMPTY_ACTION_BOOTSTRAP_THINKING_GRACE_ROUNDS`
- order 445: `EMPTY_ACTION_RECOVERY_MAX_TOKENS` (constant), lines 4911-4911, exports `EMPTY_ACTION_RECOVERY_MAX_TOKENS`
- order 446: `THINKING_BUDGET_FORCE_RATIO` (constant), lines 4912-4912, exports `THINKING_BUDGET_FORCE_RATIO`
- order 447: `_TOOL_TIMEOUT_MAP` (assignment), lines 4913-4934, exports `_TOOL_TIMEOUT_MAP`
- order 448: `_DEFAULT_TOOL_TIMEOUT` (assignment), lines 4935-4935, exports `_DEFAULT_TOOL_TIMEOUT`
- order 449: `CONVERSATION_VISIBLE_TOOL_EVENTS` (constant), lines 4936-4948, exports `CONVERSATION_VISIBLE_TOOL_EVENTS`
- order 450: `PERSIST_ON_EVENT_TYPES` (constant), lines 4949-4967, exports `PERSIST_ON_EVENT_TYPES`
- order 451: `PERSIST_EVENT_MIN_INTERVAL_SECONDS` (constant), lines 4968-4968, exports `PERSIST_EVENT_MIN_INTERVAL_SECONDS`
- order 452: `TRUNCATION_CONTINUATION_MAX_PASSES` (constant), lines 4969-4969, exports `TRUNCATION_CONTINUATION_MAX_PASSES`
- order 453: `TRUNCATION_CONTINUATION_MAX_TOKENS` (constant), lines 4970-4970, exports `TRUNCATION_CONTINUATION_MAX_TOKENS`
- order 454: `TRUNCATION_CONTINUATION_TAIL_CHARS` (constant), lines 4971-4971, exports `TRUNCATION_CONTINUATION_TAIL_CHARS`
- order 455: `TRUNCATION_CONTINUATION_ECHO_CHARS` (constant), lines 4972-4972, exports `TRUNCATION_CONTINUATION_ECHO_CHARS`
- order 456: `TRUNCATION_OVERLAP_SCAN_CHARS` (constant), lines 4973-4973, exports `TRUNCATION_OVERLAP_SCAN_CHARS`
- order 457: `TRUNCATION_PAIR_SCAN_CHARS` (constant), lines 4974-4974, exports `TRUNCATION_PAIR_SCAN_CHARS`
- order 458: `TRUNCATION_LIVE_BUFFER_MAX_CHARS` (constant), lines 4975-4975, exports `TRUNCATION_LIVE_BUFFER_MAX_CHARS`
- order 459: `MIN_CONTEXT_TOKEN_LIMIT` (constant), lines 4976-4976, exports `MIN_CONTEXT_TOKEN_LIMIT`
- order 460: `COMPACT_TIER1_PCT` (constant), lines 4977-4978, exports `COMPACT_TIER1_PCT`
- order 461: `COMPACT_TIER2_PCT` (constant), lines 4979-4979, exports `COMPACT_TIER2_PCT`
- order 462: `COMPACT_TIER3_PCT` (constant), lines 4980-4980, exports `COMPACT_TIER3_PCT`
- order 463: `COMPACT_TIER1_ABS` (constant), lines 4981-4982, exports `COMPACT_TIER1_ABS`
- order 464: `COMPACT_TIER2_ABS` (constant), lines 4983-4983, exports `COMPACT_TIER2_ABS`
- order 465: `CONTEXT_COMPACT_INEFFECTIVE_COOLDOWN_SECONDS` (constant), lines 4984-4990, exports `CONTEXT_COMPACT_INEFFECTIVE_COOLDOWN_SECONDS`
- order 466: `FILE_BUFFER_CONTENT_THRESHOLD` (constant), lines 4991-4992, exports `FILE_BUFFER_CONTENT_THRESHOLD`
- order 467: `FILE_BUFFER_MAX_FILES` (constant), lines 4993-4993, exports `FILE_BUFFER_MAX_FILES`
- order 468: `AUTHORITATIVE_USER_GOAL_OPEN` (constant), lines 4994-4994, exports `AUTHORITATIVE_USER_GOAL_OPEN`
- order 469: `AUTHORITATIVE_USER_GOAL_CLOSE` (constant), lines 4995-4995, exports `AUTHORITATIVE_USER_GOAL_CLOSE`
- order 470: `AGENT_MSG_LIMIT_TIER0` (constant), lines 4996-4997, exports `AGENT_MSG_LIMIT_TIER0`
- order 471: `AGENT_MSG_LIMIT_TIER1` (constant), lines 4998-4998, exports `AGENT_MSG_LIMIT_TIER1`
- order 472: `AGENT_MSG_LIMIT_TIER2` (constant), lines 4999-4999, exports `AGENT_MSG_LIMIT_TIER2`
- order 473: `AGENT_MSG_LIMIT_TIER3` (constant), lines 5000-5000, exports `AGENT_MSG_LIMIT_TIER3`
- order 474: `AGENT_CTX_LIMIT_TIER0` (constant), lines 5001-5001, exports `AGENT_CTX_LIMIT_TIER0`
- order 475: `AGENT_CTX_LIMIT_TIER1` (constant), lines 5002-5002, exports `AGENT_CTX_LIMIT_TIER1`
- order 476: `AGENT_CTX_LIMIT_TIER2` (constant), lines 5003-5003, exports `AGENT_CTX_LIMIT_TIER2`
- order 477: `AGENT_CTX_LIMIT_TIER3` (constant), lines 5004-5004, exports `AGENT_CTX_LIMIT_TIER3`
- order 478: `MANAGER_CTX_LIMIT_TIER0` (constant), lines 5005-5005, exports `MANAGER_CTX_LIMIT_TIER0`
- order 479: `MANAGER_CTX_LIMIT_TIER1` (constant), lines 5006-5006, exports `MANAGER_CTX_LIMIT_TIER1`
- order 480: `MANAGER_CTX_LIMIT_TIER2` (constant), lines 5007-5007, exports `MANAGER_CTX_LIMIT_TIER2`
- order 481: `MANAGER_CTX_LIMIT_TIER3` (constant), lines 5008-5008, exports `MANAGER_CTX_LIMIT_TIER3`
- order 482: `MAX_CONTEXT_ARCHIVE_SEGMENTS` (constant), lines 5009-5009, exports `MAX_CONTEXT_ARCHIVE_SEGMENTS`
- order 483: `MAX_USER_BUBBLE_LOG` (constant), lines 5010-5011, exports `MAX_USER_BUBBLE_LOG`
- order 484: `MANAGER_INSTRUCTION_MAX_CHARS` (constant), lines 5012-5016, exports `MANAGER_INSTRUCTION_MAX_CHARS`
- order 485: `MANAGER_MOMENTUM_MAX_SKIPS` (constant), lines 5017-5022, exports `MANAGER_MOMENTUM_MAX_SKIPS`
- order 486: `MODEL_OUTPUT_RETRY_TIMES` (constant), lines 5023-5027, exports `MODEL_OUTPUT_RETRY_TIMES`
- order 487: `ARBITER_TRIGGER_MIN_CONTENT_CHARS` (constant), lines 5028-5028, exports `ARBITER_TRIGGER_MIN_CONTENT_CHARS`
- order 488: `ARBITER_VALID_PLANNING_STREAK_LIMIT` (constant), lines 5029-5029, exports `ARBITER_VALID_PLANNING_STREAK_LIMIT`
- order 489: `ARBITER_DEFAULT_TIMEOUT_SECONDS` (constant), lines 5030-5030, exports `ARBITER_DEFAULT_TIMEOUT_SECONDS`
- order 490: `ARBITER_DEFAULT_MAX_TOKENS` (constant), lines 5031-5031, exports `ARBITER_DEFAULT_MAX_TOKENS`
- order 491: `ARBITER_DEFAULT_TEMPERATURE` (constant), lines 5032-5032, exports `ARBITER_DEFAULT_TEMPERATURE`
- order 492: `LIVE_INPUT_DELAY_WRITE_ROUNDS` (constant), lines 5033-5033, exports `LIVE_INPUT_DELAY_WRITE_ROUNDS`
- order 493: `LIVE_INPUT_DELAY_TOOL_ROUNDS` (constant), lines 5034-5034, exports `LIVE_INPUT_DELAY_TOOL_ROUNDS`
- order 494: `LIVE_INPUT_DELAY_NORMAL_ROUNDS` (constant), lines 5035-5035, exports `LIVE_INPUT_DELAY_NORMAL_ROUNDS`
- order 495: `LIVE_INPUT_MAX_INJECTIONS` (constant), lines 5036-5036, exports `LIVE_INPUT_MAX_INJECTIONS`
- order 496: `LIVE_INPUT_REINJECT_INTERVAL` (constant), lines 5037-5037, exports `LIVE_INPUT_REINJECT_INTERVAL`
- order 497: `LIVE_INPUT_WEIGHT_BASE_DELAYED` (constant), lines 5038-5038, exports `LIVE_INPUT_WEIGHT_BASE_DELAYED`
- order 498: `LIVE_INPUT_WEIGHT_BASE_NORMAL` (constant), lines 5039-5039, exports `LIVE_INPUT_WEIGHT_BASE_NORMAL`
- order 499: `LIVE_INPUT_WEIGHT_STEP_DELAYED` (constant), lines 5040-5040, exports `LIVE_INPUT_WEIGHT_STEP_DELAYED`
- order 500: `LIVE_INPUT_WEIGHT_STEP_NORMAL` (constant), lines 5041-5041, exports `LIVE_INPUT_WEIGHT_STEP_NORMAL`
- order 502: `BENIGN_SOCKET_DEBUG_LOG_ENABLED` (constant), lines 5048-5054, exports `BENIGN_SOCKET_DEBUG_LOG_ENABLED`
- order 503: `BENIGN_SOCKET_LOG_INTERVAL_SECONDS` (constant), lines 5055-5055, exports `BENIGN_SOCKET_LOG_INTERVAL_SECONDS`
- order 504: `FINAL_SUMMARY_MIN_CHARS` (constant), lines 5056-5056, exports `FINAL_SUMMARY_MIN_CHARS`
- order 505: `FINAL_SUMMARY_STRICT_MIN_CHARS` (constant), lines 5057-5057, exports `FINAL_SUMMARY_STRICT_MIN_CHARS`
- order 506: `RUNTIME_CONTROL_HINT_PREFIXES` (constant), lines 5058-5078, exports `RUNTIME_CONTROL_HINT_PREFIXES`
- order 507: `UI_HIDDEN_RUNTIME_CONTROL_PREFIXES` (constant), lines 5079-5107, exports `UI_HIDDEN_RUNTIME_CONTROL_PREFIXES`
- order 508: `UI_PROJECTED_RUNTIME_CONTROL_TAGS` (constant), lines 5108-5130, exports `UI_PROJECTED_RUNTIME_CONTROL_TAGS`
- order 509: `UI_LEGACY_PROJECTED_RUNTIME_CONTROL_TAGS` (constant), lines 5131-5133, exports `UI_LEGACY_PROJECTED_RUNTIME_CONTROL_TAGS`
- order 510: `RETRY_RUNTIME_HINT_PREFIXES` (constant), lines 5134-5148, exports `RETRY_RUNTIME_HINT_PREFIXES`
- order 511: `EXECUTION_MODE_SINGLE` (constant), lines 5149-5149, exports `EXECUTION_MODE_SINGLE`
- order 512: `EXECUTION_MODE_SEQUENTIAL` (constant), lines 5150-5150, exports `EXECUTION_MODE_SEQUENTIAL`
- order 513: `EXECUTION_MODE_SYNC` (constant), lines 5151-5151, exports `EXECUTION_MODE_SYNC`
- order 514: `EXECUTION_MODE_CHOICES` (constant), lines 5152-5156, exports `EXECUTION_MODE_CHOICES`
- order 515: `AGENT_ROLES` (constant), lines 5157-5157, exports `AGENT_ROLES`
- order 516: `AGENT_BUBBLE_ROLES` (constant), lines 5158-5158, exports `AGENT_BUBBLE_ROLES`
- order 517: `AGENT_ROLE_LABELS` (constant), lines 5159-5165, exports `AGENT_ROLE_LABELS`
- order 518: `AGENT_ROLE_BUBBLE_COLORS` (constant), lines 5166-5172, exports `AGENT_ROLE_BUBBLE_COLORS`
- order 519: `BLACKBOARD_STATUSES` (constant), lines 5173-5182, exports `BLACKBOARD_STATUSES`
- order 520: `TASK_COMPLEXITY_LEVELS` (constant), lines 5183-5183, exports `TASK_COMPLEXITY_LEVELS`
- order 521: `TASK_COMPLEXITY_RANKS` (constant), lines 5184-5189, exports `TASK_COMPLEXITY_RANKS`
- order 522: `TASK_PROFILE_TYPES` (constant), lines 5190-5196, exports `TASK_PROFILE_TYPES`
- order 523: `TASK_LEVEL_CHOICES` (constant), lines 5197-5197, exports `TASK_LEVEL_CHOICES`
- order 524: `TASK_SCALE_PREFERENCES` (constant), lines 5198-5198, exports `TASK_SCALE_PREFERENCES`
- order 525: `SEMANTIC_CONFIDENCE_CHOICES` (constant), lines 5199-5199, exports `SEMANTIC_CONFIDENCE_CHOICES`
- order 526: `L2_TODO_POLICY_CHOICES` (constant), lines 5200-5204, exports `L2_TODO_POLICY_CHOICES`
- order 527: `DEFAULT_L2_TODO_POLICY` (constant), lines 5205-5205, exports `DEFAULT_L2_TODO_POLICY`
- order 528: `TASK_LEVEL_POLICIES` (constant), lines 5206-5259, exports `TASK_LEVEL_POLICIES`
- order 529: `MANAGER_ROUTE_TARGETS` (constant), lines 5260-5260, exports `MANAGER_ROUTE_TARGETS`
- order 530: `BLACKBOARD_MAX_LOG_ENTRIES` (constant), lines 5261-5261, exports `BLACKBOARD_MAX_LOG_ENTRIES`
- order 531: `BLACKBOARD_MAX_TEXT` (constant), lines 5262-5262, exports `BLACKBOARD_MAX_TEXT`
- order 532: `BLACKBOARD_MEMORY_SHORT_MAX` (constant), lines 5263-5263, exports `BLACKBOARD_MEMORY_SHORT_MAX`
- order 533: `BLACKBOARD_MEMORY_MID_MAX_STEPS` (constant), lines 5264-5264, exports `BLACKBOARD_MEMORY_MID_MAX_STEPS`
- order 534: `BLACKBOARD_MEMORY_MID_ITEMS_PER_STEP` (constant), lines 5265-5265, exports `BLACKBOARD_MEMORY_MID_ITEMS_PER_STEP`
- order 535: `BLACKBOARD_MEMORY_LONG_MAX` (constant), lines 5266-5266, exports `BLACKBOARD_MEMORY_LONG_MAX`
- order 536: `BLACKBOARD_MEMORY_INDEX_MAX` (constant), lines 5267-5267, exports `BLACKBOARD_MEMORY_INDEX_MAX`
- order 537: `SKILL_REFRESH_MIN_INTERVAL_SECONDS` (constant), lines 5268-5268, exports `SKILL_REFRESH_MIN_INTERVAL_SECONDS`
- order 538: `SKILL_CATALOG_FULL_REFRESH_SECONDS` (constant), lines 5269-5272, exports `SKILL_CATALOG_FULL_REFRESH_SECONDS`
- order 539: `SKILL_PROMPT_MAX_ITEMS` (constant), lines 5273-5273, exports `SKILL_PROMPT_MAX_ITEMS`
- order 540: `SKILL_PROMPT_MAX_CHARS` (constant), lines 5274-5274, exports `SKILL_PROMPT_MAX_CHARS`
- order 541: `SKILL_RUNTIME_CACHE_MAX_ENTRIES` (constant), lines 5275-5275, exports `SKILL_RUNTIME_CACHE_MAX_ENTRIES`
- order 542: `SKILL_RUNTIME_CACHE_MAX_BYTES` (constant), lines 5276-5276, exports `SKILL_RUNTIME_CACHE_MAX_BYTES`
- order 543: `SKILL_AUTOLOAD_SCORE_THRESHOLD` (constant), lines 5277-5280, exports `SKILL_AUTOLOAD_SCORE_THRESHOLD`
- order 544: `SKILL_AUTOLOAD_CONFIDENCE_THRESHOLD` (constant), lines 5281-5281, exports `SKILL_AUTOLOAD_CONFIDENCE_THRESHOLD`
- order 545: `SKILL_RUNTIME_EVALUATION_TTL_SECONDS` (constant), lines 5282-5282, exports `SKILL_RUNTIME_EVALUATION_TTL_SECONDS`
- order 546: `SKILL_RUNTIME_EVALUATION_TIMEOUT_SECONDS` (constant), lines 5283-5283, exports `SKILL_RUNTIME_EVALUATION_TIMEOUT_SECONDS`
- order 547: `SKILL_RUNTIME_UNLOAD_CONFIDENCE_THRESHOLD` (constant), lines 5284-5284, exports `SKILL_RUNTIME_UNLOAD_CONFIDENCE_THRESHOLD`
- order 548: `SKILL_RUNTIME_KEY_TOOL_INTERVAL` (constant), lines 5285-5285, exports `SKILL_RUNTIME_KEY_TOOL_INTERVAL`
- order 549: `SKILL_RUNTIME_EVENTS_MAX` (constant), lines 5286-5286, exports `SKILL_RUNTIME_EVENTS_MAX`
- order 550: `SKILL_METADATA_CAPSULE_MAX_CHARS` (constant), lines 5287-5287, exports `SKILL_METADATA_CAPSULE_MAX_CHARS`
- order 551: `SKILL_DEPENDENCY_MAX_DEPTH` (constant), lines 5288-5288, exports `SKILL_DEPENDENCY_MAX_DEPTH`
- order 552: `AUTO_SKILLS_ROOT_CANDIDATES` (constant), lines 5289-5289, exports `AUTO_SKILLS_ROOT_CANDIDATES`
- order 553: `SKILL_DEFAULT_ATTACHMENT_GLOBS` (constant), lines 5290-5320, exports `SKILL_DEFAULT_ATTACHMENT_GLOBS`
- order 554: `SKILL_INLINE_ATTACHMENT_MAX_FILES` (constant), lines 5321-5321, exports `SKILL_INLINE_ATTACHMENT_MAX_FILES`
- order 555: `SKILL_INLINE_ATTACHMENT_MAX_CHARS` (constant), lines 5322-5322, exports `SKILL_INLINE_ATTACHMENT_MAX_CHARS`
- order 556: `SKILL_RESOURCE_MANIFEST_MAX_ITEMS` (constant), lines 5323-5323, exports `SKILL_RESOURCE_MANIFEST_MAX_ITEMS`
- order 557: `SKILL_BODY_COMPACT_THRESHOLD_CHARS` (constant), lines 5324-5324, exports `SKILL_BODY_COMPACT_THRESHOLD_CHARS`
- order 558: `SKILL_BODY_PREVIEW_CHARS` (constant), lines 5325-5325, exports `SKILL_BODY_PREVIEW_CHARS`
- order 559: `SKILLS_VIRTUAL_PREFIX` (constant), lines 5326-5326, exports `SKILLS_VIRTUAL_PREFIX`
- order 560: `SKILLS_EXTERNAL_MOUNT` (constant), lines 5327-5327, exports `SKILLS_EXTERNAL_MOUNT`
- order 561: `PLAN_MODE_ENABLED_LEVELS` (constant), lines 5328-5328, exports `PLAN_MODE_ENABLED_LEVELS`
- order 562: `PLAN_MODE_FORCED_LEVELS` (constant), lines 5329-5329, exports `PLAN_MODE_FORCED_LEVELS`
- order 563: `PLAN_MODE_USER_CHOICES` (constant), lines 5330-5330, exports `PLAN_MODE_USER_CHOICES`
- order 564: `TASK_PHASES` (constant), lines 5331-5332, exports `TASK_PHASES`
- order 565: `TASK_PHASE_ROUTING` (constant), lines 5333-5340, exports `TASK_PHASE_ROUTING`
- order 566: `COMPLEXITY_KEYWORDS` (constant), lines 5341-5347, exports `COMPLEXITY_KEYWORDS`
- order 567: `USER_COMPLEXITY_SIMPLE_TOKENS` (constant), lines 5348-5352, exports `USER_COMPLEXITY_SIMPLE_TOKENS`
- order 568: `USER_COMPLEXITY_MODERATE_TOKENS` (constant), lines 5353-5357, exports `USER_COMPLEXITY_MODERATE_TOKENS`
- order 569: `USER_COMPLEXITY_COMPLEX_TOKENS` (constant), lines 5358-5362, exports `USER_COMPLEXITY_COMPLEX_TOKENS`
- order 570: `USER_COMPLEXITY_EXPERT_TOKENS` (constant), lines 5363-5367, exports `USER_COMPLEXITY_EXPERT_TOKENS`
- order 571: `PLAN_MODE_EXPLORER_MAX_ROUNDS` (constant), lines 5368-5371, exports `PLAN_MODE_EXPLORER_MAX_ROUNDS`
- order 572: `PLAN_MODE_EXPLORER_PRODUCTIVE_ROUNDS` (constant), lines 5372-5372, exports `PLAN_MODE_EXPLORER_PRODUCTIVE_ROUNDS`
- order 573: `PLAN_MODE_EXPLORER_STALE_ROUNDS` (constant), lines 5373-5373, exports `PLAN_MODE_EXPLORER_STALE_ROUNDS`
- order 574: `PLAN_MODE_SYNTHESIS_MAX_ATTEMPTS` (constant), lines 5374-5374, exports `PLAN_MODE_SYNTHESIS_MAX_ATTEMPTS`
- order 575: `REVIEWER_DEBUG_MODE_MAX_ROUNDS` (constant), lines 5375-5376, exports `REVIEWER_DEBUG_MODE_MAX_ROUNDS`
- order 576: `REVIEWER_DEBUG_TOOL_ALLOWLIST` (constant), lines 5377-5382, exports `REVIEWER_DEBUG_TOOL_ALLOWLIST`
- order 577: `EXPLORER_STALL_THRESHOLD` (constant), lines 5383-5383, exports `EXPLORER_STALL_THRESHOLD`
- order 578: `DEVELOPER_EDIT_STALL_THRESHOLD` (constant), lines 5384-5384, exports `DEVELOPER_EDIT_STALL_THRESHOLD`
- order 579: `ACCEPTANCE_GATE_STALL_THRESHOLD` (constant), lines 5385-5388, exports `ACCEPTANCE_GATE_STALL_THRESHOLD`
- order 580: `ACCEPTANCE_GATE_HARD_CEILING` (constant), lines 5389-5392, exports `ACCEPTANCE_GATE_HARD_CEILING`
- order 581: `ACCEPTANCE_GATE_TOTAL_ROUND_CEILING` (constant), lines 5393-5393, exports `ACCEPTANCE_GATE_TOTAL_ROUND_CEILING`
- order 582: `PLAN_MODE_MANAGER_SYNTHESIS_MAX_TOKENS` (constant), lines 5394-5394, exports `PLAN_MODE_MANAGER_SYNTHESIS_MAX_TOKENS`
- order 583: `PLAN_MODE_MAX_OPTIONS` (constant), lines 5395-5395, exports `PLAN_MODE_MAX_OPTIONS`
- order 584: `PLAN_FILE_RELATIVE_PATH` (constant), lines 5396-5396, exports `PLAN_FILE_RELATIVE_PATH`
- order 585: `PLAN_BUBBLE_MAX_CHARS` (constant), lines 5397-5397, exports `PLAN_BUBBLE_MAX_CHARS`
- order 586: `PLAN_NOTICE_BODY_MAX_CHARS` (constant), lines 5398-5398, exports `PLAN_NOTICE_BODY_MAX_CHARS`
- order 587: `PLAN_MESSAGE_EVENT_MAX_CHARS` (constant), lines 5399-5399, exports `PLAN_MESSAGE_EVENT_MAX_CHARS`
- order 588: `PLAN_STEP_FULL_CONTENT_MAX_CHARS` (constant), lines 5400-5400, exports `PLAN_STEP_FULL_CONTENT_MAX_CHARS`
- order 589: `PLAN_MODE_RESEARCH_TOOL_ALLOWLIST` (constant), lines 5401-5408, exports `PLAN_MODE_RESEARCH_TOOL_ALLOWLIST`
- order 590: `FAILURE_LEDGER_MAX_FIXES` (constant), lines 5409-5409, exports `FAILURE_LEDGER_MAX_FIXES`
- order 591: `FAILURE_LEDGER_MAX_COMPILE_ERRORS` (constant), lines 5410-5410, exports `FAILURE_LEDGER_MAX_COMPILE_ERRORS`
- order 592: `FAILURE_LEDGER_MAX_DELEGATIONS` (constant), lines 5411-5411, exports `FAILURE_LEDGER_MAX_DELEGATIONS`
- order 593: `FAILURE_LEDGER_MAX_STALLS` (constant), lines 5412-5412, exports `FAILURE_LEDGER_MAX_STALLS`
- order 594: `FAILURE_LEDGER_MAX_TOOL_FPS` (constant), lines 5413-5413, exports `FAILURE_LEDGER_MAX_TOOL_FPS`
- order 595: `FAILURE_LEDGER_MAX_ERRORS` (constant), lines 5414-5414, exports `FAILURE_LEDGER_MAX_ERRORS`
- order 596: `ERROR_CATEGORY_DEFS` (constant), lines 5415-5454, exports `ERROR_CATEGORY_DEFS`
- order 597: `CHECKPOINT_MAX_COUNT` (constant), lines 5455-5455, exports `CHECKPOINT_MAX_COUNT`
- order 598: `CHECKPOINT_INTERVAL_ROUNDS` (constant), lines 5456-5456, exports `CHECKPOINT_INTERVAL_ROUNDS`
- order 599: `PERSISTED_ROUTES_MAX` (constant), lines 5457-5457, exports `PERSISTED_ROUTES_MAX`
- order 600: `HTML_FRONTEND_REQUEST_KEYWORDS` (constant), lines 5458-5497, exports `HTML_FRONTEND_REQUEST_KEYWORDS`
- order 601: `DEEP_RESEARCH_REQUEST_KEYWORDS` (constant), lines 5498-5520, exports `DEEP_RESEARCH_REQUEST_KEYWORDS`
- order 602: `DEEP_RESEARCH_RETRIEVAL_KEYWORDS` (constant), lines 5521-5540, exports `DEEP_RESEARCH_RETRIEVAL_KEYWORDS`
- order 603: `DEEP_RESEARCH_TEXT_ONLY_HINT_KEYWORDS` (constant), lines 5541-5558, exports `DEEP_RESEARCH_TEXT_ONLY_HINT_KEYWORDS`
- order 604: `DANGEROUS_PATTERNS` (constant), lines 5559-5560, exports `DANGEROUS_PATTERNS`
- order 605: `VALID_MSG_TYPES` (constant), lines 5561-5567, exports `VALID_MSG_TYPES`
- order 606: `SUPPORTED_UI_LANGUAGES` (constant), lines 5568-5574, exports `SUPPORTED_UI_LANGUAGES`
- order 607: `UI_LANGUAGE_LABELS` (constant), lines 5575-5575, exports `UI_LANGUAGE_LABELS`
- order 608: `DEFAULT_UI_LANGUAGE` (constant), lines 5576-5576, exports `DEFAULT_UI_LANGUAGE`
- order 609: `PUBLIC_TOOL_PROGRESS_SUMMARY_ENABLED` (constant), lines 5577-5579, exports `PUBLIC_TOOL_PROGRESS_SUMMARY_ENABLED`
- order 610: `AGENT_LANGUAGE_PREFERENCES` (constant), lines 5580-5621, exports `AGENT_LANGUAGE_PREFERENCES`
- order 611: `UI_STYLE_CHOICES` (constant), lines 5622-5622, exports `UI_STYLE_CHOICES`
- order 612: `UI_STYLE_LABELS` (constant), lines 5623-5623, exports `UI_STYLE_LABELS`
- order 613: `DEFAULT_UI_STYLE` (constant), lines 5624-5624, exports `DEFAULT_UI_STYLE`
- order 614: `DEFAULT_WEB_UI_DIR` (constant), lines 5625-5625, exports `DEFAULT_WEB_UI_DIR`
- order 615: `DEFAULT_WEB_UI_CONFIG` (constant), lines 5626-5626, exports `DEFAULT_WEB_UI_CONFIG`
- order 616: `WEB_UI_REQUIRED_FILES` (constant), lines 5627-5634, exports `WEB_UI_REQUIRED_FILES`
- order 617: `WEB_UI_OPTIONAL_FILES` (constant), lines 5635-5635, exports `WEB_UI_OPTIONAL_FILES`
- order 618: `WEB_UI_APPLICATION_CONTRACT_VERSION` (constant), lines 5636-5636, exports `WEB_UI_APPLICATION_CONTRACT_VERSION`
- order 619: `WEB_UI_APPLICATION_FEATURE_MARKERS` (constant), lines 5637-5656, exports `WEB_UI_APPLICATION_FEATURE_MARKERS`
- order 620: `IMAGE_EXTS` (constant), lines 5657-5671, exports `IMAGE_EXTS`
- order 621: `IMAGE_FORMATS_NEED_CONVERSION` (constant), lines 5672-5672, exports `IMAGE_FORMATS_NEED_CONVERSION`
- order 622: `IMAGE_SAFE_FORMATS` (constant), lines 5673-5673, exports `IMAGE_SAFE_FORMATS`
- order 623: `AUDIO_EXTS` (constant), lines 5674-5684, exports `AUDIO_EXTS`
- order 624: `VIDEO_EXTS` (constant), lines 5685-5695, exports `VIDEO_EXTS`
- order 625: `CODE_PREVIEW_STAGE_MAX_BYTES` (constant), lines 5696-5696, exports `CODE_PREVIEW_STAGE_MAX_BYTES`
- order 626: `CODE_PREVIEW_STAGE_MAX_ROWS` (constant), lines 5697-5697, exports `CODE_PREVIEW_STAGE_MAX_ROWS`
- order 627: `CODE_PREVIEW_STAGE_MAX_PER_FILE` (constant), lines 5698-5698, exports `CODE_PREVIEW_STAGE_MAX_PER_FILE`
- order 628: `CODE_PREVIEW_STAGE_MAX_TOTAL` (constant), lines 5699-5699, exports `CODE_PREVIEW_STAGE_MAX_TOTAL`
- order 629: `CODE_PREVIEW_DIFF_CONTEXT_LINES` (constant), lines 5700-5700, exports `CODE_PREVIEW_DIFF_CONTEXT_LINES`
- order 630: `CODE_PREVIEW_DIFF_MERGE_GAP` (constant), lines 5701-5701, exports `CODE_PREVIEW_DIFF_MERGE_GAP`
- order 631: `PREVIEW_DOWNLOAD_MAX_FILES` (constant), lines 5702-5702, exports `PREVIEW_DOWNLOAD_MAX_FILES`
- order 632: `PREVIEW_DOWNLOAD_MAX_BYTES` (constant), lines 5703-5703, exports `PREVIEW_DOWNLOAD_MAX_BYTES`
- order 633: `FILES_TREE_DEFAULT_MAX_NODES` (constant), lines 5704-5704, exports `FILES_TREE_DEFAULT_MAX_NODES`
- order 634: `FILES_TREE_DEFAULT_MAX_DEPTH` (constant), lines 5705-5705, exports `FILES_TREE_DEFAULT_MAX_DEPTH`
- order 635: `FILES_TREE_SKIP_DIRS` (constant), lines 5706-5714, exports `FILES_TREE_SKIP_DIRS`
- order 636: `FILES_TREE_SKIP_REL_DIRS` (constant), lines 5715-5717, exports `FILES_TREE_SKIP_REL_DIRS`
- order 637: `IDE_FILE_MAX_BYTES` (constant), lines 5718-5718, exports `IDE_FILE_MAX_BYTES`
- order 638: `IDE_UPLOAD_MAX_BYTES` (constant), lines 5719-5719, exports `IDE_UPLOAD_MAX_BYTES`
- order 639: `IDE_UPLOAD_TOTAL_MAX_BYTES` (constant), lines 5720-5720, exports `IDE_UPLOAD_TOTAL_MAX_BYTES`
- order 640: `IDE_UPLOAD_MAX_ITEMS` (constant), lines 5721-5721, exports `IDE_UPLOAD_MAX_ITEMS`
- order 641: `IDE_UPLOAD_CHUNK_MAX_BYTES` (constant), lines 5722-5722, exports `IDE_UPLOAD_CHUNK_MAX_BYTES`
- order 642: `IDE_UPLOAD_STREAM_MAX_BYTES` (constant), lines 5723-5723, exports `IDE_UPLOAD_STREAM_MAX_BYTES`
- order 643: `IDE_TEXT_PREVIEW_MAX_BYTES` (constant), lines 5724-5724, exports `IDE_TEXT_PREVIEW_MAX_BYTES`
- order 644: `IDE_MARKDOWN_PREVIEW_MAX_LINES` (constant), lines 5725-5725, exports `IDE_MARKDOWN_PREVIEW_MAX_LINES`
- order 645: `IDE_IMAGE_PREVIEW_MAX_EDGE` (constant), lines 5726-5726, exports `IDE_IMAGE_PREVIEW_MAX_EDGE`
- order 646: `IDE_IMAGE_PREVIEW_MAX_PIXELS` (constant), lines 5727-5727, exports `IDE_IMAGE_PREVIEW_MAX_PIXELS`
- order 647: `IDE_IMAGE_PREVIEW_SOURCE_MAX_PIXELS` (constant), lines 5728-5728, exports `IDE_IMAGE_PREVIEW_SOURCE_MAX_PIXELS`
- order 648: `IDE_VECTOR_PREVIEW_MAX_BYTES` (constant), lines 5729-5729, exports `IDE_VECTOR_PREVIEW_MAX_BYTES`
- order 649: `IDE_TABLE_PREVIEW_SOURCE_MAX_BYTES` (constant), lines 5730-5730, exports `IDE_TABLE_PREVIEW_SOURCE_MAX_BYTES`
- order 650: `IDE_TABLE_PREVIEW_CELL_MAX_CHARS` (constant), lines 5731-5731, exports `IDE_TABLE_PREVIEW_CELL_MAX_CHARS`
- order 651: `IDE_TABLE_PREVIEW_TOTAL_CHARS` (constant), lines 5732-5732, exports `IDE_TABLE_PREVIEW_TOTAL_CHARS`
- order 652: `IDE_OFFICE_PREVIEW_MAX_ENTRIES` (constant), lines 5733-5733, exports `IDE_OFFICE_PREVIEW_MAX_ENTRIES`
- order 653: `IDE_OFFICE_PREVIEW_MAX_EXPANDED_BYTES` (constant), lines 5734-5734, exports `IDE_OFFICE_PREVIEW_MAX_EXPANDED_BYTES`
- order 654: `IDE_OFFICE_PREVIEW_MAX_ENTRY_BYTES` (constant), lines 5735-5735, exports `IDE_OFFICE_PREVIEW_MAX_ENTRY_BYTES`
- order 655: `IDE_COMMAND_TIMEOUT_DEFAULT` (constant), lines 5736-5736, exports `IDE_COMMAND_TIMEOUT_DEFAULT`
- order 656: `IDE_TREE_DEFAULT_MAX_NODES` (constant), lines 5737-5737, exports `IDE_TREE_DEFAULT_MAX_NODES`
- order 657: `IDE_TREE_MAX_NODES` (constant), lines 5738-5738, exports `IDE_TREE_MAX_NODES`
- order 658: `IDE_SEARCH_MAX_RESULTS` (constant), lines 5739-5739, exports `IDE_SEARCH_MAX_RESULTS`
- order 659: `IDE_SEARCH_MAX_FILE_BYTES` (constant), lines 5740-5740, exports `IDE_SEARCH_MAX_FILE_BYTES`
- order 660: `IDE_TERMINAL_SCROLLBACK_BYTES` (constant), lines 5741-5741, exports `IDE_TERMINAL_SCROLLBACK_BYTES`
- order 661: `IDE_TERMINAL_IDLE_SECONDS` (constant), lines 5742-5742, exports `IDE_TERMINAL_IDLE_SECONDS`
- order 662: `IDE_DEBUG_ADAPTER_START_ATTEMPTS` (constant), lines 5743-5743, exports `IDE_DEBUG_ADAPTER_START_ATTEMPTS`
- order 663: `IDE_DEBUG_ADAPTER_START_TIMEOUT_SECONDS` (constant), lines 5744-5744, exports `IDE_DEBUG_ADAPTER_START_TIMEOUT_SECONDS`
- order 664: `IDE_VSIX_MAX_BYTES` (constant), lines 5745-5745, exports `IDE_VSIX_MAX_BYTES`
- order 665: `IDE_VSIX_MAX_EXPANDED_BYTES` (constant), lines 5746-5746, exports `IDE_VSIX_MAX_EXPANDED_BYTES`
- order 666: `IDE_VSIX_MAX_FILES` (constant), lines 5747-5747, exports `IDE_VSIX_MAX_FILES`
- order 667: `IDE_VSIX_MAX_FILE_BYTES` (constant), lines 5748-5748, exports `IDE_VSIX_MAX_FILE_BYTES`
- order 668: `IDE_TREE_SKIP_DIRS` (constant), lines 5749-5757, exports `IDE_TREE_SKIP_DIRS`
- order 669: `RENDER_FRAME_MAX_B64_CHARS` (constant), lines 5758-5758, exports `RENDER_FRAME_MAX_B64_CHARS`
- order 670: `RENDER_FRAME_MAX_POINTS` (constant), lines 5759-5759, exports `RENDER_FRAME_MAX_POINTS`
- order 671: `RENDER_FRAME_MAX_LINES` (constant), lines 5760-5760, exports `RENDER_FRAME_MAX_LINES`
- order 672: `RENDER_FRAME_MAX_LINE_POINTS` (constant), lines 5761-5761, exports `RENDER_FRAME_MAX_LINE_POINTS`
- order 673: `RENDER_FRAME_ACTIVITY_INTERVAL_SECONDS` (constant), lines 5762-5762, exports `RENDER_FRAME_ACTIVITY_INTERVAL_SECONDS`
- order 674: `RAW_TOOLCALL_TEXT_FILTER_THRESHOLD` (constant), lines 5763-5763, exports `RAW_TOOLCALL_TEXT_FILTER_THRESHOLD`
- order 675: `ASSISTANT_TEXT_PERSIST_MAX_CHARS` (constant), lines 5764-5764, exports `ASSISTANT_TEXT_PERSIST_MAX_CHARS`
- order 676: `ASSISTANT_MESSAGE_EVENT_MAX_CHARS` (constant), lines 5765-5765, exports `ASSISTANT_MESSAGE_EVENT_MAX_CHARS`
- order 677: `CODE_PREVIEW_EXTS` (constant), lines 5766-5893, exports `CODE_PREVIEW_EXTS`
- order 678: `CODE_PREVIEW_FILENAMES` (constant), lines 5894-5945, exports `CODE_PREVIEW_FILENAMES`
- order 679: `MEDIA_CAPABILITY_KEYS` (constant), lines 5946-5953, exports `MEDIA_CAPABILITY_KEYS`
- order 683: `OFFLINE_JS_LIB_CATALOG` (constant), lines 5986-6312, exports `OFFLINE_JS_LIB_CATALOG`
- order 684: `OFFLINE_JS_ASSET_LOCK` (constant), lines 6313-6313, exports `OFFLINE_JS_ASSET_LOCK`
- order 685: `OFFLINE_JS_LIB_INDEX_FILE` (constant), lines 6314-6314, exports `OFFLINE_JS_LIB_INDEX_FILE`
- order 686: `OFFLINE_JS_LIB_README_FILE` (constant), lines 6315-6315, exports `OFFLINE_JS_LIB_README_FILE`
- order 697: `BACKEND_I18N` (constant), lines 6521-6592, exports `BACKEND_I18N`
- order 698: `_call_backend_i18n_en_update_6594` (expression), lines 6593-6694, exports —
- order 699: `_call_backend_i18n_zh_cn_update_6695` (expression), lines 6695-6795, exports —
- order 700: `_call_backend_i18n_zh_tw_update_6796` (expression), lines 6796-6896, exports —
- order 701: `_call_backend_i18n_ja_update_6897` (expression), lines 6897-6997, exports —
- order 910: `MODEL_RUNTIME_SETTING_KEYS` (constant), lines 13228-13233, exports `MODEL_RUNTIME_SETTING_KEYS`
- order 931: `LIQUID_KERNEL_STARTUP_POLICIES` (constant), lines 14927-14929, exports `LIQUID_KERNEL_STARTUP_POLICIES`
- order 932: `LIQUID_KERNEL_BOOTSTRAP_STATE_FILENAME` (constant), lines 14930-14930, exports `LIQUID_KERNEL_BOOTSTRAP_STATE_FILENAME`
- order 962: `TABULAR_PREVIEW_EXTS` (constant), lines 16828-16830, exports `TABULAR_PREVIEW_EXTS`
- order 963: `EXCEL_PREVIEW_EXTS` (constant), lines 16831-16831, exports `EXCEL_PREVIEW_EXTS`
- order 964: `PRESENTATION_PREVIEW_EXTS` (constant), lines 16832-16832, exports `PRESENTATION_PREVIEW_EXTS`
- order 965: `DOCUMENT_PREVIEW_EXTS` (constant), lines 16833-16833, exports `DOCUMENT_PREVIEW_EXTS`
- order 1175: `STUDIO_DEVICE_COOKIE` (constant), lines 116817-116834, exports `STUDIO_DEVICE_COOKIE`
- order 1176: `STUDIO_SESSION_COOKIE` (constant), lines 116835-116835, exports `STUDIO_SESSION_COOKIE`
- order 1177: `STUDIO_DEVICE_TTL` (constant), lines 116836-116836, exports `STUDIO_DEVICE_TTL`
- order 1178: `STUDIO_SESSION_TTL` (constant), lines 116837-116837, exports `STUDIO_SESSION_TTL`
- order 1179: `STUDIO_MAX_FILE_BYTES` (constant), lines 116838-116838, exports `STUDIO_MAX_FILE_BYTES`
- order 1180: `STUDIO_MAX_PROJECT_BYTES` (constant), lines 116839-116839, exports `STUDIO_MAX_PROJECT_BYTES`
- order 1181: `STUDIO_MAX_FILES` (constant), lines 116840-116840, exports `STUDIO_MAX_FILES`
- order 1182: `STUDIO_MAX_JOB_SECONDS` (constant), lines 116841-116841, exports `STUDIO_MAX_JOB_SECONDS`
- order 1188: `STUDIO_INDEX_HTML` (constant), lines 118740-118742, exports `STUDIO_INDEX_HTML`
- order 1189: `STUDIO_CSS` (constant), lines 118743-118743, exports `STUDIO_CSS`
- order 1190: `STUDIO_JS` (constant), lines 118744-118744, exports `STUDIO_JS`

### `config/paths.py`

- order 127: `SCRIPT_DIR` (constant), lines 3918-3918, exports `SCRIPT_DIR`
- order 152: `_resolve_default_agent_workdir` (function), lines 4012-4021, exports `_resolve_default_agent_workdir`
- order 153: `_is_installed_python_runtime` (function), lines 4022-4025, exports `_is_installed_python_runtime`
- order 154: `_runtime_storage_mode` (function), lines 4026-4032, exports `_runtime_storage_mode`
- order 155: `_runtime_tree_has_content` (function), lines 4033-4038, exports `_runtime_tree_has_content`
- order 156: `_copy_runtime_tree_with_crypto_migration` (function), lines 4039-4109, exports `_copy_runtime_tree_with_crypto_migration`
- order 157: `_merge_legacy_codes_root` (function), lines 4110-4175, exports `_merge_legacy_codes_root`
- order 158: `_migrate_legacy_runtime_roots` (function), lines 4176-4266, exports `_migrate_legacy_runtime_roots`
- order 159: `WORKDIR` (constant), lines 4267-4268, exports `WORKDIR`
- order 160: `CODES_ROOT` (constant), lines 4269-4269, exports `CODES_ROOT`
- order 161: `LLM_CONFIG_PATH` (constant), lines 4270-4270, exports `LLM_CONFIG_PATH`
- order 779: `detect_repo_root` (function), lines 8442-8456, exports `detect_repo_root`
- order 780: `REPO_ROOT` (constant), lines 8457-8458, exports `REPO_ROOT`

### `config/settings.py`

- order 690: `normalize_ui_language` (function), lines 6397-6421, exports `normalize_ui_language`
- order 691: `normalize_ui_style` (function), lines 6422-6441, exports `normalize_ui_style`
- order 692: `supported_ui_languages_payload` (function), lines 6442-6445, exports `supported_ui_languages_payload`
- order 694: `agent_language_preference_payload` (function), lines 6458-6467, exports `agent_language_preference_payload`
- order 695: `normalize_execution_mode` (function), lines 6468-6489, exports `normalize_execution_mode`
- order 696: `model_language_instruction` (function), lines 6490-6520, exports `model_language_instruction`
- order 702: `backend_i18n_text` (function), lines 6998-7010, exports `backend_i18n_text`
- order 703: `backend_role_label` (function), lines 7011-7017, exports `backend_role_label`
- order 704: `_detect_os_shell_instruction` (function), lines 7018-7059, exports `_detect_os_shell_instruction`
- order 705: `resolve_web_ui_dir_path` (function), lines 7060-7068, exports `resolve_web_ui_dir_path`
- order 706: `resolve_optional_file_path` (function), lines 7069-7078, exports `resolve_optional_file_path`
- order 707: `resolve_skills_root_path` (function), lines 7079-7088, exports `resolve_skills_root_path`
- order 708: `_count_skill_markdown_files` (function), lines 7089-7102, exports `_count_skill_markdown_files`
- order 709: `select_preferred_skills_root` (function), lines 7103-7139, exports `select_preferred_skills_root`
- order 710: `load_web_ui_config_file` (function), lines 7140-7156, exports `load_web_ui_config_file`
- order 711: `extract_show_upload_list_setting` (function), lines 7157-7173, exports `extract_show_upload_list_setting`
- order 712: `extract_ui_style_setting` (function), lines 7174-7190, exports `extract_ui_style_setting`
- order 713: `extract_js_lib_download_setting` (function), lines 7191-7212, exports `extract_js_lib_download_setting`
- order 714: `extract_daily_session_limit_setting` (function), lines 7213-7258, exports `extract_daily_session_limit_setting`
- order 715: `extract_shell_command_timeout_setting` (function), lines 7259-7307, exports `extract_shell_command_timeout_setting`
- order 716: `normalize_shell_timeout_mode` (function), lines 7308-7325, exports `normalize_shell_timeout_mode`
- order 717: `extract_shell_timeout_mode_setting` (function), lines 7326-7338, exports `extract_shell_timeout_mode_setting`
- order 718: `extract_shell_async_handoff_setting` (function), lines 7339-7366, exports `extract_shell_async_handoff_setting`
- order 719: `extract_context_token_limit_setting` (function), lines 7367-7401, exports `extract_context_token_limit_setting`
- order 720: `normalize_auto_task_level_ceiling` (function), lines 7402-7423, exports `normalize_auto_task_level_ceiling`
- order 721: `normalize_l2_todo_policy` (function), lines 7424-7459, exports `normalize_l2_todo_policy`
- order 722: `extract_l2_todo_policy_setting` (function), lines 7460-7502, exports `extract_l2_todo_policy_setting`
- order 723: `extract_auto_task_level_ceiling_setting` (function), lines 7503-7532, exports `extract_auto_task_level_ceiling_setting`
- order 724: `normalize_read_context_policy` (function), lines 7533-7553, exports `normalize_read_context_policy`
- order 725: `normalize_tool_memory_policy` (function), lines 7554-7557, exports `normalize_tool_memory_policy`
- order 726: `extract_read_context_policy_setting` (function), lines 7558-7581, exports `extract_read_context_policy_setting`
- order 727: `extract_tool_memory_policy_setting` (function), lines 7582-7605, exports `extract_tool_memory_policy_setting`
- order 729: `default_multimodal_capabilities` (function), lines 7612-7622, exports `default_multimodal_capabilities`
- order 730: `_to_bool_like` (function), lines 7623-7635, exports `_to_bool_like`
- order 731: `extract_web_search_enabled_setting` (function), lines 7636-7648, exports `extract_web_search_enabled_setting`
- order 732: `_single_no_plan_todo_setting_sections` (function), lines 7649-7675, exports `_single_no_plan_todo_setting_sections`
- order 733: `_single_no_plan_todo_setting_present` (function), lines 7676-7701, exports `_single_no_plan_todo_setting_present`
- order 734: `extract_single_no_plan_todo_settings` (function), lines 7702-7748, exports `extract_single_no_plan_todo_settings`
- order 735: `normalize_user_memory_mode` (function), lines 7749-7779, exports `normalize_user_memory_mode`
- order 736: `user_memory_enabled_from_mode` (function), lines 7780-7783, exports `user_memory_enabled_from_mode`
- order 737: `extract_user_memory_mode_setting` (function), lines 7784-7823, exports `extract_user_memory_mode_setting`
- order 738: `set_web_search_enabled_on_runtime` (function), lines 7824-7839, exports `set_web_search_enabled_on_runtime`
- order 739: `infer_model_multimodal_capabilities` (function), lines 7840-7886, exports `infer_model_multimodal_capabilities`
- order 740: `parse_capability_overrides` (function), lines 7887-7926, exports `parse_capability_overrides`
- order 741: `merge_multimodal_capabilities` (function), lines 7927-7936, exports `merge_multimodal_capabilities`
- order 742: `parse_media_endpoints` (function), lines 7937-7953, exports `parse_media_endpoints`
- order 758: `extract_runtime_region_hint_setting` (function), lines 8131-8156, exports `extract_runtime_region_hint_setting`
- order 759: `extract_runtime_timezone_hint_setting` (function), lines 8157-8174, exports `extract_runtime_timezone_hint_setting`
- order 760: `runtime_environment_context_snapshot` (function), lines 8175-8224, exports `runtime_environment_context_snapshot`
- order 761: `runtime_environment_context_block` (function), lines 8225-8254, exports `runtime_environment_context_block`
- order 797: `load_offline_js_lib_index` (function), lines 8729-8739, exports `load_offline_js_lib_index`
- order 852: `extract_ollama_model_capabilities` (function), lines 12248-12269, exports `extract_ollama_model_capabilities`
- order 861: `resolve_ollama_model` (function), lines 12392-12403, exports `resolve_ollama_model`
- order 862: `infer_thinking_model` (function), lines 12404-12407, exports `infer_thinking_model`
- order 873: `extract_base_url` (function), lines 12617-12626, exports `extract_base_url`
- order 875: `infer_user_complexity_value` (function), lines 12638-12655, exports `infer_user_complexity_value`
- order 876: `normalize_task_complexity` (function), lines 12656-12685, exports `normalize_task_complexity`
- order 877: `task_complexity_rank` (function), lines 12686-12688, exports `task_complexity_rank`
- order 878: `task_complexity_at_least` (function), lines 12689-12691, exports `task_complexity_at_least`
- order 879: `max_task_complexity` (function), lines 12692-12702, exports `max_task_complexity`
- order 880: `normalize_openai_compat_provider_name` (function), lines 12703-12719, exports `normalize_openai_compat_provider_name`
- order 900: `resolve_reasoning_payload` (function), lines 12847-12898, exports `resolve_reasoning_payload`
- order 904: `extract_openai_compat_model_ids` (function), lines 12967-13001, exports `extract_openai_compat_model_ids`
- order 905: `extract_openai_compat_model_records` (function), lines 13002-13081, exports `extract_openai_compat_model_records`
- order 911: `merge_probed_models_into_profile` (function), lines 13234-13277, exports `merge_probed_models_into_profile`
- order 912: `probe_and_merge_model_profiles` (function), lines 13278-13335, exports `probe_and_merge_model_profiles`
- order 913: `normalize_model_runtime_settings` (function), lines 13336-13361, exports `normalize_model_runtime_settings`
- order 914: `apply_model_runtime_settings` (function), lines 13362-13377, exports `apply_model_runtime_settings`
- order 915: `model_runtime_settings_for` (function), lines 13378-13388, exports `model_runtime_settings_for`
- order 916: `apply_model_option_runtime_fields` (function), lines 13389-13401, exports `apply_model_option_runtime_fields`
- order 919: `load_llm_config_from_source` (function), lines 13434-13469, exports `load_llm_config_from_source`
- order 920: `parse_llm_config_profiles` (function), lines 13470-14330, exports `parse_llm_config_profiles`
- order 921: `looks_like_llm_config` (function), lines 14331-14420, exports `looks_like_llm_config`
- order 925: `parse_front_matter` (function), lines 14616-14844, exports `parse_front_matter`
- order 933: `normalize_liquid_kernel_startup_policy` (function), lines 14931-14935, exports `normalize_liquid_kernel_startup_policy`
- order 960: `normalize_upload_rel_path` (function), lines 16782-16816, exports `normalize_upload_rel_path`

### `ide/assets.py`

- order 1167: `IDE_INDEX_HTML` (constant), lines 115688-115843, exports `IDE_INDEX_HTML`
- order 1168: `IDE_CSS` (constant), lines 115844-115885, exports `IDE_CSS`
- order 1169: `IDE_JS` (constant), lines 115886-116079, exports `IDE_JS`
- order 1170: `IDE_CSS` (constant), lines 116080-116100, exports `IDE_CSS`
- order 1171: `IDE_JS` (constant), lines 116101-116364, exports `IDE_JS`
- order 1172: `IDE_JS` (constant), lines 116365-116493, exports `IDE_JS`
- order 1173: `IDE_JS` (constant), lines 116494-116717, exports `IDE_JS`
- order 1174: `IDE_JS` (constant), lines 116718-116816, exports `IDE_JS`

### `ide/auth.py`

- order 939: `IDEAuthError` (class), lines 15272-15279, exports `IDEAuthError`
- order 940: `IDEAuthStore` (class), lines 15280-16003, exports `IDEAuthStore`

### `ide/errors.py`

- order 941: `IDECapabilityError` (class), lines 16004-16010, exports `IDECapabilityError`
- order 942: `IDEFileConflict` (class), lines 16011-16018, exports `IDEFileConflict`

### `ide/events.py`

- order 814: `ide_public_operation_data` (function), lines 9341-9392, exports `ide_public_operation_data`

### `ide/handler.py`

- order 1204: `IdeHandler` (class), lines 134086-135742, exports `IdeHandler`

### `ide/preview.py`

- order 959: `normalize_rel_preview_path` (function), lines 16768-16781, exports `normalize_rel_preview_path`
- order 961: `is_code_preview_candidate` (function), lines 16817-16827, exports `is_code_preview_candidate`
- order 966: `preview_kind_for_path` (function), lines 16834-16863, exports `preview_kind_for_path`
- order 967: `normalize_markdown_preview_text` (function), lines 16864-16897, exports `normalize_markdown_preview_text`
- order 968: `_preview_markdown_value_html` (function), lines 16898-16918, exports `_preview_markdown_value_html`
- order 969: `_preview_markdown_frontmatter_html` (function), lines 16919-16934, exports `_preview_markdown_frontmatter_html`
- order 970: `_preview_markdown_task_lists` (function), lines 16935-16948, exports `_preview_markdown_task_lists`
- order 971: `_preview_markdown_fallback_inline` (function), lines 16949-16990, exports `_preview_markdown_fallback_inline`
- order 972: `_preview_markdown_fallback_html` (function), lines 16991-17087, exports `_preview_markdown_fallback_html`
- order 975: `workspace_file_revision_map` (function), lines 17128-17152, exports `workspace_file_revision_map`
- order 976: `workspace_revision_delta` (function), lines 17153-17159, exports `workspace_revision_delta`
- order 977: `build_code_preview_rows` (function), lines 17160-17208, exports `build_code_preview_rows`

### `ide/sandbox.py`

- order 766: `_windows_subprocess_encodings` (function), lines 8280-8297, exports `_windows_subprocess_encodings`
- order 1060: `_IDE_SANDBOX_BACKEND_CACHE` (assignment), lines 29483-29491, exports `_IDE_SANDBOX_BACKEND_CACHE`
- order 1061: `_IDE_SANDBOX_BACKEND_LOCK` (assignment), lines 29492-29492, exports `_IDE_SANDBOX_BACKEND_LOCK`
- order 1062: `WINDOWS_JOB_SANDBOX_MARKER` (constant), lines 29493-29493, exports `WINDOWS_JOB_SANDBOX_MARKER`
- order 1063: `_WINDOWS_LOW_INTEGRITY_ROOTS` (assignment), lines 29494-29494, exports `_WINDOWS_LOW_INTEGRITY_ROOTS`
- order 1064: `_WINDOWS_LOW_INTEGRITY_FAILED_ROOTS` (assignment), lines 29495-29495, exports `_WINDOWS_LOW_INTEGRITY_FAILED_ROOTS`
- order 1065: `_WINDOWS_LOW_INTEGRITY_LOCK` (assignment), lines 29496-29496, exports `_WINDOWS_LOW_INTEGRITY_LOCK`
- order 1066: `_is_windows_job_sandbox_prefix` (function), lines 29497-29503, exports `_is_windows_job_sandbox_prefix`
- order 1067: `_windows_builtin_sandbox_probe` (function), lines 29504-29527, exports `_windows_builtin_sandbox_probe`
- order 1068: `_windows_last_error` (function), lines 29528-29535, exports `_windows_last_error`
- order 1069: `_windows_set_integrity_label` (function), lines 29536-29589, exports `_windows_set_integrity_label`
- order 1070: `_windows_set_low_integrity_label` (function), lines 29590-29592, exports `_windows_set_low_integrity_label`
- order 1071: `_windows_protect_application_snapshot` (function), lines 29593-29616, exports `_windows_protect_application_snapshot`
- order 1072: `_windows_prepare_low_integrity_workspace` (function), lines 29617-29654, exports `_windows_prepare_low_integrity_workspace`
- order 1073: `_windows_job_memory_limit` (function), lines 29655-29662, exports `_windows_job_memory_limit`
- order 1074: `_windows_lower_process_integrity` (function), lines 29663-29710, exports `_windows_lower_process_integrity`
- order 1075: `_windows_attach_sandbox_job` (function), lines 29711-29803, exports `_windows_attach_sandbox_job`
- order 1076: `_windows_close_sandbox_job` (function), lines 29804-29820, exports `_windows_close_sandbox_job`
- order 1077: `_popen_windows_sandboxed` (function), lines 29821-29852, exports `_popen_windows_sandboxed`
- order 1078: `_run_windows_sandboxed_command` (function), lines 29853-29906, exports `_run_windows_sandboxed_command`
- order 1079: `_detect_ide_sandbox_backend` (function), lines 29907-30011, exports `_detect_ide_sandbox_backend`

### `llm/client.py`

- order 1045: `OllamaError` (class), lines 26216-26238, exports `OllamaError`
- order 1046: `OllamaClient` (class), lines 26239-28756, exports `OllamaClient`

### `llm/constants.py`

- order 125: `DEFAULT_OLLAMA_BASE_URL` (constant), lines 3916-3916, exports `DEFAULT_OLLAMA_BASE_URL`
- order 126: `DEFAULT_OLLAMA_MODEL` (constant), lines 3917-3917, exports `DEFAULT_OLLAMA_MODEL`
- order 881: `OPENAI_COMPAT_PROVIDER_NAMES` (constant), lines 12720-12729, exports `OPENAI_COMPAT_PROVIDER_NAMES`
- order 882: `OPENAI_LIKE_PROVIDER_NAMES` (constant), lines 12730-12731, exports `OPENAI_LIKE_PROVIDER_NAMES`
- order 885: `EFFORT_OFF` (constant), lines 12738-12749, exports `EFFORT_OFF`
- order 886: `EFFORT_LOW` (constant), lines 12750-12750, exports `EFFORT_LOW`
- order 887: `EFFORT_MEDIUM` (constant), lines 12751-12751, exports `EFFORT_MEDIUM`
- order 888: `EFFORT_HIGH` (constant), lines 12752-12752, exports `EFFORT_HIGH`
- order 889: `EFFORT_MAX` (constant), lines 12753-12753, exports `EFFORT_MAX`
- order 890: `EFFORT_LEVELS` (constant), lines 12754-12754, exports `EFFORT_LEVELS`
- order 891: `EFFORT_ORDER` (constant), lines 12755-12755, exports `EFFORT_ORDER`
- order 892: `EFFORT_DEFAULT` (constant), lines 12756-12756, exports `EFFORT_DEFAULT`
- order 893: `EFFORT_ANTHROPIC_BUDGET` (constant), lines 12757-12764, exports `EFFORT_ANTHROPIC_BUDGET`
- order 894: `EFFORT_OPENAI_REASONING` (constant), lines 12765-12771, exports `EFFORT_OPENAI_REASONING`
- order 895: `TASK_LEVEL_EFFORT` (constant), lines 12772-12781, exports `TASK_LEVEL_EFFORT`
- order 896: `ROLE_EFFORT_FLOOR` (constant), lines 12782-12787, exports `ROLE_EFFORT_FLOOR`
- order 897: `COORDINATION_EFFORT` (constant), lines 12788-12791, exports `COORDINATION_EFFORT`

### `llm/utils.py`

- order 851: `probe_ollama_environment` (function), lines 12233-12247, exports `probe_ollama_environment`
- order 853: `probe_ollama_model_records` (function), lines 12270-12303, exports `probe_ollama_model_records`
- order 854: `list_ollama_models` (function), lines 12304-12308, exports `list_ollama_models`
- order 855: `_OLLAMA_TAG_CACHE_LOCK` (assignment), lines 12309-12310, exports `_OLLAMA_TAG_CACHE_LOCK`
- order 856: `_OLLAMA_TAG_CACHE` (assignment), lines 12311-12311, exports `_OLLAMA_TAG_CACHE`
- order 859: `_fetch_ollama_models_cached` (function), lines 12320-12345, exports `_fetch_ollama_models_cached`
- order 860: `list_ollama_models_cached` (function), lines 12346-12391, exports `list_ollama_models_cached`
- order 863: `split_thinking_content` (function), lines 12408-12452, exports `split_thinking_content`
- order 864: `strip_thinking_content` (function), lines 12453-12455, exports `strip_thinking_content`
- order 865: `check_ollama_model_ready` (function), lines 12456-12481, exports `check_ollama_model_ready`
- order 866: `list_loaded_ollama_models` (function), lines 12482-12496, exports `list_loaded_ollama_models`
- order 867: `wake_ollama_model` (function), lines 12497-12528, exports `wake_ollama_model`
- order 868: `try_pull_ollama_model` (function), lines 12529-12547, exports `try_pull_ollama_model`
- order 869: `ordered_model_candidates` (function), lines 12548-12567, exports `ordered_model_candidates`
- order 870: `pick_working_ollama_model` (function), lines 12568-12585, exports `pick_working_ollama_model`
- order 874: `complete_chat_endpoint` (function), lines 12627-12637, exports `complete_chat_endpoint`
- order 883: `is_openai_compat_provider` (function), lines 12732-12734, exports `is_openai_compat_provider`
- order 884: `is_openai_like_provider` (function), lines 12735-12737, exports `is_openai_like_provider`
- order 898: `clamp_effort` (function), lines 12792-12803, exports `clamp_effort`
- order 899: `model_reasoning_style` (function), lines 12804-12846, exports `model_reasoning_style`
- order 901: `openai_compat_probe_headers` (function), lines 12899-12917, exports `openai_compat_probe_headers`
- order 902: `openai_compat_model_list_urls` (function), lines 12918-12951, exports `openai_compat_model_list_urls`
- order 903: `anthropic_model_list_url` (function), lines 12952-12966, exports `anthropic_model_list_url`
- order 906: `_PROVIDER_MODEL_CACHE_LOCK` (assignment), lines 13082-13084, exports `_PROVIDER_MODEL_CACHE_LOCK`
- order 907: `_PROVIDER_MODEL_CACHE` (assignment), lines 13085-13085, exports `_PROVIDER_MODEL_CACHE`
- order 908: `_fetch_provider_models_cached` (function), lines 13086-13159, exports `_fetch_provider_models_cached`
- order 909: `probe_provider_models` (function), lines 13160-13227, exports `probe_provider_models`
- order 917: `_is_http_url` (function), lines 13402-13415, exports `_is_http_url`
- order 918: `_resolve_local_path` (function), lines 13416-13433, exports `_resolve_local_path`

### `mcp/constants.py`

- order 179: `MCP_SERVICE_PORT_OFFSET` (constant), lines 4288-4288, exports `MCP_SERVICE_PORT_OFFSET`
- order 1025: `MCP_PROTOCOL_VERSION` (constant), lines 24834-24863, exports `MCP_PROTOCOL_VERSION`
- order 1026: `MCP_NAME_RE` (constant), lines 24864-24864, exports `MCP_NAME_RE`
- order 1027: `MCP_TOOL_PREFIX` (constant), lines 24865-24865, exports `MCP_TOOL_PREFIX`
- order 1028: `_MCP_DEFAULT_HANDSHAKE_TIMEOUT` (assignment), lines 24866-24866, exports `_MCP_DEFAULT_HANDSHAKE_TIMEOUT`
- order 1029: `_MCP_DEFAULT_CALL_TIMEOUT` (assignment), lines 24867-24867, exports `_MCP_DEFAULT_CALL_TIMEOUT`
- order 1030: `_MCP_MAX_RESULT_CHARS` (assignment), lines 24868-24868, exports `_MCP_MAX_RESULT_CHARS`
- order 1031: `_MCP_TRUST_STORE_VERSION` (assignment), lines 24869-24869, exports `_MCP_TRUST_STORE_VERSION`

### `mcp/driver.py`

- order 1032: `mcp_normalize_name` (function), lines 24870-24879, exports `mcp_normalize_name`
- order 1033: `mcp_normalize_server_configs` (function), lines 24880-24964, exports `mcp_normalize_server_configs`
- order 1034: `mcp_extract_server_configs` (function), lines 24965-24984, exports `mcp_extract_server_configs`
- order 1035: `_mcp_sha256_file` (function), lines 24985-24995, exports `_mcp_sha256_file`
- order 1036: `_mcp_file_identity` (function), lines 24996-25013, exports `_mcp_file_identity`
- order 1037: `mcp_workspace_identity` (function), lines 25014-25032, exports `mcp_workspace_identity`
- order 1038: `mcp_config_file_digest` (function), lines 25033-25040, exports `mcp_config_file_digest`
- order 1039: `mcp_default_trust_store_path` (function), lines 25041-25075, exports `mcp_default_trust_store_path`
- order 1040: `mcp_record_definition_fingerprint` (function), lines 25076-25090, exports `mcp_record_definition_fingerprint`
- order 1041: `_mcp_effective_spawn` (function), lines 25091-25178, exports `_mcp_effective_spawn`
- order 1042: `MCPWorkspaceTrustStore` (class), lines 25179-25240, exports `MCPWorkspaceTrustStore`
- order 1043: `MCPServerProcess` (class), lines 25241-25596, exports `MCPServerProcess`
- order 1044: `MCPManager` (class), lines 25597-26215, exports `MCPManager`

### `mcp/service.py`

- order 1206: `McpServiceHandler` (class), lines 136214-136431, exports `McpServiceHandler`

### `rag/assets.py`

- order 1161: `RAG_ADMIN_INDEX_HTML` (constant), lines 113081-113313, exports `RAG_ADMIN_INDEX_HTML`
- order 1162: `RAG_ADMIN_CSS` (constant), lines 113314-113417, exports `RAG_ADMIN_CSS`
- order 1163: `RAG_ADMIN_JS` (constant), lines 113418-115638, exports `RAG_ADMIN_JS`
- order 1164: `CODE_ADMIN_INDEX_HTML` (constant), lines 115639-115651, exports `CODE_ADMIN_INDEX_HTML`
- order 1165: `CODE_ADMIN_CSS` (constant), lines 115652-115682, exports `CODE_ADMIN_CSS`
- order 1166: `CODE_ADMIN_JS` (constant), lines 115683-115687, exports `CODE_ADMIN_JS`

### `rag/constants.py`

- order 175: `RAG_LIBRARY_DIRNAME` (constant), lines 4284-4284, exports `RAG_LIBRARY_DIRNAME`
- order 176: `RAG_ADMIN_PORT_OFFSET` (constant), lines 4285-4285, exports `RAG_ADMIN_PORT_OFFSET`
- order 177: `CODE_LIBRARY_DIRNAME` (constant), lines 4286-4286, exports `CODE_LIBRARY_DIRNAME`
- order 183: `WEB_SEARCH_INDEX_DIRNAME` (constant), lines 4295-4295, exports `WEB_SEARCH_INDEX_DIRNAME`
- order 185: `USER_MEMORY_DIRNAME` (constant), lines 4297-4297, exports `USER_MEMORY_DIRNAME`
- order 186: `USER_MEMORY_DB_FILENAME` (constant), lines 4298-4298, exports `USER_MEMORY_DB_FILENAME`
- order 187: `USER_MEMORY_PROFILE_FILENAME` (constant), lines 4299-4299, exports `USER_MEMORY_PROFILE_FILENAME`
- order 188: `USER_MEMORY_MODE_CHOICES` (constant), lines 4300-4300, exports `USER_MEMORY_MODE_CHOICES`
- order 190: `USER_MEMORY_WEAK_CAPSULE_CHARS` (constant), lines 4302-4302, exports `USER_MEMORY_WEAK_CAPSULE_CHARS`
- order 191: `USER_MEMORY_ON_CAPSULE_CHARS` (constant), lines 4303-4303, exports `USER_MEMORY_ON_CAPSULE_CHARS`
- order 192: `USER_MEMORY_CAPSULE_INJECT_CHARS` (constant), lines 4304-4307, exports `USER_MEMORY_CAPSULE_INJECT_CHARS`
- order 193: `USER_MEMORY_MAX_SUMMARY_CHARS` (constant), lines 4308-4308, exports `USER_MEMORY_MAX_SUMMARY_CHARS`
- order 194: `USER_MEMORY_QUERY_LIMIT` (constant), lines 4309-4309, exports `USER_MEMORY_QUERY_LIMIT`
- order 195: `USER_MEMORY_DECAY_HALFLIFE_DAYS` (constant), lines 4310-4310, exports `USER_MEMORY_DECAY_HALFLIFE_DAYS`
- order 196: `USER_MEMORY_PROFILE_SCHEMA_VERSION` (constant), lines 4311-4311, exports `USER_MEMORY_PROFILE_SCHEMA_VERSION`
- order 216: `WEB_SEARCH_CONTEXT_REGISTRY_MAX` (constant), lines 4333-4333, exports `WEB_SEARCH_CONTEXT_REGISTRY_MAX`
- order 217: `WEB_SEARCH_CONTEXT_PROMPT_MAX_ITEMS` (constant), lines 4334-4334, exports `WEB_SEARCH_CONTEXT_PROMPT_MAX_ITEMS`
- order 218: `WEB_SEARCH_CONTEXT_PROMPT_MAX_CHARS` (constant), lines 4335-4335, exports `WEB_SEARCH_CONTEXT_PROMPT_MAX_CHARS`
- order 219: `WEB_SEARCH_CONTEXT_NODE_MAX` (constant), lines 4336-4336, exports `WEB_SEARCH_CONTEXT_NODE_MAX`
- order 220: `WEB_SEARCH_CONTEXT_URL_MAX` (constant), lines 4337-4337, exports `WEB_SEARCH_CONTEXT_URL_MAX`
- order 221: `RAG_CHUNK_CHARS` (constant), lines 4338-4338, exports `RAG_CHUNK_CHARS`
- order 222: `RAG_CHUNK_OVERLAP` (constant), lines 4339-4339, exports `RAG_CHUNK_OVERLAP`
- order 223: `RAG_MAX_CHUNKS_PER_DOC` (constant), lines 4340-4342, exports `RAG_MAX_CHUNKS_PER_DOC`
- order 224: `RAG_MAX_DOCUMENT_CHARS` (constant), lines 4343-4353, exports `RAG_MAX_DOCUMENT_CHARS`
- order 229: `RAG_MAX_QUERY_RESULTS` (constant), lines 4367-4367, exports `RAG_MAX_QUERY_RESULTS`
- order 230: `RAG_HIGH_RECALL_POOL_MULTIPLIER` (constant), lines 4368-4368, exports `RAG_HIGH_RECALL_POOL_MULTIPLIER`
- order 231: `RAG_HIGH_RECALL_MIN_POOL` (constant), lines 4369-4369, exports `RAG_HIGH_RECALL_MIN_POOL`
- order 232: `RAG_RETRIEVAL_MAX_PER_DOC` (constant), lines 4370-4370, exports `RAG_RETRIEVAL_MAX_PER_DOC`
- order 233: `RAG_BM25_K1` (constant), lines 4371-4374, exports `RAG_BM25_K1`
- order 234: `RAG_BM25_B` (constant), lines 4375-4375, exports `RAG_BM25_B`
- order 235: `RAG_BM25_SATURATION` (constant), lines 4376-4382, exports `RAG_BM25_SATURATION`
- order 236: `RAG_SYMBOL_EXACT_BOOST` (constant), lines 4383-4386, exports `RAG_SYMBOL_EXACT_BOOST`
- order 237: `RAG_INDEX_SNAPSHOT_FORMAT` (constant), lines 4387-4390, exports `RAG_INDEX_SNAPSHOT_FORMAT`
- order 238: `RAG_GRAPH_MAX_NODES` (constant), lines 4391-4391, exports `RAG_GRAPH_MAX_NODES`
- order 239: `RAG_TASK_HISTORY_LIMIT` (constant), lines 4392-4392, exports `RAG_TASK_HISTORY_LIMIT`
- order 240: `RAG_MODEL_MEDIA_MAX_BYTES` (constant), lines 4393-4393, exports `RAG_MODEL_MEDIA_MAX_BYTES`
- order 241: `RAG_MAX_IMPORT_FILES` (constant), lines 4394-4394, exports `RAG_MAX_IMPORT_FILES`
- order 242: `RAG_MAX_IMPORT_BATCH_ITEMS` (constant), lines 4395-4395, exports `RAG_MAX_IMPORT_BATCH_ITEMS`
- order 243: `RAG_MAX_IMPORT_BATCH_BYTES` (constant), lines 4396-4396, exports `RAG_MAX_IMPORT_BATCH_BYTES`
- order 244: `RAG_PDF_IMAGE_LIMIT` (constant), lines 4397-4397, exports `RAG_PDF_IMAGE_LIMIT`
- order 245: `RAG_QUERY_CONTEXT_CHARS` (constant), lines 4398-4398, exports `RAG_QUERY_CONTEXT_CHARS`
- order 246: `RAG_MAX_GLOBAL_COMMUNITIES` (constant), lines 4399-4399, exports `RAG_MAX_GLOBAL_COMMUNITIES`
- order 247: `RAG_MAX_COMMUNITY_MAP_SUPPORT` (constant), lines 4400-4400, exports `RAG_MAX_COMMUNITY_MAP_SUPPORT`
- order 248: `RAG_INCLUDE_FILENAME_ENTITIES_DEFAULT` (constant), lines 4401-4401, exports `RAG_INCLUDE_FILENAME_ENTITIES_DEFAULT`
- order 249: `RAG_DYNAMIC_NOISE_MIN_DOC_FREQ` (constant), lines 4402-4402, exports `RAG_DYNAMIC_NOISE_MIN_DOC_FREQ`
- order 250: `RAG_DYNAMIC_NOISE_MIN_COMMUNITY_FREQ` (constant), lines 4403-4403, exports `RAG_DYNAMIC_NOISE_MIN_COMMUNITY_FREQ`
- order 251: `RAG_DYNAMIC_NOISE_SOFT_DOC_RATIO` (constant), lines 4404-4404, exports `RAG_DYNAMIC_NOISE_SOFT_DOC_RATIO`
- order 252: `RAG_DYNAMIC_NOISE_HARD_DOC_RATIO` (constant), lines 4405-4405, exports `RAG_DYNAMIC_NOISE_HARD_DOC_RATIO`
- order 253: `RAG_DYNAMIC_NOISE_SOFT_COMMUNITY_RATIO` (constant), lines 4406-4406, exports `RAG_DYNAMIC_NOISE_SOFT_COMMUNITY_RATIO`
- order 254: `RAG_DYNAMIC_NOISE_HARD_COMMUNITY_RATIO` (constant), lines 4407-4407, exports `RAG_DYNAMIC_NOISE_HARD_COMMUNITY_RATIO`
- order 255: `RAG_MIN_SYNTHESIS_SCORE` (constant), lines 4408-4408, exports `RAG_MIN_SYNTHESIS_SCORE`
- order 256: `RAG_NO_EVIDENCE_THRESHOLD` (constant), lines 4409-4409, exports `RAG_NO_EVIDENCE_THRESHOLD`
- order 257: `RAG_WEAK_MATCH_SCORE_CAP` (constant), lines 4410-4410, exports `RAG_WEAK_MATCH_SCORE_CAP`
- order 258: `RAG_SYNTHESIS_MAX_PER_DOC` (constant), lines 4411-4411, exports `RAG_SYNTHESIS_MAX_PER_DOC`
- order 259: `RAG_WORKFLOW_ACCEPT_SCORE` (constant), lines 4412-4412, exports `RAG_WORKFLOW_ACCEPT_SCORE`
- order 260: `RAG_NO_EVIDENCE_MESSAGE` (constant), lines 4413-4413, exports `RAG_NO_EVIDENCE_MESSAGE`
- order 261: `RAG_CONTEXT_BUDGETS` (constant), lines 4414-4418, exports `RAG_CONTEXT_BUDGETS`
- order 262: `RAG_WEAK_EVIDENCE_MESSAGE` (constant), lines 4419-4419, exports `RAG_WEAK_EVIDENCE_MESSAGE`
- order 263: `RAG_EVIDENCE_SCHEMA_VERSION` (constant), lines 4420-4420, exports `RAG_EVIDENCE_SCHEMA_VERSION`
- order 264: `RAG_EVIDENCE_BATCH_CHARS` (constant), lines 4421-4424, exports `RAG_EVIDENCE_BATCH_CHARS`
- order 265: `RAG_EVALUATION_SUMMARY_CHARS` (constant), lines 4425-4428, exports `RAG_EVALUATION_SUMMARY_CHARS`
- order 266: `RAG_DENSE_DEFAULT_ENABLED` (constant), lines 4429-4429, exports `RAG_DENSE_DEFAULT_ENABLED`
- order 267: `RAG_EMBEDDING_MODE_VALUES` (constant), lines 4430-4430, exports `RAG_EMBEDDING_MODE_VALUES`
- order 268: `RAG_IMPORT_WORKER_COUNT` (constant), lines 4431-4434, exports `RAG_IMPORT_WORKER_COUNT`
- order 270: `RAG_PARSE_TIMEOUT_SECONDS` (constant), lines 4439-4442, exports `RAG_PARSE_TIMEOUT_SECONDS`
- order 1093: `RAG_TERM_GROUPS` (constant), lines 100075-104708, exports `RAG_TERM_GROUPS`
- order 1094: `RAG_RESEARCH_HINTS` (constant), lines 104709-104730, exports `RAG_RESEARCH_HINTS`
- order 1095: `RAG_CODE_HINTS` (constant), lines 104731-104741, exports `RAG_CODE_HINTS`
- order 1096: `RAG_SHORT_TOKEN_ALLOWLIST` (constant), lines 104742-104757, exports `RAG_SHORT_TOKEN_ALLOWLIST`
- order 1097: `RAG_EN_STOPWORDS` (constant), lines 104758-104830, exports `RAG_EN_STOPWORDS`
- order 1098: `RAG_ZH_STOPWORDS` (constant), lines 104831-104867, exports `RAG_ZH_STOPWORDS`
- order 1099: `RAG_GENERIC_ENTITY_TERMS_EN` (constant), lines 104868-104946, exports `RAG_GENERIC_ENTITY_TERMS_EN`
- order 1100: `RAG_GENERIC_ENTITY_TERMS_ZH` (constant), lines 104947-104989, exports `RAG_GENERIC_ENTITY_TERMS_ZH`
- order 1101: `RAG_STRUCTURAL_ENTITY_PATTERNS` (constant), lines 104990-105008, exports `RAG_STRUCTURAL_ENTITY_PATTERNS`
- order 1133: `CODE_LIBRARY_IGNORED_DIRS` (constant), lines 105966-105975, exports `CODE_LIBRARY_IGNORED_DIRS`
- order 1134: `CODE_LIBRARY_LANGUAGE_BY_EXT` (constant), lines 105976-106032, exports `CODE_LIBRARY_LANGUAGE_BY_EXT`
- order 1135: `CODE_LIBRARY_SPECIAL_FILENAMES` (constant), lines 106033-106039, exports `CODE_LIBRARY_SPECIAL_FILENAMES`

### `rag/index.py`

- order 1138: `_code_module_name` (function), lines 106064-106080, exports `_code_module_name`
- order 1139: `_code_choose_community` (function), lines 106081-106090, exports `_code_choose_community`
- order 1140: `_code_query_terms` (function), lines 106091-106105, exports `_code_query_terms`
- order 1149: `TFGraphIDFIndex` (class), lines 107236-108930, exports `TFGraphIDFIndex`
- order 1158: `CodeGraphIndex` (class), lines 112213-112701, exports `CodeGraphIndex`

### `rag/ingestion.py`

- order 1117: `_rag_trigram_set` (function), lines 105386-105393, exports `_rag_trigram_set`
- order 1118: `_rag_jaccard_sim` (function), lines 105394-105403, exports `_rag_jaccard_sim`
- order 1119: `_rag_mmr_select` (function), lines 105404-105453, exports `_rag_mmr_select`
- order 1124: `_rag_embed_text` (function), lines 105588-105611, exports `_rag_embed_text`
- order 1125: `_rag_embed_batch` (function), lines 105612-105620, exports `_rag_embed_batch`
- order 1126: `_rag_window_for_query` (function), lines 105621-105635, exports `_rag_window_for_query`
- order 1127: `_rag_focused_excerpt` (function), lines 105636-105678, exports `_rag_focused_excerpt`
- order 1128: `_rag_query_variants` (function), lines 105679-105718, exports `_rag_query_variants`
- order 1129: `_rag_parse_segments` (function), lines 105719-105781, exports `_rag_parse_segments`
- order 1130: `_rag_boundary_split` (function), lines 105782-105839, exports `_rag_boundary_split`
- order 1156: `_rag_parse_file_worker` (function), lines 111314-111330, exports `_rag_parse_file_worker`
- order 1157: `RAGIngestionService` (class), lines 111331-112212, exports `RAGIngestionService`
- order 1160: `CodeIngestionService` (class), lines 112993-113080, exports `CodeIngestionService`

### `rag/parsers.py`

- order 1102: `EvidenceRecord` (class), lines 105009-105043, exports `EvidenceRecord`
- order 1103: `_rag_float` (function), lines 105044-105050, exports `_rag_float`
- order 1104: `_rag_evidence_source_type` (function), lines 105051-105067, exports `_rag_evidence_source_type`
- order 1105: `_rag_normalize_evidence_record` (function), lines 105068-105123, exports `_rag_normalize_evidence_record`
- order 1106: `_rag_validate_evidence_record` (function), lines 105124-105166, exports `_rag_validate_evidence_record`
- order 1107: `_rag_evidence_batches` (function), lines 105167-105184, exports `_rag_evidence_batches`
- order 1108: `_rag_safe_name` (function), lines 105185-105190, exports `_rag_safe_name`
- order 1109: `_rag_detect_language` (function), lines 105191-105207, exports `_rag_detect_language`
- order 1110: `_rag_cjk_ngrams` (function), lines 105208-105222, exports `_rag_cjk_ngrams`
- order 1111: `_rag_is_noise_token` (function), lines 105223-105244, exports `_rag_is_noise_token`
- order 1112: `_rag_entity_allowed` (function), lines 105245-105259, exports `_rag_entity_allowed`
- order 1113: `_rag_filter_entities` (function), lines 105260-105276, exports `_rag_filter_entities`
- order 1114: `_rag_filename_entity_aliases` (function), lines 105277-105312, exports `_rag_filename_entity_aliases`
- order 1115: `_rag_apply_filename_entity_policy` (function), lines 105313-105345, exports `_rag_apply_filename_entity_policy`
- order 1116: `_rag_choose_community` (function), lines 105346-105385, exports `_rag_choose_community`
- order 1120: `_rag_tokenize` (function), lines 105454-105507, exports `_rag_tokenize`
- order 1121: `_rag_expand_tokens` (function), lines 105508-105531, exports `_rag_expand_tokens`
- order 1122: `_rag_extract_entities` (function), lines 105532-105550, exports `_rag_extract_entities`
- order 1123: `_rag_classify_document` (function), lines 105551-105587, exports `_rag_classify_document`
- order 1131: `_rag_structure_outline` (function), lines 105840-105878, exports `_rag_structure_outline`
- order 1132: `_rag_chunk_text` (function), lines 105879-105965, exports `_rag_chunk_text`
- order 1136: `_code_language_from_name` (function), lines 106040-106058, exports `_code_language_from_name`
- order 1137: `_code_is_test_path` (function), lines 106059-106063, exports `_code_is_test_path`
- order 1141: `_CallCollector` (class), lines 106106-106120, exports `_CallCollector`
- order 1142: `_ALGO_COMPLEXITY_RE` (assignment), lines 106121-106123, exports `_ALGO_COMPLEXITY_RE`
- order 1143: `_ALGO_STEP_RE` (assignment), lines 106124-106124, exports `_ALGO_STEP_RE`
- order 1144: `_ALGO_MATH_VARS` (assignment), lines 106125-106125, exports `_ALGO_MATH_VARS`
- order 1145: `_ALGO_DOC_KEYWORDS` (assignment), lines 106126-106126, exports `_ALGO_DOC_KEYWORDS`
- order 1146: `_detect_algo_chunk` (function), lines 106127-106152, exports `_detect_algo_chunk`
- order 1147: `CodeContentParser` (class), lines 106153-106719, exports `CodeContentParser`
- order 1148: `RAGContentParser` (class), lines 106720-107235, exports `RAGContentParser`

### `rag/store.py`

- order 1150: `RAGLibraryStore` (class), lines 108931-109569, exports `RAGLibraryStore`
- order 1151: `WikiStore` (class), lines 109570-110125, exports `WikiStore`
- order 1152: `UserMemoryStore` (class), lines 110126-110801, exports `UserMemoryStore`
- order 1153: `UserInteractionOptimizer` (class), lines 110802-110870, exports `UserInteractionOptimizer`
- order 1154: `UserIntentProfiler` (class), lines 110871-110912, exports `UserIntentProfiler`
- order 1155: `WorkflowMemoryStore` (class), lines 110913-111313, exports `WorkflowMemoryStore`
- order 1159: `CodeLibraryStore` (class), lines 112702-112992, exports `CodeLibraryStore`

### `rag/web_search.py`

- order 817: `_agent_web_bool` (function), lines 9427-9434, exports `_agent_web_bool`
- order 818: `_agent_web_int` (function), lines 9435-9442, exports `_agent_web_int`
- order 819: `_agent_web_host_is_local_name` (function), lines 9443-9449, exports `_agent_web_host_is_local_name`
- order 820: `_agent_web_ip_is_blocked` (function), lines 9450-9464, exports `_agent_web_ip_is_blocked`
- order 821: `_agent_web_canonical_url` (function), lines 9465-9494, exports `_agent_web_canonical_url`
- order 822: `_agent_web_domain_to_seed` (function), lines 9495-9506, exports `_agent_web_domain_to_seed`
- order 823: `_agent_web_query_terms` (function), lines 9507-9524, exports `_agent_web_query_terms`
- order 824: `_agent_web_query_domain_hints` (function), lines 9525-9565, exports `_agent_web_query_domain_hints`
- order 825: `_agent_web_query_needs_fresh_network` (function), lines 9566-9588, exports `_agent_web_query_needs_fresh_network`
- order 826: `_agent_web_extract_text_snippet` (function), lines 9589-9606, exports `_agent_web_extract_text_snippet`
- order 827: `AgentWebHTMLParser` (class), lines 9607-9686, exports `AgentWebHTMLParser`
- order 828: `_agent_web_decompress_bytes` (function), lines 9687-9710, exports `_agent_web_decompress_bytes`
- order 829: `_agent_web_charset_candidates` (function), lines 9711-9769, exports `_agent_web_charset_candidates`
- order 830: `_agent_web_decode_text_bytes` (function), lines 9770-9804, exports `_agent_web_decode_text_bytes`
- order 831: `AgentWebSearchEngine` (class), lines 9805-11585, exports `AgentWebSearchEngine`

### `server/http.py`

- order 693: `admin_language_payload` (function), lines 6446-6457, exports `admin_language_payload`
- order 806: `_UI_TRUNCATION_MARKER` (assignment), lines 9046-9048, exports `_UI_TRUNCATION_MARKER`
- order 807: `_ui_trim_text` (function), lines 9049-9057, exports `_ui_trim_text`
- order 808: `_bounded_ui_value` (function), lines 9058-9118, exports `_bounded_ui_value`
- order 809: `_bounded_ui_row` (function), lines 9119-9170, exports `_bounded_ui_row`
- order 810: `_bounded_ui_rows` (function), lines 9171-9219, exports `_bounded_ui_rows`
- order 811: `_enforce_ui_payload_budget` (function), lines 9220-9264, exports `_enforce_ui_payload_budget`
- order 812: `_apply_lite_snapshot_bounds` (function), lines 9265-9320, exports `_apply_lite_snapshot_bounds`
- order 1195: `AgentHTTPServer` (class), lines 129629-129668, exports `AgentHTTPServer`
- order 1198: `Handler` (class), lines 130855-132770, exports `Handler`
- order 1201: `SkillsReviewHandler` (class), lines 133572-133685, exports `SkillsReviewHandler`
- order 1205: `CollaborationHandler` (class), lines 135743-136213, exports `CollaborationHandler`

### `server/rag_admin.py`

- order 1200: `_RagAdminAuthMixin` (class), lines 133414-133571, exports `_RagAdminAuthMixin`
- order 1202: `RagAdminHandler` (class), lines 133686-133886, exports `RagAdminHandler`
- order 1203: `CodeAdminHandler` (class), lines 133887-134085, exports `CodeAdminHandler`

### `server/skills.py`

- order 1199: `SkillsHandler` (class), lines 132771-133413, exports `SkillsHandler`

### `session/manager.py`

- order 728: `SessionCreationLimitExceeded` (class), lines 7606-7611, exports `SessionCreationLimitExceeded`
- order 1081: `SessionManager` (class), lines 90661-93165, exports `SessionManager`

### `session/state.py`

- order 1080: `SessionState` (class), lines 30012-90660, exports `SessionState`

### `skills/embedded.py`

- order 980: `EMBEDDED_SKILLS_ARCHIVE_B64` (constant), lines 17625-17626, exports `EMBEDDED_SKILLS_ARCHIVE_B64`
- order 981: `EMBEDDED_SKILLS_ARCHIVE_SHA256` (constant), lines 17627-17627, exports `EMBEDDED_SKILLS_ARCHIVE_SHA256`
- order 982: `EMBEDDED_SKILLS_ARCHIVE_FILES` (constant), lines 17628-17650, exports `EMBEDDED_SKILLS_ARCHIVE_FILES`
- order 1007: `BUILTIN_CLAWHUB_SKILLS_VERSION` (constant), lines 20886-20888, exports `BUILTIN_CLAWHUB_SKILLS_VERSION`
- order 1008: `EMBEDDED_CLAWHUB_SKILLS_ARCHIVE_B64` (constant), lines 20889-21134, exports `EMBEDDED_CLAWHUB_SKILLS_ARCHIVE_B64`
- order 1010: `MCP_BUILDER_SKILL_MD` (constant), lines 21182-21356, exports `MCP_BUILDER_SKILL_MD`
- order 1013: `SKILL_PROTOCOL_LOCAL` (constant), lines 21388-21389, exports `SKILL_PROTOCOL_LOCAL`
- order 1014: `SKILL_PROTOCOL_CLAWHUB` (constant), lines 21390-21390, exports `SKILL_PROTOCOL_CLAWHUB`
- order 1015: `SKILL_PROTOCOL_HTTP_JSON` (constant), lines 21391-21391, exports `SKILL_PROTOCOL_HTTP_JSON`
- order 1016: `SKILL_PROTOCOL_SPECS` (constant), lines 21392-21424, exports `SKILL_PROTOCOL_SPECS`

### `skills/provisioning.py`

- order 983: `ensure_embedded_skills_at_root` (function), lines 17651-17716, exports `ensure_embedded_skills_at_root`
- order 984: `ensure_embedded_skills` (function), lines 17717-17720, exports `ensure_embedded_skills`
- order 986: `detect_upload_parser_capabilities` (function), lines 17727-17743, exports `detect_upload_parser_capabilities`
- order 987: `_render_cap_markdown` (function), lines 17744-17759, exports `_render_cap_markdown`
- order 988: `_write_text_if_changed` (function), lines 17760-17766, exports `_write_text_if_changed`
- order 989: `ensure_generated_document_skills` (function), lines 17767-17856, exports `ensure_generated_document_skills`
- order 990: `ensure_generated_image_coding_feedback_skill` (function), lines 17857-17957, exports `ensure_generated_image_coding_feedback_skill`
- order 991: `_skill_knowledge_files` (function), lines 17958-17978, exports `_skill_knowledge_files`
- order 992: `analyze_skill_building_knowledge` (function), lines 17979-18034, exports `analyze_skill_building_knowledge`
- order 993: `_sanitize_skill_slug` (function), lines 18035-18038, exports `_sanitize_skill_slug`
- order 994: `_build_skills_gen_skill_content` (function), lines 18039-18071, exports `_build_skills_gen_skill_content`
- order 995: `ensure_generated_skills_gen_skill` (function), lines 18072-18077, exports `ensure_generated_skills_gen_skill`
- order 996: `ensure_generated_execution_recovery_skill` (function), lines 18078-18162, exports `ensure_generated_execution_recovery_skill`
- order 997: `ensure_generated_systematic_debugging_skill` (function), lines 18163-18436, exports `ensure_generated_systematic_debugging_skill`
- order 998: `ensure_generated_code_engineering_mastery_skill` (function), lines 18437-18556, exports `ensure_generated_code_engineering_mastery_skill`
- order 999: `ensure_generated_smart_file_navigation_skill` (function), lines 18557-18673, exports `ensure_generated_smart_file_navigation_skill`
- order 1000: `ensure_generated_html_frontend_report_skills` (function), lines 18674-18882, exports `ensure_generated_html_frontend_report_skills`
- order 1001: `ensure_generated_deep_research_skills` (function), lines 18883-19152, exports `ensure_generated_deep_research_skills`
- order 1002: `ensure_generated_research_scientific_skills` (function), lines 19153-19790, exports `ensure_generated_research_scientific_skills`
- order 1003: `ensure_generated_rag_mastery_skills` (function), lines 19791-20092, exports `ensure_generated_rag_mastery_skills`
- order 1004: `ensure_generated_multimodal_comprehension_skills` (function), lines 20093-20787, exports `ensure_generated_multimodal_comprehension_skills`
- order 1005: `ensure_generated_runtime_skills_manifest` (function), lines 20788-20822, exports `ensure_generated_runtime_skills_manifest`
- order 1006: `ensure_generated_agent_web_search_skill` (function), lines 20823-20885, exports `ensure_generated_agent_web_search_skill`
- order 1009: `ensure_embedded_clawhub_skills` (function), lines 21135-21181, exports `ensure_embedded_clawhub_skills`
- order 1011: `ensure_generated_mcp_builder_skill` (function), lines 21357-21368, exports `ensure_generated_mcp_builder_skill`
- order 1012: `ensure_runtime_skills` (function), lines 21369-21387, exports `ensure_runtime_skills`

### `skills/store.py`

- order 1017: `_BUILTIN_SKILLS` (assignment), lines 21425-21533, exports `_BUILTIN_SKILLS`
- order 1018: `SkillStore` (class), lines 21534-23427, exports `SkillStore`

### `skills/studio.py`

- order 1183: `SkillsStudioError` (class), lines 116842-116851, exports `SkillsStudioError`
- order 1184: `_studio_slug` (function), lines 116852-116867, exports `_studio_slug`
- order 1185: `_studio_hash` (function), lines 116868-116871, exports `_studio_hash`
- order 1186: `_studio_cookie_value` (function), lines 116872-116881, exports `_studio_cookie_value`
- order 1187: `SkillsStudioStore` (class), lines 116882-118739, exports `SkillsStudioStore`

### `utils/compress.py`

- order 835: `compress_text_blob` (function), lines 11750-11756, exports `compress_text_blob`
- order 836: `decompress_text_blob` (function), lines 11757-11766, exports `decompress_text_blob`

### `utils/crypto.py`

- order 924: `CryptoBox` (class), lines 14462-14615, exports `CryptoBox`

### `utils/errors.py`

- order 857: `EmptyActionError` (class), lines 12312-12315, exports `EmptyActionError`
- order 1020: `ProcessManagerError` (class), lines 23563-23568, exports `ProcessManagerError`

### `utils/files.py`

- order 687: `_normalize_js_lib_asset_ref` (function), lines 6316-6331, exports `_normalize_js_lib_asset_ref`
- order 688: `_resolve_js_lib_asset_path` (function), lines 6332-6363, exports `_resolve_js_lib_asset_path`
- order 689: `_discover_extra_js_lib_files` (function), lines 6364-6396, exports `_discover_extra_js_lib_files`
- order 781: `safe_path` (function), lines 8459-8469, exports `safe_path`
- order 782: `_safe_js_filename` (function), lines 8470-8478, exports `_safe_js_filename`
- order 783: `_sha256_bytes` (function), lines 8479-8481, exports `_sha256_bytes`
- order 784: `_sha256_file` (function), lines 8482-8491, exports `_sha256_file`
- order 785: `_download_http_bytes` (function), lines 8492-8501, exports `_download_http_bytes`
- order 786: `offline_js_lib_root` (function), lines 8502-8504, exports `offline_js_lib_root`
- order 787: `_offline_js_entry_relative_path` (function), lines 8505-8510, exports `_offline_js_entry_relative_path`
- order 788: `_archive_member_relative_path` (function), lines 8511-8521, exports `_archive_member_relative_path`
- order 789: `_path_size_bytes` (function), lines 8522-8538, exports `_path_size_bytes`
- order 790: `_extract_archive_to_dir` (function), lines 8539-8580, exports `_extract_archive_to_dir`
- order 791: `_package_required_paths` (function), lines 8581-8588, exports `_package_required_paths`
- order 792: `_package_required_globs` (function), lines 8589-8605, exports `_package_required_globs`
- order 793: `_package_install_ready` (function), lines 8606-8628, exports `_package_install_ready`
- order 794: `_postprocess_offline_js_package` (function), lines 8629-8665, exports `_postprocess_offline_js_package`
- order 795: `_ensure_offline_js_package` (function), lines 8666-8710, exports `_ensure_offline_js_package`
- order 796: `_render_offline_js_catalog_md` (function), lines 8711-8728, exports `_render_offline_js_catalog_md`
- order 798: `ensure_offline_js_libs` (function), lines 8740-8898, exports `ensure_offline_js_libs`
- order 799: `_offline_js_catalog_entry_for_asset` (function), lines 8899-8919, exports `_offline_js_catalog_entry_for_asset`
- order 800: `ensure_offline_js_asset` (function), lines 8920-8977, exports `ensure_offline_js_asset`
- order 801: `_normalize_external_js_url` (function), lines 8978-8983, exports `_normalize_external_js_url`
- order 802: `is_external_js_src` (function), lines 8984-8987, exports `is_external_js_src`
- order 803: `match_offline_js_catalog_by_url` (function), lines 8988-9005, exports `match_offline_js_catalog_by_url`
- order 804: `cache_external_js_url` (function), lines 9006-9041, exports `cache_external_js_url`
- order 927: `try_read_text` (function), lines 14859-14868, exports `try_read_text`

### `utils/http.py`

- order 122: `_URL_OPEN_ORIGINAL` (assignment), lines 3913-3913, exports `_URL_OPEN_ORIGINAL`
- order 123: `_HTTP_SSL_CONTEXT` (assignment), lines 3914-3914, exports `_HTTP_SSL_CONTEXT`
- order 150: `_shared_http_ssl_context` (function), lines 3978-4001, exports `_shared_http_ssl_context`
- order 151: `urlopen` (function), lines 4002-4011, exports `urlopen`
- order 774: `json_response_bytes` (function), lines 8404-8406, exports `json_response_bytes`
- order 775: `read_http_json_body` (function), lines 8407-8420, exports `read_http_json_body`
- order 776: `close_if_http_request_body_unread` (function), lines 8421-8434, exports `close_if_http_request_body_unread`

### `utils/json_utils.py`

- order 174: `JSON_FSYNC_ENABLED` (constant), lines 4283-4283, exports `JSON_FSYNC_ENABLED`
- order 773: `json_dumps` (function), lines 8400-8403, exports `json_dumps`
- order 845: `parse_tool_arguments` (function), lines 12060-12070, exports `parse_tool_arguments`
- order 846: `repair_truncated_json_object` (function), lines 12071-12125, exports `repair_truncated_json_object`
- order 847: `parse_tool_arguments_with_error` (function), lines 12126-12157, exports `parse_tool_arguments_with_error`
- order 848: `_is_valid_json_object` (function), lines 12158-12163, exports `_is_valid_json_object`
- order 849: `_scan_top_level_json_objects` (function), lines 12164-12187, exports `_scan_top_level_json_objects`
- order 850: `reconstruct_streamed_tool_args` (function), lines 12188-12232, exports `reconstruct_streamed_tool_args`
- order 871: `parse_json_object` (function), lines 12586-12592, exports `parse_json_object`
- order 872: `extract_json_object_from_text` (function), lines 12593-12616, exports `extract_json_object_from_text`
- order 928: `_json_default_copy` (function), lines 14869-14875, exports `_json_default_copy`
- order 929: `_read_json_file` (function), lines 14876-14897, exports `_read_json_file`
- order 930: `_write_json_file` (function), lines 14898-14926, exports `_write_json_file`

### `utils/media.py`

- order 680: `_capability_probe_png_bytes` (function), lines 5954-5968, exports `_capability_probe_png_bytes`
- order 681: `_capability_probe_audio_bytes` (function), lines 5969-5980, exports `_capability_probe_audio_bytes`
- order 682: `_capability_probe_video_bytes` (function), lines 5981-5985, exports `_capability_probe_video_bytes`
- order 743: `guess_mime_from_name` (function), lines 7954-7958, exports `guess_mime_from_name`
- order 744: `_convert_image_to_safe_format` (function), lines 7959-7978, exports `_convert_image_to_safe_format`
- order 745: `guess_ext_from_mime` (function), lines 7979-7987, exports `guess_ext_from_mime`

### `utils/misc.py`

- order 746: `now_ts` (function), lines 7988-7990, exports `now_ts`
- order 747: `_benign_socket_log_lock` (assignment), lines 7991-7993, exports `_benign_socket_log_lock`
- order 748: `_benign_socket_log_state` (assignment), lines 7994-7994, exports `_benign_socket_log_state`
- order 750: `is_benign_socket_error` (function), lines 8010-8030, exports `is_benign_socket_error`
- order 751: `_socket_error_code` (function), lines 8031-8042, exports `_socket_error_code`
- order 752: `_log_benign_socket_error_limited` (function), lines 8043-8079, exports `_log_benign_socket_error_limited`
- order 753: `swallow_benign_socket_error` (function), lines 8080-8086, exports `swallow_benign_socket_error`
- order 754: `normalize_timeout_seconds` (function), lines 8087-8102, exports `normalize_timeout_seconds`
- order 755: `detect_local_lan_ip` (function), lines 8103-8114, exports `detect_local_lan_ip`
- order 756: `_LOCAL_LAN_IP_CACHE` (assignment), lines 8115-8116, exports `_LOCAL_LAN_IP_CACHE`
- order 757: `detect_local_lan_ip_cached` (function), lines 8117-8130, exports `detect_local_lan_ip_cached`
- order 777: `make_id` (function), lines 8435-8437, exports `make_id`
- order 778: `sanitize_profile_id` (function), lines 8438-8441, exports `sanitize_profile_id`
- order 922: `user_id_from_ip` (function), lines 14421-14428, exports `user_id_from_ip`
- order 926: `_meta_string_list` (function), lines 14845-14858, exports `_meta_string_list`
- order 985: `_module_exists` (function), lines 17721-17726, exports `_module_exists`

### `utils/sqlite.py`

- order 70: `_ClosingSQLiteConnection` (class), lines 73-82, exports `_ClosingSQLiteConnection`
- order 71: `_connect_sqlite` (function), lines 83-116, exports `_connect_sqlite`
- order 1207: `sqlite_failure_diagnostics` (function), lines 136432-136516, exports `sqlite_failure_diagnostics`

### `utils/text.py`

- order 162: `MAX_TOOL_OUTPUT` (constant), lines 4271-4271, exports `MAX_TOOL_OUTPUT`
- order 501: `SOCKET_NOISE_LINE_PATTERNS` (constant), lines 5042-5047, exports `SOCKET_NOISE_LINE_PATTERNS`
- order 749: `filter_runtime_noise_lines` (function), lines 7995-8009, exports `filter_runtime_noise_lines`
- order 762: `safe_utf8_bytes` (function), lines 8255-8257, exports `safe_utf8_bytes`
- order 763: `escape_invalid_utf8_text` (function), lines 8258-8260, exports `escape_invalid_utf8_text`
- order 764: `sanitize_utf8_surrogates` (function), lines 8261-8274, exports `sanitize_utf8_surrogates`
- order 765: `decode_utf8_replace` (function), lines 8275-8279, exports `decode_utf8_replace`
- order 805: `trim` (function), lines 9042-9045, exports `trim`
- order 813: `is_synthetic_public_progress` (function), lines 9321-9340, exports `is_synthetic_public_progress`
- order 815: `display_clean` (function), lines 9393-9407, exports `display_clean`
- order 816: `short_title_from` (function), lines 9408-9426, exports `short_title_from`
- order 832: `_fmt_export_ts` (function), lines 11586-11596, exports `_fmt_export_ts`
- order 833: `_html_esc` (function), lines 11597-11600, exports `_html_esc`
- order 834: `_text_to_minimal_pdf` (function), lines 11601-11749, exports `_text_to_minimal_pdf`
- order 837: `normalize_embedded_newlines` (function), lines 11767-11776, exports `normalize_embedded_newlines`
- order 838: `_map_todo_status_token` (function), lines 11777-11815, exports `_map_todo_status_token`
- order 839: `split_todo_status_text` (function), lines 11816-11875, exports `split_todo_status_text`
- order 840: `extract_todo_rows_from_text` (function), lines 11876-11945, exports `extract_todo_rows_from_text`
- order 841: `decode_structured_todo_container` (function), lines 11946-11964, exports `decode_structured_todo_container`
- order 842: `infer_todo_status_from_text` (function), lines 11965-11973, exports `infer_todo_status_from_text`
- order 843: `split_structured_todo_content` (function), lines 11974-12029, exports `split_structured_todo_content`
- order 844: `normalize_work_text` (function), lines 12030-12059, exports `normalize_work_text`
- order 951: `make_unified_diff` (function), lines 16483-16501, exports `make_unified_diff`
- order 952: `_skip_row` (function), lines 16502-16507, exports `_skip_row`
- order 953: `_row_is_hot` (function), lines 16508-16511, exports `_row_is_hot`
- order 954: `_hotspot_index` (function), lines 16512-16535, exports `_hotspot_index`
- order 955: `_compress_rows_keep_hotspot` (function), lines 16536-16585, exports `_compress_rows_keep_hotspot`
- order 956: `_focused_diff_rows_from_opcodes` (function), lines 16586-16720, exports `_focused_diff_rows_from_opcodes`
- order 957: `make_numbered_diff` (function), lines 16721-16753, exports `make_numbered_diff`
- order 958: `render_numbered_diff_text` (function), lines 16754-16767, exports `render_numbered_diff_text`

### `web/admin_assets.py`

- order 1090: `ADMIN_INDEX_HTML` (constant), lines 99192-99499, exports `ADMIN_INDEX_HTML`
- order 1091: `ADMIN_CSS` (constant), lines 99500-99660, exports `ADMIN_CSS`
- order 1092: `ADMIN_JS` (constant), lines 99661-100074, exports `ADMIN_JS`

### `web/assets.py`

- order 1082: `INDEX_HTML` (constant), lines 93166-93427, exports `INDEX_HTML`
- order 1083: `APP_CSS` (constant), lines 93428-93968, exports `APP_CSS`
- order 1084: `APP_JS` (constant), lines 93969-98729, exports `APP_JS`
- order 1085: `APP_CSS` (constant), lines 98730-98749, exports `APP_CSS`
- order 1086: `APP_TS` (constant), lines 98750-98789, exports `APP_TS`

### `web/skills_assets.py`

- order 1087: `SKILLS_INDEX_HTML` (constant), lines 98790-98945, exports `SKILLS_INDEX_HTML`
- order 1088: `SKILLS_EXTRA_CSS` (constant), lines 98946-99045, exports `SKILLS_EXTRA_CSS`
- order 1089: `SKILLS_APP_JS` (constant), lines 99046-99191, exports `SKILLS_APP_JS`
