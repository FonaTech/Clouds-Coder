# Code_Structure Framework

## Overview

- Source snapshot: `Clouds_Coder.py` (1077 top-level statements)
- Generated source modules: 62
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
| `_imports.py` | 68 | 83 | — | 1–3461 |
| `admin/auth.py` | 3 | 3 | `admin/constants.py`, `utils/misc.py` | 12644–13391 |
| `admin/config.py` | 8 | 8 | `config/constants.py`, `config/paths.py`, `config/settings.py`, `llm/constants.py`, `utils/http.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` | 14137–14597 |
| `admin/constants.py` | 16 | 16 | — | 3468–108483 |
| `agent/background.py` | 1 | 1 | `agent/process.py`, `config/constants.py`, `ide/sandbox.py`, `utils/misc.py`, `utils/text.py` | 21889–22514 |
| `agent/bus.py` | 1 | 1 | `config/constants.py`, `utils/crypto.py`, `utils/misc.py` | 22515–22580 |
| `agent/errors.py` | 1 | 1 | — | 11234–11237 |
| `agent/events.py` | 1 | 1 | — | 15289–15335 |
| `agent/process.py` | 7 | 7 | `ide/sandbox.py`, `utils/errors.py`, `utils/misc.py`, `utils/text.py` | 7551–21888 |
| `agent/tasks.py` | 1 | 1 | `utils/crypto.py`, `utils/json_utils.py`, `utils/misc.py` | 21388–21522 |
| `agent/todo.py` | 1 | 1 | `config/constants.py`, `config/settings.py`, `utils/misc.py`, `utils/text.py` | 15336–15696 |
| `agent/tools.py` | 15 | 19 | `config/constants.py`, `utils/text.py` | 15168–27219 |
| `agent/worktree.py` | 1 | 1 | `agent/process.py`, `agent/tasks.py`, `config/constants.py`, `utils/crypto.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` | 22581–22793 |
| `app/context.py` | 1 | 1 | `admin/auth.py`, `admin/config.py`, `admin/constants.py`, `agent/process.py`, `agent/tools.py`, `app/services.py`, `collaboration/core.py`, `config/constants.py`, `config/paths.py`, `config/settings.py`, `ide/assets.py`, `ide/auth.py`, `ide/errors.py`, `ide/events.py`, `ide/preview.py`, `ide/sandbox.py`, `llm/client.py`, `llm/constants.py`, `llm/utils.py`, `mcp/driver.py`, `rag/assets.py`, `rag/constants.py`, `rag/ingestion.py`, `rag/parsers.py`, `rag/store.py`, `session/manager.py`, `session/state.py`, `skills/provisioning.py`, `skills/store.py`, `skills/studio.py`, `utils/crypto.py`, `utils/files.py`, `utils/http.py`, `utils/json_utils.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py`, `web/assets.py`, `web/skills_assets.py` | 108484–118253 |
| `app/main.py` | 2 | 1 | `admin/config.py`, `admin/constants.py`, `agent/tools.py`, `app/context.py`, `collaboration/watcher.py`, `config/constants.py`, `config/paths.py`, `config/settings.py`, `ide/handler.py`, `llm/constants.py`, `llm/utils.py`, `mcp/constants.py`, `mcp/service.py`, `rag/constants.py`, `server/http.py`, `server/rag_admin.py`, `server/skills.py`, `skills/provisioning.py`, `utils/files.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` | 124670–126559 |
| `app/services.py` | 2 | 2 | `admin/constants.py`, `config/settings.py`, `skills/embedded.py`, `skills/store.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` | 118294–119479 |
| `collaboration/core.py` | 23 | 23 | `config/constants.py` | 83–3322 |
| `collaboration/watcher.py` | 2 | 2 | `utils/misc.py`, `utils/text.py` | 124579–124669 |
| `config/constants.py` | 422 | 418 | `rag/constants.py` | 68–108479 |
| `config/paths.py` | 13 | 13 | `agent/process.py`, `utils/crypto.py`, `utils/text.py` | 3467–7711 |
| `config/settings.py` | 66 | 66 | `agent/tools.py`, `config/constants.py`, `config/paths.py`, `llm/constants.py`, `llm/utils.py`, `rag/constants.py`, `skills/provisioning.py`, `utils/http.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` | 5662–13024 |
| `ide/assets.py` | 8 | 3 | — | 105510–106550 |
| `ide/auth.py` | 2 | 2 | `admin/auth.py`, `admin/constants.py`, `config/constants.py`, `utils/misc.py`, `utils/text.py` | 13392–14121 |
| `ide/errors.py` | 2 | 2 | — | 14122–14136 |
| `ide/events.py` | 1 | 1 | `config/constants.py`, `utils/text.py` | 8319–8365 |
| `ide/handler.py` | 1 | 1 | `admin/auth.py`, `app/context.py`, `collaboration/core.py`, `config/constants.py`, `config/settings.py`, `ide/auth.py`, `ide/errors.py`, `ide/events.py`, `session/manager.py`, `session/state.py`, `utils/http.py`, `utils/json_utils.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py` | 122415–123889 |
| `ide/preview.py` | 12 | 12 | `config/constants.py`, `utils/text.py` | 14883–15288 |
| `ide/sandbox.py` | 21 | 21 | `agent/process.py`, `utils/misc.py` | 7533–27748 |
| `llm/client.py` | 2 | 2 | `agent/tools.py`, `config/constants.py`, `config/settings.py`, `llm/utils.py`, `utils/http.py`, `utils/json_utils.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py` | 24176–26514 |
| `llm/constants.py` | 17 | 17 | — | 3465–11676 |
| `llm/utils.py` | 22 | 22 | `agent/process.py`, `config/settings.py`, `llm/constants.py`, `utils/http.py`, `utils/json_utils.py`, `utils/text.py` | 11208–11890 |
| `mcp/constants.py` | 8 | 8 | — | 3832–22829 |
| `mcp/driver.py` | 13 | 13 | `mcp/constants.py`, `utils/files.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` | 22830–24175 |
| `mcp/service.py` | 1 | 1 | `app/context.py`, `config/constants.py`, `utils/files.py`, `utils/http.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` | 124361–124578 |
| `rag/assets.py` | 6 | 6 | — | 102903–105509 |
| `rag/constants.py` | 74 | 74 | — | 3828–96049 |
| `rag/index.py` | 5 | 5 | `rag/constants.py`, `rag/ingestion.py`, `rag/parsers.py`, `utils/misc.py`, `utils/text.py` | 96074–102548 |
| `rag/ingestion.py` | 13 | 13 | `config/constants.py`, `config/settings.py`, `rag/constants.py`, `rag/parsers.py`, `rag/store.py`, `session/state.py`, `utils/files.py`, `utils/json_utils.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py` | 95442–102902 |
| `rag/parsers.py` | 24 | 24 | `agent/process.py`, `config/constants.py`, `rag/constants.py`, `rag/ingestion.py`, `utils/files.py`, `utils/json_utils.py`, `utils/media.py`, `utils/text.py` | 95232–97178 |
| `rag/store.py` | 7 | 7 | `config/constants.py`, `config/settings.py`, `ide/preview.py`, `rag/constants.py`, `rag/index.py`, `rag/ingestion.py`, `rag/parsers.py`, `skills/provisioning.py`, `utils/files.py`, `utils/json_utils.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py` | 98856–102814 |
| `rag/web_search.py` | 15 | 15 | `config/constants.py`, `config/paths.py`, `rag/constants.py`, `utils/http.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` | 8400–10560 |
| `server/http.py` | 4 | 4 | `admin/auth.py`, `admin/config.py`, `admin/constants.py`, `agent/process.py`, `app/context.py`, `collaboration/core.py`, `collaboration/watcher.py`, `config/constants.py`, `config/paths.py`, `config/settings.py`, `ide/handler.py`, `ide/preview.py`, `llm/utils.py`, `server/rag_admin.py`, `session/manager.py`, `session/state.py`, `skills/studio.py`, `utils/errors.py`, `utils/files.py`, `utils/http.py`, `utils/json_utils.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py`, `web/admin_assets.py` | 118254–124360 |
| `server/rag_admin.py` | 3 | 3 | `admin/auth.py`, `app/context.py`, `config/constants.py`, `rag/constants.py`, `utils/http.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py` | 121755–122414 |
| `server/skills.py` | 1 | 1 | `admin/auth.py`, `app/context.py`, `config/constants.py`, `config/paths.py`, `config/settings.py`, `session/manager.py`, `skills/provisioning.py`, `skills/studio.py`, `utils/http.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py` | 121112–121754 |
| `session/manager.py` | 2 | 2 | `agent/process.py`, `config/constants.py`, `config/paths.py`, `config/settings.py`, `llm/client.py`, `llm/utils.py`, `rag/store.py`, `session/state.py`, `utils/crypto.py`, `utils/files.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` | 6859–83948 |
| `session/state.py` | 1 | 1 | `admin/constants.py`, `agent/background.py`, `agent/bus.py`, `agent/errors.py`, `agent/events.py`, `agent/process.py`, `agent/tasks.py`, `agent/todo.py`, `agent/tools.py`, `agent/worktree.py`, `collaboration/core.py`, `config/constants.py`, `config/paths.py`, `config/settings.py`, `ide/preview.py`, `ide/sandbox.py`, `llm/client.py`, `llm/constants.py`, `llm/utils.py`, `mcp/constants.py`, `mcp/driver.py`, `rag/constants.py`, `rag/parsers.py`, `rag/web_search.py`, `skills/provisioning.py`, `skills/store.py`, `utils/compress.py`, `utils/crypto.py`, `utils/errors.py`, `utils/files.py`, `utils/http.py`, `utils/json_utils.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py` | 27749–82568 |
| `skills/embedded.py` | 10 | 10 | — | 15697–19496 |
| `skills/provisioning.py` | 26 | 26 | `config/paths.py`, `skills/embedded.py`, `utils/files.py`, `utils/json_utils.py`, `utils/misc.py` | 15723–19459 |
| `skills/store.py` | 2 | 2 | `config/constants.py`, `config/settings.py`, `llm/utils.py`, `skills/embedded.py`, `utils/files.py`, `utils/http.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` | 19497–21387 |
| `skills/studio.py` | 5 | 5 | `agent/process.py`, `collaboration/core.py`, `config/constants.py`, `config/settings.py`, `ide/sandbox.py`, `llm/client.py`, `llm/constants.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` | 106576–108474 |
| `utils/compress.py` | 2 | 2 | — | 10725–10741 |
| `utils/crypto.py` | 1 | 1 | `utils/json_utils.py` | 12677–12795 |
| `utils/errors.py` | 2 | 2 | — | 11230–21528 |
| `utils/files.py` | 27 | 27 | `config/constants.py`, `config/paths.py`, `utils/http.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` | 5581–13048 |
| `utils/http.py` | 7 | 7 | `utils/json_utils.py`, `utils/text.py` | 3462–7687 |
| `utils/json_utils.py` | 13 | 13 | `utils/text.py` | 3827–13106 |
| `utils/media.py` | 6 | 6 | — | 5219–7240 |
| `utils/misc.py` | 16 | 16 | `config/constants.py` | 7241–15798 |
| `utils/text.py` | 30 | 30 | `config/constants.py` | 3815–14882 |
| `web/admin_assets.py` | 3 | 3 | — | 89830–90297 |
| `web/assets.py` | 4 | 4 | — | 83949–89430 |
| `web/skills_assets.py` | 3 | 3 | — | 89431–89829 |

## Source Mapping

### `_imports.py`

- order 0: `_import_2` (import), lines 1-2, exports `annotations`
- order 1: `_import_4` (import), lines 3-4, exports `argparse`
- order 2: `_import_5` (import), lines 5-5, exports `ast`
- order 3: `_import_6` (import), lines 6-6, exports `base64`
- order 4: `_import_7` (import), lines 7-7, exports `concurrent`
- order 5: `_import_8` (import), lines 8-8, exports `csv`
- order 6: `_import_9` (import), lines 9-9, exports `ctypes`
- order 7: `_import_10` (import), lines 10-10, exports `difflib`
- order 8: `_import_11` (import), lines 11-11, exports `errno`
- order 9: `_import_12` (import), lines 12-12, exports `fnmatch`
- order 10: `_import_13` (import), lines 13-13, exports `hashlib`
- order 11: `_import_14` (import), lines 14-14, exports `hmac`
- order 12: `_import_15` (import), lines 15-15, exports `html`
- order 13: `_import_16` (import), lines 16-16, exports `importlib`
- order 14: `_import_17` (import), lines 17-17, exports `io`
- order 15: `_import_18` (import), lines 18-18, exports `ipaddress`
- order 16: `_import_19` (import), lines 19-19, exports `json`
- order 17: `_import_20` (import), lines 20-20, exports `locale`
- order 18: `_import_21` (import), lines 21-21, exports `math`
- order 19: `_import_22` (import), lines 22-22, exports `mimetypes`
- order 20: `_import_23` (import), lines 23-23, exports `multiprocessing`
- order 21: `_import_24` (import), lines 24-24, exports `os`
- order 22: `_import_25` (import), lines 25-25, exports `platform`
- order 23: `_import_26` (import), lines 26-26, exports `queue`
- order 24: `_import_27` (import), lines 27-27, exports `re`
- order 25: `_import_28` (import), lines 28-28, exports `secrets`
- order 26: `_import_29` (import), lines 29-29, exports `select`
- order 27: `_import_30` (import), lines 30-30, exports `selectors`
- order 28: `_import_31` (import), lines 31-31, exports `shlex`
- order 29: `_import_32` (import), lines 32-32, exports `shutil`
- order 30: `_import_33` (import), lines 33-33, exports `signal`
- order 31: `_import_34` (import), lines 34-34, exports `socket`
- order 32: `_import_35` (import), lines 35-35, exports `sqlite3`
- order 33: `_import_36` (import), lines 36-36, exports `ssl`
- order 34: `_import_37` (import), lines 37-37, exports `stat`
- order 35: `_import_38` (import), lines 38-38, exports `struct`
- order 36: `_import_39` (import), lines 39-39, exports `subprocess`
- order 37: `_import_40` (import), lines 40-40, exports `sys`
- order 38: `_import_41` (import), lines 41-41, exports `tarfile`
- order 39: `_import_42` (import), lines 42-42, exports `tempfile`
- order 40: `_import_43` (import), lines 43-43, exports `threading`
- order 41: `_import_44` (import), lines 44-44, exports `time`
- order 42: `_import_45` (import), lines 45-45, exports `traceback`
- order 43: `_import_46` (import), lines 46-46, exports `unicodedata`
- order 44: `_import_47` (import), lines 47-47, exports `robotparser`
- order 45: `_import_48` (import), lines 48-48, exports `uuid`
- order 46: `_import_49` (import), lines 49-49, exports `ET`
- order 47: `_import_50` (import), lines 50-50, exports `zipfile`
- order 48: `_import_51` (import), lines 51-51, exports `zlib`
- order 49: `_import_52` (import), lines 52-52, exports `Counter`, `defaultdict`, `deque`
- order 50: `_import_53` (import), lines 53-53, exports `Iterable`
- order 51: `_import_54` (import), lines 54-54, exports `dataclass`
- order 52: `_import_55` (import), lines 55-55, exports `datetime`, `timedelta`, `timezone`
- order 53: `_import_56` (import), lines 56-56, exports `parsedate_to_datetime`
- order 54: `_import_57` (import), lines 57-57, exports `HTMLParser`
- order 55: `_import_58` (import), lines 58-58, exports `HTTPStatus`
- order 56: `_import_59` (import), lines 59-59, exports `IncompleteRead`
- order 57: `_import_60` (import), lines 60-60, exports `SimpleCookie`
- order 58: `_import_61` (import), lines 61-61, exports `BaseHTTPRequestHandler`, `ThreadingHTTPServer`
- order 59: `_import_62` (import), lines 62-62, exports `Path`, `PurePosixPath`
- order 60: `_import_63` (import), lines 63-63, exports `Any`
- order 61: `_import_64` (import), lines 64-64, exports `HTTPError`, `URLError`
- order 62: `_import_65` (import), lines 65-65, exports `parse_qs`, `quote`, `unquote`, `urljoin`, `urlparse`, `urlunparse`
- order 63: `_import_66` (import), lines 66-66, exports `Request`, `urlopen`
- order 64: `_import_67` (import), lines 67-67, exports `ZoneInfo`
- order 104: `_try_import_3445` (import), lines 3443-3452, exports `_fcntl`, `_pty`, `_termios`
- order 105: `_try_import_3454` (import), lines 3453-3457, exports `_certifi`
- order 106: `_try_import_3458` (import), lines 3458-3461, exports `_yaml`

### `admin/auth.py`

- order 804: `trusted_client_ip` (function), lines 12644-12676, exports `trusted_client_ip`
- order 812: `AdminAuthError` (class), lines 13107-13114, exports `AdminAuthError`
- order 813: `AdminAuthStore` (class), lines 13115-13391, exports `AdminAuthStore`

### `admin/config.py`

- order 818: `_admin_config_schema` (function), lines 14137-14254, exports `_admin_config_schema`
- order 819: `_admin_factory_config` (function), lines 14255-14258, exports `_admin_factory_config`
- order 820: `_admin_coerce_config` (function), lines 14259-14414, exports `_admin_coerce_config`
- order 821: `_admin_config_to_argv` (function), lines 14415-14451, exports `_admin_config_to_argv`
- order 822: `_admin_restart_probe_url` (function), lines 14452-14467, exports `_admin_restart_probe_url`
- order 823: `_admin_supervised_restart` (function), lines 14468-14554, exports `_admin_supervised_restart`
- order 824: `_admin_argparse_defaults` (function), lines 14555-14576, exports `_admin_argparse_defaults`
- order 825: `_admin_config_from_namespace` (function), lines 14577-14597, exports `_admin_config_from_namespace`

### `admin/constants.py`

- order 113: `ADMIN_STATE_DIRNAME` (constant), lines 3468-3468, exports `ADMIN_STATE_DIRNAME`
- order 114: `ADMIN_CONFIG_FILENAME` (constant), lines 3469-3469, exports `ADMIN_CONFIG_FILENAME`
- order 115: `ADMIN_APPS_FILENAME` (constant), lines 3470-3470, exports `ADMIN_APPS_FILENAME`
- order 116: `ADMIN_TELEMETRY_FILENAME` (constant), lines 3471-3471, exports `ADMIN_TELEMETRY_FILENAME`
- order 117: `ADMIN_AUTH_FILENAME` (constant), lines 3472-3472, exports `ADMIN_AUTH_FILENAME`
- order 127: `ADMIN_MAX_APP_SKILLS` (constant), lines 3519-3519, exports `ADMIN_MAX_APP_SKILLS`
- order 128: `ADMIN_MAX_APP_CAPSULE_CHARS` (constant), lines 3520-3520, exports `ADMIN_MAX_APP_CAPSULE_CHARS`
- order 129: `ADMIN_MAX_APP_RESOURCE_FILES` (constant), lines 3521-3521, exports `ADMIN_MAX_APP_RESOURCE_FILES`
- order 130: `ADMIN_MAX_APP_RESOURCE_BYTES` (constant), lines 3522-3522, exports `ADMIN_MAX_APP_RESOURCE_BYTES`
- order 131: `ADMIN_APP_INLINE_BLOB_BYTES` (constant), lines 3523-3523, exports `ADMIN_APP_INLINE_BLOB_BYTES`
- order 132: `ADMIN_AUTH_SESSION_TTL_SECONDS` (constant), lines 3524-3524, exports `ADMIN_AUTH_SESSION_TTL_SECONDS`
- order 133: `ADMIN_AUTH_PASSWORD_ITERATIONS` (constant), lines 3525-3525, exports `ADMIN_AUTH_PASSWORD_ITERATIONS`
- order 134: `ADMIN_AUTH_MAX_ACTIVE_SESSIONS` (constant), lines 3526-3526, exports `ADMIN_AUTH_MAX_ACTIVE_SESSIONS`
- order 1057: `ADMIN_SKILLS_REVIEW_HTML` (constant), lines 108480-108481, exports `ADMIN_SKILLS_REVIEW_HTML`
- order 1058: `ADMIN_SKILLS_REVIEW_CSS` (constant), lines 108482-108482, exports `ADMIN_SKILLS_REVIEW_CSS`
- order 1059: `ADMIN_SKILLS_REVIEW_JS` (constant), lines 108483-108483, exports `ADMIN_SKILLS_REVIEW_JS`

### `agent/background.py`

- order 896: `BackgroundManager` (class), lines 21889-22514, exports `BackgroundManager`

### `agent/bus.py`

- order 897: `MessageBus` (class), lines 22515-22580, exports `MessageBus`

### `agent/errors.py`

- order 753: `CircuitBreakerTriggered` (class), lines 11234-11237, exports `CircuitBreakerTriggered`

### `agent/events.py`

- order 852: `EventHub` (class), lines 15289-15335, exports `EventHub`

### `agent/process.py`

- order 671: `subprocess_text_encodings` (function), lines 7551-7572, exports `subprocess_text_encodings`
- order 672: `decode_subprocess_bytes` (function), lines 7573-7599, exports `decode_subprocess_bytes`
- order 673: `run_subprocess_text` (function), lines 7600-7622, exports `run_subprocess_text`
- order 674: `windows_utf8_shell_command` (function), lines 7623-7629, exports `windows_utf8_shell_command`
- order 675: `shell_process_invocation` (function), lines 7630-7640, exports `shell_process_invocation`
- order 676: `join_shell_task_command` (function), lines 7641-7652, exports `join_shell_task_command`
- order 895: `UserProcessManager` (class), lines 21529-21888, exports `UserProcessManager`

### `agent/tasks.py`

- order 893: `TaskManager` (class), lines 21388-21522, exports `TaskManager`

### `agent/todo.py`

- order 853: `TodoManager` (class), lines 15336-15696, exports `TodoManager`

### `agent/tools.py`

- order 847: `_ask_user_option_rows` (function), lines 15168-15201, exports `_ask_user_option_rows`
- order 848: `_ask_user_option_value` (function), lines 15202-15207, exports `_ask_user_option_value`
- order 921: `tool_def` (function), lines 26515-26528, exports `tool_def`
- order 922: `TOOLS` (constant), lines 26529-27055, exports `TOOLS`
- order 923: `TOOL_REQUIRED_ARGS` (constant), lines 27056-27057, exports `TOOL_REQUIRED_ARGS`
- order 924: `TOOL_SPEC_BY_NAME` (constant), lines 27058-27058, exports `TOOL_SPEC_BY_NAME`
- order 925: `_for_27059` (statement), lines 27059-27068, exports `_tool`, `_fn`, `_name`, `_required`
- order 926: `TOOL_NAME_FUZZY_MAP` (constant), lines 27069-27070, exports `TOOL_NAME_FUZZY_MAP`
- order 927: `_for_27071` (statement), lines 27071-27074, exports `_name`, `_key`
- order 928: `_for_27076` (statement), lines 27075-27092, exports `_alias`, `_target`
- order 929: `is_todo_resume_tool_name` (function), lines 27093-27109, exports `is_todo_resume_tool_name`
- order 930: `canonicalize_tool_name` (function), lines 27110-27128, exports `canonicalize_tool_name`
- order 931: `filter_tool_specs_for_runtime` (function), lines 27129-27144, exports `filter_tool_specs_for_runtime`
- order 932: `DEVELOPER_TOOL_DROP` (constant), lines 27145-27155, exports `DEVELOPER_TOOL_DROP`
- order 933: `AGENT_TOOL_ALLOWLIST` (constant), lines 27156-27219, exports `AGENT_TOOL_ALLOWLIST`

### `agent/worktree.py`

- order 898: `WorktreeManager` (class), lines 22581-22793, exports `WorktreeManager`

### `app/context.py`

- order 1060: `AppContext` (class), lines 108484-118253, exports `AppContext`

### `app/main.py`

- order 1075: `main` (function), lines 124670-126556, exports `main`
- order 1076: `_main_guard_126558` (main_guard), lines 126557-126559, exports —

### `app/services.py`

- order 1062: `TelemetryStore` (class), lines 118294-118669, exports `TelemetryStore`
- order 1063: `ApplicationRegistry` (class), lines 118670-119479, exports `ApplicationRegistry`

### `collaboration/core.py`

- order 78: `_now` (function), lines 83-86, exports `_now`
- order 79: `_json` (function), lines 87-90, exports `_json`
- order 80: `_load_json` (function), lines 91-97, exports `_load_json`
- order 81: `_b64_token` (function), lines 98-101, exports `_b64_token`
- order 82: `_branch_label` (function), lines 102-110, exports `_branch_label`
- order 83: `_digest` (function), lines 111-114, exports `_digest`
- order 84: `_password_hash` (function), lines 115-118, exports `_password_hash`
- order 85: `_normalize_ip` (function), lines 119-128, exports `_normalize_ip`
- order 86: `_normalize_name` (function), lines 129-135, exports `_normalize_name`
- order 87: `_COLLAB_PUBLIC_SECRET_PATTERNS` (assignment), lines 136-147, exports `_COLLAB_PUBLIC_SECRET_PATTERNS`
- order 88: `_collaboration_public_text` (function), lines 148-178, exports `_collaboration_public_text`
- order 89: `_collaboration_task_objective` (function), lines 179-203, exports `_collaboration_task_objective`
- order 90: `_collaboration_task_title` (function), lines 204-211, exports `_collaboration_task_title`
- order 91: `_collaboration_task_key` (function), lines 212-218, exports `_collaboration_task_key`
- order 92: `_collaboration_plan_steps` (function), lines 219-237, exports `_collaboration_plan_steps`
- order 93: `CollaborationError` (class), lines 238-245, exports `CollaborationError`
- order 94: `CollaborationPrincipal` (class), lines 246-256, exports `CollaborationPrincipal`
- order 95: `_normalize_operation` (function), lines 257-290, exports `_normalize_operation`
- order 96: `operation_input_length` (function), lines 291-294, exports `operation_input_length`
- order 97: `apply_text_operation` (function), lines 295-317, exports `apply_text_operation`
- order 98: `transform_text_operation` (function), lines 318-394, exports `transform_text_operation`
- order 99: `CollaborationStore` (class), lines 395-3108, exports `CollaborationStore`
- order 100: `CollaborationWriteCoordinator` (class), lines 3109-3322, exports `CollaborationWriteCoordinator`

### `collaboration/watcher.py`

- order 1073: `collaboration_file_watcher_loop` (function), lines 124579-124651, exports `collaboration_file_watcher_loop`
- order 1074: `collaboration_watcher_health` (function), lines 124652-124669, exports `collaboration_watcher_health`

### `config/constants.py`

- order 65: `COLLAB_DB_FILENAME` (constant), lines 68-70, exports `COLLAB_DB_FILENAME`
- order 66: `COLLAB_SESSION_TTL_SECONDS` (constant), lines 71-71, exports `COLLAB_SESSION_TTL_SECONDS`
- order 67: `COLLAB_PRESENCE_TTL_SECONDS` (constant), lines 72-72, exports `COLLAB_PRESENCE_TTL_SECONDS`
- order 68: `COLLAB_PASSWORD_ITERATIONS` (constant), lines 73-73, exports `COLLAB_PASSWORD_ITERATIONS`
- order 69: `COLLAB_MAX_AVATAR_BYTES` (constant), lines 74-74, exports `COLLAB_MAX_AVATAR_BYTES`
- order 70: `COLLAB_MAX_TEXT_BYTES` (constant), lines 75-75, exports `COLLAB_MAX_TEXT_BYTES`
- order 71: `COLLAB_DELETE_RETENTION_DAYS` (constant), lines 76-76, exports `COLLAB_DELETE_RETENTION_DAYS`
- order 72: `COLLAB_EVENT_RETENTION` (constant), lines 77-77, exports `COLLAB_EVENT_RETENTION`
- order 73: `COLLAB_AGENT_STALE_SECONDS` (constant), lines 78-78, exports `COLLAB_AGENT_STALE_SECONDS`
- order 74: `COLLAB_AGENT_HEARTBEAT_INTERVAL_SECONDS` (constant), lines 79-79, exports `COLLAB_AGENT_HEARTBEAT_INTERVAL_SECONDS`
- order 75: `COLLAB_EXTERNAL_WRITE_SETTLE_SECONDS` (constant), lines 80-80, exports `COLLAB_EXTERNAL_WRITE_SETTLE_SECONDS`
- order 76: `COLLAB_EXTERNAL_WRITE_CONFIRMATIONS` (constant), lines 81-81, exports `COLLAB_EXTERNAL_WRITE_CONFIRMATIONS`
- order 77: `COLLAB_SCHEMA_VERSION` (constant), lines 82-82, exports `COLLAB_SCHEMA_VERSION`
- order 101: `COLLAB_INDEX_HTML` (constant), lines 3323-3394, exports `COLLAB_INDEX_HTML`
- order 102: `COLLAB_CSS` (constant), lines 3395-3401, exports `COLLAB_CSS`
- order 103: `COLLAB_JS` (constant), lines 3402-3442, exports `COLLAB_JS`
- order 109: `APP_VERSION` (constant), lines 3464-3464, exports `APP_VERSION`
- order 118: `IDE_AUTH_FILENAME` (constant), lines 3473-3473, exports `IDE_AUTH_FILENAME`
- order 119: `IDE_AUTH_SESSION_TTL_SECONDS` (constant), lines 3474-3474, exports `IDE_AUTH_SESSION_TTL_SECONDS`
- order 120: `IDE_AUTH_MAX_ACTIVE_SESSIONS` (constant), lines 3475-3475, exports `IDE_AUTH_MAX_ACTIVE_SESSIONS`
- order 121: `IDE_DEVICE_SECRET_MIN_BYTES` (constant), lines 3476-3476, exports `IDE_DEVICE_SECRET_MIN_BYTES`
- order 122: `IDE_DEVICE_LABEL_MAX_CHARS` (constant), lines 3477-3477, exports `IDE_DEVICE_LABEL_MAX_CHARS`
- order 123: `IDE_DEVICE_PAIRING_TTL_SECONDS` (constant), lines 3478-3478, exports `IDE_DEVICE_PAIRING_TTL_SECONDS`
- order 124: `IDE_WORKBENCH_STATE_FILENAME` (constant), lines 3479-3479, exports `IDE_WORKBENCH_STATE_FILENAME`
- order 125: `IDE_PROMPT_ENHANCEMENT_BUDGETS` (constant), lines 3480-3517, exports `IDE_PROMPT_ENHANCEMENT_BUDGETS`
- order 126: `IDE_EXTENSIONS_DIRNAME` (constant), lines 3518-3518, exports `IDE_EXTENSIONS_DIRNAME`
- order 148: `LONG_OUTPUT_MODEL_PAGE_CHARS` (constant), lines 3816-3816, exports `LONG_OUTPUT_MODEL_PAGE_CHARS`
- order 149: `LONG_OUTPUT_UI_PAGE_CHARS` (constant), lines 3817-3817, exports `LONG_OUTPUT_UI_PAGE_CHARS`
- order 150: `LONG_OUTPUT_UI_PREVIEW_MAX_PAGES` (constant), lines 3818-3818, exports `LONG_OUTPUT_UI_PREVIEW_MAX_PAGES`
- order 151: `LONG_OUTPUT_LISTING_OFFLOAD_CHARS` (constant), lines 3819-3819, exports `LONG_OUTPUT_LISTING_OFFLOAD_CHARS`
- order 152: `LONG_OUTPUT_READ_PAGE_LINES` (constant), lines 3820-3820, exports `LONG_OUTPUT_READ_PAGE_LINES`
- order 153: `LONG_OUTPUT_READ_PAGE_MAX_CHARS` (constant), lines 3821-3821, exports `LONG_OUTPUT_READ_PAGE_MAX_CHARS`
- order 154: `LONG_OUTPUT_TEMP_MAX_FILES` (constant), lines 3822-3822, exports `LONG_OUTPUT_TEMP_MAX_FILES`
- order 155: `READ_FILE_DEFAULT_MAX_CHARS` (constant), lines 3823-3823, exports `READ_FILE_DEFAULT_MAX_CHARS`
- order 156: `READ_FILE_HARD_MAX_CHARS` (constant), lines 3824-3824, exports `READ_FILE_HARD_MAX_CHARS`
- order 157: `READ_FILE_OVERVIEW_HEAD_LINES` (constant), lines 3825-3825, exports `READ_FILE_OVERVIEW_HEAD_LINES`
- order 158: `READ_FILE_SEARCH_MAX_MATCHES` (constant), lines 3826-3826, exports `READ_FILE_SEARCH_MAX_MATCHES`
- order 163: `CODE_ADMIN_PORT_OFFSET` (constant), lines 3831-3831, exports `CODE_ADMIN_PORT_OFFSET`
- order 165: `IDE_PORT_OFFSET` (constant), lines 3833-3836, exports `IDE_PORT_OFFSET`
- order 166: `IDE_DEFAULT_PORT` (constant), lines 3837-3837, exports `IDE_DEFAULT_PORT`
- order 167: `COLLAB_PORT_OFFSET` (constant), lines 3838-3838, exports `COLLAB_PORT_OFFSET`
- order 169: `DEFAULT_WEB_SEARCH_ENABLED` (constant), lines 3840-3840, exports `DEFAULT_WEB_SEARCH_ENABLED`
- order 174: `DEFAULT_USER_MEMORY_MODE` (constant), lines 3845-3845, exports `DEFAULT_USER_MEMORY_MODE`
- order 182: `AGENT_WEB_SEARCH_USER_AGENT` (constant), lines 3856-3856, exports `AGENT_WEB_SEARCH_USER_AGENT`
- order 183: `AGENT_WEB_SEARCH_DEFAULT_MAX_RESULTS` (constant), lines 3857-3857, exports `AGENT_WEB_SEARCH_DEFAULT_MAX_RESULTS`
- order 184: `AGENT_WEB_SEARCH_DEFAULT_MAX_PAGES` (constant), lines 3858-3858, exports `AGENT_WEB_SEARCH_DEFAULT_MAX_PAGES`
- order 185: `AGENT_WEB_SEARCH_HARD_MAX_PAGES` (constant), lines 3859-3859, exports `AGENT_WEB_SEARCH_HARD_MAX_PAGES`
- order 186: `AGENT_WEB_SEARCH_DEFAULT_DEPTH` (constant), lines 3860-3860, exports `AGENT_WEB_SEARCH_DEFAULT_DEPTH`
- order 187: `AGENT_WEB_SEARCH_HARD_DEPTH` (constant), lines 3861-3861, exports `AGENT_WEB_SEARCH_HARD_DEPTH`
- order 188: `AGENT_WEB_SEARCH_FETCH_TIMEOUT` (constant), lines 3862-3862, exports `AGENT_WEB_SEARCH_FETCH_TIMEOUT`
- order 189: `AGENT_WEB_SEARCH_TOOL_SOFT_TIMEOUT` (constant), lines 3863-3863, exports `AGENT_WEB_SEARCH_TOOL_SOFT_TIMEOUT`
- order 190: `AGENT_WEB_SEARCH_MAX_PAGE_BYTES` (constant), lines 3864-3864, exports `AGENT_WEB_SEARCH_MAX_PAGE_BYTES`
- order 191: `AGENT_WEB_SEARCH_MAX_TEXT_CHARS` (constant), lines 3865-3865, exports `AGENT_WEB_SEARCH_MAX_TEXT_CHARS`
- order 192: `AGENT_WEB_SEARCH_PUBLIC_DISCOVERY_ENABLED` (constant), lines 3866-3868, exports `AGENT_WEB_SEARCH_PUBLIC_DISCOVERY_ENABLED`
- order 193: `AGENT_WEB_SEARCH_PUBLIC_FEED_URL` (constant), lines 3869-3869, exports `AGENT_WEB_SEARCH_PUBLIC_FEED_URL`
- order 194: `AGENT_WEB_SEARCH_PUBLIC_FEED_MAX_BYTES` (constant), lines 3870-3870, exports `AGENT_WEB_SEARCH_PUBLIC_FEED_MAX_BYTES`
- order 195: `AGENT_WEB_SEARCH_LOCAL_GRAPH_MAX_NODES` (constant), lines 3871-3871, exports `AGENT_WEB_SEARCH_LOCAL_GRAPH_MAX_NODES`
- order 196: `AGENT_WEB_SEARCH_LOCAL_GRAPH_MAX_EDGES` (constant), lines 3872-3872, exports `AGENT_WEB_SEARCH_LOCAL_GRAPH_MAX_EDGES`
- order 197: `AGENT_WEB_SEARCH_LOCAL_GRAPH_EDGE_SCAN_MULTIPLIER` (constant), lines 3873-3873, exports `AGENT_WEB_SEARCH_LOCAL_GRAPH_EDGE_SCAN_MULTIPLIER`
- order 198: `AGENT_WEB_SEARCH_LOCAL_GRAPH_PAGERANK_ITERATIONS` (constant), lines 3874-3874, exports `AGENT_WEB_SEARCH_LOCAL_GRAPH_PAGERANK_ITERATIONS`
- order 199: `AGENT_WEB_SEARCH_LOCAL_GRAPH_PAGERANK_DAMPING` (constant), lines 3875-3875, exports `AGENT_WEB_SEARCH_LOCAL_GRAPH_PAGERANK_DAMPING`
- order 200: `AGENT_WEB_SEARCH_LOCAL_GRAPH_AUTHORITY_BONUS_MAX` (constant), lines 3876-3876, exports `AGENT_WEB_SEARCH_LOCAL_GRAPH_AUTHORITY_BONUS_MAX`
- order 210: `CODE_CHUNK_CHARS` (constant), lines 3898-3898, exports `CODE_CHUNK_CHARS`
- order 211: `CODE_CHUNK_OVERLAP` (constant), lines 3899-3899, exports `CODE_CHUNK_OVERLAP`
- order 212: `CODE_MAX_CHUNKS_PER_DOC` (constant), lines 3900-3900, exports `CODE_MAX_CHUNKS_PER_DOC`
- order 250: `CODE_IMPORT_WORKER_COUNT` (constant), lines 3960-3963, exports `CODE_IMPORT_WORKER_COUNT`
- order 252: `CODE_PARSE_TIMEOUT_SECONDS` (constant), lines 3968-3971, exports `CODE_PARSE_TIMEOUT_SECONDS`
- order 253: `DEFAULT_CONTEXT_TOKEN_LIMIT` (constant), lines 3972-3972, exports `DEFAULT_CONTEXT_TOKEN_LIMIT`
- order 254: `TOKEN_THRESHOLD` (constant), lines 3973-3973, exports `TOKEN_THRESHOLD`
- order 255: `CONTEXT_AUTO_COMPACT_RESERVE_RATIO` (constant), lines 3974-3977, exports `CONTEXT_AUTO_COMPACT_RESERVE_RATIO`
- order 256: `CONTEXT_ESTIMATE_SAFETY_MULTIPLIER` (constant), lines 3978-3981, exports `CONTEXT_ESTIMATE_SAFETY_MULTIPLIER`
- order 257: `CONTEXT_USAGE_CALIBRATION_MAX` (constant), lines 3982-3985, exports `CONTEXT_USAGE_CALIBRATION_MAX`
- order 258: `CONTEXT_ACTUAL_USAGE_RECENT_SECONDS` (constant), lines 3986-3989, exports `CONTEXT_ACTUAL_USAGE_RECENT_SECONDS`
- order 259: `LARGE_FILE_AUTO_PAGE_BYTES` (constant), lines 3990-3993, exports `LARGE_FILE_AUTO_PAGE_BYTES`
- order 260: `LARGE_FILE_AUTO_PAGE_LINES` (constant), lines 3994-3997, exports `LARGE_FILE_AUTO_PAGE_LINES`
- order 261: `LARGE_SOURCE_UPLOAD_EXCERPT_CHARS` (constant), lines 3998-4001, exports `LARGE_SOURCE_UPLOAD_EXCERPT_CHARS`
- order 262: `CHAT_UPLOAD_PARSE_QUEUE_MAX` (constant), lines 4002-4005, exports `CHAT_UPLOAD_PARSE_QUEUE_MAX`
- order 263: `CHAT_UPLOAD_PARSE_TIMEOUT_SECONDS` (constant), lines 4006-4009, exports `CHAT_UPLOAD_PARSE_TIMEOUT_SECONDS`
- order 264: `CHAT_UPLOAD_INLINE_TEXT_BYTES` (constant), lines 4010-4013, exports `CHAT_UPLOAD_INLINE_TEXT_BYTES`
- order 265: `CHAT_UPLOAD_PARSE_MAX_BYTES` (constant), lines 4014-4020, exports `CHAT_UPLOAD_PARSE_MAX_BYTES`
- order 266: `CHAT_UPLOAD_ZIP_ENTRY_MAX_BYTES` (constant), lines 4021-4027, exports `CHAT_UPLOAD_ZIP_ENTRY_MAX_BYTES`
- order 267: `CHAT_UPLOAD_TEXT_CONTEXT_CHARS` (constant), lines 4028-4031, exports `CHAT_UPLOAD_TEXT_CONTEXT_CHARS`
- order 268: `CHAT_UPLOAD_PROMPT_MAX_FILES` (constant), lines 4032-4035, exports `CHAT_UPLOAD_PROMPT_MAX_FILES`
- order 269: `CHAT_UPLOAD_PROMPT_MAX_CHARS` (constant), lines 4036-4039, exports `CHAT_UPLOAD_PROMPT_MAX_CHARS`
- order 270: `CHAT_UPLOAD_PROMPT_PER_FILE_CHARS` (constant), lines 4040-4043, exports `CHAT_UPLOAD_PROMPT_PER_FILE_CHARS`
- order 271: `CHAT_UPLOAD_FRONTEND_WAIT_MS` (constant), lines 4044-4047, exports `CHAT_UPLOAD_FRONTEND_WAIT_MS`
- order 272: `CHAT_UPLOAD_AUTO_LIBRARY_INGEST` (constant), lines 4048-4051, exports `CHAT_UPLOAD_AUTO_LIBRARY_INGEST`
- order 273: `CHAT_UPLOAD_INGEST_QUEUE_MAX` (constant), lines 4052-4055, exports `CHAT_UPLOAD_INGEST_QUEUE_MAX`
- order 274: `SESSION_SUBMIT_LOCK_TIMEOUT_SECONDS` (constant), lines 4056-4059, exports `SESSION_SUBMIT_LOCK_TIMEOUT_SECONDS`
- order 275: `SESSION_DEFERRED_START_QUEUE_MAX` (constant), lines 4060-4063, exports `SESSION_DEFERRED_START_QUEUE_MAX`
- order 276: `SESSION_WATCHDOG_INTERVAL_SECONDS` (constant), lines 4064-4067, exports `SESSION_WATCHDOG_INTERVAL_SECONDS`
- order 277: `SESSION_HEARTBEAT_STALE_SECONDS` (constant), lines 4068-4071, exports `SESSION_HEARTBEAT_STALE_SECONDS`
- order 278: `SESSION_LIST_DEFAULT_LIMIT` (constant), lines 4072-4075, exports `SESSION_LIST_DEFAULT_LIMIT`
- order 279: `IDLE_TIMEOUT` (constant), lines 4076-4076, exports `IDLE_TIMEOUT`
- order 280: `POLL_INTERVAL` (constant), lines 4077-4077, exports `POLL_INTERVAL`
- order 281: `SSE_HEARTBEAT_SECONDS` (constant), lines 4078-4078, exports `SSE_HEARTBEAT_SECONDS`
- order 282: `MODEL_CALL_PROGRESS_DELAY` (constant), lines 4079-4079, exports `MODEL_CALL_PROGRESS_DELAY`
- order 283: `MODEL_CALL_PROGRESS_INTERVAL` (constant), lines 4080-4080, exports `MODEL_CALL_PROGRESS_INTERVAL`
- order 284: `RUN_COMPLETION_SUMMARY_ENABLED` (constant), lines 4081-4084, exports `RUN_COMPLETION_SUMMARY_ENABLED`
- order 285: `LLM_HTTP_RETRY_MAX_ATTEMPTS` (constant), lines 4085-4088, exports `LLM_HTTP_RETRY_MAX_ATTEMPTS`
- order 286: `LLM_HTTP_RETRY_DELAY_SECONDS` (constant), lines 4089-4092, exports `LLM_HTTP_RETRY_DELAY_SECONDS`
- order 287: `LLM_HTTP_RETRY_MAX_SECONDS` (constant), lines 4093-4096, exports `LLM_HTTP_RETRY_MAX_SECONDS`
- order 288: `LLM_HTTP_RETRY_404_ON_VLLM` (constant), lines 4097-4100, exports `LLM_HTTP_RETRY_404_ON_VLLM`
- order 289: `LLM_HTTP_RETRY_STATUSES` (constant), lines 4101-4101, exports `LLM_HTTP_RETRY_STATUSES`
- order 290: `MAX_AGENT_ROUNDS` (constant), lines 4102-4102, exports `MAX_AGENT_ROUNDS`
- order 291: `MIN_AGENT_ROUNDS` (constant), lines 4103-4103, exports `MIN_AGENT_ROUNDS`
- order 292: `MAX_AGENT_ROUNDS_CAP` (constant), lines 4104-4104, exports `MAX_AGENT_ROUNDS_CAP`
- order 293: `REPEATED_TOOL_LOOP_THRESHOLD` (constant), lines 4105-4105, exports `REPEATED_TOOL_LOOP_THRESHOLD`
- order 294: `BASH_READ_LOOP_THRESHOLD` (constant), lines 4106-4106, exports `BASH_READ_LOOP_THRESHOLD`
- order 295: `READ_FILE_LOOP_THRESHOLD` (constant), lines 4107-4107, exports `READ_FILE_LOOP_THRESHOLD`
- order 296: `READ_FILE_LOOP_DISTINCT_SOFT_LIMIT` (constant), lines 4108-4108, exports `READ_FILE_LOOP_DISTINCT_SOFT_LIMIT`
- order 297: `READ_FILE_COMPACT_PIN_DISTINCT` (constant), lines 4109-4109, exports `READ_FILE_COMPACT_PIN_DISTINCT`
- order 298: `READ_FILE_COMPACT_PIN_MAX_CHARS` (constant), lines 4110-4110, exports `READ_FILE_COMPACT_PIN_MAX_CHARS`
- order 299: `READ_CONTEXT_REGISTRY_MAX` (constant), lines 4111-4111, exports `READ_CONTEXT_REGISTRY_MAX`
- order 300: `READ_CONTEXT_PROMPT_MAX_ITEMS` (constant), lines 4112-4112, exports `READ_CONTEXT_PROMPT_MAX_ITEMS`
- order 301: `READ_CONTEXT_PROMPT_MAX_CHARS` (constant), lines 4113-4113, exports `READ_CONTEXT_PROMPT_MAX_CHARS`
- order 302: `READ_CONTEXT_SUMMARY_MAX_CHARS` (constant), lines 4114-4114, exports `READ_CONTEXT_SUMMARY_MAX_CHARS`
- order 303: `READ_CONTEXT_SHARED_MAX_ITEMS` (constant), lines 4115-4115, exports `READ_CONTEXT_SHARED_MAX_ITEMS`
- order 304: `READ_CONTEXT_POLICY_CHOICES` (constant), lines 4116-4116, exports `READ_CONTEXT_POLICY_CHOICES`
- order 305: `DEFAULT_READ_CONTEXT_POLICY` (constant), lines 4117-4117, exports `DEFAULT_READ_CONTEXT_POLICY`
- order 306: `TOOL_MEMORY_REGISTRY_MAX` (constant), lines 4118-4118, exports `TOOL_MEMORY_REGISTRY_MAX`
- order 307: `TOOL_MEMORY_PROMPT_MAX_ITEMS` (constant), lines 4119-4119, exports `TOOL_MEMORY_PROMPT_MAX_ITEMS`
- order 308: `TOOL_MEMORY_PROMPT_MAX_CHARS` (constant), lines 4120-4120, exports `TOOL_MEMORY_PROMPT_MAX_CHARS`
- order 309: `TOOL_MEMORY_SUMMARY_MAX_CHARS` (constant), lines 4121-4121, exports `TOOL_MEMORY_SUMMARY_MAX_CHARS`
- order 310: `TOOL_MEMORY_SHARED_MAX_ITEMS` (constant), lines 4122-4122, exports `TOOL_MEMORY_SHARED_MAX_ITEMS`
- order 311: `TOOL_MEMORY_COMPACT_PIN_DISTINCT` (constant), lines 4123-4123, exports `TOOL_MEMORY_COMPACT_PIN_DISTINCT`
- order 312: `TOOL_MEMORY_COMPACT_PIN_MAX_CHARS` (constant), lines 4124-4124, exports `TOOL_MEMORY_COMPACT_PIN_MAX_CHARS`
- order 313: `TOOL_MEMORY_POLICY_CHOICES` (constant), lines 4125-4125, exports `TOOL_MEMORY_POLICY_CHOICES`
- order 314: `DEFAULT_TOOL_MEMORY_POLICY` (constant), lines 4126-4126, exports `DEFAULT_TOOL_MEMORY_POLICY`
- order 315: `DEFAULT_AUTO_TASK_LEVEL_CEILING` (constant), lines 4127-4127, exports `DEFAULT_AUTO_TASK_LEVEL_CEILING`
- order 316: `HARD_BREAK_TOOL_ERROR_THRESHOLD` (constant), lines 4128-4128, exports `HARD_BREAK_TOOL_ERROR_THRESHOLD`
- order 317: `HARD_BREAK_RECOVERY_ROUND_THRESHOLD` (constant), lines 4129-4131, exports `HARD_BREAK_RECOVERY_ROUND_THRESHOLD`
- order 318: `FUSED_FAULT_BREAK_THRESHOLD` (constant), lines 4132-4132, exports `FUSED_FAULT_BREAK_THRESHOLD`
- order 319: `STALL_SEVERITY_ESCALATION_THRESHOLD` (constant), lines 4133-4133, exports `STALL_SEVERITY_ESCALATION_THRESHOLD`
- order 320: `STALL_SEVERITY_WEIGHT_BASH_READ_LOOP` (constant), lines 4134-4134, exports `STALL_SEVERITY_WEIGHT_BASH_READ_LOOP`
- order 321: `STALL_SEVERITY_WEIGHT_REPEATED_TOOL` (constant), lines 4135-4135, exports `STALL_SEVERITY_WEIGHT_REPEATED_TOOL`
- order 322: `STALL_SEVERITY_WEIGHT_FAULT` (constant), lines 4136-4136, exports `STALL_SEVERITY_WEIGHT_FAULT`
- order 323: `STALL_SEVERITY_WEIGHT_RECOVERY_RETRY` (constant), lines 4137-4137, exports `STALL_SEVERITY_WEIGHT_RECOVERY_RETRY`
- order 324: `STALL_SEVERITY_WEIGHT_WATCHDOG` (constant), lines 4138-4138, exports `STALL_SEVERITY_WEIGHT_WATCHDOG`
- order 325: `STALL_SEVERITY_DECAY_ON_SUCCESS` (constant), lines 4139-4139, exports `STALL_SEVERITY_DECAY_ON_SUCCESS`
- order 326: `STALL_ESCALATION_MIN_LEVEL` (constant), lines 4140-4140, exports `STALL_ESCALATION_MIN_LEVEL`
- order 327: `STALL_PLAN_SYNTHESIS_MAX_TOKENS` (constant), lines 4141-4141, exports `STALL_PLAN_SYNTHESIS_MAX_TOKENS`
- order 328: `STALL_ESCALATION_CONTEXT_MAX_CHARS` (constant), lines 4142-4142, exports `STALL_ESCALATION_CONTEXT_MAX_CHARS`
- order 329: `MAX_RUN_SECONDS` (constant), lines 4143-4143, exports `MAX_RUN_SECONDS`
- order 330: `MIN_RUN_TIMEOUT_SECONDS` (constant), lines 4144-4144, exports `MIN_RUN_TIMEOUT_SECONDS`
- order 331: `MAX_RUN_TIMEOUT_SECONDS` (constant), lines 4145-4145, exports `MAX_RUN_TIMEOUT_SECONDS`
- order 332: `MIN_TIMEOUT_SECONDS` (constant), lines 4146-4146, exports `MIN_TIMEOUT_SECONDS`
- order 333: `MAX_TIMEOUT_SECONDS` (constant), lines 4147-4147, exports `MAX_TIMEOUT_SECONDS`
- order 334: `DEFAULT_TIMEOUT_SECONDS` (constant), lines 4148-4154, exports `DEFAULT_TIMEOUT_SECONDS`
- order 335: `DEFAULT_REQUEST_TIMEOUT` (constant), lines 4155-4155, exports `DEFAULT_REQUEST_TIMEOUT`
- order 336: `_SHELL_AUTO_CONFIRM_PATTERNS` (assignment), lines 4156-4171, exports `_SHELL_AUTO_CONFIRM_PATTERNS`
- order 337: `MIN_SHELL_COMMAND_TIMEOUT_SECONDS` (constant), lines 4172-4172, exports `MIN_SHELL_COMMAND_TIMEOUT_SECONDS`
- order 338: `MAX_SHELL_COMMAND_TIMEOUT_SECONDS` (constant), lines 4173-4173, exports `MAX_SHELL_COMMAND_TIMEOUT_SECONDS`
- order 339: `SHELL_TIMEOUT_MODES` (constant), lines 4174-4174, exports `SHELL_TIMEOUT_MODES`
- order 340: `_DEFAULT_SHELL_TIMEOUT_MODE_RAW` (assignment), lines 4175-4178, exports `_DEFAULT_SHELL_TIMEOUT_MODE_RAW`
- order 341: `DEFAULT_SHELL_TIMEOUT_MODE` (constant), lines 4179-4183, exports `DEFAULT_SHELL_TIMEOUT_MODE`
- order 342: `MIN_SHELL_ASYNC_HANDOFF_SECONDS` (constant), lines 4184-4184, exports `MIN_SHELL_ASYNC_HANDOFF_SECONDS`
- order 343: `MAX_SHELL_ASYNC_HANDOFF_SECONDS` (constant), lines 4185-4185, exports `MAX_SHELL_ASYNC_HANDOFF_SECONDS`
- order 344: `SHELL_FAILURE_GUIDANCE_SECONDS` (constant), lines 4186-4188, exports `SHELL_FAILURE_GUIDANCE_SECONDS`
- order 345: `DEFAULT_SHELL_ASYNC_HANDOFF_SECONDS` (constant), lines 4189-4203, exports `DEFAULT_SHELL_ASYNC_HANDOFF_SECONDS`
- order 346: `DEFAULT_SHELL_COMMAND_TIMEOUT_SECONDS` (constant), lines 4204-4218, exports `DEFAULT_SHELL_COMMAND_TIMEOUT_SECONDS`
- order 347: `DEFAULT_SINGLE_NO_PLAN_TODO_PROMPT` (constant), lines 4219-4233, exports `DEFAULT_SINGLE_NO_PLAN_TODO_PROMPT`
- order 348: `SINGLE_NO_PLAN_TODO_BOOTSTRAP_MAX_ATTEMPTS` (constant), lines 4234-4234, exports `SINGLE_NO_PLAN_TODO_BOOTSTRAP_MAX_ATTEMPTS`
- order 349: `AUTO_CONTINUE_BUDGET_DEFAULT` (constant), lines 4235-4235, exports `AUTO_CONTINUE_BUDGET_DEFAULT`
- order 350: `AGENT_MAX_OUTPUT_TOKENS` (constant), lines 4236-4236, exports `AGENT_MAX_OUTPUT_TOKENS`
- order 351: `OLLAMA_THINKING_TOOL_BUFFER` (constant), lines 4237-4237, exports `OLLAMA_THINKING_TOOL_BUFFER`
- order 352: `WATCHDOG_INTENT_NO_TOOL_THRESHOLD` (constant), lines 4238-4238, exports `WATCHDOG_INTENT_NO_TOOL_THRESHOLD`
- order 353: `WATCHDOG_REPEAT_NO_TOOL_THRESHOLD` (constant), lines 4239-4239, exports `WATCHDOG_REPEAT_NO_TOOL_THRESHOLD`
- order 354: `WATCHDOG_INTENT_NO_TOOL_THRESHOLD_SINGLE` (constant), lines 4240-4240, exports `WATCHDOG_INTENT_NO_TOOL_THRESHOLD_SINGLE`
- order 355: `WATCHDOG_REPEAT_NO_TOOL_THRESHOLD_SINGLE` (constant), lines 4241-4241, exports `WATCHDOG_REPEAT_NO_TOOL_THRESHOLD_SINGLE`
- order 356: `WATCHDOG_STATE_STALL_THRESHOLD` (constant), lines 4242-4242, exports `WATCHDOG_STATE_STALL_THRESHOLD`
- order 357: `WATCHDOG_CONTEXT_STALL_THRESHOLD` (constant), lines 4243-4243, exports `WATCHDOG_CONTEXT_STALL_THRESHOLD`
- order 358: `WATCHDOG_REPEAT_SIMILARITY_THRESHOLD` (constant), lines 4244-4244, exports `WATCHDOG_REPEAT_SIMILARITY_THRESHOLD`
- order 359: `WATCHDOG_CONTEXT_NEAR_RATIO` (constant), lines 4245-4245, exports `WATCHDOG_CONTEXT_NEAR_RATIO`
- order 360: `WATCHDOG_MAX_DECOMPOSE_STEPS` (constant), lines 4246-4246, exports `WATCHDOG_MAX_DECOMPOSE_STEPS`
- order 361: `WATCHDOG_STEP_MAX_ATTEMPTS` (constant), lines 4247-4247, exports `WATCHDOG_STEP_MAX_ATTEMPTS`
- order 362: `EMPTY_ACTION_MIN_CONTENT_CHARS` (constant), lines 4248-4248, exports `EMPTY_ACTION_MIN_CONTENT_CHARS`
- order 363: `EMPTY_ACTION_WAKEUP_RETRY_LIMIT` (constant), lines 4249-4249, exports `EMPTY_ACTION_WAKEUP_RETRY_LIMIT`
- order 364: `THINKING_BUDGET_FORCE_RATIO` (constant), lines 4250-4250, exports `THINKING_BUDGET_FORCE_RATIO`
- order 365: `_TOOL_TIMEOUT_MAP` (assignment), lines 4251-4272, exports `_TOOL_TIMEOUT_MAP`
- order 366: `_DEFAULT_TOOL_TIMEOUT` (assignment), lines 4273-4273, exports `_DEFAULT_TOOL_TIMEOUT`
- order 367: `CONVERSATION_VISIBLE_TOOL_EVENTS` (constant), lines 4274-4286, exports `CONVERSATION_VISIBLE_TOOL_EVENTS`
- order 368: `PERSIST_ON_EVENT_TYPES` (constant), lines 4287-4304, exports `PERSIST_ON_EVENT_TYPES`
- order 369: `PERSIST_EVENT_MIN_INTERVAL_SECONDS` (constant), lines 4305-4305, exports `PERSIST_EVENT_MIN_INTERVAL_SECONDS`
- order 370: `TRUNCATION_CONTINUATION_MAX_PASSES` (constant), lines 4306-4306, exports `TRUNCATION_CONTINUATION_MAX_PASSES`
- order 371: `TRUNCATION_CONTINUATION_MAX_TOKENS` (constant), lines 4307-4307, exports `TRUNCATION_CONTINUATION_MAX_TOKENS`
- order 372: `TRUNCATION_CONTINUATION_TAIL_CHARS` (constant), lines 4308-4308, exports `TRUNCATION_CONTINUATION_TAIL_CHARS`
- order 373: `TRUNCATION_CONTINUATION_ECHO_CHARS` (constant), lines 4309-4309, exports `TRUNCATION_CONTINUATION_ECHO_CHARS`
- order 374: `TRUNCATION_OVERLAP_SCAN_CHARS` (constant), lines 4310-4310, exports `TRUNCATION_OVERLAP_SCAN_CHARS`
- order 375: `TRUNCATION_PAIR_SCAN_CHARS` (constant), lines 4311-4311, exports `TRUNCATION_PAIR_SCAN_CHARS`
- order 376: `TRUNCATION_LIVE_BUFFER_MAX_CHARS` (constant), lines 4312-4312, exports `TRUNCATION_LIVE_BUFFER_MAX_CHARS`
- order 377: `MIN_CONTEXT_TOKEN_LIMIT` (constant), lines 4313-4313, exports `MIN_CONTEXT_TOKEN_LIMIT`
- order 378: `COMPACT_TIER1_PCT` (constant), lines 4314-4315, exports `COMPACT_TIER1_PCT`
- order 379: `COMPACT_TIER2_PCT` (constant), lines 4316-4316, exports `COMPACT_TIER2_PCT`
- order 380: `COMPACT_TIER3_PCT` (constant), lines 4317-4317, exports `COMPACT_TIER3_PCT`
- order 381: `COMPACT_TIER1_ABS` (constant), lines 4318-4319, exports `COMPACT_TIER1_ABS`
- order 382: `COMPACT_TIER2_ABS` (constant), lines 4320-4320, exports `COMPACT_TIER2_ABS`
- order 383: `CONTEXT_COMPACT_INEFFECTIVE_COOLDOWN_SECONDS` (constant), lines 4321-4327, exports `CONTEXT_COMPACT_INEFFECTIVE_COOLDOWN_SECONDS`
- order 384: `FILE_BUFFER_CONTENT_THRESHOLD` (constant), lines 4328-4329, exports `FILE_BUFFER_CONTENT_THRESHOLD`
- order 385: `FILE_BUFFER_MAX_FILES` (constant), lines 4330-4330, exports `FILE_BUFFER_MAX_FILES`
- order 386: `AUTHORITATIVE_USER_GOAL_OPEN` (constant), lines 4331-4331, exports `AUTHORITATIVE_USER_GOAL_OPEN`
- order 387: `AUTHORITATIVE_USER_GOAL_CLOSE` (constant), lines 4332-4332, exports `AUTHORITATIVE_USER_GOAL_CLOSE`
- order 388: `AGENT_MSG_LIMIT_TIER0` (constant), lines 4333-4334, exports `AGENT_MSG_LIMIT_TIER0`
- order 389: `AGENT_MSG_LIMIT_TIER1` (constant), lines 4335-4335, exports `AGENT_MSG_LIMIT_TIER1`
- order 390: `AGENT_MSG_LIMIT_TIER2` (constant), lines 4336-4336, exports `AGENT_MSG_LIMIT_TIER2`
- order 391: `AGENT_MSG_LIMIT_TIER3` (constant), lines 4337-4337, exports `AGENT_MSG_LIMIT_TIER3`
- order 392: `AGENT_CTX_LIMIT_TIER0` (constant), lines 4338-4338, exports `AGENT_CTX_LIMIT_TIER0`
- order 393: `AGENT_CTX_LIMIT_TIER1` (constant), lines 4339-4339, exports `AGENT_CTX_LIMIT_TIER1`
- order 394: `AGENT_CTX_LIMIT_TIER2` (constant), lines 4340-4340, exports `AGENT_CTX_LIMIT_TIER2`
- order 395: `AGENT_CTX_LIMIT_TIER3` (constant), lines 4341-4341, exports `AGENT_CTX_LIMIT_TIER3`
- order 396: `MANAGER_CTX_LIMIT_TIER0` (constant), lines 4342-4342, exports `MANAGER_CTX_LIMIT_TIER0`
- order 397: `MANAGER_CTX_LIMIT_TIER1` (constant), lines 4343-4343, exports `MANAGER_CTX_LIMIT_TIER1`
- order 398: `MANAGER_CTX_LIMIT_TIER2` (constant), lines 4344-4344, exports `MANAGER_CTX_LIMIT_TIER2`
- order 399: `MANAGER_CTX_LIMIT_TIER3` (constant), lines 4345-4345, exports `MANAGER_CTX_LIMIT_TIER3`
- order 400: `MAX_CONTEXT_ARCHIVE_SEGMENTS` (constant), lines 4346-4346, exports `MAX_CONTEXT_ARCHIVE_SEGMENTS`
- order 401: `MAX_USER_BUBBLE_LOG` (constant), lines 4347-4348, exports `MAX_USER_BUBBLE_LOG`
- order 402: `MANAGER_INSTRUCTION_MAX_CHARS` (constant), lines 4349-4353, exports `MANAGER_INSTRUCTION_MAX_CHARS`
- order 403: `MANAGER_MOMENTUM_MAX_SKIPS` (constant), lines 4354-4359, exports `MANAGER_MOMENTUM_MAX_SKIPS`
- order 404: `MODEL_OUTPUT_RETRY_TIMES` (constant), lines 4360-4364, exports `MODEL_OUTPUT_RETRY_TIMES`
- order 405: `ARBITER_TRIGGER_MIN_CONTENT_CHARS` (constant), lines 4365-4365, exports `ARBITER_TRIGGER_MIN_CONTENT_CHARS`
- order 406: `ARBITER_VALID_PLANNING_STREAK_LIMIT` (constant), lines 4366-4366, exports `ARBITER_VALID_PLANNING_STREAK_LIMIT`
- order 407: `ARBITER_DEFAULT_TIMEOUT_SECONDS` (constant), lines 4367-4367, exports `ARBITER_DEFAULT_TIMEOUT_SECONDS`
- order 408: `ARBITER_DEFAULT_MAX_TOKENS` (constant), lines 4368-4368, exports `ARBITER_DEFAULT_MAX_TOKENS`
- order 409: `ARBITER_DEFAULT_TEMPERATURE` (constant), lines 4369-4369, exports `ARBITER_DEFAULT_TEMPERATURE`
- order 410: `LIVE_INPUT_DELAY_WRITE_ROUNDS` (constant), lines 4370-4370, exports `LIVE_INPUT_DELAY_WRITE_ROUNDS`
- order 411: `LIVE_INPUT_DELAY_TOOL_ROUNDS` (constant), lines 4371-4371, exports `LIVE_INPUT_DELAY_TOOL_ROUNDS`
- order 412: `LIVE_INPUT_DELAY_NORMAL_ROUNDS` (constant), lines 4372-4372, exports `LIVE_INPUT_DELAY_NORMAL_ROUNDS`
- order 413: `LIVE_INPUT_MAX_INJECTIONS` (constant), lines 4373-4373, exports `LIVE_INPUT_MAX_INJECTIONS`
- order 414: `LIVE_INPUT_REINJECT_INTERVAL` (constant), lines 4374-4374, exports `LIVE_INPUT_REINJECT_INTERVAL`
- order 415: `LIVE_INPUT_WEIGHT_BASE_DELAYED` (constant), lines 4375-4375, exports `LIVE_INPUT_WEIGHT_BASE_DELAYED`
- order 416: `LIVE_INPUT_WEIGHT_BASE_NORMAL` (constant), lines 4376-4376, exports `LIVE_INPUT_WEIGHT_BASE_NORMAL`
- order 417: `LIVE_INPUT_WEIGHT_STEP_DELAYED` (constant), lines 4377-4377, exports `LIVE_INPUT_WEIGHT_STEP_DELAYED`
- order 418: `LIVE_INPUT_WEIGHT_STEP_NORMAL` (constant), lines 4378-4378, exports `LIVE_INPUT_WEIGHT_STEP_NORMAL`
- order 420: `BENIGN_SOCKET_DEBUG_LOG_ENABLED` (constant), lines 4385-4391, exports `BENIGN_SOCKET_DEBUG_LOG_ENABLED`
- order 421: `BENIGN_SOCKET_LOG_INTERVAL_SECONDS` (constant), lines 4392-4392, exports `BENIGN_SOCKET_LOG_INTERVAL_SECONDS`
- order 422: `FINAL_SUMMARY_MIN_CHARS` (constant), lines 4393-4393, exports `FINAL_SUMMARY_MIN_CHARS`
- order 423: `FINAL_SUMMARY_STRICT_MIN_CHARS` (constant), lines 4394-4394, exports `FINAL_SUMMARY_STRICT_MIN_CHARS`
- order 424: `RUNTIME_CONTROL_HINT_PREFIXES` (constant), lines 4395-4414, exports `RUNTIME_CONTROL_HINT_PREFIXES`
- order 425: `RETRY_RUNTIME_HINT_PREFIXES` (constant), lines 4415-4429, exports `RETRY_RUNTIME_HINT_PREFIXES`
- order 426: `EXECUTION_MODE_SINGLE` (constant), lines 4430-4430, exports `EXECUTION_MODE_SINGLE`
- order 427: `EXECUTION_MODE_SEQUENTIAL` (constant), lines 4431-4431, exports `EXECUTION_MODE_SEQUENTIAL`
- order 428: `EXECUTION_MODE_SYNC` (constant), lines 4432-4432, exports `EXECUTION_MODE_SYNC`
- order 429: `EXECUTION_MODE_CHOICES` (constant), lines 4433-4437, exports `EXECUTION_MODE_CHOICES`
- order 430: `AGENT_ROLES` (constant), lines 4438-4438, exports `AGENT_ROLES`
- order 431: `AGENT_BUBBLE_ROLES` (constant), lines 4439-4439, exports `AGENT_BUBBLE_ROLES`
- order 432: `AGENT_ROLE_LABELS` (constant), lines 4440-4446, exports `AGENT_ROLE_LABELS`
- order 433: `AGENT_ROLE_BUBBLE_COLORS` (constant), lines 4447-4453, exports `AGENT_ROLE_BUBBLE_COLORS`
- order 434: `BLACKBOARD_STATUSES` (constant), lines 4454-4463, exports `BLACKBOARD_STATUSES`
- order 435: `TASK_COMPLEXITY_LEVELS` (constant), lines 4464-4464, exports `TASK_COMPLEXITY_LEVELS`
- order 436: `TASK_COMPLEXITY_RANKS` (constant), lines 4465-4470, exports `TASK_COMPLEXITY_RANKS`
- order 437: `TASK_PROFILE_TYPES` (constant), lines 4471-4477, exports `TASK_PROFILE_TYPES`
- order 438: `TASK_LEVEL_CHOICES` (constant), lines 4478-4478, exports `TASK_LEVEL_CHOICES`
- order 439: `TASK_SCALE_PREFERENCES` (constant), lines 4479-4479, exports `TASK_SCALE_PREFERENCES`
- order 440: `SEMANTIC_CONFIDENCE_CHOICES` (constant), lines 4480-4480, exports `SEMANTIC_CONFIDENCE_CHOICES`
- order 441: `L2_TODO_POLICY_CHOICES` (constant), lines 4481-4485, exports `L2_TODO_POLICY_CHOICES`
- order 442: `DEFAULT_L2_TODO_POLICY` (constant), lines 4486-4486, exports `DEFAULT_L2_TODO_POLICY`
- order 443: `TASK_LEVEL_POLICIES` (constant), lines 4487-4540, exports `TASK_LEVEL_POLICIES`
- order 444: `MANAGER_ROUTE_TARGETS` (constant), lines 4541-4541, exports `MANAGER_ROUTE_TARGETS`
- order 445: `BLACKBOARD_MAX_LOG_ENTRIES` (constant), lines 4542-4542, exports `BLACKBOARD_MAX_LOG_ENTRIES`
- order 446: `BLACKBOARD_MAX_TEXT` (constant), lines 4543-4543, exports `BLACKBOARD_MAX_TEXT`
- order 447: `BLACKBOARD_MEMORY_SHORT_MAX` (constant), lines 4544-4544, exports `BLACKBOARD_MEMORY_SHORT_MAX`
- order 448: `BLACKBOARD_MEMORY_MID_MAX_STEPS` (constant), lines 4545-4545, exports `BLACKBOARD_MEMORY_MID_MAX_STEPS`
- order 449: `BLACKBOARD_MEMORY_MID_ITEMS_PER_STEP` (constant), lines 4546-4546, exports `BLACKBOARD_MEMORY_MID_ITEMS_PER_STEP`
- order 450: `BLACKBOARD_MEMORY_LONG_MAX` (constant), lines 4547-4547, exports `BLACKBOARD_MEMORY_LONG_MAX`
- order 451: `BLACKBOARD_MEMORY_INDEX_MAX` (constant), lines 4548-4548, exports `BLACKBOARD_MEMORY_INDEX_MAX`
- order 452: `SKILL_REFRESH_MIN_INTERVAL_SECONDS` (constant), lines 4549-4549, exports `SKILL_REFRESH_MIN_INTERVAL_SECONDS`
- order 453: `SKILL_PROMPT_MAX_ITEMS` (constant), lines 4550-4550, exports `SKILL_PROMPT_MAX_ITEMS`
- order 454: `SKILL_PROMPT_MAX_CHARS` (constant), lines 4551-4551, exports `SKILL_PROMPT_MAX_CHARS`
- order 455: `SKILL_RUNTIME_CACHE_MAX_ENTRIES` (constant), lines 4552-4552, exports `SKILL_RUNTIME_CACHE_MAX_ENTRIES`
- order 456: `SKILL_RUNTIME_CACHE_MAX_BYTES` (constant), lines 4553-4553, exports `SKILL_RUNTIME_CACHE_MAX_BYTES`
- order 457: `AUTO_SKILLS_ROOT_CANDIDATES` (constant), lines 4554-4554, exports `AUTO_SKILLS_ROOT_CANDIDATES`
- order 458: `SKILL_DEFAULT_ATTACHMENT_GLOBS` (constant), lines 4555-4585, exports `SKILL_DEFAULT_ATTACHMENT_GLOBS`
- order 459: `SKILL_INLINE_ATTACHMENT_MAX_FILES` (constant), lines 4586-4586, exports `SKILL_INLINE_ATTACHMENT_MAX_FILES`
- order 460: `SKILL_INLINE_ATTACHMENT_MAX_CHARS` (constant), lines 4587-4587, exports `SKILL_INLINE_ATTACHMENT_MAX_CHARS`
- order 461: `SKILL_RESOURCE_MANIFEST_MAX_ITEMS` (constant), lines 4588-4588, exports `SKILL_RESOURCE_MANIFEST_MAX_ITEMS`
- order 462: `SKILL_BODY_COMPACT_THRESHOLD_CHARS` (constant), lines 4589-4589, exports `SKILL_BODY_COMPACT_THRESHOLD_CHARS`
- order 463: `SKILL_BODY_PREVIEW_CHARS` (constant), lines 4590-4590, exports `SKILL_BODY_PREVIEW_CHARS`
- order 464: `SKILLS_VIRTUAL_PREFIX` (constant), lines 4591-4591, exports `SKILLS_VIRTUAL_PREFIX`
- order 465: `SKILLS_EXTERNAL_MOUNT` (constant), lines 4592-4592, exports `SKILLS_EXTERNAL_MOUNT`
- order 466: `PLAN_MODE_ENABLED_LEVELS` (constant), lines 4593-4593, exports `PLAN_MODE_ENABLED_LEVELS`
- order 467: `PLAN_MODE_FORCED_LEVELS` (constant), lines 4594-4594, exports `PLAN_MODE_FORCED_LEVELS`
- order 468: `PLAN_MODE_USER_CHOICES` (constant), lines 4595-4595, exports `PLAN_MODE_USER_CHOICES`
- order 469: `TASK_PHASES` (constant), lines 4596-4597, exports `TASK_PHASES`
- order 470: `TASK_PHASE_ROUTING` (constant), lines 4598-4605, exports `TASK_PHASE_ROUTING`
- order 471: `COMPLEXITY_KEYWORDS` (constant), lines 4606-4612, exports `COMPLEXITY_KEYWORDS`
- order 472: `USER_COMPLEXITY_SIMPLE_TOKENS` (constant), lines 4613-4617, exports `USER_COMPLEXITY_SIMPLE_TOKENS`
- order 473: `USER_COMPLEXITY_MODERATE_TOKENS` (constant), lines 4618-4622, exports `USER_COMPLEXITY_MODERATE_TOKENS`
- order 474: `USER_COMPLEXITY_COMPLEX_TOKENS` (constant), lines 4623-4627, exports `USER_COMPLEXITY_COMPLEX_TOKENS`
- order 475: `USER_COMPLEXITY_EXPERT_TOKENS` (constant), lines 4628-4632, exports `USER_COMPLEXITY_EXPERT_TOKENS`
- order 476: `PLAN_MODE_EXPLORER_MAX_ROUNDS` (constant), lines 4633-4636, exports `PLAN_MODE_EXPLORER_MAX_ROUNDS`
- order 477: `PLAN_MODE_EXPLORER_PRODUCTIVE_ROUNDS` (constant), lines 4637-4637, exports `PLAN_MODE_EXPLORER_PRODUCTIVE_ROUNDS`
- order 478: `PLAN_MODE_EXPLORER_STALE_ROUNDS` (constant), lines 4638-4638, exports `PLAN_MODE_EXPLORER_STALE_ROUNDS`
- order 479: `PLAN_MODE_SYNTHESIS_MAX_ATTEMPTS` (constant), lines 4639-4639, exports `PLAN_MODE_SYNTHESIS_MAX_ATTEMPTS`
- order 480: `REVIEWER_DEBUG_MODE_MAX_ROUNDS` (constant), lines 4640-4641, exports `REVIEWER_DEBUG_MODE_MAX_ROUNDS`
- order 481: `REVIEWER_DEBUG_TOOL_ALLOWLIST` (constant), lines 4642-4647, exports `REVIEWER_DEBUG_TOOL_ALLOWLIST`
- order 482: `EXPLORER_STALL_THRESHOLD` (constant), lines 4648-4648, exports `EXPLORER_STALL_THRESHOLD`
- order 483: `DEVELOPER_EDIT_STALL_THRESHOLD` (constant), lines 4649-4649, exports `DEVELOPER_EDIT_STALL_THRESHOLD`
- order 484: `ACCEPTANCE_GATE_STALL_THRESHOLD` (constant), lines 4650-4653, exports `ACCEPTANCE_GATE_STALL_THRESHOLD`
- order 485: `ACCEPTANCE_GATE_HARD_CEILING` (constant), lines 4654-4657, exports `ACCEPTANCE_GATE_HARD_CEILING`
- order 486: `ACCEPTANCE_GATE_TOTAL_ROUND_CEILING` (constant), lines 4658-4658, exports `ACCEPTANCE_GATE_TOTAL_ROUND_CEILING`
- order 487: `PLAN_MODE_MANAGER_SYNTHESIS_MAX_TOKENS` (constant), lines 4659-4659, exports `PLAN_MODE_MANAGER_SYNTHESIS_MAX_TOKENS`
- order 488: `PLAN_MODE_MAX_OPTIONS` (constant), lines 4660-4660, exports `PLAN_MODE_MAX_OPTIONS`
- order 489: `PLAN_FILE_RELATIVE_PATH` (constant), lines 4661-4661, exports `PLAN_FILE_RELATIVE_PATH`
- order 490: `PLAN_BUBBLE_MAX_CHARS` (constant), lines 4662-4662, exports `PLAN_BUBBLE_MAX_CHARS`
- order 491: `PLAN_NOTICE_BODY_MAX_CHARS` (constant), lines 4663-4663, exports `PLAN_NOTICE_BODY_MAX_CHARS`
- order 492: `PLAN_MESSAGE_EVENT_MAX_CHARS` (constant), lines 4664-4664, exports `PLAN_MESSAGE_EVENT_MAX_CHARS`
- order 493: `PLAN_STEP_FULL_CONTENT_MAX_CHARS` (constant), lines 4665-4665, exports `PLAN_STEP_FULL_CONTENT_MAX_CHARS`
- order 494: `PLAN_MODE_RESEARCH_TOOL_ALLOWLIST` (constant), lines 4666-4673, exports `PLAN_MODE_RESEARCH_TOOL_ALLOWLIST`
- order 495: `FAILURE_LEDGER_MAX_FIXES` (constant), lines 4674-4674, exports `FAILURE_LEDGER_MAX_FIXES`
- order 496: `FAILURE_LEDGER_MAX_COMPILE_ERRORS` (constant), lines 4675-4675, exports `FAILURE_LEDGER_MAX_COMPILE_ERRORS`
- order 497: `FAILURE_LEDGER_MAX_DELEGATIONS` (constant), lines 4676-4676, exports `FAILURE_LEDGER_MAX_DELEGATIONS`
- order 498: `FAILURE_LEDGER_MAX_STALLS` (constant), lines 4677-4677, exports `FAILURE_LEDGER_MAX_STALLS`
- order 499: `FAILURE_LEDGER_MAX_TOOL_FPS` (constant), lines 4678-4678, exports `FAILURE_LEDGER_MAX_TOOL_FPS`
- order 500: `FAILURE_LEDGER_MAX_ERRORS` (constant), lines 4679-4679, exports `FAILURE_LEDGER_MAX_ERRORS`
- order 501: `ERROR_CATEGORY_DEFS` (constant), lines 4680-4719, exports `ERROR_CATEGORY_DEFS`
- order 502: `CHECKPOINT_MAX_COUNT` (constant), lines 4720-4720, exports `CHECKPOINT_MAX_COUNT`
- order 503: `CHECKPOINT_INTERVAL_ROUNDS` (constant), lines 4721-4721, exports `CHECKPOINT_INTERVAL_ROUNDS`
- order 504: `PERSISTED_ROUTES_MAX` (constant), lines 4722-4722, exports `PERSISTED_ROUTES_MAX`
- order 505: `HTML_FRONTEND_REQUEST_KEYWORDS` (constant), lines 4723-4762, exports `HTML_FRONTEND_REQUEST_KEYWORDS`
- order 506: `DEEP_RESEARCH_REQUEST_KEYWORDS` (constant), lines 4763-4785, exports `DEEP_RESEARCH_REQUEST_KEYWORDS`
- order 507: `DEEP_RESEARCH_RETRIEVAL_KEYWORDS` (constant), lines 4786-4805, exports `DEEP_RESEARCH_RETRIEVAL_KEYWORDS`
- order 508: `DEEP_RESEARCH_TEXT_ONLY_HINT_KEYWORDS` (constant), lines 4806-4823, exports `DEEP_RESEARCH_TEXT_ONLY_HINT_KEYWORDS`
- order 509: `DANGEROUS_PATTERNS` (constant), lines 4824-4825, exports `DANGEROUS_PATTERNS`
- order 510: `VALID_MSG_TYPES` (constant), lines 4826-4832, exports `VALID_MSG_TYPES`
- order 511: `SUPPORTED_UI_LANGUAGES` (constant), lines 4833-4839, exports `SUPPORTED_UI_LANGUAGES`
- order 512: `UI_LANGUAGE_LABELS` (constant), lines 4840-4840, exports `UI_LANGUAGE_LABELS`
- order 513: `DEFAULT_UI_LANGUAGE` (constant), lines 4841-4841, exports `DEFAULT_UI_LANGUAGE`
- order 514: `PUBLIC_TOOL_PROGRESS_SUMMARY_ENABLED` (constant), lines 4842-4844, exports `PUBLIC_TOOL_PROGRESS_SUMMARY_ENABLED`
- order 515: `AGENT_LANGUAGE_PREFERENCES` (constant), lines 4845-4886, exports `AGENT_LANGUAGE_PREFERENCES`
- order 516: `UI_STYLE_CHOICES` (constant), lines 4887-4887, exports `UI_STYLE_CHOICES`
- order 517: `UI_STYLE_LABELS` (constant), lines 4888-4888, exports `UI_STYLE_LABELS`
- order 518: `DEFAULT_UI_STYLE` (constant), lines 4889-4889, exports `DEFAULT_UI_STYLE`
- order 519: `DEFAULT_WEB_UI_DIR` (constant), lines 4890-4890, exports `DEFAULT_WEB_UI_DIR`
- order 520: `DEFAULT_WEB_UI_CONFIG` (constant), lines 4891-4891, exports `DEFAULT_WEB_UI_CONFIG`
- order 521: `WEB_UI_REQUIRED_FILES` (constant), lines 4892-4899, exports `WEB_UI_REQUIRED_FILES`
- order 522: `WEB_UI_OPTIONAL_FILES` (constant), lines 4900-4900, exports `WEB_UI_OPTIONAL_FILES`
- order 523: `WEB_UI_APPLICATION_CONTRACT_VERSION` (constant), lines 4901-4901, exports `WEB_UI_APPLICATION_CONTRACT_VERSION`
- order 524: `WEB_UI_APPLICATION_FEATURE_MARKERS` (constant), lines 4902-4921, exports `WEB_UI_APPLICATION_FEATURE_MARKERS`
- order 525: `IMAGE_EXTS` (constant), lines 4922-4936, exports `IMAGE_EXTS`
- order 526: `IMAGE_FORMATS_NEED_CONVERSION` (constant), lines 4937-4937, exports `IMAGE_FORMATS_NEED_CONVERSION`
- order 527: `IMAGE_SAFE_FORMATS` (constant), lines 4938-4938, exports `IMAGE_SAFE_FORMATS`
- order 528: `AUDIO_EXTS` (constant), lines 4939-4949, exports `AUDIO_EXTS`
- order 529: `VIDEO_EXTS` (constant), lines 4950-4960, exports `VIDEO_EXTS`
- order 530: `CODE_PREVIEW_STAGE_MAX_BYTES` (constant), lines 4961-4961, exports `CODE_PREVIEW_STAGE_MAX_BYTES`
- order 531: `CODE_PREVIEW_STAGE_MAX_ROWS` (constant), lines 4962-4962, exports `CODE_PREVIEW_STAGE_MAX_ROWS`
- order 532: `CODE_PREVIEW_STAGE_MAX_PER_FILE` (constant), lines 4963-4963, exports `CODE_PREVIEW_STAGE_MAX_PER_FILE`
- order 533: `CODE_PREVIEW_STAGE_MAX_TOTAL` (constant), lines 4964-4964, exports `CODE_PREVIEW_STAGE_MAX_TOTAL`
- order 534: `CODE_PREVIEW_DIFF_CONTEXT_LINES` (constant), lines 4965-4965, exports `CODE_PREVIEW_DIFF_CONTEXT_LINES`
- order 535: `CODE_PREVIEW_DIFF_MERGE_GAP` (constant), lines 4966-4966, exports `CODE_PREVIEW_DIFF_MERGE_GAP`
- order 536: `PREVIEW_DOWNLOAD_MAX_FILES` (constant), lines 4967-4967, exports `PREVIEW_DOWNLOAD_MAX_FILES`
- order 537: `PREVIEW_DOWNLOAD_MAX_BYTES` (constant), lines 4968-4968, exports `PREVIEW_DOWNLOAD_MAX_BYTES`
- order 538: `FILES_TREE_DEFAULT_MAX_NODES` (constant), lines 4969-4969, exports `FILES_TREE_DEFAULT_MAX_NODES`
- order 539: `FILES_TREE_DEFAULT_MAX_DEPTH` (constant), lines 4970-4970, exports `FILES_TREE_DEFAULT_MAX_DEPTH`
- order 540: `FILES_TREE_SKIP_DIRS` (constant), lines 4971-4979, exports `FILES_TREE_SKIP_DIRS`
- order 541: `FILES_TREE_SKIP_REL_DIRS` (constant), lines 4980-4982, exports `FILES_TREE_SKIP_REL_DIRS`
- order 542: `IDE_FILE_MAX_BYTES` (constant), lines 4983-4983, exports `IDE_FILE_MAX_BYTES`
- order 543: `IDE_UPLOAD_MAX_BYTES` (constant), lines 4984-4984, exports `IDE_UPLOAD_MAX_BYTES`
- order 544: `IDE_UPLOAD_TOTAL_MAX_BYTES` (constant), lines 4985-4985, exports `IDE_UPLOAD_TOTAL_MAX_BYTES`
- order 545: `IDE_UPLOAD_MAX_ITEMS` (constant), lines 4986-4986, exports `IDE_UPLOAD_MAX_ITEMS`
- order 546: `IDE_UPLOAD_CHUNK_MAX_BYTES` (constant), lines 4987-4987, exports `IDE_UPLOAD_CHUNK_MAX_BYTES`
- order 547: `IDE_UPLOAD_STREAM_MAX_BYTES` (constant), lines 4988-4988, exports `IDE_UPLOAD_STREAM_MAX_BYTES`
- order 548: `IDE_TEXT_PREVIEW_MAX_BYTES` (constant), lines 4989-4989, exports `IDE_TEXT_PREVIEW_MAX_BYTES`
- order 549: `IDE_MARKDOWN_PREVIEW_MAX_LINES` (constant), lines 4990-4990, exports `IDE_MARKDOWN_PREVIEW_MAX_LINES`
- order 550: `IDE_IMAGE_PREVIEW_MAX_EDGE` (constant), lines 4991-4991, exports `IDE_IMAGE_PREVIEW_MAX_EDGE`
- order 551: `IDE_IMAGE_PREVIEW_MAX_PIXELS` (constant), lines 4992-4992, exports `IDE_IMAGE_PREVIEW_MAX_PIXELS`
- order 552: `IDE_IMAGE_PREVIEW_SOURCE_MAX_PIXELS` (constant), lines 4993-4993, exports `IDE_IMAGE_PREVIEW_SOURCE_MAX_PIXELS`
- order 553: `IDE_VECTOR_PREVIEW_MAX_BYTES` (constant), lines 4994-4994, exports `IDE_VECTOR_PREVIEW_MAX_BYTES`
- order 554: `IDE_TABLE_PREVIEW_SOURCE_MAX_BYTES` (constant), lines 4995-4995, exports `IDE_TABLE_PREVIEW_SOURCE_MAX_BYTES`
- order 555: `IDE_TABLE_PREVIEW_CELL_MAX_CHARS` (constant), lines 4996-4996, exports `IDE_TABLE_PREVIEW_CELL_MAX_CHARS`
- order 556: `IDE_TABLE_PREVIEW_TOTAL_CHARS` (constant), lines 4997-4997, exports `IDE_TABLE_PREVIEW_TOTAL_CHARS`
- order 557: `IDE_OFFICE_PREVIEW_MAX_ENTRIES` (constant), lines 4998-4998, exports `IDE_OFFICE_PREVIEW_MAX_ENTRIES`
- order 558: `IDE_OFFICE_PREVIEW_MAX_EXPANDED_BYTES` (constant), lines 4999-4999, exports `IDE_OFFICE_PREVIEW_MAX_EXPANDED_BYTES`
- order 559: `IDE_OFFICE_PREVIEW_MAX_ENTRY_BYTES` (constant), lines 5000-5000, exports `IDE_OFFICE_PREVIEW_MAX_ENTRY_BYTES`
- order 560: `IDE_COMMAND_TIMEOUT_DEFAULT` (constant), lines 5001-5001, exports `IDE_COMMAND_TIMEOUT_DEFAULT`
- order 561: `IDE_TREE_DEFAULT_MAX_NODES` (constant), lines 5002-5002, exports `IDE_TREE_DEFAULT_MAX_NODES`
- order 562: `IDE_TREE_MAX_NODES` (constant), lines 5003-5003, exports `IDE_TREE_MAX_NODES`
- order 563: `IDE_SEARCH_MAX_RESULTS` (constant), lines 5004-5004, exports `IDE_SEARCH_MAX_RESULTS`
- order 564: `IDE_SEARCH_MAX_FILE_BYTES` (constant), lines 5005-5005, exports `IDE_SEARCH_MAX_FILE_BYTES`
- order 565: `IDE_TERMINAL_SCROLLBACK_BYTES` (constant), lines 5006-5006, exports `IDE_TERMINAL_SCROLLBACK_BYTES`
- order 566: `IDE_TERMINAL_IDLE_SECONDS` (constant), lines 5007-5007, exports `IDE_TERMINAL_IDLE_SECONDS`
- order 567: `IDE_DEBUG_ADAPTER_START_ATTEMPTS` (constant), lines 5008-5008, exports `IDE_DEBUG_ADAPTER_START_ATTEMPTS`
- order 568: `IDE_DEBUG_ADAPTER_START_TIMEOUT_SECONDS` (constant), lines 5009-5009, exports `IDE_DEBUG_ADAPTER_START_TIMEOUT_SECONDS`
- order 569: `IDE_VSIX_MAX_BYTES` (constant), lines 5010-5010, exports `IDE_VSIX_MAX_BYTES`
- order 570: `IDE_VSIX_MAX_EXPANDED_BYTES` (constant), lines 5011-5011, exports `IDE_VSIX_MAX_EXPANDED_BYTES`
- order 571: `IDE_VSIX_MAX_FILES` (constant), lines 5012-5012, exports `IDE_VSIX_MAX_FILES`
- order 572: `IDE_VSIX_MAX_FILE_BYTES` (constant), lines 5013-5013, exports `IDE_VSIX_MAX_FILE_BYTES`
- order 573: `IDE_TREE_SKIP_DIRS` (constant), lines 5014-5022, exports `IDE_TREE_SKIP_DIRS`
- order 574: `RENDER_FRAME_MAX_B64_CHARS` (constant), lines 5023-5023, exports `RENDER_FRAME_MAX_B64_CHARS`
- order 575: `RENDER_FRAME_MAX_POINTS` (constant), lines 5024-5024, exports `RENDER_FRAME_MAX_POINTS`
- order 576: `RENDER_FRAME_MAX_LINES` (constant), lines 5025-5025, exports `RENDER_FRAME_MAX_LINES`
- order 577: `RENDER_FRAME_MAX_LINE_POINTS` (constant), lines 5026-5026, exports `RENDER_FRAME_MAX_LINE_POINTS`
- order 578: `RENDER_FRAME_ACTIVITY_INTERVAL_SECONDS` (constant), lines 5027-5027, exports `RENDER_FRAME_ACTIVITY_INTERVAL_SECONDS`
- order 579: `RAW_TOOLCALL_TEXT_FILTER_THRESHOLD` (constant), lines 5028-5028, exports `RAW_TOOLCALL_TEXT_FILTER_THRESHOLD`
- order 580: `ASSISTANT_TEXT_PERSIST_MAX_CHARS` (constant), lines 5029-5029, exports `ASSISTANT_TEXT_PERSIST_MAX_CHARS`
- order 581: `ASSISTANT_MESSAGE_EVENT_MAX_CHARS` (constant), lines 5030-5030, exports `ASSISTANT_MESSAGE_EVENT_MAX_CHARS`
- order 582: `CODE_PREVIEW_EXTS` (constant), lines 5031-5158, exports `CODE_PREVIEW_EXTS`
- order 583: `CODE_PREVIEW_FILENAMES` (constant), lines 5159-5210, exports `CODE_PREVIEW_FILENAMES`
- order 584: `MEDIA_CAPABILITY_KEYS` (constant), lines 5211-5218, exports `MEDIA_CAPABILITY_KEYS`
- order 588: `OFFLINE_JS_LIB_CATALOG` (constant), lines 5251-5577, exports `OFFLINE_JS_LIB_CATALOG`
- order 589: `OFFLINE_JS_ASSET_LOCK` (constant), lines 5578-5578, exports `OFFLINE_JS_ASSET_LOCK`
- order 590: `OFFLINE_JS_LIB_INDEX_FILE` (constant), lines 5579-5579, exports `OFFLINE_JS_LIB_INDEX_FILE`
- order 591: `OFFLINE_JS_LIB_README_FILE` (constant), lines 5580-5580, exports `OFFLINE_JS_LIB_README_FILE`
- order 601: `BACKEND_I18N` (constant), lines 5774-5845, exports `BACKEND_I18N`
- order 602: `_call_backend_i18n_en_update_5847` (expression), lines 5846-5947, exports —
- order 603: `_call_backend_i18n_zh_cn_update_5948` (expression), lines 5948-6048, exports —
- order 604: `_call_backend_i18n_zh_tw_update_6049` (expression), lines 6049-6149, exports —
- order 605: `_call_backend_i18n_ja_update_6150` (expression), lines 6150-6250, exports —
- order 836: `TABULAR_PREVIEW_EXTS` (constant), lines 14908-14910, exports `TABULAR_PREVIEW_EXTS`
- order 837: `EXCEL_PREVIEW_EXTS` (constant), lines 14911-14911, exports `EXCEL_PREVIEW_EXTS`
- order 838: `PRESENTATION_PREVIEW_EXTS` (constant), lines 14912-14912, exports `PRESENTATION_PREVIEW_EXTS`
- order 839: `DOCUMENT_PREVIEW_EXTS` (constant), lines 14913-14913, exports `DOCUMENT_PREVIEW_EXTS`
- order 1041: `STUDIO_DEVICE_COOKIE` (constant), lines 106551-106568, exports `STUDIO_DEVICE_COOKIE`
- order 1042: `STUDIO_SESSION_COOKIE` (constant), lines 106569-106569, exports `STUDIO_SESSION_COOKIE`
- order 1043: `STUDIO_DEVICE_TTL` (constant), lines 106570-106570, exports `STUDIO_DEVICE_TTL`
- order 1044: `STUDIO_SESSION_TTL` (constant), lines 106571-106571, exports `STUDIO_SESSION_TTL`
- order 1045: `STUDIO_MAX_FILE_BYTES` (constant), lines 106572-106572, exports `STUDIO_MAX_FILE_BYTES`
- order 1046: `STUDIO_MAX_PROJECT_BYTES` (constant), lines 106573-106573, exports `STUDIO_MAX_PROJECT_BYTES`
- order 1047: `STUDIO_MAX_FILES` (constant), lines 106574-106574, exports `STUDIO_MAX_FILES`
- order 1048: `STUDIO_MAX_JOB_SECONDS` (constant), lines 106575-106575, exports `STUDIO_MAX_JOB_SECONDS`
- order 1054: `STUDIO_INDEX_HTML` (constant), lines 108475-108477, exports `STUDIO_INDEX_HTML`
- order 1055: `STUDIO_CSS` (constant), lines 108478-108478, exports `STUDIO_CSS`
- order 1056: `STUDIO_JS` (constant), lines 108479-108479, exports `STUDIO_JS`

### `config/paths.py`

- order 112: `SCRIPT_DIR` (constant), lines 3467-3467, exports `SCRIPT_DIR`
- order 137: `_resolve_default_agent_workdir` (function), lines 3561-3570, exports `_resolve_default_agent_workdir`
- order 138: `_is_installed_python_runtime` (function), lines 3571-3574, exports `_is_installed_python_runtime`
- order 139: `_runtime_storage_mode` (function), lines 3575-3581, exports `_runtime_storage_mode`
- order 140: `_runtime_tree_has_content` (function), lines 3582-3587, exports `_runtime_tree_has_content`
- order 141: `_copy_runtime_tree_with_crypto_migration` (function), lines 3588-3653, exports `_copy_runtime_tree_with_crypto_migration`
- order 142: `_merge_legacy_codes_root` (function), lines 3654-3719, exports `_merge_legacy_codes_root`
- order 143: `_migrate_legacy_runtime_roots` (function), lines 3720-3810, exports `_migrate_legacy_runtime_roots`
- order 144: `WORKDIR` (constant), lines 3811-3812, exports `WORKDIR`
- order 145: `CODES_ROOT` (constant), lines 3813-3813, exports `CODES_ROOT`
- order 146: `LLM_CONFIG_PATH` (constant), lines 3814-3814, exports `LLM_CONFIG_PATH`
- order 683: `detect_repo_root` (function), lines 7695-7709, exports `detect_repo_root`
- order 684: `REPO_ROOT` (constant), lines 7710-7711, exports `REPO_ROOT`

### `config/settings.py`

- order 595: `normalize_ui_language` (function), lines 5662-5686, exports `normalize_ui_language`
- order 596: `normalize_ui_style` (function), lines 5687-5706, exports `normalize_ui_style`
- order 597: `supported_ui_languages_payload` (function), lines 5707-5710, exports `supported_ui_languages_payload`
- order 598: `agent_language_preference_payload` (function), lines 5711-5720, exports `agent_language_preference_payload`
- order 599: `normalize_execution_mode` (function), lines 5721-5742, exports `normalize_execution_mode`
- order 600: `model_language_instruction` (function), lines 5743-5773, exports `model_language_instruction`
- order 606: `backend_i18n_text` (function), lines 6251-6263, exports `backend_i18n_text`
- order 607: `backend_role_label` (function), lines 6264-6270, exports `backend_role_label`
- order 608: `_detect_os_shell_instruction` (function), lines 6271-6312, exports `_detect_os_shell_instruction`
- order 609: `resolve_web_ui_dir_path` (function), lines 6313-6321, exports `resolve_web_ui_dir_path`
- order 610: `resolve_optional_file_path` (function), lines 6322-6331, exports `resolve_optional_file_path`
- order 611: `resolve_skills_root_path` (function), lines 6332-6341, exports `resolve_skills_root_path`
- order 612: `_count_skill_markdown_files` (function), lines 6342-6355, exports `_count_skill_markdown_files`
- order 613: `select_preferred_skills_root` (function), lines 6356-6392, exports `select_preferred_skills_root`
- order 614: `load_web_ui_config_file` (function), lines 6393-6409, exports `load_web_ui_config_file`
- order 615: `extract_show_upload_list_setting` (function), lines 6410-6426, exports `extract_show_upload_list_setting`
- order 616: `extract_ui_style_setting` (function), lines 6427-6443, exports `extract_ui_style_setting`
- order 617: `extract_js_lib_download_setting` (function), lines 6444-6465, exports `extract_js_lib_download_setting`
- order 618: `extract_daily_session_limit_setting` (function), lines 6466-6511, exports `extract_daily_session_limit_setting`
- order 619: `extract_shell_command_timeout_setting` (function), lines 6512-6560, exports `extract_shell_command_timeout_setting`
- order 620: `normalize_shell_timeout_mode` (function), lines 6561-6578, exports `normalize_shell_timeout_mode`
- order 621: `extract_shell_timeout_mode_setting` (function), lines 6579-6591, exports `extract_shell_timeout_mode_setting`
- order 622: `extract_shell_async_handoff_setting` (function), lines 6592-6619, exports `extract_shell_async_handoff_setting`
- order 623: `extract_context_token_limit_setting` (function), lines 6620-6654, exports `extract_context_token_limit_setting`
- order 624: `normalize_auto_task_level_ceiling` (function), lines 6655-6676, exports `normalize_auto_task_level_ceiling`
- order 625: `normalize_l2_todo_policy` (function), lines 6677-6712, exports `normalize_l2_todo_policy`
- order 626: `extract_l2_todo_policy_setting` (function), lines 6713-6755, exports `extract_l2_todo_policy_setting`
- order 627: `extract_auto_task_level_ceiling_setting` (function), lines 6756-6785, exports `extract_auto_task_level_ceiling_setting`
- order 628: `normalize_read_context_policy` (function), lines 6786-6806, exports `normalize_read_context_policy`
- order 629: `normalize_tool_memory_policy` (function), lines 6807-6810, exports `normalize_tool_memory_policy`
- order 630: `extract_read_context_policy_setting` (function), lines 6811-6834, exports `extract_read_context_policy_setting`
- order 631: `extract_tool_memory_policy_setting` (function), lines 6835-6858, exports `extract_tool_memory_policy_setting`
- order 633: `default_multimodal_capabilities` (function), lines 6865-6875, exports `default_multimodal_capabilities`
- order 634: `_to_bool_like` (function), lines 6876-6888, exports `_to_bool_like`
- order 635: `extract_web_search_enabled_setting` (function), lines 6889-6901, exports `extract_web_search_enabled_setting`
- order 636: `_single_no_plan_todo_setting_sections` (function), lines 6902-6928, exports `_single_no_plan_todo_setting_sections`
- order 637: `_single_no_plan_todo_setting_present` (function), lines 6929-6954, exports `_single_no_plan_todo_setting_present`
- order 638: `extract_single_no_plan_todo_settings` (function), lines 6955-7001, exports `extract_single_no_plan_todo_settings`
- order 639: `normalize_user_memory_mode` (function), lines 7002-7032, exports `normalize_user_memory_mode`
- order 640: `user_memory_enabled_from_mode` (function), lines 7033-7036, exports `user_memory_enabled_from_mode`
- order 641: `extract_user_memory_mode_setting` (function), lines 7037-7076, exports `extract_user_memory_mode_setting`
- order 642: `set_web_search_enabled_on_runtime` (function), lines 7077-7092, exports `set_web_search_enabled_on_runtime`
- order 643: `infer_model_multimodal_capabilities` (function), lines 7093-7139, exports `infer_model_multimodal_capabilities`
- order 644: `parse_capability_overrides` (function), lines 7140-7179, exports `parse_capability_overrides`
- order 645: `merge_multimodal_capabilities` (function), lines 7180-7189, exports `merge_multimodal_capabilities`
- order 646: `parse_media_endpoints` (function), lines 7190-7206, exports `parse_media_endpoints`
- order 662: `extract_runtime_region_hint_setting` (function), lines 7384-7409, exports `extract_runtime_region_hint_setting`
- order 663: `extract_runtime_timezone_hint_setting` (function), lines 7410-7427, exports `extract_runtime_timezone_hint_setting`
- order 664: `runtime_environment_context_snapshot` (function), lines 7428-7477, exports `runtime_environment_context_snapshot`
- order 665: `runtime_environment_context_block` (function), lines 7478-7507, exports `runtime_environment_context_block`
- order 701: `load_offline_js_lib_index` (function), lines 7982-7992, exports `load_offline_js_lib_index`
- order 755: `resolve_ollama_model` (function), lines 11277-11288, exports `resolve_ollama_model`
- order 756: `infer_thinking_model` (function), lines 11289-11292, exports `infer_thinking_model`
- order 767: `extract_base_url` (function), lines 11502-11511, exports `extract_base_url`
- order 769: `infer_user_complexity_value` (function), lines 11523-11540, exports `infer_user_complexity_value`
- order 770: `normalize_task_complexity` (function), lines 11541-11570, exports `normalize_task_complexity`
- order 771: `task_complexity_rank` (function), lines 11571-11573, exports `task_complexity_rank`
- order 772: `task_complexity_at_least` (function), lines 11574-11576, exports `task_complexity_at_least`
- order 773: `max_task_complexity` (function), lines 11577-11587, exports `max_task_complexity`
- order 774: `normalize_openai_compat_provider_name` (function), lines 11588-11604, exports `normalize_openai_compat_provider_name`
- order 794: `resolve_reasoning_payload` (function), lines 11726-11776, exports `resolve_reasoning_payload`
- order 797: `extract_openai_compat_model_ids` (function), lines 11824-11858, exports `extract_openai_compat_model_ids`
- order 800: `load_llm_config_from_source` (function), lines 11891-11926, exports `load_llm_config_from_source`
- order 801: `parse_llm_config_profiles` (function), lines 11927-12557, exports `parse_llm_config_profiles`
- order 802: `looks_like_llm_config` (function), lines 12558-12635, exports `looks_like_llm_config`
- order 806: `parse_front_matter` (function), lines 12796-13024, exports `parse_front_matter`

### `ide/assets.py`

- order 1033: `IDE_INDEX_HTML` (constant), lines 105510-105665, exports `IDE_INDEX_HTML`
- order 1034: `IDE_CSS` (constant), lines 105666-105705, exports `IDE_CSS`
- order 1035: `IDE_JS` (constant), lines 105706-105899, exports `IDE_JS`
- order 1036: `IDE_CSS` (constant), lines 105900-105906, exports `IDE_CSS`
- order 1037: `IDE_JS` (constant), lines 105907-106143, exports `IDE_JS`
- order 1038: `IDE_JS` (constant), lines 106144-106271, exports `IDE_JS`
- order 1039: `IDE_JS` (constant), lines 106272-106453, exports `IDE_JS`
- order 1040: `IDE_JS` (constant), lines 106454-106550, exports `IDE_JS`

### `ide/auth.py`

- order 814: `IDEAuthError` (class), lines 13392-13399, exports `IDEAuthError`
- order 815: `IDEAuthStore` (class), lines 13400-14121, exports `IDEAuthStore`

### `ide/errors.py`

- order 816: `IDECapabilityError` (class), lines 14122-14128, exports `IDECapabilityError`
- order 817: `IDEFileConflict` (class), lines 14129-14136, exports `IDEFileConflict`

### `ide/events.py`

- order 711: `ide_public_operation_data` (function), lines 8319-8365, exports `ide_public_operation_data`

### `ide/handler.py`

- order 1070: `IdeHandler` (class), lines 122415-123889, exports `IdeHandler`

### `ide/preview.py`

- order 834: `normalize_rel_preview_path` (function), lines 14883-14896, exports `normalize_rel_preview_path`
- order 835: `is_code_preview_candidate` (function), lines 14897-14907, exports `is_code_preview_candidate`
- order 840: `preview_kind_for_path` (function), lines 14914-14943, exports `preview_kind_for_path`
- order 841: `normalize_markdown_preview_text` (function), lines 14944-14977, exports `normalize_markdown_preview_text`
- order 842: `_preview_markdown_value_html` (function), lines 14978-14998, exports `_preview_markdown_value_html`
- order 843: `_preview_markdown_frontmatter_html` (function), lines 14999-15014, exports `_preview_markdown_frontmatter_html`
- order 844: `_preview_markdown_task_lists` (function), lines 15015-15028, exports `_preview_markdown_task_lists`
- order 845: `_preview_markdown_fallback_inline` (function), lines 15029-15070, exports `_preview_markdown_fallback_inline`
- order 846: `_preview_markdown_fallback_html` (function), lines 15071-15167, exports `_preview_markdown_fallback_html`
- order 849: `workspace_file_revision_map` (function), lines 15208-15232, exports `workspace_file_revision_map`
- order 850: `workspace_revision_delta` (function), lines 15233-15239, exports `workspace_revision_delta`
- order 851: `build_code_preview_rows` (function), lines 15240-15288, exports `build_code_preview_rows`

### `ide/sandbox.py`

- order 670: `_windows_subprocess_encodings` (function), lines 7533-7550, exports `_windows_subprocess_encodings`
- order 934: `_IDE_SANDBOX_BACKEND_CACHE` (assignment), lines 27220-27228, exports `_IDE_SANDBOX_BACKEND_CACHE`
- order 935: `_IDE_SANDBOX_BACKEND_LOCK` (assignment), lines 27229-27229, exports `_IDE_SANDBOX_BACKEND_LOCK`
- order 936: `WINDOWS_JOB_SANDBOX_MARKER` (constant), lines 27230-27230, exports `WINDOWS_JOB_SANDBOX_MARKER`
- order 937: `_WINDOWS_LOW_INTEGRITY_ROOTS` (assignment), lines 27231-27231, exports `_WINDOWS_LOW_INTEGRITY_ROOTS`
- order 938: `_WINDOWS_LOW_INTEGRITY_FAILED_ROOTS` (assignment), lines 27232-27232, exports `_WINDOWS_LOW_INTEGRITY_FAILED_ROOTS`
- order 939: `_WINDOWS_LOW_INTEGRITY_LOCK` (assignment), lines 27233-27233, exports `_WINDOWS_LOW_INTEGRITY_LOCK`
- order 940: `_is_windows_job_sandbox_prefix` (function), lines 27234-27240, exports `_is_windows_job_sandbox_prefix`
- order 941: `_windows_builtin_sandbox_probe` (function), lines 27241-27264, exports `_windows_builtin_sandbox_probe`
- order 942: `_windows_last_error` (function), lines 27265-27272, exports `_windows_last_error`
- order 943: `_windows_set_integrity_label` (function), lines 27273-27326, exports `_windows_set_integrity_label`
- order 944: `_windows_set_low_integrity_label` (function), lines 27327-27329, exports `_windows_set_low_integrity_label`
- order 945: `_windows_protect_application_snapshot` (function), lines 27330-27353, exports `_windows_protect_application_snapshot`
- order 946: `_windows_prepare_low_integrity_workspace` (function), lines 27354-27391, exports `_windows_prepare_low_integrity_workspace`
- order 947: `_windows_job_memory_limit` (function), lines 27392-27399, exports `_windows_job_memory_limit`
- order 948: `_windows_lower_process_integrity` (function), lines 27400-27447, exports `_windows_lower_process_integrity`
- order 949: `_windows_attach_sandbox_job` (function), lines 27448-27540, exports `_windows_attach_sandbox_job`
- order 950: `_windows_close_sandbox_job` (function), lines 27541-27557, exports `_windows_close_sandbox_job`
- order 951: `_popen_windows_sandboxed` (function), lines 27558-27589, exports `_popen_windows_sandboxed`
- order 952: `_run_windows_sandboxed_command` (function), lines 27590-27643, exports `_run_windows_sandboxed_command`
- order 953: `_detect_ide_sandbox_backend` (function), lines 27644-27748, exports `_detect_ide_sandbox_backend`

### `llm/client.py`

- order 919: `OllamaError` (class), lines 24176-24198, exports `OllamaError`
- order 920: `OllamaClient` (class), lines 24199-26514, exports `OllamaClient`

### `llm/constants.py`

- order 110: `DEFAULT_OLLAMA_BASE_URL` (constant), lines 3465-3465, exports `DEFAULT_OLLAMA_BASE_URL`
- order 111: `DEFAULT_OLLAMA_MODEL` (constant), lines 3466-3466, exports `DEFAULT_OLLAMA_MODEL`
- order 775: `OPENAI_COMPAT_PROVIDER_NAMES` (constant), lines 11605-11614, exports `OPENAI_COMPAT_PROVIDER_NAMES`
- order 776: `OPENAI_LIKE_PROVIDER_NAMES` (constant), lines 11615-11616, exports `OPENAI_LIKE_PROVIDER_NAMES`
- order 779: `EFFORT_OFF` (constant), lines 11623-11634, exports `EFFORT_OFF`
- order 780: `EFFORT_LOW` (constant), lines 11635-11635, exports `EFFORT_LOW`
- order 781: `EFFORT_MEDIUM` (constant), lines 11636-11636, exports `EFFORT_MEDIUM`
- order 782: `EFFORT_HIGH` (constant), lines 11637-11637, exports `EFFORT_HIGH`
- order 783: `EFFORT_MAX` (constant), lines 11638-11638, exports `EFFORT_MAX`
- order 784: `EFFORT_LEVELS` (constant), lines 11639-11639, exports `EFFORT_LEVELS`
- order 785: `EFFORT_ORDER` (constant), lines 11640-11640, exports `EFFORT_ORDER`
- order 786: `EFFORT_DEFAULT` (constant), lines 11641-11641, exports `EFFORT_DEFAULT`
- order 787: `EFFORT_ANTHROPIC_BUDGET` (constant), lines 11642-11649, exports `EFFORT_ANTHROPIC_BUDGET`
- order 788: `EFFORT_OPENAI_REASONING` (constant), lines 11650-11656, exports `EFFORT_OPENAI_REASONING`
- order 789: `TASK_LEVEL_EFFORT` (constant), lines 11657-11666, exports `TASK_LEVEL_EFFORT`
- order 790: `ROLE_EFFORT_FLOOR` (constant), lines 11667-11672, exports `ROLE_EFFORT_FLOOR`
- order 791: `COORDINATION_EFFORT` (constant), lines 11673-11676, exports `COORDINATION_EFFORT`

### `llm/utils.py`

- order 748: `probe_ollama_environment` (function), lines 11208-11222, exports `probe_ollama_environment`
- order 749: `list_ollama_models` (function), lines 11223-11226, exports `list_ollama_models`
- order 750: `_OLLAMA_TAG_CACHE_LOCK` (assignment), lines 11227-11228, exports `_OLLAMA_TAG_CACHE_LOCK`
- order 751: `_OLLAMA_TAG_CACHE` (assignment), lines 11229-11229, exports `_OLLAMA_TAG_CACHE`
- order 754: `list_ollama_models_cached` (function), lines 11238-11276, exports `list_ollama_models_cached`
- order 757: `split_thinking_content` (function), lines 11293-11337, exports `split_thinking_content`
- order 758: `strip_thinking_content` (function), lines 11338-11340, exports `strip_thinking_content`
- order 759: `check_ollama_model_ready` (function), lines 11341-11366, exports `check_ollama_model_ready`
- order 760: `list_loaded_ollama_models` (function), lines 11367-11381, exports `list_loaded_ollama_models`
- order 761: `wake_ollama_model` (function), lines 11382-11413, exports `wake_ollama_model`
- order 762: `try_pull_ollama_model` (function), lines 11414-11432, exports `try_pull_ollama_model`
- order 763: `ordered_model_candidates` (function), lines 11433-11452, exports `ordered_model_candidates`
- order 764: `pick_working_ollama_model` (function), lines 11453-11470, exports `pick_working_ollama_model`
- order 768: `complete_chat_endpoint` (function), lines 11512-11522, exports `complete_chat_endpoint`
- order 777: `is_openai_compat_provider` (function), lines 11617-11619, exports `is_openai_compat_provider`
- order 778: `is_openai_like_provider` (function), lines 11620-11622, exports `is_openai_like_provider`
- order 792: `clamp_effort` (function), lines 11677-11688, exports `clamp_effort`
- order 793: `model_reasoning_style` (function), lines 11689-11725, exports `model_reasoning_style`
- order 795: `openai_compat_probe_headers` (function), lines 11777-11789, exports `openai_compat_probe_headers`
- order 796: `openai_compat_model_list_urls` (function), lines 11790-11823, exports `openai_compat_model_list_urls`
- order 798: `_is_http_url` (function), lines 11859-11872, exports `_is_http_url`
- order 799: `_resolve_local_path` (function), lines 11873-11890, exports `_resolve_local_path`

### `mcp/constants.py`

- order 164: `MCP_SERVICE_PORT_OFFSET` (constant), lines 3832-3832, exports `MCP_SERVICE_PORT_OFFSET`
- order 899: `MCP_PROTOCOL_VERSION` (constant), lines 22794-22823, exports `MCP_PROTOCOL_VERSION`
- order 900: `MCP_NAME_RE` (constant), lines 22824-22824, exports `MCP_NAME_RE`
- order 901: `MCP_TOOL_PREFIX` (constant), lines 22825-22825, exports `MCP_TOOL_PREFIX`
- order 902: `_MCP_DEFAULT_HANDSHAKE_TIMEOUT` (assignment), lines 22826-22826, exports `_MCP_DEFAULT_HANDSHAKE_TIMEOUT`
- order 903: `_MCP_DEFAULT_CALL_TIMEOUT` (assignment), lines 22827-22827, exports `_MCP_DEFAULT_CALL_TIMEOUT`
- order 904: `_MCP_MAX_RESULT_CHARS` (assignment), lines 22828-22828, exports `_MCP_MAX_RESULT_CHARS`
- order 905: `_MCP_TRUST_STORE_VERSION` (assignment), lines 22829-22829, exports `_MCP_TRUST_STORE_VERSION`

### `mcp/driver.py`

- order 906: `mcp_normalize_name` (function), lines 22830-22839, exports `mcp_normalize_name`
- order 907: `mcp_normalize_server_configs` (function), lines 22840-22924, exports `mcp_normalize_server_configs`
- order 908: `mcp_extract_server_configs` (function), lines 22925-22944, exports `mcp_extract_server_configs`
- order 909: `_mcp_sha256_file` (function), lines 22945-22955, exports `_mcp_sha256_file`
- order 910: `_mcp_file_identity` (function), lines 22956-22973, exports `_mcp_file_identity`
- order 911: `mcp_workspace_identity` (function), lines 22974-22992, exports `mcp_workspace_identity`
- order 912: `mcp_config_file_digest` (function), lines 22993-23000, exports `mcp_config_file_digest`
- order 913: `mcp_default_trust_store_path` (function), lines 23001-23035, exports `mcp_default_trust_store_path`
- order 914: `mcp_record_definition_fingerprint` (function), lines 23036-23050, exports `mcp_record_definition_fingerprint`
- order 915: `_mcp_effective_spawn` (function), lines 23051-23138, exports `_mcp_effective_spawn`
- order 916: `MCPWorkspaceTrustStore` (class), lines 23139-23200, exports `MCPWorkspaceTrustStore`
- order 917: `MCPServerProcess` (class), lines 23201-23556, exports `MCPServerProcess`
- order 918: `MCPManager` (class), lines 23557-24175, exports `MCPManager`

### `mcp/service.py`

- order 1072: `McpServiceHandler` (class), lines 124361-124578, exports `McpServiceHandler`

### `rag/assets.py`

- order 1027: `RAG_ADMIN_INDEX_HTML` (constant), lines 102903-103135, exports `RAG_ADMIN_INDEX_HTML`
- order 1028: `RAG_ADMIN_CSS` (constant), lines 103136-103239, exports `RAG_ADMIN_CSS`
- order 1029: `RAG_ADMIN_JS` (constant), lines 103240-105460, exports `RAG_ADMIN_JS`
- order 1030: `CODE_ADMIN_INDEX_HTML` (constant), lines 105461-105473, exports `CODE_ADMIN_INDEX_HTML`
- order 1031: `CODE_ADMIN_CSS` (constant), lines 105474-105504, exports `CODE_ADMIN_CSS`
- order 1032: `CODE_ADMIN_JS` (constant), lines 105505-105509, exports `CODE_ADMIN_JS`

### `rag/constants.py`

- order 160: `RAG_LIBRARY_DIRNAME` (constant), lines 3828-3828, exports `RAG_LIBRARY_DIRNAME`
- order 161: `RAG_ADMIN_PORT_OFFSET` (constant), lines 3829-3829, exports `RAG_ADMIN_PORT_OFFSET`
- order 162: `CODE_LIBRARY_DIRNAME` (constant), lines 3830-3830, exports `CODE_LIBRARY_DIRNAME`
- order 168: `WEB_SEARCH_INDEX_DIRNAME` (constant), lines 3839-3839, exports `WEB_SEARCH_INDEX_DIRNAME`
- order 170: `USER_MEMORY_DIRNAME` (constant), lines 3841-3841, exports `USER_MEMORY_DIRNAME`
- order 171: `USER_MEMORY_DB_FILENAME` (constant), lines 3842-3842, exports `USER_MEMORY_DB_FILENAME`
- order 172: `USER_MEMORY_PROFILE_FILENAME` (constant), lines 3843-3843, exports `USER_MEMORY_PROFILE_FILENAME`
- order 173: `USER_MEMORY_MODE_CHOICES` (constant), lines 3844-3844, exports `USER_MEMORY_MODE_CHOICES`
- order 175: `USER_MEMORY_WEAK_CAPSULE_CHARS` (constant), lines 3846-3846, exports `USER_MEMORY_WEAK_CAPSULE_CHARS`
- order 176: `USER_MEMORY_ON_CAPSULE_CHARS` (constant), lines 3847-3847, exports `USER_MEMORY_ON_CAPSULE_CHARS`
- order 177: `USER_MEMORY_CAPSULE_INJECT_CHARS` (constant), lines 3848-3851, exports `USER_MEMORY_CAPSULE_INJECT_CHARS`
- order 178: `USER_MEMORY_MAX_SUMMARY_CHARS` (constant), lines 3852-3852, exports `USER_MEMORY_MAX_SUMMARY_CHARS`
- order 179: `USER_MEMORY_QUERY_LIMIT` (constant), lines 3853-3853, exports `USER_MEMORY_QUERY_LIMIT`
- order 180: `USER_MEMORY_DECAY_HALFLIFE_DAYS` (constant), lines 3854-3854, exports `USER_MEMORY_DECAY_HALFLIFE_DAYS`
- order 181: `USER_MEMORY_PROFILE_SCHEMA_VERSION` (constant), lines 3855-3855, exports `USER_MEMORY_PROFILE_SCHEMA_VERSION`
- order 201: `WEB_SEARCH_CONTEXT_REGISTRY_MAX` (constant), lines 3877-3877, exports `WEB_SEARCH_CONTEXT_REGISTRY_MAX`
- order 202: `WEB_SEARCH_CONTEXT_PROMPT_MAX_ITEMS` (constant), lines 3878-3878, exports `WEB_SEARCH_CONTEXT_PROMPT_MAX_ITEMS`
- order 203: `WEB_SEARCH_CONTEXT_PROMPT_MAX_CHARS` (constant), lines 3879-3879, exports `WEB_SEARCH_CONTEXT_PROMPT_MAX_CHARS`
- order 204: `WEB_SEARCH_CONTEXT_NODE_MAX` (constant), lines 3880-3880, exports `WEB_SEARCH_CONTEXT_NODE_MAX`
- order 205: `WEB_SEARCH_CONTEXT_URL_MAX` (constant), lines 3881-3881, exports `WEB_SEARCH_CONTEXT_URL_MAX`
- order 206: `RAG_CHUNK_CHARS` (constant), lines 3882-3882, exports `RAG_CHUNK_CHARS`
- order 207: `RAG_CHUNK_OVERLAP` (constant), lines 3883-3883, exports `RAG_CHUNK_OVERLAP`
- order 208: `RAG_MAX_CHUNKS_PER_DOC` (constant), lines 3884-3886, exports `RAG_MAX_CHUNKS_PER_DOC`
- order 209: `RAG_MAX_DOCUMENT_CHARS` (constant), lines 3887-3897, exports `RAG_MAX_DOCUMENT_CHARS`
- order 213: `RAG_MAX_QUERY_RESULTS` (constant), lines 3901-3901, exports `RAG_MAX_QUERY_RESULTS`
- order 214: `RAG_HIGH_RECALL_POOL_MULTIPLIER` (constant), lines 3902-3902, exports `RAG_HIGH_RECALL_POOL_MULTIPLIER`
- order 215: `RAG_HIGH_RECALL_MIN_POOL` (constant), lines 3903-3903, exports `RAG_HIGH_RECALL_MIN_POOL`
- order 216: `RAG_RETRIEVAL_MAX_PER_DOC` (constant), lines 3904-3904, exports `RAG_RETRIEVAL_MAX_PER_DOC`
- order 217: `RAG_BM25_K1` (constant), lines 3905-3908, exports `RAG_BM25_K1`
- order 218: `RAG_BM25_B` (constant), lines 3909-3909, exports `RAG_BM25_B`
- order 219: `RAG_BM25_SATURATION` (constant), lines 3910-3916, exports `RAG_BM25_SATURATION`
- order 220: `RAG_SYMBOL_EXACT_BOOST` (constant), lines 3917-3920, exports `RAG_SYMBOL_EXACT_BOOST`
- order 221: `RAG_INDEX_SNAPSHOT_FORMAT` (constant), lines 3921-3924, exports `RAG_INDEX_SNAPSHOT_FORMAT`
- order 222: `RAG_GRAPH_MAX_NODES` (constant), lines 3925-3925, exports `RAG_GRAPH_MAX_NODES`
- order 223: `RAG_TASK_HISTORY_LIMIT` (constant), lines 3926-3926, exports `RAG_TASK_HISTORY_LIMIT`
- order 224: `RAG_MODEL_MEDIA_MAX_BYTES` (constant), lines 3927-3927, exports `RAG_MODEL_MEDIA_MAX_BYTES`
- order 225: `RAG_MAX_IMPORT_FILES` (constant), lines 3928-3928, exports `RAG_MAX_IMPORT_FILES`
- order 226: `RAG_MAX_IMPORT_BATCH_ITEMS` (constant), lines 3929-3929, exports `RAG_MAX_IMPORT_BATCH_ITEMS`
- order 227: `RAG_MAX_IMPORT_BATCH_BYTES` (constant), lines 3930-3930, exports `RAG_MAX_IMPORT_BATCH_BYTES`
- order 228: `RAG_PDF_IMAGE_LIMIT` (constant), lines 3931-3931, exports `RAG_PDF_IMAGE_LIMIT`
- order 229: `RAG_QUERY_CONTEXT_CHARS` (constant), lines 3932-3932, exports `RAG_QUERY_CONTEXT_CHARS`
- order 230: `RAG_MAX_GLOBAL_COMMUNITIES` (constant), lines 3933-3933, exports `RAG_MAX_GLOBAL_COMMUNITIES`
- order 231: `RAG_MAX_COMMUNITY_MAP_SUPPORT` (constant), lines 3934-3934, exports `RAG_MAX_COMMUNITY_MAP_SUPPORT`
- order 232: `RAG_INCLUDE_FILENAME_ENTITIES_DEFAULT` (constant), lines 3935-3935, exports `RAG_INCLUDE_FILENAME_ENTITIES_DEFAULT`
- order 233: `RAG_DYNAMIC_NOISE_MIN_DOC_FREQ` (constant), lines 3936-3936, exports `RAG_DYNAMIC_NOISE_MIN_DOC_FREQ`
- order 234: `RAG_DYNAMIC_NOISE_MIN_COMMUNITY_FREQ` (constant), lines 3937-3937, exports `RAG_DYNAMIC_NOISE_MIN_COMMUNITY_FREQ`
- order 235: `RAG_DYNAMIC_NOISE_SOFT_DOC_RATIO` (constant), lines 3938-3938, exports `RAG_DYNAMIC_NOISE_SOFT_DOC_RATIO`
- order 236: `RAG_DYNAMIC_NOISE_HARD_DOC_RATIO` (constant), lines 3939-3939, exports `RAG_DYNAMIC_NOISE_HARD_DOC_RATIO`
- order 237: `RAG_DYNAMIC_NOISE_SOFT_COMMUNITY_RATIO` (constant), lines 3940-3940, exports `RAG_DYNAMIC_NOISE_SOFT_COMMUNITY_RATIO`
- order 238: `RAG_DYNAMIC_NOISE_HARD_COMMUNITY_RATIO` (constant), lines 3941-3941, exports `RAG_DYNAMIC_NOISE_HARD_COMMUNITY_RATIO`
- order 239: `RAG_MIN_SYNTHESIS_SCORE` (constant), lines 3942-3942, exports `RAG_MIN_SYNTHESIS_SCORE`
- order 240: `RAG_NO_EVIDENCE_THRESHOLD` (constant), lines 3943-3943, exports `RAG_NO_EVIDENCE_THRESHOLD`
- order 241: `RAG_WEAK_MATCH_SCORE_CAP` (constant), lines 3944-3944, exports `RAG_WEAK_MATCH_SCORE_CAP`
- order 242: `RAG_SYNTHESIS_MAX_PER_DOC` (constant), lines 3945-3945, exports `RAG_SYNTHESIS_MAX_PER_DOC`
- order 243: `RAG_WORKFLOW_ACCEPT_SCORE` (constant), lines 3946-3946, exports `RAG_WORKFLOW_ACCEPT_SCORE`
- order 244: `RAG_NO_EVIDENCE_MESSAGE` (constant), lines 3947-3947, exports `RAG_NO_EVIDENCE_MESSAGE`
- order 245: `RAG_CONTEXT_BUDGETS` (constant), lines 3948-3952, exports `RAG_CONTEXT_BUDGETS`
- order 246: `RAG_WEAK_EVIDENCE_MESSAGE` (constant), lines 3953-3953, exports `RAG_WEAK_EVIDENCE_MESSAGE`
- order 247: `RAG_DENSE_DEFAULT_ENABLED` (constant), lines 3954-3954, exports `RAG_DENSE_DEFAULT_ENABLED`
- order 248: `RAG_EMBEDDING_MODE_VALUES` (constant), lines 3955-3955, exports `RAG_EMBEDDING_MODE_VALUES`
- order 249: `RAG_IMPORT_WORKER_COUNT` (constant), lines 3956-3959, exports `RAG_IMPORT_WORKER_COUNT`
- order 251: `RAG_PARSE_TIMEOUT_SECONDS` (constant), lines 3964-3967, exports `RAG_PARSE_TIMEOUT_SECONDS`
- order 966: `RAG_TERM_GROUPS` (constant), lines 90298-94931, exports `RAG_TERM_GROUPS`
- order 967: `RAG_RESEARCH_HINTS` (constant), lines 94932-94953, exports `RAG_RESEARCH_HINTS`
- order 968: `RAG_CODE_HINTS` (constant), lines 94954-94964, exports `RAG_CODE_HINTS`
- order 969: `RAG_SHORT_TOKEN_ALLOWLIST` (constant), lines 94965-94980, exports `RAG_SHORT_TOKEN_ALLOWLIST`
- order 970: `RAG_EN_STOPWORDS` (constant), lines 94981-95053, exports `RAG_EN_STOPWORDS`
- order 971: `RAG_ZH_STOPWORDS` (constant), lines 95054-95090, exports `RAG_ZH_STOPWORDS`
- order 972: `RAG_GENERIC_ENTITY_TERMS_EN` (constant), lines 95091-95169, exports `RAG_GENERIC_ENTITY_TERMS_EN`
- order 973: `RAG_GENERIC_ENTITY_TERMS_ZH` (constant), lines 95170-95212, exports `RAG_GENERIC_ENTITY_TERMS_ZH`
- order 974: `RAG_STRUCTURAL_ENTITY_PATTERNS` (constant), lines 95213-95231, exports `RAG_STRUCTURAL_ENTITY_PATTERNS`
- order 999: `CODE_LIBRARY_IGNORED_DIRS` (constant), lines 95976-95985, exports `CODE_LIBRARY_IGNORED_DIRS`
- order 1000: `CODE_LIBRARY_LANGUAGE_BY_EXT` (constant), lines 95986-96042, exports `CODE_LIBRARY_LANGUAGE_BY_EXT`
- order 1001: `CODE_LIBRARY_SPECIAL_FILENAMES` (constant), lines 96043-96049, exports `CODE_LIBRARY_SPECIAL_FILENAMES`

### `rag/index.py`

- order 1004: `_code_module_name` (function), lines 96074-96090, exports `_code_module_name`
- order 1005: `_code_choose_community` (function), lines 96091-96100, exports `_code_choose_community`
- order 1006: `_code_query_terms` (function), lines 96101-96115, exports `_code_query_terms`
- order 1015: `TFGraphIDFIndex` (class), lines 97179-98855, exports `TFGraphIDFIndex`
- order 1024: `CodeGraphIndex` (class), lines 102063-102548, exports `CodeGraphIndex`

### `rag/ingestion.py`

- order 984: `_rag_trigram_set` (function), lines 95442-95449, exports `_rag_trigram_set`
- order 985: `_rag_jaccard_sim` (function), lines 95450-95459, exports `_rag_jaccard_sim`
- order 986: `_rag_mmr_select` (function), lines 95460-95509, exports `_rag_mmr_select`
- order 991: `_rag_embed_text` (function), lines 95644-95667, exports `_rag_embed_text`
- order 992: `_rag_embed_batch` (function), lines 95668-95676, exports `_rag_embed_batch`
- order 993: `_rag_window_for_query` (function), lines 95677-95691, exports `_rag_window_for_query`
- order 994: `_rag_focused_excerpt` (function), lines 95692-95734, exports `_rag_focused_excerpt`
- order 995: `_rag_query_variants` (function), lines 95735-95774, exports `_rag_query_variants`
- order 996: `_rag_parse_segments` (function), lines 95775-95837, exports `_rag_parse_segments`
- order 997: `_rag_boundary_split` (function), lines 95838-95895, exports `_rag_boundary_split`
- order 1022: `_rag_parse_file_worker` (function), lines 101164-101180, exports `_rag_parse_file_worker`
- order 1023: `RAGIngestionService` (class), lines 101181-102062, exports `RAGIngestionService`
- order 1026: `CodeIngestionService` (class), lines 102815-102902, exports `CodeIngestionService`

### `rag/parsers.py`

- order 975: `_rag_safe_name` (function), lines 95232-95246, exports `_rag_safe_name`
- order 976: `_rag_detect_language` (function), lines 95247-95263, exports `_rag_detect_language`
- order 977: `_rag_cjk_ngrams` (function), lines 95264-95278, exports `_rag_cjk_ngrams`
- order 978: `_rag_is_noise_token` (function), lines 95279-95300, exports `_rag_is_noise_token`
- order 979: `_rag_entity_allowed` (function), lines 95301-95315, exports `_rag_entity_allowed`
- order 980: `_rag_filter_entities` (function), lines 95316-95332, exports `_rag_filter_entities`
- order 981: `_rag_filename_entity_aliases` (function), lines 95333-95368, exports `_rag_filename_entity_aliases`
- order 982: `_rag_apply_filename_entity_policy` (function), lines 95369-95401, exports `_rag_apply_filename_entity_policy`
- order 983: `_rag_choose_community` (function), lines 95402-95441, exports `_rag_choose_community`
- order 987: `_rag_tokenize` (function), lines 95510-95563, exports `_rag_tokenize`
- order 988: `_rag_expand_tokens` (function), lines 95564-95587, exports `_rag_expand_tokens`
- order 989: `_rag_extract_entities` (function), lines 95588-95606, exports `_rag_extract_entities`
- order 990: `_rag_classify_document` (function), lines 95607-95643, exports `_rag_classify_document`
- order 998: `_rag_chunk_text` (function), lines 95896-95975, exports `_rag_chunk_text`
- order 1002: `_code_language_from_name` (function), lines 96050-96068, exports `_code_language_from_name`
- order 1003: `_code_is_test_path` (function), lines 96069-96073, exports `_code_is_test_path`
- order 1007: `_CallCollector` (class), lines 96116-96130, exports `_CallCollector`
- order 1008: `_ALGO_COMPLEXITY_RE` (assignment), lines 96131-96133, exports `_ALGO_COMPLEXITY_RE`
- order 1009: `_ALGO_STEP_RE` (assignment), lines 96134-96134, exports `_ALGO_STEP_RE`
- order 1010: `_ALGO_MATH_VARS` (assignment), lines 96135-96135, exports `_ALGO_MATH_VARS`
- order 1011: `_ALGO_DOC_KEYWORDS` (assignment), lines 96136-96136, exports `_ALGO_DOC_KEYWORDS`
- order 1012: `_detect_algo_chunk` (function), lines 96137-96162, exports `_detect_algo_chunk`
- order 1013: `CodeContentParser` (class), lines 96163-96672, exports `CodeContentParser`
- order 1014: `RAGContentParser` (class), lines 96673-97178, exports `RAGContentParser`

### `rag/store.py`

- order 1016: `RAGLibraryStore` (class), lines 98856-99441, exports `RAGLibraryStore`
- order 1017: `WikiStore` (class), lines 99442-99973, exports `WikiStore`
- order 1018: `UserMemoryStore` (class), lines 99974-100651, exports `UserMemoryStore`
- order 1019: `UserInteractionOptimizer` (class), lines 100652-100720, exports `UserInteractionOptimizer`
- order 1020: `UserIntentProfiler` (class), lines 100721-100762, exports `UserIntentProfiler`
- order 1021: `WorkflowMemoryStore` (class), lines 100763-101163, exports `WorkflowMemoryStore`
- order 1025: `CodeLibraryStore` (class), lines 102549-102814, exports `CodeLibraryStore`

### `rag/web_search.py`

- order 714: `_agent_web_bool` (function), lines 8400-8407, exports `_agent_web_bool`
- order 715: `_agent_web_int` (function), lines 8408-8415, exports `_agent_web_int`
- order 716: `_agent_web_host_is_local_name` (function), lines 8416-8422, exports `_agent_web_host_is_local_name`
- order 717: `_agent_web_ip_is_blocked` (function), lines 8423-8437, exports `_agent_web_ip_is_blocked`
- order 718: `_agent_web_canonical_url` (function), lines 8438-8467, exports `_agent_web_canonical_url`
- order 719: `_agent_web_domain_to_seed` (function), lines 8468-8479, exports `_agent_web_domain_to_seed`
- order 720: `_agent_web_query_terms` (function), lines 8480-8497, exports `_agent_web_query_terms`
- order 721: `_agent_web_query_domain_hints` (function), lines 8498-8538, exports `_agent_web_query_domain_hints`
- order 722: `_agent_web_query_needs_fresh_network` (function), lines 8539-8561, exports `_agent_web_query_needs_fresh_network`
- order 723: `_agent_web_extract_text_snippet` (function), lines 8562-8579, exports `_agent_web_extract_text_snippet`
- order 724: `AgentWebHTMLParser` (class), lines 8580-8659, exports `AgentWebHTMLParser`
- order 725: `_agent_web_decompress_bytes` (function), lines 8660-8683, exports `_agent_web_decompress_bytes`
- order 726: `_agent_web_charset_candidates` (function), lines 8684-8742, exports `_agent_web_charset_candidates`
- order 727: `_agent_web_decode_text_bytes` (function), lines 8743-8777, exports `_agent_web_decode_text_bytes`
- order 728: `AgentWebSearchEngine` (class), lines 8778-10560, exports `AgentWebSearchEngine`

### `server/http.py`

- order 1061: `AgentHTTPServer` (class), lines 118254-118293, exports `AgentHTTPServer`
- order 1064: `Handler` (class), lines 119480-121111, exports `Handler`
- order 1067: `SkillsReviewHandler` (class), lines 121913-122026, exports `SkillsReviewHandler`
- order 1071: `CollaborationHandler` (class), lines 123890-124360, exports `CollaborationHandler`

### `server/rag_admin.py`

- order 1066: `_RagAdminAuthMixin` (class), lines 121755-121912, exports `_RagAdminAuthMixin`
- order 1068: `RagAdminHandler` (class), lines 122027-122215, exports `RagAdminHandler`
- order 1069: `CodeAdminHandler` (class), lines 122216-122414, exports `CodeAdminHandler`

### `server/skills.py`

- order 1065: `SkillsHandler` (class), lines 121112-121754, exports `SkillsHandler`

### `session/manager.py`

- order 632: `SessionCreationLimitExceeded` (class), lines 6859-6864, exports `SessionCreationLimitExceeded`
- order 955: `SessionManager` (class), lines 82569-83948, exports `SessionManager`

### `session/state.py`

- order 954: `SessionState` (class), lines 27749-82568, exports `SessionState`

### `skills/embedded.py`

- order 854: `EMBEDDED_SKILLS_ARCHIVE_B64` (constant), lines 15697-15698, exports `EMBEDDED_SKILLS_ARCHIVE_B64`
- order 855: `EMBEDDED_SKILLS_ARCHIVE_SHA256` (constant), lines 15699-15699, exports `EMBEDDED_SKILLS_ARCHIVE_SHA256`
- order 856: `EMBEDDED_SKILLS_ARCHIVE_FILES` (constant), lines 15700-15722, exports `EMBEDDED_SKILLS_ARCHIVE_FILES`
- order 881: `BUILTIN_CLAWHUB_SKILLS_VERSION` (constant), lines 18958-18960, exports `BUILTIN_CLAWHUB_SKILLS_VERSION`
- order 882: `EMBEDDED_CLAWHUB_SKILLS_ARCHIVE_B64` (constant), lines 18961-19206, exports `EMBEDDED_CLAWHUB_SKILLS_ARCHIVE_B64`
- order 884: `MCP_BUILDER_SKILL_MD` (constant), lines 19254-19428, exports `MCP_BUILDER_SKILL_MD`
- order 887: `SKILL_PROTOCOL_LOCAL` (constant), lines 19460-19461, exports `SKILL_PROTOCOL_LOCAL`
- order 888: `SKILL_PROTOCOL_CLAWHUB` (constant), lines 19462-19462, exports `SKILL_PROTOCOL_CLAWHUB`
- order 889: `SKILL_PROTOCOL_HTTP_JSON` (constant), lines 19463-19463, exports `SKILL_PROTOCOL_HTTP_JSON`
- order 890: `SKILL_PROTOCOL_SPECS` (constant), lines 19464-19496, exports `SKILL_PROTOCOL_SPECS`

### `skills/provisioning.py`

- order 857: `ensure_embedded_skills_at_root` (function), lines 15723-15788, exports `ensure_embedded_skills_at_root`
- order 858: `ensure_embedded_skills` (function), lines 15789-15792, exports `ensure_embedded_skills`
- order 860: `detect_upload_parser_capabilities` (function), lines 15799-15815, exports `detect_upload_parser_capabilities`
- order 861: `_render_cap_markdown` (function), lines 15816-15831, exports `_render_cap_markdown`
- order 862: `_write_text_if_changed` (function), lines 15832-15838, exports `_write_text_if_changed`
- order 863: `ensure_generated_document_skills` (function), lines 15839-15928, exports `ensure_generated_document_skills`
- order 864: `ensure_generated_image_coding_feedback_skill` (function), lines 15929-16029, exports `ensure_generated_image_coding_feedback_skill`
- order 865: `_skill_knowledge_files` (function), lines 16030-16050, exports `_skill_knowledge_files`
- order 866: `analyze_skill_building_knowledge` (function), lines 16051-16106, exports `analyze_skill_building_knowledge`
- order 867: `_sanitize_skill_slug` (function), lines 16107-16110, exports `_sanitize_skill_slug`
- order 868: `_build_skills_gen_skill_content` (function), lines 16111-16143, exports `_build_skills_gen_skill_content`
- order 869: `ensure_generated_skills_gen_skill` (function), lines 16144-16149, exports `ensure_generated_skills_gen_skill`
- order 870: `ensure_generated_execution_recovery_skill` (function), lines 16150-16234, exports `ensure_generated_execution_recovery_skill`
- order 871: `ensure_generated_systematic_debugging_skill` (function), lines 16235-16508, exports `ensure_generated_systematic_debugging_skill`
- order 872: `ensure_generated_code_engineering_mastery_skill` (function), lines 16509-16628, exports `ensure_generated_code_engineering_mastery_skill`
- order 873: `ensure_generated_smart_file_navigation_skill` (function), lines 16629-16745, exports `ensure_generated_smart_file_navigation_skill`
- order 874: `ensure_generated_html_frontend_report_skills` (function), lines 16746-16954, exports `ensure_generated_html_frontend_report_skills`
- order 875: `ensure_generated_deep_research_skills` (function), lines 16955-17224, exports `ensure_generated_deep_research_skills`
- order 876: `ensure_generated_research_scientific_skills` (function), lines 17225-17862, exports `ensure_generated_research_scientific_skills`
- order 877: `ensure_generated_rag_mastery_skills` (function), lines 17863-18164, exports `ensure_generated_rag_mastery_skills`
- order 878: `ensure_generated_multimodal_comprehension_skills` (function), lines 18165-18859, exports `ensure_generated_multimodal_comprehension_skills`
- order 879: `ensure_generated_runtime_skills_manifest` (function), lines 18860-18894, exports `ensure_generated_runtime_skills_manifest`
- order 880: `ensure_generated_agent_web_search_skill` (function), lines 18895-18957, exports `ensure_generated_agent_web_search_skill`
- order 883: `ensure_embedded_clawhub_skills` (function), lines 19207-19253, exports `ensure_embedded_clawhub_skills`
- order 885: `ensure_generated_mcp_builder_skill` (function), lines 19429-19440, exports `ensure_generated_mcp_builder_skill`
- order 886: `ensure_runtime_skills` (function), lines 19441-19459, exports `ensure_runtime_skills`

### `skills/store.py`

- order 891: `_BUILTIN_SKILLS` (assignment), lines 19497-19605, exports `_BUILTIN_SKILLS`
- order 892: `SkillStore` (class), lines 19606-21387, exports `SkillStore`

### `skills/studio.py`

- order 1049: `SkillsStudioError` (class), lines 106576-106585, exports `SkillsStudioError`
- order 1050: `_studio_slug` (function), lines 106586-106601, exports `_studio_slug`
- order 1051: `_studio_hash` (function), lines 106602-106605, exports `_studio_hash`
- order 1052: `_studio_cookie_value` (function), lines 106606-106615, exports `_studio_cookie_value`
- order 1053: `SkillsStudioStore` (class), lines 106616-108474, exports `SkillsStudioStore`

### `utils/compress.py`

- order 732: `compress_text_blob` (function), lines 10725-10731, exports `compress_text_blob`
- order 733: `decompress_text_blob` (function), lines 10732-10741, exports `decompress_text_blob`

### `utils/crypto.py`

- order 805: `CryptoBox` (class), lines 12677-12795, exports `CryptoBox`

### `utils/errors.py`

- order 752: `EmptyActionError` (class), lines 11230-11233, exports `EmptyActionError`
- order 894: `ProcessManagerError` (class), lines 21523-21528, exports `ProcessManagerError`

### `utils/files.py`

- order 592: `_normalize_js_lib_asset_ref` (function), lines 5581-5596, exports `_normalize_js_lib_asset_ref`
- order 593: `_resolve_js_lib_asset_path` (function), lines 5597-5628, exports `_resolve_js_lib_asset_path`
- order 594: `_discover_extra_js_lib_files` (function), lines 5629-5661, exports `_discover_extra_js_lib_files`
- order 685: `safe_path` (function), lines 7712-7722, exports `safe_path`
- order 686: `_safe_js_filename` (function), lines 7723-7731, exports `_safe_js_filename`
- order 687: `_sha256_bytes` (function), lines 7732-7734, exports `_sha256_bytes`
- order 688: `_sha256_file` (function), lines 7735-7744, exports `_sha256_file`
- order 689: `_download_http_bytes` (function), lines 7745-7754, exports `_download_http_bytes`
- order 690: `offline_js_lib_root` (function), lines 7755-7757, exports `offline_js_lib_root`
- order 691: `_offline_js_entry_relative_path` (function), lines 7758-7763, exports `_offline_js_entry_relative_path`
- order 692: `_archive_member_relative_path` (function), lines 7764-7774, exports `_archive_member_relative_path`
- order 693: `_path_size_bytes` (function), lines 7775-7791, exports `_path_size_bytes`
- order 694: `_extract_archive_to_dir` (function), lines 7792-7833, exports `_extract_archive_to_dir`
- order 695: `_package_required_paths` (function), lines 7834-7841, exports `_package_required_paths`
- order 696: `_package_required_globs` (function), lines 7842-7858, exports `_package_required_globs`
- order 697: `_package_install_ready` (function), lines 7859-7881, exports `_package_install_ready`
- order 698: `_postprocess_offline_js_package` (function), lines 7882-7918, exports `_postprocess_offline_js_package`
- order 699: `_ensure_offline_js_package` (function), lines 7919-7963, exports `_ensure_offline_js_package`
- order 700: `_render_offline_js_catalog_md` (function), lines 7964-7981, exports `_render_offline_js_catalog_md`
- order 702: `ensure_offline_js_libs` (function), lines 7993-8151, exports `ensure_offline_js_libs`
- order 703: `_offline_js_catalog_entry_for_asset` (function), lines 8152-8172, exports `_offline_js_catalog_entry_for_asset`
- order 704: `ensure_offline_js_asset` (function), lines 8173-8230, exports `ensure_offline_js_asset`
- order 705: `_normalize_external_js_url` (function), lines 8231-8236, exports `_normalize_external_js_url`
- order 706: `is_external_js_src` (function), lines 8237-8240, exports `is_external_js_src`
- order 707: `match_offline_js_catalog_by_url` (function), lines 8241-8258, exports `match_offline_js_catalog_by_url`
- order 708: `cache_external_js_url` (function), lines 8259-8294, exports `cache_external_js_url`
- order 808: `try_read_text` (function), lines 13039-13048, exports `try_read_text`

### `utils/http.py`

- order 107: `_URL_OPEN_ORIGINAL` (assignment), lines 3462-3462, exports `_URL_OPEN_ORIGINAL`
- order 108: `_HTTP_SSL_CONTEXT` (assignment), lines 3463-3463, exports `_HTTP_SSL_CONTEXT`
- order 135: `_shared_http_ssl_context` (function), lines 3527-3550, exports `_shared_http_ssl_context`
- order 136: `urlopen` (function), lines 3551-3560, exports `urlopen`
- order 678: `json_response_bytes` (function), lines 7657-7659, exports `json_response_bytes`
- order 679: `read_http_json_body` (function), lines 7660-7673, exports `read_http_json_body`
- order 680: `close_if_http_request_body_unread` (function), lines 7674-7687, exports `close_if_http_request_body_unread`

### `utils/json_utils.py`

- order 159: `JSON_FSYNC_ENABLED` (constant), lines 3827-3827, exports `JSON_FSYNC_ENABLED`
- order 677: `json_dumps` (function), lines 7653-7656, exports `json_dumps`
- order 742: `parse_tool_arguments` (function), lines 11035-11045, exports `parse_tool_arguments`
- order 743: `repair_truncated_json_object` (function), lines 11046-11100, exports `repair_truncated_json_object`
- order 744: `parse_tool_arguments_with_error` (function), lines 11101-11132, exports `parse_tool_arguments_with_error`
- order 745: `_is_valid_json_object` (function), lines 11133-11138, exports `_is_valid_json_object`
- order 746: `_scan_top_level_json_objects` (function), lines 11139-11162, exports `_scan_top_level_json_objects`
- order 747: `reconstruct_streamed_tool_args` (function), lines 11163-11207, exports `reconstruct_streamed_tool_args`
- order 765: `parse_json_object` (function), lines 11471-11477, exports `parse_json_object`
- order 766: `extract_json_object_from_text` (function), lines 11478-11501, exports `extract_json_object_from_text`
- order 809: `_json_default_copy` (function), lines 13049-13055, exports `_json_default_copy`
- order 810: `_read_json_file` (function), lines 13056-13077, exports `_read_json_file`
- order 811: `_write_json_file` (function), lines 13078-13106, exports `_write_json_file`

### `utils/media.py`

- order 585: `_capability_probe_png_bytes` (function), lines 5219-5233, exports `_capability_probe_png_bytes`
- order 586: `_capability_probe_audio_bytes` (function), lines 5234-5245, exports `_capability_probe_audio_bytes`
- order 587: `_capability_probe_video_bytes` (function), lines 5246-5250, exports `_capability_probe_video_bytes`
- order 647: `guess_mime_from_name` (function), lines 7207-7211, exports `guess_mime_from_name`
- order 648: `_convert_image_to_safe_format` (function), lines 7212-7231, exports `_convert_image_to_safe_format`
- order 649: `guess_ext_from_mime` (function), lines 7232-7240, exports `guess_ext_from_mime`

### `utils/misc.py`

- order 650: `now_ts` (function), lines 7241-7243, exports `now_ts`
- order 651: `_benign_socket_log_lock` (assignment), lines 7244-7246, exports `_benign_socket_log_lock`
- order 652: `_benign_socket_log_state` (assignment), lines 7247-7247, exports `_benign_socket_log_state`
- order 654: `is_benign_socket_error` (function), lines 7263-7283, exports `is_benign_socket_error`
- order 655: `_socket_error_code` (function), lines 7284-7295, exports `_socket_error_code`
- order 656: `_log_benign_socket_error_limited` (function), lines 7296-7332, exports `_log_benign_socket_error_limited`
- order 657: `swallow_benign_socket_error` (function), lines 7333-7339, exports `swallow_benign_socket_error`
- order 658: `normalize_timeout_seconds` (function), lines 7340-7355, exports `normalize_timeout_seconds`
- order 659: `detect_local_lan_ip` (function), lines 7356-7367, exports `detect_local_lan_ip`
- order 660: `_LOCAL_LAN_IP_CACHE` (assignment), lines 7368-7369, exports `_LOCAL_LAN_IP_CACHE`
- order 661: `detect_local_lan_ip_cached` (function), lines 7370-7383, exports `detect_local_lan_ip_cached`
- order 681: `make_id` (function), lines 7688-7690, exports `make_id`
- order 682: `sanitize_profile_id` (function), lines 7691-7694, exports `sanitize_profile_id`
- order 803: `user_id_from_ip` (function), lines 12636-12643, exports `user_id_from_ip`
- order 807: `_meta_string_list` (function), lines 13025-13038, exports `_meta_string_list`
- order 859: `_module_exists` (function), lines 15793-15798, exports `_module_exists`

### `utils/text.py`

- order 147: `MAX_TOOL_OUTPUT` (constant), lines 3815-3815, exports `MAX_TOOL_OUTPUT`
- order 419: `SOCKET_NOISE_LINE_PATTERNS` (constant), lines 4379-4384, exports `SOCKET_NOISE_LINE_PATTERNS`
- order 653: `filter_runtime_noise_lines` (function), lines 7248-7262, exports `filter_runtime_noise_lines`
- order 666: `safe_utf8_bytes` (function), lines 7508-7510, exports `safe_utf8_bytes`
- order 667: `escape_invalid_utf8_text` (function), lines 7511-7513, exports `escape_invalid_utf8_text`
- order 668: `sanitize_utf8_surrogates` (function), lines 7514-7527, exports `sanitize_utf8_surrogates`
- order 669: `decode_utf8_replace` (function), lines 7528-7532, exports `decode_utf8_replace`
- order 709: `trim` (function), lines 8295-8298, exports `trim`
- order 710: `is_synthetic_public_progress` (function), lines 8299-8318, exports `is_synthetic_public_progress`
- order 712: `display_clean` (function), lines 8366-8380, exports `display_clean`
- order 713: `short_title_from` (function), lines 8381-8399, exports `short_title_from`
- order 729: `_fmt_export_ts` (function), lines 10561-10571, exports `_fmt_export_ts`
- order 730: `_html_esc` (function), lines 10572-10575, exports `_html_esc`
- order 731: `_text_to_minimal_pdf` (function), lines 10576-10724, exports `_text_to_minimal_pdf`
- order 734: `normalize_embedded_newlines` (function), lines 10742-10751, exports `normalize_embedded_newlines`
- order 735: `_map_todo_status_token` (function), lines 10752-10790, exports `_map_todo_status_token`
- order 736: `split_todo_status_text` (function), lines 10791-10850, exports `split_todo_status_text`
- order 737: `extract_todo_rows_from_text` (function), lines 10851-10920, exports `extract_todo_rows_from_text`
- order 738: `decode_structured_todo_container` (function), lines 10921-10939, exports `decode_structured_todo_container`
- order 739: `infer_todo_status_from_text` (function), lines 10940-10948, exports `infer_todo_status_from_text`
- order 740: `split_structured_todo_content` (function), lines 10949-11004, exports `split_structured_todo_content`
- order 741: `normalize_work_text` (function), lines 11005-11034, exports `normalize_work_text`
- order 826: `make_unified_diff` (function), lines 14598-14616, exports `make_unified_diff`
- order 827: `_skip_row` (function), lines 14617-14622, exports `_skip_row`
- order 828: `_row_is_hot` (function), lines 14623-14626, exports `_row_is_hot`
- order 829: `_hotspot_index` (function), lines 14627-14650, exports `_hotspot_index`
- order 830: `_compress_rows_keep_hotspot` (function), lines 14651-14700, exports `_compress_rows_keep_hotspot`
- order 831: `_focused_diff_rows_from_opcodes` (function), lines 14701-14835, exports `_focused_diff_rows_from_opcodes`
- order 832: `make_numbered_diff` (function), lines 14836-14868, exports `make_numbered_diff`
- order 833: `render_numbered_diff_text` (function), lines 14869-14882, exports `render_numbered_diff_text`

### `web/admin_assets.py`

- order 963: `ADMIN_INDEX_HTML` (constant), lines 89830-90065, exports `ADMIN_INDEX_HTML`
- order 964: `ADMIN_CSS` (constant), lines 90066-90199, exports `ADMIN_CSS`
- order 965: `ADMIN_JS` (constant), lines 90200-90297, exports `ADMIN_JS`

### `web/assets.py`

- order 956: `INDEX_HTML` (constant), lines 83949-84200, exports `INDEX_HTML`
- order 957: `APP_CSS` (constant), lines 84201-84737, exports `APP_CSS`
- order 958: `APP_JS` (constant), lines 84738-89390, exports `APP_JS`
- order 959: `APP_TS` (constant), lines 89391-89430, exports `APP_TS`

### `web/skills_assets.py`

- order 960: `SKILLS_INDEX_HTML` (constant), lines 89431-89586, exports `SKILLS_INDEX_HTML`
- order 961: `SKILLS_EXTRA_CSS` (constant), lines 89587-89683, exports `SKILLS_EXTRA_CSS`
- order 962: `SKILLS_APP_JS` (constant), lines 89684-89829, exports `SKILLS_APP_JS`
