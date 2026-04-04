# Code_Structure Framework

## Overview

- Source file: `/Users/macbookair/Downloads/Split Coder/Clouds_Coder.py`
- Output directory: `/Users/macbookair/Downloads/Split Coder/Code_Structure`
- Generated modules: 30
- Top-level symbols: 531
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
│   ├── http.py
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
| `config/constants.py` | 294 | `utils/json_utils.py`, `utils/misc.py` |
| `config/paths.py` | 8 | `utils/text.py` |
| `config/settings.py` | 33 | `config/constants.py`, `config/paths.py`, `llm/utils.py`, `skills/store.py`, `utils/http.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` |
| `llm/client.py` | 2 | `config/constants.py`, `config/settings.py`, `llm/utils.py`, `utils/http.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` |
| `llm/utils.py` | 25 | `config/constants.py`, `utils/http.py`, `utils/json_utils.py`, `utils/text.py` |
| `rag/index.py` | 5 | `config/constants.py`, `rag/parsers.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` |
| `rag/ingestion.py` | 3 | `config/constants.py`, `config/settings.py`, `rag/parsers.py`, `rag/store.py`, `session/state.py`, `utils/files.py`, `utils/json_utils.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py` |
| `rag/parsers.py` | 22 | `config/constants.py`, `utils/files.py`, `utils/json_utils.py`, `utils/media.py`, `utils/text.py` |
| `rag/store.py` | 2 | `config/constants.py`, `rag/index.py`, `rag/parsers.py`, `utils/files.py`, `utils/json_utils.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py` |
| `server/handlers.py` | 5 | `app/context.py`, `config/constants.py`, `config/paths.py`, `config/settings.py`, `llm/utils.py`, `session/manager.py`, `session/state.py`, `skills/store.py`, `utils/files.py`, `utils/http.py`, `utils/json_utils.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py` |
| `session/manager.py` | 2 | `config/constants.py`, `config/paths.py`, `config/settings.py`, `llm/client.py`, `llm/utils.py`, `session/state.py`, `utils/crypto.py`, `utils/files.py`, `utils/json_utils.py`, `utils/misc.py` |
| `session/state.py` | 1 | `agent/background.py`, `agent/bus.py`, `agent/events.py`, `agent/tasks.py`, `agent/todo.py`, `agent/worktree.py`, `config/constants.py`, `config/paths.py`, `config/settings.py`, `llm/client.py`, `llm/utils.py`, `rag/parsers.py`, `skills/store.py`, `utils/compress.py`, `utils/crypto.py`, `utils/errors.py`, `utils/files.py`, `utils/http.py`, `utils/json_utils.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py` |
| `skills/store.py` | 26 | `config/constants.py`, `config/paths.py`, `llm/utils.py`, `utils/files.py`, `utils/http.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` |
| `utils/compress.py` | 2 | — |
| `utils/crypto.py` | 1 | `utils/json_utils.py` |
| `utils/errors.py` | 2 | — |
| `utils/files.py` | 25 | `config/constants.py`, `config/paths.py`, `utils/http.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` |
| `utils/http.py` | 4 | — |
| `utils/json_utils.py` | 16 | `utils/text.py` |
| `utils/media.py` | 3 | — |
| `utils/misc.py` | 19 | — |
| `utils/text.py` | 22 | — |

## Module Details

### `__main__.py`

- Routed symbols: 2
- Cross-module imports: `app/context.py`: `AppContext`; `config/constants.py`: `AGENT_MAX_OUTPUT_TOKENS`, `ARBITER_DEFAULT_MAX_TOKENS`, `ARBITER_DEFAULT_TEMPERATURE`, `ARBITER_DEFAULT_TIMEOUT_SECONDS`, `CODE_ADMIN_PORT_OFFSET`, `DEFAULT_OLLAMA_BASE_URL`, `DEFAULT_OLLAMA_MODEL`, `DEFAULT_SHELL_COMMAND_TIMEOUT_SECONDS`, `DEFAULT_UI_LANGUAGE`, `DEFAULT_UI_STYLE`, `DEFAULT_WEB_UI_CONFIG`, `DEFAULT_WEB_UI_DIR`, `EXECUTION_MODE_SYNC`, `LIVE_INPUT_DELAY_NORMAL_ROUNDS`, `LIVE_INPUT_DELAY_TOOL_ROUNDS`, `LIVE_INPUT_DELAY_WRITE_ROUNDS`, `LIVE_INPUT_MAX_INJECTIONS`, `LIVE_INPUT_REINJECT_INTERVAL`, `LIVE_INPUT_WEIGHT_BASE_DELAYED`, `LIVE_INPUT_WEIGHT_BASE_NORMAL`, `LIVE_INPUT_WEIGHT_STEP_DELAYED`, `LIVE_INPUT_WEIGHT_STEP_NORMAL`, `MAX_AGENT_ROUNDS`, `MAX_AGENT_ROUNDS_CAP`, `MAX_RUN_SECONDS`, `MAX_RUN_TIMEOUT_SECONDS`, `MAX_SHELL_COMMAND_TIMEOUT_SECONDS`, `MIN_AGENT_ROUNDS`, `MIN_CONTEXT_TOKEN_LIMIT`, `MIN_RUN_TIMEOUT_SECONDS`, `MIN_SHELL_COMMAND_TIMEOUT_SECONDS`, `OFFLINE_JS_LIB_CATALOG`, `RAG_ADMIN_PORT_OFFSET`, `RAG_INCLUDE_FILENAME_ENTITIES_DEFAULT`, `TOKEN_THRESHOLD`, `UI_LANGUAGE_LABELS`, `UI_STYLE_LABELS`; `config/paths.py`: `LLM_CONFIG_PATH`, `REPO_ROOT`, `WORKDIR`; `config/settings.py`: `_to_bool_like`, `extract_daily_session_limit_setting`, `extract_js_lib_download_setting`, `extract_shell_command_timeout_setting`, `extract_show_upload_list_setting`, `extract_ui_style_setting`, `load_llm_config_from_source`, `load_web_ui_config_file`, `normalize_execution_mode`, `normalize_ui_language`, `normalize_ui_style`, `parse_llm_config_profiles`, `resolve_optional_file_path`, `resolve_web_ui_dir_path`, `select_preferred_skills_root`; `llm/utils.py`: `list_ollama_models`; `server/handlers.py`: `AgentHTTPServer`, `CodeAdminHandler`, `Handler`, `RagAdminHandler`, `SkillsHandler`; `skills/store.py`: `ensure_embedded_skills_at_root`, `ensure_runtime_skills`; `utils/files.py`: `ensure_offline_js_libs`; `utils/misc.py`: `BENIGN_SOCKET_DEBUG_LOG_ENABLED`, `detect_local_lan_ip`, `normalize_timeout_seconds`, `swallow_benign_socket_error`; `utils/text.py`: `trim`
- Symbols:
  - `main` (function, lines 54726-55707)
  - `_main_guard_55709` (main_guard, lines 55709-55710)

### `agent/background.py`

- Routed symbols: 1
- Cross-module imports: `utils/misc.py`: `make_id`, `now_ts`; `utils/text.py`: `trim`
- Symbols:
  - `BackgroundManager` (class, lines 11424-11504)

### `agent/bus.py`

- Routed symbols: 1
- Cross-module imports: `config/constants.py`: `VALID_MSG_TYPES`; `utils/crypto.py`: `CryptoBox`; `utils/misc.py`: `now_ts`
- Symbols:
  - `MessageBus` (class, lines 11506-11560)

### `agent/events.py`

- Routed symbols: 1
- Cross-module imports: none
- Symbols:
  - `EventHub` (class, lines 5543-5588)

### `agent/tasks.py`

- Routed symbols: 1
- Cross-module imports: `utils/crypto.py`: `CryptoBox`; `utils/json_utils.py`: `json_dumps`; `utils/misc.py`: `now_ts`
- Symbols:
  - `TaskManager` (class, lines 11296-11422)

### `agent/todo.py`

- Routed symbols: 1
- Cross-module imports: `config/constants.py`: `DEFAULT_UI_LANGUAGE`; `config/settings.py`: `backend_i18n_text`, `backend_role_label`, `normalize_ui_language`; `utils/text.py`: `infer_todo_status_from_text`, `normalize_work_text`, `split_structured_todo_content`, `trim`
- Symbols:
  - `TodoManager` (class, lines 5590-5859)

### `agent/worktree.py`

- Routed symbols: 1
- Cross-module imports: `agent/tasks.py`: `TaskManager`; `config/constants.py`: `DANGEROUS_PATTERNS`; `utils/crypto.py`: `CryptoBox`; `utils/json_utils.py`: `json_dumps`; `utils/misc.py`: `now_ts`; `utils/text.py`: `trim`
- Symbols:
  - `WorktreeManager` (class, lines 11562-11773)

### `app/context.py`

- Routed symbols: 1
- Cross-module imports: `config/constants.py`: `AGENT_MAX_OUTPUT_TOKENS`, `APP_CSS`, `APP_JS`, `APP_TS`, `ARBITER_DEFAULT_MAX_TOKENS`, `ARBITER_DEFAULT_TEMPERATURE`, `ARBITER_DEFAULT_TIMEOUT_SECONDS`, `CODE_ADMIN_CSS`, `CODE_ADMIN_INDEX_HTML`, `CODE_ADMIN_JS`, `CODE_IMPORT_WORKER_COUNT`, `CODE_LIBRARY_DIRNAME`, `CODE_PARSE_TIMEOUT_SECONDS`, `DEFAULT_REQUEST_TIMEOUT`, `DEFAULT_SHELL_COMMAND_TIMEOUT_SECONDS`, `DEFAULT_UI_LANGUAGE`, `DEFAULT_UI_STYLE`, `DEFAULT_WEB_UI_DIR`, `EXECUTION_MODE_SYNC`, `INDEX_HTML`, `MAX_AGENT_ROUNDS`, `MAX_AGENT_ROUNDS_CAP`, `MAX_RUN_SECONDS`, `MAX_RUN_TIMEOUT_SECONDS`, `MAX_SHELL_COMMAND_TIMEOUT_SECONDS`, `MIN_AGENT_ROUNDS`, `MIN_CONTEXT_TOKEN_LIMIT`, `MIN_RUN_TIMEOUT_SECONDS`, `MIN_SHELL_COMMAND_TIMEOUT_SECONDS`, `RAG_ADMIN_CSS`, `RAG_ADMIN_INDEX_HTML`, `RAG_ADMIN_JS`, `RAG_GRAPH_MAX_NODES`, `RAG_IMPORT_WORKER_COUNT`, `RAG_INCLUDE_FILENAME_ENTITIES_DEFAULT`, `RAG_LIBRARY_DIRNAME`, `RAG_MAX_GLOBAL_COMMUNITIES`, `RAG_MAX_IMPORT_BATCH_BYTES`, `RAG_MAX_IMPORT_BATCH_ITEMS`, `RAG_MAX_IMPORT_FILES`, `RAG_MAX_QUERY_RESULTS`, `RAG_PARSE_TIMEOUT_SECONDS`, `RAG_QUERY_CONTEXT_CHARS`, `SKILLS_APP_JS`, `SKILLS_EXTRA_CSS`, `SKILLS_INDEX_HTML`, `SKILL_REFRESH_MIN_INTERVAL_SECONDS`, `TOKEN_THRESHOLD`, `WEB_UI_OPTIONAL_FILES`, `WEB_UI_REQUIRED_FILES`; `config/paths.py`: `LLM_CONFIG_PATH`, `REPO_ROOT`, `_migrate_legacy_runtime_roots`; `config/settings.py`: `default_multimodal_capabilities`, `infer_model_multimodal_capabilities`, `merge_multimodal_capabilities`, `model_language_instruction`, `normalize_execution_mode`, `normalize_ui_language`, `normalize_ui_style`, `parse_capability_overrides`, `parse_llm_config_profiles`, `resolve_optional_file_path`, `resolve_web_ui_dir_path`; `llm/client.py`: `OllamaClient`; `llm/utils.py`: `extract_base_url`; `rag/ingestion.py`: `CodeIngestionService`, `RAGIngestionService`; `rag/parsers.py`: `CodeContentParser`, `RAGContentParser`; `rag/store.py`: `CodeLibraryStore`, `RAGLibraryStore`; `session/manager.py`: `SessionCreationLimitExceeded`, `SessionManager`; `session/state.py`: `SessionState`; `skills/store.py`: `SkillStore`, `_sanitize_skill_slug`, `analyze_skill_building_knowledge`, `ensure_runtime_skills`; `utils/crypto.py`: `CryptoBox`; `utils/files.py`: `_resolve_js_lib_asset_path`, `ensure_offline_js_libs`, `load_offline_js_lib_index`, `offline_js_lib_root`, `safe_path`, `try_read_text`; `utils/json_utils.py`: `TOOLS`, `extract_json_object_from_text`, `json_dumps`, `parse_json_object`; `utils/misc.py`: `DEFAULT_TIMEOUT_SECONDS`, `MAX_TIMEOUT_SECONDS`, `MIN_TIMEOUT_SECONDS`, `normalize_timeout_seconds`, `now_ts`, `sanitize_profile_id`; `utils/text.py`: `parse_front_matter`, `trim`
- Symbols:
  - `AppContext` (class, lines 50889-53322)

### `config/constants.py`

- Routed symbols: 294
- Cross-module imports: `utils/json_utils.py`: `TOOL_SPEC_BY_NAME`; `utils/misc.py`: `DEFAULT_TIMEOUT_SECONDS`
- Symbols:
  - `APP_VERSION` (constant, lines 58-58)
  - `DEFAULT_OLLAMA_BASE_URL` (constant, lines 59-59)
  - `DEFAULT_OLLAMA_MODEL` (constant, lines 60-60)
  - `LONG_OUTPUT_MODEL_PAGE_CHARS` (constant, lines 130-130)
  - `LONG_OUTPUT_UI_PAGE_CHARS` (constant, lines 131-131)
  - `LONG_OUTPUT_UI_PREVIEW_MAX_PAGES` (constant, lines 132-132)
  - `LONG_OUTPUT_LISTING_OFFLOAD_CHARS` (constant, lines 133-133)
  - `LONG_OUTPUT_READ_PAGE_LINES` (constant, lines 134-134)
  - `LONG_OUTPUT_READ_PAGE_MAX_CHARS` (constant, lines 135-135)
  - `LONG_OUTPUT_TEMP_MAX_FILES` (constant, lines 136-136)
  - `RAG_LIBRARY_DIRNAME` (constant, lines 138-138)
  - `RAG_ADMIN_PORT_OFFSET` (constant, lines 139-139)
  - `CODE_LIBRARY_DIRNAME` (constant, lines 140-140)
  - `CODE_ADMIN_PORT_OFFSET` (constant, lines 141-141)
  - `RAG_CHUNK_CHARS` (constant, lines 142-142)
  - `RAG_CHUNK_OVERLAP` (constant, lines 143-143)
  - `RAG_MAX_CHUNKS_PER_DOC` (constant, lines 144-144)
  - `CODE_CHUNK_CHARS` (constant, lines 145-145)
  - `CODE_CHUNK_OVERLAP` (constant, lines 146-146)
  - `CODE_MAX_CHUNKS_PER_DOC` (constant, lines 147-147)
  - `RAG_MAX_QUERY_RESULTS` (constant, lines 148-148)
  - `RAG_GRAPH_MAX_NODES` (constant, lines 149-149)
  - `RAG_TASK_HISTORY_LIMIT` (constant, lines 150-150)
  - `RAG_MODEL_MEDIA_MAX_BYTES` (constant, lines 151-151)
  - `RAG_MAX_IMPORT_FILES` (constant, lines 152-152)
  - `RAG_MAX_IMPORT_BATCH_ITEMS` (constant, lines 153-153)
  - `RAG_MAX_IMPORT_BATCH_BYTES` (constant, lines 154-154)
  - `RAG_PDF_IMAGE_LIMIT` (constant, lines 155-155)
  - `RAG_QUERY_CONTEXT_CHARS` (constant, lines 156-156)
  - `RAG_MAX_GLOBAL_COMMUNITIES` (constant, lines 157-157)
  - `RAG_MAX_COMMUNITY_MAP_SUPPORT` (constant, lines 158-158)
  - `RAG_INCLUDE_FILENAME_ENTITIES_DEFAULT` (constant, lines 159-159)
  - `RAG_DYNAMIC_NOISE_MIN_DOC_FREQ` (constant, lines 160-160)
  - `RAG_DYNAMIC_NOISE_MIN_COMMUNITY_FREQ` (constant, lines 161-161)
  - `RAG_DYNAMIC_NOISE_SOFT_DOC_RATIO` (constant, lines 162-162)
  - `RAG_DYNAMIC_NOISE_HARD_DOC_RATIO` (constant, lines 163-163)
  - `RAG_DYNAMIC_NOISE_SOFT_COMMUNITY_RATIO` (constant, lines 164-164)
  - `RAG_DYNAMIC_NOISE_HARD_COMMUNITY_RATIO` (constant, lines 165-165)
  - `RAG_IMPORT_WORKER_COUNT` (constant, lines 166-169)
  - `CODE_IMPORT_WORKER_COUNT` (constant, lines 170-173)
  - `RAG_PARSE_TIMEOUT_SECONDS` (constant, lines 174-177)
  - `CODE_PARSE_TIMEOUT_SECONDS` (constant, lines 178-181)
  - `TOKEN_THRESHOLD` (constant, lines 182-182)
  - `IDLE_TIMEOUT` (constant, lines 183-183)
  - `POLL_INTERVAL` (constant, lines 184-184)
  - `SSE_HEARTBEAT_SECONDS` (constant, lines 185-185)
  - `MODEL_CALL_PROGRESS_DELAY` (constant, lines 186-186)
  - `MODEL_CALL_PROGRESS_INTERVAL` (constant, lines 187-187)
  - `MAX_AGENT_ROUNDS` (constant, lines 188-188)
  - `MIN_AGENT_ROUNDS` (constant, lines 189-189)
  - `MAX_AGENT_ROUNDS_CAP` (constant, lines 190-190)
  - `REPEATED_TOOL_LOOP_THRESHOLD` (constant, lines 191-191)
  - `BASH_READ_LOOP_THRESHOLD` (constant, lines 192-192)
  - `HARD_BREAK_TOOL_ERROR_THRESHOLD` (constant, lines 193-193)
  - `HARD_BREAK_RECOVERY_ROUND_THRESHOLD` (constant, lines 194-194)
  - `FUSED_FAULT_BREAK_THRESHOLD` (constant, lines 195-195)
  - `STALL_SEVERITY_ESCALATION_THRESHOLD` (constant, lines 196-196)
  - `STALL_SEVERITY_WEIGHT_BASH_READ_LOOP` (constant, lines 197-197)
  - `STALL_SEVERITY_WEIGHT_REPEATED_TOOL` (constant, lines 198-198)
  - `STALL_SEVERITY_WEIGHT_FAULT` (constant, lines 199-199)
  - `STALL_SEVERITY_WEIGHT_RECOVERY_RETRY` (constant, lines 200-200)
  - `STALL_SEVERITY_WEIGHT_WATCHDOG` (constant, lines 201-201)
  - `STALL_SEVERITY_DECAY_ON_SUCCESS` (constant, lines 202-202)
  - `STALL_ESCALATION_MIN_LEVEL` (constant, lines 203-203)
  - `STALL_PLAN_SYNTHESIS_MAX_TOKENS` (constant, lines 204-204)
  - `STALL_ESCALATION_CONTEXT_MAX_CHARS` (constant, lines 205-205)
  - `MAX_RUN_SECONDS` (constant, lines 206-206)
  - `MIN_RUN_TIMEOUT_SECONDS` (constant, lines 207-207)
  - `MAX_RUN_TIMEOUT_SECONDS` (constant, lines 208-208)
  - `DEFAULT_REQUEST_TIMEOUT` (constant, lines 218-218)
  - `_SHELL_AUTO_CONFIRM_PATTERNS` (assignment, lines 221-234)
  - `MIN_SHELL_COMMAND_TIMEOUT_SECONDS` (constant, lines 235-235)
  - `MAX_SHELL_COMMAND_TIMEOUT_SECONDS` (constant, lines 236-236)
  - `DEFAULT_SHELL_COMMAND_TIMEOUT_SECONDS` (constant, lines 237-251)
  - `AUTO_CONTINUE_BUDGET_DEFAULT` (constant, lines 252-252)
  - `AGENT_MAX_OUTPUT_TOKENS` (constant, lines 253-253)
  - `OLLAMA_THINKING_TOOL_BUFFER` (constant, lines 254-254)
  - `WATCHDOG_INTENT_NO_TOOL_THRESHOLD` (constant, lines 255-255)
  - `WATCHDOG_REPEAT_NO_TOOL_THRESHOLD` (constant, lines 256-256)
  - `WATCHDOG_INTENT_NO_TOOL_THRESHOLD_SINGLE` (constant, lines 257-257)
  - `WATCHDOG_REPEAT_NO_TOOL_THRESHOLD_SINGLE` (constant, lines 258-258)
  - `WATCHDOG_STATE_STALL_THRESHOLD` (constant, lines 259-259)
  - `WATCHDOG_CONTEXT_STALL_THRESHOLD` (constant, lines 260-260)
  - `WATCHDOG_REPEAT_SIMILARITY_THRESHOLD` (constant, lines 261-261)
  - `WATCHDOG_CONTEXT_NEAR_RATIO` (constant, lines 262-262)
  - `WATCHDOG_MAX_DECOMPOSE_STEPS` (constant, lines 263-263)
  - `WATCHDOG_STEP_MAX_ATTEMPTS` (constant, lines 264-264)
  - `EMPTY_ACTION_MIN_CONTENT_CHARS` (constant, lines 265-265)
  - `EMPTY_ACTION_WAKEUP_RETRY_LIMIT` (constant, lines 266-266)
  - `THINKING_BUDGET_FORCE_RATIO` (constant, lines 267-267)
  - `_TOOL_TIMEOUT_MAP` (assignment, lines 269-285)
  - `_DEFAULT_TOOL_TIMEOUT` (assignment, lines 286-286)
  - `TRUNCATION_CONTINUATION_MAX_PASSES` (constant, lines 287-287)
  - `TRUNCATION_CONTINUATION_MAX_TOKENS` (constant, lines 288-288)
  - `TRUNCATION_CONTINUATION_TAIL_CHARS` (constant, lines 289-289)
  - `TRUNCATION_CONTINUATION_ECHO_CHARS` (constant, lines 290-290)
  - `TRUNCATION_OVERLAP_SCAN_CHARS` (constant, lines 291-291)
  - `TRUNCATION_PAIR_SCAN_CHARS` (constant, lines 292-292)
  - `TRUNCATION_LIVE_BUFFER_MAX_CHARS` (constant, lines 293-293)
  - `MIN_CONTEXT_TOKEN_LIMIT` (constant, lines 294-294)
  - `COMPACT_TIER1_PCT` (constant, lines 296-296)
  - `COMPACT_TIER2_PCT` (constant, lines 297-297)
  - `COMPACT_TIER3_PCT` (constant, lines 298-298)
  - `COMPACT_TIER1_ABS` (constant, lines 300-300)
  - `COMPACT_TIER2_ABS` (constant, lines 301-301)
  - `FILE_BUFFER_CONTENT_THRESHOLD` (constant, lines 303-303)
  - `FILE_BUFFER_MAX_FILES` (constant, lines 304-304)
  - `AGENT_MSG_LIMIT_TIER0` (constant, lines 306-306)
  - `AGENT_MSG_LIMIT_TIER1` (constant, lines 307-307)
  - `AGENT_MSG_LIMIT_TIER2` (constant, lines 308-308)
  - `AGENT_MSG_LIMIT_TIER3` (constant, lines 309-309)
  - `AGENT_CTX_LIMIT_TIER0` (constant, lines 310-310)
  - `AGENT_CTX_LIMIT_TIER1` (constant, lines 311-311)
  - `AGENT_CTX_LIMIT_TIER2` (constant, lines 312-312)
  - `AGENT_CTX_LIMIT_TIER3` (constant, lines 313-313)
  - `MANAGER_CTX_LIMIT_TIER0` (constant, lines 314-314)
  - `MANAGER_CTX_LIMIT_TIER1` (constant, lines 315-315)
  - `MANAGER_CTX_LIMIT_TIER2` (constant, lines 316-316)
  - `MANAGER_CTX_LIMIT_TIER3` (constant, lines 317-317)
  - `MAX_CONTEXT_ARCHIVE_SEGMENTS` (constant, lines 318-318)
  - `MODEL_OUTPUT_RETRY_TIMES` (constant, lines 319-319)
  - `ARBITER_TRIGGER_MIN_CONTENT_CHARS` (constant, lines 320-320)
  - `ARBITER_VALID_PLANNING_STREAK_LIMIT` (constant, lines 321-321)
  - `ARBITER_DEFAULT_TIMEOUT_SECONDS` (constant, lines 322-322)
  - `ARBITER_DEFAULT_MAX_TOKENS` (constant, lines 323-323)
  - `ARBITER_DEFAULT_TEMPERATURE` (constant, lines 324-324)
  - `LIVE_INPUT_DELAY_WRITE_ROUNDS` (constant, lines 325-325)
  - `LIVE_INPUT_DELAY_TOOL_ROUNDS` (constant, lines 326-326)
  - `LIVE_INPUT_DELAY_NORMAL_ROUNDS` (constant, lines 327-327)
  - `LIVE_INPUT_MAX_INJECTIONS` (constant, lines 328-328)
  - `LIVE_INPUT_REINJECT_INTERVAL` (constant, lines 329-329)
  - `LIVE_INPUT_WEIGHT_BASE_DELAYED` (constant, lines 330-330)
  - `LIVE_INPUT_WEIGHT_BASE_NORMAL` (constant, lines 331-331)
  - `LIVE_INPUT_WEIGHT_STEP_DELAYED` (constant, lines 332-332)
  - `LIVE_INPUT_WEIGHT_STEP_NORMAL` (constant, lines 333-333)
  - `FINAL_SUMMARY_MIN_CHARS` (constant, lines 348-348)
  - `FINAL_SUMMARY_STRICT_MIN_CHARS` (constant, lines 349-349)
  - `RUNTIME_CONTROL_HINT_PREFIXES` (constant, lines 350-367)
  - `RETRY_RUNTIME_HINT_PREFIXES` (constant, lines 368-382)
  - `EXECUTION_MODE_SINGLE` (constant, lines 383-383)
  - `EXECUTION_MODE_SEQUENTIAL` (constant, lines 384-384)
  - `EXECUTION_MODE_SYNC` (constant, lines 385-385)
  - `EXECUTION_MODE_CHOICES` (constant, lines 386-390)
  - `AGENT_ROLES` (constant, lines 391-391)
  - `AGENT_BUBBLE_ROLES` (constant, lines 392-392)
  - `AGENT_ROLE_LABELS` (constant, lines 393-399)
  - `AGENT_ROLE_BUBBLE_COLORS` (constant, lines 400-406)
  - `BLACKBOARD_STATUSES` (constant, lines 407-416)
  - `TASK_COMPLEXITY_LEVELS` (constant, lines 417-417)
  - `TASK_COMPLEXITY_RANKS` (constant, lines 418-423)
  - `TASK_PROFILE_TYPES` (constant, lines 424-430)
  - `TASK_LEVEL_CHOICES` (constant, lines 431-431)
  - `TASK_SCALE_PREFERENCES` (constant, lines 432-432)
  - `SEMANTIC_CONFIDENCE_CHOICES` (constant, lines 433-433)
  - `TASK_LEVEL_POLICIES` (constant, lines 434-480)
  - `MANAGER_ROUTE_TARGETS` (constant, lines 481-481)
  - `BLACKBOARD_MAX_LOG_ENTRIES` (constant, lines 482-482)
  - `BLACKBOARD_MAX_TEXT` (constant, lines 483-483)
  - `SKILL_REFRESH_MIN_INTERVAL_SECONDS` (constant, lines 484-484)
  - `SKILL_PROMPT_MAX_ITEMS` (constant, lines 485-485)
  - `SKILL_PROMPT_MAX_CHARS` (constant, lines 486-486)
  - `SKILL_RUNTIME_CACHE_MAX_ENTRIES` (constant, lines 487-487)
  - `SKILL_RUNTIME_CACHE_MAX_BYTES` (constant, lines 488-488)
  - `AUTO_SKILLS_ROOT_CANDIDATES` (constant, lines 489-489)
  - `SKILL_DEFAULT_ATTACHMENT_GLOBS` (constant, lines 490-520)
  - `SKILL_INLINE_ATTACHMENT_MAX_FILES` (constant, lines 521-521)
  - `SKILL_INLINE_ATTACHMENT_MAX_CHARS` (constant, lines 522-522)
  - `SKILL_RESOURCE_MANIFEST_MAX_ITEMS` (constant, lines 523-523)
  - `SKILL_BODY_COMPACT_THRESHOLD_CHARS` (constant, lines 524-524)
  - `SKILL_BODY_PREVIEW_CHARS` (constant, lines 525-525)
  - `SKILLS_VIRTUAL_PREFIX` (constant, lines 526-526)
  - `SKILLS_EXTERNAL_MOUNT` (constant, lines 527-527)
  - `PLAN_MODE_ENABLED_LEVELS` (constant, lines 528-528)
  - `PLAN_MODE_FORCED_LEVELS` (constant, lines 529-529)
  - `PLAN_MODE_USER_CHOICES` (constant, lines 530-530)
  - `TASK_PHASES` (constant, lines 532-532)
  - `TASK_PHASE_ROUTING` (constant, lines 533-540)
  - `COMPLEXITY_KEYWORDS` (constant, lines 542-547)
  - `USER_COMPLEXITY_SIMPLE_TOKENS` (constant, lines 548-552)
  - `USER_COMPLEXITY_MODERATE_TOKENS` (constant, lines 553-557)
  - `USER_COMPLEXITY_COMPLEX_TOKENS` (constant, lines 558-562)
  - `USER_COMPLEXITY_EXPERT_TOKENS` (constant, lines 563-567)
  - `PLAN_MODE_EXPLORER_MAX_ROUNDS` (constant, lines 568-568)
  - `PLAN_MODE_SYNTHESIS_MAX_ATTEMPTS` (constant, lines 569-569)
  - `REVIEWER_DEBUG_MODE_MAX_ROUNDS` (constant, lines 571-571)
  - `REVIEWER_DEBUG_TOOL_ALLOWLIST` (constant, lines 572-576)
  - `EXPLORER_STALL_THRESHOLD` (constant, lines 577-577)
  - `DEVELOPER_EDIT_STALL_THRESHOLD` (constant, lines 578-578)
  - `PLAN_MODE_MANAGER_SYNTHESIS_MAX_TOKENS` (constant, lines 579-579)
  - `PLAN_MODE_MAX_OPTIONS` (constant, lines 580-580)
  - `PLAN_FILE_RELATIVE_PATH` (constant, lines 581-581)
  - `PLAN_BUBBLE_MAX_CHARS` (constant, lines 582-582)
  - `PLAN_NOTICE_BODY_MAX_CHARS` (constant, lines 583-583)
  - `PLAN_MESSAGE_EVENT_MAX_CHARS` (constant, lines 584-584)
  - `PLAN_STEP_FULL_CONTENT_MAX_CHARS` (constant, lines 585-585)
  - `PLAN_MODE_RESEARCH_TOOL_ALLOWLIST` (constant, lines 586-590)
  - `FAILURE_LEDGER_MAX_FIXES` (constant, lines 591-591)
  - `FAILURE_LEDGER_MAX_COMPILE_ERRORS` (constant, lines 592-592)
  - `FAILURE_LEDGER_MAX_DELEGATIONS` (constant, lines 593-593)
  - `FAILURE_LEDGER_MAX_STALLS` (constant, lines 594-594)
  - `FAILURE_LEDGER_MAX_TOOL_FPS` (constant, lines 595-595)
  - `FAILURE_LEDGER_MAX_ERRORS` (constant, lines 596-596)
  - `ERROR_CATEGORY_DEFS` (constant, lines 599-636)
  - `CHECKPOINT_MAX_COUNT` (constant, lines 637-637)
  - `CHECKPOINT_INTERVAL_ROUNDS` (constant, lines 638-638)
  - `PERSISTED_ROUTES_MAX` (constant, lines 639-639)
  - `HTML_FRONTEND_REQUEST_KEYWORDS` (constant, lines 640-679)
  - `DEEP_RESEARCH_REQUEST_KEYWORDS` (constant, lines 680-702)
  - `DEEP_RESEARCH_RETRIEVAL_KEYWORDS` (constant, lines 703-722)
  - `DEEP_RESEARCH_TEXT_ONLY_HINT_KEYWORDS` (constant, lines 723-740)
  - `DANGEROUS_PATTERNS` (constant, lines 742-742)
  - `VALID_MSG_TYPES` (constant, lines 743-749)
  - `SUPPORTED_UI_LANGUAGES` (constant, lines 751-756)
  - `UI_LANGUAGE_LABELS` (constant, lines 757-757)
  - `DEFAULT_UI_LANGUAGE` (constant, lines 758-758)
  - `UI_STYLE_CHOICES` (constant, lines 759-759)
  - `UI_STYLE_LABELS` (constant, lines 760-760)
  - `DEFAULT_UI_STYLE` (constant, lines 761-761)
  - `DEFAULT_WEB_UI_DIR` (constant, lines 762-762)
  - `DEFAULT_WEB_UI_CONFIG` (constant, lines 763-763)
  - `WEB_UI_REQUIRED_FILES` (constant, lines 764-771)
  - `WEB_UI_OPTIONAL_FILES` (constant, lines 772-772)
  - `IMAGE_EXTS` (constant, lines 774-787)
  - `IMAGE_FORMATS_NEED_CONVERSION` (constant, lines 788-788)
  - `IMAGE_SAFE_FORMATS` (constant, lines 789-789)
  - `AUDIO_EXTS` (constant, lines 790-800)
  - `VIDEO_EXTS` (constant, lines 801-811)
  - `CODE_PREVIEW_STAGE_MAX_BYTES` (constant, lines 812-812)
  - `CODE_PREVIEW_STAGE_MAX_ROWS` (constant, lines 813-813)
  - `CODE_PREVIEW_STAGE_MAX_PER_FILE` (constant, lines 814-814)
  - `CODE_PREVIEW_STAGE_MAX_TOTAL` (constant, lines 815-815)
  - `RENDER_FRAME_MAX_B64_CHARS` (constant, lines 816-816)
  - `RENDER_FRAME_MAX_POINTS` (constant, lines 817-817)
  - `RENDER_FRAME_MAX_LINES` (constant, lines 818-818)
  - `RENDER_FRAME_MAX_LINE_POINTS` (constant, lines 819-819)
  - `RENDER_FRAME_ACTIVITY_INTERVAL_SECONDS` (constant, lines 820-820)
  - `RAW_TOOLCALL_TEXT_FILTER_THRESHOLD` (constant, lines 821-821)
  - `ASSISTANT_TEXT_PERSIST_MAX_CHARS` (constant, lines 822-822)
  - `ASSISTANT_MESSAGE_EVENT_MAX_CHARS` (constant, lines 823-823)
  - `CODE_PREVIEW_EXTS` (constant, lines 824-913)
  - `CODE_PREVIEW_FILENAMES` (constant, lines 914-925)
  - `MEDIA_CAPABILITY_KEYS` (constant, lines 926-933)
  - `SAMPLE_IMAGE_PNG_B64` (constant, lines 934-937)
  - `SAMPLE_AUDIO_WAV_B64` (constant, lines 938-940)
  - `SAMPLE_VIDEO_MP4_B64` (constant, lines 941-943)
  - `OFFLINE_JS_LIB_CATALOG` (constant, lines 945-1203)
  - `OFFLINE_JS_LIB_INDEX_FILE` (constant, lines 1204-1204)
  - `OFFLINE_JS_LIB_README_FILE` (constant, lines 1205-1205)
  - `BACKEND_I18N` (constant, lines 1391-1460)
  - `call_backend_i18n_en_update_l1462` (expression, lines 1462-1555)
  - `call_backend_i18n_zh_cn_update_l1556` (expression, lines 1556-1649)
  - `call_backend_i18n_zh_tw_update_l1650` (expression, lines 1650-1743)
  - `call_backend_i18n_ja_update_l1744` (expression, lines 1744-1837)
  - `OPENAI_COMPAT_PROVIDER_NAMES` (constant, lines 3867-3875)
  - `OPENAI_LIKE_PROVIDER_NAMES` (constant, lines 3877-3877)
  - `TABULAR_PREVIEW_EXTS` (constant, lines 5321-5321)
  - `EXCEL_PREVIEW_EXTS` (constant, lines 5322-5322)
  - `PRESENTATION_PREVIEW_EXTS` (constant, lines 5323-5323)
  - `DOCUMENT_PREVIEW_EXTS` (constant, lines 5324-5324)
  - `EMBEDDED_SKILLS_ARCHIVE_B64` (constant, lines 5861-6380)
  - `EMBEDDED_SKILLS_ARCHIVE_SHA256` (constant, lines 6381-6381)
  - `EMBEDDED_SKILLS_ARCHIVE_FILES` (constant, lines 6382-6405)
  - `BUILTIN_CLAWHUB_SKILLS_VERSION` (constant, lines 9565-9565)
  - `EMBEDDED_CLAWHUB_SKILLS_ARCHIVE_B64` (constant, lines 9567-9811)
  - `SKILL_PROTOCOL_LOCAL` (constant, lines 9870-9870)
  - `SKILL_PROTOCOL_CLAWHUB` (constant, lines 9871-9871)
  - `SKILL_PROTOCOL_HTTP_JSON` (constant, lines 9872-9872)
  - `SKILL_PROTOCOL_SPECS` (constant, lines 9874-9905)
  - `AGENT_TOOL_ALLOWLIST` (constant, lines 13070-13113)
  - `INDEX_HTML` (constant, lines 39946-40133)
  - `APP_CSS` (constant, lines 40135-40523)
  - `APP_JS` (constant, lines 40525-43627)
  - `APP_TS` (constant, lines 43629-43656)
  - `SKILLS_INDEX_HTML` (constant, lines 43658-43812)
  - `SKILLS_EXTRA_CSS` (constant, lines 43814-43909)
  - `SKILLS_APP_JS` (constant, lines 43911-44052)
  - `RAG_TERM_GROUPS` (constant, lines 44054-44064)
  - `RAG_RESEARCH_HINTS` (constant, lines 44065-44086)
  - `RAG_CODE_HINTS` (constant, lines 44087-44097)
  - `RAG_SHORT_TOKEN_ALLOWLIST` (constant, lines 44098-44113)
  - `RAG_EN_STOPWORDS` (constant, lines 44114-44186)
  - `RAG_ZH_STOPWORDS` (constant, lines 44187-44223)
  - `RAG_GENERIC_ENTITY_TERMS_EN` (constant, lines 44224-44302)
  - `RAG_GENERIC_ENTITY_TERMS_ZH` (constant, lines 44303-44345)
  - `RAG_STRUCTURAL_ENTITY_PATTERNS` (constant, lines 44346-44364)
  - `CODE_LIBRARY_IGNORED_DIRS` (constant, lines 44687-44692)
  - `CODE_LIBRARY_LANGUAGE_BY_EXT` (constant, lines 44693-44749)
  - `CODE_LIBRARY_SPECIAL_FILENAMES` (constant, lines 44750-44756)
  - `RAG_ADMIN_INDEX_HTML` (constant, lines 49363-49520)
  - `RAG_ADMIN_CSS` (constant, lines 49522-49612)
  - `RAG_ADMIN_JS` (constant, lines 49614-50840)
  - `CODE_ADMIN_INDEX_HTML` (constant, lines 50842-50851)
  - `CODE_ADMIN_CSS` (constant, lines 50852-50882)
  - `CODE_ADMIN_JS` (constant, lines 50883-50887)

### `config/paths.py`

- Routed symbols: 8
- Cross-module imports: `utils/text.py`: `trim`
- Symbols:
  - `SCRIPT_DIR` (constant, lines 61-61)
  - `_resolve_default_agent_workdir` (function, lines 90-94)
  - `_migrate_legacy_runtime_roots` (function, lines 96-124)
  - `WORKDIR` (constant, lines 126-126)
  - `CODES_ROOT` (constant, lines 127-127)
  - `LLM_CONFIG_PATH` (constant, lines 128-128)
  - `detect_repo_root` (function, lines 2464-2478)
  - `REPO_ROOT` (constant, lines 2480-2480)

### `config/settings.py`

- Routed symbols: 33
- Cross-module imports: `config/constants.py`: `AUTO_SKILLS_ROOT_CANDIDATES`, `BACKEND_I18N`, `DEFAULT_REQUEST_TIMEOUT`, `DEFAULT_SHELL_COMMAND_TIMEOUT_SECONDS`, `DEFAULT_UI_LANGUAGE`, `DEFAULT_UI_STYLE`, `DEFAULT_WEB_UI_CONFIG`, `DEFAULT_WEB_UI_DIR`, `EXECUTION_MODE_CHOICES`, `EXECUTION_MODE_SEQUENTIAL`, `EXECUTION_MODE_SINGLE`, `EXECUTION_MODE_SYNC`, `MAX_SHELL_COMMAND_TIMEOUT_SECONDS`, `MEDIA_CAPABILITY_KEYS`, `MIN_SHELL_COMMAND_TIMEOUT_SECONDS`, `SUPPORTED_UI_LANGUAGES`, `TASK_COMPLEXITY_LEVELS`, `TASK_COMPLEXITY_RANKS`, `UI_LANGUAGE_LABELS`, `UI_STYLE_CHOICES`, `USER_COMPLEXITY_COMPLEX_TOKENS`, `USER_COMPLEXITY_EXPERT_TOKENS`, `USER_COMPLEXITY_MODERATE_TOKENS`, `USER_COMPLEXITY_SIMPLE_TOKENS`; `config/paths.py`: `WORKDIR`; `llm/utils.py`: `_is_http_url`, `_resolve_local_path`, `complete_chat_endpoint`, `extract_base_url`, `is_openai_like_provider`, `normalize_openai_compat_provider_name`, `strip_thinking_content`; `skills/store.py`: `ensure_embedded_skills`; `utils/http.py`: `urlopen`; `utils/json_utils.py`: `parse_json_object`; `utils/misc.py`: `MAX_TIMEOUT_SECONDS`, `MIN_TIMEOUT_SECONDS`, `normalize_timeout_seconds`, `sanitize_profile_id`; `utils/text.py`: `trim`
- Symbols:
  - `normalize_ui_language` (function, lines 1289-1311)
  - `normalize_ui_style` (function, lines 1314-1331)
  - `supported_ui_languages_payload` (function, lines 1334-1335)
  - `normalize_execution_mode` (function, lines 1338-1357)
  - `model_language_instruction` (function, lines 1360-1388)
  - `backend_i18n_text` (function, lines 1840-1850)
  - `backend_role_label` (function, lines 1853-1857)
  - `_detect_os_shell_instruction` (function, lines 1860-1899)
  - `resolve_web_ui_dir_path` (function, lines 1901-1908)
  - `resolve_optional_file_path` (function, lines 1911-1918)
  - `resolve_skills_root_path` (function, lines 1921-1928)
  - `_count_skill_markdown_files` (function, lines 1931-1942)
  - `select_preferred_skills_root` (function, lines 1945-1979)
  - `load_web_ui_config_file` (function, lines 1982-1996)
  - `extract_show_upload_list_setting` (function, lines 1999-2013)
  - `extract_ui_style_setting` (function, lines 2016-2030)
  - `extract_js_lib_download_setting` (function, lines 2033-2052)
  - `extract_daily_session_limit_setting` (function, lines 2055-2098)
  - `extract_shell_command_timeout_setting` (function, lines 2101-2147)
  - `default_multimodal_capabilities` (function, lines 2156-2164)
  - `_to_bool_like` (function, lines 2167-2177)
  - `infer_model_multimodal_capabilities` (function, lines 2180-2224)
  - `parse_capability_overrides` (function, lines 2227-2264)
  - `merge_multimodal_capabilities` (function, lines 2267-2274)
  - `parse_media_endpoints` (function, lines 2277-2291)
  - `infer_user_complexity_value` (function, lines 3785-3801)
  - `normalize_task_complexity` (function, lines 3803-3831)
  - `task_complexity_rank` (function, lines 3833-3834)
  - `task_complexity_at_least` (function, lines 3836-3837)
  - `max_task_complexity` (function, lines 3839-3848)
  - `load_llm_config_from_source` (function, lines 3992-4026)
  - `parse_llm_config_profiles` (function, lines 4028-4614)
  - `looks_like_llm_config` (function, lines 4616-4690)

### `llm/client.py`

- Routed symbols: 2
- Cross-module imports: `config/constants.py`: `DEFAULT_REQUEST_TIMEOUT`, `OLLAMA_THINKING_TOOL_BUFFER`, `SAMPLE_AUDIO_WAV_B64`, `SAMPLE_IMAGE_PNG_B64`, `SAMPLE_VIDEO_MP4_B64`; `config/settings.py`: `default_multimodal_capabilities`, `infer_model_multimodal_capabilities`, `merge_multimodal_capabilities`, `parse_capability_overrides`, `parse_media_endpoints`; `llm/utils.py`: `complete_chat_endpoint`, `is_openai_compat_provider`, `is_openai_like_provider`, `split_thinking_content`; `utils/http.py`: `urlopen`; `utils/json_utils.py`: `canonicalize_tool_name`, `json_dumps`, `parse_json_object`, `parse_tool_arguments`, `parse_tool_arguments_with_error`; `utils/misc.py`: `MAX_TIMEOUT_SECONDS`, `MIN_TIMEOUT_SECONDS`, `make_id`, `normalize_timeout_seconds`, `now_ts`; `utils/text.py`: `trim`
- Symbols:
  - `OllamaError` (class, lines 11775-11778)
  - `OllamaClient` (class, lines 11780-12832)

### `llm/utils.py`

- Routed symbols: 25
- Cross-module imports: `config/constants.py`: `OPENAI_COMPAT_PROVIDER_NAMES`, `OPENAI_LIKE_PROVIDER_NAMES`; `utils/http.py`: `urlopen`; `utils/json_utils.py`: `json_dumps`, `parse_json_object`; `utils/text.py`: `trim`
- Symbols:
  - `probe_ollama_environment` (function, lines 3471-3484)
  - `list_ollama_models` (function, lines 3486-3488)
  - `_OLLAMA_TAG_CACHE_LOCK` (assignment, lines 3490-3490)
  - `_OLLAMA_TAG_CACHE` (assignment, lines 3491-3491)
  - `list_ollama_models_cached` (function, lines 3501-3538)
  - `resolve_ollama_model` (function, lines 3540-3550)
  - `infer_thinking_model` (function, lines 3552-3554)
  - `split_thinking_content` (function, lines 3556-3597)
  - `strip_thinking_content` (function, lines 3599-3600)
  - `check_ollama_model_ready` (function, lines 3602-3626)
  - `list_loaded_ollama_models` (function, lines 3628-3641)
  - `wake_ollama_model` (function, lines 3643-3673)
  - `try_pull_ollama_model` (function, lines 3675-3693)
  - `ordered_model_candidates` (function, lines 3695-3713)
  - `pick_working_ollama_model` (function, lines 3715-3731)
  - `extract_base_url` (function, lines 3764-3772)
  - `complete_chat_endpoint` (function, lines 3774-3783)
  - `normalize_openai_compat_provider_name` (function, lines 3850-3865)
  - `is_openai_compat_provider` (function, lines 3879-3880)
  - `is_openai_like_provider` (function, lines 3882-3883)
  - `openai_compat_probe_headers` (function, lines 3885-3896)
  - `openai_compat_model_list_urls` (function, lines 3898-3930)
  - `extract_openai_compat_model_ids` (function, lines 3932-3965)
  - `_is_http_url` (function, lines 3967-3972)
  - `_resolve_local_path` (function, lines 3974-3990)

### `rag/index.py`

- Routed symbols: 5
- Cross-module imports: `config/constants.py`: `RAG_DYNAMIC_NOISE_HARD_COMMUNITY_RATIO`, `RAG_DYNAMIC_NOISE_HARD_DOC_RATIO`, `RAG_DYNAMIC_NOISE_MIN_COMMUNITY_FREQ`, `RAG_DYNAMIC_NOISE_MIN_DOC_FREQ`, `RAG_DYNAMIC_NOISE_SOFT_COMMUNITY_RATIO`, `RAG_DYNAMIC_NOISE_SOFT_DOC_RATIO`, `RAG_EN_STOPWORDS`, `RAG_GRAPH_MAX_NODES`, `RAG_INCLUDE_FILENAME_ENTITIES_DEFAULT`, `RAG_MAX_COMMUNITY_MAP_SUPPORT`, `RAG_MAX_GLOBAL_COMMUNITIES`, `RAG_MAX_QUERY_RESULTS`; `rag/parsers.py`: `_code_is_test_path`, `_rag_apply_filename_entity_policy`, `_rag_choose_community`, `_rag_classify_document`, `_rag_expand_tokens`, `_rag_extract_entities`, `_rag_filter_entities`, `_rag_tokenize`; `utils/json_utils.py`: `json_dumps`; `utils/misc.py`: `now_ts`; `utils/text.py`: `trim`
- Symbols:
  - `_code_module_name` (function, lines 44783-44797)
  - `_code_choose_community` (function, lines 44800-44807)
  - `_code_query_terms` (function, lines 44810-44822)
  - `TFGraphIDFIndex` (class, lines 45798-47156)
  - `CodeGraphIndex` (class, lines 48596-49008)

### `rag/ingestion.py`

- Routed symbols: 3
- Cross-module imports: `config/constants.py`: `CODE_IMPORT_WORKER_COUNT`, `CODE_LIBRARY_IGNORED_DIRS`, `CODE_PARSE_TIMEOUT_SECONDS`, `RAG_IMPORT_WORKER_COUNT`, `RAG_MAX_IMPORT_BATCH_ITEMS`, `RAG_MAX_IMPORT_FILES`, `RAG_MODEL_MEDIA_MAX_BYTES`, `RAG_PARSE_TIMEOUT_SECONDS`, `RAG_PDF_IMAGE_LIMIT`; `config/settings.py`: `default_multimodal_capabilities`; `rag/parsers.py`: `CodeContentParser`, `RAGContentParser`, `_rag_extract_entities`, `_rag_safe_name`; `rag/store.py`: `CodeLibraryStore`, `RAGLibraryStore`; `session/state.py`: `SessionState`; `utils/files.py`: `try_read_text`; `utils/json_utils.py`: `_read_json_file`, `_write_json_file`, `parse_json_object`; `utils/media.py`: `guess_mime_from_name`; `utils/misc.py`: `make_id`, `now_ts`; `utils/text.py`: `trim`
- Symbols:
  - `_rag_parse_file_worker` (function, lines 47709-47723)
  - `RAGIngestionService` (class, lines 47726-48593)
  - `CodeIngestionService` (class, lines 49277-49361)

### `rag/parsers.py`

- Routed symbols: 22
- Cross-module imports: `config/constants.py`: `AUDIO_EXTS`, `CODE_CHUNK_CHARS`, `CODE_CHUNK_OVERLAP`, `CODE_LIBRARY_LANGUAGE_BY_EXT`, `CODE_LIBRARY_SPECIAL_FILENAMES`, `CODE_MAX_CHUNKS_PER_DOC`, `CODE_PREVIEW_EXTS`, `CODE_PREVIEW_FILENAMES`, `CODE_PREVIEW_STAGE_MAX_ROWS`, `DOCUMENT_PREVIEW_EXTS`, `EXCEL_PREVIEW_EXTS`, `IMAGE_EXTS`, `PRESENTATION_PREVIEW_EXTS`, `RAG_CHUNK_CHARS`, `RAG_CHUNK_OVERLAP`, `RAG_CODE_HINTS`, `RAG_EN_STOPWORDS`, `RAG_GENERIC_ENTITY_TERMS_EN`, `RAG_GENERIC_ENTITY_TERMS_ZH`, `RAG_INCLUDE_FILENAME_ENTITIES_DEFAULT`, `RAG_MAX_CHUNKS_PER_DOC`, `RAG_PDF_IMAGE_LIMIT`, `RAG_RESEARCH_HINTS`, `RAG_SHORT_TOKEN_ALLOWLIST`, `RAG_STRUCTURAL_ENTITY_PATTERNS`, `RAG_TERM_GROUPS`, `RAG_ZH_STOPWORDS`, `TABULAR_PREVIEW_EXTS`, `VIDEO_EXTS`; `utils/files.py`: `_sha256_bytes`, `_sha256_file`; `utils/json_utils.py`: `parse_json_object`; `utils/media.py`: `guess_mime_from_name`; `utils/text.py`: `_compress_rows_keep_hotspot`, `_skip_row`, `trim`
- Symbols:
  - `normalize_rel_preview_path` (function, lines 5296-5307)
  - `is_code_preview_candidate` (function, lines 5310-5318)
  - `preview_kind_for_path` (function, lines 5327-5354)
  - `build_code_preview_rows` (function, lines 5357-5541)
  - `_rag_safe_name` (function, lines 44367-44370)
  - `_rag_detect_language` (function, lines 44373-44387)
  - `_rag_cjk_ngrams` (function, lines 44390-44402)
  - `_rag_is_noise_token` (function, lines 44405-44424)
  - `_rag_entity_allowed` (function, lines 44427-44439)
  - `_rag_filter_entities` (function, lines 44442-44456)
  - `_rag_filename_entity_aliases` (function, lines 44459-44492)
  - `_rag_apply_filename_entity_policy` (function, lines 44495-44525)
  - `_rag_choose_community` (function, lines 44528-44545)
  - `_rag_tokenize` (function, lines 44548-44578)
  - `_rag_expand_tokens` (function, lines 44581-44595)
  - `_rag_extract_entities` (function, lines 44598-44614)
  - `_rag_classify_document` (function, lines 44617-44651)
  - `_rag_chunk_text` (function, lines 44654-44684)
  - `_code_language_from_name` (function, lines 44759-44775)
  - `_code_is_test_path` (function, lines 44778-44780)
  - `CodeContentParser` (class, lines 44825-45285)
  - `RAGContentParser` (class, lines 45288-45795)

### `rag/store.py`

- Routed symbols: 2
- Cross-module imports: `config/constants.py`: `CODE_CHUNK_CHARS`, `CODE_CHUNK_OVERLAP`, `CODE_MAX_CHUNKS_PER_DOC`, `RAG_INCLUDE_FILENAME_ENTITIES_DEFAULT`, `RAG_TASK_HISTORY_LIMIT`; `rag/index.py`: `CodeGraphIndex`, `TFGraphIDFIndex`, `_code_choose_community`, `_code_module_name`; `rag/parsers.py`: `_code_is_test_path`, `_rag_apply_filename_entity_policy`, `_rag_choose_community`, `_rag_chunk_text`, `_rag_entity_allowed`, `_rag_extract_entities`, `_rag_safe_name`; `utils/files.py`: `_sha256_bytes`, `_sha256_file`; `utils/json_utils.py`: `_read_json_file`, `_write_json_file`; `utils/media.py`: `guess_mime_from_name`; `utils/misc.py`: `make_id`, `now_ts`; `utils/text.py`: `trim`
- Symbols:
  - `RAGLibraryStore` (class, lines 47159-47706)
  - `CodeLibraryStore` (class, lines 49011-49274)

### `server/handlers.py`

- Routed symbols: 5
- Cross-module imports: `app/context.py`: `AppContext`; `config/constants.py`: `APP_VERSION`, `DEFAULT_REQUEST_TIMEOUT`, `DEFAULT_SHELL_COMMAND_TIMEOUT_SECONDS`, `DEFAULT_UI_LANGUAGE`, `DEFAULT_UI_STYLE`, `EXECUTION_MODE_CHOICES`, `EXECUTION_MODE_SYNC`, `MIN_RUN_TIMEOUT_SECONDS`, `PLAN_MODE_USER_CHOICES`, `RAG_GRAPH_MAX_NODES`, `SSE_HEARTBEAT_SECONDS`, `TASK_COMPLEXITY_LEVELS`, `TASK_LEVEL_CHOICES`, `TASK_LEVEL_POLICIES`, `UI_STYLE_LABELS`; `config/paths.py`: `LLM_CONFIG_PATH`, `REPO_ROOT`, `WORKDIR`; `config/settings.py`: `_to_bool_like`, `infer_user_complexity_value`, `looks_like_llm_config`, `normalize_execution_mode`, `normalize_task_complexity`, `normalize_ui_language`, `normalize_ui_style`, `resolve_web_ui_dir_path`, `supported_ui_languages_payload`; `llm/utils.py`: `extract_base_url`, `extract_openai_compat_model_ids`, `list_ollama_models`, `normalize_openai_compat_provider_name`, `openai_compat_model_list_urls`, `openai_compat_probe_headers`; `session/manager.py`: `SessionCreationLimitExceeded`, `SessionManager`; `session/state.py`: `SessionState`; `skills/store.py`: `analyze_skill_building_knowledge`; `utils/files.py`: `safe_path`, `try_read_text`; `utils/http.py`: `urlopen`; `utils/json_utils.py`: `json_dumps`, `parse_json_object`; `utils/media.py`: `guess_mime_from_name`; `utils/misc.py`: `now_ts`, `swallow_benign_socket_error`, `user_id_from_ip`; `utils/text.py`: `trim`
- Symbols:
  - `AgentHTTPServer` (class, lines 53324-53352)
  - `Handler` (class, lines 53354-54213)
  - `SkillsHandler` (class, lines 54215-54411)
  - `RagAdminHandler` (class, lines 54413-54567)
  - `CodeAdminHandler` (class, lines 54570-54724)

### `session/manager.py`

- Routed symbols: 2
- Cross-module imports: `config/constants.py`: `AGENT_MAX_OUTPUT_TOKENS`, `ARBITER_DEFAULT_MAX_TOKENS`, `ARBITER_DEFAULT_TEMPERATURE`, `ARBITER_DEFAULT_TIMEOUT_SECONDS`, `DEFAULT_REQUEST_TIMEOUT`, `DEFAULT_SHELL_COMMAND_TIMEOUT_SECONDS`, `DEFAULT_UI_LANGUAGE`, `EXECUTION_MODE_SYNC`, `MAX_AGENT_ROUNDS`, `MAX_AGENT_ROUNDS_CAP`, `MAX_RUN_SECONDS`, `MAX_RUN_TIMEOUT_SECONDS`, `MAX_SHELL_COMMAND_TIMEOUT_SECONDS`, `MIN_AGENT_ROUNDS`, `MIN_CONTEXT_TOKEN_LIMIT`, `MIN_RUN_TIMEOUT_SECONDS`, `MIN_SHELL_COMMAND_TIMEOUT_SECONDS`, `TOKEN_THRESHOLD`; `config/paths.py`: `LLM_CONFIG_PATH`; `config/settings.py`: `infer_model_multimodal_capabilities`, `merge_multimodal_capabilities`, `normalize_execution_mode`, `normalize_ui_language`, `parse_capability_overrides`, `parse_llm_config_profiles`; `llm/client.py`: `OllamaClient`; `llm/utils.py`: `complete_chat_endpoint`, `extract_base_url`, `is_openai_compat_provider`, `list_ollama_models_cached`, `probe_ollama_environment`; `session/state.py`: `SessionState`; `utils/crypto.py`: `CryptoBox`; `utils/files.py`: `try_read_text`; `utils/json_utils.py`: `parse_json_object`; `utils/misc.py`: `make_id`, `normalize_timeout_seconds`, `now_ts`, `sanitize_profile_id`
- Symbols:
  - `SessionCreationLimitExceeded` (class, lines 2150-2153)
  - `SessionManager` (class, lines 39057-39944)

### `session/state.py`

- Routed symbols: 1
- Cross-module imports: `agent/background.py`: `BackgroundManager`; `agent/bus.py`: `MessageBus`; `agent/events.py`: `EventHub`; `agent/tasks.py`: `TaskManager`; `agent/todo.py`: `TodoManager`; `agent/worktree.py`: `WorktreeManager`; `config/constants.py`: `AGENT_BUBBLE_ROLES`, `AGENT_CTX_LIMIT_TIER0`, `AGENT_CTX_LIMIT_TIER1`, `AGENT_CTX_LIMIT_TIER2`, `AGENT_CTX_LIMIT_TIER3`, `AGENT_MAX_OUTPUT_TOKENS`, `AGENT_MSG_LIMIT_TIER0`, `AGENT_MSG_LIMIT_TIER1`, `AGENT_MSG_LIMIT_TIER2`, `AGENT_MSG_LIMIT_TIER3`, `AGENT_ROLES`, `AGENT_TOOL_ALLOWLIST`, `ARBITER_DEFAULT_MAX_TOKENS`, `ARBITER_DEFAULT_TEMPERATURE`, `ARBITER_DEFAULT_TIMEOUT_SECONDS`, `ARBITER_TRIGGER_MIN_CONTENT_CHARS`, `ARBITER_VALID_PLANNING_STREAK_LIMIT`, `ASSISTANT_MESSAGE_EVENT_MAX_CHARS`, `ASSISTANT_TEXT_PERSIST_MAX_CHARS`, `AUDIO_EXTS`, `AUTO_CONTINUE_BUDGET_DEFAULT`, `BASH_READ_LOOP_THRESHOLD`, `BLACKBOARD_MAX_LOG_ENTRIES`, `BLACKBOARD_MAX_TEXT`, `BLACKBOARD_STATUSES`, `CHECKPOINT_INTERVAL_ROUNDS`, `CHECKPOINT_MAX_COUNT`, `CODE_PREVIEW_STAGE_MAX_BYTES`, `CODE_PREVIEW_STAGE_MAX_PER_FILE`, `CODE_PREVIEW_STAGE_MAX_ROWS`, `CODE_PREVIEW_STAGE_MAX_TOTAL`, `COMPACT_TIER1_ABS`, `COMPACT_TIER1_PCT`, `COMPACT_TIER2_ABS`, `COMPACT_TIER2_PCT`, `COMPACT_TIER3_PCT`, `DANGEROUS_PATTERNS`, `DEEP_RESEARCH_REQUEST_KEYWORDS`, `DEEP_RESEARCH_RETRIEVAL_KEYWORDS`, `DEEP_RESEARCH_TEXT_ONLY_HINT_KEYWORDS`, `DEFAULT_REQUEST_TIMEOUT`, `DEFAULT_SHELL_COMMAND_TIMEOUT_SECONDS`, `DEFAULT_UI_LANGUAGE`, `DEVELOPER_EDIT_STALL_THRESHOLD`, `EMPTY_ACTION_MIN_CONTENT_CHARS`, `EMPTY_ACTION_WAKEUP_RETRY_LIMIT`, `ERROR_CATEGORY_DEFS`, `EXECUTION_MODE_CHOICES`, `EXECUTION_MODE_SEQUENTIAL`, `EXECUTION_MODE_SINGLE`, `EXECUTION_MODE_SYNC`, `EXPLORER_STALL_THRESHOLD`, `FAILURE_LEDGER_MAX_COMPILE_ERRORS`, `FAILURE_LEDGER_MAX_DELEGATIONS`, `FAILURE_LEDGER_MAX_ERRORS`, `FAILURE_LEDGER_MAX_FIXES`, `FAILURE_LEDGER_MAX_STALLS`, `FAILURE_LEDGER_MAX_TOOL_FPS`, `FILE_BUFFER_CONTENT_THRESHOLD`, `FILE_BUFFER_MAX_FILES`, `FINAL_SUMMARY_MIN_CHARS`, `FINAL_SUMMARY_STRICT_MIN_CHARS`, `FUSED_FAULT_BREAK_THRESHOLD`, `HARD_BREAK_RECOVERY_ROUND_THRESHOLD`, `HARD_BREAK_TOOL_ERROR_THRESHOLD`, `HTML_FRONTEND_REQUEST_KEYWORDS`, `IMAGE_EXTS`, `IMAGE_FORMATS_NEED_CONVERSION`, `LIVE_INPUT_DELAY_NORMAL_ROUNDS`, `LIVE_INPUT_DELAY_TOOL_ROUNDS`, `LIVE_INPUT_DELAY_WRITE_ROUNDS`, `LIVE_INPUT_MAX_INJECTIONS`, `LIVE_INPUT_REINJECT_INTERVAL`, `LIVE_INPUT_WEIGHT_BASE_DELAYED`, `LIVE_INPUT_WEIGHT_BASE_NORMAL`, `LIVE_INPUT_WEIGHT_STEP_DELAYED`, `LIVE_INPUT_WEIGHT_STEP_NORMAL`, `LONG_OUTPUT_LISTING_OFFLOAD_CHARS`, `LONG_OUTPUT_MODEL_PAGE_CHARS`, `LONG_OUTPUT_READ_PAGE_LINES`, `LONG_OUTPUT_READ_PAGE_MAX_CHARS`, `LONG_OUTPUT_TEMP_MAX_FILES`, `LONG_OUTPUT_UI_PAGE_CHARS`, `LONG_OUTPUT_UI_PREVIEW_MAX_PAGES`, `MANAGER_CTX_LIMIT_TIER0`, `MANAGER_CTX_LIMIT_TIER1`, `MANAGER_CTX_LIMIT_TIER2`, `MANAGER_CTX_LIMIT_TIER3`, `MANAGER_ROUTE_TARGETS`, `MAX_AGENT_ROUNDS`, `MAX_AGENT_ROUNDS_CAP`, `MAX_CONTEXT_ARCHIVE_SEGMENTS`, `MAX_RUN_SECONDS`, `MAX_RUN_TIMEOUT_SECONDS`, `MAX_SHELL_COMMAND_TIMEOUT_SECONDS`, `MIN_AGENT_ROUNDS`, `MIN_CONTEXT_TOKEN_LIMIT`, `MIN_RUN_TIMEOUT_SECONDS`, `MIN_SHELL_COMMAND_TIMEOUT_SECONDS`, `MODEL_CALL_PROGRESS_DELAY`, `MODEL_CALL_PROGRESS_INTERVAL`, `MODEL_OUTPUT_RETRY_TIMES`, `PERSISTED_ROUTES_MAX`, `PLAN_BUBBLE_MAX_CHARS`, `PLAN_FILE_RELATIVE_PATH`, `PLAN_MESSAGE_EVENT_MAX_CHARS`, `PLAN_MODE_ENABLED_LEVELS`, `PLAN_MODE_EXPLORER_MAX_ROUNDS`, `PLAN_MODE_FORCED_LEVELS`, `PLAN_MODE_MANAGER_SYNTHESIS_MAX_TOKENS`, `PLAN_MODE_MAX_OPTIONS`, `PLAN_MODE_RESEARCH_TOOL_ALLOWLIST`, `PLAN_MODE_SYNTHESIS_MAX_ATTEMPTS`, `PLAN_MODE_USER_CHOICES`, `PLAN_NOTICE_BODY_MAX_CHARS`, `PLAN_STEP_FULL_CONTENT_MAX_CHARS`, `RENDER_FRAME_ACTIVITY_INTERVAL_SECONDS`, `RENDER_FRAME_MAX_B64_CHARS`, `RENDER_FRAME_MAX_LINES`, `RENDER_FRAME_MAX_LINE_POINTS`, `RENDER_FRAME_MAX_POINTS`, `REPEATED_TOOL_LOOP_THRESHOLD`, `RETRY_RUNTIME_HINT_PREFIXES`, `REVIEWER_DEBUG_MODE_MAX_ROUNDS`, `RUNTIME_CONTROL_HINT_PREFIXES`, `SEMANTIC_CONFIDENCE_CHOICES`, `SKILLS_VIRTUAL_PREFIX`, `SKILL_REFRESH_MIN_INTERVAL_SECONDS`, `SKILL_RUNTIME_CACHE_MAX_BYTES`, `SKILL_RUNTIME_CACHE_MAX_ENTRIES`, `STALL_ESCALATION_CONTEXT_MAX_CHARS`, `STALL_ESCALATION_MIN_LEVEL`, `STALL_PLAN_SYNTHESIS_MAX_TOKENS`, `STALL_SEVERITY_DECAY_ON_SUCCESS`, `STALL_SEVERITY_ESCALATION_THRESHOLD`, `STALL_SEVERITY_WEIGHT_BASH_READ_LOOP`, `STALL_SEVERITY_WEIGHT_FAULT`, `STALL_SEVERITY_WEIGHT_RECOVERY_RETRY`, `STALL_SEVERITY_WEIGHT_REPEATED_TOOL`, `STALL_SEVERITY_WEIGHT_WATCHDOG`, `TASK_COMPLEXITY_LEVELS`, `TASK_LEVEL_CHOICES`, `TASK_LEVEL_POLICIES`, `TASK_PHASE_ROUTING`, `TASK_PROFILE_TYPES`, `TASK_SCALE_PREFERENCES`, `THINKING_BUDGET_FORCE_RATIO`, `TOKEN_THRESHOLD`, `TRUNCATION_CONTINUATION_ECHO_CHARS`, `TRUNCATION_CONTINUATION_MAX_PASSES`, `TRUNCATION_CONTINUATION_MAX_TOKENS`, `TRUNCATION_CONTINUATION_TAIL_CHARS`, `TRUNCATION_LIVE_BUFFER_MAX_CHARS`, `TRUNCATION_OVERLAP_SCAN_CHARS`, `TRUNCATION_PAIR_SCAN_CHARS`, `VIDEO_EXTS`, `WATCHDOG_CONTEXT_NEAR_RATIO`, `WATCHDOG_CONTEXT_STALL_THRESHOLD`, `WATCHDOG_INTENT_NO_TOOL_THRESHOLD`, `WATCHDOG_INTENT_NO_TOOL_THRESHOLD_SINGLE`, `WATCHDOG_MAX_DECOMPOSE_STEPS`, `WATCHDOG_REPEAT_NO_TOOL_THRESHOLD`, `WATCHDOG_REPEAT_NO_TOOL_THRESHOLD_SINGLE`, `WATCHDOG_REPEAT_SIMILARITY_THRESHOLD`, `WATCHDOG_STATE_STALL_THRESHOLD`, `WATCHDOG_STEP_MAX_ATTEMPTS`, `_DEFAULT_TOOL_TIMEOUT`, `_SHELL_AUTO_CONFIRM_PATTERNS`, `_TOOL_TIMEOUT_MAP`; `config/paths.py`: `WORKDIR`; `config/settings.py`: `_detect_os_shell_instruction`, `_to_bool_like`, `backend_i18n_text`, `backend_role_label`, `default_multimodal_capabilities`, `infer_model_multimodal_capabilities`, `infer_user_complexity_value`, `looks_like_llm_config`, `max_task_complexity`, `merge_multimodal_capabilities`, `model_language_instruction`, `normalize_execution_mode`, `normalize_task_complexity`, `normalize_ui_language`, `parse_capability_overrides`, `parse_llm_config_profiles`, `task_complexity_at_least`, `task_complexity_rank`; `llm/client.py`: `OllamaClient`, `OllamaError`; `llm/utils.py`: `complete_chat_endpoint`, `extract_base_url`, `is_openai_compat_provider`, `list_loaded_ollama_models`, `list_ollama_models`, `list_ollama_models_cached`, `probe_ollama_environment`, `resolve_ollama_model`, `split_thinking_content`, `strip_thinking_content`, `wake_ollama_model`; `rag/parsers.py`: `build_code_preview_rows`, `is_code_preview_candidate`, `normalize_rel_preview_path`, `preview_kind_for_path`; `skills/store.py`: `SkillStore`, `ensure_runtime_skills`; `utils/compress.py`: `compress_text_blob`, `decompress_text_blob`; `utils/crypto.py`: `CryptoBox`; `utils/errors.py`: `CircuitBreakerTriggered`, `EmptyActionError`; `utils/files.py`: `_normalize_external_js_url`, `_safe_js_filename`, `cache_external_js_url`, `ensure_offline_js_libs`, `is_external_js_src`, `load_offline_js_lib_index`, `match_offline_js_catalog_by_url`, `offline_js_lib_root`, `safe_path`, `try_read_text`; `utils/http.py`: `urlopen`; `utils/json_utils.py`: `TOOLS`, `TOOL_REQUIRED_ARGS`, `canonicalize_tool_name`, `extract_json_object_from_text`, `json_dumps`, `parse_json_object`, `parse_tool_arguments_with_error`, `repair_truncated_json_object`, `tool_def`; `utils/media.py`: `_convert_image_to_safe_format`, `guess_ext_from_mime`, `guess_mime_from_name`; `utils/misc.py`: `MAX_TIMEOUT_SECONDS`, `MIN_TIMEOUT_SECONDS`, `is_benign_socket_error`, `make_id`, `normalize_timeout_seconds`, `now_ts`, `sanitize_profile_id`; `utils/text.py`: `MAX_TOOL_OUTPUT`, `_fmt_export_ts`, `_html_esc`, `_text_to_minimal_pdf`, `extract_todo_rows_from_text`, `filter_runtime_noise_lines`, `make_numbered_diff`, `make_unified_diff`, `normalize_embedded_newlines`, `normalize_work_text`, `parse_front_matter`, `render_numbered_diff_text`, `split_structured_todo_content`, `split_todo_status_text`, `trim`
- Symbols:
  - `SessionState` (class, lines 13115-39055)

### `skills/store.py`

- Routed symbols: 26
- Cross-module imports: `config/constants.py`: `BUILTIN_CLAWHUB_SKILLS_VERSION`, `EMBEDDED_CLAWHUB_SKILLS_ARCHIVE_B64`, `EMBEDDED_SKILLS_ARCHIVE_B64`, `EMBEDDED_SKILLS_ARCHIVE_FILES`, `EMBEDDED_SKILLS_ARCHIVE_SHA256`, `SKILLS_EXTERNAL_MOUNT`, `SKILLS_VIRTUAL_PREFIX`, `SKILL_BODY_COMPACT_THRESHOLD_CHARS`, `SKILL_BODY_PREVIEW_CHARS`, `SKILL_DEFAULT_ATTACHMENT_GLOBS`, `SKILL_INLINE_ATTACHMENT_MAX_CHARS`, `SKILL_INLINE_ATTACHMENT_MAX_FILES`, `SKILL_PROMPT_MAX_CHARS`, `SKILL_PROMPT_MAX_ITEMS`, `SKILL_PROTOCOL_CLAWHUB`, `SKILL_PROTOCOL_HTTP_JSON`, `SKILL_PROTOCOL_LOCAL`, `SKILL_PROTOCOL_SPECS`, `SKILL_REFRESH_MIN_INTERVAL_SECONDS`, `SKILL_RESOURCE_MANIFEST_MAX_ITEMS`; `config/paths.py`: `WORKDIR`; `llm/utils.py`: `_is_http_url`; `utils/files.py`: `_render_offline_js_catalog_md`, `safe_path`, `try_read_text`; `utils/http.py`: `urlopen`; `utils/json_utils.py`: `json_dumps`, `parse_json_object`; `utils/misc.py`: `_meta_string_list`, `_module_exists`, `now_ts`; `utils/text.py`: `parse_front_matter`, `trim`
- Symbols:
  - `ensure_embedded_skills_at_root` (function, lines 6408-6460)
  - `ensure_embedded_skills` (function, lines 6463-6464)
  - `detect_upload_parser_capabilities` (function, lines 6472-6487)
  - `_render_cap_markdown` (function, lines 6489-6503)
  - `_write_text_if_changed` (function, lines 6505-6510)
  - `ensure_generated_document_skills` (function, lines 6512-6600)
  - `ensure_generated_image_coding_feedback_skill` (function, lines 6602-6701)
  - `_skill_knowledge_files` (function, lines 6703-6722)
  - `analyze_skill_building_knowledge` (function, lines 6724-6778)
  - `_sanitize_skill_slug` (function, lines 6780-6782)
  - `_build_skills_gen_skill_content` (function, lines 6784-6815)
  - `ensure_generated_skills_gen_skill` (function, lines 6817-6821)
  - `ensure_generated_execution_recovery_skill` (function, lines 6823-6901)
  - `ensure_generated_systematic_debugging_skill` (function, lines 6903-7175)
  - `ensure_generated_code_engineering_mastery_skill` (function, lines 7177-7295)
  - `ensure_generated_smart_file_navigation_skill` (function, lines 7297-7415)
  - `ensure_generated_html_frontend_report_skills` (function, lines 7417-7624)
  - `ensure_generated_deep_research_skills` (function, lines 7626-7894)
  - `ensure_generated_research_scientific_skills` (function, lines 7896-8532)
  - `ensure_generated_rag_mastery_skills` (function, lines 8538-8834)
  - `ensure_generated_multimodal_comprehension_skills` (function, lines 8840-9529)
  - `ensure_generated_runtime_skills_manifest` (function, lines 9532-9563)
  - `ensure_embedded_clawhub_skills` (function, lines 9814-9851)
  - `ensure_runtime_skills` (function, lines 9853-9868)
  - `_BUILTIN_SKILLS` (assignment, lines 9910-9998)
  - `SkillStore` (class, lines 10000-11294)

### `utils/compress.py`

- Routed symbols: 2
- Cross-module imports: none
- Symbols:
  - `compress_text_blob` (function, lines 3105-3110)
  - `decompress_text_blob` (function, lines 3112-3120)

### `utils/crypto.py`

- Routed symbols: 1
- Cross-module imports: `utils/json_utils.py`: `json_dumps`
- Symbols:
  - `CryptoBox` (class, lines 4700-4817)

### `utils/errors.py`

- Routed symbols: 2
- Cross-module imports: none
- Symbols:
  - `EmptyActionError` (class, lines 3494-3495)
  - `CircuitBreakerTriggered` (class, lines 3498-3499)

### `utils/files.py`

- Routed symbols: 25
- Cross-module imports: `config/constants.py`: `OFFLINE_JS_LIB_CATALOG`, `OFFLINE_JS_LIB_INDEX_FILE`, `OFFLINE_JS_LIB_README_FILE`; `config/paths.py`: `WORKDIR`; `utils/http.py`: `urlopen`; `utils/json_utils.py`: `json_dumps`; `utils/misc.py`: `now_ts`; `utils/text.py`: `trim`
- Symbols:
  - `_normalize_js_lib_asset_ref` (function, lines 1208-1221)
  - `_resolve_js_lib_asset_path` (function, lines 1224-1253)
  - `_discover_extra_js_lib_files` (function, lines 1256-1286)
  - `safe_path` (function, lines 2482-2491)
  - `_safe_js_filename` (function, lines 2493-2500)
  - `_sha256_bytes` (function, lines 2502-2503)
  - `_sha256_file` (function, lines 2505-2513)
  - `_download_http_bytes` (function, lines 2515-2523)
  - `offline_js_lib_root` (function, lines 2525-2526)
  - `_offline_js_entry_relative_path` (function, lines 2528-2532)
  - `_archive_member_relative_path` (function, lines 2534-2543)
  - `_path_size_bytes` (function, lines 2545-2560)
  - `_extract_archive_to_dir` (function, lines 2562-2602)
  - `_package_required_paths` (function, lines 2604-2610)
  - `_package_install_ready` (function, lines 2612-2620)
  - `_postprocess_offline_js_package` (function, lines 2622-2657)
  - `_ensure_offline_js_package` (function, lines 2659-2698)
  - `_render_offline_js_catalog_md` (function, lines 2700-2716)
  - `load_offline_js_lib_index` (function, lines 2718-2727)
  - `ensure_offline_js_libs` (function, lines 2729-2873)
  - `_normalize_external_js_url` (function, lines 2875-2879)
  - `is_external_js_src` (function, lines 2881-2883)
  - `match_offline_js_catalog_by_url` (function, lines 2885-2901)
  - `cache_external_js_url` (function, lines 2903-2935)
  - `try_read_text` (function, lines 5022-5030)

### `utils/http.py`

- Routed symbols: 4
- Cross-module imports: none
- Symbols:
  - `_URL_OPEN_ORIGINAL` (assignment, lines 56-56)
  - `_HTTP_SSL_CONTEXT` (assignment, lines 57-57)
  - `_shared_http_ssl_context` (function, lines 63-78)
  - `urlopen` (function, lines 80-88)

### `utils/json_utils.py`

- Routed symbols: 16
- Cross-module imports: `utils/text.py`: `trim`
- Symbols:
  - `JSON_FSYNC_ENABLED` (constant, lines 137-137)
  - `json_dumps` (function, lines 2454-2455)
  - `parse_tool_arguments` (function, lines 3373-3382)
  - `repair_truncated_json_object` (function, lines 3384-3437)
  - `parse_tool_arguments_with_error` (function, lines 3439-3469)
  - `parse_json_object` (function, lines 3733-3738)
  - `extract_json_object_from_text` (function, lines 3740-3762)
  - `_json_default_copy` (function, lines 5032-5037)
  - `_read_json_file` (function, lines 5039-5059)
  - `_write_json_file` (function, lines 5061-5088)
  - `tool_def` (function, lines 12834-12846)
  - `TOOLS` (constant, lines 12848-13024)
  - `TOOL_REQUIRED_ARGS` (constant, lines 13026-13026)
  - `TOOL_SPEC_BY_NAME` (constant, lines 13027-13027)
  - `TOOL_NAME_FUZZY_MAP` (constant, lines 13039-13039)
  - `canonicalize_tool_name` (function, lines 13057-13068)

### `utils/media.py`

- Routed symbols: 3
- Cross-module imports: none
- Symbols:
  - `guess_mime_from_name` (function, lines 2294-2296)
  - `_convert_image_to_safe_format` (function, lines 2299-2316)
  - `guess_ext_from_mime` (function, lines 2319-2325)

### `utils/misc.py`

- Routed symbols: 19
- Cross-module imports: none
- Symbols:
  - `MIN_TIMEOUT_SECONDS` (constant, lines 209-209)
  - `MAX_TIMEOUT_SECONDS` (constant, lines 210-210)
  - `DEFAULT_TIMEOUT_SECONDS` (constant, lines 211-217)
  - `BENIGN_SOCKET_DEBUG_LOG_ENABLED` (constant, lines 340-346)
  - `BENIGN_SOCKET_LOG_INTERVAL_SECONDS` (constant, lines 347-347)
  - `now_ts` (function, lines 2327-2328)
  - `_benign_socket_log_lock` (assignment, lines 2331-2331)
  - `_benign_socket_log_state` (assignment, lines 2332-2332)
  - `is_benign_socket_error` (function, lines 2350-2368)
  - `_socket_error_code` (function, lines 2371-2380)
  - `_log_benign_socket_error_limited` (function, lines 2383-2417)
  - `swallow_benign_socket_error` (function, lines 2420-2424)
  - `normalize_timeout_seconds` (function, lines 2427-2440)
  - `detect_local_lan_ip` (function, lines 2442-2452)
  - `make_id` (function, lines 2457-2458)
  - `sanitize_profile_id` (function, lines 2460-2462)
  - `user_id_from_ip` (function, lines 4692-4698)
  - `_meta_string_list` (function, lines 5009-5020)
  - `_module_exists` (function, lines 6466-6470)

### `utils/text.py`

- Routed symbols: 22
- Cross-module imports: none
- Symbols:
  - `MAX_TOOL_OUTPUT` (constant, lines 129-129)
  - `SOCKET_NOISE_LINE_PATTERNS` (constant, lines 334-339)
  - `filter_runtime_noise_lines` (function, lines 2335-2347)
  - `trim` (function, lines 2937-2939)
  - `_fmt_export_ts` (function, lines 2942-2950)
  - `_html_esc` (function, lines 2953-2954)
  - `_text_to_minimal_pdf` (function, lines 2957-3103)
  - `normalize_embedded_newlines` (function, lines 3122-3130)
  - `_map_todo_status_token` (function, lines 3133-3148)
  - `split_todo_status_text` (function, lines 3151-3206)
  - `extract_todo_rows_from_text` (function, lines 3209-3276)
  - `infer_todo_status_from_text` (function, lines 3279-3285)
  - `split_structured_todo_content` (function, lines 3288-3341)
  - `normalize_work_text` (function, lines 3344-3371)
  - `parse_front_matter` (function, lines 4819-5006)
  - `make_unified_diff` (function, lines 5090-5107)
  - `_skip_row` (function, lines 5109-5113)
  - `_row_is_hot` (function, lines 5116-5117)
  - `_hotspot_index` (function, lines 5120-5141)
  - `_compress_rows_keep_hotspot` (function, lines 5144-5191)
  - `make_numbered_diff` (function, lines 5194-5279)
  - `render_numbered_diff_text` (function, lines 5281-5293)
