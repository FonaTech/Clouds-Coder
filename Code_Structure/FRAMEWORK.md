# Code_Structure Framework

## Overview

- Source file: `/Users/macbookair/Downloads/Split Coder/Clouds_Coder.py`
- Output directory: `/Users/macbookair/Downloads/Split Coder/Code_Structure`
- Generated modules: 29
- Top-level symbols: 500
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
| `config/constants.py` | 283 | `utils/json_utils.py`, `utils/misc.py` |
| `config/paths.py` | 8 | `utils/text.py` |
| `config/settings.py` | 27 | `config/constants.py`, `config/paths.py`, `llm/utils.py`, `skills/store.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` |
| `llm/client.py` | 2 | `config/constants.py`, `config/settings.py`, `llm/utils.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` |
| `llm/utils.py` | 25 | `config/constants.py`, `utils/json_utils.py`, `utils/text.py` |
| `rag/index.py` | 5 | `config/constants.py`, `rag/parsers.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` |
| `rag/ingestion.py` | 3 | `config/constants.py`, `config/settings.py`, `rag/parsers.py`, `rag/store.py`, `session/state.py`, `utils/files.py`, `utils/json_utils.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py` |
| `rag/parsers.py` | 22 | `config/constants.py`, `utils/files.py`, `utils/json_utils.py`, `utils/media.py`, `utils/text.py` |
| `rag/store.py` | 2 | `config/constants.py`, `rag/index.py`, `rag/parsers.py`, `utils/files.py`, `utils/json_utils.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py` |
| `server/handlers.py` | 5 | `app/context.py`, `config/constants.py`, `config/paths.py`, `config/settings.py`, `llm/utils.py`, `session/manager.py`, `session/state.py`, `skills/store.py`, `utils/files.py`, `utils/json_utils.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py` |
| `session/manager.py` | 1 | `config/constants.py`, `config/paths.py`, `config/settings.py`, `llm/client.py`, `llm/utils.py`, `session/state.py`, `utils/crypto.py`, `utils/files.py`, `utils/json_utils.py`, `utils/misc.py` |
| `session/state.py` | 1 | `agent/background.py`, `agent/bus.py`, `agent/events.py`, `agent/tasks.py`, `agent/todo.py`, `agent/worktree.py`, `config/constants.py`, `config/paths.py`, `config/settings.py`, `llm/client.py`, `llm/utils.py`, `rag/parsers.py`, `skills/store.py`, `utils/compress.py`, `utils/crypto.py`, `utils/errors.py`, `utils/files.py`, `utils/json_utils.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py` |
| `skills/store.py` | 23 | `config/constants.py`, `config/paths.py`, `llm/utils.py`, `utils/files.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` |
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
- Cross-module imports: `app/context.py`: `AppContext`; `config/constants.py`: `AGENT_MAX_OUTPUT_TOKENS`, `ARBITER_DEFAULT_MAX_TOKENS`, `ARBITER_DEFAULT_TEMPERATURE`, `ARBITER_DEFAULT_TIMEOUT_SECONDS`, `CODE_ADMIN_PORT_OFFSET`, `DEFAULT_OLLAMA_BASE_URL`, `DEFAULT_OLLAMA_MODEL`, `DEFAULT_UI_LANGUAGE`, `DEFAULT_UI_STYLE`, `DEFAULT_WEB_UI_CONFIG`, `DEFAULT_WEB_UI_DIR`, `EXECUTION_MODE_SYNC`, `LIVE_INPUT_DELAY_NORMAL_ROUNDS`, `LIVE_INPUT_DELAY_TOOL_ROUNDS`, `LIVE_INPUT_DELAY_WRITE_ROUNDS`, `LIVE_INPUT_MAX_INJECTIONS`, `LIVE_INPUT_REINJECT_INTERVAL`, `LIVE_INPUT_WEIGHT_BASE_DELAYED`, `LIVE_INPUT_WEIGHT_BASE_NORMAL`, `LIVE_INPUT_WEIGHT_STEP_DELAYED`, `LIVE_INPUT_WEIGHT_STEP_NORMAL`, `MAX_AGENT_ROUNDS`, `MAX_AGENT_ROUNDS_CAP`, `MAX_RUN_SECONDS`, `MAX_RUN_TIMEOUT_SECONDS`, `MIN_AGENT_ROUNDS`, `MIN_CONTEXT_TOKEN_LIMIT`, `MIN_RUN_TIMEOUT_SECONDS`, `OFFLINE_JS_LIB_CATALOG`, `RAG_ADMIN_PORT_OFFSET`, `RAG_INCLUDE_FILENAME_ENTITIES_DEFAULT`, `TOKEN_THRESHOLD`, `UI_LANGUAGE_LABELS`, `UI_STYLE_LABELS`; `config/paths.py`: `LLM_CONFIG_PATH`, `REPO_ROOT`, `WORKDIR`; `config/settings.py`: `_to_bool_like`, `extract_js_lib_download_setting`, `extract_show_upload_list_setting`, `extract_ui_style_setting`, `load_llm_config_from_source`, `load_web_ui_config_file`, `normalize_execution_mode`, `normalize_ui_language`, `normalize_ui_style`, `parse_llm_config_profiles`, `resolve_optional_file_path`, `resolve_web_ui_dir_path`, `select_preferred_skills_root`; `llm/utils.py`: `list_ollama_models`; `server/handlers.py`: `AgentHTTPServer`, `CodeAdminHandler`, `Handler`, `RagAdminHandler`, `SkillsHandler`; `skills/store.py`: `ensure_embedded_skills_at_root`, `ensure_runtime_skills`; `utils/files.py`: `ensure_offline_js_libs`; `utils/misc.py`: `BENIGN_SOCKET_DEBUG_LOG_ENABLED`, `detect_local_lan_ip`, `normalize_timeout_seconds`, `swallow_benign_socket_error`; `utils/text.py`: `trim`
- Symbols:
  - `main` (function, lines 50734-51584)
  - `_main_guard_51586` (main_guard, lines 51586-51587)

### `agent/background.py`

- Routed symbols: 1
- Cross-module imports: `utils/misc.py`: `make_id`, `now_ts`; `utils/text.py`: `trim`
- Symbols:
  - `BackgroundManager` (class, lines 10412-10492)

### `agent/bus.py`

- Routed symbols: 1
- Cross-module imports: `config/constants.py`: `VALID_MSG_TYPES`; `utils/crypto.py`: `CryptoBox`; `utils/misc.py`: `now_ts`
- Symbols:
  - `MessageBus` (class, lines 10494-10548)

### `agent/events.py`

- Routed symbols: 1
- Cross-module imports: none
- Symbols:
  - `EventHub` (class, lines 5076-5121)

### `agent/tasks.py`

- Routed symbols: 1
- Cross-module imports: `utils/crypto.py`: `CryptoBox`; `utils/json_utils.py`: `json_dumps`; `utils/misc.py`: `now_ts`
- Symbols:
  - `TaskManager` (class, lines 10284-10410)

### `agent/todo.py`

- Routed symbols: 1
- Cross-module imports: `config/constants.py`: `DEFAULT_UI_LANGUAGE`; `config/settings.py`: `backend_i18n_text`, `backend_role_label`, `normalize_ui_language`; `utils/text.py`: `normalize_work_text`, `trim`
- Symbols:
  - `TodoManager` (class, lines 5123-5367)

### `agent/worktree.py`

- Routed symbols: 1
- Cross-module imports: `agent/tasks.py`: `TaskManager`; `config/constants.py`: `DANGEROUS_PATTERNS`; `utils/crypto.py`: `CryptoBox`; `utils/json_utils.py`: `json_dumps`; `utils/misc.py`: `now_ts`; `utils/text.py`: `trim`
- Symbols:
  - `WorktreeManager` (class, lines 10550-10761)

### `app/context.py`

- Routed symbols: 1
- Cross-module imports: `config/constants.py`: `AGENT_MAX_OUTPUT_TOKENS`, `APP_CSS`, `APP_JS`, `APP_TS`, `ARBITER_DEFAULT_MAX_TOKENS`, `ARBITER_DEFAULT_TEMPERATURE`, `ARBITER_DEFAULT_TIMEOUT_SECONDS`, `CODE_ADMIN_CSS`, `CODE_ADMIN_INDEX_HTML`, `CODE_ADMIN_JS`, `CODE_IMPORT_WORKER_COUNT`, `CODE_LIBRARY_DIRNAME`, `CODE_PARSE_TIMEOUT_SECONDS`, `DEFAULT_REQUEST_TIMEOUT`, `DEFAULT_UI_LANGUAGE`, `DEFAULT_UI_STYLE`, `DEFAULT_WEB_UI_DIR`, `EXECUTION_MODE_SYNC`, `INDEX_HTML`, `MAX_AGENT_ROUNDS`, `MAX_AGENT_ROUNDS_CAP`, `MAX_RUN_SECONDS`, `MAX_RUN_TIMEOUT_SECONDS`, `MIN_AGENT_ROUNDS`, `MIN_CONTEXT_TOKEN_LIMIT`, `MIN_RUN_TIMEOUT_SECONDS`, `RAG_ADMIN_CSS`, `RAG_ADMIN_INDEX_HTML`, `RAG_ADMIN_JS`, `RAG_GRAPH_MAX_NODES`, `RAG_IMPORT_WORKER_COUNT`, `RAG_INCLUDE_FILENAME_ENTITIES_DEFAULT`, `RAG_LIBRARY_DIRNAME`, `RAG_MAX_GLOBAL_COMMUNITIES`, `RAG_MAX_IMPORT_BATCH_BYTES`, `RAG_MAX_IMPORT_BATCH_ITEMS`, `RAG_MAX_IMPORT_FILES`, `RAG_MAX_QUERY_RESULTS`, `RAG_PARSE_TIMEOUT_SECONDS`, `RAG_QUERY_CONTEXT_CHARS`, `SKILLS_APP_JS`, `SKILLS_EXTRA_CSS`, `SKILLS_INDEX_HTML`, `SKILL_REFRESH_MIN_INTERVAL_SECONDS`, `TOKEN_THRESHOLD`, `WEB_UI_OPTIONAL_FILES`, `WEB_UI_REQUIRED_FILES`; `config/paths.py`: `LLM_CONFIG_PATH`, `REPO_ROOT`, `SCRIPT_DIR`, `_migrate_legacy_runtime_roots`; `config/settings.py`: `default_multimodal_capabilities`, `infer_model_multimodal_capabilities`, `merge_multimodal_capabilities`, `model_language_instruction`, `normalize_execution_mode`, `normalize_ui_language`, `normalize_ui_style`, `parse_capability_overrides`, `parse_llm_config_profiles`, `resolve_optional_file_path`, `resolve_web_ui_dir_path`; `llm/client.py`: `OllamaClient`; `llm/utils.py`: `extract_base_url`; `rag/ingestion.py`: `CodeIngestionService`, `RAGIngestionService`; `rag/parsers.py`: `CodeContentParser`, `RAGContentParser`; `rag/store.py`: `CodeLibraryStore`, `RAGLibraryStore`; `session/manager.py`: `SessionManager`; `session/state.py`: `SessionState`; `skills/store.py`: `SkillStore`, `_sanitize_skill_slug`, `analyze_skill_building_knowledge`, `ensure_runtime_skills`; `utils/crypto.py`: `CryptoBox`; `utils/files.py`: `_resolve_js_lib_asset_path`, `ensure_offline_js_libs`, `load_offline_js_lib_index`, `offline_js_lib_root`, `safe_path`, `try_read_text`; `utils/json_utils.py`: `TOOLS`, `extract_json_object_from_text`, `json_dumps`, `parse_json_object`; `utils/misc.py`: `DEFAULT_TIMEOUT_SECONDS`, `MAX_TIMEOUT_SECONDS`, `MIN_TIMEOUT_SECONDS`, `normalize_timeout_seconds`, `now_ts`, `sanitize_profile_id`; `utils/text.py`: `parse_front_matter`, `trim`
- Symbols:
  - `AppContext` (class, lines 47069-49391)

### `config/constants.py`

- Routed symbols: 283
- Cross-module imports: `utils/json_utils.py`: `TOOL_SPEC_BY_NAME`; `utils/misc.py`: `DEFAULT_TIMEOUT_SECONDS`
- Symbols:
  - `APP_VERSION` (constant, lines 49-49)
  - `DEFAULT_OLLAMA_BASE_URL` (constant, lines 50-50)
  - `DEFAULT_OLLAMA_MODEL` (constant, lines 51-51)
  - `LONG_OUTPUT_MODEL_PAGE_CHARS` (constant, lines 94-94)
  - `LONG_OUTPUT_UI_PAGE_CHARS` (constant, lines 95-95)
  - `LONG_OUTPUT_UI_PREVIEW_MAX_PAGES` (constant, lines 96-96)
  - `LONG_OUTPUT_LISTING_OFFLOAD_CHARS` (constant, lines 97-97)
  - `LONG_OUTPUT_READ_PAGE_LINES` (constant, lines 98-98)
  - `LONG_OUTPUT_READ_PAGE_MAX_CHARS` (constant, lines 99-99)
  - `LONG_OUTPUT_TEMP_MAX_FILES` (constant, lines 100-100)
  - `RAG_LIBRARY_DIRNAME` (constant, lines 102-102)
  - `RAG_ADMIN_PORT_OFFSET` (constant, lines 103-103)
  - `CODE_LIBRARY_DIRNAME` (constant, lines 104-104)
  - `CODE_ADMIN_PORT_OFFSET` (constant, lines 105-105)
  - `RAG_CHUNK_CHARS` (constant, lines 106-106)
  - `RAG_CHUNK_OVERLAP` (constant, lines 107-107)
  - `RAG_MAX_CHUNKS_PER_DOC` (constant, lines 108-108)
  - `CODE_CHUNK_CHARS` (constant, lines 109-109)
  - `CODE_CHUNK_OVERLAP` (constant, lines 110-110)
  - `CODE_MAX_CHUNKS_PER_DOC` (constant, lines 111-111)
  - `RAG_MAX_QUERY_RESULTS` (constant, lines 112-112)
  - `RAG_GRAPH_MAX_NODES` (constant, lines 113-113)
  - `RAG_TASK_HISTORY_LIMIT` (constant, lines 114-114)
  - `RAG_MODEL_MEDIA_MAX_BYTES` (constant, lines 115-115)
  - `RAG_MAX_IMPORT_FILES` (constant, lines 116-116)
  - `RAG_MAX_IMPORT_BATCH_ITEMS` (constant, lines 117-117)
  - `RAG_MAX_IMPORT_BATCH_BYTES` (constant, lines 118-118)
  - `RAG_PDF_IMAGE_LIMIT` (constant, lines 119-119)
  - `RAG_QUERY_CONTEXT_CHARS` (constant, lines 120-120)
  - `RAG_MAX_GLOBAL_COMMUNITIES` (constant, lines 121-121)
  - `RAG_MAX_COMMUNITY_MAP_SUPPORT` (constant, lines 122-122)
  - `RAG_INCLUDE_FILENAME_ENTITIES_DEFAULT` (constant, lines 123-123)
  - `RAG_DYNAMIC_NOISE_MIN_DOC_FREQ` (constant, lines 124-124)
  - `RAG_DYNAMIC_NOISE_MIN_COMMUNITY_FREQ` (constant, lines 125-125)
  - `RAG_DYNAMIC_NOISE_SOFT_DOC_RATIO` (constant, lines 126-126)
  - `RAG_DYNAMIC_NOISE_HARD_DOC_RATIO` (constant, lines 127-127)
  - `RAG_DYNAMIC_NOISE_SOFT_COMMUNITY_RATIO` (constant, lines 128-128)
  - `RAG_DYNAMIC_NOISE_HARD_COMMUNITY_RATIO` (constant, lines 129-129)
  - `RAG_IMPORT_WORKER_COUNT` (constant, lines 130-133)
  - `CODE_IMPORT_WORKER_COUNT` (constant, lines 134-137)
  - `RAG_PARSE_TIMEOUT_SECONDS` (constant, lines 138-141)
  - `CODE_PARSE_TIMEOUT_SECONDS` (constant, lines 142-145)
  - `TOKEN_THRESHOLD` (constant, lines 146-146)
  - `IDLE_TIMEOUT` (constant, lines 147-147)
  - `POLL_INTERVAL` (constant, lines 148-148)
  - `SSE_HEARTBEAT_SECONDS` (constant, lines 149-149)
  - `MODEL_CALL_PROGRESS_DELAY` (constant, lines 150-150)
  - `MODEL_CALL_PROGRESS_INTERVAL` (constant, lines 151-151)
  - `MAX_AGENT_ROUNDS` (constant, lines 152-152)
  - `MIN_AGENT_ROUNDS` (constant, lines 153-153)
  - `MAX_AGENT_ROUNDS_CAP` (constant, lines 154-154)
  - `REPEATED_TOOL_LOOP_THRESHOLD` (constant, lines 155-155)
  - `BASH_READ_LOOP_THRESHOLD` (constant, lines 156-156)
  - `HARD_BREAK_TOOL_ERROR_THRESHOLD` (constant, lines 157-157)
  - `HARD_BREAK_RECOVERY_ROUND_THRESHOLD` (constant, lines 158-158)
  - `FUSED_FAULT_BREAK_THRESHOLD` (constant, lines 159-159)
  - `STALL_SEVERITY_ESCALATION_THRESHOLD` (constant, lines 160-160)
  - `STALL_SEVERITY_WEIGHT_BASH_READ_LOOP` (constant, lines 161-161)
  - `STALL_SEVERITY_WEIGHT_REPEATED_TOOL` (constant, lines 162-162)
  - `STALL_SEVERITY_WEIGHT_FAULT` (constant, lines 163-163)
  - `STALL_SEVERITY_WEIGHT_RECOVERY_RETRY` (constant, lines 164-164)
  - `STALL_SEVERITY_WEIGHT_WATCHDOG` (constant, lines 165-165)
  - `STALL_SEVERITY_DECAY_ON_SUCCESS` (constant, lines 166-166)
  - `STALL_ESCALATION_MIN_LEVEL` (constant, lines 167-167)
  - `STALL_PLAN_SYNTHESIS_MAX_TOKENS` (constant, lines 168-168)
  - `STALL_ESCALATION_CONTEXT_MAX_CHARS` (constant, lines 169-169)
  - `MAX_RUN_SECONDS` (constant, lines 170-170)
  - `MIN_RUN_TIMEOUT_SECONDS` (constant, lines 171-171)
  - `MAX_RUN_TIMEOUT_SECONDS` (constant, lines 172-172)
  - `DEFAULT_REQUEST_TIMEOUT` (constant, lines 182-182)
  - `AUTO_CONTINUE_BUDGET_DEFAULT` (constant, lines 183-183)
  - `AGENT_MAX_OUTPUT_TOKENS` (constant, lines 184-184)
  - `OLLAMA_THINKING_TOOL_BUFFER` (constant, lines 185-185)
  - `WATCHDOG_INTENT_NO_TOOL_THRESHOLD` (constant, lines 186-186)
  - `WATCHDOG_REPEAT_NO_TOOL_THRESHOLD` (constant, lines 187-187)
  - `WATCHDOG_INTENT_NO_TOOL_THRESHOLD_SINGLE` (constant, lines 188-188)
  - `WATCHDOG_REPEAT_NO_TOOL_THRESHOLD_SINGLE` (constant, lines 189-189)
  - `WATCHDOG_STATE_STALL_THRESHOLD` (constant, lines 190-190)
  - `WATCHDOG_CONTEXT_STALL_THRESHOLD` (constant, lines 191-191)
  - `WATCHDOG_REPEAT_SIMILARITY_THRESHOLD` (constant, lines 192-192)
  - `WATCHDOG_CONTEXT_NEAR_RATIO` (constant, lines 193-193)
  - `WATCHDOG_MAX_DECOMPOSE_STEPS` (constant, lines 194-194)
  - `WATCHDOG_STEP_MAX_ATTEMPTS` (constant, lines 195-195)
  - `EMPTY_ACTION_MIN_CONTENT_CHARS` (constant, lines 196-196)
  - `EMPTY_ACTION_WAKEUP_RETRY_LIMIT` (constant, lines 197-197)
  - `THINKING_BUDGET_FORCE_RATIO` (constant, lines 198-198)
  - `_TOOL_TIMEOUT_MAP` (assignment, lines 200-216)
  - `_DEFAULT_TOOL_TIMEOUT` (assignment, lines 217-217)
  - `TRUNCATION_CONTINUATION_MAX_PASSES` (constant, lines 218-218)
  - `TRUNCATION_CONTINUATION_MAX_TOKENS` (constant, lines 219-219)
  - `TRUNCATION_CONTINUATION_TAIL_CHARS` (constant, lines 220-220)
  - `TRUNCATION_CONTINUATION_ECHO_CHARS` (constant, lines 221-221)
  - `TRUNCATION_OVERLAP_SCAN_CHARS` (constant, lines 222-222)
  - `TRUNCATION_PAIR_SCAN_CHARS` (constant, lines 223-223)
  - `TRUNCATION_LIVE_BUFFER_MAX_CHARS` (constant, lines 224-224)
  - `MIN_CONTEXT_TOKEN_LIMIT` (constant, lines 225-225)
  - `COMPACT_TIER1_PCT` (constant, lines 227-227)
  - `COMPACT_TIER2_PCT` (constant, lines 228-228)
  - `COMPACT_TIER3_PCT` (constant, lines 229-229)
  - `COMPACT_TIER1_ABS` (constant, lines 231-231)
  - `COMPACT_TIER2_ABS` (constant, lines 232-232)
  - `FILE_BUFFER_CONTENT_THRESHOLD` (constant, lines 234-234)
  - `FILE_BUFFER_MAX_FILES` (constant, lines 235-235)
  - `AGENT_MSG_LIMIT_TIER0` (constant, lines 237-237)
  - `AGENT_MSG_LIMIT_TIER1` (constant, lines 238-238)
  - `AGENT_MSG_LIMIT_TIER2` (constant, lines 239-239)
  - `AGENT_MSG_LIMIT_TIER3` (constant, lines 240-240)
  - `AGENT_CTX_LIMIT_TIER0` (constant, lines 241-241)
  - `AGENT_CTX_LIMIT_TIER1` (constant, lines 242-242)
  - `AGENT_CTX_LIMIT_TIER2` (constant, lines 243-243)
  - `AGENT_CTX_LIMIT_TIER3` (constant, lines 244-244)
  - `MANAGER_CTX_LIMIT_TIER0` (constant, lines 245-245)
  - `MANAGER_CTX_LIMIT_TIER1` (constant, lines 246-246)
  - `MANAGER_CTX_LIMIT_TIER2` (constant, lines 247-247)
  - `MANAGER_CTX_LIMIT_TIER3` (constant, lines 248-248)
  - `MAX_CONTEXT_ARCHIVE_SEGMENTS` (constant, lines 249-249)
  - `MODEL_OUTPUT_RETRY_TIMES` (constant, lines 250-250)
  - `ARBITER_TRIGGER_MIN_CONTENT_CHARS` (constant, lines 251-251)
  - `ARBITER_VALID_PLANNING_STREAK_LIMIT` (constant, lines 252-252)
  - `ARBITER_DEFAULT_TIMEOUT_SECONDS` (constant, lines 253-253)
  - `ARBITER_DEFAULT_MAX_TOKENS` (constant, lines 254-254)
  - `ARBITER_DEFAULT_TEMPERATURE` (constant, lines 255-255)
  - `LIVE_INPUT_DELAY_WRITE_ROUNDS` (constant, lines 256-256)
  - `LIVE_INPUT_DELAY_TOOL_ROUNDS` (constant, lines 257-257)
  - `LIVE_INPUT_DELAY_NORMAL_ROUNDS` (constant, lines 258-258)
  - `LIVE_INPUT_MAX_INJECTIONS` (constant, lines 259-259)
  - `LIVE_INPUT_REINJECT_INTERVAL` (constant, lines 260-260)
  - `LIVE_INPUT_WEIGHT_BASE_DELAYED` (constant, lines 261-261)
  - `LIVE_INPUT_WEIGHT_BASE_NORMAL` (constant, lines 262-262)
  - `LIVE_INPUT_WEIGHT_STEP_DELAYED` (constant, lines 263-263)
  - `LIVE_INPUT_WEIGHT_STEP_NORMAL` (constant, lines 264-264)
  - `FINAL_SUMMARY_MIN_CHARS` (constant, lines 279-279)
  - `FINAL_SUMMARY_STRICT_MIN_CHARS` (constant, lines 280-280)
  - `RUNTIME_CONTROL_HINT_PREFIXES` (constant, lines 281-298)
  - `RETRY_RUNTIME_HINT_PREFIXES` (constant, lines 299-313)
  - `EXECUTION_MODE_SINGLE` (constant, lines 314-314)
  - `EXECUTION_MODE_SEQUENTIAL` (constant, lines 315-315)
  - `EXECUTION_MODE_SYNC` (constant, lines 316-316)
  - `EXECUTION_MODE_CHOICES` (constant, lines 317-321)
  - `AGENT_ROLES` (constant, lines 322-322)
  - `AGENT_BUBBLE_ROLES` (constant, lines 323-323)
  - `AGENT_ROLE_LABELS` (constant, lines 324-330)
  - `AGENT_ROLE_BUBBLE_COLORS` (constant, lines 331-337)
  - `BLACKBOARD_STATUSES` (constant, lines 338-347)
  - `TASK_COMPLEXITY_LEVELS` (constant, lines 348-348)
  - `TASK_PROFILE_TYPES` (constant, lines 349-355)
  - `TASK_LEVEL_CHOICES` (constant, lines 356-356)
  - `TASK_SCALE_PREFERENCES` (constant, lines 357-357)
  - `SEMANTIC_CONFIDENCE_CHOICES` (constant, lines 358-358)
  - `TASK_LEVEL_POLICIES` (constant, lines 359-405)
  - `MANAGER_ROUTE_TARGETS` (constant, lines 406-406)
  - `BLACKBOARD_MAX_LOG_ENTRIES` (constant, lines 407-407)
  - `BLACKBOARD_MAX_TEXT` (constant, lines 408-408)
  - `SKILL_REFRESH_MIN_INTERVAL_SECONDS` (constant, lines 409-409)
  - `SKILL_PROMPT_MAX_ITEMS` (constant, lines 410-410)
  - `SKILL_PROMPT_MAX_CHARS` (constant, lines 411-411)
  - `SKILL_RUNTIME_CACHE_MAX_ENTRIES` (constant, lines 412-412)
  - `SKILL_RUNTIME_CACHE_MAX_BYTES` (constant, lines 413-413)
  - `AUTO_SKILLS_ROOT_CANDIDATES` (constant, lines 414-414)
  - `SKILL_DEFAULT_ATTACHMENT_GLOBS` (constant, lines 415-445)
  - `SKILL_INLINE_ATTACHMENT_MAX_FILES` (constant, lines 446-446)
  - `SKILL_INLINE_ATTACHMENT_MAX_CHARS` (constant, lines 447-447)
  - `SKILL_RESOURCE_MANIFEST_MAX_ITEMS` (constant, lines 448-448)
  - `SKILL_BODY_COMPACT_THRESHOLD_CHARS` (constant, lines 449-449)
  - `SKILL_BODY_PREVIEW_CHARS` (constant, lines 450-450)
  - `SKILLS_VIRTUAL_PREFIX` (constant, lines 451-451)
  - `SKILLS_EXTERNAL_MOUNT` (constant, lines 452-452)
  - `PLAN_MODE_ENABLED_LEVELS` (constant, lines 453-453)
  - `PLAN_MODE_FORCED_LEVELS` (constant, lines 454-454)
  - `PLAN_MODE_USER_CHOICES` (constant, lines 455-455)
  - `TASK_PHASES` (constant, lines 457-457)
  - `TASK_PHASE_ROUTING` (constant, lines 458-465)
  - `COMPLEXITY_KEYWORDS` (constant, lines 467-472)
  - `USER_COMPLEXITY_SIMPLE_TOKENS` (constant, lines 473-477)
  - `USER_COMPLEXITY_COMPLEX_TOKENS` (constant, lines 478-482)
  - `PLAN_MODE_EXPLORER_MAX_ROUNDS` (constant, lines 483-483)
  - `REVIEWER_DEBUG_MODE_MAX_ROUNDS` (constant, lines 485-485)
  - `REVIEWER_DEBUG_TOOL_ALLOWLIST` (constant, lines 486-490)
  - `EXPLORER_STALL_THRESHOLD` (constant, lines 491-491)
  - `DEVELOPER_EDIT_STALL_THRESHOLD` (constant, lines 492-492)
  - `PLAN_MODE_MANAGER_SYNTHESIS_MAX_TOKENS` (constant, lines 493-493)
  - `PLAN_MODE_MAX_OPTIONS` (constant, lines 494-494)
  - `PLAN_FILE_RELATIVE_PATH` (constant, lines 495-495)
  - `PLAN_BUBBLE_MAX_CHARS` (constant, lines 496-496)
  - `PLAN_MODE_RESEARCH_TOOL_ALLOWLIST` (constant, lines 497-501)
  - `FAILURE_LEDGER_MAX_FIXES` (constant, lines 502-502)
  - `FAILURE_LEDGER_MAX_COMPILE_ERRORS` (constant, lines 503-503)
  - `FAILURE_LEDGER_MAX_DELEGATIONS` (constant, lines 504-504)
  - `FAILURE_LEDGER_MAX_STALLS` (constant, lines 505-505)
  - `FAILURE_LEDGER_MAX_TOOL_FPS` (constant, lines 506-506)
  - `FAILURE_LEDGER_MAX_ERRORS` (constant, lines 507-507)
  - `ERROR_CATEGORY_DEFS` (constant, lines 510-547)
  - `CHECKPOINT_MAX_COUNT` (constant, lines 548-548)
  - `CHECKPOINT_INTERVAL_ROUNDS` (constant, lines 549-549)
  - `PERSISTED_ROUTES_MAX` (constant, lines 550-550)
  - `HTML_FRONTEND_REQUEST_KEYWORDS` (constant, lines 551-590)
  - `DEEP_RESEARCH_REQUEST_KEYWORDS` (constant, lines 591-613)
  - `DEEP_RESEARCH_RETRIEVAL_KEYWORDS` (constant, lines 614-633)
  - `DEEP_RESEARCH_TEXT_ONLY_HINT_KEYWORDS` (constant, lines 634-651)
  - `DANGEROUS_PATTERNS` (constant, lines 653-653)
  - `VALID_MSG_TYPES` (constant, lines 654-660)
  - `SUPPORTED_UI_LANGUAGES` (constant, lines 662-667)
  - `UI_LANGUAGE_LABELS` (constant, lines 668-668)
  - `DEFAULT_UI_LANGUAGE` (constant, lines 669-669)
  - `UI_STYLE_CHOICES` (constant, lines 670-670)
  - `UI_STYLE_LABELS` (constant, lines 671-671)
  - `DEFAULT_UI_STYLE` (constant, lines 672-672)
  - `DEFAULT_WEB_UI_DIR` (constant, lines 673-673)
  - `DEFAULT_WEB_UI_CONFIG` (constant, lines 674-674)
  - `WEB_UI_REQUIRED_FILES` (constant, lines 675-682)
  - `WEB_UI_OPTIONAL_FILES` (constant, lines 683-683)
  - `IMAGE_EXTS` (constant, lines 685-698)
  - `IMAGE_FORMATS_NEED_CONVERSION` (constant, lines 699-699)
  - `IMAGE_SAFE_FORMATS` (constant, lines 700-700)
  - `AUDIO_EXTS` (constant, lines 701-711)
  - `VIDEO_EXTS` (constant, lines 712-722)
  - `CODE_PREVIEW_STAGE_MAX_BYTES` (constant, lines 723-723)
  - `CODE_PREVIEW_STAGE_MAX_ROWS` (constant, lines 724-724)
  - `CODE_PREVIEW_STAGE_MAX_PER_FILE` (constant, lines 725-725)
  - `CODE_PREVIEW_STAGE_MAX_TOTAL` (constant, lines 726-726)
  - `RENDER_FRAME_MAX_B64_CHARS` (constant, lines 727-727)
  - `RENDER_FRAME_MAX_POINTS` (constant, lines 728-728)
  - `RENDER_FRAME_MAX_LINES` (constant, lines 729-729)
  - `RENDER_FRAME_MAX_LINE_POINTS` (constant, lines 730-730)
  - `RENDER_FRAME_ACTIVITY_INTERVAL_SECONDS` (constant, lines 731-731)
  - `RAW_TOOLCALL_TEXT_FILTER_THRESHOLD` (constant, lines 732-732)
  - `ASSISTANT_TEXT_PERSIST_MAX_CHARS` (constant, lines 733-733)
  - `ASSISTANT_MESSAGE_EVENT_MAX_CHARS` (constant, lines 734-734)
  - `CODE_PREVIEW_EXTS` (constant, lines 735-824)
  - `CODE_PREVIEW_FILENAMES` (constant, lines 825-836)
  - `MEDIA_CAPABILITY_KEYS` (constant, lines 837-844)
  - `SAMPLE_IMAGE_PNG_B64` (constant, lines 845-848)
  - `SAMPLE_AUDIO_WAV_B64` (constant, lines 849-851)
  - `SAMPLE_VIDEO_MP4_B64` (constant, lines 852-854)
  - `OFFLINE_JS_LIB_CATALOG` (constant, lines 856-1114)
  - `OFFLINE_JS_LIB_INDEX_FILE` (constant, lines 1115-1115)
  - `OFFLINE_JS_LIB_README_FILE` (constant, lines 1116-1116)
  - `BACKEND_I18N` (constant, lines 1302-1371)
  - `call_backend_i18n_en_update_l1373` (expression, lines 1373-1466)
  - `call_backend_i18n_zh_cn_update_l1467` (expression, lines 1467-1560)
  - `call_backend_i18n_zh_tw_update_l1561` (expression, lines 1561-1654)
  - `call_backend_i18n_ja_update_l1655` (expression, lines 1655-1748)
  - `OPENAI_COMPAT_PROVIDER_NAMES` (constant, lines 3400-3408)
  - `OPENAI_LIKE_PROVIDER_NAMES` (constant, lines 3410-3410)
  - `TABULAR_PREVIEW_EXTS` (constant, lines 4854-4854)
  - `EXCEL_PREVIEW_EXTS` (constant, lines 4855-4855)
  - `PRESENTATION_PREVIEW_EXTS` (constant, lines 4856-4856)
  - `DOCUMENT_PREVIEW_EXTS` (constant, lines 4857-4857)
  - `EMBEDDED_SKILLS_ARCHIVE_B64` (constant, lines 5369-5888)
  - `EMBEDDED_SKILLS_ARCHIVE_SHA256` (constant, lines 5889-5889)
  - `EMBEDDED_SKILLS_ARCHIVE_FILES` (constant, lines 5890-5913)
  - `BUILTIN_CLAWHUB_SKILLS_VERSION` (constant, lines 8557-8557)
  - `EMBEDDED_CLAWHUB_SKILLS_ARCHIVE_B64` (constant, lines 8559-8803)
  - `SKILL_PROTOCOL_LOCAL` (constant, lines 8859-8859)
  - `SKILL_PROTOCOL_CLAWHUB` (constant, lines 8860-8860)
  - `SKILL_PROTOCOL_HTTP_JSON` (constant, lines 8861-8861)
  - `SKILL_PROTOCOL_SPECS` (constant, lines 8863-8894)
  - `AGENT_TOOL_ALLOWLIST` (constant, lines 12058-12101)
  - `INDEX_HTML` (constant, lines 36259-36446)
  - `APP_CSS` (constant, lines 36448-36826)
  - `APP_JS` (constant, lines 36828-39807)
  - `APP_TS` (constant, lines 39809-39836)
  - `SKILLS_INDEX_HTML` (constant, lines 39838-39992)
  - `SKILLS_EXTRA_CSS` (constant, lines 39994-40089)
  - `SKILLS_APP_JS` (constant, lines 40091-40232)
  - `RAG_TERM_GROUPS` (constant, lines 40234-40244)
  - `RAG_RESEARCH_HINTS` (constant, lines 40245-40266)
  - `RAG_CODE_HINTS` (constant, lines 40267-40277)
  - `RAG_SHORT_TOKEN_ALLOWLIST` (constant, lines 40278-40293)
  - `RAG_EN_STOPWORDS` (constant, lines 40294-40366)
  - `RAG_ZH_STOPWORDS` (constant, lines 40367-40403)
  - `RAG_GENERIC_ENTITY_TERMS_EN` (constant, lines 40404-40482)
  - `RAG_GENERIC_ENTITY_TERMS_ZH` (constant, lines 40483-40525)
  - `RAG_STRUCTURAL_ENTITY_PATTERNS` (constant, lines 40526-40544)
  - `CODE_LIBRARY_IGNORED_DIRS` (constant, lines 40867-40872)
  - `CODE_LIBRARY_LANGUAGE_BY_EXT` (constant, lines 40873-40929)
  - `CODE_LIBRARY_SPECIAL_FILENAMES` (constant, lines 40930-40936)
  - `RAG_ADMIN_INDEX_HTML` (constant, lines 45543-45700)
  - `RAG_ADMIN_CSS` (constant, lines 45702-45792)
  - `RAG_ADMIN_JS` (constant, lines 45794-47020)
  - `CODE_ADMIN_INDEX_HTML` (constant, lines 47022-47031)
  - `CODE_ADMIN_CSS` (constant, lines 47032-47062)
  - `CODE_ADMIN_JS` (constant, lines 47063-47067)

### `config/paths.py`

- Routed symbols: 8
- Cross-module imports: `utils/text.py`: `trim`
- Symbols:
  - `SCRIPT_DIR` (constant, lines 52-52)
  - `_resolve_default_agent_workdir` (function, lines 54-58)
  - `_migrate_legacy_runtime_roots` (function, lines 60-88)
  - `WORKDIR` (constant, lines 90-90)
  - `CODES_ROOT` (constant, lines 91-91)
  - `LLM_CONFIG_PATH` (constant, lines 92-92)
  - `detect_repo_root` (function, lines 2274-2288)
  - `REPO_ROOT` (constant, lines 2290-2290)

### `config/settings.py`

- Routed symbols: 27
- Cross-module imports: `config/constants.py`: `AUTO_SKILLS_ROOT_CANDIDATES`, `BACKEND_I18N`, `DEFAULT_REQUEST_TIMEOUT`, `DEFAULT_UI_LANGUAGE`, `DEFAULT_UI_STYLE`, `DEFAULT_WEB_UI_CONFIG`, `DEFAULT_WEB_UI_DIR`, `EXECUTION_MODE_CHOICES`, `EXECUTION_MODE_SEQUENTIAL`, `EXECUTION_MODE_SINGLE`, `EXECUTION_MODE_SYNC`, `MEDIA_CAPABILITY_KEYS`, `SUPPORTED_UI_LANGUAGES`, `UI_LANGUAGE_LABELS`, `UI_STYLE_CHOICES`, `USER_COMPLEXITY_COMPLEX_TOKENS`, `USER_COMPLEXITY_SIMPLE_TOKENS`; `config/paths.py`: `WORKDIR`; `llm/utils.py`: `_is_http_url`, `_resolve_local_path`, `complete_chat_endpoint`, `extract_base_url`, `is_openai_like_provider`, `normalize_openai_compat_provider_name`, `strip_thinking_content`; `skills/store.py`: `ensure_embedded_skills`; `utils/json_utils.py`: `parse_json_object`; `utils/misc.py`: `MAX_TIMEOUT_SECONDS`, `MIN_TIMEOUT_SECONDS`, `normalize_timeout_seconds`, `sanitize_profile_id`; `utils/text.py`: `trim`
- Symbols:
  - `normalize_ui_language` (function, lines 1200-1222)
  - `normalize_ui_style` (function, lines 1225-1242)
  - `supported_ui_languages_payload` (function, lines 1245-1246)
  - `normalize_execution_mode` (function, lines 1249-1268)
  - `model_language_instruction` (function, lines 1271-1299)
  - `backend_i18n_text` (function, lines 1751-1761)
  - `backend_role_label` (function, lines 1764-1768)
  - `_detect_os_shell_instruction` (function, lines 1771-1810)
  - `resolve_web_ui_dir_path` (function, lines 1812-1819)
  - `resolve_optional_file_path` (function, lines 1822-1829)
  - `resolve_skills_root_path` (function, lines 1832-1839)
  - `_count_skill_markdown_files` (function, lines 1842-1853)
  - `select_preferred_skills_root` (function, lines 1856-1890)
  - `load_web_ui_config_file` (function, lines 1893-1907)
  - `extract_show_upload_list_setting` (function, lines 1910-1924)
  - `extract_ui_style_setting` (function, lines 1927-1941)
  - `extract_js_lib_download_setting` (function, lines 1944-1963)
  - `default_multimodal_capabilities` (function, lines 1966-1974)
  - `_to_bool_like` (function, lines 1977-1987)
  - `infer_model_multimodal_capabilities` (function, lines 1990-2034)
  - `parse_capability_overrides` (function, lines 2037-2074)
  - `merge_multimodal_capabilities` (function, lines 2077-2084)
  - `parse_media_endpoints` (function, lines 2087-2101)
  - `infer_user_complexity_value` (function, lines 3371-3381)
  - `load_llm_config_from_source` (function, lines 3525-3559)
  - `parse_llm_config_profiles` (function, lines 3561-4147)
  - `looks_like_llm_config` (function, lines 4149-4223)

### `llm/client.py`

- Routed symbols: 2
- Cross-module imports: `config/constants.py`: `DEFAULT_REQUEST_TIMEOUT`, `OLLAMA_THINKING_TOOL_BUFFER`, `SAMPLE_AUDIO_WAV_B64`, `SAMPLE_IMAGE_PNG_B64`, `SAMPLE_VIDEO_MP4_B64`; `config/settings.py`: `default_multimodal_capabilities`, `infer_model_multimodal_capabilities`, `merge_multimodal_capabilities`, `parse_capability_overrides`, `parse_media_endpoints`; `llm/utils.py`: `complete_chat_endpoint`, `is_openai_compat_provider`, `is_openai_like_provider`, `split_thinking_content`; `utils/json_utils.py`: `canonicalize_tool_name`, `json_dumps`, `parse_json_object`, `parse_tool_arguments`, `parse_tool_arguments_with_error`; `utils/misc.py`: `MAX_TIMEOUT_SECONDS`, `MIN_TIMEOUT_SECONDS`, `make_id`, `normalize_timeout_seconds`, `now_ts`; `utils/text.py`: `trim`
- Symbols:
  - `OllamaError` (class, lines 10763-10766)
  - `OllamaClient` (class, lines 10768-11820)

### `llm/utils.py`

- Routed symbols: 25
- Cross-module imports: `config/constants.py`: `OPENAI_COMPAT_PROVIDER_NAMES`, `OPENAI_LIKE_PROVIDER_NAMES`; `utils/json_utils.py`: `json_dumps`, `parse_json_object`; `utils/text.py`: `trim`
- Symbols:
  - `probe_ollama_environment` (function, lines 3057-3070)
  - `list_ollama_models` (function, lines 3072-3074)
  - `_OLLAMA_TAG_CACHE_LOCK` (assignment, lines 3076-3076)
  - `_OLLAMA_TAG_CACHE` (assignment, lines 3077-3077)
  - `list_ollama_models_cached` (function, lines 3087-3124)
  - `resolve_ollama_model` (function, lines 3126-3136)
  - `infer_thinking_model` (function, lines 3138-3140)
  - `split_thinking_content` (function, lines 3142-3183)
  - `strip_thinking_content` (function, lines 3185-3186)
  - `check_ollama_model_ready` (function, lines 3188-3212)
  - `list_loaded_ollama_models` (function, lines 3214-3227)
  - `wake_ollama_model` (function, lines 3229-3259)
  - `try_pull_ollama_model` (function, lines 3261-3279)
  - `ordered_model_candidates` (function, lines 3281-3299)
  - `pick_working_ollama_model` (function, lines 3301-3317)
  - `extract_base_url` (function, lines 3350-3358)
  - `complete_chat_endpoint` (function, lines 3360-3369)
  - `normalize_openai_compat_provider_name` (function, lines 3383-3398)
  - `is_openai_compat_provider` (function, lines 3412-3413)
  - `is_openai_like_provider` (function, lines 3415-3416)
  - `openai_compat_probe_headers` (function, lines 3418-3429)
  - `openai_compat_model_list_urls` (function, lines 3431-3463)
  - `extract_openai_compat_model_ids` (function, lines 3465-3498)
  - `_is_http_url` (function, lines 3500-3505)
  - `_resolve_local_path` (function, lines 3507-3523)

### `rag/index.py`

- Routed symbols: 5
- Cross-module imports: `config/constants.py`: `RAG_DYNAMIC_NOISE_HARD_COMMUNITY_RATIO`, `RAG_DYNAMIC_NOISE_HARD_DOC_RATIO`, `RAG_DYNAMIC_NOISE_MIN_COMMUNITY_FREQ`, `RAG_DYNAMIC_NOISE_MIN_DOC_FREQ`, `RAG_DYNAMIC_NOISE_SOFT_COMMUNITY_RATIO`, `RAG_DYNAMIC_NOISE_SOFT_DOC_RATIO`, `RAG_EN_STOPWORDS`, `RAG_GRAPH_MAX_NODES`, `RAG_INCLUDE_FILENAME_ENTITIES_DEFAULT`, `RAG_MAX_COMMUNITY_MAP_SUPPORT`, `RAG_MAX_GLOBAL_COMMUNITIES`, `RAG_MAX_QUERY_RESULTS`; `rag/parsers.py`: `_code_is_test_path`, `_rag_apply_filename_entity_policy`, `_rag_choose_community`, `_rag_classify_document`, `_rag_expand_tokens`, `_rag_extract_entities`, `_rag_filter_entities`, `_rag_tokenize`; `utils/json_utils.py`: `json_dumps`; `utils/misc.py`: `now_ts`; `utils/text.py`: `trim`
- Symbols:
  - `_code_module_name` (function, lines 40963-40977)
  - `_code_choose_community` (function, lines 40980-40987)
  - `_code_query_terms` (function, lines 40990-41002)
  - `TFGraphIDFIndex` (class, lines 41978-43336)
  - `CodeGraphIndex` (class, lines 44776-45188)

### `rag/ingestion.py`

- Routed symbols: 3
- Cross-module imports: `config/constants.py`: `CODE_IMPORT_WORKER_COUNT`, `CODE_LIBRARY_IGNORED_DIRS`, `CODE_PARSE_TIMEOUT_SECONDS`, `RAG_IMPORT_WORKER_COUNT`, `RAG_MAX_IMPORT_BATCH_ITEMS`, `RAG_MAX_IMPORT_FILES`, `RAG_MODEL_MEDIA_MAX_BYTES`, `RAG_PARSE_TIMEOUT_SECONDS`, `RAG_PDF_IMAGE_LIMIT`; `config/settings.py`: `default_multimodal_capabilities`; `rag/parsers.py`: `CodeContentParser`, `RAGContentParser`, `_rag_extract_entities`, `_rag_safe_name`; `rag/store.py`: `CodeLibraryStore`, `RAGLibraryStore`; `session/state.py`: `SessionState`; `utils/files.py`: `try_read_text`; `utils/json_utils.py`: `_read_json_file`, `_write_json_file`, `parse_json_object`; `utils/media.py`: `guess_mime_from_name`; `utils/misc.py`: `make_id`, `now_ts`; `utils/text.py`: `trim`
- Symbols:
  - `_rag_parse_file_worker` (function, lines 43889-43903)
  - `RAGIngestionService` (class, lines 43906-44773)
  - `CodeIngestionService` (class, lines 45457-45541)

### `rag/parsers.py`

- Routed symbols: 22
- Cross-module imports: `config/constants.py`: `AUDIO_EXTS`, `CODE_CHUNK_CHARS`, `CODE_CHUNK_OVERLAP`, `CODE_LIBRARY_LANGUAGE_BY_EXT`, `CODE_LIBRARY_SPECIAL_FILENAMES`, `CODE_MAX_CHUNKS_PER_DOC`, `CODE_PREVIEW_EXTS`, `CODE_PREVIEW_FILENAMES`, `CODE_PREVIEW_STAGE_MAX_ROWS`, `DOCUMENT_PREVIEW_EXTS`, `EXCEL_PREVIEW_EXTS`, `IMAGE_EXTS`, `PRESENTATION_PREVIEW_EXTS`, `RAG_CHUNK_CHARS`, `RAG_CHUNK_OVERLAP`, `RAG_CODE_HINTS`, `RAG_EN_STOPWORDS`, `RAG_GENERIC_ENTITY_TERMS_EN`, `RAG_GENERIC_ENTITY_TERMS_ZH`, `RAG_INCLUDE_FILENAME_ENTITIES_DEFAULT`, `RAG_MAX_CHUNKS_PER_DOC`, `RAG_PDF_IMAGE_LIMIT`, `RAG_RESEARCH_HINTS`, `RAG_SHORT_TOKEN_ALLOWLIST`, `RAG_STRUCTURAL_ENTITY_PATTERNS`, `RAG_TERM_GROUPS`, `RAG_ZH_STOPWORDS`, `TABULAR_PREVIEW_EXTS`, `VIDEO_EXTS`; `utils/files.py`: `_sha256_bytes`, `_sha256_file`; `utils/json_utils.py`: `parse_json_object`; `utils/media.py`: `guess_mime_from_name`; `utils/text.py`: `_compress_rows_keep_hotspot`, `_skip_row`, `trim`
- Symbols:
  - `normalize_rel_preview_path` (function, lines 4829-4840)
  - `is_code_preview_candidate` (function, lines 4843-4851)
  - `preview_kind_for_path` (function, lines 4860-4887)
  - `build_code_preview_rows` (function, lines 4890-5074)
  - `_rag_safe_name` (function, lines 40547-40550)
  - `_rag_detect_language` (function, lines 40553-40567)
  - `_rag_cjk_ngrams` (function, lines 40570-40582)
  - `_rag_is_noise_token` (function, lines 40585-40604)
  - `_rag_entity_allowed` (function, lines 40607-40619)
  - `_rag_filter_entities` (function, lines 40622-40636)
  - `_rag_filename_entity_aliases` (function, lines 40639-40672)
  - `_rag_apply_filename_entity_policy` (function, lines 40675-40705)
  - `_rag_choose_community` (function, lines 40708-40725)
  - `_rag_tokenize` (function, lines 40728-40758)
  - `_rag_expand_tokens` (function, lines 40761-40775)
  - `_rag_extract_entities` (function, lines 40778-40794)
  - `_rag_classify_document` (function, lines 40797-40831)
  - `_rag_chunk_text` (function, lines 40834-40864)
  - `_code_language_from_name` (function, lines 40939-40955)
  - `_code_is_test_path` (function, lines 40958-40960)
  - `CodeContentParser` (class, lines 41005-41465)
  - `RAGContentParser` (class, lines 41468-41975)

### `rag/store.py`

- Routed symbols: 2
- Cross-module imports: `config/constants.py`: `CODE_CHUNK_CHARS`, `CODE_CHUNK_OVERLAP`, `CODE_MAX_CHUNKS_PER_DOC`, `RAG_INCLUDE_FILENAME_ENTITIES_DEFAULT`, `RAG_TASK_HISTORY_LIMIT`; `rag/index.py`: `CodeGraphIndex`, `TFGraphIDFIndex`, `_code_choose_community`, `_code_module_name`; `rag/parsers.py`: `_code_is_test_path`, `_rag_apply_filename_entity_policy`, `_rag_choose_community`, `_rag_chunk_text`, `_rag_entity_allowed`, `_rag_extract_entities`, `_rag_safe_name`; `utils/files.py`: `_sha256_bytes`, `_sha256_file`; `utils/json_utils.py`: `_read_json_file`, `_write_json_file`; `utils/media.py`: `guess_mime_from_name`; `utils/misc.py`: `make_id`, `now_ts`; `utils/text.py`: `trim`
- Symbols:
  - `RAGLibraryStore` (class, lines 43339-43886)
  - `CodeLibraryStore` (class, lines 45191-45454)

### `server/handlers.py`

- Routed symbols: 5
- Cross-module imports: `app/context.py`: `AppContext`; `config/constants.py`: `APP_VERSION`, `DEFAULT_REQUEST_TIMEOUT`, `DEFAULT_UI_LANGUAGE`, `DEFAULT_UI_STYLE`, `EXECUTION_MODE_CHOICES`, `EXECUTION_MODE_SYNC`, `MIN_RUN_TIMEOUT_SECONDS`, `PLAN_MODE_USER_CHOICES`, `RAG_GRAPH_MAX_NODES`, `SSE_HEARTBEAT_SECONDS`, `TASK_COMPLEXITY_LEVELS`, `TASK_LEVEL_CHOICES`, `TASK_LEVEL_POLICIES`, `UI_STYLE_LABELS`; `config/paths.py`: `LLM_CONFIG_PATH`, `REPO_ROOT`, `WORKDIR`; `config/settings.py`: `_to_bool_like`, `infer_user_complexity_value`, `looks_like_llm_config`, `normalize_execution_mode`, `normalize_ui_language`, `normalize_ui_style`, `resolve_web_ui_dir_path`, `supported_ui_languages_payload`; `llm/utils.py`: `extract_base_url`, `extract_openai_compat_model_ids`, `list_ollama_models`, `normalize_openai_compat_provider_name`, `openai_compat_model_list_urls`, `openai_compat_probe_headers`; `session/manager.py`: `SessionManager`; `session/state.py`: `SessionState`; `skills/store.py`: `analyze_skill_building_knowledge`; `utils/files.py`: `safe_path`, `try_read_text`; `utils/json_utils.py`: `json_dumps`, `parse_json_object`; `utils/media.py`: `guess_mime_from_name`; `utils/misc.py`: `now_ts`, `swallow_benign_socket_error`, `user_id_from_ip`; `utils/text.py`: `trim`
- Symbols:
  - `AgentHTTPServer` (class, lines 49393-49421)
  - `Handler` (class, lines 49423-50222)
  - `SkillsHandler` (class, lines 50224-50419)
  - `RagAdminHandler` (class, lines 50421-50575)
  - `CodeAdminHandler` (class, lines 50578-50732)

### `session/manager.py`

- Routed symbols: 1
- Cross-module imports: `config/constants.py`: `AGENT_MAX_OUTPUT_TOKENS`, `ARBITER_DEFAULT_MAX_TOKENS`, `ARBITER_DEFAULT_TEMPERATURE`, `ARBITER_DEFAULT_TIMEOUT_SECONDS`, `DEFAULT_REQUEST_TIMEOUT`, `DEFAULT_UI_LANGUAGE`, `EXECUTION_MODE_SYNC`, `MAX_AGENT_ROUNDS`, `MAX_AGENT_ROUNDS_CAP`, `MAX_RUN_SECONDS`, `MAX_RUN_TIMEOUT_SECONDS`, `MIN_AGENT_ROUNDS`, `MIN_CONTEXT_TOKEN_LIMIT`, `MIN_RUN_TIMEOUT_SECONDS`, `TOKEN_THRESHOLD`; `config/paths.py`: `LLM_CONFIG_PATH`; `config/settings.py`: `infer_model_multimodal_capabilities`, `merge_multimodal_capabilities`, `normalize_execution_mode`, `normalize_ui_language`, `parse_capability_overrides`, `parse_llm_config_profiles`; `llm/client.py`: `OllamaClient`; `llm/utils.py`: `complete_chat_endpoint`, `extract_base_url`, `is_openai_compat_provider`, `list_ollama_models_cached`, `probe_ollama_environment`; `session/state.py`: `SessionState`; `utils/crypto.py`: `CryptoBox`; `utils/files.py`: `try_read_text`; `utils/json_utils.py`: `parse_json_object`; `utils/misc.py`: `make_id`, `normalize_timeout_seconds`, `now_ts`, `sanitize_profile_id`
- Symbols:
  - `SessionManager` (class, lines 35385-36257)

### `session/state.py`

- Routed symbols: 1
- Cross-module imports: `agent/background.py`: `BackgroundManager`; `agent/bus.py`: `MessageBus`; `agent/events.py`: `EventHub`; `agent/tasks.py`: `TaskManager`; `agent/todo.py`: `TodoManager`; `agent/worktree.py`: `WorktreeManager`; `config/constants.py`: `AGENT_BUBBLE_ROLES`, `AGENT_CTX_LIMIT_TIER0`, `AGENT_CTX_LIMIT_TIER1`, `AGENT_CTX_LIMIT_TIER2`, `AGENT_CTX_LIMIT_TIER3`, `AGENT_MAX_OUTPUT_TOKENS`, `AGENT_MSG_LIMIT_TIER0`, `AGENT_MSG_LIMIT_TIER1`, `AGENT_MSG_LIMIT_TIER2`, `AGENT_MSG_LIMIT_TIER3`, `AGENT_ROLES`, `AGENT_TOOL_ALLOWLIST`, `ARBITER_DEFAULT_MAX_TOKENS`, `ARBITER_DEFAULT_TEMPERATURE`, `ARBITER_DEFAULT_TIMEOUT_SECONDS`, `ARBITER_TRIGGER_MIN_CONTENT_CHARS`, `ARBITER_VALID_PLANNING_STREAK_LIMIT`, `ASSISTANT_MESSAGE_EVENT_MAX_CHARS`, `ASSISTANT_TEXT_PERSIST_MAX_CHARS`, `AUDIO_EXTS`, `AUTO_CONTINUE_BUDGET_DEFAULT`, `BASH_READ_LOOP_THRESHOLD`, `BLACKBOARD_MAX_LOG_ENTRIES`, `BLACKBOARD_MAX_TEXT`, `BLACKBOARD_STATUSES`, `CHECKPOINT_INTERVAL_ROUNDS`, `CHECKPOINT_MAX_COUNT`, `CODE_PREVIEW_STAGE_MAX_BYTES`, `CODE_PREVIEW_STAGE_MAX_PER_FILE`, `CODE_PREVIEW_STAGE_MAX_ROWS`, `CODE_PREVIEW_STAGE_MAX_TOTAL`, `COMPACT_TIER1_ABS`, `COMPACT_TIER1_PCT`, `COMPACT_TIER2_ABS`, `COMPACT_TIER2_PCT`, `COMPACT_TIER3_PCT`, `DANGEROUS_PATTERNS`, `DEEP_RESEARCH_REQUEST_KEYWORDS`, `DEEP_RESEARCH_RETRIEVAL_KEYWORDS`, `DEEP_RESEARCH_TEXT_ONLY_HINT_KEYWORDS`, `DEFAULT_REQUEST_TIMEOUT`, `DEFAULT_UI_LANGUAGE`, `DEVELOPER_EDIT_STALL_THRESHOLD`, `EMPTY_ACTION_MIN_CONTENT_CHARS`, `EMPTY_ACTION_WAKEUP_RETRY_LIMIT`, `ERROR_CATEGORY_DEFS`, `EXECUTION_MODE_CHOICES`, `EXECUTION_MODE_SEQUENTIAL`, `EXECUTION_MODE_SINGLE`, `EXECUTION_MODE_SYNC`, `EXPLORER_STALL_THRESHOLD`, `FAILURE_LEDGER_MAX_COMPILE_ERRORS`, `FAILURE_LEDGER_MAX_DELEGATIONS`, `FAILURE_LEDGER_MAX_ERRORS`, `FAILURE_LEDGER_MAX_FIXES`, `FAILURE_LEDGER_MAX_STALLS`, `FAILURE_LEDGER_MAX_TOOL_FPS`, `FILE_BUFFER_CONTENT_THRESHOLD`, `FILE_BUFFER_MAX_FILES`, `FINAL_SUMMARY_MIN_CHARS`, `FINAL_SUMMARY_STRICT_MIN_CHARS`, `FUSED_FAULT_BREAK_THRESHOLD`, `HARD_BREAK_RECOVERY_ROUND_THRESHOLD`, `HARD_BREAK_TOOL_ERROR_THRESHOLD`, `HTML_FRONTEND_REQUEST_KEYWORDS`, `IMAGE_EXTS`, `IMAGE_FORMATS_NEED_CONVERSION`, `LIVE_INPUT_DELAY_NORMAL_ROUNDS`, `LIVE_INPUT_DELAY_TOOL_ROUNDS`, `LIVE_INPUT_DELAY_WRITE_ROUNDS`, `LIVE_INPUT_MAX_INJECTIONS`, `LIVE_INPUT_REINJECT_INTERVAL`, `LIVE_INPUT_WEIGHT_BASE_DELAYED`, `LIVE_INPUT_WEIGHT_BASE_NORMAL`, `LIVE_INPUT_WEIGHT_STEP_DELAYED`, `LIVE_INPUT_WEIGHT_STEP_NORMAL`, `LONG_OUTPUT_LISTING_OFFLOAD_CHARS`, `LONG_OUTPUT_MODEL_PAGE_CHARS`, `LONG_OUTPUT_READ_PAGE_LINES`, `LONG_OUTPUT_READ_PAGE_MAX_CHARS`, `LONG_OUTPUT_TEMP_MAX_FILES`, `LONG_OUTPUT_UI_PAGE_CHARS`, `LONG_OUTPUT_UI_PREVIEW_MAX_PAGES`, `MANAGER_CTX_LIMIT_TIER0`, `MANAGER_CTX_LIMIT_TIER1`, `MANAGER_CTX_LIMIT_TIER2`, `MANAGER_CTX_LIMIT_TIER3`, `MANAGER_ROUTE_TARGETS`, `MAX_AGENT_ROUNDS`, `MAX_AGENT_ROUNDS_CAP`, `MAX_CONTEXT_ARCHIVE_SEGMENTS`, `MAX_RUN_SECONDS`, `MAX_RUN_TIMEOUT_SECONDS`, `MIN_AGENT_ROUNDS`, `MIN_CONTEXT_TOKEN_LIMIT`, `MIN_RUN_TIMEOUT_SECONDS`, `MODEL_CALL_PROGRESS_DELAY`, `MODEL_CALL_PROGRESS_INTERVAL`, `MODEL_OUTPUT_RETRY_TIMES`, `PERSISTED_ROUTES_MAX`, `PLAN_BUBBLE_MAX_CHARS`, `PLAN_FILE_RELATIVE_PATH`, `PLAN_MODE_ENABLED_LEVELS`, `PLAN_MODE_EXPLORER_MAX_ROUNDS`, `PLAN_MODE_FORCED_LEVELS`, `PLAN_MODE_MANAGER_SYNTHESIS_MAX_TOKENS`, `PLAN_MODE_MAX_OPTIONS`, `PLAN_MODE_RESEARCH_TOOL_ALLOWLIST`, `PLAN_MODE_USER_CHOICES`, `RENDER_FRAME_ACTIVITY_INTERVAL_SECONDS`, `RENDER_FRAME_MAX_B64_CHARS`, `RENDER_FRAME_MAX_LINES`, `RENDER_FRAME_MAX_LINE_POINTS`, `RENDER_FRAME_MAX_POINTS`, `REPEATED_TOOL_LOOP_THRESHOLD`, `RETRY_RUNTIME_HINT_PREFIXES`, `REVIEWER_DEBUG_MODE_MAX_ROUNDS`, `RUNTIME_CONTROL_HINT_PREFIXES`, `SEMANTIC_CONFIDENCE_CHOICES`, `SKILLS_VIRTUAL_PREFIX`, `SKILL_REFRESH_MIN_INTERVAL_SECONDS`, `SKILL_RUNTIME_CACHE_MAX_BYTES`, `SKILL_RUNTIME_CACHE_MAX_ENTRIES`, `STALL_ESCALATION_CONTEXT_MAX_CHARS`, `STALL_ESCALATION_MIN_LEVEL`, `STALL_PLAN_SYNTHESIS_MAX_TOKENS`, `STALL_SEVERITY_DECAY_ON_SUCCESS`, `STALL_SEVERITY_ESCALATION_THRESHOLD`, `STALL_SEVERITY_WEIGHT_BASH_READ_LOOP`, `STALL_SEVERITY_WEIGHT_FAULT`, `STALL_SEVERITY_WEIGHT_RECOVERY_RETRY`, `STALL_SEVERITY_WEIGHT_REPEATED_TOOL`, `STALL_SEVERITY_WEIGHT_WATCHDOG`, `TASK_COMPLEXITY_LEVELS`, `TASK_LEVEL_CHOICES`, `TASK_LEVEL_POLICIES`, `TASK_PHASE_ROUTING`, `TASK_PROFILE_TYPES`, `TASK_SCALE_PREFERENCES`, `THINKING_BUDGET_FORCE_RATIO`, `TOKEN_THRESHOLD`, `TRUNCATION_CONTINUATION_ECHO_CHARS`, `TRUNCATION_CONTINUATION_MAX_PASSES`, `TRUNCATION_CONTINUATION_MAX_TOKENS`, `TRUNCATION_CONTINUATION_TAIL_CHARS`, `TRUNCATION_LIVE_BUFFER_MAX_CHARS`, `TRUNCATION_OVERLAP_SCAN_CHARS`, `TRUNCATION_PAIR_SCAN_CHARS`, `VIDEO_EXTS`, `WATCHDOG_CONTEXT_NEAR_RATIO`, `WATCHDOG_CONTEXT_STALL_THRESHOLD`, `WATCHDOG_INTENT_NO_TOOL_THRESHOLD`, `WATCHDOG_INTENT_NO_TOOL_THRESHOLD_SINGLE`, `WATCHDOG_MAX_DECOMPOSE_STEPS`, `WATCHDOG_REPEAT_NO_TOOL_THRESHOLD`, `WATCHDOG_REPEAT_NO_TOOL_THRESHOLD_SINGLE`, `WATCHDOG_REPEAT_SIMILARITY_THRESHOLD`, `WATCHDOG_STATE_STALL_THRESHOLD`, `WATCHDOG_STEP_MAX_ATTEMPTS`, `_DEFAULT_TOOL_TIMEOUT`, `_TOOL_TIMEOUT_MAP`; `config/paths.py`: `WORKDIR`; `config/settings.py`: `_detect_os_shell_instruction`, `_to_bool_like`, `backend_i18n_text`, `backend_role_label`, `default_multimodal_capabilities`, `infer_model_multimodal_capabilities`, `infer_user_complexity_value`, `looks_like_llm_config`, `merge_multimodal_capabilities`, `model_language_instruction`, `normalize_execution_mode`, `normalize_ui_language`, `parse_capability_overrides`, `parse_llm_config_profiles`; `llm/client.py`: `OllamaClient`, `OllamaError`; `llm/utils.py`: `complete_chat_endpoint`, `extract_base_url`, `is_openai_compat_provider`, `list_loaded_ollama_models`, `list_ollama_models`, `list_ollama_models_cached`, `probe_ollama_environment`, `resolve_ollama_model`, `split_thinking_content`, `strip_thinking_content`, `wake_ollama_model`; `rag/parsers.py`: `build_code_preview_rows`, `is_code_preview_candidate`, `normalize_rel_preview_path`, `preview_kind_for_path`; `skills/store.py`: `SkillStore`, `ensure_runtime_skills`; `utils/compress.py`: `compress_text_blob`, `decompress_text_blob`; `utils/crypto.py`: `CryptoBox`; `utils/errors.py`: `CircuitBreakerTriggered`, `EmptyActionError`; `utils/files.py`: `_normalize_external_js_url`, `_safe_js_filename`, `cache_external_js_url`, `ensure_offline_js_libs`, `is_external_js_src`, `load_offline_js_lib_index`, `match_offline_js_catalog_by_url`, `offline_js_lib_root`, `safe_path`, `try_read_text`; `utils/json_utils.py`: `TOOLS`, `TOOL_REQUIRED_ARGS`, `canonicalize_tool_name`, `extract_json_object_from_text`, `json_dumps`, `parse_json_object`, `repair_truncated_json_object`, `tool_def`; `utils/media.py`: `_convert_image_to_safe_format`, `guess_ext_from_mime`, `guess_mime_from_name`; `utils/misc.py`: `MAX_TIMEOUT_SECONDS`, `MIN_TIMEOUT_SECONDS`, `is_benign_socket_error`, `make_id`, `normalize_timeout_seconds`, `now_ts`, `sanitize_profile_id`; `utils/text.py`: `MAX_TOOL_OUTPUT`, `_fmt_export_ts`, `_html_esc`, `_text_to_minimal_pdf`, `filter_runtime_noise_lines`, `make_numbered_diff`, `make_unified_diff`, `normalize_work_text`, `parse_front_matter`, `render_numbered_diff_text`, `trim`
- Symbols:
  - `SessionState` (class, lines 12103-35383)

### `skills/store.py`

- Routed symbols: 23
- Cross-module imports: `config/constants.py`: `BUILTIN_CLAWHUB_SKILLS_VERSION`, `EMBEDDED_CLAWHUB_SKILLS_ARCHIVE_B64`, `EMBEDDED_SKILLS_ARCHIVE_B64`, `EMBEDDED_SKILLS_ARCHIVE_FILES`, `EMBEDDED_SKILLS_ARCHIVE_SHA256`, `SKILLS_EXTERNAL_MOUNT`, `SKILLS_VIRTUAL_PREFIX`, `SKILL_BODY_COMPACT_THRESHOLD_CHARS`, `SKILL_BODY_PREVIEW_CHARS`, `SKILL_DEFAULT_ATTACHMENT_GLOBS`, `SKILL_INLINE_ATTACHMENT_MAX_CHARS`, `SKILL_INLINE_ATTACHMENT_MAX_FILES`, `SKILL_PROMPT_MAX_CHARS`, `SKILL_PROMPT_MAX_ITEMS`, `SKILL_PROTOCOL_CLAWHUB`, `SKILL_PROTOCOL_HTTP_JSON`, `SKILL_PROTOCOL_LOCAL`, `SKILL_PROTOCOL_SPECS`, `SKILL_REFRESH_MIN_INTERVAL_SECONDS`, `SKILL_RESOURCE_MANIFEST_MAX_ITEMS`; `config/paths.py`: `WORKDIR`; `llm/utils.py`: `_is_http_url`; `utils/files.py`: `_render_offline_js_catalog_md`, `safe_path`, `try_read_text`; `utils/json_utils.py`: `json_dumps`, `parse_json_object`; `utils/misc.py`: `_meta_string_list`, `_module_exists`, `now_ts`; `utils/text.py`: `parse_front_matter`, `trim`
- Symbols:
  - `ensure_embedded_skills_at_root` (function, lines 5916-5968)
  - `ensure_embedded_skills` (function, lines 5971-5972)
  - `detect_upload_parser_capabilities` (function, lines 5980-5995)
  - `_render_cap_markdown` (function, lines 5997-6011)
  - `_write_text_if_changed` (function, lines 6013-6018)
  - `ensure_generated_document_skills` (function, lines 6020-6108)
  - `ensure_generated_image_coding_feedback_skill` (function, lines 6110-6209)
  - `_skill_knowledge_files` (function, lines 6211-6230)
  - `analyze_skill_building_knowledge` (function, lines 6232-6286)
  - `_sanitize_skill_slug` (function, lines 6288-6290)
  - `_build_skills_gen_skill_content` (function, lines 6292-6323)
  - `ensure_generated_skills_gen_skill` (function, lines 6325-6329)
  - `ensure_generated_execution_recovery_skill` (function, lines 6331-6409)
  - `ensure_generated_html_frontend_report_skills` (function, lines 6411-6616)
  - `ensure_generated_deep_research_skills` (function, lines 6618-6886)
  - `ensure_generated_research_scientific_skills` (function, lines 6888-7524)
  - `ensure_generated_rag_mastery_skills` (function, lines 7530-7826)
  - `ensure_generated_multimodal_comprehension_skills` (function, lines 7832-8521)
  - `ensure_generated_runtime_skills_manifest` (function, lines 8524-8555)
  - `ensure_embedded_clawhub_skills` (function, lines 8806-8843)
  - `ensure_runtime_skills` (function, lines 8845-8857)
  - `_BUILTIN_SKILLS` (assignment, lines 8899-8986)
  - `SkillStore` (class, lines 8988-10282)

### `utils/compress.py`

- Routed symbols: 2
- Cross-module imports: none
- Symbols:
  - `compress_text_blob` (function, lines 2915-2920)
  - `decompress_text_blob` (function, lines 2922-2930)

### `utils/crypto.py`

- Routed symbols: 1
- Cross-module imports: `utils/json_utils.py`: `json_dumps`
- Symbols:
  - `CryptoBox` (class, lines 4233-4350)

### `utils/errors.py`

- Routed symbols: 2
- Cross-module imports: none
- Symbols:
  - `EmptyActionError` (class, lines 3080-3081)
  - `CircuitBreakerTriggered` (class, lines 3084-3085)

### `utils/files.py`

- Routed symbols: 25
- Cross-module imports: `config/constants.py`: `OFFLINE_JS_LIB_CATALOG`, `OFFLINE_JS_LIB_INDEX_FILE`, `OFFLINE_JS_LIB_README_FILE`; `config/paths.py`: `WORKDIR`; `utils/json_utils.py`: `json_dumps`; `utils/misc.py`: `now_ts`; `utils/text.py`: `trim`
- Symbols:
  - `_normalize_js_lib_asset_ref` (function, lines 1119-1132)
  - `_resolve_js_lib_asset_path` (function, lines 1135-1164)
  - `_discover_extra_js_lib_files` (function, lines 1167-1197)
  - `safe_path` (function, lines 2292-2301)
  - `_safe_js_filename` (function, lines 2303-2310)
  - `_sha256_bytes` (function, lines 2312-2313)
  - `_sha256_file` (function, lines 2315-2323)
  - `_download_http_bytes` (function, lines 2325-2333)
  - `offline_js_lib_root` (function, lines 2335-2336)
  - `_offline_js_entry_relative_path` (function, lines 2338-2342)
  - `_archive_member_relative_path` (function, lines 2344-2353)
  - `_path_size_bytes` (function, lines 2355-2370)
  - `_extract_archive_to_dir` (function, lines 2372-2412)
  - `_package_required_paths` (function, lines 2414-2420)
  - `_package_install_ready` (function, lines 2422-2430)
  - `_postprocess_offline_js_package` (function, lines 2432-2467)
  - `_ensure_offline_js_package` (function, lines 2469-2508)
  - `_render_offline_js_catalog_md` (function, lines 2510-2526)
  - `load_offline_js_lib_index` (function, lines 2528-2537)
  - `ensure_offline_js_libs` (function, lines 2539-2683)
  - `_normalize_external_js_url` (function, lines 2685-2689)
  - `is_external_js_src` (function, lines 2691-2693)
  - `match_offline_js_catalog_by_url` (function, lines 2695-2711)
  - `cache_external_js_url` (function, lines 2713-2745)
  - `try_read_text` (function, lines 4555-4563)

### `utils/json_utils.py`

- Routed symbols: 16
- Cross-module imports: `utils/text.py`: `trim`
- Symbols:
  - `JSON_FSYNC_ENABLED` (constant, lines 101-101)
  - `json_dumps` (function, lines 2264-2265)
  - `parse_tool_arguments` (function, lines 2959-2968)
  - `repair_truncated_json_object` (function, lines 2970-3023)
  - `parse_tool_arguments_with_error` (function, lines 3025-3055)
  - `parse_json_object` (function, lines 3319-3324)
  - `extract_json_object_from_text` (function, lines 3326-3348)
  - `_json_default_copy` (function, lines 4565-4570)
  - `_read_json_file` (function, lines 4572-4592)
  - `_write_json_file` (function, lines 4594-4621)
  - `tool_def` (function, lines 11822-11834)
  - `TOOLS` (constant, lines 11836-12012)
  - `TOOL_REQUIRED_ARGS` (constant, lines 12014-12014)
  - `TOOL_SPEC_BY_NAME` (constant, lines 12015-12015)
  - `TOOL_NAME_FUZZY_MAP` (constant, lines 12027-12027)
  - `canonicalize_tool_name` (function, lines 12045-12056)

### `utils/media.py`

- Routed symbols: 3
- Cross-module imports: none
- Symbols:
  - `guess_mime_from_name` (function, lines 2104-2106)
  - `_convert_image_to_safe_format` (function, lines 2109-2126)
  - `guess_ext_from_mime` (function, lines 2129-2135)

### `utils/misc.py`

- Routed symbols: 19
- Cross-module imports: none
- Symbols:
  - `MIN_TIMEOUT_SECONDS` (constant, lines 173-173)
  - `MAX_TIMEOUT_SECONDS` (constant, lines 174-174)
  - `DEFAULT_TIMEOUT_SECONDS` (constant, lines 175-181)
  - `BENIGN_SOCKET_DEBUG_LOG_ENABLED` (constant, lines 271-277)
  - `BENIGN_SOCKET_LOG_INTERVAL_SECONDS` (constant, lines 278-278)
  - `now_ts` (function, lines 2137-2138)
  - `_benign_socket_log_lock` (assignment, lines 2141-2141)
  - `_benign_socket_log_state` (assignment, lines 2142-2142)
  - `is_benign_socket_error` (function, lines 2160-2178)
  - `_socket_error_code` (function, lines 2181-2190)
  - `_log_benign_socket_error_limited` (function, lines 2193-2227)
  - `swallow_benign_socket_error` (function, lines 2230-2234)
  - `normalize_timeout_seconds` (function, lines 2237-2250)
  - `detect_local_lan_ip` (function, lines 2252-2262)
  - `make_id` (function, lines 2267-2268)
  - `sanitize_profile_id` (function, lines 2270-2272)
  - `user_id_from_ip` (function, lines 4225-4231)
  - `_meta_string_list` (function, lines 4542-4553)
  - `_module_exists` (function, lines 5974-5978)

### `utils/text.py`

- Routed symbols: 16
- Cross-module imports: none
- Symbols:
  - `MAX_TOOL_OUTPUT` (constant, lines 93-93)
  - `SOCKET_NOISE_LINE_PATTERNS` (constant, lines 265-270)
  - `filter_runtime_noise_lines` (function, lines 2145-2157)
  - `trim` (function, lines 2747-2749)
  - `_fmt_export_ts` (function, lines 2752-2760)
  - `_html_esc` (function, lines 2763-2764)
  - `_text_to_minimal_pdf` (function, lines 2767-2913)
  - `normalize_work_text` (function, lines 2932-2957)
  - `parse_front_matter` (function, lines 4352-4539)
  - `make_unified_diff` (function, lines 4623-4640)
  - `_skip_row` (function, lines 4642-4646)
  - `_row_is_hot` (function, lines 4649-4650)
  - `_hotspot_index` (function, lines 4653-4674)
  - `_compress_rows_keep_hotspot` (function, lines 4677-4724)
  - `make_numbered_diff` (function, lines 4727-4812)
  - `render_numbered_diff_text` (function, lines 4814-4826)
