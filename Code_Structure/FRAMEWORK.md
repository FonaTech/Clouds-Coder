# Code_Structure Framework

## Overview

- Source snapshot: `Clouds_Coder.py` (1192 top-level statements)
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
| `_imports.py` | 75 | 93 | — | 1–3818 |
| `admin/auth.py` | 3 | 3 | `admin/constants.py`, `utils/misc.py`, `utils/sqlite.py` | 13575–14417 |
| `admin/config.py` | 8 | 8 | `config/constants.py`, `config/paths.py`, `config/settings.py`, `llm/constants.py`, `utils/http.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` | 15165–15628 |
| `admin/constants.py` | 16 | 16 | — | 3825–117419 |
| `agent/background.py` | 1 | 1 | `agent/process.py`, `config/constants.py`, `ide/sandbox.py`, `utils/misc.py`, `utils/text.py` | 23075–23700 |
| `agent/bus.py` | 1 | 1 | `config/constants.py`, `utils/crypto.py`, `utils/misc.py` | 23701–23766 |
| `agent/errors.py` | 1 | 1 | — | 12165–12168 |
| `agent/events.py` | 1 | 1 | — | 16355–16409 |
| `agent/process.py` | 7 | 7 | `ide/sandbox.py`, `utils/errors.py`, `utils/misc.py`, `utils/text.py` | 8204–23074 |
| `agent/tasks.py` | 1 | 1 | `utils/crypto.py`, `utils/json_utils.py`, `utils/misc.py` | 22574–22708 |
| `agent/todo.py` | 1 | 1 | `config/constants.py`, `config/settings.py`, `utils/misc.py`, `utils/text.py` | 16410–16770 |
| `agent/tools.py` | 15 | 19 | `config/constants.py`, `utils/text.py` | 16234–28613 |
| `agent/worktree.py` | 1 | 1 | `agent/process.py`, `agent/tasks.py`, `config/constants.py`, `utils/crypto.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` | 23767–23979 |
| `app/context.py` | 1 | 1 | `admin/auth.py`, `admin/config.py`, `admin/constants.py`, `agent/process.py`, `agent/tools.py`, `app/services.py`, `collaboration/core.py`, `config/bootstrap.py`, `config/constants.py`, `config/paths.py`, `config/settings.py`, `ide/assets.py`, `ide/auth.py`, `ide/errors.py`, `ide/events.py`, `ide/preview.py`, `ide/sandbox.py`, `llm/client.py`, `llm/constants.py`, `llm/utils.py`, `mcp/driver.py`, `rag/assets.py`, `rag/constants.py`, `rag/ingestion.py`, `rag/parsers.py`, `rag/store.py`, `server/http.py`, `session/manager.py`, `session/state.py`, `skills/provisioning.py`, `skills/store.py`, `skills/studio.py`, `utils/crypto.py`, `utils/files.py`, `utils/http.py`, `utils/json_utils.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py`, `web/assets.py`, `web/skills_assets.py` | 117420–128136 |
| `app/main.py` | 2 | 1 | `admin/config.py`, `admin/constants.py`, `agent/tools.py`, `app/context.py`, `collaboration/watcher.py`, `config/constants.py`, `config/paths.py`, `config/settings.py`, `ide/handler.py`, `llm/constants.py`, `llm/utils.py`, `mcp/constants.py`, `mcp/service.py`, `rag/constants.py`, `server/http.py`, `server/rag_admin.py`, `server/skills.py`, `skills/provisioning.py`, `utils/files.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` | 134882–136833 |
| `app/services.py` | 2 | 2 | `admin/constants.py`, `config/settings.py`, `skills/embedded.py`, `skills/store.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/sqlite.py`, `utils/text.py` | 128177–129362 |
| `collaboration/core.py` | 23 | 23 | `config/constants.py`, `utils/sqlite.py` | 437–3678 |
| `collaboration/watcher.py` | 2 | 2 | `utils/misc.py`, `utils/text.py` | 134791–134881 |
| `config/bootstrap.py` | 5 | 5 | `config/constants.py`, `config/settings.py`, `utils/json_utils.py`, `utils/misc.py` | 114–14130 |
| `config/constants.py` | 502 | 498 | `config/bootstrap.py`, `rag/constants.py` | 413–117415 |
| `config/paths.py` | 13 | 13 | `agent/process.py`, `utils/crypto.py`, `utils/text.py` | 3824–8364 |
| `config/settings.py` | 68 | 68 | `agent/tools.py`, `config/constants.py`, `config/paths.py`, `ide/preview.py`, `llm/constants.py`, `llm/utils.py`, `rag/constants.py`, `skills/provisioning.py`, `utils/http.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` | 6303–15962 |
| `ide/assets.py` | 8 | 3 | — | 114359–115487 |
| `ide/auth.py` | 2 | 2 | `admin/auth.py`, `admin/constants.py`, `config/constants.py`, `utils/misc.py`, `utils/sqlite.py`, `utils/text.py` | 14418–15149 |
| `ide/errors.py` | 2 | 2 | — | 15150–15164 |
| `ide/events.py` | 1 | 1 | `config/constants.py`, `utils/text.py` | 9247–9298 |
| `ide/handler.py` | 1 | 1 | `admin/auth.py`, `app/context.py`, `collaboration/core.py`, `config/constants.py`, `config/settings.py`, `ide/auth.py`, `ide/errors.py`, `ide/events.py`, `session/manager.py`, `session/state.py`, `utils/http.py`, `utils/json_utils.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py` | 132446–134101 |
| `ide/preview.py` | 12 | 12 | `config/constants.py`, `utils/text.py` | 15914–16354 |
| `ide/sandbox.py` | 21 | 21 | `agent/process.py`, `utils/misc.py` | 8186–29142 |
| `llm/client.py` | 2 | 2 | `agent/tools.py`, `config/constants.py`, `config/settings.py`, `llm/utils.py`, `utils/http.py`, `utils/json_utils.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py` | 25362–27887 |
| `llm/constants.py` | 17 | 17 | — | 3822–12607 |
| `llm/utils.py` | 22 | 22 | `agent/process.py`, `config/settings.py`, `llm/constants.py`, `utils/http.py`, `utils/json_utils.py`, `utils/text.py` | 12139–12821 |
| `mcp/constants.py` | 8 | 8 | — | 4194–24015 |
| `mcp/driver.py` | 13 | 13 | `mcp/constants.py`, `utils/files.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` | 24016–25361 |
| `mcp/service.py` | 1 | 1 | `app/context.py`, `config/constants.py`, `utils/files.py`, `utils/http.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` | 134573–134790 |
| `rag/assets.py` | 6 | 6 | — | 111752–114358 |
| `rag/constants.py` | 77 | 77 | — | 4190–104710 |
| `rag/index.py` | 5 | 5 | `config/constants.py`, `rag/constants.py`, `rag/ingestion.py`, `rag/parsers.py`, `utils/misc.py`, `utils/text.py` | 104735–111372 |
| `rag/ingestion.py` | 13 | 13 | `config/constants.py`, `config/settings.py`, `rag/constants.py`, `rag/parsers.py`, `rag/store.py`, `session/state.py`, `utils/files.py`, `utils/json_utils.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py` | 104057–111751 |
| `rag/parsers.py` | 31 | 31 | `agent/process.py`, `config/constants.py`, `rag/constants.py`, `rag/ingestion.py`, `utils/files.py`, `utils/json_utils.py`, `utils/media.py`, `utils/text.py` | 103680–105906 |
| `rag/store.py` | 7 | 7 | `config/constants.py`, `config/settings.py`, `ide/preview.py`, `rag/constants.py`, `rag/index.py`, `rag/ingestion.py`, `rag/parsers.py`, `skills/provisioning.py`, `utils/files.py`, `utils/json_utils.py`, `utils/media.py`, `utils/misc.py`, `utils/sqlite.py`, `utils/text.py` | 107602–111663 |
| `rag/web_search.py` | 15 | 15 | `config/constants.py`, `config/paths.py`, `rag/constants.py`, `utils/http.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/sqlite.py`, `utils/text.py` | 9333–11491 |
| `server/http.py` | 12 | 12 | `admin/auth.py`, `admin/config.py`, `admin/constants.py`, `agent/process.py`, `app/context.py`, `collaboration/core.py`, `collaboration/watcher.py`, `config/constants.py`, `config/paths.py`, `config/settings.py`, `ide/handler.py`, `ide/preview.py`, `llm/utils.py`, `server/rag_admin.py`, `session/manager.py`, `session/state.py`, `skills/studio.py`, `utils/errors.py`, `utils/files.py`, `utils/http.py`, `utils/json_utils.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py`, `web/admin_assets.py` | 6352–134572 |
| `server/rag_admin.py` | 3 | 3 | `admin/auth.py`, `app/context.py`, `config/constants.py`, `rag/constants.py`, `utils/http.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py` | 131774–132445 |
| `server/skills.py` | 1 | 1 | `admin/auth.py`, `app/context.py`, `config/constants.py`, `config/paths.py`, `config/settings.py`, `session/manager.py`, `skills/provisioning.py`, `skills/studio.py`, `utils/http.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py` | 131131–131773 |
| `session/manager.py` | 2 | 2 | `agent/process.py`, `config/constants.py`, `config/paths.py`, `config/settings.py`, `llm/client.py`, `llm/utils.py`, `rag/store.py`, `session/state.py`, `skills/store.py`, `utils/crypto.py`, `utils/files.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` | 7512–91947 |
| `session/state.py` | 1 | 1 | `admin/constants.py`, `agent/background.py`, `agent/bus.py`, `agent/errors.py`, `agent/events.py`, `agent/process.py`, `agent/tasks.py`, `agent/todo.py`, `agent/tools.py`, `agent/worktree.py`, `collaboration/core.py`, `config/constants.py`, `config/paths.py`, `config/settings.py`, `ide/events.py`, `ide/preview.py`, `ide/sandbox.py`, `llm/client.py`, `llm/constants.py`, `llm/utils.py`, `mcp/constants.py`, `mcp/driver.py`, `rag/constants.py`, `rag/parsers.py`, `rag/web_search.py`, `server/http.py`, `skills/provisioning.py`, `skills/store.py`, `utils/compress.py`, `utils/crypto.py`, `utils/errors.py`, `utils/files.py`, `utils/http.py`, `utils/json_utils.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py` | 29143–89604 |
| `skills/embedded.py` | 10 | 10 | — | 16771–20570 |
| `skills/provisioning.py` | 26 | 26 | `config/paths.py`, `skills/embedded.py`, `utils/files.py`, `utils/json_utils.py`, `utils/misc.py` | 16797–20533 |
| `skills/store.py` | 2 | 2 | `config/constants.py`, `config/settings.py`, `llm/utils.py`, `skills/embedded.py`, `utils/files.py`, `utils/http.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` | 20571–22573 |
| `skills/studio.py` | 5 | 5 | `agent/process.py`, `collaboration/core.py`, `config/constants.py`, `config/settings.py`, `ide/sandbox.py`, `llm/client.py`, `llm/constants.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/sqlite.py`, `utils/text.py` | 115513–117410 |
| `utils/compress.py` | 2 | 2 | — | 11656–11672 |
| `utils/crypto.py` | 1 | 1 | `utils/json_utils.py` | 13608–13761 |
| `utils/errors.py` | 2 | 2 | — | 12161–22714 |
| `utils/files.py` | 27 | 27 | `config/constants.py`, `config/paths.py`, `utils/http.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` | 6222–14014 |
| `utils/http.py` | 7 | 7 | `utils/json_utils.py`, `utils/text.py` | 3819–8340 |
| `utils/json_utils.py` | 13 | 13 | `utils/text.py` | 4189–14072 |
| `utils/media.py` | 6 | 6 | — | 5860–7893 |
| `utils/misc.py` | 16 | 16 | `config/constants.py` | 7894–16872 |
| `utils/sqlite.py` | 2 | 2 | — | 74–107 |
| `utils/text.py` | 30 | 30 | `config/constants.py` | 4177–15913 |
| `web/admin_assets.py` | 3 | 3 | — | 97932–98745 |
| `web/assets.py` | 5 | 4 | — | 91948–97529 |
| `web/skills_assets.py` | 3 | 3 | — | 97530–97931 |

## Source Mapping

### `_imports.py`

- order 0: `_import_3` (import), lines 1-3, exports `annotations`
- order 1: `_import_5` (import), lines 4-5, exports `argparse`
- order 2: `_import_6` (import), lines 6-6, exports `ast`
- order 3: `_import_7` (import), lines 7-7, exports `base64`
- order 4: `_import_8` (import), lines 8-8, exports `concurrent`
- order 5: `_import_9` (import), lines 9-9, exports `contextlib`
- order 6: `_import_10` (import), lines 10-10, exports `copy`
- order 7: `_import_11` (import), lines 11-11, exports `csv`
- order 8: `_import_12` (import), lines 12-12, exports `ctypes`
- order 9: `_import_13` (import), lines 13-13, exports `difflib`
- order 10: `_import_14` (import), lines 14-14, exports `errno`
- order 11: `_import_15` (import), lines 15-15, exports `fnmatch`
- order 12: `_import_16` (import), lines 16-16, exports `hashlib`
- order 13: `_import_17` (import), lines 17-17, exports `hmac`
- order 14: `_import_18` (import), lines 18-18, exports `html`
- order 15: `_import_19` (import), lines 19-19, exports `importlib`
- order 16: `_import_20` (import), lines 20-20, exports `io`
- order 17: `_import_21` (import), lines 21-21, exports `ipaddress`
- order 18: `_import_22` (import), lines 22-22, exports `json`
- order 19: `_import_23` (import), lines 23-23, exports `locale`
- order 20: `_import_24` (import), lines 24-24, exports `math`
- order 21: `_import_25` (import), lines 25-25, exports `mimetypes`
- order 22: `_import_26` (import), lines 26-26, exports `multiprocessing`
- order 23: `_import_27` (import), lines 27-27, exports `os`
- order 24: `_import_28` (import), lines 28-28, exports `platform`
- order 25: `_import_29` (import), lines 29-29, exports `posixpath`
- order 26: `_import_30` (import), lines 30-30, exports `queue`
- order 27: `_import_31` (import), lines 31-31, exports `random`
- order 28: `_import_32` (import), lines 32-32, exports `re`
- order 29: `_import_33` (import), lines 33-33, exports `secrets`
- order 30: `_import_34` (import), lines 34-34, exports `select`
- order 31: `_import_35` (import), lines 35-35, exports `selectors`
- order 32: `_import_36` (import), lines 36-36, exports `shlex`
- order 33: `_import_37` (import), lines 37-37, exports `shutil`
- order 34: `_import_38` (import), lines 38-38, exports `signal`
- order 35: `_import_39` (import), lines 39-39, exports `socket`
- order 36: `_import_40` (import), lines 40-40, exports `sqlite3`
- order 37: `_import_41` (import), lines 41-41, exports `ssl`
- order 38: `_import_42` (import), lines 42-42, exports `stat`
- order 39: `_import_43` (import), lines 43-43, exports `struct`
- order 40: `_import_44` (import), lines 44-44, exports `subprocess`
- order 41: `_import_45` (import), lines 45-45, exports `sys`
- order 42: `_import_46` (import), lines 46-46, exports `tarfile`
- order 43: `_import_47` (import), lines 47-47, exports `tempfile`
- order 44: `_import_48` (import), lines 48-48, exports `threading`
- order 45: `_import_49` (import), lines 49-49, exports `time`
- order 46: `_import_50` (import), lines 50-50, exports `traceback`
- order 47: `_import_51` (import), lines 51-51, exports `unicodedata`
- order 48: `_import_52` (import), lines 52-52, exports `robotparser`
- order 49: `_import_53` (import), lines 53-53, exports `uuid`
- order 50: `_import_54` (import), lines 54-54, exports `ET`
- order 51: `_import_55` (import), lines 55-55, exports `zipfile`
- order 52: `_import_56` (import), lines 56-56, exports `zlib`
- order 53: `_import_57` (import), lines 57-57, exports `Counter`, `defaultdict`, `deque`
- order 54: `_import_58` (import), lines 58-58, exports `Iterable`
- order 55: `_import_59` (import), lines 59-59, exports `asdict`, `dataclass`
- order 56: `_import_60` (import), lines 60-60, exports `dataclass_field`
- order 57: `_import_61` (import), lines 61-61, exports `datetime`, `timedelta`, `timezone`
- order 58: `_import_62` (import), lines 62-62, exports `parsedate_to_datetime`
- order 59: `_import_63` (import), lines 63-63, exports `HTMLParser`
- order 60: `_import_64` (import), lines 64-64, exports `HTTPStatus`
- order 61: `_import_65` (import), lines 65-65, exports `IncompleteRead`
- order 62: `_import_66` (import), lines 66-66, exports `SimpleCookie`
- order 63: `_import_67` (import), lines 67-67, exports `BaseHTTPRequestHandler`, `ThreadingHTTPServer`
- order 64: `_import_68` (import), lines 68-68, exports `Path`, `PurePosixPath`
- order 65: `_import_69` (import), lines 69-69, exports `Any`
- order 66: `_import_70` (import), lines 70-70, exports `HTTPError`, `URLError`
- order 67: `_import_71` (import), lines 71-71, exports `parse_qs`, `quote`, `unquote`, `urljoin`, `urlparse`, `urlunparse`
- order 68: `_import_72` (import), lines 72-72, exports `Request`, `urlopen`
- order 69: `_import_73` (import), lines 73-73, exports `ZoneInfo`
- order 72: `_try_import_110` (import), lines 108-113, exports `_AESGCM`
- order 76: `_import_417` (import), lines 416-421, exports `EVOLUTION_MODES`, `LiquidKernelControlPlane`, `LiquidKernelError`
- order 116: `_try_import_3802` (import), lines 3800-3809, exports `_fcntl`, `_pty`, `_termios`
- order 117: `_try_import_3811` (import), lines 3810-3814, exports `_certifi`
- order 118: `_try_import_3815` (import), lines 3815-3818, exports `_yaml`

### `admin/auth.py`

- order 904: `trusted_client_ip` (function), lines 13575-13607, exports `trusted_client_ip`
- order 918: `AdminAuthError` (class), lines 14131-14138, exports `AdminAuthError`
- order 919: `AdminAuthStore` (class), lines 14139-14417, exports `AdminAuthStore`

### `admin/config.py`

- order 924: `_admin_config_schema` (function), lines 15165-15285, exports `_admin_config_schema`
- order 925: `_admin_factory_config` (function), lines 15286-15289, exports `_admin_factory_config`
- order 926: `_admin_coerce_config` (function), lines 15290-15445, exports `_admin_coerce_config`
- order 927: `_admin_config_to_argv` (function), lines 15446-15482, exports `_admin_config_to_argv`
- order 928: `_admin_restart_probe_url` (function), lines 15483-15498, exports `_admin_restart_probe_url`
- order 929: `_admin_supervised_restart` (function), lines 15499-15585, exports `_admin_supervised_restart`
- order 930: `_admin_argparse_defaults` (function), lines 15586-15607, exports `_admin_argparse_defaults`
- order 931: `_admin_config_from_namespace` (function), lines 15608-15628, exports `_admin_config_from_namespace`

### `admin/constants.py`

- order 125: `ADMIN_STATE_DIRNAME` (constant), lines 3825-3825, exports `ADMIN_STATE_DIRNAME`
- order 126: `ADMIN_CONFIG_FILENAME` (constant), lines 3826-3826, exports `ADMIN_CONFIG_FILENAME`
- order 127: `ADMIN_APPS_FILENAME` (constant), lines 3827-3827, exports `ADMIN_APPS_FILENAME`
- order 128: `ADMIN_TELEMETRY_FILENAME` (constant), lines 3828-3828, exports `ADMIN_TELEMETRY_FILENAME`
- order 129: `ADMIN_AUTH_FILENAME` (constant), lines 3829-3829, exports `ADMIN_AUTH_FILENAME`
- order 139: `ADMIN_MAX_APP_SKILLS` (constant), lines 3876-3876, exports `ADMIN_MAX_APP_SKILLS`
- order 140: `ADMIN_MAX_APP_CAPSULE_CHARS` (constant), lines 3877-3877, exports `ADMIN_MAX_APP_CAPSULE_CHARS`
- order 141: `ADMIN_MAX_APP_RESOURCE_FILES` (constant), lines 3878-3878, exports `ADMIN_MAX_APP_RESOURCE_FILES`
- order 142: `ADMIN_MAX_APP_RESOURCE_BYTES` (constant), lines 3879-3879, exports `ADMIN_MAX_APP_RESOURCE_BYTES`
- order 143: `ADMIN_APP_INLINE_BLOB_BYTES` (constant), lines 3880-3880, exports `ADMIN_APP_INLINE_BLOB_BYTES`
- order 144: `ADMIN_AUTH_SESSION_TTL_SECONDS` (constant), lines 3881-3881, exports `ADMIN_AUTH_SESSION_TTL_SECONDS`
- order 145: `ADMIN_AUTH_PASSWORD_ITERATIONS` (constant), lines 3882-3882, exports `ADMIN_AUTH_PASSWORD_ITERATIONS`
- order 146: `ADMIN_AUTH_MAX_ACTIVE_SESSIONS` (constant), lines 3883-3883, exports `ADMIN_AUTH_MAX_ACTIVE_SESSIONS`
- order 1172: `ADMIN_SKILLS_REVIEW_HTML` (constant), lines 117416-117417, exports `ADMIN_SKILLS_REVIEW_HTML`
- order 1173: `ADMIN_SKILLS_REVIEW_CSS` (constant), lines 117418-117418, exports `ADMIN_SKILLS_REVIEW_CSS`
- order 1174: `ADMIN_SKILLS_REVIEW_JS` (constant), lines 117419-117419, exports `ADMIN_SKILLS_REVIEW_JS`

### `agent/background.py`

- order 1003: `BackgroundManager` (class), lines 23075-23700, exports `BackgroundManager`

### `agent/bus.py`

- order 1004: `MessageBus` (class), lines 23701-23766, exports `MessageBus`

### `agent/errors.py`

- order 853: `CircuitBreakerTriggered` (class), lines 12165-12168, exports `CircuitBreakerTriggered`

### `agent/events.py`

- order 959: `EventHub` (class), lines 16355-16409, exports `EventHub`

### `agent/process.py`

- order 764: `subprocess_text_encodings` (function), lines 8204-8225, exports `subprocess_text_encodings`
- order 765: `decode_subprocess_bytes` (function), lines 8226-8252, exports `decode_subprocess_bytes`
- order 766: `run_subprocess_text` (function), lines 8253-8275, exports `run_subprocess_text`
- order 767: `windows_utf8_shell_command` (function), lines 8276-8282, exports `windows_utf8_shell_command`
- order 768: `shell_process_invocation` (function), lines 8283-8293, exports `shell_process_invocation`
- order 769: `join_shell_task_command` (function), lines 8294-8305, exports `join_shell_task_command`
- order 1002: `UserProcessManager` (class), lines 22715-23074, exports `UserProcessManager`

### `agent/tasks.py`

- order 1000: `TaskManager` (class), lines 22574-22708, exports `TaskManager`

### `agent/todo.py`

- order 960: `TodoManager` (class), lines 16410-16770, exports `TodoManager`

### `agent/tools.py`

- order 954: `_ask_user_option_rows` (function), lines 16234-16267, exports `_ask_user_option_rows`
- order 955: `_ask_user_option_value` (function), lines 16268-16273, exports `_ask_user_option_value`
- order 1028: `tool_def` (function), lines 27888-27901, exports `tool_def`
- order 1029: `TOOLS` (constant), lines 27902-28449, exports `TOOLS`
- order 1030: `TOOL_REQUIRED_ARGS` (constant), lines 28450-28451, exports `TOOL_REQUIRED_ARGS`
- order 1031: `TOOL_SPEC_BY_NAME` (constant), lines 28452-28452, exports `TOOL_SPEC_BY_NAME`
- order 1032: `_for_28453` (statement), lines 28453-28462, exports `_tool`, `_fn`, `_name`, `_required`
- order 1033: `TOOL_NAME_FUZZY_MAP` (constant), lines 28463-28464, exports `TOOL_NAME_FUZZY_MAP`
- order 1034: `_for_28465` (statement), lines 28465-28468, exports `_name`, `_key`
- order 1035: `_for_28470` (statement), lines 28469-28486, exports `_alias`, `_target`
- order 1036: `is_todo_resume_tool_name` (function), lines 28487-28503, exports `is_todo_resume_tool_name`
- order 1037: `canonicalize_tool_name` (function), lines 28504-28522, exports `canonicalize_tool_name`
- order 1038: `filter_tool_specs_for_runtime` (function), lines 28523-28538, exports `filter_tool_specs_for_runtime`
- order 1039: `DEVELOPER_TOOL_DROP` (constant), lines 28539-28549, exports `DEVELOPER_TOOL_DROP`
- order 1040: `AGENT_TOOL_ALLOWLIST` (constant), lines 28550-28613, exports `AGENT_TOOL_ALLOWLIST`

### `agent/worktree.py`

- order 1005: `WorktreeManager` (class), lines 23767-23979, exports `WorktreeManager`

### `app/context.py`

- order 1175: `AppContext` (class), lines 117420-128136, exports `AppContext`

### `app/main.py`

- order 1190: `main` (function), lines 134882-136830, exports `main`
- order 1191: `_main_guard_136832` (main_guard), lines 136831-136833, exports —

### `app/services.py`

- order 1177: `TelemetryStore` (class), lines 128177-128552, exports `TelemetryStore`
- order 1178: `ApplicationRegistry` (class), lines 128553-129362, exports `ApplicationRegistry`

### `collaboration/core.py`

- order 90: `_now` (function), lines 437-440, exports `_now`
- order 91: `_json` (function), lines 441-444, exports `_json`
- order 92: `_load_json` (function), lines 445-451, exports `_load_json`
- order 93: `_b64_token` (function), lines 452-455, exports `_b64_token`
- order 94: `_branch_label` (function), lines 456-464, exports `_branch_label`
- order 95: `_digest` (function), lines 465-468, exports `_digest`
- order 96: `_password_hash` (function), lines 469-472, exports `_password_hash`
- order 97: `_normalize_ip` (function), lines 473-482, exports `_normalize_ip`
- order 98: `_normalize_name` (function), lines 483-489, exports `_normalize_name`
- order 99: `_COLLAB_PUBLIC_SECRET_PATTERNS` (assignment), lines 490-501, exports `_COLLAB_PUBLIC_SECRET_PATTERNS`
- order 100: `_collaboration_public_text` (function), lines 502-532, exports `_collaboration_public_text`
- order 101: `_collaboration_task_objective` (function), lines 533-557, exports `_collaboration_task_objective`
- order 102: `_collaboration_task_title` (function), lines 558-565, exports `_collaboration_task_title`
- order 103: `_collaboration_task_key` (function), lines 566-572, exports `_collaboration_task_key`
- order 104: `_collaboration_plan_steps` (function), lines 573-591, exports `_collaboration_plan_steps`
- order 105: `CollaborationError` (class), lines 592-599, exports `CollaborationError`
- order 106: `CollaborationPrincipal` (class), lines 600-610, exports `CollaborationPrincipal`
- order 107: `_normalize_operation` (function), lines 611-644, exports `_normalize_operation`
- order 108: `operation_input_length` (function), lines 645-648, exports `operation_input_length`
- order 109: `apply_text_operation` (function), lines 649-671, exports `apply_text_operation`
- order 110: `transform_text_operation` (function), lines 672-748, exports `transform_text_operation`
- order 111: `CollaborationStore` (class), lines 749-3464, exports `CollaborationStore`
- order 112: `CollaborationWriteCoordinator` (class), lines 3465-3678, exports `CollaborationWriteCoordinator`

### `collaboration/watcher.py`

- order 1188: `collaboration_file_watcher_loop` (function), lines 134791-134863, exports `collaboration_file_watcher_loop`
- order 1189: `collaboration_watcher_health` (function), lines 134864-134881, exports `collaboration_watcher_health`

### `config/bootstrap.py`

- order 73: `_EMBEDDED_LIQUID_KERNEL_PACKAGE_B64` (assignment), lines 114-366, exports `_EMBEDDED_LIQUID_KERNEL_PACKAGE_B64`
- order 74: `_ensure_embedded_liquid_kernel_package` (function), lines 367-412, exports `_ensure_embedded_liquid_kernel_package`
- order 915: `_liquid_kernel_history_present` (function), lines 14082-14086, exports `_liquid_kernel_history_present`
- order 916: `prepare_liquid_kernel_runtime` (function), lines 14087-14116, exports `prepare_liquid_kernel_runtime`
- order 917: `_persist_liquid_kernel_bootstrap` (function), lines 14117-14130, exports `_persist_liquid_kernel_bootstrap`

### `config/constants.py`

- order 75: `LIQUID_KERNEL_PACKAGE_STATUS` (constant), lines 413-415, exports `LIQUID_KERNEL_PACKAGE_STATUS`
- order 77: `COLLAB_DB_FILENAME` (constant), lines 422-424, exports `COLLAB_DB_FILENAME`
- order 78: `COLLAB_SESSION_TTL_SECONDS` (constant), lines 425-425, exports `COLLAB_SESSION_TTL_SECONDS`
- order 79: `COLLAB_PRESENCE_TTL_SECONDS` (constant), lines 426-426, exports `COLLAB_PRESENCE_TTL_SECONDS`
- order 80: `COLLAB_PASSWORD_ITERATIONS` (constant), lines 427-427, exports `COLLAB_PASSWORD_ITERATIONS`
- order 81: `COLLAB_MAX_AVATAR_BYTES` (constant), lines 428-428, exports `COLLAB_MAX_AVATAR_BYTES`
- order 82: `COLLAB_MAX_TEXT_BYTES` (constant), lines 429-429, exports `COLLAB_MAX_TEXT_BYTES`
- order 83: `COLLAB_DELETE_RETENTION_DAYS` (constant), lines 430-430, exports `COLLAB_DELETE_RETENTION_DAYS`
- order 84: `COLLAB_EVENT_RETENTION` (constant), lines 431-431, exports `COLLAB_EVENT_RETENTION`
- order 85: `COLLAB_AGENT_STALE_SECONDS` (constant), lines 432-432, exports `COLLAB_AGENT_STALE_SECONDS`
- order 86: `COLLAB_AGENT_HEARTBEAT_INTERVAL_SECONDS` (constant), lines 433-433, exports `COLLAB_AGENT_HEARTBEAT_INTERVAL_SECONDS`
- order 87: `COLLAB_EXTERNAL_WRITE_SETTLE_SECONDS` (constant), lines 434-434, exports `COLLAB_EXTERNAL_WRITE_SETTLE_SECONDS`
- order 88: `COLLAB_EXTERNAL_WRITE_CONFIRMATIONS` (constant), lines 435-435, exports `COLLAB_EXTERNAL_WRITE_CONFIRMATIONS`
- order 89: `COLLAB_SCHEMA_VERSION` (constant), lines 436-436, exports `COLLAB_SCHEMA_VERSION`
- order 113: `COLLAB_INDEX_HTML` (constant), lines 3679-3750, exports `COLLAB_INDEX_HTML`
- order 114: `COLLAB_CSS` (constant), lines 3751-3758, exports `COLLAB_CSS`
- order 115: `COLLAB_JS` (constant), lines 3759-3799, exports `COLLAB_JS`
- order 121: `APP_VERSION` (constant), lines 3821-3821, exports `APP_VERSION`
- order 130: `IDE_AUTH_FILENAME` (constant), lines 3830-3830, exports `IDE_AUTH_FILENAME`
- order 131: `IDE_AUTH_SESSION_TTL_SECONDS` (constant), lines 3831-3831, exports `IDE_AUTH_SESSION_TTL_SECONDS`
- order 132: `IDE_AUTH_MAX_ACTIVE_SESSIONS` (constant), lines 3832-3832, exports `IDE_AUTH_MAX_ACTIVE_SESSIONS`
- order 133: `IDE_DEVICE_SECRET_MIN_BYTES` (constant), lines 3833-3833, exports `IDE_DEVICE_SECRET_MIN_BYTES`
- order 134: `IDE_DEVICE_LABEL_MAX_CHARS` (constant), lines 3834-3834, exports `IDE_DEVICE_LABEL_MAX_CHARS`
- order 135: `IDE_DEVICE_PAIRING_TTL_SECONDS` (constant), lines 3835-3835, exports `IDE_DEVICE_PAIRING_TTL_SECONDS`
- order 136: `IDE_WORKBENCH_STATE_FILENAME` (constant), lines 3836-3836, exports `IDE_WORKBENCH_STATE_FILENAME`
- order 137: `IDE_PROMPT_ENHANCEMENT_BUDGETS` (constant), lines 3837-3874, exports `IDE_PROMPT_ENHANCEMENT_BUDGETS`
- order 138: `IDE_EXTENSIONS_DIRNAME` (constant), lines 3875-3875, exports `IDE_EXTENSIONS_DIRNAME`
- order 160: `LONG_OUTPUT_MODEL_PAGE_CHARS` (constant), lines 4178-4178, exports `LONG_OUTPUT_MODEL_PAGE_CHARS`
- order 161: `LONG_OUTPUT_UI_PAGE_CHARS` (constant), lines 4179-4179, exports `LONG_OUTPUT_UI_PAGE_CHARS`
- order 162: `LONG_OUTPUT_UI_PREVIEW_MAX_PAGES` (constant), lines 4180-4180, exports `LONG_OUTPUT_UI_PREVIEW_MAX_PAGES`
- order 163: `LONG_OUTPUT_LISTING_OFFLOAD_CHARS` (constant), lines 4181-4181, exports `LONG_OUTPUT_LISTING_OFFLOAD_CHARS`
- order 164: `LONG_OUTPUT_READ_PAGE_LINES` (constant), lines 4182-4182, exports `LONG_OUTPUT_READ_PAGE_LINES`
- order 165: `LONG_OUTPUT_READ_PAGE_MAX_CHARS` (constant), lines 4183-4183, exports `LONG_OUTPUT_READ_PAGE_MAX_CHARS`
- order 166: `LONG_OUTPUT_TEMP_MAX_FILES` (constant), lines 4184-4184, exports `LONG_OUTPUT_TEMP_MAX_FILES`
- order 167: `READ_FILE_DEFAULT_MAX_CHARS` (constant), lines 4185-4185, exports `READ_FILE_DEFAULT_MAX_CHARS`
- order 168: `READ_FILE_HARD_MAX_CHARS` (constant), lines 4186-4186, exports `READ_FILE_HARD_MAX_CHARS`
- order 169: `READ_FILE_OVERVIEW_HEAD_LINES` (constant), lines 4187-4187, exports `READ_FILE_OVERVIEW_HEAD_LINES`
- order 170: `READ_FILE_SEARCH_MAX_MATCHES` (constant), lines 4188-4188, exports `READ_FILE_SEARCH_MAX_MATCHES`
- order 175: `CODE_ADMIN_PORT_OFFSET` (constant), lines 4193-4193, exports `CODE_ADMIN_PORT_OFFSET`
- order 177: `IDE_PORT_OFFSET` (constant), lines 4195-4198, exports `IDE_PORT_OFFSET`
- order 178: `IDE_DEFAULT_PORT` (constant), lines 4199-4199, exports `IDE_DEFAULT_PORT`
- order 179: `COLLAB_PORT_OFFSET` (constant), lines 4200-4200, exports `COLLAB_PORT_OFFSET`
- order 181: `DEFAULT_WEB_SEARCH_ENABLED` (constant), lines 4202-4202, exports `DEFAULT_WEB_SEARCH_ENABLED`
- order 186: `DEFAULT_USER_MEMORY_MODE` (constant), lines 4207-4207, exports `DEFAULT_USER_MEMORY_MODE`
- order 194: `AGENT_WEB_SEARCH_USER_AGENT` (constant), lines 4218-4218, exports `AGENT_WEB_SEARCH_USER_AGENT`
- order 195: `AGENT_WEB_SEARCH_DEFAULT_MAX_RESULTS` (constant), lines 4219-4219, exports `AGENT_WEB_SEARCH_DEFAULT_MAX_RESULTS`
- order 196: `AGENT_WEB_SEARCH_DEFAULT_MAX_PAGES` (constant), lines 4220-4220, exports `AGENT_WEB_SEARCH_DEFAULT_MAX_PAGES`
- order 197: `AGENT_WEB_SEARCH_HARD_MAX_PAGES` (constant), lines 4221-4221, exports `AGENT_WEB_SEARCH_HARD_MAX_PAGES`
- order 198: `AGENT_WEB_SEARCH_DEFAULT_DEPTH` (constant), lines 4222-4222, exports `AGENT_WEB_SEARCH_DEFAULT_DEPTH`
- order 199: `AGENT_WEB_SEARCH_HARD_DEPTH` (constant), lines 4223-4223, exports `AGENT_WEB_SEARCH_HARD_DEPTH`
- order 200: `AGENT_WEB_SEARCH_FETCH_TIMEOUT` (constant), lines 4224-4224, exports `AGENT_WEB_SEARCH_FETCH_TIMEOUT`
- order 201: `AGENT_WEB_SEARCH_TOOL_SOFT_TIMEOUT` (constant), lines 4225-4225, exports `AGENT_WEB_SEARCH_TOOL_SOFT_TIMEOUT`
- order 202: `AGENT_WEB_SEARCH_MAX_PAGE_BYTES` (constant), lines 4226-4226, exports `AGENT_WEB_SEARCH_MAX_PAGE_BYTES`
- order 203: `AGENT_WEB_SEARCH_MAX_TEXT_CHARS` (constant), lines 4227-4227, exports `AGENT_WEB_SEARCH_MAX_TEXT_CHARS`
- order 204: `AGENT_WEB_SEARCH_PUBLIC_DISCOVERY_ENABLED` (constant), lines 4228-4230, exports `AGENT_WEB_SEARCH_PUBLIC_DISCOVERY_ENABLED`
- order 205: `AGENT_WEB_SEARCH_PUBLIC_FEED_URL` (constant), lines 4231-4231, exports `AGENT_WEB_SEARCH_PUBLIC_FEED_URL`
- order 206: `AGENT_WEB_SEARCH_PUBLIC_FEED_MAX_BYTES` (constant), lines 4232-4232, exports `AGENT_WEB_SEARCH_PUBLIC_FEED_MAX_BYTES`
- order 207: `AGENT_WEB_SEARCH_LOCAL_GRAPH_MAX_NODES` (constant), lines 4233-4233, exports `AGENT_WEB_SEARCH_LOCAL_GRAPH_MAX_NODES`
- order 208: `AGENT_WEB_SEARCH_LOCAL_GRAPH_MAX_EDGES` (constant), lines 4234-4234, exports `AGENT_WEB_SEARCH_LOCAL_GRAPH_MAX_EDGES`
- order 209: `AGENT_WEB_SEARCH_LOCAL_GRAPH_EDGE_SCAN_MULTIPLIER` (constant), lines 4235-4235, exports `AGENT_WEB_SEARCH_LOCAL_GRAPH_EDGE_SCAN_MULTIPLIER`
- order 210: `AGENT_WEB_SEARCH_LOCAL_GRAPH_PAGERANK_ITERATIONS` (constant), lines 4236-4236, exports `AGENT_WEB_SEARCH_LOCAL_GRAPH_PAGERANK_ITERATIONS`
- order 211: `AGENT_WEB_SEARCH_LOCAL_GRAPH_PAGERANK_DAMPING` (constant), lines 4237-4237, exports `AGENT_WEB_SEARCH_LOCAL_GRAPH_PAGERANK_DAMPING`
- order 212: `AGENT_WEB_SEARCH_LOCAL_GRAPH_AUTHORITY_BONUS_MAX` (constant), lines 4238-4238, exports `AGENT_WEB_SEARCH_LOCAL_GRAPH_AUTHORITY_BONUS_MAX`
- order 222: `CODE_CHUNK_CHARS` (constant), lines 4260-4260, exports `CODE_CHUNK_CHARS`
- order 223: `CODE_CHUNK_OVERLAP` (constant), lines 4261-4261, exports `CODE_CHUNK_OVERLAP`
- order 224: `CODE_MAX_CHUNKS_PER_DOC` (constant), lines 4262-4262, exports `CODE_MAX_CHUNKS_PER_DOC`
- order 225: `CODE_SOURCE_ANALYSIS_MAX_CHARS` (constant), lines 4263-4272, exports `CODE_SOURCE_ANALYSIS_MAX_CHARS`
- order 266: `CODE_IMPORT_WORKER_COUNT` (constant), lines 4341-4344, exports `CODE_IMPORT_WORKER_COUNT`
- order 268: `CODE_PARSE_TIMEOUT_SECONDS` (constant), lines 4349-4352, exports `CODE_PARSE_TIMEOUT_SECONDS`
- order 269: `DEFAULT_CONTEXT_TOKEN_LIMIT` (constant), lines 4353-4353, exports `DEFAULT_CONTEXT_TOKEN_LIMIT`
- order 270: `TOKEN_THRESHOLD` (constant), lines 4354-4354, exports `TOKEN_THRESHOLD`
- order 271: `CONTEXT_AUTO_COMPACT_RESERVE_RATIO` (constant), lines 4355-4358, exports `CONTEXT_AUTO_COMPACT_RESERVE_RATIO`
- order 272: `CONTEXT_ESTIMATE_SAFETY_MULTIPLIER` (constant), lines 4359-4362, exports `CONTEXT_ESTIMATE_SAFETY_MULTIPLIER`
- order 273: `CONTEXT_USAGE_CALIBRATION_MAX` (constant), lines 4363-4366, exports `CONTEXT_USAGE_CALIBRATION_MAX`
- order 274: `CONTEXT_ACTUAL_USAGE_RECENT_SECONDS` (constant), lines 4367-4370, exports `CONTEXT_ACTUAL_USAGE_RECENT_SECONDS`
- order 275: `LARGE_FILE_AUTO_PAGE_BYTES` (constant), lines 4371-4374, exports `LARGE_FILE_AUTO_PAGE_BYTES`
- order 276: `LARGE_FILE_AUTO_PAGE_LINES` (constant), lines 4375-4378, exports `LARGE_FILE_AUTO_PAGE_LINES`
- order 277: `LARGE_SOURCE_UPLOAD_EXCERPT_CHARS` (constant), lines 4379-4382, exports `LARGE_SOURCE_UPLOAD_EXCERPT_CHARS`
- order 278: `CHAT_UPLOAD_PARSE_QUEUE_MAX` (constant), lines 4383-4386, exports `CHAT_UPLOAD_PARSE_QUEUE_MAX`
- order 279: `CHAT_UPLOAD_PARSE_TIMEOUT_SECONDS` (constant), lines 4387-4390, exports `CHAT_UPLOAD_PARSE_TIMEOUT_SECONDS`
- order 280: `CHAT_UPLOAD_INLINE_TEXT_BYTES` (constant), lines 4391-4394, exports `CHAT_UPLOAD_INLINE_TEXT_BYTES`
- order 281: `CHAT_UPLOAD_PARSE_MAX_BYTES` (constant), lines 4395-4401, exports `CHAT_UPLOAD_PARSE_MAX_BYTES`
- order 282: `CHAT_UPLOAD_ZIP_ENTRY_MAX_BYTES` (constant), lines 4402-4408, exports `CHAT_UPLOAD_ZIP_ENTRY_MAX_BYTES`
- order 283: `CHAT_UPLOAD_TEXT_CONTEXT_CHARS` (constant), lines 4409-4412, exports `CHAT_UPLOAD_TEXT_CONTEXT_CHARS`
- order 284: `CHAT_UPLOAD_PROMPT_MAX_FILES` (constant), lines 4413-4416, exports `CHAT_UPLOAD_PROMPT_MAX_FILES`
- order 285: `CHAT_UPLOAD_PROMPT_MAX_CHARS` (constant), lines 4417-4420, exports `CHAT_UPLOAD_PROMPT_MAX_CHARS`
- order 286: `CHAT_UPLOAD_PROMPT_PER_FILE_CHARS` (constant), lines 4421-4424, exports `CHAT_UPLOAD_PROMPT_PER_FILE_CHARS`
- order 287: `CHAT_UPLOAD_FRONTEND_WAIT_MS` (constant), lines 4425-4428, exports `CHAT_UPLOAD_FRONTEND_WAIT_MS`
- order 288: `CHAT_UPLOAD_AUTO_LIBRARY_INGEST` (constant), lines 4429-4432, exports `CHAT_UPLOAD_AUTO_LIBRARY_INGEST`
- order 289: `CHAT_UPLOAD_INGEST_QUEUE_MAX` (constant), lines 4433-4436, exports `CHAT_UPLOAD_INGEST_QUEUE_MAX`
- order 290: `SESSION_SUBMIT_LOCK_TIMEOUT_SECONDS` (constant), lines 4437-4440, exports `SESSION_SUBMIT_LOCK_TIMEOUT_SECONDS`
- order 291: `SESSION_DEFERRED_START_QUEUE_MAX` (constant), lines 4441-4444, exports `SESSION_DEFERRED_START_QUEUE_MAX`
- order 292: `SESSION_SUBMISSION_DEDUPE_MAX` (constant), lines 4445-4445, exports `SESSION_SUBMISSION_DEDUPE_MAX`
- order 293: `SESSION_SUBMISSION_DEDUPE_SECONDS` (constant), lines 4446-4446, exports `SESSION_SUBMISSION_DEDUPE_SECONDS`
- order 294: `SCHEDULER_SUBMISSION_DEDUPE_MAX` (constant), lines 4447-4447, exports `SCHEDULER_SUBMISSION_DEDUPE_MAX`
- order 295: `FAST_START_LOCAL_CLASSIFICATION` (constant), lines 4448-4450, exports `FAST_START_LOCAL_CLASSIFICATION`
- order 296: `FAST_START_LOCAL_TITLE` (constant), lines 4451-4453, exports `FAST_START_LOCAL_TITLE`
- order 297: `AUTO_TITLE_MODEL_REFINE` (constant), lines 4454-4456, exports `AUTO_TITLE_MODEL_REFINE`
- order 298: `AUTO_TITLE_MODEL_TIMEOUT_SECONDS` (constant), lines 4457-4460, exports `AUTO_TITLE_MODEL_TIMEOUT_SECONDS`
- order 299: `AUTO_TITLE_MODEL_RETRY_COOLDOWN_SECONDS` (constant), lines 4461-4467, exports `AUTO_TITLE_MODEL_RETRY_COOLDOWN_SECONDS`
- order 300: `FAST_START_DEFER_CAPABILITY_PROBE` (constant), lines 4468-4470, exports `FAST_START_DEFER_CAPABILITY_PROBE`
- order 301: `SESSION_RUNTIME_MESSAGE_WINDOW` (constant), lines 4471-4471, exports `SESSION_RUNTIME_MESSAGE_WINDOW`
- order 302: `SESSION_RUNTIME_ACTIVITY_WINDOW` (constant), lines 4472-4472, exports `SESSION_RUNTIME_ACTIVITY_WINDOW`
- order 303: `SESSION_RUNTIME_OPERATION_WINDOW` (constant), lines 4473-4473, exports `SESSION_RUNTIME_OPERATION_WINDOW`
- order 304: `SESSION_RUNTIME_UPLOAD_WINDOW` (constant), lines 4474-4474, exports `SESSION_RUNTIME_UPLOAD_WINDOW`
- order 305: `LITE_SNAPSHOT_MAX_BYTES` (constant), lines 4475-4478, exports `LITE_SNAPSHOT_MAX_BYTES`
- order 306: `LITE_SNAPSHOT_MESSAGES_BYTES` (constant), lines 4479-4479, exports `LITE_SNAPSHOT_MESSAGES_BYTES`
- order 307: `LITE_SNAPSHOT_FEED_BYTES` (constant), lines 4480-4480, exports `LITE_SNAPSHOT_FEED_BYTES`
- order 308: `LITE_SNAPSHOT_OPERATIONS_BYTES` (constant), lines 4481-4481, exports `LITE_SNAPSHOT_OPERATIONS_BYTES`
- order 309: `IDE_AGENT_STATE_MAX_BYTES` (constant), lines 4482-4485, exports `IDE_AGENT_STATE_MAX_BYTES`
- order 310: `IDE_AGENT_FEED_BYTES` (constant), lines 4486-4486, exports `IDE_AGENT_FEED_BYTES`
- order 311: `IDE_AGENT_OPERATIONS_BYTES` (constant), lines 4487-4487, exports `IDE_AGENT_OPERATIONS_BYTES`
- order 312: `SESSION_WATCHDOG_INTERVAL_SECONDS` (constant), lines 4488-4491, exports `SESSION_WATCHDOG_INTERVAL_SECONDS`
- order 313: `SESSION_HEARTBEAT_STALE_SECONDS` (constant), lines 4492-4495, exports `SESSION_HEARTBEAT_STALE_SECONDS`
- order 314: `SESSION_LIST_DEFAULT_LIMIT` (constant), lines 4496-4499, exports `SESSION_LIST_DEFAULT_LIMIT`
- order 315: `SESSION_INDEX_SYNC_SNAPSHOT_MAX` (constant), lines 4500-4503, exports `SESSION_INDEX_SYNC_SNAPSHOT_MAX`
- order 316: `SESSION_INDEX_JOURNAL_COMPACT_RECORDS` (constant), lines 4504-4507, exports `SESSION_INDEX_JOURNAL_COMPACT_RECORDS`
- order 317: `SESSION_INDEX_JOURNAL_COMPACT_BYTES` (constant), lines 4508-4511, exports `SESSION_INDEX_JOURNAL_COMPACT_BYTES`
- order 318: `SESSION_CATALOG_RECENT_MAX` (constant), lines 4512-4515, exports `SESSION_CATALOG_RECENT_MAX`
- order 319: `IDE_SESSION_LIST_DEFAULT_LIMIT` (constant), lines 4516-4519, exports `IDE_SESSION_LIST_DEFAULT_LIMIT`
- order 320: `IDLE_TIMEOUT` (constant), lines 4520-4520, exports `IDLE_TIMEOUT`
- order 321: `POLL_INTERVAL` (constant), lines 4521-4521, exports `POLL_INTERVAL`
- order 322: `SSE_HEARTBEAT_SECONDS` (constant), lines 4522-4522, exports `SSE_HEARTBEAT_SECONDS`
- order 323: `MODEL_CALL_PROGRESS_DELAY` (constant), lines 4523-4523, exports `MODEL_CALL_PROGRESS_DELAY`
- order 324: `MODEL_CALL_PROGRESS_INTERVAL` (constant), lines 4524-4524, exports `MODEL_CALL_PROGRESS_INTERVAL`
- order 325: `RUN_COMPLETION_SUMMARY_ENABLED` (constant), lines 4525-4528, exports `RUN_COMPLETION_SUMMARY_ENABLED`
- order 326: `LLM_HTTP_RETRY_MAX_ATTEMPTS` (constant), lines 4529-4532, exports `LLM_HTTP_RETRY_MAX_ATTEMPTS`
- order 327: `LLM_HTTP_RETRY_DELAY_SECONDS` (constant), lines 4533-4536, exports `LLM_HTTP_RETRY_DELAY_SECONDS`
- order 328: `LLM_HTTP_RETRY_MAX_SECONDS` (constant), lines 4537-4540, exports `LLM_HTTP_RETRY_MAX_SECONDS`
- order 329: `LLM_HTTP_RETRY_404_ON_VLLM` (constant), lines 4541-4544, exports `LLM_HTTP_RETRY_404_ON_VLLM`
- order 330: `LLM_HTTP_RETRY_STATUSES` (constant), lines 4545-4545, exports `LLM_HTTP_RETRY_STATUSES`
- order 331: `MAX_AGENT_ROUNDS` (constant), lines 4546-4546, exports `MAX_AGENT_ROUNDS`
- order 332: `MIN_AGENT_ROUNDS` (constant), lines 4547-4547, exports `MIN_AGENT_ROUNDS`
- order 333: `MAX_AGENT_ROUNDS_CAP` (constant), lines 4548-4548, exports `MAX_AGENT_ROUNDS_CAP`
- order 334: `REPEATED_TOOL_LOOP_THRESHOLD` (constant), lines 4549-4549, exports `REPEATED_TOOL_LOOP_THRESHOLD`
- order 335: `BASH_READ_LOOP_THRESHOLD` (constant), lines 4550-4550, exports `BASH_READ_LOOP_THRESHOLD`
- order 336: `READ_FILE_LOOP_THRESHOLD` (constant), lines 4551-4551, exports `READ_FILE_LOOP_THRESHOLD`
- order 337: `READ_FILE_LOOP_DISTINCT_SOFT_LIMIT` (constant), lines 4552-4552, exports `READ_FILE_LOOP_DISTINCT_SOFT_LIMIT`
- order 338: `READ_FILE_COMPACT_PIN_DISTINCT` (constant), lines 4553-4553, exports `READ_FILE_COMPACT_PIN_DISTINCT`
- order 339: `READ_FILE_COMPACT_PIN_MAX_CHARS` (constant), lines 4554-4554, exports `READ_FILE_COMPACT_PIN_MAX_CHARS`
- order 340: `READ_CONTEXT_REGISTRY_MAX` (constant), lines 4555-4555, exports `READ_CONTEXT_REGISTRY_MAX`
- order 341: `READ_CONTEXT_PROMPT_MAX_ITEMS` (constant), lines 4556-4556, exports `READ_CONTEXT_PROMPT_MAX_ITEMS`
- order 342: `READ_CONTEXT_PROMPT_MAX_CHARS` (constant), lines 4557-4557, exports `READ_CONTEXT_PROMPT_MAX_CHARS`
- order 343: `READ_CONTEXT_SUMMARY_MAX_CHARS` (constant), lines 4558-4558, exports `READ_CONTEXT_SUMMARY_MAX_CHARS`
- order 344: `READ_CONTEXT_SHARED_MAX_ITEMS` (constant), lines 4559-4559, exports `READ_CONTEXT_SHARED_MAX_ITEMS`
- order 345: `READ_CONTEXT_POLICY_CHOICES` (constant), lines 4560-4560, exports `READ_CONTEXT_POLICY_CHOICES`
- order 346: `DEFAULT_READ_CONTEXT_POLICY` (constant), lines 4561-4561, exports `DEFAULT_READ_CONTEXT_POLICY`
- order 347: `READ_CONTEXT_CACHE_SEARCH_MAX_BYTES` (constant), lines 4562-4568, exports `READ_CONTEXT_CACHE_SEARCH_MAX_BYTES`
- order 348: `READ_CONTEXT_CACHE_SEARCH_MAX_MATCHES` (constant), lines 4569-4569, exports `READ_CONTEXT_CACHE_SEARCH_MAX_MATCHES`
- order 349: `READ_CONTEXT_CACHE_SNIPPET_CHARS` (constant), lines 4570-4570, exports `READ_CONTEXT_CACHE_SNIPPET_CHARS`
- order 350: `READ_CONTEXT_CACHE_LINE_CONTEXT` (constant), lines 4571-4571, exports `READ_CONTEXT_CACHE_LINE_CONTEXT`
- order 351: `LONG_CONTENT_SOURCE_CACHE_MAX_BYTES` (constant), lines 4572-4578, exports `LONG_CONTENT_SOURCE_CACHE_MAX_BYTES`
- order 352: `LONG_CONTENT_SOURCE_CACHE_MAX_FILES` (constant), lines 4579-4582, exports `LONG_CONTENT_SOURCE_CACHE_MAX_FILES`
- order 353: `LONG_CONTENT_SYMBOL_MEMORY_MAX` (constant), lines 4583-4586, exports `LONG_CONTENT_SYMBOL_MEMORY_MAX`
- order 354: `TOOL_MEMORY_REGISTRY_MAX` (constant), lines 4587-4587, exports `TOOL_MEMORY_REGISTRY_MAX`
- order 355: `TOOL_MEMORY_PROMPT_MAX_ITEMS` (constant), lines 4588-4588, exports `TOOL_MEMORY_PROMPT_MAX_ITEMS`
- order 356: `TOOL_MEMORY_PROMPT_MAX_CHARS` (constant), lines 4589-4589, exports `TOOL_MEMORY_PROMPT_MAX_CHARS`
- order 357: `TOOL_MEMORY_SUMMARY_MAX_CHARS` (constant), lines 4590-4590, exports `TOOL_MEMORY_SUMMARY_MAX_CHARS`
- order 358: `TOOL_MEMORY_SHARED_MAX_ITEMS` (constant), lines 4591-4591, exports `TOOL_MEMORY_SHARED_MAX_ITEMS`
- order 359: `TOOL_MEMORY_COMPACT_PIN_DISTINCT` (constant), lines 4592-4592, exports `TOOL_MEMORY_COMPACT_PIN_DISTINCT`
- order 360: `TOOL_MEMORY_COMPACT_PIN_MAX_CHARS` (constant), lines 4593-4593, exports `TOOL_MEMORY_COMPACT_PIN_MAX_CHARS`
- order 361: `TOOL_MEMORY_POLICY_CHOICES` (constant), lines 4594-4594, exports `TOOL_MEMORY_POLICY_CHOICES`
- order 362: `DEFAULT_TOOL_MEMORY_POLICY` (constant), lines 4595-4595, exports `DEFAULT_TOOL_MEMORY_POLICY`
- order 363: `LONG_CONTENT_MEMORY_VERSION` (constant), lines 4596-4608, exports `LONG_CONTENT_MEMORY_VERSION`
- order 364: `LONG_CONTENT_MEMORY_MAX_ITEMS` (constant), lines 4609-4612, exports `LONG_CONTENT_MEMORY_MAX_ITEMS`
- order 365: `LONG_CONTENT_MEMORY_MAX_SEGMENTS` (constant), lines 4613-4616, exports `LONG_CONTENT_MEMORY_MAX_SEGMENTS`
- order 366: `LONG_CONTENT_TEXT_SEGMENT_LINES` (constant), lines 4617-4620, exports `LONG_CONTENT_TEXT_SEGMENT_LINES`
- order 367: `LONG_CONTENT_CODE_SEGMENT_LINES` (constant), lines 4621-4624, exports `LONG_CONTENT_CODE_SEGMENT_LINES`
- order 368: `LONG_CONTENT_CARD_CHARS` (constant), lines 4625-4628, exports `LONG_CONTENT_CARD_CHARS`
- order 369: `LONG_CONTENT_STRUCTURE_MAX_CHARS` (constant), lines 4629-4632, exports `LONG_CONTENT_STRUCTURE_MAX_CHARS`
- order 370: `LONG_CONTENT_SEMANTIC_ENABLED` (constant), lines 4633-4640, exports `LONG_CONTENT_SEMANTIC_ENABLED`
- order 371: `LONG_CONTENT_SEMANTIC_TIMEOUT_SECONDS` (constant), lines 4641-4644, exports `LONG_CONTENT_SEMANTIC_TIMEOUT_SECONDS`
- order 372: `LONG_CONTENT_SEMANTIC_MAX_INPUT_CHARS` (constant), lines 4645-4648, exports `LONG_CONTENT_SEMANTIC_MAX_INPUT_CHARS`
- order 373: `LONG_CONTENT_SEMANTIC_MAX_OUTPUT_TOKENS` (constant), lines 4649-4652, exports `LONG_CONTENT_SEMANTIC_MAX_OUTPUT_TOKENS`
- order 374: `LONG_CONTENT_SEMANTIC_MAX_KEY_POINTS` (constant), lines 4653-4653, exports `LONG_CONTENT_SEMANTIC_MAX_KEY_POINTS`
- order 375: `LONG_CONTENT_SEMANTIC_MAX_DEFINITIONS` (constant), lines 4654-4654, exports `LONG_CONTENT_SEMANTIC_MAX_DEFINITIONS`
- order 376: `LONG_CONTENT_SEMANTIC_MAX_RELATIONS` (constant), lines 4655-4655, exports `LONG_CONTENT_SEMANTIC_MAX_RELATIONS`
- order 377: `LONG_CONTENT_SEMANTIC_MAX_UNCERTAINTIES` (constant), lines 4656-4656, exports `LONG_CONTENT_SEMANTIC_MAX_UNCERTAINTIES`
- order 378: `LONG_CONTENT_SEMANTIC_MAX_EVIDENCE` (constant), lines 4657-4657, exports `LONG_CONTENT_SEMANTIC_MAX_EVIDENCE`
- order 379: `LONG_CONTENT_SEMANTIC_MAX_NEXT_SEGMENTS` (constant), lines 4658-4658, exports `LONG_CONTENT_SEMANTIC_MAX_NEXT_SEGMENTS`
- order 380: `LONG_CONTENT_SEMANTIC_MAX_COVERED` (constant), lines 4659-4659, exports `LONG_CONTENT_SEMANTIC_MAX_COVERED`
- order 381: `LONG_CONTENT_SEMANTIC_MAX_OPEN_QUESTIONS` (constant), lines 4660-4660, exports `LONG_CONTENT_SEMANTIC_MAX_OPEN_QUESTIONS`
- order 382: `LONG_CONTENT_SEMANTIC_MAX_REFRESHES` (constant), lines 4661-4664, exports `LONG_CONTENT_SEMANTIC_MAX_REFRESHES`
- order 383: `LONG_CONTENT_OBSERVATION_MAX` (constant), lines 4665-4668, exports `LONG_CONTENT_OBSERVATION_MAX`
- order 384: `LONG_CONTENT_OBSERVATION_MAX_RANGES` (constant), lines 4669-4669, exports `LONG_CONTENT_OBSERVATION_MAX_RANGES`
- order 385: `LONG_CONTENT_OBSERVATION_MAX_EXCERPTS` (constant), lines 4670-4670, exports `LONG_CONTENT_OBSERVATION_MAX_EXCERPTS`
- order 386: `LONG_CONTENT_OBSERVATION_EXCERPT_CHARS` (constant), lines 4671-4671, exports `LONG_CONTENT_OBSERVATION_EXCERPT_CHARS`
- order 387: `LONG_CONTENT_RELATED_SOURCE_MAX` (constant), lines 4672-4672, exports `LONG_CONTENT_RELATED_SOURCE_MAX`
- order 388: `SHELL_SOURCE_CANDIDATE_MAX` (constant), lines 4673-4673, exports `SHELL_SOURCE_CANDIDATE_MAX`
- order 389: `LONG_CONTENT_TEXT_EXTS` (constant), lines 4674-4676, exports `LONG_CONTENT_TEXT_EXTS`
- order 390: `LONG_CONTENT_DATA_EXTS` (constant), lines 4677-4681, exports `LONG_CONTENT_DATA_EXTS`
- order 391: `DEFAULT_AUTO_TASK_LEVEL_CEILING` (constant), lines 4682-4682, exports `DEFAULT_AUTO_TASK_LEVEL_CEILING`
- order 392: `HARD_BREAK_TOOL_ERROR_THRESHOLD` (constant), lines 4683-4683, exports `HARD_BREAK_TOOL_ERROR_THRESHOLD`
- order 393: `HARD_BREAK_RECOVERY_ROUND_THRESHOLD` (constant), lines 4684-4686, exports `HARD_BREAK_RECOVERY_ROUND_THRESHOLD`
- order 394: `FUSED_FAULT_BREAK_THRESHOLD` (constant), lines 4687-4687, exports `FUSED_FAULT_BREAK_THRESHOLD`
- order 395: `STALL_SEVERITY_ESCALATION_THRESHOLD` (constant), lines 4688-4688, exports `STALL_SEVERITY_ESCALATION_THRESHOLD`
- order 396: `STALL_SEVERITY_WEIGHT_BASH_READ_LOOP` (constant), lines 4689-4689, exports `STALL_SEVERITY_WEIGHT_BASH_READ_LOOP`
- order 397: `STALL_SEVERITY_WEIGHT_REPEATED_TOOL` (constant), lines 4690-4690, exports `STALL_SEVERITY_WEIGHT_REPEATED_TOOL`
- order 398: `STALL_SEVERITY_WEIGHT_FAULT` (constant), lines 4691-4691, exports `STALL_SEVERITY_WEIGHT_FAULT`
- order 399: `STALL_SEVERITY_WEIGHT_RECOVERY_RETRY` (constant), lines 4692-4692, exports `STALL_SEVERITY_WEIGHT_RECOVERY_RETRY`
- order 400: `STALL_SEVERITY_WEIGHT_WATCHDOG` (constant), lines 4693-4693, exports `STALL_SEVERITY_WEIGHT_WATCHDOG`
- order 401: `STALL_SEVERITY_DECAY_ON_SUCCESS` (constant), lines 4694-4694, exports `STALL_SEVERITY_DECAY_ON_SUCCESS`
- order 402: `STALL_ESCALATION_MIN_LEVEL` (constant), lines 4695-4695, exports `STALL_ESCALATION_MIN_LEVEL`
- order 403: `STALL_PLAN_SYNTHESIS_MAX_TOKENS` (constant), lines 4696-4696, exports `STALL_PLAN_SYNTHESIS_MAX_TOKENS`
- order 404: `STALL_ESCALATION_CONTEXT_MAX_CHARS` (constant), lines 4697-4697, exports `STALL_ESCALATION_CONTEXT_MAX_CHARS`
- order 405: `MAX_RUN_SECONDS` (constant), lines 4698-4698, exports `MAX_RUN_SECONDS`
- order 406: `MIN_RUN_TIMEOUT_SECONDS` (constant), lines 4699-4699, exports `MIN_RUN_TIMEOUT_SECONDS`
- order 407: `MAX_RUN_TIMEOUT_SECONDS` (constant), lines 4700-4700, exports `MAX_RUN_TIMEOUT_SECONDS`
- order 408: `MIN_TIMEOUT_SECONDS` (constant), lines 4701-4701, exports `MIN_TIMEOUT_SECONDS`
- order 409: `MAX_TIMEOUT_SECONDS` (constant), lines 4702-4702, exports `MAX_TIMEOUT_SECONDS`
- order 410: `DEFAULT_TIMEOUT_SECONDS` (constant), lines 4703-4709, exports `DEFAULT_TIMEOUT_SECONDS`
- order 411: `DEFAULT_REQUEST_TIMEOUT` (constant), lines 4710-4710, exports `DEFAULT_REQUEST_TIMEOUT`
- order 412: `_SHELL_AUTO_CONFIRM_PATTERNS` (assignment), lines 4711-4726, exports `_SHELL_AUTO_CONFIRM_PATTERNS`
- order 413: `MIN_SHELL_COMMAND_TIMEOUT_SECONDS` (constant), lines 4727-4727, exports `MIN_SHELL_COMMAND_TIMEOUT_SECONDS`
- order 414: `MAX_SHELL_COMMAND_TIMEOUT_SECONDS` (constant), lines 4728-4728, exports `MAX_SHELL_COMMAND_TIMEOUT_SECONDS`
- order 415: `SHELL_TIMEOUT_MODES` (constant), lines 4729-4729, exports `SHELL_TIMEOUT_MODES`
- order 416: `_DEFAULT_SHELL_TIMEOUT_MODE_RAW` (assignment), lines 4730-4733, exports `_DEFAULT_SHELL_TIMEOUT_MODE_RAW`
- order 417: `DEFAULT_SHELL_TIMEOUT_MODE` (constant), lines 4734-4738, exports `DEFAULT_SHELL_TIMEOUT_MODE`
- order 418: `MIN_SHELL_ASYNC_HANDOFF_SECONDS` (constant), lines 4739-4739, exports `MIN_SHELL_ASYNC_HANDOFF_SECONDS`
- order 419: `MAX_SHELL_ASYNC_HANDOFF_SECONDS` (constant), lines 4740-4740, exports `MAX_SHELL_ASYNC_HANDOFF_SECONDS`
- order 420: `SHELL_FAILURE_GUIDANCE_SECONDS` (constant), lines 4741-4743, exports `SHELL_FAILURE_GUIDANCE_SECONDS`
- order 421: `DEFAULT_SHELL_ASYNC_HANDOFF_SECONDS` (constant), lines 4744-4758, exports `DEFAULT_SHELL_ASYNC_HANDOFF_SECONDS`
- order 422: `DEFAULT_SHELL_COMMAND_TIMEOUT_SECONDS` (constant), lines 4759-4773, exports `DEFAULT_SHELL_COMMAND_TIMEOUT_SECONDS`
- order 423: `DEFAULT_SINGLE_NO_PLAN_TODO_PROMPT` (constant), lines 4774-4788, exports `DEFAULT_SINGLE_NO_PLAN_TODO_PROMPT`
- order 424: `SINGLE_NO_PLAN_TODO_BOOTSTRAP_MAX_ATTEMPTS` (constant), lines 4789-4789, exports `SINGLE_NO_PLAN_TODO_BOOTSTRAP_MAX_ATTEMPTS`
- order 425: `AUTO_CONTINUE_BUDGET_DEFAULT` (constant), lines 4790-4790, exports `AUTO_CONTINUE_BUDGET_DEFAULT`
- order 426: `AGENT_MAX_OUTPUT_TOKENS` (constant), lines 4791-4791, exports `AGENT_MAX_OUTPUT_TOKENS`
- order 427: `OLLAMA_THINKING_TOOL_BUFFER` (constant), lines 4792-4792, exports `OLLAMA_THINKING_TOOL_BUFFER`
- order 428: `WATCHDOG_INTENT_NO_TOOL_THRESHOLD` (constant), lines 4793-4793, exports `WATCHDOG_INTENT_NO_TOOL_THRESHOLD`
- order 429: `WATCHDOG_REPEAT_NO_TOOL_THRESHOLD` (constant), lines 4794-4794, exports `WATCHDOG_REPEAT_NO_TOOL_THRESHOLD`
- order 430: `WATCHDOG_INTENT_NO_TOOL_THRESHOLD_SINGLE` (constant), lines 4795-4795, exports `WATCHDOG_INTENT_NO_TOOL_THRESHOLD_SINGLE`
- order 431: `WATCHDOG_REPEAT_NO_TOOL_THRESHOLD_SINGLE` (constant), lines 4796-4796, exports `WATCHDOG_REPEAT_NO_TOOL_THRESHOLD_SINGLE`
- order 432: `WATCHDOG_STATE_STALL_THRESHOLD` (constant), lines 4797-4797, exports `WATCHDOG_STATE_STALL_THRESHOLD`
- order 433: `WATCHDOG_CONTEXT_STALL_THRESHOLD` (constant), lines 4798-4798, exports `WATCHDOG_CONTEXT_STALL_THRESHOLD`
- order 434: `WATCHDOG_REPEAT_SIMILARITY_THRESHOLD` (constant), lines 4799-4799, exports `WATCHDOG_REPEAT_SIMILARITY_THRESHOLD`
- order 435: `WATCHDOG_CONTEXT_NEAR_RATIO` (constant), lines 4800-4800, exports `WATCHDOG_CONTEXT_NEAR_RATIO`
- order 436: `WATCHDOG_MAX_DECOMPOSE_STEPS` (constant), lines 4801-4801, exports `WATCHDOG_MAX_DECOMPOSE_STEPS`
- order 437: `WATCHDOG_STEP_MAX_ATTEMPTS` (constant), lines 4802-4802, exports `WATCHDOG_STEP_MAX_ATTEMPTS`
- order 438: `EMPTY_ACTION_MIN_CONTENT_CHARS` (constant), lines 4803-4803, exports `EMPTY_ACTION_MIN_CONTENT_CHARS`
- order 439: `EMPTY_ACTION_WAKEUP_RETRY_LIMIT` (constant), lines 4804-4804, exports `EMPTY_ACTION_WAKEUP_RETRY_LIMIT`
- order 440: `EMPTY_ACTION_INTERVENTION_THRESHOLD` (constant), lines 4805-4811, exports `EMPTY_ACTION_INTERVENTION_THRESHOLD`
- order 441: `EMPTY_ACTION_BOOTSTRAP_THINKING_GRACE_ROUNDS` (constant), lines 4812-4816, exports `EMPTY_ACTION_BOOTSTRAP_THINKING_GRACE_ROUNDS`
- order 442: `EMPTY_ACTION_RECOVERY_MAX_TOKENS` (constant), lines 4817-4817, exports `EMPTY_ACTION_RECOVERY_MAX_TOKENS`
- order 443: `THINKING_BUDGET_FORCE_RATIO` (constant), lines 4818-4818, exports `THINKING_BUDGET_FORCE_RATIO`
- order 444: `_TOOL_TIMEOUT_MAP` (assignment), lines 4819-4840, exports `_TOOL_TIMEOUT_MAP`
- order 445: `_DEFAULT_TOOL_TIMEOUT` (assignment), lines 4841-4841, exports `_DEFAULT_TOOL_TIMEOUT`
- order 446: `CONVERSATION_VISIBLE_TOOL_EVENTS` (constant), lines 4842-4854, exports `CONVERSATION_VISIBLE_TOOL_EVENTS`
- order 447: `PERSIST_ON_EVENT_TYPES` (constant), lines 4855-4873, exports `PERSIST_ON_EVENT_TYPES`
- order 448: `PERSIST_EVENT_MIN_INTERVAL_SECONDS` (constant), lines 4874-4874, exports `PERSIST_EVENT_MIN_INTERVAL_SECONDS`
- order 449: `TRUNCATION_CONTINUATION_MAX_PASSES` (constant), lines 4875-4875, exports `TRUNCATION_CONTINUATION_MAX_PASSES`
- order 450: `TRUNCATION_CONTINUATION_MAX_TOKENS` (constant), lines 4876-4876, exports `TRUNCATION_CONTINUATION_MAX_TOKENS`
- order 451: `TRUNCATION_CONTINUATION_TAIL_CHARS` (constant), lines 4877-4877, exports `TRUNCATION_CONTINUATION_TAIL_CHARS`
- order 452: `TRUNCATION_CONTINUATION_ECHO_CHARS` (constant), lines 4878-4878, exports `TRUNCATION_CONTINUATION_ECHO_CHARS`
- order 453: `TRUNCATION_OVERLAP_SCAN_CHARS` (constant), lines 4879-4879, exports `TRUNCATION_OVERLAP_SCAN_CHARS`
- order 454: `TRUNCATION_PAIR_SCAN_CHARS` (constant), lines 4880-4880, exports `TRUNCATION_PAIR_SCAN_CHARS`
- order 455: `TRUNCATION_LIVE_BUFFER_MAX_CHARS` (constant), lines 4881-4881, exports `TRUNCATION_LIVE_BUFFER_MAX_CHARS`
- order 456: `MIN_CONTEXT_TOKEN_LIMIT` (constant), lines 4882-4882, exports `MIN_CONTEXT_TOKEN_LIMIT`
- order 457: `COMPACT_TIER1_PCT` (constant), lines 4883-4884, exports `COMPACT_TIER1_PCT`
- order 458: `COMPACT_TIER2_PCT` (constant), lines 4885-4885, exports `COMPACT_TIER2_PCT`
- order 459: `COMPACT_TIER3_PCT` (constant), lines 4886-4886, exports `COMPACT_TIER3_PCT`
- order 460: `COMPACT_TIER1_ABS` (constant), lines 4887-4888, exports `COMPACT_TIER1_ABS`
- order 461: `COMPACT_TIER2_ABS` (constant), lines 4889-4889, exports `COMPACT_TIER2_ABS`
- order 462: `CONTEXT_COMPACT_INEFFECTIVE_COOLDOWN_SECONDS` (constant), lines 4890-4896, exports `CONTEXT_COMPACT_INEFFECTIVE_COOLDOWN_SECONDS`
- order 463: `FILE_BUFFER_CONTENT_THRESHOLD` (constant), lines 4897-4898, exports `FILE_BUFFER_CONTENT_THRESHOLD`
- order 464: `FILE_BUFFER_MAX_FILES` (constant), lines 4899-4899, exports `FILE_BUFFER_MAX_FILES`
- order 465: `AUTHORITATIVE_USER_GOAL_OPEN` (constant), lines 4900-4900, exports `AUTHORITATIVE_USER_GOAL_OPEN`
- order 466: `AUTHORITATIVE_USER_GOAL_CLOSE` (constant), lines 4901-4901, exports `AUTHORITATIVE_USER_GOAL_CLOSE`
- order 467: `AGENT_MSG_LIMIT_TIER0` (constant), lines 4902-4903, exports `AGENT_MSG_LIMIT_TIER0`
- order 468: `AGENT_MSG_LIMIT_TIER1` (constant), lines 4904-4904, exports `AGENT_MSG_LIMIT_TIER1`
- order 469: `AGENT_MSG_LIMIT_TIER2` (constant), lines 4905-4905, exports `AGENT_MSG_LIMIT_TIER2`
- order 470: `AGENT_MSG_LIMIT_TIER3` (constant), lines 4906-4906, exports `AGENT_MSG_LIMIT_TIER3`
- order 471: `AGENT_CTX_LIMIT_TIER0` (constant), lines 4907-4907, exports `AGENT_CTX_LIMIT_TIER0`
- order 472: `AGENT_CTX_LIMIT_TIER1` (constant), lines 4908-4908, exports `AGENT_CTX_LIMIT_TIER1`
- order 473: `AGENT_CTX_LIMIT_TIER2` (constant), lines 4909-4909, exports `AGENT_CTX_LIMIT_TIER2`
- order 474: `AGENT_CTX_LIMIT_TIER3` (constant), lines 4910-4910, exports `AGENT_CTX_LIMIT_TIER3`
- order 475: `MANAGER_CTX_LIMIT_TIER0` (constant), lines 4911-4911, exports `MANAGER_CTX_LIMIT_TIER0`
- order 476: `MANAGER_CTX_LIMIT_TIER1` (constant), lines 4912-4912, exports `MANAGER_CTX_LIMIT_TIER1`
- order 477: `MANAGER_CTX_LIMIT_TIER2` (constant), lines 4913-4913, exports `MANAGER_CTX_LIMIT_TIER2`
- order 478: `MANAGER_CTX_LIMIT_TIER3` (constant), lines 4914-4914, exports `MANAGER_CTX_LIMIT_TIER3`
- order 479: `MAX_CONTEXT_ARCHIVE_SEGMENTS` (constant), lines 4915-4915, exports `MAX_CONTEXT_ARCHIVE_SEGMENTS`
- order 480: `MAX_USER_BUBBLE_LOG` (constant), lines 4916-4917, exports `MAX_USER_BUBBLE_LOG`
- order 481: `MANAGER_INSTRUCTION_MAX_CHARS` (constant), lines 4918-4922, exports `MANAGER_INSTRUCTION_MAX_CHARS`
- order 482: `MANAGER_MOMENTUM_MAX_SKIPS` (constant), lines 4923-4928, exports `MANAGER_MOMENTUM_MAX_SKIPS`
- order 483: `MODEL_OUTPUT_RETRY_TIMES` (constant), lines 4929-4933, exports `MODEL_OUTPUT_RETRY_TIMES`
- order 484: `ARBITER_TRIGGER_MIN_CONTENT_CHARS` (constant), lines 4934-4934, exports `ARBITER_TRIGGER_MIN_CONTENT_CHARS`
- order 485: `ARBITER_VALID_PLANNING_STREAK_LIMIT` (constant), lines 4935-4935, exports `ARBITER_VALID_PLANNING_STREAK_LIMIT`
- order 486: `ARBITER_DEFAULT_TIMEOUT_SECONDS` (constant), lines 4936-4936, exports `ARBITER_DEFAULT_TIMEOUT_SECONDS`
- order 487: `ARBITER_DEFAULT_MAX_TOKENS` (constant), lines 4937-4937, exports `ARBITER_DEFAULT_MAX_TOKENS`
- order 488: `ARBITER_DEFAULT_TEMPERATURE` (constant), lines 4938-4938, exports `ARBITER_DEFAULT_TEMPERATURE`
- order 489: `LIVE_INPUT_DELAY_WRITE_ROUNDS` (constant), lines 4939-4939, exports `LIVE_INPUT_DELAY_WRITE_ROUNDS`
- order 490: `LIVE_INPUT_DELAY_TOOL_ROUNDS` (constant), lines 4940-4940, exports `LIVE_INPUT_DELAY_TOOL_ROUNDS`
- order 491: `LIVE_INPUT_DELAY_NORMAL_ROUNDS` (constant), lines 4941-4941, exports `LIVE_INPUT_DELAY_NORMAL_ROUNDS`
- order 492: `LIVE_INPUT_MAX_INJECTIONS` (constant), lines 4942-4942, exports `LIVE_INPUT_MAX_INJECTIONS`
- order 493: `LIVE_INPUT_REINJECT_INTERVAL` (constant), lines 4943-4943, exports `LIVE_INPUT_REINJECT_INTERVAL`
- order 494: `LIVE_INPUT_WEIGHT_BASE_DELAYED` (constant), lines 4944-4944, exports `LIVE_INPUT_WEIGHT_BASE_DELAYED`
- order 495: `LIVE_INPUT_WEIGHT_BASE_NORMAL` (constant), lines 4945-4945, exports `LIVE_INPUT_WEIGHT_BASE_NORMAL`
- order 496: `LIVE_INPUT_WEIGHT_STEP_DELAYED` (constant), lines 4946-4946, exports `LIVE_INPUT_WEIGHT_STEP_DELAYED`
- order 497: `LIVE_INPUT_WEIGHT_STEP_NORMAL` (constant), lines 4947-4947, exports `LIVE_INPUT_WEIGHT_STEP_NORMAL`
- order 499: `BENIGN_SOCKET_DEBUG_LOG_ENABLED` (constant), lines 4954-4960, exports `BENIGN_SOCKET_DEBUG_LOG_ENABLED`
- order 500: `BENIGN_SOCKET_LOG_INTERVAL_SECONDS` (constant), lines 4961-4961, exports `BENIGN_SOCKET_LOG_INTERVAL_SECONDS`
- order 501: `FINAL_SUMMARY_MIN_CHARS` (constant), lines 4962-4962, exports `FINAL_SUMMARY_MIN_CHARS`
- order 502: `FINAL_SUMMARY_STRICT_MIN_CHARS` (constant), lines 4963-4963, exports `FINAL_SUMMARY_STRICT_MIN_CHARS`
- order 503: `RUNTIME_CONTROL_HINT_PREFIXES` (constant), lines 4964-4984, exports `RUNTIME_CONTROL_HINT_PREFIXES`
- order 504: `UI_HIDDEN_RUNTIME_CONTROL_PREFIXES` (constant), lines 4985-5013, exports `UI_HIDDEN_RUNTIME_CONTROL_PREFIXES`
- order 505: `UI_PROJECTED_RUNTIME_CONTROL_TAGS` (constant), lines 5014-5036, exports `UI_PROJECTED_RUNTIME_CONTROL_TAGS`
- order 506: `UI_LEGACY_PROJECTED_RUNTIME_CONTROL_TAGS` (constant), lines 5037-5039, exports `UI_LEGACY_PROJECTED_RUNTIME_CONTROL_TAGS`
- order 507: `RETRY_RUNTIME_HINT_PREFIXES` (constant), lines 5040-5054, exports `RETRY_RUNTIME_HINT_PREFIXES`
- order 508: `EXECUTION_MODE_SINGLE` (constant), lines 5055-5055, exports `EXECUTION_MODE_SINGLE`
- order 509: `EXECUTION_MODE_SEQUENTIAL` (constant), lines 5056-5056, exports `EXECUTION_MODE_SEQUENTIAL`
- order 510: `EXECUTION_MODE_SYNC` (constant), lines 5057-5057, exports `EXECUTION_MODE_SYNC`
- order 511: `EXECUTION_MODE_CHOICES` (constant), lines 5058-5062, exports `EXECUTION_MODE_CHOICES`
- order 512: `AGENT_ROLES` (constant), lines 5063-5063, exports `AGENT_ROLES`
- order 513: `AGENT_BUBBLE_ROLES` (constant), lines 5064-5064, exports `AGENT_BUBBLE_ROLES`
- order 514: `AGENT_ROLE_LABELS` (constant), lines 5065-5071, exports `AGENT_ROLE_LABELS`
- order 515: `AGENT_ROLE_BUBBLE_COLORS` (constant), lines 5072-5078, exports `AGENT_ROLE_BUBBLE_COLORS`
- order 516: `BLACKBOARD_STATUSES` (constant), lines 5079-5088, exports `BLACKBOARD_STATUSES`
- order 517: `TASK_COMPLEXITY_LEVELS` (constant), lines 5089-5089, exports `TASK_COMPLEXITY_LEVELS`
- order 518: `TASK_COMPLEXITY_RANKS` (constant), lines 5090-5095, exports `TASK_COMPLEXITY_RANKS`
- order 519: `TASK_PROFILE_TYPES` (constant), lines 5096-5102, exports `TASK_PROFILE_TYPES`
- order 520: `TASK_LEVEL_CHOICES` (constant), lines 5103-5103, exports `TASK_LEVEL_CHOICES`
- order 521: `TASK_SCALE_PREFERENCES` (constant), lines 5104-5104, exports `TASK_SCALE_PREFERENCES`
- order 522: `SEMANTIC_CONFIDENCE_CHOICES` (constant), lines 5105-5105, exports `SEMANTIC_CONFIDENCE_CHOICES`
- order 523: `L2_TODO_POLICY_CHOICES` (constant), lines 5106-5110, exports `L2_TODO_POLICY_CHOICES`
- order 524: `DEFAULT_L2_TODO_POLICY` (constant), lines 5111-5111, exports `DEFAULT_L2_TODO_POLICY`
- order 525: `TASK_LEVEL_POLICIES` (constant), lines 5112-5165, exports `TASK_LEVEL_POLICIES`
- order 526: `MANAGER_ROUTE_TARGETS` (constant), lines 5166-5166, exports `MANAGER_ROUTE_TARGETS`
- order 527: `BLACKBOARD_MAX_LOG_ENTRIES` (constant), lines 5167-5167, exports `BLACKBOARD_MAX_LOG_ENTRIES`
- order 528: `BLACKBOARD_MAX_TEXT` (constant), lines 5168-5168, exports `BLACKBOARD_MAX_TEXT`
- order 529: `BLACKBOARD_MEMORY_SHORT_MAX` (constant), lines 5169-5169, exports `BLACKBOARD_MEMORY_SHORT_MAX`
- order 530: `BLACKBOARD_MEMORY_MID_MAX_STEPS` (constant), lines 5170-5170, exports `BLACKBOARD_MEMORY_MID_MAX_STEPS`
- order 531: `BLACKBOARD_MEMORY_MID_ITEMS_PER_STEP` (constant), lines 5171-5171, exports `BLACKBOARD_MEMORY_MID_ITEMS_PER_STEP`
- order 532: `BLACKBOARD_MEMORY_LONG_MAX` (constant), lines 5172-5172, exports `BLACKBOARD_MEMORY_LONG_MAX`
- order 533: `BLACKBOARD_MEMORY_INDEX_MAX` (constant), lines 5173-5173, exports `BLACKBOARD_MEMORY_INDEX_MAX`
- order 534: `SKILL_REFRESH_MIN_INTERVAL_SECONDS` (constant), lines 5174-5174, exports `SKILL_REFRESH_MIN_INTERVAL_SECONDS`
- order 535: `SKILL_CATALOG_FULL_REFRESH_SECONDS` (constant), lines 5175-5178, exports `SKILL_CATALOG_FULL_REFRESH_SECONDS`
- order 536: `SKILL_PROMPT_MAX_ITEMS` (constant), lines 5179-5179, exports `SKILL_PROMPT_MAX_ITEMS`
- order 537: `SKILL_PROMPT_MAX_CHARS` (constant), lines 5180-5180, exports `SKILL_PROMPT_MAX_CHARS`
- order 538: `SKILL_RUNTIME_CACHE_MAX_ENTRIES` (constant), lines 5181-5181, exports `SKILL_RUNTIME_CACHE_MAX_ENTRIES`
- order 539: `SKILL_RUNTIME_CACHE_MAX_BYTES` (constant), lines 5182-5182, exports `SKILL_RUNTIME_CACHE_MAX_BYTES`
- order 540: `SKILL_AUTOLOAD_SCORE_THRESHOLD` (constant), lines 5183-5186, exports `SKILL_AUTOLOAD_SCORE_THRESHOLD`
- order 541: `SKILL_AUTOLOAD_CONFIDENCE_THRESHOLD` (constant), lines 5187-5187, exports `SKILL_AUTOLOAD_CONFIDENCE_THRESHOLD`
- order 542: `SKILL_RUNTIME_EVALUATION_TTL_SECONDS` (constant), lines 5188-5188, exports `SKILL_RUNTIME_EVALUATION_TTL_SECONDS`
- order 543: `SKILL_RUNTIME_EVALUATION_TIMEOUT_SECONDS` (constant), lines 5189-5189, exports `SKILL_RUNTIME_EVALUATION_TIMEOUT_SECONDS`
- order 544: `SKILL_RUNTIME_UNLOAD_CONFIDENCE_THRESHOLD` (constant), lines 5190-5190, exports `SKILL_RUNTIME_UNLOAD_CONFIDENCE_THRESHOLD`
- order 545: `SKILL_RUNTIME_KEY_TOOL_INTERVAL` (constant), lines 5191-5191, exports `SKILL_RUNTIME_KEY_TOOL_INTERVAL`
- order 546: `SKILL_RUNTIME_EVENTS_MAX` (constant), lines 5192-5192, exports `SKILL_RUNTIME_EVENTS_MAX`
- order 547: `SKILL_METADATA_CAPSULE_MAX_CHARS` (constant), lines 5193-5193, exports `SKILL_METADATA_CAPSULE_MAX_CHARS`
- order 548: `SKILL_DEPENDENCY_MAX_DEPTH` (constant), lines 5194-5194, exports `SKILL_DEPENDENCY_MAX_DEPTH`
- order 549: `AUTO_SKILLS_ROOT_CANDIDATES` (constant), lines 5195-5195, exports `AUTO_SKILLS_ROOT_CANDIDATES`
- order 550: `SKILL_DEFAULT_ATTACHMENT_GLOBS` (constant), lines 5196-5226, exports `SKILL_DEFAULT_ATTACHMENT_GLOBS`
- order 551: `SKILL_INLINE_ATTACHMENT_MAX_FILES` (constant), lines 5227-5227, exports `SKILL_INLINE_ATTACHMENT_MAX_FILES`
- order 552: `SKILL_INLINE_ATTACHMENT_MAX_CHARS` (constant), lines 5228-5228, exports `SKILL_INLINE_ATTACHMENT_MAX_CHARS`
- order 553: `SKILL_RESOURCE_MANIFEST_MAX_ITEMS` (constant), lines 5229-5229, exports `SKILL_RESOURCE_MANIFEST_MAX_ITEMS`
- order 554: `SKILL_BODY_COMPACT_THRESHOLD_CHARS` (constant), lines 5230-5230, exports `SKILL_BODY_COMPACT_THRESHOLD_CHARS`
- order 555: `SKILL_BODY_PREVIEW_CHARS` (constant), lines 5231-5231, exports `SKILL_BODY_PREVIEW_CHARS`
- order 556: `SKILLS_VIRTUAL_PREFIX` (constant), lines 5232-5232, exports `SKILLS_VIRTUAL_PREFIX`
- order 557: `SKILLS_EXTERNAL_MOUNT` (constant), lines 5233-5233, exports `SKILLS_EXTERNAL_MOUNT`
- order 558: `PLAN_MODE_ENABLED_LEVELS` (constant), lines 5234-5234, exports `PLAN_MODE_ENABLED_LEVELS`
- order 559: `PLAN_MODE_FORCED_LEVELS` (constant), lines 5235-5235, exports `PLAN_MODE_FORCED_LEVELS`
- order 560: `PLAN_MODE_USER_CHOICES` (constant), lines 5236-5236, exports `PLAN_MODE_USER_CHOICES`
- order 561: `TASK_PHASES` (constant), lines 5237-5238, exports `TASK_PHASES`
- order 562: `TASK_PHASE_ROUTING` (constant), lines 5239-5246, exports `TASK_PHASE_ROUTING`
- order 563: `COMPLEXITY_KEYWORDS` (constant), lines 5247-5253, exports `COMPLEXITY_KEYWORDS`
- order 564: `USER_COMPLEXITY_SIMPLE_TOKENS` (constant), lines 5254-5258, exports `USER_COMPLEXITY_SIMPLE_TOKENS`
- order 565: `USER_COMPLEXITY_MODERATE_TOKENS` (constant), lines 5259-5263, exports `USER_COMPLEXITY_MODERATE_TOKENS`
- order 566: `USER_COMPLEXITY_COMPLEX_TOKENS` (constant), lines 5264-5268, exports `USER_COMPLEXITY_COMPLEX_TOKENS`
- order 567: `USER_COMPLEXITY_EXPERT_TOKENS` (constant), lines 5269-5273, exports `USER_COMPLEXITY_EXPERT_TOKENS`
- order 568: `PLAN_MODE_EXPLORER_MAX_ROUNDS` (constant), lines 5274-5277, exports `PLAN_MODE_EXPLORER_MAX_ROUNDS`
- order 569: `PLAN_MODE_EXPLORER_PRODUCTIVE_ROUNDS` (constant), lines 5278-5278, exports `PLAN_MODE_EXPLORER_PRODUCTIVE_ROUNDS`
- order 570: `PLAN_MODE_EXPLORER_STALE_ROUNDS` (constant), lines 5279-5279, exports `PLAN_MODE_EXPLORER_STALE_ROUNDS`
- order 571: `PLAN_MODE_SYNTHESIS_MAX_ATTEMPTS` (constant), lines 5280-5280, exports `PLAN_MODE_SYNTHESIS_MAX_ATTEMPTS`
- order 572: `REVIEWER_DEBUG_MODE_MAX_ROUNDS` (constant), lines 5281-5282, exports `REVIEWER_DEBUG_MODE_MAX_ROUNDS`
- order 573: `REVIEWER_DEBUG_TOOL_ALLOWLIST` (constant), lines 5283-5288, exports `REVIEWER_DEBUG_TOOL_ALLOWLIST`
- order 574: `EXPLORER_STALL_THRESHOLD` (constant), lines 5289-5289, exports `EXPLORER_STALL_THRESHOLD`
- order 575: `DEVELOPER_EDIT_STALL_THRESHOLD` (constant), lines 5290-5290, exports `DEVELOPER_EDIT_STALL_THRESHOLD`
- order 576: `ACCEPTANCE_GATE_STALL_THRESHOLD` (constant), lines 5291-5294, exports `ACCEPTANCE_GATE_STALL_THRESHOLD`
- order 577: `ACCEPTANCE_GATE_HARD_CEILING` (constant), lines 5295-5298, exports `ACCEPTANCE_GATE_HARD_CEILING`
- order 578: `ACCEPTANCE_GATE_TOTAL_ROUND_CEILING` (constant), lines 5299-5299, exports `ACCEPTANCE_GATE_TOTAL_ROUND_CEILING`
- order 579: `PLAN_MODE_MANAGER_SYNTHESIS_MAX_TOKENS` (constant), lines 5300-5300, exports `PLAN_MODE_MANAGER_SYNTHESIS_MAX_TOKENS`
- order 580: `PLAN_MODE_MAX_OPTIONS` (constant), lines 5301-5301, exports `PLAN_MODE_MAX_OPTIONS`
- order 581: `PLAN_FILE_RELATIVE_PATH` (constant), lines 5302-5302, exports `PLAN_FILE_RELATIVE_PATH`
- order 582: `PLAN_BUBBLE_MAX_CHARS` (constant), lines 5303-5303, exports `PLAN_BUBBLE_MAX_CHARS`
- order 583: `PLAN_NOTICE_BODY_MAX_CHARS` (constant), lines 5304-5304, exports `PLAN_NOTICE_BODY_MAX_CHARS`
- order 584: `PLAN_MESSAGE_EVENT_MAX_CHARS` (constant), lines 5305-5305, exports `PLAN_MESSAGE_EVENT_MAX_CHARS`
- order 585: `PLAN_STEP_FULL_CONTENT_MAX_CHARS` (constant), lines 5306-5306, exports `PLAN_STEP_FULL_CONTENT_MAX_CHARS`
- order 586: `PLAN_MODE_RESEARCH_TOOL_ALLOWLIST` (constant), lines 5307-5314, exports `PLAN_MODE_RESEARCH_TOOL_ALLOWLIST`
- order 587: `FAILURE_LEDGER_MAX_FIXES` (constant), lines 5315-5315, exports `FAILURE_LEDGER_MAX_FIXES`
- order 588: `FAILURE_LEDGER_MAX_COMPILE_ERRORS` (constant), lines 5316-5316, exports `FAILURE_LEDGER_MAX_COMPILE_ERRORS`
- order 589: `FAILURE_LEDGER_MAX_DELEGATIONS` (constant), lines 5317-5317, exports `FAILURE_LEDGER_MAX_DELEGATIONS`
- order 590: `FAILURE_LEDGER_MAX_STALLS` (constant), lines 5318-5318, exports `FAILURE_LEDGER_MAX_STALLS`
- order 591: `FAILURE_LEDGER_MAX_TOOL_FPS` (constant), lines 5319-5319, exports `FAILURE_LEDGER_MAX_TOOL_FPS`
- order 592: `FAILURE_LEDGER_MAX_ERRORS` (constant), lines 5320-5320, exports `FAILURE_LEDGER_MAX_ERRORS`
- order 593: `ERROR_CATEGORY_DEFS` (constant), lines 5321-5360, exports `ERROR_CATEGORY_DEFS`
- order 594: `CHECKPOINT_MAX_COUNT` (constant), lines 5361-5361, exports `CHECKPOINT_MAX_COUNT`
- order 595: `CHECKPOINT_INTERVAL_ROUNDS` (constant), lines 5362-5362, exports `CHECKPOINT_INTERVAL_ROUNDS`
- order 596: `PERSISTED_ROUTES_MAX` (constant), lines 5363-5363, exports `PERSISTED_ROUTES_MAX`
- order 597: `HTML_FRONTEND_REQUEST_KEYWORDS` (constant), lines 5364-5403, exports `HTML_FRONTEND_REQUEST_KEYWORDS`
- order 598: `DEEP_RESEARCH_REQUEST_KEYWORDS` (constant), lines 5404-5426, exports `DEEP_RESEARCH_REQUEST_KEYWORDS`
- order 599: `DEEP_RESEARCH_RETRIEVAL_KEYWORDS` (constant), lines 5427-5446, exports `DEEP_RESEARCH_RETRIEVAL_KEYWORDS`
- order 600: `DEEP_RESEARCH_TEXT_ONLY_HINT_KEYWORDS` (constant), lines 5447-5464, exports `DEEP_RESEARCH_TEXT_ONLY_HINT_KEYWORDS`
- order 601: `DANGEROUS_PATTERNS` (constant), lines 5465-5466, exports `DANGEROUS_PATTERNS`
- order 602: `VALID_MSG_TYPES` (constant), lines 5467-5473, exports `VALID_MSG_TYPES`
- order 603: `SUPPORTED_UI_LANGUAGES` (constant), lines 5474-5480, exports `SUPPORTED_UI_LANGUAGES`
- order 604: `UI_LANGUAGE_LABELS` (constant), lines 5481-5481, exports `UI_LANGUAGE_LABELS`
- order 605: `DEFAULT_UI_LANGUAGE` (constant), lines 5482-5482, exports `DEFAULT_UI_LANGUAGE`
- order 606: `PUBLIC_TOOL_PROGRESS_SUMMARY_ENABLED` (constant), lines 5483-5485, exports `PUBLIC_TOOL_PROGRESS_SUMMARY_ENABLED`
- order 607: `AGENT_LANGUAGE_PREFERENCES` (constant), lines 5486-5527, exports `AGENT_LANGUAGE_PREFERENCES`
- order 608: `UI_STYLE_CHOICES` (constant), lines 5528-5528, exports `UI_STYLE_CHOICES`
- order 609: `UI_STYLE_LABELS` (constant), lines 5529-5529, exports `UI_STYLE_LABELS`
- order 610: `DEFAULT_UI_STYLE` (constant), lines 5530-5530, exports `DEFAULT_UI_STYLE`
- order 611: `DEFAULT_WEB_UI_DIR` (constant), lines 5531-5531, exports `DEFAULT_WEB_UI_DIR`
- order 612: `DEFAULT_WEB_UI_CONFIG` (constant), lines 5532-5532, exports `DEFAULT_WEB_UI_CONFIG`
- order 613: `WEB_UI_REQUIRED_FILES` (constant), lines 5533-5540, exports `WEB_UI_REQUIRED_FILES`
- order 614: `WEB_UI_OPTIONAL_FILES` (constant), lines 5541-5541, exports `WEB_UI_OPTIONAL_FILES`
- order 615: `WEB_UI_APPLICATION_CONTRACT_VERSION` (constant), lines 5542-5542, exports `WEB_UI_APPLICATION_CONTRACT_VERSION`
- order 616: `WEB_UI_APPLICATION_FEATURE_MARKERS` (constant), lines 5543-5562, exports `WEB_UI_APPLICATION_FEATURE_MARKERS`
- order 617: `IMAGE_EXTS` (constant), lines 5563-5577, exports `IMAGE_EXTS`
- order 618: `IMAGE_FORMATS_NEED_CONVERSION` (constant), lines 5578-5578, exports `IMAGE_FORMATS_NEED_CONVERSION`
- order 619: `IMAGE_SAFE_FORMATS` (constant), lines 5579-5579, exports `IMAGE_SAFE_FORMATS`
- order 620: `AUDIO_EXTS` (constant), lines 5580-5590, exports `AUDIO_EXTS`
- order 621: `VIDEO_EXTS` (constant), lines 5591-5601, exports `VIDEO_EXTS`
- order 622: `CODE_PREVIEW_STAGE_MAX_BYTES` (constant), lines 5602-5602, exports `CODE_PREVIEW_STAGE_MAX_BYTES`
- order 623: `CODE_PREVIEW_STAGE_MAX_ROWS` (constant), lines 5603-5603, exports `CODE_PREVIEW_STAGE_MAX_ROWS`
- order 624: `CODE_PREVIEW_STAGE_MAX_PER_FILE` (constant), lines 5604-5604, exports `CODE_PREVIEW_STAGE_MAX_PER_FILE`
- order 625: `CODE_PREVIEW_STAGE_MAX_TOTAL` (constant), lines 5605-5605, exports `CODE_PREVIEW_STAGE_MAX_TOTAL`
- order 626: `CODE_PREVIEW_DIFF_CONTEXT_LINES` (constant), lines 5606-5606, exports `CODE_PREVIEW_DIFF_CONTEXT_LINES`
- order 627: `CODE_PREVIEW_DIFF_MERGE_GAP` (constant), lines 5607-5607, exports `CODE_PREVIEW_DIFF_MERGE_GAP`
- order 628: `PREVIEW_DOWNLOAD_MAX_FILES` (constant), lines 5608-5608, exports `PREVIEW_DOWNLOAD_MAX_FILES`
- order 629: `PREVIEW_DOWNLOAD_MAX_BYTES` (constant), lines 5609-5609, exports `PREVIEW_DOWNLOAD_MAX_BYTES`
- order 630: `FILES_TREE_DEFAULT_MAX_NODES` (constant), lines 5610-5610, exports `FILES_TREE_DEFAULT_MAX_NODES`
- order 631: `FILES_TREE_DEFAULT_MAX_DEPTH` (constant), lines 5611-5611, exports `FILES_TREE_DEFAULT_MAX_DEPTH`
- order 632: `FILES_TREE_SKIP_DIRS` (constant), lines 5612-5620, exports `FILES_TREE_SKIP_DIRS`
- order 633: `FILES_TREE_SKIP_REL_DIRS` (constant), lines 5621-5623, exports `FILES_TREE_SKIP_REL_DIRS`
- order 634: `IDE_FILE_MAX_BYTES` (constant), lines 5624-5624, exports `IDE_FILE_MAX_BYTES`
- order 635: `IDE_UPLOAD_MAX_BYTES` (constant), lines 5625-5625, exports `IDE_UPLOAD_MAX_BYTES`
- order 636: `IDE_UPLOAD_TOTAL_MAX_BYTES` (constant), lines 5626-5626, exports `IDE_UPLOAD_TOTAL_MAX_BYTES`
- order 637: `IDE_UPLOAD_MAX_ITEMS` (constant), lines 5627-5627, exports `IDE_UPLOAD_MAX_ITEMS`
- order 638: `IDE_UPLOAD_CHUNK_MAX_BYTES` (constant), lines 5628-5628, exports `IDE_UPLOAD_CHUNK_MAX_BYTES`
- order 639: `IDE_UPLOAD_STREAM_MAX_BYTES` (constant), lines 5629-5629, exports `IDE_UPLOAD_STREAM_MAX_BYTES`
- order 640: `IDE_TEXT_PREVIEW_MAX_BYTES` (constant), lines 5630-5630, exports `IDE_TEXT_PREVIEW_MAX_BYTES`
- order 641: `IDE_MARKDOWN_PREVIEW_MAX_LINES` (constant), lines 5631-5631, exports `IDE_MARKDOWN_PREVIEW_MAX_LINES`
- order 642: `IDE_IMAGE_PREVIEW_MAX_EDGE` (constant), lines 5632-5632, exports `IDE_IMAGE_PREVIEW_MAX_EDGE`
- order 643: `IDE_IMAGE_PREVIEW_MAX_PIXELS` (constant), lines 5633-5633, exports `IDE_IMAGE_PREVIEW_MAX_PIXELS`
- order 644: `IDE_IMAGE_PREVIEW_SOURCE_MAX_PIXELS` (constant), lines 5634-5634, exports `IDE_IMAGE_PREVIEW_SOURCE_MAX_PIXELS`
- order 645: `IDE_VECTOR_PREVIEW_MAX_BYTES` (constant), lines 5635-5635, exports `IDE_VECTOR_PREVIEW_MAX_BYTES`
- order 646: `IDE_TABLE_PREVIEW_SOURCE_MAX_BYTES` (constant), lines 5636-5636, exports `IDE_TABLE_PREVIEW_SOURCE_MAX_BYTES`
- order 647: `IDE_TABLE_PREVIEW_CELL_MAX_CHARS` (constant), lines 5637-5637, exports `IDE_TABLE_PREVIEW_CELL_MAX_CHARS`
- order 648: `IDE_TABLE_PREVIEW_TOTAL_CHARS` (constant), lines 5638-5638, exports `IDE_TABLE_PREVIEW_TOTAL_CHARS`
- order 649: `IDE_OFFICE_PREVIEW_MAX_ENTRIES` (constant), lines 5639-5639, exports `IDE_OFFICE_PREVIEW_MAX_ENTRIES`
- order 650: `IDE_OFFICE_PREVIEW_MAX_EXPANDED_BYTES` (constant), lines 5640-5640, exports `IDE_OFFICE_PREVIEW_MAX_EXPANDED_BYTES`
- order 651: `IDE_OFFICE_PREVIEW_MAX_ENTRY_BYTES` (constant), lines 5641-5641, exports `IDE_OFFICE_PREVIEW_MAX_ENTRY_BYTES`
- order 652: `IDE_COMMAND_TIMEOUT_DEFAULT` (constant), lines 5642-5642, exports `IDE_COMMAND_TIMEOUT_DEFAULT`
- order 653: `IDE_TREE_DEFAULT_MAX_NODES` (constant), lines 5643-5643, exports `IDE_TREE_DEFAULT_MAX_NODES`
- order 654: `IDE_TREE_MAX_NODES` (constant), lines 5644-5644, exports `IDE_TREE_MAX_NODES`
- order 655: `IDE_SEARCH_MAX_RESULTS` (constant), lines 5645-5645, exports `IDE_SEARCH_MAX_RESULTS`
- order 656: `IDE_SEARCH_MAX_FILE_BYTES` (constant), lines 5646-5646, exports `IDE_SEARCH_MAX_FILE_BYTES`
- order 657: `IDE_TERMINAL_SCROLLBACK_BYTES` (constant), lines 5647-5647, exports `IDE_TERMINAL_SCROLLBACK_BYTES`
- order 658: `IDE_TERMINAL_IDLE_SECONDS` (constant), lines 5648-5648, exports `IDE_TERMINAL_IDLE_SECONDS`
- order 659: `IDE_DEBUG_ADAPTER_START_ATTEMPTS` (constant), lines 5649-5649, exports `IDE_DEBUG_ADAPTER_START_ATTEMPTS`
- order 660: `IDE_DEBUG_ADAPTER_START_TIMEOUT_SECONDS` (constant), lines 5650-5650, exports `IDE_DEBUG_ADAPTER_START_TIMEOUT_SECONDS`
- order 661: `IDE_VSIX_MAX_BYTES` (constant), lines 5651-5651, exports `IDE_VSIX_MAX_BYTES`
- order 662: `IDE_VSIX_MAX_EXPANDED_BYTES` (constant), lines 5652-5652, exports `IDE_VSIX_MAX_EXPANDED_BYTES`
- order 663: `IDE_VSIX_MAX_FILES` (constant), lines 5653-5653, exports `IDE_VSIX_MAX_FILES`
- order 664: `IDE_VSIX_MAX_FILE_BYTES` (constant), lines 5654-5654, exports `IDE_VSIX_MAX_FILE_BYTES`
- order 665: `IDE_TREE_SKIP_DIRS` (constant), lines 5655-5663, exports `IDE_TREE_SKIP_DIRS`
- order 666: `RENDER_FRAME_MAX_B64_CHARS` (constant), lines 5664-5664, exports `RENDER_FRAME_MAX_B64_CHARS`
- order 667: `RENDER_FRAME_MAX_POINTS` (constant), lines 5665-5665, exports `RENDER_FRAME_MAX_POINTS`
- order 668: `RENDER_FRAME_MAX_LINES` (constant), lines 5666-5666, exports `RENDER_FRAME_MAX_LINES`
- order 669: `RENDER_FRAME_MAX_LINE_POINTS` (constant), lines 5667-5667, exports `RENDER_FRAME_MAX_LINE_POINTS`
- order 670: `RENDER_FRAME_ACTIVITY_INTERVAL_SECONDS` (constant), lines 5668-5668, exports `RENDER_FRAME_ACTIVITY_INTERVAL_SECONDS`
- order 671: `RAW_TOOLCALL_TEXT_FILTER_THRESHOLD` (constant), lines 5669-5669, exports `RAW_TOOLCALL_TEXT_FILTER_THRESHOLD`
- order 672: `ASSISTANT_TEXT_PERSIST_MAX_CHARS` (constant), lines 5670-5670, exports `ASSISTANT_TEXT_PERSIST_MAX_CHARS`
- order 673: `ASSISTANT_MESSAGE_EVENT_MAX_CHARS` (constant), lines 5671-5671, exports `ASSISTANT_MESSAGE_EVENT_MAX_CHARS`
- order 674: `CODE_PREVIEW_EXTS` (constant), lines 5672-5799, exports `CODE_PREVIEW_EXTS`
- order 675: `CODE_PREVIEW_FILENAMES` (constant), lines 5800-5851, exports `CODE_PREVIEW_FILENAMES`
- order 676: `MEDIA_CAPABILITY_KEYS` (constant), lines 5852-5859, exports `MEDIA_CAPABILITY_KEYS`
- order 680: `OFFLINE_JS_LIB_CATALOG` (constant), lines 5892-6218, exports `OFFLINE_JS_LIB_CATALOG`
- order 681: `OFFLINE_JS_ASSET_LOCK` (constant), lines 6219-6219, exports `OFFLINE_JS_ASSET_LOCK`
- order 682: `OFFLINE_JS_LIB_INDEX_FILE` (constant), lines 6220-6220, exports `OFFLINE_JS_LIB_INDEX_FILE`
- order 683: `OFFLINE_JS_LIB_README_FILE` (constant), lines 6221-6221, exports `OFFLINE_JS_LIB_README_FILE`
- order 694: `BACKEND_I18N` (constant), lines 6427-6498, exports `BACKEND_I18N`
- order 695: `_call_backend_i18n_en_update_6500` (expression), lines 6499-6600, exports —
- order 696: `_call_backend_i18n_zh_cn_update_6601` (expression), lines 6601-6701, exports —
- order 697: `_call_backend_i18n_zh_tw_update_6702` (expression), lines 6702-6802, exports —
- order 698: `_call_backend_i18n_ja_update_6803` (expression), lines 6803-6903, exports —
- order 912: `LIQUID_KERNEL_STARTUP_POLICIES` (constant), lines 14073-14075, exports `LIQUID_KERNEL_STARTUP_POLICIES`
- order 913: `LIQUID_KERNEL_BOOTSTRAP_STATE_FILENAME` (constant), lines 14076-14076, exports `LIQUID_KERNEL_BOOTSTRAP_STATE_FILENAME`
- order 943: `TABULAR_PREVIEW_EXTS` (constant), lines 15974-15976, exports `TABULAR_PREVIEW_EXTS`
- order 944: `EXCEL_PREVIEW_EXTS` (constant), lines 15977-15977, exports `EXCEL_PREVIEW_EXTS`
- order 945: `PRESENTATION_PREVIEW_EXTS` (constant), lines 15978-15978, exports `PRESENTATION_PREVIEW_EXTS`
- order 946: `DOCUMENT_PREVIEW_EXTS` (constant), lines 15979-15979, exports `DOCUMENT_PREVIEW_EXTS`
- order 1156: `STUDIO_DEVICE_COOKIE` (constant), lines 115488-115505, exports `STUDIO_DEVICE_COOKIE`
- order 1157: `STUDIO_SESSION_COOKIE` (constant), lines 115506-115506, exports `STUDIO_SESSION_COOKIE`
- order 1158: `STUDIO_DEVICE_TTL` (constant), lines 115507-115507, exports `STUDIO_DEVICE_TTL`
- order 1159: `STUDIO_SESSION_TTL` (constant), lines 115508-115508, exports `STUDIO_SESSION_TTL`
- order 1160: `STUDIO_MAX_FILE_BYTES` (constant), lines 115509-115509, exports `STUDIO_MAX_FILE_BYTES`
- order 1161: `STUDIO_MAX_PROJECT_BYTES` (constant), lines 115510-115510, exports `STUDIO_MAX_PROJECT_BYTES`
- order 1162: `STUDIO_MAX_FILES` (constant), lines 115511-115511, exports `STUDIO_MAX_FILES`
- order 1163: `STUDIO_MAX_JOB_SECONDS` (constant), lines 115512-115512, exports `STUDIO_MAX_JOB_SECONDS`
- order 1169: `STUDIO_INDEX_HTML` (constant), lines 117411-117413, exports `STUDIO_INDEX_HTML`
- order 1170: `STUDIO_CSS` (constant), lines 117414-117414, exports `STUDIO_CSS`
- order 1171: `STUDIO_JS` (constant), lines 117415-117415, exports `STUDIO_JS`

### `config/paths.py`

- order 124: `SCRIPT_DIR` (constant), lines 3824-3824, exports `SCRIPT_DIR`
- order 149: `_resolve_default_agent_workdir` (function), lines 3918-3927, exports `_resolve_default_agent_workdir`
- order 150: `_is_installed_python_runtime` (function), lines 3928-3931, exports `_is_installed_python_runtime`
- order 151: `_runtime_storage_mode` (function), lines 3932-3938, exports `_runtime_storage_mode`
- order 152: `_runtime_tree_has_content` (function), lines 3939-3944, exports `_runtime_tree_has_content`
- order 153: `_copy_runtime_tree_with_crypto_migration` (function), lines 3945-4015, exports `_copy_runtime_tree_with_crypto_migration`
- order 154: `_merge_legacy_codes_root` (function), lines 4016-4081, exports `_merge_legacy_codes_root`
- order 155: `_migrate_legacy_runtime_roots` (function), lines 4082-4172, exports `_migrate_legacy_runtime_roots`
- order 156: `WORKDIR` (constant), lines 4173-4174, exports `WORKDIR`
- order 157: `CODES_ROOT` (constant), lines 4175-4175, exports `CODES_ROOT`
- order 158: `LLM_CONFIG_PATH` (constant), lines 4176-4176, exports `LLM_CONFIG_PATH`
- order 776: `detect_repo_root` (function), lines 8348-8362, exports `detect_repo_root`
- order 777: `REPO_ROOT` (constant), lines 8363-8364, exports `REPO_ROOT`

### `config/settings.py`

- order 687: `normalize_ui_language` (function), lines 6303-6327, exports `normalize_ui_language`
- order 688: `normalize_ui_style` (function), lines 6328-6347, exports `normalize_ui_style`
- order 689: `supported_ui_languages_payload` (function), lines 6348-6351, exports `supported_ui_languages_payload`
- order 691: `agent_language_preference_payload` (function), lines 6364-6373, exports `agent_language_preference_payload`
- order 692: `normalize_execution_mode` (function), lines 6374-6395, exports `normalize_execution_mode`
- order 693: `model_language_instruction` (function), lines 6396-6426, exports `model_language_instruction`
- order 699: `backend_i18n_text` (function), lines 6904-6916, exports `backend_i18n_text`
- order 700: `backend_role_label` (function), lines 6917-6923, exports `backend_role_label`
- order 701: `_detect_os_shell_instruction` (function), lines 6924-6965, exports `_detect_os_shell_instruction`
- order 702: `resolve_web_ui_dir_path` (function), lines 6966-6974, exports `resolve_web_ui_dir_path`
- order 703: `resolve_optional_file_path` (function), lines 6975-6984, exports `resolve_optional_file_path`
- order 704: `resolve_skills_root_path` (function), lines 6985-6994, exports `resolve_skills_root_path`
- order 705: `_count_skill_markdown_files` (function), lines 6995-7008, exports `_count_skill_markdown_files`
- order 706: `select_preferred_skills_root` (function), lines 7009-7045, exports `select_preferred_skills_root`
- order 707: `load_web_ui_config_file` (function), lines 7046-7062, exports `load_web_ui_config_file`
- order 708: `extract_show_upload_list_setting` (function), lines 7063-7079, exports `extract_show_upload_list_setting`
- order 709: `extract_ui_style_setting` (function), lines 7080-7096, exports `extract_ui_style_setting`
- order 710: `extract_js_lib_download_setting` (function), lines 7097-7118, exports `extract_js_lib_download_setting`
- order 711: `extract_daily_session_limit_setting` (function), lines 7119-7164, exports `extract_daily_session_limit_setting`
- order 712: `extract_shell_command_timeout_setting` (function), lines 7165-7213, exports `extract_shell_command_timeout_setting`
- order 713: `normalize_shell_timeout_mode` (function), lines 7214-7231, exports `normalize_shell_timeout_mode`
- order 714: `extract_shell_timeout_mode_setting` (function), lines 7232-7244, exports `extract_shell_timeout_mode_setting`
- order 715: `extract_shell_async_handoff_setting` (function), lines 7245-7272, exports `extract_shell_async_handoff_setting`
- order 716: `extract_context_token_limit_setting` (function), lines 7273-7307, exports `extract_context_token_limit_setting`
- order 717: `normalize_auto_task_level_ceiling` (function), lines 7308-7329, exports `normalize_auto_task_level_ceiling`
- order 718: `normalize_l2_todo_policy` (function), lines 7330-7365, exports `normalize_l2_todo_policy`
- order 719: `extract_l2_todo_policy_setting` (function), lines 7366-7408, exports `extract_l2_todo_policy_setting`
- order 720: `extract_auto_task_level_ceiling_setting` (function), lines 7409-7438, exports `extract_auto_task_level_ceiling_setting`
- order 721: `normalize_read_context_policy` (function), lines 7439-7459, exports `normalize_read_context_policy`
- order 722: `normalize_tool_memory_policy` (function), lines 7460-7463, exports `normalize_tool_memory_policy`
- order 723: `extract_read_context_policy_setting` (function), lines 7464-7487, exports `extract_read_context_policy_setting`
- order 724: `extract_tool_memory_policy_setting` (function), lines 7488-7511, exports `extract_tool_memory_policy_setting`
- order 726: `default_multimodal_capabilities` (function), lines 7518-7528, exports `default_multimodal_capabilities`
- order 727: `_to_bool_like` (function), lines 7529-7541, exports `_to_bool_like`
- order 728: `extract_web_search_enabled_setting` (function), lines 7542-7554, exports `extract_web_search_enabled_setting`
- order 729: `_single_no_plan_todo_setting_sections` (function), lines 7555-7581, exports `_single_no_plan_todo_setting_sections`
- order 730: `_single_no_plan_todo_setting_present` (function), lines 7582-7607, exports `_single_no_plan_todo_setting_present`
- order 731: `extract_single_no_plan_todo_settings` (function), lines 7608-7654, exports `extract_single_no_plan_todo_settings`
- order 732: `normalize_user_memory_mode` (function), lines 7655-7685, exports `normalize_user_memory_mode`
- order 733: `user_memory_enabled_from_mode` (function), lines 7686-7689, exports `user_memory_enabled_from_mode`
- order 734: `extract_user_memory_mode_setting` (function), lines 7690-7729, exports `extract_user_memory_mode_setting`
- order 735: `set_web_search_enabled_on_runtime` (function), lines 7730-7745, exports `set_web_search_enabled_on_runtime`
- order 736: `infer_model_multimodal_capabilities` (function), lines 7746-7792, exports `infer_model_multimodal_capabilities`
- order 737: `parse_capability_overrides` (function), lines 7793-7832, exports `parse_capability_overrides`
- order 738: `merge_multimodal_capabilities` (function), lines 7833-7842, exports `merge_multimodal_capabilities`
- order 739: `parse_media_endpoints` (function), lines 7843-7859, exports `parse_media_endpoints`
- order 755: `extract_runtime_region_hint_setting` (function), lines 8037-8062, exports `extract_runtime_region_hint_setting`
- order 756: `extract_runtime_timezone_hint_setting` (function), lines 8063-8080, exports `extract_runtime_timezone_hint_setting`
- order 757: `runtime_environment_context_snapshot` (function), lines 8081-8130, exports `runtime_environment_context_snapshot`
- order 758: `runtime_environment_context_block` (function), lines 8131-8160, exports `runtime_environment_context_block`
- order 794: `load_offline_js_lib_index` (function), lines 8635-8645, exports `load_offline_js_lib_index`
- order 855: `resolve_ollama_model` (function), lines 12208-12219, exports `resolve_ollama_model`
- order 856: `infer_thinking_model` (function), lines 12220-12223, exports `infer_thinking_model`
- order 867: `extract_base_url` (function), lines 12433-12442, exports `extract_base_url`
- order 869: `infer_user_complexity_value` (function), lines 12454-12471, exports `infer_user_complexity_value`
- order 870: `normalize_task_complexity` (function), lines 12472-12501, exports `normalize_task_complexity`
- order 871: `task_complexity_rank` (function), lines 12502-12504, exports `task_complexity_rank`
- order 872: `task_complexity_at_least` (function), lines 12505-12507, exports `task_complexity_at_least`
- order 873: `max_task_complexity` (function), lines 12508-12518, exports `max_task_complexity`
- order 874: `normalize_openai_compat_provider_name` (function), lines 12519-12535, exports `normalize_openai_compat_provider_name`
- order 894: `resolve_reasoning_payload` (function), lines 12657-12707, exports `resolve_reasoning_payload`
- order 897: `extract_openai_compat_model_ids` (function), lines 12755-12789, exports `extract_openai_compat_model_ids`
- order 900: `load_llm_config_from_source` (function), lines 12822-12857, exports `load_llm_config_from_source`
- order 901: `parse_llm_config_profiles` (function), lines 12858-13488, exports `parse_llm_config_profiles`
- order 902: `looks_like_llm_config` (function), lines 13489-13566, exports `looks_like_llm_config`
- order 906: `parse_front_matter` (function), lines 13762-13990, exports `parse_front_matter`
- order 914: `normalize_liquid_kernel_startup_policy` (function), lines 14077-14081, exports `normalize_liquid_kernel_startup_policy`
- order 941: `normalize_upload_rel_path` (function), lines 15928-15962, exports `normalize_upload_rel_path`

### `ide/assets.py`

- order 1148: `IDE_INDEX_HTML` (constant), lines 114359-114514, exports `IDE_INDEX_HTML`
- order 1149: `IDE_CSS` (constant), lines 114515-114556, exports `IDE_CSS`
- order 1150: `IDE_JS` (constant), lines 114557-114750, exports `IDE_JS`
- order 1151: `IDE_CSS` (constant), lines 114751-114771, exports `IDE_CSS`
- order 1152: `IDE_JS` (constant), lines 114772-115035, exports `IDE_JS`
- order 1153: `IDE_JS` (constant), lines 115036-115164, exports `IDE_JS`
- order 1154: `IDE_JS` (constant), lines 115165-115388, exports `IDE_JS`
- order 1155: `IDE_JS` (constant), lines 115389-115487, exports `IDE_JS`

### `ide/auth.py`

- order 920: `IDEAuthError` (class), lines 14418-14425, exports `IDEAuthError`
- order 921: `IDEAuthStore` (class), lines 14426-15149, exports `IDEAuthStore`

### `ide/errors.py`

- order 922: `IDECapabilityError` (class), lines 15150-15156, exports `IDECapabilityError`
- order 923: `IDEFileConflict` (class), lines 15157-15164, exports `IDEFileConflict`

### `ide/events.py`

- order 811: `ide_public_operation_data` (function), lines 9247-9298, exports `ide_public_operation_data`

### `ide/handler.py`

- order 1185: `IdeHandler` (class), lines 132446-134101, exports `IdeHandler`

### `ide/preview.py`

- order 940: `normalize_rel_preview_path` (function), lines 15914-15927, exports `normalize_rel_preview_path`
- order 942: `is_code_preview_candidate` (function), lines 15963-15973, exports `is_code_preview_candidate`
- order 947: `preview_kind_for_path` (function), lines 15980-16009, exports `preview_kind_for_path`
- order 948: `normalize_markdown_preview_text` (function), lines 16010-16043, exports `normalize_markdown_preview_text`
- order 949: `_preview_markdown_value_html` (function), lines 16044-16064, exports `_preview_markdown_value_html`
- order 950: `_preview_markdown_frontmatter_html` (function), lines 16065-16080, exports `_preview_markdown_frontmatter_html`
- order 951: `_preview_markdown_task_lists` (function), lines 16081-16094, exports `_preview_markdown_task_lists`
- order 952: `_preview_markdown_fallback_inline` (function), lines 16095-16136, exports `_preview_markdown_fallback_inline`
- order 953: `_preview_markdown_fallback_html` (function), lines 16137-16233, exports `_preview_markdown_fallback_html`
- order 956: `workspace_file_revision_map` (function), lines 16274-16298, exports `workspace_file_revision_map`
- order 957: `workspace_revision_delta` (function), lines 16299-16305, exports `workspace_revision_delta`
- order 958: `build_code_preview_rows` (function), lines 16306-16354, exports `build_code_preview_rows`

### `ide/sandbox.py`

- order 763: `_windows_subprocess_encodings` (function), lines 8186-8203, exports `_windows_subprocess_encodings`
- order 1041: `_IDE_SANDBOX_BACKEND_CACHE` (assignment), lines 28614-28622, exports `_IDE_SANDBOX_BACKEND_CACHE`
- order 1042: `_IDE_SANDBOX_BACKEND_LOCK` (assignment), lines 28623-28623, exports `_IDE_SANDBOX_BACKEND_LOCK`
- order 1043: `WINDOWS_JOB_SANDBOX_MARKER` (constant), lines 28624-28624, exports `WINDOWS_JOB_SANDBOX_MARKER`
- order 1044: `_WINDOWS_LOW_INTEGRITY_ROOTS` (assignment), lines 28625-28625, exports `_WINDOWS_LOW_INTEGRITY_ROOTS`
- order 1045: `_WINDOWS_LOW_INTEGRITY_FAILED_ROOTS` (assignment), lines 28626-28626, exports `_WINDOWS_LOW_INTEGRITY_FAILED_ROOTS`
- order 1046: `_WINDOWS_LOW_INTEGRITY_LOCK` (assignment), lines 28627-28627, exports `_WINDOWS_LOW_INTEGRITY_LOCK`
- order 1047: `_is_windows_job_sandbox_prefix` (function), lines 28628-28634, exports `_is_windows_job_sandbox_prefix`
- order 1048: `_windows_builtin_sandbox_probe` (function), lines 28635-28658, exports `_windows_builtin_sandbox_probe`
- order 1049: `_windows_last_error` (function), lines 28659-28666, exports `_windows_last_error`
- order 1050: `_windows_set_integrity_label` (function), lines 28667-28720, exports `_windows_set_integrity_label`
- order 1051: `_windows_set_low_integrity_label` (function), lines 28721-28723, exports `_windows_set_low_integrity_label`
- order 1052: `_windows_protect_application_snapshot` (function), lines 28724-28747, exports `_windows_protect_application_snapshot`
- order 1053: `_windows_prepare_low_integrity_workspace` (function), lines 28748-28785, exports `_windows_prepare_low_integrity_workspace`
- order 1054: `_windows_job_memory_limit` (function), lines 28786-28793, exports `_windows_job_memory_limit`
- order 1055: `_windows_lower_process_integrity` (function), lines 28794-28841, exports `_windows_lower_process_integrity`
- order 1056: `_windows_attach_sandbox_job` (function), lines 28842-28934, exports `_windows_attach_sandbox_job`
- order 1057: `_windows_close_sandbox_job` (function), lines 28935-28951, exports `_windows_close_sandbox_job`
- order 1058: `_popen_windows_sandboxed` (function), lines 28952-28983, exports `_popen_windows_sandboxed`
- order 1059: `_run_windows_sandboxed_command` (function), lines 28984-29037, exports `_run_windows_sandboxed_command`
- order 1060: `_detect_ide_sandbox_backend` (function), lines 29038-29142, exports `_detect_ide_sandbox_backend`

### `llm/client.py`

- order 1026: `OllamaError` (class), lines 25362-25384, exports `OllamaError`
- order 1027: `OllamaClient` (class), lines 25385-27887, exports `OllamaClient`

### `llm/constants.py`

- order 122: `DEFAULT_OLLAMA_BASE_URL` (constant), lines 3822-3822, exports `DEFAULT_OLLAMA_BASE_URL`
- order 123: `DEFAULT_OLLAMA_MODEL` (constant), lines 3823-3823, exports `DEFAULT_OLLAMA_MODEL`
- order 875: `OPENAI_COMPAT_PROVIDER_NAMES` (constant), lines 12536-12545, exports `OPENAI_COMPAT_PROVIDER_NAMES`
- order 876: `OPENAI_LIKE_PROVIDER_NAMES` (constant), lines 12546-12547, exports `OPENAI_LIKE_PROVIDER_NAMES`
- order 879: `EFFORT_OFF` (constant), lines 12554-12565, exports `EFFORT_OFF`
- order 880: `EFFORT_LOW` (constant), lines 12566-12566, exports `EFFORT_LOW`
- order 881: `EFFORT_MEDIUM` (constant), lines 12567-12567, exports `EFFORT_MEDIUM`
- order 882: `EFFORT_HIGH` (constant), lines 12568-12568, exports `EFFORT_HIGH`
- order 883: `EFFORT_MAX` (constant), lines 12569-12569, exports `EFFORT_MAX`
- order 884: `EFFORT_LEVELS` (constant), lines 12570-12570, exports `EFFORT_LEVELS`
- order 885: `EFFORT_ORDER` (constant), lines 12571-12571, exports `EFFORT_ORDER`
- order 886: `EFFORT_DEFAULT` (constant), lines 12572-12572, exports `EFFORT_DEFAULT`
- order 887: `EFFORT_ANTHROPIC_BUDGET` (constant), lines 12573-12580, exports `EFFORT_ANTHROPIC_BUDGET`
- order 888: `EFFORT_OPENAI_REASONING` (constant), lines 12581-12587, exports `EFFORT_OPENAI_REASONING`
- order 889: `TASK_LEVEL_EFFORT` (constant), lines 12588-12597, exports `TASK_LEVEL_EFFORT`
- order 890: `ROLE_EFFORT_FLOOR` (constant), lines 12598-12603, exports `ROLE_EFFORT_FLOOR`
- order 891: `COORDINATION_EFFORT` (constant), lines 12604-12607, exports `COORDINATION_EFFORT`

### `llm/utils.py`

- order 848: `probe_ollama_environment` (function), lines 12139-12153, exports `probe_ollama_environment`
- order 849: `list_ollama_models` (function), lines 12154-12157, exports `list_ollama_models`
- order 850: `_OLLAMA_TAG_CACHE_LOCK` (assignment), lines 12158-12159, exports `_OLLAMA_TAG_CACHE_LOCK`
- order 851: `_OLLAMA_TAG_CACHE` (assignment), lines 12160-12160, exports `_OLLAMA_TAG_CACHE`
- order 854: `list_ollama_models_cached` (function), lines 12169-12207, exports `list_ollama_models_cached`
- order 857: `split_thinking_content` (function), lines 12224-12268, exports `split_thinking_content`
- order 858: `strip_thinking_content` (function), lines 12269-12271, exports `strip_thinking_content`
- order 859: `check_ollama_model_ready` (function), lines 12272-12297, exports `check_ollama_model_ready`
- order 860: `list_loaded_ollama_models` (function), lines 12298-12312, exports `list_loaded_ollama_models`
- order 861: `wake_ollama_model` (function), lines 12313-12344, exports `wake_ollama_model`
- order 862: `try_pull_ollama_model` (function), lines 12345-12363, exports `try_pull_ollama_model`
- order 863: `ordered_model_candidates` (function), lines 12364-12383, exports `ordered_model_candidates`
- order 864: `pick_working_ollama_model` (function), lines 12384-12401, exports `pick_working_ollama_model`
- order 868: `complete_chat_endpoint` (function), lines 12443-12453, exports `complete_chat_endpoint`
- order 877: `is_openai_compat_provider` (function), lines 12548-12550, exports `is_openai_compat_provider`
- order 878: `is_openai_like_provider` (function), lines 12551-12553, exports `is_openai_like_provider`
- order 892: `clamp_effort` (function), lines 12608-12619, exports `clamp_effort`
- order 893: `model_reasoning_style` (function), lines 12620-12656, exports `model_reasoning_style`
- order 895: `openai_compat_probe_headers` (function), lines 12708-12720, exports `openai_compat_probe_headers`
- order 896: `openai_compat_model_list_urls` (function), lines 12721-12754, exports `openai_compat_model_list_urls`
- order 898: `_is_http_url` (function), lines 12790-12803, exports `_is_http_url`
- order 899: `_resolve_local_path` (function), lines 12804-12821, exports `_resolve_local_path`

### `mcp/constants.py`

- order 176: `MCP_SERVICE_PORT_OFFSET` (constant), lines 4194-4194, exports `MCP_SERVICE_PORT_OFFSET`
- order 1006: `MCP_PROTOCOL_VERSION` (constant), lines 23980-24009, exports `MCP_PROTOCOL_VERSION`
- order 1007: `MCP_NAME_RE` (constant), lines 24010-24010, exports `MCP_NAME_RE`
- order 1008: `MCP_TOOL_PREFIX` (constant), lines 24011-24011, exports `MCP_TOOL_PREFIX`
- order 1009: `_MCP_DEFAULT_HANDSHAKE_TIMEOUT` (assignment), lines 24012-24012, exports `_MCP_DEFAULT_HANDSHAKE_TIMEOUT`
- order 1010: `_MCP_DEFAULT_CALL_TIMEOUT` (assignment), lines 24013-24013, exports `_MCP_DEFAULT_CALL_TIMEOUT`
- order 1011: `_MCP_MAX_RESULT_CHARS` (assignment), lines 24014-24014, exports `_MCP_MAX_RESULT_CHARS`
- order 1012: `_MCP_TRUST_STORE_VERSION` (assignment), lines 24015-24015, exports `_MCP_TRUST_STORE_VERSION`

### `mcp/driver.py`

- order 1013: `mcp_normalize_name` (function), lines 24016-24025, exports `mcp_normalize_name`
- order 1014: `mcp_normalize_server_configs` (function), lines 24026-24110, exports `mcp_normalize_server_configs`
- order 1015: `mcp_extract_server_configs` (function), lines 24111-24130, exports `mcp_extract_server_configs`
- order 1016: `_mcp_sha256_file` (function), lines 24131-24141, exports `_mcp_sha256_file`
- order 1017: `_mcp_file_identity` (function), lines 24142-24159, exports `_mcp_file_identity`
- order 1018: `mcp_workspace_identity` (function), lines 24160-24178, exports `mcp_workspace_identity`
- order 1019: `mcp_config_file_digest` (function), lines 24179-24186, exports `mcp_config_file_digest`
- order 1020: `mcp_default_trust_store_path` (function), lines 24187-24221, exports `mcp_default_trust_store_path`
- order 1021: `mcp_record_definition_fingerprint` (function), lines 24222-24236, exports `mcp_record_definition_fingerprint`
- order 1022: `_mcp_effective_spawn` (function), lines 24237-24324, exports `_mcp_effective_spawn`
- order 1023: `MCPWorkspaceTrustStore` (class), lines 24325-24386, exports `MCPWorkspaceTrustStore`
- order 1024: `MCPServerProcess` (class), lines 24387-24742, exports `MCPServerProcess`
- order 1025: `MCPManager` (class), lines 24743-25361, exports `MCPManager`

### `mcp/service.py`

- order 1187: `McpServiceHandler` (class), lines 134573-134790, exports `McpServiceHandler`

### `rag/assets.py`

- order 1142: `RAG_ADMIN_INDEX_HTML` (constant), lines 111752-111984, exports `RAG_ADMIN_INDEX_HTML`
- order 1143: `RAG_ADMIN_CSS` (constant), lines 111985-112088, exports `RAG_ADMIN_CSS`
- order 1144: `RAG_ADMIN_JS` (constant), lines 112089-114309, exports `RAG_ADMIN_JS`
- order 1145: `CODE_ADMIN_INDEX_HTML` (constant), lines 114310-114322, exports `CODE_ADMIN_INDEX_HTML`
- order 1146: `CODE_ADMIN_CSS` (constant), lines 114323-114353, exports `CODE_ADMIN_CSS`
- order 1147: `CODE_ADMIN_JS` (constant), lines 114354-114358, exports `CODE_ADMIN_JS`

### `rag/constants.py`

- order 172: `RAG_LIBRARY_DIRNAME` (constant), lines 4190-4190, exports `RAG_LIBRARY_DIRNAME`
- order 173: `RAG_ADMIN_PORT_OFFSET` (constant), lines 4191-4191, exports `RAG_ADMIN_PORT_OFFSET`
- order 174: `CODE_LIBRARY_DIRNAME` (constant), lines 4192-4192, exports `CODE_LIBRARY_DIRNAME`
- order 180: `WEB_SEARCH_INDEX_DIRNAME` (constant), lines 4201-4201, exports `WEB_SEARCH_INDEX_DIRNAME`
- order 182: `USER_MEMORY_DIRNAME` (constant), lines 4203-4203, exports `USER_MEMORY_DIRNAME`
- order 183: `USER_MEMORY_DB_FILENAME` (constant), lines 4204-4204, exports `USER_MEMORY_DB_FILENAME`
- order 184: `USER_MEMORY_PROFILE_FILENAME` (constant), lines 4205-4205, exports `USER_MEMORY_PROFILE_FILENAME`
- order 185: `USER_MEMORY_MODE_CHOICES` (constant), lines 4206-4206, exports `USER_MEMORY_MODE_CHOICES`
- order 187: `USER_MEMORY_WEAK_CAPSULE_CHARS` (constant), lines 4208-4208, exports `USER_MEMORY_WEAK_CAPSULE_CHARS`
- order 188: `USER_MEMORY_ON_CAPSULE_CHARS` (constant), lines 4209-4209, exports `USER_MEMORY_ON_CAPSULE_CHARS`
- order 189: `USER_MEMORY_CAPSULE_INJECT_CHARS` (constant), lines 4210-4213, exports `USER_MEMORY_CAPSULE_INJECT_CHARS`
- order 190: `USER_MEMORY_MAX_SUMMARY_CHARS` (constant), lines 4214-4214, exports `USER_MEMORY_MAX_SUMMARY_CHARS`
- order 191: `USER_MEMORY_QUERY_LIMIT` (constant), lines 4215-4215, exports `USER_MEMORY_QUERY_LIMIT`
- order 192: `USER_MEMORY_DECAY_HALFLIFE_DAYS` (constant), lines 4216-4216, exports `USER_MEMORY_DECAY_HALFLIFE_DAYS`
- order 193: `USER_MEMORY_PROFILE_SCHEMA_VERSION` (constant), lines 4217-4217, exports `USER_MEMORY_PROFILE_SCHEMA_VERSION`
- order 213: `WEB_SEARCH_CONTEXT_REGISTRY_MAX` (constant), lines 4239-4239, exports `WEB_SEARCH_CONTEXT_REGISTRY_MAX`
- order 214: `WEB_SEARCH_CONTEXT_PROMPT_MAX_ITEMS` (constant), lines 4240-4240, exports `WEB_SEARCH_CONTEXT_PROMPT_MAX_ITEMS`
- order 215: `WEB_SEARCH_CONTEXT_PROMPT_MAX_CHARS` (constant), lines 4241-4241, exports `WEB_SEARCH_CONTEXT_PROMPT_MAX_CHARS`
- order 216: `WEB_SEARCH_CONTEXT_NODE_MAX` (constant), lines 4242-4242, exports `WEB_SEARCH_CONTEXT_NODE_MAX`
- order 217: `WEB_SEARCH_CONTEXT_URL_MAX` (constant), lines 4243-4243, exports `WEB_SEARCH_CONTEXT_URL_MAX`
- order 218: `RAG_CHUNK_CHARS` (constant), lines 4244-4244, exports `RAG_CHUNK_CHARS`
- order 219: `RAG_CHUNK_OVERLAP` (constant), lines 4245-4245, exports `RAG_CHUNK_OVERLAP`
- order 220: `RAG_MAX_CHUNKS_PER_DOC` (constant), lines 4246-4248, exports `RAG_MAX_CHUNKS_PER_DOC`
- order 221: `RAG_MAX_DOCUMENT_CHARS` (constant), lines 4249-4259, exports `RAG_MAX_DOCUMENT_CHARS`
- order 226: `RAG_MAX_QUERY_RESULTS` (constant), lines 4273-4273, exports `RAG_MAX_QUERY_RESULTS`
- order 227: `RAG_HIGH_RECALL_POOL_MULTIPLIER` (constant), lines 4274-4274, exports `RAG_HIGH_RECALL_POOL_MULTIPLIER`
- order 228: `RAG_HIGH_RECALL_MIN_POOL` (constant), lines 4275-4275, exports `RAG_HIGH_RECALL_MIN_POOL`
- order 229: `RAG_RETRIEVAL_MAX_PER_DOC` (constant), lines 4276-4276, exports `RAG_RETRIEVAL_MAX_PER_DOC`
- order 230: `RAG_BM25_K1` (constant), lines 4277-4280, exports `RAG_BM25_K1`
- order 231: `RAG_BM25_B` (constant), lines 4281-4281, exports `RAG_BM25_B`
- order 232: `RAG_BM25_SATURATION` (constant), lines 4282-4288, exports `RAG_BM25_SATURATION`
- order 233: `RAG_SYMBOL_EXACT_BOOST` (constant), lines 4289-4292, exports `RAG_SYMBOL_EXACT_BOOST`
- order 234: `RAG_INDEX_SNAPSHOT_FORMAT` (constant), lines 4293-4296, exports `RAG_INDEX_SNAPSHOT_FORMAT`
- order 235: `RAG_GRAPH_MAX_NODES` (constant), lines 4297-4297, exports `RAG_GRAPH_MAX_NODES`
- order 236: `RAG_TASK_HISTORY_LIMIT` (constant), lines 4298-4298, exports `RAG_TASK_HISTORY_LIMIT`
- order 237: `RAG_MODEL_MEDIA_MAX_BYTES` (constant), lines 4299-4299, exports `RAG_MODEL_MEDIA_MAX_BYTES`
- order 238: `RAG_MAX_IMPORT_FILES` (constant), lines 4300-4300, exports `RAG_MAX_IMPORT_FILES`
- order 239: `RAG_MAX_IMPORT_BATCH_ITEMS` (constant), lines 4301-4301, exports `RAG_MAX_IMPORT_BATCH_ITEMS`
- order 240: `RAG_MAX_IMPORT_BATCH_BYTES` (constant), lines 4302-4302, exports `RAG_MAX_IMPORT_BATCH_BYTES`
- order 241: `RAG_PDF_IMAGE_LIMIT` (constant), lines 4303-4303, exports `RAG_PDF_IMAGE_LIMIT`
- order 242: `RAG_QUERY_CONTEXT_CHARS` (constant), lines 4304-4304, exports `RAG_QUERY_CONTEXT_CHARS`
- order 243: `RAG_MAX_GLOBAL_COMMUNITIES` (constant), lines 4305-4305, exports `RAG_MAX_GLOBAL_COMMUNITIES`
- order 244: `RAG_MAX_COMMUNITY_MAP_SUPPORT` (constant), lines 4306-4306, exports `RAG_MAX_COMMUNITY_MAP_SUPPORT`
- order 245: `RAG_INCLUDE_FILENAME_ENTITIES_DEFAULT` (constant), lines 4307-4307, exports `RAG_INCLUDE_FILENAME_ENTITIES_DEFAULT`
- order 246: `RAG_DYNAMIC_NOISE_MIN_DOC_FREQ` (constant), lines 4308-4308, exports `RAG_DYNAMIC_NOISE_MIN_DOC_FREQ`
- order 247: `RAG_DYNAMIC_NOISE_MIN_COMMUNITY_FREQ` (constant), lines 4309-4309, exports `RAG_DYNAMIC_NOISE_MIN_COMMUNITY_FREQ`
- order 248: `RAG_DYNAMIC_NOISE_SOFT_DOC_RATIO` (constant), lines 4310-4310, exports `RAG_DYNAMIC_NOISE_SOFT_DOC_RATIO`
- order 249: `RAG_DYNAMIC_NOISE_HARD_DOC_RATIO` (constant), lines 4311-4311, exports `RAG_DYNAMIC_NOISE_HARD_DOC_RATIO`
- order 250: `RAG_DYNAMIC_NOISE_SOFT_COMMUNITY_RATIO` (constant), lines 4312-4312, exports `RAG_DYNAMIC_NOISE_SOFT_COMMUNITY_RATIO`
- order 251: `RAG_DYNAMIC_NOISE_HARD_COMMUNITY_RATIO` (constant), lines 4313-4313, exports `RAG_DYNAMIC_NOISE_HARD_COMMUNITY_RATIO`
- order 252: `RAG_MIN_SYNTHESIS_SCORE` (constant), lines 4314-4314, exports `RAG_MIN_SYNTHESIS_SCORE`
- order 253: `RAG_NO_EVIDENCE_THRESHOLD` (constant), lines 4315-4315, exports `RAG_NO_EVIDENCE_THRESHOLD`
- order 254: `RAG_WEAK_MATCH_SCORE_CAP` (constant), lines 4316-4316, exports `RAG_WEAK_MATCH_SCORE_CAP`
- order 255: `RAG_SYNTHESIS_MAX_PER_DOC` (constant), lines 4317-4317, exports `RAG_SYNTHESIS_MAX_PER_DOC`
- order 256: `RAG_WORKFLOW_ACCEPT_SCORE` (constant), lines 4318-4318, exports `RAG_WORKFLOW_ACCEPT_SCORE`
- order 257: `RAG_NO_EVIDENCE_MESSAGE` (constant), lines 4319-4319, exports `RAG_NO_EVIDENCE_MESSAGE`
- order 258: `RAG_CONTEXT_BUDGETS` (constant), lines 4320-4324, exports `RAG_CONTEXT_BUDGETS`
- order 259: `RAG_WEAK_EVIDENCE_MESSAGE` (constant), lines 4325-4325, exports `RAG_WEAK_EVIDENCE_MESSAGE`
- order 260: `RAG_EVIDENCE_SCHEMA_VERSION` (constant), lines 4326-4326, exports `RAG_EVIDENCE_SCHEMA_VERSION`
- order 261: `RAG_EVIDENCE_BATCH_CHARS` (constant), lines 4327-4330, exports `RAG_EVIDENCE_BATCH_CHARS`
- order 262: `RAG_EVALUATION_SUMMARY_CHARS` (constant), lines 4331-4334, exports `RAG_EVALUATION_SUMMARY_CHARS`
- order 263: `RAG_DENSE_DEFAULT_ENABLED` (constant), lines 4335-4335, exports `RAG_DENSE_DEFAULT_ENABLED`
- order 264: `RAG_EMBEDDING_MODE_VALUES` (constant), lines 4336-4336, exports `RAG_EMBEDDING_MODE_VALUES`
- order 265: `RAG_IMPORT_WORKER_COUNT` (constant), lines 4337-4340, exports `RAG_IMPORT_WORKER_COUNT`
- order 267: `RAG_PARSE_TIMEOUT_SECONDS` (constant), lines 4345-4348, exports `RAG_PARSE_TIMEOUT_SECONDS`
- order 1074: `RAG_TERM_GROUPS` (constant), lines 98746-103379, exports `RAG_TERM_GROUPS`
- order 1075: `RAG_RESEARCH_HINTS` (constant), lines 103380-103401, exports `RAG_RESEARCH_HINTS`
- order 1076: `RAG_CODE_HINTS` (constant), lines 103402-103412, exports `RAG_CODE_HINTS`
- order 1077: `RAG_SHORT_TOKEN_ALLOWLIST` (constant), lines 103413-103428, exports `RAG_SHORT_TOKEN_ALLOWLIST`
- order 1078: `RAG_EN_STOPWORDS` (constant), lines 103429-103501, exports `RAG_EN_STOPWORDS`
- order 1079: `RAG_ZH_STOPWORDS` (constant), lines 103502-103538, exports `RAG_ZH_STOPWORDS`
- order 1080: `RAG_GENERIC_ENTITY_TERMS_EN` (constant), lines 103539-103617, exports `RAG_GENERIC_ENTITY_TERMS_EN`
- order 1081: `RAG_GENERIC_ENTITY_TERMS_ZH` (constant), lines 103618-103660, exports `RAG_GENERIC_ENTITY_TERMS_ZH`
- order 1082: `RAG_STRUCTURAL_ENTITY_PATTERNS` (constant), lines 103661-103679, exports `RAG_STRUCTURAL_ENTITY_PATTERNS`
- order 1114: `CODE_LIBRARY_IGNORED_DIRS` (constant), lines 104637-104646, exports `CODE_LIBRARY_IGNORED_DIRS`
- order 1115: `CODE_LIBRARY_LANGUAGE_BY_EXT` (constant), lines 104647-104703, exports `CODE_LIBRARY_LANGUAGE_BY_EXT`
- order 1116: `CODE_LIBRARY_SPECIAL_FILENAMES` (constant), lines 104704-104710, exports `CODE_LIBRARY_SPECIAL_FILENAMES`

### `rag/index.py`

- order 1119: `_code_module_name` (function), lines 104735-104751, exports `_code_module_name`
- order 1120: `_code_choose_community` (function), lines 104752-104761, exports `_code_choose_community`
- order 1121: `_code_query_terms` (function), lines 104762-104776, exports `_code_query_terms`
- order 1130: `TFGraphIDFIndex` (class), lines 105907-107601, exports `TFGraphIDFIndex`
- order 1139: `CodeGraphIndex` (class), lines 110884-111372, exports `CodeGraphIndex`

### `rag/ingestion.py`

- order 1098: `_rag_trigram_set` (function), lines 104057-104064, exports `_rag_trigram_set`
- order 1099: `_rag_jaccard_sim` (function), lines 104065-104074, exports `_rag_jaccard_sim`
- order 1100: `_rag_mmr_select` (function), lines 104075-104124, exports `_rag_mmr_select`
- order 1105: `_rag_embed_text` (function), lines 104259-104282, exports `_rag_embed_text`
- order 1106: `_rag_embed_batch` (function), lines 104283-104291, exports `_rag_embed_batch`
- order 1107: `_rag_window_for_query` (function), lines 104292-104306, exports `_rag_window_for_query`
- order 1108: `_rag_focused_excerpt` (function), lines 104307-104349, exports `_rag_focused_excerpt`
- order 1109: `_rag_query_variants` (function), lines 104350-104389, exports `_rag_query_variants`
- order 1110: `_rag_parse_segments` (function), lines 104390-104452, exports `_rag_parse_segments`
- order 1111: `_rag_boundary_split` (function), lines 104453-104510, exports `_rag_boundary_split`
- order 1137: `_rag_parse_file_worker` (function), lines 109985-110001, exports `_rag_parse_file_worker`
- order 1138: `RAGIngestionService` (class), lines 110002-110883, exports `RAGIngestionService`
- order 1141: `CodeIngestionService` (class), lines 111664-111751, exports `CodeIngestionService`

### `rag/parsers.py`

- order 1083: `EvidenceRecord` (class), lines 103680-103714, exports `EvidenceRecord`
- order 1084: `_rag_float` (function), lines 103715-103721, exports `_rag_float`
- order 1085: `_rag_evidence_source_type` (function), lines 103722-103738, exports `_rag_evidence_source_type`
- order 1086: `_rag_normalize_evidence_record` (function), lines 103739-103794, exports `_rag_normalize_evidence_record`
- order 1087: `_rag_validate_evidence_record` (function), lines 103795-103837, exports `_rag_validate_evidence_record`
- order 1088: `_rag_evidence_batches` (function), lines 103838-103855, exports `_rag_evidence_batches`
- order 1089: `_rag_safe_name` (function), lines 103856-103861, exports `_rag_safe_name`
- order 1090: `_rag_detect_language` (function), lines 103862-103878, exports `_rag_detect_language`
- order 1091: `_rag_cjk_ngrams` (function), lines 103879-103893, exports `_rag_cjk_ngrams`
- order 1092: `_rag_is_noise_token` (function), lines 103894-103915, exports `_rag_is_noise_token`
- order 1093: `_rag_entity_allowed` (function), lines 103916-103930, exports `_rag_entity_allowed`
- order 1094: `_rag_filter_entities` (function), lines 103931-103947, exports `_rag_filter_entities`
- order 1095: `_rag_filename_entity_aliases` (function), lines 103948-103983, exports `_rag_filename_entity_aliases`
- order 1096: `_rag_apply_filename_entity_policy` (function), lines 103984-104016, exports `_rag_apply_filename_entity_policy`
- order 1097: `_rag_choose_community` (function), lines 104017-104056, exports `_rag_choose_community`
- order 1101: `_rag_tokenize` (function), lines 104125-104178, exports `_rag_tokenize`
- order 1102: `_rag_expand_tokens` (function), lines 104179-104202, exports `_rag_expand_tokens`
- order 1103: `_rag_extract_entities` (function), lines 104203-104221, exports `_rag_extract_entities`
- order 1104: `_rag_classify_document` (function), lines 104222-104258, exports `_rag_classify_document`
- order 1112: `_rag_structure_outline` (function), lines 104511-104549, exports `_rag_structure_outline`
- order 1113: `_rag_chunk_text` (function), lines 104550-104636, exports `_rag_chunk_text`
- order 1117: `_code_language_from_name` (function), lines 104711-104729, exports `_code_language_from_name`
- order 1118: `_code_is_test_path` (function), lines 104730-104734, exports `_code_is_test_path`
- order 1122: `_CallCollector` (class), lines 104777-104791, exports `_CallCollector`
- order 1123: `_ALGO_COMPLEXITY_RE` (assignment), lines 104792-104794, exports `_ALGO_COMPLEXITY_RE`
- order 1124: `_ALGO_STEP_RE` (assignment), lines 104795-104795, exports `_ALGO_STEP_RE`
- order 1125: `_ALGO_MATH_VARS` (assignment), lines 104796-104796, exports `_ALGO_MATH_VARS`
- order 1126: `_ALGO_DOC_KEYWORDS` (assignment), lines 104797-104797, exports `_ALGO_DOC_KEYWORDS`
- order 1127: `_detect_algo_chunk` (function), lines 104798-104823, exports `_detect_algo_chunk`
- order 1128: `CodeContentParser` (class), lines 104824-105390, exports `CodeContentParser`
- order 1129: `RAGContentParser` (class), lines 105391-105906, exports `RAGContentParser`

### `rag/store.py`

- order 1131: `RAGLibraryStore` (class), lines 107602-108240, exports `RAGLibraryStore`
- order 1132: `WikiStore` (class), lines 108241-108796, exports `WikiStore`
- order 1133: `UserMemoryStore` (class), lines 108797-109472, exports `UserMemoryStore`
- order 1134: `UserInteractionOptimizer` (class), lines 109473-109541, exports `UserInteractionOptimizer`
- order 1135: `UserIntentProfiler` (class), lines 109542-109583, exports `UserIntentProfiler`
- order 1136: `WorkflowMemoryStore` (class), lines 109584-109984, exports `WorkflowMemoryStore`
- order 1140: `CodeLibraryStore` (class), lines 111373-111663, exports `CodeLibraryStore`

### `rag/web_search.py`

- order 814: `_agent_web_bool` (function), lines 9333-9340, exports `_agent_web_bool`
- order 815: `_agent_web_int` (function), lines 9341-9348, exports `_agent_web_int`
- order 816: `_agent_web_host_is_local_name` (function), lines 9349-9355, exports `_agent_web_host_is_local_name`
- order 817: `_agent_web_ip_is_blocked` (function), lines 9356-9370, exports `_agent_web_ip_is_blocked`
- order 818: `_agent_web_canonical_url` (function), lines 9371-9400, exports `_agent_web_canonical_url`
- order 819: `_agent_web_domain_to_seed` (function), lines 9401-9412, exports `_agent_web_domain_to_seed`
- order 820: `_agent_web_query_terms` (function), lines 9413-9430, exports `_agent_web_query_terms`
- order 821: `_agent_web_query_domain_hints` (function), lines 9431-9471, exports `_agent_web_query_domain_hints`
- order 822: `_agent_web_query_needs_fresh_network` (function), lines 9472-9494, exports `_agent_web_query_needs_fresh_network`
- order 823: `_agent_web_extract_text_snippet` (function), lines 9495-9512, exports `_agent_web_extract_text_snippet`
- order 824: `AgentWebHTMLParser` (class), lines 9513-9592, exports `AgentWebHTMLParser`
- order 825: `_agent_web_decompress_bytes` (function), lines 9593-9616, exports `_agent_web_decompress_bytes`
- order 826: `_agent_web_charset_candidates` (function), lines 9617-9675, exports `_agent_web_charset_candidates`
- order 827: `_agent_web_decode_text_bytes` (function), lines 9676-9710, exports `_agent_web_decode_text_bytes`
- order 828: `AgentWebSearchEngine` (class), lines 9711-11491, exports `AgentWebSearchEngine`

### `server/http.py`

- order 690: `admin_language_payload` (function), lines 6352-6363, exports `admin_language_payload`
- order 803: `_UI_TRUNCATION_MARKER` (assignment), lines 8952-8954, exports `_UI_TRUNCATION_MARKER`
- order 804: `_ui_trim_text` (function), lines 8955-8963, exports `_ui_trim_text`
- order 805: `_bounded_ui_value` (function), lines 8964-9024, exports `_bounded_ui_value`
- order 806: `_bounded_ui_row` (function), lines 9025-9076, exports `_bounded_ui_row`
- order 807: `_bounded_ui_rows` (function), lines 9077-9125, exports `_bounded_ui_rows`
- order 808: `_enforce_ui_payload_budget` (function), lines 9126-9170, exports `_enforce_ui_payload_budget`
- order 809: `_apply_lite_snapshot_bounds` (function), lines 9171-9226, exports `_apply_lite_snapshot_bounds`
- order 1176: `AgentHTTPServer` (class), lines 128137-128176, exports `AgentHTTPServer`
- order 1179: `Handler` (class), lines 129363-131130, exports `Handler`
- order 1182: `SkillsReviewHandler` (class), lines 131932-132045, exports `SkillsReviewHandler`
- order 1186: `CollaborationHandler` (class), lines 134102-134572, exports `CollaborationHandler`

### `server/rag_admin.py`

- order 1181: `_RagAdminAuthMixin` (class), lines 131774-131931, exports `_RagAdminAuthMixin`
- order 1183: `RagAdminHandler` (class), lines 132046-132246, exports `RagAdminHandler`
- order 1184: `CodeAdminHandler` (class), lines 132247-132445, exports `CodeAdminHandler`

### `server/skills.py`

- order 1180: `SkillsHandler` (class), lines 131131-131773, exports `SkillsHandler`

### `session/manager.py`

- order 725: `SessionCreationLimitExceeded` (class), lines 7512-7517, exports `SessionCreationLimitExceeded`
- order 1062: `SessionManager` (class), lines 89605-91947, exports `SessionManager`

### `session/state.py`

- order 1061: `SessionState` (class), lines 29143-89604, exports `SessionState`

### `skills/embedded.py`

- order 961: `EMBEDDED_SKILLS_ARCHIVE_B64` (constant), lines 16771-16772, exports `EMBEDDED_SKILLS_ARCHIVE_B64`
- order 962: `EMBEDDED_SKILLS_ARCHIVE_SHA256` (constant), lines 16773-16773, exports `EMBEDDED_SKILLS_ARCHIVE_SHA256`
- order 963: `EMBEDDED_SKILLS_ARCHIVE_FILES` (constant), lines 16774-16796, exports `EMBEDDED_SKILLS_ARCHIVE_FILES`
- order 988: `BUILTIN_CLAWHUB_SKILLS_VERSION` (constant), lines 20032-20034, exports `BUILTIN_CLAWHUB_SKILLS_VERSION`
- order 989: `EMBEDDED_CLAWHUB_SKILLS_ARCHIVE_B64` (constant), lines 20035-20280, exports `EMBEDDED_CLAWHUB_SKILLS_ARCHIVE_B64`
- order 991: `MCP_BUILDER_SKILL_MD` (constant), lines 20328-20502, exports `MCP_BUILDER_SKILL_MD`
- order 994: `SKILL_PROTOCOL_LOCAL` (constant), lines 20534-20535, exports `SKILL_PROTOCOL_LOCAL`
- order 995: `SKILL_PROTOCOL_CLAWHUB` (constant), lines 20536-20536, exports `SKILL_PROTOCOL_CLAWHUB`
- order 996: `SKILL_PROTOCOL_HTTP_JSON` (constant), lines 20537-20537, exports `SKILL_PROTOCOL_HTTP_JSON`
- order 997: `SKILL_PROTOCOL_SPECS` (constant), lines 20538-20570, exports `SKILL_PROTOCOL_SPECS`

### `skills/provisioning.py`

- order 964: `ensure_embedded_skills_at_root` (function), lines 16797-16862, exports `ensure_embedded_skills_at_root`
- order 965: `ensure_embedded_skills` (function), lines 16863-16866, exports `ensure_embedded_skills`
- order 967: `detect_upload_parser_capabilities` (function), lines 16873-16889, exports `detect_upload_parser_capabilities`
- order 968: `_render_cap_markdown` (function), lines 16890-16905, exports `_render_cap_markdown`
- order 969: `_write_text_if_changed` (function), lines 16906-16912, exports `_write_text_if_changed`
- order 970: `ensure_generated_document_skills` (function), lines 16913-17002, exports `ensure_generated_document_skills`
- order 971: `ensure_generated_image_coding_feedback_skill` (function), lines 17003-17103, exports `ensure_generated_image_coding_feedback_skill`
- order 972: `_skill_knowledge_files` (function), lines 17104-17124, exports `_skill_knowledge_files`
- order 973: `analyze_skill_building_knowledge` (function), lines 17125-17180, exports `analyze_skill_building_knowledge`
- order 974: `_sanitize_skill_slug` (function), lines 17181-17184, exports `_sanitize_skill_slug`
- order 975: `_build_skills_gen_skill_content` (function), lines 17185-17217, exports `_build_skills_gen_skill_content`
- order 976: `ensure_generated_skills_gen_skill` (function), lines 17218-17223, exports `ensure_generated_skills_gen_skill`
- order 977: `ensure_generated_execution_recovery_skill` (function), lines 17224-17308, exports `ensure_generated_execution_recovery_skill`
- order 978: `ensure_generated_systematic_debugging_skill` (function), lines 17309-17582, exports `ensure_generated_systematic_debugging_skill`
- order 979: `ensure_generated_code_engineering_mastery_skill` (function), lines 17583-17702, exports `ensure_generated_code_engineering_mastery_skill`
- order 980: `ensure_generated_smart_file_navigation_skill` (function), lines 17703-17819, exports `ensure_generated_smart_file_navigation_skill`
- order 981: `ensure_generated_html_frontend_report_skills` (function), lines 17820-18028, exports `ensure_generated_html_frontend_report_skills`
- order 982: `ensure_generated_deep_research_skills` (function), lines 18029-18298, exports `ensure_generated_deep_research_skills`
- order 983: `ensure_generated_research_scientific_skills` (function), lines 18299-18936, exports `ensure_generated_research_scientific_skills`
- order 984: `ensure_generated_rag_mastery_skills` (function), lines 18937-19238, exports `ensure_generated_rag_mastery_skills`
- order 985: `ensure_generated_multimodal_comprehension_skills` (function), lines 19239-19933, exports `ensure_generated_multimodal_comprehension_skills`
- order 986: `ensure_generated_runtime_skills_manifest` (function), lines 19934-19968, exports `ensure_generated_runtime_skills_manifest`
- order 987: `ensure_generated_agent_web_search_skill` (function), lines 19969-20031, exports `ensure_generated_agent_web_search_skill`
- order 990: `ensure_embedded_clawhub_skills` (function), lines 20281-20327, exports `ensure_embedded_clawhub_skills`
- order 992: `ensure_generated_mcp_builder_skill` (function), lines 20503-20514, exports `ensure_generated_mcp_builder_skill`
- order 993: `ensure_runtime_skills` (function), lines 20515-20533, exports `ensure_runtime_skills`

### `skills/store.py`

- order 998: `_BUILTIN_SKILLS` (assignment), lines 20571-20679, exports `_BUILTIN_SKILLS`
- order 999: `SkillStore` (class), lines 20680-22573, exports `SkillStore`

### `skills/studio.py`

- order 1164: `SkillsStudioError` (class), lines 115513-115522, exports `SkillsStudioError`
- order 1165: `_studio_slug` (function), lines 115523-115538, exports `_studio_slug`
- order 1166: `_studio_hash` (function), lines 115539-115542, exports `_studio_hash`
- order 1167: `_studio_cookie_value` (function), lines 115543-115552, exports `_studio_cookie_value`
- order 1168: `SkillsStudioStore` (class), lines 115553-117410, exports `SkillsStudioStore`

### `utils/compress.py`

- order 832: `compress_text_blob` (function), lines 11656-11662, exports `compress_text_blob`
- order 833: `decompress_text_blob` (function), lines 11663-11672, exports `decompress_text_blob`

### `utils/crypto.py`

- order 905: `CryptoBox` (class), lines 13608-13761, exports `CryptoBox`

### `utils/errors.py`

- order 852: `EmptyActionError` (class), lines 12161-12164, exports `EmptyActionError`
- order 1001: `ProcessManagerError` (class), lines 22709-22714, exports `ProcessManagerError`

### `utils/files.py`

- order 684: `_normalize_js_lib_asset_ref` (function), lines 6222-6237, exports `_normalize_js_lib_asset_ref`
- order 685: `_resolve_js_lib_asset_path` (function), lines 6238-6269, exports `_resolve_js_lib_asset_path`
- order 686: `_discover_extra_js_lib_files` (function), lines 6270-6302, exports `_discover_extra_js_lib_files`
- order 778: `safe_path` (function), lines 8365-8375, exports `safe_path`
- order 779: `_safe_js_filename` (function), lines 8376-8384, exports `_safe_js_filename`
- order 780: `_sha256_bytes` (function), lines 8385-8387, exports `_sha256_bytes`
- order 781: `_sha256_file` (function), lines 8388-8397, exports `_sha256_file`
- order 782: `_download_http_bytes` (function), lines 8398-8407, exports `_download_http_bytes`
- order 783: `offline_js_lib_root` (function), lines 8408-8410, exports `offline_js_lib_root`
- order 784: `_offline_js_entry_relative_path` (function), lines 8411-8416, exports `_offline_js_entry_relative_path`
- order 785: `_archive_member_relative_path` (function), lines 8417-8427, exports `_archive_member_relative_path`
- order 786: `_path_size_bytes` (function), lines 8428-8444, exports `_path_size_bytes`
- order 787: `_extract_archive_to_dir` (function), lines 8445-8486, exports `_extract_archive_to_dir`
- order 788: `_package_required_paths` (function), lines 8487-8494, exports `_package_required_paths`
- order 789: `_package_required_globs` (function), lines 8495-8511, exports `_package_required_globs`
- order 790: `_package_install_ready` (function), lines 8512-8534, exports `_package_install_ready`
- order 791: `_postprocess_offline_js_package` (function), lines 8535-8571, exports `_postprocess_offline_js_package`
- order 792: `_ensure_offline_js_package` (function), lines 8572-8616, exports `_ensure_offline_js_package`
- order 793: `_render_offline_js_catalog_md` (function), lines 8617-8634, exports `_render_offline_js_catalog_md`
- order 795: `ensure_offline_js_libs` (function), lines 8646-8804, exports `ensure_offline_js_libs`
- order 796: `_offline_js_catalog_entry_for_asset` (function), lines 8805-8825, exports `_offline_js_catalog_entry_for_asset`
- order 797: `ensure_offline_js_asset` (function), lines 8826-8883, exports `ensure_offline_js_asset`
- order 798: `_normalize_external_js_url` (function), lines 8884-8889, exports `_normalize_external_js_url`
- order 799: `is_external_js_src` (function), lines 8890-8893, exports `is_external_js_src`
- order 800: `match_offline_js_catalog_by_url` (function), lines 8894-8911, exports `match_offline_js_catalog_by_url`
- order 801: `cache_external_js_url` (function), lines 8912-8947, exports `cache_external_js_url`
- order 908: `try_read_text` (function), lines 14005-14014, exports `try_read_text`

### `utils/http.py`

- order 119: `_URL_OPEN_ORIGINAL` (assignment), lines 3819-3819, exports `_URL_OPEN_ORIGINAL`
- order 120: `_HTTP_SSL_CONTEXT` (assignment), lines 3820-3820, exports `_HTTP_SSL_CONTEXT`
- order 147: `_shared_http_ssl_context` (function), lines 3884-3907, exports `_shared_http_ssl_context`
- order 148: `urlopen` (function), lines 3908-3917, exports `urlopen`
- order 771: `json_response_bytes` (function), lines 8310-8312, exports `json_response_bytes`
- order 772: `read_http_json_body` (function), lines 8313-8326, exports `read_http_json_body`
- order 773: `close_if_http_request_body_unread` (function), lines 8327-8340, exports `close_if_http_request_body_unread`

### `utils/json_utils.py`

- order 171: `JSON_FSYNC_ENABLED` (constant), lines 4189-4189, exports `JSON_FSYNC_ENABLED`
- order 770: `json_dumps` (function), lines 8306-8309, exports `json_dumps`
- order 842: `parse_tool_arguments` (function), lines 11966-11976, exports `parse_tool_arguments`
- order 843: `repair_truncated_json_object` (function), lines 11977-12031, exports `repair_truncated_json_object`
- order 844: `parse_tool_arguments_with_error` (function), lines 12032-12063, exports `parse_tool_arguments_with_error`
- order 845: `_is_valid_json_object` (function), lines 12064-12069, exports `_is_valid_json_object`
- order 846: `_scan_top_level_json_objects` (function), lines 12070-12093, exports `_scan_top_level_json_objects`
- order 847: `reconstruct_streamed_tool_args` (function), lines 12094-12138, exports `reconstruct_streamed_tool_args`
- order 865: `parse_json_object` (function), lines 12402-12408, exports `parse_json_object`
- order 866: `extract_json_object_from_text` (function), lines 12409-12432, exports `extract_json_object_from_text`
- order 909: `_json_default_copy` (function), lines 14015-14021, exports `_json_default_copy`
- order 910: `_read_json_file` (function), lines 14022-14043, exports `_read_json_file`
- order 911: `_write_json_file` (function), lines 14044-14072, exports `_write_json_file`

### `utils/media.py`

- order 677: `_capability_probe_png_bytes` (function), lines 5860-5874, exports `_capability_probe_png_bytes`
- order 678: `_capability_probe_audio_bytes` (function), lines 5875-5886, exports `_capability_probe_audio_bytes`
- order 679: `_capability_probe_video_bytes` (function), lines 5887-5891, exports `_capability_probe_video_bytes`
- order 740: `guess_mime_from_name` (function), lines 7860-7864, exports `guess_mime_from_name`
- order 741: `_convert_image_to_safe_format` (function), lines 7865-7884, exports `_convert_image_to_safe_format`
- order 742: `guess_ext_from_mime` (function), lines 7885-7893, exports `guess_ext_from_mime`

### `utils/misc.py`

- order 743: `now_ts` (function), lines 7894-7896, exports `now_ts`
- order 744: `_benign_socket_log_lock` (assignment), lines 7897-7899, exports `_benign_socket_log_lock`
- order 745: `_benign_socket_log_state` (assignment), lines 7900-7900, exports `_benign_socket_log_state`
- order 747: `is_benign_socket_error` (function), lines 7916-7936, exports `is_benign_socket_error`
- order 748: `_socket_error_code` (function), lines 7937-7948, exports `_socket_error_code`
- order 749: `_log_benign_socket_error_limited` (function), lines 7949-7985, exports `_log_benign_socket_error_limited`
- order 750: `swallow_benign_socket_error` (function), lines 7986-7992, exports `swallow_benign_socket_error`
- order 751: `normalize_timeout_seconds` (function), lines 7993-8008, exports `normalize_timeout_seconds`
- order 752: `detect_local_lan_ip` (function), lines 8009-8020, exports `detect_local_lan_ip`
- order 753: `_LOCAL_LAN_IP_CACHE` (assignment), lines 8021-8022, exports `_LOCAL_LAN_IP_CACHE`
- order 754: `detect_local_lan_ip_cached` (function), lines 8023-8036, exports `detect_local_lan_ip_cached`
- order 774: `make_id` (function), lines 8341-8343, exports `make_id`
- order 775: `sanitize_profile_id` (function), lines 8344-8347, exports `sanitize_profile_id`
- order 903: `user_id_from_ip` (function), lines 13567-13574, exports `user_id_from_ip`
- order 907: `_meta_string_list` (function), lines 13991-14004, exports `_meta_string_list`
- order 966: `_module_exists` (function), lines 16867-16872, exports `_module_exists`

### `utils/sqlite.py`

- order 70: `_ClosingSQLiteConnection` (class), lines 74-83, exports `_ClosingSQLiteConnection`
- order 71: `_connect_sqlite` (function), lines 84-107, exports `_connect_sqlite`

### `utils/text.py`

- order 159: `MAX_TOOL_OUTPUT` (constant), lines 4177-4177, exports `MAX_TOOL_OUTPUT`
- order 498: `SOCKET_NOISE_LINE_PATTERNS` (constant), lines 4948-4953, exports `SOCKET_NOISE_LINE_PATTERNS`
- order 746: `filter_runtime_noise_lines` (function), lines 7901-7915, exports `filter_runtime_noise_lines`
- order 759: `safe_utf8_bytes` (function), lines 8161-8163, exports `safe_utf8_bytes`
- order 760: `escape_invalid_utf8_text` (function), lines 8164-8166, exports `escape_invalid_utf8_text`
- order 761: `sanitize_utf8_surrogates` (function), lines 8167-8180, exports `sanitize_utf8_surrogates`
- order 762: `decode_utf8_replace` (function), lines 8181-8185, exports `decode_utf8_replace`
- order 802: `trim` (function), lines 8948-8951, exports `trim`
- order 810: `is_synthetic_public_progress` (function), lines 9227-9246, exports `is_synthetic_public_progress`
- order 812: `display_clean` (function), lines 9299-9313, exports `display_clean`
- order 813: `short_title_from` (function), lines 9314-9332, exports `short_title_from`
- order 829: `_fmt_export_ts` (function), lines 11492-11502, exports `_fmt_export_ts`
- order 830: `_html_esc` (function), lines 11503-11506, exports `_html_esc`
- order 831: `_text_to_minimal_pdf` (function), lines 11507-11655, exports `_text_to_minimal_pdf`
- order 834: `normalize_embedded_newlines` (function), lines 11673-11682, exports `normalize_embedded_newlines`
- order 835: `_map_todo_status_token` (function), lines 11683-11721, exports `_map_todo_status_token`
- order 836: `split_todo_status_text` (function), lines 11722-11781, exports `split_todo_status_text`
- order 837: `extract_todo_rows_from_text` (function), lines 11782-11851, exports `extract_todo_rows_from_text`
- order 838: `decode_structured_todo_container` (function), lines 11852-11870, exports `decode_structured_todo_container`
- order 839: `infer_todo_status_from_text` (function), lines 11871-11879, exports `infer_todo_status_from_text`
- order 840: `split_structured_todo_content` (function), lines 11880-11935, exports `split_structured_todo_content`
- order 841: `normalize_work_text` (function), lines 11936-11965, exports `normalize_work_text`
- order 932: `make_unified_diff` (function), lines 15629-15647, exports `make_unified_diff`
- order 933: `_skip_row` (function), lines 15648-15653, exports `_skip_row`
- order 934: `_row_is_hot` (function), lines 15654-15657, exports `_row_is_hot`
- order 935: `_hotspot_index` (function), lines 15658-15681, exports `_hotspot_index`
- order 936: `_compress_rows_keep_hotspot` (function), lines 15682-15731, exports `_compress_rows_keep_hotspot`
- order 937: `_focused_diff_rows_from_opcodes` (function), lines 15732-15866, exports `_focused_diff_rows_from_opcodes`
- order 938: `make_numbered_diff` (function), lines 15867-15899, exports `make_numbered_diff`
- order 939: `render_numbered_diff_text` (function), lines 15900-15913, exports `render_numbered_diff_text`

### `web/admin_assets.py`

- order 1071: `ADMIN_INDEX_HTML` (constant), lines 97932-98232, exports `ADMIN_INDEX_HTML`
- order 1072: `ADMIN_CSS` (constant), lines 98233-98369, exports `ADMIN_CSS`
- order 1073: `ADMIN_JS` (constant), lines 98370-98745, exports `ADMIN_JS`

### `web/assets.py`

- order 1063: `INDEX_HTML` (constant), lines 91948-92207, exports `INDEX_HTML`
- order 1064: `APP_CSS` (constant), lines 92208-92748, exports `APP_CSS`
- order 1065: `APP_JS` (constant), lines 92749-97472, exports `APP_JS`
- order 1066: `APP_CSS` (constant), lines 97473-97489, exports `APP_CSS`
- order 1067: `APP_TS` (constant), lines 97490-97529, exports `APP_TS`

### `web/skills_assets.py`

- order 1068: `SKILLS_INDEX_HTML` (constant), lines 97530-97685, exports `SKILLS_INDEX_HTML`
- order 1069: `SKILLS_EXTRA_CSS` (constant), lines 97686-97785, exports `SKILLS_EXTRA_CSS`
- order 1070: `SKILLS_APP_JS` (constant), lines 97786-97931, exports `SKILLS_APP_JS`
