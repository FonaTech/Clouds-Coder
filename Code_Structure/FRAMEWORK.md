# Code_Structure Framework

## Overview

- Source file: `/Users/Fona/Downloads/Split Tools/Clouds_Coder.py`
- Output directory: `/Users/Fona/Downloads/Split Tools/Code_Structure`
- Generated modules: 29
- Top-level symbols: 508
- Entry point present: yes
- Unclassified symbols: 0

## Package Tree

```text
Code_Structure/
├── agent
│   ├── background.py
│   ├── bus.py
│   ├── events.py
│   ├── tasks.py
│   ├── todo.py
│   └── worktree.py
├── app
│   └── context.py
├── config
│   ├── constants.py
│   ├── paths.py
│   └── settings.py
├── llm
│   ├── client.py
│   └── utils.py
├── rag
│   ├── index.py
│   ├── ingestion.py
│   ├── parsers.py
│   └── store.py
├── server
│   └── handlers.py
├── session
│   ├── manager.py
│   └── state.py
├── skills
│   └── store.py
├── utils
│   ├── compress.py
│   ├── crypto.py
│   ├── errors.py
│   ├── files.py
│   ├── json_utils.py
│   ├── media.py
│   ├── misc.py
│   └── text.py
├── __init__.py
└── __main__.py
```

## Module Summary

| Module | Symbols | Cross-module deps |
| --- | ---: | --- |
| `__main__.py` | 2 | `app/context.py`, `config/constants.py`, `config/paths.py`, `config/settings.py`, `llm/utils.py`, `server/handlers.py`, `skills/store.py`, `utils/files.py`, `utils/misc.py`, `utils/text.py` |
| `agent/background.py` | 1 | `utils/misc.py`, `utils/text.py` |
| `agent/bus.py` | 1 | `config/constants.py`, `utils/crypto.py`, `utils/misc.py` |
| `agent/events.py` | 1 | — |
| `agent/tasks.py` | 1 | `utils/crypto.py`, `utils/json_utils.py`, `utils/misc.py` |
| `agent/todo.py` | 1 | `config/constants.py`, `config/settings.py`, `utils/text.py` |
| `agent/worktree.py` | 1 | `agent/tasks.py`, `config/constants.py`, `utils/crypto.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` |
| `app/context.py` | 1 | `config/constants.py`, `config/paths.py`, `config/settings.py`, `llm/client.py`, `llm/utils.py`, `rag/ingestion.py`, `rag/parsers.py`, `rag/store.py`, `session/manager.py`, `session/state.py`, `skills/store.py`, `utils/crypto.py`, `utils/files.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` |
| `config/constants.py` | 286 | `utils/json_utils.py`, `utils/misc.py` |
| `config/paths.py` | 8 | `utils/text.py` |
| `config/settings.py` | 28 | `config/constants.py`, `config/paths.py`, `llm/utils.py`, `skills/store.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` |
| `llm/client.py` | 2 | `config/constants.py`, `config/settings.py`, `llm/utils.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` |
| `llm/utils.py` | 25 | `config/constants.py`, `utils/json_utils.py`, `utils/text.py` |
| `rag/index.py` | 5 | `config/constants.py`, `rag/parsers.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` |
| `rag/ingestion.py` | 3 | `config/constants.py`, `config/settings.py`, `rag/parsers.py`, `rag/store.py`, `session/state.py`, `utils/files.py`, `utils/json_utils.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py` |
| `rag/parsers.py` | 22 | `config/constants.py`, `utils/files.py`, `utils/json_utils.py`, `utils/media.py`, `utils/text.py` |
| `rag/store.py` | 2 | `config/constants.py`, `rag/index.py`, `rag/parsers.py`, `utils/files.py`, `utils/json_utils.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py` |
| `server/handlers.py` | 5 | `app/context.py`, `config/constants.py`, `config/paths.py`, `config/settings.py`, `llm/utils.py`, `session/manager.py`, `session/state.py`, `skills/store.py`, `utils/files.py`, `utils/json_utils.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py` |
| `session/manager.py` | 2 | `config/constants.py`, `config/paths.py`, `config/settings.py`, `llm/client.py`, `llm/utils.py`, `session/state.py`, `utils/crypto.py`, `utils/files.py`, `utils/json_utils.py`, `utils/misc.py` |
| `session/state.py` | 1 | `agent/background.py`, `agent/bus.py`, `agent/events.py`, `agent/tasks.py`, `agent/todo.py`, `agent/worktree.py`, `config/constants.py`, `config/paths.py`, `config/settings.py`, `llm/client.py`, `llm/utils.py`, `rag/parsers.py`, `skills/store.py`, `utils/compress.py`, `utils/crypto.py`, `utils/errors.py`, `utils/files.py`, `utils/json_utils.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py` |
| `skills/store.py` | 26 | `config/constants.py`, `config/paths.py`, `llm/utils.py`, `utils/files.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` |
| `utils/compress.py` | 2 | — |
| `utils/crypto.py` | 1 | `utils/json_utils.py` |
| `utils/errors.py` | 2 | — |
| `utils/files.py` | 25 | `config/constants.py`, `config/paths.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` |
| `utils/json_utils.py` | 16 | `utils/text.py` |
| `utils/media.py` | 3 | — |
| `utils/misc.py` | 19 | — |
| `utils/text.py` | 16 | — |

## Module Details

### `__main__.py`

- Routed symbols: 2
- Cross-module imports: `app/context.py`: `AppContext`; `config/constants.py`: `AGENT_MAX_OUTPUT_TOKENS`, `ARBITER_DEFAULT_MAX_TOKENS`, `ARBITER_DEFAULT_TEMPERATURE`, `ARBITER_DEFAULT_TIMEOUT_SECONDS`, `CODE_ADMIN_PORT_OFFSET`, `DEFAULT_OLLAMA_BASE_URL`, `DEFAULT_OLLAMA_MODEL`, `DEFAULT_UI_LANGUAGE`, `DEFAULT_UI_STYLE`, `DEFAULT_WEB_UI_CONFIG`, `DEFAULT_WEB_UI_DIR`, `EXECUTION_MODE_SYNC`, `LIVE_INPUT_DELAY_NORMAL_ROUNDS`, `LIVE_INPUT_DELAY_TOOL_ROUNDS`, `LIVE_INPUT_DELAY_WRITE_ROUNDS`, `LIVE_INPUT_MAX_INJECTIONS`, `LIVE_INPUT_REINJECT_INTERVAL`, `LIVE_INPUT_WEIGHT_BASE_DELAYED`, `LIVE_INPUT_WEIGHT_BASE_NORMAL`, `LIVE_INPUT_WEIGHT_STEP_DELAYED`, `LIVE_INPUT_WEIGHT_STEP_NORMAL`, `MAX_AGENT_ROUNDS`, `MAX_AGENT_ROUNDS_CAP`, `MAX_RUN_SECONDS`, `MAX_RUN_TIMEOUT_SECONDS`, `MIN_AGENT_ROUNDS`, `MIN_CONTEXT_TOKEN_LIMIT`, `MIN_RUN_TIMEOUT_SECONDS`, `OFFLINE_JS_LIB_CATALOG`, `RAG_ADMIN_PORT_OFFSET`, `RAG_INCLUDE_FILENAME_ENTITIES_DEFAULT`, `TOKEN_THRESHOLD`, `UI_LANGUAGE_LABELS`, `UI_STYLE_LABELS`; `config/paths.py`: `LLM_CONFIG_PATH`, `REPO_ROOT`, `WORKDIR`; `config/settings.py`: `_to_bool_like`, `extract_daily_session_limit_setting`, `extract_js_lib_download_setting`, `extract_show_upload_list_setting`, `extract_ui_style_setting`, `load_llm_config_from_source`, `load_web_ui_config_file`, `normalize_execution_mode`, `normalize_ui_language`, `normalize_ui_style`, `parse_llm_config_profiles`, `resolve_optional_file_path`, `resolve_web_ui_dir_path`, `select_preferred_skills_root`; `llm/utils.py`: `list_ollama_models`; `server/handlers.py`: `AgentHTTPServer`, `CodeAdminHandler`, `Handler`, `RagAdminHandler`, `SkillsHandler`; `skills/store.py`: `ensure_embedded_skills_at_root`, `ensure_runtime_skills`; `utils/files.py`: `ensure_offline_js_libs`; `utils/misc.py`: `BENIGN_SOCKET_DEBUG_LOG_ENABLED`, `detect_local_lan_ip`, `normalize_timeout_seconds`, `swallow_benign_socket_error`; `utils/text.py`: `trim`
- Symbols:
  - `main` (function, lines 52257-53190)
  - `_main_guard_53192` (main_guard, lines 53192-53193)

### `agent/background.py`

- Routed symbols: 1
- Cross-module imports: `utils/misc.py`: `make_id`, `now_ts`; `utils/text.py`: `trim`
- Symbols:
  - `BackgroundManager` (class, lines 10989-11069)

### `agent/bus.py`

- Routed symbols: 1
- Cross-module imports: `config/constants.py`: `VALID_MSG_TYPES`; `utils/crypto.py`: `CryptoBox`; `utils/misc.py`: `now_ts`
- Symbols:
  - `MessageBus` (class, lines 11071-11125)

### `agent/events.py`

- Routed symbols: 1
- Cross-module imports: none
- Symbols:
  - `EventHub` (class, lines 5133-5178)

### `agent/tasks.py`

- Routed symbols: 1
- Cross-module imports: `utils/crypto.py`: `CryptoBox`; `utils/json_utils.py`: `json_dumps`; `utils/misc.py`: `now_ts`
- Symbols:
  - `TaskManager` (class, lines 10861-10987)

### `agent/todo.py`

- Routed symbols: 1
- Cross-module imports: `config/constants.py`: `DEFAULT_UI_LANGUAGE`; `config/settings.py`: `backend_i18n_text`, `backend_role_label`, `normalize_ui_language`; `utils/text.py`: `normalize_work_text`, `trim`
- Symbols:
  - `TodoManager` (class, lines 5180-5426)

### `agent/worktree.py`

- Routed symbols: 1
- Cross-module imports: `agent/tasks.py`: `TaskManager`; `config/constants.py`: `DANGEROUS_PATTERNS`; `utils/crypto.py`: `CryptoBox`; `utils/json_utils.py`: `json_dumps`; `utils/misc.py`: `now_ts`; `utils/text.py`: `trim`
- Symbols:
  - `WorktreeManager` (class, lines 11127-11338)

### `app/context.py`

- Routed symbols: 1
- Cross-module imports: `config/constants.py`: `AGENT_MAX_OUTPUT_TOKENS`, `APP_CSS`, `APP_JS`, `APP_TS`, `ARBITER_DEFAULT_MAX_TOKENS`, `ARBITER_DEFAULT_TEMPERATURE`, `ARBITER_DEFAULT_TIMEOUT_SECONDS`, `CODE_ADMIN_CSS`, `CODE_ADMIN_INDEX_HTML`, `CODE_ADMIN_JS`, `CODE_IMPORT_WORKER_COUNT`, `CODE_LIBRARY_DIRNAME`, `CODE_PARSE_TIMEOUT_SECONDS`, `DEFAULT_REQUEST_TIMEOUT`, `DEFAULT_UI_LANGUAGE`, `DEFAULT_UI_STYLE`, `DEFAULT_WEB_UI_DIR`, `EXECUTION_MODE_SYNC`, `INDEX_HTML`, `MAX_AGENT_ROUNDS`, `MAX_AGENT_ROUNDS_CAP`, `MAX_RUN_SECONDS`, `MAX_RUN_TIMEOUT_SECONDS`, `MIN_AGENT_ROUNDS`, `MIN_CONTEXT_TOKEN_LIMIT`, `MIN_RUN_TIMEOUT_SECONDS`, `RAG_ADMIN_CSS`, `RAG_ADMIN_INDEX_HTML`, `RAG_ADMIN_JS`, `RAG_GRAPH_MAX_NODES`, `RAG_IMPORT_WORKER_COUNT`, `RAG_INCLUDE_FILENAME_ENTITIES_DEFAULT`, `RAG_LIBRARY_DIRNAME`, `RAG_MAX_GLOBAL_COMMUNITIES`, `RAG_MAX_IMPORT_BATCH_BYTES`, `RAG_MAX_IMPORT_BATCH_ITEMS`, `RAG_MAX_IMPORT_FILES`, `RAG_MAX_QUERY_RESULTS`, `RAG_PARSE_TIMEOUT_SECONDS`, `RAG_QUERY_CONTEXT_CHARS`, `SKILLS_APP_JS`, `SKILLS_EXTRA_CSS`, `SKILLS_INDEX_HTML`, `SKILL_REFRESH_MIN_INTERVAL_SECONDS`, `TOKEN_THRESHOLD`, `WEB_UI_OPTIONAL_FILES`, `WEB_UI_REQUIRED_FILES`; `config/paths.py`: `LLM_CONFIG_PATH`, `REPO_ROOT`, `SCRIPT_DIR`, `_migrate_legacy_runtime_roots`; `config/settings.py`: `default_multimodal_capabilities`, `infer_model_multimodal_capabilities`, `merge_multimodal_capabilities`, `model_language_instruction`, `normalize_execution_mode`, `normalize_ui_language`, `normalize_ui_style`, `parse_capability_overrides`, `parse_llm_config_profiles`, `resolve_optional_file_path`, `resolve_web_ui_dir_path`; `llm/client.py`: `OllamaClient`; `llm/utils.py`: `extract_base_url`; `rag/ingestion.py`: `CodeIngestionService`, `RAGIngestionService`; `rag/parsers.py`: `CodeContentParser`, `RAGContentParser`; `rag/store.py`: `CodeLibraryStore`, `RAGLibraryStore`; `session/manager.py`: `SessionCreationLimitExceeded`, `SessionManager`; `session/state.py`: `SessionState`; `skills/store.py`: `SkillStore`, `_sanitize_skill_slug`, `analyze_skill_building_knowledge`, `ensure_runtime_skills`; `utils/crypto.py`: `CryptoBox`; `utils/files.py`: `_resolve_js_lib_asset_path`, `ensure_offline_js_libs`, `load_offline_js_lib_index`, `offline_js_lib_root`, `safe_path`, `try_read_text`; `utils/json_utils.py`: `TOOLS`, `extract_json_object_from_text`, `json_dumps`, `parse_json_object`; `utils/misc.py`: `DEFAULT_TIMEOUT_SECONDS`, `MAX_TIMEOUT_SECONDS`, `MIN_TIMEOUT_SECONDS`, `normalize_timeout_seconds`, `now_ts`, `sanitize_profile_id`; `utils/text.py`: `parse_front_matter`, `trim`
- Symbols:
  - `AppContext` (class, lines 48457-50873)

### `config/constants.py`

- Routed symbols: 286
- Cross-module imports: `utils/json_utils.py`: `TOOL_SPEC_BY_NAME`; `utils/misc.py`: `DEFAULT_TIMEOUT_SECONDS`
- Symbols:
  - `APP_VERSION` (constant, lines 51-51)
  - `DEFAULT_OLLAMA_BASE_URL` (constant, lines 52-52)
  - `DEFAULT_OLLAMA_MODEL` (constant, lines 53-53)
  - `LONG_OUTPUT_MODEL_PAGE_CHARS` (constant, lines 96-96)
  - `LONG_OUTPUT_UI_PAGE_CHARS` (constant, lines 97-97)
  - `LONG_OUTPUT_UI_PREVIEW_MAX_PAGES` (constant, lines 98-98)
  - `LONG_OUTPUT_LISTING_OFFLOAD_CHARS` (constant, lines 99-99)
  - `LONG_OUTPUT_READ_PAGE_LINES` (constant, lines 100-100)
  - `LONG_OUTPUT_READ_PAGE_MAX_CHARS` (constant, lines 101-101)
  - `LONG_OUTPUT_TEMP_MAX_FILES` (constant, lines 102-102)
  - `RAG_LIBRARY_DIRNAME` (constant, lines 104-104)
  - `RAG_ADMIN_PORT_OFFSET` (constant, lines 105-105)
  - `CODE_LIBRARY_DIRNAME` (constant, lines 106-106)
  - `CODE_ADMIN_PORT_OFFSET` (constant, lines 107-107)
  - `RAG_CHUNK_CHARS` (constant, lines 108-108)
  - `RAG_CHUNK_OVERLAP` (constant, lines 109-109)
  - `RAG_MAX_CHUNKS_PER_DOC` (constant, lines 110-110)
  - `CODE_CHUNK_CHARS` (constant, lines 111-111)
  - `CODE_CHUNK_OVERLAP` (constant, lines 112-112)
  - `CODE_MAX_CHUNKS_PER_DOC` (constant, lines 113-113)
  - `RAG_MAX_QUERY_RESULTS` (constant, lines 114-114)
  - `RAG_GRAPH_MAX_NODES` (constant, lines 115-115)
  - `RAG_TASK_HISTORY_LIMIT` (constant, lines 116-116)
  - `RAG_MODEL_MEDIA_MAX_BYTES` (constant, lines 117-117)
  - `RAG_MAX_IMPORT_FILES` (constant, lines 118-118)
  - `RAG_MAX_IMPORT_BATCH_ITEMS` (constant, lines 119-119)
  - `RAG_MAX_IMPORT_BATCH_BYTES` (constant, lines 120-120)
  - `RAG_PDF_IMAGE_LIMIT` (constant, lines 121-121)
  - `RAG_QUERY_CONTEXT_CHARS` (constant, lines 122-122)
  - `RAG_MAX_GLOBAL_COMMUNITIES` (constant, lines 123-123)
  - `RAG_MAX_COMMUNITY_MAP_SUPPORT` (constant, lines 124-124)
  - `RAG_INCLUDE_FILENAME_ENTITIES_DEFAULT` (constant, lines 125-125)
  - `RAG_DYNAMIC_NOISE_MIN_DOC_FREQ` (constant, lines 126-126)
  - `RAG_DYNAMIC_NOISE_MIN_COMMUNITY_FREQ` (constant, lines 127-127)
  - `RAG_DYNAMIC_NOISE_SOFT_DOC_RATIO` (constant, lines 128-128)
  - `RAG_DYNAMIC_NOISE_HARD_DOC_RATIO` (constant, lines 129-129)
  - `RAG_DYNAMIC_NOISE_SOFT_COMMUNITY_RATIO` (constant, lines 130-130)
  - `RAG_DYNAMIC_NOISE_HARD_COMMUNITY_RATIO` (constant, lines 131-131)
  - `RAG_IMPORT_WORKER_COUNT` (constant, lines 132-135)
  - `CODE_IMPORT_WORKER_COUNT` (constant, lines 136-139)
  - `RAG_PARSE_TIMEOUT_SECONDS` (constant, lines 140-143)
  - `CODE_PARSE_TIMEOUT_SECONDS` (constant, lines 144-147)
  - `TOKEN_THRESHOLD` (constant, lines 148-148)
  - `IDLE_TIMEOUT` (constant, lines 149-149)
  - `POLL_INTERVAL` (constant, lines 150-150)
  - `SSE_HEARTBEAT_SECONDS` (constant, lines 151-151)
  - `MODEL_CALL_PROGRESS_DELAY` (constant, lines 152-152)
  - `MODEL_CALL_PROGRESS_INTERVAL` (constant, lines 153-153)
  - `MAX_AGENT_ROUNDS` (constant, lines 154-154)
  - `MIN_AGENT_ROUNDS` (constant, lines 155-155)
  - `MAX_AGENT_ROUNDS_CAP` (constant, lines 156-156)
  - `REPEATED_TOOL_LOOP_THRESHOLD` (constant, lines 157-157)
  - `BASH_READ_LOOP_THRESHOLD` (constant, lines 158-158)
  - `HARD_BREAK_TOOL_ERROR_THRESHOLD` (constant, lines 159-159)
  - `HARD_BREAK_RECOVERY_ROUND_THRESHOLD` (constant, lines 160-160)
  - `FUSED_FAULT_BREAK_THRESHOLD` (constant, lines 161-161)
  - `STALL_SEVERITY_ESCALATION_THRESHOLD` (constant, lines 162-162)
  - `STALL_SEVERITY_WEIGHT_BASH_READ_LOOP` (constant, lines 163-163)
  - `STALL_SEVERITY_WEIGHT_REPEATED_TOOL` (constant, lines 164-164)
  - `STALL_SEVERITY_WEIGHT_FAULT` (constant, lines 165-165)
  - `STALL_SEVERITY_WEIGHT_RECOVERY_RETRY` (constant, lines 166-166)
  - `STALL_SEVERITY_WEIGHT_WATCHDOG` (constant, lines 167-167)
  - `STALL_SEVERITY_DECAY_ON_SUCCESS` (constant, lines 168-168)
  - `STALL_ESCALATION_MIN_LEVEL` (constant, lines 169-169)
  - `STALL_PLAN_SYNTHESIS_MAX_TOKENS` (constant, lines 170-170)
  - `STALL_ESCALATION_CONTEXT_MAX_CHARS` (constant, lines 171-171)
  - `MAX_RUN_SECONDS` (constant, lines 172-172)
  - `MIN_RUN_TIMEOUT_SECONDS` (constant, lines 173-173)
  - `MAX_RUN_TIMEOUT_SECONDS` (constant, lines 174-174)
  - `DEFAULT_REQUEST_TIMEOUT` (constant, lines 184-184)
  - `AUTO_CONTINUE_BUDGET_DEFAULT` (constant, lines 185-185)
  - `AGENT_MAX_OUTPUT_TOKENS` (constant, lines 186-186)
  - `OLLAMA_THINKING_TOOL_BUFFER` (constant, lines 187-187)
  - `WATCHDOG_INTENT_NO_TOOL_THRESHOLD` (constant, lines 188-188)
  - `WATCHDOG_REPEAT_NO_TOOL_THRESHOLD` (constant, lines 189-189)
  - `WATCHDOG_INTENT_NO_TOOL_THRESHOLD_SINGLE` (constant, lines 190-190)
  - `WATCHDOG_REPEAT_NO_TOOL_THRESHOLD_SINGLE` (constant, lines 191-191)
  - `WATCHDOG_STATE_STALL_THRESHOLD` (constant, lines 192-192)
  - `WATCHDOG_CONTEXT_STALL_THRESHOLD` (constant, lines 193-193)
  - `WATCHDOG_REPEAT_SIMILARITY_THRESHOLD` (constant, lines 194-194)
  - `WATCHDOG_CONTEXT_NEAR_RATIO` (constant, lines 195-195)
  - `WATCHDOG_MAX_DECOMPOSE_STEPS` (constant, lines 196-196)
  - `WATCHDOG_STEP_MAX_ATTEMPTS` (constant, lines 197-197)
  - `EMPTY_ACTION_MIN_CONTENT_CHARS` (constant, lines 198-198)
  - `EMPTY_ACTION_WAKEUP_RETRY_LIMIT` (constant, lines 199-199)
  - `THINKING_BUDGET_FORCE_RATIO` (constant, lines 200-200)
  - `_TOOL_TIMEOUT_MAP` (assignment, lines 202-218)
  - `_DEFAULT_TOOL_TIMEOUT` (assignment, lines 219-219)
  - `TRUNCATION_CONTINUATION_MAX_PASSES` (constant, lines 220-220)
  - `TRUNCATION_CONTINUATION_MAX_TOKENS` (constant, lines 221-221)
  - `TRUNCATION_CONTINUATION_TAIL_CHARS` (constant, lines 222-222)
  - `TRUNCATION_CONTINUATION_ECHO_CHARS` (constant, lines 223-223)
  - `TRUNCATION_OVERLAP_SCAN_CHARS` (constant, lines 224-224)
  - `TRUNCATION_PAIR_SCAN_CHARS` (constant, lines 225-225)
  - `TRUNCATION_LIVE_BUFFER_MAX_CHARS` (constant, lines 226-226)
  - `MIN_CONTEXT_TOKEN_LIMIT` (constant, lines 227-227)
  - `COMPACT_TIER1_PCT` (constant, lines 229-229)
  - `COMPACT_TIER2_PCT` (constant, lines 230-230)
  - `COMPACT_TIER3_PCT` (constant, lines 231-231)
  - `COMPACT_TIER1_ABS` (constant, lines 233-233)
  - `COMPACT_TIER2_ABS` (constant, lines 234-234)
  - `FILE_BUFFER_CONTENT_THRESHOLD` (constant, lines 236-236)
  - `FILE_BUFFER_MAX_FILES` (constant, lines 237-237)
  - `AGENT_MSG_LIMIT_TIER0` (constant, lines 239-239)
  - `AGENT_MSG_LIMIT_TIER1` (constant, lines 240-240)
  - `AGENT_MSG_LIMIT_TIER2` (constant, lines 241-241)
  - `AGENT_MSG_LIMIT_TIER3` (constant, lines 242-242)
  - `AGENT_CTX_LIMIT_TIER0` (constant, lines 243-243)
  - `AGENT_CTX_LIMIT_TIER1` (constant, lines 244-244)
  - `AGENT_CTX_LIMIT_TIER2` (constant, lines 245-245)
  - `AGENT_CTX_LIMIT_TIER3` (constant, lines 246-246)
  - `MANAGER_CTX_LIMIT_TIER0` (constant, lines 247-247)
  - `MANAGER_CTX_LIMIT_TIER1` (constant, lines 248-248)
  - `MANAGER_CTX_LIMIT_TIER2` (constant, lines 249-249)
  - `MANAGER_CTX_LIMIT_TIER3` (constant, lines 250-250)
  - `MAX_CONTEXT_ARCHIVE_SEGMENTS` (constant, lines 251-251)
  - `MODEL_OUTPUT_RETRY_TIMES` (constant, lines 252-252)
  - `ARBITER_TRIGGER_MIN_CONTENT_CHARS` (constant, lines 253-253)
  - `ARBITER_VALID_PLANNING_STREAK_LIMIT` (constant, lines 254-254)
  - `ARBITER_DEFAULT_TIMEOUT_SECONDS` (constant, lines 255-255)
  - `ARBITER_DEFAULT_MAX_TOKENS` (constant, lines 256-256)
  - `ARBITER_DEFAULT_TEMPERATURE` (constant, lines 257-257)
  - `LIVE_INPUT_DELAY_WRITE_ROUNDS` (constant, lines 258-258)
  - `LIVE_INPUT_DELAY_TOOL_ROUNDS` (constant, lines 259-259)
  - `LIVE_INPUT_DELAY_NORMAL_ROUNDS` (constant, lines 260-260)
  - `LIVE_INPUT_MAX_INJECTIONS` (constant, lines 261-261)
  - `LIVE_INPUT_REINJECT_INTERVAL` (constant, lines 262-262)
  - `LIVE_INPUT_WEIGHT_BASE_DELAYED` (constant, lines 263-263)
  - `LIVE_INPUT_WEIGHT_BASE_NORMAL` (constant, lines 264-264)
  - `LIVE_INPUT_WEIGHT_STEP_DELAYED` (constant, lines 265-265)
  - `LIVE_INPUT_WEIGHT_STEP_NORMAL` (constant, lines 266-266)
  - `FINAL_SUMMARY_MIN_CHARS` (constant, lines 281-281)
  - `FINAL_SUMMARY_STRICT_MIN_CHARS` (constant, lines 282-282)
  - `RUNTIME_CONTROL_HINT_PREFIXES` (constant, lines 283-300)
  - `RETRY_RUNTIME_HINT_PREFIXES` (constant, lines 301-315)
  - `EXECUTION_MODE_SINGLE` (constant, lines 316-316)
  - `EXECUTION_MODE_SEQUENTIAL` (constant, lines 317-317)
  - `EXECUTION_MODE_SYNC` (constant, lines 318-318)
  - `EXECUTION_MODE_CHOICES` (constant, lines 319-323)
  - `AGENT_ROLES` (constant, lines 324-324)
  - `AGENT_BUBBLE_ROLES` (constant, lines 325-325)
  - `AGENT_ROLE_LABELS` (constant, lines 326-332)
  - `AGENT_ROLE_BUBBLE_COLORS` (constant, lines 333-339)
  - `BLACKBOARD_STATUSES` (constant, lines 340-349)
  - `TASK_COMPLEXITY_LEVELS` (constant, lines 350-350)
  - `TASK_PROFILE_TYPES` (constant, lines 351-357)
  - `TASK_LEVEL_CHOICES` (constant, lines 358-358)
  - `TASK_SCALE_PREFERENCES` (constant, lines 359-359)
  - `SEMANTIC_CONFIDENCE_CHOICES` (constant, lines 360-360)
  - `TASK_LEVEL_POLICIES` (constant, lines 361-407)
  - `MANAGER_ROUTE_TARGETS` (constant, lines 408-408)
  - `BLACKBOARD_MAX_LOG_ENTRIES` (constant, lines 409-409)
  - `BLACKBOARD_MAX_TEXT` (constant, lines 410-410)
  - `SKILL_REFRESH_MIN_INTERVAL_SECONDS` (constant, lines 411-411)
  - `SKILL_PROMPT_MAX_ITEMS` (constant, lines 412-412)
  - `SKILL_PROMPT_MAX_CHARS` (constant, lines 413-413)
  - `SKILL_RUNTIME_CACHE_MAX_ENTRIES` (constant, lines 414-414)
  - `SKILL_RUNTIME_CACHE_MAX_BYTES` (constant, lines 415-415)
  - `AUTO_SKILLS_ROOT_CANDIDATES` (constant, lines 416-416)
  - `SKILL_DEFAULT_ATTACHMENT_GLOBS` (constant, lines 417-447)
  - `SKILL_INLINE_ATTACHMENT_MAX_FILES` (constant, lines 448-448)
  - `SKILL_INLINE_ATTACHMENT_MAX_CHARS` (constant, lines 449-449)
  - `SKILL_RESOURCE_MANIFEST_MAX_ITEMS` (constant, lines 450-450)
  - `SKILL_BODY_COMPACT_THRESHOLD_CHARS` (constant, lines 451-451)
  - `SKILL_BODY_PREVIEW_CHARS` (constant, lines 452-452)
  - `SKILLS_VIRTUAL_PREFIX` (constant, lines 453-453)
  - `SKILLS_EXTERNAL_MOUNT` (constant, lines 454-454)
  - `PLAN_MODE_ENABLED_LEVELS` (constant, lines 455-455)
  - `PLAN_MODE_FORCED_LEVELS` (constant, lines 456-456)
  - `PLAN_MODE_USER_CHOICES` (constant, lines 457-457)
  - `TASK_PHASES` (constant, lines 459-459)
  - `TASK_PHASE_ROUTING` (constant, lines 460-467)
  - `COMPLEXITY_KEYWORDS` (constant, lines 469-474)
  - `USER_COMPLEXITY_SIMPLE_TOKENS` (constant, lines 475-479)
  - `USER_COMPLEXITY_COMPLEX_TOKENS` (constant, lines 480-484)
  - `PLAN_MODE_EXPLORER_MAX_ROUNDS` (constant, lines 485-485)
  - `REVIEWER_DEBUG_MODE_MAX_ROUNDS` (constant, lines 487-487)
  - `REVIEWER_DEBUG_TOOL_ALLOWLIST` (constant, lines 488-492)
  - `EXPLORER_STALL_THRESHOLD` (constant, lines 493-493)
  - `DEVELOPER_EDIT_STALL_THRESHOLD` (constant, lines 494-494)
  - `PLAN_MODE_MANAGER_SYNTHESIS_MAX_TOKENS` (constant, lines 495-495)
  - `PLAN_MODE_MAX_OPTIONS` (constant, lines 496-496)
  - `PLAN_FILE_RELATIVE_PATH` (constant, lines 497-497)
  - `PLAN_BUBBLE_MAX_CHARS` (constant, lines 498-498)
  - `PLAN_NOTICE_BODY_MAX_CHARS` (constant, lines 499-499)
  - `PLAN_MESSAGE_EVENT_MAX_CHARS` (constant, lines 500-500)
  - `PLAN_STEP_FULL_CONTENT_MAX_CHARS` (constant, lines 501-501)
  - `PLAN_MODE_RESEARCH_TOOL_ALLOWLIST` (constant, lines 502-506)
  - `FAILURE_LEDGER_MAX_FIXES` (constant, lines 507-507)
  - `FAILURE_LEDGER_MAX_COMPILE_ERRORS` (constant, lines 508-508)
  - `FAILURE_LEDGER_MAX_DELEGATIONS` (constant, lines 509-509)
  - `FAILURE_LEDGER_MAX_STALLS` (constant, lines 510-510)
  - `FAILURE_LEDGER_MAX_TOOL_FPS` (constant, lines 511-511)
  - `FAILURE_LEDGER_MAX_ERRORS` (constant, lines 512-512)
  - `ERROR_CATEGORY_DEFS` (constant, lines 515-552)
  - `CHECKPOINT_MAX_COUNT` (constant, lines 553-553)
  - `CHECKPOINT_INTERVAL_ROUNDS` (constant, lines 554-554)
  - `PERSISTED_ROUTES_MAX` (constant, lines 555-555)
  - `HTML_FRONTEND_REQUEST_KEYWORDS` (constant, lines 556-595)
  - `DEEP_RESEARCH_REQUEST_KEYWORDS` (constant, lines 596-618)
  - `DEEP_RESEARCH_RETRIEVAL_KEYWORDS` (constant, lines 619-638)
  - `DEEP_RESEARCH_TEXT_ONLY_HINT_KEYWORDS` (constant, lines 639-656)
  - `DANGEROUS_PATTERNS` (constant, lines 658-658)
  - `VALID_MSG_TYPES` (constant, lines 659-665)
  - `SUPPORTED_UI_LANGUAGES` (constant, lines 667-672)
  - `UI_LANGUAGE_LABELS` (constant, lines 673-673)
  - `DEFAULT_UI_LANGUAGE` (constant, lines 674-674)
  - `UI_STYLE_CHOICES` (constant, lines 675-675)
  - `UI_STYLE_LABELS` (constant, lines 676-676)
  - `DEFAULT_UI_STYLE` (constant, lines 677-677)
  - `DEFAULT_WEB_UI_DIR` (constant, lines 678-678)
  - `DEFAULT_WEB_UI_CONFIG` (constant, lines 679-679)
  - `WEB_UI_REQUIRED_FILES` (constant, lines 680-687)
  - `WEB_UI_OPTIONAL_FILES` (constant, lines 688-688)
  - `IMAGE_EXTS` (constant, lines 690-703)
  - `IMAGE_FORMATS_NEED_CONVERSION` (constant, lines 704-704)
  - `IMAGE_SAFE_FORMATS` (constant, lines 705-705)
  - `AUDIO_EXTS` (constant, lines 706-716)
  - `VIDEO_EXTS` (constant, lines 717-727)
  - `CODE_PREVIEW_STAGE_MAX_BYTES` (constant, lines 728-728)
  - `CODE_PREVIEW_STAGE_MAX_ROWS` (constant, lines 729-729)
  - `CODE_PREVIEW_STAGE_MAX_PER_FILE` (constant, lines 730-730)
  - `CODE_PREVIEW_STAGE_MAX_TOTAL` (constant, lines 731-731)
  - `RENDER_FRAME_MAX_B64_CHARS` (constant, lines 732-732)
  - `RENDER_FRAME_MAX_POINTS` (constant, lines 733-733)
  - `RENDER_FRAME_MAX_LINES` (constant, lines 734-734)
  - `RENDER_FRAME_MAX_LINE_POINTS` (constant, lines 735-735)
  - `RENDER_FRAME_ACTIVITY_INTERVAL_SECONDS` (constant, lines 736-736)
  - `RAW_TOOLCALL_TEXT_FILTER_THRESHOLD` (constant, lines 737-737)
  - `ASSISTANT_TEXT_PERSIST_MAX_CHARS` (constant, lines 738-738)
  - `ASSISTANT_MESSAGE_EVENT_MAX_CHARS` (constant, lines 739-739)
  - `CODE_PREVIEW_EXTS` (constant, lines 740-829)
  - `CODE_PREVIEW_FILENAMES` (constant, lines 830-841)
  - `MEDIA_CAPABILITY_KEYS` (constant, lines 842-849)
  - `SAMPLE_IMAGE_PNG_B64` (constant, lines 850-853)
  - `SAMPLE_AUDIO_WAV_B64` (constant, lines 854-856)
  - `SAMPLE_VIDEO_MP4_B64` (constant, lines 857-859)
  - `OFFLINE_JS_LIB_CATALOG` (constant, lines 861-1119)
  - `OFFLINE_JS_LIB_INDEX_FILE` (constant, lines 1120-1120)
  - `OFFLINE_JS_LIB_README_FILE` (constant, lines 1121-1121)
  - `BACKEND_I18N` (constant, lines 1307-1376)
  - `call_backend_i18n_en_update_l1378` (expression, lines 1378-1471)
  - `call_backend_i18n_zh_cn_update_l1472` (expression, lines 1472-1565)
  - `call_backend_i18n_zh_tw_update_l1566` (expression, lines 1566-1659)
  - `call_backend_i18n_ja_update_l1660` (expression, lines 1660-1753)
  - `OPENAI_COMPAT_PROVIDER_NAMES` (constant, lines 3457-3465)
  - `OPENAI_LIKE_PROVIDER_NAMES` (constant, lines 3467-3467)
  - `TABULAR_PREVIEW_EXTS` (constant, lines 4911-4911)
  - `EXCEL_PREVIEW_EXTS` (constant, lines 4912-4912)
  - `PRESENTATION_PREVIEW_EXTS` (constant, lines 4913-4913)
  - `DOCUMENT_PREVIEW_EXTS` (constant, lines 4914-4914)
  - `EMBEDDED_SKILLS_ARCHIVE_B64` (constant, lines 5428-5947)
  - `EMBEDDED_SKILLS_ARCHIVE_SHA256` (constant, lines 5948-5948)
  - `EMBEDDED_SKILLS_ARCHIVE_FILES` (constant, lines 5949-5972)
  - `BUILTIN_CLAWHUB_SKILLS_VERSION` (constant, lines 9130-9130)
  - `EMBEDDED_CLAWHUB_SKILLS_ARCHIVE_B64` (constant, lines 9132-9376)
  - `SKILL_PROTOCOL_LOCAL` (constant, lines 9435-9435)
  - `SKILL_PROTOCOL_CLAWHUB` (constant, lines 9436-9436)
  - `SKILL_PROTOCOL_HTTP_JSON` (constant, lines 9437-9437)
  - `SKILL_PROTOCOL_SPECS` (constant, lines 9439-9470)
  - `AGENT_TOOL_ALLOWLIST` (constant, lines 12635-12678)
  - `INDEX_HTML` (constant, lines 37514-37701)
  - `APP_CSS` (constant, lines 37703-38091)
  - `APP_JS` (constant, lines 38093-41195)
  - `APP_TS` (constant, lines 41197-41224)
  - `SKILLS_INDEX_HTML` (constant, lines 41226-41380)
  - `SKILLS_EXTRA_CSS` (constant, lines 41382-41477)
  - `SKILLS_APP_JS` (constant, lines 41479-41620)
  - `RAG_TERM_GROUPS` (constant, lines 41622-41632)
  - `RAG_RESEARCH_HINTS` (constant, lines 41633-41654)
  - `RAG_CODE_HINTS` (constant, lines 41655-41665)
  - `RAG_SHORT_TOKEN_ALLOWLIST` (constant, lines 41666-41681)
  - `RAG_EN_STOPWORDS` (constant, lines 41682-41754)
  - `RAG_ZH_STOPWORDS` (constant, lines 41755-41791)
  - `RAG_GENERIC_ENTITY_TERMS_EN` (constant, lines 41792-41870)
  - `RAG_GENERIC_ENTITY_TERMS_ZH` (constant, lines 41871-41913)
  - `RAG_STRUCTURAL_ENTITY_PATTERNS` (constant, lines 41914-41932)
  - `CODE_LIBRARY_IGNORED_DIRS` (constant, lines 42255-42260)
  - `CODE_LIBRARY_LANGUAGE_BY_EXT` (constant, lines 42261-42317)
  - `CODE_LIBRARY_SPECIAL_FILENAMES` (constant, lines 42318-42324)
  - `RAG_ADMIN_INDEX_HTML` (constant, lines 46931-47088)
  - `RAG_ADMIN_CSS` (constant, lines 47090-47180)
  - `RAG_ADMIN_JS` (constant, lines 47182-48408)
  - `CODE_ADMIN_INDEX_HTML` (constant, lines 48410-48419)
  - `CODE_ADMIN_CSS` (constant, lines 48420-48450)
  - `CODE_ADMIN_JS` (constant, lines 48451-48455)

### `config/paths.py`

- Routed symbols: 8
- Cross-module imports: `utils/text.py`: `trim`
- Symbols:
  - `SCRIPT_DIR` (constant, lines 54-54)
  - `_resolve_default_agent_workdir` (function, lines 56-60)
  - `_migrate_legacy_runtime_roots` (function, lines 62-90)
  - `WORKDIR` (constant, lines 92-92)
  - `CODES_ROOT` (constant, lines 93-93)
  - `LLM_CONFIG_PATH` (constant, lines 94-94)
  - `detect_repo_root` (function, lines 2331-2345)
  - `REPO_ROOT` (constant, lines 2347-2347)

### `config/settings.py`

- Routed symbols: 28
- Cross-module imports: `config/constants.py`: `AUTO_SKILLS_ROOT_CANDIDATES`, `BACKEND_I18N`, `DEFAULT_REQUEST_TIMEOUT`, `DEFAULT_UI_LANGUAGE`, `DEFAULT_UI_STYLE`, `DEFAULT_WEB_UI_CONFIG`, `DEFAULT_WEB_UI_DIR`, `EXECUTION_MODE_CHOICES`, `EXECUTION_MODE_SEQUENTIAL`, `EXECUTION_MODE_SINGLE`, `EXECUTION_MODE_SYNC`, `MEDIA_CAPABILITY_KEYS`, `SUPPORTED_UI_LANGUAGES`, `UI_LANGUAGE_LABELS`, `UI_STYLE_CHOICES`, `USER_COMPLEXITY_COMPLEX_TOKENS`, `USER_COMPLEXITY_SIMPLE_TOKENS`; `config/paths.py`: `WORKDIR`; `llm/utils.py`: `_is_http_url`, `_resolve_local_path`, `complete_chat_endpoint`, `extract_base_url`, `is_openai_like_provider`, `normalize_openai_compat_provider_name`, `strip_thinking_content`; `skills/store.py`: `ensure_embedded_skills`; `utils/json_utils.py`: `parse_json_object`; `utils/misc.py`: `MAX_TIMEOUT_SECONDS`, `MIN_TIMEOUT_SECONDS`, `normalize_timeout_seconds`, `sanitize_profile_id`; `utils/text.py`: `trim`
- Symbols:
  - `normalize_ui_language` (function, lines 1205-1227)
  - `normalize_ui_style` (function, lines 1230-1247)
  - `supported_ui_languages_payload` (function, lines 1250-1251)
  - `normalize_execution_mode` (function, lines 1254-1273)
  - `model_language_instruction` (function, lines 1276-1304)
  - `backend_i18n_text` (function, lines 1756-1766)
  - `backend_role_label` (function, lines 1769-1773)
  - `_detect_os_shell_instruction` (function, lines 1776-1815)
  - `resolve_web_ui_dir_path` (function, lines 1817-1824)
  - `resolve_optional_file_path` (function, lines 1827-1834)
  - `resolve_skills_root_path` (function, lines 1837-1844)
  - `_count_skill_markdown_files` (function, lines 1847-1858)
  - `select_preferred_skills_root` (function, lines 1861-1895)
  - `load_web_ui_config_file` (function, lines 1898-1912)
  - `extract_show_upload_list_setting` (function, lines 1915-1929)
  - `extract_ui_style_setting` (function, lines 1932-1946)
  - `extract_js_lib_download_setting` (function, lines 1949-1968)
  - `extract_daily_session_limit_setting` (function, lines 1971-2014)
  - `default_multimodal_capabilities` (function, lines 2023-2031)
  - `_to_bool_like` (function, lines 2034-2044)
  - `infer_model_multimodal_capabilities` (function, lines 2047-2091)
  - `parse_capability_overrides` (function, lines 2094-2131)
  - `merge_multimodal_capabilities` (function, lines 2134-2141)
  - `parse_media_endpoints` (function, lines 2144-2158)
  - `infer_user_complexity_value` (function, lines 3428-3438)
  - `load_llm_config_from_source` (function, lines 3582-3616)
  - `parse_llm_config_profiles` (function, lines 3618-4204)
  - `looks_like_llm_config` (function, lines 4206-4280)

### `llm/client.py`

- Routed symbols: 2
- Cross-module imports: `config/constants.py`: `DEFAULT_REQUEST_TIMEOUT`, `OLLAMA_THINKING_TOOL_BUFFER`, `SAMPLE_AUDIO_WAV_B64`, `SAMPLE_IMAGE_PNG_B64`, `SAMPLE_VIDEO_MP4_B64`; `config/settings.py`: `default_multimodal_capabilities`, `infer_model_multimodal_capabilities`, `merge_multimodal_capabilities`, `parse_capability_overrides`, `parse_media_endpoints`; `llm/utils.py`: `complete_chat_endpoint`, `is_openai_compat_provider`, `is_openai_like_provider`, `split_thinking_content`; `utils/json_utils.py`: `canonicalize_tool_name`, `json_dumps`, `parse_json_object`, `parse_tool_arguments`, `parse_tool_arguments_with_error`; `utils/misc.py`: `MAX_TIMEOUT_SECONDS`, `MIN_TIMEOUT_SECONDS`, `make_id`, `normalize_timeout_seconds`, `now_ts`; `utils/text.py`: `trim`
- Symbols:
  - `OllamaError` (class, lines 11340-11343)
  - `OllamaClient` (class, lines 11345-12397)

### `llm/utils.py`

- Routed symbols: 25
- Cross-module imports: `config/constants.py`: `OPENAI_COMPAT_PROVIDER_NAMES`, `OPENAI_LIKE_PROVIDER_NAMES`; `utils/json_utils.py`: `json_dumps`, `parse_json_object`; `utils/text.py`: `trim`
- Symbols:
  - `probe_ollama_environment` (function, lines 3114-3127)
  - `list_ollama_models` (function, lines 3129-3131)
  - `_OLLAMA_TAG_CACHE_LOCK` (assignment, lines 3133-3133)
  - `_OLLAMA_TAG_CACHE` (assignment, lines 3134-3134)
  - `list_ollama_models_cached` (function, lines 3144-3181)
  - `resolve_ollama_model` (function, lines 3183-3193)
  - `infer_thinking_model` (function, lines 3195-3197)
  - `split_thinking_content` (function, lines 3199-3240)
  - `strip_thinking_content` (function, lines 3242-3243)
  - `check_ollama_model_ready` (function, lines 3245-3269)
  - `list_loaded_ollama_models` (function, lines 3271-3284)
  - `wake_ollama_model` (function, lines 3286-3316)
  - `try_pull_ollama_model` (function, lines 3318-3336)
  - `ordered_model_candidates` (function, lines 3338-3356)
  - `pick_working_ollama_model` (function, lines 3358-3374)
  - `extract_base_url` (function, lines 3407-3415)
  - `complete_chat_endpoint` (function, lines 3417-3426)
  - `normalize_openai_compat_provider_name` (function, lines 3440-3455)
  - `is_openai_compat_provider` (function, lines 3469-3470)
  - `is_openai_like_provider` (function, lines 3472-3473)
  - `openai_compat_probe_headers` (function, lines 3475-3486)
  - `openai_compat_model_list_urls` (function, lines 3488-3520)
  - `extract_openai_compat_model_ids` (function, lines 3522-3555)
  - `_is_http_url` (function, lines 3557-3562)
  - `_resolve_local_path` (function, lines 3564-3580)

### `rag/index.py`

- Routed symbols: 5
- Cross-module imports: `config/constants.py`: `RAG_DYNAMIC_NOISE_HARD_COMMUNITY_RATIO`, `RAG_DYNAMIC_NOISE_HARD_DOC_RATIO`, `RAG_DYNAMIC_NOISE_MIN_COMMUNITY_FREQ`, `RAG_DYNAMIC_NOISE_MIN_DOC_FREQ`, `RAG_DYNAMIC_NOISE_SOFT_COMMUNITY_RATIO`, `RAG_DYNAMIC_NOISE_SOFT_DOC_RATIO`, `RAG_EN_STOPWORDS`, `RAG_GRAPH_MAX_NODES`, `RAG_INCLUDE_FILENAME_ENTITIES_DEFAULT`, `RAG_MAX_COMMUNITY_MAP_SUPPORT`, `RAG_MAX_GLOBAL_COMMUNITIES`, `RAG_MAX_QUERY_RESULTS`; `rag/parsers.py`: `_code_is_test_path`, `_rag_apply_filename_entity_policy`, `_rag_choose_community`, `_rag_classify_document`, `_rag_expand_tokens`, `_rag_extract_entities`, `_rag_filter_entities`, `_rag_tokenize`; `utils/json_utils.py`: `json_dumps`; `utils/misc.py`: `now_ts`; `utils/text.py`: `trim`
- Symbols:
  - `_code_module_name` (function, lines 42351-42365)
  - `_code_choose_community` (function, lines 42368-42375)
  - `_code_query_terms` (function, lines 42378-42390)
  - `TFGraphIDFIndex` (class, lines 43366-44724)
  - `CodeGraphIndex` (class, lines 46164-46576)

### `rag/ingestion.py`

- Routed symbols: 3
- Cross-module imports: `config/constants.py`: `CODE_IMPORT_WORKER_COUNT`, `CODE_LIBRARY_IGNORED_DIRS`, `CODE_PARSE_TIMEOUT_SECONDS`, `RAG_IMPORT_WORKER_COUNT`, `RAG_MAX_IMPORT_BATCH_ITEMS`, `RAG_MAX_IMPORT_FILES`, `RAG_MODEL_MEDIA_MAX_BYTES`, `RAG_PARSE_TIMEOUT_SECONDS`, `RAG_PDF_IMAGE_LIMIT`; `config/settings.py`: `default_multimodal_capabilities`; `rag/parsers.py`: `CodeContentParser`, `RAGContentParser`, `_rag_extract_entities`, `_rag_safe_name`; `rag/store.py`: `CodeLibraryStore`, `RAGLibraryStore`; `session/state.py`: `SessionState`; `utils/files.py`: `try_read_text`; `utils/json_utils.py`: `_read_json_file`, `_write_json_file`, `parse_json_object`; `utils/media.py`: `guess_mime_from_name`; `utils/misc.py`: `make_id`, `now_ts`; `utils/text.py`: `trim`
- Symbols:
  - `_rag_parse_file_worker` (function, lines 45277-45291)
  - `RAGIngestionService` (class, lines 45294-46161)
  - `CodeIngestionService` (class, lines 46845-46929)

### `rag/parsers.py`

- Routed symbols: 22
- Cross-module imports: `config/constants.py`: `AUDIO_EXTS`, `CODE_CHUNK_CHARS`, `CODE_CHUNK_OVERLAP`, `CODE_LIBRARY_LANGUAGE_BY_EXT`, `CODE_LIBRARY_SPECIAL_FILENAMES`, `CODE_MAX_CHUNKS_PER_DOC`, `CODE_PREVIEW_EXTS`, `CODE_PREVIEW_FILENAMES`, `CODE_PREVIEW_STAGE_MAX_ROWS`, `DOCUMENT_PREVIEW_EXTS`, `EXCEL_PREVIEW_EXTS`, `IMAGE_EXTS`, `PRESENTATION_PREVIEW_EXTS`, `RAG_CHUNK_CHARS`, `RAG_CHUNK_OVERLAP`, `RAG_CODE_HINTS`, `RAG_EN_STOPWORDS`, `RAG_GENERIC_ENTITY_TERMS_EN`, `RAG_GENERIC_ENTITY_TERMS_ZH`, `RAG_INCLUDE_FILENAME_ENTITIES_DEFAULT`, `RAG_MAX_CHUNKS_PER_DOC`, `RAG_PDF_IMAGE_LIMIT`, `RAG_RESEARCH_HINTS`, `RAG_SHORT_TOKEN_ALLOWLIST`, `RAG_STRUCTURAL_ENTITY_PATTERNS`, `RAG_TERM_GROUPS`, `RAG_ZH_STOPWORDS`, `TABULAR_PREVIEW_EXTS`, `VIDEO_EXTS`; `utils/files.py`: `_sha256_bytes`, `_sha256_file`; `utils/json_utils.py`: `parse_json_object`; `utils/media.py`: `guess_mime_from_name`; `utils/text.py`: `_compress_rows_keep_hotspot`, `_skip_row`, `trim`
- Symbols:
  - `normalize_rel_preview_path` (function, lines 4886-4897)
  - `is_code_preview_candidate` (function, lines 4900-4908)
  - `preview_kind_for_path` (function, lines 4917-4944)
  - `build_code_preview_rows` (function, lines 4947-5131)
  - `_rag_safe_name` (function, lines 41935-41938)
  - `_rag_detect_language` (function, lines 41941-41955)
  - `_rag_cjk_ngrams` (function, lines 41958-41970)
  - `_rag_is_noise_token` (function, lines 41973-41992)
  - `_rag_entity_allowed` (function, lines 41995-42007)
  - `_rag_filter_entities` (function, lines 42010-42024)
  - `_rag_filename_entity_aliases` (function, lines 42027-42060)
  - `_rag_apply_filename_entity_policy` (function, lines 42063-42093)
  - `_rag_choose_community` (function, lines 42096-42113)
  - `_rag_tokenize` (function, lines 42116-42146)
  - `_rag_expand_tokens` (function, lines 42149-42163)
  - `_rag_extract_entities` (function, lines 42166-42182)
  - `_rag_classify_document` (function, lines 42185-42219)
  - `_rag_chunk_text` (function, lines 42222-42252)
  - `_code_language_from_name` (function, lines 42327-42343)
  - `_code_is_test_path` (function, lines 42346-42348)
  - `CodeContentParser` (class, lines 42393-42853)
  - `RAGContentParser` (class, lines 42856-43363)

### `rag/store.py`

- Routed symbols: 2
- Cross-module imports: `config/constants.py`: `CODE_CHUNK_CHARS`, `CODE_CHUNK_OVERLAP`, `CODE_MAX_CHUNKS_PER_DOC`, `RAG_INCLUDE_FILENAME_ENTITIES_DEFAULT`, `RAG_TASK_HISTORY_LIMIT`; `rag/index.py`: `CodeGraphIndex`, `TFGraphIDFIndex`, `_code_choose_community`, `_code_module_name`; `rag/parsers.py`: `_code_is_test_path`, `_rag_apply_filename_entity_policy`, `_rag_choose_community`, `_rag_chunk_text`, `_rag_entity_allowed`, `_rag_extract_entities`, `_rag_safe_name`; `utils/files.py`: `_sha256_bytes`, `_sha256_file`; `utils/json_utils.py`: `_read_json_file`, `_write_json_file`; `utils/media.py`: `guess_mime_from_name`; `utils/misc.py`: `make_id`, `now_ts`; `utils/text.py`: `trim`
- Symbols:
  - `RAGLibraryStore` (class, lines 44727-45274)
  - `CodeLibraryStore` (class, lines 46579-46842)

### `server/handlers.py`

- Routed symbols: 5
- Cross-module imports: `app/context.py`: `AppContext`; `config/constants.py`: `APP_VERSION`, `DEFAULT_REQUEST_TIMEOUT`, `DEFAULT_UI_LANGUAGE`, `DEFAULT_UI_STYLE`, `EXECUTION_MODE_CHOICES`, `EXECUTION_MODE_SYNC`, `MIN_RUN_TIMEOUT_SECONDS`, `PLAN_MODE_USER_CHOICES`, `RAG_GRAPH_MAX_NODES`, `SSE_HEARTBEAT_SECONDS`, `TASK_COMPLEXITY_LEVELS`, `TASK_LEVEL_CHOICES`, `TASK_LEVEL_POLICIES`, `UI_STYLE_LABELS`; `config/paths.py`: `LLM_CONFIG_PATH`, `REPO_ROOT`, `WORKDIR`; `config/settings.py`: `_to_bool_like`, `infer_user_complexity_value`, `looks_like_llm_config`, `normalize_execution_mode`, `normalize_ui_language`, `normalize_ui_style`, `resolve_web_ui_dir_path`, `supported_ui_languages_payload`; `llm/utils.py`: `extract_base_url`, `extract_openai_compat_model_ids`, `list_ollama_models`, `normalize_openai_compat_provider_name`, `openai_compat_model_list_urls`, `openai_compat_probe_headers`; `session/manager.py`: `SessionCreationLimitExceeded`, `SessionManager`; `session/state.py`: `SessionState`; `skills/store.py`: `analyze_skill_building_knowledge`; `utils/files.py`: `safe_path`, `try_read_text`; `utils/json_utils.py`: `json_dumps`, `parse_json_object`; `utils/media.py`: `guess_mime_from_name`; `utils/misc.py`: `now_ts`, `swallow_benign_socket_error`, `user_id_from_ip`; `utils/text.py`: `trim`
- Symbols:
  - `AgentHTTPServer` (class, lines 50875-50903)
  - `Handler` (class, lines 50905-51745)
  - `SkillsHandler` (class, lines 51747-51942)
  - `RagAdminHandler` (class, lines 51944-52098)
  - `CodeAdminHandler` (class, lines 52101-52255)

### `session/manager.py`

- Routed symbols: 2
- Cross-module imports: `config/constants.py`: `AGENT_MAX_OUTPUT_TOKENS`, `ARBITER_DEFAULT_MAX_TOKENS`, `ARBITER_DEFAULT_TEMPERATURE`, `ARBITER_DEFAULT_TIMEOUT_SECONDS`, `DEFAULT_REQUEST_TIMEOUT`, `DEFAULT_UI_LANGUAGE`, `EXECUTION_MODE_SYNC`, `MAX_AGENT_ROUNDS`, `MAX_AGENT_ROUNDS_CAP`, `MAX_RUN_SECONDS`, `MAX_RUN_TIMEOUT_SECONDS`, `MIN_AGENT_ROUNDS`, `MIN_CONTEXT_TOKEN_LIMIT`, `MIN_RUN_TIMEOUT_SECONDS`, `TOKEN_THRESHOLD`; `config/paths.py`: `LLM_CONFIG_PATH`; `config/settings.py`: `infer_model_multimodal_capabilities`, `merge_multimodal_capabilities`, `normalize_execution_mode`, `normalize_ui_language`, `parse_capability_overrides`, `parse_llm_config_profiles`; `llm/client.py`: `OllamaClient`; `llm/utils.py`: `complete_chat_endpoint`, `extract_base_url`, `is_openai_compat_provider`, `list_ollama_models_cached`, `probe_ollama_environment`; `session/state.py`: `SessionState`; `utils/crypto.py`: `CryptoBox`; `utils/files.py`: `try_read_text`; `utils/json_utils.py`: `parse_json_object`; `utils/misc.py`: `make_id`, `normalize_timeout_seconds`, `now_ts`, `sanitize_profile_id`
- Symbols:
  - `SessionCreationLimitExceeded` (class, lines 2017-2020)
  - `SessionManager` (class, lines 36640-37512)

### `session/state.py`

- Routed symbols: 1
- Cross-module imports: `agent/background.py`: `BackgroundManager`; `agent/bus.py`: `MessageBus`; `agent/events.py`: `EventHub`; `agent/tasks.py`: `TaskManager`; `agent/todo.py`: `TodoManager`; `agent/worktree.py`: `WorktreeManager`; `config/constants.py`: `AGENT_BUBBLE_ROLES`, `AGENT_CTX_LIMIT_TIER0`, `AGENT_CTX_LIMIT_TIER1`, `AGENT_CTX_LIMIT_TIER2`, `AGENT_CTX_LIMIT_TIER3`, `AGENT_MAX_OUTPUT_TOKENS`, `AGENT_MSG_LIMIT_TIER0`, `AGENT_MSG_LIMIT_TIER1`, `AGENT_MSG_LIMIT_TIER2`, `AGENT_MSG_LIMIT_TIER3`, `AGENT_ROLES`, `AGENT_TOOL_ALLOWLIST`, `ARBITER_DEFAULT_MAX_TOKENS`, `ARBITER_DEFAULT_TEMPERATURE`, `ARBITER_DEFAULT_TIMEOUT_SECONDS`, `ARBITER_TRIGGER_MIN_CONTENT_CHARS`, `ARBITER_VALID_PLANNING_STREAK_LIMIT`, `ASSISTANT_MESSAGE_EVENT_MAX_CHARS`, `ASSISTANT_TEXT_PERSIST_MAX_CHARS`, `AUDIO_EXTS`, `AUTO_CONTINUE_BUDGET_DEFAULT`, `BASH_READ_LOOP_THRESHOLD`, `BLACKBOARD_MAX_LOG_ENTRIES`, `BLACKBOARD_MAX_TEXT`, `BLACKBOARD_STATUSES`, `CHECKPOINT_INTERVAL_ROUNDS`, `CHECKPOINT_MAX_COUNT`, `CODE_PREVIEW_STAGE_MAX_BYTES`, `CODE_PREVIEW_STAGE_MAX_PER_FILE`, `CODE_PREVIEW_STAGE_MAX_ROWS`, `CODE_PREVIEW_STAGE_MAX_TOTAL`, `COMPACT_TIER1_ABS`, `COMPACT_TIER1_PCT`, `COMPACT_TIER2_ABS`, `COMPACT_TIER2_PCT`, `COMPACT_TIER3_PCT`, `DANGEROUS_PATTERNS`, `DEEP_RESEARCH_REQUEST_KEYWORDS`, `DEEP_RESEARCH_RETRIEVAL_KEYWORDS`, `DEEP_RESEARCH_TEXT_ONLY_HINT_KEYWORDS`, `DEFAULT_REQUEST_TIMEOUT`, `DEFAULT_UI_LANGUAGE`, `DEVELOPER_EDIT_STALL_THRESHOLD`, `EMPTY_ACTION_MIN_CONTENT_CHARS`, `EMPTY_ACTION_WAKEUP_RETRY_LIMIT`, `ERROR_CATEGORY_DEFS`, `EXECUTION_MODE_CHOICES`, `EXECUTION_MODE_SEQUENTIAL`, `EXECUTION_MODE_SINGLE`, `EXECUTION_MODE_SYNC`, `EXPLORER_STALL_THRESHOLD`, `FAILURE_LEDGER_MAX_COMPILE_ERRORS`, `FAILURE_LEDGER_MAX_DELEGATIONS`, `FAILURE_LEDGER_MAX_ERRORS`, `FAILURE_LEDGER_MAX_FIXES`, `FAILURE_LEDGER_MAX_STALLS`, `FAILURE_LEDGER_MAX_TOOL_FPS`, `FILE_BUFFER_CONTENT_THRESHOLD`, `FILE_BUFFER_MAX_FILES`, `FINAL_SUMMARY_MIN_CHARS`, `FINAL_SUMMARY_STRICT_MIN_CHARS`, `FUSED_FAULT_BREAK_THRESHOLD`, `HARD_BREAK_RECOVERY_ROUND_THRESHOLD`, `HARD_BREAK_TOOL_ERROR_THRESHOLD`, `HTML_FRONTEND_REQUEST_KEYWORDS`, `IMAGE_EXTS`, `IMAGE_FORMATS_NEED_CONVERSION`, `LIVE_INPUT_DELAY_NORMAL_ROUNDS`, `LIVE_INPUT_DELAY_TOOL_ROUNDS`, `LIVE_INPUT_DELAY_WRITE_ROUNDS`, `LIVE_INPUT_MAX_INJECTIONS`, `LIVE_INPUT_REINJECT_INTERVAL`, `LIVE_INPUT_WEIGHT_BASE_DELAYED`, `LIVE_INPUT_WEIGHT_BASE_NORMAL`, `LIVE_INPUT_WEIGHT_STEP_DELAYED`, `LIVE_INPUT_WEIGHT_STEP_NORMAL`, `LONG_OUTPUT_LISTING_OFFLOAD_CHARS`, `LONG_OUTPUT_MODEL_PAGE_CHARS`, `LONG_OUTPUT_READ_PAGE_LINES`, `LONG_OUTPUT_READ_PAGE_MAX_CHARS`, `LONG_OUTPUT_TEMP_MAX_FILES`, `LONG_OUTPUT_UI_PAGE_CHARS`, `LONG_OUTPUT_UI_PREVIEW_MAX_PAGES`, `MANAGER_CTX_LIMIT_TIER0`, `MANAGER_CTX_LIMIT_TIER1`, `MANAGER_CTX_LIMIT_TIER2`, `MANAGER_CTX_LIMIT_TIER3`, `MANAGER_ROUTE_TARGETS`, `MAX_AGENT_ROUNDS`, `MAX_AGENT_ROUNDS_CAP`, `MAX_CONTEXT_ARCHIVE_SEGMENTS`, `MAX_RUN_SECONDS`, `MAX_RUN_TIMEOUT_SECONDS`, `MIN_AGENT_ROUNDS`, `MIN_CONTEXT_TOKEN_LIMIT`, `MIN_RUN_TIMEOUT_SECONDS`, `MODEL_CALL_PROGRESS_DELAY`, `MODEL_CALL_PROGRESS_INTERVAL`, `MODEL_OUTPUT_RETRY_TIMES`, `PERSISTED_ROUTES_MAX`, `PLAN_BUBBLE_MAX_CHARS`, `PLAN_FILE_RELATIVE_PATH`, `PLAN_MESSAGE_EVENT_MAX_CHARS`, `PLAN_MODE_ENABLED_LEVELS`, `PLAN_MODE_EXPLORER_MAX_ROUNDS`, `PLAN_MODE_FORCED_LEVELS`, `PLAN_MODE_MANAGER_SYNTHESIS_MAX_TOKENS`, `PLAN_MODE_MAX_OPTIONS`, `PLAN_MODE_RESEARCH_TOOL_ALLOWLIST`, `PLAN_MODE_USER_CHOICES`, `PLAN_NOTICE_BODY_MAX_CHARS`, `PLAN_STEP_FULL_CONTENT_MAX_CHARS`, `RENDER_FRAME_ACTIVITY_INTERVAL_SECONDS`, `RENDER_FRAME_MAX_B64_CHARS`, `RENDER_FRAME_MAX_LINES`, `RENDER_FRAME_MAX_LINE_POINTS`, `RENDER_FRAME_MAX_POINTS`, `REPEATED_TOOL_LOOP_THRESHOLD`, `RETRY_RUNTIME_HINT_PREFIXES`, `REVIEWER_DEBUG_MODE_MAX_ROUNDS`, `RUNTIME_CONTROL_HINT_PREFIXES`, `SEMANTIC_CONFIDENCE_CHOICES`, `SKILLS_VIRTUAL_PREFIX`, `SKILL_REFRESH_MIN_INTERVAL_SECONDS`, `SKILL_RUNTIME_CACHE_MAX_BYTES`, `SKILL_RUNTIME_CACHE_MAX_ENTRIES`, `STALL_ESCALATION_CONTEXT_MAX_CHARS`, `STALL_ESCALATION_MIN_LEVEL`, `STALL_PLAN_SYNTHESIS_MAX_TOKENS`, `STALL_SEVERITY_DECAY_ON_SUCCESS`, `STALL_SEVERITY_ESCALATION_THRESHOLD`, `STALL_SEVERITY_WEIGHT_BASH_READ_LOOP`, `STALL_SEVERITY_WEIGHT_FAULT`, `STALL_SEVERITY_WEIGHT_RECOVERY_RETRY`, `STALL_SEVERITY_WEIGHT_REPEATED_TOOL`, `STALL_SEVERITY_WEIGHT_WATCHDOG`, `TASK_COMPLEXITY_LEVELS`, `TASK_LEVEL_CHOICES`, `TASK_LEVEL_POLICIES`, `TASK_PHASE_ROUTING`, `TASK_PROFILE_TYPES`, `TASK_SCALE_PREFERENCES`, `THINKING_BUDGET_FORCE_RATIO`, `TOKEN_THRESHOLD`, `TRUNCATION_CONTINUATION_ECHO_CHARS`, `TRUNCATION_CONTINUATION_MAX_PASSES`, `TRUNCATION_CONTINUATION_MAX_TOKENS`, `TRUNCATION_CONTINUATION_TAIL_CHARS`, `TRUNCATION_LIVE_BUFFER_MAX_CHARS`, `TRUNCATION_OVERLAP_SCAN_CHARS`, `TRUNCATION_PAIR_SCAN_CHARS`, `VIDEO_EXTS`, `WATCHDOG_CONTEXT_NEAR_RATIO`, `WATCHDOG_CONTEXT_STALL_THRESHOLD`, `WATCHDOG_INTENT_NO_TOOL_THRESHOLD`, `WATCHDOG_INTENT_NO_TOOL_THRESHOLD_SINGLE`, `WATCHDOG_MAX_DECOMPOSE_STEPS`, `WATCHDOG_REPEAT_NO_TOOL_THRESHOLD`, `WATCHDOG_REPEAT_NO_TOOL_THRESHOLD_SINGLE`, `WATCHDOG_REPEAT_SIMILARITY_THRESHOLD`, `WATCHDOG_STATE_STALL_THRESHOLD`, `WATCHDOG_STEP_MAX_ATTEMPTS`, `_DEFAULT_TOOL_TIMEOUT`, `_TOOL_TIMEOUT_MAP`; `config/paths.py`: `WORKDIR`; `config/settings.py`: `_detect_os_shell_instruction`, `_to_bool_like`, `backend_i18n_text`, `backend_role_label`, `default_multimodal_capabilities`, `infer_model_multimodal_capabilities`, `infer_user_complexity_value`, `looks_like_llm_config`, `merge_multimodal_capabilities`, `model_language_instruction`, `normalize_execution_mode`, `normalize_ui_language`, `parse_capability_overrides`, `parse_llm_config_profiles`; `llm/client.py`: `OllamaClient`, `OllamaError`; `llm/utils.py`: `complete_chat_endpoint`, `extract_base_url`, `is_openai_compat_provider`, `list_loaded_ollama_models`, `list_ollama_models`, `list_ollama_models_cached`, `probe_ollama_environment`, `resolve_ollama_model`, `split_thinking_content`, `strip_thinking_content`, `wake_ollama_model`; `rag/parsers.py`: `build_code_preview_rows`, `is_code_preview_candidate`, `normalize_rel_preview_path`, `preview_kind_for_path`; `skills/store.py`: `SkillStore`, `ensure_runtime_skills`; `utils/compress.py`: `compress_text_blob`, `decompress_text_blob`; `utils/crypto.py`: `CryptoBox`; `utils/errors.py`: `CircuitBreakerTriggered`, `EmptyActionError`; `utils/files.py`: `_normalize_external_js_url`, `_safe_js_filename`, `cache_external_js_url`, `ensure_offline_js_libs`, `is_external_js_src`, `load_offline_js_lib_index`, `match_offline_js_catalog_by_url`, `offline_js_lib_root`, `safe_path`, `try_read_text`; `utils/json_utils.py`: `TOOLS`, `TOOL_REQUIRED_ARGS`, `canonicalize_tool_name`, `extract_json_object_from_text`, `json_dumps`, `parse_json_object`, `repair_truncated_json_object`, `tool_def`; `utils/media.py`: `_convert_image_to_safe_format`, `guess_ext_from_mime`, `guess_mime_from_name`; `utils/misc.py`: `MAX_TIMEOUT_SECONDS`, `MIN_TIMEOUT_SECONDS`, `is_benign_socket_error`, `make_id`, `normalize_timeout_seconds`, `now_ts`, `sanitize_profile_id`; `utils/text.py`: `MAX_TOOL_OUTPUT`, `_fmt_export_ts`, `_html_esc`, `_text_to_minimal_pdf`, `filter_runtime_noise_lines`, `make_numbered_diff`, `make_unified_diff`, `normalize_work_text`, `parse_front_matter`, `render_numbered_diff_text`, `trim`
- Symbols:
  - `SessionState` (class, lines 12680-36638)

### `skills/store.py`

- Routed symbols: 26
- Cross-module imports: `config/constants.py`: `BUILTIN_CLAWHUB_SKILLS_VERSION`, `EMBEDDED_CLAWHUB_SKILLS_ARCHIVE_B64`, `EMBEDDED_SKILLS_ARCHIVE_B64`, `EMBEDDED_SKILLS_ARCHIVE_FILES`, `EMBEDDED_SKILLS_ARCHIVE_SHA256`, `SKILLS_EXTERNAL_MOUNT`, `SKILLS_VIRTUAL_PREFIX`, `SKILL_BODY_COMPACT_THRESHOLD_CHARS`, `SKILL_BODY_PREVIEW_CHARS`, `SKILL_DEFAULT_ATTACHMENT_GLOBS`, `SKILL_INLINE_ATTACHMENT_MAX_CHARS`, `SKILL_INLINE_ATTACHMENT_MAX_FILES`, `SKILL_PROMPT_MAX_CHARS`, `SKILL_PROMPT_MAX_ITEMS`, `SKILL_PROTOCOL_CLAWHUB`, `SKILL_PROTOCOL_HTTP_JSON`, `SKILL_PROTOCOL_LOCAL`, `SKILL_PROTOCOL_SPECS`, `SKILL_REFRESH_MIN_INTERVAL_SECONDS`, `SKILL_RESOURCE_MANIFEST_MAX_ITEMS`; `config/paths.py`: `WORKDIR`; `llm/utils.py`: `_is_http_url`; `utils/files.py`: `_render_offline_js_catalog_md`, `safe_path`, `try_read_text`; `utils/json_utils.py`: `json_dumps`, `parse_json_object`; `utils/misc.py`: `_meta_string_list`, `_module_exists`, `now_ts`; `utils/text.py`: `parse_front_matter`, `trim`
- Symbols:
  - `ensure_embedded_skills_at_root` (function, lines 5975-6027)
  - `ensure_embedded_skills` (function, lines 6030-6031)
  - `detect_upload_parser_capabilities` (function, lines 6039-6054)
  - `_render_cap_markdown` (function, lines 6056-6070)
  - `_write_text_if_changed` (function, lines 6072-6077)
  - `ensure_generated_document_skills` (function, lines 6079-6167)
  - `ensure_generated_image_coding_feedback_skill` (function, lines 6169-6268)
  - `_skill_knowledge_files` (function, lines 6270-6289)
  - `analyze_skill_building_knowledge` (function, lines 6291-6345)
  - `_sanitize_skill_slug` (function, lines 6347-6349)
  - `_build_skills_gen_skill_content` (function, lines 6351-6382)
  - `ensure_generated_skills_gen_skill` (function, lines 6384-6388)
  - `ensure_generated_execution_recovery_skill` (function, lines 6390-6468)
  - `ensure_generated_systematic_debugging_skill` (function, lines 6470-6742)
  - `ensure_generated_code_engineering_mastery_skill` (function, lines 6744-6862)
  - `ensure_generated_smart_file_navigation_skill` (function, lines 6864-6982)
  - `ensure_generated_html_frontend_report_skills` (function, lines 6984-7189)
  - `ensure_generated_deep_research_skills` (function, lines 7191-7459)
  - `ensure_generated_research_scientific_skills` (function, lines 7461-8097)
  - `ensure_generated_rag_mastery_skills` (function, lines 8103-8399)
  - `ensure_generated_multimodal_comprehension_skills` (function, lines 8405-9094)
  - `ensure_generated_runtime_skills_manifest` (function, lines 9097-9128)
  - `ensure_embedded_clawhub_skills` (function, lines 9379-9416)
  - `ensure_runtime_skills` (function, lines 9418-9433)
  - `_BUILTIN_SKILLS` (assignment, lines 9475-9563)
  - `SkillStore` (class, lines 9565-10859)

### `utils/compress.py`

- Routed symbols: 2
- Cross-module imports: none
- Symbols:
  - `compress_text_blob` (function, lines 2972-2977)
  - `decompress_text_blob` (function, lines 2979-2987)

### `utils/crypto.py`

- Routed symbols: 1
- Cross-module imports: `utils/json_utils.py`: `json_dumps`
- Symbols:
  - `CryptoBox` (class, lines 4290-4407)

### `utils/errors.py`

- Routed symbols: 2
- Cross-module imports: none
- Symbols:
  - `EmptyActionError` (class, lines 3137-3138)
  - `CircuitBreakerTriggered` (class, lines 3141-3142)

### `utils/files.py`

- Routed symbols: 25
- Cross-module imports: `config/constants.py`: `OFFLINE_JS_LIB_CATALOG`, `OFFLINE_JS_LIB_INDEX_FILE`, `OFFLINE_JS_LIB_README_FILE`; `config/paths.py`: `WORKDIR`; `utils/json_utils.py`: `json_dumps`; `utils/misc.py`: `now_ts`; `utils/text.py`: `trim`
- Symbols:
  - `_normalize_js_lib_asset_ref` (function, lines 1124-1137)
  - `_resolve_js_lib_asset_path` (function, lines 1140-1169)
  - `_discover_extra_js_lib_files` (function, lines 1172-1202)
  - `safe_path` (function, lines 2349-2358)
  - `_safe_js_filename` (function, lines 2360-2367)
  - `_sha256_bytes` (function, lines 2369-2370)
  - `_sha256_file` (function, lines 2372-2380)
  - `_download_http_bytes` (function, lines 2382-2390)
  - `offline_js_lib_root` (function, lines 2392-2393)
  - `_offline_js_entry_relative_path` (function, lines 2395-2399)
  - `_archive_member_relative_path` (function, lines 2401-2410)
  - `_path_size_bytes` (function, lines 2412-2427)
  - `_extract_archive_to_dir` (function, lines 2429-2469)
  - `_package_required_paths` (function, lines 2471-2477)
  - `_package_install_ready` (function, lines 2479-2487)
  - `_postprocess_offline_js_package` (function, lines 2489-2524)
  - `_ensure_offline_js_package` (function, lines 2526-2565)
  - `_render_offline_js_catalog_md` (function, lines 2567-2583)
  - `load_offline_js_lib_index` (function, lines 2585-2594)
  - `ensure_offline_js_libs` (function, lines 2596-2740)
  - `_normalize_external_js_url` (function, lines 2742-2746)
  - `is_external_js_src` (function, lines 2748-2750)
  - `match_offline_js_catalog_by_url` (function, lines 2752-2768)
  - `cache_external_js_url` (function, lines 2770-2802)
  - `try_read_text` (function, lines 4612-4620)

### `utils/json_utils.py`

- Routed symbols: 16
- Cross-module imports: `utils/text.py`: `trim`
- Symbols:
  - `JSON_FSYNC_ENABLED` (constant, lines 103-103)
  - `json_dumps` (function, lines 2321-2322)
  - `parse_tool_arguments` (function, lines 3016-3025)
  - `repair_truncated_json_object` (function, lines 3027-3080)
  - `parse_tool_arguments_with_error` (function, lines 3082-3112)
  - `parse_json_object` (function, lines 3376-3381)
  - `extract_json_object_from_text` (function, lines 3383-3405)
  - `_json_default_copy` (function, lines 4622-4627)
  - `_read_json_file` (function, lines 4629-4649)
  - `_write_json_file` (function, lines 4651-4678)
  - `tool_def` (function, lines 12399-12411)
  - `TOOLS` (constant, lines 12413-12589)
  - `TOOL_REQUIRED_ARGS` (constant, lines 12591-12591)
  - `TOOL_SPEC_BY_NAME` (constant, lines 12592-12592)
  - `TOOL_NAME_FUZZY_MAP` (constant, lines 12604-12604)
  - `canonicalize_tool_name` (function, lines 12622-12633)

### `utils/media.py`

- Routed symbols: 3
- Cross-module imports: none
- Symbols:
  - `guess_mime_from_name` (function, lines 2161-2163)
  - `_convert_image_to_safe_format` (function, lines 2166-2183)
  - `guess_ext_from_mime` (function, lines 2186-2192)

### `utils/misc.py`

- Routed symbols: 19
- Cross-module imports: none
- Symbols:
  - `MIN_TIMEOUT_SECONDS` (constant, lines 175-175)
  - `MAX_TIMEOUT_SECONDS` (constant, lines 176-176)
  - `DEFAULT_TIMEOUT_SECONDS` (constant, lines 177-183)
  - `BENIGN_SOCKET_DEBUG_LOG_ENABLED` (constant, lines 273-279)
  - `BENIGN_SOCKET_LOG_INTERVAL_SECONDS` (constant, lines 280-280)
  - `now_ts` (function, lines 2194-2195)
  - `_benign_socket_log_lock` (assignment, lines 2198-2198)
  - `_benign_socket_log_state` (assignment, lines 2199-2199)
  - `is_benign_socket_error` (function, lines 2217-2235)
  - `_socket_error_code` (function, lines 2238-2247)
  - `_log_benign_socket_error_limited` (function, lines 2250-2284)
  - `swallow_benign_socket_error` (function, lines 2287-2291)
  - `normalize_timeout_seconds` (function, lines 2294-2307)
  - `detect_local_lan_ip` (function, lines 2309-2319)
  - `make_id` (function, lines 2324-2325)
  - `sanitize_profile_id` (function, lines 2327-2329)
  - `user_id_from_ip` (function, lines 4282-4288)
  - `_meta_string_list` (function, lines 4599-4610)
  - `_module_exists` (function, lines 6033-6037)

### `utils/text.py`

- Routed symbols: 16
- Cross-module imports: none
- Symbols:
  - `MAX_TOOL_OUTPUT` (constant, lines 95-95)
  - `SOCKET_NOISE_LINE_PATTERNS` (constant, lines 267-272)
  - `filter_runtime_noise_lines` (function, lines 2202-2214)
  - `trim` (function, lines 2804-2806)
  - `_fmt_export_ts` (function, lines 2809-2817)
  - `_html_esc` (function, lines 2820-2821)
  - `_text_to_minimal_pdf` (function, lines 2824-2970)
  - `normalize_work_text` (function, lines 2989-3014)
  - `parse_front_matter` (function, lines 4409-4596)
  - `make_unified_diff` (function, lines 4680-4697)
  - `_skip_row` (function, lines 4699-4703)
  - `_row_is_hot` (function, lines 4706-4707)
  - `_hotspot_index` (function, lines 4710-4731)
  - `_compress_rows_keep_hotspot` (function, lines 4734-4781)
  - `make_numbered_diff` (function, lines 4784-4869)
  - `render_numbered_diff_text` (function, lines 4871-4883)
