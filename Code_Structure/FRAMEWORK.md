# Code_Structure Framework

## Overview

- Source file: `/Users/macbookair/Downloads/Split Coder/Clouds_Coder.py`
- Output directory: `/Users/macbookair/Downloads/Split Coder/Code_Structure`
- Generated modules: 29
- Top-level symbols: 489
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
| `config/constants.py` | 279 | `utils/json_utils.py`, `utils/misc.py` |
| `config/paths.py` | 8 | `utils/text.py` |
| `config/settings.py` | 26 | `config/constants.py`, `config/paths.py`, `llm/utils.py`, `skills/store.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` |
| `llm/client.py` | 2 | `config/constants.py`, `config/settings.py`, `llm/utils.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` |
| `llm/utils.py` | 19 | `utils/json_utils.py`, `utils/text.py` |
| `rag/index.py` | 5 | `config/constants.py`, `rag/parsers.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` |
| `rag/ingestion.py` | 3 | `config/constants.py`, `config/settings.py`, `rag/parsers.py`, `rag/store.py`, `session/state.py`, `utils/files.py`, `utils/json_utils.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py` |
| `rag/parsers.py` | 22 | `config/constants.py`, `utils/files.py`, `utils/json_utils.py`, `utils/media.py`, `utils/text.py` |
| `rag/store.py` | 2 | `config/constants.py`, `rag/index.py`, `rag/parsers.py`, `utils/files.py`, `utils/json_utils.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py` |
| `server/handlers.py` | 5 | `app/context.py`, `config/constants.py`, `config/paths.py`, `config/settings.py`, `llm/utils.py`, `session/manager.py`, `session/state.py`, `skills/store.py`, `utils/files.py`, `utils/json_utils.py`, `utils/media.py`, `utils/misc.py` |
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
  - `main` (function, lines 49609-50459)
  - `_main_guard_50461` (main_guard, lines 50461-50462)

### `agent/background.py`

- Routed symbols: 1
- Cross-module imports: `utils/misc.py`: `make_id`, `now_ts`; `utils/text.py`: `trim`
- Symbols:
  - `BackgroundManager` (class, lines 10034-10114)

### `agent/bus.py`

- Routed symbols: 1
- Cross-module imports: `config/constants.py`: `VALID_MSG_TYPES`; `utils/crypto.py`: `CryptoBox`; `utils/misc.py`: `now_ts`
- Symbols:
  - `MessageBus` (class, lines 10116-10170)

### `agent/events.py`

- Routed symbols: 1
- Cross-module imports: none
- Symbols:
  - `EventHub` (class, lines 4699-4744)

### `agent/tasks.py`

- Routed symbols: 1
- Cross-module imports: `utils/crypto.py`: `CryptoBox`; `utils/json_utils.py`: `json_dumps`; `utils/misc.py`: `now_ts`
- Symbols:
  - `TaskManager` (class, lines 9906-10032)

### `agent/todo.py`

- Routed symbols: 1
- Cross-module imports: `config/constants.py`: `DEFAULT_UI_LANGUAGE`; `config/settings.py`: `backend_i18n_text`, `backend_role_label`, `normalize_ui_language`; `utils/text.py`: `normalize_work_text`, `trim`
- Symbols:
  - `TodoManager` (class, lines 4746-4990)

### `agent/worktree.py`

- Routed symbols: 1
- Cross-module imports: `agent/tasks.py`: `TaskManager`; `config/constants.py`: `DANGEROUS_PATTERNS`; `utils/crypto.py`: `CryptoBox`; `utils/json_utils.py`: `json_dumps`; `utils/misc.py`: `now_ts`; `utils/text.py`: `trim`
- Symbols:
  - `WorktreeManager` (class, lines 10172-10383)

### `app/context.py`

- Routed symbols: 1
- Cross-module imports: `config/constants.py`: `AGENT_MAX_OUTPUT_TOKENS`, `APP_CSS`, `APP_JS`, `APP_TS`, `ARBITER_DEFAULT_MAX_TOKENS`, `ARBITER_DEFAULT_TEMPERATURE`, `ARBITER_DEFAULT_TIMEOUT_SECONDS`, `CODE_ADMIN_CSS`, `CODE_ADMIN_INDEX_HTML`, `CODE_ADMIN_JS`, `CODE_IMPORT_WORKER_COUNT`, `CODE_LIBRARY_DIRNAME`, `CODE_PARSE_TIMEOUT_SECONDS`, `DEFAULT_REQUEST_TIMEOUT`, `DEFAULT_UI_LANGUAGE`, `DEFAULT_UI_STYLE`, `DEFAULT_WEB_UI_DIR`, `EXECUTION_MODE_SYNC`, `INDEX_HTML`, `MAX_AGENT_ROUNDS`, `MAX_AGENT_ROUNDS_CAP`, `MAX_RUN_SECONDS`, `MAX_RUN_TIMEOUT_SECONDS`, `MIN_AGENT_ROUNDS`, `MIN_CONTEXT_TOKEN_LIMIT`, `MIN_RUN_TIMEOUT_SECONDS`, `RAG_ADMIN_CSS`, `RAG_ADMIN_INDEX_HTML`, `RAG_ADMIN_JS`, `RAG_GRAPH_MAX_NODES`, `RAG_IMPORT_WORKER_COUNT`, `RAG_INCLUDE_FILENAME_ENTITIES_DEFAULT`, `RAG_LIBRARY_DIRNAME`, `RAG_MAX_GLOBAL_COMMUNITIES`, `RAG_MAX_IMPORT_BATCH_BYTES`, `RAG_MAX_IMPORT_BATCH_ITEMS`, `RAG_MAX_IMPORT_FILES`, `RAG_MAX_QUERY_RESULTS`, `RAG_PARSE_TIMEOUT_SECONDS`, `RAG_QUERY_CONTEXT_CHARS`, `SKILLS_APP_JS`, `SKILLS_EXTRA_CSS`, `SKILLS_INDEX_HTML`, `SKILL_REFRESH_MIN_INTERVAL_SECONDS`, `TOKEN_THRESHOLD`, `WEB_UI_OPTIONAL_FILES`, `WEB_UI_REQUIRED_FILES`; `config/paths.py`: `LLM_CONFIG_PATH`, `REPO_ROOT`, `SCRIPT_DIR`, `_migrate_legacy_runtime_roots`; `config/settings.py`: `default_multimodal_capabilities`, `infer_model_multimodal_capabilities`, `merge_multimodal_capabilities`, `model_language_instruction`, `normalize_execution_mode`, `normalize_ui_language`, `normalize_ui_style`, `parse_capability_overrides`, `parse_llm_config_profiles`, `resolve_optional_file_path`, `resolve_web_ui_dir_path`; `llm/client.py`: `OllamaClient`; `llm/utils.py`: `extract_base_url`; `rag/ingestion.py`: `CodeIngestionService`, `RAGIngestionService`; `rag/parsers.py`: `CodeContentParser`, `RAGContentParser`; `rag/store.py`: `CodeLibraryStore`, `RAGLibraryStore`; `session/manager.py`: `SessionManager`; `session/state.py`: `SessionState`; `skills/store.py`: `SkillStore`, `_sanitize_skill_slug`, `analyze_skill_building_knowledge`, `ensure_runtime_skills`; `utils/crypto.py`: `CryptoBox`; `utils/files.py`: `_resolve_js_lib_asset_path`, `ensure_offline_js_libs`, `load_offline_js_lib_index`, `offline_js_lib_root`, `safe_path`, `try_read_text`; `utils/json_utils.py`: `TOOLS`, `extract_json_object_from_text`, `json_dumps`, `parse_json_object`; `utils/misc.py`: `DEFAULT_TIMEOUT_SECONDS`, `MAX_TIMEOUT_SECONDS`, `MIN_TIMEOUT_SECONDS`, `normalize_timeout_seconds`, `now_ts`, `sanitize_profile_id`; `utils/text.py`: `parse_front_matter`, `trim`
- Symbols:
  - `AppContext` (class, lines 46075-48384)

### `config/constants.py`

- Routed symbols: 279
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
  - `PLAN_MODE_EXPLORER_MAX_ROUNDS` (constant, lines 473-473)
  - `REVIEWER_DEBUG_MODE_MAX_ROUNDS` (constant, lines 475-475)
  - `REVIEWER_DEBUG_TOOL_ALLOWLIST` (constant, lines 476-480)
  - `EXPLORER_STALL_THRESHOLD` (constant, lines 481-481)
  - `DEVELOPER_EDIT_STALL_THRESHOLD` (constant, lines 482-482)
  - `PLAN_MODE_MANAGER_SYNTHESIS_MAX_TOKENS` (constant, lines 483-483)
  - `PLAN_MODE_MAX_OPTIONS` (constant, lines 484-484)
  - `PLAN_FILE_RELATIVE_PATH` (constant, lines 485-485)
  - `PLAN_BUBBLE_MAX_CHARS` (constant, lines 486-486)
  - `PLAN_MODE_RESEARCH_TOOL_ALLOWLIST` (constant, lines 487-491)
  - `FAILURE_LEDGER_MAX_FIXES` (constant, lines 492-492)
  - `FAILURE_LEDGER_MAX_COMPILE_ERRORS` (constant, lines 493-493)
  - `FAILURE_LEDGER_MAX_DELEGATIONS` (constant, lines 494-494)
  - `FAILURE_LEDGER_MAX_STALLS` (constant, lines 495-495)
  - `FAILURE_LEDGER_MAX_TOOL_FPS` (constant, lines 496-496)
  - `FAILURE_LEDGER_MAX_ERRORS` (constant, lines 497-497)
  - `ERROR_CATEGORY_DEFS` (constant, lines 500-537)
  - `CHECKPOINT_MAX_COUNT` (constant, lines 538-538)
  - `CHECKPOINT_INTERVAL_ROUNDS` (constant, lines 539-539)
  - `PERSISTED_ROUTES_MAX` (constant, lines 540-540)
  - `HTML_FRONTEND_REQUEST_KEYWORDS` (constant, lines 541-580)
  - `DEEP_RESEARCH_REQUEST_KEYWORDS` (constant, lines 581-603)
  - `DEEP_RESEARCH_RETRIEVAL_KEYWORDS` (constant, lines 604-623)
  - `DEEP_RESEARCH_TEXT_ONLY_HINT_KEYWORDS` (constant, lines 624-641)
  - `DANGEROUS_PATTERNS` (constant, lines 643-643)
  - `VALID_MSG_TYPES` (constant, lines 644-650)
  - `SUPPORTED_UI_LANGUAGES` (constant, lines 652-657)
  - `UI_LANGUAGE_LABELS` (constant, lines 658-658)
  - `DEFAULT_UI_LANGUAGE` (constant, lines 659-659)
  - `UI_STYLE_CHOICES` (constant, lines 660-660)
  - `UI_STYLE_LABELS` (constant, lines 661-661)
  - `DEFAULT_UI_STYLE` (constant, lines 662-662)
  - `DEFAULT_WEB_UI_DIR` (constant, lines 663-663)
  - `DEFAULT_WEB_UI_CONFIG` (constant, lines 664-664)
  - `WEB_UI_REQUIRED_FILES` (constant, lines 665-672)
  - `WEB_UI_OPTIONAL_FILES` (constant, lines 673-673)
  - `IMAGE_EXTS` (constant, lines 675-688)
  - `IMAGE_FORMATS_NEED_CONVERSION` (constant, lines 689-689)
  - `IMAGE_SAFE_FORMATS` (constant, lines 690-690)
  - `AUDIO_EXTS` (constant, lines 691-701)
  - `VIDEO_EXTS` (constant, lines 702-712)
  - `CODE_PREVIEW_STAGE_MAX_BYTES` (constant, lines 713-713)
  - `CODE_PREVIEW_STAGE_MAX_ROWS` (constant, lines 714-714)
  - `CODE_PREVIEW_STAGE_MAX_PER_FILE` (constant, lines 715-715)
  - `CODE_PREVIEW_STAGE_MAX_TOTAL` (constant, lines 716-716)
  - `RENDER_FRAME_MAX_B64_CHARS` (constant, lines 717-717)
  - `RENDER_FRAME_MAX_POINTS` (constant, lines 718-718)
  - `RENDER_FRAME_MAX_LINES` (constant, lines 719-719)
  - `RENDER_FRAME_MAX_LINE_POINTS` (constant, lines 720-720)
  - `RENDER_FRAME_ACTIVITY_INTERVAL_SECONDS` (constant, lines 721-721)
  - `RAW_TOOLCALL_TEXT_FILTER_THRESHOLD` (constant, lines 722-722)
  - `ASSISTANT_TEXT_PERSIST_MAX_CHARS` (constant, lines 723-723)
  - `ASSISTANT_MESSAGE_EVENT_MAX_CHARS` (constant, lines 724-724)
  - `CODE_PREVIEW_EXTS` (constant, lines 725-814)
  - `CODE_PREVIEW_FILENAMES` (constant, lines 815-826)
  - `MEDIA_CAPABILITY_KEYS` (constant, lines 827-834)
  - `SAMPLE_IMAGE_PNG_B64` (constant, lines 835-838)
  - `SAMPLE_AUDIO_WAV_B64` (constant, lines 839-841)
  - `SAMPLE_VIDEO_MP4_B64` (constant, lines 842-844)
  - `OFFLINE_JS_LIB_CATALOG` (constant, lines 846-1104)
  - `OFFLINE_JS_LIB_INDEX_FILE` (constant, lines 1105-1105)
  - `OFFLINE_JS_LIB_README_FILE` (constant, lines 1106-1106)
  - `BACKEND_I18N` (constant, lines 1292-1361)
  - `call_backend_i18n_en_update_l1363` (expression, lines 1363-1456)
  - `call_backend_i18n_zh_cn_update_l1457` (expression, lines 1457-1550)
  - `call_backend_i18n_zh_tw_update_l1551` (expression, lines 1551-1644)
  - `call_backend_i18n_ja_update_l1645` (expression, lines 1645-1738)
  - `TABULAR_PREVIEW_EXTS` (constant, lines 4477-4477)
  - `EXCEL_PREVIEW_EXTS` (constant, lines 4478-4478)
  - `PRESENTATION_PREVIEW_EXTS` (constant, lines 4479-4479)
  - `DOCUMENT_PREVIEW_EXTS` (constant, lines 4480-4480)
  - `EMBEDDED_SKILLS_ARCHIVE_B64` (constant, lines 4992-5511)
  - `EMBEDDED_SKILLS_ARCHIVE_SHA256` (constant, lines 5512-5512)
  - `EMBEDDED_SKILLS_ARCHIVE_FILES` (constant, lines 5513-5536)
  - `BUILTIN_CLAWHUB_SKILLS_VERSION` (constant, lines 8180-8180)
  - `EMBEDDED_CLAWHUB_SKILLS_ARCHIVE_B64` (constant, lines 8182-8426)
  - `SKILL_PROTOCOL_LOCAL` (constant, lines 8482-8482)
  - `SKILL_PROTOCOL_CLAWHUB` (constant, lines 8483-8483)
  - `SKILL_PROTOCOL_HTTP_JSON` (constant, lines 8484-8484)
  - `SKILL_PROTOCOL_SPECS` (constant, lines 8486-8517)
  - `AGENT_TOOL_ALLOWLIST` (constant, lines 11680-11723)
  - `INDEX_HTML` (constant, lines 35275-35462)
  - `APP_CSS` (constant, lines 35464-35842)
  - `APP_JS` (constant, lines 35844-38814)
  - `APP_TS` (constant, lines 38816-38843)
  - `SKILLS_INDEX_HTML` (constant, lines 38845-38999)
  - `SKILLS_EXTRA_CSS` (constant, lines 39001-39096)
  - `SKILLS_APP_JS` (constant, lines 39098-39238)
  - `RAG_TERM_GROUPS` (constant, lines 39240-39250)
  - `RAG_RESEARCH_HINTS` (constant, lines 39251-39272)
  - `RAG_CODE_HINTS` (constant, lines 39273-39283)
  - `RAG_SHORT_TOKEN_ALLOWLIST` (constant, lines 39284-39299)
  - `RAG_EN_STOPWORDS` (constant, lines 39300-39372)
  - `RAG_ZH_STOPWORDS` (constant, lines 39373-39409)
  - `RAG_GENERIC_ENTITY_TERMS_EN` (constant, lines 39410-39488)
  - `RAG_GENERIC_ENTITY_TERMS_ZH` (constant, lines 39489-39531)
  - `RAG_STRUCTURAL_ENTITY_PATTERNS` (constant, lines 39532-39550)
  - `CODE_LIBRARY_IGNORED_DIRS` (constant, lines 39873-39878)
  - `CODE_LIBRARY_LANGUAGE_BY_EXT` (constant, lines 39879-39935)
  - `CODE_LIBRARY_SPECIAL_FILENAMES` (constant, lines 39936-39942)
  - `RAG_ADMIN_INDEX_HTML` (constant, lines 44549-44706)
  - `RAG_ADMIN_CSS` (constant, lines 44708-44798)
  - `RAG_ADMIN_JS` (constant, lines 44800-46026)
  - `CODE_ADMIN_INDEX_HTML` (constant, lines 46028-46037)
  - `CODE_ADMIN_CSS` (constant, lines 46038-46068)
  - `CODE_ADMIN_JS` (constant, lines 46069-46073)

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
  - `detect_repo_root` (function, lines 2264-2278)
  - `REPO_ROOT` (constant, lines 2280-2280)

### `config/settings.py`

- Routed symbols: 26
- Cross-module imports: `config/constants.py`: `AUTO_SKILLS_ROOT_CANDIDATES`, `BACKEND_I18N`, `DEFAULT_REQUEST_TIMEOUT`, `DEFAULT_UI_LANGUAGE`, `DEFAULT_UI_STYLE`, `DEFAULT_WEB_UI_CONFIG`, `DEFAULT_WEB_UI_DIR`, `EXECUTION_MODE_CHOICES`, `EXECUTION_MODE_SEQUENTIAL`, `EXECUTION_MODE_SINGLE`, `EXECUTION_MODE_SYNC`, `MEDIA_CAPABILITY_KEYS`, `SUPPORTED_UI_LANGUAGES`, `UI_LANGUAGE_LABELS`, `UI_STYLE_CHOICES`; `config/paths.py`: `WORKDIR`; `llm/utils.py`: `_is_http_url`, `_resolve_local_path`, `complete_chat_endpoint`, `extract_base_url`; `skills/store.py`: `ensure_embedded_skills`; `utils/json_utils.py`: `parse_json_object`; `utils/misc.py`: `MAX_TIMEOUT_SECONDS`, `MIN_TIMEOUT_SECONDS`, `normalize_timeout_seconds`; `utils/text.py`: `trim`
- Symbols:
  - `normalize_ui_language` (function, lines 1190-1212)
  - `normalize_ui_style` (function, lines 1215-1232)
  - `supported_ui_languages_payload` (function, lines 1235-1236)
  - `normalize_execution_mode` (function, lines 1239-1258)
  - `model_language_instruction` (function, lines 1261-1289)
  - `backend_i18n_text` (function, lines 1741-1751)
  - `backend_role_label` (function, lines 1754-1758)
  - `_detect_os_shell_instruction` (function, lines 1761-1800)
  - `resolve_web_ui_dir_path` (function, lines 1802-1809)
  - `resolve_optional_file_path` (function, lines 1812-1819)
  - `resolve_skills_root_path` (function, lines 1822-1829)
  - `_count_skill_markdown_files` (function, lines 1832-1843)
  - `select_preferred_skills_root` (function, lines 1846-1880)
  - `load_web_ui_config_file` (function, lines 1883-1897)
  - `extract_show_upload_list_setting` (function, lines 1900-1914)
  - `extract_ui_style_setting` (function, lines 1917-1931)
  - `extract_js_lib_download_setting` (function, lines 1934-1953)
  - `default_multimodal_capabilities` (function, lines 1956-1964)
  - `_to_bool_like` (function, lines 1967-1977)
  - `infer_model_multimodal_capabilities` (function, lines 1980-2024)
  - `parse_capability_overrides` (function, lines 2027-2064)
  - `merge_multimodal_capabilities` (function, lines 2067-2074)
  - `parse_media_endpoints` (function, lines 2077-2091)
  - `load_llm_config_from_source` (function, lines 3386-3420)
  - `parse_llm_config_profiles` (function, lines 3422-3776)
  - `looks_like_llm_config` (function, lines 3778-3846)

### `llm/client.py`

- Routed symbols: 2
- Cross-module imports: `config/constants.py`: `DEFAULT_REQUEST_TIMEOUT`, `OLLAMA_THINKING_TOOL_BUFFER`, `SAMPLE_AUDIO_WAV_B64`, `SAMPLE_IMAGE_PNG_B64`, `SAMPLE_VIDEO_MP4_B64`; `config/settings.py`: `default_multimodal_capabilities`, `infer_model_multimodal_capabilities`, `merge_multimodal_capabilities`, `parse_capability_overrides`, `parse_media_endpoints`; `llm/utils.py`: `complete_chat_endpoint`, `split_thinking_content`; `utils/json_utils.py`: `canonicalize_tool_name`, `json_dumps`, `parse_json_object`, `parse_tool_arguments`, `parse_tool_arguments_with_error`; `utils/misc.py`: `MAX_TIMEOUT_SECONDS`, `MIN_TIMEOUT_SECONDS`, `make_id`, `normalize_timeout_seconds`, `now_ts`; `utils/text.py`: `trim`
- Symbols:
  - `OllamaError` (class, lines 10385-10388)
  - `OllamaClient` (class, lines 10390-11442)

### `llm/utils.py`

- Routed symbols: 19
- Cross-module imports: `utils/json_utils.py`: `json_dumps`, `parse_json_object`; `utils/text.py`: `trim`
- Symbols:
  - `probe_ollama_environment` (function, lines 3047-3060)
  - `list_ollama_models` (function, lines 3062-3064)
  - `_OLLAMA_TAG_CACHE_LOCK` (assignment, lines 3066-3066)
  - `_OLLAMA_TAG_CACHE` (assignment, lines 3067-3067)
  - `list_ollama_models_cached` (function, lines 3077-3114)
  - `resolve_ollama_model` (function, lines 3116-3126)
  - `infer_thinking_model` (function, lines 3128-3130)
  - `split_thinking_content` (function, lines 3132-3173)
  - `strip_thinking_content` (function, lines 3175-3176)
  - `check_ollama_model_ready` (function, lines 3178-3202)
  - `list_loaded_ollama_models` (function, lines 3204-3217)
  - `wake_ollama_model` (function, lines 3219-3249)
  - `try_pull_ollama_model` (function, lines 3251-3269)
  - `ordered_model_candidates` (function, lines 3271-3289)
  - `pick_working_ollama_model` (function, lines 3291-3307)
  - `extract_base_url` (function, lines 3340-3348)
  - `complete_chat_endpoint` (function, lines 3350-3359)
  - `_is_http_url` (function, lines 3361-3366)
  - `_resolve_local_path` (function, lines 3368-3384)

### `rag/index.py`

- Routed symbols: 5
- Cross-module imports: `config/constants.py`: `RAG_DYNAMIC_NOISE_HARD_COMMUNITY_RATIO`, `RAG_DYNAMIC_NOISE_HARD_DOC_RATIO`, `RAG_DYNAMIC_NOISE_MIN_COMMUNITY_FREQ`, `RAG_DYNAMIC_NOISE_MIN_DOC_FREQ`, `RAG_DYNAMIC_NOISE_SOFT_COMMUNITY_RATIO`, `RAG_DYNAMIC_NOISE_SOFT_DOC_RATIO`, `RAG_EN_STOPWORDS`, `RAG_GRAPH_MAX_NODES`, `RAG_INCLUDE_FILENAME_ENTITIES_DEFAULT`, `RAG_MAX_COMMUNITY_MAP_SUPPORT`, `RAG_MAX_GLOBAL_COMMUNITIES`, `RAG_MAX_QUERY_RESULTS`; `rag/parsers.py`: `_code_is_test_path`, `_rag_apply_filename_entity_policy`, `_rag_choose_community`, `_rag_classify_document`, `_rag_expand_tokens`, `_rag_extract_entities`, `_rag_filter_entities`, `_rag_tokenize`; `utils/json_utils.py`: `json_dumps`; `utils/misc.py`: `now_ts`; `utils/text.py`: `trim`
- Symbols:
  - `_code_module_name` (function, lines 39969-39983)
  - `_code_choose_community` (function, lines 39986-39993)
  - `_code_query_terms` (function, lines 39996-40008)
  - `TFGraphIDFIndex` (class, lines 40984-42342)
  - `CodeGraphIndex` (class, lines 43782-44194)

### `rag/ingestion.py`

- Routed symbols: 3
- Cross-module imports: `config/constants.py`: `CODE_IMPORT_WORKER_COUNT`, `CODE_LIBRARY_IGNORED_DIRS`, `CODE_PARSE_TIMEOUT_SECONDS`, `RAG_IMPORT_WORKER_COUNT`, `RAG_MAX_IMPORT_BATCH_ITEMS`, `RAG_MAX_IMPORT_FILES`, `RAG_MODEL_MEDIA_MAX_BYTES`, `RAG_PARSE_TIMEOUT_SECONDS`, `RAG_PDF_IMAGE_LIMIT`; `config/settings.py`: `default_multimodal_capabilities`; `rag/parsers.py`: `CodeContentParser`, `RAGContentParser`, `_rag_extract_entities`, `_rag_safe_name`; `rag/store.py`: `CodeLibraryStore`, `RAGLibraryStore`; `session/state.py`: `SessionState`; `utils/files.py`: `try_read_text`; `utils/json_utils.py`: `_read_json_file`, `_write_json_file`, `parse_json_object`; `utils/media.py`: `guess_mime_from_name`; `utils/misc.py`: `make_id`, `now_ts`; `utils/text.py`: `trim`
- Symbols:
  - `_rag_parse_file_worker` (function, lines 42895-42909)
  - `RAGIngestionService` (class, lines 42912-43779)
  - `CodeIngestionService` (class, lines 44463-44547)

### `rag/parsers.py`

- Routed symbols: 22
- Cross-module imports: `config/constants.py`: `AUDIO_EXTS`, `CODE_CHUNK_CHARS`, `CODE_CHUNK_OVERLAP`, `CODE_LIBRARY_LANGUAGE_BY_EXT`, `CODE_LIBRARY_SPECIAL_FILENAMES`, `CODE_MAX_CHUNKS_PER_DOC`, `CODE_PREVIEW_EXTS`, `CODE_PREVIEW_FILENAMES`, `CODE_PREVIEW_STAGE_MAX_ROWS`, `DOCUMENT_PREVIEW_EXTS`, `EXCEL_PREVIEW_EXTS`, `IMAGE_EXTS`, `PRESENTATION_PREVIEW_EXTS`, `RAG_CHUNK_CHARS`, `RAG_CHUNK_OVERLAP`, `RAG_CODE_HINTS`, `RAG_EN_STOPWORDS`, `RAG_GENERIC_ENTITY_TERMS_EN`, `RAG_GENERIC_ENTITY_TERMS_ZH`, `RAG_INCLUDE_FILENAME_ENTITIES_DEFAULT`, `RAG_MAX_CHUNKS_PER_DOC`, `RAG_PDF_IMAGE_LIMIT`, `RAG_RESEARCH_HINTS`, `RAG_SHORT_TOKEN_ALLOWLIST`, `RAG_STRUCTURAL_ENTITY_PATTERNS`, `RAG_TERM_GROUPS`, `RAG_ZH_STOPWORDS`, `TABULAR_PREVIEW_EXTS`, `VIDEO_EXTS`; `utils/files.py`: `_sha256_bytes`, `_sha256_file`; `utils/json_utils.py`: `parse_json_object`; `utils/media.py`: `guess_mime_from_name`; `utils/text.py`: `_compress_rows_keep_hotspot`, `_skip_row`, `trim`
- Symbols:
  - `normalize_rel_preview_path` (function, lines 4452-4463)
  - `is_code_preview_candidate` (function, lines 4466-4474)
  - `preview_kind_for_path` (function, lines 4483-4510)
  - `build_code_preview_rows` (function, lines 4513-4697)
  - `_rag_safe_name` (function, lines 39553-39556)
  - `_rag_detect_language` (function, lines 39559-39573)
  - `_rag_cjk_ngrams` (function, lines 39576-39588)
  - `_rag_is_noise_token` (function, lines 39591-39610)
  - `_rag_entity_allowed` (function, lines 39613-39625)
  - `_rag_filter_entities` (function, lines 39628-39642)
  - `_rag_filename_entity_aliases` (function, lines 39645-39678)
  - `_rag_apply_filename_entity_policy` (function, lines 39681-39711)
  - `_rag_choose_community` (function, lines 39714-39731)
  - `_rag_tokenize` (function, lines 39734-39764)
  - `_rag_expand_tokens` (function, lines 39767-39781)
  - `_rag_extract_entities` (function, lines 39784-39800)
  - `_rag_classify_document` (function, lines 39803-39837)
  - `_rag_chunk_text` (function, lines 39840-39870)
  - `_code_language_from_name` (function, lines 39945-39961)
  - `_code_is_test_path` (function, lines 39964-39966)
  - `CodeContentParser` (class, lines 40011-40471)
  - `RAGContentParser` (class, lines 40474-40981)

### `rag/store.py`

- Routed symbols: 2
- Cross-module imports: `config/constants.py`: `CODE_CHUNK_CHARS`, `CODE_CHUNK_OVERLAP`, `CODE_MAX_CHUNKS_PER_DOC`, `RAG_INCLUDE_FILENAME_ENTITIES_DEFAULT`, `RAG_TASK_HISTORY_LIMIT`; `rag/index.py`: `CodeGraphIndex`, `TFGraphIDFIndex`, `_code_choose_community`, `_code_module_name`; `rag/parsers.py`: `_code_is_test_path`, `_rag_apply_filename_entity_policy`, `_rag_choose_community`, `_rag_chunk_text`, `_rag_entity_allowed`, `_rag_extract_entities`, `_rag_safe_name`; `utils/files.py`: `_sha256_bytes`, `_sha256_file`; `utils/json_utils.py`: `_read_json_file`, `_write_json_file`; `utils/media.py`: `guess_mime_from_name`; `utils/misc.py`: `make_id`, `now_ts`; `utils/text.py`: `trim`
- Symbols:
  - `RAGLibraryStore` (class, lines 42345-42892)
  - `CodeLibraryStore` (class, lines 44197-44460)

### `server/handlers.py`

- Routed symbols: 5
- Cross-module imports: `app/context.py`: `AppContext`; `config/constants.py`: `APP_VERSION`, `DEFAULT_REQUEST_TIMEOUT`, `DEFAULT_UI_LANGUAGE`, `DEFAULT_UI_STYLE`, `EXECUTION_MODE_CHOICES`, `EXECUTION_MODE_SYNC`, `MIN_RUN_TIMEOUT_SECONDS`, `PLAN_MODE_USER_CHOICES`, `RAG_GRAPH_MAX_NODES`, `SSE_HEARTBEAT_SECONDS`, `TASK_LEVEL_CHOICES`, `TASK_LEVEL_POLICIES`, `UI_STYLE_LABELS`; `config/paths.py`: `LLM_CONFIG_PATH`, `REPO_ROOT`, `WORKDIR`; `config/settings.py`: `_to_bool_like`, `looks_like_llm_config`, `normalize_execution_mode`, `normalize_ui_language`, `normalize_ui_style`, `resolve_web_ui_dir_path`, `supported_ui_languages_payload`; `llm/utils.py`: `list_ollama_models`; `session/manager.py`: `SessionManager`; `session/state.py`: `SessionState`; `skills/store.py`: `analyze_skill_building_knowledge`; `utils/files.py`: `safe_path`, `try_read_text`; `utils/json_utils.py`: `json_dumps`, `parse_json_object`; `utils/media.py`: `guess_mime_from_name`; `utils/misc.py`: `now_ts`, `swallow_benign_socket_error`, `user_id_from_ip`
- Symbols:
  - `AgentHTTPServer` (class, lines 48386-48414)
  - `Handler` (class, lines 48416-49099)
  - `SkillsHandler` (class, lines 49101-49294)
  - `RagAdminHandler` (class, lines 49296-49450)
  - `CodeAdminHandler` (class, lines 49453-49607)

### `session/manager.py`

- Routed symbols: 1
- Cross-module imports: `config/constants.py`: `AGENT_MAX_OUTPUT_TOKENS`, `ARBITER_DEFAULT_MAX_TOKENS`, `ARBITER_DEFAULT_TEMPERATURE`, `ARBITER_DEFAULT_TIMEOUT_SECONDS`, `DEFAULT_REQUEST_TIMEOUT`, `DEFAULT_UI_LANGUAGE`, `EXECUTION_MODE_SYNC`, `MAX_AGENT_ROUNDS`, `MAX_AGENT_ROUNDS_CAP`, `MAX_RUN_SECONDS`, `MAX_RUN_TIMEOUT_SECONDS`, `MIN_AGENT_ROUNDS`, `MIN_CONTEXT_TOKEN_LIMIT`, `MIN_RUN_TIMEOUT_SECONDS`, `TOKEN_THRESHOLD`; `config/paths.py`: `LLM_CONFIG_PATH`; `config/settings.py`: `infer_model_multimodal_capabilities`, `merge_multimodal_capabilities`, `normalize_execution_mode`, `normalize_ui_language`, `parse_capability_overrides`, `parse_llm_config_profiles`; `llm/client.py`: `OllamaClient`; `llm/utils.py`: `complete_chat_endpoint`, `extract_base_url`, `list_ollama_models_cached`, `probe_ollama_environment`; `session/state.py`: `SessionState`; `utils/crypto.py`: `CryptoBox`; `utils/files.py`: `try_read_text`; `utils/json_utils.py`: `parse_json_object`; `utils/misc.py`: `make_id`, `normalize_timeout_seconds`, `now_ts`, `sanitize_profile_id`
- Symbols:
  - `SessionManager` (class, lines 34421-35273)

### `session/state.py`

- Routed symbols: 1
- Cross-module imports: `agent/background.py`: `BackgroundManager`; `agent/bus.py`: `MessageBus`; `agent/events.py`: `EventHub`; `agent/tasks.py`: `TaskManager`; `agent/todo.py`: `TodoManager`; `agent/worktree.py`: `WorktreeManager`; `config/constants.py`: `AGENT_BUBBLE_ROLES`, `AGENT_CTX_LIMIT_TIER0`, `AGENT_CTX_LIMIT_TIER1`, `AGENT_CTX_LIMIT_TIER2`, `AGENT_CTX_LIMIT_TIER3`, `AGENT_MAX_OUTPUT_TOKENS`, `AGENT_MSG_LIMIT_TIER0`, `AGENT_MSG_LIMIT_TIER1`, `AGENT_MSG_LIMIT_TIER2`, `AGENT_MSG_LIMIT_TIER3`, `AGENT_ROLES`, `AGENT_TOOL_ALLOWLIST`, `ARBITER_DEFAULT_MAX_TOKENS`, `ARBITER_DEFAULT_TEMPERATURE`, `ARBITER_DEFAULT_TIMEOUT_SECONDS`, `ARBITER_TRIGGER_MIN_CONTENT_CHARS`, `ARBITER_VALID_PLANNING_STREAK_LIMIT`, `ASSISTANT_MESSAGE_EVENT_MAX_CHARS`, `ASSISTANT_TEXT_PERSIST_MAX_CHARS`, `AUDIO_EXTS`, `AUTO_CONTINUE_BUDGET_DEFAULT`, `BASH_READ_LOOP_THRESHOLD`, `BLACKBOARD_MAX_LOG_ENTRIES`, `BLACKBOARD_MAX_TEXT`, `BLACKBOARD_STATUSES`, `CHECKPOINT_INTERVAL_ROUNDS`, `CHECKPOINT_MAX_COUNT`, `CODE_PREVIEW_STAGE_MAX_BYTES`, `CODE_PREVIEW_STAGE_MAX_PER_FILE`, `CODE_PREVIEW_STAGE_MAX_ROWS`, `CODE_PREVIEW_STAGE_MAX_TOTAL`, `COMPACT_TIER1_ABS`, `COMPACT_TIER1_PCT`, `COMPACT_TIER2_ABS`, `COMPACT_TIER2_PCT`, `COMPACT_TIER3_PCT`, `COMPLEXITY_KEYWORDS`, `DANGEROUS_PATTERNS`, `DEEP_RESEARCH_REQUEST_KEYWORDS`, `DEEP_RESEARCH_RETRIEVAL_KEYWORDS`, `DEEP_RESEARCH_TEXT_ONLY_HINT_KEYWORDS`, `DEFAULT_REQUEST_TIMEOUT`, `DEFAULT_UI_LANGUAGE`, `DEVELOPER_EDIT_STALL_THRESHOLD`, `EMPTY_ACTION_MIN_CONTENT_CHARS`, `EMPTY_ACTION_WAKEUP_RETRY_LIMIT`, `ERROR_CATEGORY_DEFS`, `EXECUTION_MODE_CHOICES`, `EXECUTION_MODE_SEQUENTIAL`, `EXECUTION_MODE_SINGLE`, `EXECUTION_MODE_SYNC`, `EXPLORER_STALL_THRESHOLD`, `FAILURE_LEDGER_MAX_COMPILE_ERRORS`, `FAILURE_LEDGER_MAX_DELEGATIONS`, `FAILURE_LEDGER_MAX_ERRORS`, `FAILURE_LEDGER_MAX_FIXES`, `FAILURE_LEDGER_MAX_STALLS`, `FAILURE_LEDGER_MAX_TOOL_FPS`, `FILE_BUFFER_CONTENT_THRESHOLD`, `FILE_BUFFER_MAX_FILES`, `FINAL_SUMMARY_MIN_CHARS`, `FINAL_SUMMARY_STRICT_MIN_CHARS`, `FUSED_FAULT_BREAK_THRESHOLD`, `HARD_BREAK_RECOVERY_ROUND_THRESHOLD`, `HARD_BREAK_TOOL_ERROR_THRESHOLD`, `HTML_FRONTEND_REQUEST_KEYWORDS`, `IMAGE_EXTS`, `IMAGE_FORMATS_NEED_CONVERSION`, `LIVE_INPUT_DELAY_NORMAL_ROUNDS`, `LIVE_INPUT_DELAY_TOOL_ROUNDS`, `LIVE_INPUT_DELAY_WRITE_ROUNDS`, `LIVE_INPUT_MAX_INJECTIONS`, `LIVE_INPUT_REINJECT_INTERVAL`, `LIVE_INPUT_WEIGHT_BASE_DELAYED`, `LIVE_INPUT_WEIGHT_BASE_NORMAL`, `LIVE_INPUT_WEIGHT_STEP_DELAYED`, `LIVE_INPUT_WEIGHT_STEP_NORMAL`, `LONG_OUTPUT_LISTING_OFFLOAD_CHARS`, `LONG_OUTPUT_MODEL_PAGE_CHARS`, `LONG_OUTPUT_READ_PAGE_LINES`, `LONG_OUTPUT_READ_PAGE_MAX_CHARS`, `LONG_OUTPUT_TEMP_MAX_FILES`, `LONG_OUTPUT_UI_PAGE_CHARS`, `LONG_OUTPUT_UI_PREVIEW_MAX_PAGES`, `MANAGER_CTX_LIMIT_TIER0`, `MANAGER_CTX_LIMIT_TIER1`, `MANAGER_CTX_LIMIT_TIER2`, `MANAGER_CTX_LIMIT_TIER3`, `MANAGER_ROUTE_TARGETS`, `MAX_AGENT_ROUNDS`, `MAX_AGENT_ROUNDS_CAP`, `MAX_CONTEXT_ARCHIVE_SEGMENTS`, `MAX_RUN_SECONDS`, `MAX_RUN_TIMEOUT_SECONDS`, `MIN_AGENT_ROUNDS`, `MIN_CONTEXT_TOKEN_LIMIT`, `MIN_RUN_TIMEOUT_SECONDS`, `MODEL_CALL_PROGRESS_DELAY`, `MODEL_CALL_PROGRESS_INTERVAL`, `MODEL_OUTPUT_RETRY_TIMES`, `PERSISTED_ROUTES_MAX`, `PLAN_BUBBLE_MAX_CHARS`, `PLAN_FILE_RELATIVE_PATH`, `PLAN_MODE_ENABLED_LEVELS`, `PLAN_MODE_EXPLORER_MAX_ROUNDS`, `PLAN_MODE_FORCED_LEVELS`, `PLAN_MODE_MANAGER_SYNTHESIS_MAX_TOKENS`, `PLAN_MODE_MAX_OPTIONS`, `PLAN_MODE_RESEARCH_TOOL_ALLOWLIST`, `PLAN_MODE_USER_CHOICES`, `RENDER_FRAME_ACTIVITY_INTERVAL_SECONDS`, `RENDER_FRAME_MAX_B64_CHARS`, `RENDER_FRAME_MAX_LINES`, `RENDER_FRAME_MAX_LINE_POINTS`, `RENDER_FRAME_MAX_POINTS`, `REPEATED_TOOL_LOOP_THRESHOLD`, `RETRY_RUNTIME_HINT_PREFIXES`, `REVIEWER_DEBUG_MODE_MAX_ROUNDS`, `RUNTIME_CONTROL_HINT_PREFIXES`, `SEMANTIC_CONFIDENCE_CHOICES`, `SKILLS_VIRTUAL_PREFIX`, `SKILL_REFRESH_MIN_INTERVAL_SECONDS`, `SKILL_RUNTIME_CACHE_MAX_BYTES`, `SKILL_RUNTIME_CACHE_MAX_ENTRIES`, `STALL_ESCALATION_CONTEXT_MAX_CHARS`, `STALL_ESCALATION_MIN_LEVEL`, `STALL_PLAN_SYNTHESIS_MAX_TOKENS`, `STALL_SEVERITY_DECAY_ON_SUCCESS`, `STALL_SEVERITY_ESCALATION_THRESHOLD`, `STALL_SEVERITY_WEIGHT_BASH_READ_LOOP`, `STALL_SEVERITY_WEIGHT_FAULT`, `STALL_SEVERITY_WEIGHT_RECOVERY_RETRY`, `STALL_SEVERITY_WEIGHT_REPEATED_TOOL`, `STALL_SEVERITY_WEIGHT_WATCHDOG`, `TASK_COMPLEXITY_LEVELS`, `TASK_LEVEL_CHOICES`, `TASK_LEVEL_POLICIES`, `TASK_PHASE_ROUTING`, `TASK_PROFILE_TYPES`, `TASK_SCALE_PREFERENCES`, `THINKING_BUDGET_FORCE_RATIO`, `TOKEN_THRESHOLD`, `TRUNCATION_CONTINUATION_ECHO_CHARS`, `TRUNCATION_CONTINUATION_MAX_PASSES`, `TRUNCATION_CONTINUATION_MAX_TOKENS`, `TRUNCATION_CONTINUATION_TAIL_CHARS`, `TRUNCATION_LIVE_BUFFER_MAX_CHARS`, `TRUNCATION_OVERLAP_SCAN_CHARS`, `TRUNCATION_PAIR_SCAN_CHARS`, `VIDEO_EXTS`, `WATCHDOG_CONTEXT_NEAR_RATIO`, `WATCHDOG_CONTEXT_STALL_THRESHOLD`, `WATCHDOG_INTENT_NO_TOOL_THRESHOLD`, `WATCHDOG_INTENT_NO_TOOL_THRESHOLD_SINGLE`, `WATCHDOG_MAX_DECOMPOSE_STEPS`, `WATCHDOG_REPEAT_NO_TOOL_THRESHOLD`, `WATCHDOG_REPEAT_NO_TOOL_THRESHOLD_SINGLE`, `WATCHDOG_REPEAT_SIMILARITY_THRESHOLD`, `WATCHDOG_STATE_STALL_THRESHOLD`, `WATCHDOG_STEP_MAX_ATTEMPTS`, `_DEFAULT_TOOL_TIMEOUT`, `_TOOL_TIMEOUT_MAP`; `config/paths.py`: `WORKDIR`; `config/settings.py`: `_detect_os_shell_instruction`, `_to_bool_like`, `backend_i18n_text`, `backend_role_label`, `default_multimodal_capabilities`, `infer_model_multimodal_capabilities`, `looks_like_llm_config`, `merge_multimodal_capabilities`, `model_language_instruction`, `normalize_execution_mode`, `normalize_ui_language`, `parse_capability_overrides`, `parse_llm_config_profiles`; `llm/client.py`: `OllamaClient`, `OllamaError`; `llm/utils.py`: `complete_chat_endpoint`, `list_loaded_ollama_models`, `list_ollama_models`, `list_ollama_models_cached`, `probe_ollama_environment`, `resolve_ollama_model`, `split_thinking_content`, `strip_thinking_content`, `wake_ollama_model`; `rag/parsers.py`: `build_code_preview_rows`, `is_code_preview_candidate`, `normalize_rel_preview_path`, `preview_kind_for_path`; `skills/store.py`: `SkillStore`, `ensure_runtime_skills`; `utils/compress.py`: `compress_text_blob`, `decompress_text_blob`; `utils/crypto.py`: `CryptoBox`; `utils/errors.py`: `CircuitBreakerTriggered`, `EmptyActionError`; `utils/files.py`: `_normalize_external_js_url`, `_safe_js_filename`, `cache_external_js_url`, `ensure_offline_js_libs`, `is_external_js_src`, `load_offline_js_lib_index`, `match_offline_js_catalog_by_url`, `offline_js_lib_root`, `safe_path`, `try_read_text`; `utils/json_utils.py`: `TOOLS`, `TOOL_REQUIRED_ARGS`, `canonicalize_tool_name`, `extract_json_object_from_text`, `json_dumps`, `parse_json_object`, `repair_truncated_json_object`, `tool_def`; `utils/media.py`: `_convert_image_to_safe_format`, `guess_ext_from_mime`, `guess_mime_from_name`; `utils/misc.py`: `MAX_TIMEOUT_SECONDS`, `MIN_TIMEOUT_SECONDS`, `is_benign_socket_error`, `make_id`, `normalize_timeout_seconds`, `now_ts`, `sanitize_profile_id`; `utils/text.py`: `MAX_TOOL_OUTPUT`, `_fmt_export_ts`, `_html_esc`, `_text_to_minimal_pdf`, `filter_runtime_noise_lines`, `make_numbered_diff`, `make_unified_diff`, `normalize_work_text`, `parse_front_matter`, `render_numbered_diff_text`, `trim`
- Symbols:
  - `SessionState` (class, lines 11725-34419)

### `skills/store.py`

- Routed symbols: 23
- Cross-module imports: `config/constants.py`: `BUILTIN_CLAWHUB_SKILLS_VERSION`, `EMBEDDED_CLAWHUB_SKILLS_ARCHIVE_B64`, `EMBEDDED_SKILLS_ARCHIVE_B64`, `EMBEDDED_SKILLS_ARCHIVE_FILES`, `EMBEDDED_SKILLS_ARCHIVE_SHA256`, `SKILLS_EXTERNAL_MOUNT`, `SKILLS_VIRTUAL_PREFIX`, `SKILL_BODY_COMPACT_THRESHOLD_CHARS`, `SKILL_BODY_PREVIEW_CHARS`, `SKILL_DEFAULT_ATTACHMENT_GLOBS`, `SKILL_INLINE_ATTACHMENT_MAX_CHARS`, `SKILL_INLINE_ATTACHMENT_MAX_FILES`, `SKILL_PROMPT_MAX_CHARS`, `SKILL_PROMPT_MAX_ITEMS`, `SKILL_PROTOCOL_CLAWHUB`, `SKILL_PROTOCOL_HTTP_JSON`, `SKILL_PROTOCOL_LOCAL`, `SKILL_PROTOCOL_SPECS`, `SKILL_REFRESH_MIN_INTERVAL_SECONDS`, `SKILL_RESOURCE_MANIFEST_MAX_ITEMS`; `config/paths.py`: `WORKDIR`; `llm/utils.py`: `_is_http_url`; `utils/files.py`: `_render_offline_js_catalog_md`, `safe_path`, `try_read_text`; `utils/json_utils.py`: `json_dumps`, `parse_json_object`; `utils/misc.py`: `_meta_string_list`, `_module_exists`, `now_ts`; `utils/text.py`: `parse_front_matter`, `trim`
- Symbols:
  - `ensure_embedded_skills_at_root` (function, lines 5539-5591)
  - `ensure_embedded_skills` (function, lines 5594-5595)
  - `detect_upload_parser_capabilities` (function, lines 5603-5618)
  - `_render_cap_markdown` (function, lines 5620-5634)
  - `_write_text_if_changed` (function, lines 5636-5641)
  - `ensure_generated_document_skills` (function, lines 5643-5731)
  - `ensure_generated_image_coding_feedback_skill` (function, lines 5733-5832)
  - `_skill_knowledge_files` (function, lines 5834-5853)
  - `analyze_skill_building_knowledge` (function, lines 5855-5909)
  - `_sanitize_skill_slug` (function, lines 5911-5913)
  - `_build_skills_gen_skill_content` (function, lines 5915-5946)
  - `ensure_generated_skills_gen_skill` (function, lines 5948-5952)
  - `ensure_generated_execution_recovery_skill` (function, lines 5954-6032)
  - `ensure_generated_html_frontend_report_skills` (function, lines 6034-6239)
  - `ensure_generated_deep_research_skills` (function, lines 6241-6509)
  - `ensure_generated_research_scientific_skills` (function, lines 6511-7147)
  - `ensure_generated_rag_mastery_skills` (function, lines 7153-7449)
  - `ensure_generated_multimodal_comprehension_skills` (function, lines 7455-8144)
  - `ensure_generated_runtime_skills_manifest` (function, lines 8147-8178)
  - `ensure_embedded_clawhub_skills` (function, lines 8429-8466)
  - `ensure_runtime_skills` (function, lines 8468-8480)
  - `_BUILTIN_SKILLS` (assignment, lines 8522-8608)
  - `SkillStore` (class, lines 8610-9904)

### `utils/compress.py`

- Routed symbols: 2
- Cross-module imports: none
- Symbols:
  - `compress_text_blob` (function, lines 2905-2910)
  - `decompress_text_blob` (function, lines 2912-2920)

### `utils/crypto.py`

- Routed symbols: 1
- Cross-module imports: `utils/json_utils.py`: `json_dumps`
- Symbols:
  - `CryptoBox` (class, lines 3856-3973)

### `utils/errors.py`

- Routed symbols: 2
- Cross-module imports: none
- Symbols:
  - `EmptyActionError` (class, lines 3070-3071)
  - `CircuitBreakerTriggered` (class, lines 3074-3075)

### `utils/files.py`

- Routed symbols: 25
- Cross-module imports: `config/constants.py`: `OFFLINE_JS_LIB_CATALOG`, `OFFLINE_JS_LIB_INDEX_FILE`, `OFFLINE_JS_LIB_README_FILE`; `config/paths.py`: `WORKDIR`; `utils/json_utils.py`: `json_dumps`; `utils/misc.py`: `now_ts`; `utils/text.py`: `trim`
- Symbols:
  - `_normalize_js_lib_asset_ref` (function, lines 1109-1122)
  - `_resolve_js_lib_asset_path` (function, lines 1125-1154)
  - `_discover_extra_js_lib_files` (function, lines 1157-1187)
  - `safe_path` (function, lines 2282-2291)
  - `_safe_js_filename` (function, lines 2293-2300)
  - `_sha256_bytes` (function, lines 2302-2303)
  - `_sha256_file` (function, lines 2305-2313)
  - `_download_http_bytes` (function, lines 2315-2323)
  - `offline_js_lib_root` (function, lines 2325-2326)
  - `_offline_js_entry_relative_path` (function, lines 2328-2332)
  - `_archive_member_relative_path` (function, lines 2334-2343)
  - `_path_size_bytes` (function, lines 2345-2360)
  - `_extract_archive_to_dir` (function, lines 2362-2402)
  - `_package_required_paths` (function, lines 2404-2410)
  - `_package_install_ready` (function, lines 2412-2420)
  - `_postprocess_offline_js_package` (function, lines 2422-2457)
  - `_ensure_offline_js_package` (function, lines 2459-2498)
  - `_render_offline_js_catalog_md` (function, lines 2500-2516)
  - `load_offline_js_lib_index` (function, lines 2518-2527)
  - `ensure_offline_js_libs` (function, lines 2529-2673)
  - `_normalize_external_js_url` (function, lines 2675-2679)
  - `is_external_js_src` (function, lines 2681-2683)
  - `match_offline_js_catalog_by_url` (function, lines 2685-2701)
  - `cache_external_js_url` (function, lines 2703-2735)
  - `try_read_text` (function, lines 4178-4186)

### `utils/json_utils.py`

- Routed symbols: 16
- Cross-module imports: `utils/text.py`: `trim`
- Symbols:
  - `JSON_FSYNC_ENABLED` (constant, lines 101-101)
  - `json_dumps` (function, lines 2254-2255)
  - `parse_tool_arguments` (function, lines 2949-2958)
  - `repair_truncated_json_object` (function, lines 2960-3013)
  - `parse_tool_arguments_with_error` (function, lines 3015-3045)
  - `parse_json_object` (function, lines 3309-3314)
  - `extract_json_object_from_text` (function, lines 3316-3338)
  - `_json_default_copy` (function, lines 4188-4193)
  - `_read_json_file` (function, lines 4195-4215)
  - `_write_json_file` (function, lines 4217-4244)
  - `tool_def` (function, lines 11444-11456)
  - `TOOLS` (constant, lines 11458-11634)
  - `TOOL_REQUIRED_ARGS` (constant, lines 11636-11636)
  - `TOOL_SPEC_BY_NAME` (constant, lines 11637-11637)
  - `TOOL_NAME_FUZZY_MAP` (constant, lines 11649-11649)
  - `canonicalize_tool_name` (function, lines 11667-11678)

### `utils/media.py`

- Routed symbols: 3
- Cross-module imports: none
- Symbols:
  - `guess_mime_from_name` (function, lines 2094-2096)
  - `_convert_image_to_safe_format` (function, lines 2099-2116)
  - `guess_ext_from_mime` (function, lines 2119-2125)

### `utils/misc.py`

- Routed symbols: 19
- Cross-module imports: none
- Symbols:
  - `MIN_TIMEOUT_SECONDS` (constant, lines 173-173)
  - `MAX_TIMEOUT_SECONDS` (constant, lines 174-174)
  - `DEFAULT_TIMEOUT_SECONDS` (constant, lines 175-181)
  - `BENIGN_SOCKET_DEBUG_LOG_ENABLED` (constant, lines 271-277)
  - `BENIGN_SOCKET_LOG_INTERVAL_SECONDS` (constant, lines 278-278)
  - `now_ts` (function, lines 2127-2128)
  - `_benign_socket_log_lock` (assignment, lines 2131-2131)
  - `_benign_socket_log_state` (assignment, lines 2132-2132)
  - `is_benign_socket_error` (function, lines 2150-2168)
  - `_socket_error_code` (function, lines 2171-2180)
  - `_log_benign_socket_error_limited` (function, lines 2183-2217)
  - `swallow_benign_socket_error` (function, lines 2220-2224)
  - `normalize_timeout_seconds` (function, lines 2227-2240)
  - `detect_local_lan_ip` (function, lines 2242-2252)
  - `make_id` (function, lines 2257-2258)
  - `sanitize_profile_id` (function, lines 2260-2262)
  - `user_id_from_ip` (function, lines 3848-3854)
  - `_meta_string_list` (function, lines 4165-4176)
  - `_module_exists` (function, lines 5597-5601)

### `utils/text.py`

- Routed symbols: 16
- Cross-module imports: none
- Symbols:
  - `MAX_TOOL_OUTPUT` (constant, lines 93-93)
  - `SOCKET_NOISE_LINE_PATTERNS` (constant, lines 265-270)
  - `filter_runtime_noise_lines` (function, lines 2135-2147)
  - `trim` (function, lines 2737-2739)
  - `_fmt_export_ts` (function, lines 2742-2750)
  - `_html_esc` (function, lines 2753-2754)
  - `_text_to_minimal_pdf` (function, lines 2757-2903)
  - `normalize_work_text` (function, lines 2922-2947)
  - `parse_front_matter` (function, lines 3975-4162)
  - `make_unified_diff` (function, lines 4246-4263)
  - `_skip_row` (function, lines 4265-4269)
  - `_row_is_hot` (function, lines 4272-4273)
  - `_hotspot_index` (function, lines 4276-4297)
  - `_compress_rows_keep_hotspot` (function, lines 4300-4347)
  - `make_numbered_diff` (function, lines 4350-4435)
  - `render_numbered_diff_text` (function, lines 4437-4449)
