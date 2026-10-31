# Code_Structure Framework

## Overview

- Source snapshot: `Clouds_Coder.py` (1277 top-level statements)
- Generated source modules: 68
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
│   ├── context.py
│   ├── errors.py
│   ├── events.py
│   ├── evidence.py
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
│   ├── sandbox.py
│   └── toolchains.py
├── llm
│   ├── client.py
│   ├── constants.py
│   ├── gate.py
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
| `_imports.py` | 76 | 94 | — | 1–4908 |
| `admin/auth.py` | 3 | 3 | `admin/constants.py`, `utils/misc.py`, `utils/sqlite.py` | 15851–16693 |
| `admin/config.py` | 8 | 8 | `config/constants.py`, `config/paths.py`, `config/settings.py`, `llm/constants.py`, `llm/gate.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` | 17441–17956 |
| `admin/constants.py` | 16 | 16 | — | 4915–125041 |
| `agent/background.py` | 1 | 1 | `agent/process.py`, `config/constants.py`, `ide/sandbox.py`, `utils/misc.py`, `utils/text.py` | 25491–26116 |
| `agent/bus.py` | 1 | 1 | `config/constants.py`, `utils/crypto.py`, `utils/misc.py` | 26117–26182 |
| `agent/context.py` | 2 | 2 | `agent/tools.py` | 5648–13832 |
| `agent/errors.py` | 1 | 1 | — | 13517–13520 |
| `agent/events.py` | 1 | 1 | — | 18683–18737 |
| `agent/evidence.py` | 2 | 2 | `utils/sqlite.py` | 32507–32846 |
| `agent/process.py` | 9 | 9 | `ide/sandbox.py`, `utils/errors.py`, `utils/misc.py`, `utils/text.py` | 5968–25490 |
| `agent/tasks.py` | 1 | 1 | `utils/crypto.py`, `utils/json_utils.py`, `utils/misc.py` | 24990–25124 |
| `agent/todo.py` | 1 | 1 | `config/constants.py`, `config/settings.py`, `utils/misc.py`, `utils/text.py` | 18738–19164 |
| `agent/tools.py` | 17 | 21 | `config/constants.py`, `config/settings.py`, `utils/text.py` | 18562–31974 |
| `agent/worktree.py` | 1 | 1 | `agent/process.py`, `agent/tasks.py`, `config/constants.py`, `utils/crypto.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` | 26183–26395 |
| `app/context.py` | 1 | 1 | `admin/auth.py`, `admin/config.py`, `admin/constants.py`, `agent/process.py`, `agent/tools.py`, `app/services.py`, `collaboration/core.py`, `config/bootstrap.py`, `config/constants.py`, `config/paths.py`, `config/settings.py`, `ide/assets.py`, `ide/auth.py`, `ide/errors.py`, `ide/events.py`, `ide/preview.py`, `ide/sandbox.py`, `ide/toolchains.py`, `llm/client.py`, `llm/constants.py`, `llm/gate.py`, `llm/utils.py`, `mcp/driver.py`, `rag/assets.py`, `rag/constants.py`, `rag/ingestion.py`, `rag/parsers.py`, `rag/store.py`, `server/http.py`, `session/manager.py`, `session/state.py`, `skills/provisioning.py`, `skills/store.py`, `skills/studio.py`, `utils/crypto.py`, `utils/files.py`, `utils/http.py`, `utils/json_utils.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py`, `web/assets.py`, `web/skills_assets.py` | 125107–136695 |
| `app/main.py` | 2 | 1 | `admin/config.py`, `admin/constants.py`, `agent/tools.py`, `app/context.py`, `collaboration/watcher.py`, `config/constants.py`, `config/paths.py`, `config/settings.py`, `ide/handler.py`, `llm/constants.py`, `llm/gate.py`, `llm/utils.py`, `mcp/constants.py`, `mcp/service.py`, `rag/constants.py`, `server/http.py`, `server/rag_admin.py`, `server/skills.py`, `skills/provisioning.py`, `utils/files.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` | 143715–145718 |
| `app/services.py` | 2 | 2 | `admin/constants.py`, `config/settings.py`, `skills/embedded.py`, `skills/store.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/sqlite.py`, `utils/text.py` | 136736–137936 |
| `collaboration/core.py` | 23 | 23 | `config/constants.py`, `utils/sqlite.py` | 1527–4768 |
| `collaboration/watcher.py` | 2 | 2 | `utils/misc.py`, `utils/sqlite.py`, `utils/text.py` | 143622–143714 |
| `config/bootstrap.py` | 7 | 7 | `config/constants.py`, `config/settings.py`, `utils/json_utils.py`, `utils/misc.py` | 124–16406 |
| `config/constants.py` | 515 | 510 | `config/bootstrap.py`, `rag/constants.py` | 1478–125037 |
| `config/paths.py` | 13 | 13 | `agent/process.py`, `utils/crypto.py`, `utils/text.py` | 4914–9588 |
| `config/settings.py` | 71 | 71 | `agent/tools.py`, `config/constants.py`, `config/paths.py`, `ide/preview.py`, `llm/constants.py`, `llm/gate.py`, `llm/utils.py`, `rag/constants.py`, `skills/provisioning.py`, `utils/http.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` | 7481–31209 |
| `ide/assets.py` | 8 | 3 | — | 121952–123109 |
| `ide/auth.py` | 2 | 2 | `admin/auth.py`, `admin/constants.py`, `config/constants.py`, `utils/misc.py`, `utils/sqlite.py`, `utils/text.py` | 16694–17425 |
| `ide/errors.py` | 2 | 2 | — | 17426–17440 |
| `ide/events.py` | 1 | 1 | `config/constants.py`, `utils/text.py` | 10471–10522 |
| `ide/handler.py` | 1 | 1 | `admin/auth.py`, `app/context.py`, `collaboration/core.py`, `config/constants.py`, `config/settings.py`, `ide/auth.py`, `ide/errors.py`, `ide/events.py`, `session/manager.py`, `session/state.py`, `utils/http.py`, `utils/json_utils.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py` | 141191–142847 |
| `ide/preview.py` | 12 | 12 | `config/constants.py`, `utils/text.py` | 18242–18682 |
| `ide/sandbox.py` | 21 | 21 | `agent/process.py`, `utils/misc.py` | 9410–32506 |
| `ide/toolchains.py` | 7 | 7 | — | 6307–125106 |
| `llm/client.py` | 2 | 2 | `agent/context.py`, `agent/tools.py`, `config/constants.py`, `config/settings.py`, `llm/gate.py`, `llm/utils.py`, `utils/http.py`, `utils/json_utils.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py` | 27778–31115 |
| `llm/constants.py` | 17 | 17 | — | 4912–14195 |
| `llm/gate.py` | 22 | 22 | `config/constants.py`, `config/settings.py`, `llm/client.py`, `utils/misc.py`, `utils/text.py` | 5790–28255 |
| `llm/utils.py` | 37 | 37 | `agent/context.py`, `agent/process.py`, `config/settings.py`, `llm/constants.py`, `utils/http.py`, `utils/json_utils.py`, `utils/text.py` | 13433–14850 |
| `mcp/constants.py` | 8 | 8 | — | 5284–26431 |
| `mcp/driver.py` | 13 | 13 | `mcp/constants.py`, `utils/files.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` | 26432–27777 |
| `mcp/service.py` | 1 | 1 | `app/context.py`, `config/constants.py`, `utils/files.py`, `utils/http.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` | 143319–143536 |
| `rag/assets.py` | 6 | 6 | — | 119328–121951 |
| `rag/constants.py` | 77 | 77 | — | 5280–112282 |
| `rag/index.py` | 5 | 5 | `config/constants.py`, `rag/constants.py`, `rag/ingestion.py`, `rag/parsers.py`, `utils/misc.py`, `utils/text.py` | 112307–118948 |
| `rag/ingestion.py` | 13 | 13 | `config/constants.py`, `config/settings.py`, `rag/constants.py`, `rag/parsers.py`, `rag/store.py`, `session/state.py`, `utils/files.py`, `utils/json_utils.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py` | 111629–119327 |
| `rag/parsers.py` | 31 | 31 | `agent/process.py`, `config/constants.py`, `rag/constants.py`, `rag/ingestion.py`, `utils/files.py`, `utils/json_utils.py`, `utils/media.py`, `utils/text.py` | 111252–113478 |
| `rag/store.py` | 7 | 7 | `config/constants.py`, `config/settings.py`, `ide/preview.py`, `rag/constants.py`, `rag/index.py`, `rag/ingestion.py`, `rag/parsers.py`, `skills/provisioning.py`, `utils/files.py`, `utils/json_utils.py`, `utils/media.py`, `utils/misc.py`, `utils/sqlite.py`, `utils/text.py` | 115174–119239 |
| `rag/web_search.py` | 15 | 15 | `config/constants.py`, `config/paths.py`, `rag/constants.py`, `utils/http.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/sqlite.py`, `utils/text.py` | 10557–12715 |
| `server/http.py` | 12 | 12 | `admin/auth.py`, `admin/config.py`, `admin/constants.py`, `agent/process.py`, `app/context.py`, `collaboration/core.py`, `collaboration/watcher.py`, `config/constants.py`, `config/paths.py`, `config/settings.py`, `ide/auth.py`, `ide/handler.py`, `ide/preview.py`, `llm/gate.py`, `llm/utils.py`, `server/rag_admin.py`, `session/manager.py`, `session/state.py`, `skills/studio.py`, `utils/errors.py`, `utils/files.py`, `utils/http.py`, `utils/json_utils.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py`, `web/admin_assets.py` | 7530–143318 |
| `server/rag_admin.py` | 3 | 3 | `admin/auth.py`, `app/context.py`, `config/constants.py`, `rag/constants.py`, `utils/http.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py` | 140519–141190 |
| `server/skills.py` | 1 | 1 | `admin/auth.py`, `app/context.py`, `config/constants.py`, `config/paths.py`, `config/settings.py`, `llm/gate.py`, `session/manager.py`, `skills/provisioning.py`, `skills/studio.py`, `utils/http.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py` | 139869–140518 |
| `session/manager.py` | 2 | 2 | `agent/process.py`, `config/constants.py`, `config/paths.py`, `config/settings.py`, `llm/client.py`, `llm/gate.py`, `llm/utils.py`, `rag/store.py`, `session/state.py`, `skills/store.py`, `utils/crypto.py`, `utils/files.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` | 8734–99272 |
| `session/state.py` | 1 | 1 | `admin/constants.py`, `agent/background.py`, `agent/bus.py`, `agent/context.py`, `agent/errors.py`, `agent/events.py`, `agent/evidence.py`, `agent/process.py`, `agent/tasks.py`, `agent/todo.py`, `agent/tools.py`, `agent/worktree.py`, `collaboration/core.py`, `config/constants.py`, `config/paths.py`, `config/settings.py`, `ide/events.py`, `ide/preview.py`, `ide/sandbox.py`, `llm/client.py`, `llm/constants.py`, `llm/gate.py`, `llm/utils.py`, `mcp/constants.py`, `mcp/driver.py`, `rag/constants.py`, `rag/parsers.py`, `rag/web_search.py`, `server/http.py`, `skills/provisioning.py`, `skills/store.py`, `utils/compress.py`, `utils/crypto.py`, `utils/errors.py`, `utils/files.py`, `utils/http.py`, `utils/json_utils.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py` | 32847–96728 |
| `skills/embedded.py` | 10 | 10 | — | 19165–22964 |
| `skills/provisioning.py` | 26 | 26 | `config/paths.py`, `skills/embedded.py`, `utils/files.py`, `utils/json_utils.py`, `utils/misc.py` | 19191–22927 |
| `skills/store.py` | 3 | 3 | `config/constants.py`, `config/settings.py`, `llm/utils.py`, `skills/embedded.py`, `utils/files.py`, `utils/http.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` | 6326–24989 |
| `skills/studio.py` | 5 | 5 | `agent/process.py`, `collaboration/core.py`, `config/constants.py`, `config/settings.py`, `ide/sandbox.py`, `llm/client.py`, `llm/constants.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/sqlite.py`, `utils/text.py` | 123135–125032 |
| `utils/compress.py` | 2 | 2 | — | 12880–12896 |
| `utils/crypto.py` | 1 | 1 | `utils/json_utils.py` | 15884–16037 |
| `utils/errors.py` | 2 | 2 | — | 13513–25130 |
| `utils/files.py` | 29 | 29 | `config/constants.py`, `config/paths.py`, `utils/http.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` | 7400–17911 |
| `utils/http.py` | 7 | 7 | `utils/json_utils.py`, `utils/text.py` | 4909–9564 |
| `utils/json_utils.py` | 17 | 17 | `utils/text.py` | 5279–16348 |
| `utils/media.py` | 6 | 6 | — | 7038–9115 |
| `utils/misc.py` | 16 | 16 | `config/constants.py` | 9116–19266 |
| `utils/sqlite.py` | 3 | 3 | — | 74–143621 |
| `utils/text.py` | 36 | 36 | `config/constants.py` | 5267–18241 |
| `web/admin_assets.py` | 3 | 3 | — | 105325–106317 |
| `web/assets.py` | 5 | 4 | — | 99273–104922 |
| `web/skills_assets.py` | 3 | 3 | — | 104923–105324 |

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
- order 72: `_try_import_120` (import), lines 118-123, exports `_AESGCM`
- order 77: `_import_1481` (import), lines 1480-1485, exports `EVOLUTION_MODES`, `LiquidKernelControlPlane`, `LiquidKernelError`
- order 79: `_import_1506` (import), lines 1502-1508, exports `_LiquidKernelRegistry`
- order 120: `_try_import_4892` (import), lines 4890-4899, exports `_fcntl`, `_pty`, `_termios`
- order 121: `_try_import_4901` (import), lines 4900-4904, exports `_certifi`
- order 122: `_try_import_4905` (import), lines 4905-4908, exports `_yaml`

### `admin/auth.py`

- order 957: `trusted_client_ip` (function), lines 15851-15883, exports `trusted_client_ip`
- order 971: `AdminAuthError` (class), lines 16407-16414, exports `AdminAuthError`
- order 972: `AdminAuthStore` (class), lines 16415-16693, exports `AdminAuthStore`

### `admin/config.py`

- order 977: `_admin_config_schema` (function), lines 17441-17564, exports `_admin_config_schema`
- order 978: `_admin_factory_config` (function), lines 17565-17568, exports `_admin_factory_config`
- order 979: `_admin_coerce_config` (function), lines 17569-17724, exports `_admin_coerce_config`
- order 980: `_admin_config_to_argv` (function), lines 17725-17765, exports `_admin_config_to_argv`
- order 981: `_admin_restart_probe_url` (function), lines 17766-17781, exports `_admin_restart_probe_url`
- order 982: `_admin_supervised_restart` (function), lines 17782-17893, exports `_admin_supervised_restart`
- order 984: `_admin_argparse_defaults` (function), lines 17912-17935, exports `_admin_argparse_defaults`
- order 985: `_admin_config_from_namespace` (function), lines 17936-17956, exports `_admin_config_from_namespace`

### `admin/constants.py`

- order 129: `ADMIN_STATE_DIRNAME` (constant), lines 4915-4915, exports `ADMIN_STATE_DIRNAME`
- order 130: `ADMIN_CONFIG_FILENAME` (constant), lines 4916-4916, exports `ADMIN_CONFIG_FILENAME`
- order 131: `ADMIN_APPS_FILENAME` (constant), lines 4917-4917, exports `ADMIN_APPS_FILENAME`
- order 132: `ADMIN_TELEMETRY_FILENAME` (constant), lines 4918-4918, exports `ADMIN_TELEMETRY_FILENAME`
- order 133: `ADMIN_AUTH_FILENAME` (constant), lines 4919-4919, exports `ADMIN_AUTH_FILENAME`
- order 143: `ADMIN_MAX_APP_SKILLS` (constant), lines 4966-4966, exports `ADMIN_MAX_APP_SKILLS`
- order 144: `ADMIN_MAX_APP_CAPSULE_CHARS` (constant), lines 4967-4967, exports `ADMIN_MAX_APP_CAPSULE_CHARS`
- order 145: `ADMIN_MAX_APP_RESOURCE_FILES` (constant), lines 4968-4968, exports `ADMIN_MAX_APP_RESOURCE_FILES`
- order 146: `ADMIN_MAX_APP_RESOURCE_BYTES` (constant), lines 4969-4969, exports `ADMIN_MAX_APP_RESOURCE_BYTES`
- order 147: `ADMIN_APP_INLINE_BLOB_BYTES` (constant), lines 4970-4970, exports `ADMIN_APP_INLINE_BLOB_BYTES`
- order 148: `ADMIN_AUTH_SESSION_TTL_SECONDS` (constant), lines 4971-4971, exports `ADMIN_AUTH_SESSION_TTL_SECONDS`
- order 149: `ADMIN_AUTH_PASSWORD_ITERATIONS` (constant), lines 4972-4972, exports `ADMIN_AUTH_PASSWORD_ITERATIONS`
- order 150: `ADMIN_AUTH_MAX_ACTIVE_SESSIONS` (constant), lines 4973-4973, exports `ADMIN_AUTH_MAX_ACTIVE_SESSIONS`
- order 1253: `ADMIN_SKILLS_REVIEW_HTML` (constant), lines 125038-125039, exports `ADMIN_SKILLS_REVIEW_HTML`
- order 1254: `ADMIN_SKILLS_REVIEW_CSS` (constant), lines 125040-125040, exports `ADMIN_SKILLS_REVIEW_CSS`
- order 1255: `ADMIN_SKILLS_REVIEW_JS` (constant), lines 125041-125041, exports `ADMIN_SKILLS_REVIEW_JS`

### `agent/background.py`

- order 1057: `BackgroundManager` (class), lines 25491-26116, exports `BackgroundManager`

### `agent/bus.py`

- order 1058: `MessageBus` (class), lines 26117-26182, exports `MessageBus`

### `agent/context.py`

- order 345: `_READ_DISPATCH_CONTEXT` (assignment), lines 5648-5651, exports `_READ_DISPATCH_CONTEXT`
- order 901: `compact_successful_write_history` (function), lines 13829-13832, exports `compact_successful_write_history`

### `agent/errors.py`

- order 886: `CircuitBreakerTriggered` (class), lines 13517-13520, exports `CircuitBreakerTriggered`

### `agent/events.py`

- order 1013: `EventHub` (class), lines 18683-18737, exports `EventHub`

### `agent/evidence.py`

- order 1140: `EvidenceRetrievalController` (class), lines 32507-32843, exports `EvidenceRetrievalController`
- order 1141: `_EVIDENCE_CONTROLLER_INIT_LOCK` (assignment), lines 32844-32846, exports `_EVIDENCE_CONTROLLER_INIT_LOCK`

### `agent/process.py`

- order 458: `_TOOL_CANCEL_LOCAL` (assignment), lines 5968-5971, exports `_TOOL_CANCEL_LOCAL`
- order 459: `_TOOL_ORPHAN_LOCK` (assignment), lines 5972-5972, exports `_TOOL_ORPHAN_LOCK`
- order 789: `subprocess_text_encodings` (function), lines 9428-9449, exports `subprocess_text_encodings`
- order 790: `decode_subprocess_bytes` (function), lines 9450-9476, exports `decode_subprocess_bytes`
- order 791: `run_subprocess_text` (function), lines 9477-9499, exports `run_subprocess_text`
- order 792: `windows_utf8_shell_command` (function), lines 9500-9506, exports `windows_utf8_shell_command`
- order 793: `shell_process_invocation` (function), lines 9507-9517, exports `shell_process_invocation`
- order 794: `join_shell_task_command` (function), lines 9518-9529, exports `join_shell_task_command`
- order 1056: `UserProcessManager` (class), lines 25131-25490, exports `UserProcessManager`

### `agent/tasks.py`

- order 1054: `TaskManager` (class), lines 24990-25124, exports `TaskManager`

### `agent/todo.py`

- order 1014: `TodoManager` (class), lines 18738-19164, exports `TodoManager`

### `agent/tools.py`

- order 1008: `_ask_user_option_rows` (function), lines 18562-18595, exports `_ask_user_option_rows`
- order 1009: `_ask_user_option_value` (function), lines 18596-18601, exports `_ask_user_option_value`
- order 1101: `tool_def` (function), lines 31116-31129, exports `tool_def`
- order 1106: `bash_operation_is_observation` (function), lines 31210-31213, exports `bash_operation_is_observation`
- order 1107: `bash_operation_is_marked_observation` (function), lines 31214-31218, exports `bash_operation_is_marked_observation`
- order 1108: `TOOLS` (constant), lines 31219-31810, exports `TOOLS`
- order 1109: `TOOL_REQUIRED_ARGS` (constant), lines 31811-31812, exports `TOOL_REQUIRED_ARGS`
- order 1110: `TOOL_SPEC_BY_NAME` (constant), lines 31813-31813, exports `TOOL_SPEC_BY_NAME`
- order 1111: `_for_31814` (statement), lines 31814-31823, exports `_tool`, `_fn`, `_name`, `_required`
- order 1112: `TOOL_NAME_FUZZY_MAP` (constant), lines 31824-31825, exports `TOOL_NAME_FUZZY_MAP`
- order 1113: `_for_31826` (statement), lines 31826-31829, exports `_name`, `_key`
- order 1114: `_for_31831` (statement), lines 31830-31847, exports `_alias`, `_target`
- order 1115: `is_todo_resume_tool_name` (function), lines 31848-31864, exports `is_todo_resume_tool_name`
- order 1116: `canonicalize_tool_name` (function), lines 31865-31883, exports `canonicalize_tool_name`
- order 1117: `filter_tool_specs_for_runtime` (function), lines 31884-31899, exports `filter_tool_specs_for_runtime`
- order 1118: `DEVELOPER_TOOL_DROP` (constant), lines 31900-31910, exports `DEVELOPER_TOOL_DROP`
- order 1119: `AGENT_TOOL_ALLOWLIST` (constant), lines 31911-31974, exports `AGENT_TOOL_ALLOWLIST`

### `agent/worktree.py`

- order 1059: `WorktreeManager` (class), lines 26183-26395, exports `WorktreeManager`

### `app/context.py`

- order 1259: `AppContext` (class), lines 125107-136695, exports `AppContext`

### `app/main.py`

- order 1275: `main` (function), lines 143715-145715, exports `main`
- order 1276: `_main_guard_145717` (main_guard), lines 145716-145718, exports —

### `app/services.py`

- order 1261: `TelemetryStore` (class), lines 136736-137126, exports `TelemetryStore`
- order 1262: `ApplicationRegistry` (class), lines 137127-137936, exports `ApplicationRegistry`

### `collaboration/core.py`

- order 94: `_now` (function), lines 1527-1530, exports `_now`
- order 95: `_json` (function), lines 1531-1534, exports `_json`
- order 96: `_load_json` (function), lines 1535-1541, exports `_load_json`
- order 97: `_b64_token` (function), lines 1542-1545, exports `_b64_token`
- order 98: `_branch_label` (function), lines 1546-1554, exports `_branch_label`
- order 99: `_digest` (function), lines 1555-1558, exports `_digest`
- order 100: `_password_hash` (function), lines 1559-1562, exports `_password_hash`
- order 101: `_normalize_ip` (function), lines 1563-1572, exports `_normalize_ip`
- order 102: `_normalize_name` (function), lines 1573-1579, exports `_normalize_name`
- order 103: `_COLLAB_PUBLIC_SECRET_PATTERNS` (assignment), lines 1580-1591, exports `_COLLAB_PUBLIC_SECRET_PATTERNS`
- order 104: `_collaboration_public_text` (function), lines 1592-1622, exports `_collaboration_public_text`
- order 105: `_collaboration_task_objective` (function), lines 1623-1647, exports `_collaboration_task_objective`
- order 106: `_collaboration_task_title` (function), lines 1648-1655, exports `_collaboration_task_title`
- order 107: `_collaboration_task_key` (function), lines 1656-1662, exports `_collaboration_task_key`
- order 108: `_collaboration_plan_steps` (function), lines 1663-1681, exports `_collaboration_plan_steps`
- order 109: `CollaborationError` (class), lines 1682-1689, exports `CollaborationError`
- order 110: `CollaborationPrincipal` (class), lines 1690-1700, exports `CollaborationPrincipal`
- order 111: `_normalize_operation` (function), lines 1701-1734, exports `_normalize_operation`
- order 112: `operation_input_length` (function), lines 1735-1738, exports `operation_input_length`
- order 113: `apply_text_operation` (function), lines 1739-1761, exports `apply_text_operation`
- order 114: `transform_text_operation` (function), lines 1762-1838, exports `transform_text_operation`
- order 115: `CollaborationStore` (class), lines 1839-4554, exports `CollaborationStore`
- order 116: `CollaborationWriteCoordinator` (class), lines 4555-4768, exports `CollaborationWriteCoordinator`

### `collaboration/watcher.py`

- order 1273: `collaboration_file_watcher_loop` (function), lines 143622-143696, exports `collaboration_file_watcher_loop`
- order 1274: `collaboration_watcher_health` (function), lines 143697-143714, exports `collaboration_watcher_health`

### `config/bootstrap.py`

- order 73: `_EMBEDDED_LIQUID_KERNEL_PACKAGE_B64` (assignment), lines 124-1360, exports `_EMBEDDED_LIQUID_KERNEL_PACKAGE_B64`
- order 74: `sync_embedded_liquid_kernel_bundle` (function), lines 1361-1384, exports `sync_embedded_liquid_kernel_bundle`
- order 75: `_ensure_embedded_liquid_kernel_package` (function), lines 1385-1477, exports `_ensure_embedded_liquid_kernel_package`
- order 78: `_ensure_liquid_kernel_sqlite_lifecycle` (function), lines 1486-1501, exports `_ensure_liquid_kernel_sqlite_lifecycle`
- order 968: `_liquid_kernel_history_present` (function), lines 16358-16362, exports `_liquid_kernel_history_present`
- order 969: `prepare_liquid_kernel_runtime` (function), lines 16363-16392, exports `prepare_liquid_kernel_runtime`
- order 970: `_persist_liquid_kernel_bootstrap` (function), lines 16393-16406, exports `_persist_liquid_kernel_bootstrap`

### `config/constants.py`

- order 76: `LIQUID_KERNEL_PACKAGE_STATUS` (constant), lines 1478-1479, exports `LIQUID_KERNEL_PACKAGE_STATUS`
- order 80: `_call_ensure_liquid_kernel_sqlite_lifecycle_1510` (expression), lines 1509-1510, exports —
- order 81: `COLLAB_DB_FILENAME` (constant), lines 1511-1514, exports `COLLAB_DB_FILENAME`
- order 82: `COLLAB_SESSION_TTL_SECONDS` (constant), lines 1515-1515, exports `COLLAB_SESSION_TTL_SECONDS`
- order 83: `COLLAB_PRESENCE_TTL_SECONDS` (constant), lines 1516-1516, exports `COLLAB_PRESENCE_TTL_SECONDS`
- order 84: `COLLAB_PASSWORD_ITERATIONS` (constant), lines 1517-1517, exports `COLLAB_PASSWORD_ITERATIONS`
- order 85: `COLLAB_MAX_AVATAR_BYTES` (constant), lines 1518-1518, exports `COLLAB_MAX_AVATAR_BYTES`
- order 86: `COLLAB_MAX_TEXT_BYTES` (constant), lines 1519-1519, exports `COLLAB_MAX_TEXT_BYTES`
- order 87: `COLLAB_DELETE_RETENTION_DAYS` (constant), lines 1520-1520, exports `COLLAB_DELETE_RETENTION_DAYS`
- order 88: `COLLAB_EVENT_RETENTION` (constant), lines 1521-1521, exports `COLLAB_EVENT_RETENTION`
- order 89: `COLLAB_AGENT_STALE_SECONDS` (constant), lines 1522-1522, exports `COLLAB_AGENT_STALE_SECONDS`
- order 90: `COLLAB_AGENT_HEARTBEAT_INTERVAL_SECONDS` (constant), lines 1523-1523, exports `COLLAB_AGENT_HEARTBEAT_INTERVAL_SECONDS`
- order 91: `COLLAB_EXTERNAL_WRITE_SETTLE_SECONDS` (constant), lines 1524-1524, exports `COLLAB_EXTERNAL_WRITE_SETTLE_SECONDS`
- order 92: `COLLAB_EXTERNAL_WRITE_CONFIRMATIONS` (constant), lines 1525-1525, exports `COLLAB_EXTERNAL_WRITE_CONFIRMATIONS`
- order 93: `COLLAB_SCHEMA_VERSION` (constant), lines 1526-1526, exports `COLLAB_SCHEMA_VERSION`
- order 117: `COLLAB_INDEX_HTML` (constant), lines 4769-4840, exports `COLLAB_INDEX_HTML`
- order 118: `COLLAB_CSS` (constant), lines 4841-4848, exports `COLLAB_CSS`
- order 119: `COLLAB_JS` (constant), lines 4849-4889, exports `COLLAB_JS`
- order 125: `APP_VERSION` (constant), lines 4911-4911, exports `APP_VERSION`
- order 134: `IDE_AUTH_FILENAME` (constant), lines 4920-4920, exports `IDE_AUTH_FILENAME`
- order 135: `IDE_AUTH_SESSION_TTL_SECONDS` (constant), lines 4921-4921, exports `IDE_AUTH_SESSION_TTL_SECONDS`
- order 136: `IDE_AUTH_MAX_ACTIVE_SESSIONS` (constant), lines 4922-4922, exports `IDE_AUTH_MAX_ACTIVE_SESSIONS`
- order 137: `IDE_DEVICE_SECRET_MIN_BYTES` (constant), lines 4923-4923, exports `IDE_DEVICE_SECRET_MIN_BYTES`
- order 138: `IDE_DEVICE_LABEL_MAX_CHARS` (constant), lines 4924-4924, exports `IDE_DEVICE_LABEL_MAX_CHARS`
- order 139: `IDE_DEVICE_PAIRING_TTL_SECONDS` (constant), lines 4925-4925, exports `IDE_DEVICE_PAIRING_TTL_SECONDS`
- order 140: `IDE_WORKBENCH_STATE_FILENAME` (constant), lines 4926-4926, exports `IDE_WORKBENCH_STATE_FILENAME`
- order 141: `IDE_PROMPT_ENHANCEMENT_BUDGETS` (constant), lines 4927-4964, exports `IDE_PROMPT_ENHANCEMENT_BUDGETS`
- order 142: `IDE_EXTENSIONS_DIRNAME` (constant), lines 4965-4965, exports `IDE_EXTENSIONS_DIRNAME`
- order 164: `LONG_OUTPUT_MODEL_PAGE_CHARS` (constant), lines 5268-5268, exports `LONG_OUTPUT_MODEL_PAGE_CHARS`
- order 165: `LONG_OUTPUT_UI_PAGE_CHARS` (constant), lines 5269-5269, exports `LONG_OUTPUT_UI_PAGE_CHARS`
- order 166: `LONG_OUTPUT_UI_PREVIEW_MAX_PAGES` (constant), lines 5270-5270, exports `LONG_OUTPUT_UI_PREVIEW_MAX_PAGES`
- order 167: `LONG_OUTPUT_LISTING_OFFLOAD_CHARS` (constant), lines 5271-5271, exports `LONG_OUTPUT_LISTING_OFFLOAD_CHARS`
- order 168: `LONG_OUTPUT_READ_PAGE_LINES` (constant), lines 5272-5272, exports `LONG_OUTPUT_READ_PAGE_LINES`
- order 169: `LONG_OUTPUT_READ_PAGE_MAX_CHARS` (constant), lines 5273-5273, exports `LONG_OUTPUT_READ_PAGE_MAX_CHARS`
- order 170: `LONG_OUTPUT_TEMP_MAX_FILES` (constant), lines 5274-5274, exports `LONG_OUTPUT_TEMP_MAX_FILES`
- order 171: `READ_FILE_DEFAULT_MAX_CHARS` (constant), lines 5275-5275, exports `READ_FILE_DEFAULT_MAX_CHARS`
- order 172: `READ_FILE_HARD_MAX_CHARS` (constant), lines 5276-5276, exports `READ_FILE_HARD_MAX_CHARS`
- order 173: `READ_FILE_OVERVIEW_HEAD_LINES` (constant), lines 5277-5277, exports `READ_FILE_OVERVIEW_HEAD_LINES`
- order 174: `READ_FILE_SEARCH_MAX_MATCHES` (constant), lines 5278-5278, exports `READ_FILE_SEARCH_MAX_MATCHES`
- order 179: `CODE_ADMIN_PORT_OFFSET` (constant), lines 5283-5283, exports `CODE_ADMIN_PORT_OFFSET`
- order 181: `IDE_PORT_OFFSET` (constant), lines 5285-5288, exports `IDE_PORT_OFFSET`
- order 182: `IDE_DEFAULT_PORT` (constant), lines 5289-5289, exports `IDE_DEFAULT_PORT`
- order 183: `COLLAB_PORT_OFFSET` (constant), lines 5290-5290, exports `COLLAB_PORT_OFFSET`
- order 185: `DEFAULT_WEB_SEARCH_ENABLED` (constant), lines 5292-5292, exports `DEFAULT_WEB_SEARCH_ENABLED`
- order 190: `DEFAULT_USER_MEMORY_MODE` (constant), lines 5297-5297, exports `DEFAULT_USER_MEMORY_MODE`
- order 198: `AGENT_WEB_SEARCH_USER_AGENT` (constant), lines 5308-5308, exports `AGENT_WEB_SEARCH_USER_AGENT`
- order 199: `AGENT_WEB_SEARCH_DEFAULT_MAX_RESULTS` (constant), lines 5309-5309, exports `AGENT_WEB_SEARCH_DEFAULT_MAX_RESULTS`
- order 200: `AGENT_WEB_SEARCH_DEFAULT_MAX_PAGES` (constant), lines 5310-5310, exports `AGENT_WEB_SEARCH_DEFAULT_MAX_PAGES`
- order 201: `AGENT_WEB_SEARCH_HARD_MAX_PAGES` (constant), lines 5311-5311, exports `AGENT_WEB_SEARCH_HARD_MAX_PAGES`
- order 202: `AGENT_WEB_SEARCH_DEFAULT_DEPTH` (constant), lines 5312-5312, exports `AGENT_WEB_SEARCH_DEFAULT_DEPTH`
- order 203: `AGENT_WEB_SEARCH_HARD_DEPTH` (constant), lines 5313-5313, exports `AGENT_WEB_SEARCH_HARD_DEPTH`
- order 204: `AGENT_WEB_SEARCH_FETCH_TIMEOUT` (constant), lines 5314-5314, exports `AGENT_WEB_SEARCH_FETCH_TIMEOUT`
- order 205: `AGENT_WEB_SEARCH_TOOL_SOFT_TIMEOUT` (constant), lines 5315-5315, exports `AGENT_WEB_SEARCH_TOOL_SOFT_TIMEOUT`
- order 206: `AGENT_WEB_SEARCH_MAX_PAGE_BYTES` (constant), lines 5316-5316, exports `AGENT_WEB_SEARCH_MAX_PAGE_BYTES`
- order 207: `AGENT_WEB_SEARCH_MAX_TEXT_CHARS` (constant), lines 5317-5317, exports `AGENT_WEB_SEARCH_MAX_TEXT_CHARS`
- order 208: `AGENT_WEB_SEARCH_PUBLIC_DISCOVERY_ENABLED` (constant), lines 5318-5320, exports `AGENT_WEB_SEARCH_PUBLIC_DISCOVERY_ENABLED`
- order 209: `AGENT_WEB_SEARCH_PUBLIC_FEED_URL` (constant), lines 5321-5321, exports `AGENT_WEB_SEARCH_PUBLIC_FEED_URL`
- order 210: `AGENT_WEB_SEARCH_PUBLIC_FEED_MAX_BYTES` (constant), lines 5322-5322, exports `AGENT_WEB_SEARCH_PUBLIC_FEED_MAX_BYTES`
- order 211: `AGENT_WEB_SEARCH_LOCAL_GRAPH_MAX_NODES` (constant), lines 5323-5323, exports `AGENT_WEB_SEARCH_LOCAL_GRAPH_MAX_NODES`
- order 212: `AGENT_WEB_SEARCH_LOCAL_GRAPH_MAX_EDGES` (constant), lines 5324-5324, exports `AGENT_WEB_SEARCH_LOCAL_GRAPH_MAX_EDGES`
- order 213: `AGENT_WEB_SEARCH_LOCAL_GRAPH_EDGE_SCAN_MULTIPLIER` (constant), lines 5325-5325, exports `AGENT_WEB_SEARCH_LOCAL_GRAPH_EDGE_SCAN_MULTIPLIER`
- order 214: `AGENT_WEB_SEARCH_LOCAL_GRAPH_PAGERANK_ITERATIONS` (constant), lines 5326-5326, exports `AGENT_WEB_SEARCH_LOCAL_GRAPH_PAGERANK_ITERATIONS`
- order 215: `AGENT_WEB_SEARCH_LOCAL_GRAPH_PAGERANK_DAMPING` (constant), lines 5327-5327, exports `AGENT_WEB_SEARCH_LOCAL_GRAPH_PAGERANK_DAMPING`
- order 216: `AGENT_WEB_SEARCH_LOCAL_GRAPH_AUTHORITY_BONUS_MAX` (constant), lines 5328-5328, exports `AGENT_WEB_SEARCH_LOCAL_GRAPH_AUTHORITY_BONUS_MAX`
- order 226: `CODE_CHUNK_CHARS` (constant), lines 5350-5350, exports `CODE_CHUNK_CHARS`
- order 227: `CODE_CHUNK_OVERLAP` (constant), lines 5351-5351, exports `CODE_CHUNK_OVERLAP`
- order 228: `CODE_MAX_CHUNKS_PER_DOC` (constant), lines 5352-5352, exports `CODE_MAX_CHUNKS_PER_DOC`
- order 229: `CODE_SOURCE_ANALYSIS_MAX_CHARS` (constant), lines 5353-5362, exports `CODE_SOURCE_ANALYSIS_MAX_CHARS`
- order 270: `CODE_IMPORT_WORKER_COUNT` (constant), lines 5431-5434, exports `CODE_IMPORT_WORKER_COUNT`
- order 272: `CODE_PARSE_TIMEOUT_SECONDS` (constant), lines 5439-5442, exports `CODE_PARSE_TIMEOUT_SECONDS`
- order 273: `DEFAULT_CONTEXT_TOKEN_LIMIT` (constant), lines 5443-5443, exports `DEFAULT_CONTEXT_TOKEN_LIMIT`
- order 274: `TOKEN_THRESHOLD` (constant), lines 5444-5444, exports `TOKEN_THRESHOLD`
- order 275: `CONTEXT_AUTO_COMPACT_RESERVE_RATIO` (constant), lines 5445-5448, exports `CONTEXT_AUTO_COMPACT_RESERVE_RATIO`
- order 276: `CONTEXT_ESTIMATE_SAFETY_MULTIPLIER` (constant), lines 5449-5452, exports `CONTEXT_ESTIMATE_SAFETY_MULTIPLIER`
- order 277: `CONTEXT_USAGE_CALIBRATION_MAX` (constant), lines 5453-5456, exports `CONTEXT_USAGE_CALIBRATION_MAX`
- order 278: `CONTEXT_ACTUAL_USAGE_RECENT_SECONDS` (constant), lines 5457-5460, exports `CONTEXT_ACTUAL_USAGE_RECENT_SECONDS`
- order 279: `LARGE_FILE_AUTO_PAGE_BYTES` (constant), lines 5461-5464, exports `LARGE_FILE_AUTO_PAGE_BYTES`
- order 280: `LARGE_FILE_AUTO_PAGE_LINES` (constant), lines 5465-5468, exports `LARGE_FILE_AUTO_PAGE_LINES`
- order 281: `LARGE_SOURCE_UPLOAD_EXCERPT_CHARS` (constant), lines 5469-5472, exports `LARGE_SOURCE_UPLOAD_EXCERPT_CHARS`
- order 282: `CHAT_UPLOAD_PARSE_QUEUE_MAX` (constant), lines 5473-5476, exports `CHAT_UPLOAD_PARSE_QUEUE_MAX`
- order 283: `CHAT_UPLOAD_PARSE_TIMEOUT_SECONDS` (constant), lines 5477-5480, exports `CHAT_UPLOAD_PARSE_TIMEOUT_SECONDS`
- order 284: `CHAT_UPLOAD_INLINE_TEXT_BYTES` (constant), lines 5481-5484, exports `CHAT_UPLOAD_INLINE_TEXT_BYTES`
- order 285: `CHAT_UPLOAD_PARSE_MAX_BYTES` (constant), lines 5485-5491, exports `CHAT_UPLOAD_PARSE_MAX_BYTES`
- order 286: `CHAT_UPLOAD_ZIP_ENTRY_MAX_BYTES` (constant), lines 5492-5498, exports `CHAT_UPLOAD_ZIP_ENTRY_MAX_BYTES`
- order 287: `CHAT_UPLOAD_TEXT_CONTEXT_CHARS` (constant), lines 5499-5502, exports `CHAT_UPLOAD_TEXT_CONTEXT_CHARS`
- order 288: `CHAT_UPLOAD_PROMPT_MAX_FILES` (constant), lines 5503-5506, exports `CHAT_UPLOAD_PROMPT_MAX_FILES`
- order 289: `CHAT_UPLOAD_PROMPT_MAX_CHARS` (constant), lines 5507-5510, exports `CHAT_UPLOAD_PROMPT_MAX_CHARS`
- order 290: `CHAT_UPLOAD_PROMPT_PER_FILE_CHARS` (constant), lines 5511-5514, exports `CHAT_UPLOAD_PROMPT_PER_FILE_CHARS`
- order 291: `CHAT_UPLOAD_FRONTEND_WAIT_MS` (constant), lines 5515-5518, exports `CHAT_UPLOAD_FRONTEND_WAIT_MS`
- order 292: `CHAT_UPLOAD_AUTO_LIBRARY_INGEST` (constant), lines 5519-5522, exports `CHAT_UPLOAD_AUTO_LIBRARY_INGEST`
- order 293: `CHAT_UPLOAD_INGEST_QUEUE_MAX` (constant), lines 5523-5526, exports `CHAT_UPLOAD_INGEST_QUEUE_MAX`
- order 294: `SESSION_SUBMIT_LOCK_TIMEOUT_SECONDS` (constant), lines 5527-5530, exports `SESSION_SUBMIT_LOCK_TIMEOUT_SECONDS`
- order 295: `SESSION_DEFERRED_START_QUEUE_MAX` (constant), lines 5531-5534, exports `SESSION_DEFERRED_START_QUEUE_MAX`
- order 296: `SESSION_SUBMISSION_DEDUPE_MAX` (constant), lines 5535-5535, exports `SESSION_SUBMISSION_DEDUPE_MAX`
- order 297: `SESSION_SUBMISSION_DEDUPE_SECONDS` (constant), lines 5536-5536, exports `SESSION_SUBMISSION_DEDUPE_SECONDS`
- order 298: `SCHEDULER_SUBMISSION_DEDUPE_MAX` (constant), lines 5537-5537, exports `SCHEDULER_SUBMISSION_DEDUPE_MAX`
- order 299: `FAST_START_LOCAL_CLASSIFICATION` (constant), lines 5538-5540, exports `FAST_START_LOCAL_CLASSIFICATION`
- order 300: `FAST_START_LOCAL_TITLE` (constant), lines 5541-5543, exports `FAST_START_LOCAL_TITLE`
- order 301: `AUTO_TITLE_MODEL_REFINE` (constant), lines 5544-5546, exports `AUTO_TITLE_MODEL_REFINE`
- order 302: `AUTO_TITLE_MODEL_TIMEOUT_SECONDS` (constant), lines 5547-5550, exports `AUTO_TITLE_MODEL_TIMEOUT_SECONDS`
- order 303: `AUTO_TITLE_MODEL_RETRY_COOLDOWN_SECONDS` (constant), lines 5551-5557, exports `AUTO_TITLE_MODEL_RETRY_COOLDOWN_SECONDS`
- order 304: `FAST_START_DEFER_CAPABILITY_PROBE` (constant), lines 5558-5560, exports `FAST_START_DEFER_CAPABILITY_PROBE`
- order 305: `SESSION_RUNTIME_MESSAGE_WINDOW` (constant), lines 5561-5561, exports `SESSION_RUNTIME_MESSAGE_WINDOW`
- order 306: `SESSION_RUNTIME_ACTIVITY_WINDOW` (constant), lines 5562-5562, exports `SESSION_RUNTIME_ACTIVITY_WINDOW`
- order 307: `SESSION_RUNTIME_OPERATION_WINDOW` (constant), lines 5563-5563, exports `SESSION_RUNTIME_OPERATION_WINDOW`
- order 308: `SESSION_RUNTIME_UPLOAD_WINDOW` (constant), lines 5564-5564, exports `SESSION_RUNTIME_UPLOAD_WINDOW`
- order 309: `LITE_SNAPSHOT_MAX_BYTES` (constant), lines 5565-5568, exports `LITE_SNAPSHOT_MAX_BYTES`
- order 310: `LITE_SNAPSHOT_MESSAGES_BYTES` (constant), lines 5569-5569, exports `LITE_SNAPSHOT_MESSAGES_BYTES`
- order 311: `LITE_SNAPSHOT_FEED_BYTES` (constant), lines 5570-5570, exports `LITE_SNAPSHOT_FEED_BYTES`
- order 312: `LITE_SNAPSHOT_OPERATIONS_BYTES` (constant), lines 5571-5571, exports `LITE_SNAPSHOT_OPERATIONS_BYTES`
- order 313: `IDE_AGENT_STATE_MAX_BYTES` (constant), lines 5572-5575, exports `IDE_AGENT_STATE_MAX_BYTES`
- order 314: `IDE_AGENT_FEED_BYTES` (constant), lines 5576-5576, exports `IDE_AGENT_FEED_BYTES`
- order 315: `IDE_AGENT_OPERATIONS_BYTES` (constant), lines 5577-5577, exports `IDE_AGENT_OPERATIONS_BYTES`
- order 316: `SESSION_WATCHDOG_INTERVAL_SECONDS` (constant), lines 5578-5581, exports `SESSION_WATCHDOG_INTERVAL_SECONDS`
- order 317: `SESSION_HEARTBEAT_STALE_SECONDS` (constant), lines 5582-5585, exports `SESSION_HEARTBEAT_STALE_SECONDS`
- order 318: `SESSION_LIST_DEFAULT_LIMIT` (constant), lines 5586-5589, exports `SESSION_LIST_DEFAULT_LIMIT`
- order 319: `SESSION_INDEX_SYNC_SNAPSHOT_MAX` (constant), lines 5590-5593, exports `SESSION_INDEX_SYNC_SNAPSHOT_MAX`
- order 320: `SESSION_INDEX_JOURNAL_COMPACT_RECORDS` (constant), lines 5594-5597, exports `SESSION_INDEX_JOURNAL_COMPACT_RECORDS`
- order 321: `SESSION_INDEX_JOURNAL_COMPACT_BYTES` (constant), lines 5598-5601, exports `SESSION_INDEX_JOURNAL_COMPACT_BYTES`
- order 322: `SESSION_CATALOG_RECENT_MAX` (constant), lines 5602-5605, exports `SESSION_CATALOG_RECENT_MAX`
- order 323: `IDE_SESSION_LIST_DEFAULT_LIMIT` (constant), lines 5606-5609, exports `IDE_SESSION_LIST_DEFAULT_LIMIT`
- order 324: `IDLE_TIMEOUT` (constant), lines 5610-5610, exports `IDLE_TIMEOUT`
- order 325: `POLL_INTERVAL` (constant), lines 5611-5611, exports `POLL_INTERVAL`
- order 326: `SSE_HEARTBEAT_SECONDS` (constant), lines 5612-5612, exports `SSE_HEARTBEAT_SECONDS`
- order 327: `MODEL_CALL_PROGRESS_DELAY` (constant), lines 5613-5613, exports `MODEL_CALL_PROGRESS_DELAY`
- order 328: `MODEL_CALL_PROGRESS_INTERVAL` (constant), lines 5614-5614, exports `MODEL_CALL_PROGRESS_INTERVAL`
- order 329: `RUN_COMPLETION_SUMMARY_ENABLED` (constant), lines 5615-5618, exports `RUN_COMPLETION_SUMMARY_ENABLED`
- order 330: `LLM_HTTP_RETRY_MAX_ATTEMPTS` (constant), lines 5619-5622, exports `LLM_HTTP_RETRY_MAX_ATTEMPTS`
- order 331: `LLM_HTTP_RETRY_DELAY_SECONDS` (constant), lines 5623-5626, exports `LLM_HTTP_RETRY_DELAY_SECONDS`
- order 332: `LLM_HTTP_RETRY_MAX_SECONDS` (constant), lines 5627-5630, exports `LLM_HTTP_RETRY_MAX_SECONDS`
- order 333: `LLM_HTTP_RETRY_404_ON_VLLM` (constant), lines 5631-5634, exports `LLM_HTTP_RETRY_404_ON_VLLM`
- order 334: `LLM_HTTP_RETRY_STATUSES` (constant), lines 5635-5635, exports `LLM_HTTP_RETRY_STATUSES`
- order 335: `MAX_AGENT_ROUNDS` (constant), lines 5636-5636, exports `MAX_AGENT_ROUNDS`
- order 336: `MIN_AGENT_ROUNDS` (constant), lines 5637-5637, exports `MIN_AGENT_ROUNDS`
- order 337: `MAX_AGENT_ROUNDS_CAP` (constant), lines 5638-5638, exports `MAX_AGENT_ROUNDS_CAP`
- order 338: `REPEATED_TOOL_LOOP_THRESHOLD` (constant), lines 5639-5639, exports `REPEATED_TOOL_LOOP_THRESHOLD`
- order 339: `BASH_READ_LOOP_THRESHOLD` (constant), lines 5640-5640, exports `BASH_READ_LOOP_THRESHOLD`
- order 340: `READ_FILE_LOOP_THRESHOLD` (constant), lines 5641-5641, exports `READ_FILE_LOOP_THRESHOLD`
- order 341: `READ_FILE_LOOP_DISTINCT_SOFT_LIMIT` (constant), lines 5642-5642, exports `READ_FILE_LOOP_DISTINCT_SOFT_LIMIT`
- order 342: `READ_FILE_COMPACT_PIN_DISTINCT` (constant), lines 5643-5643, exports `READ_FILE_COMPACT_PIN_DISTINCT`
- order 343: `READ_FILE_COMPACT_PIN_MAX_CHARS` (constant), lines 5644-5644, exports `READ_FILE_COMPACT_PIN_MAX_CHARS`
- order 344: `READ_FILE_PIN_TOTAL_CHARS` (constant), lines 5645-5647, exports `READ_FILE_PIN_TOTAL_CHARS`
- order 346: `READ_RESULT_PLACEHOLDER_PREFIXES` (constant), lines 5652-5661, exports `READ_RESULT_PLACEHOLDER_PREFIXES`
- order 347: `READ_CONTEXT_REGISTRY_MAX` (constant), lines 5662-5662, exports `READ_CONTEXT_REGISTRY_MAX`
- order 348: `READ_CONTEXT_PROMPT_MAX_ITEMS` (constant), lines 5663-5663, exports `READ_CONTEXT_PROMPT_MAX_ITEMS`
- order 349: `READ_CONTEXT_PROMPT_MAX_CHARS` (constant), lines 5664-5664, exports `READ_CONTEXT_PROMPT_MAX_CHARS`
- order 350: `READ_CONTEXT_SUMMARY_MAX_CHARS` (constant), lines 5665-5665, exports `READ_CONTEXT_SUMMARY_MAX_CHARS`
- order 351: `READ_CONTEXT_SHARED_MAX_ITEMS` (constant), lines 5666-5666, exports `READ_CONTEXT_SHARED_MAX_ITEMS`
- order 352: `READ_CONTEXT_POLICY_CHOICES` (constant), lines 5667-5667, exports `READ_CONTEXT_POLICY_CHOICES`
- order 353: `DEFAULT_READ_CONTEXT_POLICY` (constant), lines 5668-5668, exports `DEFAULT_READ_CONTEXT_POLICY`
- order 354: `READ_CONTEXT_CACHE_SEARCH_MAX_BYTES` (constant), lines 5669-5675, exports `READ_CONTEXT_CACHE_SEARCH_MAX_BYTES`
- order 355: `READ_CONTEXT_CACHE_SEARCH_MAX_MATCHES` (constant), lines 5676-5676, exports `READ_CONTEXT_CACHE_SEARCH_MAX_MATCHES`
- order 356: `READ_CONTEXT_CACHE_SNIPPET_CHARS` (constant), lines 5677-5677, exports `READ_CONTEXT_CACHE_SNIPPET_CHARS`
- order 357: `READ_CONTEXT_CACHE_LINE_CONTEXT` (constant), lines 5678-5678, exports `READ_CONTEXT_CACHE_LINE_CONTEXT`
- order 358: `LONG_CONTENT_SOURCE_CACHE_MAX_BYTES` (constant), lines 5679-5685, exports `LONG_CONTENT_SOURCE_CACHE_MAX_BYTES`
- order 359: `LONG_CONTENT_SOURCE_CACHE_MAX_FILES` (constant), lines 5686-5689, exports `LONG_CONTENT_SOURCE_CACHE_MAX_FILES`
- order 360: `LONG_CONTENT_SYMBOL_MEMORY_MAX` (constant), lines 5690-5693, exports `LONG_CONTENT_SYMBOL_MEMORY_MAX`
- order 361: `TOOL_MEMORY_REGISTRY_MAX` (constant), lines 5694-5694, exports `TOOL_MEMORY_REGISTRY_MAX`
- order 362: `TOOL_MEMORY_PROMPT_MAX_ITEMS` (constant), lines 5695-5695, exports `TOOL_MEMORY_PROMPT_MAX_ITEMS`
- order 363: `TOOL_MEMORY_PROMPT_MAX_CHARS` (constant), lines 5696-5696, exports `TOOL_MEMORY_PROMPT_MAX_CHARS`
- order 364: `TOOL_MEMORY_SUMMARY_MAX_CHARS` (constant), lines 5697-5697, exports `TOOL_MEMORY_SUMMARY_MAX_CHARS`
- order 365: `TOOL_MEMORY_SHARED_MAX_ITEMS` (constant), lines 5698-5698, exports `TOOL_MEMORY_SHARED_MAX_ITEMS`
- order 366: `TOOL_MEMORY_COMPACT_PIN_DISTINCT` (constant), lines 5699-5699, exports `TOOL_MEMORY_COMPACT_PIN_DISTINCT`
- order 367: `TOOL_MEMORY_COMPACT_PIN_MAX_CHARS` (constant), lines 5700-5700, exports `TOOL_MEMORY_COMPACT_PIN_MAX_CHARS`
- order 368: `TOOL_MEMORY_POLICY_CHOICES` (constant), lines 5701-5701, exports `TOOL_MEMORY_POLICY_CHOICES`
- order 369: `DEFAULT_TOOL_MEMORY_POLICY` (constant), lines 5702-5702, exports `DEFAULT_TOOL_MEMORY_POLICY`
- order 370: `LONG_CONTENT_MEMORY_VERSION` (constant), lines 5703-5715, exports `LONG_CONTENT_MEMORY_VERSION`
- order 371: `LONG_CONTENT_MEMORY_MAX_ITEMS` (constant), lines 5716-5719, exports `LONG_CONTENT_MEMORY_MAX_ITEMS`
- order 372: `LONG_CONTENT_MEMORY_MAX_SEGMENTS` (constant), lines 5720-5723, exports `LONG_CONTENT_MEMORY_MAX_SEGMENTS`
- order 373: `LONG_CONTENT_TEXT_SEGMENT_LINES` (constant), lines 5724-5727, exports `LONG_CONTENT_TEXT_SEGMENT_LINES`
- order 374: `LONG_CONTENT_CODE_SEGMENT_LINES` (constant), lines 5728-5731, exports `LONG_CONTENT_CODE_SEGMENT_LINES`
- order 375: `LONG_CONTENT_CARD_CHARS` (constant), lines 5732-5735, exports `LONG_CONTENT_CARD_CHARS`
- order 376: `LONG_CONTENT_STRUCTURE_MAX_CHARS` (constant), lines 5736-5739, exports `LONG_CONTENT_STRUCTURE_MAX_CHARS`
- order 377: `LONG_CONTENT_SEMANTIC_ENABLED` (constant), lines 5740-5747, exports `LONG_CONTENT_SEMANTIC_ENABLED`
- order 378: `LONG_CONTENT_SEMANTIC_TIMEOUT_SECONDS` (constant), lines 5748-5751, exports `LONG_CONTENT_SEMANTIC_TIMEOUT_SECONDS`
- order 379: `LONG_CONTENT_SEMANTIC_MAX_INPUT_CHARS` (constant), lines 5752-5755, exports `LONG_CONTENT_SEMANTIC_MAX_INPUT_CHARS`
- order 380: `LONG_CONTENT_SEMANTIC_MAX_OUTPUT_TOKENS` (constant), lines 5756-5759, exports `LONG_CONTENT_SEMANTIC_MAX_OUTPUT_TOKENS`
- order 381: `LONG_CONTENT_SEMANTIC_MAX_KEY_POINTS` (constant), lines 5760-5760, exports `LONG_CONTENT_SEMANTIC_MAX_KEY_POINTS`
- order 382: `LONG_CONTENT_SEMANTIC_MAX_DEFINITIONS` (constant), lines 5761-5761, exports `LONG_CONTENT_SEMANTIC_MAX_DEFINITIONS`
- order 383: `LONG_CONTENT_SEMANTIC_MAX_RELATIONS` (constant), lines 5762-5762, exports `LONG_CONTENT_SEMANTIC_MAX_RELATIONS`
- order 384: `LONG_CONTENT_SEMANTIC_MAX_UNCERTAINTIES` (constant), lines 5763-5763, exports `LONG_CONTENT_SEMANTIC_MAX_UNCERTAINTIES`
- order 385: `LONG_CONTENT_SEMANTIC_MAX_EVIDENCE` (constant), lines 5764-5764, exports `LONG_CONTENT_SEMANTIC_MAX_EVIDENCE`
- order 386: `LONG_CONTENT_SEMANTIC_MAX_NEXT_SEGMENTS` (constant), lines 5765-5765, exports `LONG_CONTENT_SEMANTIC_MAX_NEXT_SEGMENTS`
- order 387: `LONG_CONTENT_SEMANTIC_MAX_COVERED` (constant), lines 5766-5766, exports `LONG_CONTENT_SEMANTIC_MAX_COVERED`
- order 388: `LONG_CONTENT_SEMANTIC_MAX_OPEN_QUESTIONS` (constant), lines 5767-5767, exports `LONG_CONTENT_SEMANTIC_MAX_OPEN_QUESTIONS`
- order 389: `LONG_CONTENT_SEMANTIC_MAX_REFRESHES` (constant), lines 5768-5771, exports `LONG_CONTENT_SEMANTIC_MAX_REFRESHES`
- order 390: `LONG_CONTENT_OBSERVATION_MAX` (constant), lines 5772-5775, exports `LONG_CONTENT_OBSERVATION_MAX`
- order 391: `LONG_CONTENT_OBSERVATION_MAX_RANGES` (constant), lines 5776-5776, exports `LONG_CONTENT_OBSERVATION_MAX_RANGES`
- order 392: `LONG_CONTENT_OBSERVATION_MAX_EXCERPTS` (constant), lines 5777-5777, exports `LONG_CONTENT_OBSERVATION_MAX_EXCERPTS`
- order 393: `LONG_CONTENT_OBSERVATION_EXCERPT_CHARS` (constant), lines 5778-5778, exports `LONG_CONTENT_OBSERVATION_EXCERPT_CHARS`
- order 394: `LONG_CONTENT_RELATED_SOURCE_MAX` (constant), lines 5779-5779, exports `LONG_CONTENT_RELATED_SOURCE_MAX`
- order 395: `SHELL_SOURCE_CANDIDATE_MAX` (constant), lines 5780-5780, exports `SHELL_SOURCE_CANDIDATE_MAX`
- order 396: `LONG_CONTENT_TEXT_EXTS` (constant), lines 5781-5783, exports `LONG_CONTENT_TEXT_EXTS`
- order 397: `LONG_CONTENT_DATA_EXTS` (constant), lines 5784-5788, exports `LONG_CONTENT_DATA_EXTS`
- order 398: `DEFAULT_AUTO_TASK_LEVEL_CEILING` (constant), lines 5789-5789, exports `DEFAULT_AUTO_TASK_LEVEL_CEILING`
- order 404: `HARD_BREAK_TOOL_ERROR_THRESHOLD` (constant), lines 5809-5809, exports `HARD_BREAK_TOOL_ERROR_THRESHOLD`
- order 405: `HARD_BREAK_RECOVERY_ROUND_THRESHOLD` (constant), lines 5810-5812, exports `HARD_BREAK_RECOVERY_ROUND_THRESHOLD`
- order 406: `FUSED_FAULT_BREAK_THRESHOLD` (constant), lines 5813-5813, exports `FUSED_FAULT_BREAK_THRESHOLD`
- order 407: `STALL_SEVERITY_ESCALATION_THRESHOLD` (constant), lines 5814-5814, exports `STALL_SEVERITY_ESCALATION_THRESHOLD`
- order 408: `STALL_SEVERITY_WEIGHT_BASH_READ_LOOP` (constant), lines 5815-5815, exports `STALL_SEVERITY_WEIGHT_BASH_READ_LOOP`
- order 409: `STALL_SEVERITY_WEIGHT_REPEATED_TOOL` (constant), lines 5816-5816, exports `STALL_SEVERITY_WEIGHT_REPEATED_TOOL`
- order 410: `STALL_SEVERITY_WEIGHT_FAULT` (constant), lines 5817-5817, exports `STALL_SEVERITY_WEIGHT_FAULT`
- order 411: `STALL_SEVERITY_WEIGHT_RECOVERY_RETRY` (constant), lines 5818-5818, exports `STALL_SEVERITY_WEIGHT_RECOVERY_RETRY`
- order 412: `STALL_SEVERITY_WEIGHT_WATCHDOG` (constant), lines 5819-5819, exports `STALL_SEVERITY_WEIGHT_WATCHDOG`
- order 413: `STALL_SEVERITY_DECAY_ON_SUCCESS` (constant), lines 5820-5820, exports `STALL_SEVERITY_DECAY_ON_SUCCESS`
- order 414: `STALL_ESCALATION_MIN_LEVEL` (constant), lines 5821-5821, exports `STALL_ESCALATION_MIN_LEVEL`
- order 415: `STALL_PLAN_SYNTHESIS_MAX_TOKENS` (constant), lines 5822-5822, exports `STALL_PLAN_SYNTHESIS_MAX_TOKENS`
- order 416: `STALL_ESCALATION_CONTEXT_MAX_CHARS` (constant), lines 5823-5823, exports `STALL_ESCALATION_CONTEXT_MAX_CHARS`
- order 417: `MAX_RUN_SECONDS` (constant), lines 5824-5824, exports `MAX_RUN_SECONDS`
- order 418: `MIN_RUN_TIMEOUT_SECONDS` (constant), lines 5825-5825, exports `MIN_RUN_TIMEOUT_SECONDS`
- order 419: `MAX_RUN_TIMEOUT_SECONDS` (constant), lines 5826-5826, exports `MAX_RUN_TIMEOUT_SECONDS`
- order 420: `MIN_TIMEOUT_SECONDS` (constant), lines 5827-5827, exports `MIN_TIMEOUT_SECONDS`
- order 421: `MAX_TIMEOUT_SECONDS` (constant), lines 5828-5828, exports `MAX_TIMEOUT_SECONDS`
- order 422: `DEFAULT_TIMEOUT_SECONDS` (constant), lines 5829-5835, exports `DEFAULT_TIMEOUT_SECONDS`
- order 423: `DEFAULT_REQUEST_TIMEOUT` (constant), lines 5836-5836, exports `DEFAULT_REQUEST_TIMEOUT`
- order 424: `_SHELL_AUTO_CONFIRM_PATTERNS` (assignment), lines 5837-5852, exports `_SHELL_AUTO_CONFIRM_PATTERNS`
- order 425: `MIN_SHELL_COMMAND_TIMEOUT_SECONDS` (constant), lines 5853-5853, exports `MIN_SHELL_COMMAND_TIMEOUT_SECONDS`
- order 426: `MAX_SHELL_COMMAND_TIMEOUT_SECONDS` (constant), lines 5854-5854, exports `MAX_SHELL_COMMAND_TIMEOUT_SECONDS`
- order 427: `SHELL_TIMEOUT_MODES` (constant), lines 5855-5855, exports `SHELL_TIMEOUT_MODES`
- order 428: `_DEFAULT_SHELL_TIMEOUT_MODE_RAW` (assignment), lines 5856-5859, exports `_DEFAULT_SHELL_TIMEOUT_MODE_RAW`
- order 429: `DEFAULT_SHELL_TIMEOUT_MODE` (constant), lines 5860-5864, exports `DEFAULT_SHELL_TIMEOUT_MODE`
- order 430: `MIN_SHELL_ASYNC_HANDOFF_SECONDS` (constant), lines 5865-5865, exports `MIN_SHELL_ASYNC_HANDOFF_SECONDS`
- order 431: `MAX_SHELL_ASYNC_HANDOFF_SECONDS` (constant), lines 5866-5866, exports `MAX_SHELL_ASYNC_HANDOFF_SECONDS`
- order 432: `SHELL_FAILURE_GUIDANCE_SECONDS` (constant), lines 5867-5869, exports `SHELL_FAILURE_GUIDANCE_SECONDS`
- order 433: `DEFAULT_SHELL_ASYNC_HANDOFF_SECONDS` (constant), lines 5870-5884, exports `DEFAULT_SHELL_ASYNC_HANDOFF_SECONDS`
- order 434: `DEFAULT_SHELL_COMMAND_TIMEOUT_SECONDS` (constant), lines 5885-5899, exports `DEFAULT_SHELL_COMMAND_TIMEOUT_SECONDS`
- order 435: `DEFAULT_SINGLE_NO_PLAN_TODO_PROMPT` (constant), lines 5900-5914, exports `DEFAULT_SINGLE_NO_PLAN_TODO_PROMPT`
- order 436: `SINGLE_NO_PLAN_TODO_BOOTSTRAP_MAX_ATTEMPTS` (constant), lines 5915-5915, exports `SINGLE_NO_PLAN_TODO_BOOTSTRAP_MAX_ATTEMPTS`
- order 437: `AUTO_CONTINUE_BUDGET_DEFAULT` (constant), lines 5916-5916, exports `AUTO_CONTINUE_BUDGET_DEFAULT`
- order 438: `AGENT_MAX_OUTPUT_TOKENS` (constant), lines 5917-5917, exports `AGENT_MAX_OUTPUT_TOKENS`
- order 439: `OLLAMA_THINKING_TOOL_BUFFER` (constant), lines 5918-5918, exports `OLLAMA_THINKING_TOOL_BUFFER`
- order 440: `WATCHDOG_INTENT_NO_TOOL_THRESHOLD` (constant), lines 5919-5919, exports `WATCHDOG_INTENT_NO_TOOL_THRESHOLD`
- order 441: `WATCHDOG_REPEAT_NO_TOOL_THRESHOLD` (constant), lines 5920-5920, exports `WATCHDOG_REPEAT_NO_TOOL_THRESHOLD`
- order 442: `WATCHDOG_INTENT_NO_TOOL_THRESHOLD_SINGLE` (constant), lines 5921-5921, exports `WATCHDOG_INTENT_NO_TOOL_THRESHOLD_SINGLE`
- order 443: `WATCHDOG_REPEAT_NO_TOOL_THRESHOLD_SINGLE` (constant), lines 5922-5922, exports `WATCHDOG_REPEAT_NO_TOOL_THRESHOLD_SINGLE`
- order 444: `WATCHDOG_STATE_STALL_THRESHOLD` (constant), lines 5923-5923, exports `WATCHDOG_STATE_STALL_THRESHOLD`
- order 445: `WATCHDOG_CONTEXT_STALL_THRESHOLD` (constant), lines 5924-5924, exports `WATCHDOG_CONTEXT_STALL_THRESHOLD`
- order 446: `WATCHDOG_REPEAT_SIMILARITY_THRESHOLD` (constant), lines 5925-5925, exports `WATCHDOG_REPEAT_SIMILARITY_THRESHOLD`
- order 447: `WATCHDOG_CONTEXT_NEAR_RATIO` (constant), lines 5926-5926, exports `WATCHDOG_CONTEXT_NEAR_RATIO`
- order 448: `WATCHDOG_MAX_DECOMPOSE_STEPS` (constant), lines 5927-5927, exports `WATCHDOG_MAX_DECOMPOSE_STEPS`
- order 449: `WATCHDOG_STEP_MAX_ATTEMPTS` (constant), lines 5928-5928, exports `WATCHDOG_STEP_MAX_ATTEMPTS`
- order 450: `EMPTY_ACTION_MIN_CONTENT_CHARS` (constant), lines 5929-5929, exports `EMPTY_ACTION_MIN_CONTENT_CHARS`
- order 451: `EMPTY_ACTION_WAKEUP_RETRY_LIMIT` (constant), lines 5930-5930, exports `EMPTY_ACTION_WAKEUP_RETRY_LIMIT`
- order 452: `EMPTY_ACTION_INTERVENTION_THRESHOLD` (constant), lines 5931-5937, exports `EMPTY_ACTION_INTERVENTION_THRESHOLD`
- order 453: `EMPTY_ACTION_BOOTSTRAP_THINKING_GRACE_ROUNDS` (constant), lines 5938-5942, exports `EMPTY_ACTION_BOOTSTRAP_THINKING_GRACE_ROUNDS`
- order 454: `EMPTY_ACTION_RECOVERY_MAX_TOKENS` (constant), lines 5943-5943, exports `EMPTY_ACTION_RECOVERY_MAX_TOKENS`
- order 455: `THINKING_BUDGET_FORCE_RATIO` (constant), lines 5944-5944, exports `THINKING_BUDGET_FORCE_RATIO`
- order 456: `_TOOL_TIMEOUT_MAP` (assignment), lines 5945-5966, exports `_TOOL_TIMEOUT_MAP`
- order 457: `_DEFAULT_TOOL_TIMEOUT` (assignment), lines 5967-5967, exports `_DEFAULT_TOOL_TIMEOUT`
- order 460: `CONVERSATION_VISIBLE_TOOL_EVENTS` (constant), lines 5973-5985, exports `CONVERSATION_VISIBLE_TOOL_EVENTS`
- order 461: `PERSIST_ON_EVENT_TYPES` (constant), lines 5986-6004, exports `PERSIST_ON_EVENT_TYPES`
- order 462: `PERSIST_EVENT_MIN_INTERVAL_SECONDS` (constant), lines 6005-6005, exports `PERSIST_EVENT_MIN_INTERVAL_SECONDS`
- order 463: `TRUNCATION_CONTINUATION_MAX_PASSES` (constant), lines 6006-6006, exports `TRUNCATION_CONTINUATION_MAX_PASSES`
- order 464: `TRUNCATION_CONTINUATION_MAX_TOKENS` (constant), lines 6007-6007, exports `TRUNCATION_CONTINUATION_MAX_TOKENS`
- order 465: `TRUNCATION_CONTINUATION_TAIL_CHARS` (constant), lines 6008-6008, exports `TRUNCATION_CONTINUATION_TAIL_CHARS`
- order 466: `TRUNCATION_CONTINUATION_ECHO_CHARS` (constant), lines 6009-6009, exports `TRUNCATION_CONTINUATION_ECHO_CHARS`
- order 467: `TRUNCATION_OVERLAP_SCAN_CHARS` (constant), lines 6010-6010, exports `TRUNCATION_OVERLAP_SCAN_CHARS`
- order 468: `TRUNCATION_PAIR_SCAN_CHARS` (constant), lines 6011-6011, exports `TRUNCATION_PAIR_SCAN_CHARS`
- order 469: `TRUNCATION_LIVE_BUFFER_MAX_CHARS` (constant), lines 6012-6012, exports `TRUNCATION_LIVE_BUFFER_MAX_CHARS`
- order 470: `MIN_CONTEXT_TOKEN_LIMIT` (constant), lines 6013-6013, exports `MIN_CONTEXT_TOKEN_LIMIT`
- order 471: `COMPACT_TIER1_PCT` (constant), lines 6014-6015, exports `COMPACT_TIER1_PCT`
- order 472: `COMPACT_TIER2_PCT` (constant), lines 6016-6016, exports `COMPACT_TIER2_PCT`
- order 473: `COMPACT_TIER3_PCT` (constant), lines 6017-6017, exports `COMPACT_TIER3_PCT`
- order 474: `COMPACT_TIER1_ABS` (constant), lines 6018-6019, exports `COMPACT_TIER1_ABS`
- order 475: `COMPACT_TIER2_ABS` (constant), lines 6020-6020, exports `COMPACT_TIER2_ABS`
- order 476: `CONTEXT_COMPACT_INEFFECTIVE_COOLDOWN_SECONDS` (constant), lines 6021-6027, exports `CONTEXT_COMPACT_INEFFECTIVE_COOLDOWN_SECONDS`
- order 477: `FILE_BUFFER_CONTENT_THRESHOLD` (constant), lines 6028-6029, exports `FILE_BUFFER_CONTENT_THRESHOLD`
- order 478: `FILE_BUFFER_MAX_FILES` (constant), lines 6030-6030, exports `FILE_BUFFER_MAX_FILES`
- order 479: `AUTHORITATIVE_USER_GOAL_OPEN` (constant), lines 6031-6031, exports `AUTHORITATIVE_USER_GOAL_OPEN`
- order 480: `AUTHORITATIVE_USER_GOAL_CLOSE` (constant), lines 6032-6032, exports `AUTHORITATIVE_USER_GOAL_CLOSE`
- order 481: `AGENT_MSG_LIMIT_TIER0` (constant), lines 6033-6034, exports `AGENT_MSG_LIMIT_TIER0`
- order 482: `AGENT_MSG_LIMIT_TIER1` (constant), lines 6035-6035, exports `AGENT_MSG_LIMIT_TIER1`
- order 483: `AGENT_MSG_LIMIT_TIER2` (constant), lines 6036-6036, exports `AGENT_MSG_LIMIT_TIER2`
- order 484: `AGENT_MSG_LIMIT_TIER3` (constant), lines 6037-6037, exports `AGENT_MSG_LIMIT_TIER3`
- order 485: `AGENT_CTX_LIMIT_TIER0` (constant), lines 6038-6038, exports `AGENT_CTX_LIMIT_TIER0`
- order 486: `AGENT_CTX_LIMIT_TIER1` (constant), lines 6039-6039, exports `AGENT_CTX_LIMIT_TIER1`
- order 487: `AGENT_CTX_LIMIT_TIER2` (constant), lines 6040-6040, exports `AGENT_CTX_LIMIT_TIER2`
- order 488: `AGENT_CTX_LIMIT_TIER3` (constant), lines 6041-6041, exports `AGENT_CTX_LIMIT_TIER3`
- order 489: `MANAGER_CTX_LIMIT_TIER0` (constant), lines 6042-6042, exports `MANAGER_CTX_LIMIT_TIER0`
- order 490: `MANAGER_CTX_LIMIT_TIER1` (constant), lines 6043-6043, exports `MANAGER_CTX_LIMIT_TIER1`
- order 491: `MANAGER_CTX_LIMIT_TIER2` (constant), lines 6044-6044, exports `MANAGER_CTX_LIMIT_TIER2`
- order 492: `MANAGER_CTX_LIMIT_TIER3` (constant), lines 6045-6045, exports `MANAGER_CTX_LIMIT_TIER3`
- order 493: `MAX_CONTEXT_ARCHIVE_SEGMENTS` (constant), lines 6046-6046, exports `MAX_CONTEXT_ARCHIVE_SEGMENTS`
- order 494: `MAX_USER_BUBBLE_LOG` (constant), lines 6047-6048, exports `MAX_USER_BUBBLE_LOG`
- order 495: `MANAGER_INSTRUCTION_MAX_CHARS` (constant), lines 6049-6053, exports `MANAGER_INSTRUCTION_MAX_CHARS`
- order 496: `MANAGER_MOMENTUM_MAX_SKIPS` (constant), lines 6054-6059, exports `MANAGER_MOMENTUM_MAX_SKIPS`
- order 497: `MODEL_OUTPUT_RETRY_TIMES` (constant), lines 6060-6064, exports `MODEL_OUTPUT_RETRY_TIMES`
- order 498: `ARBITER_TRIGGER_MIN_CONTENT_CHARS` (constant), lines 6065-6065, exports `ARBITER_TRIGGER_MIN_CONTENT_CHARS`
- order 499: `ARBITER_VALID_PLANNING_STREAK_LIMIT` (constant), lines 6066-6066, exports `ARBITER_VALID_PLANNING_STREAK_LIMIT`
- order 500: `ARBITER_DEFAULT_TIMEOUT_SECONDS` (constant), lines 6067-6067, exports `ARBITER_DEFAULT_TIMEOUT_SECONDS`
- order 501: `ARBITER_DEFAULT_MAX_TOKENS` (constant), lines 6068-6068, exports `ARBITER_DEFAULT_MAX_TOKENS`
- order 502: `ARBITER_DEFAULT_TEMPERATURE` (constant), lines 6069-6069, exports `ARBITER_DEFAULT_TEMPERATURE`
- order 503: `LIVE_INPUT_DELAY_WRITE_ROUNDS` (constant), lines 6070-6070, exports `LIVE_INPUT_DELAY_WRITE_ROUNDS`
- order 504: `LIVE_INPUT_DELAY_TOOL_ROUNDS` (constant), lines 6071-6071, exports `LIVE_INPUT_DELAY_TOOL_ROUNDS`
- order 505: `LIVE_INPUT_DELAY_NORMAL_ROUNDS` (constant), lines 6072-6072, exports `LIVE_INPUT_DELAY_NORMAL_ROUNDS`
- order 506: `LIVE_INPUT_MAX_INJECTIONS` (constant), lines 6073-6073, exports `LIVE_INPUT_MAX_INJECTIONS`
- order 507: `LIVE_INPUT_REINJECT_INTERVAL` (constant), lines 6074-6074, exports `LIVE_INPUT_REINJECT_INTERVAL`
- order 508: `LIVE_INPUT_WEIGHT_BASE_DELAYED` (constant), lines 6075-6075, exports `LIVE_INPUT_WEIGHT_BASE_DELAYED`
- order 509: `LIVE_INPUT_WEIGHT_BASE_NORMAL` (constant), lines 6076-6076, exports `LIVE_INPUT_WEIGHT_BASE_NORMAL`
- order 510: `LIVE_INPUT_WEIGHT_STEP_DELAYED` (constant), lines 6077-6077, exports `LIVE_INPUT_WEIGHT_STEP_DELAYED`
- order 511: `LIVE_INPUT_WEIGHT_STEP_NORMAL` (constant), lines 6078-6078, exports `LIVE_INPUT_WEIGHT_STEP_NORMAL`
- order 513: `BENIGN_SOCKET_DEBUG_LOG_ENABLED` (constant), lines 6085-6091, exports `BENIGN_SOCKET_DEBUG_LOG_ENABLED`
- order 514: `BENIGN_SOCKET_LOG_INTERVAL_SECONDS` (constant), lines 6092-6092, exports `BENIGN_SOCKET_LOG_INTERVAL_SECONDS`
- order 515: `FINAL_SUMMARY_MIN_CHARS` (constant), lines 6093-6093, exports `FINAL_SUMMARY_MIN_CHARS`
- order 516: `FINAL_SUMMARY_STRICT_MIN_CHARS` (constant), lines 6094-6094, exports `FINAL_SUMMARY_STRICT_MIN_CHARS`
- order 517: `RUNTIME_CONTROL_HINT_PREFIXES` (constant), lines 6095-6116, exports `RUNTIME_CONTROL_HINT_PREFIXES`
- order 518: `UI_HIDDEN_RUNTIME_CONTROL_PREFIXES` (constant), lines 6117-6145, exports `UI_HIDDEN_RUNTIME_CONTROL_PREFIXES`
- order 519: `UI_PROJECTED_RUNTIME_CONTROL_TAGS` (constant), lines 6146-6168, exports `UI_PROJECTED_RUNTIME_CONTROL_TAGS`
- order 520: `UI_LEGACY_PROJECTED_RUNTIME_CONTROL_TAGS` (constant), lines 6169-6171, exports `UI_LEGACY_PROJECTED_RUNTIME_CONTROL_TAGS`
- order 521: `RETRY_RUNTIME_HINT_PREFIXES` (constant), lines 6172-6186, exports `RETRY_RUNTIME_HINT_PREFIXES`
- order 522: `EXECUTION_MODE_SINGLE` (constant), lines 6187-6187, exports `EXECUTION_MODE_SINGLE`
- order 523: `EXECUTION_MODE_SEQUENTIAL` (constant), lines 6188-6188, exports `EXECUTION_MODE_SEQUENTIAL`
- order 524: `EXECUTION_MODE_SYNC` (constant), lines 6189-6189, exports `EXECUTION_MODE_SYNC`
- order 525: `EXECUTION_MODE_CHOICES` (constant), lines 6190-6194, exports `EXECUTION_MODE_CHOICES`
- order 526: `AGENT_ROLES` (constant), lines 6195-6195, exports `AGENT_ROLES`
- order 527: `AGENT_BUBBLE_ROLES` (constant), lines 6196-6196, exports `AGENT_BUBBLE_ROLES`
- order 528: `AGENT_ROLE_LABELS` (constant), lines 6197-6203, exports `AGENT_ROLE_LABELS`
- order 529: `AGENT_ROLE_BUBBLE_COLORS` (constant), lines 6204-6210, exports `AGENT_ROLE_BUBBLE_COLORS`
- order 530: `BLACKBOARD_STATUSES` (constant), lines 6211-6220, exports `BLACKBOARD_STATUSES`
- order 531: `TASK_COMPLEXITY_LEVELS` (constant), lines 6221-6221, exports `TASK_COMPLEXITY_LEVELS`
- order 532: `TASK_COMPLEXITY_RANKS` (constant), lines 6222-6227, exports `TASK_COMPLEXITY_RANKS`
- order 533: `TASK_PROFILE_TYPES` (constant), lines 6228-6234, exports `TASK_PROFILE_TYPES`
- order 534: `TASK_LEVEL_CHOICES` (constant), lines 6235-6235, exports `TASK_LEVEL_CHOICES`
- order 535: `TASK_SCALE_PREFERENCES` (constant), lines 6236-6236, exports `TASK_SCALE_PREFERENCES`
- order 536: `SEMANTIC_CONFIDENCE_CHOICES` (constant), lines 6237-6237, exports `SEMANTIC_CONFIDENCE_CHOICES`
- order 537: `L2_TODO_POLICY_CHOICES` (constant), lines 6238-6242, exports `L2_TODO_POLICY_CHOICES`
- order 538: `DEFAULT_L2_TODO_POLICY` (constant), lines 6243-6243, exports `DEFAULT_L2_TODO_POLICY`
- order 539: `TASK_LEVEL_POLICIES` (constant), lines 6244-6297, exports `TASK_LEVEL_POLICIES`
- order 540: `MANAGER_ROUTE_TARGETS` (constant), lines 6298-6298, exports `MANAGER_ROUTE_TARGETS`
- order 541: `BLACKBOARD_MAX_LOG_ENTRIES` (constant), lines 6299-6299, exports `BLACKBOARD_MAX_LOG_ENTRIES`
- order 542: `BLACKBOARD_MAX_TEXT` (constant), lines 6300-6300, exports `BLACKBOARD_MAX_TEXT`
- order 543: `BLACKBOARD_MEMORY_SHORT_MAX` (constant), lines 6301-6301, exports `BLACKBOARD_MEMORY_SHORT_MAX`
- order 544: `BLACKBOARD_MEMORY_MID_MAX_STEPS` (constant), lines 6302-6302, exports `BLACKBOARD_MEMORY_MID_MAX_STEPS`
- order 545: `BLACKBOARD_MEMORY_MID_ITEMS_PER_STEP` (constant), lines 6303-6303, exports `BLACKBOARD_MEMORY_MID_ITEMS_PER_STEP`
- order 546: `BLACKBOARD_MEMORY_LONG_MAX` (constant), lines 6304-6304, exports `BLACKBOARD_MEMORY_LONG_MAX`
- order 547: `BLACKBOARD_MEMORY_INDEX_MAX` (constant), lines 6305-6305, exports `BLACKBOARD_MEMORY_INDEX_MAX`
- order 548: `SKILL_REFRESH_MIN_INTERVAL_SECONDS` (constant), lines 6306-6306, exports `SKILL_REFRESH_MIN_INTERVAL_SECONDS`
- order 553: `SKILL_RECALL_CACHE_TTL_SECONDS` (constant), lines 6317-6317, exports `SKILL_RECALL_CACHE_TTL_SECONDS`
- order 554: `SKILL_RECALL_CACHE_MAX_ENTRIES` (constant), lines 6318-6318, exports `SKILL_RECALL_CACHE_MAX_ENTRIES`
- order 555: `SKILL_RECALL_GENERIC_TOKENS` (constant), lines 6319-6325, exports `SKILL_RECALL_GENERIC_TOKENS`
- order 557: `SKILL_CATALOG_FULL_REFRESH_SECONDS` (constant), lines 6347-6350, exports `SKILL_CATALOG_FULL_REFRESH_SECONDS`
- order 558: `SKILL_PROMPT_MAX_ITEMS` (constant), lines 6351-6351, exports `SKILL_PROMPT_MAX_ITEMS`
- order 559: `SKILL_PROMPT_MAX_CHARS` (constant), lines 6352-6352, exports `SKILL_PROMPT_MAX_CHARS`
- order 560: `SKILL_RUNTIME_CACHE_MAX_ENTRIES` (constant), lines 6353-6353, exports `SKILL_RUNTIME_CACHE_MAX_ENTRIES`
- order 561: `SKILL_RUNTIME_CACHE_MAX_BYTES` (constant), lines 6354-6354, exports `SKILL_RUNTIME_CACHE_MAX_BYTES`
- order 562: `SKILL_AUTOLOAD_SCORE_THRESHOLD` (constant), lines 6355-6358, exports `SKILL_AUTOLOAD_SCORE_THRESHOLD`
- order 563: `SKILL_AUTOLOAD_CONFIDENCE_THRESHOLD` (constant), lines 6359-6359, exports `SKILL_AUTOLOAD_CONFIDENCE_THRESHOLD`
- order 564: `SKILL_RUNTIME_EVALUATION_TTL_SECONDS` (constant), lines 6360-6360, exports `SKILL_RUNTIME_EVALUATION_TTL_SECONDS`
- order 565: `SKILL_RUNTIME_EVALUATION_TIMEOUT_SECONDS` (constant), lines 6361-6361, exports `SKILL_RUNTIME_EVALUATION_TIMEOUT_SECONDS`
- order 566: `ACCEPTANCE_VERIFY_TIMEOUT_SECONDS` (constant), lines 6362-6367, exports `ACCEPTANCE_VERIFY_TIMEOUT_SECONDS`
- order 567: `SKILL_RUNTIME_UNLOAD_CONFIDENCE_THRESHOLD` (constant), lines 6368-6368, exports `SKILL_RUNTIME_UNLOAD_CONFIDENCE_THRESHOLD`
- order 568: `SKILL_RUNTIME_KEY_TOOL_INTERVAL` (constant), lines 6369-6369, exports `SKILL_RUNTIME_KEY_TOOL_INTERVAL`
- order 569: `SKILL_RUNTIME_EVENTS_MAX` (constant), lines 6370-6370, exports `SKILL_RUNTIME_EVENTS_MAX`
- order 570: `SKILL_METADATA_CAPSULE_MAX_CHARS` (constant), lines 6371-6371, exports `SKILL_METADATA_CAPSULE_MAX_CHARS`
- order 571: `SKILL_DEPENDENCY_MAX_DEPTH` (constant), lines 6372-6372, exports `SKILL_DEPENDENCY_MAX_DEPTH`
- order 572: `AUTO_SKILLS_ROOT_CANDIDATES` (constant), lines 6373-6373, exports `AUTO_SKILLS_ROOT_CANDIDATES`
- order 573: `SKILL_DEFAULT_ATTACHMENT_GLOBS` (constant), lines 6374-6404, exports `SKILL_DEFAULT_ATTACHMENT_GLOBS`
- order 574: `SKILL_INLINE_ATTACHMENT_MAX_FILES` (constant), lines 6405-6405, exports `SKILL_INLINE_ATTACHMENT_MAX_FILES`
- order 575: `SKILL_INLINE_ATTACHMENT_MAX_CHARS` (constant), lines 6406-6406, exports `SKILL_INLINE_ATTACHMENT_MAX_CHARS`
- order 576: `SKILL_RESOURCE_MANIFEST_MAX_ITEMS` (constant), lines 6407-6407, exports `SKILL_RESOURCE_MANIFEST_MAX_ITEMS`
- order 577: `SKILL_BODY_COMPACT_THRESHOLD_CHARS` (constant), lines 6408-6408, exports `SKILL_BODY_COMPACT_THRESHOLD_CHARS`
- order 578: `SKILL_BODY_PREVIEW_CHARS` (constant), lines 6409-6409, exports `SKILL_BODY_PREVIEW_CHARS`
- order 579: `SKILLS_VIRTUAL_PREFIX` (constant), lines 6410-6410, exports `SKILLS_VIRTUAL_PREFIX`
- order 580: `SKILLS_EXTERNAL_MOUNT` (constant), lines 6411-6411, exports `SKILLS_EXTERNAL_MOUNT`
- order 581: `PLAN_MODE_ENABLED_LEVELS` (constant), lines 6412-6412, exports `PLAN_MODE_ENABLED_LEVELS`
- order 582: `PLAN_MODE_FORCED_LEVELS` (constant), lines 6413-6413, exports `PLAN_MODE_FORCED_LEVELS`
- order 583: `PLAN_MODE_USER_CHOICES` (constant), lines 6414-6414, exports `PLAN_MODE_USER_CHOICES`
- order 584: `TASK_PHASES` (constant), lines 6415-6416, exports `TASK_PHASES`
- order 585: `TASK_PHASE_ROUTING` (constant), lines 6417-6424, exports `TASK_PHASE_ROUTING`
- order 586: `COMPLEXITY_KEYWORDS` (constant), lines 6425-6431, exports `COMPLEXITY_KEYWORDS`
- order 587: `USER_COMPLEXITY_SIMPLE_TOKENS` (constant), lines 6432-6436, exports `USER_COMPLEXITY_SIMPLE_TOKENS`
- order 588: `USER_COMPLEXITY_MODERATE_TOKENS` (constant), lines 6437-6441, exports `USER_COMPLEXITY_MODERATE_TOKENS`
- order 589: `USER_COMPLEXITY_COMPLEX_TOKENS` (constant), lines 6442-6446, exports `USER_COMPLEXITY_COMPLEX_TOKENS`
- order 590: `USER_COMPLEXITY_EXPERT_TOKENS` (constant), lines 6447-6451, exports `USER_COMPLEXITY_EXPERT_TOKENS`
- order 591: `PLAN_MODE_EXPLORER_MAX_ROUNDS` (constant), lines 6452-6455, exports `PLAN_MODE_EXPLORER_MAX_ROUNDS`
- order 592: `PLAN_MODE_EXPLORER_PRODUCTIVE_ROUNDS` (constant), lines 6456-6456, exports `PLAN_MODE_EXPLORER_PRODUCTIVE_ROUNDS`
- order 593: `PLAN_MODE_EXPLORER_STALE_ROUNDS` (constant), lines 6457-6457, exports `PLAN_MODE_EXPLORER_STALE_ROUNDS`
- order 594: `PLAN_MODE_SYNTHESIS_MAX_ATTEMPTS` (constant), lines 6458-6458, exports `PLAN_MODE_SYNTHESIS_MAX_ATTEMPTS`
- order 595: `REVIEWER_DEBUG_MODE_MAX_ROUNDS` (constant), lines 6459-6460, exports `REVIEWER_DEBUG_MODE_MAX_ROUNDS`
- order 596: `REVIEWER_DEBUG_TOOL_ALLOWLIST` (constant), lines 6461-6466, exports `REVIEWER_DEBUG_TOOL_ALLOWLIST`
- order 597: `EXPLORER_STALL_THRESHOLD` (constant), lines 6467-6467, exports `EXPLORER_STALL_THRESHOLD`
- order 598: `DEVELOPER_EDIT_STALL_THRESHOLD` (constant), lines 6468-6468, exports `DEVELOPER_EDIT_STALL_THRESHOLD`
- order 599: `ACCEPTANCE_GATE_STALL_THRESHOLD` (constant), lines 6469-6472, exports `ACCEPTANCE_GATE_STALL_THRESHOLD`
- order 600: `ACCEPTANCE_GATE_HARD_CEILING` (constant), lines 6473-6476, exports `ACCEPTANCE_GATE_HARD_CEILING`
- order 601: `ACCEPTANCE_GATE_TOTAL_ROUND_CEILING` (constant), lines 6477-6477, exports `ACCEPTANCE_GATE_TOTAL_ROUND_CEILING`
- order 602: `PLAN_MODE_MANAGER_SYNTHESIS_MAX_TOKENS` (constant), lines 6478-6478, exports `PLAN_MODE_MANAGER_SYNTHESIS_MAX_TOKENS`
- order 603: `PLAN_MODE_MAX_OPTIONS` (constant), lines 6479-6479, exports `PLAN_MODE_MAX_OPTIONS`
- order 604: `PLAN_FILE_RELATIVE_PATH` (constant), lines 6480-6480, exports `PLAN_FILE_RELATIVE_PATH`
- order 605: `PLAN_BUBBLE_MAX_CHARS` (constant), lines 6481-6481, exports `PLAN_BUBBLE_MAX_CHARS`
- order 606: `PLAN_NOTICE_BODY_MAX_CHARS` (constant), lines 6482-6482, exports `PLAN_NOTICE_BODY_MAX_CHARS`
- order 607: `PLAN_MESSAGE_EVENT_MAX_CHARS` (constant), lines 6483-6483, exports `PLAN_MESSAGE_EVENT_MAX_CHARS`
- order 608: `PLAN_STEP_FULL_CONTENT_MAX_CHARS` (constant), lines 6484-6484, exports `PLAN_STEP_FULL_CONTENT_MAX_CHARS`
- order 609: `PLAN_MODE_RESEARCH_TOOL_ALLOWLIST` (constant), lines 6485-6492, exports `PLAN_MODE_RESEARCH_TOOL_ALLOWLIST`
- order 610: `FAILURE_LEDGER_MAX_FIXES` (constant), lines 6493-6493, exports `FAILURE_LEDGER_MAX_FIXES`
- order 611: `FAILURE_LEDGER_MAX_COMPILE_ERRORS` (constant), lines 6494-6494, exports `FAILURE_LEDGER_MAX_COMPILE_ERRORS`
- order 612: `FAILURE_LEDGER_MAX_DELEGATIONS` (constant), lines 6495-6495, exports `FAILURE_LEDGER_MAX_DELEGATIONS`
- order 613: `FAILURE_LEDGER_MAX_STALLS` (constant), lines 6496-6496, exports `FAILURE_LEDGER_MAX_STALLS`
- order 614: `FAILURE_LEDGER_MAX_TOOL_FPS` (constant), lines 6497-6497, exports `FAILURE_LEDGER_MAX_TOOL_FPS`
- order 615: `FAILURE_LEDGER_MAX_ERRORS` (constant), lines 6498-6498, exports `FAILURE_LEDGER_MAX_ERRORS`
- order 616: `ERROR_CATEGORY_DEFS` (constant), lines 6499-6538, exports `ERROR_CATEGORY_DEFS`
- order 617: `CHECKPOINT_MAX_COUNT` (constant), lines 6539-6539, exports `CHECKPOINT_MAX_COUNT`
- order 618: `CHECKPOINT_INTERVAL_ROUNDS` (constant), lines 6540-6540, exports `CHECKPOINT_INTERVAL_ROUNDS`
- order 619: `PERSISTED_ROUTES_MAX` (constant), lines 6541-6541, exports `PERSISTED_ROUTES_MAX`
- order 620: `HTML_FRONTEND_REQUEST_KEYWORDS` (constant), lines 6542-6581, exports `HTML_FRONTEND_REQUEST_KEYWORDS`
- order 621: `DEEP_RESEARCH_REQUEST_KEYWORDS` (constant), lines 6582-6604, exports `DEEP_RESEARCH_REQUEST_KEYWORDS`
- order 622: `DEEP_RESEARCH_RETRIEVAL_KEYWORDS` (constant), lines 6605-6624, exports `DEEP_RESEARCH_RETRIEVAL_KEYWORDS`
- order 623: `DEEP_RESEARCH_TEXT_ONLY_HINT_KEYWORDS` (constant), lines 6625-6642, exports `DEEP_RESEARCH_TEXT_ONLY_HINT_KEYWORDS`
- order 624: `DANGEROUS_PATTERNS` (constant), lines 6643-6644, exports `DANGEROUS_PATTERNS`
- order 625: `VALID_MSG_TYPES` (constant), lines 6645-6651, exports `VALID_MSG_TYPES`
- order 626: `SUPPORTED_UI_LANGUAGES` (constant), lines 6652-6658, exports `SUPPORTED_UI_LANGUAGES`
- order 627: `UI_LANGUAGE_LABELS` (constant), lines 6659-6659, exports `UI_LANGUAGE_LABELS`
- order 628: `DEFAULT_UI_LANGUAGE` (constant), lines 6660-6660, exports `DEFAULT_UI_LANGUAGE`
- order 629: `PUBLIC_TOOL_PROGRESS_SUMMARY_ENABLED` (constant), lines 6661-6663, exports `PUBLIC_TOOL_PROGRESS_SUMMARY_ENABLED`
- order 630: `AGENT_LANGUAGE_PREFERENCES` (constant), lines 6664-6705, exports `AGENT_LANGUAGE_PREFERENCES`
- order 631: `UI_STYLE_CHOICES` (constant), lines 6706-6706, exports `UI_STYLE_CHOICES`
- order 632: `UI_STYLE_LABELS` (constant), lines 6707-6707, exports `UI_STYLE_LABELS`
- order 633: `DEFAULT_UI_STYLE` (constant), lines 6708-6708, exports `DEFAULT_UI_STYLE`
- order 634: `DEFAULT_WEB_UI_DIR` (constant), lines 6709-6709, exports `DEFAULT_WEB_UI_DIR`
- order 635: `DEFAULT_WEB_UI_CONFIG` (constant), lines 6710-6710, exports `DEFAULT_WEB_UI_CONFIG`
- order 636: `WEB_UI_REQUIRED_FILES` (constant), lines 6711-6718, exports `WEB_UI_REQUIRED_FILES`
- order 637: `WEB_UI_OPTIONAL_FILES` (constant), lines 6719-6719, exports `WEB_UI_OPTIONAL_FILES`
- order 638: `WEB_UI_APPLICATION_CONTRACT_VERSION` (constant), lines 6720-6720, exports `WEB_UI_APPLICATION_CONTRACT_VERSION`
- order 639: `WEB_UI_APPLICATION_FEATURE_MARKERS` (constant), lines 6721-6740, exports `WEB_UI_APPLICATION_FEATURE_MARKERS`
- order 640: `IMAGE_EXTS` (constant), lines 6741-6755, exports `IMAGE_EXTS`
- order 641: `IMAGE_FORMATS_NEED_CONVERSION` (constant), lines 6756-6756, exports `IMAGE_FORMATS_NEED_CONVERSION`
- order 642: `IMAGE_SAFE_FORMATS` (constant), lines 6757-6757, exports `IMAGE_SAFE_FORMATS`
- order 643: `AUDIO_EXTS` (constant), lines 6758-6768, exports `AUDIO_EXTS`
- order 644: `VIDEO_EXTS` (constant), lines 6769-6779, exports `VIDEO_EXTS`
- order 645: `CODE_PREVIEW_STAGE_MAX_BYTES` (constant), lines 6780-6780, exports `CODE_PREVIEW_STAGE_MAX_BYTES`
- order 646: `CODE_PREVIEW_STAGE_MAX_ROWS` (constant), lines 6781-6781, exports `CODE_PREVIEW_STAGE_MAX_ROWS`
- order 647: `CODE_PREVIEW_STAGE_MAX_PER_FILE` (constant), lines 6782-6782, exports `CODE_PREVIEW_STAGE_MAX_PER_FILE`
- order 648: `CODE_PREVIEW_STAGE_MAX_TOTAL` (constant), lines 6783-6783, exports `CODE_PREVIEW_STAGE_MAX_TOTAL`
- order 649: `CODE_PREVIEW_DIFF_CONTEXT_LINES` (constant), lines 6784-6784, exports `CODE_PREVIEW_DIFF_CONTEXT_LINES`
- order 650: `CODE_PREVIEW_DIFF_MERGE_GAP` (constant), lines 6785-6785, exports `CODE_PREVIEW_DIFF_MERGE_GAP`
- order 651: `PREVIEW_DOWNLOAD_MAX_FILES` (constant), lines 6786-6786, exports `PREVIEW_DOWNLOAD_MAX_FILES`
- order 652: `PREVIEW_DOWNLOAD_MAX_BYTES` (constant), lines 6787-6787, exports `PREVIEW_DOWNLOAD_MAX_BYTES`
- order 653: `FILES_TREE_DEFAULT_MAX_NODES` (constant), lines 6788-6788, exports `FILES_TREE_DEFAULT_MAX_NODES`
- order 654: `FILES_TREE_DEFAULT_MAX_DEPTH` (constant), lines 6789-6789, exports `FILES_TREE_DEFAULT_MAX_DEPTH`
- order 655: `FILES_TREE_SKIP_DIRS` (constant), lines 6790-6798, exports `FILES_TREE_SKIP_DIRS`
- order 656: `FILES_TREE_SKIP_REL_DIRS` (constant), lines 6799-6801, exports `FILES_TREE_SKIP_REL_DIRS`
- order 657: `IDE_FILE_MAX_BYTES` (constant), lines 6802-6802, exports `IDE_FILE_MAX_BYTES`
- order 658: `IDE_UPLOAD_MAX_BYTES` (constant), lines 6803-6803, exports `IDE_UPLOAD_MAX_BYTES`
- order 659: `IDE_UPLOAD_TOTAL_MAX_BYTES` (constant), lines 6804-6804, exports `IDE_UPLOAD_TOTAL_MAX_BYTES`
- order 660: `IDE_UPLOAD_MAX_ITEMS` (constant), lines 6805-6805, exports `IDE_UPLOAD_MAX_ITEMS`
- order 661: `IDE_UPLOAD_CHUNK_MAX_BYTES` (constant), lines 6806-6806, exports `IDE_UPLOAD_CHUNK_MAX_BYTES`
- order 662: `IDE_UPLOAD_STREAM_MAX_BYTES` (constant), lines 6807-6807, exports `IDE_UPLOAD_STREAM_MAX_BYTES`
- order 663: `IDE_TEXT_PREVIEW_MAX_BYTES` (constant), lines 6808-6808, exports `IDE_TEXT_PREVIEW_MAX_BYTES`
- order 664: `IDE_MARKDOWN_PREVIEW_MAX_LINES` (constant), lines 6809-6809, exports `IDE_MARKDOWN_PREVIEW_MAX_LINES`
- order 665: `IDE_IMAGE_PREVIEW_MAX_EDGE` (constant), lines 6810-6810, exports `IDE_IMAGE_PREVIEW_MAX_EDGE`
- order 666: `IDE_IMAGE_PREVIEW_MAX_PIXELS` (constant), lines 6811-6811, exports `IDE_IMAGE_PREVIEW_MAX_PIXELS`
- order 667: `IDE_IMAGE_PREVIEW_SOURCE_MAX_PIXELS` (constant), lines 6812-6812, exports `IDE_IMAGE_PREVIEW_SOURCE_MAX_PIXELS`
- order 668: `IDE_VECTOR_PREVIEW_MAX_BYTES` (constant), lines 6813-6813, exports `IDE_VECTOR_PREVIEW_MAX_BYTES`
- order 669: `IDE_TABLE_PREVIEW_SOURCE_MAX_BYTES` (constant), lines 6814-6814, exports `IDE_TABLE_PREVIEW_SOURCE_MAX_BYTES`
- order 670: `IDE_TABLE_PREVIEW_CELL_MAX_CHARS` (constant), lines 6815-6815, exports `IDE_TABLE_PREVIEW_CELL_MAX_CHARS`
- order 671: `IDE_TABLE_PREVIEW_TOTAL_CHARS` (constant), lines 6816-6816, exports `IDE_TABLE_PREVIEW_TOTAL_CHARS`
- order 672: `IDE_OFFICE_PREVIEW_MAX_ENTRIES` (constant), lines 6817-6817, exports `IDE_OFFICE_PREVIEW_MAX_ENTRIES`
- order 673: `IDE_OFFICE_PREVIEW_MAX_EXPANDED_BYTES` (constant), lines 6818-6818, exports `IDE_OFFICE_PREVIEW_MAX_EXPANDED_BYTES`
- order 674: `IDE_OFFICE_PREVIEW_MAX_ENTRY_BYTES` (constant), lines 6819-6819, exports `IDE_OFFICE_PREVIEW_MAX_ENTRY_BYTES`
- order 675: `IDE_COMMAND_TIMEOUT_DEFAULT` (constant), lines 6820-6820, exports `IDE_COMMAND_TIMEOUT_DEFAULT`
- order 676: `IDE_TREE_DEFAULT_MAX_NODES` (constant), lines 6821-6821, exports `IDE_TREE_DEFAULT_MAX_NODES`
- order 677: `IDE_TREE_MAX_NODES` (constant), lines 6822-6822, exports `IDE_TREE_MAX_NODES`
- order 678: `IDE_SEARCH_MAX_RESULTS` (constant), lines 6823-6823, exports `IDE_SEARCH_MAX_RESULTS`
- order 679: `IDE_SEARCH_MAX_FILE_BYTES` (constant), lines 6824-6824, exports `IDE_SEARCH_MAX_FILE_BYTES`
- order 680: `IDE_TERMINAL_SCROLLBACK_BYTES` (constant), lines 6825-6825, exports `IDE_TERMINAL_SCROLLBACK_BYTES`
- order 681: `IDE_TERMINAL_IDLE_SECONDS` (constant), lines 6826-6826, exports `IDE_TERMINAL_IDLE_SECONDS`
- order 682: `IDE_DEBUG_ADAPTER_START_ATTEMPTS` (constant), lines 6827-6827, exports `IDE_DEBUG_ADAPTER_START_ATTEMPTS`
- order 683: `IDE_DEBUG_ADAPTER_START_TIMEOUT_SECONDS` (constant), lines 6828-6828, exports `IDE_DEBUG_ADAPTER_START_TIMEOUT_SECONDS`
- order 684: `IDE_VSIX_MAX_BYTES` (constant), lines 6829-6829, exports `IDE_VSIX_MAX_BYTES`
- order 685: `IDE_VSIX_MAX_EXPANDED_BYTES` (constant), lines 6830-6830, exports `IDE_VSIX_MAX_EXPANDED_BYTES`
- order 686: `IDE_VSIX_MAX_FILES` (constant), lines 6831-6831, exports `IDE_VSIX_MAX_FILES`
- order 687: `IDE_VSIX_MAX_FILE_BYTES` (constant), lines 6832-6832, exports `IDE_VSIX_MAX_FILE_BYTES`
- order 688: `IDE_TREE_SKIP_DIRS` (constant), lines 6833-6841, exports `IDE_TREE_SKIP_DIRS`
- order 689: `RENDER_FRAME_MAX_B64_CHARS` (constant), lines 6842-6842, exports `RENDER_FRAME_MAX_B64_CHARS`
- order 690: `RENDER_FRAME_MAX_POINTS` (constant), lines 6843-6843, exports `RENDER_FRAME_MAX_POINTS`
- order 691: `RENDER_FRAME_MAX_LINES` (constant), lines 6844-6844, exports `RENDER_FRAME_MAX_LINES`
- order 692: `RENDER_FRAME_MAX_LINE_POINTS` (constant), lines 6845-6845, exports `RENDER_FRAME_MAX_LINE_POINTS`
- order 693: `RENDER_FRAME_ACTIVITY_INTERVAL_SECONDS` (constant), lines 6846-6846, exports `RENDER_FRAME_ACTIVITY_INTERVAL_SECONDS`
- order 694: `RAW_TOOLCALL_TEXT_FILTER_THRESHOLD` (constant), lines 6847-6847, exports `RAW_TOOLCALL_TEXT_FILTER_THRESHOLD`
- order 695: `ASSISTANT_TEXT_PERSIST_MAX_CHARS` (constant), lines 6848-6848, exports `ASSISTANT_TEXT_PERSIST_MAX_CHARS`
- order 696: `ASSISTANT_MESSAGE_EVENT_MAX_CHARS` (constant), lines 6849-6849, exports `ASSISTANT_MESSAGE_EVENT_MAX_CHARS`
- order 697: `CODE_PREVIEW_EXTS` (constant), lines 6850-6977, exports `CODE_PREVIEW_EXTS`
- order 698: `CODE_PREVIEW_FILENAMES` (constant), lines 6978-7029, exports `CODE_PREVIEW_FILENAMES`
- order 699: `MEDIA_CAPABILITY_KEYS` (constant), lines 7030-7037, exports `MEDIA_CAPABILITY_KEYS`
- order 703: `OFFLINE_JS_LIB_CATALOG` (constant), lines 7070-7396, exports `OFFLINE_JS_LIB_CATALOG`
- order 704: `OFFLINE_JS_ASSET_LOCK` (constant), lines 7397-7397, exports `OFFLINE_JS_ASSET_LOCK`
- order 705: `OFFLINE_JS_LIB_INDEX_FILE` (constant), lines 7398-7398, exports `OFFLINE_JS_LIB_INDEX_FILE`
- order 706: `OFFLINE_JS_LIB_README_FILE` (constant), lines 7399-7399, exports `OFFLINE_JS_LIB_README_FILE`
- order 717: `BACKEND_I18N` (constant), lines 7605-7676, exports `BACKEND_I18N`
- order 718: `_call_backend_i18n_en_update_7678` (expression), lines 7677-7778, exports —
- order 719: `_call_backend_i18n_zh_cn_update_7779` (expression), lines 7779-7879, exports —
- order 720: `_call_backend_i18n_zh_tw_update_7880` (expression), lines 7880-7980, exports —
- order 721: `_call_backend_i18n_ja_update_7981` (expression), lines 7981-8081, exports —
- order 944: `MODEL_RUNTIME_SETTING_KEYS` (constant), lines 14643-14648, exports `MODEL_RUNTIME_SETTING_KEYS`
- order 965: `LIQUID_KERNEL_STARTUP_POLICIES` (constant), lines 16349-16351, exports `LIQUID_KERNEL_STARTUP_POLICIES`
- order 966: `LIQUID_KERNEL_BOOTSTRAP_STATE_FILENAME` (constant), lines 16352-16352, exports `LIQUID_KERNEL_BOOTSTRAP_STATE_FILENAME`
- order 997: `TABULAR_PREVIEW_EXTS` (constant), lines 18302-18304, exports `TABULAR_PREVIEW_EXTS`
- order 998: `EXCEL_PREVIEW_EXTS` (constant), lines 18305-18305, exports `EXCEL_PREVIEW_EXTS`
- order 999: `PRESENTATION_PREVIEW_EXTS` (constant), lines 18306-18306, exports `PRESENTATION_PREVIEW_EXTS`
- order 1000: `DOCUMENT_PREVIEW_EXTS` (constant), lines 18307-18307, exports `DOCUMENT_PREVIEW_EXTS`
- order 1081: `SESSION_LLM_PRIORITY_RANKS` (constant), lines 27820-27824, exports `SESSION_LLM_PRIORITY_RANKS`
- order 1087: `TODO_REVISION_FALLBACK_MAX_ROWS` (constant), lines 27834-27836, exports `TODO_REVISION_FALLBACK_MAX_ROWS`
- order 1102: `BASH_OPERATION_CODES` (constant), lines 31130-31152, exports `BASH_OPERATION_CODES`
- order 1103: `BASH_OBSERVATION_OPERATION_CODES` (constant), lines 31153-31164, exports `BASH_OBSERVATION_OPERATION_CODES`
- order 1104: `BASH_OPERATION_ALIASES` (constant), lines 31165-31191, exports `BASH_OPERATION_ALIASES`
- order 1237: `STUDIO_DEVICE_COOKIE` (constant), lines 123110-123127, exports `STUDIO_DEVICE_COOKIE`
- order 1238: `STUDIO_SESSION_COOKIE` (constant), lines 123128-123128, exports `STUDIO_SESSION_COOKIE`
- order 1239: `STUDIO_DEVICE_TTL` (constant), lines 123129-123129, exports `STUDIO_DEVICE_TTL`
- order 1240: `STUDIO_SESSION_TTL` (constant), lines 123130-123130, exports `STUDIO_SESSION_TTL`
- order 1241: `STUDIO_MAX_FILE_BYTES` (constant), lines 123131-123131, exports `STUDIO_MAX_FILE_BYTES`
- order 1242: `STUDIO_MAX_PROJECT_BYTES` (constant), lines 123132-123132, exports `STUDIO_MAX_PROJECT_BYTES`
- order 1243: `STUDIO_MAX_FILES` (constant), lines 123133-123133, exports `STUDIO_MAX_FILES`
- order 1244: `STUDIO_MAX_JOB_SECONDS` (constant), lines 123134-123134, exports `STUDIO_MAX_JOB_SECONDS`
- order 1250: `STUDIO_INDEX_HTML` (constant), lines 125033-125035, exports `STUDIO_INDEX_HTML`
- order 1251: `STUDIO_CSS` (constant), lines 125036-125036, exports `STUDIO_CSS`
- order 1252: `STUDIO_JS` (constant), lines 125037-125037, exports `STUDIO_JS`

### `config/paths.py`

- order 128: `SCRIPT_DIR` (constant), lines 4914-4914, exports `SCRIPT_DIR`
- order 153: `_resolve_default_agent_workdir` (function), lines 5008-5017, exports `_resolve_default_agent_workdir`
- order 154: `_is_installed_python_runtime` (function), lines 5018-5021, exports `_is_installed_python_runtime`
- order 155: `_runtime_storage_mode` (function), lines 5022-5028, exports `_runtime_storage_mode`
- order 156: `_runtime_tree_has_content` (function), lines 5029-5034, exports `_runtime_tree_has_content`
- order 157: `_copy_runtime_tree_with_crypto_migration` (function), lines 5035-5105, exports `_copy_runtime_tree_with_crypto_migration`
- order 158: `_merge_legacy_codes_root` (function), lines 5106-5171, exports `_merge_legacy_codes_root`
- order 159: `_migrate_legacy_runtime_roots` (function), lines 5172-5262, exports `_migrate_legacy_runtime_roots`
- order 160: `WORKDIR` (constant), lines 5263-5264, exports `WORKDIR`
- order 161: `CODES_ROOT` (constant), lines 5265-5265, exports `CODES_ROOT`
- order 162: `LLM_CONFIG_PATH` (constant), lines 5266-5266, exports `LLM_CONFIG_PATH`
- order 801: `detect_repo_root` (function), lines 9572-9586, exports `detect_repo_root`
- order 802: `REPO_ROOT` (constant), lines 9587-9588, exports `REPO_ROOT`

### `config/settings.py`

- order 710: `normalize_ui_language` (function), lines 7481-7505, exports `normalize_ui_language`
- order 711: `normalize_ui_style` (function), lines 7506-7525, exports `normalize_ui_style`
- order 712: `supported_ui_languages_payload` (function), lines 7526-7529, exports `supported_ui_languages_payload`
- order 714: `agent_language_preference_payload` (function), lines 7542-7551, exports `agent_language_preference_payload`
- order 715: `normalize_execution_mode` (function), lines 7552-7573, exports `normalize_execution_mode`
- order 716: `model_language_instruction` (function), lines 7574-7604, exports `model_language_instruction`
- order 722: `backend_i18n_text` (function), lines 8082-8094, exports `backend_i18n_text`
- order 723: `backend_role_label` (function), lines 8095-8101, exports `backend_role_label`
- order 724: `_detect_os_shell_instruction` (function), lines 8102-8143, exports `_detect_os_shell_instruction`
- order 725: `resolve_web_ui_dir_path` (function), lines 8144-8152, exports `resolve_web_ui_dir_path`
- order 726: `resolve_optional_file_path` (function), lines 8153-8162, exports `resolve_optional_file_path`
- order 727: `resolve_skills_root_path` (function), lines 8163-8172, exports `resolve_skills_root_path`
- order 728: `_count_skill_markdown_files` (function), lines 8173-8186, exports `_count_skill_markdown_files`
- order 729: `select_preferred_skills_root` (function), lines 8187-8223, exports `select_preferred_skills_root`
- order 730: `load_web_ui_config_file` (function), lines 8224-8240, exports `load_web_ui_config_file`
- order 731: `extract_show_upload_list_setting` (function), lines 8241-8257, exports `extract_show_upload_list_setting`
- order 732: `extract_ui_style_setting` (function), lines 8258-8274, exports `extract_ui_style_setting`
- order 733: `extract_js_lib_download_setting` (function), lines 8275-8296, exports `extract_js_lib_download_setting`
- order 734: `extract_daily_session_limit_setting` (function), lines 8297-8342, exports `extract_daily_session_limit_setting`
- order 735: `extract_shell_command_timeout_setting` (function), lines 8343-8391, exports `extract_shell_command_timeout_setting`
- order 736: `normalize_shell_timeout_mode` (function), lines 8392-8409, exports `normalize_shell_timeout_mode`
- order 737: `extract_shell_timeout_mode_setting` (function), lines 8410-8422, exports `extract_shell_timeout_mode_setting`
- order 738: `extract_shell_async_handoff_setting` (function), lines 8423-8450, exports `extract_shell_async_handoff_setting`
- order 739: `extract_context_token_limit_setting` (function), lines 8451-8485, exports `extract_context_token_limit_setting`
- order 740: `normalize_auto_task_level_ceiling` (function), lines 8486-8507, exports `normalize_auto_task_level_ceiling`
- order 741: `normalize_l2_todo_policy` (function), lines 8508-8543, exports `normalize_l2_todo_policy`
- order 742: `extract_l2_todo_policy_setting` (function), lines 8544-8586, exports `extract_l2_todo_policy_setting`
- order 743: `extract_auto_task_level_ceiling_setting` (function), lines 8587-8616, exports `extract_auto_task_level_ceiling_setting`
- order 744: `normalize_session_llm_concurrency` (function), lines 8617-8638, exports `normalize_session_llm_concurrency`
- order 745: `extract_session_llm_concurrency_setting` (function), lines 8639-8660, exports `extract_session_llm_concurrency_setting`
- order 746: `normalize_read_context_policy` (function), lines 8661-8681, exports `normalize_read_context_policy`
- order 747: `normalize_tool_memory_policy` (function), lines 8682-8685, exports `normalize_tool_memory_policy`
- order 748: `extract_read_context_policy_setting` (function), lines 8686-8709, exports `extract_read_context_policy_setting`
- order 749: `extract_tool_memory_policy_setting` (function), lines 8710-8733, exports `extract_tool_memory_policy_setting`
- order 751: `default_multimodal_capabilities` (function), lines 8740-8750, exports `default_multimodal_capabilities`
- order 752: `_to_bool_like` (function), lines 8751-8763, exports `_to_bool_like`
- order 753: `extract_web_search_enabled_setting` (function), lines 8764-8776, exports `extract_web_search_enabled_setting`
- order 754: `_single_no_plan_todo_setting_sections` (function), lines 8777-8803, exports `_single_no_plan_todo_setting_sections`
- order 755: `_single_no_plan_todo_setting_present` (function), lines 8804-8829, exports `_single_no_plan_todo_setting_present`
- order 756: `extract_single_no_plan_todo_settings` (function), lines 8830-8876, exports `extract_single_no_plan_todo_settings`
- order 757: `normalize_user_memory_mode` (function), lines 8877-8907, exports `normalize_user_memory_mode`
- order 758: `user_memory_enabled_from_mode` (function), lines 8908-8911, exports `user_memory_enabled_from_mode`
- order 759: `extract_user_memory_mode_setting` (function), lines 8912-8951, exports `extract_user_memory_mode_setting`
- order 760: `set_web_search_enabled_on_runtime` (function), lines 8952-8967, exports `set_web_search_enabled_on_runtime`
- order 761: `infer_model_multimodal_capabilities` (function), lines 8968-9014, exports `infer_model_multimodal_capabilities`
- order 762: `parse_capability_overrides` (function), lines 9015-9054, exports `parse_capability_overrides`
- order 763: `merge_multimodal_capabilities` (function), lines 9055-9064, exports `merge_multimodal_capabilities`
- order 764: `parse_media_endpoints` (function), lines 9065-9081, exports `parse_media_endpoints`
- order 780: `extract_runtime_region_hint_setting` (function), lines 9259-9284, exports `extract_runtime_region_hint_setting`
- order 781: `extract_runtime_timezone_hint_setting` (function), lines 9285-9302, exports `extract_runtime_timezone_hint_setting`
- order 782: `runtime_environment_context_snapshot` (function), lines 9303-9352, exports `runtime_environment_context_snapshot`
- order 783: `runtime_environment_context_block` (function), lines 9353-9382, exports `runtime_environment_context_block`
- order 880: `extract_ollama_model_capabilities` (function), lines 13448-13470, exports `extract_ollama_model_capabilities`
- order 909: `infer_user_complexity_value` (function), lines 14042-14059, exports `infer_user_complexity_value`
- order 910: `normalize_task_complexity` (function), lines 14060-14089, exports `normalize_task_complexity`
- order 911: `task_complexity_rank` (function), lines 14090-14092, exports `task_complexity_rank`
- order 912: `task_complexity_at_least` (function), lines 14093-14095, exports `task_complexity_at_least`
- order 913: `max_task_complexity` (function), lines 14096-14106, exports `max_task_complexity`
- order 945: `merge_probed_models_into_profile` (function), lines 14649-14694, exports `merge_probed_models_into_profile`
- order 946: `probe_and_merge_model_profiles` (function), lines 14695-14752, exports `probe_and_merge_model_profiles`
- order 947: `normalize_model_runtime_settings` (function), lines 14753-14778, exports `normalize_model_runtime_settings`
- order 948: `apply_model_runtime_settings` (function), lines 14779-14794, exports `apply_model_runtime_settings`
- order 949: `model_runtime_settings_for` (function), lines 14795-14805, exports `model_runtime_settings_for`
- order 950: `apply_model_option_runtime_fields` (function), lines 14806-14818, exports `apply_model_option_runtime_fields`
- order 953: `load_llm_config_from_source` (function), lines 14851-14886, exports `load_llm_config_from_source`
- order 954: `parse_llm_config_profiles` (function), lines 14887-15752, exports `parse_llm_config_profiles`
- order 955: `looks_like_llm_config` (function), lines 15753-15842, exports `looks_like_llm_config`
- order 959: `parse_front_matter` (function), lines 16038-16266, exports `parse_front_matter`
- order 967: `normalize_liquid_kernel_startup_policy` (function), lines 16353-16357, exports `normalize_liquid_kernel_startup_policy`
- order 995: `normalize_upload_rel_path` (function), lines 18256-18290, exports `normalize_upload_rel_path`
- order 1105: `normalize_bash_operation` (function), lines 31192-31209, exports `normalize_bash_operation`

### `ide/assets.py`

- order 1229: `IDE_INDEX_HTML` (constant), lines 121952-122107, exports `IDE_INDEX_HTML`
- order 1230: `IDE_CSS` (constant), lines 122108-122149, exports `IDE_CSS`
- order 1231: `IDE_JS` (constant), lines 122150-122343, exports `IDE_JS`
- order 1232: `IDE_CSS` (constant), lines 122344-122365, exports `IDE_CSS`
- order 1233: `IDE_JS` (constant), lines 122366-122629, exports `IDE_JS`
- order 1234: `IDE_JS` (constant), lines 122630-122758, exports `IDE_JS`
- order 1235: `IDE_JS` (constant), lines 122759-122982, exports `IDE_JS`
- order 1236: `IDE_JS` (constant), lines 122983-123109, exports `IDE_JS`

### `ide/auth.py`

- order 973: `IDEAuthError` (class), lines 16694-16701, exports `IDEAuthError`
- order 974: `IDEAuthStore` (class), lines 16702-17425, exports `IDEAuthStore`

### `ide/errors.py`

- order 975: `IDECapabilityError` (class), lines 17426-17432, exports `IDECapabilityError`
- order 976: `IDEFileConflict` (class), lines 17433-17440, exports `IDEFileConflict`

### `ide/events.py`

- order 836: `ide_public_operation_data` (function), lines 10471-10522, exports `ide_public_operation_data`

### `ide/handler.py`

- order 1269: `IdeHandler` (class), lines 141191-142847, exports `IdeHandler`

### `ide/preview.py`

- order 994: `normalize_rel_preview_path` (function), lines 18242-18255, exports `normalize_rel_preview_path`
- order 996: `is_code_preview_candidate` (function), lines 18291-18301, exports `is_code_preview_candidate`
- order 1001: `preview_kind_for_path` (function), lines 18308-18337, exports `preview_kind_for_path`
- order 1002: `normalize_markdown_preview_text` (function), lines 18338-18371, exports `normalize_markdown_preview_text`
- order 1003: `_preview_markdown_value_html` (function), lines 18372-18392, exports `_preview_markdown_value_html`
- order 1004: `_preview_markdown_frontmatter_html` (function), lines 18393-18408, exports `_preview_markdown_frontmatter_html`
- order 1005: `_preview_markdown_task_lists` (function), lines 18409-18422, exports `_preview_markdown_task_lists`
- order 1006: `_preview_markdown_fallback_inline` (function), lines 18423-18464, exports `_preview_markdown_fallback_inline`
- order 1007: `_preview_markdown_fallback_html` (function), lines 18465-18561, exports `_preview_markdown_fallback_html`
- order 1010: `workspace_file_revision_map` (function), lines 18602-18626, exports `workspace_file_revision_map`
- order 1011: `workspace_revision_delta` (function), lines 18627-18633, exports `workspace_revision_delta`
- order 1012: `build_code_preview_rows` (function), lines 18634-18682, exports `build_code_preview_rows`

### `ide/sandbox.py`

- order 788: `_windows_subprocess_encodings` (function), lines 9410-9427, exports `_windows_subprocess_encodings`
- order 1120: `_IDE_SANDBOX_BACKEND_CACHE` (assignment), lines 31975-31983, exports `_IDE_SANDBOX_BACKEND_CACHE`
- order 1121: `_IDE_SANDBOX_BACKEND_LOCK` (assignment), lines 31984-31984, exports `_IDE_SANDBOX_BACKEND_LOCK`
- order 1122: `WINDOWS_JOB_SANDBOX_MARKER` (constant), lines 31985-31985, exports `WINDOWS_JOB_SANDBOX_MARKER`
- order 1123: `_WINDOWS_LOW_INTEGRITY_ROOTS` (assignment), lines 31986-31986, exports `_WINDOWS_LOW_INTEGRITY_ROOTS`
- order 1124: `_WINDOWS_LOW_INTEGRITY_FAILED_ROOTS` (assignment), lines 31987-31987, exports `_WINDOWS_LOW_INTEGRITY_FAILED_ROOTS`
- order 1125: `_WINDOWS_LOW_INTEGRITY_LOCK` (assignment), lines 31988-31988, exports `_WINDOWS_LOW_INTEGRITY_LOCK`
- order 1126: `_is_windows_job_sandbox_prefix` (function), lines 31989-31995, exports `_is_windows_job_sandbox_prefix`
- order 1127: `_windows_builtin_sandbox_probe` (function), lines 31996-32019, exports `_windows_builtin_sandbox_probe`
- order 1128: `_windows_last_error` (function), lines 32020-32027, exports `_windows_last_error`
- order 1129: `_windows_set_integrity_label` (function), lines 32028-32081, exports `_windows_set_integrity_label`
- order 1130: `_windows_set_low_integrity_label` (function), lines 32082-32084, exports `_windows_set_low_integrity_label`
- order 1131: `_windows_protect_application_snapshot` (function), lines 32085-32108, exports `_windows_protect_application_snapshot`
- order 1132: `_windows_prepare_low_integrity_workspace` (function), lines 32109-32146, exports `_windows_prepare_low_integrity_workspace`
- order 1133: `_windows_job_memory_limit` (function), lines 32147-32154, exports `_windows_job_memory_limit`
- order 1134: `_windows_lower_process_integrity` (function), lines 32155-32202, exports `_windows_lower_process_integrity`
- order 1135: `_windows_attach_sandbox_job` (function), lines 32203-32295, exports `_windows_attach_sandbox_job`
- order 1136: `_windows_close_sandbox_job` (function), lines 32296-32312, exports `_windows_close_sandbox_job`
- order 1137: `_popen_windows_sandboxed` (function), lines 32313-32344, exports `_popen_windows_sandboxed`
- order 1138: `_run_windows_sandboxed_command` (function), lines 32345-32398, exports `_run_windows_sandboxed_command`
- order 1139: `_detect_ide_sandbox_backend` (function), lines 32399-32506, exports `_detect_ide_sandbox_backend`

### `ide/toolchains.py`

- order 549: `IDE_TOOLCHAIN_CACHE_TTL_SECONDS` (constant), lines 6307-6313, exports `IDE_TOOLCHAIN_CACHE_TTL_SECONDS`
- order 550: `_IDE_TOOLCHAIN_CACHE_LOCK` (assignment), lines 6314-6314, exports `_IDE_TOOLCHAIN_CACHE_LOCK`
- order 551: `_IDE_TOOLCHAIN_CACHE` (assignment), lines 6315-6315, exports `_IDE_TOOLCHAIN_CACHE`
- order 552: `_IDE_TOOLCHAIN_REFRESHING` (assignment), lines 6316-6316, exports `_IDE_TOOLCHAIN_REFRESHING`
- order 1256: `_ide_toolchain_cache_key` (function), lines 125042-125052, exports `_ide_toolchain_cache_key`
- order 1257: `_probe_ide_toolchains` (function), lines 125053-125096, exports `_probe_ide_toolchains`
- order 1258: `_refresh_ide_toolchains_in_background` (function), lines 125097-125106, exports `_refresh_ide_toolchains_in_background`

### `llm/client.py`

- order 1080: `OllamaError` (class), lines 27778-27819, exports `OllamaError`
- order 1100: `OllamaClient` (class), lines 28256-31115, exports `OllamaClient`

### `llm/constants.py`

- order 126: `DEFAULT_OLLAMA_BASE_URL` (constant), lines 4912-4912, exports `DEFAULT_OLLAMA_BASE_URL`
- order 127: `DEFAULT_OLLAMA_MODEL` (constant), lines 4913-4913, exports `DEFAULT_OLLAMA_MODEL`
- order 915: `OPENAI_COMPAT_PROVIDER_NAMES` (constant), lines 14124-14133, exports `OPENAI_COMPAT_PROVIDER_NAMES`
- order 916: `OPENAI_LIKE_PROVIDER_NAMES` (constant), lines 14134-14135, exports `OPENAI_LIKE_PROVIDER_NAMES`
- order 919: `EFFORT_OFF` (constant), lines 14142-14153, exports `EFFORT_OFF`
- order 920: `EFFORT_LOW` (constant), lines 14154-14154, exports `EFFORT_LOW`
- order 921: `EFFORT_MEDIUM` (constant), lines 14155-14155, exports `EFFORT_MEDIUM`
- order 922: `EFFORT_HIGH` (constant), lines 14156-14156, exports `EFFORT_HIGH`
- order 923: `EFFORT_MAX` (constant), lines 14157-14157, exports `EFFORT_MAX`
- order 924: `EFFORT_LEVELS` (constant), lines 14158-14158, exports `EFFORT_LEVELS`
- order 925: `EFFORT_ORDER` (constant), lines 14159-14159, exports `EFFORT_ORDER`
- order 926: `EFFORT_DEFAULT` (constant), lines 14160-14160, exports `EFFORT_DEFAULT`
- order 927: `EFFORT_ANTHROPIC_BUDGET` (constant), lines 14161-14168, exports `EFFORT_ANTHROPIC_BUDGET`
- order 928: `EFFORT_OPENAI_REASONING` (constant), lines 14169-14175, exports `EFFORT_OPENAI_REASONING`
- order 929: `TASK_LEVEL_EFFORT` (constant), lines 14176-14185, exports `TASK_LEVEL_EFFORT`
- order 930: `ROLE_EFFORT_FLOOR` (constant), lines 14186-14191, exports `ROLE_EFFORT_FLOOR`
- order 931: `COORDINATION_EFFORT` (constant), lines 14192-14195, exports `COORDINATION_EFFORT`

### `llm/gate.py`

- order 399: `SESSION_LLM_CONCURRENCY_MIN` (constant), lines 5790-5794, exports `SESSION_LLM_CONCURRENCY_MIN`
- order 400: `SESSION_LLM_CONCURRENCY_MAX` (constant), lines 5795-5795, exports `SESSION_LLM_CONCURRENCY_MAX`
- order 401: `SESSION_LLM_CONCURRENCY_FACTORY_DEFAULT` (constant), lines 5796-5796, exports `SESSION_LLM_CONCURRENCY_FACTORY_DEFAULT`
- order 402: `_session_llm_concurrency_env_default` (function), lines 5797-5805, exports `_session_llm_concurrency_env_default`
- order 403: `DEFAULT_SESSION_LLM_CONCURRENCY` (constant), lines 5806-5808, exports `DEFAULT_SESSION_LLM_CONCURRENCY`
- order 1082: `SESSION_LLM_GATE_POLL_SECONDS` (constant), lines 27825-27825, exports `SESSION_LLM_GATE_POLL_SECONDS`
- order 1083: `SESSION_LLM_GATE_SNAPSHOT_MAX_REQUESTS` (constant), lines 27826-27826, exports `SESSION_LLM_GATE_SNAPSHOT_MAX_REQUESTS`
- order 1084: `SESSION_LLM_CONCURRENCY_PUSH_INTERVAL_SECONDS` (constant), lines 27827-27829, exports `SESSION_LLM_CONCURRENCY_PUSH_INTERVAL_SECONDS`
- order 1085: `TODO_LLM_CALL_BUDGET` (constant), lines 27830-27832, exports `TODO_LLM_CALL_BUDGET`
- order 1086: `TODO_LLM_TIMEOUT_FACTORY_DEFAULT` (constant), lines 27833-27833, exports `TODO_LLM_TIMEOUT_FACTORY_DEFAULT`
- order 1088: `_todo_llm_timeout_env_default` (function), lines 27837-27847, exports `_todo_llm_timeout_env_default`
- order 1089: `TODO_LLM_TIMEOUT_SECONDS` (constant), lines 27848-27853, exports `TODO_LLM_TIMEOUT_SECONDS`
- order 1090: `LLMGateBusy` (class), lines 27854-27863, exports `LLMGateBusy`
- order 1091: `TodoLLMBudgetExhausted` (class), lines 27864-27867, exports `TodoLLMBudgetExhausted`
- order 1092: `_TODO_LLM_BUDGET_LOCAL` (assignment), lines 27868-27870, exports `_TODO_LLM_BUDGET_LOCAL`
- order 1093: `todo_llm_budget_scope` (function), lines 27871-27896, exports `todo_llm_budget_scope`
- order 1094: `_consume_todo_llm_budget` (function), lines 27897-27908, exports `_consume_todo_llm_budget`
- order 1095: `todo_llm_budget_active` (function), lines 27909-27913, exports `todo_llm_budget_active`
- order 1096: `todo_llm_skip_reason` (function), lines 27914-27941, exports `todo_llm_skip_reason`
- order 1097: `SessionLLMGate` (class), lines 27942-28242, exports `SessionLLMGate`
- order 1098: `_SESSION_LLM_GATE_INIT_LOCK` (assignment), lines 28243-28245, exports `_SESSION_LLM_GATE_INIT_LOCK`
- order 1099: `set_session_llm_concurrency_on_runtime` (function), lines 28246-28255, exports `set_session_llm_concurrency_on_runtime`

### `llm/utils.py`

- order 879: `probe_ollama_environment` (function), lines 13433-13447, exports `probe_ollama_environment`
- order 881: `probe_ollama_model_records` (function), lines 13471-13504, exports `probe_ollama_model_records`
- order 882: `list_ollama_models` (function), lines 13505-13509, exports `list_ollama_models`
- order 883: `_OLLAMA_TAG_CACHE_LOCK` (assignment), lines 13510-13511, exports `_OLLAMA_TAG_CACHE_LOCK`
- order 884: `_OLLAMA_TAG_CACHE` (assignment), lines 13512-13512, exports `_OLLAMA_TAG_CACHE`
- order 887: `_fetch_ollama_models_cached` (function), lines 13521-13546, exports `_fetch_ollama_models_cached`
- order 888: `list_ollama_models_cached` (function), lines 13547-13592, exports `list_ollama_models_cached`
- order 889: `resolve_ollama_model` (function), lines 13593-13604, exports `resolve_ollama_model`
- order 890: `infer_thinking_model` (function), lines 13605-13608, exports `infer_thinking_model`
- order 891: `split_thinking_content` (function), lines 13609-13653, exports `split_thinking_content`
- order 892: `strip_thinking_content` (function), lines 13654-13656, exports `strip_thinking_content`
- order 893: `check_ollama_model_ready` (function), lines 13657-13682, exports `check_ollama_model_ready`
- order 894: `list_loaded_ollama_models` (function), lines 13683-13697, exports `list_loaded_ollama_models`
- order 895: `wake_ollama_model` (function), lines 13698-13729, exports `wake_ollama_model`
- order 896: `try_pull_ollama_model` (function), lines 13730-13748, exports `try_pull_ollama_model`
- order 897: `ordered_model_candidates` (function), lines 13749-13768, exports `ordered_model_candidates`
- order 898: `pick_working_ollama_model` (function), lines 13769-13786, exports `pick_working_ollama_model`
- order 905: `evolution_worker_chat_messages` (function), lines 13944-13995, exports `evolution_worker_chat_messages`
- order 907: `extract_base_url` (function), lines 14021-14030, exports `extract_base_url`
- order 908: `complete_chat_endpoint` (function), lines 14031-14041, exports `complete_chat_endpoint`
- order 914: `normalize_openai_compat_provider_name` (function), lines 14107-14123, exports `normalize_openai_compat_provider_name`
- order 917: `is_openai_compat_provider` (function), lines 14136-14138, exports `is_openai_compat_provider`
- order 918: `is_openai_like_provider` (function), lines 14139-14141, exports `is_openai_like_provider`
- order 932: `clamp_effort` (function), lines 14196-14207, exports `clamp_effort`
- order 933: `model_reasoning_style` (function), lines 14208-14250, exports `model_reasoning_style`
- order 934: `resolve_reasoning_payload` (function), lines 14251-14313, exports `resolve_reasoning_payload`
- order 935: `openai_compat_probe_headers` (function), lines 14314-14332, exports `openai_compat_probe_headers`
- order 936: `openai_compat_model_list_urls` (function), lines 14333-14366, exports `openai_compat_model_list_urls`
- order 937: `anthropic_model_list_url` (function), lines 14367-14381, exports `anthropic_model_list_url`
- order 938: `extract_openai_compat_model_ids` (function), lines 14382-14416, exports `extract_openai_compat_model_ids`
- order 939: `extract_openai_compat_model_records` (function), lines 14417-14496, exports `extract_openai_compat_model_records`
- order 940: `_PROVIDER_MODEL_CACHE_LOCK` (assignment), lines 14497-14499, exports `_PROVIDER_MODEL_CACHE_LOCK`
- order 941: `_PROVIDER_MODEL_CACHE` (assignment), lines 14500-14500, exports `_PROVIDER_MODEL_CACHE`
- order 942: `_fetch_provider_models_cached` (function), lines 14501-14574, exports `_fetch_provider_models_cached`
- order 943: `probe_provider_models` (function), lines 14575-14642, exports `probe_provider_models`
- order 951: `_is_http_url` (function), lines 14819-14832, exports `_is_http_url`
- order 952: `_resolve_local_path` (function), lines 14833-14850, exports `_resolve_local_path`

### `mcp/constants.py`

- order 180: `MCP_SERVICE_PORT_OFFSET` (constant), lines 5284-5284, exports `MCP_SERVICE_PORT_OFFSET`
- order 1060: `MCP_PROTOCOL_VERSION` (constant), lines 26396-26425, exports `MCP_PROTOCOL_VERSION`
- order 1061: `MCP_NAME_RE` (constant), lines 26426-26426, exports `MCP_NAME_RE`
- order 1062: `MCP_TOOL_PREFIX` (constant), lines 26427-26427, exports `MCP_TOOL_PREFIX`
- order 1063: `_MCP_DEFAULT_HANDSHAKE_TIMEOUT` (assignment), lines 26428-26428, exports `_MCP_DEFAULT_HANDSHAKE_TIMEOUT`
- order 1064: `_MCP_DEFAULT_CALL_TIMEOUT` (assignment), lines 26429-26429, exports `_MCP_DEFAULT_CALL_TIMEOUT`
- order 1065: `_MCP_MAX_RESULT_CHARS` (assignment), lines 26430-26430, exports `_MCP_MAX_RESULT_CHARS`
- order 1066: `_MCP_TRUST_STORE_VERSION` (assignment), lines 26431-26431, exports `_MCP_TRUST_STORE_VERSION`

### `mcp/driver.py`

- order 1067: `mcp_normalize_name` (function), lines 26432-26441, exports `mcp_normalize_name`
- order 1068: `mcp_normalize_server_configs` (function), lines 26442-26526, exports `mcp_normalize_server_configs`
- order 1069: `mcp_extract_server_configs` (function), lines 26527-26546, exports `mcp_extract_server_configs`
- order 1070: `_mcp_sha256_file` (function), lines 26547-26557, exports `_mcp_sha256_file`
- order 1071: `_mcp_file_identity` (function), lines 26558-26575, exports `_mcp_file_identity`
- order 1072: `mcp_workspace_identity` (function), lines 26576-26594, exports `mcp_workspace_identity`
- order 1073: `mcp_config_file_digest` (function), lines 26595-26602, exports `mcp_config_file_digest`
- order 1074: `mcp_default_trust_store_path` (function), lines 26603-26637, exports `mcp_default_trust_store_path`
- order 1075: `mcp_record_definition_fingerprint` (function), lines 26638-26652, exports `mcp_record_definition_fingerprint`
- order 1076: `_mcp_effective_spawn` (function), lines 26653-26740, exports `_mcp_effective_spawn`
- order 1077: `MCPWorkspaceTrustStore` (class), lines 26741-26802, exports `MCPWorkspaceTrustStore`
- order 1078: `MCPServerProcess` (class), lines 26803-27158, exports `MCPServerProcess`
- order 1079: `MCPManager` (class), lines 27159-27777, exports `MCPManager`

### `mcp/service.py`

- order 1271: `McpServiceHandler` (class), lines 143319-143536, exports `McpServiceHandler`

### `rag/assets.py`

- order 1223: `RAG_ADMIN_INDEX_HTML` (constant), lines 119328-119560, exports `RAG_ADMIN_INDEX_HTML`
- order 1224: `RAG_ADMIN_CSS` (constant), lines 119561-119664, exports `RAG_ADMIN_CSS`
- order 1225: `RAG_ADMIN_JS` (constant), lines 119665-121902, exports `RAG_ADMIN_JS`
- order 1226: `CODE_ADMIN_INDEX_HTML` (constant), lines 121903-121915, exports `CODE_ADMIN_INDEX_HTML`
- order 1227: `CODE_ADMIN_CSS` (constant), lines 121916-121946, exports `CODE_ADMIN_CSS`
- order 1228: `CODE_ADMIN_JS` (constant), lines 121947-121951, exports `CODE_ADMIN_JS`

### `rag/constants.py`

- order 176: `RAG_LIBRARY_DIRNAME` (constant), lines 5280-5280, exports `RAG_LIBRARY_DIRNAME`
- order 177: `RAG_ADMIN_PORT_OFFSET` (constant), lines 5281-5281, exports `RAG_ADMIN_PORT_OFFSET`
- order 178: `CODE_LIBRARY_DIRNAME` (constant), lines 5282-5282, exports `CODE_LIBRARY_DIRNAME`
- order 184: `WEB_SEARCH_INDEX_DIRNAME` (constant), lines 5291-5291, exports `WEB_SEARCH_INDEX_DIRNAME`
- order 186: `USER_MEMORY_DIRNAME` (constant), lines 5293-5293, exports `USER_MEMORY_DIRNAME`
- order 187: `USER_MEMORY_DB_FILENAME` (constant), lines 5294-5294, exports `USER_MEMORY_DB_FILENAME`
- order 188: `USER_MEMORY_PROFILE_FILENAME` (constant), lines 5295-5295, exports `USER_MEMORY_PROFILE_FILENAME`
- order 189: `USER_MEMORY_MODE_CHOICES` (constant), lines 5296-5296, exports `USER_MEMORY_MODE_CHOICES`
- order 191: `USER_MEMORY_WEAK_CAPSULE_CHARS` (constant), lines 5298-5298, exports `USER_MEMORY_WEAK_CAPSULE_CHARS`
- order 192: `USER_MEMORY_ON_CAPSULE_CHARS` (constant), lines 5299-5299, exports `USER_MEMORY_ON_CAPSULE_CHARS`
- order 193: `USER_MEMORY_CAPSULE_INJECT_CHARS` (constant), lines 5300-5303, exports `USER_MEMORY_CAPSULE_INJECT_CHARS`
- order 194: `USER_MEMORY_MAX_SUMMARY_CHARS` (constant), lines 5304-5304, exports `USER_MEMORY_MAX_SUMMARY_CHARS`
- order 195: `USER_MEMORY_QUERY_LIMIT` (constant), lines 5305-5305, exports `USER_MEMORY_QUERY_LIMIT`
- order 196: `USER_MEMORY_DECAY_HALFLIFE_DAYS` (constant), lines 5306-5306, exports `USER_MEMORY_DECAY_HALFLIFE_DAYS`
- order 197: `USER_MEMORY_PROFILE_SCHEMA_VERSION` (constant), lines 5307-5307, exports `USER_MEMORY_PROFILE_SCHEMA_VERSION`
- order 217: `WEB_SEARCH_CONTEXT_REGISTRY_MAX` (constant), lines 5329-5329, exports `WEB_SEARCH_CONTEXT_REGISTRY_MAX`
- order 218: `WEB_SEARCH_CONTEXT_PROMPT_MAX_ITEMS` (constant), lines 5330-5330, exports `WEB_SEARCH_CONTEXT_PROMPT_MAX_ITEMS`
- order 219: `WEB_SEARCH_CONTEXT_PROMPT_MAX_CHARS` (constant), lines 5331-5331, exports `WEB_SEARCH_CONTEXT_PROMPT_MAX_CHARS`
- order 220: `WEB_SEARCH_CONTEXT_NODE_MAX` (constant), lines 5332-5332, exports `WEB_SEARCH_CONTEXT_NODE_MAX`
- order 221: `WEB_SEARCH_CONTEXT_URL_MAX` (constant), lines 5333-5333, exports `WEB_SEARCH_CONTEXT_URL_MAX`
- order 222: `RAG_CHUNK_CHARS` (constant), lines 5334-5334, exports `RAG_CHUNK_CHARS`
- order 223: `RAG_CHUNK_OVERLAP` (constant), lines 5335-5335, exports `RAG_CHUNK_OVERLAP`
- order 224: `RAG_MAX_CHUNKS_PER_DOC` (constant), lines 5336-5338, exports `RAG_MAX_CHUNKS_PER_DOC`
- order 225: `RAG_MAX_DOCUMENT_CHARS` (constant), lines 5339-5349, exports `RAG_MAX_DOCUMENT_CHARS`
- order 230: `RAG_MAX_QUERY_RESULTS` (constant), lines 5363-5363, exports `RAG_MAX_QUERY_RESULTS`
- order 231: `RAG_HIGH_RECALL_POOL_MULTIPLIER` (constant), lines 5364-5364, exports `RAG_HIGH_RECALL_POOL_MULTIPLIER`
- order 232: `RAG_HIGH_RECALL_MIN_POOL` (constant), lines 5365-5365, exports `RAG_HIGH_RECALL_MIN_POOL`
- order 233: `RAG_RETRIEVAL_MAX_PER_DOC` (constant), lines 5366-5366, exports `RAG_RETRIEVAL_MAX_PER_DOC`
- order 234: `RAG_BM25_K1` (constant), lines 5367-5370, exports `RAG_BM25_K1`
- order 235: `RAG_BM25_B` (constant), lines 5371-5371, exports `RAG_BM25_B`
- order 236: `RAG_BM25_SATURATION` (constant), lines 5372-5378, exports `RAG_BM25_SATURATION`
- order 237: `RAG_SYMBOL_EXACT_BOOST` (constant), lines 5379-5382, exports `RAG_SYMBOL_EXACT_BOOST`
- order 238: `RAG_INDEX_SNAPSHOT_FORMAT` (constant), lines 5383-5386, exports `RAG_INDEX_SNAPSHOT_FORMAT`
- order 239: `RAG_GRAPH_MAX_NODES` (constant), lines 5387-5387, exports `RAG_GRAPH_MAX_NODES`
- order 240: `RAG_TASK_HISTORY_LIMIT` (constant), lines 5388-5388, exports `RAG_TASK_HISTORY_LIMIT`
- order 241: `RAG_MODEL_MEDIA_MAX_BYTES` (constant), lines 5389-5389, exports `RAG_MODEL_MEDIA_MAX_BYTES`
- order 242: `RAG_MAX_IMPORT_FILES` (constant), lines 5390-5390, exports `RAG_MAX_IMPORT_FILES`
- order 243: `RAG_MAX_IMPORT_BATCH_ITEMS` (constant), lines 5391-5391, exports `RAG_MAX_IMPORT_BATCH_ITEMS`
- order 244: `RAG_MAX_IMPORT_BATCH_BYTES` (constant), lines 5392-5392, exports `RAG_MAX_IMPORT_BATCH_BYTES`
- order 245: `RAG_PDF_IMAGE_LIMIT` (constant), lines 5393-5393, exports `RAG_PDF_IMAGE_LIMIT`
- order 246: `RAG_QUERY_CONTEXT_CHARS` (constant), lines 5394-5394, exports `RAG_QUERY_CONTEXT_CHARS`
- order 247: `RAG_MAX_GLOBAL_COMMUNITIES` (constant), lines 5395-5395, exports `RAG_MAX_GLOBAL_COMMUNITIES`
- order 248: `RAG_MAX_COMMUNITY_MAP_SUPPORT` (constant), lines 5396-5396, exports `RAG_MAX_COMMUNITY_MAP_SUPPORT`
- order 249: `RAG_INCLUDE_FILENAME_ENTITIES_DEFAULT` (constant), lines 5397-5397, exports `RAG_INCLUDE_FILENAME_ENTITIES_DEFAULT`
- order 250: `RAG_DYNAMIC_NOISE_MIN_DOC_FREQ` (constant), lines 5398-5398, exports `RAG_DYNAMIC_NOISE_MIN_DOC_FREQ`
- order 251: `RAG_DYNAMIC_NOISE_MIN_COMMUNITY_FREQ` (constant), lines 5399-5399, exports `RAG_DYNAMIC_NOISE_MIN_COMMUNITY_FREQ`
- order 252: `RAG_DYNAMIC_NOISE_SOFT_DOC_RATIO` (constant), lines 5400-5400, exports `RAG_DYNAMIC_NOISE_SOFT_DOC_RATIO`
- order 253: `RAG_DYNAMIC_NOISE_HARD_DOC_RATIO` (constant), lines 5401-5401, exports `RAG_DYNAMIC_NOISE_HARD_DOC_RATIO`
- order 254: `RAG_DYNAMIC_NOISE_SOFT_COMMUNITY_RATIO` (constant), lines 5402-5402, exports `RAG_DYNAMIC_NOISE_SOFT_COMMUNITY_RATIO`
- order 255: `RAG_DYNAMIC_NOISE_HARD_COMMUNITY_RATIO` (constant), lines 5403-5403, exports `RAG_DYNAMIC_NOISE_HARD_COMMUNITY_RATIO`
- order 256: `RAG_MIN_SYNTHESIS_SCORE` (constant), lines 5404-5404, exports `RAG_MIN_SYNTHESIS_SCORE`
- order 257: `RAG_NO_EVIDENCE_THRESHOLD` (constant), lines 5405-5405, exports `RAG_NO_EVIDENCE_THRESHOLD`
- order 258: `RAG_WEAK_MATCH_SCORE_CAP` (constant), lines 5406-5406, exports `RAG_WEAK_MATCH_SCORE_CAP`
- order 259: `RAG_SYNTHESIS_MAX_PER_DOC` (constant), lines 5407-5407, exports `RAG_SYNTHESIS_MAX_PER_DOC`
- order 260: `RAG_WORKFLOW_ACCEPT_SCORE` (constant), lines 5408-5408, exports `RAG_WORKFLOW_ACCEPT_SCORE`
- order 261: `RAG_NO_EVIDENCE_MESSAGE` (constant), lines 5409-5409, exports `RAG_NO_EVIDENCE_MESSAGE`
- order 262: `RAG_CONTEXT_BUDGETS` (constant), lines 5410-5414, exports `RAG_CONTEXT_BUDGETS`
- order 263: `RAG_WEAK_EVIDENCE_MESSAGE` (constant), lines 5415-5415, exports `RAG_WEAK_EVIDENCE_MESSAGE`
- order 264: `RAG_EVIDENCE_SCHEMA_VERSION` (constant), lines 5416-5416, exports `RAG_EVIDENCE_SCHEMA_VERSION`
- order 265: `RAG_EVIDENCE_BATCH_CHARS` (constant), lines 5417-5420, exports `RAG_EVIDENCE_BATCH_CHARS`
- order 266: `RAG_EVALUATION_SUMMARY_CHARS` (constant), lines 5421-5424, exports `RAG_EVALUATION_SUMMARY_CHARS`
- order 267: `RAG_DENSE_DEFAULT_ENABLED` (constant), lines 5425-5425, exports `RAG_DENSE_DEFAULT_ENABLED`
- order 268: `RAG_EMBEDDING_MODE_VALUES` (constant), lines 5426-5426, exports `RAG_EMBEDDING_MODE_VALUES`
- order 269: `RAG_IMPORT_WORKER_COUNT` (constant), lines 5427-5430, exports `RAG_IMPORT_WORKER_COUNT`
- order 271: `RAG_PARSE_TIMEOUT_SECONDS` (constant), lines 5435-5438, exports `RAG_PARSE_TIMEOUT_SECONDS`
- order 1155: `RAG_TERM_GROUPS` (constant), lines 106318-110951, exports `RAG_TERM_GROUPS`
- order 1156: `RAG_RESEARCH_HINTS` (constant), lines 110952-110973, exports `RAG_RESEARCH_HINTS`
- order 1157: `RAG_CODE_HINTS` (constant), lines 110974-110984, exports `RAG_CODE_HINTS`
- order 1158: `RAG_SHORT_TOKEN_ALLOWLIST` (constant), lines 110985-111000, exports `RAG_SHORT_TOKEN_ALLOWLIST`
- order 1159: `RAG_EN_STOPWORDS` (constant), lines 111001-111073, exports `RAG_EN_STOPWORDS`
- order 1160: `RAG_ZH_STOPWORDS` (constant), lines 111074-111110, exports `RAG_ZH_STOPWORDS`
- order 1161: `RAG_GENERIC_ENTITY_TERMS_EN` (constant), lines 111111-111189, exports `RAG_GENERIC_ENTITY_TERMS_EN`
- order 1162: `RAG_GENERIC_ENTITY_TERMS_ZH` (constant), lines 111190-111232, exports `RAG_GENERIC_ENTITY_TERMS_ZH`
- order 1163: `RAG_STRUCTURAL_ENTITY_PATTERNS` (constant), lines 111233-111251, exports `RAG_STRUCTURAL_ENTITY_PATTERNS`
- order 1195: `CODE_LIBRARY_IGNORED_DIRS` (constant), lines 112209-112218, exports `CODE_LIBRARY_IGNORED_DIRS`
- order 1196: `CODE_LIBRARY_LANGUAGE_BY_EXT` (constant), lines 112219-112275, exports `CODE_LIBRARY_LANGUAGE_BY_EXT`
- order 1197: `CODE_LIBRARY_SPECIAL_FILENAMES` (constant), lines 112276-112282, exports `CODE_LIBRARY_SPECIAL_FILENAMES`

### `rag/index.py`

- order 1200: `_code_module_name` (function), lines 112307-112323, exports `_code_module_name`
- order 1201: `_code_choose_community` (function), lines 112324-112333, exports `_code_choose_community`
- order 1202: `_code_query_terms` (function), lines 112334-112348, exports `_code_query_terms`
- order 1211: `TFGraphIDFIndex` (class), lines 113479-115173, exports `TFGraphIDFIndex`
- order 1220: `CodeGraphIndex` (class), lines 118460-118948, exports `CodeGraphIndex`

### `rag/ingestion.py`

- order 1179: `_rag_trigram_set` (function), lines 111629-111636, exports `_rag_trigram_set`
- order 1180: `_rag_jaccard_sim` (function), lines 111637-111646, exports `_rag_jaccard_sim`
- order 1181: `_rag_mmr_select` (function), lines 111647-111696, exports `_rag_mmr_select`
- order 1186: `_rag_embed_text` (function), lines 111831-111854, exports `_rag_embed_text`
- order 1187: `_rag_embed_batch` (function), lines 111855-111863, exports `_rag_embed_batch`
- order 1188: `_rag_window_for_query` (function), lines 111864-111878, exports `_rag_window_for_query`
- order 1189: `_rag_focused_excerpt` (function), lines 111879-111921, exports `_rag_focused_excerpt`
- order 1190: `_rag_query_variants` (function), lines 111922-111961, exports `_rag_query_variants`
- order 1191: `_rag_parse_segments` (function), lines 111962-112024, exports `_rag_parse_segments`
- order 1192: `_rag_boundary_split` (function), lines 112025-112082, exports `_rag_boundary_split`
- order 1218: `_rag_parse_file_worker` (function), lines 117559-117575, exports `_rag_parse_file_worker`
- order 1219: `RAGIngestionService` (class), lines 117576-118459, exports `RAGIngestionService`
- order 1222: `CodeIngestionService` (class), lines 119240-119327, exports `CodeIngestionService`

### `rag/parsers.py`

- order 1164: `EvidenceRecord` (class), lines 111252-111286, exports `EvidenceRecord`
- order 1165: `_rag_float` (function), lines 111287-111293, exports `_rag_float`
- order 1166: `_rag_evidence_source_type` (function), lines 111294-111310, exports `_rag_evidence_source_type`
- order 1167: `_rag_normalize_evidence_record` (function), lines 111311-111366, exports `_rag_normalize_evidence_record`
- order 1168: `_rag_validate_evidence_record` (function), lines 111367-111409, exports `_rag_validate_evidence_record`
- order 1169: `_rag_evidence_batches` (function), lines 111410-111427, exports `_rag_evidence_batches`
- order 1170: `_rag_safe_name` (function), lines 111428-111433, exports `_rag_safe_name`
- order 1171: `_rag_detect_language` (function), lines 111434-111450, exports `_rag_detect_language`
- order 1172: `_rag_cjk_ngrams` (function), lines 111451-111465, exports `_rag_cjk_ngrams`
- order 1173: `_rag_is_noise_token` (function), lines 111466-111487, exports `_rag_is_noise_token`
- order 1174: `_rag_entity_allowed` (function), lines 111488-111502, exports `_rag_entity_allowed`
- order 1175: `_rag_filter_entities` (function), lines 111503-111519, exports `_rag_filter_entities`
- order 1176: `_rag_filename_entity_aliases` (function), lines 111520-111555, exports `_rag_filename_entity_aliases`
- order 1177: `_rag_apply_filename_entity_policy` (function), lines 111556-111588, exports `_rag_apply_filename_entity_policy`
- order 1178: `_rag_choose_community` (function), lines 111589-111628, exports `_rag_choose_community`
- order 1182: `_rag_tokenize` (function), lines 111697-111750, exports `_rag_tokenize`
- order 1183: `_rag_expand_tokens` (function), lines 111751-111774, exports `_rag_expand_tokens`
- order 1184: `_rag_extract_entities` (function), lines 111775-111793, exports `_rag_extract_entities`
- order 1185: `_rag_classify_document` (function), lines 111794-111830, exports `_rag_classify_document`
- order 1193: `_rag_structure_outline` (function), lines 112083-112121, exports `_rag_structure_outline`
- order 1194: `_rag_chunk_text` (function), lines 112122-112208, exports `_rag_chunk_text`
- order 1198: `_code_language_from_name` (function), lines 112283-112301, exports `_code_language_from_name`
- order 1199: `_code_is_test_path` (function), lines 112302-112306, exports `_code_is_test_path`
- order 1203: `_CallCollector` (class), lines 112349-112363, exports `_CallCollector`
- order 1204: `_ALGO_COMPLEXITY_RE` (assignment), lines 112364-112366, exports `_ALGO_COMPLEXITY_RE`
- order 1205: `_ALGO_STEP_RE` (assignment), lines 112367-112367, exports `_ALGO_STEP_RE`
- order 1206: `_ALGO_MATH_VARS` (assignment), lines 112368-112368, exports `_ALGO_MATH_VARS`
- order 1207: `_ALGO_DOC_KEYWORDS` (assignment), lines 112369-112369, exports `_ALGO_DOC_KEYWORDS`
- order 1208: `_detect_algo_chunk` (function), lines 112370-112395, exports `_detect_algo_chunk`
- order 1209: `CodeContentParser` (class), lines 112396-112962, exports `CodeContentParser`
- order 1210: `RAGContentParser` (class), lines 112963-113478, exports `RAGContentParser`

### `rag/store.py`

- order 1212: `RAGLibraryStore` (class), lines 115174-115812, exports `RAGLibraryStore`
- order 1213: `WikiStore` (class), lines 115813-116368, exports `WikiStore`
- order 1214: `UserMemoryStore` (class), lines 116369-117046, exports `UserMemoryStore`
- order 1215: `UserInteractionOptimizer` (class), lines 117047-117115, exports `UserInteractionOptimizer`
- order 1216: `UserIntentProfiler` (class), lines 117116-117157, exports `UserIntentProfiler`
- order 1217: `WorkflowMemoryStore` (class), lines 117158-117558, exports `WorkflowMemoryStore`
- order 1221: `CodeLibraryStore` (class), lines 118949-119239, exports `CodeLibraryStore`

### `rag/web_search.py`

- order 839: `_agent_web_bool` (function), lines 10557-10564, exports `_agent_web_bool`
- order 840: `_agent_web_int` (function), lines 10565-10572, exports `_agent_web_int`
- order 841: `_agent_web_host_is_local_name` (function), lines 10573-10579, exports `_agent_web_host_is_local_name`
- order 842: `_agent_web_ip_is_blocked` (function), lines 10580-10594, exports `_agent_web_ip_is_blocked`
- order 843: `_agent_web_canonical_url` (function), lines 10595-10624, exports `_agent_web_canonical_url`
- order 844: `_agent_web_domain_to_seed` (function), lines 10625-10636, exports `_agent_web_domain_to_seed`
- order 845: `_agent_web_query_terms` (function), lines 10637-10654, exports `_agent_web_query_terms`
- order 846: `_agent_web_query_domain_hints` (function), lines 10655-10695, exports `_agent_web_query_domain_hints`
- order 847: `_agent_web_query_needs_fresh_network` (function), lines 10696-10718, exports `_agent_web_query_needs_fresh_network`
- order 848: `_agent_web_extract_text_snippet` (function), lines 10719-10736, exports `_agent_web_extract_text_snippet`
- order 849: `AgentWebHTMLParser` (class), lines 10737-10816, exports `AgentWebHTMLParser`
- order 850: `_agent_web_decompress_bytes` (function), lines 10817-10840, exports `_agent_web_decompress_bytes`
- order 851: `_agent_web_charset_candidates` (function), lines 10841-10899, exports `_agent_web_charset_candidates`
- order 852: `_agent_web_decode_text_bytes` (function), lines 10900-10934, exports `_agent_web_decode_text_bytes`
- order 853: `AgentWebSearchEngine` (class), lines 10935-12715, exports `AgentWebSearchEngine`

### `server/http.py`

- order 713: `admin_language_payload` (function), lines 7530-7541, exports `admin_language_payload`
- order 828: `_UI_TRUNCATION_MARKER` (assignment), lines 10176-10178, exports `_UI_TRUNCATION_MARKER`
- order 829: `_ui_trim_text` (function), lines 10179-10187, exports `_ui_trim_text`
- order 830: `_bounded_ui_value` (function), lines 10188-10248, exports `_bounded_ui_value`
- order 831: `_bounded_ui_row` (function), lines 10249-10300, exports `_bounded_ui_row`
- order 832: `_bounded_ui_rows` (function), lines 10301-10349, exports `_bounded_ui_rows`
- order 833: `_enforce_ui_payload_budget` (function), lines 10350-10394, exports `_enforce_ui_payload_budget`
- order 834: `_apply_lite_snapshot_bounds` (function), lines 10395-10450, exports `_apply_lite_snapshot_bounds`
- order 1260: `AgentHTTPServer` (class), lines 136696-136735, exports `AgentHTTPServer`
- order 1263: `Handler` (class), lines 137937-139868, exports `Handler`
- order 1266: `SkillsReviewHandler` (class), lines 140677-140790, exports `SkillsReviewHandler`
- order 1270: `CollaborationHandler` (class), lines 142848-143318, exports `CollaborationHandler`

### `server/rag_admin.py`

- order 1265: `_RagAdminAuthMixin` (class), lines 140519-140676, exports `_RagAdminAuthMixin`
- order 1267: `RagAdminHandler` (class), lines 140791-140991, exports `RagAdminHandler`
- order 1268: `CodeAdminHandler` (class), lines 140992-141190, exports `CodeAdminHandler`

### `server/skills.py`

- order 1264: `SkillsHandler` (class), lines 139869-140518, exports `SkillsHandler`

### `session/manager.py`

- order 750: `SessionCreationLimitExceeded` (class), lines 8734-8739, exports `SessionCreationLimitExceeded`
- order 1143: `SessionManager` (class), lines 96729-99272, exports `SessionManager`

### `session/state.py`

- order 1142: `SessionState` (class), lines 32847-96728, exports `SessionState`

### `skills/embedded.py`

- order 1015: `EMBEDDED_SKILLS_ARCHIVE_B64` (constant), lines 19165-19166, exports `EMBEDDED_SKILLS_ARCHIVE_B64`
- order 1016: `EMBEDDED_SKILLS_ARCHIVE_SHA256` (constant), lines 19167-19167, exports `EMBEDDED_SKILLS_ARCHIVE_SHA256`
- order 1017: `EMBEDDED_SKILLS_ARCHIVE_FILES` (constant), lines 19168-19190, exports `EMBEDDED_SKILLS_ARCHIVE_FILES`
- order 1042: `BUILTIN_CLAWHUB_SKILLS_VERSION` (constant), lines 22426-22428, exports `BUILTIN_CLAWHUB_SKILLS_VERSION`
- order 1043: `EMBEDDED_CLAWHUB_SKILLS_ARCHIVE_B64` (constant), lines 22429-22674, exports `EMBEDDED_CLAWHUB_SKILLS_ARCHIVE_B64`
- order 1045: `MCP_BUILDER_SKILL_MD` (constant), lines 22722-22896, exports `MCP_BUILDER_SKILL_MD`
- order 1048: `SKILL_PROTOCOL_LOCAL` (constant), lines 22928-22929, exports `SKILL_PROTOCOL_LOCAL`
- order 1049: `SKILL_PROTOCOL_CLAWHUB` (constant), lines 22930-22930, exports `SKILL_PROTOCOL_CLAWHUB`
- order 1050: `SKILL_PROTOCOL_HTTP_JSON` (constant), lines 22931-22931, exports `SKILL_PROTOCOL_HTTP_JSON`
- order 1051: `SKILL_PROTOCOL_SPECS` (constant), lines 22932-22964, exports `SKILL_PROTOCOL_SPECS`

### `skills/provisioning.py`

- order 1018: `ensure_embedded_skills_at_root` (function), lines 19191-19256, exports `ensure_embedded_skills_at_root`
- order 1019: `ensure_embedded_skills` (function), lines 19257-19260, exports `ensure_embedded_skills`
- order 1021: `detect_upload_parser_capabilities` (function), lines 19267-19283, exports `detect_upload_parser_capabilities`
- order 1022: `_render_cap_markdown` (function), lines 19284-19299, exports `_render_cap_markdown`
- order 1023: `_write_text_if_changed` (function), lines 19300-19306, exports `_write_text_if_changed`
- order 1024: `ensure_generated_document_skills` (function), lines 19307-19396, exports `ensure_generated_document_skills`
- order 1025: `ensure_generated_image_coding_feedback_skill` (function), lines 19397-19497, exports `ensure_generated_image_coding_feedback_skill`
- order 1026: `_skill_knowledge_files` (function), lines 19498-19518, exports `_skill_knowledge_files`
- order 1027: `analyze_skill_building_knowledge` (function), lines 19519-19574, exports `analyze_skill_building_knowledge`
- order 1028: `_sanitize_skill_slug` (function), lines 19575-19578, exports `_sanitize_skill_slug`
- order 1029: `_build_skills_gen_skill_content` (function), lines 19579-19611, exports `_build_skills_gen_skill_content`
- order 1030: `ensure_generated_skills_gen_skill` (function), lines 19612-19617, exports `ensure_generated_skills_gen_skill`
- order 1031: `ensure_generated_execution_recovery_skill` (function), lines 19618-19702, exports `ensure_generated_execution_recovery_skill`
- order 1032: `ensure_generated_systematic_debugging_skill` (function), lines 19703-19976, exports `ensure_generated_systematic_debugging_skill`
- order 1033: `ensure_generated_code_engineering_mastery_skill` (function), lines 19977-20096, exports `ensure_generated_code_engineering_mastery_skill`
- order 1034: `ensure_generated_smart_file_navigation_skill` (function), lines 20097-20213, exports `ensure_generated_smart_file_navigation_skill`
- order 1035: `ensure_generated_html_frontend_report_skills` (function), lines 20214-20422, exports `ensure_generated_html_frontend_report_skills`
- order 1036: `ensure_generated_deep_research_skills` (function), lines 20423-20692, exports `ensure_generated_deep_research_skills`
- order 1037: `ensure_generated_research_scientific_skills` (function), lines 20693-21330, exports `ensure_generated_research_scientific_skills`
- order 1038: `ensure_generated_rag_mastery_skills` (function), lines 21331-21632, exports `ensure_generated_rag_mastery_skills`
- order 1039: `ensure_generated_multimodal_comprehension_skills` (function), lines 21633-22327, exports `ensure_generated_multimodal_comprehension_skills`
- order 1040: `ensure_generated_runtime_skills_manifest` (function), lines 22328-22362, exports `ensure_generated_runtime_skills_manifest`
- order 1041: `ensure_generated_agent_web_search_skill` (function), lines 22363-22425, exports `ensure_generated_agent_web_search_skill`
- order 1044: `ensure_embedded_clawhub_skills` (function), lines 22675-22721, exports `ensure_embedded_clawhub_skills`
- order 1046: `ensure_generated_mcp_builder_skill` (function), lines 22897-22908, exports `ensure_generated_mcp_builder_skill`
- order 1047: `ensure_runtime_skills` (function), lines 22909-22927, exports `ensure_runtime_skills`

### `skills/store.py`

- order 556: `_skill_term_match` (function), lines 6326-6346, exports `_skill_term_match`
- order 1052: `_BUILTIN_SKILLS` (assignment), lines 22965-23073, exports `_BUILTIN_SKILLS`
- order 1053: `SkillStore` (class), lines 23074-24989, exports `SkillStore`

### `skills/studio.py`

- order 1245: `SkillsStudioError` (class), lines 123135-123144, exports `SkillsStudioError`
- order 1246: `_studio_slug` (function), lines 123145-123160, exports `_studio_slug`
- order 1247: `_studio_hash` (function), lines 123161-123164, exports `_studio_hash`
- order 1248: `_studio_cookie_value` (function), lines 123165-123174, exports `_studio_cookie_value`
- order 1249: `SkillsStudioStore` (class), lines 123175-125032, exports `SkillsStudioStore`

### `utils/compress.py`

- order 857: `compress_text_blob` (function), lines 12880-12886, exports `compress_text_blob`
- order 858: `decompress_text_blob` (function), lines 12887-12896, exports `decompress_text_blob`

### `utils/crypto.py`

- order 958: `CryptoBox` (class), lines 15884-16037, exports `CryptoBox`

### `utils/errors.py`

- order 885: `EmptyActionError` (class), lines 13513-13516, exports `EmptyActionError`
- order 1055: `ProcessManagerError` (class), lines 25125-25130, exports `ProcessManagerError`

### `utils/files.py`

- order 707: `_normalize_js_lib_asset_ref` (function), lines 7400-7415, exports `_normalize_js_lib_asset_ref`
- order 708: `_resolve_js_lib_asset_path` (function), lines 7416-7447, exports `_resolve_js_lib_asset_path`
- order 709: `_discover_extra_js_lib_files` (function), lines 7448-7480, exports `_discover_extra_js_lib_files`
- order 803: `safe_path` (function), lines 9589-9599, exports `safe_path`
- order 804: `_safe_js_filename` (function), lines 9600-9608, exports `_safe_js_filename`
- order 805: `_sha256_bytes` (function), lines 9609-9611, exports `_sha256_bytes`
- order 806: `_sha256_file` (function), lines 9612-9621, exports `_sha256_file`
- order 807: `_download_http_bytes` (function), lines 9622-9631, exports `_download_http_bytes`
- order 808: `offline_js_lib_root` (function), lines 9632-9634, exports `offline_js_lib_root`
- order 809: `_offline_js_entry_relative_path` (function), lines 9635-9640, exports `_offline_js_entry_relative_path`
- order 810: `_archive_member_relative_path` (function), lines 9641-9651, exports `_archive_member_relative_path`
- order 811: `_path_size_bytes` (function), lines 9652-9668, exports `_path_size_bytes`
- order 812: `_extract_archive_to_dir` (function), lines 9669-9710, exports `_extract_archive_to_dir`
- order 813: `_package_required_paths` (function), lines 9711-9718, exports `_package_required_paths`
- order 814: `_package_required_globs` (function), lines 9719-9735, exports `_package_required_globs`
- order 815: `_package_install_ready` (function), lines 9736-9758, exports `_package_install_ready`
- order 816: `_postprocess_offline_js_package` (function), lines 9759-9795, exports `_postprocess_offline_js_package`
- order 817: `_ensure_offline_js_package` (function), lines 9796-9840, exports `_ensure_offline_js_package`
- order 818: `_render_offline_js_catalog_md` (function), lines 9841-9858, exports `_render_offline_js_catalog_md`
- order 819: `load_offline_js_lib_index` (function), lines 9859-9869, exports `load_offline_js_lib_index`
- order 820: `ensure_offline_js_libs` (function), lines 9870-10028, exports `ensure_offline_js_libs`
- order 821: `_offline_js_catalog_entry_for_asset` (function), lines 10029-10049, exports `_offline_js_catalog_entry_for_asset`
- order 822: `ensure_offline_js_asset` (function), lines 10050-10107, exports `ensure_offline_js_asset`
- order 823: `_normalize_external_js_url` (function), lines 10108-10113, exports `_normalize_external_js_url`
- order 824: `is_external_js_src` (function), lines 10114-10117, exports `is_external_js_src`
- order 825: `match_offline_js_catalog_by_url` (function), lines 10118-10135, exports `match_offline_js_catalog_by_url`
- order 826: `cache_external_js_url` (function), lines 10136-10171, exports `cache_external_js_url`
- order 961: `try_read_text` (function), lines 16281-16290, exports `try_read_text`
- order 983: `_start_offline_js_warmup` (function), lines 17894-17911, exports `_start_offline_js_warmup`

### `utils/http.py`

- order 123: `_URL_OPEN_ORIGINAL` (assignment), lines 4909-4909, exports `_URL_OPEN_ORIGINAL`
- order 124: `_HTTP_SSL_CONTEXT` (assignment), lines 4910-4910, exports `_HTTP_SSL_CONTEXT`
- order 151: `_shared_http_ssl_context` (function), lines 4974-4997, exports `_shared_http_ssl_context`
- order 152: `urlopen` (function), lines 4998-5007, exports `urlopen`
- order 796: `json_response_bytes` (function), lines 9534-9536, exports `json_response_bytes`
- order 797: `read_http_json_body` (function), lines 9537-9550, exports `read_http_json_body`
- order 798: `close_if_http_request_body_unread` (function), lines 9551-9564, exports `close_if_http_request_body_unread`

### `utils/json_utils.py`

- order 175: `JSON_FSYNC_ENABLED` (constant), lines 5279-5279, exports `JSON_FSYNC_ENABLED`
- order 795: `json_dumps` (function), lines 9530-9533, exports `json_dumps`
- order 873: `parse_tool_arguments` (function), lines 13260-13270, exports `parse_tool_arguments`
- order 874: `repair_truncated_json_object` (function), lines 13271-13325, exports `repair_truncated_json_object`
- order 875: `parse_tool_arguments_with_error` (function), lines 13326-13357, exports `parse_tool_arguments_with_error`
- order 876: `_is_valid_json_object` (function), lines 13358-13363, exports `_is_valid_json_object`
- order 877: `_scan_top_level_json_objects` (function), lines 13364-13387, exports `_scan_top_level_json_objects`
- order 878: `reconstruct_streamed_tool_args` (function), lines 13388-13432, exports `reconstruct_streamed_tool_args`
- order 899: `parse_json_object` (function), lines 13787-13793, exports `parse_json_object`
- order 900: `decode_model_json_object` (function), lines 13794-13828, exports `decode_model_json_object`
- order 902: `standard_model_json_object` (function), lines 13833-13896, exports `standard_model_json_object`
- order 903: `semantic_json_repair_request` (function), lines 13897-13913, exports `semantic_json_repair_request`
- order 904: `validate_semantic_json_repair` (function), lines 13914-13943, exports `validate_semantic_json_repair`
- order 906: `extract_json_object_from_text` (function), lines 13996-14020, exports `extract_json_object_from_text`
- order 962: `_json_default_copy` (function), lines 16291-16297, exports `_json_default_copy`
- order 963: `_read_json_file` (function), lines 16298-16319, exports `_read_json_file`
- order 964: `_write_json_file` (function), lines 16320-16348, exports `_write_json_file`

### `utils/media.py`

- order 700: `_capability_probe_png_bytes` (function), lines 7038-7052, exports `_capability_probe_png_bytes`
- order 701: `_capability_probe_audio_bytes` (function), lines 7053-7064, exports `_capability_probe_audio_bytes`
- order 702: `_capability_probe_video_bytes` (function), lines 7065-7069, exports `_capability_probe_video_bytes`
- order 765: `guess_mime_from_name` (function), lines 9082-9086, exports `guess_mime_from_name`
- order 766: `_convert_image_to_safe_format` (function), lines 9087-9106, exports `_convert_image_to_safe_format`
- order 767: `guess_ext_from_mime` (function), lines 9107-9115, exports `guess_ext_from_mime`

### `utils/misc.py`

- order 768: `now_ts` (function), lines 9116-9118, exports `now_ts`
- order 769: `_benign_socket_log_lock` (assignment), lines 9119-9121, exports `_benign_socket_log_lock`
- order 770: `_benign_socket_log_state` (assignment), lines 9122-9122, exports `_benign_socket_log_state`
- order 772: `is_benign_socket_error` (function), lines 9138-9158, exports `is_benign_socket_error`
- order 773: `_socket_error_code` (function), lines 9159-9170, exports `_socket_error_code`
- order 774: `_log_benign_socket_error_limited` (function), lines 9171-9207, exports `_log_benign_socket_error_limited`
- order 775: `swallow_benign_socket_error` (function), lines 9208-9214, exports `swallow_benign_socket_error`
- order 776: `normalize_timeout_seconds` (function), lines 9215-9230, exports `normalize_timeout_seconds`
- order 777: `detect_local_lan_ip` (function), lines 9231-9242, exports `detect_local_lan_ip`
- order 778: `_LOCAL_LAN_IP_CACHE` (assignment), lines 9243-9244, exports `_LOCAL_LAN_IP_CACHE`
- order 779: `detect_local_lan_ip_cached` (function), lines 9245-9258, exports `detect_local_lan_ip_cached`
- order 799: `make_id` (function), lines 9565-9567, exports `make_id`
- order 800: `sanitize_profile_id` (function), lines 9568-9571, exports `sanitize_profile_id`
- order 956: `user_id_from_ip` (function), lines 15843-15850, exports `user_id_from_ip`
- order 960: `_meta_string_list` (function), lines 16267-16280, exports `_meta_string_list`
- order 1020: `_module_exists` (function), lines 19261-19266, exports `_module_exists`

### `utils/sqlite.py`

- order 70: `_ClosingSQLiteConnection` (class), lines 74-83, exports `_ClosingSQLiteConnection`
- order 71: `_connect_sqlite` (function), lines 84-117, exports `_connect_sqlite`
- order 1272: `sqlite_failure_diagnostics` (function), lines 143537-143621, exports `sqlite_failure_diagnostics`

### `utils/text.py`

- order 163: `MAX_TOOL_OUTPUT` (constant), lines 5267-5267, exports `MAX_TOOL_OUTPUT`
- order 512: `SOCKET_NOISE_LINE_PATTERNS` (constant), lines 6079-6084, exports `SOCKET_NOISE_LINE_PATTERNS`
- order 771: `filter_runtime_noise_lines` (function), lines 9123-9137, exports `filter_runtime_noise_lines`
- order 784: `safe_utf8_bytes` (function), lines 9383-9387, exports `safe_utf8_bytes`
- order 785: `escape_invalid_utf8_text` (function), lines 9388-9390, exports `escape_invalid_utf8_text`
- order 786: `sanitize_utf8_surrogates` (function), lines 9391-9404, exports `sanitize_utf8_surrogates`
- order 787: `decode_utf8_replace` (function), lines 9405-9409, exports `decode_utf8_replace`
- order 827: `trim` (function), lines 10172-10175, exports `trim`
- order 835: `is_synthetic_public_progress` (function), lines 10451-10470, exports `is_synthetic_public_progress`
- order 837: `display_clean` (function), lines 10523-10537, exports `display_clean`
- order 838: `short_title_from` (function), lines 10538-10556, exports `short_title_from`
- order 854: `_fmt_export_ts` (function), lines 12716-12726, exports `_fmt_export_ts`
- order 855: `_html_esc` (function), lines 12727-12730, exports `_html_esc`
- order 856: `_text_to_minimal_pdf` (function), lines 12731-12879, exports `_text_to_minimal_pdf`
- order 859: `normalize_embedded_newlines` (function), lines 12897-12906, exports `normalize_embedded_newlines`
- order 860: `_map_todo_status_token` (function), lines 12907-12945, exports `_map_todo_status_token`
- order 861: `_TODO_SHORT_ID_RE` (assignment), lines 12946-12953, exports `_TODO_SHORT_ID_RE`
- order 862: `_TODO_SHORT_ID_TAG_RE` (assignment), lines 12954-12954, exports `_TODO_SHORT_ID_TAG_RE`
- order 863: `normalize_todo_short_id` (function), lines 12955-12960, exports `normalize_todo_short_id`
- order 864: `strip_todo_short_id_tag` (function), lines 12961-12969, exports `strip_todo_short_id_tag`
- order 865: `split_todo_status_text` (function), lines 12970-12974, exports `split_todo_status_text`
- order 866: `split_todo_status_text_with_id` (function), lines 12975-13048, exports `split_todo_status_text_with_id`
- order 867: `extract_todo_rows_from_text` (function), lines 13049-13131, exports `extract_todo_rows_from_text`
- order 868: `decode_structured_todo_container` (function), lines 13132-13150, exports `decode_structured_todo_container`
- order 869: `infer_todo_status_from_text` (function), lines 13151-13159, exports `infer_todo_status_from_text`
- order 870: `split_structured_todo_content` (function), lines 13160-13215, exports `split_structured_todo_content`
- order 871: `is_todo_transport_metadata` (function), lines 13216-13229, exports `is_todo_transport_metadata`
- order 872: `normalize_work_text` (function), lines 13230-13259, exports `normalize_work_text`
- order 986: `make_unified_diff` (function), lines 17957-17975, exports `make_unified_diff`
- order 987: `_skip_row` (function), lines 17976-17981, exports `_skip_row`
- order 988: `_row_is_hot` (function), lines 17982-17985, exports `_row_is_hot`
- order 989: `_hotspot_index` (function), lines 17986-18009, exports `_hotspot_index`
- order 990: `_compress_rows_keep_hotspot` (function), lines 18010-18059, exports `_compress_rows_keep_hotspot`
- order 991: `_focused_diff_rows_from_opcodes` (function), lines 18060-18194, exports `_focused_diff_rows_from_opcodes`
- order 992: `make_numbered_diff` (function), lines 18195-18227, exports `make_numbered_diff`
- order 993: `render_numbered_diff_text` (function), lines 18228-18241, exports `render_numbered_diff_text`

### `web/admin_assets.py`

- order 1152: `ADMIN_INDEX_HTML` (constant), lines 105325-105642, exports `ADMIN_INDEX_HTML`
- order 1153: `ADMIN_CSS` (constant), lines 105643-105805, exports `ADMIN_CSS`
- order 1154: `ADMIN_JS` (constant), lines 105806-106317, exports `ADMIN_JS`

### `web/assets.py`

- order 1144: `INDEX_HTML` (constant), lines 99273-99534, exports `INDEX_HTML`
- order 1145: `APP_CSS` (constant), lines 99535-100077, exports `APP_CSS`
- order 1146: `APP_JS` (constant), lines 100078-104861, exports `APP_JS`
- order 1147: `APP_CSS` (constant), lines 104862-104882, exports `APP_CSS`
- order 1148: `APP_TS` (constant), lines 104883-104922, exports `APP_TS`

### `web/skills_assets.py`

- order 1149: `SKILLS_INDEX_HTML` (constant), lines 104923-105078, exports `SKILLS_INDEX_HTML`
- order 1150: `SKILLS_EXTRA_CSS` (constant), lines 105079-105178, exports `SKILLS_EXTRA_CSS`
- order 1151: `SKILLS_APP_JS` (constant), lines 105179-105324, exports `SKILLS_APP_JS`
