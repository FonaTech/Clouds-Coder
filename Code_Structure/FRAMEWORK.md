# Code_Structure Framework

## Overview

- Source snapshot: `Clouds_Coder.py` (1276 top-level statements)
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
| `_imports.py` | 76 | 94 | — | 1–5116 |
| `admin/auth.py` | 3 | 3 | `admin/constants.py`, `utils/misc.py`, `utils/sqlite.py` | 16059–16901 |
| `admin/config.py` | 8 | 8 | `config/constants.py`, `config/paths.py`, `config/settings.py`, `llm/constants.py`, `llm/gate.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` | 17649–18152 |
| `admin/constants.py` | 16 | 16 | — | 5123–125237 |
| `agent/background.py` | 1 | 1 | `agent/process.py`, `config/constants.py`, `ide/sandbox.py`, `utils/misc.py`, `utils/text.py` | 25687–26312 |
| `agent/bus.py` | 1 | 1 | `config/constants.py`, `utils/crypto.py`, `utils/misc.py` | 26313–26378 |
| `agent/context.py` | 2 | 2 | `agent/tools.py` | 5856–14040 |
| `agent/errors.py` | 1 | 1 | — | 13725–13728 |
| `agent/events.py` | 1 | 1 | — | 18879–18933 |
| `agent/evidence.py` | 2 | 2 | `utils/sqlite.py` | 32703–33042 |
| `agent/process.py` | 9 | 9 | `ide/sandbox.py`, `utils/errors.py`, `utils/misc.py`, `utils/text.py` | 6176–25686 |
| `agent/tasks.py` | 1 | 1 | `utils/crypto.py`, `utils/json_utils.py`, `utils/misc.py` | 25186–25320 |
| `agent/todo.py` | 1 | 1 | `config/constants.py`, `config/settings.py`, `utils/misc.py`, `utils/text.py` | 18934–19360 |
| `agent/tools.py` | 17 | 21 | `config/constants.py`, `config/settings.py`, `utils/text.py` | 18758–32170 |
| `agent/worktree.py` | 1 | 1 | `agent/process.py`, `agent/tasks.py`, `config/constants.py`, `utils/crypto.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` | 26379–26591 |
| `app/context.py` | 1 | 1 | `admin/auth.py`, `admin/config.py`, `admin/constants.py`, `agent/process.py`, `agent/tools.py`, `app/services.py`, `collaboration/core.py`, `config/bootstrap.py`, `config/constants.py`, `config/paths.py`, `config/settings.py`, `ide/assets.py`, `ide/auth.py`, `ide/errors.py`, `ide/events.py`, `ide/preview.py`, `ide/sandbox.py`, `ide/toolchains.py`, `llm/client.py`, `llm/constants.py`, `llm/gate.py`, `llm/utils.py`, `mcp/driver.py`, `rag/assets.py`, `rag/constants.py`, `rag/ingestion.py`, `rag/parsers.py`, `rag/store.py`, `server/http.py`, `session/manager.py`, `session/state.py`, `skills/provisioning.py`, `skills/store.py`, `skills/studio.py`, `utils/crypto.py`, `utils/files.py`, `utils/http.py`, `utils/json_utils.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py`, `web/assets.py`, `web/skills_assets.py` | 125303–136841 |
| `app/main.py` | 2 | 1 | `admin/config.py`, `admin/constants.py`, `agent/tools.py`, `app/context.py`, `collaboration/watcher.py`, `config/constants.py`, `config/paths.py`, `config/settings.py`, `ide/handler.py`, `llm/constants.py`, `llm/gate.py`, `llm/utils.py`, `mcp/constants.py`, `mcp/service.py`, `rag/constants.py`, `server/http.py`, `server/rag_admin.py`, `server/skills.py`, `skills/provisioning.py`, `utils/files.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` | 143859–145848 |
| `app/services.py` | 2 | 2 | `admin/constants.py`, `config/settings.py`, `skills/embedded.py`, `skills/store.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/sqlite.py`, `utils/text.py` | 136882–138082 |
| `collaboration/core.py` | 23 | 23 | `config/constants.py`, `utils/sqlite.py` | 1735–4976 |
| `collaboration/watcher.py` | 2 | 2 | `utils/misc.py`, `utils/sqlite.py`, `utils/text.py` | 143766–143858 |
| `config/bootstrap.py` | 6 | 6 | `config/constants.py`, `config/settings.py`, `utils/json_utils.py`, `utils/misc.py` | 123–16614 |
| `config/constants.py` | 515 | 510 | `config/bootstrap.py`, `rag/constants.py` | 1686–125233 |
| `config/paths.py` | 13 | 13 | `agent/process.py`, `utils/crypto.py`, `utils/text.py` | 5122–9796 |
| `config/settings.py` | 71 | 71 | `agent/tools.py`, `config/constants.py`, `config/paths.py`, `ide/preview.py`, `llm/constants.py`, `llm/gate.py`, `llm/utils.py`, `rag/constants.py`, `skills/provisioning.py`, `utils/http.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` | 7689–31405 |
| `ide/assets.py` | 8 | 3 | — | 122148–123305 |
| `ide/auth.py` | 2 | 2 | `admin/auth.py`, `admin/constants.py`, `config/constants.py`, `utils/misc.py`, `utils/sqlite.py`, `utils/text.py` | 16902–17633 |
| `ide/errors.py` | 2 | 2 | — | 17634–17648 |
| `ide/events.py` | 1 | 1 | `config/constants.py`, `utils/text.py` | 10679–10730 |
| `ide/handler.py` | 1 | 1 | `admin/auth.py`, `app/context.py`, `collaboration/core.py`, `config/constants.py`, `config/settings.py`, `ide/auth.py`, `ide/errors.py`, `ide/events.py`, `session/manager.py`, `session/state.py`, `utils/http.py`, `utils/json_utils.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py` | 141335–142991 |
| `ide/preview.py` | 12 | 12 | `config/constants.py`, `utils/text.py` | 18438–18878 |
| `ide/sandbox.py` | 21 | 21 | `agent/process.py`, `utils/misc.py` | 9618–32702 |
| `ide/toolchains.py` | 7 | 7 | — | 6515–125302 |
| `llm/client.py` | 2 | 2 | `agent/context.py`, `agent/tools.py`, `config/constants.py`, `config/settings.py`, `llm/gate.py`, `llm/utils.py`, `utils/http.py`, `utils/json_utils.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py` | 27974–31311 |
| `llm/constants.py` | 17 | 17 | — | 5120–14403 |
| `llm/gate.py` | 22 | 22 | `config/constants.py`, `config/settings.py`, `llm/client.py`, `utils/misc.py`, `utils/text.py` | 5998–28451 |
| `llm/utils.py` | 37 | 37 | `agent/context.py`, `agent/process.py`, `config/settings.py`, `llm/constants.py`, `utils/http.py`, `utils/json_utils.py`, `utils/text.py` | 13641–15058 |
| `mcp/constants.py` | 8 | 8 | — | 5492–26627 |
| `mcp/driver.py` | 13 | 13 | `mcp/constants.py`, `utils/files.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` | 26628–27973 |
| `mcp/service.py` | 1 | 1 | `app/context.py`, `config/constants.py`, `utils/files.py`, `utils/http.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` | 143463–143680 |
| `rag/assets.py` | 6 | 6 | — | 119524–122147 |
| `rag/constants.py` | 77 | 77 | — | 5488–112478 |
| `rag/index.py` | 5 | 5 | `config/constants.py`, `rag/constants.py`, `rag/ingestion.py`, `rag/parsers.py`, `utils/misc.py`, `utils/text.py` | 112503–119144 |
| `rag/ingestion.py` | 13 | 13 | `config/constants.py`, `config/settings.py`, `rag/constants.py`, `rag/parsers.py`, `rag/store.py`, `session/state.py`, `utils/files.py`, `utils/json_utils.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py` | 111825–119523 |
| `rag/parsers.py` | 31 | 31 | `agent/process.py`, `config/constants.py`, `rag/constants.py`, `rag/ingestion.py`, `utils/files.py`, `utils/json_utils.py`, `utils/media.py`, `utils/text.py` | 111448–113674 |
| `rag/store.py` | 7 | 7 | `config/constants.py`, `config/settings.py`, `ide/preview.py`, `rag/constants.py`, `rag/index.py`, `rag/ingestion.py`, `rag/parsers.py`, `skills/provisioning.py`, `utils/files.py`, `utils/json_utils.py`, `utils/media.py`, `utils/misc.py`, `utils/sqlite.py`, `utils/text.py` | 115370–119435 |
| `rag/web_search.py` | 15 | 15 | `config/constants.py`, `config/paths.py`, `rag/constants.py`, `utils/http.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/sqlite.py`, `utils/text.py` | 10765–12923 |
| `server/http.py` | 12 | 12 | `admin/auth.py`, `admin/config.py`, `admin/constants.py`, `agent/process.py`, `app/context.py`, `collaboration/core.py`, `collaboration/watcher.py`, `config/constants.py`, `config/paths.py`, `config/settings.py`, `ide/auth.py`, `ide/handler.py`, `ide/preview.py`, `llm/gate.py`, `llm/utils.py`, `server/rag_admin.py`, `session/manager.py`, `session/state.py`, `skills/studio.py`, `utils/errors.py`, `utils/files.py`, `utils/http.py`, `utils/json_utils.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py`, `web/admin_assets.py` | 7738–143462 |
| `server/rag_admin.py` | 3 | 3 | `admin/auth.py`, `app/context.py`, `config/constants.py`, `rag/constants.py`, `utils/http.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py` | 140663–141334 |
| `server/skills.py` | 1 | 1 | `admin/auth.py`, `app/context.py`, `config/constants.py`, `config/paths.py`, `config/settings.py`, `llm/gate.py`, `session/manager.py`, `skills/provisioning.py`, `skills/studio.py`, `utils/http.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py` | 140013–140662 |
| `session/manager.py` | 2 | 2 | `agent/process.py`, `config/constants.py`, `config/paths.py`, `config/settings.py`, `llm/client.py`, `llm/gate.py`, `llm/utils.py`, `rag/store.py`, `session/state.py`, `skills/store.py`, `utils/crypto.py`, `utils/files.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` | 8942–99468 |
| `session/state.py` | 1 | 1 | `admin/constants.py`, `agent/background.py`, `agent/bus.py`, `agent/context.py`, `agent/errors.py`, `agent/events.py`, `agent/evidence.py`, `agent/process.py`, `agent/tasks.py`, `agent/todo.py`, `agent/tools.py`, `agent/worktree.py`, `collaboration/core.py`, `config/constants.py`, `config/paths.py`, `config/settings.py`, `ide/events.py`, `ide/preview.py`, `ide/sandbox.py`, `llm/client.py`, `llm/constants.py`, `llm/gate.py`, `llm/utils.py`, `mcp/constants.py`, `mcp/driver.py`, `rag/constants.py`, `rag/parsers.py`, `rag/web_search.py`, `server/http.py`, `skills/provisioning.py`, `skills/store.py`, `utils/compress.py`, `utils/crypto.py`, `utils/errors.py`, `utils/files.py`, `utils/http.py`, `utils/json_utils.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py` | 33043–96924 |
| `skills/embedded.py` | 10 | 10 | — | 19361–23160 |
| `skills/provisioning.py` | 26 | 26 | `config/paths.py`, `skills/embedded.py`, `utils/files.py`, `utils/json_utils.py`, `utils/misc.py` | 19387–23123 |
| `skills/store.py` | 3 | 3 | `config/constants.py`, `config/settings.py`, `llm/utils.py`, `skills/embedded.py`, `utils/files.py`, `utils/http.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` | 6534–25185 |
| `skills/studio.py` | 5 | 5 | `agent/process.py`, `collaboration/core.py`, `config/constants.py`, `config/settings.py`, `ide/sandbox.py`, `llm/client.py`, `llm/constants.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/sqlite.py`, `utils/text.py` | 123331–125228 |
| `utils/compress.py` | 2 | 2 | — | 13088–13104 |
| `utils/crypto.py` | 1 | 1 | `utils/json_utils.py` | 16092–16245 |
| `utils/errors.py` | 2 | 2 | — | 13721–25326 |
| `utils/files.py` | 29 | 29 | `config/constants.py`, `config/paths.py`, `utils/http.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` | 7608–18109 |
| `utils/http.py` | 7 | 7 | `utils/json_utils.py`, `utils/text.py` | 5117–9772 |
| `utils/json_utils.py` | 17 | 17 | `utils/text.py` | 5487–16556 |
| `utils/media.py` | 6 | 6 | — | 7246–9323 |
| `utils/misc.py` | 16 | 16 | `config/constants.py` | 9324–19462 |
| `utils/sqlite.py` | 3 | 3 | — | 73–143765 |
| `utils/text.py` | 36 | 36 | `config/constants.py` | 5475–18437 |
| `web/admin_assets.py` | 3 | 3 | — | 105521–106513 |
| `web/assets.py` | 5 | 4 | — | 99469–105118 |
| `web/skills_assets.py` | 3 | 3 | — | 105119–105520 |

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
- order 76: `_import_1689` (import), lines 1688-1693, exports `EVOLUTION_MODES`, `LiquidKernelControlPlane`, `LiquidKernelError`
- order 78: `_import_1714` (import), lines 1710-1716, exports `_LiquidKernelRegistry`
- order 119: `_try_import_5100` (import), lines 5098-5107, exports `_fcntl`, `_pty`, `_termios`
- order 120: `_try_import_5109` (import), lines 5108-5112, exports `_certifi`
- order 121: `_try_import_5113` (import), lines 5113-5116, exports `_yaml`

### `admin/auth.py`

- order 956: `trusted_client_ip` (function), lines 16059-16091, exports `trusted_client_ip`
- order 970: `AdminAuthError` (class), lines 16615-16622, exports `AdminAuthError`
- order 971: `AdminAuthStore` (class), lines 16623-16901, exports `AdminAuthStore`

### `admin/config.py`

- order 976: `_admin_config_schema` (function), lines 17649-17772, exports `_admin_config_schema`
- order 977: `_admin_factory_config` (function), lines 17773-17776, exports `_admin_factory_config`
- order 978: `_admin_coerce_config` (function), lines 17777-17932, exports `_admin_coerce_config`
- order 979: `_admin_config_to_argv` (function), lines 17933-17969, exports `_admin_config_to_argv`
- order 980: `_admin_restart_probe_url` (function), lines 17970-17985, exports `_admin_restart_probe_url`
- order 981: `_admin_supervised_restart` (function), lines 17986-18091, exports `_admin_supervised_restart`
- order 983: `_admin_argparse_defaults` (function), lines 18110-18131, exports `_admin_argparse_defaults`
- order 984: `_admin_config_from_namespace` (function), lines 18132-18152, exports `_admin_config_from_namespace`

### `admin/constants.py`

- order 128: `ADMIN_STATE_DIRNAME` (constant), lines 5123-5123, exports `ADMIN_STATE_DIRNAME`
- order 129: `ADMIN_CONFIG_FILENAME` (constant), lines 5124-5124, exports `ADMIN_CONFIG_FILENAME`
- order 130: `ADMIN_APPS_FILENAME` (constant), lines 5125-5125, exports `ADMIN_APPS_FILENAME`
- order 131: `ADMIN_TELEMETRY_FILENAME` (constant), lines 5126-5126, exports `ADMIN_TELEMETRY_FILENAME`
- order 132: `ADMIN_AUTH_FILENAME` (constant), lines 5127-5127, exports `ADMIN_AUTH_FILENAME`
- order 142: `ADMIN_MAX_APP_SKILLS` (constant), lines 5174-5174, exports `ADMIN_MAX_APP_SKILLS`
- order 143: `ADMIN_MAX_APP_CAPSULE_CHARS` (constant), lines 5175-5175, exports `ADMIN_MAX_APP_CAPSULE_CHARS`
- order 144: `ADMIN_MAX_APP_RESOURCE_FILES` (constant), lines 5176-5176, exports `ADMIN_MAX_APP_RESOURCE_FILES`
- order 145: `ADMIN_MAX_APP_RESOURCE_BYTES` (constant), lines 5177-5177, exports `ADMIN_MAX_APP_RESOURCE_BYTES`
- order 146: `ADMIN_APP_INLINE_BLOB_BYTES` (constant), lines 5178-5178, exports `ADMIN_APP_INLINE_BLOB_BYTES`
- order 147: `ADMIN_AUTH_SESSION_TTL_SECONDS` (constant), lines 5179-5179, exports `ADMIN_AUTH_SESSION_TTL_SECONDS`
- order 148: `ADMIN_AUTH_PASSWORD_ITERATIONS` (constant), lines 5180-5180, exports `ADMIN_AUTH_PASSWORD_ITERATIONS`
- order 149: `ADMIN_AUTH_MAX_ACTIVE_SESSIONS` (constant), lines 5181-5181, exports `ADMIN_AUTH_MAX_ACTIVE_SESSIONS`
- order 1252: `ADMIN_SKILLS_REVIEW_HTML` (constant), lines 125234-125235, exports `ADMIN_SKILLS_REVIEW_HTML`
- order 1253: `ADMIN_SKILLS_REVIEW_CSS` (constant), lines 125236-125236, exports `ADMIN_SKILLS_REVIEW_CSS`
- order 1254: `ADMIN_SKILLS_REVIEW_JS` (constant), lines 125237-125237, exports `ADMIN_SKILLS_REVIEW_JS`

### `agent/background.py`

- order 1056: `BackgroundManager` (class), lines 25687-26312, exports `BackgroundManager`

### `agent/bus.py`

- order 1057: `MessageBus` (class), lines 26313-26378, exports `MessageBus`

### `agent/context.py`

- order 344: `_READ_DISPATCH_CONTEXT` (assignment), lines 5856-5859, exports `_READ_DISPATCH_CONTEXT`
- order 900: `compact_successful_write_history` (function), lines 14037-14040, exports `compact_successful_write_history`

### `agent/errors.py`

- order 885: `CircuitBreakerTriggered` (class), lines 13725-13728, exports `CircuitBreakerTriggered`

### `agent/events.py`

- order 1012: `EventHub` (class), lines 18879-18933, exports `EventHub`

### `agent/evidence.py`

- order 1139: `EvidenceRetrievalController` (class), lines 32703-33039, exports `EvidenceRetrievalController`
- order 1140: `_EVIDENCE_CONTROLLER_INIT_LOCK` (assignment), lines 33040-33042, exports `_EVIDENCE_CONTROLLER_INIT_LOCK`

### `agent/process.py`

- order 457: `_TOOL_CANCEL_LOCAL` (assignment), lines 6176-6179, exports `_TOOL_CANCEL_LOCAL`
- order 458: `_TOOL_ORPHAN_LOCK` (assignment), lines 6180-6180, exports `_TOOL_ORPHAN_LOCK`
- order 788: `subprocess_text_encodings` (function), lines 9636-9657, exports `subprocess_text_encodings`
- order 789: `decode_subprocess_bytes` (function), lines 9658-9684, exports `decode_subprocess_bytes`
- order 790: `run_subprocess_text` (function), lines 9685-9707, exports `run_subprocess_text`
- order 791: `windows_utf8_shell_command` (function), lines 9708-9714, exports `windows_utf8_shell_command`
- order 792: `shell_process_invocation` (function), lines 9715-9725, exports `shell_process_invocation`
- order 793: `join_shell_task_command` (function), lines 9726-9737, exports `join_shell_task_command`
- order 1055: `UserProcessManager` (class), lines 25327-25686, exports `UserProcessManager`

### `agent/tasks.py`

- order 1053: `TaskManager` (class), lines 25186-25320, exports `TaskManager`

### `agent/todo.py`

- order 1013: `TodoManager` (class), lines 18934-19360, exports `TodoManager`

### `agent/tools.py`

- order 1007: `_ask_user_option_rows` (function), lines 18758-18791, exports `_ask_user_option_rows`
- order 1008: `_ask_user_option_value` (function), lines 18792-18797, exports `_ask_user_option_value`
- order 1100: `tool_def` (function), lines 31312-31325, exports `tool_def`
- order 1105: `bash_operation_is_observation` (function), lines 31406-31409, exports `bash_operation_is_observation`
- order 1106: `bash_operation_is_marked_observation` (function), lines 31410-31414, exports `bash_operation_is_marked_observation`
- order 1107: `TOOLS` (constant), lines 31415-32006, exports `TOOLS`
- order 1108: `TOOL_REQUIRED_ARGS` (constant), lines 32007-32008, exports `TOOL_REQUIRED_ARGS`
- order 1109: `TOOL_SPEC_BY_NAME` (constant), lines 32009-32009, exports `TOOL_SPEC_BY_NAME`
- order 1110: `_for_32010` (statement), lines 32010-32019, exports `_tool`, `_fn`, `_name`, `_required`
- order 1111: `TOOL_NAME_FUZZY_MAP` (constant), lines 32020-32021, exports `TOOL_NAME_FUZZY_MAP`
- order 1112: `_for_32022` (statement), lines 32022-32025, exports `_name`, `_key`
- order 1113: `_for_32027` (statement), lines 32026-32043, exports `_alias`, `_target`
- order 1114: `is_todo_resume_tool_name` (function), lines 32044-32060, exports `is_todo_resume_tool_name`
- order 1115: `canonicalize_tool_name` (function), lines 32061-32079, exports `canonicalize_tool_name`
- order 1116: `filter_tool_specs_for_runtime` (function), lines 32080-32095, exports `filter_tool_specs_for_runtime`
- order 1117: `DEVELOPER_TOOL_DROP` (constant), lines 32096-32106, exports `DEVELOPER_TOOL_DROP`
- order 1118: `AGENT_TOOL_ALLOWLIST` (constant), lines 32107-32170, exports `AGENT_TOOL_ALLOWLIST`

### `agent/worktree.py`

- order 1058: `WorktreeManager` (class), lines 26379-26591, exports `WorktreeManager`

### `app/context.py`

- order 1258: `AppContext` (class), lines 125303-136841, exports `AppContext`

### `app/main.py`

- order 1274: `main` (function), lines 143859-145845, exports `main`
- order 1275: `_main_guard_145847` (main_guard), lines 145846-145848, exports —

### `app/services.py`

- order 1260: `TelemetryStore` (class), lines 136882-137272, exports `TelemetryStore`
- order 1261: `ApplicationRegistry` (class), lines 137273-138082, exports `ApplicationRegistry`

### `collaboration/core.py`

- order 93: `_now` (function), lines 1735-1738, exports `_now`
- order 94: `_json` (function), lines 1739-1742, exports `_json`
- order 95: `_load_json` (function), lines 1743-1749, exports `_load_json`
- order 96: `_b64_token` (function), lines 1750-1753, exports `_b64_token`
- order 97: `_branch_label` (function), lines 1754-1762, exports `_branch_label`
- order 98: `_digest` (function), lines 1763-1766, exports `_digest`
- order 99: `_password_hash` (function), lines 1767-1770, exports `_password_hash`
- order 100: `_normalize_ip` (function), lines 1771-1780, exports `_normalize_ip`
- order 101: `_normalize_name` (function), lines 1781-1787, exports `_normalize_name`
- order 102: `_COLLAB_PUBLIC_SECRET_PATTERNS` (assignment), lines 1788-1799, exports `_COLLAB_PUBLIC_SECRET_PATTERNS`
- order 103: `_collaboration_public_text` (function), lines 1800-1830, exports `_collaboration_public_text`
- order 104: `_collaboration_task_objective` (function), lines 1831-1855, exports `_collaboration_task_objective`
- order 105: `_collaboration_task_title` (function), lines 1856-1863, exports `_collaboration_task_title`
- order 106: `_collaboration_task_key` (function), lines 1864-1870, exports `_collaboration_task_key`
- order 107: `_collaboration_plan_steps` (function), lines 1871-1889, exports `_collaboration_plan_steps`
- order 108: `CollaborationError` (class), lines 1890-1897, exports `CollaborationError`
- order 109: `CollaborationPrincipal` (class), lines 1898-1908, exports `CollaborationPrincipal`
- order 110: `_normalize_operation` (function), lines 1909-1942, exports `_normalize_operation`
- order 111: `operation_input_length` (function), lines 1943-1946, exports `operation_input_length`
- order 112: `apply_text_operation` (function), lines 1947-1969, exports `apply_text_operation`
- order 113: `transform_text_operation` (function), lines 1970-2046, exports `transform_text_operation`
- order 114: `CollaborationStore` (class), lines 2047-4762, exports `CollaborationStore`
- order 115: `CollaborationWriteCoordinator` (class), lines 4763-4976, exports `CollaborationWriteCoordinator`

### `collaboration/watcher.py`

- order 1272: `collaboration_file_watcher_loop` (function), lines 143766-143840, exports `collaboration_file_watcher_loop`
- order 1273: `collaboration_watcher_health` (function), lines 143841-143858, exports `collaboration_watcher_health`

### `config/bootstrap.py`

- order 73: `_EMBEDDED_LIQUID_KERNEL_PACKAGE_B64` (assignment), lines 123-1592, exports `_EMBEDDED_LIQUID_KERNEL_PACKAGE_B64`
- order 74: `_ensure_embedded_liquid_kernel_package` (function), lines 1593-1685, exports `_ensure_embedded_liquid_kernel_package`
- order 77: `_ensure_liquid_kernel_sqlite_lifecycle` (function), lines 1694-1709, exports `_ensure_liquid_kernel_sqlite_lifecycle`
- order 967: `_liquid_kernel_history_present` (function), lines 16566-16570, exports `_liquid_kernel_history_present`
- order 968: `prepare_liquid_kernel_runtime` (function), lines 16571-16600, exports `prepare_liquid_kernel_runtime`
- order 969: `_persist_liquid_kernel_bootstrap` (function), lines 16601-16614, exports `_persist_liquid_kernel_bootstrap`

### `config/constants.py`

- order 75: `LIQUID_KERNEL_PACKAGE_STATUS` (constant), lines 1686-1687, exports `LIQUID_KERNEL_PACKAGE_STATUS`
- order 79: `_call_ensure_liquid_kernel_sqlite_lifecycle_1718` (expression), lines 1717-1718, exports —
- order 80: `COLLAB_DB_FILENAME` (constant), lines 1719-1722, exports `COLLAB_DB_FILENAME`
- order 81: `COLLAB_SESSION_TTL_SECONDS` (constant), lines 1723-1723, exports `COLLAB_SESSION_TTL_SECONDS`
- order 82: `COLLAB_PRESENCE_TTL_SECONDS` (constant), lines 1724-1724, exports `COLLAB_PRESENCE_TTL_SECONDS`
- order 83: `COLLAB_PASSWORD_ITERATIONS` (constant), lines 1725-1725, exports `COLLAB_PASSWORD_ITERATIONS`
- order 84: `COLLAB_MAX_AVATAR_BYTES` (constant), lines 1726-1726, exports `COLLAB_MAX_AVATAR_BYTES`
- order 85: `COLLAB_MAX_TEXT_BYTES` (constant), lines 1727-1727, exports `COLLAB_MAX_TEXT_BYTES`
- order 86: `COLLAB_DELETE_RETENTION_DAYS` (constant), lines 1728-1728, exports `COLLAB_DELETE_RETENTION_DAYS`
- order 87: `COLLAB_EVENT_RETENTION` (constant), lines 1729-1729, exports `COLLAB_EVENT_RETENTION`
- order 88: `COLLAB_AGENT_STALE_SECONDS` (constant), lines 1730-1730, exports `COLLAB_AGENT_STALE_SECONDS`
- order 89: `COLLAB_AGENT_HEARTBEAT_INTERVAL_SECONDS` (constant), lines 1731-1731, exports `COLLAB_AGENT_HEARTBEAT_INTERVAL_SECONDS`
- order 90: `COLLAB_EXTERNAL_WRITE_SETTLE_SECONDS` (constant), lines 1732-1732, exports `COLLAB_EXTERNAL_WRITE_SETTLE_SECONDS`
- order 91: `COLLAB_EXTERNAL_WRITE_CONFIRMATIONS` (constant), lines 1733-1733, exports `COLLAB_EXTERNAL_WRITE_CONFIRMATIONS`
- order 92: `COLLAB_SCHEMA_VERSION` (constant), lines 1734-1734, exports `COLLAB_SCHEMA_VERSION`
- order 116: `COLLAB_INDEX_HTML` (constant), lines 4977-5048, exports `COLLAB_INDEX_HTML`
- order 117: `COLLAB_CSS` (constant), lines 5049-5056, exports `COLLAB_CSS`
- order 118: `COLLAB_JS` (constant), lines 5057-5097, exports `COLLAB_JS`
- order 124: `APP_VERSION` (constant), lines 5119-5119, exports `APP_VERSION`
- order 133: `IDE_AUTH_FILENAME` (constant), lines 5128-5128, exports `IDE_AUTH_FILENAME`
- order 134: `IDE_AUTH_SESSION_TTL_SECONDS` (constant), lines 5129-5129, exports `IDE_AUTH_SESSION_TTL_SECONDS`
- order 135: `IDE_AUTH_MAX_ACTIVE_SESSIONS` (constant), lines 5130-5130, exports `IDE_AUTH_MAX_ACTIVE_SESSIONS`
- order 136: `IDE_DEVICE_SECRET_MIN_BYTES` (constant), lines 5131-5131, exports `IDE_DEVICE_SECRET_MIN_BYTES`
- order 137: `IDE_DEVICE_LABEL_MAX_CHARS` (constant), lines 5132-5132, exports `IDE_DEVICE_LABEL_MAX_CHARS`
- order 138: `IDE_DEVICE_PAIRING_TTL_SECONDS` (constant), lines 5133-5133, exports `IDE_DEVICE_PAIRING_TTL_SECONDS`
- order 139: `IDE_WORKBENCH_STATE_FILENAME` (constant), lines 5134-5134, exports `IDE_WORKBENCH_STATE_FILENAME`
- order 140: `IDE_PROMPT_ENHANCEMENT_BUDGETS` (constant), lines 5135-5172, exports `IDE_PROMPT_ENHANCEMENT_BUDGETS`
- order 141: `IDE_EXTENSIONS_DIRNAME` (constant), lines 5173-5173, exports `IDE_EXTENSIONS_DIRNAME`
- order 163: `LONG_OUTPUT_MODEL_PAGE_CHARS` (constant), lines 5476-5476, exports `LONG_OUTPUT_MODEL_PAGE_CHARS`
- order 164: `LONG_OUTPUT_UI_PAGE_CHARS` (constant), lines 5477-5477, exports `LONG_OUTPUT_UI_PAGE_CHARS`
- order 165: `LONG_OUTPUT_UI_PREVIEW_MAX_PAGES` (constant), lines 5478-5478, exports `LONG_OUTPUT_UI_PREVIEW_MAX_PAGES`
- order 166: `LONG_OUTPUT_LISTING_OFFLOAD_CHARS` (constant), lines 5479-5479, exports `LONG_OUTPUT_LISTING_OFFLOAD_CHARS`
- order 167: `LONG_OUTPUT_READ_PAGE_LINES` (constant), lines 5480-5480, exports `LONG_OUTPUT_READ_PAGE_LINES`
- order 168: `LONG_OUTPUT_READ_PAGE_MAX_CHARS` (constant), lines 5481-5481, exports `LONG_OUTPUT_READ_PAGE_MAX_CHARS`
- order 169: `LONG_OUTPUT_TEMP_MAX_FILES` (constant), lines 5482-5482, exports `LONG_OUTPUT_TEMP_MAX_FILES`
- order 170: `READ_FILE_DEFAULT_MAX_CHARS` (constant), lines 5483-5483, exports `READ_FILE_DEFAULT_MAX_CHARS`
- order 171: `READ_FILE_HARD_MAX_CHARS` (constant), lines 5484-5484, exports `READ_FILE_HARD_MAX_CHARS`
- order 172: `READ_FILE_OVERVIEW_HEAD_LINES` (constant), lines 5485-5485, exports `READ_FILE_OVERVIEW_HEAD_LINES`
- order 173: `READ_FILE_SEARCH_MAX_MATCHES` (constant), lines 5486-5486, exports `READ_FILE_SEARCH_MAX_MATCHES`
- order 178: `CODE_ADMIN_PORT_OFFSET` (constant), lines 5491-5491, exports `CODE_ADMIN_PORT_OFFSET`
- order 180: `IDE_PORT_OFFSET` (constant), lines 5493-5496, exports `IDE_PORT_OFFSET`
- order 181: `IDE_DEFAULT_PORT` (constant), lines 5497-5497, exports `IDE_DEFAULT_PORT`
- order 182: `COLLAB_PORT_OFFSET` (constant), lines 5498-5498, exports `COLLAB_PORT_OFFSET`
- order 184: `DEFAULT_WEB_SEARCH_ENABLED` (constant), lines 5500-5500, exports `DEFAULT_WEB_SEARCH_ENABLED`
- order 189: `DEFAULT_USER_MEMORY_MODE` (constant), lines 5505-5505, exports `DEFAULT_USER_MEMORY_MODE`
- order 197: `AGENT_WEB_SEARCH_USER_AGENT` (constant), lines 5516-5516, exports `AGENT_WEB_SEARCH_USER_AGENT`
- order 198: `AGENT_WEB_SEARCH_DEFAULT_MAX_RESULTS` (constant), lines 5517-5517, exports `AGENT_WEB_SEARCH_DEFAULT_MAX_RESULTS`
- order 199: `AGENT_WEB_SEARCH_DEFAULT_MAX_PAGES` (constant), lines 5518-5518, exports `AGENT_WEB_SEARCH_DEFAULT_MAX_PAGES`
- order 200: `AGENT_WEB_SEARCH_HARD_MAX_PAGES` (constant), lines 5519-5519, exports `AGENT_WEB_SEARCH_HARD_MAX_PAGES`
- order 201: `AGENT_WEB_SEARCH_DEFAULT_DEPTH` (constant), lines 5520-5520, exports `AGENT_WEB_SEARCH_DEFAULT_DEPTH`
- order 202: `AGENT_WEB_SEARCH_HARD_DEPTH` (constant), lines 5521-5521, exports `AGENT_WEB_SEARCH_HARD_DEPTH`
- order 203: `AGENT_WEB_SEARCH_FETCH_TIMEOUT` (constant), lines 5522-5522, exports `AGENT_WEB_SEARCH_FETCH_TIMEOUT`
- order 204: `AGENT_WEB_SEARCH_TOOL_SOFT_TIMEOUT` (constant), lines 5523-5523, exports `AGENT_WEB_SEARCH_TOOL_SOFT_TIMEOUT`
- order 205: `AGENT_WEB_SEARCH_MAX_PAGE_BYTES` (constant), lines 5524-5524, exports `AGENT_WEB_SEARCH_MAX_PAGE_BYTES`
- order 206: `AGENT_WEB_SEARCH_MAX_TEXT_CHARS` (constant), lines 5525-5525, exports `AGENT_WEB_SEARCH_MAX_TEXT_CHARS`
- order 207: `AGENT_WEB_SEARCH_PUBLIC_DISCOVERY_ENABLED` (constant), lines 5526-5528, exports `AGENT_WEB_SEARCH_PUBLIC_DISCOVERY_ENABLED`
- order 208: `AGENT_WEB_SEARCH_PUBLIC_FEED_URL` (constant), lines 5529-5529, exports `AGENT_WEB_SEARCH_PUBLIC_FEED_URL`
- order 209: `AGENT_WEB_SEARCH_PUBLIC_FEED_MAX_BYTES` (constant), lines 5530-5530, exports `AGENT_WEB_SEARCH_PUBLIC_FEED_MAX_BYTES`
- order 210: `AGENT_WEB_SEARCH_LOCAL_GRAPH_MAX_NODES` (constant), lines 5531-5531, exports `AGENT_WEB_SEARCH_LOCAL_GRAPH_MAX_NODES`
- order 211: `AGENT_WEB_SEARCH_LOCAL_GRAPH_MAX_EDGES` (constant), lines 5532-5532, exports `AGENT_WEB_SEARCH_LOCAL_GRAPH_MAX_EDGES`
- order 212: `AGENT_WEB_SEARCH_LOCAL_GRAPH_EDGE_SCAN_MULTIPLIER` (constant), lines 5533-5533, exports `AGENT_WEB_SEARCH_LOCAL_GRAPH_EDGE_SCAN_MULTIPLIER`
- order 213: `AGENT_WEB_SEARCH_LOCAL_GRAPH_PAGERANK_ITERATIONS` (constant), lines 5534-5534, exports `AGENT_WEB_SEARCH_LOCAL_GRAPH_PAGERANK_ITERATIONS`
- order 214: `AGENT_WEB_SEARCH_LOCAL_GRAPH_PAGERANK_DAMPING` (constant), lines 5535-5535, exports `AGENT_WEB_SEARCH_LOCAL_GRAPH_PAGERANK_DAMPING`
- order 215: `AGENT_WEB_SEARCH_LOCAL_GRAPH_AUTHORITY_BONUS_MAX` (constant), lines 5536-5536, exports `AGENT_WEB_SEARCH_LOCAL_GRAPH_AUTHORITY_BONUS_MAX`
- order 225: `CODE_CHUNK_CHARS` (constant), lines 5558-5558, exports `CODE_CHUNK_CHARS`
- order 226: `CODE_CHUNK_OVERLAP` (constant), lines 5559-5559, exports `CODE_CHUNK_OVERLAP`
- order 227: `CODE_MAX_CHUNKS_PER_DOC` (constant), lines 5560-5560, exports `CODE_MAX_CHUNKS_PER_DOC`
- order 228: `CODE_SOURCE_ANALYSIS_MAX_CHARS` (constant), lines 5561-5570, exports `CODE_SOURCE_ANALYSIS_MAX_CHARS`
- order 269: `CODE_IMPORT_WORKER_COUNT` (constant), lines 5639-5642, exports `CODE_IMPORT_WORKER_COUNT`
- order 271: `CODE_PARSE_TIMEOUT_SECONDS` (constant), lines 5647-5650, exports `CODE_PARSE_TIMEOUT_SECONDS`
- order 272: `DEFAULT_CONTEXT_TOKEN_LIMIT` (constant), lines 5651-5651, exports `DEFAULT_CONTEXT_TOKEN_LIMIT`
- order 273: `TOKEN_THRESHOLD` (constant), lines 5652-5652, exports `TOKEN_THRESHOLD`
- order 274: `CONTEXT_AUTO_COMPACT_RESERVE_RATIO` (constant), lines 5653-5656, exports `CONTEXT_AUTO_COMPACT_RESERVE_RATIO`
- order 275: `CONTEXT_ESTIMATE_SAFETY_MULTIPLIER` (constant), lines 5657-5660, exports `CONTEXT_ESTIMATE_SAFETY_MULTIPLIER`
- order 276: `CONTEXT_USAGE_CALIBRATION_MAX` (constant), lines 5661-5664, exports `CONTEXT_USAGE_CALIBRATION_MAX`
- order 277: `CONTEXT_ACTUAL_USAGE_RECENT_SECONDS` (constant), lines 5665-5668, exports `CONTEXT_ACTUAL_USAGE_RECENT_SECONDS`
- order 278: `LARGE_FILE_AUTO_PAGE_BYTES` (constant), lines 5669-5672, exports `LARGE_FILE_AUTO_PAGE_BYTES`
- order 279: `LARGE_FILE_AUTO_PAGE_LINES` (constant), lines 5673-5676, exports `LARGE_FILE_AUTO_PAGE_LINES`
- order 280: `LARGE_SOURCE_UPLOAD_EXCERPT_CHARS` (constant), lines 5677-5680, exports `LARGE_SOURCE_UPLOAD_EXCERPT_CHARS`
- order 281: `CHAT_UPLOAD_PARSE_QUEUE_MAX` (constant), lines 5681-5684, exports `CHAT_UPLOAD_PARSE_QUEUE_MAX`
- order 282: `CHAT_UPLOAD_PARSE_TIMEOUT_SECONDS` (constant), lines 5685-5688, exports `CHAT_UPLOAD_PARSE_TIMEOUT_SECONDS`
- order 283: `CHAT_UPLOAD_INLINE_TEXT_BYTES` (constant), lines 5689-5692, exports `CHAT_UPLOAD_INLINE_TEXT_BYTES`
- order 284: `CHAT_UPLOAD_PARSE_MAX_BYTES` (constant), lines 5693-5699, exports `CHAT_UPLOAD_PARSE_MAX_BYTES`
- order 285: `CHAT_UPLOAD_ZIP_ENTRY_MAX_BYTES` (constant), lines 5700-5706, exports `CHAT_UPLOAD_ZIP_ENTRY_MAX_BYTES`
- order 286: `CHAT_UPLOAD_TEXT_CONTEXT_CHARS` (constant), lines 5707-5710, exports `CHAT_UPLOAD_TEXT_CONTEXT_CHARS`
- order 287: `CHAT_UPLOAD_PROMPT_MAX_FILES` (constant), lines 5711-5714, exports `CHAT_UPLOAD_PROMPT_MAX_FILES`
- order 288: `CHAT_UPLOAD_PROMPT_MAX_CHARS` (constant), lines 5715-5718, exports `CHAT_UPLOAD_PROMPT_MAX_CHARS`
- order 289: `CHAT_UPLOAD_PROMPT_PER_FILE_CHARS` (constant), lines 5719-5722, exports `CHAT_UPLOAD_PROMPT_PER_FILE_CHARS`
- order 290: `CHAT_UPLOAD_FRONTEND_WAIT_MS` (constant), lines 5723-5726, exports `CHAT_UPLOAD_FRONTEND_WAIT_MS`
- order 291: `CHAT_UPLOAD_AUTO_LIBRARY_INGEST` (constant), lines 5727-5730, exports `CHAT_UPLOAD_AUTO_LIBRARY_INGEST`
- order 292: `CHAT_UPLOAD_INGEST_QUEUE_MAX` (constant), lines 5731-5734, exports `CHAT_UPLOAD_INGEST_QUEUE_MAX`
- order 293: `SESSION_SUBMIT_LOCK_TIMEOUT_SECONDS` (constant), lines 5735-5738, exports `SESSION_SUBMIT_LOCK_TIMEOUT_SECONDS`
- order 294: `SESSION_DEFERRED_START_QUEUE_MAX` (constant), lines 5739-5742, exports `SESSION_DEFERRED_START_QUEUE_MAX`
- order 295: `SESSION_SUBMISSION_DEDUPE_MAX` (constant), lines 5743-5743, exports `SESSION_SUBMISSION_DEDUPE_MAX`
- order 296: `SESSION_SUBMISSION_DEDUPE_SECONDS` (constant), lines 5744-5744, exports `SESSION_SUBMISSION_DEDUPE_SECONDS`
- order 297: `SCHEDULER_SUBMISSION_DEDUPE_MAX` (constant), lines 5745-5745, exports `SCHEDULER_SUBMISSION_DEDUPE_MAX`
- order 298: `FAST_START_LOCAL_CLASSIFICATION` (constant), lines 5746-5748, exports `FAST_START_LOCAL_CLASSIFICATION`
- order 299: `FAST_START_LOCAL_TITLE` (constant), lines 5749-5751, exports `FAST_START_LOCAL_TITLE`
- order 300: `AUTO_TITLE_MODEL_REFINE` (constant), lines 5752-5754, exports `AUTO_TITLE_MODEL_REFINE`
- order 301: `AUTO_TITLE_MODEL_TIMEOUT_SECONDS` (constant), lines 5755-5758, exports `AUTO_TITLE_MODEL_TIMEOUT_SECONDS`
- order 302: `AUTO_TITLE_MODEL_RETRY_COOLDOWN_SECONDS` (constant), lines 5759-5765, exports `AUTO_TITLE_MODEL_RETRY_COOLDOWN_SECONDS`
- order 303: `FAST_START_DEFER_CAPABILITY_PROBE` (constant), lines 5766-5768, exports `FAST_START_DEFER_CAPABILITY_PROBE`
- order 304: `SESSION_RUNTIME_MESSAGE_WINDOW` (constant), lines 5769-5769, exports `SESSION_RUNTIME_MESSAGE_WINDOW`
- order 305: `SESSION_RUNTIME_ACTIVITY_WINDOW` (constant), lines 5770-5770, exports `SESSION_RUNTIME_ACTIVITY_WINDOW`
- order 306: `SESSION_RUNTIME_OPERATION_WINDOW` (constant), lines 5771-5771, exports `SESSION_RUNTIME_OPERATION_WINDOW`
- order 307: `SESSION_RUNTIME_UPLOAD_WINDOW` (constant), lines 5772-5772, exports `SESSION_RUNTIME_UPLOAD_WINDOW`
- order 308: `LITE_SNAPSHOT_MAX_BYTES` (constant), lines 5773-5776, exports `LITE_SNAPSHOT_MAX_BYTES`
- order 309: `LITE_SNAPSHOT_MESSAGES_BYTES` (constant), lines 5777-5777, exports `LITE_SNAPSHOT_MESSAGES_BYTES`
- order 310: `LITE_SNAPSHOT_FEED_BYTES` (constant), lines 5778-5778, exports `LITE_SNAPSHOT_FEED_BYTES`
- order 311: `LITE_SNAPSHOT_OPERATIONS_BYTES` (constant), lines 5779-5779, exports `LITE_SNAPSHOT_OPERATIONS_BYTES`
- order 312: `IDE_AGENT_STATE_MAX_BYTES` (constant), lines 5780-5783, exports `IDE_AGENT_STATE_MAX_BYTES`
- order 313: `IDE_AGENT_FEED_BYTES` (constant), lines 5784-5784, exports `IDE_AGENT_FEED_BYTES`
- order 314: `IDE_AGENT_OPERATIONS_BYTES` (constant), lines 5785-5785, exports `IDE_AGENT_OPERATIONS_BYTES`
- order 315: `SESSION_WATCHDOG_INTERVAL_SECONDS` (constant), lines 5786-5789, exports `SESSION_WATCHDOG_INTERVAL_SECONDS`
- order 316: `SESSION_HEARTBEAT_STALE_SECONDS` (constant), lines 5790-5793, exports `SESSION_HEARTBEAT_STALE_SECONDS`
- order 317: `SESSION_LIST_DEFAULT_LIMIT` (constant), lines 5794-5797, exports `SESSION_LIST_DEFAULT_LIMIT`
- order 318: `SESSION_INDEX_SYNC_SNAPSHOT_MAX` (constant), lines 5798-5801, exports `SESSION_INDEX_SYNC_SNAPSHOT_MAX`
- order 319: `SESSION_INDEX_JOURNAL_COMPACT_RECORDS` (constant), lines 5802-5805, exports `SESSION_INDEX_JOURNAL_COMPACT_RECORDS`
- order 320: `SESSION_INDEX_JOURNAL_COMPACT_BYTES` (constant), lines 5806-5809, exports `SESSION_INDEX_JOURNAL_COMPACT_BYTES`
- order 321: `SESSION_CATALOG_RECENT_MAX` (constant), lines 5810-5813, exports `SESSION_CATALOG_RECENT_MAX`
- order 322: `IDE_SESSION_LIST_DEFAULT_LIMIT` (constant), lines 5814-5817, exports `IDE_SESSION_LIST_DEFAULT_LIMIT`
- order 323: `IDLE_TIMEOUT` (constant), lines 5818-5818, exports `IDLE_TIMEOUT`
- order 324: `POLL_INTERVAL` (constant), lines 5819-5819, exports `POLL_INTERVAL`
- order 325: `SSE_HEARTBEAT_SECONDS` (constant), lines 5820-5820, exports `SSE_HEARTBEAT_SECONDS`
- order 326: `MODEL_CALL_PROGRESS_DELAY` (constant), lines 5821-5821, exports `MODEL_CALL_PROGRESS_DELAY`
- order 327: `MODEL_CALL_PROGRESS_INTERVAL` (constant), lines 5822-5822, exports `MODEL_CALL_PROGRESS_INTERVAL`
- order 328: `RUN_COMPLETION_SUMMARY_ENABLED` (constant), lines 5823-5826, exports `RUN_COMPLETION_SUMMARY_ENABLED`
- order 329: `LLM_HTTP_RETRY_MAX_ATTEMPTS` (constant), lines 5827-5830, exports `LLM_HTTP_RETRY_MAX_ATTEMPTS`
- order 330: `LLM_HTTP_RETRY_DELAY_SECONDS` (constant), lines 5831-5834, exports `LLM_HTTP_RETRY_DELAY_SECONDS`
- order 331: `LLM_HTTP_RETRY_MAX_SECONDS` (constant), lines 5835-5838, exports `LLM_HTTP_RETRY_MAX_SECONDS`
- order 332: `LLM_HTTP_RETRY_404_ON_VLLM` (constant), lines 5839-5842, exports `LLM_HTTP_RETRY_404_ON_VLLM`
- order 333: `LLM_HTTP_RETRY_STATUSES` (constant), lines 5843-5843, exports `LLM_HTTP_RETRY_STATUSES`
- order 334: `MAX_AGENT_ROUNDS` (constant), lines 5844-5844, exports `MAX_AGENT_ROUNDS`
- order 335: `MIN_AGENT_ROUNDS` (constant), lines 5845-5845, exports `MIN_AGENT_ROUNDS`
- order 336: `MAX_AGENT_ROUNDS_CAP` (constant), lines 5846-5846, exports `MAX_AGENT_ROUNDS_CAP`
- order 337: `REPEATED_TOOL_LOOP_THRESHOLD` (constant), lines 5847-5847, exports `REPEATED_TOOL_LOOP_THRESHOLD`
- order 338: `BASH_READ_LOOP_THRESHOLD` (constant), lines 5848-5848, exports `BASH_READ_LOOP_THRESHOLD`
- order 339: `READ_FILE_LOOP_THRESHOLD` (constant), lines 5849-5849, exports `READ_FILE_LOOP_THRESHOLD`
- order 340: `READ_FILE_LOOP_DISTINCT_SOFT_LIMIT` (constant), lines 5850-5850, exports `READ_FILE_LOOP_DISTINCT_SOFT_LIMIT`
- order 341: `READ_FILE_COMPACT_PIN_DISTINCT` (constant), lines 5851-5851, exports `READ_FILE_COMPACT_PIN_DISTINCT`
- order 342: `READ_FILE_COMPACT_PIN_MAX_CHARS` (constant), lines 5852-5852, exports `READ_FILE_COMPACT_PIN_MAX_CHARS`
- order 343: `READ_FILE_PIN_TOTAL_CHARS` (constant), lines 5853-5855, exports `READ_FILE_PIN_TOTAL_CHARS`
- order 345: `READ_RESULT_PLACEHOLDER_PREFIXES` (constant), lines 5860-5869, exports `READ_RESULT_PLACEHOLDER_PREFIXES`
- order 346: `READ_CONTEXT_REGISTRY_MAX` (constant), lines 5870-5870, exports `READ_CONTEXT_REGISTRY_MAX`
- order 347: `READ_CONTEXT_PROMPT_MAX_ITEMS` (constant), lines 5871-5871, exports `READ_CONTEXT_PROMPT_MAX_ITEMS`
- order 348: `READ_CONTEXT_PROMPT_MAX_CHARS` (constant), lines 5872-5872, exports `READ_CONTEXT_PROMPT_MAX_CHARS`
- order 349: `READ_CONTEXT_SUMMARY_MAX_CHARS` (constant), lines 5873-5873, exports `READ_CONTEXT_SUMMARY_MAX_CHARS`
- order 350: `READ_CONTEXT_SHARED_MAX_ITEMS` (constant), lines 5874-5874, exports `READ_CONTEXT_SHARED_MAX_ITEMS`
- order 351: `READ_CONTEXT_POLICY_CHOICES` (constant), lines 5875-5875, exports `READ_CONTEXT_POLICY_CHOICES`
- order 352: `DEFAULT_READ_CONTEXT_POLICY` (constant), lines 5876-5876, exports `DEFAULT_READ_CONTEXT_POLICY`
- order 353: `READ_CONTEXT_CACHE_SEARCH_MAX_BYTES` (constant), lines 5877-5883, exports `READ_CONTEXT_CACHE_SEARCH_MAX_BYTES`
- order 354: `READ_CONTEXT_CACHE_SEARCH_MAX_MATCHES` (constant), lines 5884-5884, exports `READ_CONTEXT_CACHE_SEARCH_MAX_MATCHES`
- order 355: `READ_CONTEXT_CACHE_SNIPPET_CHARS` (constant), lines 5885-5885, exports `READ_CONTEXT_CACHE_SNIPPET_CHARS`
- order 356: `READ_CONTEXT_CACHE_LINE_CONTEXT` (constant), lines 5886-5886, exports `READ_CONTEXT_CACHE_LINE_CONTEXT`
- order 357: `LONG_CONTENT_SOURCE_CACHE_MAX_BYTES` (constant), lines 5887-5893, exports `LONG_CONTENT_SOURCE_CACHE_MAX_BYTES`
- order 358: `LONG_CONTENT_SOURCE_CACHE_MAX_FILES` (constant), lines 5894-5897, exports `LONG_CONTENT_SOURCE_CACHE_MAX_FILES`
- order 359: `LONG_CONTENT_SYMBOL_MEMORY_MAX` (constant), lines 5898-5901, exports `LONG_CONTENT_SYMBOL_MEMORY_MAX`
- order 360: `TOOL_MEMORY_REGISTRY_MAX` (constant), lines 5902-5902, exports `TOOL_MEMORY_REGISTRY_MAX`
- order 361: `TOOL_MEMORY_PROMPT_MAX_ITEMS` (constant), lines 5903-5903, exports `TOOL_MEMORY_PROMPT_MAX_ITEMS`
- order 362: `TOOL_MEMORY_PROMPT_MAX_CHARS` (constant), lines 5904-5904, exports `TOOL_MEMORY_PROMPT_MAX_CHARS`
- order 363: `TOOL_MEMORY_SUMMARY_MAX_CHARS` (constant), lines 5905-5905, exports `TOOL_MEMORY_SUMMARY_MAX_CHARS`
- order 364: `TOOL_MEMORY_SHARED_MAX_ITEMS` (constant), lines 5906-5906, exports `TOOL_MEMORY_SHARED_MAX_ITEMS`
- order 365: `TOOL_MEMORY_COMPACT_PIN_DISTINCT` (constant), lines 5907-5907, exports `TOOL_MEMORY_COMPACT_PIN_DISTINCT`
- order 366: `TOOL_MEMORY_COMPACT_PIN_MAX_CHARS` (constant), lines 5908-5908, exports `TOOL_MEMORY_COMPACT_PIN_MAX_CHARS`
- order 367: `TOOL_MEMORY_POLICY_CHOICES` (constant), lines 5909-5909, exports `TOOL_MEMORY_POLICY_CHOICES`
- order 368: `DEFAULT_TOOL_MEMORY_POLICY` (constant), lines 5910-5910, exports `DEFAULT_TOOL_MEMORY_POLICY`
- order 369: `LONG_CONTENT_MEMORY_VERSION` (constant), lines 5911-5923, exports `LONG_CONTENT_MEMORY_VERSION`
- order 370: `LONG_CONTENT_MEMORY_MAX_ITEMS` (constant), lines 5924-5927, exports `LONG_CONTENT_MEMORY_MAX_ITEMS`
- order 371: `LONG_CONTENT_MEMORY_MAX_SEGMENTS` (constant), lines 5928-5931, exports `LONG_CONTENT_MEMORY_MAX_SEGMENTS`
- order 372: `LONG_CONTENT_TEXT_SEGMENT_LINES` (constant), lines 5932-5935, exports `LONG_CONTENT_TEXT_SEGMENT_LINES`
- order 373: `LONG_CONTENT_CODE_SEGMENT_LINES` (constant), lines 5936-5939, exports `LONG_CONTENT_CODE_SEGMENT_LINES`
- order 374: `LONG_CONTENT_CARD_CHARS` (constant), lines 5940-5943, exports `LONG_CONTENT_CARD_CHARS`
- order 375: `LONG_CONTENT_STRUCTURE_MAX_CHARS` (constant), lines 5944-5947, exports `LONG_CONTENT_STRUCTURE_MAX_CHARS`
- order 376: `LONG_CONTENT_SEMANTIC_ENABLED` (constant), lines 5948-5955, exports `LONG_CONTENT_SEMANTIC_ENABLED`
- order 377: `LONG_CONTENT_SEMANTIC_TIMEOUT_SECONDS` (constant), lines 5956-5959, exports `LONG_CONTENT_SEMANTIC_TIMEOUT_SECONDS`
- order 378: `LONG_CONTENT_SEMANTIC_MAX_INPUT_CHARS` (constant), lines 5960-5963, exports `LONG_CONTENT_SEMANTIC_MAX_INPUT_CHARS`
- order 379: `LONG_CONTENT_SEMANTIC_MAX_OUTPUT_TOKENS` (constant), lines 5964-5967, exports `LONG_CONTENT_SEMANTIC_MAX_OUTPUT_TOKENS`
- order 380: `LONG_CONTENT_SEMANTIC_MAX_KEY_POINTS` (constant), lines 5968-5968, exports `LONG_CONTENT_SEMANTIC_MAX_KEY_POINTS`
- order 381: `LONG_CONTENT_SEMANTIC_MAX_DEFINITIONS` (constant), lines 5969-5969, exports `LONG_CONTENT_SEMANTIC_MAX_DEFINITIONS`
- order 382: `LONG_CONTENT_SEMANTIC_MAX_RELATIONS` (constant), lines 5970-5970, exports `LONG_CONTENT_SEMANTIC_MAX_RELATIONS`
- order 383: `LONG_CONTENT_SEMANTIC_MAX_UNCERTAINTIES` (constant), lines 5971-5971, exports `LONG_CONTENT_SEMANTIC_MAX_UNCERTAINTIES`
- order 384: `LONG_CONTENT_SEMANTIC_MAX_EVIDENCE` (constant), lines 5972-5972, exports `LONG_CONTENT_SEMANTIC_MAX_EVIDENCE`
- order 385: `LONG_CONTENT_SEMANTIC_MAX_NEXT_SEGMENTS` (constant), lines 5973-5973, exports `LONG_CONTENT_SEMANTIC_MAX_NEXT_SEGMENTS`
- order 386: `LONG_CONTENT_SEMANTIC_MAX_COVERED` (constant), lines 5974-5974, exports `LONG_CONTENT_SEMANTIC_MAX_COVERED`
- order 387: `LONG_CONTENT_SEMANTIC_MAX_OPEN_QUESTIONS` (constant), lines 5975-5975, exports `LONG_CONTENT_SEMANTIC_MAX_OPEN_QUESTIONS`
- order 388: `LONG_CONTENT_SEMANTIC_MAX_REFRESHES` (constant), lines 5976-5979, exports `LONG_CONTENT_SEMANTIC_MAX_REFRESHES`
- order 389: `LONG_CONTENT_OBSERVATION_MAX` (constant), lines 5980-5983, exports `LONG_CONTENT_OBSERVATION_MAX`
- order 390: `LONG_CONTENT_OBSERVATION_MAX_RANGES` (constant), lines 5984-5984, exports `LONG_CONTENT_OBSERVATION_MAX_RANGES`
- order 391: `LONG_CONTENT_OBSERVATION_MAX_EXCERPTS` (constant), lines 5985-5985, exports `LONG_CONTENT_OBSERVATION_MAX_EXCERPTS`
- order 392: `LONG_CONTENT_OBSERVATION_EXCERPT_CHARS` (constant), lines 5986-5986, exports `LONG_CONTENT_OBSERVATION_EXCERPT_CHARS`
- order 393: `LONG_CONTENT_RELATED_SOURCE_MAX` (constant), lines 5987-5987, exports `LONG_CONTENT_RELATED_SOURCE_MAX`
- order 394: `SHELL_SOURCE_CANDIDATE_MAX` (constant), lines 5988-5988, exports `SHELL_SOURCE_CANDIDATE_MAX`
- order 395: `LONG_CONTENT_TEXT_EXTS` (constant), lines 5989-5991, exports `LONG_CONTENT_TEXT_EXTS`
- order 396: `LONG_CONTENT_DATA_EXTS` (constant), lines 5992-5996, exports `LONG_CONTENT_DATA_EXTS`
- order 397: `DEFAULT_AUTO_TASK_LEVEL_CEILING` (constant), lines 5997-5997, exports `DEFAULT_AUTO_TASK_LEVEL_CEILING`
- order 403: `HARD_BREAK_TOOL_ERROR_THRESHOLD` (constant), lines 6017-6017, exports `HARD_BREAK_TOOL_ERROR_THRESHOLD`
- order 404: `HARD_BREAK_RECOVERY_ROUND_THRESHOLD` (constant), lines 6018-6020, exports `HARD_BREAK_RECOVERY_ROUND_THRESHOLD`
- order 405: `FUSED_FAULT_BREAK_THRESHOLD` (constant), lines 6021-6021, exports `FUSED_FAULT_BREAK_THRESHOLD`
- order 406: `STALL_SEVERITY_ESCALATION_THRESHOLD` (constant), lines 6022-6022, exports `STALL_SEVERITY_ESCALATION_THRESHOLD`
- order 407: `STALL_SEVERITY_WEIGHT_BASH_READ_LOOP` (constant), lines 6023-6023, exports `STALL_SEVERITY_WEIGHT_BASH_READ_LOOP`
- order 408: `STALL_SEVERITY_WEIGHT_REPEATED_TOOL` (constant), lines 6024-6024, exports `STALL_SEVERITY_WEIGHT_REPEATED_TOOL`
- order 409: `STALL_SEVERITY_WEIGHT_FAULT` (constant), lines 6025-6025, exports `STALL_SEVERITY_WEIGHT_FAULT`
- order 410: `STALL_SEVERITY_WEIGHT_RECOVERY_RETRY` (constant), lines 6026-6026, exports `STALL_SEVERITY_WEIGHT_RECOVERY_RETRY`
- order 411: `STALL_SEVERITY_WEIGHT_WATCHDOG` (constant), lines 6027-6027, exports `STALL_SEVERITY_WEIGHT_WATCHDOG`
- order 412: `STALL_SEVERITY_DECAY_ON_SUCCESS` (constant), lines 6028-6028, exports `STALL_SEVERITY_DECAY_ON_SUCCESS`
- order 413: `STALL_ESCALATION_MIN_LEVEL` (constant), lines 6029-6029, exports `STALL_ESCALATION_MIN_LEVEL`
- order 414: `STALL_PLAN_SYNTHESIS_MAX_TOKENS` (constant), lines 6030-6030, exports `STALL_PLAN_SYNTHESIS_MAX_TOKENS`
- order 415: `STALL_ESCALATION_CONTEXT_MAX_CHARS` (constant), lines 6031-6031, exports `STALL_ESCALATION_CONTEXT_MAX_CHARS`
- order 416: `MAX_RUN_SECONDS` (constant), lines 6032-6032, exports `MAX_RUN_SECONDS`
- order 417: `MIN_RUN_TIMEOUT_SECONDS` (constant), lines 6033-6033, exports `MIN_RUN_TIMEOUT_SECONDS`
- order 418: `MAX_RUN_TIMEOUT_SECONDS` (constant), lines 6034-6034, exports `MAX_RUN_TIMEOUT_SECONDS`
- order 419: `MIN_TIMEOUT_SECONDS` (constant), lines 6035-6035, exports `MIN_TIMEOUT_SECONDS`
- order 420: `MAX_TIMEOUT_SECONDS` (constant), lines 6036-6036, exports `MAX_TIMEOUT_SECONDS`
- order 421: `DEFAULT_TIMEOUT_SECONDS` (constant), lines 6037-6043, exports `DEFAULT_TIMEOUT_SECONDS`
- order 422: `DEFAULT_REQUEST_TIMEOUT` (constant), lines 6044-6044, exports `DEFAULT_REQUEST_TIMEOUT`
- order 423: `_SHELL_AUTO_CONFIRM_PATTERNS` (assignment), lines 6045-6060, exports `_SHELL_AUTO_CONFIRM_PATTERNS`
- order 424: `MIN_SHELL_COMMAND_TIMEOUT_SECONDS` (constant), lines 6061-6061, exports `MIN_SHELL_COMMAND_TIMEOUT_SECONDS`
- order 425: `MAX_SHELL_COMMAND_TIMEOUT_SECONDS` (constant), lines 6062-6062, exports `MAX_SHELL_COMMAND_TIMEOUT_SECONDS`
- order 426: `SHELL_TIMEOUT_MODES` (constant), lines 6063-6063, exports `SHELL_TIMEOUT_MODES`
- order 427: `_DEFAULT_SHELL_TIMEOUT_MODE_RAW` (assignment), lines 6064-6067, exports `_DEFAULT_SHELL_TIMEOUT_MODE_RAW`
- order 428: `DEFAULT_SHELL_TIMEOUT_MODE` (constant), lines 6068-6072, exports `DEFAULT_SHELL_TIMEOUT_MODE`
- order 429: `MIN_SHELL_ASYNC_HANDOFF_SECONDS` (constant), lines 6073-6073, exports `MIN_SHELL_ASYNC_HANDOFF_SECONDS`
- order 430: `MAX_SHELL_ASYNC_HANDOFF_SECONDS` (constant), lines 6074-6074, exports `MAX_SHELL_ASYNC_HANDOFF_SECONDS`
- order 431: `SHELL_FAILURE_GUIDANCE_SECONDS` (constant), lines 6075-6077, exports `SHELL_FAILURE_GUIDANCE_SECONDS`
- order 432: `DEFAULT_SHELL_ASYNC_HANDOFF_SECONDS` (constant), lines 6078-6092, exports `DEFAULT_SHELL_ASYNC_HANDOFF_SECONDS`
- order 433: `DEFAULT_SHELL_COMMAND_TIMEOUT_SECONDS` (constant), lines 6093-6107, exports `DEFAULT_SHELL_COMMAND_TIMEOUT_SECONDS`
- order 434: `DEFAULT_SINGLE_NO_PLAN_TODO_PROMPT` (constant), lines 6108-6122, exports `DEFAULT_SINGLE_NO_PLAN_TODO_PROMPT`
- order 435: `SINGLE_NO_PLAN_TODO_BOOTSTRAP_MAX_ATTEMPTS` (constant), lines 6123-6123, exports `SINGLE_NO_PLAN_TODO_BOOTSTRAP_MAX_ATTEMPTS`
- order 436: `AUTO_CONTINUE_BUDGET_DEFAULT` (constant), lines 6124-6124, exports `AUTO_CONTINUE_BUDGET_DEFAULT`
- order 437: `AGENT_MAX_OUTPUT_TOKENS` (constant), lines 6125-6125, exports `AGENT_MAX_OUTPUT_TOKENS`
- order 438: `OLLAMA_THINKING_TOOL_BUFFER` (constant), lines 6126-6126, exports `OLLAMA_THINKING_TOOL_BUFFER`
- order 439: `WATCHDOG_INTENT_NO_TOOL_THRESHOLD` (constant), lines 6127-6127, exports `WATCHDOG_INTENT_NO_TOOL_THRESHOLD`
- order 440: `WATCHDOG_REPEAT_NO_TOOL_THRESHOLD` (constant), lines 6128-6128, exports `WATCHDOG_REPEAT_NO_TOOL_THRESHOLD`
- order 441: `WATCHDOG_INTENT_NO_TOOL_THRESHOLD_SINGLE` (constant), lines 6129-6129, exports `WATCHDOG_INTENT_NO_TOOL_THRESHOLD_SINGLE`
- order 442: `WATCHDOG_REPEAT_NO_TOOL_THRESHOLD_SINGLE` (constant), lines 6130-6130, exports `WATCHDOG_REPEAT_NO_TOOL_THRESHOLD_SINGLE`
- order 443: `WATCHDOG_STATE_STALL_THRESHOLD` (constant), lines 6131-6131, exports `WATCHDOG_STATE_STALL_THRESHOLD`
- order 444: `WATCHDOG_CONTEXT_STALL_THRESHOLD` (constant), lines 6132-6132, exports `WATCHDOG_CONTEXT_STALL_THRESHOLD`
- order 445: `WATCHDOG_REPEAT_SIMILARITY_THRESHOLD` (constant), lines 6133-6133, exports `WATCHDOG_REPEAT_SIMILARITY_THRESHOLD`
- order 446: `WATCHDOG_CONTEXT_NEAR_RATIO` (constant), lines 6134-6134, exports `WATCHDOG_CONTEXT_NEAR_RATIO`
- order 447: `WATCHDOG_MAX_DECOMPOSE_STEPS` (constant), lines 6135-6135, exports `WATCHDOG_MAX_DECOMPOSE_STEPS`
- order 448: `WATCHDOG_STEP_MAX_ATTEMPTS` (constant), lines 6136-6136, exports `WATCHDOG_STEP_MAX_ATTEMPTS`
- order 449: `EMPTY_ACTION_MIN_CONTENT_CHARS` (constant), lines 6137-6137, exports `EMPTY_ACTION_MIN_CONTENT_CHARS`
- order 450: `EMPTY_ACTION_WAKEUP_RETRY_LIMIT` (constant), lines 6138-6138, exports `EMPTY_ACTION_WAKEUP_RETRY_LIMIT`
- order 451: `EMPTY_ACTION_INTERVENTION_THRESHOLD` (constant), lines 6139-6145, exports `EMPTY_ACTION_INTERVENTION_THRESHOLD`
- order 452: `EMPTY_ACTION_BOOTSTRAP_THINKING_GRACE_ROUNDS` (constant), lines 6146-6150, exports `EMPTY_ACTION_BOOTSTRAP_THINKING_GRACE_ROUNDS`
- order 453: `EMPTY_ACTION_RECOVERY_MAX_TOKENS` (constant), lines 6151-6151, exports `EMPTY_ACTION_RECOVERY_MAX_TOKENS`
- order 454: `THINKING_BUDGET_FORCE_RATIO` (constant), lines 6152-6152, exports `THINKING_BUDGET_FORCE_RATIO`
- order 455: `_TOOL_TIMEOUT_MAP` (assignment), lines 6153-6174, exports `_TOOL_TIMEOUT_MAP`
- order 456: `_DEFAULT_TOOL_TIMEOUT` (assignment), lines 6175-6175, exports `_DEFAULT_TOOL_TIMEOUT`
- order 459: `CONVERSATION_VISIBLE_TOOL_EVENTS` (constant), lines 6181-6193, exports `CONVERSATION_VISIBLE_TOOL_EVENTS`
- order 460: `PERSIST_ON_EVENT_TYPES` (constant), lines 6194-6212, exports `PERSIST_ON_EVENT_TYPES`
- order 461: `PERSIST_EVENT_MIN_INTERVAL_SECONDS` (constant), lines 6213-6213, exports `PERSIST_EVENT_MIN_INTERVAL_SECONDS`
- order 462: `TRUNCATION_CONTINUATION_MAX_PASSES` (constant), lines 6214-6214, exports `TRUNCATION_CONTINUATION_MAX_PASSES`
- order 463: `TRUNCATION_CONTINUATION_MAX_TOKENS` (constant), lines 6215-6215, exports `TRUNCATION_CONTINUATION_MAX_TOKENS`
- order 464: `TRUNCATION_CONTINUATION_TAIL_CHARS` (constant), lines 6216-6216, exports `TRUNCATION_CONTINUATION_TAIL_CHARS`
- order 465: `TRUNCATION_CONTINUATION_ECHO_CHARS` (constant), lines 6217-6217, exports `TRUNCATION_CONTINUATION_ECHO_CHARS`
- order 466: `TRUNCATION_OVERLAP_SCAN_CHARS` (constant), lines 6218-6218, exports `TRUNCATION_OVERLAP_SCAN_CHARS`
- order 467: `TRUNCATION_PAIR_SCAN_CHARS` (constant), lines 6219-6219, exports `TRUNCATION_PAIR_SCAN_CHARS`
- order 468: `TRUNCATION_LIVE_BUFFER_MAX_CHARS` (constant), lines 6220-6220, exports `TRUNCATION_LIVE_BUFFER_MAX_CHARS`
- order 469: `MIN_CONTEXT_TOKEN_LIMIT` (constant), lines 6221-6221, exports `MIN_CONTEXT_TOKEN_LIMIT`
- order 470: `COMPACT_TIER1_PCT` (constant), lines 6222-6223, exports `COMPACT_TIER1_PCT`
- order 471: `COMPACT_TIER2_PCT` (constant), lines 6224-6224, exports `COMPACT_TIER2_PCT`
- order 472: `COMPACT_TIER3_PCT` (constant), lines 6225-6225, exports `COMPACT_TIER3_PCT`
- order 473: `COMPACT_TIER1_ABS` (constant), lines 6226-6227, exports `COMPACT_TIER1_ABS`
- order 474: `COMPACT_TIER2_ABS` (constant), lines 6228-6228, exports `COMPACT_TIER2_ABS`
- order 475: `CONTEXT_COMPACT_INEFFECTIVE_COOLDOWN_SECONDS` (constant), lines 6229-6235, exports `CONTEXT_COMPACT_INEFFECTIVE_COOLDOWN_SECONDS`
- order 476: `FILE_BUFFER_CONTENT_THRESHOLD` (constant), lines 6236-6237, exports `FILE_BUFFER_CONTENT_THRESHOLD`
- order 477: `FILE_BUFFER_MAX_FILES` (constant), lines 6238-6238, exports `FILE_BUFFER_MAX_FILES`
- order 478: `AUTHORITATIVE_USER_GOAL_OPEN` (constant), lines 6239-6239, exports `AUTHORITATIVE_USER_GOAL_OPEN`
- order 479: `AUTHORITATIVE_USER_GOAL_CLOSE` (constant), lines 6240-6240, exports `AUTHORITATIVE_USER_GOAL_CLOSE`
- order 480: `AGENT_MSG_LIMIT_TIER0` (constant), lines 6241-6242, exports `AGENT_MSG_LIMIT_TIER0`
- order 481: `AGENT_MSG_LIMIT_TIER1` (constant), lines 6243-6243, exports `AGENT_MSG_LIMIT_TIER1`
- order 482: `AGENT_MSG_LIMIT_TIER2` (constant), lines 6244-6244, exports `AGENT_MSG_LIMIT_TIER2`
- order 483: `AGENT_MSG_LIMIT_TIER3` (constant), lines 6245-6245, exports `AGENT_MSG_LIMIT_TIER3`
- order 484: `AGENT_CTX_LIMIT_TIER0` (constant), lines 6246-6246, exports `AGENT_CTX_LIMIT_TIER0`
- order 485: `AGENT_CTX_LIMIT_TIER1` (constant), lines 6247-6247, exports `AGENT_CTX_LIMIT_TIER1`
- order 486: `AGENT_CTX_LIMIT_TIER2` (constant), lines 6248-6248, exports `AGENT_CTX_LIMIT_TIER2`
- order 487: `AGENT_CTX_LIMIT_TIER3` (constant), lines 6249-6249, exports `AGENT_CTX_LIMIT_TIER3`
- order 488: `MANAGER_CTX_LIMIT_TIER0` (constant), lines 6250-6250, exports `MANAGER_CTX_LIMIT_TIER0`
- order 489: `MANAGER_CTX_LIMIT_TIER1` (constant), lines 6251-6251, exports `MANAGER_CTX_LIMIT_TIER1`
- order 490: `MANAGER_CTX_LIMIT_TIER2` (constant), lines 6252-6252, exports `MANAGER_CTX_LIMIT_TIER2`
- order 491: `MANAGER_CTX_LIMIT_TIER3` (constant), lines 6253-6253, exports `MANAGER_CTX_LIMIT_TIER3`
- order 492: `MAX_CONTEXT_ARCHIVE_SEGMENTS` (constant), lines 6254-6254, exports `MAX_CONTEXT_ARCHIVE_SEGMENTS`
- order 493: `MAX_USER_BUBBLE_LOG` (constant), lines 6255-6256, exports `MAX_USER_BUBBLE_LOG`
- order 494: `MANAGER_INSTRUCTION_MAX_CHARS` (constant), lines 6257-6261, exports `MANAGER_INSTRUCTION_MAX_CHARS`
- order 495: `MANAGER_MOMENTUM_MAX_SKIPS` (constant), lines 6262-6267, exports `MANAGER_MOMENTUM_MAX_SKIPS`
- order 496: `MODEL_OUTPUT_RETRY_TIMES` (constant), lines 6268-6272, exports `MODEL_OUTPUT_RETRY_TIMES`
- order 497: `ARBITER_TRIGGER_MIN_CONTENT_CHARS` (constant), lines 6273-6273, exports `ARBITER_TRIGGER_MIN_CONTENT_CHARS`
- order 498: `ARBITER_VALID_PLANNING_STREAK_LIMIT` (constant), lines 6274-6274, exports `ARBITER_VALID_PLANNING_STREAK_LIMIT`
- order 499: `ARBITER_DEFAULT_TIMEOUT_SECONDS` (constant), lines 6275-6275, exports `ARBITER_DEFAULT_TIMEOUT_SECONDS`
- order 500: `ARBITER_DEFAULT_MAX_TOKENS` (constant), lines 6276-6276, exports `ARBITER_DEFAULT_MAX_TOKENS`
- order 501: `ARBITER_DEFAULT_TEMPERATURE` (constant), lines 6277-6277, exports `ARBITER_DEFAULT_TEMPERATURE`
- order 502: `LIVE_INPUT_DELAY_WRITE_ROUNDS` (constant), lines 6278-6278, exports `LIVE_INPUT_DELAY_WRITE_ROUNDS`
- order 503: `LIVE_INPUT_DELAY_TOOL_ROUNDS` (constant), lines 6279-6279, exports `LIVE_INPUT_DELAY_TOOL_ROUNDS`
- order 504: `LIVE_INPUT_DELAY_NORMAL_ROUNDS` (constant), lines 6280-6280, exports `LIVE_INPUT_DELAY_NORMAL_ROUNDS`
- order 505: `LIVE_INPUT_MAX_INJECTIONS` (constant), lines 6281-6281, exports `LIVE_INPUT_MAX_INJECTIONS`
- order 506: `LIVE_INPUT_REINJECT_INTERVAL` (constant), lines 6282-6282, exports `LIVE_INPUT_REINJECT_INTERVAL`
- order 507: `LIVE_INPUT_WEIGHT_BASE_DELAYED` (constant), lines 6283-6283, exports `LIVE_INPUT_WEIGHT_BASE_DELAYED`
- order 508: `LIVE_INPUT_WEIGHT_BASE_NORMAL` (constant), lines 6284-6284, exports `LIVE_INPUT_WEIGHT_BASE_NORMAL`
- order 509: `LIVE_INPUT_WEIGHT_STEP_DELAYED` (constant), lines 6285-6285, exports `LIVE_INPUT_WEIGHT_STEP_DELAYED`
- order 510: `LIVE_INPUT_WEIGHT_STEP_NORMAL` (constant), lines 6286-6286, exports `LIVE_INPUT_WEIGHT_STEP_NORMAL`
- order 512: `BENIGN_SOCKET_DEBUG_LOG_ENABLED` (constant), lines 6293-6299, exports `BENIGN_SOCKET_DEBUG_LOG_ENABLED`
- order 513: `BENIGN_SOCKET_LOG_INTERVAL_SECONDS` (constant), lines 6300-6300, exports `BENIGN_SOCKET_LOG_INTERVAL_SECONDS`
- order 514: `FINAL_SUMMARY_MIN_CHARS` (constant), lines 6301-6301, exports `FINAL_SUMMARY_MIN_CHARS`
- order 515: `FINAL_SUMMARY_STRICT_MIN_CHARS` (constant), lines 6302-6302, exports `FINAL_SUMMARY_STRICT_MIN_CHARS`
- order 516: `RUNTIME_CONTROL_HINT_PREFIXES` (constant), lines 6303-6324, exports `RUNTIME_CONTROL_HINT_PREFIXES`
- order 517: `UI_HIDDEN_RUNTIME_CONTROL_PREFIXES` (constant), lines 6325-6353, exports `UI_HIDDEN_RUNTIME_CONTROL_PREFIXES`
- order 518: `UI_PROJECTED_RUNTIME_CONTROL_TAGS` (constant), lines 6354-6376, exports `UI_PROJECTED_RUNTIME_CONTROL_TAGS`
- order 519: `UI_LEGACY_PROJECTED_RUNTIME_CONTROL_TAGS` (constant), lines 6377-6379, exports `UI_LEGACY_PROJECTED_RUNTIME_CONTROL_TAGS`
- order 520: `RETRY_RUNTIME_HINT_PREFIXES` (constant), lines 6380-6394, exports `RETRY_RUNTIME_HINT_PREFIXES`
- order 521: `EXECUTION_MODE_SINGLE` (constant), lines 6395-6395, exports `EXECUTION_MODE_SINGLE`
- order 522: `EXECUTION_MODE_SEQUENTIAL` (constant), lines 6396-6396, exports `EXECUTION_MODE_SEQUENTIAL`
- order 523: `EXECUTION_MODE_SYNC` (constant), lines 6397-6397, exports `EXECUTION_MODE_SYNC`
- order 524: `EXECUTION_MODE_CHOICES` (constant), lines 6398-6402, exports `EXECUTION_MODE_CHOICES`
- order 525: `AGENT_ROLES` (constant), lines 6403-6403, exports `AGENT_ROLES`
- order 526: `AGENT_BUBBLE_ROLES` (constant), lines 6404-6404, exports `AGENT_BUBBLE_ROLES`
- order 527: `AGENT_ROLE_LABELS` (constant), lines 6405-6411, exports `AGENT_ROLE_LABELS`
- order 528: `AGENT_ROLE_BUBBLE_COLORS` (constant), lines 6412-6418, exports `AGENT_ROLE_BUBBLE_COLORS`
- order 529: `BLACKBOARD_STATUSES` (constant), lines 6419-6428, exports `BLACKBOARD_STATUSES`
- order 530: `TASK_COMPLEXITY_LEVELS` (constant), lines 6429-6429, exports `TASK_COMPLEXITY_LEVELS`
- order 531: `TASK_COMPLEXITY_RANKS` (constant), lines 6430-6435, exports `TASK_COMPLEXITY_RANKS`
- order 532: `TASK_PROFILE_TYPES` (constant), lines 6436-6442, exports `TASK_PROFILE_TYPES`
- order 533: `TASK_LEVEL_CHOICES` (constant), lines 6443-6443, exports `TASK_LEVEL_CHOICES`
- order 534: `TASK_SCALE_PREFERENCES` (constant), lines 6444-6444, exports `TASK_SCALE_PREFERENCES`
- order 535: `SEMANTIC_CONFIDENCE_CHOICES` (constant), lines 6445-6445, exports `SEMANTIC_CONFIDENCE_CHOICES`
- order 536: `L2_TODO_POLICY_CHOICES` (constant), lines 6446-6450, exports `L2_TODO_POLICY_CHOICES`
- order 537: `DEFAULT_L2_TODO_POLICY` (constant), lines 6451-6451, exports `DEFAULT_L2_TODO_POLICY`
- order 538: `TASK_LEVEL_POLICIES` (constant), lines 6452-6505, exports `TASK_LEVEL_POLICIES`
- order 539: `MANAGER_ROUTE_TARGETS` (constant), lines 6506-6506, exports `MANAGER_ROUTE_TARGETS`
- order 540: `BLACKBOARD_MAX_LOG_ENTRIES` (constant), lines 6507-6507, exports `BLACKBOARD_MAX_LOG_ENTRIES`
- order 541: `BLACKBOARD_MAX_TEXT` (constant), lines 6508-6508, exports `BLACKBOARD_MAX_TEXT`
- order 542: `BLACKBOARD_MEMORY_SHORT_MAX` (constant), lines 6509-6509, exports `BLACKBOARD_MEMORY_SHORT_MAX`
- order 543: `BLACKBOARD_MEMORY_MID_MAX_STEPS` (constant), lines 6510-6510, exports `BLACKBOARD_MEMORY_MID_MAX_STEPS`
- order 544: `BLACKBOARD_MEMORY_MID_ITEMS_PER_STEP` (constant), lines 6511-6511, exports `BLACKBOARD_MEMORY_MID_ITEMS_PER_STEP`
- order 545: `BLACKBOARD_MEMORY_LONG_MAX` (constant), lines 6512-6512, exports `BLACKBOARD_MEMORY_LONG_MAX`
- order 546: `BLACKBOARD_MEMORY_INDEX_MAX` (constant), lines 6513-6513, exports `BLACKBOARD_MEMORY_INDEX_MAX`
- order 547: `SKILL_REFRESH_MIN_INTERVAL_SECONDS` (constant), lines 6514-6514, exports `SKILL_REFRESH_MIN_INTERVAL_SECONDS`
- order 552: `SKILL_RECALL_CACHE_TTL_SECONDS` (constant), lines 6525-6525, exports `SKILL_RECALL_CACHE_TTL_SECONDS`
- order 553: `SKILL_RECALL_CACHE_MAX_ENTRIES` (constant), lines 6526-6526, exports `SKILL_RECALL_CACHE_MAX_ENTRIES`
- order 554: `SKILL_RECALL_GENERIC_TOKENS` (constant), lines 6527-6533, exports `SKILL_RECALL_GENERIC_TOKENS`
- order 556: `SKILL_CATALOG_FULL_REFRESH_SECONDS` (constant), lines 6555-6558, exports `SKILL_CATALOG_FULL_REFRESH_SECONDS`
- order 557: `SKILL_PROMPT_MAX_ITEMS` (constant), lines 6559-6559, exports `SKILL_PROMPT_MAX_ITEMS`
- order 558: `SKILL_PROMPT_MAX_CHARS` (constant), lines 6560-6560, exports `SKILL_PROMPT_MAX_CHARS`
- order 559: `SKILL_RUNTIME_CACHE_MAX_ENTRIES` (constant), lines 6561-6561, exports `SKILL_RUNTIME_CACHE_MAX_ENTRIES`
- order 560: `SKILL_RUNTIME_CACHE_MAX_BYTES` (constant), lines 6562-6562, exports `SKILL_RUNTIME_CACHE_MAX_BYTES`
- order 561: `SKILL_AUTOLOAD_SCORE_THRESHOLD` (constant), lines 6563-6566, exports `SKILL_AUTOLOAD_SCORE_THRESHOLD`
- order 562: `SKILL_AUTOLOAD_CONFIDENCE_THRESHOLD` (constant), lines 6567-6567, exports `SKILL_AUTOLOAD_CONFIDENCE_THRESHOLD`
- order 563: `SKILL_RUNTIME_EVALUATION_TTL_SECONDS` (constant), lines 6568-6568, exports `SKILL_RUNTIME_EVALUATION_TTL_SECONDS`
- order 564: `SKILL_RUNTIME_EVALUATION_TIMEOUT_SECONDS` (constant), lines 6569-6569, exports `SKILL_RUNTIME_EVALUATION_TIMEOUT_SECONDS`
- order 565: `ACCEPTANCE_VERIFY_TIMEOUT_SECONDS` (constant), lines 6570-6575, exports `ACCEPTANCE_VERIFY_TIMEOUT_SECONDS`
- order 566: `SKILL_RUNTIME_UNLOAD_CONFIDENCE_THRESHOLD` (constant), lines 6576-6576, exports `SKILL_RUNTIME_UNLOAD_CONFIDENCE_THRESHOLD`
- order 567: `SKILL_RUNTIME_KEY_TOOL_INTERVAL` (constant), lines 6577-6577, exports `SKILL_RUNTIME_KEY_TOOL_INTERVAL`
- order 568: `SKILL_RUNTIME_EVENTS_MAX` (constant), lines 6578-6578, exports `SKILL_RUNTIME_EVENTS_MAX`
- order 569: `SKILL_METADATA_CAPSULE_MAX_CHARS` (constant), lines 6579-6579, exports `SKILL_METADATA_CAPSULE_MAX_CHARS`
- order 570: `SKILL_DEPENDENCY_MAX_DEPTH` (constant), lines 6580-6580, exports `SKILL_DEPENDENCY_MAX_DEPTH`
- order 571: `AUTO_SKILLS_ROOT_CANDIDATES` (constant), lines 6581-6581, exports `AUTO_SKILLS_ROOT_CANDIDATES`
- order 572: `SKILL_DEFAULT_ATTACHMENT_GLOBS` (constant), lines 6582-6612, exports `SKILL_DEFAULT_ATTACHMENT_GLOBS`
- order 573: `SKILL_INLINE_ATTACHMENT_MAX_FILES` (constant), lines 6613-6613, exports `SKILL_INLINE_ATTACHMENT_MAX_FILES`
- order 574: `SKILL_INLINE_ATTACHMENT_MAX_CHARS` (constant), lines 6614-6614, exports `SKILL_INLINE_ATTACHMENT_MAX_CHARS`
- order 575: `SKILL_RESOURCE_MANIFEST_MAX_ITEMS` (constant), lines 6615-6615, exports `SKILL_RESOURCE_MANIFEST_MAX_ITEMS`
- order 576: `SKILL_BODY_COMPACT_THRESHOLD_CHARS` (constant), lines 6616-6616, exports `SKILL_BODY_COMPACT_THRESHOLD_CHARS`
- order 577: `SKILL_BODY_PREVIEW_CHARS` (constant), lines 6617-6617, exports `SKILL_BODY_PREVIEW_CHARS`
- order 578: `SKILLS_VIRTUAL_PREFIX` (constant), lines 6618-6618, exports `SKILLS_VIRTUAL_PREFIX`
- order 579: `SKILLS_EXTERNAL_MOUNT` (constant), lines 6619-6619, exports `SKILLS_EXTERNAL_MOUNT`
- order 580: `PLAN_MODE_ENABLED_LEVELS` (constant), lines 6620-6620, exports `PLAN_MODE_ENABLED_LEVELS`
- order 581: `PLAN_MODE_FORCED_LEVELS` (constant), lines 6621-6621, exports `PLAN_MODE_FORCED_LEVELS`
- order 582: `PLAN_MODE_USER_CHOICES` (constant), lines 6622-6622, exports `PLAN_MODE_USER_CHOICES`
- order 583: `TASK_PHASES` (constant), lines 6623-6624, exports `TASK_PHASES`
- order 584: `TASK_PHASE_ROUTING` (constant), lines 6625-6632, exports `TASK_PHASE_ROUTING`
- order 585: `COMPLEXITY_KEYWORDS` (constant), lines 6633-6639, exports `COMPLEXITY_KEYWORDS`
- order 586: `USER_COMPLEXITY_SIMPLE_TOKENS` (constant), lines 6640-6644, exports `USER_COMPLEXITY_SIMPLE_TOKENS`
- order 587: `USER_COMPLEXITY_MODERATE_TOKENS` (constant), lines 6645-6649, exports `USER_COMPLEXITY_MODERATE_TOKENS`
- order 588: `USER_COMPLEXITY_COMPLEX_TOKENS` (constant), lines 6650-6654, exports `USER_COMPLEXITY_COMPLEX_TOKENS`
- order 589: `USER_COMPLEXITY_EXPERT_TOKENS` (constant), lines 6655-6659, exports `USER_COMPLEXITY_EXPERT_TOKENS`
- order 590: `PLAN_MODE_EXPLORER_MAX_ROUNDS` (constant), lines 6660-6663, exports `PLAN_MODE_EXPLORER_MAX_ROUNDS`
- order 591: `PLAN_MODE_EXPLORER_PRODUCTIVE_ROUNDS` (constant), lines 6664-6664, exports `PLAN_MODE_EXPLORER_PRODUCTIVE_ROUNDS`
- order 592: `PLAN_MODE_EXPLORER_STALE_ROUNDS` (constant), lines 6665-6665, exports `PLAN_MODE_EXPLORER_STALE_ROUNDS`
- order 593: `PLAN_MODE_SYNTHESIS_MAX_ATTEMPTS` (constant), lines 6666-6666, exports `PLAN_MODE_SYNTHESIS_MAX_ATTEMPTS`
- order 594: `REVIEWER_DEBUG_MODE_MAX_ROUNDS` (constant), lines 6667-6668, exports `REVIEWER_DEBUG_MODE_MAX_ROUNDS`
- order 595: `REVIEWER_DEBUG_TOOL_ALLOWLIST` (constant), lines 6669-6674, exports `REVIEWER_DEBUG_TOOL_ALLOWLIST`
- order 596: `EXPLORER_STALL_THRESHOLD` (constant), lines 6675-6675, exports `EXPLORER_STALL_THRESHOLD`
- order 597: `DEVELOPER_EDIT_STALL_THRESHOLD` (constant), lines 6676-6676, exports `DEVELOPER_EDIT_STALL_THRESHOLD`
- order 598: `ACCEPTANCE_GATE_STALL_THRESHOLD` (constant), lines 6677-6680, exports `ACCEPTANCE_GATE_STALL_THRESHOLD`
- order 599: `ACCEPTANCE_GATE_HARD_CEILING` (constant), lines 6681-6684, exports `ACCEPTANCE_GATE_HARD_CEILING`
- order 600: `ACCEPTANCE_GATE_TOTAL_ROUND_CEILING` (constant), lines 6685-6685, exports `ACCEPTANCE_GATE_TOTAL_ROUND_CEILING`
- order 601: `PLAN_MODE_MANAGER_SYNTHESIS_MAX_TOKENS` (constant), lines 6686-6686, exports `PLAN_MODE_MANAGER_SYNTHESIS_MAX_TOKENS`
- order 602: `PLAN_MODE_MAX_OPTIONS` (constant), lines 6687-6687, exports `PLAN_MODE_MAX_OPTIONS`
- order 603: `PLAN_FILE_RELATIVE_PATH` (constant), lines 6688-6688, exports `PLAN_FILE_RELATIVE_PATH`
- order 604: `PLAN_BUBBLE_MAX_CHARS` (constant), lines 6689-6689, exports `PLAN_BUBBLE_MAX_CHARS`
- order 605: `PLAN_NOTICE_BODY_MAX_CHARS` (constant), lines 6690-6690, exports `PLAN_NOTICE_BODY_MAX_CHARS`
- order 606: `PLAN_MESSAGE_EVENT_MAX_CHARS` (constant), lines 6691-6691, exports `PLAN_MESSAGE_EVENT_MAX_CHARS`
- order 607: `PLAN_STEP_FULL_CONTENT_MAX_CHARS` (constant), lines 6692-6692, exports `PLAN_STEP_FULL_CONTENT_MAX_CHARS`
- order 608: `PLAN_MODE_RESEARCH_TOOL_ALLOWLIST` (constant), lines 6693-6700, exports `PLAN_MODE_RESEARCH_TOOL_ALLOWLIST`
- order 609: `FAILURE_LEDGER_MAX_FIXES` (constant), lines 6701-6701, exports `FAILURE_LEDGER_MAX_FIXES`
- order 610: `FAILURE_LEDGER_MAX_COMPILE_ERRORS` (constant), lines 6702-6702, exports `FAILURE_LEDGER_MAX_COMPILE_ERRORS`
- order 611: `FAILURE_LEDGER_MAX_DELEGATIONS` (constant), lines 6703-6703, exports `FAILURE_LEDGER_MAX_DELEGATIONS`
- order 612: `FAILURE_LEDGER_MAX_STALLS` (constant), lines 6704-6704, exports `FAILURE_LEDGER_MAX_STALLS`
- order 613: `FAILURE_LEDGER_MAX_TOOL_FPS` (constant), lines 6705-6705, exports `FAILURE_LEDGER_MAX_TOOL_FPS`
- order 614: `FAILURE_LEDGER_MAX_ERRORS` (constant), lines 6706-6706, exports `FAILURE_LEDGER_MAX_ERRORS`
- order 615: `ERROR_CATEGORY_DEFS` (constant), lines 6707-6746, exports `ERROR_CATEGORY_DEFS`
- order 616: `CHECKPOINT_MAX_COUNT` (constant), lines 6747-6747, exports `CHECKPOINT_MAX_COUNT`
- order 617: `CHECKPOINT_INTERVAL_ROUNDS` (constant), lines 6748-6748, exports `CHECKPOINT_INTERVAL_ROUNDS`
- order 618: `PERSISTED_ROUTES_MAX` (constant), lines 6749-6749, exports `PERSISTED_ROUTES_MAX`
- order 619: `HTML_FRONTEND_REQUEST_KEYWORDS` (constant), lines 6750-6789, exports `HTML_FRONTEND_REQUEST_KEYWORDS`
- order 620: `DEEP_RESEARCH_REQUEST_KEYWORDS` (constant), lines 6790-6812, exports `DEEP_RESEARCH_REQUEST_KEYWORDS`
- order 621: `DEEP_RESEARCH_RETRIEVAL_KEYWORDS` (constant), lines 6813-6832, exports `DEEP_RESEARCH_RETRIEVAL_KEYWORDS`
- order 622: `DEEP_RESEARCH_TEXT_ONLY_HINT_KEYWORDS` (constant), lines 6833-6850, exports `DEEP_RESEARCH_TEXT_ONLY_HINT_KEYWORDS`
- order 623: `DANGEROUS_PATTERNS` (constant), lines 6851-6852, exports `DANGEROUS_PATTERNS`
- order 624: `VALID_MSG_TYPES` (constant), lines 6853-6859, exports `VALID_MSG_TYPES`
- order 625: `SUPPORTED_UI_LANGUAGES` (constant), lines 6860-6866, exports `SUPPORTED_UI_LANGUAGES`
- order 626: `UI_LANGUAGE_LABELS` (constant), lines 6867-6867, exports `UI_LANGUAGE_LABELS`
- order 627: `DEFAULT_UI_LANGUAGE` (constant), lines 6868-6868, exports `DEFAULT_UI_LANGUAGE`
- order 628: `PUBLIC_TOOL_PROGRESS_SUMMARY_ENABLED` (constant), lines 6869-6871, exports `PUBLIC_TOOL_PROGRESS_SUMMARY_ENABLED`
- order 629: `AGENT_LANGUAGE_PREFERENCES` (constant), lines 6872-6913, exports `AGENT_LANGUAGE_PREFERENCES`
- order 630: `UI_STYLE_CHOICES` (constant), lines 6914-6914, exports `UI_STYLE_CHOICES`
- order 631: `UI_STYLE_LABELS` (constant), lines 6915-6915, exports `UI_STYLE_LABELS`
- order 632: `DEFAULT_UI_STYLE` (constant), lines 6916-6916, exports `DEFAULT_UI_STYLE`
- order 633: `DEFAULT_WEB_UI_DIR` (constant), lines 6917-6917, exports `DEFAULT_WEB_UI_DIR`
- order 634: `DEFAULT_WEB_UI_CONFIG` (constant), lines 6918-6918, exports `DEFAULT_WEB_UI_CONFIG`
- order 635: `WEB_UI_REQUIRED_FILES` (constant), lines 6919-6926, exports `WEB_UI_REQUIRED_FILES`
- order 636: `WEB_UI_OPTIONAL_FILES` (constant), lines 6927-6927, exports `WEB_UI_OPTIONAL_FILES`
- order 637: `WEB_UI_APPLICATION_CONTRACT_VERSION` (constant), lines 6928-6928, exports `WEB_UI_APPLICATION_CONTRACT_VERSION`
- order 638: `WEB_UI_APPLICATION_FEATURE_MARKERS` (constant), lines 6929-6948, exports `WEB_UI_APPLICATION_FEATURE_MARKERS`
- order 639: `IMAGE_EXTS` (constant), lines 6949-6963, exports `IMAGE_EXTS`
- order 640: `IMAGE_FORMATS_NEED_CONVERSION` (constant), lines 6964-6964, exports `IMAGE_FORMATS_NEED_CONVERSION`
- order 641: `IMAGE_SAFE_FORMATS` (constant), lines 6965-6965, exports `IMAGE_SAFE_FORMATS`
- order 642: `AUDIO_EXTS` (constant), lines 6966-6976, exports `AUDIO_EXTS`
- order 643: `VIDEO_EXTS` (constant), lines 6977-6987, exports `VIDEO_EXTS`
- order 644: `CODE_PREVIEW_STAGE_MAX_BYTES` (constant), lines 6988-6988, exports `CODE_PREVIEW_STAGE_MAX_BYTES`
- order 645: `CODE_PREVIEW_STAGE_MAX_ROWS` (constant), lines 6989-6989, exports `CODE_PREVIEW_STAGE_MAX_ROWS`
- order 646: `CODE_PREVIEW_STAGE_MAX_PER_FILE` (constant), lines 6990-6990, exports `CODE_PREVIEW_STAGE_MAX_PER_FILE`
- order 647: `CODE_PREVIEW_STAGE_MAX_TOTAL` (constant), lines 6991-6991, exports `CODE_PREVIEW_STAGE_MAX_TOTAL`
- order 648: `CODE_PREVIEW_DIFF_CONTEXT_LINES` (constant), lines 6992-6992, exports `CODE_PREVIEW_DIFF_CONTEXT_LINES`
- order 649: `CODE_PREVIEW_DIFF_MERGE_GAP` (constant), lines 6993-6993, exports `CODE_PREVIEW_DIFF_MERGE_GAP`
- order 650: `PREVIEW_DOWNLOAD_MAX_FILES` (constant), lines 6994-6994, exports `PREVIEW_DOWNLOAD_MAX_FILES`
- order 651: `PREVIEW_DOWNLOAD_MAX_BYTES` (constant), lines 6995-6995, exports `PREVIEW_DOWNLOAD_MAX_BYTES`
- order 652: `FILES_TREE_DEFAULT_MAX_NODES` (constant), lines 6996-6996, exports `FILES_TREE_DEFAULT_MAX_NODES`
- order 653: `FILES_TREE_DEFAULT_MAX_DEPTH` (constant), lines 6997-6997, exports `FILES_TREE_DEFAULT_MAX_DEPTH`
- order 654: `FILES_TREE_SKIP_DIRS` (constant), lines 6998-7006, exports `FILES_TREE_SKIP_DIRS`
- order 655: `FILES_TREE_SKIP_REL_DIRS` (constant), lines 7007-7009, exports `FILES_TREE_SKIP_REL_DIRS`
- order 656: `IDE_FILE_MAX_BYTES` (constant), lines 7010-7010, exports `IDE_FILE_MAX_BYTES`
- order 657: `IDE_UPLOAD_MAX_BYTES` (constant), lines 7011-7011, exports `IDE_UPLOAD_MAX_BYTES`
- order 658: `IDE_UPLOAD_TOTAL_MAX_BYTES` (constant), lines 7012-7012, exports `IDE_UPLOAD_TOTAL_MAX_BYTES`
- order 659: `IDE_UPLOAD_MAX_ITEMS` (constant), lines 7013-7013, exports `IDE_UPLOAD_MAX_ITEMS`
- order 660: `IDE_UPLOAD_CHUNK_MAX_BYTES` (constant), lines 7014-7014, exports `IDE_UPLOAD_CHUNK_MAX_BYTES`
- order 661: `IDE_UPLOAD_STREAM_MAX_BYTES` (constant), lines 7015-7015, exports `IDE_UPLOAD_STREAM_MAX_BYTES`
- order 662: `IDE_TEXT_PREVIEW_MAX_BYTES` (constant), lines 7016-7016, exports `IDE_TEXT_PREVIEW_MAX_BYTES`
- order 663: `IDE_MARKDOWN_PREVIEW_MAX_LINES` (constant), lines 7017-7017, exports `IDE_MARKDOWN_PREVIEW_MAX_LINES`
- order 664: `IDE_IMAGE_PREVIEW_MAX_EDGE` (constant), lines 7018-7018, exports `IDE_IMAGE_PREVIEW_MAX_EDGE`
- order 665: `IDE_IMAGE_PREVIEW_MAX_PIXELS` (constant), lines 7019-7019, exports `IDE_IMAGE_PREVIEW_MAX_PIXELS`
- order 666: `IDE_IMAGE_PREVIEW_SOURCE_MAX_PIXELS` (constant), lines 7020-7020, exports `IDE_IMAGE_PREVIEW_SOURCE_MAX_PIXELS`
- order 667: `IDE_VECTOR_PREVIEW_MAX_BYTES` (constant), lines 7021-7021, exports `IDE_VECTOR_PREVIEW_MAX_BYTES`
- order 668: `IDE_TABLE_PREVIEW_SOURCE_MAX_BYTES` (constant), lines 7022-7022, exports `IDE_TABLE_PREVIEW_SOURCE_MAX_BYTES`
- order 669: `IDE_TABLE_PREVIEW_CELL_MAX_CHARS` (constant), lines 7023-7023, exports `IDE_TABLE_PREVIEW_CELL_MAX_CHARS`
- order 670: `IDE_TABLE_PREVIEW_TOTAL_CHARS` (constant), lines 7024-7024, exports `IDE_TABLE_PREVIEW_TOTAL_CHARS`
- order 671: `IDE_OFFICE_PREVIEW_MAX_ENTRIES` (constant), lines 7025-7025, exports `IDE_OFFICE_PREVIEW_MAX_ENTRIES`
- order 672: `IDE_OFFICE_PREVIEW_MAX_EXPANDED_BYTES` (constant), lines 7026-7026, exports `IDE_OFFICE_PREVIEW_MAX_EXPANDED_BYTES`
- order 673: `IDE_OFFICE_PREVIEW_MAX_ENTRY_BYTES` (constant), lines 7027-7027, exports `IDE_OFFICE_PREVIEW_MAX_ENTRY_BYTES`
- order 674: `IDE_COMMAND_TIMEOUT_DEFAULT` (constant), lines 7028-7028, exports `IDE_COMMAND_TIMEOUT_DEFAULT`
- order 675: `IDE_TREE_DEFAULT_MAX_NODES` (constant), lines 7029-7029, exports `IDE_TREE_DEFAULT_MAX_NODES`
- order 676: `IDE_TREE_MAX_NODES` (constant), lines 7030-7030, exports `IDE_TREE_MAX_NODES`
- order 677: `IDE_SEARCH_MAX_RESULTS` (constant), lines 7031-7031, exports `IDE_SEARCH_MAX_RESULTS`
- order 678: `IDE_SEARCH_MAX_FILE_BYTES` (constant), lines 7032-7032, exports `IDE_SEARCH_MAX_FILE_BYTES`
- order 679: `IDE_TERMINAL_SCROLLBACK_BYTES` (constant), lines 7033-7033, exports `IDE_TERMINAL_SCROLLBACK_BYTES`
- order 680: `IDE_TERMINAL_IDLE_SECONDS` (constant), lines 7034-7034, exports `IDE_TERMINAL_IDLE_SECONDS`
- order 681: `IDE_DEBUG_ADAPTER_START_ATTEMPTS` (constant), lines 7035-7035, exports `IDE_DEBUG_ADAPTER_START_ATTEMPTS`
- order 682: `IDE_DEBUG_ADAPTER_START_TIMEOUT_SECONDS` (constant), lines 7036-7036, exports `IDE_DEBUG_ADAPTER_START_TIMEOUT_SECONDS`
- order 683: `IDE_VSIX_MAX_BYTES` (constant), lines 7037-7037, exports `IDE_VSIX_MAX_BYTES`
- order 684: `IDE_VSIX_MAX_EXPANDED_BYTES` (constant), lines 7038-7038, exports `IDE_VSIX_MAX_EXPANDED_BYTES`
- order 685: `IDE_VSIX_MAX_FILES` (constant), lines 7039-7039, exports `IDE_VSIX_MAX_FILES`
- order 686: `IDE_VSIX_MAX_FILE_BYTES` (constant), lines 7040-7040, exports `IDE_VSIX_MAX_FILE_BYTES`
- order 687: `IDE_TREE_SKIP_DIRS` (constant), lines 7041-7049, exports `IDE_TREE_SKIP_DIRS`
- order 688: `RENDER_FRAME_MAX_B64_CHARS` (constant), lines 7050-7050, exports `RENDER_FRAME_MAX_B64_CHARS`
- order 689: `RENDER_FRAME_MAX_POINTS` (constant), lines 7051-7051, exports `RENDER_FRAME_MAX_POINTS`
- order 690: `RENDER_FRAME_MAX_LINES` (constant), lines 7052-7052, exports `RENDER_FRAME_MAX_LINES`
- order 691: `RENDER_FRAME_MAX_LINE_POINTS` (constant), lines 7053-7053, exports `RENDER_FRAME_MAX_LINE_POINTS`
- order 692: `RENDER_FRAME_ACTIVITY_INTERVAL_SECONDS` (constant), lines 7054-7054, exports `RENDER_FRAME_ACTIVITY_INTERVAL_SECONDS`
- order 693: `RAW_TOOLCALL_TEXT_FILTER_THRESHOLD` (constant), lines 7055-7055, exports `RAW_TOOLCALL_TEXT_FILTER_THRESHOLD`
- order 694: `ASSISTANT_TEXT_PERSIST_MAX_CHARS` (constant), lines 7056-7056, exports `ASSISTANT_TEXT_PERSIST_MAX_CHARS`
- order 695: `ASSISTANT_MESSAGE_EVENT_MAX_CHARS` (constant), lines 7057-7057, exports `ASSISTANT_MESSAGE_EVENT_MAX_CHARS`
- order 696: `CODE_PREVIEW_EXTS` (constant), lines 7058-7185, exports `CODE_PREVIEW_EXTS`
- order 697: `CODE_PREVIEW_FILENAMES` (constant), lines 7186-7237, exports `CODE_PREVIEW_FILENAMES`
- order 698: `MEDIA_CAPABILITY_KEYS` (constant), lines 7238-7245, exports `MEDIA_CAPABILITY_KEYS`
- order 702: `OFFLINE_JS_LIB_CATALOG` (constant), lines 7278-7604, exports `OFFLINE_JS_LIB_CATALOG`
- order 703: `OFFLINE_JS_ASSET_LOCK` (constant), lines 7605-7605, exports `OFFLINE_JS_ASSET_LOCK`
- order 704: `OFFLINE_JS_LIB_INDEX_FILE` (constant), lines 7606-7606, exports `OFFLINE_JS_LIB_INDEX_FILE`
- order 705: `OFFLINE_JS_LIB_README_FILE` (constant), lines 7607-7607, exports `OFFLINE_JS_LIB_README_FILE`
- order 716: `BACKEND_I18N` (constant), lines 7813-7884, exports `BACKEND_I18N`
- order 717: `_call_backend_i18n_en_update_7886` (expression), lines 7885-7986, exports —
- order 718: `_call_backend_i18n_zh_cn_update_7987` (expression), lines 7987-8087, exports —
- order 719: `_call_backend_i18n_zh_tw_update_8088` (expression), lines 8088-8188, exports —
- order 720: `_call_backend_i18n_ja_update_8189` (expression), lines 8189-8289, exports —
- order 943: `MODEL_RUNTIME_SETTING_KEYS` (constant), lines 14851-14856, exports `MODEL_RUNTIME_SETTING_KEYS`
- order 964: `LIQUID_KERNEL_STARTUP_POLICIES` (constant), lines 16557-16559, exports `LIQUID_KERNEL_STARTUP_POLICIES`
- order 965: `LIQUID_KERNEL_BOOTSTRAP_STATE_FILENAME` (constant), lines 16560-16560, exports `LIQUID_KERNEL_BOOTSTRAP_STATE_FILENAME`
- order 996: `TABULAR_PREVIEW_EXTS` (constant), lines 18498-18500, exports `TABULAR_PREVIEW_EXTS`
- order 997: `EXCEL_PREVIEW_EXTS` (constant), lines 18501-18501, exports `EXCEL_PREVIEW_EXTS`
- order 998: `PRESENTATION_PREVIEW_EXTS` (constant), lines 18502-18502, exports `PRESENTATION_PREVIEW_EXTS`
- order 999: `DOCUMENT_PREVIEW_EXTS` (constant), lines 18503-18503, exports `DOCUMENT_PREVIEW_EXTS`
- order 1080: `SESSION_LLM_PRIORITY_RANKS` (constant), lines 28016-28020, exports `SESSION_LLM_PRIORITY_RANKS`
- order 1086: `TODO_REVISION_FALLBACK_MAX_ROWS` (constant), lines 28030-28032, exports `TODO_REVISION_FALLBACK_MAX_ROWS`
- order 1101: `BASH_OPERATION_CODES` (constant), lines 31326-31348, exports `BASH_OPERATION_CODES`
- order 1102: `BASH_OBSERVATION_OPERATION_CODES` (constant), lines 31349-31360, exports `BASH_OBSERVATION_OPERATION_CODES`
- order 1103: `BASH_OPERATION_ALIASES` (constant), lines 31361-31387, exports `BASH_OPERATION_ALIASES`
- order 1236: `STUDIO_DEVICE_COOKIE` (constant), lines 123306-123323, exports `STUDIO_DEVICE_COOKIE`
- order 1237: `STUDIO_SESSION_COOKIE` (constant), lines 123324-123324, exports `STUDIO_SESSION_COOKIE`
- order 1238: `STUDIO_DEVICE_TTL` (constant), lines 123325-123325, exports `STUDIO_DEVICE_TTL`
- order 1239: `STUDIO_SESSION_TTL` (constant), lines 123326-123326, exports `STUDIO_SESSION_TTL`
- order 1240: `STUDIO_MAX_FILE_BYTES` (constant), lines 123327-123327, exports `STUDIO_MAX_FILE_BYTES`
- order 1241: `STUDIO_MAX_PROJECT_BYTES` (constant), lines 123328-123328, exports `STUDIO_MAX_PROJECT_BYTES`
- order 1242: `STUDIO_MAX_FILES` (constant), lines 123329-123329, exports `STUDIO_MAX_FILES`
- order 1243: `STUDIO_MAX_JOB_SECONDS` (constant), lines 123330-123330, exports `STUDIO_MAX_JOB_SECONDS`
- order 1249: `STUDIO_INDEX_HTML` (constant), lines 125229-125231, exports `STUDIO_INDEX_HTML`
- order 1250: `STUDIO_CSS` (constant), lines 125232-125232, exports `STUDIO_CSS`
- order 1251: `STUDIO_JS` (constant), lines 125233-125233, exports `STUDIO_JS`

### `config/paths.py`

- order 127: `SCRIPT_DIR` (constant), lines 5122-5122, exports `SCRIPT_DIR`
- order 152: `_resolve_default_agent_workdir` (function), lines 5216-5225, exports `_resolve_default_agent_workdir`
- order 153: `_is_installed_python_runtime` (function), lines 5226-5229, exports `_is_installed_python_runtime`
- order 154: `_runtime_storage_mode` (function), lines 5230-5236, exports `_runtime_storage_mode`
- order 155: `_runtime_tree_has_content` (function), lines 5237-5242, exports `_runtime_tree_has_content`
- order 156: `_copy_runtime_tree_with_crypto_migration` (function), lines 5243-5313, exports `_copy_runtime_tree_with_crypto_migration`
- order 157: `_merge_legacy_codes_root` (function), lines 5314-5379, exports `_merge_legacy_codes_root`
- order 158: `_migrate_legacy_runtime_roots` (function), lines 5380-5470, exports `_migrate_legacy_runtime_roots`
- order 159: `WORKDIR` (constant), lines 5471-5472, exports `WORKDIR`
- order 160: `CODES_ROOT` (constant), lines 5473-5473, exports `CODES_ROOT`
- order 161: `LLM_CONFIG_PATH` (constant), lines 5474-5474, exports `LLM_CONFIG_PATH`
- order 800: `detect_repo_root` (function), lines 9780-9794, exports `detect_repo_root`
- order 801: `REPO_ROOT` (constant), lines 9795-9796, exports `REPO_ROOT`

### `config/settings.py`

- order 709: `normalize_ui_language` (function), lines 7689-7713, exports `normalize_ui_language`
- order 710: `normalize_ui_style` (function), lines 7714-7733, exports `normalize_ui_style`
- order 711: `supported_ui_languages_payload` (function), lines 7734-7737, exports `supported_ui_languages_payload`
- order 713: `agent_language_preference_payload` (function), lines 7750-7759, exports `agent_language_preference_payload`
- order 714: `normalize_execution_mode` (function), lines 7760-7781, exports `normalize_execution_mode`
- order 715: `model_language_instruction` (function), lines 7782-7812, exports `model_language_instruction`
- order 721: `backend_i18n_text` (function), lines 8290-8302, exports `backend_i18n_text`
- order 722: `backend_role_label` (function), lines 8303-8309, exports `backend_role_label`
- order 723: `_detect_os_shell_instruction` (function), lines 8310-8351, exports `_detect_os_shell_instruction`
- order 724: `resolve_web_ui_dir_path` (function), lines 8352-8360, exports `resolve_web_ui_dir_path`
- order 725: `resolve_optional_file_path` (function), lines 8361-8370, exports `resolve_optional_file_path`
- order 726: `resolve_skills_root_path` (function), lines 8371-8380, exports `resolve_skills_root_path`
- order 727: `_count_skill_markdown_files` (function), lines 8381-8394, exports `_count_skill_markdown_files`
- order 728: `select_preferred_skills_root` (function), lines 8395-8431, exports `select_preferred_skills_root`
- order 729: `load_web_ui_config_file` (function), lines 8432-8448, exports `load_web_ui_config_file`
- order 730: `extract_show_upload_list_setting` (function), lines 8449-8465, exports `extract_show_upload_list_setting`
- order 731: `extract_ui_style_setting` (function), lines 8466-8482, exports `extract_ui_style_setting`
- order 732: `extract_js_lib_download_setting` (function), lines 8483-8504, exports `extract_js_lib_download_setting`
- order 733: `extract_daily_session_limit_setting` (function), lines 8505-8550, exports `extract_daily_session_limit_setting`
- order 734: `extract_shell_command_timeout_setting` (function), lines 8551-8599, exports `extract_shell_command_timeout_setting`
- order 735: `normalize_shell_timeout_mode` (function), lines 8600-8617, exports `normalize_shell_timeout_mode`
- order 736: `extract_shell_timeout_mode_setting` (function), lines 8618-8630, exports `extract_shell_timeout_mode_setting`
- order 737: `extract_shell_async_handoff_setting` (function), lines 8631-8658, exports `extract_shell_async_handoff_setting`
- order 738: `extract_context_token_limit_setting` (function), lines 8659-8693, exports `extract_context_token_limit_setting`
- order 739: `normalize_auto_task_level_ceiling` (function), lines 8694-8715, exports `normalize_auto_task_level_ceiling`
- order 740: `normalize_l2_todo_policy` (function), lines 8716-8751, exports `normalize_l2_todo_policy`
- order 741: `extract_l2_todo_policy_setting` (function), lines 8752-8794, exports `extract_l2_todo_policy_setting`
- order 742: `extract_auto_task_level_ceiling_setting` (function), lines 8795-8824, exports `extract_auto_task_level_ceiling_setting`
- order 743: `normalize_session_llm_concurrency` (function), lines 8825-8846, exports `normalize_session_llm_concurrency`
- order 744: `extract_session_llm_concurrency_setting` (function), lines 8847-8868, exports `extract_session_llm_concurrency_setting`
- order 745: `normalize_read_context_policy` (function), lines 8869-8889, exports `normalize_read_context_policy`
- order 746: `normalize_tool_memory_policy` (function), lines 8890-8893, exports `normalize_tool_memory_policy`
- order 747: `extract_read_context_policy_setting` (function), lines 8894-8917, exports `extract_read_context_policy_setting`
- order 748: `extract_tool_memory_policy_setting` (function), lines 8918-8941, exports `extract_tool_memory_policy_setting`
- order 750: `default_multimodal_capabilities` (function), lines 8948-8958, exports `default_multimodal_capabilities`
- order 751: `_to_bool_like` (function), lines 8959-8971, exports `_to_bool_like`
- order 752: `extract_web_search_enabled_setting` (function), lines 8972-8984, exports `extract_web_search_enabled_setting`
- order 753: `_single_no_plan_todo_setting_sections` (function), lines 8985-9011, exports `_single_no_plan_todo_setting_sections`
- order 754: `_single_no_plan_todo_setting_present` (function), lines 9012-9037, exports `_single_no_plan_todo_setting_present`
- order 755: `extract_single_no_plan_todo_settings` (function), lines 9038-9084, exports `extract_single_no_plan_todo_settings`
- order 756: `normalize_user_memory_mode` (function), lines 9085-9115, exports `normalize_user_memory_mode`
- order 757: `user_memory_enabled_from_mode` (function), lines 9116-9119, exports `user_memory_enabled_from_mode`
- order 758: `extract_user_memory_mode_setting` (function), lines 9120-9159, exports `extract_user_memory_mode_setting`
- order 759: `set_web_search_enabled_on_runtime` (function), lines 9160-9175, exports `set_web_search_enabled_on_runtime`
- order 760: `infer_model_multimodal_capabilities` (function), lines 9176-9222, exports `infer_model_multimodal_capabilities`
- order 761: `parse_capability_overrides` (function), lines 9223-9262, exports `parse_capability_overrides`
- order 762: `merge_multimodal_capabilities` (function), lines 9263-9272, exports `merge_multimodal_capabilities`
- order 763: `parse_media_endpoints` (function), lines 9273-9289, exports `parse_media_endpoints`
- order 779: `extract_runtime_region_hint_setting` (function), lines 9467-9492, exports `extract_runtime_region_hint_setting`
- order 780: `extract_runtime_timezone_hint_setting` (function), lines 9493-9510, exports `extract_runtime_timezone_hint_setting`
- order 781: `runtime_environment_context_snapshot` (function), lines 9511-9560, exports `runtime_environment_context_snapshot`
- order 782: `runtime_environment_context_block` (function), lines 9561-9590, exports `runtime_environment_context_block`
- order 879: `extract_ollama_model_capabilities` (function), lines 13656-13678, exports `extract_ollama_model_capabilities`
- order 908: `infer_user_complexity_value` (function), lines 14250-14267, exports `infer_user_complexity_value`
- order 909: `normalize_task_complexity` (function), lines 14268-14297, exports `normalize_task_complexity`
- order 910: `task_complexity_rank` (function), lines 14298-14300, exports `task_complexity_rank`
- order 911: `task_complexity_at_least` (function), lines 14301-14303, exports `task_complexity_at_least`
- order 912: `max_task_complexity` (function), lines 14304-14314, exports `max_task_complexity`
- order 944: `merge_probed_models_into_profile` (function), lines 14857-14902, exports `merge_probed_models_into_profile`
- order 945: `probe_and_merge_model_profiles` (function), lines 14903-14960, exports `probe_and_merge_model_profiles`
- order 946: `normalize_model_runtime_settings` (function), lines 14961-14986, exports `normalize_model_runtime_settings`
- order 947: `apply_model_runtime_settings` (function), lines 14987-15002, exports `apply_model_runtime_settings`
- order 948: `model_runtime_settings_for` (function), lines 15003-15013, exports `model_runtime_settings_for`
- order 949: `apply_model_option_runtime_fields` (function), lines 15014-15026, exports `apply_model_option_runtime_fields`
- order 952: `load_llm_config_from_source` (function), lines 15059-15094, exports `load_llm_config_from_source`
- order 953: `parse_llm_config_profiles` (function), lines 15095-15960, exports `parse_llm_config_profiles`
- order 954: `looks_like_llm_config` (function), lines 15961-16050, exports `looks_like_llm_config`
- order 958: `parse_front_matter` (function), lines 16246-16474, exports `parse_front_matter`
- order 966: `normalize_liquid_kernel_startup_policy` (function), lines 16561-16565, exports `normalize_liquid_kernel_startup_policy`
- order 994: `normalize_upload_rel_path` (function), lines 18452-18486, exports `normalize_upload_rel_path`
- order 1104: `normalize_bash_operation` (function), lines 31388-31405, exports `normalize_bash_operation`

### `ide/assets.py`

- order 1228: `IDE_INDEX_HTML` (constant), lines 122148-122303, exports `IDE_INDEX_HTML`
- order 1229: `IDE_CSS` (constant), lines 122304-122345, exports `IDE_CSS`
- order 1230: `IDE_JS` (constant), lines 122346-122539, exports `IDE_JS`
- order 1231: `IDE_CSS` (constant), lines 122540-122561, exports `IDE_CSS`
- order 1232: `IDE_JS` (constant), lines 122562-122825, exports `IDE_JS`
- order 1233: `IDE_JS` (constant), lines 122826-122954, exports `IDE_JS`
- order 1234: `IDE_JS` (constant), lines 122955-123178, exports `IDE_JS`
- order 1235: `IDE_JS` (constant), lines 123179-123305, exports `IDE_JS`

### `ide/auth.py`

- order 972: `IDEAuthError` (class), lines 16902-16909, exports `IDEAuthError`
- order 973: `IDEAuthStore` (class), lines 16910-17633, exports `IDEAuthStore`

### `ide/errors.py`

- order 974: `IDECapabilityError` (class), lines 17634-17640, exports `IDECapabilityError`
- order 975: `IDEFileConflict` (class), lines 17641-17648, exports `IDEFileConflict`

### `ide/events.py`

- order 835: `ide_public_operation_data` (function), lines 10679-10730, exports `ide_public_operation_data`

### `ide/handler.py`

- order 1268: `IdeHandler` (class), lines 141335-142991, exports `IdeHandler`

### `ide/preview.py`

- order 993: `normalize_rel_preview_path` (function), lines 18438-18451, exports `normalize_rel_preview_path`
- order 995: `is_code_preview_candidate` (function), lines 18487-18497, exports `is_code_preview_candidate`
- order 1000: `preview_kind_for_path` (function), lines 18504-18533, exports `preview_kind_for_path`
- order 1001: `normalize_markdown_preview_text` (function), lines 18534-18567, exports `normalize_markdown_preview_text`
- order 1002: `_preview_markdown_value_html` (function), lines 18568-18588, exports `_preview_markdown_value_html`
- order 1003: `_preview_markdown_frontmatter_html` (function), lines 18589-18604, exports `_preview_markdown_frontmatter_html`
- order 1004: `_preview_markdown_task_lists` (function), lines 18605-18618, exports `_preview_markdown_task_lists`
- order 1005: `_preview_markdown_fallback_inline` (function), lines 18619-18660, exports `_preview_markdown_fallback_inline`
- order 1006: `_preview_markdown_fallback_html` (function), lines 18661-18757, exports `_preview_markdown_fallback_html`
- order 1009: `workspace_file_revision_map` (function), lines 18798-18822, exports `workspace_file_revision_map`
- order 1010: `workspace_revision_delta` (function), lines 18823-18829, exports `workspace_revision_delta`
- order 1011: `build_code_preview_rows` (function), lines 18830-18878, exports `build_code_preview_rows`

### `ide/sandbox.py`

- order 787: `_windows_subprocess_encodings` (function), lines 9618-9635, exports `_windows_subprocess_encodings`
- order 1119: `_IDE_SANDBOX_BACKEND_CACHE` (assignment), lines 32171-32179, exports `_IDE_SANDBOX_BACKEND_CACHE`
- order 1120: `_IDE_SANDBOX_BACKEND_LOCK` (assignment), lines 32180-32180, exports `_IDE_SANDBOX_BACKEND_LOCK`
- order 1121: `WINDOWS_JOB_SANDBOX_MARKER` (constant), lines 32181-32181, exports `WINDOWS_JOB_SANDBOX_MARKER`
- order 1122: `_WINDOWS_LOW_INTEGRITY_ROOTS` (assignment), lines 32182-32182, exports `_WINDOWS_LOW_INTEGRITY_ROOTS`
- order 1123: `_WINDOWS_LOW_INTEGRITY_FAILED_ROOTS` (assignment), lines 32183-32183, exports `_WINDOWS_LOW_INTEGRITY_FAILED_ROOTS`
- order 1124: `_WINDOWS_LOW_INTEGRITY_LOCK` (assignment), lines 32184-32184, exports `_WINDOWS_LOW_INTEGRITY_LOCK`
- order 1125: `_is_windows_job_sandbox_prefix` (function), lines 32185-32191, exports `_is_windows_job_sandbox_prefix`
- order 1126: `_windows_builtin_sandbox_probe` (function), lines 32192-32215, exports `_windows_builtin_sandbox_probe`
- order 1127: `_windows_last_error` (function), lines 32216-32223, exports `_windows_last_error`
- order 1128: `_windows_set_integrity_label` (function), lines 32224-32277, exports `_windows_set_integrity_label`
- order 1129: `_windows_set_low_integrity_label` (function), lines 32278-32280, exports `_windows_set_low_integrity_label`
- order 1130: `_windows_protect_application_snapshot` (function), lines 32281-32304, exports `_windows_protect_application_snapshot`
- order 1131: `_windows_prepare_low_integrity_workspace` (function), lines 32305-32342, exports `_windows_prepare_low_integrity_workspace`
- order 1132: `_windows_job_memory_limit` (function), lines 32343-32350, exports `_windows_job_memory_limit`
- order 1133: `_windows_lower_process_integrity` (function), lines 32351-32398, exports `_windows_lower_process_integrity`
- order 1134: `_windows_attach_sandbox_job` (function), lines 32399-32491, exports `_windows_attach_sandbox_job`
- order 1135: `_windows_close_sandbox_job` (function), lines 32492-32508, exports `_windows_close_sandbox_job`
- order 1136: `_popen_windows_sandboxed` (function), lines 32509-32540, exports `_popen_windows_sandboxed`
- order 1137: `_run_windows_sandboxed_command` (function), lines 32541-32594, exports `_run_windows_sandboxed_command`
- order 1138: `_detect_ide_sandbox_backend` (function), lines 32595-32702, exports `_detect_ide_sandbox_backend`

### `ide/toolchains.py`

- order 548: `IDE_TOOLCHAIN_CACHE_TTL_SECONDS` (constant), lines 6515-6521, exports `IDE_TOOLCHAIN_CACHE_TTL_SECONDS`
- order 549: `_IDE_TOOLCHAIN_CACHE_LOCK` (assignment), lines 6522-6522, exports `_IDE_TOOLCHAIN_CACHE_LOCK`
- order 550: `_IDE_TOOLCHAIN_CACHE` (assignment), lines 6523-6523, exports `_IDE_TOOLCHAIN_CACHE`
- order 551: `_IDE_TOOLCHAIN_REFRESHING` (assignment), lines 6524-6524, exports `_IDE_TOOLCHAIN_REFRESHING`
- order 1255: `_ide_toolchain_cache_key` (function), lines 125238-125248, exports `_ide_toolchain_cache_key`
- order 1256: `_probe_ide_toolchains` (function), lines 125249-125292, exports `_probe_ide_toolchains`
- order 1257: `_refresh_ide_toolchains_in_background` (function), lines 125293-125302, exports `_refresh_ide_toolchains_in_background`

### `llm/client.py`

- order 1079: `OllamaError` (class), lines 27974-28015, exports `OllamaError`
- order 1099: `OllamaClient` (class), lines 28452-31311, exports `OllamaClient`

### `llm/constants.py`

- order 125: `DEFAULT_OLLAMA_BASE_URL` (constant), lines 5120-5120, exports `DEFAULT_OLLAMA_BASE_URL`
- order 126: `DEFAULT_OLLAMA_MODEL` (constant), lines 5121-5121, exports `DEFAULT_OLLAMA_MODEL`
- order 914: `OPENAI_COMPAT_PROVIDER_NAMES` (constant), lines 14332-14341, exports `OPENAI_COMPAT_PROVIDER_NAMES`
- order 915: `OPENAI_LIKE_PROVIDER_NAMES` (constant), lines 14342-14343, exports `OPENAI_LIKE_PROVIDER_NAMES`
- order 918: `EFFORT_OFF` (constant), lines 14350-14361, exports `EFFORT_OFF`
- order 919: `EFFORT_LOW` (constant), lines 14362-14362, exports `EFFORT_LOW`
- order 920: `EFFORT_MEDIUM` (constant), lines 14363-14363, exports `EFFORT_MEDIUM`
- order 921: `EFFORT_HIGH` (constant), lines 14364-14364, exports `EFFORT_HIGH`
- order 922: `EFFORT_MAX` (constant), lines 14365-14365, exports `EFFORT_MAX`
- order 923: `EFFORT_LEVELS` (constant), lines 14366-14366, exports `EFFORT_LEVELS`
- order 924: `EFFORT_ORDER` (constant), lines 14367-14367, exports `EFFORT_ORDER`
- order 925: `EFFORT_DEFAULT` (constant), lines 14368-14368, exports `EFFORT_DEFAULT`
- order 926: `EFFORT_ANTHROPIC_BUDGET` (constant), lines 14369-14376, exports `EFFORT_ANTHROPIC_BUDGET`
- order 927: `EFFORT_OPENAI_REASONING` (constant), lines 14377-14383, exports `EFFORT_OPENAI_REASONING`
- order 928: `TASK_LEVEL_EFFORT` (constant), lines 14384-14393, exports `TASK_LEVEL_EFFORT`
- order 929: `ROLE_EFFORT_FLOOR` (constant), lines 14394-14399, exports `ROLE_EFFORT_FLOOR`
- order 930: `COORDINATION_EFFORT` (constant), lines 14400-14403, exports `COORDINATION_EFFORT`

### `llm/gate.py`

- order 398: `SESSION_LLM_CONCURRENCY_MIN` (constant), lines 5998-6002, exports `SESSION_LLM_CONCURRENCY_MIN`
- order 399: `SESSION_LLM_CONCURRENCY_MAX` (constant), lines 6003-6003, exports `SESSION_LLM_CONCURRENCY_MAX`
- order 400: `SESSION_LLM_CONCURRENCY_FACTORY_DEFAULT` (constant), lines 6004-6004, exports `SESSION_LLM_CONCURRENCY_FACTORY_DEFAULT`
- order 401: `_session_llm_concurrency_env_default` (function), lines 6005-6013, exports `_session_llm_concurrency_env_default`
- order 402: `DEFAULT_SESSION_LLM_CONCURRENCY` (constant), lines 6014-6016, exports `DEFAULT_SESSION_LLM_CONCURRENCY`
- order 1081: `SESSION_LLM_GATE_POLL_SECONDS` (constant), lines 28021-28021, exports `SESSION_LLM_GATE_POLL_SECONDS`
- order 1082: `SESSION_LLM_GATE_SNAPSHOT_MAX_REQUESTS` (constant), lines 28022-28022, exports `SESSION_LLM_GATE_SNAPSHOT_MAX_REQUESTS`
- order 1083: `SESSION_LLM_CONCURRENCY_PUSH_INTERVAL_SECONDS` (constant), lines 28023-28025, exports `SESSION_LLM_CONCURRENCY_PUSH_INTERVAL_SECONDS`
- order 1084: `TODO_LLM_CALL_BUDGET` (constant), lines 28026-28028, exports `TODO_LLM_CALL_BUDGET`
- order 1085: `TODO_LLM_TIMEOUT_FACTORY_DEFAULT` (constant), lines 28029-28029, exports `TODO_LLM_TIMEOUT_FACTORY_DEFAULT`
- order 1087: `_todo_llm_timeout_env_default` (function), lines 28033-28043, exports `_todo_llm_timeout_env_default`
- order 1088: `TODO_LLM_TIMEOUT_SECONDS` (constant), lines 28044-28049, exports `TODO_LLM_TIMEOUT_SECONDS`
- order 1089: `LLMGateBusy` (class), lines 28050-28059, exports `LLMGateBusy`
- order 1090: `TodoLLMBudgetExhausted` (class), lines 28060-28063, exports `TodoLLMBudgetExhausted`
- order 1091: `_TODO_LLM_BUDGET_LOCAL` (assignment), lines 28064-28066, exports `_TODO_LLM_BUDGET_LOCAL`
- order 1092: `todo_llm_budget_scope` (function), lines 28067-28092, exports `todo_llm_budget_scope`
- order 1093: `_consume_todo_llm_budget` (function), lines 28093-28104, exports `_consume_todo_llm_budget`
- order 1094: `todo_llm_budget_active` (function), lines 28105-28109, exports `todo_llm_budget_active`
- order 1095: `todo_llm_skip_reason` (function), lines 28110-28137, exports `todo_llm_skip_reason`
- order 1096: `SessionLLMGate` (class), lines 28138-28438, exports `SessionLLMGate`
- order 1097: `_SESSION_LLM_GATE_INIT_LOCK` (assignment), lines 28439-28441, exports `_SESSION_LLM_GATE_INIT_LOCK`
- order 1098: `set_session_llm_concurrency_on_runtime` (function), lines 28442-28451, exports `set_session_llm_concurrency_on_runtime`

### `llm/utils.py`

- order 878: `probe_ollama_environment` (function), lines 13641-13655, exports `probe_ollama_environment`
- order 880: `probe_ollama_model_records` (function), lines 13679-13712, exports `probe_ollama_model_records`
- order 881: `list_ollama_models` (function), lines 13713-13717, exports `list_ollama_models`
- order 882: `_OLLAMA_TAG_CACHE_LOCK` (assignment), lines 13718-13719, exports `_OLLAMA_TAG_CACHE_LOCK`
- order 883: `_OLLAMA_TAG_CACHE` (assignment), lines 13720-13720, exports `_OLLAMA_TAG_CACHE`
- order 886: `_fetch_ollama_models_cached` (function), lines 13729-13754, exports `_fetch_ollama_models_cached`
- order 887: `list_ollama_models_cached` (function), lines 13755-13800, exports `list_ollama_models_cached`
- order 888: `resolve_ollama_model` (function), lines 13801-13812, exports `resolve_ollama_model`
- order 889: `infer_thinking_model` (function), lines 13813-13816, exports `infer_thinking_model`
- order 890: `split_thinking_content` (function), lines 13817-13861, exports `split_thinking_content`
- order 891: `strip_thinking_content` (function), lines 13862-13864, exports `strip_thinking_content`
- order 892: `check_ollama_model_ready` (function), lines 13865-13890, exports `check_ollama_model_ready`
- order 893: `list_loaded_ollama_models` (function), lines 13891-13905, exports `list_loaded_ollama_models`
- order 894: `wake_ollama_model` (function), lines 13906-13937, exports `wake_ollama_model`
- order 895: `try_pull_ollama_model` (function), lines 13938-13956, exports `try_pull_ollama_model`
- order 896: `ordered_model_candidates` (function), lines 13957-13976, exports `ordered_model_candidates`
- order 897: `pick_working_ollama_model` (function), lines 13977-13994, exports `pick_working_ollama_model`
- order 904: `evolution_worker_chat_messages` (function), lines 14152-14203, exports `evolution_worker_chat_messages`
- order 906: `extract_base_url` (function), lines 14229-14238, exports `extract_base_url`
- order 907: `complete_chat_endpoint` (function), lines 14239-14249, exports `complete_chat_endpoint`
- order 913: `normalize_openai_compat_provider_name` (function), lines 14315-14331, exports `normalize_openai_compat_provider_name`
- order 916: `is_openai_compat_provider` (function), lines 14344-14346, exports `is_openai_compat_provider`
- order 917: `is_openai_like_provider` (function), lines 14347-14349, exports `is_openai_like_provider`
- order 931: `clamp_effort` (function), lines 14404-14415, exports `clamp_effort`
- order 932: `model_reasoning_style` (function), lines 14416-14458, exports `model_reasoning_style`
- order 933: `resolve_reasoning_payload` (function), lines 14459-14521, exports `resolve_reasoning_payload`
- order 934: `openai_compat_probe_headers` (function), lines 14522-14540, exports `openai_compat_probe_headers`
- order 935: `openai_compat_model_list_urls` (function), lines 14541-14574, exports `openai_compat_model_list_urls`
- order 936: `anthropic_model_list_url` (function), lines 14575-14589, exports `anthropic_model_list_url`
- order 937: `extract_openai_compat_model_ids` (function), lines 14590-14624, exports `extract_openai_compat_model_ids`
- order 938: `extract_openai_compat_model_records` (function), lines 14625-14704, exports `extract_openai_compat_model_records`
- order 939: `_PROVIDER_MODEL_CACHE_LOCK` (assignment), lines 14705-14707, exports `_PROVIDER_MODEL_CACHE_LOCK`
- order 940: `_PROVIDER_MODEL_CACHE` (assignment), lines 14708-14708, exports `_PROVIDER_MODEL_CACHE`
- order 941: `_fetch_provider_models_cached` (function), lines 14709-14782, exports `_fetch_provider_models_cached`
- order 942: `probe_provider_models` (function), lines 14783-14850, exports `probe_provider_models`
- order 950: `_is_http_url` (function), lines 15027-15040, exports `_is_http_url`
- order 951: `_resolve_local_path` (function), lines 15041-15058, exports `_resolve_local_path`

### `mcp/constants.py`

- order 179: `MCP_SERVICE_PORT_OFFSET` (constant), lines 5492-5492, exports `MCP_SERVICE_PORT_OFFSET`
- order 1059: `MCP_PROTOCOL_VERSION` (constant), lines 26592-26621, exports `MCP_PROTOCOL_VERSION`
- order 1060: `MCP_NAME_RE` (constant), lines 26622-26622, exports `MCP_NAME_RE`
- order 1061: `MCP_TOOL_PREFIX` (constant), lines 26623-26623, exports `MCP_TOOL_PREFIX`
- order 1062: `_MCP_DEFAULT_HANDSHAKE_TIMEOUT` (assignment), lines 26624-26624, exports `_MCP_DEFAULT_HANDSHAKE_TIMEOUT`
- order 1063: `_MCP_DEFAULT_CALL_TIMEOUT` (assignment), lines 26625-26625, exports `_MCP_DEFAULT_CALL_TIMEOUT`
- order 1064: `_MCP_MAX_RESULT_CHARS` (assignment), lines 26626-26626, exports `_MCP_MAX_RESULT_CHARS`
- order 1065: `_MCP_TRUST_STORE_VERSION` (assignment), lines 26627-26627, exports `_MCP_TRUST_STORE_VERSION`

### `mcp/driver.py`

- order 1066: `mcp_normalize_name` (function), lines 26628-26637, exports `mcp_normalize_name`
- order 1067: `mcp_normalize_server_configs` (function), lines 26638-26722, exports `mcp_normalize_server_configs`
- order 1068: `mcp_extract_server_configs` (function), lines 26723-26742, exports `mcp_extract_server_configs`
- order 1069: `_mcp_sha256_file` (function), lines 26743-26753, exports `_mcp_sha256_file`
- order 1070: `_mcp_file_identity` (function), lines 26754-26771, exports `_mcp_file_identity`
- order 1071: `mcp_workspace_identity` (function), lines 26772-26790, exports `mcp_workspace_identity`
- order 1072: `mcp_config_file_digest` (function), lines 26791-26798, exports `mcp_config_file_digest`
- order 1073: `mcp_default_trust_store_path` (function), lines 26799-26833, exports `mcp_default_trust_store_path`
- order 1074: `mcp_record_definition_fingerprint` (function), lines 26834-26848, exports `mcp_record_definition_fingerprint`
- order 1075: `_mcp_effective_spawn` (function), lines 26849-26936, exports `_mcp_effective_spawn`
- order 1076: `MCPWorkspaceTrustStore` (class), lines 26937-26998, exports `MCPWorkspaceTrustStore`
- order 1077: `MCPServerProcess` (class), lines 26999-27354, exports `MCPServerProcess`
- order 1078: `MCPManager` (class), lines 27355-27973, exports `MCPManager`

### `mcp/service.py`

- order 1270: `McpServiceHandler` (class), lines 143463-143680, exports `McpServiceHandler`

### `rag/assets.py`

- order 1222: `RAG_ADMIN_INDEX_HTML` (constant), lines 119524-119756, exports `RAG_ADMIN_INDEX_HTML`
- order 1223: `RAG_ADMIN_CSS` (constant), lines 119757-119860, exports `RAG_ADMIN_CSS`
- order 1224: `RAG_ADMIN_JS` (constant), lines 119861-122098, exports `RAG_ADMIN_JS`
- order 1225: `CODE_ADMIN_INDEX_HTML` (constant), lines 122099-122111, exports `CODE_ADMIN_INDEX_HTML`
- order 1226: `CODE_ADMIN_CSS` (constant), lines 122112-122142, exports `CODE_ADMIN_CSS`
- order 1227: `CODE_ADMIN_JS` (constant), lines 122143-122147, exports `CODE_ADMIN_JS`

### `rag/constants.py`

- order 175: `RAG_LIBRARY_DIRNAME` (constant), lines 5488-5488, exports `RAG_LIBRARY_DIRNAME`
- order 176: `RAG_ADMIN_PORT_OFFSET` (constant), lines 5489-5489, exports `RAG_ADMIN_PORT_OFFSET`
- order 177: `CODE_LIBRARY_DIRNAME` (constant), lines 5490-5490, exports `CODE_LIBRARY_DIRNAME`
- order 183: `WEB_SEARCH_INDEX_DIRNAME` (constant), lines 5499-5499, exports `WEB_SEARCH_INDEX_DIRNAME`
- order 185: `USER_MEMORY_DIRNAME` (constant), lines 5501-5501, exports `USER_MEMORY_DIRNAME`
- order 186: `USER_MEMORY_DB_FILENAME` (constant), lines 5502-5502, exports `USER_MEMORY_DB_FILENAME`
- order 187: `USER_MEMORY_PROFILE_FILENAME` (constant), lines 5503-5503, exports `USER_MEMORY_PROFILE_FILENAME`
- order 188: `USER_MEMORY_MODE_CHOICES` (constant), lines 5504-5504, exports `USER_MEMORY_MODE_CHOICES`
- order 190: `USER_MEMORY_WEAK_CAPSULE_CHARS` (constant), lines 5506-5506, exports `USER_MEMORY_WEAK_CAPSULE_CHARS`
- order 191: `USER_MEMORY_ON_CAPSULE_CHARS` (constant), lines 5507-5507, exports `USER_MEMORY_ON_CAPSULE_CHARS`
- order 192: `USER_MEMORY_CAPSULE_INJECT_CHARS` (constant), lines 5508-5511, exports `USER_MEMORY_CAPSULE_INJECT_CHARS`
- order 193: `USER_MEMORY_MAX_SUMMARY_CHARS` (constant), lines 5512-5512, exports `USER_MEMORY_MAX_SUMMARY_CHARS`
- order 194: `USER_MEMORY_QUERY_LIMIT` (constant), lines 5513-5513, exports `USER_MEMORY_QUERY_LIMIT`
- order 195: `USER_MEMORY_DECAY_HALFLIFE_DAYS` (constant), lines 5514-5514, exports `USER_MEMORY_DECAY_HALFLIFE_DAYS`
- order 196: `USER_MEMORY_PROFILE_SCHEMA_VERSION` (constant), lines 5515-5515, exports `USER_MEMORY_PROFILE_SCHEMA_VERSION`
- order 216: `WEB_SEARCH_CONTEXT_REGISTRY_MAX` (constant), lines 5537-5537, exports `WEB_SEARCH_CONTEXT_REGISTRY_MAX`
- order 217: `WEB_SEARCH_CONTEXT_PROMPT_MAX_ITEMS` (constant), lines 5538-5538, exports `WEB_SEARCH_CONTEXT_PROMPT_MAX_ITEMS`
- order 218: `WEB_SEARCH_CONTEXT_PROMPT_MAX_CHARS` (constant), lines 5539-5539, exports `WEB_SEARCH_CONTEXT_PROMPT_MAX_CHARS`
- order 219: `WEB_SEARCH_CONTEXT_NODE_MAX` (constant), lines 5540-5540, exports `WEB_SEARCH_CONTEXT_NODE_MAX`
- order 220: `WEB_SEARCH_CONTEXT_URL_MAX` (constant), lines 5541-5541, exports `WEB_SEARCH_CONTEXT_URL_MAX`
- order 221: `RAG_CHUNK_CHARS` (constant), lines 5542-5542, exports `RAG_CHUNK_CHARS`
- order 222: `RAG_CHUNK_OVERLAP` (constant), lines 5543-5543, exports `RAG_CHUNK_OVERLAP`
- order 223: `RAG_MAX_CHUNKS_PER_DOC` (constant), lines 5544-5546, exports `RAG_MAX_CHUNKS_PER_DOC`
- order 224: `RAG_MAX_DOCUMENT_CHARS` (constant), lines 5547-5557, exports `RAG_MAX_DOCUMENT_CHARS`
- order 229: `RAG_MAX_QUERY_RESULTS` (constant), lines 5571-5571, exports `RAG_MAX_QUERY_RESULTS`
- order 230: `RAG_HIGH_RECALL_POOL_MULTIPLIER` (constant), lines 5572-5572, exports `RAG_HIGH_RECALL_POOL_MULTIPLIER`
- order 231: `RAG_HIGH_RECALL_MIN_POOL` (constant), lines 5573-5573, exports `RAG_HIGH_RECALL_MIN_POOL`
- order 232: `RAG_RETRIEVAL_MAX_PER_DOC` (constant), lines 5574-5574, exports `RAG_RETRIEVAL_MAX_PER_DOC`
- order 233: `RAG_BM25_K1` (constant), lines 5575-5578, exports `RAG_BM25_K1`
- order 234: `RAG_BM25_B` (constant), lines 5579-5579, exports `RAG_BM25_B`
- order 235: `RAG_BM25_SATURATION` (constant), lines 5580-5586, exports `RAG_BM25_SATURATION`
- order 236: `RAG_SYMBOL_EXACT_BOOST` (constant), lines 5587-5590, exports `RAG_SYMBOL_EXACT_BOOST`
- order 237: `RAG_INDEX_SNAPSHOT_FORMAT` (constant), lines 5591-5594, exports `RAG_INDEX_SNAPSHOT_FORMAT`
- order 238: `RAG_GRAPH_MAX_NODES` (constant), lines 5595-5595, exports `RAG_GRAPH_MAX_NODES`
- order 239: `RAG_TASK_HISTORY_LIMIT` (constant), lines 5596-5596, exports `RAG_TASK_HISTORY_LIMIT`
- order 240: `RAG_MODEL_MEDIA_MAX_BYTES` (constant), lines 5597-5597, exports `RAG_MODEL_MEDIA_MAX_BYTES`
- order 241: `RAG_MAX_IMPORT_FILES` (constant), lines 5598-5598, exports `RAG_MAX_IMPORT_FILES`
- order 242: `RAG_MAX_IMPORT_BATCH_ITEMS` (constant), lines 5599-5599, exports `RAG_MAX_IMPORT_BATCH_ITEMS`
- order 243: `RAG_MAX_IMPORT_BATCH_BYTES` (constant), lines 5600-5600, exports `RAG_MAX_IMPORT_BATCH_BYTES`
- order 244: `RAG_PDF_IMAGE_LIMIT` (constant), lines 5601-5601, exports `RAG_PDF_IMAGE_LIMIT`
- order 245: `RAG_QUERY_CONTEXT_CHARS` (constant), lines 5602-5602, exports `RAG_QUERY_CONTEXT_CHARS`
- order 246: `RAG_MAX_GLOBAL_COMMUNITIES` (constant), lines 5603-5603, exports `RAG_MAX_GLOBAL_COMMUNITIES`
- order 247: `RAG_MAX_COMMUNITY_MAP_SUPPORT` (constant), lines 5604-5604, exports `RAG_MAX_COMMUNITY_MAP_SUPPORT`
- order 248: `RAG_INCLUDE_FILENAME_ENTITIES_DEFAULT` (constant), lines 5605-5605, exports `RAG_INCLUDE_FILENAME_ENTITIES_DEFAULT`
- order 249: `RAG_DYNAMIC_NOISE_MIN_DOC_FREQ` (constant), lines 5606-5606, exports `RAG_DYNAMIC_NOISE_MIN_DOC_FREQ`
- order 250: `RAG_DYNAMIC_NOISE_MIN_COMMUNITY_FREQ` (constant), lines 5607-5607, exports `RAG_DYNAMIC_NOISE_MIN_COMMUNITY_FREQ`
- order 251: `RAG_DYNAMIC_NOISE_SOFT_DOC_RATIO` (constant), lines 5608-5608, exports `RAG_DYNAMIC_NOISE_SOFT_DOC_RATIO`
- order 252: `RAG_DYNAMIC_NOISE_HARD_DOC_RATIO` (constant), lines 5609-5609, exports `RAG_DYNAMIC_NOISE_HARD_DOC_RATIO`
- order 253: `RAG_DYNAMIC_NOISE_SOFT_COMMUNITY_RATIO` (constant), lines 5610-5610, exports `RAG_DYNAMIC_NOISE_SOFT_COMMUNITY_RATIO`
- order 254: `RAG_DYNAMIC_NOISE_HARD_COMMUNITY_RATIO` (constant), lines 5611-5611, exports `RAG_DYNAMIC_NOISE_HARD_COMMUNITY_RATIO`
- order 255: `RAG_MIN_SYNTHESIS_SCORE` (constant), lines 5612-5612, exports `RAG_MIN_SYNTHESIS_SCORE`
- order 256: `RAG_NO_EVIDENCE_THRESHOLD` (constant), lines 5613-5613, exports `RAG_NO_EVIDENCE_THRESHOLD`
- order 257: `RAG_WEAK_MATCH_SCORE_CAP` (constant), lines 5614-5614, exports `RAG_WEAK_MATCH_SCORE_CAP`
- order 258: `RAG_SYNTHESIS_MAX_PER_DOC` (constant), lines 5615-5615, exports `RAG_SYNTHESIS_MAX_PER_DOC`
- order 259: `RAG_WORKFLOW_ACCEPT_SCORE` (constant), lines 5616-5616, exports `RAG_WORKFLOW_ACCEPT_SCORE`
- order 260: `RAG_NO_EVIDENCE_MESSAGE` (constant), lines 5617-5617, exports `RAG_NO_EVIDENCE_MESSAGE`
- order 261: `RAG_CONTEXT_BUDGETS` (constant), lines 5618-5622, exports `RAG_CONTEXT_BUDGETS`
- order 262: `RAG_WEAK_EVIDENCE_MESSAGE` (constant), lines 5623-5623, exports `RAG_WEAK_EVIDENCE_MESSAGE`
- order 263: `RAG_EVIDENCE_SCHEMA_VERSION` (constant), lines 5624-5624, exports `RAG_EVIDENCE_SCHEMA_VERSION`
- order 264: `RAG_EVIDENCE_BATCH_CHARS` (constant), lines 5625-5628, exports `RAG_EVIDENCE_BATCH_CHARS`
- order 265: `RAG_EVALUATION_SUMMARY_CHARS` (constant), lines 5629-5632, exports `RAG_EVALUATION_SUMMARY_CHARS`
- order 266: `RAG_DENSE_DEFAULT_ENABLED` (constant), lines 5633-5633, exports `RAG_DENSE_DEFAULT_ENABLED`
- order 267: `RAG_EMBEDDING_MODE_VALUES` (constant), lines 5634-5634, exports `RAG_EMBEDDING_MODE_VALUES`
- order 268: `RAG_IMPORT_WORKER_COUNT` (constant), lines 5635-5638, exports `RAG_IMPORT_WORKER_COUNT`
- order 270: `RAG_PARSE_TIMEOUT_SECONDS` (constant), lines 5643-5646, exports `RAG_PARSE_TIMEOUT_SECONDS`
- order 1154: `RAG_TERM_GROUPS` (constant), lines 106514-111147, exports `RAG_TERM_GROUPS`
- order 1155: `RAG_RESEARCH_HINTS` (constant), lines 111148-111169, exports `RAG_RESEARCH_HINTS`
- order 1156: `RAG_CODE_HINTS` (constant), lines 111170-111180, exports `RAG_CODE_HINTS`
- order 1157: `RAG_SHORT_TOKEN_ALLOWLIST` (constant), lines 111181-111196, exports `RAG_SHORT_TOKEN_ALLOWLIST`
- order 1158: `RAG_EN_STOPWORDS` (constant), lines 111197-111269, exports `RAG_EN_STOPWORDS`
- order 1159: `RAG_ZH_STOPWORDS` (constant), lines 111270-111306, exports `RAG_ZH_STOPWORDS`
- order 1160: `RAG_GENERIC_ENTITY_TERMS_EN` (constant), lines 111307-111385, exports `RAG_GENERIC_ENTITY_TERMS_EN`
- order 1161: `RAG_GENERIC_ENTITY_TERMS_ZH` (constant), lines 111386-111428, exports `RAG_GENERIC_ENTITY_TERMS_ZH`
- order 1162: `RAG_STRUCTURAL_ENTITY_PATTERNS` (constant), lines 111429-111447, exports `RAG_STRUCTURAL_ENTITY_PATTERNS`
- order 1194: `CODE_LIBRARY_IGNORED_DIRS` (constant), lines 112405-112414, exports `CODE_LIBRARY_IGNORED_DIRS`
- order 1195: `CODE_LIBRARY_LANGUAGE_BY_EXT` (constant), lines 112415-112471, exports `CODE_LIBRARY_LANGUAGE_BY_EXT`
- order 1196: `CODE_LIBRARY_SPECIAL_FILENAMES` (constant), lines 112472-112478, exports `CODE_LIBRARY_SPECIAL_FILENAMES`

### `rag/index.py`

- order 1199: `_code_module_name` (function), lines 112503-112519, exports `_code_module_name`
- order 1200: `_code_choose_community` (function), lines 112520-112529, exports `_code_choose_community`
- order 1201: `_code_query_terms` (function), lines 112530-112544, exports `_code_query_terms`
- order 1210: `TFGraphIDFIndex` (class), lines 113675-115369, exports `TFGraphIDFIndex`
- order 1219: `CodeGraphIndex` (class), lines 118656-119144, exports `CodeGraphIndex`

### `rag/ingestion.py`

- order 1178: `_rag_trigram_set` (function), lines 111825-111832, exports `_rag_trigram_set`
- order 1179: `_rag_jaccard_sim` (function), lines 111833-111842, exports `_rag_jaccard_sim`
- order 1180: `_rag_mmr_select` (function), lines 111843-111892, exports `_rag_mmr_select`
- order 1185: `_rag_embed_text` (function), lines 112027-112050, exports `_rag_embed_text`
- order 1186: `_rag_embed_batch` (function), lines 112051-112059, exports `_rag_embed_batch`
- order 1187: `_rag_window_for_query` (function), lines 112060-112074, exports `_rag_window_for_query`
- order 1188: `_rag_focused_excerpt` (function), lines 112075-112117, exports `_rag_focused_excerpt`
- order 1189: `_rag_query_variants` (function), lines 112118-112157, exports `_rag_query_variants`
- order 1190: `_rag_parse_segments` (function), lines 112158-112220, exports `_rag_parse_segments`
- order 1191: `_rag_boundary_split` (function), lines 112221-112278, exports `_rag_boundary_split`
- order 1217: `_rag_parse_file_worker` (function), lines 117755-117771, exports `_rag_parse_file_worker`
- order 1218: `RAGIngestionService` (class), lines 117772-118655, exports `RAGIngestionService`
- order 1221: `CodeIngestionService` (class), lines 119436-119523, exports `CodeIngestionService`

### `rag/parsers.py`

- order 1163: `EvidenceRecord` (class), lines 111448-111482, exports `EvidenceRecord`
- order 1164: `_rag_float` (function), lines 111483-111489, exports `_rag_float`
- order 1165: `_rag_evidence_source_type` (function), lines 111490-111506, exports `_rag_evidence_source_type`
- order 1166: `_rag_normalize_evidence_record` (function), lines 111507-111562, exports `_rag_normalize_evidence_record`
- order 1167: `_rag_validate_evidence_record` (function), lines 111563-111605, exports `_rag_validate_evidence_record`
- order 1168: `_rag_evidence_batches` (function), lines 111606-111623, exports `_rag_evidence_batches`
- order 1169: `_rag_safe_name` (function), lines 111624-111629, exports `_rag_safe_name`
- order 1170: `_rag_detect_language` (function), lines 111630-111646, exports `_rag_detect_language`
- order 1171: `_rag_cjk_ngrams` (function), lines 111647-111661, exports `_rag_cjk_ngrams`
- order 1172: `_rag_is_noise_token` (function), lines 111662-111683, exports `_rag_is_noise_token`
- order 1173: `_rag_entity_allowed` (function), lines 111684-111698, exports `_rag_entity_allowed`
- order 1174: `_rag_filter_entities` (function), lines 111699-111715, exports `_rag_filter_entities`
- order 1175: `_rag_filename_entity_aliases` (function), lines 111716-111751, exports `_rag_filename_entity_aliases`
- order 1176: `_rag_apply_filename_entity_policy` (function), lines 111752-111784, exports `_rag_apply_filename_entity_policy`
- order 1177: `_rag_choose_community` (function), lines 111785-111824, exports `_rag_choose_community`
- order 1181: `_rag_tokenize` (function), lines 111893-111946, exports `_rag_tokenize`
- order 1182: `_rag_expand_tokens` (function), lines 111947-111970, exports `_rag_expand_tokens`
- order 1183: `_rag_extract_entities` (function), lines 111971-111989, exports `_rag_extract_entities`
- order 1184: `_rag_classify_document` (function), lines 111990-112026, exports `_rag_classify_document`
- order 1192: `_rag_structure_outline` (function), lines 112279-112317, exports `_rag_structure_outline`
- order 1193: `_rag_chunk_text` (function), lines 112318-112404, exports `_rag_chunk_text`
- order 1197: `_code_language_from_name` (function), lines 112479-112497, exports `_code_language_from_name`
- order 1198: `_code_is_test_path` (function), lines 112498-112502, exports `_code_is_test_path`
- order 1202: `_CallCollector` (class), lines 112545-112559, exports `_CallCollector`
- order 1203: `_ALGO_COMPLEXITY_RE` (assignment), lines 112560-112562, exports `_ALGO_COMPLEXITY_RE`
- order 1204: `_ALGO_STEP_RE` (assignment), lines 112563-112563, exports `_ALGO_STEP_RE`
- order 1205: `_ALGO_MATH_VARS` (assignment), lines 112564-112564, exports `_ALGO_MATH_VARS`
- order 1206: `_ALGO_DOC_KEYWORDS` (assignment), lines 112565-112565, exports `_ALGO_DOC_KEYWORDS`
- order 1207: `_detect_algo_chunk` (function), lines 112566-112591, exports `_detect_algo_chunk`
- order 1208: `CodeContentParser` (class), lines 112592-113158, exports `CodeContentParser`
- order 1209: `RAGContentParser` (class), lines 113159-113674, exports `RAGContentParser`

### `rag/store.py`

- order 1211: `RAGLibraryStore` (class), lines 115370-116008, exports `RAGLibraryStore`
- order 1212: `WikiStore` (class), lines 116009-116564, exports `WikiStore`
- order 1213: `UserMemoryStore` (class), lines 116565-117242, exports `UserMemoryStore`
- order 1214: `UserInteractionOptimizer` (class), lines 117243-117311, exports `UserInteractionOptimizer`
- order 1215: `UserIntentProfiler` (class), lines 117312-117353, exports `UserIntentProfiler`
- order 1216: `WorkflowMemoryStore` (class), lines 117354-117754, exports `WorkflowMemoryStore`
- order 1220: `CodeLibraryStore` (class), lines 119145-119435, exports `CodeLibraryStore`

### `rag/web_search.py`

- order 838: `_agent_web_bool` (function), lines 10765-10772, exports `_agent_web_bool`
- order 839: `_agent_web_int` (function), lines 10773-10780, exports `_agent_web_int`
- order 840: `_agent_web_host_is_local_name` (function), lines 10781-10787, exports `_agent_web_host_is_local_name`
- order 841: `_agent_web_ip_is_blocked` (function), lines 10788-10802, exports `_agent_web_ip_is_blocked`
- order 842: `_agent_web_canonical_url` (function), lines 10803-10832, exports `_agent_web_canonical_url`
- order 843: `_agent_web_domain_to_seed` (function), lines 10833-10844, exports `_agent_web_domain_to_seed`
- order 844: `_agent_web_query_terms` (function), lines 10845-10862, exports `_agent_web_query_terms`
- order 845: `_agent_web_query_domain_hints` (function), lines 10863-10903, exports `_agent_web_query_domain_hints`
- order 846: `_agent_web_query_needs_fresh_network` (function), lines 10904-10926, exports `_agent_web_query_needs_fresh_network`
- order 847: `_agent_web_extract_text_snippet` (function), lines 10927-10944, exports `_agent_web_extract_text_snippet`
- order 848: `AgentWebHTMLParser` (class), lines 10945-11024, exports `AgentWebHTMLParser`
- order 849: `_agent_web_decompress_bytes` (function), lines 11025-11048, exports `_agent_web_decompress_bytes`
- order 850: `_agent_web_charset_candidates` (function), lines 11049-11107, exports `_agent_web_charset_candidates`
- order 851: `_agent_web_decode_text_bytes` (function), lines 11108-11142, exports `_agent_web_decode_text_bytes`
- order 852: `AgentWebSearchEngine` (class), lines 11143-12923, exports `AgentWebSearchEngine`

### `server/http.py`

- order 712: `admin_language_payload` (function), lines 7738-7749, exports `admin_language_payload`
- order 827: `_UI_TRUNCATION_MARKER` (assignment), lines 10384-10386, exports `_UI_TRUNCATION_MARKER`
- order 828: `_ui_trim_text` (function), lines 10387-10395, exports `_ui_trim_text`
- order 829: `_bounded_ui_value` (function), lines 10396-10456, exports `_bounded_ui_value`
- order 830: `_bounded_ui_row` (function), lines 10457-10508, exports `_bounded_ui_row`
- order 831: `_bounded_ui_rows` (function), lines 10509-10557, exports `_bounded_ui_rows`
- order 832: `_enforce_ui_payload_budget` (function), lines 10558-10602, exports `_enforce_ui_payload_budget`
- order 833: `_apply_lite_snapshot_bounds` (function), lines 10603-10658, exports `_apply_lite_snapshot_bounds`
- order 1259: `AgentHTTPServer` (class), lines 136842-136881, exports `AgentHTTPServer`
- order 1262: `Handler` (class), lines 138083-140012, exports `Handler`
- order 1265: `SkillsReviewHandler` (class), lines 140821-140934, exports `SkillsReviewHandler`
- order 1269: `CollaborationHandler` (class), lines 142992-143462, exports `CollaborationHandler`

### `server/rag_admin.py`

- order 1264: `_RagAdminAuthMixin` (class), lines 140663-140820, exports `_RagAdminAuthMixin`
- order 1266: `RagAdminHandler` (class), lines 140935-141135, exports `RagAdminHandler`
- order 1267: `CodeAdminHandler` (class), lines 141136-141334, exports `CodeAdminHandler`

### `server/skills.py`

- order 1263: `SkillsHandler` (class), lines 140013-140662, exports `SkillsHandler`

### `session/manager.py`

- order 749: `SessionCreationLimitExceeded` (class), lines 8942-8947, exports `SessionCreationLimitExceeded`
- order 1142: `SessionManager` (class), lines 96925-99468, exports `SessionManager`

### `session/state.py`

- order 1141: `SessionState` (class), lines 33043-96924, exports `SessionState`

### `skills/embedded.py`

- order 1014: `EMBEDDED_SKILLS_ARCHIVE_B64` (constant), lines 19361-19362, exports `EMBEDDED_SKILLS_ARCHIVE_B64`
- order 1015: `EMBEDDED_SKILLS_ARCHIVE_SHA256` (constant), lines 19363-19363, exports `EMBEDDED_SKILLS_ARCHIVE_SHA256`
- order 1016: `EMBEDDED_SKILLS_ARCHIVE_FILES` (constant), lines 19364-19386, exports `EMBEDDED_SKILLS_ARCHIVE_FILES`
- order 1041: `BUILTIN_CLAWHUB_SKILLS_VERSION` (constant), lines 22622-22624, exports `BUILTIN_CLAWHUB_SKILLS_VERSION`
- order 1042: `EMBEDDED_CLAWHUB_SKILLS_ARCHIVE_B64` (constant), lines 22625-22870, exports `EMBEDDED_CLAWHUB_SKILLS_ARCHIVE_B64`
- order 1044: `MCP_BUILDER_SKILL_MD` (constant), lines 22918-23092, exports `MCP_BUILDER_SKILL_MD`
- order 1047: `SKILL_PROTOCOL_LOCAL` (constant), lines 23124-23125, exports `SKILL_PROTOCOL_LOCAL`
- order 1048: `SKILL_PROTOCOL_CLAWHUB` (constant), lines 23126-23126, exports `SKILL_PROTOCOL_CLAWHUB`
- order 1049: `SKILL_PROTOCOL_HTTP_JSON` (constant), lines 23127-23127, exports `SKILL_PROTOCOL_HTTP_JSON`
- order 1050: `SKILL_PROTOCOL_SPECS` (constant), lines 23128-23160, exports `SKILL_PROTOCOL_SPECS`

### `skills/provisioning.py`

- order 1017: `ensure_embedded_skills_at_root` (function), lines 19387-19452, exports `ensure_embedded_skills_at_root`
- order 1018: `ensure_embedded_skills` (function), lines 19453-19456, exports `ensure_embedded_skills`
- order 1020: `detect_upload_parser_capabilities` (function), lines 19463-19479, exports `detect_upload_parser_capabilities`
- order 1021: `_render_cap_markdown` (function), lines 19480-19495, exports `_render_cap_markdown`
- order 1022: `_write_text_if_changed` (function), lines 19496-19502, exports `_write_text_if_changed`
- order 1023: `ensure_generated_document_skills` (function), lines 19503-19592, exports `ensure_generated_document_skills`
- order 1024: `ensure_generated_image_coding_feedback_skill` (function), lines 19593-19693, exports `ensure_generated_image_coding_feedback_skill`
- order 1025: `_skill_knowledge_files` (function), lines 19694-19714, exports `_skill_knowledge_files`
- order 1026: `analyze_skill_building_knowledge` (function), lines 19715-19770, exports `analyze_skill_building_knowledge`
- order 1027: `_sanitize_skill_slug` (function), lines 19771-19774, exports `_sanitize_skill_slug`
- order 1028: `_build_skills_gen_skill_content` (function), lines 19775-19807, exports `_build_skills_gen_skill_content`
- order 1029: `ensure_generated_skills_gen_skill` (function), lines 19808-19813, exports `ensure_generated_skills_gen_skill`
- order 1030: `ensure_generated_execution_recovery_skill` (function), lines 19814-19898, exports `ensure_generated_execution_recovery_skill`
- order 1031: `ensure_generated_systematic_debugging_skill` (function), lines 19899-20172, exports `ensure_generated_systematic_debugging_skill`
- order 1032: `ensure_generated_code_engineering_mastery_skill` (function), lines 20173-20292, exports `ensure_generated_code_engineering_mastery_skill`
- order 1033: `ensure_generated_smart_file_navigation_skill` (function), lines 20293-20409, exports `ensure_generated_smart_file_navigation_skill`
- order 1034: `ensure_generated_html_frontend_report_skills` (function), lines 20410-20618, exports `ensure_generated_html_frontend_report_skills`
- order 1035: `ensure_generated_deep_research_skills` (function), lines 20619-20888, exports `ensure_generated_deep_research_skills`
- order 1036: `ensure_generated_research_scientific_skills` (function), lines 20889-21526, exports `ensure_generated_research_scientific_skills`
- order 1037: `ensure_generated_rag_mastery_skills` (function), lines 21527-21828, exports `ensure_generated_rag_mastery_skills`
- order 1038: `ensure_generated_multimodal_comprehension_skills` (function), lines 21829-22523, exports `ensure_generated_multimodal_comprehension_skills`
- order 1039: `ensure_generated_runtime_skills_manifest` (function), lines 22524-22558, exports `ensure_generated_runtime_skills_manifest`
- order 1040: `ensure_generated_agent_web_search_skill` (function), lines 22559-22621, exports `ensure_generated_agent_web_search_skill`
- order 1043: `ensure_embedded_clawhub_skills` (function), lines 22871-22917, exports `ensure_embedded_clawhub_skills`
- order 1045: `ensure_generated_mcp_builder_skill` (function), lines 23093-23104, exports `ensure_generated_mcp_builder_skill`
- order 1046: `ensure_runtime_skills` (function), lines 23105-23123, exports `ensure_runtime_skills`

### `skills/store.py`

- order 555: `_skill_term_match` (function), lines 6534-6554, exports `_skill_term_match`
- order 1051: `_BUILTIN_SKILLS` (assignment), lines 23161-23269, exports `_BUILTIN_SKILLS`
- order 1052: `SkillStore` (class), lines 23270-25185, exports `SkillStore`

### `skills/studio.py`

- order 1244: `SkillsStudioError` (class), lines 123331-123340, exports `SkillsStudioError`
- order 1245: `_studio_slug` (function), lines 123341-123356, exports `_studio_slug`
- order 1246: `_studio_hash` (function), lines 123357-123360, exports `_studio_hash`
- order 1247: `_studio_cookie_value` (function), lines 123361-123370, exports `_studio_cookie_value`
- order 1248: `SkillsStudioStore` (class), lines 123371-125228, exports `SkillsStudioStore`

### `utils/compress.py`

- order 856: `compress_text_blob` (function), lines 13088-13094, exports `compress_text_blob`
- order 857: `decompress_text_blob` (function), lines 13095-13104, exports `decompress_text_blob`

### `utils/crypto.py`

- order 957: `CryptoBox` (class), lines 16092-16245, exports `CryptoBox`

### `utils/errors.py`

- order 884: `EmptyActionError` (class), lines 13721-13724, exports `EmptyActionError`
- order 1054: `ProcessManagerError` (class), lines 25321-25326, exports `ProcessManagerError`

### `utils/files.py`

- order 706: `_normalize_js_lib_asset_ref` (function), lines 7608-7623, exports `_normalize_js_lib_asset_ref`
- order 707: `_resolve_js_lib_asset_path` (function), lines 7624-7655, exports `_resolve_js_lib_asset_path`
- order 708: `_discover_extra_js_lib_files` (function), lines 7656-7688, exports `_discover_extra_js_lib_files`
- order 802: `safe_path` (function), lines 9797-9807, exports `safe_path`
- order 803: `_safe_js_filename` (function), lines 9808-9816, exports `_safe_js_filename`
- order 804: `_sha256_bytes` (function), lines 9817-9819, exports `_sha256_bytes`
- order 805: `_sha256_file` (function), lines 9820-9829, exports `_sha256_file`
- order 806: `_download_http_bytes` (function), lines 9830-9839, exports `_download_http_bytes`
- order 807: `offline_js_lib_root` (function), lines 9840-9842, exports `offline_js_lib_root`
- order 808: `_offline_js_entry_relative_path` (function), lines 9843-9848, exports `_offline_js_entry_relative_path`
- order 809: `_archive_member_relative_path` (function), lines 9849-9859, exports `_archive_member_relative_path`
- order 810: `_path_size_bytes` (function), lines 9860-9876, exports `_path_size_bytes`
- order 811: `_extract_archive_to_dir` (function), lines 9877-9918, exports `_extract_archive_to_dir`
- order 812: `_package_required_paths` (function), lines 9919-9926, exports `_package_required_paths`
- order 813: `_package_required_globs` (function), lines 9927-9943, exports `_package_required_globs`
- order 814: `_package_install_ready` (function), lines 9944-9966, exports `_package_install_ready`
- order 815: `_postprocess_offline_js_package` (function), lines 9967-10003, exports `_postprocess_offline_js_package`
- order 816: `_ensure_offline_js_package` (function), lines 10004-10048, exports `_ensure_offline_js_package`
- order 817: `_render_offline_js_catalog_md` (function), lines 10049-10066, exports `_render_offline_js_catalog_md`
- order 818: `load_offline_js_lib_index` (function), lines 10067-10077, exports `load_offline_js_lib_index`
- order 819: `ensure_offline_js_libs` (function), lines 10078-10236, exports `ensure_offline_js_libs`
- order 820: `_offline_js_catalog_entry_for_asset` (function), lines 10237-10257, exports `_offline_js_catalog_entry_for_asset`
- order 821: `ensure_offline_js_asset` (function), lines 10258-10315, exports `ensure_offline_js_asset`
- order 822: `_normalize_external_js_url` (function), lines 10316-10321, exports `_normalize_external_js_url`
- order 823: `is_external_js_src` (function), lines 10322-10325, exports `is_external_js_src`
- order 824: `match_offline_js_catalog_by_url` (function), lines 10326-10343, exports `match_offline_js_catalog_by_url`
- order 825: `cache_external_js_url` (function), lines 10344-10379, exports `cache_external_js_url`
- order 960: `try_read_text` (function), lines 16489-16498, exports `try_read_text`
- order 982: `_start_offline_js_warmup` (function), lines 18092-18109, exports `_start_offline_js_warmup`

### `utils/http.py`

- order 122: `_URL_OPEN_ORIGINAL` (assignment), lines 5117-5117, exports `_URL_OPEN_ORIGINAL`
- order 123: `_HTTP_SSL_CONTEXT` (assignment), lines 5118-5118, exports `_HTTP_SSL_CONTEXT`
- order 150: `_shared_http_ssl_context` (function), lines 5182-5205, exports `_shared_http_ssl_context`
- order 151: `urlopen` (function), lines 5206-5215, exports `urlopen`
- order 795: `json_response_bytes` (function), lines 9742-9744, exports `json_response_bytes`
- order 796: `read_http_json_body` (function), lines 9745-9758, exports `read_http_json_body`
- order 797: `close_if_http_request_body_unread` (function), lines 9759-9772, exports `close_if_http_request_body_unread`

### `utils/json_utils.py`

- order 174: `JSON_FSYNC_ENABLED` (constant), lines 5487-5487, exports `JSON_FSYNC_ENABLED`
- order 794: `json_dumps` (function), lines 9738-9741, exports `json_dumps`
- order 872: `parse_tool_arguments` (function), lines 13468-13478, exports `parse_tool_arguments`
- order 873: `repair_truncated_json_object` (function), lines 13479-13533, exports `repair_truncated_json_object`
- order 874: `parse_tool_arguments_with_error` (function), lines 13534-13565, exports `parse_tool_arguments_with_error`
- order 875: `_is_valid_json_object` (function), lines 13566-13571, exports `_is_valid_json_object`
- order 876: `_scan_top_level_json_objects` (function), lines 13572-13595, exports `_scan_top_level_json_objects`
- order 877: `reconstruct_streamed_tool_args` (function), lines 13596-13640, exports `reconstruct_streamed_tool_args`
- order 898: `parse_json_object` (function), lines 13995-14001, exports `parse_json_object`
- order 899: `decode_model_json_object` (function), lines 14002-14036, exports `decode_model_json_object`
- order 901: `standard_model_json_object` (function), lines 14041-14104, exports `standard_model_json_object`
- order 902: `semantic_json_repair_request` (function), lines 14105-14121, exports `semantic_json_repair_request`
- order 903: `validate_semantic_json_repair` (function), lines 14122-14151, exports `validate_semantic_json_repair`
- order 905: `extract_json_object_from_text` (function), lines 14204-14228, exports `extract_json_object_from_text`
- order 961: `_json_default_copy` (function), lines 16499-16505, exports `_json_default_copy`
- order 962: `_read_json_file` (function), lines 16506-16527, exports `_read_json_file`
- order 963: `_write_json_file` (function), lines 16528-16556, exports `_write_json_file`

### `utils/media.py`

- order 699: `_capability_probe_png_bytes` (function), lines 7246-7260, exports `_capability_probe_png_bytes`
- order 700: `_capability_probe_audio_bytes` (function), lines 7261-7272, exports `_capability_probe_audio_bytes`
- order 701: `_capability_probe_video_bytes` (function), lines 7273-7277, exports `_capability_probe_video_bytes`
- order 764: `guess_mime_from_name` (function), lines 9290-9294, exports `guess_mime_from_name`
- order 765: `_convert_image_to_safe_format` (function), lines 9295-9314, exports `_convert_image_to_safe_format`
- order 766: `guess_ext_from_mime` (function), lines 9315-9323, exports `guess_ext_from_mime`

### `utils/misc.py`

- order 767: `now_ts` (function), lines 9324-9326, exports `now_ts`
- order 768: `_benign_socket_log_lock` (assignment), lines 9327-9329, exports `_benign_socket_log_lock`
- order 769: `_benign_socket_log_state` (assignment), lines 9330-9330, exports `_benign_socket_log_state`
- order 771: `is_benign_socket_error` (function), lines 9346-9366, exports `is_benign_socket_error`
- order 772: `_socket_error_code` (function), lines 9367-9378, exports `_socket_error_code`
- order 773: `_log_benign_socket_error_limited` (function), lines 9379-9415, exports `_log_benign_socket_error_limited`
- order 774: `swallow_benign_socket_error` (function), lines 9416-9422, exports `swallow_benign_socket_error`
- order 775: `normalize_timeout_seconds` (function), lines 9423-9438, exports `normalize_timeout_seconds`
- order 776: `detect_local_lan_ip` (function), lines 9439-9450, exports `detect_local_lan_ip`
- order 777: `_LOCAL_LAN_IP_CACHE` (assignment), lines 9451-9452, exports `_LOCAL_LAN_IP_CACHE`
- order 778: `detect_local_lan_ip_cached` (function), lines 9453-9466, exports `detect_local_lan_ip_cached`
- order 798: `make_id` (function), lines 9773-9775, exports `make_id`
- order 799: `sanitize_profile_id` (function), lines 9776-9779, exports `sanitize_profile_id`
- order 955: `user_id_from_ip` (function), lines 16051-16058, exports `user_id_from_ip`
- order 959: `_meta_string_list` (function), lines 16475-16488, exports `_meta_string_list`
- order 1019: `_module_exists` (function), lines 19457-19462, exports `_module_exists`

### `utils/sqlite.py`

- order 70: `_ClosingSQLiteConnection` (class), lines 73-82, exports `_ClosingSQLiteConnection`
- order 71: `_connect_sqlite` (function), lines 83-116, exports `_connect_sqlite`
- order 1271: `sqlite_failure_diagnostics` (function), lines 143681-143765, exports `sqlite_failure_diagnostics`

### `utils/text.py`

- order 162: `MAX_TOOL_OUTPUT` (constant), lines 5475-5475, exports `MAX_TOOL_OUTPUT`
- order 511: `SOCKET_NOISE_LINE_PATTERNS` (constant), lines 6287-6292, exports `SOCKET_NOISE_LINE_PATTERNS`
- order 770: `filter_runtime_noise_lines` (function), lines 9331-9345, exports `filter_runtime_noise_lines`
- order 783: `safe_utf8_bytes` (function), lines 9591-9595, exports `safe_utf8_bytes`
- order 784: `escape_invalid_utf8_text` (function), lines 9596-9598, exports `escape_invalid_utf8_text`
- order 785: `sanitize_utf8_surrogates` (function), lines 9599-9612, exports `sanitize_utf8_surrogates`
- order 786: `decode_utf8_replace` (function), lines 9613-9617, exports `decode_utf8_replace`
- order 826: `trim` (function), lines 10380-10383, exports `trim`
- order 834: `is_synthetic_public_progress` (function), lines 10659-10678, exports `is_synthetic_public_progress`
- order 836: `display_clean` (function), lines 10731-10745, exports `display_clean`
- order 837: `short_title_from` (function), lines 10746-10764, exports `short_title_from`
- order 853: `_fmt_export_ts` (function), lines 12924-12934, exports `_fmt_export_ts`
- order 854: `_html_esc` (function), lines 12935-12938, exports `_html_esc`
- order 855: `_text_to_minimal_pdf` (function), lines 12939-13087, exports `_text_to_minimal_pdf`
- order 858: `normalize_embedded_newlines` (function), lines 13105-13114, exports `normalize_embedded_newlines`
- order 859: `_map_todo_status_token` (function), lines 13115-13153, exports `_map_todo_status_token`
- order 860: `_TODO_SHORT_ID_RE` (assignment), lines 13154-13161, exports `_TODO_SHORT_ID_RE`
- order 861: `_TODO_SHORT_ID_TAG_RE` (assignment), lines 13162-13162, exports `_TODO_SHORT_ID_TAG_RE`
- order 862: `normalize_todo_short_id` (function), lines 13163-13168, exports `normalize_todo_short_id`
- order 863: `strip_todo_short_id_tag` (function), lines 13169-13177, exports `strip_todo_short_id_tag`
- order 864: `split_todo_status_text` (function), lines 13178-13182, exports `split_todo_status_text`
- order 865: `split_todo_status_text_with_id` (function), lines 13183-13256, exports `split_todo_status_text_with_id`
- order 866: `extract_todo_rows_from_text` (function), lines 13257-13339, exports `extract_todo_rows_from_text`
- order 867: `decode_structured_todo_container` (function), lines 13340-13358, exports `decode_structured_todo_container`
- order 868: `infer_todo_status_from_text` (function), lines 13359-13367, exports `infer_todo_status_from_text`
- order 869: `split_structured_todo_content` (function), lines 13368-13423, exports `split_structured_todo_content`
- order 870: `is_todo_transport_metadata` (function), lines 13424-13437, exports `is_todo_transport_metadata`
- order 871: `normalize_work_text` (function), lines 13438-13467, exports `normalize_work_text`
- order 985: `make_unified_diff` (function), lines 18153-18171, exports `make_unified_diff`
- order 986: `_skip_row` (function), lines 18172-18177, exports `_skip_row`
- order 987: `_row_is_hot` (function), lines 18178-18181, exports `_row_is_hot`
- order 988: `_hotspot_index` (function), lines 18182-18205, exports `_hotspot_index`
- order 989: `_compress_rows_keep_hotspot` (function), lines 18206-18255, exports `_compress_rows_keep_hotspot`
- order 990: `_focused_diff_rows_from_opcodes` (function), lines 18256-18390, exports `_focused_diff_rows_from_opcodes`
- order 991: `make_numbered_diff` (function), lines 18391-18423, exports `make_numbered_diff`
- order 992: `render_numbered_diff_text` (function), lines 18424-18437, exports `render_numbered_diff_text`

### `web/admin_assets.py`

- order 1151: `ADMIN_INDEX_HTML` (constant), lines 105521-105838, exports `ADMIN_INDEX_HTML`
- order 1152: `ADMIN_CSS` (constant), lines 105839-106001, exports `ADMIN_CSS`
- order 1153: `ADMIN_JS` (constant), lines 106002-106513, exports `ADMIN_JS`

### `web/assets.py`

- order 1143: `INDEX_HTML` (constant), lines 99469-99730, exports `INDEX_HTML`
- order 1144: `APP_CSS` (constant), lines 99731-100273, exports `APP_CSS`
- order 1145: `APP_JS` (constant), lines 100274-105057, exports `APP_JS`
- order 1146: `APP_CSS` (constant), lines 105058-105078, exports `APP_CSS`
- order 1147: `APP_TS` (constant), lines 105079-105118, exports `APP_TS`

### `web/skills_assets.py`

- order 1148: `SKILLS_INDEX_HTML` (constant), lines 105119-105274, exports `SKILLS_INDEX_HTML`
- order 1149: `SKILLS_EXTRA_CSS` (constant), lines 105275-105374, exports `SKILLS_EXTRA_CSS`
- order 1150: `SKILLS_APP_JS` (constant), lines 105375-105520, exports `SKILLS_APP_JS`
