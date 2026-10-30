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
| `_imports.py` | 76 | 94 | — | 1–5141 |
| `admin/auth.py` | 3 | 3 | `admin/constants.py`, `utils/misc.py`, `utils/sqlite.py` | 16084–16926 |
| `admin/config.py` | 8 | 8 | `config/constants.py`, `config/paths.py`, `config/settings.py`, `llm/constants.py`, `llm/gate.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` | 17674–18177 |
| `admin/constants.py` | 16 | 16 | — | 5148–125262 |
| `agent/background.py` | 1 | 1 | `agent/process.py`, `config/constants.py`, `ide/sandbox.py`, `utils/misc.py`, `utils/text.py` | 25712–26337 |
| `agent/bus.py` | 1 | 1 | `config/constants.py`, `utils/crypto.py`, `utils/misc.py` | 26338–26403 |
| `agent/context.py` | 2 | 2 | `agent/tools.py` | 5881–14065 |
| `agent/errors.py` | 1 | 1 | — | 13750–13753 |
| `agent/events.py` | 1 | 1 | — | 18904–18958 |
| `agent/evidence.py` | 2 | 2 | `utils/sqlite.py` | 32728–33067 |
| `agent/process.py` | 9 | 9 | `ide/sandbox.py`, `utils/errors.py`, `utils/misc.py`, `utils/text.py` | 6201–25711 |
| `agent/tasks.py` | 1 | 1 | `utils/crypto.py`, `utils/json_utils.py`, `utils/misc.py` | 25211–25345 |
| `agent/todo.py` | 1 | 1 | `config/constants.py`, `config/settings.py`, `utils/misc.py`, `utils/text.py` | 18959–19385 |
| `agent/tools.py` | 17 | 21 | `config/constants.py`, `config/settings.py`, `utils/text.py` | 18783–32195 |
| `agent/worktree.py` | 1 | 1 | `agent/process.py`, `agent/tasks.py`, `config/constants.py`, `utils/crypto.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` | 26404–26616 |
| `app/context.py` | 1 | 1 | `admin/auth.py`, `admin/config.py`, `admin/constants.py`, `agent/process.py`, `agent/tools.py`, `app/services.py`, `collaboration/core.py`, `config/bootstrap.py`, `config/constants.py`, `config/paths.py`, `config/settings.py`, `ide/assets.py`, `ide/auth.py`, `ide/errors.py`, `ide/events.py`, `ide/preview.py`, `ide/sandbox.py`, `ide/toolchains.py`, `llm/client.py`, `llm/constants.py`, `llm/gate.py`, `llm/utils.py`, `mcp/driver.py`, `rag/assets.py`, `rag/constants.py`, `rag/ingestion.py`, `rag/parsers.py`, `rag/store.py`, `server/http.py`, `session/manager.py`, `session/state.py`, `skills/provisioning.py`, `skills/store.py`, `skills/studio.py`, `utils/crypto.py`, `utils/files.py`, `utils/http.py`, `utils/json_utils.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py`, `web/assets.py`, `web/skills_assets.py` | 125328–136866 |
| `app/main.py` | 2 | 1 | `admin/config.py`, `admin/constants.py`, `agent/tools.py`, `app/context.py`, `collaboration/watcher.py`, `config/constants.py`, `config/paths.py`, `config/settings.py`, `ide/handler.py`, `llm/constants.py`, `llm/gate.py`, `llm/utils.py`, `mcp/constants.py`, `mcp/service.py`, `rag/constants.py`, `server/http.py`, `server/rag_admin.py`, `server/skills.py`, `skills/provisioning.py`, `utils/files.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` | 143884–145873 |
| `app/services.py` | 2 | 2 | `admin/constants.py`, `config/settings.py`, `skills/embedded.py`, `skills/store.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/sqlite.py`, `utils/text.py` | 136907–138107 |
| `collaboration/core.py` | 23 | 23 | `config/constants.py`, `utils/sqlite.py` | 1760–5001 |
| `collaboration/watcher.py` | 2 | 2 | `utils/misc.py`, `utils/sqlite.py`, `utils/text.py` | 143791–143883 |
| `config/bootstrap.py` | 7 | 7 | `config/constants.py`, `config/settings.py`, `utils/json_utils.py`, `utils/misc.py` | 124–16639 |
| `config/constants.py` | 515 | 510 | `config/bootstrap.py`, `rag/constants.py` | 1711–125258 |
| `config/paths.py` | 13 | 13 | `agent/process.py`, `utils/crypto.py`, `utils/text.py` | 5147–9821 |
| `config/settings.py` | 71 | 71 | `agent/tools.py`, `config/constants.py`, `config/paths.py`, `ide/preview.py`, `llm/constants.py`, `llm/gate.py`, `llm/utils.py`, `rag/constants.py`, `skills/provisioning.py`, `utils/http.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` | 7714–31430 |
| `ide/assets.py` | 8 | 3 | — | 122173–123330 |
| `ide/auth.py` | 2 | 2 | `admin/auth.py`, `admin/constants.py`, `config/constants.py`, `utils/misc.py`, `utils/sqlite.py`, `utils/text.py` | 16927–17658 |
| `ide/errors.py` | 2 | 2 | — | 17659–17673 |
| `ide/events.py` | 1 | 1 | `config/constants.py`, `utils/text.py` | 10704–10755 |
| `ide/handler.py` | 1 | 1 | `admin/auth.py`, `app/context.py`, `collaboration/core.py`, `config/constants.py`, `config/settings.py`, `ide/auth.py`, `ide/errors.py`, `ide/events.py`, `session/manager.py`, `session/state.py`, `utils/http.py`, `utils/json_utils.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py` | 141360–143016 |
| `ide/preview.py` | 12 | 12 | `config/constants.py`, `utils/text.py` | 18463–18903 |
| `ide/sandbox.py` | 21 | 21 | `agent/process.py`, `utils/misc.py` | 9643–32727 |
| `ide/toolchains.py` | 7 | 7 | — | 6540–125327 |
| `llm/client.py` | 2 | 2 | `agent/context.py`, `agent/tools.py`, `config/constants.py`, `config/settings.py`, `llm/gate.py`, `llm/utils.py`, `utils/http.py`, `utils/json_utils.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py` | 27999–31336 |
| `llm/constants.py` | 17 | 17 | — | 5145–14428 |
| `llm/gate.py` | 22 | 22 | `config/constants.py`, `config/settings.py`, `llm/client.py`, `utils/misc.py`, `utils/text.py` | 6023–28476 |
| `llm/utils.py` | 37 | 37 | `agent/context.py`, `agent/process.py`, `config/settings.py`, `llm/constants.py`, `utils/http.py`, `utils/json_utils.py`, `utils/text.py` | 13666–15083 |
| `mcp/constants.py` | 8 | 8 | — | 5517–26652 |
| `mcp/driver.py` | 13 | 13 | `mcp/constants.py`, `utils/files.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` | 26653–27998 |
| `mcp/service.py` | 1 | 1 | `app/context.py`, `config/constants.py`, `utils/files.py`, `utils/http.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` | 143488–143705 |
| `rag/assets.py` | 6 | 6 | — | 119549–122172 |
| `rag/constants.py` | 77 | 77 | — | 5513–112503 |
| `rag/index.py` | 5 | 5 | `config/constants.py`, `rag/constants.py`, `rag/ingestion.py`, `rag/parsers.py`, `utils/misc.py`, `utils/text.py` | 112528–119169 |
| `rag/ingestion.py` | 13 | 13 | `config/constants.py`, `config/settings.py`, `rag/constants.py`, `rag/parsers.py`, `rag/store.py`, `session/state.py`, `utils/files.py`, `utils/json_utils.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py` | 111850–119548 |
| `rag/parsers.py` | 31 | 31 | `agent/process.py`, `config/constants.py`, `rag/constants.py`, `rag/ingestion.py`, `utils/files.py`, `utils/json_utils.py`, `utils/media.py`, `utils/text.py` | 111473–113699 |
| `rag/store.py` | 7 | 7 | `config/constants.py`, `config/settings.py`, `ide/preview.py`, `rag/constants.py`, `rag/index.py`, `rag/ingestion.py`, `rag/parsers.py`, `skills/provisioning.py`, `utils/files.py`, `utils/json_utils.py`, `utils/media.py`, `utils/misc.py`, `utils/sqlite.py`, `utils/text.py` | 115395–119460 |
| `rag/web_search.py` | 15 | 15 | `config/constants.py`, `config/paths.py`, `rag/constants.py`, `utils/http.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/sqlite.py`, `utils/text.py` | 10790–12948 |
| `server/http.py` | 12 | 12 | `admin/auth.py`, `admin/config.py`, `admin/constants.py`, `agent/process.py`, `app/context.py`, `collaboration/core.py`, `collaboration/watcher.py`, `config/constants.py`, `config/paths.py`, `config/settings.py`, `ide/auth.py`, `ide/handler.py`, `ide/preview.py`, `llm/gate.py`, `llm/utils.py`, `server/rag_admin.py`, `session/manager.py`, `session/state.py`, `skills/studio.py`, `utils/errors.py`, `utils/files.py`, `utils/http.py`, `utils/json_utils.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py`, `web/admin_assets.py` | 7763–143487 |
| `server/rag_admin.py` | 3 | 3 | `admin/auth.py`, `app/context.py`, `config/constants.py`, `rag/constants.py`, `utils/http.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py` | 140688–141359 |
| `server/skills.py` | 1 | 1 | `admin/auth.py`, `app/context.py`, `config/constants.py`, `config/paths.py`, `config/settings.py`, `llm/gate.py`, `session/manager.py`, `skills/provisioning.py`, `skills/studio.py`, `utils/http.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py` | 140038–140687 |
| `session/manager.py` | 2 | 2 | `agent/process.py`, `config/constants.py`, `config/paths.py`, `config/settings.py`, `llm/client.py`, `llm/gate.py`, `llm/utils.py`, `rag/store.py`, `session/state.py`, `skills/store.py`, `utils/crypto.py`, `utils/files.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` | 8967–99493 |
| `session/state.py` | 1 | 1 | `admin/constants.py`, `agent/background.py`, `agent/bus.py`, `agent/context.py`, `agent/errors.py`, `agent/events.py`, `agent/evidence.py`, `agent/process.py`, `agent/tasks.py`, `agent/todo.py`, `agent/tools.py`, `agent/worktree.py`, `collaboration/core.py`, `config/constants.py`, `config/paths.py`, `config/settings.py`, `ide/events.py`, `ide/preview.py`, `ide/sandbox.py`, `llm/client.py`, `llm/constants.py`, `llm/gate.py`, `llm/utils.py`, `mcp/constants.py`, `mcp/driver.py`, `rag/constants.py`, `rag/parsers.py`, `rag/web_search.py`, `server/http.py`, `skills/provisioning.py`, `skills/store.py`, `utils/compress.py`, `utils/crypto.py`, `utils/errors.py`, `utils/files.py`, `utils/http.py`, `utils/json_utils.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py` | 33068–96949 |
| `skills/embedded.py` | 10 | 10 | — | 19386–23185 |
| `skills/provisioning.py` | 26 | 26 | `config/paths.py`, `skills/embedded.py`, `utils/files.py`, `utils/json_utils.py`, `utils/misc.py` | 19412–23148 |
| `skills/store.py` | 3 | 3 | `config/constants.py`, `config/settings.py`, `llm/utils.py`, `skills/embedded.py`, `utils/files.py`, `utils/http.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` | 6559–25210 |
| `skills/studio.py` | 5 | 5 | `agent/process.py`, `collaboration/core.py`, `config/constants.py`, `config/settings.py`, `ide/sandbox.py`, `llm/client.py`, `llm/constants.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/sqlite.py`, `utils/text.py` | 123356–125253 |
| `utils/compress.py` | 2 | 2 | — | 13113–13129 |
| `utils/crypto.py` | 1 | 1 | `utils/json_utils.py` | 16117–16270 |
| `utils/errors.py` | 2 | 2 | — | 13746–25351 |
| `utils/files.py` | 29 | 29 | `config/constants.py`, `config/paths.py`, `utils/http.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` | 7633–18134 |
| `utils/http.py` | 7 | 7 | `utils/json_utils.py`, `utils/text.py` | 5142–9797 |
| `utils/json_utils.py` | 17 | 17 | `utils/text.py` | 5512–16581 |
| `utils/media.py` | 6 | 6 | — | 7271–9348 |
| `utils/misc.py` | 16 | 16 | `config/constants.py` | 9349–19487 |
| `utils/sqlite.py` | 3 | 3 | — | 74–143790 |
| `utils/text.py` | 36 | 36 | `config/constants.py` | 5500–18462 |
| `web/admin_assets.py` | 3 | 3 | — | 105546–106538 |
| `web/assets.py` | 5 | 4 | — | 99494–105143 |
| `web/skills_assets.py` | 3 | 3 | — | 105144–105545 |

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
- order 77: `_import_1714` (import), lines 1713-1718, exports `EVOLUTION_MODES`, `LiquidKernelControlPlane`, `LiquidKernelError`
- order 79: `_import_1739` (import), lines 1735-1741, exports `_LiquidKernelRegistry`
- order 120: `_try_import_5125` (import), lines 5123-5132, exports `_fcntl`, `_pty`, `_termios`
- order 121: `_try_import_5134` (import), lines 5133-5137, exports `_certifi`
- order 122: `_try_import_5138` (import), lines 5138-5141, exports `_yaml`

### `admin/auth.py`

- order 957: `trusted_client_ip` (function), lines 16084-16116, exports `trusted_client_ip`
- order 971: `AdminAuthError` (class), lines 16640-16647, exports `AdminAuthError`
- order 972: `AdminAuthStore` (class), lines 16648-16926, exports `AdminAuthStore`

### `admin/config.py`

- order 977: `_admin_config_schema` (function), lines 17674-17797, exports `_admin_config_schema`
- order 978: `_admin_factory_config` (function), lines 17798-17801, exports `_admin_factory_config`
- order 979: `_admin_coerce_config` (function), lines 17802-17957, exports `_admin_coerce_config`
- order 980: `_admin_config_to_argv` (function), lines 17958-17994, exports `_admin_config_to_argv`
- order 981: `_admin_restart_probe_url` (function), lines 17995-18010, exports `_admin_restart_probe_url`
- order 982: `_admin_supervised_restart` (function), lines 18011-18116, exports `_admin_supervised_restart`
- order 984: `_admin_argparse_defaults` (function), lines 18135-18156, exports `_admin_argparse_defaults`
- order 985: `_admin_config_from_namespace` (function), lines 18157-18177, exports `_admin_config_from_namespace`

### `admin/constants.py`

- order 129: `ADMIN_STATE_DIRNAME` (constant), lines 5148-5148, exports `ADMIN_STATE_DIRNAME`
- order 130: `ADMIN_CONFIG_FILENAME` (constant), lines 5149-5149, exports `ADMIN_CONFIG_FILENAME`
- order 131: `ADMIN_APPS_FILENAME` (constant), lines 5150-5150, exports `ADMIN_APPS_FILENAME`
- order 132: `ADMIN_TELEMETRY_FILENAME` (constant), lines 5151-5151, exports `ADMIN_TELEMETRY_FILENAME`
- order 133: `ADMIN_AUTH_FILENAME` (constant), lines 5152-5152, exports `ADMIN_AUTH_FILENAME`
- order 143: `ADMIN_MAX_APP_SKILLS` (constant), lines 5199-5199, exports `ADMIN_MAX_APP_SKILLS`
- order 144: `ADMIN_MAX_APP_CAPSULE_CHARS` (constant), lines 5200-5200, exports `ADMIN_MAX_APP_CAPSULE_CHARS`
- order 145: `ADMIN_MAX_APP_RESOURCE_FILES` (constant), lines 5201-5201, exports `ADMIN_MAX_APP_RESOURCE_FILES`
- order 146: `ADMIN_MAX_APP_RESOURCE_BYTES` (constant), lines 5202-5202, exports `ADMIN_MAX_APP_RESOURCE_BYTES`
- order 147: `ADMIN_APP_INLINE_BLOB_BYTES` (constant), lines 5203-5203, exports `ADMIN_APP_INLINE_BLOB_BYTES`
- order 148: `ADMIN_AUTH_SESSION_TTL_SECONDS` (constant), lines 5204-5204, exports `ADMIN_AUTH_SESSION_TTL_SECONDS`
- order 149: `ADMIN_AUTH_PASSWORD_ITERATIONS` (constant), lines 5205-5205, exports `ADMIN_AUTH_PASSWORD_ITERATIONS`
- order 150: `ADMIN_AUTH_MAX_ACTIVE_SESSIONS` (constant), lines 5206-5206, exports `ADMIN_AUTH_MAX_ACTIVE_SESSIONS`
- order 1253: `ADMIN_SKILLS_REVIEW_HTML` (constant), lines 125259-125260, exports `ADMIN_SKILLS_REVIEW_HTML`
- order 1254: `ADMIN_SKILLS_REVIEW_CSS` (constant), lines 125261-125261, exports `ADMIN_SKILLS_REVIEW_CSS`
- order 1255: `ADMIN_SKILLS_REVIEW_JS` (constant), lines 125262-125262, exports `ADMIN_SKILLS_REVIEW_JS`

### `agent/background.py`

- order 1057: `BackgroundManager` (class), lines 25712-26337, exports `BackgroundManager`

### `agent/bus.py`

- order 1058: `MessageBus` (class), lines 26338-26403, exports `MessageBus`

### `agent/context.py`

- order 345: `_READ_DISPATCH_CONTEXT` (assignment), lines 5881-5884, exports `_READ_DISPATCH_CONTEXT`
- order 901: `compact_successful_write_history` (function), lines 14062-14065, exports `compact_successful_write_history`

### `agent/errors.py`

- order 886: `CircuitBreakerTriggered` (class), lines 13750-13753, exports `CircuitBreakerTriggered`

### `agent/events.py`

- order 1013: `EventHub` (class), lines 18904-18958, exports `EventHub`

### `agent/evidence.py`

- order 1140: `EvidenceRetrievalController` (class), lines 32728-33064, exports `EvidenceRetrievalController`
- order 1141: `_EVIDENCE_CONTROLLER_INIT_LOCK` (assignment), lines 33065-33067, exports `_EVIDENCE_CONTROLLER_INIT_LOCK`

### `agent/process.py`

- order 458: `_TOOL_CANCEL_LOCAL` (assignment), lines 6201-6204, exports `_TOOL_CANCEL_LOCAL`
- order 459: `_TOOL_ORPHAN_LOCK` (assignment), lines 6205-6205, exports `_TOOL_ORPHAN_LOCK`
- order 789: `subprocess_text_encodings` (function), lines 9661-9682, exports `subprocess_text_encodings`
- order 790: `decode_subprocess_bytes` (function), lines 9683-9709, exports `decode_subprocess_bytes`
- order 791: `run_subprocess_text` (function), lines 9710-9732, exports `run_subprocess_text`
- order 792: `windows_utf8_shell_command` (function), lines 9733-9739, exports `windows_utf8_shell_command`
- order 793: `shell_process_invocation` (function), lines 9740-9750, exports `shell_process_invocation`
- order 794: `join_shell_task_command` (function), lines 9751-9762, exports `join_shell_task_command`
- order 1056: `UserProcessManager` (class), lines 25352-25711, exports `UserProcessManager`

### `agent/tasks.py`

- order 1054: `TaskManager` (class), lines 25211-25345, exports `TaskManager`

### `agent/todo.py`

- order 1014: `TodoManager` (class), lines 18959-19385, exports `TodoManager`

### `agent/tools.py`

- order 1008: `_ask_user_option_rows` (function), lines 18783-18816, exports `_ask_user_option_rows`
- order 1009: `_ask_user_option_value` (function), lines 18817-18822, exports `_ask_user_option_value`
- order 1101: `tool_def` (function), lines 31337-31350, exports `tool_def`
- order 1106: `bash_operation_is_observation` (function), lines 31431-31434, exports `bash_operation_is_observation`
- order 1107: `bash_operation_is_marked_observation` (function), lines 31435-31439, exports `bash_operation_is_marked_observation`
- order 1108: `TOOLS` (constant), lines 31440-32031, exports `TOOLS`
- order 1109: `TOOL_REQUIRED_ARGS` (constant), lines 32032-32033, exports `TOOL_REQUIRED_ARGS`
- order 1110: `TOOL_SPEC_BY_NAME` (constant), lines 32034-32034, exports `TOOL_SPEC_BY_NAME`
- order 1111: `_for_32035` (statement), lines 32035-32044, exports `_tool`, `_fn`, `_name`, `_required`
- order 1112: `TOOL_NAME_FUZZY_MAP` (constant), lines 32045-32046, exports `TOOL_NAME_FUZZY_MAP`
- order 1113: `_for_32047` (statement), lines 32047-32050, exports `_name`, `_key`
- order 1114: `_for_32052` (statement), lines 32051-32068, exports `_alias`, `_target`
- order 1115: `is_todo_resume_tool_name` (function), lines 32069-32085, exports `is_todo_resume_tool_name`
- order 1116: `canonicalize_tool_name` (function), lines 32086-32104, exports `canonicalize_tool_name`
- order 1117: `filter_tool_specs_for_runtime` (function), lines 32105-32120, exports `filter_tool_specs_for_runtime`
- order 1118: `DEVELOPER_TOOL_DROP` (constant), lines 32121-32131, exports `DEVELOPER_TOOL_DROP`
- order 1119: `AGENT_TOOL_ALLOWLIST` (constant), lines 32132-32195, exports `AGENT_TOOL_ALLOWLIST`

### `agent/worktree.py`

- order 1059: `WorktreeManager` (class), lines 26404-26616, exports `WorktreeManager`

### `app/context.py`

- order 1259: `AppContext` (class), lines 125328-136866, exports `AppContext`

### `app/main.py`

- order 1275: `main` (function), lines 143884-145870, exports `main`
- order 1276: `_main_guard_145872` (main_guard), lines 145871-145873, exports —

### `app/services.py`

- order 1261: `TelemetryStore` (class), lines 136907-137297, exports `TelemetryStore`
- order 1262: `ApplicationRegistry` (class), lines 137298-138107, exports `ApplicationRegistry`

### `collaboration/core.py`

- order 94: `_now` (function), lines 1760-1763, exports `_now`
- order 95: `_json` (function), lines 1764-1767, exports `_json`
- order 96: `_load_json` (function), lines 1768-1774, exports `_load_json`
- order 97: `_b64_token` (function), lines 1775-1778, exports `_b64_token`
- order 98: `_branch_label` (function), lines 1779-1787, exports `_branch_label`
- order 99: `_digest` (function), lines 1788-1791, exports `_digest`
- order 100: `_password_hash` (function), lines 1792-1795, exports `_password_hash`
- order 101: `_normalize_ip` (function), lines 1796-1805, exports `_normalize_ip`
- order 102: `_normalize_name` (function), lines 1806-1812, exports `_normalize_name`
- order 103: `_COLLAB_PUBLIC_SECRET_PATTERNS` (assignment), lines 1813-1824, exports `_COLLAB_PUBLIC_SECRET_PATTERNS`
- order 104: `_collaboration_public_text` (function), lines 1825-1855, exports `_collaboration_public_text`
- order 105: `_collaboration_task_objective` (function), lines 1856-1880, exports `_collaboration_task_objective`
- order 106: `_collaboration_task_title` (function), lines 1881-1888, exports `_collaboration_task_title`
- order 107: `_collaboration_task_key` (function), lines 1889-1895, exports `_collaboration_task_key`
- order 108: `_collaboration_plan_steps` (function), lines 1896-1914, exports `_collaboration_plan_steps`
- order 109: `CollaborationError` (class), lines 1915-1922, exports `CollaborationError`
- order 110: `CollaborationPrincipal` (class), lines 1923-1933, exports `CollaborationPrincipal`
- order 111: `_normalize_operation` (function), lines 1934-1967, exports `_normalize_operation`
- order 112: `operation_input_length` (function), lines 1968-1971, exports `operation_input_length`
- order 113: `apply_text_operation` (function), lines 1972-1994, exports `apply_text_operation`
- order 114: `transform_text_operation` (function), lines 1995-2071, exports `transform_text_operation`
- order 115: `CollaborationStore` (class), lines 2072-4787, exports `CollaborationStore`
- order 116: `CollaborationWriteCoordinator` (class), lines 4788-5001, exports `CollaborationWriteCoordinator`

### `collaboration/watcher.py`

- order 1273: `collaboration_file_watcher_loop` (function), lines 143791-143865, exports `collaboration_file_watcher_loop`
- order 1274: `collaboration_watcher_health` (function), lines 143866-143883, exports `collaboration_watcher_health`

### `config/bootstrap.py`

- order 73: `_EMBEDDED_LIQUID_KERNEL_PACKAGE_B64` (assignment), lines 124-1593, exports `_EMBEDDED_LIQUID_KERNEL_PACKAGE_B64`
- order 74: `sync_embedded_liquid_kernel_bundle` (function), lines 1594-1617, exports `sync_embedded_liquid_kernel_bundle`
- order 75: `_ensure_embedded_liquid_kernel_package` (function), lines 1618-1710, exports `_ensure_embedded_liquid_kernel_package`
- order 78: `_ensure_liquid_kernel_sqlite_lifecycle` (function), lines 1719-1734, exports `_ensure_liquid_kernel_sqlite_lifecycle`
- order 968: `_liquid_kernel_history_present` (function), lines 16591-16595, exports `_liquid_kernel_history_present`
- order 969: `prepare_liquid_kernel_runtime` (function), lines 16596-16625, exports `prepare_liquid_kernel_runtime`
- order 970: `_persist_liquid_kernel_bootstrap` (function), lines 16626-16639, exports `_persist_liquid_kernel_bootstrap`

### `config/constants.py`

- order 76: `LIQUID_KERNEL_PACKAGE_STATUS` (constant), lines 1711-1712, exports `LIQUID_KERNEL_PACKAGE_STATUS`
- order 80: `_call_ensure_liquid_kernel_sqlite_lifecycle_1743` (expression), lines 1742-1743, exports —
- order 81: `COLLAB_DB_FILENAME` (constant), lines 1744-1747, exports `COLLAB_DB_FILENAME`
- order 82: `COLLAB_SESSION_TTL_SECONDS` (constant), lines 1748-1748, exports `COLLAB_SESSION_TTL_SECONDS`
- order 83: `COLLAB_PRESENCE_TTL_SECONDS` (constant), lines 1749-1749, exports `COLLAB_PRESENCE_TTL_SECONDS`
- order 84: `COLLAB_PASSWORD_ITERATIONS` (constant), lines 1750-1750, exports `COLLAB_PASSWORD_ITERATIONS`
- order 85: `COLLAB_MAX_AVATAR_BYTES` (constant), lines 1751-1751, exports `COLLAB_MAX_AVATAR_BYTES`
- order 86: `COLLAB_MAX_TEXT_BYTES` (constant), lines 1752-1752, exports `COLLAB_MAX_TEXT_BYTES`
- order 87: `COLLAB_DELETE_RETENTION_DAYS` (constant), lines 1753-1753, exports `COLLAB_DELETE_RETENTION_DAYS`
- order 88: `COLLAB_EVENT_RETENTION` (constant), lines 1754-1754, exports `COLLAB_EVENT_RETENTION`
- order 89: `COLLAB_AGENT_STALE_SECONDS` (constant), lines 1755-1755, exports `COLLAB_AGENT_STALE_SECONDS`
- order 90: `COLLAB_AGENT_HEARTBEAT_INTERVAL_SECONDS` (constant), lines 1756-1756, exports `COLLAB_AGENT_HEARTBEAT_INTERVAL_SECONDS`
- order 91: `COLLAB_EXTERNAL_WRITE_SETTLE_SECONDS` (constant), lines 1757-1757, exports `COLLAB_EXTERNAL_WRITE_SETTLE_SECONDS`
- order 92: `COLLAB_EXTERNAL_WRITE_CONFIRMATIONS` (constant), lines 1758-1758, exports `COLLAB_EXTERNAL_WRITE_CONFIRMATIONS`
- order 93: `COLLAB_SCHEMA_VERSION` (constant), lines 1759-1759, exports `COLLAB_SCHEMA_VERSION`
- order 117: `COLLAB_INDEX_HTML` (constant), lines 5002-5073, exports `COLLAB_INDEX_HTML`
- order 118: `COLLAB_CSS` (constant), lines 5074-5081, exports `COLLAB_CSS`
- order 119: `COLLAB_JS` (constant), lines 5082-5122, exports `COLLAB_JS`
- order 125: `APP_VERSION` (constant), lines 5144-5144, exports `APP_VERSION`
- order 134: `IDE_AUTH_FILENAME` (constant), lines 5153-5153, exports `IDE_AUTH_FILENAME`
- order 135: `IDE_AUTH_SESSION_TTL_SECONDS` (constant), lines 5154-5154, exports `IDE_AUTH_SESSION_TTL_SECONDS`
- order 136: `IDE_AUTH_MAX_ACTIVE_SESSIONS` (constant), lines 5155-5155, exports `IDE_AUTH_MAX_ACTIVE_SESSIONS`
- order 137: `IDE_DEVICE_SECRET_MIN_BYTES` (constant), lines 5156-5156, exports `IDE_DEVICE_SECRET_MIN_BYTES`
- order 138: `IDE_DEVICE_LABEL_MAX_CHARS` (constant), lines 5157-5157, exports `IDE_DEVICE_LABEL_MAX_CHARS`
- order 139: `IDE_DEVICE_PAIRING_TTL_SECONDS` (constant), lines 5158-5158, exports `IDE_DEVICE_PAIRING_TTL_SECONDS`
- order 140: `IDE_WORKBENCH_STATE_FILENAME` (constant), lines 5159-5159, exports `IDE_WORKBENCH_STATE_FILENAME`
- order 141: `IDE_PROMPT_ENHANCEMENT_BUDGETS` (constant), lines 5160-5197, exports `IDE_PROMPT_ENHANCEMENT_BUDGETS`
- order 142: `IDE_EXTENSIONS_DIRNAME` (constant), lines 5198-5198, exports `IDE_EXTENSIONS_DIRNAME`
- order 164: `LONG_OUTPUT_MODEL_PAGE_CHARS` (constant), lines 5501-5501, exports `LONG_OUTPUT_MODEL_PAGE_CHARS`
- order 165: `LONG_OUTPUT_UI_PAGE_CHARS` (constant), lines 5502-5502, exports `LONG_OUTPUT_UI_PAGE_CHARS`
- order 166: `LONG_OUTPUT_UI_PREVIEW_MAX_PAGES` (constant), lines 5503-5503, exports `LONG_OUTPUT_UI_PREVIEW_MAX_PAGES`
- order 167: `LONG_OUTPUT_LISTING_OFFLOAD_CHARS` (constant), lines 5504-5504, exports `LONG_OUTPUT_LISTING_OFFLOAD_CHARS`
- order 168: `LONG_OUTPUT_READ_PAGE_LINES` (constant), lines 5505-5505, exports `LONG_OUTPUT_READ_PAGE_LINES`
- order 169: `LONG_OUTPUT_READ_PAGE_MAX_CHARS` (constant), lines 5506-5506, exports `LONG_OUTPUT_READ_PAGE_MAX_CHARS`
- order 170: `LONG_OUTPUT_TEMP_MAX_FILES` (constant), lines 5507-5507, exports `LONG_OUTPUT_TEMP_MAX_FILES`
- order 171: `READ_FILE_DEFAULT_MAX_CHARS` (constant), lines 5508-5508, exports `READ_FILE_DEFAULT_MAX_CHARS`
- order 172: `READ_FILE_HARD_MAX_CHARS` (constant), lines 5509-5509, exports `READ_FILE_HARD_MAX_CHARS`
- order 173: `READ_FILE_OVERVIEW_HEAD_LINES` (constant), lines 5510-5510, exports `READ_FILE_OVERVIEW_HEAD_LINES`
- order 174: `READ_FILE_SEARCH_MAX_MATCHES` (constant), lines 5511-5511, exports `READ_FILE_SEARCH_MAX_MATCHES`
- order 179: `CODE_ADMIN_PORT_OFFSET` (constant), lines 5516-5516, exports `CODE_ADMIN_PORT_OFFSET`
- order 181: `IDE_PORT_OFFSET` (constant), lines 5518-5521, exports `IDE_PORT_OFFSET`
- order 182: `IDE_DEFAULT_PORT` (constant), lines 5522-5522, exports `IDE_DEFAULT_PORT`
- order 183: `COLLAB_PORT_OFFSET` (constant), lines 5523-5523, exports `COLLAB_PORT_OFFSET`
- order 185: `DEFAULT_WEB_SEARCH_ENABLED` (constant), lines 5525-5525, exports `DEFAULT_WEB_SEARCH_ENABLED`
- order 190: `DEFAULT_USER_MEMORY_MODE` (constant), lines 5530-5530, exports `DEFAULT_USER_MEMORY_MODE`
- order 198: `AGENT_WEB_SEARCH_USER_AGENT` (constant), lines 5541-5541, exports `AGENT_WEB_SEARCH_USER_AGENT`
- order 199: `AGENT_WEB_SEARCH_DEFAULT_MAX_RESULTS` (constant), lines 5542-5542, exports `AGENT_WEB_SEARCH_DEFAULT_MAX_RESULTS`
- order 200: `AGENT_WEB_SEARCH_DEFAULT_MAX_PAGES` (constant), lines 5543-5543, exports `AGENT_WEB_SEARCH_DEFAULT_MAX_PAGES`
- order 201: `AGENT_WEB_SEARCH_HARD_MAX_PAGES` (constant), lines 5544-5544, exports `AGENT_WEB_SEARCH_HARD_MAX_PAGES`
- order 202: `AGENT_WEB_SEARCH_DEFAULT_DEPTH` (constant), lines 5545-5545, exports `AGENT_WEB_SEARCH_DEFAULT_DEPTH`
- order 203: `AGENT_WEB_SEARCH_HARD_DEPTH` (constant), lines 5546-5546, exports `AGENT_WEB_SEARCH_HARD_DEPTH`
- order 204: `AGENT_WEB_SEARCH_FETCH_TIMEOUT` (constant), lines 5547-5547, exports `AGENT_WEB_SEARCH_FETCH_TIMEOUT`
- order 205: `AGENT_WEB_SEARCH_TOOL_SOFT_TIMEOUT` (constant), lines 5548-5548, exports `AGENT_WEB_SEARCH_TOOL_SOFT_TIMEOUT`
- order 206: `AGENT_WEB_SEARCH_MAX_PAGE_BYTES` (constant), lines 5549-5549, exports `AGENT_WEB_SEARCH_MAX_PAGE_BYTES`
- order 207: `AGENT_WEB_SEARCH_MAX_TEXT_CHARS` (constant), lines 5550-5550, exports `AGENT_WEB_SEARCH_MAX_TEXT_CHARS`
- order 208: `AGENT_WEB_SEARCH_PUBLIC_DISCOVERY_ENABLED` (constant), lines 5551-5553, exports `AGENT_WEB_SEARCH_PUBLIC_DISCOVERY_ENABLED`
- order 209: `AGENT_WEB_SEARCH_PUBLIC_FEED_URL` (constant), lines 5554-5554, exports `AGENT_WEB_SEARCH_PUBLIC_FEED_URL`
- order 210: `AGENT_WEB_SEARCH_PUBLIC_FEED_MAX_BYTES` (constant), lines 5555-5555, exports `AGENT_WEB_SEARCH_PUBLIC_FEED_MAX_BYTES`
- order 211: `AGENT_WEB_SEARCH_LOCAL_GRAPH_MAX_NODES` (constant), lines 5556-5556, exports `AGENT_WEB_SEARCH_LOCAL_GRAPH_MAX_NODES`
- order 212: `AGENT_WEB_SEARCH_LOCAL_GRAPH_MAX_EDGES` (constant), lines 5557-5557, exports `AGENT_WEB_SEARCH_LOCAL_GRAPH_MAX_EDGES`
- order 213: `AGENT_WEB_SEARCH_LOCAL_GRAPH_EDGE_SCAN_MULTIPLIER` (constant), lines 5558-5558, exports `AGENT_WEB_SEARCH_LOCAL_GRAPH_EDGE_SCAN_MULTIPLIER`
- order 214: `AGENT_WEB_SEARCH_LOCAL_GRAPH_PAGERANK_ITERATIONS` (constant), lines 5559-5559, exports `AGENT_WEB_SEARCH_LOCAL_GRAPH_PAGERANK_ITERATIONS`
- order 215: `AGENT_WEB_SEARCH_LOCAL_GRAPH_PAGERANK_DAMPING` (constant), lines 5560-5560, exports `AGENT_WEB_SEARCH_LOCAL_GRAPH_PAGERANK_DAMPING`
- order 216: `AGENT_WEB_SEARCH_LOCAL_GRAPH_AUTHORITY_BONUS_MAX` (constant), lines 5561-5561, exports `AGENT_WEB_SEARCH_LOCAL_GRAPH_AUTHORITY_BONUS_MAX`
- order 226: `CODE_CHUNK_CHARS` (constant), lines 5583-5583, exports `CODE_CHUNK_CHARS`
- order 227: `CODE_CHUNK_OVERLAP` (constant), lines 5584-5584, exports `CODE_CHUNK_OVERLAP`
- order 228: `CODE_MAX_CHUNKS_PER_DOC` (constant), lines 5585-5585, exports `CODE_MAX_CHUNKS_PER_DOC`
- order 229: `CODE_SOURCE_ANALYSIS_MAX_CHARS` (constant), lines 5586-5595, exports `CODE_SOURCE_ANALYSIS_MAX_CHARS`
- order 270: `CODE_IMPORT_WORKER_COUNT` (constant), lines 5664-5667, exports `CODE_IMPORT_WORKER_COUNT`
- order 272: `CODE_PARSE_TIMEOUT_SECONDS` (constant), lines 5672-5675, exports `CODE_PARSE_TIMEOUT_SECONDS`
- order 273: `DEFAULT_CONTEXT_TOKEN_LIMIT` (constant), lines 5676-5676, exports `DEFAULT_CONTEXT_TOKEN_LIMIT`
- order 274: `TOKEN_THRESHOLD` (constant), lines 5677-5677, exports `TOKEN_THRESHOLD`
- order 275: `CONTEXT_AUTO_COMPACT_RESERVE_RATIO` (constant), lines 5678-5681, exports `CONTEXT_AUTO_COMPACT_RESERVE_RATIO`
- order 276: `CONTEXT_ESTIMATE_SAFETY_MULTIPLIER` (constant), lines 5682-5685, exports `CONTEXT_ESTIMATE_SAFETY_MULTIPLIER`
- order 277: `CONTEXT_USAGE_CALIBRATION_MAX` (constant), lines 5686-5689, exports `CONTEXT_USAGE_CALIBRATION_MAX`
- order 278: `CONTEXT_ACTUAL_USAGE_RECENT_SECONDS` (constant), lines 5690-5693, exports `CONTEXT_ACTUAL_USAGE_RECENT_SECONDS`
- order 279: `LARGE_FILE_AUTO_PAGE_BYTES` (constant), lines 5694-5697, exports `LARGE_FILE_AUTO_PAGE_BYTES`
- order 280: `LARGE_FILE_AUTO_PAGE_LINES` (constant), lines 5698-5701, exports `LARGE_FILE_AUTO_PAGE_LINES`
- order 281: `LARGE_SOURCE_UPLOAD_EXCERPT_CHARS` (constant), lines 5702-5705, exports `LARGE_SOURCE_UPLOAD_EXCERPT_CHARS`
- order 282: `CHAT_UPLOAD_PARSE_QUEUE_MAX` (constant), lines 5706-5709, exports `CHAT_UPLOAD_PARSE_QUEUE_MAX`
- order 283: `CHAT_UPLOAD_PARSE_TIMEOUT_SECONDS` (constant), lines 5710-5713, exports `CHAT_UPLOAD_PARSE_TIMEOUT_SECONDS`
- order 284: `CHAT_UPLOAD_INLINE_TEXT_BYTES` (constant), lines 5714-5717, exports `CHAT_UPLOAD_INLINE_TEXT_BYTES`
- order 285: `CHAT_UPLOAD_PARSE_MAX_BYTES` (constant), lines 5718-5724, exports `CHAT_UPLOAD_PARSE_MAX_BYTES`
- order 286: `CHAT_UPLOAD_ZIP_ENTRY_MAX_BYTES` (constant), lines 5725-5731, exports `CHAT_UPLOAD_ZIP_ENTRY_MAX_BYTES`
- order 287: `CHAT_UPLOAD_TEXT_CONTEXT_CHARS` (constant), lines 5732-5735, exports `CHAT_UPLOAD_TEXT_CONTEXT_CHARS`
- order 288: `CHAT_UPLOAD_PROMPT_MAX_FILES` (constant), lines 5736-5739, exports `CHAT_UPLOAD_PROMPT_MAX_FILES`
- order 289: `CHAT_UPLOAD_PROMPT_MAX_CHARS` (constant), lines 5740-5743, exports `CHAT_UPLOAD_PROMPT_MAX_CHARS`
- order 290: `CHAT_UPLOAD_PROMPT_PER_FILE_CHARS` (constant), lines 5744-5747, exports `CHAT_UPLOAD_PROMPT_PER_FILE_CHARS`
- order 291: `CHAT_UPLOAD_FRONTEND_WAIT_MS` (constant), lines 5748-5751, exports `CHAT_UPLOAD_FRONTEND_WAIT_MS`
- order 292: `CHAT_UPLOAD_AUTO_LIBRARY_INGEST` (constant), lines 5752-5755, exports `CHAT_UPLOAD_AUTO_LIBRARY_INGEST`
- order 293: `CHAT_UPLOAD_INGEST_QUEUE_MAX` (constant), lines 5756-5759, exports `CHAT_UPLOAD_INGEST_QUEUE_MAX`
- order 294: `SESSION_SUBMIT_LOCK_TIMEOUT_SECONDS` (constant), lines 5760-5763, exports `SESSION_SUBMIT_LOCK_TIMEOUT_SECONDS`
- order 295: `SESSION_DEFERRED_START_QUEUE_MAX` (constant), lines 5764-5767, exports `SESSION_DEFERRED_START_QUEUE_MAX`
- order 296: `SESSION_SUBMISSION_DEDUPE_MAX` (constant), lines 5768-5768, exports `SESSION_SUBMISSION_DEDUPE_MAX`
- order 297: `SESSION_SUBMISSION_DEDUPE_SECONDS` (constant), lines 5769-5769, exports `SESSION_SUBMISSION_DEDUPE_SECONDS`
- order 298: `SCHEDULER_SUBMISSION_DEDUPE_MAX` (constant), lines 5770-5770, exports `SCHEDULER_SUBMISSION_DEDUPE_MAX`
- order 299: `FAST_START_LOCAL_CLASSIFICATION` (constant), lines 5771-5773, exports `FAST_START_LOCAL_CLASSIFICATION`
- order 300: `FAST_START_LOCAL_TITLE` (constant), lines 5774-5776, exports `FAST_START_LOCAL_TITLE`
- order 301: `AUTO_TITLE_MODEL_REFINE` (constant), lines 5777-5779, exports `AUTO_TITLE_MODEL_REFINE`
- order 302: `AUTO_TITLE_MODEL_TIMEOUT_SECONDS` (constant), lines 5780-5783, exports `AUTO_TITLE_MODEL_TIMEOUT_SECONDS`
- order 303: `AUTO_TITLE_MODEL_RETRY_COOLDOWN_SECONDS` (constant), lines 5784-5790, exports `AUTO_TITLE_MODEL_RETRY_COOLDOWN_SECONDS`
- order 304: `FAST_START_DEFER_CAPABILITY_PROBE` (constant), lines 5791-5793, exports `FAST_START_DEFER_CAPABILITY_PROBE`
- order 305: `SESSION_RUNTIME_MESSAGE_WINDOW` (constant), lines 5794-5794, exports `SESSION_RUNTIME_MESSAGE_WINDOW`
- order 306: `SESSION_RUNTIME_ACTIVITY_WINDOW` (constant), lines 5795-5795, exports `SESSION_RUNTIME_ACTIVITY_WINDOW`
- order 307: `SESSION_RUNTIME_OPERATION_WINDOW` (constant), lines 5796-5796, exports `SESSION_RUNTIME_OPERATION_WINDOW`
- order 308: `SESSION_RUNTIME_UPLOAD_WINDOW` (constant), lines 5797-5797, exports `SESSION_RUNTIME_UPLOAD_WINDOW`
- order 309: `LITE_SNAPSHOT_MAX_BYTES` (constant), lines 5798-5801, exports `LITE_SNAPSHOT_MAX_BYTES`
- order 310: `LITE_SNAPSHOT_MESSAGES_BYTES` (constant), lines 5802-5802, exports `LITE_SNAPSHOT_MESSAGES_BYTES`
- order 311: `LITE_SNAPSHOT_FEED_BYTES` (constant), lines 5803-5803, exports `LITE_SNAPSHOT_FEED_BYTES`
- order 312: `LITE_SNAPSHOT_OPERATIONS_BYTES` (constant), lines 5804-5804, exports `LITE_SNAPSHOT_OPERATIONS_BYTES`
- order 313: `IDE_AGENT_STATE_MAX_BYTES` (constant), lines 5805-5808, exports `IDE_AGENT_STATE_MAX_BYTES`
- order 314: `IDE_AGENT_FEED_BYTES` (constant), lines 5809-5809, exports `IDE_AGENT_FEED_BYTES`
- order 315: `IDE_AGENT_OPERATIONS_BYTES` (constant), lines 5810-5810, exports `IDE_AGENT_OPERATIONS_BYTES`
- order 316: `SESSION_WATCHDOG_INTERVAL_SECONDS` (constant), lines 5811-5814, exports `SESSION_WATCHDOG_INTERVAL_SECONDS`
- order 317: `SESSION_HEARTBEAT_STALE_SECONDS` (constant), lines 5815-5818, exports `SESSION_HEARTBEAT_STALE_SECONDS`
- order 318: `SESSION_LIST_DEFAULT_LIMIT` (constant), lines 5819-5822, exports `SESSION_LIST_DEFAULT_LIMIT`
- order 319: `SESSION_INDEX_SYNC_SNAPSHOT_MAX` (constant), lines 5823-5826, exports `SESSION_INDEX_SYNC_SNAPSHOT_MAX`
- order 320: `SESSION_INDEX_JOURNAL_COMPACT_RECORDS` (constant), lines 5827-5830, exports `SESSION_INDEX_JOURNAL_COMPACT_RECORDS`
- order 321: `SESSION_INDEX_JOURNAL_COMPACT_BYTES` (constant), lines 5831-5834, exports `SESSION_INDEX_JOURNAL_COMPACT_BYTES`
- order 322: `SESSION_CATALOG_RECENT_MAX` (constant), lines 5835-5838, exports `SESSION_CATALOG_RECENT_MAX`
- order 323: `IDE_SESSION_LIST_DEFAULT_LIMIT` (constant), lines 5839-5842, exports `IDE_SESSION_LIST_DEFAULT_LIMIT`
- order 324: `IDLE_TIMEOUT` (constant), lines 5843-5843, exports `IDLE_TIMEOUT`
- order 325: `POLL_INTERVAL` (constant), lines 5844-5844, exports `POLL_INTERVAL`
- order 326: `SSE_HEARTBEAT_SECONDS` (constant), lines 5845-5845, exports `SSE_HEARTBEAT_SECONDS`
- order 327: `MODEL_CALL_PROGRESS_DELAY` (constant), lines 5846-5846, exports `MODEL_CALL_PROGRESS_DELAY`
- order 328: `MODEL_CALL_PROGRESS_INTERVAL` (constant), lines 5847-5847, exports `MODEL_CALL_PROGRESS_INTERVAL`
- order 329: `RUN_COMPLETION_SUMMARY_ENABLED` (constant), lines 5848-5851, exports `RUN_COMPLETION_SUMMARY_ENABLED`
- order 330: `LLM_HTTP_RETRY_MAX_ATTEMPTS` (constant), lines 5852-5855, exports `LLM_HTTP_RETRY_MAX_ATTEMPTS`
- order 331: `LLM_HTTP_RETRY_DELAY_SECONDS` (constant), lines 5856-5859, exports `LLM_HTTP_RETRY_DELAY_SECONDS`
- order 332: `LLM_HTTP_RETRY_MAX_SECONDS` (constant), lines 5860-5863, exports `LLM_HTTP_RETRY_MAX_SECONDS`
- order 333: `LLM_HTTP_RETRY_404_ON_VLLM` (constant), lines 5864-5867, exports `LLM_HTTP_RETRY_404_ON_VLLM`
- order 334: `LLM_HTTP_RETRY_STATUSES` (constant), lines 5868-5868, exports `LLM_HTTP_RETRY_STATUSES`
- order 335: `MAX_AGENT_ROUNDS` (constant), lines 5869-5869, exports `MAX_AGENT_ROUNDS`
- order 336: `MIN_AGENT_ROUNDS` (constant), lines 5870-5870, exports `MIN_AGENT_ROUNDS`
- order 337: `MAX_AGENT_ROUNDS_CAP` (constant), lines 5871-5871, exports `MAX_AGENT_ROUNDS_CAP`
- order 338: `REPEATED_TOOL_LOOP_THRESHOLD` (constant), lines 5872-5872, exports `REPEATED_TOOL_LOOP_THRESHOLD`
- order 339: `BASH_READ_LOOP_THRESHOLD` (constant), lines 5873-5873, exports `BASH_READ_LOOP_THRESHOLD`
- order 340: `READ_FILE_LOOP_THRESHOLD` (constant), lines 5874-5874, exports `READ_FILE_LOOP_THRESHOLD`
- order 341: `READ_FILE_LOOP_DISTINCT_SOFT_LIMIT` (constant), lines 5875-5875, exports `READ_FILE_LOOP_DISTINCT_SOFT_LIMIT`
- order 342: `READ_FILE_COMPACT_PIN_DISTINCT` (constant), lines 5876-5876, exports `READ_FILE_COMPACT_PIN_DISTINCT`
- order 343: `READ_FILE_COMPACT_PIN_MAX_CHARS` (constant), lines 5877-5877, exports `READ_FILE_COMPACT_PIN_MAX_CHARS`
- order 344: `READ_FILE_PIN_TOTAL_CHARS` (constant), lines 5878-5880, exports `READ_FILE_PIN_TOTAL_CHARS`
- order 346: `READ_RESULT_PLACEHOLDER_PREFIXES` (constant), lines 5885-5894, exports `READ_RESULT_PLACEHOLDER_PREFIXES`
- order 347: `READ_CONTEXT_REGISTRY_MAX` (constant), lines 5895-5895, exports `READ_CONTEXT_REGISTRY_MAX`
- order 348: `READ_CONTEXT_PROMPT_MAX_ITEMS` (constant), lines 5896-5896, exports `READ_CONTEXT_PROMPT_MAX_ITEMS`
- order 349: `READ_CONTEXT_PROMPT_MAX_CHARS` (constant), lines 5897-5897, exports `READ_CONTEXT_PROMPT_MAX_CHARS`
- order 350: `READ_CONTEXT_SUMMARY_MAX_CHARS` (constant), lines 5898-5898, exports `READ_CONTEXT_SUMMARY_MAX_CHARS`
- order 351: `READ_CONTEXT_SHARED_MAX_ITEMS` (constant), lines 5899-5899, exports `READ_CONTEXT_SHARED_MAX_ITEMS`
- order 352: `READ_CONTEXT_POLICY_CHOICES` (constant), lines 5900-5900, exports `READ_CONTEXT_POLICY_CHOICES`
- order 353: `DEFAULT_READ_CONTEXT_POLICY` (constant), lines 5901-5901, exports `DEFAULT_READ_CONTEXT_POLICY`
- order 354: `READ_CONTEXT_CACHE_SEARCH_MAX_BYTES` (constant), lines 5902-5908, exports `READ_CONTEXT_CACHE_SEARCH_MAX_BYTES`
- order 355: `READ_CONTEXT_CACHE_SEARCH_MAX_MATCHES` (constant), lines 5909-5909, exports `READ_CONTEXT_CACHE_SEARCH_MAX_MATCHES`
- order 356: `READ_CONTEXT_CACHE_SNIPPET_CHARS` (constant), lines 5910-5910, exports `READ_CONTEXT_CACHE_SNIPPET_CHARS`
- order 357: `READ_CONTEXT_CACHE_LINE_CONTEXT` (constant), lines 5911-5911, exports `READ_CONTEXT_CACHE_LINE_CONTEXT`
- order 358: `LONG_CONTENT_SOURCE_CACHE_MAX_BYTES` (constant), lines 5912-5918, exports `LONG_CONTENT_SOURCE_CACHE_MAX_BYTES`
- order 359: `LONG_CONTENT_SOURCE_CACHE_MAX_FILES` (constant), lines 5919-5922, exports `LONG_CONTENT_SOURCE_CACHE_MAX_FILES`
- order 360: `LONG_CONTENT_SYMBOL_MEMORY_MAX` (constant), lines 5923-5926, exports `LONG_CONTENT_SYMBOL_MEMORY_MAX`
- order 361: `TOOL_MEMORY_REGISTRY_MAX` (constant), lines 5927-5927, exports `TOOL_MEMORY_REGISTRY_MAX`
- order 362: `TOOL_MEMORY_PROMPT_MAX_ITEMS` (constant), lines 5928-5928, exports `TOOL_MEMORY_PROMPT_MAX_ITEMS`
- order 363: `TOOL_MEMORY_PROMPT_MAX_CHARS` (constant), lines 5929-5929, exports `TOOL_MEMORY_PROMPT_MAX_CHARS`
- order 364: `TOOL_MEMORY_SUMMARY_MAX_CHARS` (constant), lines 5930-5930, exports `TOOL_MEMORY_SUMMARY_MAX_CHARS`
- order 365: `TOOL_MEMORY_SHARED_MAX_ITEMS` (constant), lines 5931-5931, exports `TOOL_MEMORY_SHARED_MAX_ITEMS`
- order 366: `TOOL_MEMORY_COMPACT_PIN_DISTINCT` (constant), lines 5932-5932, exports `TOOL_MEMORY_COMPACT_PIN_DISTINCT`
- order 367: `TOOL_MEMORY_COMPACT_PIN_MAX_CHARS` (constant), lines 5933-5933, exports `TOOL_MEMORY_COMPACT_PIN_MAX_CHARS`
- order 368: `TOOL_MEMORY_POLICY_CHOICES` (constant), lines 5934-5934, exports `TOOL_MEMORY_POLICY_CHOICES`
- order 369: `DEFAULT_TOOL_MEMORY_POLICY` (constant), lines 5935-5935, exports `DEFAULT_TOOL_MEMORY_POLICY`
- order 370: `LONG_CONTENT_MEMORY_VERSION` (constant), lines 5936-5948, exports `LONG_CONTENT_MEMORY_VERSION`
- order 371: `LONG_CONTENT_MEMORY_MAX_ITEMS` (constant), lines 5949-5952, exports `LONG_CONTENT_MEMORY_MAX_ITEMS`
- order 372: `LONG_CONTENT_MEMORY_MAX_SEGMENTS` (constant), lines 5953-5956, exports `LONG_CONTENT_MEMORY_MAX_SEGMENTS`
- order 373: `LONG_CONTENT_TEXT_SEGMENT_LINES` (constant), lines 5957-5960, exports `LONG_CONTENT_TEXT_SEGMENT_LINES`
- order 374: `LONG_CONTENT_CODE_SEGMENT_LINES` (constant), lines 5961-5964, exports `LONG_CONTENT_CODE_SEGMENT_LINES`
- order 375: `LONG_CONTENT_CARD_CHARS` (constant), lines 5965-5968, exports `LONG_CONTENT_CARD_CHARS`
- order 376: `LONG_CONTENT_STRUCTURE_MAX_CHARS` (constant), lines 5969-5972, exports `LONG_CONTENT_STRUCTURE_MAX_CHARS`
- order 377: `LONG_CONTENT_SEMANTIC_ENABLED` (constant), lines 5973-5980, exports `LONG_CONTENT_SEMANTIC_ENABLED`
- order 378: `LONG_CONTENT_SEMANTIC_TIMEOUT_SECONDS` (constant), lines 5981-5984, exports `LONG_CONTENT_SEMANTIC_TIMEOUT_SECONDS`
- order 379: `LONG_CONTENT_SEMANTIC_MAX_INPUT_CHARS` (constant), lines 5985-5988, exports `LONG_CONTENT_SEMANTIC_MAX_INPUT_CHARS`
- order 380: `LONG_CONTENT_SEMANTIC_MAX_OUTPUT_TOKENS` (constant), lines 5989-5992, exports `LONG_CONTENT_SEMANTIC_MAX_OUTPUT_TOKENS`
- order 381: `LONG_CONTENT_SEMANTIC_MAX_KEY_POINTS` (constant), lines 5993-5993, exports `LONG_CONTENT_SEMANTIC_MAX_KEY_POINTS`
- order 382: `LONG_CONTENT_SEMANTIC_MAX_DEFINITIONS` (constant), lines 5994-5994, exports `LONG_CONTENT_SEMANTIC_MAX_DEFINITIONS`
- order 383: `LONG_CONTENT_SEMANTIC_MAX_RELATIONS` (constant), lines 5995-5995, exports `LONG_CONTENT_SEMANTIC_MAX_RELATIONS`
- order 384: `LONG_CONTENT_SEMANTIC_MAX_UNCERTAINTIES` (constant), lines 5996-5996, exports `LONG_CONTENT_SEMANTIC_MAX_UNCERTAINTIES`
- order 385: `LONG_CONTENT_SEMANTIC_MAX_EVIDENCE` (constant), lines 5997-5997, exports `LONG_CONTENT_SEMANTIC_MAX_EVIDENCE`
- order 386: `LONG_CONTENT_SEMANTIC_MAX_NEXT_SEGMENTS` (constant), lines 5998-5998, exports `LONG_CONTENT_SEMANTIC_MAX_NEXT_SEGMENTS`
- order 387: `LONG_CONTENT_SEMANTIC_MAX_COVERED` (constant), lines 5999-5999, exports `LONG_CONTENT_SEMANTIC_MAX_COVERED`
- order 388: `LONG_CONTENT_SEMANTIC_MAX_OPEN_QUESTIONS` (constant), lines 6000-6000, exports `LONG_CONTENT_SEMANTIC_MAX_OPEN_QUESTIONS`
- order 389: `LONG_CONTENT_SEMANTIC_MAX_REFRESHES` (constant), lines 6001-6004, exports `LONG_CONTENT_SEMANTIC_MAX_REFRESHES`
- order 390: `LONG_CONTENT_OBSERVATION_MAX` (constant), lines 6005-6008, exports `LONG_CONTENT_OBSERVATION_MAX`
- order 391: `LONG_CONTENT_OBSERVATION_MAX_RANGES` (constant), lines 6009-6009, exports `LONG_CONTENT_OBSERVATION_MAX_RANGES`
- order 392: `LONG_CONTENT_OBSERVATION_MAX_EXCERPTS` (constant), lines 6010-6010, exports `LONG_CONTENT_OBSERVATION_MAX_EXCERPTS`
- order 393: `LONG_CONTENT_OBSERVATION_EXCERPT_CHARS` (constant), lines 6011-6011, exports `LONG_CONTENT_OBSERVATION_EXCERPT_CHARS`
- order 394: `LONG_CONTENT_RELATED_SOURCE_MAX` (constant), lines 6012-6012, exports `LONG_CONTENT_RELATED_SOURCE_MAX`
- order 395: `SHELL_SOURCE_CANDIDATE_MAX` (constant), lines 6013-6013, exports `SHELL_SOURCE_CANDIDATE_MAX`
- order 396: `LONG_CONTENT_TEXT_EXTS` (constant), lines 6014-6016, exports `LONG_CONTENT_TEXT_EXTS`
- order 397: `LONG_CONTENT_DATA_EXTS` (constant), lines 6017-6021, exports `LONG_CONTENT_DATA_EXTS`
- order 398: `DEFAULT_AUTO_TASK_LEVEL_CEILING` (constant), lines 6022-6022, exports `DEFAULT_AUTO_TASK_LEVEL_CEILING`
- order 404: `HARD_BREAK_TOOL_ERROR_THRESHOLD` (constant), lines 6042-6042, exports `HARD_BREAK_TOOL_ERROR_THRESHOLD`
- order 405: `HARD_BREAK_RECOVERY_ROUND_THRESHOLD` (constant), lines 6043-6045, exports `HARD_BREAK_RECOVERY_ROUND_THRESHOLD`
- order 406: `FUSED_FAULT_BREAK_THRESHOLD` (constant), lines 6046-6046, exports `FUSED_FAULT_BREAK_THRESHOLD`
- order 407: `STALL_SEVERITY_ESCALATION_THRESHOLD` (constant), lines 6047-6047, exports `STALL_SEVERITY_ESCALATION_THRESHOLD`
- order 408: `STALL_SEVERITY_WEIGHT_BASH_READ_LOOP` (constant), lines 6048-6048, exports `STALL_SEVERITY_WEIGHT_BASH_READ_LOOP`
- order 409: `STALL_SEVERITY_WEIGHT_REPEATED_TOOL` (constant), lines 6049-6049, exports `STALL_SEVERITY_WEIGHT_REPEATED_TOOL`
- order 410: `STALL_SEVERITY_WEIGHT_FAULT` (constant), lines 6050-6050, exports `STALL_SEVERITY_WEIGHT_FAULT`
- order 411: `STALL_SEVERITY_WEIGHT_RECOVERY_RETRY` (constant), lines 6051-6051, exports `STALL_SEVERITY_WEIGHT_RECOVERY_RETRY`
- order 412: `STALL_SEVERITY_WEIGHT_WATCHDOG` (constant), lines 6052-6052, exports `STALL_SEVERITY_WEIGHT_WATCHDOG`
- order 413: `STALL_SEVERITY_DECAY_ON_SUCCESS` (constant), lines 6053-6053, exports `STALL_SEVERITY_DECAY_ON_SUCCESS`
- order 414: `STALL_ESCALATION_MIN_LEVEL` (constant), lines 6054-6054, exports `STALL_ESCALATION_MIN_LEVEL`
- order 415: `STALL_PLAN_SYNTHESIS_MAX_TOKENS` (constant), lines 6055-6055, exports `STALL_PLAN_SYNTHESIS_MAX_TOKENS`
- order 416: `STALL_ESCALATION_CONTEXT_MAX_CHARS` (constant), lines 6056-6056, exports `STALL_ESCALATION_CONTEXT_MAX_CHARS`
- order 417: `MAX_RUN_SECONDS` (constant), lines 6057-6057, exports `MAX_RUN_SECONDS`
- order 418: `MIN_RUN_TIMEOUT_SECONDS` (constant), lines 6058-6058, exports `MIN_RUN_TIMEOUT_SECONDS`
- order 419: `MAX_RUN_TIMEOUT_SECONDS` (constant), lines 6059-6059, exports `MAX_RUN_TIMEOUT_SECONDS`
- order 420: `MIN_TIMEOUT_SECONDS` (constant), lines 6060-6060, exports `MIN_TIMEOUT_SECONDS`
- order 421: `MAX_TIMEOUT_SECONDS` (constant), lines 6061-6061, exports `MAX_TIMEOUT_SECONDS`
- order 422: `DEFAULT_TIMEOUT_SECONDS` (constant), lines 6062-6068, exports `DEFAULT_TIMEOUT_SECONDS`
- order 423: `DEFAULT_REQUEST_TIMEOUT` (constant), lines 6069-6069, exports `DEFAULT_REQUEST_TIMEOUT`
- order 424: `_SHELL_AUTO_CONFIRM_PATTERNS` (assignment), lines 6070-6085, exports `_SHELL_AUTO_CONFIRM_PATTERNS`
- order 425: `MIN_SHELL_COMMAND_TIMEOUT_SECONDS` (constant), lines 6086-6086, exports `MIN_SHELL_COMMAND_TIMEOUT_SECONDS`
- order 426: `MAX_SHELL_COMMAND_TIMEOUT_SECONDS` (constant), lines 6087-6087, exports `MAX_SHELL_COMMAND_TIMEOUT_SECONDS`
- order 427: `SHELL_TIMEOUT_MODES` (constant), lines 6088-6088, exports `SHELL_TIMEOUT_MODES`
- order 428: `_DEFAULT_SHELL_TIMEOUT_MODE_RAW` (assignment), lines 6089-6092, exports `_DEFAULT_SHELL_TIMEOUT_MODE_RAW`
- order 429: `DEFAULT_SHELL_TIMEOUT_MODE` (constant), lines 6093-6097, exports `DEFAULT_SHELL_TIMEOUT_MODE`
- order 430: `MIN_SHELL_ASYNC_HANDOFF_SECONDS` (constant), lines 6098-6098, exports `MIN_SHELL_ASYNC_HANDOFF_SECONDS`
- order 431: `MAX_SHELL_ASYNC_HANDOFF_SECONDS` (constant), lines 6099-6099, exports `MAX_SHELL_ASYNC_HANDOFF_SECONDS`
- order 432: `SHELL_FAILURE_GUIDANCE_SECONDS` (constant), lines 6100-6102, exports `SHELL_FAILURE_GUIDANCE_SECONDS`
- order 433: `DEFAULT_SHELL_ASYNC_HANDOFF_SECONDS` (constant), lines 6103-6117, exports `DEFAULT_SHELL_ASYNC_HANDOFF_SECONDS`
- order 434: `DEFAULT_SHELL_COMMAND_TIMEOUT_SECONDS` (constant), lines 6118-6132, exports `DEFAULT_SHELL_COMMAND_TIMEOUT_SECONDS`
- order 435: `DEFAULT_SINGLE_NO_PLAN_TODO_PROMPT` (constant), lines 6133-6147, exports `DEFAULT_SINGLE_NO_PLAN_TODO_PROMPT`
- order 436: `SINGLE_NO_PLAN_TODO_BOOTSTRAP_MAX_ATTEMPTS` (constant), lines 6148-6148, exports `SINGLE_NO_PLAN_TODO_BOOTSTRAP_MAX_ATTEMPTS`
- order 437: `AUTO_CONTINUE_BUDGET_DEFAULT` (constant), lines 6149-6149, exports `AUTO_CONTINUE_BUDGET_DEFAULT`
- order 438: `AGENT_MAX_OUTPUT_TOKENS` (constant), lines 6150-6150, exports `AGENT_MAX_OUTPUT_TOKENS`
- order 439: `OLLAMA_THINKING_TOOL_BUFFER` (constant), lines 6151-6151, exports `OLLAMA_THINKING_TOOL_BUFFER`
- order 440: `WATCHDOG_INTENT_NO_TOOL_THRESHOLD` (constant), lines 6152-6152, exports `WATCHDOG_INTENT_NO_TOOL_THRESHOLD`
- order 441: `WATCHDOG_REPEAT_NO_TOOL_THRESHOLD` (constant), lines 6153-6153, exports `WATCHDOG_REPEAT_NO_TOOL_THRESHOLD`
- order 442: `WATCHDOG_INTENT_NO_TOOL_THRESHOLD_SINGLE` (constant), lines 6154-6154, exports `WATCHDOG_INTENT_NO_TOOL_THRESHOLD_SINGLE`
- order 443: `WATCHDOG_REPEAT_NO_TOOL_THRESHOLD_SINGLE` (constant), lines 6155-6155, exports `WATCHDOG_REPEAT_NO_TOOL_THRESHOLD_SINGLE`
- order 444: `WATCHDOG_STATE_STALL_THRESHOLD` (constant), lines 6156-6156, exports `WATCHDOG_STATE_STALL_THRESHOLD`
- order 445: `WATCHDOG_CONTEXT_STALL_THRESHOLD` (constant), lines 6157-6157, exports `WATCHDOG_CONTEXT_STALL_THRESHOLD`
- order 446: `WATCHDOG_REPEAT_SIMILARITY_THRESHOLD` (constant), lines 6158-6158, exports `WATCHDOG_REPEAT_SIMILARITY_THRESHOLD`
- order 447: `WATCHDOG_CONTEXT_NEAR_RATIO` (constant), lines 6159-6159, exports `WATCHDOG_CONTEXT_NEAR_RATIO`
- order 448: `WATCHDOG_MAX_DECOMPOSE_STEPS` (constant), lines 6160-6160, exports `WATCHDOG_MAX_DECOMPOSE_STEPS`
- order 449: `WATCHDOG_STEP_MAX_ATTEMPTS` (constant), lines 6161-6161, exports `WATCHDOG_STEP_MAX_ATTEMPTS`
- order 450: `EMPTY_ACTION_MIN_CONTENT_CHARS` (constant), lines 6162-6162, exports `EMPTY_ACTION_MIN_CONTENT_CHARS`
- order 451: `EMPTY_ACTION_WAKEUP_RETRY_LIMIT` (constant), lines 6163-6163, exports `EMPTY_ACTION_WAKEUP_RETRY_LIMIT`
- order 452: `EMPTY_ACTION_INTERVENTION_THRESHOLD` (constant), lines 6164-6170, exports `EMPTY_ACTION_INTERVENTION_THRESHOLD`
- order 453: `EMPTY_ACTION_BOOTSTRAP_THINKING_GRACE_ROUNDS` (constant), lines 6171-6175, exports `EMPTY_ACTION_BOOTSTRAP_THINKING_GRACE_ROUNDS`
- order 454: `EMPTY_ACTION_RECOVERY_MAX_TOKENS` (constant), lines 6176-6176, exports `EMPTY_ACTION_RECOVERY_MAX_TOKENS`
- order 455: `THINKING_BUDGET_FORCE_RATIO` (constant), lines 6177-6177, exports `THINKING_BUDGET_FORCE_RATIO`
- order 456: `_TOOL_TIMEOUT_MAP` (assignment), lines 6178-6199, exports `_TOOL_TIMEOUT_MAP`
- order 457: `_DEFAULT_TOOL_TIMEOUT` (assignment), lines 6200-6200, exports `_DEFAULT_TOOL_TIMEOUT`
- order 460: `CONVERSATION_VISIBLE_TOOL_EVENTS` (constant), lines 6206-6218, exports `CONVERSATION_VISIBLE_TOOL_EVENTS`
- order 461: `PERSIST_ON_EVENT_TYPES` (constant), lines 6219-6237, exports `PERSIST_ON_EVENT_TYPES`
- order 462: `PERSIST_EVENT_MIN_INTERVAL_SECONDS` (constant), lines 6238-6238, exports `PERSIST_EVENT_MIN_INTERVAL_SECONDS`
- order 463: `TRUNCATION_CONTINUATION_MAX_PASSES` (constant), lines 6239-6239, exports `TRUNCATION_CONTINUATION_MAX_PASSES`
- order 464: `TRUNCATION_CONTINUATION_MAX_TOKENS` (constant), lines 6240-6240, exports `TRUNCATION_CONTINUATION_MAX_TOKENS`
- order 465: `TRUNCATION_CONTINUATION_TAIL_CHARS` (constant), lines 6241-6241, exports `TRUNCATION_CONTINUATION_TAIL_CHARS`
- order 466: `TRUNCATION_CONTINUATION_ECHO_CHARS` (constant), lines 6242-6242, exports `TRUNCATION_CONTINUATION_ECHO_CHARS`
- order 467: `TRUNCATION_OVERLAP_SCAN_CHARS` (constant), lines 6243-6243, exports `TRUNCATION_OVERLAP_SCAN_CHARS`
- order 468: `TRUNCATION_PAIR_SCAN_CHARS` (constant), lines 6244-6244, exports `TRUNCATION_PAIR_SCAN_CHARS`
- order 469: `TRUNCATION_LIVE_BUFFER_MAX_CHARS` (constant), lines 6245-6245, exports `TRUNCATION_LIVE_BUFFER_MAX_CHARS`
- order 470: `MIN_CONTEXT_TOKEN_LIMIT` (constant), lines 6246-6246, exports `MIN_CONTEXT_TOKEN_LIMIT`
- order 471: `COMPACT_TIER1_PCT` (constant), lines 6247-6248, exports `COMPACT_TIER1_PCT`
- order 472: `COMPACT_TIER2_PCT` (constant), lines 6249-6249, exports `COMPACT_TIER2_PCT`
- order 473: `COMPACT_TIER3_PCT` (constant), lines 6250-6250, exports `COMPACT_TIER3_PCT`
- order 474: `COMPACT_TIER1_ABS` (constant), lines 6251-6252, exports `COMPACT_TIER1_ABS`
- order 475: `COMPACT_TIER2_ABS` (constant), lines 6253-6253, exports `COMPACT_TIER2_ABS`
- order 476: `CONTEXT_COMPACT_INEFFECTIVE_COOLDOWN_SECONDS` (constant), lines 6254-6260, exports `CONTEXT_COMPACT_INEFFECTIVE_COOLDOWN_SECONDS`
- order 477: `FILE_BUFFER_CONTENT_THRESHOLD` (constant), lines 6261-6262, exports `FILE_BUFFER_CONTENT_THRESHOLD`
- order 478: `FILE_BUFFER_MAX_FILES` (constant), lines 6263-6263, exports `FILE_BUFFER_MAX_FILES`
- order 479: `AUTHORITATIVE_USER_GOAL_OPEN` (constant), lines 6264-6264, exports `AUTHORITATIVE_USER_GOAL_OPEN`
- order 480: `AUTHORITATIVE_USER_GOAL_CLOSE` (constant), lines 6265-6265, exports `AUTHORITATIVE_USER_GOAL_CLOSE`
- order 481: `AGENT_MSG_LIMIT_TIER0` (constant), lines 6266-6267, exports `AGENT_MSG_LIMIT_TIER0`
- order 482: `AGENT_MSG_LIMIT_TIER1` (constant), lines 6268-6268, exports `AGENT_MSG_LIMIT_TIER1`
- order 483: `AGENT_MSG_LIMIT_TIER2` (constant), lines 6269-6269, exports `AGENT_MSG_LIMIT_TIER2`
- order 484: `AGENT_MSG_LIMIT_TIER3` (constant), lines 6270-6270, exports `AGENT_MSG_LIMIT_TIER3`
- order 485: `AGENT_CTX_LIMIT_TIER0` (constant), lines 6271-6271, exports `AGENT_CTX_LIMIT_TIER0`
- order 486: `AGENT_CTX_LIMIT_TIER1` (constant), lines 6272-6272, exports `AGENT_CTX_LIMIT_TIER1`
- order 487: `AGENT_CTX_LIMIT_TIER2` (constant), lines 6273-6273, exports `AGENT_CTX_LIMIT_TIER2`
- order 488: `AGENT_CTX_LIMIT_TIER3` (constant), lines 6274-6274, exports `AGENT_CTX_LIMIT_TIER3`
- order 489: `MANAGER_CTX_LIMIT_TIER0` (constant), lines 6275-6275, exports `MANAGER_CTX_LIMIT_TIER0`
- order 490: `MANAGER_CTX_LIMIT_TIER1` (constant), lines 6276-6276, exports `MANAGER_CTX_LIMIT_TIER1`
- order 491: `MANAGER_CTX_LIMIT_TIER2` (constant), lines 6277-6277, exports `MANAGER_CTX_LIMIT_TIER2`
- order 492: `MANAGER_CTX_LIMIT_TIER3` (constant), lines 6278-6278, exports `MANAGER_CTX_LIMIT_TIER3`
- order 493: `MAX_CONTEXT_ARCHIVE_SEGMENTS` (constant), lines 6279-6279, exports `MAX_CONTEXT_ARCHIVE_SEGMENTS`
- order 494: `MAX_USER_BUBBLE_LOG` (constant), lines 6280-6281, exports `MAX_USER_BUBBLE_LOG`
- order 495: `MANAGER_INSTRUCTION_MAX_CHARS` (constant), lines 6282-6286, exports `MANAGER_INSTRUCTION_MAX_CHARS`
- order 496: `MANAGER_MOMENTUM_MAX_SKIPS` (constant), lines 6287-6292, exports `MANAGER_MOMENTUM_MAX_SKIPS`
- order 497: `MODEL_OUTPUT_RETRY_TIMES` (constant), lines 6293-6297, exports `MODEL_OUTPUT_RETRY_TIMES`
- order 498: `ARBITER_TRIGGER_MIN_CONTENT_CHARS` (constant), lines 6298-6298, exports `ARBITER_TRIGGER_MIN_CONTENT_CHARS`
- order 499: `ARBITER_VALID_PLANNING_STREAK_LIMIT` (constant), lines 6299-6299, exports `ARBITER_VALID_PLANNING_STREAK_LIMIT`
- order 500: `ARBITER_DEFAULT_TIMEOUT_SECONDS` (constant), lines 6300-6300, exports `ARBITER_DEFAULT_TIMEOUT_SECONDS`
- order 501: `ARBITER_DEFAULT_MAX_TOKENS` (constant), lines 6301-6301, exports `ARBITER_DEFAULT_MAX_TOKENS`
- order 502: `ARBITER_DEFAULT_TEMPERATURE` (constant), lines 6302-6302, exports `ARBITER_DEFAULT_TEMPERATURE`
- order 503: `LIVE_INPUT_DELAY_WRITE_ROUNDS` (constant), lines 6303-6303, exports `LIVE_INPUT_DELAY_WRITE_ROUNDS`
- order 504: `LIVE_INPUT_DELAY_TOOL_ROUNDS` (constant), lines 6304-6304, exports `LIVE_INPUT_DELAY_TOOL_ROUNDS`
- order 505: `LIVE_INPUT_DELAY_NORMAL_ROUNDS` (constant), lines 6305-6305, exports `LIVE_INPUT_DELAY_NORMAL_ROUNDS`
- order 506: `LIVE_INPUT_MAX_INJECTIONS` (constant), lines 6306-6306, exports `LIVE_INPUT_MAX_INJECTIONS`
- order 507: `LIVE_INPUT_REINJECT_INTERVAL` (constant), lines 6307-6307, exports `LIVE_INPUT_REINJECT_INTERVAL`
- order 508: `LIVE_INPUT_WEIGHT_BASE_DELAYED` (constant), lines 6308-6308, exports `LIVE_INPUT_WEIGHT_BASE_DELAYED`
- order 509: `LIVE_INPUT_WEIGHT_BASE_NORMAL` (constant), lines 6309-6309, exports `LIVE_INPUT_WEIGHT_BASE_NORMAL`
- order 510: `LIVE_INPUT_WEIGHT_STEP_DELAYED` (constant), lines 6310-6310, exports `LIVE_INPUT_WEIGHT_STEP_DELAYED`
- order 511: `LIVE_INPUT_WEIGHT_STEP_NORMAL` (constant), lines 6311-6311, exports `LIVE_INPUT_WEIGHT_STEP_NORMAL`
- order 513: `BENIGN_SOCKET_DEBUG_LOG_ENABLED` (constant), lines 6318-6324, exports `BENIGN_SOCKET_DEBUG_LOG_ENABLED`
- order 514: `BENIGN_SOCKET_LOG_INTERVAL_SECONDS` (constant), lines 6325-6325, exports `BENIGN_SOCKET_LOG_INTERVAL_SECONDS`
- order 515: `FINAL_SUMMARY_MIN_CHARS` (constant), lines 6326-6326, exports `FINAL_SUMMARY_MIN_CHARS`
- order 516: `FINAL_SUMMARY_STRICT_MIN_CHARS` (constant), lines 6327-6327, exports `FINAL_SUMMARY_STRICT_MIN_CHARS`
- order 517: `RUNTIME_CONTROL_HINT_PREFIXES` (constant), lines 6328-6349, exports `RUNTIME_CONTROL_HINT_PREFIXES`
- order 518: `UI_HIDDEN_RUNTIME_CONTROL_PREFIXES` (constant), lines 6350-6378, exports `UI_HIDDEN_RUNTIME_CONTROL_PREFIXES`
- order 519: `UI_PROJECTED_RUNTIME_CONTROL_TAGS` (constant), lines 6379-6401, exports `UI_PROJECTED_RUNTIME_CONTROL_TAGS`
- order 520: `UI_LEGACY_PROJECTED_RUNTIME_CONTROL_TAGS` (constant), lines 6402-6404, exports `UI_LEGACY_PROJECTED_RUNTIME_CONTROL_TAGS`
- order 521: `RETRY_RUNTIME_HINT_PREFIXES` (constant), lines 6405-6419, exports `RETRY_RUNTIME_HINT_PREFIXES`
- order 522: `EXECUTION_MODE_SINGLE` (constant), lines 6420-6420, exports `EXECUTION_MODE_SINGLE`
- order 523: `EXECUTION_MODE_SEQUENTIAL` (constant), lines 6421-6421, exports `EXECUTION_MODE_SEQUENTIAL`
- order 524: `EXECUTION_MODE_SYNC` (constant), lines 6422-6422, exports `EXECUTION_MODE_SYNC`
- order 525: `EXECUTION_MODE_CHOICES` (constant), lines 6423-6427, exports `EXECUTION_MODE_CHOICES`
- order 526: `AGENT_ROLES` (constant), lines 6428-6428, exports `AGENT_ROLES`
- order 527: `AGENT_BUBBLE_ROLES` (constant), lines 6429-6429, exports `AGENT_BUBBLE_ROLES`
- order 528: `AGENT_ROLE_LABELS` (constant), lines 6430-6436, exports `AGENT_ROLE_LABELS`
- order 529: `AGENT_ROLE_BUBBLE_COLORS` (constant), lines 6437-6443, exports `AGENT_ROLE_BUBBLE_COLORS`
- order 530: `BLACKBOARD_STATUSES` (constant), lines 6444-6453, exports `BLACKBOARD_STATUSES`
- order 531: `TASK_COMPLEXITY_LEVELS` (constant), lines 6454-6454, exports `TASK_COMPLEXITY_LEVELS`
- order 532: `TASK_COMPLEXITY_RANKS` (constant), lines 6455-6460, exports `TASK_COMPLEXITY_RANKS`
- order 533: `TASK_PROFILE_TYPES` (constant), lines 6461-6467, exports `TASK_PROFILE_TYPES`
- order 534: `TASK_LEVEL_CHOICES` (constant), lines 6468-6468, exports `TASK_LEVEL_CHOICES`
- order 535: `TASK_SCALE_PREFERENCES` (constant), lines 6469-6469, exports `TASK_SCALE_PREFERENCES`
- order 536: `SEMANTIC_CONFIDENCE_CHOICES` (constant), lines 6470-6470, exports `SEMANTIC_CONFIDENCE_CHOICES`
- order 537: `L2_TODO_POLICY_CHOICES` (constant), lines 6471-6475, exports `L2_TODO_POLICY_CHOICES`
- order 538: `DEFAULT_L2_TODO_POLICY` (constant), lines 6476-6476, exports `DEFAULT_L2_TODO_POLICY`
- order 539: `TASK_LEVEL_POLICIES` (constant), lines 6477-6530, exports `TASK_LEVEL_POLICIES`
- order 540: `MANAGER_ROUTE_TARGETS` (constant), lines 6531-6531, exports `MANAGER_ROUTE_TARGETS`
- order 541: `BLACKBOARD_MAX_LOG_ENTRIES` (constant), lines 6532-6532, exports `BLACKBOARD_MAX_LOG_ENTRIES`
- order 542: `BLACKBOARD_MAX_TEXT` (constant), lines 6533-6533, exports `BLACKBOARD_MAX_TEXT`
- order 543: `BLACKBOARD_MEMORY_SHORT_MAX` (constant), lines 6534-6534, exports `BLACKBOARD_MEMORY_SHORT_MAX`
- order 544: `BLACKBOARD_MEMORY_MID_MAX_STEPS` (constant), lines 6535-6535, exports `BLACKBOARD_MEMORY_MID_MAX_STEPS`
- order 545: `BLACKBOARD_MEMORY_MID_ITEMS_PER_STEP` (constant), lines 6536-6536, exports `BLACKBOARD_MEMORY_MID_ITEMS_PER_STEP`
- order 546: `BLACKBOARD_MEMORY_LONG_MAX` (constant), lines 6537-6537, exports `BLACKBOARD_MEMORY_LONG_MAX`
- order 547: `BLACKBOARD_MEMORY_INDEX_MAX` (constant), lines 6538-6538, exports `BLACKBOARD_MEMORY_INDEX_MAX`
- order 548: `SKILL_REFRESH_MIN_INTERVAL_SECONDS` (constant), lines 6539-6539, exports `SKILL_REFRESH_MIN_INTERVAL_SECONDS`
- order 553: `SKILL_RECALL_CACHE_TTL_SECONDS` (constant), lines 6550-6550, exports `SKILL_RECALL_CACHE_TTL_SECONDS`
- order 554: `SKILL_RECALL_CACHE_MAX_ENTRIES` (constant), lines 6551-6551, exports `SKILL_RECALL_CACHE_MAX_ENTRIES`
- order 555: `SKILL_RECALL_GENERIC_TOKENS` (constant), lines 6552-6558, exports `SKILL_RECALL_GENERIC_TOKENS`
- order 557: `SKILL_CATALOG_FULL_REFRESH_SECONDS` (constant), lines 6580-6583, exports `SKILL_CATALOG_FULL_REFRESH_SECONDS`
- order 558: `SKILL_PROMPT_MAX_ITEMS` (constant), lines 6584-6584, exports `SKILL_PROMPT_MAX_ITEMS`
- order 559: `SKILL_PROMPT_MAX_CHARS` (constant), lines 6585-6585, exports `SKILL_PROMPT_MAX_CHARS`
- order 560: `SKILL_RUNTIME_CACHE_MAX_ENTRIES` (constant), lines 6586-6586, exports `SKILL_RUNTIME_CACHE_MAX_ENTRIES`
- order 561: `SKILL_RUNTIME_CACHE_MAX_BYTES` (constant), lines 6587-6587, exports `SKILL_RUNTIME_CACHE_MAX_BYTES`
- order 562: `SKILL_AUTOLOAD_SCORE_THRESHOLD` (constant), lines 6588-6591, exports `SKILL_AUTOLOAD_SCORE_THRESHOLD`
- order 563: `SKILL_AUTOLOAD_CONFIDENCE_THRESHOLD` (constant), lines 6592-6592, exports `SKILL_AUTOLOAD_CONFIDENCE_THRESHOLD`
- order 564: `SKILL_RUNTIME_EVALUATION_TTL_SECONDS` (constant), lines 6593-6593, exports `SKILL_RUNTIME_EVALUATION_TTL_SECONDS`
- order 565: `SKILL_RUNTIME_EVALUATION_TIMEOUT_SECONDS` (constant), lines 6594-6594, exports `SKILL_RUNTIME_EVALUATION_TIMEOUT_SECONDS`
- order 566: `ACCEPTANCE_VERIFY_TIMEOUT_SECONDS` (constant), lines 6595-6600, exports `ACCEPTANCE_VERIFY_TIMEOUT_SECONDS`
- order 567: `SKILL_RUNTIME_UNLOAD_CONFIDENCE_THRESHOLD` (constant), lines 6601-6601, exports `SKILL_RUNTIME_UNLOAD_CONFIDENCE_THRESHOLD`
- order 568: `SKILL_RUNTIME_KEY_TOOL_INTERVAL` (constant), lines 6602-6602, exports `SKILL_RUNTIME_KEY_TOOL_INTERVAL`
- order 569: `SKILL_RUNTIME_EVENTS_MAX` (constant), lines 6603-6603, exports `SKILL_RUNTIME_EVENTS_MAX`
- order 570: `SKILL_METADATA_CAPSULE_MAX_CHARS` (constant), lines 6604-6604, exports `SKILL_METADATA_CAPSULE_MAX_CHARS`
- order 571: `SKILL_DEPENDENCY_MAX_DEPTH` (constant), lines 6605-6605, exports `SKILL_DEPENDENCY_MAX_DEPTH`
- order 572: `AUTO_SKILLS_ROOT_CANDIDATES` (constant), lines 6606-6606, exports `AUTO_SKILLS_ROOT_CANDIDATES`
- order 573: `SKILL_DEFAULT_ATTACHMENT_GLOBS` (constant), lines 6607-6637, exports `SKILL_DEFAULT_ATTACHMENT_GLOBS`
- order 574: `SKILL_INLINE_ATTACHMENT_MAX_FILES` (constant), lines 6638-6638, exports `SKILL_INLINE_ATTACHMENT_MAX_FILES`
- order 575: `SKILL_INLINE_ATTACHMENT_MAX_CHARS` (constant), lines 6639-6639, exports `SKILL_INLINE_ATTACHMENT_MAX_CHARS`
- order 576: `SKILL_RESOURCE_MANIFEST_MAX_ITEMS` (constant), lines 6640-6640, exports `SKILL_RESOURCE_MANIFEST_MAX_ITEMS`
- order 577: `SKILL_BODY_COMPACT_THRESHOLD_CHARS` (constant), lines 6641-6641, exports `SKILL_BODY_COMPACT_THRESHOLD_CHARS`
- order 578: `SKILL_BODY_PREVIEW_CHARS` (constant), lines 6642-6642, exports `SKILL_BODY_PREVIEW_CHARS`
- order 579: `SKILLS_VIRTUAL_PREFIX` (constant), lines 6643-6643, exports `SKILLS_VIRTUAL_PREFIX`
- order 580: `SKILLS_EXTERNAL_MOUNT` (constant), lines 6644-6644, exports `SKILLS_EXTERNAL_MOUNT`
- order 581: `PLAN_MODE_ENABLED_LEVELS` (constant), lines 6645-6645, exports `PLAN_MODE_ENABLED_LEVELS`
- order 582: `PLAN_MODE_FORCED_LEVELS` (constant), lines 6646-6646, exports `PLAN_MODE_FORCED_LEVELS`
- order 583: `PLAN_MODE_USER_CHOICES` (constant), lines 6647-6647, exports `PLAN_MODE_USER_CHOICES`
- order 584: `TASK_PHASES` (constant), lines 6648-6649, exports `TASK_PHASES`
- order 585: `TASK_PHASE_ROUTING` (constant), lines 6650-6657, exports `TASK_PHASE_ROUTING`
- order 586: `COMPLEXITY_KEYWORDS` (constant), lines 6658-6664, exports `COMPLEXITY_KEYWORDS`
- order 587: `USER_COMPLEXITY_SIMPLE_TOKENS` (constant), lines 6665-6669, exports `USER_COMPLEXITY_SIMPLE_TOKENS`
- order 588: `USER_COMPLEXITY_MODERATE_TOKENS` (constant), lines 6670-6674, exports `USER_COMPLEXITY_MODERATE_TOKENS`
- order 589: `USER_COMPLEXITY_COMPLEX_TOKENS` (constant), lines 6675-6679, exports `USER_COMPLEXITY_COMPLEX_TOKENS`
- order 590: `USER_COMPLEXITY_EXPERT_TOKENS` (constant), lines 6680-6684, exports `USER_COMPLEXITY_EXPERT_TOKENS`
- order 591: `PLAN_MODE_EXPLORER_MAX_ROUNDS` (constant), lines 6685-6688, exports `PLAN_MODE_EXPLORER_MAX_ROUNDS`
- order 592: `PLAN_MODE_EXPLORER_PRODUCTIVE_ROUNDS` (constant), lines 6689-6689, exports `PLAN_MODE_EXPLORER_PRODUCTIVE_ROUNDS`
- order 593: `PLAN_MODE_EXPLORER_STALE_ROUNDS` (constant), lines 6690-6690, exports `PLAN_MODE_EXPLORER_STALE_ROUNDS`
- order 594: `PLAN_MODE_SYNTHESIS_MAX_ATTEMPTS` (constant), lines 6691-6691, exports `PLAN_MODE_SYNTHESIS_MAX_ATTEMPTS`
- order 595: `REVIEWER_DEBUG_MODE_MAX_ROUNDS` (constant), lines 6692-6693, exports `REVIEWER_DEBUG_MODE_MAX_ROUNDS`
- order 596: `REVIEWER_DEBUG_TOOL_ALLOWLIST` (constant), lines 6694-6699, exports `REVIEWER_DEBUG_TOOL_ALLOWLIST`
- order 597: `EXPLORER_STALL_THRESHOLD` (constant), lines 6700-6700, exports `EXPLORER_STALL_THRESHOLD`
- order 598: `DEVELOPER_EDIT_STALL_THRESHOLD` (constant), lines 6701-6701, exports `DEVELOPER_EDIT_STALL_THRESHOLD`
- order 599: `ACCEPTANCE_GATE_STALL_THRESHOLD` (constant), lines 6702-6705, exports `ACCEPTANCE_GATE_STALL_THRESHOLD`
- order 600: `ACCEPTANCE_GATE_HARD_CEILING` (constant), lines 6706-6709, exports `ACCEPTANCE_GATE_HARD_CEILING`
- order 601: `ACCEPTANCE_GATE_TOTAL_ROUND_CEILING` (constant), lines 6710-6710, exports `ACCEPTANCE_GATE_TOTAL_ROUND_CEILING`
- order 602: `PLAN_MODE_MANAGER_SYNTHESIS_MAX_TOKENS` (constant), lines 6711-6711, exports `PLAN_MODE_MANAGER_SYNTHESIS_MAX_TOKENS`
- order 603: `PLAN_MODE_MAX_OPTIONS` (constant), lines 6712-6712, exports `PLAN_MODE_MAX_OPTIONS`
- order 604: `PLAN_FILE_RELATIVE_PATH` (constant), lines 6713-6713, exports `PLAN_FILE_RELATIVE_PATH`
- order 605: `PLAN_BUBBLE_MAX_CHARS` (constant), lines 6714-6714, exports `PLAN_BUBBLE_MAX_CHARS`
- order 606: `PLAN_NOTICE_BODY_MAX_CHARS` (constant), lines 6715-6715, exports `PLAN_NOTICE_BODY_MAX_CHARS`
- order 607: `PLAN_MESSAGE_EVENT_MAX_CHARS` (constant), lines 6716-6716, exports `PLAN_MESSAGE_EVENT_MAX_CHARS`
- order 608: `PLAN_STEP_FULL_CONTENT_MAX_CHARS` (constant), lines 6717-6717, exports `PLAN_STEP_FULL_CONTENT_MAX_CHARS`
- order 609: `PLAN_MODE_RESEARCH_TOOL_ALLOWLIST` (constant), lines 6718-6725, exports `PLAN_MODE_RESEARCH_TOOL_ALLOWLIST`
- order 610: `FAILURE_LEDGER_MAX_FIXES` (constant), lines 6726-6726, exports `FAILURE_LEDGER_MAX_FIXES`
- order 611: `FAILURE_LEDGER_MAX_COMPILE_ERRORS` (constant), lines 6727-6727, exports `FAILURE_LEDGER_MAX_COMPILE_ERRORS`
- order 612: `FAILURE_LEDGER_MAX_DELEGATIONS` (constant), lines 6728-6728, exports `FAILURE_LEDGER_MAX_DELEGATIONS`
- order 613: `FAILURE_LEDGER_MAX_STALLS` (constant), lines 6729-6729, exports `FAILURE_LEDGER_MAX_STALLS`
- order 614: `FAILURE_LEDGER_MAX_TOOL_FPS` (constant), lines 6730-6730, exports `FAILURE_LEDGER_MAX_TOOL_FPS`
- order 615: `FAILURE_LEDGER_MAX_ERRORS` (constant), lines 6731-6731, exports `FAILURE_LEDGER_MAX_ERRORS`
- order 616: `ERROR_CATEGORY_DEFS` (constant), lines 6732-6771, exports `ERROR_CATEGORY_DEFS`
- order 617: `CHECKPOINT_MAX_COUNT` (constant), lines 6772-6772, exports `CHECKPOINT_MAX_COUNT`
- order 618: `CHECKPOINT_INTERVAL_ROUNDS` (constant), lines 6773-6773, exports `CHECKPOINT_INTERVAL_ROUNDS`
- order 619: `PERSISTED_ROUTES_MAX` (constant), lines 6774-6774, exports `PERSISTED_ROUTES_MAX`
- order 620: `HTML_FRONTEND_REQUEST_KEYWORDS` (constant), lines 6775-6814, exports `HTML_FRONTEND_REQUEST_KEYWORDS`
- order 621: `DEEP_RESEARCH_REQUEST_KEYWORDS` (constant), lines 6815-6837, exports `DEEP_RESEARCH_REQUEST_KEYWORDS`
- order 622: `DEEP_RESEARCH_RETRIEVAL_KEYWORDS` (constant), lines 6838-6857, exports `DEEP_RESEARCH_RETRIEVAL_KEYWORDS`
- order 623: `DEEP_RESEARCH_TEXT_ONLY_HINT_KEYWORDS` (constant), lines 6858-6875, exports `DEEP_RESEARCH_TEXT_ONLY_HINT_KEYWORDS`
- order 624: `DANGEROUS_PATTERNS` (constant), lines 6876-6877, exports `DANGEROUS_PATTERNS`
- order 625: `VALID_MSG_TYPES` (constant), lines 6878-6884, exports `VALID_MSG_TYPES`
- order 626: `SUPPORTED_UI_LANGUAGES` (constant), lines 6885-6891, exports `SUPPORTED_UI_LANGUAGES`
- order 627: `UI_LANGUAGE_LABELS` (constant), lines 6892-6892, exports `UI_LANGUAGE_LABELS`
- order 628: `DEFAULT_UI_LANGUAGE` (constant), lines 6893-6893, exports `DEFAULT_UI_LANGUAGE`
- order 629: `PUBLIC_TOOL_PROGRESS_SUMMARY_ENABLED` (constant), lines 6894-6896, exports `PUBLIC_TOOL_PROGRESS_SUMMARY_ENABLED`
- order 630: `AGENT_LANGUAGE_PREFERENCES` (constant), lines 6897-6938, exports `AGENT_LANGUAGE_PREFERENCES`
- order 631: `UI_STYLE_CHOICES` (constant), lines 6939-6939, exports `UI_STYLE_CHOICES`
- order 632: `UI_STYLE_LABELS` (constant), lines 6940-6940, exports `UI_STYLE_LABELS`
- order 633: `DEFAULT_UI_STYLE` (constant), lines 6941-6941, exports `DEFAULT_UI_STYLE`
- order 634: `DEFAULT_WEB_UI_DIR` (constant), lines 6942-6942, exports `DEFAULT_WEB_UI_DIR`
- order 635: `DEFAULT_WEB_UI_CONFIG` (constant), lines 6943-6943, exports `DEFAULT_WEB_UI_CONFIG`
- order 636: `WEB_UI_REQUIRED_FILES` (constant), lines 6944-6951, exports `WEB_UI_REQUIRED_FILES`
- order 637: `WEB_UI_OPTIONAL_FILES` (constant), lines 6952-6952, exports `WEB_UI_OPTIONAL_FILES`
- order 638: `WEB_UI_APPLICATION_CONTRACT_VERSION` (constant), lines 6953-6953, exports `WEB_UI_APPLICATION_CONTRACT_VERSION`
- order 639: `WEB_UI_APPLICATION_FEATURE_MARKERS` (constant), lines 6954-6973, exports `WEB_UI_APPLICATION_FEATURE_MARKERS`
- order 640: `IMAGE_EXTS` (constant), lines 6974-6988, exports `IMAGE_EXTS`
- order 641: `IMAGE_FORMATS_NEED_CONVERSION` (constant), lines 6989-6989, exports `IMAGE_FORMATS_NEED_CONVERSION`
- order 642: `IMAGE_SAFE_FORMATS` (constant), lines 6990-6990, exports `IMAGE_SAFE_FORMATS`
- order 643: `AUDIO_EXTS` (constant), lines 6991-7001, exports `AUDIO_EXTS`
- order 644: `VIDEO_EXTS` (constant), lines 7002-7012, exports `VIDEO_EXTS`
- order 645: `CODE_PREVIEW_STAGE_MAX_BYTES` (constant), lines 7013-7013, exports `CODE_PREVIEW_STAGE_MAX_BYTES`
- order 646: `CODE_PREVIEW_STAGE_MAX_ROWS` (constant), lines 7014-7014, exports `CODE_PREVIEW_STAGE_MAX_ROWS`
- order 647: `CODE_PREVIEW_STAGE_MAX_PER_FILE` (constant), lines 7015-7015, exports `CODE_PREVIEW_STAGE_MAX_PER_FILE`
- order 648: `CODE_PREVIEW_STAGE_MAX_TOTAL` (constant), lines 7016-7016, exports `CODE_PREVIEW_STAGE_MAX_TOTAL`
- order 649: `CODE_PREVIEW_DIFF_CONTEXT_LINES` (constant), lines 7017-7017, exports `CODE_PREVIEW_DIFF_CONTEXT_LINES`
- order 650: `CODE_PREVIEW_DIFF_MERGE_GAP` (constant), lines 7018-7018, exports `CODE_PREVIEW_DIFF_MERGE_GAP`
- order 651: `PREVIEW_DOWNLOAD_MAX_FILES` (constant), lines 7019-7019, exports `PREVIEW_DOWNLOAD_MAX_FILES`
- order 652: `PREVIEW_DOWNLOAD_MAX_BYTES` (constant), lines 7020-7020, exports `PREVIEW_DOWNLOAD_MAX_BYTES`
- order 653: `FILES_TREE_DEFAULT_MAX_NODES` (constant), lines 7021-7021, exports `FILES_TREE_DEFAULT_MAX_NODES`
- order 654: `FILES_TREE_DEFAULT_MAX_DEPTH` (constant), lines 7022-7022, exports `FILES_TREE_DEFAULT_MAX_DEPTH`
- order 655: `FILES_TREE_SKIP_DIRS` (constant), lines 7023-7031, exports `FILES_TREE_SKIP_DIRS`
- order 656: `FILES_TREE_SKIP_REL_DIRS` (constant), lines 7032-7034, exports `FILES_TREE_SKIP_REL_DIRS`
- order 657: `IDE_FILE_MAX_BYTES` (constant), lines 7035-7035, exports `IDE_FILE_MAX_BYTES`
- order 658: `IDE_UPLOAD_MAX_BYTES` (constant), lines 7036-7036, exports `IDE_UPLOAD_MAX_BYTES`
- order 659: `IDE_UPLOAD_TOTAL_MAX_BYTES` (constant), lines 7037-7037, exports `IDE_UPLOAD_TOTAL_MAX_BYTES`
- order 660: `IDE_UPLOAD_MAX_ITEMS` (constant), lines 7038-7038, exports `IDE_UPLOAD_MAX_ITEMS`
- order 661: `IDE_UPLOAD_CHUNK_MAX_BYTES` (constant), lines 7039-7039, exports `IDE_UPLOAD_CHUNK_MAX_BYTES`
- order 662: `IDE_UPLOAD_STREAM_MAX_BYTES` (constant), lines 7040-7040, exports `IDE_UPLOAD_STREAM_MAX_BYTES`
- order 663: `IDE_TEXT_PREVIEW_MAX_BYTES` (constant), lines 7041-7041, exports `IDE_TEXT_PREVIEW_MAX_BYTES`
- order 664: `IDE_MARKDOWN_PREVIEW_MAX_LINES` (constant), lines 7042-7042, exports `IDE_MARKDOWN_PREVIEW_MAX_LINES`
- order 665: `IDE_IMAGE_PREVIEW_MAX_EDGE` (constant), lines 7043-7043, exports `IDE_IMAGE_PREVIEW_MAX_EDGE`
- order 666: `IDE_IMAGE_PREVIEW_MAX_PIXELS` (constant), lines 7044-7044, exports `IDE_IMAGE_PREVIEW_MAX_PIXELS`
- order 667: `IDE_IMAGE_PREVIEW_SOURCE_MAX_PIXELS` (constant), lines 7045-7045, exports `IDE_IMAGE_PREVIEW_SOURCE_MAX_PIXELS`
- order 668: `IDE_VECTOR_PREVIEW_MAX_BYTES` (constant), lines 7046-7046, exports `IDE_VECTOR_PREVIEW_MAX_BYTES`
- order 669: `IDE_TABLE_PREVIEW_SOURCE_MAX_BYTES` (constant), lines 7047-7047, exports `IDE_TABLE_PREVIEW_SOURCE_MAX_BYTES`
- order 670: `IDE_TABLE_PREVIEW_CELL_MAX_CHARS` (constant), lines 7048-7048, exports `IDE_TABLE_PREVIEW_CELL_MAX_CHARS`
- order 671: `IDE_TABLE_PREVIEW_TOTAL_CHARS` (constant), lines 7049-7049, exports `IDE_TABLE_PREVIEW_TOTAL_CHARS`
- order 672: `IDE_OFFICE_PREVIEW_MAX_ENTRIES` (constant), lines 7050-7050, exports `IDE_OFFICE_PREVIEW_MAX_ENTRIES`
- order 673: `IDE_OFFICE_PREVIEW_MAX_EXPANDED_BYTES` (constant), lines 7051-7051, exports `IDE_OFFICE_PREVIEW_MAX_EXPANDED_BYTES`
- order 674: `IDE_OFFICE_PREVIEW_MAX_ENTRY_BYTES` (constant), lines 7052-7052, exports `IDE_OFFICE_PREVIEW_MAX_ENTRY_BYTES`
- order 675: `IDE_COMMAND_TIMEOUT_DEFAULT` (constant), lines 7053-7053, exports `IDE_COMMAND_TIMEOUT_DEFAULT`
- order 676: `IDE_TREE_DEFAULT_MAX_NODES` (constant), lines 7054-7054, exports `IDE_TREE_DEFAULT_MAX_NODES`
- order 677: `IDE_TREE_MAX_NODES` (constant), lines 7055-7055, exports `IDE_TREE_MAX_NODES`
- order 678: `IDE_SEARCH_MAX_RESULTS` (constant), lines 7056-7056, exports `IDE_SEARCH_MAX_RESULTS`
- order 679: `IDE_SEARCH_MAX_FILE_BYTES` (constant), lines 7057-7057, exports `IDE_SEARCH_MAX_FILE_BYTES`
- order 680: `IDE_TERMINAL_SCROLLBACK_BYTES` (constant), lines 7058-7058, exports `IDE_TERMINAL_SCROLLBACK_BYTES`
- order 681: `IDE_TERMINAL_IDLE_SECONDS` (constant), lines 7059-7059, exports `IDE_TERMINAL_IDLE_SECONDS`
- order 682: `IDE_DEBUG_ADAPTER_START_ATTEMPTS` (constant), lines 7060-7060, exports `IDE_DEBUG_ADAPTER_START_ATTEMPTS`
- order 683: `IDE_DEBUG_ADAPTER_START_TIMEOUT_SECONDS` (constant), lines 7061-7061, exports `IDE_DEBUG_ADAPTER_START_TIMEOUT_SECONDS`
- order 684: `IDE_VSIX_MAX_BYTES` (constant), lines 7062-7062, exports `IDE_VSIX_MAX_BYTES`
- order 685: `IDE_VSIX_MAX_EXPANDED_BYTES` (constant), lines 7063-7063, exports `IDE_VSIX_MAX_EXPANDED_BYTES`
- order 686: `IDE_VSIX_MAX_FILES` (constant), lines 7064-7064, exports `IDE_VSIX_MAX_FILES`
- order 687: `IDE_VSIX_MAX_FILE_BYTES` (constant), lines 7065-7065, exports `IDE_VSIX_MAX_FILE_BYTES`
- order 688: `IDE_TREE_SKIP_DIRS` (constant), lines 7066-7074, exports `IDE_TREE_SKIP_DIRS`
- order 689: `RENDER_FRAME_MAX_B64_CHARS` (constant), lines 7075-7075, exports `RENDER_FRAME_MAX_B64_CHARS`
- order 690: `RENDER_FRAME_MAX_POINTS` (constant), lines 7076-7076, exports `RENDER_FRAME_MAX_POINTS`
- order 691: `RENDER_FRAME_MAX_LINES` (constant), lines 7077-7077, exports `RENDER_FRAME_MAX_LINES`
- order 692: `RENDER_FRAME_MAX_LINE_POINTS` (constant), lines 7078-7078, exports `RENDER_FRAME_MAX_LINE_POINTS`
- order 693: `RENDER_FRAME_ACTIVITY_INTERVAL_SECONDS` (constant), lines 7079-7079, exports `RENDER_FRAME_ACTIVITY_INTERVAL_SECONDS`
- order 694: `RAW_TOOLCALL_TEXT_FILTER_THRESHOLD` (constant), lines 7080-7080, exports `RAW_TOOLCALL_TEXT_FILTER_THRESHOLD`
- order 695: `ASSISTANT_TEXT_PERSIST_MAX_CHARS` (constant), lines 7081-7081, exports `ASSISTANT_TEXT_PERSIST_MAX_CHARS`
- order 696: `ASSISTANT_MESSAGE_EVENT_MAX_CHARS` (constant), lines 7082-7082, exports `ASSISTANT_MESSAGE_EVENT_MAX_CHARS`
- order 697: `CODE_PREVIEW_EXTS` (constant), lines 7083-7210, exports `CODE_PREVIEW_EXTS`
- order 698: `CODE_PREVIEW_FILENAMES` (constant), lines 7211-7262, exports `CODE_PREVIEW_FILENAMES`
- order 699: `MEDIA_CAPABILITY_KEYS` (constant), lines 7263-7270, exports `MEDIA_CAPABILITY_KEYS`
- order 703: `OFFLINE_JS_LIB_CATALOG` (constant), lines 7303-7629, exports `OFFLINE_JS_LIB_CATALOG`
- order 704: `OFFLINE_JS_ASSET_LOCK` (constant), lines 7630-7630, exports `OFFLINE_JS_ASSET_LOCK`
- order 705: `OFFLINE_JS_LIB_INDEX_FILE` (constant), lines 7631-7631, exports `OFFLINE_JS_LIB_INDEX_FILE`
- order 706: `OFFLINE_JS_LIB_README_FILE` (constant), lines 7632-7632, exports `OFFLINE_JS_LIB_README_FILE`
- order 717: `BACKEND_I18N` (constant), lines 7838-7909, exports `BACKEND_I18N`
- order 718: `_call_backend_i18n_en_update_7911` (expression), lines 7910-8011, exports —
- order 719: `_call_backend_i18n_zh_cn_update_8012` (expression), lines 8012-8112, exports —
- order 720: `_call_backend_i18n_zh_tw_update_8113` (expression), lines 8113-8213, exports —
- order 721: `_call_backend_i18n_ja_update_8214` (expression), lines 8214-8314, exports —
- order 944: `MODEL_RUNTIME_SETTING_KEYS` (constant), lines 14876-14881, exports `MODEL_RUNTIME_SETTING_KEYS`
- order 965: `LIQUID_KERNEL_STARTUP_POLICIES` (constant), lines 16582-16584, exports `LIQUID_KERNEL_STARTUP_POLICIES`
- order 966: `LIQUID_KERNEL_BOOTSTRAP_STATE_FILENAME` (constant), lines 16585-16585, exports `LIQUID_KERNEL_BOOTSTRAP_STATE_FILENAME`
- order 997: `TABULAR_PREVIEW_EXTS` (constant), lines 18523-18525, exports `TABULAR_PREVIEW_EXTS`
- order 998: `EXCEL_PREVIEW_EXTS` (constant), lines 18526-18526, exports `EXCEL_PREVIEW_EXTS`
- order 999: `PRESENTATION_PREVIEW_EXTS` (constant), lines 18527-18527, exports `PRESENTATION_PREVIEW_EXTS`
- order 1000: `DOCUMENT_PREVIEW_EXTS` (constant), lines 18528-18528, exports `DOCUMENT_PREVIEW_EXTS`
- order 1081: `SESSION_LLM_PRIORITY_RANKS` (constant), lines 28041-28045, exports `SESSION_LLM_PRIORITY_RANKS`
- order 1087: `TODO_REVISION_FALLBACK_MAX_ROWS` (constant), lines 28055-28057, exports `TODO_REVISION_FALLBACK_MAX_ROWS`
- order 1102: `BASH_OPERATION_CODES` (constant), lines 31351-31373, exports `BASH_OPERATION_CODES`
- order 1103: `BASH_OBSERVATION_OPERATION_CODES` (constant), lines 31374-31385, exports `BASH_OBSERVATION_OPERATION_CODES`
- order 1104: `BASH_OPERATION_ALIASES` (constant), lines 31386-31412, exports `BASH_OPERATION_ALIASES`
- order 1237: `STUDIO_DEVICE_COOKIE` (constant), lines 123331-123348, exports `STUDIO_DEVICE_COOKIE`
- order 1238: `STUDIO_SESSION_COOKIE` (constant), lines 123349-123349, exports `STUDIO_SESSION_COOKIE`
- order 1239: `STUDIO_DEVICE_TTL` (constant), lines 123350-123350, exports `STUDIO_DEVICE_TTL`
- order 1240: `STUDIO_SESSION_TTL` (constant), lines 123351-123351, exports `STUDIO_SESSION_TTL`
- order 1241: `STUDIO_MAX_FILE_BYTES` (constant), lines 123352-123352, exports `STUDIO_MAX_FILE_BYTES`
- order 1242: `STUDIO_MAX_PROJECT_BYTES` (constant), lines 123353-123353, exports `STUDIO_MAX_PROJECT_BYTES`
- order 1243: `STUDIO_MAX_FILES` (constant), lines 123354-123354, exports `STUDIO_MAX_FILES`
- order 1244: `STUDIO_MAX_JOB_SECONDS` (constant), lines 123355-123355, exports `STUDIO_MAX_JOB_SECONDS`
- order 1250: `STUDIO_INDEX_HTML` (constant), lines 125254-125256, exports `STUDIO_INDEX_HTML`
- order 1251: `STUDIO_CSS` (constant), lines 125257-125257, exports `STUDIO_CSS`
- order 1252: `STUDIO_JS` (constant), lines 125258-125258, exports `STUDIO_JS`

### `config/paths.py`

- order 128: `SCRIPT_DIR` (constant), lines 5147-5147, exports `SCRIPT_DIR`
- order 153: `_resolve_default_agent_workdir` (function), lines 5241-5250, exports `_resolve_default_agent_workdir`
- order 154: `_is_installed_python_runtime` (function), lines 5251-5254, exports `_is_installed_python_runtime`
- order 155: `_runtime_storage_mode` (function), lines 5255-5261, exports `_runtime_storage_mode`
- order 156: `_runtime_tree_has_content` (function), lines 5262-5267, exports `_runtime_tree_has_content`
- order 157: `_copy_runtime_tree_with_crypto_migration` (function), lines 5268-5338, exports `_copy_runtime_tree_with_crypto_migration`
- order 158: `_merge_legacy_codes_root` (function), lines 5339-5404, exports `_merge_legacy_codes_root`
- order 159: `_migrate_legacy_runtime_roots` (function), lines 5405-5495, exports `_migrate_legacy_runtime_roots`
- order 160: `WORKDIR` (constant), lines 5496-5497, exports `WORKDIR`
- order 161: `CODES_ROOT` (constant), lines 5498-5498, exports `CODES_ROOT`
- order 162: `LLM_CONFIG_PATH` (constant), lines 5499-5499, exports `LLM_CONFIG_PATH`
- order 801: `detect_repo_root` (function), lines 9805-9819, exports `detect_repo_root`
- order 802: `REPO_ROOT` (constant), lines 9820-9821, exports `REPO_ROOT`

### `config/settings.py`

- order 710: `normalize_ui_language` (function), lines 7714-7738, exports `normalize_ui_language`
- order 711: `normalize_ui_style` (function), lines 7739-7758, exports `normalize_ui_style`
- order 712: `supported_ui_languages_payload` (function), lines 7759-7762, exports `supported_ui_languages_payload`
- order 714: `agent_language_preference_payload` (function), lines 7775-7784, exports `agent_language_preference_payload`
- order 715: `normalize_execution_mode` (function), lines 7785-7806, exports `normalize_execution_mode`
- order 716: `model_language_instruction` (function), lines 7807-7837, exports `model_language_instruction`
- order 722: `backend_i18n_text` (function), lines 8315-8327, exports `backend_i18n_text`
- order 723: `backend_role_label` (function), lines 8328-8334, exports `backend_role_label`
- order 724: `_detect_os_shell_instruction` (function), lines 8335-8376, exports `_detect_os_shell_instruction`
- order 725: `resolve_web_ui_dir_path` (function), lines 8377-8385, exports `resolve_web_ui_dir_path`
- order 726: `resolve_optional_file_path` (function), lines 8386-8395, exports `resolve_optional_file_path`
- order 727: `resolve_skills_root_path` (function), lines 8396-8405, exports `resolve_skills_root_path`
- order 728: `_count_skill_markdown_files` (function), lines 8406-8419, exports `_count_skill_markdown_files`
- order 729: `select_preferred_skills_root` (function), lines 8420-8456, exports `select_preferred_skills_root`
- order 730: `load_web_ui_config_file` (function), lines 8457-8473, exports `load_web_ui_config_file`
- order 731: `extract_show_upload_list_setting` (function), lines 8474-8490, exports `extract_show_upload_list_setting`
- order 732: `extract_ui_style_setting` (function), lines 8491-8507, exports `extract_ui_style_setting`
- order 733: `extract_js_lib_download_setting` (function), lines 8508-8529, exports `extract_js_lib_download_setting`
- order 734: `extract_daily_session_limit_setting` (function), lines 8530-8575, exports `extract_daily_session_limit_setting`
- order 735: `extract_shell_command_timeout_setting` (function), lines 8576-8624, exports `extract_shell_command_timeout_setting`
- order 736: `normalize_shell_timeout_mode` (function), lines 8625-8642, exports `normalize_shell_timeout_mode`
- order 737: `extract_shell_timeout_mode_setting` (function), lines 8643-8655, exports `extract_shell_timeout_mode_setting`
- order 738: `extract_shell_async_handoff_setting` (function), lines 8656-8683, exports `extract_shell_async_handoff_setting`
- order 739: `extract_context_token_limit_setting` (function), lines 8684-8718, exports `extract_context_token_limit_setting`
- order 740: `normalize_auto_task_level_ceiling` (function), lines 8719-8740, exports `normalize_auto_task_level_ceiling`
- order 741: `normalize_l2_todo_policy` (function), lines 8741-8776, exports `normalize_l2_todo_policy`
- order 742: `extract_l2_todo_policy_setting` (function), lines 8777-8819, exports `extract_l2_todo_policy_setting`
- order 743: `extract_auto_task_level_ceiling_setting` (function), lines 8820-8849, exports `extract_auto_task_level_ceiling_setting`
- order 744: `normalize_session_llm_concurrency` (function), lines 8850-8871, exports `normalize_session_llm_concurrency`
- order 745: `extract_session_llm_concurrency_setting` (function), lines 8872-8893, exports `extract_session_llm_concurrency_setting`
- order 746: `normalize_read_context_policy` (function), lines 8894-8914, exports `normalize_read_context_policy`
- order 747: `normalize_tool_memory_policy` (function), lines 8915-8918, exports `normalize_tool_memory_policy`
- order 748: `extract_read_context_policy_setting` (function), lines 8919-8942, exports `extract_read_context_policy_setting`
- order 749: `extract_tool_memory_policy_setting` (function), lines 8943-8966, exports `extract_tool_memory_policy_setting`
- order 751: `default_multimodal_capabilities` (function), lines 8973-8983, exports `default_multimodal_capabilities`
- order 752: `_to_bool_like` (function), lines 8984-8996, exports `_to_bool_like`
- order 753: `extract_web_search_enabled_setting` (function), lines 8997-9009, exports `extract_web_search_enabled_setting`
- order 754: `_single_no_plan_todo_setting_sections` (function), lines 9010-9036, exports `_single_no_plan_todo_setting_sections`
- order 755: `_single_no_plan_todo_setting_present` (function), lines 9037-9062, exports `_single_no_plan_todo_setting_present`
- order 756: `extract_single_no_plan_todo_settings` (function), lines 9063-9109, exports `extract_single_no_plan_todo_settings`
- order 757: `normalize_user_memory_mode` (function), lines 9110-9140, exports `normalize_user_memory_mode`
- order 758: `user_memory_enabled_from_mode` (function), lines 9141-9144, exports `user_memory_enabled_from_mode`
- order 759: `extract_user_memory_mode_setting` (function), lines 9145-9184, exports `extract_user_memory_mode_setting`
- order 760: `set_web_search_enabled_on_runtime` (function), lines 9185-9200, exports `set_web_search_enabled_on_runtime`
- order 761: `infer_model_multimodal_capabilities` (function), lines 9201-9247, exports `infer_model_multimodal_capabilities`
- order 762: `parse_capability_overrides` (function), lines 9248-9287, exports `parse_capability_overrides`
- order 763: `merge_multimodal_capabilities` (function), lines 9288-9297, exports `merge_multimodal_capabilities`
- order 764: `parse_media_endpoints` (function), lines 9298-9314, exports `parse_media_endpoints`
- order 780: `extract_runtime_region_hint_setting` (function), lines 9492-9517, exports `extract_runtime_region_hint_setting`
- order 781: `extract_runtime_timezone_hint_setting` (function), lines 9518-9535, exports `extract_runtime_timezone_hint_setting`
- order 782: `runtime_environment_context_snapshot` (function), lines 9536-9585, exports `runtime_environment_context_snapshot`
- order 783: `runtime_environment_context_block` (function), lines 9586-9615, exports `runtime_environment_context_block`
- order 880: `extract_ollama_model_capabilities` (function), lines 13681-13703, exports `extract_ollama_model_capabilities`
- order 909: `infer_user_complexity_value` (function), lines 14275-14292, exports `infer_user_complexity_value`
- order 910: `normalize_task_complexity` (function), lines 14293-14322, exports `normalize_task_complexity`
- order 911: `task_complexity_rank` (function), lines 14323-14325, exports `task_complexity_rank`
- order 912: `task_complexity_at_least` (function), lines 14326-14328, exports `task_complexity_at_least`
- order 913: `max_task_complexity` (function), lines 14329-14339, exports `max_task_complexity`
- order 945: `merge_probed_models_into_profile` (function), lines 14882-14927, exports `merge_probed_models_into_profile`
- order 946: `probe_and_merge_model_profiles` (function), lines 14928-14985, exports `probe_and_merge_model_profiles`
- order 947: `normalize_model_runtime_settings` (function), lines 14986-15011, exports `normalize_model_runtime_settings`
- order 948: `apply_model_runtime_settings` (function), lines 15012-15027, exports `apply_model_runtime_settings`
- order 949: `model_runtime_settings_for` (function), lines 15028-15038, exports `model_runtime_settings_for`
- order 950: `apply_model_option_runtime_fields` (function), lines 15039-15051, exports `apply_model_option_runtime_fields`
- order 953: `load_llm_config_from_source` (function), lines 15084-15119, exports `load_llm_config_from_source`
- order 954: `parse_llm_config_profiles` (function), lines 15120-15985, exports `parse_llm_config_profiles`
- order 955: `looks_like_llm_config` (function), lines 15986-16075, exports `looks_like_llm_config`
- order 959: `parse_front_matter` (function), lines 16271-16499, exports `parse_front_matter`
- order 967: `normalize_liquid_kernel_startup_policy` (function), lines 16586-16590, exports `normalize_liquid_kernel_startup_policy`
- order 995: `normalize_upload_rel_path` (function), lines 18477-18511, exports `normalize_upload_rel_path`
- order 1105: `normalize_bash_operation` (function), lines 31413-31430, exports `normalize_bash_operation`

### `ide/assets.py`

- order 1229: `IDE_INDEX_HTML` (constant), lines 122173-122328, exports `IDE_INDEX_HTML`
- order 1230: `IDE_CSS` (constant), lines 122329-122370, exports `IDE_CSS`
- order 1231: `IDE_JS` (constant), lines 122371-122564, exports `IDE_JS`
- order 1232: `IDE_CSS` (constant), lines 122565-122586, exports `IDE_CSS`
- order 1233: `IDE_JS` (constant), lines 122587-122850, exports `IDE_JS`
- order 1234: `IDE_JS` (constant), lines 122851-122979, exports `IDE_JS`
- order 1235: `IDE_JS` (constant), lines 122980-123203, exports `IDE_JS`
- order 1236: `IDE_JS` (constant), lines 123204-123330, exports `IDE_JS`

### `ide/auth.py`

- order 973: `IDEAuthError` (class), lines 16927-16934, exports `IDEAuthError`
- order 974: `IDEAuthStore` (class), lines 16935-17658, exports `IDEAuthStore`

### `ide/errors.py`

- order 975: `IDECapabilityError` (class), lines 17659-17665, exports `IDECapabilityError`
- order 976: `IDEFileConflict` (class), lines 17666-17673, exports `IDEFileConflict`

### `ide/events.py`

- order 836: `ide_public_operation_data` (function), lines 10704-10755, exports `ide_public_operation_data`

### `ide/handler.py`

- order 1269: `IdeHandler` (class), lines 141360-143016, exports `IdeHandler`

### `ide/preview.py`

- order 994: `normalize_rel_preview_path` (function), lines 18463-18476, exports `normalize_rel_preview_path`
- order 996: `is_code_preview_candidate` (function), lines 18512-18522, exports `is_code_preview_candidate`
- order 1001: `preview_kind_for_path` (function), lines 18529-18558, exports `preview_kind_for_path`
- order 1002: `normalize_markdown_preview_text` (function), lines 18559-18592, exports `normalize_markdown_preview_text`
- order 1003: `_preview_markdown_value_html` (function), lines 18593-18613, exports `_preview_markdown_value_html`
- order 1004: `_preview_markdown_frontmatter_html` (function), lines 18614-18629, exports `_preview_markdown_frontmatter_html`
- order 1005: `_preview_markdown_task_lists` (function), lines 18630-18643, exports `_preview_markdown_task_lists`
- order 1006: `_preview_markdown_fallback_inline` (function), lines 18644-18685, exports `_preview_markdown_fallback_inline`
- order 1007: `_preview_markdown_fallback_html` (function), lines 18686-18782, exports `_preview_markdown_fallback_html`
- order 1010: `workspace_file_revision_map` (function), lines 18823-18847, exports `workspace_file_revision_map`
- order 1011: `workspace_revision_delta` (function), lines 18848-18854, exports `workspace_revision_delta`
- order 1012: `build_code_preview_rows` (function), lines 18855-18903, exports `build_code_preview_rows`

### `ide/sandbox.py`

- order 788: `_windows_subprocess_encodings` (function), lines 9643-9660, exports `_windows_subprocess_encodings`
- order 1120: `_IDE_SANDBOX_BACKEND_CACHE` (assignment), lines 32196-32204, exports `_IDE_SANDBOX_BACKEND_CACHE`
- order 1121: `_IDE_SANDBOX_BACKEND_LOCK` (assignment), lines 32205-32205, exports `_IDE_SANDBOX_BACKEND_LOCK`
- order 1122: `WINDOWS_JOB_SANDBOX_MARKER` (constant), lines 32206-32206, exports `WINDOWS_JOB_SANDBOX_MARKER`
- order 1123: `_WINDOWS_LOW_INTEGRITY_ROOTS` (assignment), lines 32207-32207, exports `_WINDOWS_LOW_INTEGRITY_ROOTS`
- order 1124: `_WINDOWS_LOW_INTEGRITY_FAILED_ROOTS` (assignment), lines 32208-32208, exports `_WINDOWS_LOW_INTEGRITY_FAILED_ROOTS`
- order 1125: `_WINDOWS_LOW_INTEGRITY_LOCK` (assignment), lines 32209-32209, exports `_WINDOWS_LOW_INTEGRITY_LOCK`
- order 1126: `_is_windows_job_sandbox_prefix` (function), lines 32210-32216, exports `_is_windows_job_sandbox_prefix`
- order 1127: `_windows_builtin_sandbox_probe` (function), lines 32217-32240, exports `_windows_builtin_sandbox_probe`
- order 1128: `_windows_last_error` (function), lines 32241-32248, exports `_windows_last_error`
- order 1129: `_windows_set_integrity_label` (function), lines 32249-32302, exports `_windows_set_integrity_label`
- order 1130: `_windows_set_low_integrity_label` (function), lines 32303-32305, exports `_windows_set_low_integrity_label`
- order 1131: `_windows_protect_application_snapshot` (function), lines 32306-32329, exports `_windows_protect_application_snapshot`
- order 1132: `_windows_prepare_low_integrity_workspace` (function), lines 32330-32367, exports `_windows_prepare_low_integrity_workspace`
- order 1133: `_windows_job_memory_limit` (function), lines 32368-32375, exports `_windows_job_memory_limit`
- order 1134: `_windows_lower_process_integrity` (function), lines 32376-32423, exports `_windows_lower_process_integrity`
- order 1135: `_windows_attach_sandbox_job` (function), lines 32424-32516, exports `_windows_attach_sandbox_job`
- order 1136: `_windows_close_sandbox_job` (function), lines 32517-32533, exports `_windows_close_sandbox_job`
- order 1137: `_popen_windows_sandboxed` (function), lines 32534-32565, exports `_popen_windows_sandboxed`
- order 1138: `_run_windows_sandboxed_command` (function), lines 32566-32619, exports `_run_windows_sandboxed_command`
- order 1139: `_detect_ide_sandbox_backend` (function), lines 32620-32727, exports `_detect_ide_sandbox_backend`

### `ide/toolchains.py`

- order 549: `IDE_TOOLCHAIN_CACHE_TTL_SECONDS` (constant), lines 6540-6546, exports `IDE_TOOLCHAIN_CACHE_TTL_SECONDS`
- order 550: `_IDE_TOOLCHAIN_CACHE_LOCK` (assignment), lines 6547-6547, exports `_IDE_TOOLCHAIN_CACHE_LOCK`
- order 551: `_IDE_TOOLCHAIN_CACHE` (assignment), lines 6548-6548, exports `_IDE_TOOLCHAIN_CACHE`
- order 552: `_IDE_TOOLCHAIN_REFRESHING` (assignment), lines 6549-6549, exports `_IDE_TOOLCHAIN_REFRESHING`
- order 1256: `_ide_toolchain_cache_key` (function), lines 125263-125273, exports `_ide_toolchain_cache_key`
- order 1257: `_probe_ide_toolchains` (function), lines 125274-125317, exports `_probe_ide_toolchains`
- order 1258: `_refresh_ide_toolchains_in_background` (function), lines 125318-125327, exports `_refresh_ide_toolchains_in_background`

### `llm/client.py`

- order 1080: `OllamaError` (class), lines 27999-28040, exports `OllamaError`
- order 1100: `OllamaClient` (class), lines 28477-31336, exports `OllamaClient`

### `llm/constants.py`

- order 126: `DEFAULT_OLLAMA_BASE_URL` (constant), lines 5145-5145, exports `DEFAULT_OLLAMA_BASE_URL`
- order 127: `DEFAULT_OLLAMA_MODEL` (constant), lines 5146-5146, exports `DEFAULT_OLLAMA_MODEL`
- order 915: `OPENAI_COMPAT_PROVIDER_NAMES` (constant), lines 14357-14366, exports `OPENAI_COMPAT_PROVIDER_NAMES`
- order 916: `OPENAI_LIKE_PROVIDER_NAMES` (constant), lines 14367-14368, exports `OPENAI_LIKE_PROVIDER_NAMES`
- order 919: `EFFORT_OFF` (constant), lines 14375-14386, exports `EFFORT_OFF`
- order 920: `EFFORT_LOW` (constant), lines 14387-14387, exports `EFFORT_LOW`
- order 921: `EFFORT_MEDIUM` (constant), lines 14388-14388, exports `EFFORT_MEDIUM`
- order 922: `EFFORT_HIGH` (constant), lines 14389-14389, exports `EFFORT_HIGH`
- order 923: `EFFORT_MAX` (constant), lines 14390-14390, exports `EFFORT_MAX`
- order 924: `EFFORT_LEVELS` (constant), lines 14391-14391, exports `EFFORT_LEVELS`
- order 925: `EFFORT_ORDER` (constant), lines 14392-14392, exports `EFFORT_ORDER`
- order 926: `EFFORT_DEFAULT` (constant), lines 14393-14393, exports `EFFORT_DEFAULT`
- order 927: `EFFORT_ANTHROPIC_BUDGET` (constant), lines 14394-14401, exports `EFFORT_ANTHROPIC_BUDGET`
- order 928: `EFFORT_OPENAI_REASONING` (constant), lines 14402-14408, exports `EFFORT_OPENAI_REASONING`
- order 929: `TASK_LEVEL_EFFORT` (constant), lines 14409-14418, exports `TASK_LEVEL_EFFORT`
- order 930: `ROLE_EFFORT_FLOOR` (constant), lines 14419-14424, exports `ROLE_EFFORT_FLOOR`
- order 931: `COORDINATION_EFFORT` (constant), lines 14425-14428, exports `COORDINATION_EFFORT`

### `llm/gate.py`

- order 399: `SESSION_LLM_CONCURRENCY_MIN` (constant), lines 6023-6027, exports `SESSION_LLM_CONCURRENCY_MIN`
- order 400: `SESSION_LLM_CONCURRENCY_MAX` (constant), lines 6028-6028, exports `SESSION_LLM_CONCURRENCY_MAX`
- order 401: `SESSION_LLM_CONCURRENCY_FACTORY_DEFAULT` (constant), lines 6029-6029, exports `SESSION_LLM_CONCURRENCY_FACTORY_DEFAULT`
- order 402: `_session_llm_concurrency_env_default` (function), lines 6030-6038, exports `_session_llm_concurrency_env_default`
- order 403: `DEFAULT_SESSION_LLM_CONCURRENCY` (constant), lines 6039-6041, exports `DEFAULT_SESSION_LLM_CONCURRENCY`
- order 1082: `SESSION_LLM_GATE_POLL_SECONDS` (constant), lines 28046-28046, exports `SESSION_LLM_GATE_POLL_SECONDS`
- order 1083: `SESSION_LLM_GATE_SNAPSHOT_MAX_REQUESTS` (constant), lines 28047-28047, exports `SESSION_LLM_GATE_SNAPSHOT_MAX_REQUESTS`
- order 1084: `SESSION_LLM_CONCURRENCY_PUSH_INTERVAL_SECONDS` (constant), lines 28048-28050, exports `SESSION_LLM_CONCURRENCY_PUSH_INTERVAL_SECONDS`
- order 1085: `TODO_LLM_CALL_BUDGET` (constant), lines 28051-28053, exports `TODO_LLM_CALL_BUDGET`
- order 1086: `TODO_LLM_TIMEOUT_FACTORY_DEFAULT` (constant), lines 28054-28054, exports `TODO_LLM_TIMEOUT_FACTORY_DEFAULT`
- order 1088: `_todo_llm_timeout_env_default` (function), lines 28058-28068, exports `_todo_llm_timeout_env_default`
- order 1089: `TODO_LLM_TIMEOUT_SECONDS` (constant), lines 28069-28074, exports `TODO_LLM_TIMEOUT_SECONDS`
- order 1090: `LLMGateBusy` (class), lines 28075-28084, exports `LLMGateBusy`
- order 1091: `TodoLLMBudgetExhausted` (class), lines 28085-28088, exports `TodoLLMBudgetExhausted`
- order 1092: `_TODO_LLM_BUDGET_LOCAL` (assignment), lines 28089-28091, exports `_TODO_LLM_BUDGET_LOCAL`
- order 1093: `todo_llm_budget_scope` (function), lines 28092-28117, exports `todo_llm_budget_scope`
- order 1094: `_consume_todo_llm_budget` (function), lines 28118-28129, exports `_consume_todo_llm_budget`
- order 1095: `todo_llm_budget_active` (function), lines 28130-28134, exports `todo_llm_budget_active`
- order 1096: `todo_llm_skip_reason` (function), lines 28135-28162, exports `todo_llm_skip_reason`
- order 1097: `SessionLLMGate` (class), lines 28163-28463, exports `SessionLLMGate`
- order 1098: `_SESSION_LLM_GATE_INIT_LOCK` (assignment), lines 28464-28466, exports `_SESSION_LLM_GATE_INIT_LOCK`
- order 1099: `set_session_llm_concurrency_on_runtime` (function), lines 28467-28476, exports `set_session_llm_concurrency_on_runtime`

### `llm/utils.py`

- order 879: `probe_ollama_environment` (function), lines 13666-13680, exports `probe_ollama_environment`
- order 881: `probe_ollama_model_records` (function), lines 13704-13737, exports `probe_ollama_model_records`
- order 882: `list_ollama_models` (function), lines 13738-13742, exports `list_ollama_models`
- order 883: `_OLLAMA_TAG_CACHE_LOCK` (assignment), lines 13743-13744, exports `_OLLAMA_TAG_CACHE_LOCK`
- order 884: `_OLLAMA_TAG_CACHE` (assignment), lines 13745-13745, exports `_OLLAMA_TAG_CACHE`
- order 887: `_fetch_ollama_models_cached` (function), lines 13754-13779, exports `_fetch_ollama_models_cached`
- order 888: `list_ollama_models_cached` (function), lines 13780-13825, exports `list_ollama_models_cached`
- order 889: `resolve_ollama_model` (function), lines 13826-13837, exports `resolve_ollama_model`
- order 890: `infer_thinking_model` (function), lines 13838-13841, exports `infer_thinking_model`
- order 891: `split_thinking_content` (function), lines 13842-13886, exports `split_thinking_content`
- order 892: `strip_thinking_content` (function), lines 13887-13889, exports `strip_thinking_content`
- order 893: `check_ollama_model_ready` (function), lines 13890-13915, exports `check_ollama_model_ready`
- order 894: `list_loaded_ollama_models` (function), lines 13916-13930, exports `list_loaded_ollama_models`
- order 895: `wake_ollama_model` (function), lines 13931-13962, exports `wake_ollama_model`
- order 896: `try_pull_ollama_model` (function), lines 13963-13981, exports `try_pull_ollama_model`
- order 897: `ordered_model_candidates` (function), lines 13982-14001, exports `ordered_model_candidates`
- order 898: `pick_working_ollama_model` (function), lines 14002-14019, exports `pick_working_ollama_model`
- order 905: `evolution_worker_chat_messages` (function), lines 14177-14228, exports `evolution_worker_chat_messages`
- order 907: `extract_base_url` (function), lines 14254-14263, exports `extract_base_url`
- order 908: `complete_chat_endpoint` (function), lines 14264-14274, exports `complete_chat_endpoint`
- order 914: `normalize_openai_compat_provider_name` (function), lines 14340-14356, exports `normalize_openai_compat_provider_name`
- order 917: `is_openai_compat_provider` (function), lines 14369-14371, exports `is_openai_compat_provider`
- order 918: `is_openai_like_provider` (function), lines 14372-14374, exports `is_openai_like_provider`
- order 932: `clamp_effort` (function), lines 14429-14440, exports `clamp_effort`
- order 933: `model_reasoning_style` (function), lines 14441-14483, exports `model_reasoning_style`
- order 934: `resolve_reasoning_payload` (function), lines 14484-14546, exports `resolve_reasoning_payload`
- order 935: `openai_compat_probe_headers` (function), lines 14547-14565, exports `openai_compat_probe_headers`
- order 936: `openai_compat_model_list_urls` (function), lines 14566-14599, exports `openai_compat_model_list_urls`
- order 937: `anthropic_model_list_url` (function), lines 14600-14614, exports `anthropic_model_list_url`
- order 938: `extract_openai_compat_model_ids` (function), lines 14615-14649, exports `extract_openai_compat_model_ids`
- order 939: `extract_openai_compat_model_records` (function), lines 14650-14729, exports `extract_openai_compat_model_records`
- order 940: `_PROVIDER_MODEL_CACHE_LOCK` (assignment), lines 14730-14732, exports `_PROVIDER_MODEL_CACHE_LOCK`
- order 941: `_PROVIDER_MODEL_CACHE` (assignment), lines 14733-14733, exports `_PROVIDER_MODEL_CACHE`
- order 942: `_fetch_provider_models_cached` (function), lines 14734-14807, exports `_fetch_provider_models_cached`
- order 943: `probe_provider_models` (function), lines 14808-14875, exports `probe_provider_models`
- order 951: `_is_http_url` (function), lines 15052-15065, exports `_is_http_url`
- order 952: `_resolve_local_path` (function), lines 15066-15083, exports `_resolve_local_path`

### `mcp/constants.py`

- order 180: `MCP_SERVICE_PORT_OFFSET` (constant), lines 5517-5517, exports `MCP_SERVICE_PORT_OFFSET`
- order 1060: `MCP_PROTOCOL_VERSION` (constant), lines 26617-26646, exports `MCP_PROTOCOL_VERSION`
- order 1061: `MCP_NAME_RE` (constant), lines 26647-26647, exports `MCP_NAME_RE`
- order 1062: `MCP_TOOL_PREFIX` (constant), lines 26648-26648, exports `MCP_TOOL_PREFIX`
- order 1063: `_MCP_DEFAULT_HANDSHAKE_TIMEOUT` (assignment), lines 26649-26649, exports `_MCP_DEFAULT_HANDSHAKE_TIMEOUT`
- order 1064: `_MCP_DEFAULT_CALL_TIMEOUT` (assignment), lines 26650-26650, exports `_MCP_DEFAULT_CALL_TIMEOUT`
- order 1065: `_MCP_MAX_RESULT_CHARS` (assignment), lines 26651-26651, exports `_MCP_MAX_RESULT_CHARS`
- order 1066: `_MCP_TRUST_STORE_VERSION` (assignment), lines 26652-26652, exports `_MCP_TRUST_STORE_VERSION`

### `mcp/driver.py`

- order 1067: `mcp_normalize_name` (function), lines 26653-26662, exports `mcp_normalize_name`
- order 1068: `mcp_normalize_server_configs` (function), lines 26663-26747, exports `mcp_normalize_server_configs`
- order 1069: `mcp_extract_server_configs` (function), lines 26748-26767, exports `mcp_extract_server_configs`
- order 1070: `_mcp_sha256_file` (function), lines 26768-26778, exports `_mcp_sha256_file`
- order 1071: `_mcp_file_identity` (function), lines 26779-26796, exports `_mcp_file_identity`
- order 1072: `mcp_workspace_identity` (function), lines 26797-26815, exports `mcp_workspace_identity`
- order 1073: `mcp_config_file_digest` (function), lines 26816-26823, exports `mcp_config_file_digest`
- order 1074: `mcp_default_trust_store_path` (function), lines 26824-26858, exports `mcp_default_trust_store_path`
- order 1075: `mcp_record_definition_fingerprint` (function), lines 26859-26873, exports `mcp_record_definition_fingerprint`
- order 1076: `_mcp_effective_spawn` (function), lines 26874-26961, exports `_mcp_effective_spawn`
- order 1077: `MCPWorkspaceTrustStore` (class), lines 26962-27023, exports `MCPWorkspaceTrustStore`
- order 1078: `MCPServerProcess` (class), lines 27024-27379, exports `MCPServerProcess`
- order 1079: `MCPManager` (class), lines 27380-27998, exports `MCPManager`

### `mcp/service.py`

- order 1271: `McpServiceHandler` (class), lines 143488-143705, exports `McpServiceHandler`

### `rag/assets.py`

- order 1223: `RAG_ADMIN_INDEX_HTML` (constant), lines 119549-119781, exports `RAG_ADMIN_INDEX_HTML`
- order 1224: `RAG_ADMIN_CSS` (constant), lines 119782-119885, exports `RAG_ADMIN_CSS`
- order 1225: `RAG_ADMIN_JS` (constant), lines 119886-122123, exports `RAG_ADMIN_JS`
- order 1226: `CODE_ADMIN_INDEX_HTML` (constant), lines 122124-122136, exports `CODE_ADMIN_INDEX_HTML`
- order 1227: `CODE_ADMIN_CSS` (constant), lines 122137-122167, exports `CODE_ADMIN_CSS`
- order 1228: `CODE_ADMIN_JS` (constant), lines 122168-122172, exports `CODE_ADMIN_JS`

### `rag/constants.py`

- order 176: `RAG_LIBRARY_DIRNAME` (constant), lines 5513-5513, exports `RAG_LIBRARY_DIRNAME`
- order 177: `RAG_ADMIN_PORT_OFFSET` (constant), lines 5514-5514, exports `RAG_ADMIN_PORT_OFFSET`
- order 178: `CODE_LIBRARY_DIRNAME` (constant), lines 5515-5515, exports `CODE_LIBRARY_DIRNAME`
- order 184: `WEB_SEARCH_INDEX_DIRNAME` (constant), lines 5524-5524, exports `WEB_SEARCH_INDEX_DIRNAME`
- order 186: `USER_MEMORY_DIRNAME` (constant), lines 5526-5526, exports `USER_MEMORY_DIRNAME`
- order 187: `USER_MEMORY_DB_FILENAME` (constant), lines 5527-5527, exports `USER_MEMORY_DB_FILENAME`
- order 188: `USER_MEMORY_PROFILE_FILENAME` (constant), lines 5528-5528, exports `USER_MEMORY_PROFILE_FILENAME`
- order 189: `USER_MEMORY_MODE_CHOICES` (constant), lines 5529-5529, exports `USER_MEMORY_MODE_CHOICES`
- order 191: `USER_MEMORY_WEAK_CAPSULE_CHARS` (constant), lines 5531-5531, exports `USER_MEMORY_WEAK_CAPSULE_CHARS`
- order 192: `USER_MEMORY_ON_CAPSULE_CHARS` (constant), lines 5532-5532, exports `USER_MEMORY_ON_CAPSULE_CHARS`
- order 193: `USER_MEMORY_CAPSULE_INJECT_CHARS` (constant), lines 5533-5536, exports `USER_MEMORY_CAPSULE_INJECT_CHARS`
- order 194: `USER_MEMORY_MAX_SUMMARY_CHARS` (constant), lines 5537-5537, exports `USER_MEMORY_MAX_SUMMARY_CHARS`
- order 195: `USER_MEMORY_QUERY_LIMIT` (constant), lines 5538-5538, exports `USER_MEMORY_QUERY_LIMIT`
- order 196: `USER_MEMORY_DECAY_HALFLIFE_DAYS` (constant), lines 5539-5539, exports `USER_MEMORY_DECAY_HALFLIFE_DAYS`
- order 197: `USER_MEMORY_PROFILE_SCHEMA_VERSION` (constant), lines 5540-5540, exports `USER_MEMORY_PROFILE_SCHEMA_VERSION`
- order 217: `WEB_SEARCH_CONTEXT_REGISTRY_MAX` (constant), lines 5562-5562, exports `WEB_SEARCH_CONTEXT_REGISTRY_MAX`
- order 218: `WEB_SEARCH_CONTEXT_PROMPT_MAX_ITEMS` (constant), lines 5563-5563, exports `WEB_SEARCH_CONTEXT_PROMPT_MAX_ITEMS`
- order 219: `WEB_SEARCH_CONTEXT_PROMPT_MAX_CHARS` (constant), lines 5564-5564, exports `WEB_SEARCH_CONTEXT_PROMPT_MAX_CHARS`
- order 220: `WEB_SEARCH_CONTEXT_NODE_MAX` (constant), lines 5565-5565, exports `WEB_SEARCH_CONTEXT_NODE_MAX`
- order 221: `WEB_SEARCH_CONTEXT_URL_MAX` (constant), lines 5566-5566, exports `WEB_SEARCH_CONTEXT_URL_MAX`
- order 222: `RAG_CHUNK_CHARS` (constant), lines 5567-5567, exports `RAG_CHUNK_CHARS`
- order 223: `RAG_CHUNK_OVERLAP` (constant), lines 5568-5568, exports `RAG_CHUNK_OVERLAP`
- order 224: `RAG_MAX_CHUNKS_PER_DOC` (constant), lines 5569-5571, exports `RAG_MAX_CHUNKS_PER_DOC`
- order 225: `RAG_MAX_DOCUMENT_CHARS` (constant), lines 5572-5582, exports `RAG_MAX_DOCUMENT_CHARS`
- order 230: `RAG_MAX_QUERY_RESULTS` (constant), lines 5596-5596, exports `RAG_MAX_QUERY_RESULTS`
- order 231: `RAG_HIGH_RECALL_POOL_MULTIPLIER` (constant), lines 5597-5597, exports `RAG_HIGH_RECALL_POOL_MULTIPLIER`
- order 232: `RAG_HIGH_RECALL_MIN_POOL` (constant), lines 5598-5598, exports `RAG_HIGH_RECALL_MIN_POOL`
- order 233: `RAG_RETRIEVAL_MAX_PER_DOC` (constant), lines 5599-5599, exports `RAG_RETRIEVAL_MAX_PER_DOC`
- order 234: `RAG_BM25_K1` (constant), lines 5600-5603, exports `RAG_BM25_K1`
- order 235: `RAG_BM25_B` (constant), lines 5604-5604, exports `RAG_BM25_B`
- order 236: `RAG_BM25_SATURATION` (constant), lines 5605-5611, exports `RAG_BM25_SATURATION`
- order 237: `RAG_SYMBOL_EXACT_BOOST` (constant), lines 5612-5615, exports `RAG_SYMBOL_EXACT_BOOST`
- order 238: `RAG_INDEX_SNAPSHOT_FORMAT` (constant), lines 5616-5619, exports `RAG_INDEX_SNAPSHOT_FORMAT`
- order 239: `RAG_GRAPH_MAX_NODES` (constant), lines 5620-5620, exports `RAG_GRAPH_MAX_NODES`
- order 240: `RAG_TASK_HISTORY_LIMIT` (constant), lines 5621-5621, exports `RAG_TASK_HISTORY_LIMIT`
- order 241: `RAG_MODEL_MEDIA_MAX_BYTES` (constant), lines 5622-5622, exports `RAG_MODEL_MEDIA_MAX_BYTES`
- order 242: `RAG_MAX_IMPORT_FILES` (constant), lines 5623-5623, exports `RAG_MAX_IMPORT_FILES`
- order 243: `RAG_MAX_IMPORT_BATCH_ITEMS` (constant), lines 5624-5624, exports `RAG_MAX_IMPORT_BATCH_ITEMS`
- order 244: `RAG_MAX_IMPORT_BATCH_BYTES` (constant), lines 5625-5625, exports `RAG_MAX_IMPORT_BATCH_BYTES`
- order 245: `RAG_PDF_IMAGE_LIMIT` (constant), lines 5626-5626, exports `RAG_PDF_IMAGE_LIMIT`
- order 246: `RAG_QUERY_CONTEXT_CHARS` (constant), lines 5627-5627, exports `RAG_QUERY_CONTEXT_CHARS`
- order 247: `RAG_MAX_GLOBAL_COMMUNITIES` (constant), lines 5628-5628, exports `RAG_MAX_GLOBAL_COMMUNITIES`
- order 248: `RAG_MAX_COMMUNITY_MAP_SUPPORT` (constant), lines 5629-5629, exports `RAG_MAX_COMMUNITY_MAP_SUPPORT`
- order 249: `RAG_INCLUDE_FILENAME_ENTITIES_DEFAULT` (constant), lines 5630-5630, exports `RAG_INCLUDE_FILENAME_ENTITIES_DEFAULT`
- order 250: `RAG_DYNAMIC_NOISE_MIN_DOC_FREQ` (constant), lines 5631-5631, exports `RAG_DYNAMIC_NOISE_MIN_DOC_FREQ`
- order 251: `RAG_DYNAMIC_NOISE_MIN_COMMUNITY_FREQ` (constant), lines 5632-5632, exports `RAG_DYNAMIC_NOISE_MIN_COMMUNITY_FREQ`
- order 252: `RAG_DYNAMIC_NOISE_SOFT_DOC_RATIO` (constant), lines 5633-5633, exports `RAG_DYNAMIC_NOISE_SOFT_DOC_RATIO`
- order 253: `RAG_DYNAMIC_NOISE_HARD_DOC_RATIO` (constant), lines 5634-5634, exports `RAG_DYNAMIC_NOISE_HARD_DOC_RATIO`
- order 254: `RAG_DYNAMIC_NOISE_SOFT_COMMUNITY_RATIO` (constant), lines 5635-5635, exports `RAG_DYNAMIC_NOISE_SOFT_COMMUNITY_RATIO`
- order 255: `RAG_DYNAMIC_NOISE_HARD_COMMUNITY_RATIO` (constant), lines 5636-5636, exports `RAG_DYNAMIC_NOISE_HARD_COMMUNITY_RATIO`
- order 256: `RAG_MIN_SYNTHESIS_SCORE` (constant), lines 5637-5637, exports `RAG_MIN_SYNTHESIS_SCORE`
- order 257: `RAG_NO_EVIDENCE_THRESHOLD` (constant), lines 5638-5638, exports `RAG_NO_EVIDENCE_THRESHOLD`
- order 258: `RAG_WEAK_MATCH_SCORE_CAP` (constant), lines 5639-5639, exports `RAG_WEAK_MATCH_SCORE_CAP`
- order 259: `RAG_SYNTHESIS_MAX_PER_DOC` (constant), lines 5640-5640, exports `RAG_SYNTHESIS_MAX_PER_DOC`
- order 260: `RAG_WORKFLOW_ACCEPT_SCORE` (constant), lines 5641-5641, exports `RAG_WORKFLOW_ACCEPT_SCORE`
- order 261: `RAG_NO_EVIDENCE_MESSAGE` (constant), lines 5642-5642, exports `RAG_NO_EVIDENCE_MESSAGE`
- order 262: `RAG_CONTEXT_BUDGETS` (constant), lines 5643-5647, exports `RAG_CONTEXT_BUDGETS`
- order 263: `RAG_WEAK_EVIDENCE_MESSAGE` (constant), lines 5648-5648, exports `RAG_WEAK_EVIDENCE_MESSAGE`
- order 264: `RAG_EVIDENCE_SCHEMA_VERSION` (constant), lines 5649-5649, exports `RAG_EVIDENCE_SCHEMA_VERSION`
- order 265: `RAG_EVIDENCE_BATCH_CHARS` (constant), lines 5650-5653, exports `RAG_EVIDENCE_BATCH_CHARS`
- order 266: `RAG_EVALUATION_SUMMARY_CHARS` (constant), lines 5654-5657, exports `RAG_EVALUATION_SUMMARY_CHARS`
- order 267: `RAG_DENSE_DEFAULT_ENABLED` (constant), lines 5658-5658, exports `RAG_DENSE_DEFAULT_ENABLED`
- order 268: `RAG_EMBEDDING_MODE_VALUES` (constant), lines 5659-5659, exports `RAG_EMBEDDING_MODE_VALUES`
- order 269: `RAG_IMPORT_WORKER_COUNT` (constant), lines 5660-5663, exports `RAG_IMPORT_WORKER_COUNT`
- order 271: `RAG_PARSE_TIMEOUT_SECONDS` (constant), lines 5668-5671, exports `RAG_PARSE_TIMEOUT_SECONDS`
- order 1155: `RAG_TERM_GROUPS` (constant), lines 106539-111172, exports `RAG_TERM_GROUPS`
- order 1156: `RAG_RESEARCH_HINTS` (constant), lines 111173-111194, exports `RAG_RESEARCH_HINTS`
- order 1157: `RAG_CODE_HINTS` (constant), lines 111195-111205, exports `RAG_CODE_HINTS`
- order 1158: `RAG_SHORT_TOKEN_ALLOWLIST` (constant), lines 111206-111221, exports `RAG_SHORT_TOKEN_ALLOWLIST`
- order 1159: `RAG_EN_STOPWORDS` (constant), lines 111222-111294, exports `RAG_EN_STOPWORDS`
- order 1160: `RAG_ZH_STOPWORDS` (constant), lines 111295-111331, exports `RAG_ZH_STOPWORDS`
- order 1161: `RAG_GENERIC_ENTITY_TERMS_EN` (constant), lines 111332-111410, exports `RAG_GENERIC_ENTITY_TERMS_EN`
- order 1162: `RAG_GENERIC_ENTITY_TERMS_ZH` (constant), lines 111411-111453, exports `RAG_GENERIC_ENTITY_TERMS_ZH`
- order 1163: `RAG_STRUCTURAL_ENTITY_PATTERNS` (constant), lines 111454-111472, exports `RAG_STRUCTURAL_ENTITY_PATTERNS`
- order 1195: `CODE_LIBRARY_IGNORED_DIRS` (constant), lines 112430-112439, exports `CODE_LIBRARY_IGNORED_DIRS`
- order 1196: `CODE_LIBRARY_LANGUAGE_BY_EXT` (constant), lines 112440-112496, exports `CODE_LIBRARY_LANGUAGE_BY_EXT`
- order 1197: `CODE_LIBRARY_SPECIAL_FILENAMES` (constant), lines 112497-112503, exports `CODE_LIBRARY_SPECIAL_FILENAMES`

### `rag/index.py`

- order 1200: `_code_module_name` (function), lines 112528-112544, exports `_code_module_name`
- order 1201: `_code_choose_community` (function), lines 112545-112554, exports `_code_choose_community`
- order 1202: `_code_query_terms` (function), lines 112555-112569, exports `_code_query_terms`
- order 1211: `TFGraphIDFIndex` (class), lines 113700-115394, exports `TFGraphIDFIndex`
- order 1220: `CodeGraphIndex` (class), lines 118681-119169, exports `CodeGraphIndex`

### `rag/ingestion.py`

- order 1179: `_rag_trigram_set` (function), lines 111850-111857, exports `_rag_trigram_set`
- order 1180: `_rag_jaccard_sim` (function), lines 111858-111867, exports `_rag_jaccard_sim`
- order 1181: `_rag_mmr_select` (function), lines 111868-111917, exports `_rag_mmr_select`
- order 1186: `_rag_embed_text` (function), lines 112052-112075, exports `_rag_embed_text`
- order 1187: `_rag_embed_batch` (function), lines 112076-112084, exports `_rag_embed_batch`
- order 1188: `_rag_window_for_query` (function), lines 112085-112099, exports `_rag_window_for_query`
- order 1189: `_rag_focused_excerpt` (function), lines 112100-112142, exports `_rag_focused_excerpt`
- order 1190: `_rag_query_variants` (function), lines 112143-112182, exports `_rag_query_variants`
- order 1191: `_rag_parse_segments` (function), lines 112183-112245, exports `_rag_parse_segments`
- order 1192: `_rag_boundary_split` (function), lines 112246-112303, exports `_rag_boundary_split`
- order 1218: `_rag_parse_file_worker` (function), lines 117780-117796, exports `_rag_parse_file_worker`
- order 1219: `RAGIngestionService` (class), lines 117797-118680, exports `RAGIngestionService`
- order 1222: `CodeIngestionService` (class), lines 119461-119548, exports `CodeIngestionService`

### `rag/parsers.py`

- order 1164: `EvidenceRecord` (class), lines 111473-111507, exports `EvidenceRecord`
- order 1165: `_rag_float` (function), lines 111508-111514, exports `_rag_float`
- order 1166: `_rag_evidence_source_type` (function), lines 111515-111531, exports `_rag_evidence_source_type`
- order 1167: `_rag_normalize_evidence_record` (function), lines 111532-111587, exports `_rag_normalize_evidence_record`
- order 1168: `_rag_validate_evidence_record` (function), lines 111588-111630, exports `_rag_validate_evidence_record`
- order 1169: `_rag_evidence_batches` (function), lines 111631-111648, exports `_rag_evidence_batches`
- order 1170: `_rag_safe_name` (function), lines 111649-111654, exports `_rag_safe_name`
- order 1171: `_rag_detect_language` (function), lines 111655-111671, exports `_rag_detect_language`
- order 1172: `_rag_cjk_ngrams` (function), lines 111672-111686, exports `_rag_cjk_ngrams`
- order 1173: `_rag_is_noise_token` (function), lines 111687-111708, exports `_rag_is_noise_token`
- order 1174: `_rag_entity_allowed` (function), lines 111709-111723, exports `_rag_entity_allowed`
- order 1175: `_rag_filter_entities` (function), lines 111724-111740, exports `_rag_filter_entities`
- order 1176: `_rag_filename_entity_aliases` (function), lines 111741-111776, exports `_rag_filename_entity_aliases`
- order 1177: `_rag_apply_filename_entity_policy` (function), lines 111777-111809, exports `_rag_apply_filename_entity_policy`
- order 1178: `_rag_choose_community` (function), lines 111810-111849, exports `_rag_choose_community`
- order 1182: `_rag_tokenize` (function), lines 111918-111971, exports `_rag_tokenize`
- order 1183: `_rag_expand_tokens` (function), lines 111972-111995, exports `_rag_expand_tokens`
- order 1184: `_rag_extract_entities` (function), lines 111996-112014, exports `_rag_extract_entities`
- order 1185: `_rag_classify_document` (function), lines 112015-112051, exports `_rag_classify_document`
- order 1193: `_rag_structure_outline` (function), lines 112304-112342, exports `_rag_structure_outline`
- order 1194: `_rag_chunk_text` (function), lines 112343-112429, exports `_rag_chunk_text`
- order 1198: `_code_language_from_name` (function), lines 112504-112522, exports `_code_language_from_name`
- order 1199: `_code_is_test_path` (function), lines 112523-112527, exports `_code_is_test_path`
- order 1203: `_CallCollector` (class), lines 112570-112584, exports `_CallCollector`
- order 1204: `_ALGO_COMPLEXITY_RE` (assignment), lines 112585-112587, exports `_ALGO_COMPLEXITY_RE`
- order 1205: `_ALGO_STEP_RE` (assignment), lines 112588-112588, exports `_ALGO_STEP_RE`
- order 1206: `_ALGO_MATH_VARS` (assignment), lines 112589-112589, exports `_ALGO_MATH_VARS`
- order 1207: `_ALGO_DOC_KEYWORDS` (assignment), lines 112590-112590, exports `_ALGO_DOC_KEYWORDS`
- order 1208: `_detect_algo_chunk` (function), lines 112591-112616, exports `_detect_algo_chunk`
- order 1209: `CodeContentParser` (class), lines 112617-113183, exports `CodeContentParser`
- order 1210: `RAGContentParser` (class), lines 113184-113699, exports `RAGContentParser`

### `rag/store.py`

- order 1212: `RAGLibraryStore` (class), lines 115395-116033, exports `RAGLibraryStore`
- order 1213: `WikiStore` (class), lines 116034-116589, exports `WikiStore`
- order 1214: `UserMemoryStore` (class), lines 116590-117267, exports `UserMemoryStore`
- order 1215: `UserInteractionOptimizer` (class), lines 117268-117336, exports `UserInteractionOptimizer`
- order 1216: `UserIntentProfiler` (class), lines 117337-117378, exports `UserIntentProfiler`
- order 1217: `WorkflowMemoryStore` (class), lines 117379-117779, exports `WorkflowMemoryStore`
- order 1221: `CodeLibraryStore` (class), lines 119170-119460, exports `CodeLibraryStore`

### `rag/web_search.py`

- order 839: `_agent_web_bool` (function), lines 10790-10797, exports `_agent_web_bool`
- order 840: `_agent_web_int` (function), lines 10798-10805, exports `_agent_web_int`
- order 841: `_agent_web_host_is_local_name` (function), lines 10806-10812, exports `_agent_web_host_is_local_name`
- order 842: `_agent_web_ip_is_blocked` (function), lines 10813-10827, exports `_agent_web_ip_is_blocked`
- order 843: `_agent_web_canonical_url` (function), lines 10828-10857, exports `_agent_web_canonical_url`
- order 844: `_agent_web_domain_to_seed` (function), lines 10858-10869, exports `_agent_web_domain_to_seed`
- order 845: `_agent_web_query_terms` (function), lines 10870-10887, exports `_agent_web_query_terms`
- order 846: `_agent_web_query_domain_hints` (function), lines 10888-10928, exports `_agent_web_query_domain_hints`
- order 847: `_agent_web_query_needs_fresh_network` (function), lines 10929-10951, exports `_agent_web_query_needs_fresh_network`
- order 848: `_agent_web_extract_text_snippet` (function), lines 10952-10969, exports `_agent_web_extract_text_snippet`
- order 849: `AgentWebHTMLParser` (class), lines 10970-11049, exports `AgentWebHTMLParser`
- order 850: `_agent_web_decompress_bytes` (function), lines 11050-11073, exports `_agent_web_decompress_bytes`
- order 851: `_agent_web_charset_candidates` (function), lines 11074-11132, exports `_agent_web_charset_candidates`
- order 852: `_agent_web_decode_text_bytes` (function), lines 11133-11167, exports `_agent_web_decode_text_bytes`
- order 853: `AgentWebSearchEngine` (class), lines 11168-12948, exports `AgentWebSearchEngine`

### `server/http.py`

- order 713: `admin_language_payload` (function), lines 7763-7774, exports `admin_language_payload`
- order 828: `_UI_TRUNCATION_MARKER` (assignment), lines 10409-10411, exports `_UI_TRUNCATION_MARKER`
- order 829: `_ui_trim_text` (function), lines 10412-10420, exports `_ui_trim_text`
- order 830: `_bounded_ui_value` (function), lines 10421-10481, exports `_bounded_ui_value`
- order 831: `_bounded_ui_row` (function), lines 10482-10533, exports `_bounded_ui_row`
- order 832: `_bounded_ui_rows` (function), lines 10534-10582, exports `_bounded_ui_rows`
- order 833: `_enforce_ui_payload_budget` (function), lines 10583-10627, exports `_enforce_ui_payload_budget`
- order 834: `_apply_lite_snapshot_bounds` (function), lines 10628-10683, exports `_apply_lite_snapshot_bounds`
- order 1260: `AgentHTTPServer` (class), lines 136867-136906, exports `AgentHTTPServer`
- order 1263: `Handler` (class), lines 138108-140037, exports `Handler`
- order 1266: `SkillsReviewHandler` (class), lines 140846-140959, exports `SkillsReviewHandler`
- order 1270: `CollaborationHandler` (class), lines 143017-143487, exports `CollaborationHandler`

### `server/rag_admin.py`

- order 1265: `_RagAdminAuthMixin` (class), lines 140688-140845, exports `_RagAdminAuthMixin`
- order 1267: `RagAdminHandler` (class), lines 140960-141160, exports `RagAdminHandler`
- order 1268: `CodeAdminHandler` (class), lines 141161-141359, exports `CodeAdminHandler`

### `server/skills.py`

- order 1264: `SkillsHandler` (class), lines 140038-140687, exports `SkillsHandler`

### `session/manager.py`

- order 750: `SessionCreationLimitExceeded` (class), lines 8967-8972, exports `SessionCreationLimitExceeded`
- order 1143: `SessionManager` (class), lines 96950-99493, exports `SessionManager`

### `session/state.py`

- order 1142: `SessionState` (class), lines 33068-96949, exports `SessionState`

### `skills/embedded.py`

- order 1015: `EMBEDDED_SKILLS_ARCHIVE_B64` (constant), lines 19386-19387, exports `EMBEDDED_SKILLS_ARCHIVE_B64`
- order 1016: `EMBEDDED_SKILLS_ARCHIVE_SHA256` (constant), lines 19388-19388, exports `EMBEDDED_SKILLS_ARCHIVE_SHA256`
- order 1017: `EMBEDDED_SKILLS_ARCHIVE_FILES` (constant), lines 19389-19411, exports `EMBEDDED_SKILLS_ARCHIVE_FILES`
- order 1042: `BUILTIN_CLAWHUB_SKILLS_VERSION` (constant), lines 22647-22649, exports `BUILTIN_CLAWHUB_SKILLS_VERSION`
- order 1043: `EMBEDDED_CLAWHUB_SKILLS_ARCHIVE_B64` (constant), lines 22650-22895, exports `EMBEDDED_CLAWHUB_SKILLS_ARCHIVE_B64`
- order 1045: `MCP_BUILDER_SKILL_MD` (constant), lines 22943-23117, exports `MCP_BUILDER_SKILL_MD`
- order 1048: `SKILL_PROTOCOL_LOCAL` (constant), lines 23149-23150, exports `SKILL_PROTOCOL_LOCAL`
- order 1049: `SKILL_PROTOCOL_CLAWHUB` (constant), lines 23151-23151, exports `SKILL_PROTOCOL_CLAWHUB`
- order 1050: `SKILL_PROTOCOL_HTTP_JSON` (constant), lines 23152-23152, exports `SKILL_PROTOCOL_HTTP_JSON`
- order 1051: `SKILL_PROTOCOL_SPECS` (constant), lines 23153-23185, exports `SKILL_PROTOCOL_SPECS`

### `skills/provisioning.py`

- order 1018: `ensure_embedded_skills_at_root` (function), lines 19412-19477, exports `ensure_embedded_skills_at_root`
- order 1019: `ensure_embedded_skills` (function), lines 19478-19481, exports `ensure_embedded_skills`
- order 1021: `detect_upload_parser_capabilities` (function), lines 19488-19504, exports `detect_upload_parser_capabilities`
- order 1022: `_render_cap_markdown` (function), lines 19505-19520, exports `_render_cap_markdown`
- order 1023: `_write_text_if_changed` (function), lines 19521-19527, exports `_write_text_if_changed`
- order 1024: `ensure_generated_document_skills` (function), lines 19528-19617, exports `ensure_generated_document_skills`
- order 1025: `ensure_generated_image_coding_feedback_skill` (function), lines 19618-19718, exports `ensure_generated_image_coding_feedback_skill`
- order 1026: `_skill_knowledge_files` (function), lines 19719-19739, exports `_skill_knowledge_files`
- order 1027: `analyze_skill_building_knowledge` (function), lines 19740-19795, exports `analyze_skill_building_knowledge`
- order 1028: `_sanitize_skill_slug` (function), lines 19796-19799, exports `_sanitize_skill_slug`
- order 1029: `_build_skills_gen_skill_content` (function), lines 19800-19832, exports `_build_skills_gen_skill_content`
- order 1030: `ensure_generated_skills_gen_skill` (function), lines 19833-19838, exports `ensure_generated_skills_gen_skill`
- order 1031: `ensure_generated_execution_recovery_skill` (function), lines 19839-19923, exports `ensure_generated_execution_recovery_skill`
- order 1032: `ensure_generated_systematic_debugging_skill` (function), lines 19924-20197, exports `ensure_generated_systematic_debugging_skill`
- order 1033: `ensure_generated_code_engineering_mastery_skill` (function), lines 20198-20317, exports `ensure_generated_code_engineering_mastery_skill`
- order 1034: `ensure_generated_smart_file_navigation_skill` (function), lines 20318-20434, exports `ensure_generated_smart_file_navigation_skill`
- order 1035: `ensure_generated_html_frontend_report_skills` (function), lines 20435-20643, exports `ensure_generated_html_frontend_report_skills`
- order 1036: `ensure_generated_deep_research_skills` (function), lines 20644-20913, exports `ensure_generated_deep_research_skills`
- order 1037: `ensure_generated_research_scientific_skills` (function), lines 20914-21551, exports `ensure_generated_research_scientific_skills`
- order 1038: `ensure_generated_rag_mastery_skills` (function), lines 21552-21853, exports `ensure_generated_rag_mastery_skills`
- order 1039: `ensure_generated_multimodal_comprehension_skills` (function), lines 21854-22548, exports `ensure_generated_multimodal_comprehension_skills`
- order 1040: `ensure_generated_runtime_skills_manifest` (function), lines 22549-22583, exports `ensure_generated_runtime_skills_manifest`
- order 1041: `ensure_generated_agent_web_search_skill` (function), lines 22584-22646, exports `ensure_generated_agent_web_search_skill`
- order 1044: `ensure_embedded_clawhub_skills` (function), lines 22896-22942, exports `ensure_embedded_clawhub_skills`
- order 1046: `ensure_generated_mcp_builder_skill` (function), lines 23118-23129, exports `ensure_generated_mcp_builder_skill`
- order 1047: `ensure_runtime_skills` (function), lines 23130-23148, exports `ensure_runtime_skills`

### `skills/store.py`

- order 556: `_skill_term_match` (function), lines 6559-6579, exports `_skill_term_match`
- order 1052: `_BUILTIN_SKILLS` (assignment), lines 23186-23294, exports `_BUILTIN_SKILLS`
- order 1053: `SkillStore` (class), lines 23295-25210, exports `SkillStore`

### `skills/studio.py`

- order 1245: `SkillsStudioError` (class), lines 123356-123365, exports `SkillsStudioError`
- order 1246: `_studio_slug` (function), lines 123366-123381, exports `_studio_slug`
- order 1247: `_studio_hash` (function), lines 123382-123385, exports `_studio_hash`
- order 1248: `_studio_cookie_value` (function), lines 123386-123395, exports `_studio_cookie_value`
- order 1249: `SkillsStudioStore` (class), lines 123396-125253, exports `SkillsStudioStore`

### `utils/compress.py`

- order 857: `compress_text_blob` (function), lines 13113-13119, exports `compress_text_blob`
- order 858: `decompress_text_blob` (function), lines 13120-13129, exports `decompress_text_blob`

### `utils/crypto.py`

- order 958: `CryptoBox` (class), lines 16117-16270, exports `CryptoBox`

### `utils/errors.py`

- order 885: `EmptyActionError` (class), lines 13746-13749, exports `EmptyActionError`
- order 1055: `ProcessManagerError` (class), lines 25346-25351, exports `ProcessManagerError`

### `utils/files.py`

- order 707: `_normalize_js_lib_asset_ref` (function), lines 7633-7648, exports `_normalize_js_lib_asset_ref`
- order 708: `_resolve_js_lib_asset_path` (function), lines 7649-7680, exports `_resolve_js_lib_asset_path`
- order 709: `_discover_extra_js_lib_files` (function), lines 7681-7713, exports `_discover_extra_js_lib_files`
- order 803: `safe_path` (function), lines 9822-9832, exports `safe_path`
- order 804: `_safe_js_filename` (function), lines 9833-9841, exports `_safe_js_filename`
- order 805: `_sha256_bytes` (function), lines 9842-9844, exports `_sha256_bytes`
- order 806: `_sha256_file` (function), lines 9845-9854, exports `_sha256_file`
- order 807: `_download_http_bytes` (function), lines 9855-9864, exports `_download_http_bytes`
- order 808: `offline_js_lib_root` (function), lines 9865-9867, exports `offline_js_lib_root`
- order 809: `_offline_js_entry_relative_path` (function), lines 9868-9873, exports `_offline_js_entry_relative_path`
- order 810: `_archive_member_relative_path` (function), lines 9874-9884, exports `_archive_member_relative_path`
- order 811: `_path_size_bytes` (function), lines 9885-9901, exports `_path_size_bytes`
- order 812: `_extract_archive_to_dir` (function), lines 9902-9943, exports `_extract_archive_to_dir`
- order 813: `_package_required_paths` (function), lines 9944-9951, exports `_package_required_paths`
- order 814: `_package_required_globs` (function), lines 9952-9968, exports `_package_required_globs`
- order 815: `_package_install_ready` (function), lines 9969-9991, exports `_package_install_ready`
- order 816: `_postprocess_offline_js_package` (function), lines 9992-10028, exports `_postprocess_offline_js_package`
- order 817: `_ensure_offline_js_package` (function), lines 10029-10073, exports `_ensure_offline_js_package`
- order 818: `_render_offline_js_catalog_md` (function), lines 10074-10091, exports `_render_offline_js_catalog_md`
- order 819: `load_offline_js_lib_index` (function), lines 10092-10102, exports `load_offline_js_lib_index`
- order 820: `ensure_offline_js_libs` (function), lines 10103-10261, exports `ensure_offline_js_libs`
- order 821: `_offline_js_catalog_entry_for_asset` (function), lines 10262-10282, exports `_offline_js_catalog_entry_for_asset`
- order 822: `ensure_offline_js_asset` (function), lines 10283-10340, exports `ensure_offline_js_asset`
- order 823: `_normalize_external_js_url` (function), lines 10341-10346, exports `_normalize_external_js_url`
- order 824: `is_external_js_src` (function), lines 10347-10350, exports `is_external_js_src`
- order 825: `match_offline_js_catalog_by_url` (function), lines 10351-10368, exports `match_offline_js_catalog_by_url`
- order 826: `cache_external_js_url` (function), lines 10369-10404, exports `cache_external_js_url`
- order 961: `try_read_text` (function), lines 16514-16523, exports `try_read_text`
- order 983: `_start_offline_js_warmup` (function), lines 18117-18134, exports `_start_offline_js_warmup`

### `utils/http.py`

- order 123: `_URL_OPEN_ORIGINAL` (assignment), lines 5142-5142, exports `_URL_OPEN_ORIGINAL`
- order 124: `_HTTP_SSL_CONTEXT` (assignment), lines 5143-5143, exports `_HTTP_SSL_CONTEXT`
- order 151: `_shared_http_ssl_context` (function), lines 5207-5230, exports `_shared_http_ssl_context`
- order 152: `urlopen` (function), lines 5231-5240, exports `urlopen`
- order 796: `json_response_bytes` (function), lines 9767-9769, exports `json_response_bytes`
- order 797: `read_http_json_body` (function), lines 9770-9783, exports `read_http_json_body`
- order 798: `close_if_http_request_body_unread` (function), lines 9784-9797, exports `close_if_http_request_body_unread`

### `utils/json_utils.py`

- order 175: `JSON_FSYNC_ENABLED` (constant), lines 5512-5512, exports `JSON_FSYNC_ENABLED`
- order 795: `json_dumps` (function), lines 9763-9766, exports `json_dumps`
- order 873: `parse_tool_arguments` (function), lines 13493-13503, exports `parse_tool_arguments`
- order 874: `repair_truncated_json_object` (function), lines 13504-13558, exports `repair_truncated_json_object`
- order 875: `parse_tool_arguments_with_error` (function), lines 13559-13590, exports `parse_tool_arguments_with_error`
- order 876: `_is_valid_json_object` (function), lines 13591-13596, exports `_is_valid_json_object`
- order 877: `_scan_top_level_json_objects` (function), lines 13597-13620, exports `_scan_top_level_json_objects`
- order 878: `reconstruct_streamed_tool_args` (function), lines 13621-13665, exports `reconstruct_streamed_tool_args`
- order 899: `parse_json_object` (function), lines 14020-14026, exports `parse_json_object`
- order 900: `decode_model_json_object` (function), lines 14027-14061, exports `decode_model_json_object`
- order 902: `standard_model_json_object` (function), lines 14066-14129, exports `standard_model_json_object`
- order 903: `semantic_json_repair_request` (function), lines 14130-14146, exports `semantic_json_repair_request`
- order 904: `validate_semantic_json_repair` (function), lines 14147-14176, exports `validate_semantic_json_repair`
- order 906: `extract_json_object_from_text` (function), lines 14229-14253, exports `extract_json_object_from_text`
- order 962: `_json_default_copy` (function), lines 16524-16530, exports `_json_default_copy`
- order 963: `_read_json_file` (function), lines 16531-16552, exports `_read_json_file`
- order 964: `_write_json_file` (function), lines 16553-16581, exports `_write_json_file`

### `utils/media.py`

- order 700: `_capability_probe_png_bytes` (function), lines 7271-7285, exports `_capability_probe_png_bytes`
- order 701: `_capability_probe_audio_bytes` (function), lines 7286-7297, exports `_capability_probe_audio_bytes`
- order 702: `_capability_probe_video_bytes` (function), lines 7298-7302, exports `_capability_probe_video_bytes`
- order 765: `guess_mime_from_name` (function), lines 9315-9319, exports `guess_mime_from_name`
- order 766: `_convert_image_to_safe_format` (function), lines 9320-9339, exports `_convert_image_to_safe_format`
- order 767: `guess_ext_from_mime` (function), lines 9340-9348, exports `guess_ext_from_mime`

### `utils/misc.py`

- order 768: `now_ts` (function), lines 9349-9351, exports `now_ts`
- order 769: `_benign_socket_log_lock` (assignment), lines 9352-9354, exports `_benign_socket_log_lock`
- order 770: `_benign_socket_log_state` (assignment), lines 9355-9355, exports `_benign_socket_log_state`
- order 772: `is_benign_socket_error` (function), lines 9371-9391, exports `is_benign_socket_error`
- order 773: `_socket_error_code` (function), lines 9392-9403, exports `_socket_error_code`
- order 774: `_log_benign_socket_error_limited` (function), lines 9404-9440, exports `_log_benign_socket_error_limited`
- order 775: `swallow_benign_socket_error` (function), lines 9441-9447, exports `swallow_benign_socket_error`
- order 776: `normalize_timeout_seconds` (function), lines 9448-9463, exports `normalize_timeout_seconds`
- order 777: `detect_local_lan_ip` (function), lines 9464-9475, exports `detect_local_lan_ip`
- order 778: `_LOCAL_LAN_IP_CACHE` (assignment), lines 9476-9477, exports `_LOCAL_LAN_IP_CACHE`
- order 779: `detect_local_lan_ip_cached` (function), lines 9478-9491, exports `detect_local_lan_ip_cached`
- order 799: `make_id` (function), lines 9798-9800, exports `make_id`
- order 800: `sanitize_profile_id` (function), lines 9801-9804, exports `sanitize_profile_id`
- order 956: `user_id_from_ip` (function), lines 16076-16083, exports `user_id_from_ip`
- order 960: `_meta_string_list` (function), lines 16500-16513, exports `_meta_string_list`
- order 1020: `_module_exists` (function), lines 19482-19487, exports `_module_exists`

### `utils/sqlite.py`

- order 70: `_ClosingSQLiteConnection` (class), lines 74-83, exports `_ClosingSQLiteConnection`
- order 71: `_connect_sqlite` (function), lines 84-117, exports `_connect_sqlite`
- order 1272: `sqlite_failure_diagnostics` (function), lines 143706-143790, exports `sqlite_failure_diagnostics`

### `utils/text.py`

- order 163: `MAX_TOOL_OUTPUT` (constant), lines 5500-5500, exports `MAX_TOOL_OUTPUT`
- order 512: `SOCKET_NOISE_LINE_PATTERNS` (constant), lines 6312-6317, exports `SOCKET_NOISE_LINE_PATTERNS`
- order 771: `filter_runtime_noise_lines` (function), lines 9356-9370, exports `filter_runtime_noise_lines`
- order 784: `safe_utf8_bytes` (function), lines 9616-9620, exports `safe_utf8_bytes`
- order 785: `escape_invalid_utf8_text` (function), lines 9621-9623, exports `escape_invalid_utf8_text`
- order 786: `sanitize_utf8_surrogates` (function), lines 9624-9637, exports `sanitize_utf8_surrogates`
- order 787: `decode_utf8_replace` (function), lines 9638-9642, exports `decode_utf8_replace`
- order 827: `trim` (function), lines 10405-10408, exports `trim`
- order 835: `is_synthetic_public_progress` (function), lines 10684-10703, exports `is_synthetic_public_progress`
- order 837: `display_clean` (function), lines 10756-10770, exports `display_clean`
- order 838: `short_title_from` (function), lines 10771-10789, exports `short_title_from`
- order 854: `_fmt_export_ts` (function), lines 12949-12959, exports `_fmt_export_ts`
- order 855: `_html_esc` (function), lines 12960-12963, exports `_html_esc`
- order 856: `_text_to_minimal_pdf` (function), lines 12964-13112, exports `_text_to_minimal_pdf`
- order 859: `normalize_embedded_newlines` (function), lines 13130-13139, exports `normalize_embedded_newlines`
- order 860: `_map_todo_status_token` (function), lines 13140-13178, exports `_map_todo_status_token`
- order 861: `_TODO_SHORT_ID_RE` (assignment), lines 13179-13186, exports `_TODO_SHORT_ID_RE`
- order 862: `_TODO_SHORT_ID_TAG_RE` (assignment), lines 13187-13187, exports `_TODO_SHORT_ID_TAG_RE`
- order 863: `normalize_todo_short_id` (function), lines 13188-13193, exports `normalize_todo_short_id`
- order 864: `strip_todo_short_id_tag` (function), lines 13194-13202, exports `strip_todo_short_id_tag`
- order 865: `split_todo_status_text` (function), lines 13203-13207, exports `split_todo_status_text`
- order 866: `split_todo_status_text_with_id` (function), lines 13208-13281, exports `split_todo_status_text_with_id`
- order 867: `extract_todo_rows_from_text` (function), lines 13282-13364, exports `extract_todo_rows_from_text`
- order 868: `decode_structured_todo_container` (function), lines 13365-13383, exports `decode_structured_todo_container`
- order 869: `infer_todo_status_from_text` (function), lines 13384-13392, exports `infer_todo_status_from_text`
- order 870: `split_structured_todo_content` (function), lines 13393-13448, exports `split_structured_todo_content`
- order 871: `is_todo_transport_metadata` (function), lines 13449-13462, exports `is_todo_transport_metadata`
- order 872: `normalize_work_text` (function), lines 13463-13492, exports `normalize_work_text`
- order 986: `make_unified_diff` (function), lines 18178-18196, exports `make_unified_diff`
- order 987: `_skip_row` (function), lines 18197-18202, exports `_skip_row`
- order 988: `_row_is_hot` (function), lines 18203-18206, exports `_row_is_hot`
- order 989: `_hotspot_index` (function), lines 18207-18230, exports `_hotspot_index`
- order 990: `_compress_rows_keep_hotspot` (function), lines 18231-18280, exports `_compress_rows_keep_hotspot`
- order 991: `_focused_diff_rows_from_opcodes` (function), lines 18281-18415, exports `_focused_diff_rows_from_opcodes`
- order 992: `make_numbered_diff` (function), lines 18416-18448, exports `make_numbered_diff`
- order 993: `render_numbered_diff_text` (function), lines 18449-18462, exports `render_numbered_diff_text`

### `web/admin_assets.py`

- order 1152: `ADMIN_INDEX_HTML` (constant), lines 105546-105863, exports `ADMIN_INDEX_HTML`
- order 1153: `ADMIN_CSS` (constant), lines 105864-106026, exports `ADMIN_CSS`
- order 1154: `ADMIN_JS` (constant), lines 106027-106538, exports `ADMIN_JS`

### `web/assets.py`

- order 1144: `INDEX_HTML` (constant), lines 99494-99755, exports `INDEX_HTML`
- order 1145: `APP_CSS` (constant), lines 99756-100298, exports `APP_CSS`
- order 1146: `APP_JS` (constant), lines 100299-105082, exports `APP_JS`
- order 1147: `APP_CSS` (constant), lines 105083-105103, exports `APP_CSS`
- order 1148: `APP_TS` (constant), lines 105104-105143, exports `APP_TS`

### `web/skills_assets.py`

- order 1149: `SKILLS_INDEX_HTML` (constant), lines 105144-105299, exports `SKILLS_INDEX_HTML`
- order 1150: `SKILLS_EXTRA_CSS` (constant), lines 105300-105399, exports `SKILLS_EXTRA_CSS`
- order 1151: `SKILLS_APP_JS` (constant), lines 105400-105545, exports `SKILLS_APP_JS`
