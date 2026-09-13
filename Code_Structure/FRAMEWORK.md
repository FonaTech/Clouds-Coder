# Code_Structure Framework

## Overview

- Source snapshot: `Clouds_Coder.py` (1190 top-level statements)
- Generated source modules: 63
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
| `_imports.py` | 75 | 93 | — | 1–3780 |
| `admin/auth.py` | 3 | 3 | `admin/constants.py`, `utils/misc.py` | 13540–14380 |
| `admin/config.py` | 8 | 8 | `config/constants.py`, `config/paths.py`, `config/settings.py`, `llm/constants.py`, `utils/http.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` | 15126–15589 |
| `admin/constants.py` | 16 | 16 | — | 3787–117383 |
| `agent/background.py` | 1 | 1 | `agent/process.py`, `config/constants.py`, `ide/sandbox.py`, `utils/misc.py`, `utils/text.py` | 23036–23661 |
| `agent/bus.py` | 1 | 1 | `config/constants.py`, `utils/crypto.py`, `utils/misc.py` | 23662–23727 |
| `agent/errors.py` | 1 | 1 | — | 12129–12132 |
| `agent/events.py` | 1 | 1 | — | 16316–16370 |
| `agent/process.py` | 7 | 7 | `ide/sandbox.py`, `utils/errors.py`, `utils/misc.py`, `utils/text.py` | 8166–23035 |
| `agent/tasks.py` | 1 | 1 | `utils/crypto.py`, `utils/json_utils.py`, `utils/misc.py` | 22535–22669 |
| `agent/todo.py` | 1 | 1 | `config/constants.py`, `config/settings.py`, `utils/misc.py`, `utils/text.py` | 16371–16731 |
| `agent/tools.py` | 15 | 19 | `config/constants.py`, `utils/text.py` | 16195–28574 |
| `agent/worktree.py` | 1 | 1 | `agent/process.py`, `agent/tasks.py`, `config/constants.py`, `utils/crypto.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` | 23728–23940 |
| `app/context.py` | 1 | 1 | `admin/auth.py`, `admin/config.py`, `admin/constants.py`, `agent/process.py`, `agent/tools.py`, `app/services.py`, `collaboration/core.py`, `config/bootstrap.py`, `config/constants.py`, `config/paths.py`, `config/settings.py`, `ide/assets.py`, `ide/auth.py`, `ide/errors.py`, `ide/events.py`, `ide/preview.py`, `ide/sandbox.py`, `llm/client.py`, `llm/constants.py`, `llm/utils.py`, `mcp/driver.py`, `rag/assets.py`, `rag/constants.py`, `rag/ingestion.py`, `rag/parsers.py`, `rag/store.py`, `server/http.py`, `session/manager.py`, `session/state.py`, `skills/provisioning.py`, `skills/store.py`, `skills/studio.py`, `utils/crypto.py`, `utils/files.py`, `utils/http.py`, `utils/json_utils.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py`, `web/assets.py`, `web/skills_assets.py` | 117384–128100 |
| `app/main.py` | 2 | 1 | `admin/config.py`, `admin/constants.py`, `agent/tools.py`, `app/context.py`, `collaboration/watcher.py`, `config/constants.py`, `config/paths.py`, `config/settings.py`, `ide/handler.py`, `llm/constants.py`, `llm/utils.py`, `mcp/constants.py`, `mcp/service.py`, `rag/constants.py`, `server/http.py`, `server/rag_admin.py`, `server/skills.py`, `skills/provisioning.py`, `utils/files.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` | 134846–136797 |
| `app/services.py` | 2 | 2 | `admin/constants.py`, `config/settings.py`, `skills/embedded.py`, `skills/store.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` | 128141–129326 |
| `collaboration/core.py` | 23 | 23 | `config/constants.py` | 401–3640 |
| `collaboration/watcher.py` | 2 | 2 | `utils/misc.py`, `utils/text.py` | 134755–134845 |
| `config/bootstrap.py` | 5 | 5 | `config/constants.py`, `config/settings.py`, `utils/json_utils.py`, `utils/misc.py` | 78–14095 |
| `config/constants.py` | 502 | 498 | `config/bootstrap.py`, `rag/constants.py` | 377–117379 |
| `config/paths.py` | 13 | 13 | `agent/process.py`, `utils/crypto.py`, `utils/text.py` | 3786–8326 |
| `config/settings.py` | 68 | 68 | `agent/tools.py`, `config/constants.py`, `config/paths.py`, `ide/preview.py`, `llm/constants.py`, `llm/utils.py`, `rag/constants.py`, `skills/provisioning.py`, `utils/http.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` | 6265–15923 |
| `ide/assets.py` | 8 | 3 | — | 114322–115450 |
| `ide/auth.py` | 2 | 2 | `admin/auth.py`, `admin/constants.py`, `config/constants.py`, `utils/misc.py`, `utils/text.py` | 14381–15110 |
| `ide/errors.py` | 2 | 2 | — | 15111–15125 |
| `ide/events.py` | 1 | 1 | `config/constants.py`, `utils/text.py` | 9209–9260 |
| `ide/handler.py` | 1 | 1 | `admin/auth.py`, `app/context.py`, `collaboration/core.py`, `config/constants.py`, `config/settings.py`, `ide/auth.py`, `ide/errors.py`, `ide/events.py`, `session/manager.py`, `session/state.py`, `utils/http.py`, `utils/json_utils.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py` | 132410–134065 |
| `ide/preview.py` | 12 | 12 | `config/constants.py`, `utils/text.py` | 15875–16315 |
| `ide/sandbox.py` | 21 | 21 | `agent/process.py`, `utils/misc.py` | 8148–29103 |
| `llm/client.py` | 2 | 2 | `agent/tools.py`, `config/constants.py`, `config/settings.py`, `llm/utils.py`, `utils/http.py`, `utils/json_utils.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py` | 25323–27848 |
| `llm/constants.py` | 17 | 17 | — | 3784–12571 |
| `llm/utils.py` | 22 | 22 | `agent/process.py`, `config/settings.py`, `llm/constants.py`, `utils/http.py`, `utils/json_utils.py`, `utils/text.py` | 12103–12786 |
| `mcp/constants.py` | 8 | 8 | — | 4156–23976 |
| `mcp/driver.py` | 13 | 13 | `mcp/constants.py`, `utils/files.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` | 23977–25322 |
| `mcp/service.py` | 1 | 1 | `app/context.py`, `config/constants.py`, `utils/files.py`, `utils/http.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` | 134537–134754 |
| `rag/assets.py` | 6 | 6 | — | 111715–114321 |
| `rag/constants.py` | 77 | 77 | — | 4152–104671 |
| `rag/index.py` | 5 | 5 | `config/constants.py`, `rag/constants.py`, `rag/ingestion.py`, `rag/parsers.py`, `utils/misc.py`, `utils/text.py` | 104696–111335 |
| `rag/ingestion.py` | 13 | 13 | `config/constants.py`, `config/settings.py`, `rag/constants.py`, `rag/parsers.py`, `rag/store.py`, `session/state.py`, `utils/files.py`, `utils/json_utils.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py` | 104018–111714 |
| `rag/parsers.py` | 31 | 31 | `agent/process.py`, `config/constants.py`, `rag/constants.py`, `rag/ingestion.py`, `utils/files.py`, `utils/json_utils.py`, `utils/media.py`, `utils/text.py` | 103641–105867 |
| `rag/store.py` | 7 | 7 | `config/constants.py`, `config/settings.py`, `ide/preview.py`, `rag/constants.py`, `rag/index.py`, `rag/ingestion.py`, `rag/parsers.py`, `skills/provisioning.py`, `utils/files.py`, `utils/json_utils.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py` | 107563–111626 |
| `rag/web_search.py` | 15 | 15 | `config/constants.py`, `config/paths.py`, `rag/constants.py`, `utils/http.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` | 9295–11455 |
| `server/http.py` | 12 | 12 | `admin/auth.py`, `admin/config.py`, `admin/constants.py`, `agent/process.py`, `app/context.py`, `collaboration/core.py`, `collaboration/watcher.py`, `config/constants.py`, `config/paths.py`, `config/settings.py`, `ide/handler.py`, `ide/preview.py`, `llm/utils.py`, `server/rag_admin.py`, `session/manager.py`, `session/state.py`, `skills/studio.py`, `utils/errors.py`, `utils/files.py`, `utils/http.py`, `utils/json_utils.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py`, `web/admin_assets.py` | 6314–134536 |
| `server/rag_admin.py` | 3 | 3 | `admin/auth.py`, `app/context.py`, `config/constants.py`, `rag/constants.py`, `utils/http.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py` | 131738–132409 |
| `server/skills.py` | 1 | 1 | `admin/auth.py`, `app/context.py`, `config/constants.py`, `config/paths.py`, `config/settings.py`, `session/manager.py`, `skills/provisioning.py`, `skills/studio.py`, `utils/http.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py` | 131095–131737 |
| `session/manager.py` | 2 | 2 | `agent/process.py`, `config/constants.py`, `config/paths.py`, `config/settings.py`, `llm/client.py`, `llm/utils.py`, `rag/store.py`, `session/state.py`, `skills/store.py`, `utils/crypto.py`, `utils/files.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` | 7474–91908 |
| `session/state.py` | 1 | 1 | `admin/constants.py`, `agent/background.py`, `agent/bus.py`, `agent/errors.py`, `agent/events.py`, `agent/process.py`, `agent/tasks.py`, `agent/todo.py`, `agent/tools.py`, `agent/worktree.py`, `collaboration/core.py`, `config/constants.py`, `config/paths.py`, `config/settings.py`, `ide/events.py`, `ide/preview.py`, `ide/sandbox.py`, `llm/client.py`, `llm/constants.py`, `llm/utils.py`, `mcp/constants.py`, `mcp/driver.py`, `rag/constants.py`, `rag/parsers.py`, `rag/web_search.py`, `server/http.py`, `skills/provisioning.py`, `skills/store.py`, `utils/compress.py`, `utils/crypto.py`, `utils/errors.py`, `utils/files.py`, `utils/http.py`, `utils/json_utils.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py` | 29104–89565 |
| `skills/embedded.py` | 10 | 10 | — | 16732–20531 |
| `skills/provisioning.py` | 26 | 26 | `config/paths.py`, `skills/embedded.py`, `utils/files.py`, `utils/json_utils.py`, `utils/misc.py` | 16758–20494 |
| `skills/store.py` | 2 | 2 | `config/constants.py`, `config/settings.py`, `llm/utils.py`, `skills/embedded.py`, `utils/files.py`, `utils/http.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` | 20532–22534 |
| `skills/studio.py` | 5 | 5 | `agent/process.py`, `collaboration/core.py`, `config/constants.py`, `config/settings.py`, `ide/sandbox.py`, `llm/client.py`, `llm/constants.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` | 115476–117374 |
| `utils/compress.py` | 2 | 2 | — | 11620–11636 |
| `utils/crypto.py` | 1 | 1 | `utils/json_utils.py` | 13573–13726 |
| `utils/errors.py` | 2 | 2 | — | 12125–22675 |
| `utils/files.py` | 27 | 27 | `config/constants.py`, `config/paths.py`, `utils/http.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` | 6184–13979 |
| `utils/http.py` | 7 | 7 | `utils/json_utils.py`, `utils/text.py` | 3781–8302 |
| `utils/json_utils.py` | 13 | 13 | `utils/text.py` | 4151–14037 |
| `utils/media.py` | 6 | 6 | — | 5822–7855 |
| `utils/misc.py` | 16 | 16 | `config/constants.py` | 7856–16833 |
| `utils/text.py` | 30 | 30 | `config/constants.py` | 4139–15874 |
| `web/admin_assets.py` | 3 | 3 | — | 97893–98706 |
| `web/assets.py` | 5 | 4 | — | 91909–97490 |
| `web/skills_assets.py` | 3 | 3 | — | 97491–97892 |

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
- order 70: `_try_import_74` (import), lines 73-77, exports `_AESGCM`
- order 74: `_import_381` (import), lines 380-385, exports `EVOLUTION_MODES`, `LiquidKernelControlPlane`, `LiquidKernelError`
- order 114: `_try_import_3764` (import), lines 3762-3771, exports `_fcntl`, `_pty`, `_termios`
- order 115: `_try_import_3773` (import), lines 3772-3776, exports `_certifi`
- order 116: `_try_import_3777` (import), lines 3777-3780, exports `_yaml`

### `admin/auth.py`

- order 902: `trusted_client_ip` (function), lines 13540-13572, exports `trusted_client_ip`
- order 916: `AdminAuthError` (class), lines 14096-14103, exports `AdminAuthError`
- order 917: `AdminAuthStore` (class), lines 14104-14380, exports `AdminAuthStore`

### `admin/config.py`

- order 922: `_admin_config_schema` (function), lines 15126-15246, exports `_admin_config_schema`
- order 923: `_admin_factory_config` (function), lines 15247-15250, exports `_admin_factory_config`
- order 924: `_admin_coerce_config` (function), lines 15251-15406, exports `_admin_coerce_config`
- order 925: `_admin_config_to_argv` (function), lines 15407-15443, exports `_admin_config_to_argv`
- order 926: `_admin_restart_probe_url` (function), lines 15444-15459, exports `_admin_restart_probe_url`
- order 927: `_admin_supervised_restart` (function), lines 15460-15546, exports `_admin_supervised_restart`
- order 928: `_admin_argparse_defaults` (function), lines 15547-15568, exports `_admin_argparse_defaults`
- order 929: `_admin_config_from_namespace` (function), lines 15569-15589, exports `_admin_config_from_namespace`

### `admin/constants.py`

- order 123: `ADMIN_STATE_DIRNAME` (constant), lines 3787-3787, exports `ADMIN_STATE_DIRNAME`
- order 124: `ADMIN_CONFIG_FILENAME` (constant), lines 3788-3788, exports `ADMIN_CONFIG_FILENAME`
- order 125: `ADMIN_APPS_FILENAME` (constant), lines 3789-3789, exports `ADMIN_APPS_FILENAME`
- order 126: `ADMIN_TELEMETRY_FILENAME` (constant), lines 3790-3790, exports `ADMIN_TELEMETRY_FILENAME`
- order 127: `ADMIN_AUTH_FILENAME` (constant), lines 3791-3791, exports `ADMIN_AUTH_FILENAME`
- order 137: `ADMIN_MAX_APP_SKILLS` (constant), lines 3838-3838, exports `ADMIN_MAX_APP_SKILLS`
- order 138: `ADMIN_MAX_APP_CAPSULE_CHARS` (constant), lines 3839-3839, exports `ADMIN_MAX_APP_CAPSULE_CHARS`
- order 139: `ADMIN_MAX_APP_RESOURCE_FILES` (constant), lines 3840-3840, exports `ADMIN_MAX_APP_RESOURCE_FILES`
- order 140: `ADMIN_MAX_APP_RESOURCE_BYTES` (constant), lines 3841-3841, exports `ADMIN_MAX_APP_RESOURCE_BYTES`
- order 141: `ADMIN_APP_INLINE_BLOB_BYTES` (constant), lines 3842-3842, exports `ADMIN_APP_INLINE_BLOB_BYTES`
- order 142: `ADMIN_AUTH_SESSION_TTL_SECONDS` (constant), lines 3843-3843, exports `ADMIN_AUTH_SESSION_TTL_SECONDS`
- order 143: `ADMIN_AUTH_PASSWORD_ITERATIONS` (constant), lines 3844-3844, exports `ADMIN_AUTH_PASSWORD_ITERATIONS`
- order 144: `ADMIN_AUTH_MAX_ACTIVE_SESSIONS` (constant), lines 3845-3845, exports `ADMIN_AUTH_MAX_ACTIVE_SESSIONS`
- order 1170: `ADMIN_SKILLS_REVIEW_HTML` (constant), lines 117380-117381, exports `ADMIN_SKILLS_REVIEW_HTML`
- order 1171: `ADMIN_SKILLS_REVIEW_CSS` (constant), lines 117382-117382, exports `ADMIN_SKILLS_REVIEW_CSS`
- order 1172: `ADMIN_SKILLS_REVIEW_JS` (constant), lines 117383-117383, exports `ADMIN_SKILLS_REVIEW_JS`

### `agent/background.py`

- order 1001: `BackgroundManager` (class), lines 23036-23661, exports `BackgroundManager`

### `agent/bus.py`

- order 1002: `MessageBus` (class), lines 23662-23727, exports `MessageBus`

### `agent/errors.py`

- order 851: `CircuitBreakerTriggered` (class), lines 12129-12132, exports `CircuitBreakerTriggered`

### `agent/events.py`

- order 957: `EventHub` (class), lines 16316-16370, exports `EventHub`

### `agent/process.py`

- order 762: `subprocess_text_encodings` (function), lines 8166-8187, exports `subprocess_text_encodings`
- order 763: `decode_subprocess_bytes` (function), lines 8188-8214, exports `decode_subprocess_bytes`
- order 764: `run_subprocess_text` (function), lines 8215-8237, exports `run_subprocess_text`
- order 765: `windows_utf8_shell_command` (function), lines 8238-8244, exports `windows_utf8_shell_command`
- order 766: `shell_process_invocation` (function), lines 8245-8255, exports `shell_process_invocation`
- order 767: `join_shell_task_command` (function), lines 8256-8267, exports `join_shell_task_command`
- order 1000: `UserProcessManager` (class), lines 22676-23035, exports `UserProcessManager`

### `agent/tasks.py`

- order 998: `TaskManager` (class), lines 22535-22669, exports `TaskManager`

### `agent/todo.py`

- order 958: `TodoManager` (class), lines 16371-16731, exports `TodoManager`

### `agent/tools.py`

- order 952: `_ask_user_option_rows` (function), lines 16195-16228, exports `_ask_user_option_rows`
- order 953: `_ask_user_option_value` (function), lines 16229-16234, exports `_ask_user_option_value`
- order 1026: `tool_def` (function), lines 27849-27862, exports `tool_def`
- order 1027: `TOOLS` (constant), lines 27863-28410, exports `TOOLS`
- order 1028: `TOOL_REQUIRED_ARGS` (constant), lines 28411-28412, exports `TOOL_REQUIRED_ARGS`
- order 1029: `TOOL_SPEC_BY_NAME` (constant), lines 28413-28413, exports `TOOL_SPEC_BY_NAME`
- order 1030: `_for_28414` (statement), lines 28414-28423, exports `_tool`, `_fn`, `_name`, `_required`
- order 1031: `TOOL_NAME_FUZZY_MAP` (constant), lines 28424-28425, exports `TOOL_NAME_FUZZY_MAP`
- order 1032: `_for_28426` (statement), lines 28426-28429, exports `_name`, `_key`
- order 1033: `_for_28431` (statement), lines 28430-28447, exports `_alias`, `_target`
- order 1034: `is_todo_resume_tool_name` (function), lines 28448-28464, exports `is_todo_resume_tool_name`
- order 1035: `canonicalize_tool_name` (function), lines 28465-28483, exports `canonicalize_tool_name`
- order 1036: `filter_tool_specs_for_runtime` (function), lines 28484-28499, exports `filter_tool_specs_for_runtime`
- order 1037: `DEVELOPER_TOOL_DROP` (constant), lines 28500-28510, exports `DEVELOPER_TOOL_DROP`
- order 1038: `AGENT_TOOL_ALLOWLIST` (constant), lines 28511-28574, exports `AGENT_TOOL_ALLOWLIST`

### `agent/worktree.py`

- order 1003: `WorktreeManager` (class), lines 23728-23940, exports `WorktreeManager`

### `app/context.py`

- order 1173: `AppContext` (class), lines 117384-128100, exports `AppContext`

### `app/main.py`

- order 1188: `main` (function), lines 134846-136794, exports `main`
- order 1189: `_main_guard_136796` (main_guard), lines 136795-136797, exports —

### `app/services.py`

- order 1175: `TelemetryStore` (class), lines 128141-128516, exports `TelemetryStore`
- order 1176: `ApplicationRegistry` (class), lines 128517-129326, exports `ApplicationRegistry`

### `collaboration/core.py`

- order 88: `_now` (function), lines 401-404, exports `_now`
- order 89: `_json` (function), lines 405-408, exports `_json`
- order 90: `_load_json` (function), lines 409-415, exports `_load_json`
- order 91: `_b64_token` (function), lines 416-419, exports `_b64_token`
- order 92: `_branch_label` (function), lines 420-428, exports `_branch_label`
- order 93: `_digest` (function), lines 429-432, exports `_digest`
- order 94: `_password_hash` (function), lines 433-436, exports `_password_hash`
- order 95: `_normalize_ip` (function), lines 437-446, exports `_normalize_ip`
- order 96: `_normalize_name` (function), lines 447-453, exports `_normalize_name`
- order 97: `_COLLAB_PUBLIC_SECRET_PATTERNS` (assignment), lines 454-465, exports `_COLLAB_PUBLIC_SECRET_PATTERNS`
- order 98: `_collaboration_public_text` (function), lines 466-496, exports `_collaboration_public_text`
- order 99: `_collaboration_task_objective` (function), lines 497-521, exports `_collaboration_task_objective`
- order 100: `_collaboration_task_title` (function), lines 522-529, exports `_collaboration_task_title`
- order 101: `_collaboration_task_key` (function), lines 530-536, exports `_collaboration_task_key`
- order 102: `_collaboration_plan_steps` (function), lines 537-555, exports `_collaboration_plan_steps`
- order 103: `CollaborationError` (class), lines 556-563, exports `CollaborationError`
- order 104: `CollaborationPrincipal` (class), lines 564-574, exports `CollaborationPrincipal`
- order 105: `_normalize_operation` (function), lines 575-608, exports `_normalize_operation`
- order 106: `operation_input_length` (function), lines 609-612, exports `operation_input_length`
- order 107: `apply_text_operation` (function), lines 613-635, exports `apply_text_operation`
- order 108: `transform_text_operation` (function), lines 636-712, exports `transform_text_operation`
- order 109: `CollaborationStore` (class), lines 713-3426, exports `CollaborationStore`
- order 110: `CollaborationWriteCoordinator` (class), lines 3427-3640, exports `CollaborationWriteCoordinator`

### `collaboration/watcher.py`

- order 1186: `collaboration_file_watcher_loop` (function), lines 134755-134827, exports `collaboration_file_watcher_loop`
- order 1187: `collaboration_watcher_health` (function), lines 134828-134845, exports `collaboration_watcher_health`

### `config/bootstrap.py`

- order 71: `_EMBEDDED_LIQUID_KERNEL_PACKAGE_B64` (assignment), lines 78-330, exports `_EMBEDDED_LIQUID_KERNEL_PACKAGE_B64`
- order 72: `_ensure_embedded_liquid_kernel_package` (function), lines 331-376, exports `_ensure_embedded_liquid_kernel_package`
- order 913: `_liquid_kernel_history_present` (function), lines 14047-14051, exports `_liquid_kernel_history_present`
- order 914: `prepare_liquid_kernel_runtime` (function), lines 14052-14081, exports `prepare_liquid_kernel_runtime`
- order 915: `_persist_liquid_kernel_bootstrap` (function), lines 14082-14095, exports `_persist_liquid_kernel_bootstrap`

### `config/constants.py`

- order 73: `LIQUID_KERNEL_PACKAGE_STATUS` (constant), lines 377-379, exports `LIQUID_KERNEL_PACKAGE_STATUS`
- order 75: `COLLAB_DB_FILENAME` (constant), lines 386-388, exports `COLLAB_DB_FILENAME`
- order 76: `COLLAB_SESSION_TTL_SECONDS` (constant), lines 389-389, exports `COLLAB_SESSION_TTL_SECONDS`
- order 77: `COLLAB_PRESENCE_TTL_SECONDS` (constant), lines 390-390, exports `COLLAB_PRESENCE_TTL_SECONDS`
- order 78: `COLLAB_PASSWORD_ITERATIONS` (constant), lines 391-391, exports `COLLAB_PASSWORD_ITERATIONS`
- order 79: `COLLAB_MAX_AVATAR_BYTES` (constant), lines 392-392, exports `COLLAB_MAX_AVATAR_BYTES`
- order 80: `COLLAB_MAX_TEXT_BYTES` (constant), lines 393-393, exports `COLLAB_MAX_TEXT_BYTES`
- order 81: `COLLAB_DELETE_RETENTION_DAYS` (constant), lines 394-394, exports `COLLAB_DELETE_RETENTION_DAYS`
- order 82: `COLLAB_EVENT_RETENTION` (constant), lines 395-395, exports `COLLAB_EVENT_RETENTION`
- order 83: `COLLAB_AGENT_STALE_SECONDS` (constant), lines 396-396, exports `COLLAB_AGENT_STALE_SECONDS`
- order 84: `COLLAB_AGENT_HEARTBEAT_INTERVAL_SECONDS` (constant), lines 397-397, exports `COLLAB_AGENT_HEARTBEAT_INTERVAL_SECONDS`
- order 85: `COLLAB_EXTERNAL_WRITE_SETTLE_SECONDS` (constant), lines 398-398, exports `COLLAB_EXTERNAL_WRITE_SETTLE_SECONDS`
- order 86: `COLLAB_EXTERNAL_WRITE_CONFIRMATIONS` (constant), lines 399-399, exports `COLLAB_EXTERNAL_WRITE_CONFIRMATIONS`
- order 87: `COLLAB_SCHEMA_VERSION` (constant), lines 400-400, exports `COLLAB_SCHEMA_VERSION`
- order 111: `COLLAB_INDEX_HTML` (constant), lines 3641-3712, exports `COLLAB_INDEX_HTML`
- order 112: `COLLAB_CSS` (constant), lines 3713-3720, exports `COLLAB_CSS`
- order 113: `COLLAB_JS` (constant), lines 3721-3761, exports `COLLAB_JS`
- order 119: `APP_VERSION` (constant), lines 3783-3783, exports `APP_VERSION`
- order 128: `IDE_AUTH_FILENAME` (constant), lines 3792-3792, exports `IDE_AUTH_FILENAME`
- order 129: `IDE_AUTH_SESSION_TTL_SECONDS` (constant), lines 3793-3793, exports `IDE_AUTH_SESSION_TTL_SECONDS`
- order 130: `IDE_AUTH_MAX_ACTIVE_SESSIONS` (constant), lines 3794-3794, exports `IDE_AUTH_MAX_ACTIVE_SESSIONS`
- order 131: `IDE_DEVICE_SECRET_MIN_BYTES` (constant), lines 3795-3795, exports `IDE_DEVICE_SECRET_MIN_BYTES`
- order 132: `IDE_DEVICE_LABEL_MAX_CHARS` (constant), lines 3796-3796, exports `IDE_DEVICE_LABEL_MAX_CHARS`
- order 133: `IDE_DEVICE_PAIRING_TTL_SECONDS` (constant), lines 3797-3797, exports `IDE_DEVICE_PAIRING_TTL_SECONDS`
- order 134: `IDE_WORKBENCH_STATE_FILENAME` (constant), lines 3798-3798, exports `IDE_WORKBENCH_STATE_FILENAME`
- order 135: `IDE_PROMPT_ENHANCEMENT_BUDGETS` (constant), lines 3799-3836, exports `IDE_PROMPT_ENHANCEMENT_BUDGETS`
- order 136: `IDE_EXTENSIONS_DIRNAME` (constant), lines 3837-3837, exports `IDE_EXTENSIONS_DIRNAME`
- order 158: `LONG_OUTPUT_MODEL_PAGE_CHARS` (constant), lines 4140-4140, exports `LONG_OUTPUT_MODEL_PAGE_CHARS`
- order 159: `LONG_OUTPUT_UI_PAGE_CHARS` (constant), lines 4141-4141, exports `LONG_OUTPUT_UI_PAGE_CHARS`
- order 160: `LONG_OUTPUT_UI_PREVIEW_MAX_PAGES` (constant), lines 4142-4142, exports `LONG_OUTPUT_UI_PREVIEW_MAX_PAGES`
- order 161: `LONG_OUTPUT_LISTING_OFFLOAD_CHARS` (constant), lines 4143-4143, exports `LONG_OUTPUT_LISTING_OFFLOAD_CHARS`
- order 162: `LONG_OUTPUT_READ_PAGE_LINES` (constant), lines 4144-4144, exports `LONG_OUTPUT_READ_PAGE_LINES`
- order 163: `LONG_OUTPUT_READ_PAGE_MAX_CHARS` (constant), lines 4145-4145, exports `LONG_OUTPUT_READ_PAGE_MAX_CHARS`
- order 164: `LONG_OUTPUT_TEMP_MAX_FILES` (constant), lines 4146-4146, exports `LONG_OUTPUT_TEMP_MAX_FILES`
- order 165: `READ_FILE_DEFAULT_MAX_CHARS` (constant), lines 4147-4147, exports `READ_FILE_DEFAULT_MAX_CHARS`
- order 166: `READ_FILE_HARD_MAX_CHARS` (constant), lines 4148-4148, exports `READ_FILE_HARD_MAX_CHARS`
- order 167: `READ_FILE_OVERVIEW_HEAD_LINES` (constant), lines 4149-4149, exports `READ_FILE_OVERVIEW_HEAD_LINES`
- order 168: `READ_FILE_SEARCH_MAX_MATCHES` (constant), lines 4150-4150, exports `READ_FILE_SEARCH_MAX_MATCHES`
- order 173: `CODE_ADMIN_PORT_OFFSET` (constant), lines 4155-4155, exports `CODE_ADMIN_PORT_OFFSET`
- order 175: `IDE_PORT_OFFSET` (constant), lines 4157-4160, exports `IDE_PORT_OFFSET`
- order 176: `IDE_DEFAULT_PORT` (constant), lines 4161-4161, exports `IDE_DEFAULT_PORT`
- order 177: `COLLAB_PORT_OFFSET` (constant), lines 4162-4162, exports `COLLAB_PORT_OFFSET`
- order 179: `DEFAULT_WEB_SEARCH_ENABLED` (constant), lines 4164-4164, exports `DEFAULT_WEB_SEARCH_ENABLED`
- order 184: `DEFAULT_USER_MEMORY_MODE` (constant), lines 4169-4169, exports `DEFAULT_USER_MEMORY_MODE`
- order 192: `AGENT_WEB_SEARCH_USER_AGENT` (constant), lines 4180-4180, exports `AGENT_WEB_SEARCH_USER_AGENT`
- order 193: `AGENT_WEB_SEARCH_DEFAULT_MAX_RESULTS` (constant), lines 4181-4181, exports `AGENT_WEB_SEARCH_DEFAULT_MAX_RESULTS`
- order 194: `AGENT_WEB_SEARCH_DEFAULT_MAX_PAGES` (constant), lines 4182-4182, exports `AGENT_WEB_SEARCH_DEFAULT_MAX_PAGES`
- order 195: `AGENT_WEB_SEARCH_HARD_MAX_PAGES` (constant), lines 4183-4183, exports `AGENT_WEB_SEARCH_HARD_MAX_PAGES`
- order 196: `AGENT_WEB_SEARCH_DEFAULT_DEPTH` (constant), lines 4184-4184, exports `AGENT_WEB_SEARCH_DEFAULT_DEPTH`
- order 197: `AGENT_WEB_SEARCH_HARD_DEPTH` (constant), lines 4185-4185, exports `AGENT_WEB_SEARCH_HARD_DEPTH`
- order 198: `AGENT_WEB_SEARCH_FETCH_TIMEOUT` (constant), lines 4186-4186, exports `AGENT_WEB_SEARCH_FETCH_TIMEOUT`
- order 199: `AGENT_WEB_SEARCH_TOOL_SOFT_TIMEOUT` (constant), lines 4187-4187, exports `AGENT_WEB_SEARCH_TOOL_SOFT_TIMEOUT`
- order 200: `AGENT_WEB_SEARCH_MAX_PAGE_BYTES` (constant), lines 4188-4188, exports `AGENT_WEB_SEARCH_MAX_PAGE_BYTES`
- order 201: `AGENT_WEB_SEARCH_MAX_TEXT_CHARS` (constant), lines 4189-4189, exports `AGENT_WEB_SEARCH_MAX_TEXT_CHARS`
- order 202: `AGENT_WEB_SEARCH_PUBLIC_DISCOVERY_ENABLED` (constant), lines 4190-4192, exports `AGENT_WEB_SEARCH_PUBLIC_DISCOVERY_ENABLED`
- order 203: `AGENT_WEB_SEARCH_PUBLIC_FEED_URL` (constant), lines 4193-4193, exports `AGENT_WEB_SEARCH_PUBLIC_FEED_URL`
- order 204: `AGENT_WEB_SEARCH_PUBLIC_FEED_MAX_BYTES` (constant), lines 4194-4194, exports `AGENT_WEB_SEARCH_PUBLIC_FEED_MAX_BYTES`
- order 205: `AGENT_WEB_SEARCH_LOCAL_GRAPH_MAX_NODES` (constant), lines 4195-4195, exports `AGENT_WEB_SEARCH_LOCAL_GRAPH_MAX_NODES`
- order 206: `AGENT_WEB_SEARCH_LOCAL_GRAPH_MAX_EDGES` (constant), lines 4196-4196, exports `AGENT_WEB_SEARCH_LOCAL_GRAPH_MAX_EDGES`
- order 207: `AGENT_WEB_SEARCH_LOCAL_GRAPH_EDGE_SCAN_MULTIPLIER` (constant), lines 4197-4197, exports `AGENT_WEB_SEARCH_LOCAL_GRAPH_EDGE_SCAN_MULTIPLIER`
- order 208: `AGENT_WEB_SEARCH_LOCAL_GRAPH_PAGERANK_ITERATIONS` (constant), lines 4198-4198, exports `AGENT_WEB_SEARCH_LOCAL_GRAPH_PAGERANK_ITERATIONS`
- order 209: `AGENT_WEB_SEARCH_LOCAL_GRAPH_PAGERANK_DAMPING` (constant), lines 4199-4199, exports `AGENT_WEB_SEARCH_LOCAL_GRAPH_PAGERANK_DAMPING`
- order 210: `AGENT_WEB_SEARCH_LOCAL_GRAPH_AUTHORITY_BONUS_MAX` (constant), lines 4200-4200, exports `AGENT_WEB_SEARCH_LOCAL_GRAPH_AUTHORITY_BONUS_MAX`
- order 220: `CODE_CHUNK_CHARS` (constant), lines 4222-4222, exports `CODE_CHUNK_CHARS`
- order 221: `CODE_CHUNK_OVERLAP` (constant), lines 4223-4223, exports `CODE_CHUNK_OVERLAP`
- order 222: `CODE_MAX_CHUNKS_PER_DOC` (constant), lines 4224-4224, exports `CODE_MAX_CHUNKS_PER_DOC`
- order 223: `CODE_SOURCE_ANALYSIS_MAX_CHARS` (constant), lines 4225-4234, exports `CODE_SOURCE_ANALYSIS_MAX_CHARS`
- order 264: `CODE_IMPORT_WORKER_COUNT` (constant), lines 4303-4306, exports `CODE_IMPORT_WORKER_COUNT`
- order 266: `CODE_PARSE_TIMEOUT_SECONDS` (constant), lines 4311-4314, exports `CODE_PARSE_TIMEOUT_SECONDS`
- order 267: `DEFAULT_CONTEXT_TOKEN_LIMIT` (constant), lines 4315-4315, exports `DEFAULT_CONTEXT_TOKEN_LIMIT`
- order 268: `TOKEN_THRESHOLD` (constant), lines 4316-4316, exports `TOKEN_THRESHOLD`
- order 269: `CONTEXT_AUTO_COMPACT_RESERVE_RATIO` (constant), lines 4317-4320, exports `CONTEXT_AUTO_COMPACT_RESERVE_RATIO`
- order 270: `CONTEXT_ESTIMATE_SAFETY_MULTIPLIER` (constant), lines 4321-4324, exports `CONTEXT_ESTIMATE_SAFETY_MULTIPLIER`
- order 271: `CONTEXT_USAGE_CALIBRATION_MAX` (constant), lines 4325-4328, exports `CONTEXT_USAGE_CALIBRATION_MAX`
- order 272: `CONTEXT_ACTUAL_USAGE_RECENT_SECONDS` (constant), lines 4329-4332, exports `CONTEXT_ACTUAL_USAGE_RECENT_SECONDS`
- order 273: `LARGE_FILE_AUTO_PAGE_BYTES` (constant), lines 4333-4336, exports `LARGE_FILE_AUTO_PAGE_BYTES`
- order 274: `LARGE_FILE_AUTO_PAGE_LINES` (constant), lines 4337-4340, exports `LARGE_FILE_AUTO_PAGE_LINES`
- order 275: `LARGE_SOURCE_UPLOAD_EXCERPT_CHARS` (constant), lines 4341-4344, exports `LARGE_SOURCE_UPLOAD_EXCERPT_CHARS`
- order 276: `CHAT_UPLOAD_PARSE_QUEUE_MAX` (constant), lines 4345-4348, exports `CHAT_UPLOAD_PARSE_QUEUE_MAX`
- order 277: `CHAT_UPLOAD_PARSE_TIMEOUT_SECONDS` (constant), lines 4349-4352, exports `CHAT_UPLOAD_PARSE_TIMEOUT_SECONDS`
- order 278: `CHAT_UPLOAD_INLINE_TEXT_BYTES` (constant), lines 4353-4356, exports `CHAT_UPLOAD_INLINE_TEXT_BYTES`
- order 279: `CHAT_UPLOAD_PARSE_MAX_BYTES` (constant), lines 4357-4363, exports `CHAT_UPLOAD_PARSE_MAX_BYTES`
- order 280: `CHAT_UPLOAD_ZIP_ENTRY_MAX_BYTES` (constant), lines 4364-4370, exports `CHAT_UPLOAD_ZIP_ENTRY_MAX_BYTES`
- order 281: `CHAT_UPLOAD_TEXT_CONTEXT_CHARS` (constant), lines 4371-4374, exports `CHAT_UPLOAD_TEXT_CONTEXT_CHARS`
- order 282: `CHAT_UPLOAD_PROMPT_MAX_FILES` (constant), lines 4375-4378, exports `CHAT_UPLOAD_PROMPT_MAX_FILES`
- order 283: `CHAT_UPLOAD_PROMPT_MAX_CHARS` (constant), lines 4379-4382, exports `CHAT_UPLOAD_PROMPT_MAX_CHARS`
- order 284: `CHAT_UPLOAD_PROMPT_PER_FILE_CHARS` (constant), lines 4383-4386, exports `CHAT_UPLOAD_PROMPT_PER_FILE_CHARS`
- order 285: `CHAT_UPLOAD_FRONTEND_WAIT_MS` (constant), lines 4387-4390, exports `CHAT_UPLOAD_FRONTEND_WAIT_MS`
- order 286: `CHAT_UPLOAD_AUTO_LIBRARY_INGEST` (constant), lines 4391-4394, exports `CHAT_UPLOAD_AUTO_LIBRARY_INGEST`
- order 287: `CHAT_UPLOAD_INGEST_QUEUE_MAX` (constant), lines 4395-4398, exports `CHAT_UPLOAD_INGEST_QUEUE_MAX`
- order 288: `SESSION_SUBMIT_LOCK_TIMEOUT_SECONDS` (constant), lines 4399-4402, exports `SESSION_SUBMIT_LOCK_TIMEOUT_SECONDS`
- order 289: `SESSION_DEFERRED_START_QUEUE_MAX` (constant), lines 4403-4406, exports `SESSION_DEFERRED_START_QUEUE_MAX`
- order 290: `SESSION_SUBMISSION_DEDUPE_MAX` (constant), lines 4407-4407, exports `SESSION_SUBMISSION_DEDUPE_MAX`
- order 291: `SESSION_SUBMISSION_DEDUPE_SECONDS` (constant), lines 4408-4408, exports `SESSION_SUBMISSION_DEDUPE_SECONDS`
- order 292: `SCHEDULER_SUBMISSION_DEDUPE_MAX` (constant), lines 4409-4409, exports `SCHEDULER_SUBMISSION_DEDUPE_MAX`
- order 293: `FAST_START_LOCAL_CLASSIFICATION` (constant), lines 4410-4412, exports `FAST_START_LOCAL_CLASSIFICATION`
- order 294: `FAST_START_LOCAL_TITLE` (constant), lines 4413-4415, exports `FAST_START_LOCAL_TITLE`
- order 295: `AUTO_TITLE_MODEL_REFINE` (constant), lines 4416-4418, exports `AUTO_TITLE_MODEL_REFINE`
- order 296: `AUTO_TITLE_MODEL_TIMEOUT_SECONDS` (constant), lines 4419-4422, exports `AUTO_TITLE_MODEL_TIMEOUT_SECONDS`
- order 297: `AUTO_TITLE_MODEL_RETRY_COOLDOWN_SECONDS` (constant), lines 4423-4429, exports `AUTO_TITLE_MODEL_RETRY_COOLDOWN_SECONDS`
- order 298: `FAST_START_DEFER_CAPABILITY_PROBE` (constant), lines 4430-4432, exports `FAST_START_DEFER_CAPABILITY_PROBE`
- order 299: `SESSION_RUNTIME_MESSAGE_WINDOW` (constant), lines 4433-4433, exports `SESSION_RUNTIME_MESSAGE_WINDOW`
- order 300: `SESSION_RUNTIME_ACTIVITY_WINDOW` (constant), lines 4434-4434, exports `SESSION_RUNTIME_ACTIVITY_WINDOW`
- order 301: `SESSION_RUNTIME_OPERATION_WINDOW` (constant), lines 4435-4435, exports `SESSION_RUNTIME_OPERATION_WINDOW`
- order 302: `SESSION_RUNTIME_UPLOAD_WINDOW` (constant), lines 4436-4436, exports `SESSION_RUNTIME_UPLOAD_WINDOW`
- order 303: `LITE_SNAPSHOT_MAX_BYTES` (constant), lines 4437-4440, exports `LITE_SNAPSHOT_MAX_BYTES`
- order 304: `LITE_SNAPSHOT_MESSAGES_BYTES` (constant), lines 4441-4441, exports `LITE_SNAPSHOT_MESSAGES_BYTES`
- order 305: `LITE_SNAPSHOT_FEED_BYTES` (constant), lines 4442-4442, exports `LITE_SNAPSHOT_FEED_BYTES`
- order 306: `LITE_SNAPSHOT_OPERATIONS_BYTES` (constant), lines 4443-4443, exports `LITE_SNAPSHOT_OPERATIONS_BYTES`
- order 307: `IDE_AGENT_STATE_MAX_BYTES` (constant), lines 4444-4447, exports `IDE_AGENT_STATE_MAX_BYTES`
- order 308: `IDE_AGENT_FEED_BYTES` (constant), lines 4448-4448, exports `IDE_AGENT_FEED_BYTES`
- order 309: `IDE_AGENT_OPERATIONS_BYTES` (constant), lines 4449-4449, exports `IDE_AGENT_OPERATIONS_BYTES`
- order 310: `SESSION_WATCHDOG_INTERVAL_SECONDS` (constant), lines 4450-4453, exports `SESSION_WATCHDOG_INTERVAL_SECONDS`
- order 311: `SESSION_HEARTBEAT_STALE_SECONDS` (constant), lines 4454-4457, exports `SESSION_HEARTBEAT_STALE_SECONDS`
- order 312: `SESSION_LIST_DEFAULT_LIMIT` (constant), lines 4458-4461, exports `SESSION_LIST_DEFAULT_LIMIT`
- order 313: `SESSION_INDEX_SYNC_SNAPSHOT_MAX` (constant), lines 4462-4465, exports `SESSION_INDEX_SYNC_SNAPSHOT_MAX`
- order 314: `SESSION_INDEX_JOURNAL_COMPACT_RECORDS` (constant), lines 4466-4469, exports `SESSION_INDEX_JOURNAL_COMPACT_RECORDS`
- order 315: `SESSION_INDEX_JOURNAL_COMPACT_BYTES` (constant), lines 4470-4473, exports `SESSION_INDEX_JOURNAL_COMPACT_BYTES`
- order 316: `SESSION_CATALOG_RECENT_MAX` (constant), lines 4474-4477, exports `SESSION_CATALOG_RECENT_MAX`
- order 317: `IDE_SESSION_LIST_DEFAULT_LIMIT` (constant), lines 4478-4481, exports `IDE_SESSION_LIST_DEFAULT_LIMIT`
- order 318: `IDLE_TIMEOUT` (constant), lines 4482-4482, exports `IDLE_TIMEOUT`
- order 319: `POLL_INTERVAL` (constant), lines 4483-4483, exports `POLL_INTERVAL`
- order 320: `SSE_HEARTBEAT_SECONDS` (constant), lines 4484-4484, exports `SSE_HEARTBEAT_SECONDS`
- order 321: `MODEL_CALL_PROGRESS_DELAY` (constant), lines 4485-4485, exports `MODEL_CALL_PROGRESS_DELAY`
- order 322: `MODEL_CALL_PROGRESS_INTERVAL` (constant), lines 4486-4486, exports `MODEL_CALL_PROGRESS_INTERVAL`
- order 323: `RUN_COMPLETION_SUMMARY_ENABLED` (constant), lines 4487-4490, exports `RUN_COMPLETION_SUMMARY_ENABLED`
- order 324: `LLM_HTTP_RETRY_MAX_ATTEMPTS` (constant), lines 4491-4494, exports `LLM_HTTP_RETRY_MAX_ATTEMPTS`
- order 325: `LLM_HTTP_RETRY_DELAY_SECONDS` (constant), lines 4495-4498, exports `LLM_HTTP_RETRY_DELAY_SECONDS`
- order 326: `LLM_HTTP_RETRY_MAX_SECONDS` (constant), lines 4499-4502, exports `LLM_HTTP_RETRY_MAX_SECONDS`
- order 327: `LLM_HTTP_RETRY_404_ON_VLLM` (constant), lines 4503-4506, exports `LLM_HTTP_RETRY_404_ON_VLLM`
- order 328: `LLM_HTTP_RETRY_STATUSES` (constant), lines 4507-4507, exports `LLM_HTTP_RETRY_STATUSES`
- order 329: `MAX_AGENT_ROUNDS` (constant), lines 4508-4508, exports `MAX_AGENT_ROUNDS`
- order 330: `MIN_AGENT_ROUNDS` (constant), lines 4509-4509, exports `MIN_AGENT_ROUNDS`
- order 331: `MAX_AGENT_ROUNDS_CAP` (constant), lines 4510-4510, exports `MAX_AGENT_ROUNDS_CAP`
- order 332: `REPEATED_TOOL_LOOP_THRESHOLD` (constant), lines 4511-4511, exports `REPEATED_TOOL_LOOP_THRESHOLD`
- order 333: `BASH_READ_LOOP_THRESHOLD` (constant), lines 4512-4512, exports `BASH_READ_LOOP_THRESHOLD`
- order 334: `READ_FILE_LOOP_THRESHOLD` (constant), lines 4513-4513, exports `READ_FILE_LOOP_THRESHOLD`
- order 335: `READ_FILE_LOOP_DISTINCT_SOFT_LIMIT` (constant), lines 4514-4514, exports `READ_FILE_LOOP_DISTINCT_SOFT_LIMIT`
- order 336: `READ_FILE_COMPACT_PIN_DISTINCT` (constant), lines 4515-4515, exports `READ_FILE_COMPACT_PIN_DISTINCT`
- order 337: `READ_FILE_COMPACT_PIN_MAX_CHARS` (constant), lines 4516-4516, exports `READ_FILE_COMPACT_PIN_MAX_CHARS`
- order 338: `READ_CONTEXT_REGISTRY_MAX` (constant), lines 4517-4517, exports `READ_CONTEXT_REGISTRY_MAX`
- order 339: `READ_CONTEXT_PROMPT_MAX_ITEMS` (constant), lines 4518-4518, exports `READ_CONTEXT_PROMPT_MAX_ITEMS`
- order 340: `READ_CONTEXT_PROMPT_MAX_CHARS` (constant), lines 4519-4519, exports `READ_CONTEXT_PROMPT_MAX_CHARS`
- order 341: `READ_CONTEXT_SUMMARY_MAX_CHARS` (constant), lines 4520-4520, exports `READ_CONTEXT_SUMMARY_MAX_CHARS`
- order 342: `READ_CONTEXT_SHARED_MAX_ITEMS` (constant), lines 4521-4521, exports `READ_CONTEXT_SHARED_MAX_ITEMS`
- order 343: `READ_CONTEXT_POLICY_CHOICES` (constant), lines 4522-4522, exports `READ_CONTEXT_POLICY_CHOICES`
- order 344: `DEFAULT_READ_CONTEXT_POLICY` (constant), lines 4523-4523, exports `DEFAULT_READ_CONTEXT_POLICY`
- order 345: `READ_CONTEXT_CACHE_SEARCH_MAX_BYTES` (constant), lines 4524-4530, exports `READ_CONTEXT_CACHE_SEARCH_MAX_BYTES`
- order 346: `READ_CONTEXT_CACHE_SEARCH_MAX_MATCHES` (constant), lines 4531-4531, exports `READ_CONTEXT_CACHE_SEARCH_MAX_MATCHES`
- order 347: `READ_CONTEXT_CACHE_SNIPPET_CHARS` (constant), lines 4532-4532, exports `READ_CONTEXT_CACHE_SNIPPET_CHARS`
- order 348: `READ_CONTEXT_CACHE_LINE_CONTEXT` (constant), lines 4533-4533, exports `READ_CONTEXT_CACHE_LINE_CONTEXT`
- order 349: `LONG_CONTENT_SOURCE_CACHE_MAX_BYTES` (constant), lines 4534-4540, exports `LONG_CONTENT_SOURCE_CACHE_MAX_BYTES`
- order 350: `LONG_CONTENT_SOURCE_CACHE_MAX_FILES` (constant), lines 4541-4544, exports `LONG_CONTENT_SOURCE_CACHE_MAX_FILES`
- order 351: `LONG_CONTENT_SYMBOL_MEMORY_MAX` (constant), lines 4545-4548, exports `LONG_CONTENT_SYMBOL_MEMORY_MAX`
- order 352: `TOOL_MEMORY_REGISTRY_MAX` (constant), lines 4549-4549, exports `TOOL_MEMORY_REGISTRY_MAX`
- order 353: `TOOL_MEMORY_PROMPT_MAX_ITEMS` (constant), lines 4550-4550, exports `TOOL_MEMORY_PROMPT_MAX_ITEMS`
- order 354: `TOOL_MEMORY_PROMPT_MAX_CHARS` (constant), lines 4551-4551, exports `TOOL_MEMORY_PROMPT_MAX_CHARS`
- order 355: `TOOL_MEMORY_SUMMARY_MAX_CHARS` (constant), lines 4552-4552, exports `TOOL_MEMORY_SUMMARY_MAX_CHARS`
- order 356: `TOOL_MEMORY_SHARED_MAX_ITEMS` (constant), lines 4553-4553, exports `TOOL_MEMORY_SHARED_MAX_ITEMS`
- order 357: `TOOL_MEMORY_COMPACT_PIN_DISTINCT` (constant), lines 4554-4554, exports `TOOL_MEMORY_COMPACT_PIN_DISTINCT`
- order 358: `TOOL_MEMORY_COMPACT_PIN_MAX_CHARS` (constant), lines 4555-4555, exports `TOOL_MEMORY_COMPACT_PIN_MAX_CHARS`
- order 359: `TOOL_MEMORY_POLICY_CHOICES` (constant), lines 4556-4556, exports `TOOL_MEMORY_POLICY_CHOICES`
- order 360: `DEFAULT_TOOL_MEMORY_POLICY` (constant), lines 4557-4557, exports `DEFAULT_TOOL_MEMORY_POLICY`
- order 361: `LONG_CONTENT_MEMORY_VERSION` (constant), lines 4558-4570, exports `LONG_CONTENT_MEMORY_VERSION`
- order 362: `LONG_CONTENT_MEMORY_MAX_ITEMS` (constant), lines 4571-4574, exports `LONG_CONTENT_MEMORY_MAX_ITEMS`
- order 363: `LONG_CONTENT_MEMORY_MAX_SEGMENTS` (constant), lines 4575-4578, exports `LONG_CONTENT_MEMORY_MAX_SEGMENTS`
- order 364: `LONG_CONTENT_TEXT_SEGMENT_LINES` (constant), lines 4579-4582, exports `LONG_CONTENT_TEXT_SEGMENT_LINES`
- order 365: `LONG_CONTENT_CODE_SEGMENT_LINES` (constant), lines 4583-4586, exports `LONG_CONTENT_CODE_SEGMENT_LINES`
- order 366: `LONG_CONTENT_CARD_CHARS` (constant), lines 4587-4590, exports `LONG_CONTENT_CARD_CHARS`
- order 367: `LONG_CONTENT_STRUCTURE_MAX_CHARS` (constant), lines 4591-4594, exports `LONG_CONTENT_STRUCTURE_MAX_CHARS`
- order 368: `LONG_CONTENT_SEMANTIC_ENABLED` (constant), lines 4595-4602, exports `LONG_CONTENT_SEMANTIC_ENABLED`
- order 369: `LONG_CONTENT_SEMANTIC_TIMEOUT_SECONDS` (constant), lines 4603-4606, exports `LONG_CONTENT_SEMANTIC_TIMEOUT_SECONDS`
- order 370: `LONG_CONTENT_SEMANTIC_MAX_INPUT_CHARS` (constant), lines 4607-4610, exports `LONG_CONTENT_SEMANTIC_MAX_INPUT_CHARS`
- order 371: `LONG_CONTENT_SEMANTIC_MAX_OUTPUT_TOKENS` (constant), lines 4611-4614, exports `LONG_CONTENT_SEMANTIC_MAX_OUTPUT_TOKENS`
- order 372: `LONG_CONTENT_SEMANTIC_MAX_KEY_POINTS` (constant), lines 4615-4615, exports `LONG_CONTENT_SEMANTIC_MAX_KEY_POINTS`
- order 373: `LONG_CONTENT_SEMANTIC_MAX_DEFINITIONS` (constant), lines 4616-4616, exports `LONG_CONTENT_SEMANTIC_MAX_DEFINITIONS`
- order 374: `LONG_CONTENT_SEMANTIC_MAX_RELATIONS` (constant), lines 4617-4617, exports `LONG_CONTENT_SEMANTIC_MAX_RELATIONS`
- order 375: `LONG_CONTENT_SEMANTIC_MAX_UNCERTAINTIES` (constant), lines 4618-4618, exports `LONG_CONTENT_SEMANTIC_MAX_UNCERTAINTIES`
- order 376: `LONG_CONTENT_SEMANTIC_MAX_EVIDENCE` (constant), lines 4619-4619, exports `LONG_CONTENT_SEMANTIC_MAX_EVIDENCE`
- order 377: `LONG_CONTENT_SEMANTIC_MAX_NEXT_SEGMENTS` (constant), lines 4620-4620, exports `LONG_CONTENT_SEMANTIC_MAX_NEXT_SEGMENTS`
- order 378: `LONG_CONTENT_SEMANTIC_MAX_COVERED` (constant), lines 4621-4621, exports `LONG_CONTENT_SEMANTIC_MAX_COVERED`
- order 379: `LONG_CONTENT_SEMANTIC_MAX_OPEN_QUESTIONS` (constant), lines 4622-4622, exports `LONG_CONTENT_SEMANTIC_MAX_OPEN_QUESTIONS`
- order 380: `LONG_CONTENT_SEMANTIC_MAX_REFRESHES` (constant), lines 4623-4626, exports `LONG_CONTENT_SEMANTIC_MAX_REFRESHES`
- order 381: `LONG_CONTENT_OBSERVATION_MAX` (constant), lines 4627-4630, exports `LONG_CONTENT_OBSERVATION_MAX`
- order 382: `LONG_CONTENT_OBSERVATION_MAX_RANGES` (constant), lines 4631-4631, exports `LONG_CONTENT_OBSERVATION_MAX_RANGES`
- order 383: `LONG_CONTENT_OBSERVATION_MAX_EXCERPTS` (constant), lines 4632-4632, exports `LONG_CONTENT_OBSERVATION_MAX_EXCERPTS`
- order 384: `LONG_CONTENT_OBSERVATION_EXCERPT_CHARS` (constant), lines 4633-4633, exports `LONG_CONTENT_OBSERVATION_EXCERPT_CHARS`
- order 385: `LONG_CONTENT_RELATED_SOURCE_MAX` (constant), lines 4634-4634, exports `LONG_CONTENT_RELATED_SOURCE_MAX`
- order 386: `SHELL_SOURCE_CANDIDATE_MAX` (constant), lines 4635-4635, exports `SHELL_SOURCE_CANDIDATE_MAX`
- order 387: `LONG_CONTENT_TEXT_EXTS` (constant), lines 4636-4638, exports `LONG_CONTENT_TEXT_EXTS`
- order 388: `LONG_CONTENT_DATA_EXTS` (constant), lines 4639-4643, exports `LONG_CONTENT_DATA_EXTS`
- order 389: `DEFAULT_AUTO_TASK_LEVEL_CEILING` (constant), lines 4644-4644, exports `DEFAULT_AUTO_TASK_LEVEL_CEILING`
- order 390: `HARD_BREAK_TOOL_ERROR_THRESHOLD` (constant), lines 4645-4645, exports `HARD_BREAK_TOOL_ERROR_THRESHOLD`
- order 391: `HARD_BREAK_RECOVERY_ROUND_THRESHOLD` (constant), lines 4646-4648, exports `HARD_BREAK_RECOVERY_ROUND_THRESHOLD`
- order 392: `FUSED_FAULT_BREAK_THRESHOLD` (constant), lines 4649-4649, exports `FUSED_FAULT_BREAK_THRESHOLD`
- order 393: `STALL_SEVERITY_ESCALATION_THRESHOLD` (constant), lines 4650-4650, exports `STALL_SEVERITY_ESCALATION_THRESHOLD`
- order 394: `STALL_SEVERITY_WEIGHT_BASH_READ_LOOP` (constant), lines 4651-4651, exports `STALL_SEVERITY_WEIGHT_BASH_READ_LOOP`
- order 395: `STALL_SEVERITY_WEIGHT_REPEATED_TOOL` (constant), lines 4652-4652, exports `STALL_SEVERITY_WEIGHT_REPEATED_TOOL`
- order 396: `STALL_SEVERITY_WEIGHT_FAULT` (constant), lines 4653-4653, exports `STALL_SEVERITY_WEIGHT_FAULT`
- order 397: `STALL_SEVERITY_WEIGHT_RECOVERY_RETRY` (constant), lines 4654-4654, exports `STALL_SEVERITY_WEIGHT_RECOVERY_RETRY`
- order 398: `STALL_SEVERITY_WEIGHT_WATCHDOG` (constant), lines 4655-4655, exports `STALL_SEVERITY_WEIGHT_WATCHDOG`
- order 399: `STALL_SEVERITY_DECAY_ON_SUCCESS` (constant), lines 4656-4656, exports `STALL_SEVERITY_DECAY_ON_SUCCESS`
- order 400: `STALL_ESCALATION_MIN_LEVEL` (constant), lines 4657-4657, exports `STALL_ESCALATION_MIN_LEVEL`
- order 401: `STALL_PLAN_SYNTHESIS_MAX_TOKENS` (constant), lines 4658-4658, exports `STALL_PLAN_SYNTHESIS_MAX_TOKENS`
- order 402: `STALL_ESCALATION_CONTEXT_MAX_CHARS` (constant), lines 4659-4659, exports `STALL_ESCALATION_CONTEXT_MAX_CHARS`
- order 403: `MAX_RUN_SECONDS` (constant), lines 4660-4660, exports `MAX_RUN_SECONDS`
- order 404: `MIN_RUN_TIMEOUT_SECONDS` (constant), lines 4661-4661, exports `MIN_RUN_TIMEOUT_SECONDS`
- order 405: `MAX_RUN_TIMEOUT_SECONDS` (constant), lines 4662-4662, exports `MAX_RUN_TIMEOUT_SECONDS`
- order 406: `MIN_TIMEOUT_SECONDS` (constant), lines 4663-4663, exports `MIN_TIMEOUT_SECONDS`
- order 407: `MAX_TIMEOUT_SECONDS` (constant), lines 4664-4664, exports `MAX_TIMEOUT_SECONDS`
- order 408: `DEFAULT_TIMEOUT_SECONDS` (constant), lines 4665-4671, exports `DEFAULT_TIMEOUT_SECONDS`
- order 409: `DEFAULT_REQUEST_TIMEOUT` (constant), lines 4672-4672, exports `DEFAULT_REQUEST_TIMEOUT`
- order 410: `_SHELL_AUTO_CONFIRM_PATTERNS` (assignment), lines 4673-4688, exports `_SHELL_AUTO_CONFIRM_PATTERNS`
- order 411: `MIN_SHELL_COMMAND_TIMEOUT_SECONDS` (constant), lines 4689-4689, exports `MIN_SHELL_COMMAND_TIMEOUT_SECONDS`
- order 412: `MAX_SHELL_COMMAND_TIMEOUT_SECONDS` (constant), lines 4690-4690, exports `MAX_SHELL_COMMAND_TIMEOUT_SECONDS`
- order 413: `SHELL_TIMEOUT_MODES` (constant), lines 4691-4691, exports `SHELL_TIMEOUT_MODES`
- order 414: `_DEFAULT_SHELL_TIMEOUT_MODE_RAW` (assignment), lines 4692-4695, exports `_DEFAULT_SHELL_TIMEOUT_MODE_RAW`
- order 415: `DEFAULT_SHELL_TIMEOUT_MODE` (constant), lines 4696-4700, exports `DEFAULT_SHELL_TIMEOUT_MODE`
- order 416: `MIN_SHELL_ASYNC_HANDOFF_SECONDS` (constant), lines 4701-4701, exports `MIN_SHELL_ASYNC_HANDOFF_SECONDS`
- order 417: `MAX_SHELL_ASYNC_HANDOFF_SECONDS` (constant), lines 4702-4702, exports `MAX_SHELL_ASYNC_HANDOFF_SECONDS`
- order 418: `SHELL_FAILURE_GUIDANCE_SECONDS` (constant), lines 4703-4705, exports `SHELL_FAILURE_GUIDANCE_SECONDS`
- order 419: `DEFAULT_SHELL_ASYNC_HANDOFF_SECONDS` (constant), lines 4706-4720, exports `DEFAULT_SHELL_ASYNC_HANDOFF_SECONDS`
- order 420: `DEFAULT_SHELL_COMMAND_TIMEOUT_SECONDS` (constant), lines 4721-4735, exports `DEFAULT_SHELL_COMMAND_TIMEOUT_SECONDS`
- order 421: `DEFAULT_SINGLE_NO_PLAN_TODO_PROMPT` (constant), lines 4736-4750, exports `DEFAULT_SINGLE_NO_PLAN_TODO_PROMPT`
- order 422: `SINGLE_NO_PLAN_TODO_BOOTSTRAP_MAX_ATTEMPTS` (constant), lines 4751-4751, exports `SINGLE_NO_PLAN_TODO_BOOTSTRAP_MAX_ATTEMPTS`
- order 423: `AUTO_CONTINUE_BUDGET_DEFAULT` (constant), lines 4752-4752, exports `AUTO_CONTINUE_BUDGET_DEFAULT`
- order 424: `AGENT_MAX_OUTPUT_TOKENS` (constant), lines 4753-4753, exports `AGENT_MAX_OUTPUT_TOKENS`
- order 425: `OLLAMA_THINKING_TOOL_BUFFER` (constant), lines 4754-4754, exports `OLLAMA_THINKING_TOOL_BUFFER`
- order 426: `WATCHDOG_INTENT_NO_TOOL_THRESHOLD` (constant), lines 4755-4755, exports `WATCHDOG_INTENT_NO_TOOL_THRESHOLD`
- order 427: `WATCHDOG_REPEAT_NO_TOOL_THRESHOLD` (constant), lines 4756-4756, exports `WATCHDOG_REPEAT_NO_TOOL_THRESHOLD`
- order 428: `WATCHDOG_INTENT_NO_TOOL_THRESHOLD_SINGLE` (constant), lines 4757-4757, exports `WATCHDOG_INTENT_NO_TOOL_THRESHOLD_SINGLE`
- order 429: `WATCHDOG_REPEAT_NO_TOOL_THRESHOLD_SINGLE` (constant), lines 4758-4758, exports `WATCHDOG_REPEAT_NO_TOOL_THRESHOLD_SINGLE`
- order 430: `WATCHDOG_STATE_STALL_THRESHOLD` (constant), lines 4759-4759, exports `WATCHDOG_STATE_STALL_THRESHOLD`
- order 431: `WATCHDOG_CONTEXT_STALL_THRESHOLD` (constant), lines 4760-4760, exports `WATCHDOG_CONTEXT_STALL_THRESHOLD`
- order 432: `WATCHDOG_REPEAT_SIMILARITY_THRESHOLD` (constant), lines 4761-4761, exports `WATCHDOG_REPEAT_SIMILARITY_THRESHOLD`
- order 433: `WATCHDOG_CONTEXT_NEAR_RATIO` (constant), lines 4762-4762, exports `WATCHDOG_CONTEXT_NEAR_RATIO`
- order 434: `WATCHDOG_MAX_DECOMPOSE_STEPS` (constant), lines 4763-4763, exports `WATCHDOG_MAX_DECOMPOSE_STEPS`
- order 435: `WATCHDOG_STEP_MAX_ATTEMPTS` (constant), lines 4764-4764, exports `WATCHDOG_STEP_MAX_ATTEMPTS`
- order 436: `EMPTY_ACTION_MIN_CONTENT_CHARS` (constant), lines 4765-4765, exports `EMPTY_ACTION_MIN_CONTENT_CHARS`
- order 437: `EMPTY_ACTION_WAKEUP_RETRY_LIMIT` (constant), lines 4766-4766, exports `EMPTY_ACTION_WAKEUP_RETRY_LIMIT`
- order 438: `EMPTY_ACTION_INTERVENTION_THRESHOLD` (constant), lines 4767-4773, exports `EMPTY_ACTION_INTERVENTION_THRESHOLD`
- order 439: `EMPTY_ACTION_BOOTSTRAP_THINKING_GRACE_ROUNDS` (constant), lines 4774-4778, exports `EMPTY_ACTION_BOOTSTRAP_THINKING_GRACE_ROUNDS`
- order 440: `EMPTY_ACTION_RECOVERY_MAX_TOKENS` (constant), lines 4779-4779, exports `EMPTY_ACTION_RECOVERY_MAX_TOKENS`
- order 441: `THINKING_BUDGET_FORCE_RATIO` (constant), lines 4780-4780, exports `THINKING_BUDGET_FORCE_RATIO`
- order 442: `_TOOL_TIMEOUT_MAP` (assignment), lines 4781-4802, exports `_TOOL_TIMEOUT_MAP`
- order 443: `_DEFAULT_TOOL_TIMEOUT` (assignment), lines 4803-4803, exports `_DEFAULT_TOOL_TIMEOUT`
- order 444: `CONVERSATION_VISIBLE_TOOL_EVENTS` (constant), lines 4804-4816, exports `CONVERSATION_VISIBLE_TOOL_EVENTS`
- order 445: `PERSIST_ON_EVENT_TYPES` (constant), lines 4817-4835, exports `PERSIST_ON_EVENT_TYPES`
- order 446: `PERSIST_EVENT_MIN_INTERVAL_SECONDS` (constant), lines 4836-4836, exports `PERSIST_EVENT_MIN_INTERVAL_SECONDS`
- order 447: `TRUNCATION_CONTINUATION_MAX_PASSES` (constant), lines 4837-4837, exports `TRUNCATION_CONTINUATION_MAX_PASSES`
- order 448: `TRUNCATION_CONTINUATION_MAX_TOKENS` (constant), lines 4838-4838, exports `TRUNCATION_CONTINUATION_MAX_TOKENS`
- order 449: `TRUNCATION_CONTINUATION_TAIL_CHARS` (constant), lines 4839-4839, exports `TRUNCATION_CONTINUATION_TAIL_CHARS`
- order 450: `TRUNCATION_CONTINUATION_ECHO_CHARS` (constant), lines 4840-4840, exports `TRUNCATION_CONTINUATION_ECHO_CHARS`
- order 451: `TRUNCATION_OVERLAP_SCAN_CHARS` (constant), lines 4841-4841, exports `TRUNCATION_OVERLAP_SCAN_CHARS`
- order 452: `TRUNCATION_PAIR_SCAN_CHARS` (constant), lines 4842-4842, exports `TRUNCATION_PAIR_SCAN_CHARS`
- order 453: `TRUNCATION_LIVE_BUFFER_MAX_CHARS` (constant), lines 4843-4843, exports `TRUNCATION_LIVE_BUFFER_MAX_CHARS`
- order 454: `MIN_CONTEXT_TOKEN_LIMIT` (constant), lines 4844-4844, exports `MIN_CONTEXT_TOKEN_LIMIT`
- order 455: `COMPACT_TIER1_PCT` (constant), lines 4845-4846, exports `COMPACT_TIER1_PCT`
- order 456: `COMPACT_TIER2_PCT` (constant), lines 4847-4847, exports `COMPACT_TIER2_PCT`
- order 457: `COMPACT_TIER3_PCT` (constant), lines 4848-4848, exports `COMPACT_TIER3_PCT`
- order 458: `COMPACT_TIER1_ABS` (constant), lines 4849-4850, exports `COMPACT_TIER1_ABS`
- order 459: `COMPACT_TIER2_ABS` (constant), lines 4851-4851, exports `COMPACT_TIER2_ABS`
- order 460: `CONTEXT_COMPACT_INEFFECTIVE_COOLDOWN_SECONDS` (constant), lines 4852-4858, exports `CONTEXT_COMPACT_INEFFECTIVE_COOLDOWN_SECONDS`
- order 461: `FILE_BUFFER_CONTENT_THRESHOLD` (constant), lines 4859-4860, exports `FILE_BUFFER_CONTENT_THRESHOLD`
- order 462: `FILE_BUFFER_MAX_FILES` (constant), lines 4861-4861, exports `FILE_BUFFER_MAX_FILES`
- order 463: `AUTHORITATIVE_USER_GOAL_OPEN` (constant), lines 4862-4862, exports `AUTHORITATIVE_USER_GOAL_OPEN`
- order 464: `AUTHORITATIVE_USER_GOAL_CLOSE` (constant), lines 4863-4863, exports `AUTHORITATIVE_USER_GOAL_CLOSE`
- order 465: `AGENT_MSG_LIMIT_TIER0` (constant), lines 4864-4865, exports `AGENT_MSG_LIMIT_TIER0`
- order 466: `AGENT_MSG_LIMIT_TIER1` (constant), lines 4866-4866, exports `AGENT_MSG_LIMIT_TIER1`
- order 467: `AGENT_MSG_LIMIT_TIER2` (constant), lines 4867-4867, exports `AGENT_MSG_LIMIT_TIER2`
- order 468: `AGENT_MSG_LIMIT_TIER3` (constant), lines 4868-4868, exports `AGENT_MSG_LIMIT_TIER3`
- order 469: `AGENT_CTX_LIMIT_TIER0` (constant), lines 4869-4869, exports `AGENT_CTX_LIMIT_TIER0`
- order 470: `AGENT_CTX_LIMIT_TIER1` (constant), lines 4870-4870, exports `AGENT_CTX_LIMIT_TIER1`
- order 471: `AGENT_CTX_LIMIT_TIER2` (constant), lines 4871-4871, exports `AGENT_CTX_LIMIT_TIER2`
- order 472: `AGENT_CTX_LIMIT_TIER3` (constant), lines 4872-4872, exports `AGENT_CTX_LIMIT_TIER3`
- order 473: `MANAGER_CTX_LIMIT_TIER0` (constant), lines 4873-4873, exports `MANAGER_CTX_LIMIT_TIER0`
- order 474: `MANAGER_CTX_LIMIT_TIER1` (constant), lines 4874-4874, exports `MANAGER_CTX_LIMIT_TIER1`
- order 475: `MANAGER_CTX_LIMIT_TIER2` (constant), lines 4875-4875, exports `MANAGER_CTX_LIMIT_TIER2`
- order 476: `MANAGER_CTX_LIMIT_TIER3` (constant), lines 4876-4876, exports `MANAGER_CTX_LIMIT_TIER3`
- order 477: `MAX_CONTEXT_ARCHIVE_SEGMENTS` (constant), lines 4877-4877, exports `MAX_CONTEXT_ARCHIVE_SEGMENTS`
- order 478: `MAX_USER_BUBBLE_LOG` (constant), lines 4878-4879, exports `MAX_USER_BUBBLE_LOG`
- order 479: `MANAGER_INSTRUCTION_MAX_CHARS` (constant), lines 4880-4884, exports `MANAGER_INSTRUCTION_MAX_CHARS`
- order 480: `MANAGER_MOMENTUM_MAX_SKIPS` (constant), lines 4885-4890, exports `MANAGER_MOMENTUM_MAX_SKIPS`
- order 481: `MODEL_OUTPUT_RETRY_TIMES` (constant), lines 4891-4895, exports `MODEL_OUTPUT_RETRY_TIMES`
- order 482: `ARBITER_TRIGGER_MIN_CONTENT_CHARS` (constant), lines 4896-4896, exports `ARBITER_TRIGGER_MIN_CONTENT_CHARS`
- order 483: `ARBITER_VALID_PLANNING_STREAK_LIMIT` (constant), lines 4897-4897, exports `ARBITER_VALID_PLANNING_STREAK_LIMIT`
- order 484: `ARBITER_DEFAULT_TIMEOUT_SECONDS` (constant), lines 4898-4898, exports `ARBITER_DEFAULT_TIMEOUT_SECONDS`
- order 485: `ARBITER_DEFAULT_MAX_TOKENS` (constant), lines 4899-4899, exports `ARBITER_DEFAULT_MAX_TOKENS`
- order 486: `ARBITER_DEFAULT_TEMPERATURE` (constant), lines 4900-4900, exports `ARBITER_DEFAULT_TEMPERATURE`
- order 487: `LIVE_INPUT_DELAY_WRITE_ROUNDS` (constant), lines 4901-4901, exports `LIVE_INPUT_DELAY_WRITE_ROUNDS`
- order 488: `LIVE_INPUT_DELAY_TOOL_ROUNDS` (constant), lines 4902-4902, exports `LIVE_INPUT_DELAY_TOOL_ROUNDS`
- order 489: `LIVE_INPUT_DELAY_NORMAL_ROUNDS` (constant), lines 4903-4903, exports `LIVE_INPUT_DELAY_NORMAL_ROUNDS`
- order 490: `LIVE_INPUT_MAX_INJECTIONS` (constant), lines 4904-4904, exports `LIVE_INPUT_MAX_INJECTIONS`
- order 491: `LIVE_INPUT_REINJECT_INTERVAL` (constant), lines 4905-4905, exports `LIVE_INPUT_REINJECT_INTERVAL`
- order 492: `LIVE_INPUT_WEIGHT_BASE_DELAYED` (constant), lines 4906-4906, exports `LIVE_INPUT_WEIGHT_BASE_DELAYED`
- order 493: `LIVE_INPUT_WEIGHT_BASE_NORMAL` (constant), lines 4907-4907, exports `LIVE_INPUT_WEIGHT_BASE_NORMAL`
- order 494: `LIVE_INPUT_WEIGHT_STEP_DELAYED` (constant), lines 4908-4908, exports `LIVE_INPUT_WEIGHT_STEP_DELAYED`
- order 495: `LIVE_INPUT_WEIGHT_STEP_NORMAL` (constant), lines 4909-4909, exports `LIVE_INPUT_WEIGHT_STEP_NORMAL`
- order 497: `BENIGN_SOCKET_DEBUG_LOG_ENABLED` (constant), lines 4916-4922, exports `BENIGN_SOCKET_DEBUG_LOG_ENABLED`
- order 498: `BENIGN_SOCKET_LOG_INTERVAL_SECONDS` (constant), lines 4923-4923, exports `BENIGN_SOCKET_LOG_INTERVAL_SECONDS`
- order 499: `FINAL_SUMMARY_MIN_CHARS` (constant), lines 4924-4924, exports `FINAL_SUMMARY_MIN_CHARS`
- order 500: `FINAL_SUMMARY_STRICT_MIN_CHARS` (constant), lines 4925-4925, exports `FINAL_SUMMARY_STRICT_MIN_CHARS`
- order 501: `RUNTIME_CONTROL_HINT_PREFIXES` (constant), lines 4926-4946, exports `RUNTIME_CONTROL_HINT_PREFIXES`
- order 502: `UI_HIDDEN_RUNTIME_CONTROL_PREFIXES` (constant), lines 4947-4975, exports `UI_HIDDEN_RUNTIME_CONTROL_PREFIXES`
- order 503: `UI_PROJECTED_RUNTIME_CONTROL_TAGS` (constant), lines 4976-4998, exports `UI_PROJECTED_RUNTIME_CONTROL_TAGS`
- order 504: `UI_LEGACY_PROJECTED_RUNTIME_CONTROL_TAGS` (constant), lines 4999-5001, exports `UI_LEGACY_PROJECTED_RUNTIME_CONTROL_TAGS`
- order 505: `RETRY_RUNTIME_HINT_PREFIXES` (constant), lines 5002-5016, exports `RETRY_RUNTIME_HINT_PREFIXES`
- order 506: `EXECUTION_MODE_SINGLE` (constant), lines 5017-5017, exports `EXECUTION_MODE_SINGLE`
- order 507: `EXECUTION_MODE_SEQUENTIAL` (constant), lines 5018-5018, exports `EXECUTION_MODE_SEQUENTIAL`
- order 508: `EXECUTION_MODE_SYNC` (constant), lines 5019-5019, exports `EXECUTION_MODE_SYNC`
- order 509: `EXECUTION_MODE_CHOICES` (constant), lines 5020-5024, exports `EXECUTION_MODE_CHOICES`
- order 510: `AGENT_ROLES` (constant), lines 5025-5025, exports `AGENT_ROLES`
- order 511: `AGENT_BUBBLE_ROLES` (constant), lines 5026-5026, exports `AGENT_BUBBLE_ROLES`
- order 512: `AGENT_ROLE_LABELS` (constant), lines 5027-5033, exports `AGENT_ROLE_LABELS`
- order 513: `AGENT_ROLE_BUBBLE_COLORS` (constant), lines 5034-5040, exports `AGENT_ROLE_BUBBLE_COLORS`
- order 514: `BLACKBOARD_STATUSES` (constant), lines 5041-5050, exports `BLACKBOARD_STATUSES`
- order 515: `TASK_COMPLEXITY_LEVELS` (constant), lines 5051-5051, exports `TASK_COMPLEXITY_LEVELS`
- order 516: `TASK_COMPLEXITY_RANKS` (constant), lines 5052-5057, exports `TASK_COMPLEXITY_RANKS`
- order 517: `TASK_PROFILE_TYPES` (constant), lines 5058-5064, exports `TASK_PROFILE_TYPES`
- order 518: `TASK_LEVEL_CHOICES` (constant), lines 5065-5065, exports `TASK_LEVEL_CHOICES`
- order 519: `TASK_SCALE_PREFERENCES` (constant), lines 5066-5066, exports `TASK_SCALE_PREFERENCES`
- order 520: `SEMANTIC_CONFIDENCE_CHOICES` (constant), lines 5067-5067, exports `SEMANTIC_CONFIDENCE_CHOICES`
- order 521: `L2_TODO_POLICY_CHOICES` (constant), lines 5068-5072, exports `L2_TODO_POLICY_CHOICES`
- order 522: `DEFAULT_L2_TODO_POLICY` (constant), lines 5073-5073, exports `DEFAULT_L2_TODO_POLICY`
- order 523: `TASK_LEVEL_POLICIES` (constant), lines 5074-5127, exports `TASK_LEVEL_POLICIES`
- order 524: `MANAGER_ROUTE_TARGETS` (constant), lines 5128-5128, exports `MANAGER_ROUTE_TARGETS`
- order 525: `BLACKBOARD_MAX_LOG_ENTRIES` (constant), lines 5129-5129, exports `BLACKBOARD_MAX_LOG_ENTRIES`
- order 526: `BLACKBOARD_MAX_TEXT` (constant), lines 5130-5130, exports `BLACKBOARD_MAX_TEXT`
- order 527: `BLACKBOARD_MEMORY_SHORT_MAX` (constant), lines 5131-5131, exports `BLACKBOARD_MEMORY_SHORT_MAX`
- order 528: `BLACKBOARD_MEMORY_MID_MAX_STEPS` (constant), lines 5132-5132, exports `BLACKBOARD_MEMORY_MID_MAX_STEPS`
- order 529: `BLACKBOARD_MEMORY_MID_ITEMS_PER_STEP` (constant), lines 5133-5133, exports `BLACKBOARD_MEMORY_MID_ITEMS_PER_STEP`
- order 530: `BLACKBOARD_MEMORY_LONG_MAX` (constant), lines 5134-5134, exports `BLACKBOARD_MEMORY_LONG_MAX`
- order 531: `BLACKBOARD_MEMORY_INDEX_MAX` (constant), lines 5135-5135, exports `BLACKBOARD_MEMORY_INDEX_MAX`
- order 532: `SKILL_REFRESH_MIN_INTERVAL_SECONDS` (constant), lines 5136-5136, exports `SKILL_REFRESH_MIN_INTERVAL_SECONDS`
- order 533: `SKILL_CATALOG_FULL_REFRESH_SECONDS` (constant), lines 5137-5140, exports `SKILL_CATALOG_FULL_REFRESH_SECONDS`
- order 534: `SKILL_PROMPT_MAX_ITEMS` (constant), lines 5141-5141, exports `SKILL_PROMPT_MAX_ITEMS`
- order 535: `SKILL_PROMPT_MAX_CHARS` (constant), lines 5142-5142, exports `SKILL_PROMPT_MAX_CHARS`
- order 536: `SKILL_RUNTIME_CACHE_MAX_ENTRIES` (constant), lines 5143-5143, exports `SKILL_RUNTIME_CACHE_MAX_ENTRIES`
- order 537: `SKILL_RUNTIME_CACHE_MAX_BYTES` (constant), lines 5144-5144, exports `SKILL_RUNTIME_CACHE_MAX_BYTES`
- order 538: `SKILL_AUTOLOAD_SCORE_THRESHOLD` (constant), lines 5145-5148, exports `SKILL_AUTOLOAD_SCORE_THRESHOLD`
- order 539: `SKILL_AUTOLOAD_CONFIDENCE_THRESHOLD` (constant), lines 5149-5149, exports `SKILL_AUTOLOAD_CONFIDENCE_THRESHOLD`
- order 540: `SKILL_RUNTIME_EVALUATION_TTL_SECONDS` (constant), lines 5150-5150, exports `SKILL_RUNTIME_EVALUATION_TTL_SECONDS`
- order 541: `SKILL_RUNTIME_EVALUATION_TIMEOUT_SECONDS` (constant), lines 5151-5151, exports `SKILL_RUNTIME_EVALUATION_TIMEOUT_SECONDS`
- order 542: `SKILL_RUNTIME_UNLOAD_CONFIDENCE_THRESHOLD` (constant), lines 5152-5152, exports `SKILL_RUNTIME_UNLOAD_CONFIDENCE_THRESHOLD`
- order 543: `SKILL_RUNTIME_KEY_TOOL_INTERVAL` (constant), lines 5153-5153, exports `SKILL_RUNTIME_KEY_TOOL_INTERVAL`
- order 544: `SKILL_RUNTIME_EVENTS_MAX` (constant), lines 5154-5154, exports `SKILL_RUNTIME_EVENTS_MAX`
- order 545: `SKILL_METADATA_CAPSULE_MAX_CHARS` (constant), lines 5155-5155, exports `SKILL_METADATA_CAPSULE_MAX_CHARS`
- order 546: `SKILL_DEPENDENCY_MAX_DEPTH` (constant), lines 5156-5156, exports `SKILL_DEPENDENCY_MAX_DEPTH`
- order 547: `AUTO_SKILLS_ROOT_CANDIDATES` (constant), lines 5157-5157, exports `AUTO_SKILLS_ROOT_CANDIDATES`
- order 548: `SKILL_DEFAULT_ATTACHMENT_GLOBS` (constant), lines 5158-5188, exports `SKILL_DEFAULT_ATTACHMENT_GLOBS`
- order 549: `SKILL_INLINE_ATTACHMENT_MAX_FILES` (constant), lines 5189-5189, exports `SKILL_INLINE_ATTACHMENT_MAX_FILES`
- order 550: `SKILL_INLINE_ATTACHMENT_MAX_CHARS` (constant), lines 5190-5190, exports `SKILL_INLINE_ATTACHMENT_MAX_CHARS`
- order 551: `SKILL_RESOURCE_MANIFEST_MAX_ITEMS` (constant), lines 5191-5191, exports `SKILL_RESOURCE_MANIFEST_MAX_ITEMS`
- order 552: `SKILL_BODY_COMPACT_THRESHOLD_CHARS` (constant), lines 5192-5192, exports `SKILL_BODY_COMPACT_THRESHOLD_CHARS`
- order 553: `SKILL_BODY_PREVIEW_CHARS` (constant), lines 5193-5193, exports `SKILL_BODY_PREVIEW_CHARS`
- order 554: `SKILLS_VIRTUAL_PREFIX` (constant), lines 5194-5194, exports `SKILLS_VIRTUAL_PREFIX`
- order 555: `SKILLS_EXTERNAL_MOUNT` (constant), lines 5195-5195, exports `SKILLS_EXTERNAL_MOUNT`
- order 556: `PLAN_MODE_ENABLED_LEVELS` (constant), lines 5196-5196, exports `PLAN_MODE_ENABLED_LEVELS`
- order 557: `PLAN_MODE_FORCED_LEVELS` (constant), lines 5197-5197, exports `PLAN_MODE_FORCED_LEVELS`
- order 558: `PLAN_MODE_USER_CHOICES` (constant), lines 5198-5198, exports `PLAN_MODE_USER_CHOICES`
- order 559: `TASK_PHASES` (constant), lines 5199-5200, exports `TASK_PHASES`
- order 560: `TASK_PHASE_ROUTING` (constant), lines 5201-5208, exports `TASK_PHASE_ROUTING`
- order 561: `COMPLEXITY_KEYWORDS` (constant), lines 5209-5215, exports `COMPLEXITY_KEYWORDS`
- order 562: `USER_COMPLEXITY_SIMPLE_TOKENS` (constant), lines 5216-5220, exports `USER_COMPLEXITY_SIMPLE_TOKENS`
- order 563: `USER_COMPLEXITY_MODERATE_TOKENS` (constant), lines 5221-5225, exports `USER_COMPLEXITY_MODERATE_TOKENS`
- order 564: `USER_COMPLEXITY_COMPLEX_TOKENS` (constant), lines 5226-5230, exports `USER_COMPLEXITY_COMPLEX_TOKENS`
- order 565: `USER_COMPLEXITY_EXPERT_TOKENS` (constant), lines 5231-5235, exports `USER_COMPLEXITY_EXPERT_TOKENS`
- order 566: `PLAN_MODE_EXPLORER_MAX_ROUNDS` (constant), lines 5236-5239, exports `PLAN_MODE_EXPLORER_MAX_ROUNDS`
- order 567: `PLAN_MODE_EXPLORER_PRODUCTIVE_ROUNDS` (constant), lines 5240-5240, exports `PLAN_MODE_EXPLORER_PRODUCTIVE_ROUNDS`
- order 568: `PLAN_MODE_EXPLORER_STALE_ROUNDS` (constant), lines 5241-5241, exports `PLAN_MODE_EXPLORER_STALE_ROUNDS`
- order 569: `PLAN_MODE_SYNTHESIS_MAX_ATTEMPTS` (constant), lines 5242-5242, exports `PLAN_MODE_SYNTHESIS_MAX_ATTEMPTS`
- order 570: `REVIEWER_DEBUG_MODE_MAX_ROUNDS` (constant), lines 5243-5244, exports `REVIEWER_DEBUG_MODE_MAX_ROUNDS`
- order 571: `REVIEWER_DEBUG_TOOL_ALLOWLIST` (constant), lines 5245-5250, exports `REVIEWER_DEBUG_TOOL_ALLOWLIST`
- order 572: `EXPLORER_STALL_THRESHOLD` (constant), lines 5251-5251, exports `EXPLORER_STALL_THRESHOLD`
- order 573: `DEVELOPER_EDIT_STALL_THRESHOLD` (constant), lines 5252-5252, exports `DEVELOPER_EDIT_STALL_THRESHOLD`
- order 574: `ACCEPTANCE_GATE_STALL_THRESHOLD` (constant), lines 5253-5256, exports `ACCEPTANCE_GATE_STALL_THRESHOLD`
- order 575: `ACCEPTANCE_GATE_HARD_CEILING` (constant), lines 5257-5260, exports `ACCEPTANCE_GATE_HARD_CEILING`
- order 576: `ACCEPTANCE_GATE_TOTAL_ROUND_CEILING` (constant), lines 5261-5261, exports `ACCEPTANCE_GATE_TOTAL_ROUND_CEILING`
- order 577: `PLAN_MODE_MANAGER_SYNTHESIS_MAX_TOKENS` (constant), lines 5262-5262, exports `PLAN_MODE_MANAGER_SYNTHESIS_MAX_TOKENS`
- order 578: `PLAN_MODE_MAX_OPTIONS` (constant), lines 5263-5263, exports `PLAN_MODE_MAX_OPTIONS`
- order 579: `PLAN_FILE_RELATIVE_PATH` (constant), lines 5264-5264, exports `PLAN_FILE_RELATIVE_PATH`
- order 580: `PLAN_BUBBLE_MAX_CHARS` (constant), lines 5265-5265, exports `PLAN_BUBBLE_MAX_CHARS`
- order 581: `PLAN_NOTICE_BODY_MAX_CHARS` (constant), lines 5266-5266, exports `PLAN_NOTICE_BODY_MAX_CHARS`
- order 582: `PLAN_MESSAGE_EVENT_MAX_CHARS` (constant), lines 5267-5267, exports `PLAN_MESSAGE_EVENT_MAX_CHARS`
- order 583: `PLAN_STEP_FULL_CONTENT_MAX_CHARS` (constant), lines 5268-5268, exports `PLAN_STEP_FULL_CONTENT_MAX_CHARS`
- order 584: `PLAN_MODE_RESEARCH_TOOL_ALLOWLIST` (constant), lines 5269-5276, exports `PLAN_MODE_RESEARCH_TOOL_ALLOWLIST`
- order 585: `FAILURE_LEDGER_MAX_FIXES` (constant), lines 5277-5277, exports `FAILURE_LEDGER_MAX_FIXES`
- order 586: `FAILURE_LEDGER_MAX_COMPILE_ERRORS` (constant), lines 5278-5278, exports `FAILURE_LEDGER_MAX_COMPILE_ERRORS`
- order 587: `FAILURE_LEDGER_MAX_DELEGATIONS` (constant), lines 5279-5279, exports `FAILURE_LEDGER_MAX_DELEGATIONS`
- order 588: `FAILURE_LEDGER_MAX_STALLS` (constant), lines 5280-5280, exports `FAILURE_LEDGER_MAX_STALLS`
- order 589: `FAILURE_LEDGER_MAX_TOOL_FPS` (constant), lines 5281-5281, exports `FAILURE_LEDGER_MAX_TOOL_FPS`
- order 590: `FAILURE_LEDGER_MAX_ERRORS` (constant), lines 5282-5282, exports `FAILURE_LEDGER_MAX_ERRORS`
- order 591: `ERROR_CATEGORY_DEFS` (constant), lines 5283-5322, exports `ERROR_CATEGORY_DEFS`
- order 592: `CHECKPOINT_MAX_COUNT` (constant), lines 5323-5323, exports `CHECKPOINT_MAX_COUNT`
- order 593: `CHECKPOINT_INTERVAL_ROUNDS` (constant), lines 5324-5324, exports `CHECKPOINT_INTERVAL_ROUNDS`
- order 594: `PERSISTED_ROUTES_MAX` (constant), lines 5325-5325, exports `PERSISTED_ROUTES_MAX`
- order 595: `HTML_FRONTEND_REQUEST_KEYWORDS` (constant), lines 5326-5365, exports `HTML_FRONTEND_REQUEST_KEYWORDS`
- order 596: `DEEP_RESEARCH_REQUEST_KEYWORDS` (constant), lines 5366-5388, exports `DEEP_RESEARCH_REQUEST_KEYWORDS`
- order 597: `DEEP_RESEARCH_RETRIEVAL_KEYWORDS` (constant), lines 5389-5408, exports `DEEP_RESEARCH_RETRIEVAL_KEYWORDS`
- order 598: `DEEP_RESEARCH_TEXT_ONLY_HINT_KEYWORDS` (constant), lines 5409-5426, exports `DEEP_RESEARCH_TEXT_ONLY_HINT_KEYWORDS`
- order 599: `DANGEROUS_PATTERNS` (constant), lines 5427-5428, exports `DANGEROUS_PATTERNS`
- order 600: `VALID_MSG_TYPES` (constant), lines 5429-5435, exports `VALID_MSG_TYPES`
- order 601: `SUPPORTED_UI_LANGUAGES` (constant), lines 5436-5442, exports `SUPPORTED_UI_LANGUAGES`
- order 602: `UI_LANGUAGE_LABELS` (constant), lines 5443-5443, exports `UI_LANGUAGE_LABELS`
- order 603: `DEFAULT_UI_LANGUAGE` (constant), lines 5444-5444, exports `DEFAULT_UI_LANGUAGE`
- order 604: `PUBLIC_TOOL_PROGRESS_SUMMARY_ENABLED` (constant), lines 5445-5447, exports `PUBLIC_TOOL_PROGRESS_SUMMARY_ENABLED`
- order 605: `AGENT_LANGUAGE_PREFERENCES` (constant), lines 5448-5489, exports `AGENT_LANGUAGE_PREFERENCES`
- order 606: `UI_STYLE_CHOICES` (constant), lines 5490-5490, exports `UI_STYLE_CHOICES`
- order 607: `UI_STYLE_LABELS` (constant), lines 5491-5491, exports `UI_STYLE_LABELS`
- order 608: `DEFAULT_UI_STYLE` (constant), lines 5492-5492, exports `DEFAULT_UI_STYLE`
- order 609: `DEFAULT_WEB_UI_DIR` (constant), lines 5493-5493, exports `DEFAULT_WEB_UI_DIR`
- order 610: `DEFAULT_WEB_UI_CONFIG` (constant), lines 5494-5494, exports `DEFAULT_WEB_UI_CONFIG`
- order 611: `WEB_UI_REQUIRED_FILES` (constant), lines 5495-5502, exports `WEB_UI_REQUIRED_FILES`
- order 612: `WEB_UI_OPTIONAL_FILES` (constant), lines 5503-5503, exports `WEB_UI_OPTIONAL_FILES`
- order 613: `WEB_UI_APPLICATION_CONTRACT_VERSION` (constant), lines 5504-5504, exports `WEB_UI_APPLICATION_CONTRACT_VERSION`
- order 614: `WEB_UI_APPLICATION_FEATURE_MARKERS` (constant), lines 5505-5524, exports `WEB_UI_APPLICATION_FEATURE_MARKERS`
- order 615: `IMAGE_EXTS` (constant), lines 5525-5539, exports `IMAGE_EXTS`
- order 616: `IMAGE_FORMATS_NEED_CONVERSION` (constant), lines 5540-5540, exports `IMAGE_FORMATS_NEED_CONVERSION`
- order 617: `IMAGE_SAFE_FORMATS` (constant), lines 5541-5541, exports `IMAGE_SAFE_FORMATS`
- order 618: `AUDIO_EXTS` (constant), lines 5542-5552, exports `AUDIO_EXTS`
- order 619: `VIDEO_EXTS` (constant), lines 5553-5563, exports `VIDEO_EXTS`
- order 620: `CODE_PREVIEW_STAGE_MAX_BYTES` (constant), lines 5564-5564, exports `CODE_PREVIEW_STAGE_MAX_BYTES`
- order 621: `CODE_PREVIEW_STAGE_MAX_ROWS` (constant), lines 5565-5565, exports `CODE_PREVIEW_STAGE_MAX_ROWS`
- order 622: `CODE_PREVIEW_STAGE_MAX_PER_FILE` (constant), lines 5566-5566, exports `CODE_PREVIEW_STAGE_MAX_PER_FILE`
- order 623: `CODE_PREVIEW_STAGE_MAX_TOTAL` (constant), lines 5567-5567, exports `CODE_PREVIEW_STAGE_MAX_TOTAL`
- order 624: `CODE_PREVIEW_DIFF_CONTEXT_LINES` (constant), lines 5568-5568, exports `CODE_PREVIEW_DIFF_CONTEXT_LINES`
- order 625: `CODE_PREVIEW_DIFF_MERGE_GAP` (constant), lines 5569-5569, exports `CODE_PREVIEW_DIFF_MERGE_GAP`
- order 626: `PREVIEW_DOWNLOAD_MAX_FILES` (constant), lines 5570-5570, exports `PREVIEW_DOWNLOAD_MAX_FILES`
- order 627: `PREVIEW_DOWNLOAD_MAX_BYTES` (constant), lines 5571-5571, exports `PREVIEW_DOWNLOAD_MAX_BYTES`
- order 628: `FILES_TREE_DEFAULT_MAX_NODES` (constant), lines 5572-5572, exports `FILES_TREE_DEFAULT_MAX_NODES`
- order 629: `FILES_TREE_DEFAULT_MAX_DEPTH` (constant), lines 5573-5573, exports `FILES_TREE_DEFAULT_MAX_DEPTH`
- order 630: `FILES_TREE_SKIP_DIRS` (constant), lines 5574-5582, exports `FILES_TREE_SKIP_DIRS`
- order 631: `FILES_TREE_SKIP_REL_DIRS` (constant), lines 5583-5585, exports `FILES_TREE_SKIP_REL_DIRS`
- order 632: `IDE_FILE_MAX_BYTES` (constant), lines 5586-5586, exports `IDE_FILE_MAX_BYTES`
- order 633: `IDE_UPLOAD_MAX_BYTES` (constant), lines 5587-5587, exports `IDE_UPLOAD_MAX_BYTES`
- order 634: `IDE_UPLOAD_TOTAL_MAX_BYTES` (constant), lines 5588-5588, exports `IDE_UPLOAD_TOTAL_MAX_BYTES`
- order 635: `IDE_UPLOAD_MAX_ITEMS` (constant), lines 5589-5589, exports `IDE_UPLOAD_MAX_ITEMS`
- order 636: `IDE_UPLOAD_CHUNK_MAX_BYTES` (constant), lines 5590-5590, exports `IDE_UPLOAD_CHUNK_MAX_BYTES`
- order 637: `IDE_UPLOAD_STREAM_MAX_BYTES` (constant), lines 5591-5591, exports `IDE_UPLOAD_STREAM_MAX_BYTES`
- order 638: `IDE_TEXT_PREVIEW_MAX_BYTES` (constant), lines 5592-5592, exports `IDE_TEXT_PREVIEW_MAX_BYTES`
- order 639: `IDE_MARKDOWN_PREVIEW_MAX_LINES` (constant), lines 5593-5593, exports `IDE_MARKDOWN_PREVIEW_MAX_LINES`
- order 640: `IDE_IMAGE_PREVIEW_MAX_EDGE` (constant), lines 5594-5594, exports `IDE_IMAGE_PREVIEW_MAX_EDGE`
- order 641: `IDE_IMAGE_PREVIEW_MAX_PIXELS` (constant), lines 5595-5595, exports `IDE_IMAGE_PREVIEW_MAX_PIXELS`
- order 642: `IDE_IMAGE_PREVIEW_SOURCE_MAX_PIXELS` (constant), lines 5596-5596, exports `IDE_IMAGE_PREVIEW_SOURCE_MAX_PIXELS`
- order 643: `IDE_VECTOR_PREVIEW_MAX_BYTES` (constant), lines 5597-5597, exports `IDE_VECTOR_PREVIEW_MAX_BYTES`
- order 644: `IDE_TABLE_PREVIEW_SOURCE_MAX_BYTES` (constant), lines 5598-5598, exports `IDE_TABLE_PREVIEW_SOURCE_MAX_BYTES`
- order 645: `IDE_TABLE_PREVIEW_CELL_MAX_CHARS` (constant), lines 5599-5599, exports `IDE_TABLE_PREVIEW_CELL_MAX_CHARS`
- order 646: `IDE_TABLE_PREVIEW_TOTAL_CHARS` (constant), lines 5600-5600, exports `IDE_TABLE_PREVIEW_TOTAL_CHARS`
- order 647: `IDE_OFFICE_PREVIEW_MAX_ENTRIES` (constant), lines 5601-5601, exports `IDE_OFFICE_PREVIEW_MAX_ENTRIES`
- order 648: `IDE_OFFICE_PREVIEW_MAX_EXPANDED_BYTES` (constant), lines 5602-5602, exports `IDE_OFFICE_PREVIEW_MAX_EXPANDED_BYTES`
- order 649: `IDE_OFFICE_PREVIEW_MAX_ENTRY_BYTES` (constant), lines 5603-5603, exports `IDE_OFFICE_PREVIEW_MAX_ENTRY_BYTES`
- order 650: `IDE_COMMAND_TIMEOUT_DEFAULT` (constant), lines 5604-5604, exports `IDE_COMMAND_TIMEOUT_DEFAULT`
- order 651: `IDE_TREE_DEFAULT_MAX_NODES` (constant), lines 5605-5605, exports `IDE_TREE_DEFAULT_MAX_NODES`
- order 652: `IDE_TREE_MAX_NODES` (constant), lines 5606-5606, exports `IDE_TREE_MAX_NODES`
- order 653: `IDE_SEARCH_MAX_RESULTS` (constant), lines 5607-5607, exports `IDE_SEARCH_MAX_RESULTS`
- order 654: `IDE_SEARCH_MAX_FILE_BYTES` (constant), lines 5608-5608, exports `IDE_SEARCH_MAX_FILE_BYTES`
- order 655: `IDE_TERMINAL_SCROLLBACK_BYTES` (constant), lines 5609-5609, exports `IDE_TERMINAL_SCROLLBACK_BYTES`
- order 656: `IDE_TERMINAL_IDLE_SECONDS` (constant), lines 5610-5610, exports `IDE_TERMINAL_IDLE_SECONDS`
- order 657: `IDE_DEBUG_ADAPTER_START_ATTEMPTS` (constant), lines 5611-5611, exports `IDE_DEBUG_ADAPTER_START_ATTEMPTS`
- order 658: `IDE_DEBUG_ADAPTER_START_TIMEOUT_SECONDS` (constant), lines 5612-5612, exports `IDE_DEBUG_ADAPTER_START_TIMEOUT_SECONDS`
- order 659: `IDE_VSIX_MAX_BYTES` (constant), lines 5613-5613, exports `IDE_VSIX_MAX_BYTES`
- order 660: `IDE_VSIX_MAX_EXPANDED_BYTES` (constant), lines 5614-5614, exports `IDE_VSIX_MAX_EXPANDED_BYTES`
- order 661: `IDE_VSIX_MAX_FILES` (constant), lines 5615-5615, exports `IDE_VSIX_MAX_FILES`
- order 662: `IDE_VSIX_MAX_FILE_BYTES` (constant), lines 5616-5616, exports `IDE_VSIX_MAX_FILE_BYTES`
- order 663: `IDE_TREE_SKIP_DIRS` (constant), lines 5617-5625, exports `IDE_TREE_SKIP_DIRS`
- order 664: `RENDER_FRAME_MAX_B64_CHARS` (constant), lines 5626-5626, exports `RENDER_FRAME_MAX_B64_CHARS`
- order 665: `RENDER_FRAME_MAX_POINTS` (constant), lines 5627-5627, exports `RENDER_FRAME_MAX_POINTS`
- order 666: `RENDER_FRAME_MAX_LINES` (constant), lines 5628-5628, exports `RENDER_FRAME_MAX_LINES`
- order 667: `RENDER_FRAME_MAX_LINE_POINTS` (constant), lines 5629-5629, exports `RENDER_FRAME_MAX_LINE_POINTS`
- order 668: `RENDER_FRAME_ACTIVITY_INTERVAL_SECONDS` (constant), lines 5630-5630, exports `RENDER_FRAME_ACTIVITY_INTERVAL_SECONDS`
- order 669: `RAW_TOOLCALL_TEXT_FILTER_THRESHOLD` (constant), lines 5631-5631, exports `RAW_TOOLCALL_TEXT_FILTER_THRESHOLD`
- order 670: `ASSISTANT_TEXT_PERSIST_MAX_CHARS` (constant), lines 5632-5632, exports `ASSISTANT_TEXT_PERSIST_MAX_CHARS`
- order 671: `ASSISTANT_MESSAGE_EVENT_MAX_CHARS` (constant), lines 5633-5633, exports `ASSISTANT_MESSAGE_EVENT_MAX_CHARS`
- order 672: `CODE_PREVIEW_EXTS` (constant), lines 5634-5761, exports `CODE_PREVIEW_EXTS`
- order 673: `CODE_PREVIEW_FILENAMES` (constant), lines 5762-5813, exports `CODE_PREVIEW_FILENAMES`
- order 674: `MEDIA_CAPABILITY_KEYS` (constant), lines 5814-5821, exports `MEDIA_CAPABILITY_KEYS`
- order 678: `OFFLINE_JS_LIB_CATALOG` (constant), lines 5854-6180, exports `OFFLINE_JS_LIB_CATALOG`
- order 679: `OFFLINE_JS_ASSET_LOCK` (constant), lines 6181-6181, exports `OFFLINE_JS_ASSET_LOCK`
- order 680: `OFFLINE_JS_LIB_INDEX_FILE` (constant), lines 6182-6182, exports `OFFLINE_JS_LIB_INDEX_FILE`
- order 681: `OFFLINE_JS_LIB_README_FILE` (constant), lines 6183-6183, exports `OFFLINE_JS_LIB_README_FILE`
- order 692: `BACKEND_I18N` (constant), lines 6389-6460, exports `BACKEND_I18N`
- order 693: `_call_backend_i18n_en_update_6462` (expression), lines 6461-6562, exports —
- order 694: `_call_backend_i18n_zh_cn_update_6563` (expression), lines 6563-6663, exports —
- order 695: `_call_backend_i18n_zh_tw_update_6664` (expression), lines 6664-6764, exports —
- order 696: `_call_backend_i18n_ja_update_6765` (expression), lines 6765-6865, exports —
- order 910: `LIQUID_KERNEL_STARTUP_POLICIES` (constant), lines 14038-14040, exports `LIQUID_KERNEL_STARTUP_POLICIES`
- order 911: `LIQUID_KERNEL_BOOTSTRAP_STATE_FILENAME` (constant), lines 14041-14041, exports `LIQUID_KERNEL_BOOTSTRAP_STATE_FILENAME`
- order 941: `TABULAR_PREVIEW_EXTS` (constant), lines 15935-15937, exports `TABULAR_PREVIEW_EXTS`
- order 942: `EXCEL_PREVIEW_EXTS` (constant), lines 15938-15938, exports `EXCEL_PREVIEW_EXTS`
- order 943: `PRESENTATION_PREVIEW_EXTS` (constant), lines 15939-15939, exports `PRESENTATION_PREVIEW_EXTS`
- order 944: `DOCUMENT_PREVIEW_EXTS` (constant), lines 15940-15940, exports `DOCUMENT_PREVIEW_EXTS`
- order 1154: `STUDIO_DEVICE_COOKIE` (constant), lines 115451-115468, exports `STUDIO_DEVICE_COOKIE`
- order 1155: `STUDIO_SESSION_COOKIE` (constant), lines 115469-115469, exports `STUDIO_SESSION_COOKIE`
- order 1156: `STUDIO_DEVICE_TTL` (constant), lines 115470-115470, exports `STUDIO_DEVICE_TTL`
- order 1157: `STUDIO_SESSION_TTL` (constant), lines 115471-115471, exports `STUDIO_SESSION_TTL`
- order 1158: `STUDIO_MAX_FILE_BYTES` (constant), lines 115472-115472, exports `STUDIO_MAX_FILE_BYTES`
- order 1159: `STUDIO_MAX_PROJECT_BYTES` (constant), lines 115473-115473, exports `STUDIO_MAX_PROJECT_BYTES`
- order 1160: `STUDIO_MAX_FILES` (constant), lines 115474-115474, exports `STUDIO_MAX_FILES`
- order 1161: `STUDIO_MAX_JOB_SECONDS` (constant), lines 115475-115475, exports `STUDIO_MAX_JOB_SECONDS`
- order 1167: `STUDIO_INDEX_HTML` (constant), lines 117375-117377, exports `STUDIO_INDEX_HTML`
- order 1168: `STUDIO_CSS` (constant), lines 117378-117378, exports `STUDIO_CSS`
- order 1169: `STUDIO_JS` (constant), lines 117379-117379, exports `STUDIO_JS`

### `config/paths.py`

- order 122: `SCRIPT_DIR` (constant), lines 3786-3786, exports `SCRIPT_DIR`
- order 147: `_resolve_default_agent_workdir` (function), lines 3880-3889, exports `_resolve_default_agent_workdir`
- order 148: `_is_installed_python_runtime` (function), lines 3890-3893, exports `_is_installed_python_runtime`
- order 149: `_runtime_storage_mode` (function), lines 3894-3900, exports `_runtime_storage_mode`
- order 150: `_runtime_tree_has_content` (function), lines 3901-3906, exports `_runtime_tree_has_content`
- order 151: `_copy_runtime_tree_with_crypto_migration` (function), lines 3907-3977, exports `_copy_runtime_tree_with_crypto_migration`
- order 152: `_merge_legacy_codes_root` (function), lines 3978-4043, exports `_merge_legacy_codes_root`
- order 153: `_migrate_legacy_runtime_roots` (function), lines 4044-4134, exports `_migrate_legacy_runtime_roots`
- order 154: `WORKDIR` (constant), lines 4135-4136, exports `WORKDIR`
- order 155: `CODES_ROOT` (constant), lines 4137-4137, exports `CODES_ROOT`
- order 156: `LLM_CONFIG_PATH` (constant), lines 4138-4138, exports `LLM_CONFIG_PATH`
- order 774: `detect_repo_root` (function), lines 8310-8324, exports `detect_repo_root`
- order 775: `REPO_ROOT` (constant), lines 8325-8326, exports `REPO_ROOT`

### `config/settings.py`

- order 685: `normalize_ui_language` (function), lines 6265-6289, exports `normalize_ui_language`
- order 686: `normalize_ui_style` (function), lines 6290-6309, exports `normalize_ui_style`
- order 687: `supported_ui_languages_payload` (function), lines 6310-6313, exports `supported_ui_languages_payload`
- order 689: `agent_language_preference_payload` (function), lines 6326-6335, exports `agent_language_preference_payload`
- order 690: `normalize_execution_mode` (function), lines 6336-6357, exports `normalize_execution_mode`
- order 691: `model_language_instruction` (function), lines 6358-6388, exports `model_language_instruction`
- order 697: `backend_i18n_text` (function), lines 6866-6878, exports `backend_i18n_text`
- order 698: `backend_role_label` (function), lines 6879-6885, exports `backend_role_label`
- order 699: `_detect_os_shell_instruction` (function), lines 6886-6927, exports `_detect_os_shell_instruction`
- order 700: `resolve_web_ui_dir_path` (function), lines 6928-6936, exports `resolve_web_ui_dir_path`
- order 701: `resolve_optional_file_path` (function), lines 6937-6946, exports `resolve_optional_file_path`
- order 702: `resolve_skills_root_path` (function), lines 6947-6956, exports `resolve_skills_root_path`
- order 703: `_count_skill_markdown_files` (function), lines 6957-6970, exports `_count_skill_markdown_files`
- order 704: `select_preferred_skills_root` (function), lines 6971-7007, exports `select_preferred_skills_root`
- order 705: `load_web_ui_config_file` (function), lines 7008-7024, exports `load_web_ui_config_file`
- order 706: `extract_show_upload_list_setting` (function), lines 7025-7041, exports `extract_show_upload_list_setting`
- order 707: `extract_ui_style_setting` (function), lines 7042-7058, exports `extract_ui_style_setting`
- order 708: `extract_js_lib_download_setting` (function), lines 7059-7080, exports `extract_js_lib_download_setting`
- order 709: `extract_daily_session_limit_setting` (function), lines 7081-7126, exports `extract_daily_session_limit_setting`
- order 710: `extract_shell_command_timeout_setting` (function), lines 7127-7175, exports `extract_shell_command_timeout_setting`
- order 711: `normalize_shell_timeout_mode` (function), lines 7176-7193, exports `normalize_shell_timeout_mode`
- order 712: `extract_shell_timeout_mode_setting` (function), lines 7194-7206, exports `extract_shell_timeout_mode_setting`
- order 713: `extract_shell_async_handoff_setting` (function), lines 7207-7234, exports `extract_shell_async_handoff_setting`
- order 714: `extract_context_token_limit_setting` (function), lines 7235-7269, exports `extract_context_token_limit_setting`
- order 715: `normalize_auto_task_level_ceiling` (function), lines 7270-7291, exports `normalize_auto_task_level_ceiling`
- order 716: `normalize_l2_todo_policy` (function), lines 7292-7327, exports `normalize_l2_todo_policy`
- order 717: `extract_l2_todo_policy_setting` (function), lines 7328-7370, exports `extract_l2_todo_policy_setting`
- order 718: `extract_auto_task_level_ceiling_setting` (function), lines 7371-7400, exports `extract_auto_task_level_ceiling_setting`
- order 719: `normalize_read_context_policy` (function), lines 7401-7421, exports `normalize_read_context_policy`
- order 720: `normalize_tool_memory_policy` (function), lines 7422-7425, exports `normalize_tool_memory_policy`
- order 721: `extract_read_context_policy_setting` (function), lines 7426-7449, exports `extract_read_context_policy_setting`
- order 722: `extract_tool_memory_policy_setting` (function), lines 7450-7473, exports `extract_tool_memory_policy_setting`
- order 724: `default_multimodal_capabilities` (function), lines 7480-7490, exports `default_multimodal_capabilities`
- order 725: `_to_bool_like` (function), lines 7491-7503, exports `_to_bool_like`
- order 726: `extract_web_search_enabled_setting` (function), lines 7504-7516, exports `extract_web_search_enabled_setting`
- order 727: `_single_no_plan_todo_setting_sections` (function), lines 7517-7543, exports `_single_no_plan_todo_setting_sections`
- order 728: `_single_no_plan_todo_setting_present` (function), lines 7544-7569, exports `_single_no_plan_todo_setting_present`
- order 729: `extract_single_no_plan_todo_settings` (function), lines 7570-7616, exports `extract_single_no_plan_todo_settings`
- order 730: `normalize_user_memory_mode` (function), lines 7617-7647, exports `normalize_user_memory_mode`
- order 731: `user_memory_enabled_from_mode` (function), lines 7648-7651, exports `user_memory_enabled_from_mode`
- order 732: `extract_user_memory_mode_setting` (function), lines 7652-7691, exports `extract_user_memory_mode_setting`
- order 733: `set_web_search_enabled_on_runtime` (function), lines 7692-7707, exports `set_web_search_enabled_on_runtime`
- order 734: `infer_model_multimodal_capabilities` (function), lines 7708-7754, exports `infer_model_multimodal_capabilities`
- order 735: `parse_capability_overrides` (function), lines 7755-7794, exports `parse_capability_overrides`
- order 736: `merge_multimodal_capabilities` (function), lines 7795-7804, exports `merge_multimodal_capabilities`
- order 737: `parse_media_endpoints` (function), lines 7805-7821, exports `parse_media_endpoints`
- order 753: `extract_runtime_region_hint_setting` (function), lines 7999-8024, exports `extract_runtime_region_hint_setting`
- order 754: `extract_runtime_timezone_hint_setting` (function), lines 8025-8042, exports `extract_runtime_timezone_hint_setting`
- order 755: `runtime_environment_context_snapshot` (function), lines 8043-8092, exports `runtime_environment_context_snapshot`
- order 756: `runtime_environment_context_block` (function), lines 8093-8122, exports `runtime_environment_context_block`
- order 792: `load_offline_js_lib_index` (function), lines 8597-8607, exports `load_offline_js_lib_index`
- order 853: `resolve_ollama_model` (function), lines 12172-12183, exports `resolve_ollama_model`
- order 854: `infer_thinking_model` (function), lines 12184-12187, exports `infer_thinking_model`
- order 865: `extract_base_url` (function), lines 12397-12406, exports `extract_base_url`
- order 867: `infer_user_complexity_value` (function), lines 12418-12435, exports `infer_user_complexity_value`
- order 868: `normalize_task_complexity` (function), lines 12436-12465, exports `normalize_task_complexity`
- order 869: `task_complexity_rank` (function), lines 12466-12468, exports `task_complexity_rank`
- order 870: `task_complexity_at_least` (function), lines 12469-12471, exports `task_complexity_at_least`
- order 871: `max_task_complexity` (function), lines 12472-12482, exports `max_task_complexity`
- order 872: `normalize_openai_compat_provider_name` (function), lines 12483-12499, exports `normalize_openai_compat_provider_name`
- order 892: `resolve_reasoning_payload` (function), lines 12621-12671, exports `resolve_reasoning_payload`
- order 895: `extract_openai_compat_model_ids` (function), lines 12719-12753, exports `extract_openai_compat_model_ids`
- order 898: `load_llm_config_from_source` (function), lines 12787-12822, exports `load_llm_config_from_source`
- order 899: `parse_llm_config_profiles` (function), lines 12823-13453, exports `parse_llm_config_profiles`
- order 900: `looks_like_llm_config` (function), lines 13454-13531, exports `looks_like_llm_config`
- order 904: `parse_front_matter` (function), lines 13727-13955, exports `parse_front_matter`
- order 912: `normalize_liquid_kernel_startup_policy` (function), lines 14042-14046, exports `normalize_liquid_kernel_startup_policy`
- order 939: `normalize_upload_rel_path` (function), lines 15889-15923, exports `normalize_upload_rel_path`

### `ide/assets.py`

- order 1146: `IDE_INDEX_HTML` (constant), lines 114322-114477, exports `IDE_INDEX_HTML`
- order 1147: `IDE_CSS` (constant), lines 114478-114519, exports `IDE_CSS`
- order 1148: `IDE_JS` (constant), lines 114520-114713, exports `IDE_JS`
- order 1149: `IDE_CSS` (constant), lines 114714-114734, exports `IDE_CSS`
- order 1150: `IDE_JS` (constant), lines 114735-114998, exports `IDE_JS`
- order 1151: `IDE_JS` (constant), lines 114999-115127, exports `IDE_JS`
- order 1152: `IDE_JS` (constant), lines 115128-115351, exports `IDE_JS`
- order 1153: `IDE_JS` (constant), lines 115352-115450, exports `IDE_JS`

### `ide/auth.py`

- order 918: `IDEAuthError` (class), lines 14381-14388, exports `IDEAuthError`
- order 919: `IDEAuthStore` (class), lines 14389-15110, exports `IDEAuthStore`

### `ide/errors.py`

- order 920: `IDECapabilityError` (class), lines 15111-15117, exports `IDECapabilityError`
- order 921: `IDEFileConflict` (class), lines 15118-15125, exports `IDEFileConflict`

### `ide/events.py`

- order 809: `ide_public_operation_data` (function), lines 9209-9260, exports `ide_public_operation_data`

### `ide/handler.py`

- order 1183: `IdeHandler` (class), lines 132410-134065, exports `IdeHandler`

### `ide/preview.py`

- order 938: `normalize_rel_preview_path` (function), lines 15875-15888, exports `normalize_rel_preview_path`
- order 940: `is_code_preview_candidate` (function), lines 15924-15934, exports `is_code_preview_candidate`
- order 945: `preview_kind_for_path` (function), lines 15941-15970, exports `preview_kind_for_path`
- order 946: `normalize_markdown_preview_text` (function), lines 15971-16004, exports `normalize_markdown_preview_text`
- order 947: `_preview_markdown_value_html` (function), lines 16005-16025, exports `_preview_markdown_value_html`
- order 948: `_preview_markdown_frontmatter_html` (function), lines 16026-16041, exports `_preview_markdown_frontmatter_html`
- order 949: `_preview_markdown_task_lists` (function), lines 16042-16055, exports `_preview_markdown_task_lists`
- order 950: `_preview_markdown_fallback_inline` (function), lines 16056-16097, exports `_preview_markdown_fallback_inline`
- order 951: `_preview_markdown_fallback_html` (function), lines 16098-16194, exports `_preview_markdown_fallback_html`
- order 954: `workspace_file_revision_map` (function), lines 16235-16259, exports `workspace_file_revision_map`
- order 955: `workspace_revision_delta` (function), lines 16260-16266, exports `workspace_revision_delta`
- order 956: `build_code_preview_rows` (function), lines 16267-16315, exports `build_code_preview_rows`

### `ide/sandbox.py`

- order 761: `_windows_subprocess_encodings` (function), lines 8148-8165, exports `_windows_subprocess_encodings`
- order 1039: `_IDE_SANDBOX_BACKEND_CACHE` (assignment), lines 28575-28583, exports `_IDE_SANDBOX_BACKEND_CACHE`
- order 1040: `_IDE_SANDBOX_BACKEND_LOCK` (assignment), lines 28584-28584, exports `_IDE_SANDBOX_BACKEND_LOCK`
- order 1041: `WINDOWS_JOB_SANDBOX_MARKER` (constant), lines 28585-28585, exports `WINDOWS_JOB_SANDBOX_MARKER`
- order 1042: `_WINDOWS_LOW_INTEGRITY_ROOTS` (assignment), lines 28586-28586, exports `_WINDOWS_LOW_INTEGRITY_ROOTS`
- order 1043: `_WINDOWS_LOW_INTEGRITY_FAILED_ROOTS` (assignment), lines 28587-28587, exports `_WINDOWS_LOW_INTEGRITY_FAILED_ROOTS`
- order 1044: `_WINDOWS_LOW_INTEGRITY_LOCK` (assignment), lines 28588-28588, exports `_WINDOWS_LOW_INTEGRITY_LOCK`
- order 1045: `_is_windows_job_sandbox_prefix` (function), lines 28589-28595, exports `_is_windows_job_sandbox_prefix`
- order 1046: `_windows_builtin_sandbox_probe` (function), lines 28596-28619, exports `_windows_builtin_sandbox_probe`
- order 1047: `_windows_last_error` (function), lines 28620-28627, exports `_windows_last_error`
- order 1048: `_windows_set_integrity_label` (function), lines 28628-28681, exports `_windows_set_integrity_label`
- order 1049: `_windows_set_low_integrity_label` (function), lines 28682-28684, exports `_windows_set_low_integrity_label`
- order 1050: `_windows_protect_application_snapshot` (function), lines 28685-28708, exports `_windows_protect_application_snapshot`
- order 1051: `_windows_prepare_low_integrity_workspace` (function), lines 28709-28746, exports `_windows_prepare_low_integrity_workspace`
- order 1052: `_windows_job_memory_limit` (function), lines 28747-28754, exports `_windows_job_memory_limit`
- order 1053: `_windows_lower_process_integrity` (function), lines 28755-28802, exports `_windows_lower_process_integrity`
- order 1054: `_windows_attach_sandbox_job` (function), lines 28803-28895, exports `_windows_attach_sandbox_job`
- order 1055: `_windows_close_sandbox_job` (function), lines 28896-28912, exports `_windows_close_sandbox_job`
- order 1056: `_popen_windows_sandboxed` (function), lines 28913-28944, exports `_popen_windows_sandboxed`
- order 1057: `_run_windows_sandboxed_command` (function), lines 28945-28998, exports `_run_windows_sandboxed_command`
- order 1058: `_detect_ide_sandbox_backend` (function), lines 28999-29103, exports `_detect_ide_sandbox_backend`

### `llm/client.py`

- order 1024: `OllamaError` (class), lines 25323-25345, exports `OllamaError`
- order 1025: `OllamaClient` (class), lines 25346-27848, exports `OllamaClient`

### `llm/constants.py`

- order 120: `DEFAULT_OLLAMA_BASE_URL` (constant), lines 3784-3784, exports `DEFAULT_OLLAMA_BASE_URL`
- order 121: `DEFAULT_OLLAMA_MODEL` (constant), lines 3785-3785, exports `DEFAULT_OLLAMA_MODEL`
- order 873: `OPENAI_COMPAT_PROVIDER_NAMES` (constant), lines 12500-12509, exports `OPENAI_COMPAT_PROVIDER_NAMES`
- order 874: `OPENAI_LIKE_PROVIDER_NAMES` (constant), lines 12510-12511, exports `OPENAI_LIKE_PROVIDER_NAMES`
- order 877: `EFFORT_OFF` (constant), lines 12518-12529, exports `EFFORT_OFF`
- order 878: `EFFORT_LOW` (constant), lines 12530-12530, exports `EFFORT_LOW`
- order 879: `EFFORT_MEDIUM` (constant), lines 12531-12531, exports `EFFORT_MEDIUM`
- order 880: `EFFORT_HIGH` (constant), lines 12532-12532, exports `EFFORT_HIGH`
- order 881: `EFFORT_MAX` (constant), lines 12533-12533, exports `EFFORT_MAX`
- order 882: `EFFORT_LEVELS` (constant), lines 12534-12534, exports `EFFORT_LEVELS`
- order 883: `EFFORT_ORDER` (constant), lines 12535-12535, exports `EFFORT_ORDER`
- order 884: `EFFORT_DEFAULT` (constant), lines 12536-12536, exports `EFFORT_DEFAULT`
- order 885: `EFFORT_ANTHROPIC_BUDGET` (constant), lines 12537-12544, exports `EFFORT_ANTHROPIC_BUDGET`
- order 886: `EFFORT_OPENAI_REASONING` (constant), lines 12545-12551, exports `EFFORT_OPENAI_REASONING`
- order 887: `TASK_LEVEL_EFFORT` (constant), lines 12552-12561, exports `TASK_LEVEL_EFFORT`
- order 888: `ROLE_EFFORT_FLOOR` (constant), lines 12562-12567, exports `ROLE_EFFORT_FLOOR`
- order 889: `COORDINATION_EFFORT` (constant), lines 12568-12571, exports `COORDINATION_EFFORT`

### `llm/utils.py`

- order 846: `probe_ollama_environment` (function), lines 12103-12117, exports `probe_ollama_environment`
- order 847: `list_ollama_models` (function), lines 12118-12121, exports `list_ollama_models`
- order 848: `_OLLAMA_TAG_CACHE_LOCK` (assignment), lines 12122-12123, exports `_OLLAMA_TAG_CACHE_LOCK`
- order 849: `_OLLAMA_TAG_CACHE` (assignment), lines 12124-12124, exports `_OLLAMA_TAG_CACHE`
- order 852: `list_ollama_models_cached` (function), lines 12133-12171, exports `list_ollama_models_cached`
- order 855: `split_thinking_content` (function), lines 12188-12232, exports `split_thinking_content`
- order 856: `strip_thinking_content` (function), lines 12233-12235, exports `strip_thinking_content`
- order 857: `check_ollama_model_ready` (function), lines 12236-12261, exports `check_ollama_model_ready`
- order 858: `list_loaded_ollama_models` (function), lines 12262-12276, exports `list_loaded_ollama_models`
- order 859: `wake_ollama_model` (function), lines 12277-12308, exports `wake_ollama_model`
- order 860: `try_pull_ollama_model` (function), lines 12309-12327, exports `try_pull_ollama_model`
- order 861: `ordered_model_candidates` (function), lines 12328-12347, exports `ordered_model_candidates`
- order 862: `pick_working_ollama_model` (function), lines 12348-12365, exports `pick_working_ollama_model`
- order 866: `complete_chat_endpoint` (function), lines 12407-12417, exports `complete_chat_endpoint`
- order 875: `is_openai_compat_provider` (function), lines 12512-12514, exports `is_openai_compat_provider`
- order 876: `is_openai_like_provider` (function), lines 12515-12517, exports `is_openai_like_provider`
- order 890: `clamp_effort` (function), lines 12572-12583, exports `clamp_effort`
- order 891: `model_reasoning_style` (function), lines 12584-12620, exports `model_reasoning_style`
- order 893: `openai_compat_probe_headers` (function), lines 12672-12684, exports `openai_compat_probe_headers`
- order 894: `openai_compat_model_list_urls` (function), lines 12685-12718, exports `openai_compat_model_list_urls`
- order 896: `_is_http_url` (function), lines 12754-12768, exports `_is_http_url`
- order 897: `_resolve_local_path` (function), lines 12769-12786, exports `_resolve_local_path`

### `mcp/constants.py`

- order 174: `MCP_SERVICE_PORT_OFFSET` (constant), lines 4156-4156, exports `MCP_SERVICE_PORT_OFFSET`
- order 1004: `MCP_PROTOCOL_VERSION` (constant), lines 23941-23970, exports `MCP_PROTOCOL_VERSION`
- order 1005: `MCP_NAME_RE` (constant), lines 23971-23971, exports `MCP_NAME_RE`
- order 1006: `MCP_TOOL_PREFIX` (constant), lines 23972-23972, exports `MCP_TOOL_PREFIX`
- order 1007: `_MCP_DEFAULT_HANDSHAKE_TIMEOUT` (assignment), lines 23973-23973, exports `_MCP_DEFAULT_HANDSHAKE_TIMEOUT`
- order 1008: `_MCP_DEFAULT_CALL_TIMEOUT` (assignment), lines 23974-23974, exports `_MCP_DEFAULT_CALL_TIMEOUT`
- order 1009: `_MCP_MAX_RESULT_CHARS` (assignment), lines 23975-23975, exports `_MCP_MAX_RESULT_CHARS`
- order 1010: `_MCP_TRUST_STORE_VERSION` (assignment), lines 23976-23976, exports `_MCP_TRUST_STORE_VERSION`

### `mcp/driver.py`

- order 1011: `mcp_normalize_name` (function), lines 23977-23986, exports `mcp_normalize_name`
- order 1012: `mcp_normalize_server_configs` (function), lines 23987-24071, exports `mcp_normalize_server_configs`
- order 1013: `mcp_extract_server_configs` (function), lines 24072-24091, exports `mcp_extract_server_configs`
- order 1014: `_mcp_sha256_file` (function), lines 24092-24102, exports `_mcp_sha256_file`
- order 1015: `_mcp_file_identity` (function), lines 24103-24120, exports `_mcp_file_identity`
- order 1016: `mcp_workspace_identity` (function), lines 24121-24139, exports `mcp_workspace_identity`
- order 1017: `mcp_config_file_digest` (function), lines 24140-24147, exports `mcp_config_file_digest`
- order 1018: `mcp_default_trust_store_path` (function), lines 24148-24182, exports `mcp_default_trust_store_path`
- order 1019: `mcp_record_definition_fingerprint` (function), lines 24183-24197, exports `mcp_record_definition_fingerprint`
- order 1020: `_mcp_effective_spawn` (function), lines 24198-24285, exports `_mcp_effective_spawn`
- order 1021: `MCPWorkspaceTrustStore` (class), lines 24286-24347, exports `MCPWorkspaceTrustStore`
- order 1022: `MCPServerProcess` (class), lines 24348-24703, exports `MCPServerProcess`
- order 1023: `MCPManager` (class), lines 24704-25322, exports `MCPManager`

### `mcp/service.py`

- order 1185: `McpServiceHandler` (class), lines 134537-134754, exports `McpServiceHandler`

### `rag/assets.py`

- order 1140: `RAG_ADMIN_INDEX_HTML` (constant), lines 111715-111947, exports `RAG_ADMIN_INDEX_HTML`
- order 1141: `RAG_ADMIN_CSS` (constant), lines 111948-112051, exports `RAG_ADMIN_CSS`
- order 1142: `RAG_ADMIN_JS` (constant), lines 112052-114272, exports `RAG_ADMIN_JS`
- order 1143: `CODE_ADMIN_INDEX_HTML` (constant), lines 114273-114285, exports `CODE_ADMIN_INDEX_HTML`
- order 1144: `CODE_ADMIN_CSS` (constant), lines 114286-114316, exports `CODE_ADMIN_CSS`
- order 1145: `CODE_ADMIN_JS` (constant), lines 114317-114321, exports `CODE_ADMIN_JS`

### `rag/constants.py`

- order 170: `RAG_LIBRARY_DIRNAME` (constant), lines 4152-4152, exports `RAG_LIBRARY_DIRNAME`
- order 171: `RAG_ADMIN_PORT_OFFSET` (constant), lines 4153-4153, exports `RAG_ADMIN_PORT_OFFSET`
- order 172: `CODE_LIBRARY_DIRNAME` (constant), lines 4154-4154, exports `CODE_LIBRARY_DIRNAME`
- order 178: `WEB_SEARCH_INDEX_DIRNAME` (constant), lines 4163-4163, exports `WEB_SEARCH_INDEX_DIRNAME`
- order 180: `USER_MEMORY_DIRNAME` (constant), lines 4165-4165, exports `USER_MEMORY_DIRNAME`
- order 181: `USER_MEMORY_DB_FILENAME` (constant), lines 4166-4166, exports `USER_MEMORY_DB_FILENAME`
- order 182: `USER_MEMORY_PROFILE_FILENAME` (constant), lines 4167-4167, exports `USER_MEMORY_PROFILE_FILENAME`
- order 183: `USER_MEMORY_MODE_CHOICES` (constant), lines 4168-4168, exports `USER_MEMORY_MODE_CHOICES`
- order 185: `USER_MEMORY_WEAK_CAPSULE_CHARS` (constant), lines 4170-4170, exports `USER_MEMORY_WEAK_CAPSULE_CHARS`
- order 186: `USER_MEMORY_ON_CAPSULE_CHARS` (constant), lines 4171-4171, exports `USER_MEMORY_ON_CAPSULE_CHARS`
- order 187: `USER_MEMORY_CAPSULE_INJECT_CHARS` (constant), lines 4172-4175, exports `USER_MEMORY_CAPSULE_INJECT_CHARS`
- order 188: `USER_MEMORY_MAX_SUMMARY_CHARS` (constant), lines 4176-4176, exports `USER_MEMORY_MAX_SUMMARY_CHARS`
- order 189: `USER_MEMORY_QUERY_LIMIT` (constant), lines 4177-4177, exports `USER_MEMORY_QUERY_LIMIT`
- order 190: `USER_MEMORY_DECAY_HALFLIFE_DAYS` (constant), lines 4178-4178, exports `USER_MEMORY_DECAY_HALFLIFE_DAYS`
- order 191: `USER_MEMORY_PROFILE_SCHEMA_VERSION` (constant), lines 4179-4179, exports `USER_MEMORY_PROFILE_SCHEMA_VERSION`
- order 211: `WEB_SEARCH_CONTEXT_REGISTRY_MAX` (constant), lines 4201-4201, exports `WEB_SEARCH_CONTEXT_REGISTRY_MAX`
- order 212: `WEB_SEARCH_CONTEXT_PROMPT_MAX_ITEMS` (constant), lines 4202-4202, exports `WEB_SEARCH_CONTEXT_PROMPT_MAX_ITEMS`
- order 213: `WEB_SEARCH_CONTEXT_PROMPT_MAX_CHARS` (constant), lines 4203-4203, exports `WEB_SEARCH_CONTEXT_PROMPT_MAX_CHARS`
- order 214: `WEB_SEARCH_CONTEXT_NODE_MAX` (constant), lines 4204-4204, exports `WEB_SEARCH_CONTEXT_NODE_MAX`
- order 215: `WEB_SEARCH_CONTEXT_URL_MAX` (constant), lines 4205-4205, exports `WEB_SEARCH_CONTEXT_URL_MAX`
- order 216: `RAG_CHUNK_CHARS` (constant), lines 4206-4206, exports `RAG_CHUNK_CHARS`
- order 217: `RAG_CHUNK_OVERLAP` (constant), lines 4207-4207, exports `RAG_CHUNK_OVERLAP`
- order 218: `RAG_MAX_CHUNKS_PER_DOC` (constant), lines 4208-4210, exports `RAG_MAX_CHUNKS_PER_DOC`
- order 219: `RAG_MAX_DOCUMENT_CHARS` (constant), lines 4211-4221, exports `RAG_MAX_DOCUMENT_CHARS`
- order 224: `RAG_MAX_QUERY_RESULTS` (constant), lines 4235-4235, exports `RAG_MAX_QUERY_RESULTS`
- order 225: `RAG_HIGH_RECALL_POOL_MULTIPLIER` (constant), lines 4236-4236, exports `RAG_HIGH_RECALL_POOL_MULTIPLIER`
- order 226: `RAG_HIGH_RECALL_MIN_POOL` (constant), lines 4237-4237, exports `RAG_HIGH_RECALL_MIN_POOL`
- order 227: `RAG_RETRIEVAL_MAX_PER_DOC` (constant), lines 4238-4238, exports `RAG_RETRIEVAL_MAX_PER_DOC`
- order 228: `RAG_BM25_K1` (constant), lines 4239-4242, exports `RAG_BM25_K1`
- order 229: `RAG_BM25_B` (constant), lines 4243-4243, exports `RAG_BM25_B`
- order 230: `RAG_BM25_SATURATION` (constant), lines 4244-4250, exports `RAG_BM25_SATURATION`
- order 231: `RAG_SYMBOL_EXACT_BOOST` (constant), lines 4251-4254, exports `RAG_SYMBOL_EXACT_BOOST`
- order 232: `RAG_INDEX_SNAPSHOT_FORMAT` (constant), lines 4255-4258, exports `RAG_INDEX_SNAPSHOT_FORMAT`
- order 233: `RAG_GRAPH_MAX_NODES` (constant), lines 4259-4259, exports `RAG_GRAPH_MAX_NODES`
- order 234: `RAG_TASK_HISTORY_LIMIT` (constant), lines 4260-4260, exports `RAG_TASK_HISTORY_LIMIT`
- order 235: `RAG_MODEL_MEDIA_MAX_BYTES` (constant), lines 4261-4261, exports `RAG_MODEL_MEDIA_MAX_BYTES`
- order 236: `RAG_MAX_IMPORT_FILES` (constant), lines 4262-4262, exports `RAG_MAX_IMPORT_FILES`
- order 237: `RAG_MAX_IMPORT_BATCH_ITEMS` (constant), lines 4263-4263, exports `RAG_MAX_IMPORT_BATCH_ITEMS`
- order 238: `RAG_MAX_IMPORT_BATCH_BYTES` (constant), lines 4264-4264, exports `RAG_MAX_IMPORT_BATCH_BYTES`
- order 239: `RAG_PDF_IMAGE_LIMIT` (constant), lines 4265-4265, exports `RAG_PDF_IMAGE_LIMIT`
- order 240: `RAG_QUERY_CONTEXT_CHARS` (constant), lines 4266-4266, exports `RAG_QUERY_CONTEXT_CHARS`
- order 241: `RAG_MAX_GLOBAL_COMMUNITIES` (constant), lines 4267-4267, exports `RAG_MAX_GLOBAL_COMMUNITIES`
- order 242: `RAG_MAX_COMMUNITY_MAP_SUPPORT` (constant), lines 4268-4268, exports `RAG_MAX_COMMUNITY_MAP_SUPPORT`
- order 243: `RAG_INCLUDE_FILENAME_ENTITIES_DEFAULT` (constant), lines 4269-4269, exports `RAG_INCLUDE_FILENAME_ENTITIES_DEFAULT`
- order 244: `RAG_DYNAMIC_NOISE_MIN_DOC_FREQ` (constant), lines 4270-4270, exports `RAG_DYNAMIC_NOISE_MIN_DOC_FREQ`
- order 245: `RAG_DYNAMIC_NOISE_MIN_COMMUNITY_FREQ` (constant), lines 4271-4271, exports `RAG_DYNAMIC_NOISE_MIN_COMMUNITY_FREQ`
- order 246: `RAG_DYNAMIC_NOISE_SOFT_DOC_RATIO` (constant), lines 4272-4272, exports `RAG_DYNAMIC_NOISE_SOFT_DOC_RATIO`
- order 247: `RAG_DYNAMIC_NOISE_HARD_DOC_RATIO` (constant), lines 4273-4273, exports `RAG_DYNAMIC_NOISE_HARD_DOC_RATIO`
- order 248: `RAG_DYNAMIC_NOISE_SOFT_COMMUNITY_RATIO` (constant), lines 4274-4274, exports `RAG_DYNAMIC_NOISE_SOFT_COMMUNITY_RATIO`
- order 249: `RAG_DYNAMIC_NOISE_HARD_COMMUNITY_RATIO` (constant), lines 4275-4275, exports `RAG_DYNAMIC_NOISE_HARD_COMMUNITY_RATIO`
- order 250: `RAG_MIN_SYNTHESIS_SCORE` (constant), lines 4276-4276, exports `RAG_MIN_SYNTHESIS_SCORE`
- order 251: `RAG_NO_EVIDENCE_THRESHOLD` (constant), lines 4277-4277, exports `RAG_NO_EVIDENCE_THRESHOLD`
- order 252: `RAG_WEAK_MATCH_SCORE_CAP` (constant), lines 4278-4278, exports `RAG_WEAK_MATCH_SCORE_CAP`
- order 253: `RAG_SYNTHESIS_MAX_PER_DOC` (constant), lines 4279-4279, exports `RAG_SYNTHESIS_MAX_PER_DOC`
- order 254: `RAG_WORKFLOW_ACCEPT_SCORE` (constant), lines 4280-4280, exports `RAG_WORKFLOW_ACCEPT_SCORE`
- order 255: `RAG_NO_EVIDENCE_MESSAGE` (constant), lines 4281-4281, exports `RAG_NO_EVIDENCE_MESSAGE`
- order 256: `RAG_CONTEXT_BUDGETS` (constant), lines 4282-4286, exports `RAG_CONTEXT_BUDGETS`
- order 257: `RAG_WEAK_EVIDENCE_MESSAGE` (constant), lines 4287-4287, exports `RAG_WEAK_EVIDENCE_MESSAGE`
- order 258: `RAG_EVIDENCE_SCHEMA_VERSION` (constant), lines 4288-4288, exports `RAG_EVIDENCE_SCHEMA_VERSION`
- order 259: `RAG_EVIDENCE_BATCH_CHARS` (constant), lines 4289-4292, exports `RAG_EVIDENCE_BATCH_CHARS`
- order 260: `RAG_EVALUATION_SUMMARY_CHARS` (constant), lines 4293-4296, exports `RAG_EVALUATION_SUMMARY_CHARS`
- order 261: `RAG_DENSE_DEFAULT_ENABLED` (constant), lines 4297-4297, exports `RAG_DENSE_DEFAULT_ENABLED`
- order 262: `RAG_EMBEDDING_MODE_VALUES` (constant), lines 4298-4298, exports `RAG_EMBEDDING_MODE_VALUES`
- order 263: `RAG_IMPORT_WORKER_COUNT` (constant), lines 4299-4302, exports `RAG_IMPORT_WORKER_COUNT`
- order 265: `RAG_PARSE_TIMEOUT_SECONDS` (constant), lines 4307-4310, exports `RAG_PARSE_TIMEOUT_SECONDS`
- order 1072: `RAG_TERM_GROUPS` (constant), lines 98707-103340, exports `RAG_TERM_GROUPS`
- order 1073: `RAG_RESEARCH_HINTS` (constant), lines 103341-103362, exports `RAG_RESEARCH_HINTS`
- order 1074: `RAG_CODE_HINTS` (constant), lines 103363-103373, exports `RAG_CODE_HINTS`
- order 1075: `RAG_SHORT_TOKEN_ALLOWLIST` (constant), lines 103374-103389, exports `RAG_SHORT_TOKEN_ALLOWLIST`
- order 1076: `RAG_EN_STOPWORDS` (constant), lines 103390-103462, exports `RAG_EN_STOPWORDS`
- order 1077: `RAG_ZH_STOPWORDS` (constant), lines 103463-103499, exports `RAG_ZH_STOPWORDS`
- order 1078: `RAG_GENERIC_ENTITY_TERMS_EN` (constant), lines 103500-103578, exports `RAG_GENERIC_ENTITY_TERMS_EN`
- order 1079: `RAG_GENERIC_ENTITY_TERMS_ZH` (constant), lines 103579-103621, exports `RAG_GENERIC_ENTITY_TERMS_ZH`
- order 1080: `RAG_STRUCTURAL_ENTITY_PATTERNS` (constant), lines 103622-103640, exports `RAG_STRUCTURAL_ENTITY_PATTERNS`
- order 1112: `CODE_LIBRARY_IGNORED_DIRS` (constant), lines 104598-104607, exports `CODE_LIBRARY_IGNORED_DIRS`
- order 1113: `CODE_LIBRARY_LANGUAGE_BY_EXT` (constant), lines 104608-104664, exports `CODE_LIBRARY_LANGUAGE_BY_EXT`
- order 1114: `CODE_LIBRARY_SPECIAL_FILENAMES` (constant), lines 104665-104671, exports `CODE_LIBRARY_SPECIAL_FILENAMES`

### `rag/index.py`

- order 1117: `_code_module_name` (function), lines 104696-104712, exports `_code_module_name`
- order 1118: `_code_choose_community` (function), lines 104713-104722, exports `_code_choose_community`
- order 1119: `_code_query_terms` (function), lines 104723-104737, exports `_code_query_terms`
- order 1128: `TFGraphIDFIndex` (class), lines 105868-107562, exports `TFGraphIDFIndex`
- order 1137: `CodeGraphIndex` (class), lines 110847-111335, exports `CodeGraphIndex`

### `rag/ingestion.py`

- order 1096: `_rag_trigram_set` (function), lines 104018-104025, exports `_rag_trigram_set`
- order 1097: `_rag_jaccard_sim` (function), lines 104026-104035, exports `_rag_jaccard_sim`
- order 1098: `_rag_mmr_select` (function), lines 104036-104085, exports `_rag_mmr_select`
- order 1103: `_rag_embed_text` (function), lines 104220-104243, exports `_rag_embed_text`
- order 1104: `_rag_embed_batch` (function), lines 104244-104252, exports `_rag_embed_batch`
- order 1105: `_rag_window_for_query` (function), lines 104253-104267, exports `_rag_window_for_query`
- order 1106: `_rag_focused_excerpt` (function), lines 104268-104310, exports `_rag_focused_excerpt`
- order 1107: `_rag_query_variants` (function), lines 104311-104350, exports `_rag_query_variants`
- order 1108: `_rag_parse_segments` (function), lines 104351-104413, exports `_rag_parse_segments`
- order 1109: `_rag_boundary_split` (function), lines 104414-104471, exports `_rag_boundary_split`
- order 1135: `_rag_parse_file_worker` (function), lines 109948-109964, exports `_rag_parse_file_worker`
- order 1136: `RAGIngestionService` (class), lines 109965-110846, exports `RAGIngestionService`
- order 1139: `CodeIngestionService` (class), lines 111627-111714, exports `CodeIngestionService`

### `rag/parsers.py`

- order 1081: `EvidenceRecord` (class), lines 103641-103675, exports `EvidenceRecord`
- order 1082: `_rag_float` (function), lines 103676-103682, exports `_rag_float`
- order 1083: `_rag_evidence_source_type` (function), lines 103683-103699, exports `_rag_evidence_source_type`
- order 1084: `_rag_normalize_evidence_record` (function), lines 103700-103755, exports `_rag_normalize_evidence_record`
- order 1085: `_rag_validate_evidence_record` (function), lines 103756-103798, exports `_rag_validate_evidence_record`
- order 1086: `_rag_evidence_batches` (function), lines 103799-103816, exports `_rag_evidence_batches`
- order 1087: `_rag_safe_name` (function), lines 103817-103822, exports `_rag_safe_name`
- order 1088: `_rag_detect_language` (function), lines 103823-103839, exports `_rag_detect_language`
- order 1089: `_rag_cjk_ngrams` (function), lines 103840-103854, exports `_rag_cjk_ngrams`
- order 1090: `_rag_is_noise_token` (function), lines 103855-103876, exports `_rag_is_noise_token`
- order 1091: `_rag_entity_allowed` (function), lines 103877-103891, exports `_rag_entity_allowed`
- order 1092: `_rag_filter_entities` (function), lines 103892-103908, exports `_rag_filter_entities`
- order 1093: `_rag_filename_entity_aliases` (function), lines 103909-103944, exports `_rag_filename_entity_aliases`
- order 1094: `_rag_apply_filename_entity_policy` (function), lines 103945-103977, exports `_rag_apply_filename_entity_policy`
- order 1095: `_rag_choose_community` (function), lines 103978-104017, exports `_rag_choose_community`
- order 1099: `_rag_tokenize` (function), lines 104086-104139, exports `_rag_tokenize`
- order 1100: `_rag_expand_tokens` (function), lines 104140-104163, exports `_rag_expand_tokens`
- order 1101: `_rag_extract_entities` (function), lines 104164-104182, exports `_rag_extract_entities`
- order 1102: `_rag_classify_document` (function), lines 104183-104219, exports `_rag_classify_document`
- order 1110: `_rag_structure_outline` (function), lines 104472-104510, exports `_rag_structure_outline`
- order 1111: `_rag_chunk_text` (function), lines 104511-104597, exports `_rag_chunk_text`
- order 1115: `_code_language_from_name` (function), lines 104672-104690, exports `_code_language_from_name`
- order 1116: `_code_is_test_path` (function), lines 104691-104695, exports `_code_is_test_path`
- order 1120: `_CallCollector` (class), lines 104738-104752, exports `_CallCollector`
- order 1121: `_ALGO_COMPLEXITY_RE` (assignment), lines 104753-104755, exports `_ALGO_COMPLEXITY_RE`
- order 1122: `_ALGO_STEP_RE` (assignment), lines 104756-104756, exports `_ALGO_STEP_RE`
- order 1123: `_ALGO_MATH_VARS` (assignment), lines 104757-104757, exports `_ALGO_MATH_VARS`
- order 1124: `_ALGO_DOC_KEYWORDS` (assignment), lines 104758-104758, exports `_ALGO_DOC_KEYWORDS`
- order 1125: `_detect_algo_chunk` (function), lines 104759-104784, exports `_detect_algo_chunk`
- order 1126: `CodeContentParser` (class), lines 104785-105351, exports `CodeContentParser`
- order 1127: `RAGContentParser` (class), lines 105352-105867, exports `RAGContentParser`

### `rag/store.py`

- order 1129: `RAGLibraryStore` (class), lines 107563-108201, exports `RAGLibraryStore`
- order 1130: `WikiStore` (class), lines 108202-108757, exports `WikiStore`
- order 1131: `UserMemoryStore` (class), lines 108758-109435, exports `UserMemoryStore`
- order 1132: `UserInteractionOptimizer` (class), lines 109436-109504, exports `UserInteractionOptimizer`
- order 1133: `UserIntentProfiler` (class), lines 109505-109546, exports `UserIntentProfiler`
- order 1134: `WorkflowMemoryStore` (class), lines 109547-109947, exports `WorkflowMemoryStore`
- order 1138: `CodeLibraryStore` (class), lines 111336-111626, exports `CodeLibraryStore`

### `rag/web_search.py`

- order 812: `_agent_web_bool` (function), lines 9295-9302, exports `_agent_web_bool`
- order 813: `_agent_web_int` (function), lines 9303-9310, exports `_agent_web_int`
- order 814: `_agent_web_host_is_local_name` (function), lines 9311-9317, exports `_agent_web_host_is_local_name`
- order 815: `_agent_web_ip_is_blocked` (function), lines 9318-9332, exports `_agent_web_ip_is_blocked`
- order 816: `_agent_web_canonical_url` (function), lines 9333-9362, exports `_agent_web_canonical_url`
- order 817: `_agent_web_domain_to_seed` (function), lines 9363-9374, exports `_agent_web_domain_to_seed`
- order 818: `_agent_web_query_terms` (function), lines 9375-9392, exports `_agent_web_query_terms`
- order 819: `_agent_web_query_domain_hints` (function), lines 9393-9433, exports `_agent_web_query_domain_hints`
- order 820: `_agent_web_query_needs_fresh_network` (function), lines 9434-9456, exports `_agent_web_query_needs_fresh_network`
- order 821: `_agent_web_extract_text_snippet` (function), lines 9457-9474, exports `_agent_web_extract_text_snippet`
- order 822: `AgentWebHTMLParser` (class), lines 9475-9554, exports `AgentWebHTMLParser`
- order 823: `_agent_web_decompress_bytes` (function), lines 9555-9578, exports `_agent_web_decompress_bytes`
- order 824: `_agent_web_charset_candidates` (function), lines 9579-9637, exports `_agent_web_charset_candidates`
- order 825: `_agent_web_decode_text_bytes` (function), lines 9638-9672, exports `_agent_web_decode_text_bytes`
- order 826: `AgentWebSearchEngine` (class), lines 9673-11455, exports `AgentWebSearchEngine`

### `server/http.py`

- order 688: `admin_language_payload` (function), lines 6314-6325, exports `admin_language_payload`
- order 801: `_UI_TRUNCATION_MARKER` (assignment), lines 8914-8916, exports `_UI_TRUNCATION_MARKER`
- order 802: `_ui_trim_text` (function), lines 8917-8925, exports `_ui_trim_text`
- order 803: `_bounded_ui_value` (function), lines 8926-8986, exports `_bounded_ui_value`
- order 804: `_bounded_ui_row` (function), lines 8987-9038, exports `_bounded_ui_row`
- order 805: `_bounded_ui_rows` (function), lines 9039-9087, exports `_bounded_ui_rows`
- order 806: `_enforce_ui_payload_budget` (function), lines 9088-9132, exports `_enforce_ui_payload_budget`
- order 807: `_apply_lite_snapshot_bounds` (function), lines 9133-9188, exports `_apply_lite_snapshot_bounds`
- order 1174: `AgentHTTPServer` (class), lines 128101-128140, exports `AgentHTTPServer`
- order 1177: `Handler` (class), lines 129327-131094, exports `Handler`
- order 1180: `SkillsReviewHandler` (class), lines 131896-132009, exports `SkillsReviewHandler`
- order 1184: `CollaborationHandler` (class), lines 134066-134536, exports `CollaborationHandler`

### `server/rag_admin.py`

- order 1179: `_RagAdminAuthMixin` (class), lines 131738-131895, exports `_RagAdminAuthMixin`
- order 1181: `RagAdminHandler` (class), lines 132010-132210, exports `RagAdminHandler`
- order 1182: `CodeAdminHandler` (class), lines 132211-132409, exports `CodeAdminHandler`

### `server/skills.py`

- order 1178: `SkillsHandler` (class), lines 131095-131737, exports `SkillsHandler`

### `session/manager.py`

- order 723: `SessionCreationLimitExceeded` (class), lines 7474-7479, exports `SessionCreationLimitExceeded`
- order 1060: `SessionManager` (class), lines 89566-91908, exports `SessionManager`

### `session/state.py`

- order 1059: `SessionState` (class), lines 29104-89565, exports `SessionState`

### `skills/embedded.py`

- order 959: `EMBEDDED_SKILLS_ARCHIVE_B64` (constant), lines 16732-16733, exports `EMBEDDED_SKILLS_ARCHIVE_B64`
- order 960: `EMBEDDED_SKILLS_ARCHIVE_SHA256` (constant), lines 16734-16734, exports `EMBEDDED_SKILLS_ARCHIVE_SHA256`
- order 961: `EMBEDDED_SKILLS_ARCHIVE_FILES` (constant), lines 16735-16757, exports `EMBEDDED_SKILLS_ARCHIVE_FILES`
- order 986: `BUILTIN_CLAWHUB_SKILLS_VERSION` (constant), lines 19993-19995, exports `BUILTIN_CLAWHUB_SKILLS_VERSION`
- order 987: `EMBEDDED_CLAWHUB_SKILLS_ARCHIVE_B64` (constant), lines 19996-20241, exports `EMBEDDED_CLAWHUB_SKILLS_ARCHIVE_B64`
- order 989: `MCP_BUILDER_SKILL_MD` (constant), lines 20289-20463, exports `MCP_BUILDER_SKILL_MD`
- order 992: `SKILL_PROTOCOL_LOCAL` (constant), lines 20495-20496, exports `SKILL_PROTOCOL_LOCAL`
- order 993: `SKILL_PROTOCOL_CLAWHUB` (constant), lines 20497-20497, exports `SKILL_PROTOCOL_CLAWHUB`
- order 994: `SKILL_PROTOCOL_HTTP_JSON` (constant), lines 20498-20498, exports `SKILL_PROTOCOL_HTTP_JSON`
- order 995: `SKILL_PROTOCOL_SPECS` (constant), lines 20499-20531, exports `SKILL_PROTOCOL_SPECS`

### `skills/provisioning.py`

- order 962: `ensure_embedded_skills_at_root` (function), lines 16758-16823, exports `ensure_embedded_skills_at_root`
- order 963: `ensure_embedded_skills` (function), lines 16824-16827, exports `ensure_embedded_skills`
- order 965: `detect_upload_parser_capabilities` (function), lines 16834-16850, exports `detect_upload_parser_capabilities`
- order 966: `_render_cap_markdown` (function), lines 16851-16866, exports `_render_cap_markdown`
- order 967: `_write_text_if_changed` (function), lines 16867-16873, exports `_write_text_if_changed`
- order 968: `ensure_generated_document_skills` (function), lines 16874-16963, exports `ensure_generated_document_skills`
- order 969: `ensure_generated_image_coding_feedback_skill` (function), lines 16964-17064, exports `ensure_generated_image_coding_feedback_skill`
- order 970: `_skill_knowledge_files` (function), lines 17065-17085, exports `_skill_knowledge_files`
- order 971: `analyze_skill_building_knowledge` (function), lines 17086-17141, exports `analyze_skill_building_knowledge`
- order 972: `_sanitize_skill_slug` (function), lines 17142-17145, exports `_sanitize_skill_slug`
- order 973: `_build_skills_gen_skill_content` (function), lines 17146-17178, exports `_build_skills_gen_skill_content`
- order 974: `ensure_generated_skills_gen_skill` (function), lines 17179-17184, exports `ensure_generated_skills_gen_skill`
- order 975: `ensure_generated_execution_recovery_skill` (function), lines 17185-17269, exports `ensure_generated_execution_recovery_skill`
- order 976: `ensure_generated_systematic_debugging_skill` (function), lines 17270-17543, exports `ensure_generated_systematic_debugging_skill`
- order 977: `ensure_generated_code_engineering_mastery_skill` (function), lines 17544-17663, exports `ensure_generated_code_engineering_mastery_skill`
- order 978: `ensure_generated_smart_file_navigation_skill` (function), lines 17664-17780, exports `ensure_generated_smart_file_navigation_skill`
- order 979: `ensure_generated_html_frontend_report_skills` (function), lines 17781-17989, exports `ensure_generated_html_frontend_report_skills`
- order 980: `ensure_generated_deep_research_skills` (function), lines 17990-18259, exports `ensure_generated_deep_research_skills`
- order 981: `ensure_generated_research_scientific_skills` (function), lines 18260-18897, exports `ensure_generated_research_scientific_skills`
- order 982: `ensure_generated_rag_mastery_skills` (function), lines 18898-19199, exports `ensure_generated_rag_mastery_skills`
- order 983: `ensure_generated_multimodal_comprehension_skills` (function), lines 19200-19894, exports `ensure_generated_multimodal_comprehension_skills`
- order 984: `ensure_generated_runtime_skills_manifest` (function), lines 19895-19929, exports `ensure_generated_runtime_skills_manifest`
- order 985: `ensure_generated_agent_web_search_skill` (function), lines 19930-19992, exports `ensure_generated_agent_web_search_skill`
- order 988: `ensure_embedded_clawhub_skills` (function), lines 20242-20288, exports `ensure_embedded_clawhub_skills`
- order 990: `ensure_generated_mcp_builder_skill` (function), lines 20464-20475, exports `ensure_generated_mcp_builder_skill`
- order 991: `ensure_runtime_skills` (function), lines 20476-20494, exports `ensure_runtime_skills`

### `skills/store.py`

- order 996: `_BUILTIN_SKILLS` (assignment), lines 20532-20640, exports `_BUILTIN_SKILLS`
- order 997: `SkillStore` (class), lines 20641-22534, exports `SkillStore`

### `skills/studio.py`

- order 1162: `SkillsStudioError` (class), lines 115476-115485, exports `SkillsStudioError`
- order 1163: `_studio_slug` (function), lines 115486-115501, exports `_studio_slug`
- order 1164: `_studio_hash` (function), lines 115502-115505, exports `_studio_hash`
- order 1165: `_studio_cookie_value` (function), lines 115506-115515, exports `_studio_cookie_value`
- order 1166: `SkillsStudioStore` (class), lines 115516-117374, exports `SkillsStudioStore`

### `utils/compress.py`

- order 830: `compress_text_blob` (function), lines 11620-11626, exports `compress_text_blob`
- order 831: `decompress_text_blob` (function), lines 11627-11636, exports `decompress_text_blob`

### `utils/crypto.py`

- order 903: `CryptoBox` (class), lines 13573-13726, exports `CryptoBox`

### `utils/errors.py`

- order 850: `EmptyActionError` (class), lines 12125-12128, exports `EmptyActionError`
- order 999: `ProcessManagerError` (class), lines 22670-22675, exports `ProcessManagerError`

### `utils/files.py`

- order 682: `_normalize_js_lib_asset_ref` (function), lines 6184-6199, exports `_normalize_js_lib_asset_ref`
- order 683: `_resolve_js_lib_asset_path` (function), lines 6200-6231, exports `_resolve_js_lib_asset_path`
- order 684: `_discover_extra_js_lib_files` (function), lines 6232-6264, exports `_discover_extra_js_lib_files`
- order 776: `safe_path` (function), lines 8327-8337, exports `safe_path`
- order 777: `_safe_js_filename` (function), lines 8338-8346, exports `_safe_js_filename`
- order 778: `_sha256_bytes` (function), lines 8347-8349, exports `_sha256_bytes`
- order 779: `_sha256_file` (function), lines 8350-8359, exports `_sha256_file`
- order 780: `_download_http_bytes` (function), lines 8360-8369, exports `_download_http_bytes`
- order 781: `offline_js_lib_root` (function), lines 8370-8372, exports `offline_js_lib_root`
- order 782: `_offline_js_entry_relative_path` (function), lines 8373-8378, exports `_offline_js_entry_relative_path`
- order 783: `_archive_member_relative_path` (function), lines 8379-8389, exports `_archive_member_relative_path`
- order 784: `_path_size_bytes` (function), lines 8390-8406, exports `_path_size_bytes`
- order 785: `_extract_archive_to_dir` (function), lines 8407-8448, exports `_extract_archive_to_dir`
- order 786: `_package_required_paths` (function), lines 8449-8456, exports `_package_required_paths`
- order 787: `_package_required_globs` (function), lines 8457-8473, exports `_package_required_globs`
- order 788: `_package_install_ready` (function), lines 8474-8496, exports `_package_install_ready`
- order 789: `_postprocess_offline_js_package` (function), lines 8497-8533, exports `_postprocess_offline_js_package`
- order 790: `_ensure_offline_js_package` (function), lines 8534-8578, exports `_ensure_offline_js_package`
- order 791: `_render_offline_js_catalog_md` (function), lines 8579-8596, exports `_render_offline_js_catalog_md`
- order 793: `ensure_offline_js_libs` (function), lines 8608-8766, exports `ensure_offline_js_libs`
- order 794: `_offline_js_catalog_entry_for_asset` (function), lines 8767-8787, exports `_offline_js_catalog_entry_for_asset`
- order 795: `ensure_offline_js_asset` (function), lines 8788-8845, exports `ensure_offline_js_asset`
- order 796: `_normalize_external_js_url` (function), lines 8846-8851, exports `_normalize_external_js_url`
- order 797: `is_external_js_src` (function), lines 8852-8855, exports `is_external_js_src`
- order 798: `match_offline_js_catalog_by_url` (function), lines 8856-8873, exports `match_offline_js_catalog_by_url`
- order 799: `cache_external_js_url` (function), lines 8874-8909, exports `cache_external_js_url`
- order 906: `try_read_text` (function), lines 13970-13979, exports `try_read_text`

### `utils/http.py`

- order 117: `_URL_OPEN_ORIGINAL` (assignment), lines 3781-3781, exports `_URL_OPEN_ORIGINAL`
- order 118: `_HTTP_SSL_CONTEXT` (assignment), lines 3782-3782, exports `_HTTP_SSL_CONTEXT`
- order 145: `_shared_http_ssl_context` (function), lines 3846-3869, exports `_shared_http_ssl_context`
- order 146: `urlopen` (function), lines 3870-3879, exports `urlopen`
- order 769: `json_response_bytes` (function), lines 8272-8274, exports `json_response_bytes`
- order 770: `read_http_json_body` (function), lines 8275-8288, exports `read_http_json_body`
- order 771: `close_if_http_request_body_unread` (function), lines 8289-8302, exports `close_if_http_request_body_unread`

### `utils/json_utils.py`

- order 169: `JSON_FSYNC_ENABLED` (constant), lines 4151-4151, exports `JSON_FSYNC_ENABLED`
- order 768: `json_dumps` (function), lines 8268-8271, exports `json_dumps`
- order 840: `parse_tool_arguments` (function), lines 11930-11940, exports `parse_tool_arguments`
- order 841: `repair_truncated_json_object` (function), lines 11941-11995, exports `repair_truncated_json_object`
- order 842: `parse_tool_arguments_with_error` (function), lines 11996-12027, exports `parse_tool_arguments_with_error`
- order 843: `_is_valid_json_object` (function), lines 12028-12033, exports `_is_valid_json_object`
- order 844: `_scan_top_level_json_objects` (function), lines 12034-12057, exports `_scan_top_level_json_objects`
- order 845: `reconstruct_streamed_tool_args` (function), lines 12058-12102, exports `reconstruct_streamed_tool_args`
- order 863: `parse_json_object` (function), lines 12366-12372, exports `parse_json_object`
- order 864: `extract_json_object_from_text` (function), lines 12373-12396, exports `extract_json_object_from_text`
- order 907: `_json_default_copy` (function), lines 13980-13986, exports `_json_default_copy`
- order 908: `_read_json_file` (function), lines 13987-14008, exports `_read_json_file`
- order 909: `_write_json_file` (function), lines 14009-14037, exports `_write_json_file`

### `utils/media.py`

- order 675: `_capability_probe_png_bytes` (function), lines 5822-5836, exports `_capability_probe_png_bytes`
- order 676: `_capability_probe_audio_bytes` (function), lines 5837-5848, exports `_capability_probe_audio_bytes`
- order 677: `_capability_probe_video_bytes` (function), lines 5849-5853, exports `_capability_probe_video_bytes`
- order 738: `guess_mime_from_name` (function), lines 7822-7826, exports `guess_mime_from_name`
- order 739: `_convert_image_to_safe_format` (function), lines 7827-7846, exports `_convert_image_to_safe_format`
- order 740: `guess_ext_from_mime` (function), lines 7847-7855, exports `guess_ext_from_mime`

### `utils/misc.py`

- order 741: `now_ts` (function), lines 7856-7858, exports `now_ts`
- order 742: `_benign_socket_log_lock` (assignment), lines 7859-7861, exports `_benign_socket_log_lock`
- order 743: `_benign_socket_log_state` (assignment), lines 7862-7862, exports `_benign_socket_log_state`
- order 745: `is_benign_socket_error` (function), lines 7878-7898, exports `is_benign_socket_error`
- order 746: `_socket_error_code` (function), lines 7899-7910, exports `_socket_error_code`
- order 747: `_log_benign_socket_error_limited` (function), lines 7911-7947, exports `_log_benign_socket_error_limited`
- order 748: `swallow_benign_socket_error` (function), lines 7948-7954, exports `swallow_benign_socket_error`
- order 749: `normalize_timeout_seconds` (function), lines 7955-7970, exports `normalize_timeout_seconds`
- order 750: `detect_local_lan_ip` (function), lines 7971-7982, exports `detect_local_lan_ip`
- order 751: `_LOCAL_LAN_IP_CACHE` (assignment), lines 7983-7984, exports `_LOCAL_LAN_IP_CACHE`
- order 752: `detect_local_lan_ip_cached` (function), lines 7985-7998, exports `detect_local_lan_ip_cached`
- order 772: `make_id` (function), lines 8303-8305, exports `make_id`
- order 773: `sanitize_profile_id` (function), lines 8306-8309, exports `sanitize_profile_id`
- order 901: `user_id_from_ip` (function), lines 13532-13539, exports `user_id_from_ip`
- order 905: `_meta_string_list` (function), lines 13956-13969, exports `_meta_string_list`
- order 964: `_module_exists` (function), lines 16828-16833, exports `_module_exists`

### `utils/text.py`

- order 157: `MAX_TOOL_OUTPUT` (constant), lines 4139-4139, exports `MAX_TOOL_OUTPUT`
- order 496: `SOCKET_NOISE_LINE_PATTERNS` (constant), lines 4910-4915, exports `SOCKET_NOISE_LINE_PATTERNS`
- order 744: `filter_runtime_noise_lines` (function), lines 7863-7877, exports `filter_runtime_noise_lines`
- order 757: `safe_utf8_bytes` (function), lines 8123-8125, exports `safe_utf8_bytes`
- order 758: `escape_invalid_utf8_text` (function), lines 8126-8128, exports `escape_invalid_utf8_text`
- order 759: `sanitize_utf8_surrogates` (function), lines 8129-8142, exports `sanitize_utf8_surrogates`
- order 760: `decode_utf8_replace` (function), lines 8143-8147, exports `decode_utf8_replace`
- order 800: `trim` (function), lines 8910-8913, exports `trim`
- order 808: `is_synthetic_public_progress` (function), lines 9189-9208, exports `is_synthetic_public_progress`
- order 810: `display_clean` (function), lines 9261-9275, exports `display_clean`
- order 811: `short_title_from` (function), lines 9276-9294, exports `short_title_from`
- order 827: `_fmt_export_ts` (function), lines 11456-11466, exports `_fmt_export_ts`
- order 828: `_html_esc` (function), lines 11467-11470, exports `_html_esc`
- order 829: `_text_to_minimal_pdf` (function), lines 11471-11619, exports `_text_to_minimal_pdf`
- order 832: `normalize_embedded_newlines` (function), lines 11637-11646, exports `normalize_embedded_newlines`
- order 833: `_map_todo_status_token` (function), lines 11647-11685, exports `_map_todo_status_token`
- order 834: `split_todo_status_text` (function), lines 11686-11745, exports `split_todo_status_text`
- order 835: `extract_todo_rows_from_text` (function), lines 11746-11815, exports `extract_todo_rows_from_text`
- order 836: `decode_structured_todo_container` (function), lines 11816-11834, exports `decode_structured_todo_container`
- order 837: `infer_todo_status_from_text` (function), lines 11835-11843, exports `infer_todo_status_from_text`
- order 838: `split_structured_todo_content` (function), lines 11844-11899, exports `split_structured_todo_content`
- order 839: `normalize_work_text` (function), lines 11900-11929, exports `normalize_work_text`
- order 930: `make_unified_diff` (function), lines 15590-15608, exports `make_unified_diff`
- order 931: `_skip_row` (function), lines 15609-15614, exports `_skip_row`
- order 932: `_row_is_hot` (function), lines 15615-15618, exports `_row_is_hot`
- order 933: `_hotspot_index` (function), lines 15619-15642, exports `_hotspot_index`
- order 934: `_compress_rows_keep_hotspot` (function), lines 15643-15692, exports `_compress_rows_keep_hotspot`
- order 935: `_focused_diff_rows_from_opcodes` (function), lines 15693-15827, exports `_focused_diff_rows_from_opcodes`
- order 936: `make_numbered_diff` (function), lines 15828-15860, exports `make_numbered_diff`
- order 937: `render_numbered_diff_text` (function), lines 15861-15874, exports `render_numbered_diff_text`

### `web/admin_assets.py`

- order 1069: `ADMIN_INDEX_HTML` (constant), lines 97893-98193, exports `ADMIN_INDEX_HTML`
- order 1070: `ADMIN_CSS` (constant), lines 98194-98330, exports `ADMIN_CSS`
- order 1071: `ADMIN_JS` (constant), lines 98331-98706, exports `ADMIN_JS`

### `web/assets.py`

- order 1061: `INDEX_HTML` (constant), lines 91909-92168, exports `INDEX_HTML`
- order 1062: `APP_CSS` (constant), lines 92169-92709, exports `APP_CSS`
- order 1063: `APP_JS` (constant), lines 92710-97433, exports `APP_JS`
- order 1064: `APP_CSS` (constant), lines 97434-97450, exports `APP_CSS`
- order 1065: `APP_TS` (constant), lines 97451-97490, exports `APP_TS`

### `web/skills_assets.py`

- order 1066: `SKILLS_INDEX_HTML` (constant), lines 97491-97646, exports `SKILLS_INDEX_HTML`
- order 1067: `SKILLS_EXTRA_CSS` (constant), lines 97647-97746, exports `SKILLS_EXTRA_CSS`
- order 1068: `SKILLS_APP_JS` (constant), lines 97747-97892, exports `SKILLS_APP_JS`
