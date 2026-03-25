# Code_Structure Framework

## Overview

- Source file: `/Users/macbookair/Downloads/Split Coder/Clouds_Coder.py`
- Output directory: `/Users/macbookair/Downloads/Split Coder/Code_Structure`
- Generated modules: 29
- Top-level symbols: 461
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
| `__main__.py` | 2 | `app/context.py`, `config/constants.py`, `config/paths.py`, `config/settings.py`, `llm/utils.py`, `server/handlers.py`, `skills/store.py`, `utils/misc.py`, `utils/text.py` |
| `agent/background.py` | 1 | `utils/misc.py`, `utils/text.py` |
| `agent/bus.py` | 1 | `config/constants.py`, `utils/crypto.py`, `utils/misc.py` |
| `agent/events.py` | 1 | — |
| `agent/tasks.py` | 1 | `utils/crypto.py`, `utils/json_utils.py`, `utils/misc.py` |
| `agent/todo.py` | 1 | `utils/text.py` |
| `agent/worktree.py` | 1 | `agent/tasks.py`, `config/constants.py`, `utils/crypto.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` |
| `app/context.py` | 1 | `config/constants.py`, `config/paths.py`, `config/settings.py`, `llm/client.py`, `llm/utils.py`, `rag/ingestion.py`, `rag/parsers.py`, `rag/store.py`, `session/manager.py`, `session/state.py`, `skills/store.py`, `utils/crypto.py`, `utils/files.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` |
| `config/constants.py` | 267 | `utils/json_utils.py`, `utils/misc.py` |
| `config/paths.py` | 8 | `utils/text.py` |
| `config/settings.py` | 23 | `config/constants.py`, `config/paths.py`, `llm/utils.py`, `skills/store.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` |
| `llm/client.py` | 2 | `config/constants.py`, `config/settings.py`, `llm/utils.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` |
| `llm/utils.py` | 19 | `utils/json_utils.py`, `utils/text.py` |
| `rag/index.py` | 5 | `config/constants.py`, `rag/parsers.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` |
| `rag/ingestion.py` | 3 | `config/constants.py`, `config/settings.py`, `rag/parsers.py`, `rag/store.py`, `session/state.py`, `utils/files.py`, `utils/json_utils.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py` |
| `rag/parsers.py` | 22 | `config/constants.py`, `utils/files.py`, `utils/json_utils.py`, `utils/media.py`, `utils/text.py` |
| `rag/store.py` | 2 | `config/constants.py`, `rag/index.py`, `rag/parsers.py`, `utils/files.py`, `utils/json_utils.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py` |
| `server/handlers.py` | 5 | `app/context.py`, `config/constants.py`, `config/paths.py`, `config/settings.py`, `llm/utils.py`, `session/manager.py`, `session/state.py`, `skills/store.py`, `utils/files.py`, `utils/json_utils.py`, `utils/media.py`, `utils/misc.py` |
| `session/manager.py` | 1 | `config/constants.py`, `config/paths.py`, `config/settings.py`, `llm/client.py`, `llm/utils.py`, `session/state.py`, `utils/crypto.py`, `utils/files.py`, `utils/json_utils.py`, `utils/misc.py` |
| `session/state.py` | 1 | `agent/background.py`, `agent/bus.py`, `agent/events.py`, `agent/tasks.py`, `agent/todo.py`, `agent/worktree.py`, `config/constants.py`, `config/paths.py`, `config/settings.py`, `llm/client.py`, `llm/utils.py`, `rag/parsers.py`, `skills/store.py`, `utils/compress.py`, `utils/crypto.py`, `utils/errors.py`, `utils/files.py`, `utils/json_utils.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py` |
| `skills/store.py` | 21 | `config/constants.py`, `config/paths.py`, `llm/utils.py`, `utils/files.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` |
| `utils/compress.py` | 2 | — |
| `utils/crypto.py` | 1 | `utils/json_utils.py` |
| `utils/errors.py` | 2 | — |
| `utils/files.py` | 14 | `config/constants.py`, `config/paths.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` |
| `utils/json_utils.py` | 16 | `utils/text.py` |
| `utils/media.py` | 3 | — |
| `utils/misc.py` | 19 | — |
| `utils/text.py` | 16 | — |

## Module Details

### `__main__.py`

- Routed symbols: 2
- Cross-module imports: `app/context.py`: `AppContext`; `config/constants.py`: `AGENT_MAX_OUTPUT_TOKENS`, `ARBITER_DEFAULT_MAX_TOKENS`, `ARBITER_DEFAULT_TEMPERATURE`, `ARBITER_DEFAULT_TIMEOUT_SECONDS`, `CODE_ADMIN_PORT_OFFSET`, `DEFAULT_OLLAMA_BASE_URL`, `DEFAULT_OLLAMA_MODEL`, `DEFAULT_UI_LANGUAGE`, `DEFAULT_UI_STYLE`, `DEFAULT_WEB_UI_CONFIG`, `DEFAULT_WEB_UI_DIR`, `EXECUTION_MODE_SYNC`, `LIVE_INPUT_DELAY_NORMAL_ROUNDS`, `LIVE_INPUT_DELAY_TOOL_ROUNDS`, `LIVE_INPUT_DELAY_WRITE_ROUNDS`, `LIVE_INPUT_MAX_INJECTIONS`, `LIVE_INPUT_REINJECT_INTERVAL`, `LIVE_INPUT_WEIGHT_BASE_DELAYED`, `LIVE_INPUT_WEIGHT_BASE_NORMAL`, `LIVE_INPUT_WEIGHT_STEP_DELAYED`, `LIVE_INPUT_WEIGHT_STEP_NORMAL`, `MAX_AGENT_ROUNDS`, `MAX_AGENT_ROUNDS_CAP`, `MAX_RUN_SECONDS`, `MAX_RUN_TIMEOUT_SECONDS`, `MIN_AGENT_ROUNDS`, `MIN_CONTEXT_TOKEN_LIMIT`, `MIN_RUN_TIMEOUT_SECONDS`, `OFFLINE_JS_LIB_CATALOG`, `RAG_ADMIN_PORT_OFFSET`, `RAG_INCLUDE_FILENAME_ENTITIES_DEFAULT`, `TOKEN_THRESHOLD`, `UI_LANGUAGE_LABELS`, `UI_STYLE_LABELS`; `config/paths.py`: `LLM_CONFIG_PATH`, `REPO_ROOT`, `WORKDIR`; `config/settings.py`: `_to_bool_like`, `extract_show_upload_list_setting`, `extract_ui_style_setting`, `load_llm_config_from_source`, `load_web_ui_config_file`, `normalize_execution_mode`, `normalize_ui_language`, `normalize_ui_style`, `parse_llm_config_profiles`, `resolve_optional_file_path`, `resolve_web_ui_dir_path`, `select_preferred_skills_root`; `llm/utils.py`: `list_ollama_models`; `server/handlers.py`: `AgentHTTPServer`, `CodeAdminHandler`, `Handler`, `RagAdminHandler`, `SkillsHandler`; `skills/store.py`: `ensure_embedded_skills_at_root`, `ensure_runtime_skills`; `utils/misc.py`: `BENIGN_SOCKET_DEBUG_LOG_ENABLED`, `detect_local_lan_ip`, `normalize_timeout_seconds`, `swallow_benign_socket_error`; `utils/text.py`: `trim`
- Symbols:
  - `main` (function, lines 43379-44216)
  - `_main_guard_44218` (main_guard, lines 44218-44219)

### `agent/background.py`

- Routed symbols: 1
- Cross-module imports: `utils/misc.py`: `make_id`, `now_ts`; `utils/text.py`: `trim`
- Symbols:
  - `BackgroundManager` (class, lines 7664-7744)

### `agent/bus.py`

- Routed symbols: 1
- Cross-module imports: `config/constants.py`: `VALID_MSG_TYPES`; `utils/crypto.py`: `CryptoBox`; `utils/misc.py`: `now_ts`
- Symbols:
  - `MessageBus` (class, lines 7746-7800)

### `agent/events.py`

- Routed symbols: 1
- Cross-module imports: none
- Symbols:
  - `EventHub` (class, lines 3548-3593)

### `agent/tasks.py`

- Routed symbols: 1
- Cross-module imports: `utils/crypto.py`: `CryptoBox`; `utils/json_utils.py`: `json_dumps`; `utils/misc.py`: `now_ts`
- Symbols:
  - `TaskManager` (class, lines 7536-7662)

### `agent/todo.py`

- Routed symbols: 1
- Cross-module imports: `utils/text.py`: `normalize_work_text`, `trim`
- Symbols:
  - `TodoManager` (class, lines 3595-3773)

### `agent/worktree.py`

- Routed symbols: 1
- Cross-module imports: `agent/tasks.py`: `TaskManager`; `config/constants.py`: `DANGEROUS_PATTERNS`; `utils/crypto.py`: `CryptoBox`; `utils/json_utils.py`: `json_dumps`; `utils/misc.py`: `now_ts`; `utils/text.py`: `trim`
- Symbols:
  - `WorktreeManager` (class, lines 7802-8013)

### `app/context.py`

- Routed symbols: 1
- Cross-module imports: `config/constants.py`: `AGENT_MAX_OUTPUT_TOKENS`, `APP_CSS`, `APP_JS`, `APP_TS`, `ARBITER_DEFAULT_MAX_TOKENS`, `ARBITER_DEFAULT_TEMPERATURE`, `ARBITER_DEFAULT_TIMEOUT_SECONDS`, `CODE_ADMIN_CSS`, `CODE_ADMIN_INDEX_HTML`, `CODE_ADMIN_JS`, `CODE_IMPORT_WORKER_COUNT`, `CODE_LIBRARY_DIRNAME`, `CODE_PARSE_TIMEOUT_SECONDS`, `DEFAULT_REQUEST_TIMEOUT`, `DEFAULT_UI_LANGUAGE`, `DEFAULT_UI_STYLE`, `DEFAULT_WEB_UI_DIR`, `EXECUTION_MODE_SYNC`, `INDEX_HTML`, `MAX_AGENT_ROUNDS`, `MAX_AGENT_ROUNDS_CAP`, `MAX_RUN_SECONDS`, `MAX_RUN_TIMEOUT_SECONDS`, `MIN_AGENT_ROUNDS`, `MIN_CONTEXT_TOKEN_LIMIT`, `MIN_RUN_TIMEOUT_SECONDS`, `OFFLINE_JS_LIB_CATALOG`, `RAG_ADMIN_CSS`, `RAG_ADMIN_INDEX_HTML`, `RAG_ADMIN_JS`, `RAG_GRAPH_MAX_NODES`, `RAG_IMPORT_WORKER_COUNT`, `RAG_INCLUDE_FILENAME_ENTITIES_DEFAULT`, `RAG_LIBRARY_DIRNAME`, `RAG_MAX_GLOBAL_COMMUNITIES`, `RAG_MAX_IMPORT_BATCH_BYTES`, `RAG_MAX_IMPORT_BATCH_ITEMS`, `RAG_MAX_IMPORT_FILES`, `RAG_MAX_QUERY_RESULTS`, `RAG_PARSE_TIMEOUT_SECONDS`, `RAG_QUERY_CONTEXT_CHARS`, `SKILLS_APP_JS`, `SKILLS_EXTRA_CSS`, `SKILLS_INDEX_HTML`, `SKILL_REFRESH_MIN_INTERVAL_SECONDS`, `TOKEN_THRESHOLD`, `WEB_UI_OPTIONAL_FILES`, `WEB_UI_REQUIRED_FILES`; `config/paths.py`: `LLM_CONFIG_PATH`, `REPO_ROOT`, `_migrate_legacy_runtime_roots`; `config/settings.py`: `default_multimodal_capabilities`, `infer_model_multimodal_capabilities`, `merge_multimodal_capabilities`, `model_language_instruction`, `normalize_execution_mode`, `normalize_ui_language`, `normalize_ui_style`, `parse_capability_overrides`, `parse_llm_config_profiles`, `resolve_optional_file_path`, `resolve_web_ui_dir_path`; `llm/client.py`: `OllamaClient`; `llm/utils.py`: `extract_base_url`; `rag/ingestion.py`: `CodeIngestionService`, `RAGIngestionService`; `rag/parsers.py`: `CodeContentParser`, `RAGContentParser`; `rag/store.py`: `CodeLibraryStore`, `RAGLibraryStore`; `session/manager.py`: `SessionManager`; `session/state.py`: `SessionState`; `skills/store.py`: `SkillStore`, `_sanitize_skill_slug`, `analyze_skill_building_knowledge`, `ensure_runtime_skills`; `utils/crypto.py`: `CryptoBox`; `utils/files.py`: `_safe_js_filename`, `ensure_offline_js_libs`, `offline_js_lib_root`, `safe_path`, `try_read_text`; `utils/json_utils.py`: `TOOLS`, `extract_json_object_from_text`, `json_dumps`, `parse_json_object`; `utils/misc.py`: `DEFAULT_TIMEOUT_SECONDS`, `MAX_TIMEOUT_SECONDS`, `MIN_TIMEOUT_SECONDS`, `normalize_timeout_seconds`, `now_ts`, `sanitize_profile_id`; `utils/text.py`: `parse_front_matter`, `trim`
- Symbols:
  - `AppContext` (class, lines 39862-42188)

### `config/constants.py`

- Routed symbols: 267
- Cross-module imports: `utils/json_utils.py`: `TOOL_SPEC_BY_NAME`; `utils/misc.py`: `DEFAULT_TIMEOUT_SECONDS`
- Symbols:
  - `APP_VERSION` (constant, lines 47-47)
  - `DEFAULT_OLLAMA_BASE_URL` (constant, lines 48-48)
  - `DEFAULT_OLLAMA_MODEL` (constant, lines 49-49)
  - `LONG_OUTPUT_MODEL_PAGE_CHARS` (constant, lines 92-92)
  - `LONG_OUTPUT_UI_PAGE_CHARS` (constant, lines 93-93)
  - `LONG_OUTPUT_UI_PREVIEW_MAX_PAGES` (constant, lines 94-94)
  - `LONG_OUTPUT_LISTING_OFFLOAD_CHARS` (constant, lines 95-95)
  - `LONG_OUTPUT_READ_PAGE_LINES` (constant, lines 96-96)
  - `LONG_OUTPUT_READ_PAGE_MAX_CHARS` (constant, lines 97-97)
  - `LONG_OUTPUT_TEMP_MAX_FILES` (constant, lines 98-98)
  - `RAG_LIBRARY_DIRNAME` (constant, lines 100-100)
  - `RAG_ADMIN_PORT_OFFSET` (constant, lines 101-101)
  - `CODE_LIBRARY_DIRNAME` (constant, lines 102-102)
  - `CODE_ADMIN_PORT_OFFSET` (constant, lines 103-103)
  - `RAG_CHUNK_CHARS` (constant, lines 104-104)
  - `RAG_CHUNK_OVERLAP` (constant, lines 105-105)
  - `RAG_MAX_CHUNKS_PER_DOC` (constant, lines 106-106)
  - `CODE_CHUNK_CHARS` (constant, lines 107-107)
  - `CODE_CHUNK_OVERLAP` (constant, lines 108-108)
  - `CODE_MAX_CHUNKS_PER_DOC` (constant, lines 109-109)
  - `RAG_MAX_QUERY_RESULTS` (constant, lines 110-110)
  - `RAG_GRAPH_MAX_NODES` (constant, lines 111-111)
  - `RAG_TASK_HISTORY_LIMIT` (constant, lines 112-112)
  - `RAG_MODEL_MEDIA_MAX_BYTES` (constant, lines 113-113)
  - `RAG_MAX_IMPORT_FILES` (constant, lines 114-114)
  - `RAG_MAX_IMPORT_BATCH_ITEMS` (constant, lines 115-115)
  - `RAG_MAX_IMPORT_BATCH_BYTES` (constant, lines 116-116)
  - `RAG_PDF_IMAGE_LIMIT` (constant, lines 117-117)
  - `RAG_QUERY_CONTEXT_CHARS` (constant, lines 118-118)
  - `RAG_MAX_GLOBAL_COMMUNITIES` (constant, lines 119-119)
  - `RAG_MAX_COMMUNITY_MAP_SUPPORT` (constant, lines 120-120)
  - `RAG_INCLUDE_FILENAME_ENTITIES_DEFAULT` (constant, lines 121-121)
  - `RAG_DYNAMIC_NOISE_MIN_DOC_FREQ` (constant, lines 122-122)
  - `RAG_DYNAMIC_NOISE_MIN_COMMUNITY_FREQ` (constant, lines 123-123)
  - `RAG_DYNAMIC_NOISE_SOFT_DOC_RATIO` (constant, lines 124-124)
  - `RAG_DYNAMIC_NOISE_HARD_DOC_RATIO` (constant, lines 125-125)
  - `RAG_DYNAMIC_NOISE_SOFT_COMMUNITY_RATIO` (constant, lines 126-126)
  - `RAG_DYNAMIC_NOISE_HARD_COMMUNITY_RATIO` (constant, lines 127-127)
  - `RAG_IMPORT_WORKER_COUNT` (constant, lines 128-131)
  - `CODE_IMPORT_WORKER_COUNT` (constant, lines 132-135)
  - `RAG_PARSE_TIMEOUT_SECONDS` (constant, lines 136-139)
  - `CODE_PARSE_TIMEOUT_SECONDS` (constant, lines 140-143)
  - `TOKEN_THRESHOLD` (constant, lines 144-144)
  - `IDLE_TIMEOUT` (constant, lines 145-145)
  - `POLL_INTERVAL` (constant, lines 146-146)
  - `SSE_HEARTBEAT_SECONDS` (constant, lines 147-147)
  - `MODEL_CALL_PROGRESS_DELAY` (constant, lines 148-148)
  - `MODEL_CALL_PROGRESS_INTERVAL` (constant, lines 149-149)
  - `MAX_AGENT_ROUNDS` (constant, lines 150-150)
  - `MIN_AGENT_ROUNDS` (constant, lines 151-151)
  - `MAX_AGENT_ROUNDS_CAP` (constant, lines 152-152)
  - `REPEATED_TOOL_LOOP_THRESHOLD` (constant, lines 153-153)
  - `BASH_READ_LOOP_THRESHOLD` (constant, lines 154-154)
  - `HARD_BREAK_TOOL_ERROR_THRESHOLD` (constant, lines 155-155)
  - `HARD_BREAK_RECOVERY_ROUND_THRESHOLD` (constant, lines 156-156)
  - `FUSED_FAULT_BREAK_THRESHOLD` (constant, lines 157-157)
  - `STALL_SEVERITY_ESCALATION_THRESHOLD` (constant, lines 158-158)
  - `STALL_SEVERITY_WEIGHT_BASH_READ_LOOP` (constant, lines 159-159)
  - `STALL_SEVERITY_WEIGHT_REPEATED_TOOL` (constant, lines 160-160)
  - `STALL_SEVERITY_WEIGHT_FAULT` (constant, lines 161-161)
  - `STALL_SEVERITY_WEIGHT_RECOVERY_RETRY` (constant, lines 162-162)
  - `STALL_SEVERITY_WEIGHT_WATCHDOG` (constant, lines 163-163)
  - `STALL_SEVERITY_DECAY_ON_SUCCESS` (constant, lines 164-164)
  - `STALL_ESCALATION_MIN_LEVEL` (constant, lines 165-165)
  - `STALL_PLAN_SYNTHESIS_MAX_TOKENS` (constant, lines 166-166)
  - `STALL_ESCALATION_CONTEXT_MAX_CHARS` (constant, lines 167-167)
  - `MAX_RUN_SECONDS` (constant, lines 168-168)
  - `MIN_RUN_TIMEOUT_SECONDS` (constant, lines 169-169)
  - `MAX_RUN_TIMEOUT_SECONDS` (constant, lines 170-170)
  - `DEFAULT_REQUEST_TIMEOUT` (constant, lines 180-180)
  - `AUTO_CONTINUE_BUDGET_DEFAULT` (constant, lines 181-181)
  - `AGENT_MAX_OUTPUT_TOKENS` (constant, lines 182-182)
  - `OLLAMA_THINKING_TOOL_BUFFER` (constant, lines 183-183)
  - `WATCHDOG_INTENT_NO_TOOL_THRESHOLD` (constant, lines 184-184)
  - `WATCHDOG_REPEAT_NO_TOOL_THRESHOLD` (constant, lines 185-185)
  - `WATCHDOG_INTENT_NO_TOOL_THRESHOLD_SINGLE` (constant, lines 186-186)
  - `WATCHDOG_REPEAT_NO_TOOL_THRESHOLD_SINGLE` (constant, lines 187-187)
  - `WATCHDOG_STATE_STALL_THRESHOLD` (constant, lines 188-188)
  - `WATCHDOG_CONTEXT_STALL_THRESHOLD` (constant, lines 189-189)
  - `WATCHDOG_REPEAT_SIMILARITY_THRESHOLD` (constant, lines 190-190)
  - `WATCHDOG_CONTEXT_NEAR_RATIO` (constant, lines 191-191)
  - `WATCHDOG_MAX_DECOMPOSE_STEPS` (constant, lines 192-192)
  - `WATCHDOG_STEP_MAX_ATTEMPTS` (constant, lines 193-193)
  - `EMPTY_ACTION_MIN_CONTENT_CHARS` (constant, lines 194-194)
  - `EMPTY_ACTION_WAKEUP_RETRY_LIMIT` (constant, lines 195-195)
  - `THINKING_BUDGET_FORCE_RATIO` (constant, lines 196-196)
  - `_TOOL_TIMEOUT_MAP` (assignment, lines 198-214)
  - `_DEFAULT_TOOL_TIMEOUT` (assignment, lines 215-215)
  - `TRUNCATION_CONTINUATION_MAX_PASSES` (constant, lines 216-216)
  - `TRUNCATION_CONTINUATION_MAX_TOKENS` (constant, lines 217-217)
  - `TRUNCATION_CONTINUATION_TAIL_CHARS` (constant, lines 218-218)
  - `TRUNCATION_CONTINUATION_ECHO_CHARS` (constant, lines 219-219)
  - `TRUNCATION_OVERLAP_SCAN_CHARS` (constant, lines 220-220)
  - `TRUNCATION_PAIR_SCAN_CHARS` (constant, lines 221-221)
  - `TRUNCATION_LIVE_BUFFER_MAX_CHARS` (constant, lines 222-222)
  - `MIN_CONTEXT_TOKEN_LIMIT` (constant, lines 223-223)
  - `COMPACT_TIER1_PCT` (constant, lines 225-225)
  - `COMPACT_TIER2_PCT` (constant, lines 226-226)
  - `COMPACT_TIER3_PCT` (constant, lines 227-227)
  - `COMPACT_TIER1_ABS` (constant, lines 229-229)
  - `COMPACT_TIER2_ABS` (constant, lines 230-230)
  - `FILE_BUFFER_CONTENT_THRESHOLD` (constant, lines 232-232)
  - `FILE_BUFFER_MAX_FILES` (constant, lines 233-233)
  - `AGENT_MSG_LIMIT_TIER0` (constant, lines 235-235)
  - `AGENT_MSG_LIMIT_TIER1` (constant, lines 236-236)
  - `AGENT_MSG_LIMIT_TIER2` (constant, lines 237-237)
  - `AGENT_MSG_LIMIT_TIER3` (constant, lines 238-238)
  - `AGENT_CTX_LIMIT_TIER0` (constant, lines 239-239)
  - `AGENT_CTX_LIMIT_TIER1` (constant, lines 240-240)
  - `AGENT_CTX_LIMIT_TIER2` (constant, lines 241-241)
  - `AGENT_CTX_LIMIT_TIER3` (constant, lines 242-242)
  - `MANAGER_CTX_LIMIT_TIER0` (constant, lines 243-243)
  - `MANAGER_CTX_LIMIT_TIER1` (constant, lines 244-244)
  - `MANAGER_CTX_LIMIT_TIER2` (constant, lines 245-245)
  - `MANAGER_CTX_LIMIT_TIER3` (constant, lines 246-246)
  - `MAX_CONTEXT_ARCHIVE_SEGMENTS` (constant, lines 247-247)
  - `MODEL_OUTPUT_RETRY_TIMES` (constant, lines 248-248)
  - `ARBITER_TRIGGER_MIN_CONTENT_CHARS` (constant, lines 249-249)
  - `ARBITER_VALID_PLANNING_STREAK_LIMIT` (constant, lines 250-250)
  - `ARBITER_DEFAULT_TIMEOUT_SECONDS` (constant, lines 251-251)
  - `ARBITER_DEFAULT_MAX_TOKENS` (constant, lines 252-252)
  - `ARBITER_DEFAULT_TEMPERATURE` (constant, lines 253-253)
  - `LIVE_INPUT_DELAY_WRITE_ROUNDS` (constant, lines 254-254)
  - `LIVE_INPUT_DELAY_TOOL_ROUNDS` (constant, lines 255-255)
  - `LIVE_INPUT_DELAY_NORMAL_ROUNDS` (constant, lines 256-256)
  - `LIVE_INPUT_MAX_INJECTIONS` (constant, lines 257-257)
  - `LIVE_INPUT_REINJECT_INTERVAL` (constant, lines 258-258)
  - `LIVE_INPUT_WEIGHT_BASE_DELAYED` (constant, lines 259-259)
  - `LIVE_INPUT_WEIGHT_BASE_NORMAL` (constant, lines 260-260)
  - `LIVE_INPUT_WEIGHT_STEP_DELAYED` (constant, lines 261-261)
  - `LIVE_INPUT_WEIGHT_STEP_NORMAL` (constant, lines 262-262)
  - `FINAL_SUMMARY_MIN_CHARS` (constant, lines 277-277)
  - `FINAL_SUMMARY_STRICT_MIN_CHARS` (constant, lines 278-278)
  - `RUNTIME_CONTROL_HINT_PREFIXES` (constant, lines 279-296)
  - `RETRY_RUNTIME_HINT_PREFIXES` (constant, lines 297-311)
  - `EXECUTION_MODE_SINGLE` (constant, lines 312-312)
  - `EXECUTION_MODE_SEQUENTIAL` (constant, lines 313-313)
  - `EXECUTION_MODE_SYNC` (constant, lines 314-314)
  - `EXECUTION_MODE_CHOICES` (constant, lines 315-319)
  - `AGENT_ROLES` (constant, lines 320-320)
  - `AGENT_BUBBLE_ROLES` (constant, lines 321-321)
  - `AGENT_ROLE_LABELS` (constant, lines 322-328)
  - `AGENT_ROLE_BUBBLE_COLORS` (constant, lines 329-335)
  - `BLACKBOARD_STATUSES` (constant, lines 336-345)
  - `TASK_COMPLEXITY_LEVELS` (constant, lines 346-346)
  - `TASK_PROFILE_TYPES` (constant, lines 347-353)
  - `TASK_LEVEL_CHOICES` (constant, lines 354-354)
  - `TASK_SCALE_PREFERENCES` (constant, lines 355-355)
  - `SEMANTIC_CONFIDENCE_CHOICES` (constant, lines 356-356)
  - `TASK_LEVEL_POLICIES` (constant, lines 357-403)
  - `MANAGER_ROUTE_TARGETS` (constant, lines 404-404)
  - `BLACKBOARD_MAX_LOG_ENTRIES` (constant, lines 405-405)
  - `BLACKBOARD_MAX_TEXT` (constant, lines 406-406)
  - `SKILL_REFRESH_MIN_INTERVAL_SECONDS` (constant, lines 407-407)
  - `SKILL_PROMPT_MAX_ITEMS` (constant, lines 408-408)
  - `SKILL_PROMPT_MAX_CHARS` (constant, lines 409-409)
  - `SKILL_RUNTIME_CACHE_MAX_ENTRIES` (constant, lines 410-410)
  - `SKILL_RUNTIME_CACHE_MAX_BYTES` (constant, lines 411-411)
  - `AUTO_SKILLS_ROOT_CANDIDATES` (constant, lines 412-412)
  - `SKILL_DEFAULT_ATTACHMENT_GLOBS` (constant, lines 413-443)
  - `SKILL_INLINE_ATTACHMENT_MAX_FILES` (constant, lines 444-444)
  - `SKILL_INLINE_ATTACHMENT_MAX_CHARS` (constant, lines 445-445)
  - `SKILL_RESOURCE_MANIFEST_MAX_ITEMS` (constant, lines 446-446)
  - `SKILL_BODY_COMPACT_THRESHOLD_CHARS` (constant, lines 447-447)
  - `SKILL_BODY_PREVIEW_CHARS` (constant, lines 448-448)
  - `SKILLS_VIRTUAL_PREFIX` (constant, lines 449-449)
  - `PLAN_MODE_ENABLED_LEVELS` (constant, lines 450-450)
  - `PLAN_MODE_FORCED_LEVELS` (constant, lines 451-451)
  - `PLAN_MODE_USER_CHOICES` (constant, lines 452-452)
  - `TASK_PHASES` (constant, lines 454-454)
  - `TASK_PHASE_ROUTING` (constant, lines 455-462)
  - `COMPLEXITY_KEYWORDS` (constant, lines 464-469)
  - `PLAN_MODE_EXPLORER_MAX_ROUNDS` (constant, lines 470-470)
  - `REVIEWER_DEBUG_MODE_MAX_ROUNDS` (constant, lines 472-472)
  - `REVIEWER_DEBUG_TOOL_ALLOWLIST` (constant, lines 473-477)
  - `EXPLORER_STALL_THRESHOLD` (constant, lines 478-478)
  - `DEVELOPER_EDIT_STALL_THRESHOLD` (constant, lines 479-479)
  - `PLAN_MODE_MANAGER_SYNTHESIS_MAX_TOKENS` (constant, lines 480-480)
  - `PLAN_MODE_MAX_OPTIONS` (constant, lines 481-481)
  - `PLAN_MODE_RESEARCH_TOOL_ALLOWLIST` (constant, lines 482-486)
  - `FAILURE_LEDGER_MAX_FIXES` (constant, lines 487-487)
  - `FAILURE_LEDGER_MAX_COMPILE_ERRORS` (constant, lines 488-488)
  - `FAILURE_LEDGER_MAX_DELEGATIONS` (constant, lines 489-489)
  - `FAILURE_LEDGER_MAX_STALLS` (constant, lines 490-490)
  - `FAILURE_LEDGER_MAX_TOOL_FPS` (constant, lines 491-491)
  - `FAILURE_LEDGER_MAX_ERRORS` (constant, lines 492-492)
  - `ERROR_CATEGORY_DEFS` (constant, lines 495-532)
  - `CHECKPOINT_MAX_COUNT` (constant, lines 533-533)
  - `CHECKPOINT_INTERVAL_ROUNDS` (constant, lines 534-534)
  - `PERSISTED_ROUTES_MAX` (constant, lines 535-535)
  - `HTML_FRONTEND_REQUEST_KEYWORDS` (constant, lines 536-575)
  - `DEEP_RESEARCH_REQUEST_KEYWORDS` (constant, lines 576-598)
  - `DEEP_RESEARCH_RETRIEVAL_KEYWORDS` (constant, lines 599-618)
  - `DEEP_RESEARCH_TEXT_ONLY_HINT_KEYWORDS` (constant, lines 619-636)
  - `DANGEROUS_PATTERNS` (constant, lines 638-638)
  - `VALID_MSG_TYPES` (constant, lines 639-645)
  - `SUPPORTED_UI_LANGUAGES` (constant, lines 647-652)
  - `UI_LANGUAGE_LABELS` (constant, lines 653-653)
  - `DEFAULT_UI_LANGUAGE` (constant, lines 654-654)
  - `UI_STYLE_CHOICES` (constant, lines 655-655)
  - `UI_STYLE_LABELS` (constant, lines 656-656)
  - `DEFAULT_UI_STYLE` (constant, lines 657-657)
  - `DEFAULT_WEB_UI_DIR` (constant, lines 658-658)
  - `DEFAULT_WEB_UI_CONFIG` (constant, lines 659-659)
  - `WEB_UI_REQUIRED_FILES` (constant, lines 660-667)
  - `WEB_UI_OPTIONAL_FILES` (constant, lines 668-668)
  - `IMAGE_EXTS` (constant, lines 670-683)
  - `IMAGE_FORMATS_NEED_CONVERSION` (constant, lines 684-684)
  - `IMAGE_SAFE_FORMATS` (constant, lines 685-685)
  - `AUDIO_EXTS` (constant, lines 686-696)
  - `VIDEO_EXTS` (constant, lines 697-707)
  - `CODE_PREVIEW_STAGE_MAX_BYTES` (constant, lines 708-708)
  - `CODE_PREVIEW_STAGE_MAX_ROWS` (constant, lines 709-709)
  - `CODE_PREVIEW_STAGE_MAX_PER_FILE` (constant, lines 710-710)
  - `CODE_PREVIEW_STAGE_MAX_TOTAL` (constant, lines 711-711)
  - `RENDER_FRAME_MAX_B64_CHARS` (constant, lines 712-712)
  - `RENDER_FRAME_MAX_POINTS` (constant, lines 713-713)
  - `RENDER_FRAME_MAX_LINES` (constant, lines 714-714)
  - `RENDER_FRAME_MAX_LINE_POINTS` (constant, lines 715-715)
  - `RENDER_FRAME_ACTIVITY_INTERVAL_SECONDS` (constant, lines 716-716)
  - `RAW_TOOLCALL_TEXT_FILTER_THRESHOLD` (constant, lines 717-717)
  - `ASSISTANT_TEXT_PERSIST_MAX_CHARS` (constant, lines 718-718)
  - `ASSISTANT_MESSAGE_EVENT_MAX_CHARS` (constant, lines 719-719)
  - `CODE_PREVIEW_EXTS` (constant, lines 720-809)
  - `CODE_PREVIEW_FILENAMES` (constant, lines 810-821)
  - `MEDIA_CAPABILITY_KEYS` (constant, lines 822-829)
  - `SAMPLE_IMAGE_PNG_B64` (constant, lines 830-833)
  - `SAMPLE_AUDIO_WAV_B64` (constant, lines 834-836)
  - `SAMPLE_VIDEO_MP4_B64` (constant, lines 837-839)
  - `OFFLINE_JS_LIB_CATALOG` (constant, lines 841-977)
  - `OFFLINE_JS_LIB_INDEX_FILE` (constant, lines 978-978)
  - `OFFLINE_JS_LIB_README_FILE` (constant, lines 979-979)
  - `EMBEDDED_SKILLS_ARCHIVE_B64` (constant, lines 3775-4294)
  - `EMBEDDED_SKILLS_ARCHIVE_SHA256` (constant, lines 4295-4295)
  - `EMBEDDED_SKILLS_ARCHIVE_FILES` (constant, lines 4296-4318)
  - `BUILTIN_CLAWHUB_SKILLS_VERSION` (constant, lines 5932-5932)
  - `EMBEDDED_CLAWHUB_SKILLS_ARCHIVE_B64` (constant, lines 5934-6178)
  - `SKILL_PROTOCOL_LOCAL` (constant, lines 6232-6232)
  - `SKILL_PROTOCOL_CLAWHUB` (constant, lines 6233-6233)
  - `SKILL_PROTOCOL_HTTP_JSON` (constant, lines 6234-6234)
  - `SKILL_PROTOCOL_SPECS` (constant, lines 6236-6267)
  - `AGENT_TOOL_ALLOWLIST` (constant, lines 9191-9234)
  - `INDEX_HTML` (constant, lines 29313-29494)
  - `APP_CSS` (constant, lines 29496-29854)
  - `APP_JS` (constant, lines 29856-32649)
  - `APP_TS` (constant, lines 32651-32678)
  - `SKILLS_INDEX_HTML` (constant, lines 32680-32834)
  - `SKILLS_EXTRA_CSS` (constant, lines 32836-32931)
  - `SKILLS_APP_JS` (constant, lines 32933-33025)
  - `RAG_TERM_GROUPS` (constant, lines 33027-33037)
  - `RAG_RESEARCH_HINTS` (constant, lines 33038-33059)
  - `RAG_CODE_HINTS` (constant, lines 33060-33070)
  - `RAG_SHORT_TOKEN_ALLOWLIST` (constant, lines 33071-33086)
  - `RAG_EN_STOPWORDS` (constant, lines 33087-33159)
  - `RAG_ZH_STOPWORDS` (constant, lines 33160-33196)
  - `RAG_GENERIC_ENTITY_TERMS_EN` (constant, lines 33197-33275)
  - `RAG_GENERIC_ENTITY_TERMS_ZH` (constant, lines 33276-33318)
  - `RAG_STRUCTURAL_ENTITY_PATTERNS` (constant, lines 33319-33337)
  - `CODE_LIBRARY_IGNORED_DIRS` (constant, lines 33660-33665)
  - `CODE_LIBRARY_LANGUAGE_BY_EXT` (constant, lines 33666-33722)
  - `CODE_LIBRARY_SPECIAL_FILENAMES` (constant, lines 33723-33729)
  - `RAG_ADMIN_INDEX_HTML` (constant, lines 38336-38493)
  - `RAG_ADMIN_CSS` (constant, lines 38495-38585)
  - `RAG_ADMIN_JS` (constant, lines 38587-39813)
  - `CODE_ADMIN_INDEX_HTML` (constant, lines 39815-39824)
  - `CODE_ADMIN_CSS` (constant, lines 39825-39855)
  - `CODE_ADMIN_JS` (constant, lines 39856-39860)

### `config/paths.py`

- Routed symbols: 8
- Cross-module imports: `utils/text.py`: `trim`
- Symbols:
  - `SCRIPT_DIR` (constant, lines 50-50)
  - `_resolve_default_agent_workdir` (function, lines 52-56)
  - `_migrate_legacy_runtime_roots` (function, lines 58-86)
  - `WORKDIR` (constant, lines 88-88)
  - `CODES_ROOT` (constant, lines 89-89)
  - `LLM_CONFIG_PATH` (constant, lines 90-90)
  - `detect_repo_root` (function, lines 1557-1571)
  - `REPO_ROOT` (constant, lines 1573-1573)

### `config/settings.py`

- Routed symbols: 23
- Cross-module imports: `config/constants.py`: `AUTO_SKILLS_ROOT_CANDIDATES`, `DEFAULT_REQUEST_TIMEOUT`, `DEFAULT_UI_LANGUAGE`, `DEFAULT_UI_STYLE`, `DEFAULT_WEB_UI_CONFIG`, `DEFAULT_WEB_UI_DIR`, `EXECUTION_MODE_CHOICES`, `EXECUTION_MODE_SEQUENTIAL`, `EXECUTION_MODE_SINGLE`, `EXECUTION_MODE_SYNC`, `MEDIA_CAPABILITY_KEYS`, `SUPPORTED_UI_LANGUAGES`, `UI_LANGUAGE_LABELS`, `UI_STYLE_CHOICES`; `config/paths.py`: `WORKDIR`; `llm/utils.py`: `_is_http_url`, `_resolve_local_path`, `complete_chat_endpoint`, `extract_base_url`; `skills/store.py`: `ensure_embedded_skills`; `utils/json_utils.py`: `parse_json_object`; `utils/misc.py`: `MAX_TIMEOUT_SECONDS`, `MIN_TIMEOUT_SECONDS`, `normalize_timeout_seconds`; `utils/text.py`: `trim`
- Symbols:
  - `normalize_ui_language` (function, lines 982-1004)
  - `normalize_ui_style` (function, lines 1007-1024)
  - `supported_ui_languages_payload` (function, lines 1027-1028)
  - `normalize_execution_mode` (function, lines 1031-1050)
  - `model_language_instruction` (function, lines 1053-1081)
  - `_detect_os_shell_instruction` (function, lines 1084-1122)
  - `resolve_web_ui_dir_path` (function, lines 1124-1131)
  - `resolve_optional_file_path` (function, lines 1134-1141)
  - `resolve_skills_root_path` (function, lines 1144-1151)
  - `_count_skill_markdown_files` (function, lines 1154-1165)
  - `select_preferred_skills_root` (function, lines 1168-1202)
  - `load_web_ui_config_file` (function, lines 1205-1219)
  - `extract_show_upload_list_setting` (function, lines 1222-1236)
  - `extract_ui_style_setting` (function, lines 1239-1253)
  - `default_multimodal_capabilities` (function, lines 1256-1264)
  - `_to_bool_like` (function, lines 1267-1277)
  - `infer_model_multimodal_capabilities` (function, lines 1280-1317)
  - `parse_capability_overrides` (function, lines 1320-1357)
  - `merge_multimodal_capabilities` (function, lines 1360-1367)
  - `parse_media_endpoints` (function, lines 1370-1384)
  - `load_llm_config_from_source` (function, lines 2425-2459)
  - `parse_llm_config_profiles` (function, lines 2461-2670)
  - `looks_like_llm_config` (function, lines 2672-2718)

### `llm/client.py`

- Routed symbols: 2
- Cross-module imports: `config/constants.py`: `DEFAULT_REQUEST_TIMEOUT`, `OLLAMA_THINKING_TOOL_BUFFER`, `SAMPLE_AUDIO_WAV_B64`, `SAMPLE_IMAGE_PNG_B64`, `SAMPLE_VIDEO_MP4_B64`; `config/settings.py`: `default_multimodal_capabilities`, `infer_model_multimodal_capabilities`, `merge_multimodal_capabilities`, `parse_capability_overrides`, `parse_media_endpoints`; `llm/utils.py`: `complete_chat_endpoint`, `split_thinking_content`; `utils/json_utils.py`: `canonicalize_tool_name`, `json_dumps`, `parse_json_object`, `parse_tool_arguments`, `parse_tool_arguments_with_error`; `utils/misc.py`: `MAX_TIMEOUT_SECONDS`, `MIN_TIMEOUT_SECONDS`, `make_id`, `normalize_timeout_seconds`, `now_ts`; `utils/text.py`: `trim`
- Symbols:
  - `OllamaError` (class, lines 8015-8018)
  - `OllamaClient` (class, lines 8020-8958)

### `llm/utils.py`

- Routed symbols: 19
- Cross-module imports: `utils/json_utils.py`: `json_dumps`, `parse_json_object`; `utils/text.py`: `trim`
- Symbols:
  - `probe_ollama_environment` (function, lines 2086-2099)
  - `list_ollama_models` (function, lines 2101-2103)
  - `_OLLAMA_TAG_CACHE_LOCK` (assignment, lines 2105-2105)
  - `_OLLAMA_TAG_CACHE` (assignment, lines 2106-2106)
  - `list_ollama_models_cached` (function, lines 2116-2153)
  - `resolve_ollama_model` (function, lines 2155-2165)
  - `infer_thinking_model` (function, lines 2167-2169)
  - `split_thinking_content` (function, lines 2171-2212)
  - `strip_thinking_content` (function, lines 2214-2215)
  - `check_ollama_model_ready` (function, lines 2217-2241)
  - `list_loaded_ollama_models` (function, lines 2243-2256)
  - `wake_ollama_model` (function, lines 2258-2288)
  - `try_pull_ollama_model` (function, lines 2290-2308)
  - `ordered_model_candidates` (function, lines 2310-2328)
  - `pick_working_ollama_model` (function, lines 2330-2346)
  - `extract_base_url` (function, lines 2379-2387)
  - `complete_chat_endpoint` (function, lines 2389-2398)
  - `_is_http_url` (function, lines 2400-2405)
  - `_resolve_local_path` (function, lines 2407-2423)

### `rag/index.py`

- Routed symbols: 5
- Cross-module imports: `config/constants.py`: `RAG_DYNAMIC_NOISE_HARD_COMMUNITY_RATIO`, `RAG_DYNAMIC_NOISE_HARD_DOC_RATIO`, `RAG_DYNAMIC_NOISE_MIN_COMMUNITY_FREQ`, `RAG_DYNAMIC_NOISE_MIN_DOC_FREQ`, `RAG_DYNAMIC_NOISE_SOFT_COMMUNITY_RATIO`, `RAG_DYNAMIC_NOISE_SOFT_DOC_RATIO`, `RAG_EN_STOPWORDS`, `RAG_GRAPH_MAX_NODES`, `RAG_INCLUDE_FILENAME_ENTITIES_DEFAULT`, `RAG_MAX_COMMUNITY_MAP_SUPPORT`, `RAG_MAX_GLOBAL_COMMUNITIES`, `RAG_MAX_QUERY_RESULTS`; `rag/parsers.py`: `_code_is_test_path`, `_rag_apply_filename_entity_policy`, `_rag_choose_community`, `_rag_classify_document`, `_rag_expand_tokens`, `_rag_extract_entities`, `_rag_filter_entities`, `_rag_tokenize`; `utils/json_utils.py`: `json_dumps`; `utils/misc.py`: `now_ts`; `utils/text.py`: `trim`
- Symbols:
  - `_code_module_name` (function, lines 33756-33770)
  - `_code_choose_community` (function, lines 33773-33780)
  - `_code_query_terms` (function, lines 33783-33795)
  - `TFGraphIDFIndex` (class, lines 34771-36129)
  - `CodeGraphIndex` (class, lines 37569-37981)

### `rag/ingestion.py`

- Routed symbols: 3
- Cross-module imports: `config/constants.py`: `CODE_IMPORT_WORKER_COUNT`, `CODE_LIBRARY_IGNORED_DIRS`, `CODE_PARSE_TIMEOUT_SECONDS`, `RAG_IMPORT_WORKER_COUNT`, `RAG_MAX_IMPORT_BATCH_ITEMS`, `RAG_MAX_IMPORT_FILES`, `RAG_MODEL_MEDIA_MAX_BYTES`, `RAG_PARSE_TIMEOUT_SECONDS`, `RAG_PDF_IMAGE_LIMIT`; `config/settings.py`: `default_multimodal_capabilities`; `rag/parsers.py`: `CodeContentParser`, `RAGContentParser`, `_rag_extract_entities`, `_rag_safe_name`; `rag/store.py`: `CodeLibraryStore`, `RAGLibraryStore`; `session/state.py`: `SessionState`; `utils/files.py`: `try_read_text`; `utils/json_utils.py`: `_read_json_file`, `_write_json_file`, `parse_json_object`; `utils/media.py`: `guess_mime_from_name`; `utils/misc.py`: `make_id`, `now_ts`; `utils/text.py`: `trim`
- Symbols:
  - `_rag_parse_file_worker` (function, lines 36682-36696)
  - `RAGIngestionService` (class, lines 36699-37566)
  - `CodeIngestionService` (class, lines 38250-38334)

### `rag/parsers.py`

- Routed symbols: 22
- Cross-module imports: `config/constants.py`: `AUDIO_EXTS`, `CODE_CHUNK_CHARS`, `CODE_CHUNK_OVERLAP`, `CODE_LIBRARY_LANGUAGE_BY_EXT`, `CODE_LIBRARY_SPECIAL_FILENAMES`, `CODE_MAX_CHUNKS_PER_DOC`, `CODE_PREVIEW_EXTS`, `CODE_PREVIEW_FILENAMES`, `CODE_PREVIEW_STAGE_MAX_ROWS`, `IMAGE_EXTS`, `RAG_CHUNK_CHARS`, `RAG_CHUNK_OVERLAP`, `RAG_CODE_HINTS`, `RAG_EN_STOPWORDS`, `RAG_GENERIC_ENTITY_TERMS_EN`, `RAG_GENERIC_ENTITY_TERMS_ZH`, `RAG_INCLUDE_FILENAME_ENTITIES_DEFAULT`, `RAG_MAX_CHUNKS_PER_DOC`, `RAG_PDF_IMAGE_LIMIT`, `RAG_RESEARCH_HINTS`, `RAG_SHORT_TOKEN_ALLOWLIST`, `RAG_STRUCTURAL_ENTITY_PATTERNS`, `RAG_TERM_GROUPS`, `RAG_ZH_STOPWORDS`, `VIDEO_EXTS`; `utils/files.py`: `_sha256_bytes`, `_sha256_file`; `utils/json_utils.py`: `parse_json_object`; `utils/media.py`: `guess_mime_from_name`; `utils/text.py`: `_compress_rows_keep_hotspot`, `_skip_row`, `trim`
- Symbols:
  - `normalize_rel_preview_path` (function, lines 3324-3335)
  - `is_code_preview_candidate` (function, lines 3338-3346)
  - `preview_kind_for_path` (function, lines 3349-3359)
  - `build_code_preview_rows` (function, lines 3362-3546)
  - `_rag_safe_name` (function, lines 33340-33343)
  - `_rag_detect_language` (function, lines 33346-33360)
  - `_rag_cjk_ngrams` (function, lines 33363-33375)
  - `_rag_is_noise_token` (function, lines 33378-33397)
  - `_rag_entity_allowed` (function, lines 33400-33412)
  - `_rag_filter_entities` (function, lines 33415-33429)
  - `_rag_filename_entity_aliases` (function, lines 33432-33465)
  - `_rag_apply_filename_entity_policy` (function, lines 33468-33498)
  - `_rag_choose_community` (function, lines 33501-33518)
  - `_rag_tokenize` (function, lines 33521-33551)
  - `_rag_expand_tokens` (function, lines 33554-33568)
  - `_rag_extract_entities` (function, lines 33571-33587)
  - `_rag_classify_document` (function, lines 33590-33624)
  - `_rag_chunk_text` (function, lines 33627-33657)
  - `_code_language_from_name` (function, lines 33732-33748)
  - `_code_is_test_path` (function, lines 33751-33753)
  - `CodeContentParser` (class, lines 33798-34258)
  - `RAGContentParser` (class, lines 34261-34768)

### `rag/store.py`

- Routed symbols: 2
- Cross-module imports: `config/constants.py`: `CODE_CHUNK_CHARS`, `CODE_CHUNK_OVERLAP`, `CODE_MAX_CHUNKS_PER_DOC`, `RAG_INCLUDE_FILENAME_ENTITIES_DEFAULT`, `RAG_TASK_HISTORY_LIMIT`; `rag/index.py`: `CodeGraphIndex`, `TFGraphIDFIndex`, `_code_choose_community`, `_code_module_name`; `rag/parsers.py`: `_code_is_test_path`, `_rag_apply_filename_entity_policy`, `_rag_choose_community`, `_rag_chunk_text`, `_rag_entity_allowed`, `_rag_extract_entities`, `_rag_safe_name`; `utils/files.py`: `_sha256_bytes`, `_sha256_file`; `utils/json_utils.py`: `_read_json_file`, `_write_json_file`; `utils/media.py`: `guess_mime_from_name`; `utils/misc.py`: `make_id`, `now_ts`; `utils/text.py`: `trim`
- Symbols:
  - `RAGLibraryStore` (class, lines 36132-36679)
  - `CodeLibraryStore` (class, lines 37984-38247)

### `server/handlers.py`

- Routed symbols: 5
- Cross-module imports: `app/context.py`: `AppContext`; `config/constants.py`: `APP_VERSION`, `DEFAULT_REQUEST_TIMEOUT`, `DEFAULT_UI_LANGUAGE`, `DEFAULT_UI_STYLE`, `EXECUTION_MODE_CHOICES`, `EXECUTION_MODE_SYNC`, `MIN_RUN_TIMEOUT_SECONDS`, `PLAN_MODE_USER_CHOICES`, `RAG_GRAPH_MAX_NODES`, `SSE_HEARTBEAT_SECONDS`, `TASK_LEVEL_CHOICES`, `TASK_LEVEL_POLICIES`, `UI_STYLE_LABELS`; `config/paths.py`: `LLM_CONFIG_PATH`, `REPO_ROOT`, `WORKDIR`; `config/settings.py`: `_to_bool_like`, `looks_like_llm_config`, `normalize_execution_mode`, `normalize_ui_language`, `normalize_ui_style`, `resolve_web_ui_dir_path`, `supported_ui_languages_payload`; `llm/utils.py`: `list_ollama_models`; `session/manager.py`: `SessionManager`; `session/state.py`: `SessionState`; `skills/store.py`: `analyze_skill_building_knowledge`; `utils/files.py`: `safe_path`, `try_read_text`; `utils/json_utils.py`: `json_dumps`, `parse_json_object`; `utils/media.py`: `guess_mime_from_name`; `utils/misc.py`: `now_ts`, `swallow_benign_socket_error`, `user_id_from_ip`
- Symbols:
  - `AgentHTTPServer` (class, lines 42190-42218)
  - `Handler` (class, lines 42220-42869)
  - `SkillsHandler` (class, lines 42871-43064)
  - `RagAdminHandler` (class, lines 43066-43220)
  - `CodeAdminHandler` (class, lines 43223-43377)

### `session/manager.py`

- Routed symbols: 1
- Cross-module imports: `config/constants.py`: `AGENT_MAX_OUTPUT_TOKENS`, `ARBITER_DEFAULT_MAX_TOKENS`, `ARBITER_DEFAULT_TEMPERATURE`, `ARBITER_DEFAULT_TIMEOUT_SECONDS`, `DEFAULT_REQUEST_TIMEOUT`, `DEFAULT_UI_LANGUAGE`, `EXECUTION_MODE_SYNC`, `MAX_AGENT_ROUNDS`, `MAX_AGENT_ROUNDS_CAP`, `MAX_RUN_SECONDS`, `MAX_RUN_TIMEOUT_SECONDS`, `MIN_AGENT_ROUNDS`, `MIN_CONTEXT_TOKEN_LIMIT`, `MIN_RUN_TIMEOUT_SECONDS`, `TOKEN_THRESHOLD`; `config/paths.py`: `LLM_CONFIG_PATH`; `config/settings.py`: `infer_model_multimodal_capabilities`, `merge_multimodal_capabilities`, `normalize_execution_mode`, `normalize_ui_language`, `parse_capability_overrides`, `parse_llm_config_profiles`; `llm/client.py`: `OllamaClient`; `llm/utils.py`: `complete_chat_endpoint`, `extract_base_url`, `list_ollama_models_cached`, `probe_ollama_environment`; `session/state.py`: `SessionState`; `utils/crypto.py`: `CryptoBox`; `utils/files.py`: `try_read_text`; `utils/json_utils.py`: `parse_json_object`; `utils/misc.py`: `make_id`, `normalize_timeout_seconds`, `now_ts`, `sanitize_profile_id`
- Symbols:
  - `SessionManager` (class, lines 28464-29311)

### `session/state.py`

- Routed symbols: 1
- Cross-module imports: `agent/background.py`: `BackgroundManager`; `agent/bus.py`: `MessageBus`; `agent/events.py`: `EventHub`; `agent/tasks.py`: `TaskManager`; `agent/todo.py`: `TodoManager`; `agent/worktree.py`: `WorktreeManager`; `config/constants.py`: `AGENT_BUBBLE_ROLES`, `AGENT_CTX_LIMIT_TIER0`, `AGENT_CTX_LIMIT_TIER1`, `AGENT_CTX_LIMIT_TIER2`, `AGENT_CTX_LIMIT_TIER3`, `AGENT_MAX_OUTPUT_TOKENS`, `AGENT_MSG_LIMIT_TIER0`, `AGENT_MSG_LIMIT_TIER1`, `AGENT_MSG_LIMIT_TIER2`, `AGENT_MSG_LIMIT_TIER3`, `AGENT_ROLES`, `AGENT_ROLE_LABELS`, `AGENT_TOOL_ALLOWLIST`, `ARBITER_DEFAULT_MAX_TOKENS`, `ARBITER_DEFAULT_TEMPERATURE`, `ARBITER_DEFAULT_TIMEOUT_SECONDS`, `ARBITER_TRIGGER_MIN_CONTENT_CHARS`, `ARBITER_VALID_PLANNING_STREAK_LIMIT`, `ASSISTANT_MESSAGE_EVENT_MAX_CHARS`, `ASSISTANT_TEXT_PERSIST_MAX_CHARS`, `AUDIO_EXTS`, `AUTO_CONTINUE_BUDGET_DEFAULT`, `BASH_READ_LOOP_THRESHOLD`, `BLACKBOARD_MAX_LOG_ENTRIES`, `BLACKBOARD_MAX_TEXT`, `BLACKBOARD_STATUSES`, `CHECKPOINT_INTERVAL_ROUNDS`, `CHECKPOINT_MAX_COUNT`, `CODE_PREVIEW_STAGE_MAX_BYTES`, `CODE_PREVIEW_STAGE_MAX_PER_FILE`, `CODE_PREVIEW_STAGE_MAX_ROWS`, `CODE_PREVIEW_STAGE_MAX_TOTAL`, `COMPACT_TIER1_ABS`, `COMPACT_TIER1_PCT`, `COMPACT_TIER2_ABS`, `COMPACT_TIER2_PCT`, `COMPACT_TIER3_PCT`, `COMPLEXITY_KEYWORDS`, `DANGEROUS_PATTERNS`, `DEEP_RESEARCH_REQUEST_KEYWORDS`, `DEEP_RESEARCH_RETRIEVAL_KEYWORDS`, `DEEP_RESEARCH_TEXT_ONLY_HINT_KEYWORDS`, `DEFAULT_REQUEST_TIMEOUT`, `DEFAULT_UI_LANGUAGE`, `DEVELOPER_EDIT_STALL_THRESHOLD`, `EMPTY_ACTION_MIN_CONTENT_CHARS`, `EMPTY_ACTION_WAKEUP_RETRY_LIMIT`, `ERROR_CATEGORY_DEFS`, `EXECUTION_MODE_CHOICES`, `EXECUTION_MODE_SEQUENTIAL`, `EXECUTION_MODE_SINGLE`, `EXECUTION_MODE_SYNC`, `EXPLORER_STALL_THRESHOLD`, `FAILURE_LEDGER_MAX_COMPILE_ERRORS`, `FAILURE_LEDGER_MAX_DELEGATIONS`, `FAILURE_LEDGER_MAX_ERRORS`, `FAILURE_LEDGER_MAX_FIXES`, `FAILURE_LEDGER_MAX_STALLS`, `FAILURE_LEDGER_MAX_TOOL_FPS`, `FILE_BUFFER_CONTENT_THRESHOLD`, `FILE_BUFFER_MAX_FILES`, `FINAL_SUMMARY_MIN_CHARS`, `FINAL_SUMMARY_STRICT_MIN_CHARS`, `FUSED_FAULT_BREAK_THRESHOLD`, `HARD_BREAK_RECOVERY_ROUND_THRESHOLD`, `HARD_BREAK_TOOL_ERROR_THRESHOLD`, `HTML_FRONTEND_REQUEST_KEYWORDS`, `IMAGE_EXTS`, `IMAGE_FORMATS_NEED_CONVERSION`, `LIVE_INPUT_DELAY_NORMAL_ROUNDS`, `LIVE_INPUT_DELAY_TOOL_ROUNDS`, `LIVE_INPUT_DELAY_WRITE_ROUNDS`, `LIVE_INPUT_MAX_INJECTIONS`, `LIVE_INPUT_REINJECT_INTERVAL`, `LIVE_INPUT_WEIGHT_BASE_DELAYED`, `LIVE_INPUT_WEIGHT_BASE_NORMAL`, `LIVE_INPUT_WEIGHT_STEP_DELAYED`, `LIVE_INPUT_WEIGHT_STEP_NORMAL`, `LONG_OUTPUT_LISTING_OFFLOAD_CHARS`, `LONG_OUTPUT_MODEL_PAGE_CHARS`, `LONG_OUTPUT_READ_PAGE_LINES`, `LONG_OUTPUT_READ_PAGE_MAX_CHARS`, `LONG_OUTPUT_TEMP_MAX_FILES`, `LONG_OUTPUT_UI_PAGE_CHARS`, `LONG_OUTPUT_UI_PREVIEW_MAX_PAGES`, `MANAGER_CTX_LIMIT_TIER0`, `MANAGER_CTX_LIMIT_TIER1`, `MANAGER_CTX_LIMIT_TIER2`, `MANAGER_CTX_LIMIT_TIER3`, `MANAGER_ROUTE_TARGETS`, `MAX_AGENT_ROUNDS`, `MAX_AGENT_ROUNDS_CAP`, `MAX_CONTEXT_ARCHIVE_SEGMENTS`, `MAX_RUN_SECONDS`, `MAX_RUN_TIMEOUT_SECONDS`, `MIN_AGENT_ROUNDS`, `MIN_CONTEXT_TOKEN_LIMIT`, `MIN_RUN_TIMEOUT_SECONDS`, `MODEL_CALL_PROGRESS_DELAY`, `MODEL_CALL_PROGRESS_INTERVAL`, `MODEL_OUTPUT_RETRY_TIMES`, `PERSISTED_ROUTES_MAX`, `PLAN_MODE_ENABLED_LEVELS`, `PLAN_MODE_EXPLORER_MAX_ROUNDS`, `PLAN_MODE_FORCED_LEVELS`, `PLAN_MODE_MANAGER_SYNTHESIS_MAX_TOKENS`, `PLAN_MODE_MAX_OPTIONS`, `PLAN_MODE_RESEARCH_TOOL_ALLOWLIST`, `PLAN_MODE_USER_CHOICES`, `RAW_TOOLCALL_TEXT_FILTER_THRESHOLD`, `RENDER_FRAME_ACTIVITY_INTERVAL_SECONDS`, `RENDER_FRAME_MAX_B64_CHARS`, `RENDER_FRAME_MAX_LINES`, `RENDER_FRAME_MAX_LINE_POINTS`, `RENDER_FRAME_MAX_POINTS`, `REPEATED_TOOL_LOOP_THRESHOLD`, `RETRY_RUNTIME_HINT_PREFIXES`, `REVIEWER_DEBUG_MODE_MAX_ROUNDS`, `RUNTIME_CONTROL_HINT_PREFIXES`, `SEMANTIC_CONFIDENCE_CHOICES`, `SKILLS_VIRTUAL_PREFIX`, `SKILL_REFRESH_MIN_INTERVAL_SECONDS`, `SKILL_RUNTIME_CACHE_MAX_BYTES`, `SKILL_RUNTIME_CACHE_MAX_ENTRIES`, `STALL_ESCALATION_CONTEXT_MAX_CHARS`, `STALL_ESCALATION_MIN_LEVEL`, `STALL_PLAN_SYNTHESIS_MAX_TOKENS`, `STALL_SEVERITY_DECAY_ON_SUCCESS`, `STALL_SEVERITY_ESCALATION_THRESHOLD`, `STALL_SEVERITY_WEIGHT_BASH_READ_LOOP`, `STALL_SEVERITY_WEIGHT_FAULT`, `STALL_SEVERITY_WEIGHT_RECOVERY_RETRY`, `STALL_SEVERITY_WEIGHT_REPEATED_TOOL`, `STALL_SEVERITY_WEIGHT_WATCHDOG`, `TASK_COMPLEXITY_LEVELS`, `TASK_LEVEL_CHOICES`, `TASK_LEVEL_POLICIES`, `TASK_PHASE_ROUTING`, `TASK_PROFILE_TYPES`, `TASK_SCALE_PREFERENCES`, `THINKING_BUDGET_FORCE_RATIO`, `TOKEN_THRESHOLD`, `TRUNCATION_CONTINUATION_ECHO_CHARS`, `TRUNCATION_CONTINUATION_MAX_PASSES`, `TRUNCATION_CONTINUATION_MAX_TOKENS`, `TRUNCATION_CONTINUATION_TAIL_CHARS`, `TRUNCATION_LIVE_BUFFER_MAX_CHARS`, `TRUNCATION_OVERLAP_SCAN_CHARS`, `TRUNCATION_PAIR_SCAN_CHARS`, `VIDEO_EXTS`, `WATCHDOG_CONTEXT_NEAR_RATIO`, `WATCHDOG_CONTEXT_STALL_THRESHOLD`, `WATCHDOG_INTENT_NO_TOOL_THRESHOLD`, `WATCHDOG_INTENT_NO_TOOL_THRESHOLD_SINGLE`, `WATCHDOG_MAX_DECOMPOSE_STEPS`, `WATCHDOG_REPEAT_NO_TOOL_THRESHOLD`, `WATCHDOG_REPEAT_NO_TOOL_THRESHOLD_SINGLE`, `WATCHDOG_REPEAT_SIMILARITY_THRESHOLD`, `WATCHDOG_STATE_STALL_THRESHOLD`, `WATCHDOG_STEP_MAX_ATTEMPTS`, `_DEFAULT_TOOL_TIMEOUT`, `_TOOL_TIMEOUT_MAP`; `config/paths.py`: `WORKDIR`; `config/settings.py`: `_detect_os_shell_instruction`, `_to_bool_like`, `default_multimodal_capabilities`, `infer_model_multimodal_capabilities`, `looks_like_llm_config`, `merge_multimodal_capabilities`, `model_language_instruction`, `normalize_execution_mode`, `normalize_ui_language`, `parse_capability_overrides`, `parse_llm_config_profiles`; `llm/client.py`: `OllamaClient`, `OllamaError`; `llm/utils.py`: `complete_chat_endpoint`, `list_loaded_ollama_models`, `list_ollama_models`, `list_ollama_models_cached`, `probe_ollama_environment`, `resolve_ollama_model`, `split_thinking_content`, `strip_thinking_content`, `wake_ollama_model`; `rag/parsers.py`: `build_code_preview_rows`, `is_code_preview_candidate`, `normalize_rel_preview_path`, `preview_kind_for_path`; `skills/store.py`: `SkillStore`, `ensure_runtime_skills`; `utils/compress.py`: `compress_text_blob`, `decompress_text_blob`; `utils/crypto.py`: `CryptoBox`; `utils/errors.py`: `CircuitBreakerTriggered`, `EmptyActionError`; `utils/files.py`: `_normalize_external_js_url`, `_safe_js_filename`, `cache_external_js_url`, `ensure_offline_js_libs`, `is_external_js_src`, `load_offline_js_lib_index`, `match_offline_js_catalog_by_url`, `offline_js_lib_root`, `safe_path`, `try_read_text`; `utils/json_utils.py`: `TOOLS`, `TOOL_REQUIRED_ARGS`, `canonicalize_tool_name`, `extract_json_object_from_text`, `json_dumps`, `parse_json_object`, `repair_truncated_json_object`, `tool_def`; `utils/media.py`: `_convert_image_to_safe_format`, `guess_ext_from_mime`, `guess_mime_from_name`; `utils/misc.py`: `MAX_TIMEOUT_SECONDS`, `MIN_TIMEOUT_SECONDS`, `is_benign_socket_error`, `make_id`, `normalize_timeout_seconds`, `now_ts`, `sanitize_profile_id`; `utils/text.py`: `MAX_TOOL_OUTPUT`, `_fmt_export_ts`, `_html_esc`, `_text_to_minimal_pdf`, `filter_runtime_noise_lines`, `make_numbered_diff`, `make_unified_diff`, `normalize_work_text`, `parse_front_matter`, `render_numbered_diff_text`, `trim`
- Symbols:
  - `SessionState` (class, lines 9236-28462)

### `skills/store.py`

- Routed symbols: 21
- Cross-module imports: `config/constants.py`: `BUILTIN_CLAWHUB_SKILLS_VERSION`, `EMBEDDED_CLAWHUB_SKILLS_ARCHIVE_B64`, `EMBEDDED_SKILLS_ARCHIVE_B64`, `EMBEDDED_SKILLS_ARCHIVE_FILES`, `EMBEDDED_SKILLS_ARCHIVE_SHA256`, `SKILLS_VIRTUAL_PREFIX`, `SKILL_BODY_COMPACT_THRESHOLD_CHARS`, `SKILL_BODY_PREVIEW_CHARS`, `SKILL_DEFAULT_ATTACHMENT_GLOBS`, `SKILL_INLINE_ATTACHMENT_MAX_CHARS`, `SKILL_INLINE_ATTACHMENT_MAX_FILES`, `SKILL_PROMPT_MAX_CHARS`, `SKILL_PROMPT_MAX_ITEMS`, `SKILL_PROTOCOL_CLAWHUB`, `SKILL_PROTOCOL_HTTP_JSON`, `SKILL_PROTOCOL_LOCAL`, `SKILL_PROTOCOL_SPECS`, `SKILL_REFRESH_MIN_INTERVAL_SECONDS`, `SKILL_RESOURCE_MANIFEST_MAX_ITEMS`; `config/paths.py`: `WORKDIR`; `llm/utils.py`: `_is_http_url`; `utils/files.py`: `_render_offline_js_catalog_md`, `try_read_text`; `utils/json_utils.py`: `json_dumps`, `parse_json_object`; `utils/misc.py`: `_meta_string_list`, `_module_exists`, `now_ts`; `utils/text.py`: `parse_front_matter`, `trim`
- Symbols:
  - `ensure_embedded_skills_at_root` (function, lines 4321-4373)
  - `ensure_embedded_skills` (function, lines 4376-4377)
  - `detect_upload_parser_capabilities` (function, lines 4385-4400)
  - `_render_cap_markdown` (function, lines 4402-4416)
  - `_write_text_if_changed` (function, lines 4418-4423)
  - `ensure_generated_document_skills` (function, lines 4425-4482)
  - `ensure_generated_image_coding_feedback_skill` (function, lines 4484-4583)
  - `_skill_knowledge_files` (function, lines 4585-4604)
  - `analyze_skill_building_knowledge` (function, lines 4606-4660)
  - `_sanitize_skill_slug` (function, lines 4662-4664)
  - `_build_skills_gen_skill_content` (function, lines 4666-4697)
  - `ensure_generated_skills_gen_skill` (function, lines 4699-4703)
  - `ensure_generated_execution_recovery_skill` (function, lines 4705-4783)
  - `ensure_generated_html_frontend_report_skills` (function, lines 4785-4990)
  - `ensure_generated_deep_research_skills` (function, lines 4992-5260)
  - `ensure_generated_research_scientific_skills` (function, lines 5262-5898)
  - `ensure_generated_runtime_skills_manifest` (function, lines 5900-5930)
  - `ensure_embedded_clawhub_skills` (function, lines 6181-6218)
  - `ensure_runtime_skills` (function, lines 6220-6230)
  - `_BUILTIN_SKILLS` (assignment, lines 6272-6358)
  - `SkillStore` (class, lines 6360-7534)

### `utils/compress.py`

- Routed symbols: 2
- Cross-module imports: none
- Symbols:
  - `compress_text_blob` (function, lines 1944-1949)
  - `decompress_text_blob` (function, lines 1951-1959)

### `utils/crypto.py`

- Routed symbols: 1
- Cross-module imports: `utils/json_utils.py`: `json_dumps`
- Symbols:
  - `CryptoBox` (class, lines 2728-2845)

### `utils/errors.py`

- Routed symbols: 2
- Cross-module imports: none
- Symbols:
  - `EmptyActionError` (class, lines 2109-2110)
  - `CircuitBreakerTriggered` (class, lines 2113-2114)

### `utils/files.py`

- Routed symbols: 14
- Cross-module imports: `config/constants.py`: `OFFLINE_JS_LIB_CATALOG`, `OFFLINE_JS_LIB_INDEX_FILE`, `OFFLINE_JS_LIB_README_FILE`; `config/paths.py`: `WORKDIR`; `utils/json_utils.py`: `json_dumps`; `utils/misc.py`: `now_ts`; `utils/text.py`: `trim`
- Symbols:
  - `safe_path` (function, lines 1575-1584)
  - `_safe_js_filename` (function, lines 1586-1593)
  - `_sha256_bytes` (function, lines 1595-1596)
  - `_sha256_file` (function, lines 1598-1606)
  - `_download_http_bytes` (function, lines 1608-1616)
  - `offline_js_lib_root` (function, lines 1618-1619)
  - `_render_offline_js_catalog_md` (function, lines 1621-1635)
  - `load_offline_js_lib_index` (function, lines 1637-1646)
  - `ensure_offline_js_libs` (function, lines 1648-1712)
  - `_normalize_external_js_url` (function, lines 1714-1718)
  - `is_external_js_src` (function, lines 1720-1722)
  - `match_offline_js_catalog_by_url` (function, lines 1724-1740)
  - `cache_external_js_url` (function, lines 1742-1774)
  - `try_read_text` (function, lines 3050-3058)

### `utils/json_utils.py`

- Routed symbols: 16
- Cross-module imports: `utils/text.py`: `trim`
- Symbols:
  - `JSON_FSYNC_ENABLED` (constant, lines 99-99)
  - `json_dumps` (function, lines 1547-1548)
  - `parse_tool_arguments` (function, lines 1988-1997)
  - `repair_truncated_json_object` (function, lines 1999-2052)
  - `parse_tool_arguments_with_error` (function, lines 2054-2084)
  - `parse_json_object` (function, lines 2348-2353)
  - `extract_json_object_from_text` (function, lines 2355-2377)
  - `_json_default_copy` (function, lines 3060-3065)
  - `_read_json_file` (function, lines 3067-3087)
  - `_write_json_file` (function, lines 3089-3116)
  - `tool_def` (function, lines 8960-8972)
  - `TOOLS` (constant, lines 8974-9145)
  - `TOOL_REQUIRED_ARGS` (constant, lines 9147-9147)
  - `TOOL_SPEC_BY_NAME` (constant, lines 9148-9148)
  - `TOOL_NAME_FUZZY_MAP` (constant, lines 9160-9160)
  - `canonicalize_tool_name` (function, lines 9178-9189)

### `utils/media.py`

- Routed symbols: 3
- Cross-module imports: none
- Symbols:
  - `guess_mime_from_name` (function, lines 1387-1389)
  - `_convert_image_to_safe_format` (function, lines 1392-1409)
  - `guess_ext_from_mime` (function, lines 1412-1418)

### `utils/misc.py`

- Routed symbols: 19
- Cross-module imports: none
- Symbols:
  - `MIN_TIMEOUT_SECONDS` (constant, lines 171-171)
  - `MAX_TIMEOUT_SECONDS` (constant, lines 172-172)
  - `DEFAULT_TIMEOUT_SECONDS` (constant, lines 173-179)
  - `BENIGN_SOCKET_DEBUG_LOG_ENABLED` (constant, lines 269-275)
  - `BENIGN_SOCKET_LOG_INTERVAL_SECONDS` (constant, lines 276-276)
  - `now_ts` (function, lines 1420-1421)
  - `_benign_socket_log_lock` (assignment, lines 1424-1424)
  - `_benign_socket_log_state` (assignment, lines 1425-1425)
  - `is_benign_socket_error` (function, lines 1443-1461)
  - `_socket_error_code` (function, lines 1464-1473)
  - `_log_benign_socket_error_limited` (function, lines 1476-1510)
  - `swallow_benign_socket_error` (function, lines 1513-1517)
  - `normalize_timeout_seconds` (function, lines 1520-1533)
  - `detect_local_lan_ip` (function, lines 1535-1545)
  - `make_id` (function, lines 1550-1551)
  - `sanitize_profile_id` (function, lines 1553-1555)
  - `user_id_from_ip` (function, lines 2720-2726)
  - `_meta_string_list` (function, lines 3037-3048)
  - `_module_exists` (function, lines 4379-4383)

### `utils/text.py`

- Routed symbols: 16
- Cross-module imports: none
- Symbols:
  - `MAX_TOOL_OUTPUT` (constant, lines 91-91)
  - `SOCKET_NOISE_LINE_PATTERNS` (constant, lines 263-268)
  - `filter_runtime_noise_lines` (function, lines 1428-1440)
  - `trim` (function, lines 1776-1778)
  - `_fmt_export_ts` (function, lines 1781-1789)
  - `_html_esc` (function, lines 1792-1793)
  - `_text_to_minimal_pdf` (function, lines 1796-1942)
  - `normalize_work_text` (function, lines 1961-1986)
  - `parse_front_matter` (function, lines 2847-3034)
  - `make_unified_diff` (function, lines 3118-3135)
  - `_skip_row` (function, lines 3137-3141)
  - `_row_is_hot` (function, lines 3144-3145)
  - `_hotspot_index` (function, lines 3148-3169)
  - `_compress_rows_keep_hotspot` (function, lines 3172-3219)
  - `make_numbered_diff` (function, lines 3222-3307)
  - `render_numbered_diff_text` (function, lines 3309-3321)
