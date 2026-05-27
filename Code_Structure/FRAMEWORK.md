# Code_Structure Framework

## Overview

- Source file: `/Users/Fona/Downloads/Clouds_Coder/Clouds_Coder.py`
- Output directory: `/Users/Fona/Downloads/Clouds_Coder/Code_Structure`
- Generated modules: 30
- Top-level symbols: 601
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
| `config/constants.py` | 346 | `utils/json_utils.py`, `utils/misc.py` |
| `config/paths.py` | 8 | `utils/text.py` |
| `config/settings.py` | 33 | `config/constants.py`, `config/paths.py`, `llm/utils.py`, `skills/store.py`, `utils/http.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` |
| `llm/client.py` | 2 | `config/constants.py`, `config/settings.py`, `llm/utils.py`, `utils/http.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` |
| `llm/utils.py` | 25 | `config/constants.py`, `utils/http.py`, `utils/json_utils.py`, `utils/text.py` |
| `rag/index.py` | 5 | `config/constants.py`, `rag/ingestion.py`, `rag/parsers.py`, `utils/misc.py`, `utils/text.py` |
| `rag/ingestion.py` | 12 | `config/constants.py`, `config/settings.py`, `rag/parsers.py`, `rag/store.py`, `session/state.py`, `utils/files.py`, `utils/json_utils.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py` |
| `rag/parsers.py` | 28 | `config/constants.py`, `rag/ingestion.py`, `utils/files.py`, `utils/json_utils.py`, `utils/media.py`, `utils/text.py` |
| `rag/store.py` | 4 | `config/constants.py`, `rag/index.py`, `rag/ingestion.py`, `rag/parsers.py`, `skills/store.py`, `utils/files.py`, `utils/json_utils.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py` |
| `server/handlers.py` | 5 | `app/context.py`, `config/constants.py`, `config/paths.py`, `config/settings.py`, `llm/utils.py`, `rag/parsers.py`, `session/manager.py`, `session/state.py`, `skills/store.py`, `utils/files.py`, `utils/http.py`, `utils/json_utils.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py` |
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
| `utils/text.py` | 23 | `config/constants.py` |

## Module Details

### `__main__.py`

- Routed symbols: 2
- Cross-module imports: `app/context.py`: `AppContext`; `config/constants.py`: `AGENT_MAX_OUTPUT_TOKENS`, `ARBITER_DEFAULT_MAX_TOKENS`, `ARBITER_DEFAULT_TEMPERATURE`, `ARBITER_DEFAULT_TIMEOUT_SECONDS`, `CODE_ADMIN_PORT_OFFSET`, `DEFAULT_OLLAMA_BASE_URL`, `DEFAULT_OLLAMA_MODEL`, `DEFAULT_SHELL_COMMAND_TIMEOUT_SECONDS`, `DEFAULT_UI_LANGUAGE`, `DEFAULT_UI_STYLE`, `DEFAULT_WEB_UI_CONFIG`, `DEFAULT_WEB_UI_DIR`, `EXECUTION_MODE_SYNC`, `LIVE_INPUT_DELAY_NORMAL_ROUNDS`, `LIVE_INPUT_DELAY_TOOL_ROUNDS`, `LIVE_INPUT_DELAY_WRITE_ROUNDS`, `LIVE_INPUT_MAX_INJECTIONS`, `LIVE_INPUT_REINJECT_INTERVAL`, `LIVE_INPUT_WEIGHT_BASE_DELAYED`, `LIVE_INPUT_WEIGHT_BASE_NORMAL`, `LIVE_INPUT_WEIGHT_STEP_DELAYED`, `LIVE_INPUT_WEIGHT_STEP_NORMAL`, `MAX_AGENT_ROUNDS`, `MAX_AGENT_ROUNDS_CAP`, `MAX_RUN_SECONDS`, `MAX_RUN_TIMEOUT_SECONDS`, `MAX_SHELL_COMMAND_TIMEOUT_SECONDS`, `MIN_AGENT_ROUNDS`, `MIN_CONTEXT_TOKEN_LIMIT`, `MIN_RUN_TIMEOUT_SECONDS`, `MIN_SHELL_COMMAND_TIMEOUT_SECONDS`, `OFFLINE_JS_LIB_CATALOG`, `RAG_ADMIN_PORT_OFFSET`, `RAG_INCLUDE_FILENAME_ENTITIES_DEFAULT`, `TOKEN_THRESHOLD`, `UI_LANGUAGE_LABELS`, `UI_STYLE_LABELS`; `config/paths.py`: `LLM_CONFIG_PATH`, `REPO_ROOT`, `WORKDIR`; `config/settings.py`: `_to_bool_like`, `extract_daily_session_limit_setting`, `extract_js_lib_download_setting`, `extract_shell_command_timeout_setting`, `extract_show_upload_list_setting`, `extract_ui_style_setting`, `load_llm_config_from_source`, `load_web_ui_config_file`, `normalize_execution_mode`, `normalize_ui_language`, `normalize_ui_style`, `parse_llm_config_profiles`, `resolve_optional_file_path`, `resolve_web_ui_dir_path`, `select_preferred_skills_root`; `llm/utils.py`: `list_ollama_models`; `server/handlers.py`: `AgentHTTPServer`, `CodeAdminHandler`, `Handler`, `RagAdminHandler`, `SkillsHandler`; `skills/store.py`: `ensure_embedded_skills_at_root`, `ensure_runtime_skills`; `utils/files.py`: `ensure_offline_js_libs`; `utils/misc.py`: `BENIGN_SOCKET_DEBUG_LOG_ENABLED`, `detect_local_lan_ip`, `normalize_timeout_seconds`, `swallow_benign_socket_error`; `utils/text.py`: `trim`
- Symbols:
  - `main` (function, lines 66467-67448)
  - `_main_guard_67450` (main_guard, lines 67450-67451)

### `agent/background.py`

- Routed symbols: 1
- Cross-module imports: `utils/misc.py`: `make_id`, `now_ts`; `utils/text.py`: `trim`
- Symbols:
  - `BackgroundManager` (class, lines 11558-11638)

### `agent/bus.py`

- Routed symbols: 1
- Cross-module imports: `config/constants.py`: `VALID_MSG_TYPES`; `utils/crypto.py`: `CryptoBox`; `utils/misc.py`: `now_ts`
- Symbols:
  - `MessageBus` (class, lines 11640-11704)

### `agent/events.py`

- Routed symbols: 1
- Cross-module imports: none
- Symbols:
  - `EventHub` (class, lines 5659-5704)

### `agent/tasks.py`

- Routed symbols: 1
- Cross-module imports: `utils/crypto.py`: `CryptoBox`; `utils/json_utils.py`: `json_dumps`; `utils/misc.py`: `now_ts`
- Symbols:
  - `TaskManager` (class, lines 11430-11556)

### `agent/todo.py`

- Routed symbols: 1
- Cross-module imports: `config/constants.py`: `DEFAULT_UI_LANGUAGE`; `config/settings.py`: `backend_i18n_text`, `backend_role_label`, `normalize_ui_language`; `utils/text.py`: `infer_todo_status_from_text`, `normalize_work_text`, `split_structured_todo_content`, `trim`
- Symbols:
  - `TodoManager` (class, lines 5706-5975)

### `agent/worktree.py`

- Routed symbols: 1
- Cross-module imports: `agent/tasks.py`: `TaskManager`; `config/constants.py`: `DANGEROUS_PATTERNS`; `utils/crypto.py`: `CryptoBox`; `utils/json_utils.py`: `json_dumps`; `utils/misc.py`: `now_ts`; `utils/text.py`: `trim`
- Symbols:
  - `WorktreeManager` (class, lines 11706-11921)

### `app/context.py`

- Routed symbols: 1
- Cross-module imports: `config/constants.py`: `AGENT_MAX_OUTPUT_TOKENS`, `APP_CSS`, `APP_JS`, `APP_TS`, `ARBITER_DEFAULT_MAX_TOKENS`, `ARBITER_DEFAULT_TEMPERATURE`, `ARBITER_DEFAULT_TIMEOUT_SECONDS`, `CODE_ADMIN_CSS`, `CODE_ADMIN_INDEX_HTML`, `CODE_ADMIN_JS`, `CODE_IMPORT_WORKER_COUNT`, `CODE_LIBRARY_DIRNAME`, `CODE_PARSE_TIMEOUT_SECONDS`, `DEFAULT_REQUEST_TIMEOUT`, `DEFAULT_SHELL_COMMAND_TIMEOUT_SECONDS`, `DEFAULT_UI_LANGUAGE`, `DEFAULT_UI_STYLE`, `DEFAULT_WEB_UI_DIR`, `EXECUTION_MODE_SYNC`, `INDEX_HTML`, `MAX_AGENT_ROUNDS`, `MAX_AGENT_ROUNDS_CAP`, `MAX_RUN_SECONDS`, `MAX_RUN_TIMEOUT_SECONDS`, `MAX_SHELL_COMMAND_TIMEOUT_SECONDS`, `MIN_AGENT_ROUNDS`, `MIN_CONTEXT_TOKEN_LIMIT`, `MIN_RUN_TIMEOUT_SECONDS`, `MIN_SHELL_COMMAND_TIMEOUT_SECONDS`, `RAG_ADMIN_CSS`, `RAG_ADMIN_INDEX_HTML`, `RAG_ADMIN_JS`, `RAG_CONTEXT_BUDGETS`, `RAG_DENSE_DEFAULT_ENABLED`, `RAG_EMBEDDING_MODE_VALUES`, `RAG_GRAPH_MAX_NODES`, `RAG_HIGH_RECALL_MIN_POOL`, `RAG_HIGH_RECALL_POOL_MULTIPLIER`, `RAG_IMPORT_WORKER_COUNT`, `RAG_INCLUDE_FILENAME_ENTITIES_DEFAULT`, `RAG_LIBRARY_DIRNAME`, `RAG_MAX_GLOBAL_COMMUNITIES`, `RAG_MAX_IMPORT_BATCH_BYTES`, `RAG_MAX_IMPORT_BATCH_ITEMS`, `RAG_MAX_IMPORT_FILES`, `RAG_MAX_QUERY_RESULTS`, `RAG_MIN_SYNTHESIS_SCORE`, `RAG_NO_EVIDENCE_MESSAGE`, `RAG_NO_EVIDENCE_THRESHOLD`, `RAG_PARSE_TIMEOUT_SECONDS`, `RAG_QUERY_CONTEXT_CHARS`, `RAG_RETRIEVAL_MAX_PER_DOC`, `RAG_SYNTHESIS_MAX_PER_DOC`, `RAG_WEAK_EVIDENCE_MESSAGE`, `RAG_WEAK_MATCH_SCORE_CAP`, `SESSION_HEARTBEAT_STALE_SECONDS`, `SESSION_WATCHDOG_INTERVAL_SECONDS`, `SKILLS_APP_JS`, `SKILLS_EXTRA_CSS`, `SKILLS_INDEX_HTML`, `SKILL_REFRESH_MIN_INTERVAL_SECONDS`, `TOKEN_THRESHOLD`, `WEB_UI_OPTIONAL_FILES`, `WEB_UI_REQUIRED_FILES`; `config/paths.py`: `LLM_CONFIG_PATH`, `REPO_ROOT`, `_migrate_legacy_runtime_roots`; `config/settings.py`: `_to_bool_like`, `default_multimodal_capabilities`, `infer_model_multimodal_capabilities`, `merge_multimodal_capabilities`, `model_language_instruction`, `normalize_execution_mode`, `normalize_ui_language`, `normalize_ui_style`, `parse_capability_overrides`, `parse_llm_config_profiles`, `resolve_optional_file_path`, `resolve_web_ui_dir_path`; `llm/client.py`: `OllamaClient`; `llm/utils.py`: `extract_base_url`, `list_ollama_models_cached`; `rag/ingestion.py`: `CodeIngestionService`, `RAGIngestionService`, `_rag_embed_batch`, `_rag_embed_text`, `_rag_mmr_select`, `_rag_query_variants`; `rag/parsers.py`: `CodeContentParser`, `RAGContentParser`; `rag/store.py`: `CodeLibraryStore`, `RAGLibraryStore`, `WikiStore`, `WorkflowMemoryStore`; `session/manager.py`: `SessionCreationLimitExceeded`, `SessionManager`; `session/state.py`: `SessionState`; `skills/store.py`: `SkillStore`, `_sanitize_skill_slug`, `analyze_skill_building_knowledge`, `ensure_runtime_skills`; `utils/crypto.py`: `CryptoBox`; `utils/files.py`: `_resolve_js_lib_asset_path`, `ensure_offline_js_libs`, `load_offline_js_lib_index`, `offline_js_lib_root`, `safe_path`, `try_read_text`; `utils/json_utils.py`: `TOOLS`, `extract_json_object_from_text`, `json_dumps`, `parse_json_object`; `utils/misc.py`: `DEFAULT_TIMEOUT_SECONDS`, `MAX_TIMEOUT_SECONDS`, `MIN_TIMEOUT_SECONDS`, `normalize_timeout_seconds`, `now_ts`, `sanitize_profile_id`; `utils/text.py`: `parse_front_matter`, `trim`
- Symbols:
  - `AppContext` (class, lines 61592-64955)

### `config/constants.py`

- Routed symbols: 346
- Cross-module imports: `utils/json_utils.py`: `TOOL_SPEC_BY_NAME`; `utils/misc.py`: `DEFAULT_TIMEOUT_SECONDS`
- Symbols:
  - `APP_VERSION` (constant, lines 59-59)
  - `DEFAULT_OLLAMA_BASE_URL` (constant, lines 60-60)
  - `DEFAULT_OLLAMA_MODEL` (constant, lines 61-61)
  - `LONG_OUTPUT_MODEL_PAGE_CHARS` (constant, lines 138-138)
  - `LONG_OUTPUT_UI_PAGE_CHARS` (constant, lines 139-139)
  - `LONG_OUTPUT_UI_PREVIEW_MAX_PAGES` (constant, lines 140-140)
  - `LONG_OUTPUT_LISTING_OFFLOAD_CHARS` (constant, lines 141-141)
  - `LONG_OUTPUT_READ_PAGE_LINES` (constant, lines 142-142)
  - `LONG_OUTPUT_READ_PAGE_MAX_CHARS` (constant, lines 143-143)
  - `LONG_OUTPUT_TEMP_MAX_FILES` (constant, lines 144-144)
  - `READ_FILE_DEFAULT_MAX_CHARS` (constant, lines 145-145)
  - `READ_FILE_HARD_MAX_CHARS` (constant, lines 146-146)
  - `READ_FILE_OVERVIEW_HEAD_LINES` (constant, lines 147-147)
  - `READ_FILE_SEARCH_MAX_MATCHES` (constant, lines 148-148)
  - `RAG_LIBRARY_DIRNAME` (constant, lines 150-150)
  - `RAG_ADMIN_PORT_OFFSET` (constant, lines 151-151)
  - `CODE_LIBRARY_DIRNAME` (constant, lines 152-152)
  - `CODE_ADMIN_PORT_OFFSET` (constant, lines 153-153)
  - `RAG_CHUNK_CHARS` (constant, lines 154-154)
  - `RAG_CHUNK_OVERLAP` (constant, lines 155-155)
  - `RAG_MAX_CHUNKS_PER_DOC` (constant, lines 156-156)
  - `CODE_CHUNK_CHARS` (constant, lines 157-157)
  - `CODE_CHUNK_OVERLAP` (constant, lines 158-158)
  - `CODE_MAX_CHUNKS_PER_DOC` (constant, lines 159-159)
  - `RAG_MAX_QUERY_RESULTS` (constant, lines 160-160)
  - `RAG_HIGH_RECALL_POOL_MULTIPLIER` (constant, lines 161-161)
  - `RAG_HIGH_RECALL_MIN_POOL` (constant, lines 162-162)
  - `RAG_RETRIEVAL_MAX_PER_DOC` (constant, lines 163-163)
  - `RAG_GRAPH_MAX_NODES` (constant, lines 164-164)
  - `RAG_TASK_HISTORY_LIMIT` (constant, lines 165-165)
  - `RAG_MODEL_MEDIA_MAX_BYTES` (constant, lines 166-166)
  - `RAG_MAX_IMPORT_FILES` (constant, lines 167-167)
  - `RAG_MAX_IMPORT_BATCH_ITEMS` (constant, lines 168-168)
  - `RAG_MAX_IMPORT_BATCH_BYTES` (constant, lines 169-169)
  - `RAG_PDF_IMAGE_LIMIT` (constant, lines 170-170)
  - `RAG_QUERY_CONTEXT_CHARS` (constant, lines 171-171)
  - `RAG_MAX_GLOBAL_COMMUNITIES` (constant, lines 172-172)
  - `RAG_MAX_COMMUNITY_MAP_SUPPORT` (constant, lines 173-173)
  - `RAG_INCLUDE_FILENAME_ENTITIES_DEFAULT` (constant, lines 174-174)
  - `RAG_DYNAMIC_NOISE_MIN_DOC_FREQ` (constant, lines 175-175)
  - `RAG_DYNAMIC_NOISE_MIN_COMMUNITY_FREQ` (constant, lines 176-176)
  - `RAG_DYNAMIC_NOISE_SOFT_DOC_RATIO` (constant, lines 177-177)
  - `RAG_DYNAMIC_NOISE_HARD_DOC_RATIO` (constant, lines 178-178)
  - `RAG_DYNAMIC_NOISE_SOFT_COMMUNITY_RATIO` (constant, lines 179-179)
  - `RAG_DYNAMIC_NOISE_HARD_COMMUNITY_RATIO` (constant, lines 180-180)
  - `RAG_MIN_SYNTHESIS_SCORE` (constant, lines 181-181)
  - `RAG_NO_EVIDENCE_THRESHOLD` (constant, lines 182-182)
  - `RAG_WEAK_MATCH_SCORE_CAP` (constant, lines 183-183)
  - `RAG_SYNTHESIS_MAX_PER_DOC` (constant, lines 184-184)
  - `RAG_WORKFLOW_ACCEPT_SCORE` (constant, lines 185-185)
  - `RAG_NO_EVIDENCE_MESSAGE` (constant, lines 186-186)
  - `RAG_CONTEXT_BUDGETS` (constant, lines 187-191)
  - `RAG_WEAK_EVIDENCE_MESSAGE` (constant, lines 192-192)
  - `RAG_DENSE_DEFAULT_ENABLED` (constant, lines 193-193)
  - `RAG_EMBEDDING_MODE_VALUES` (constant, lines 194-194)
  - `RAG_IMPORT_WORKER_COUNT` (constant, lines 195-198)
  - `CODE_IMPORT_WORKER_COUNT` (constant, lines 199-202)
  - `RAG_PARSE_TIMEOUT_SECONDS` (constant, lines 203-206)
  - `CODE_PARSE_TIMEOUT_SECONDS` (constant, lines 207-210)
  - `TOKEN_THRESHOLD` (constant, lines 211-211)
  - `CONTEXT_AUTO_COMPACT_RESERVE_RATIO` (constant, lines 212-215)
  - `CONTEXT_ESTIMATE_SAFETY_MULTIPLIER` (constant, lines 216-219)
  - `CONTEXT_USAGE_CALIBRATION_MAX` (constant, lines 220-223)
  - `CONTEXT_ACTUAL_USAGE_RECENT_SECONDS` (constant, lines 224-227)
  - `LARGE_FILE_AUTO_PAGE_BYTES` (constant, lines 228-231)
  - `LARGE_FILE_AUTO_PAGE_LINES` (constant, lines 232-235)
  - `LARGE_SOURCE_UPLOAD_EXCERPT_CHARS` (constant, lines 236-239)
  - `CHAT_UPLOAD_PARSE_QUEUE_MAX` (constant, lines 240-243)
  - `CHAT_UPLOAD_PARSE_TIMEOUT_SECONDS` (constant, lines 244-247)
  - `CHAT_UPLOAD_INLINE_TEXT_BYTES` (constant, lines 248-251)
  - `CHAT_UPLOAD_PARSE_MAX_BYTES` (constant, lines 252-258)
  - `CHAT_UPLOAD_ZIP_ENTRY_MAX_BYTES` (constant, lines 259-265)
  - `CHAT_UPLOAD_TEXT_CONTEXT_CHARS` (constant, lines 266-269)
  - `CHAT_UPLOAD_PROMPT_MAX_FILES` (constant, lines 270-273)
  - `CHAT_UPLOAD_PROMPT_MAX_CHARS` (constant, lines 274-277)
  - `CHAT_UPLOAD_PROMPT_PER_FILE_CHARS` (constant, lines 278-281)
  - `CHAT_UPLOAD_FRONTEND_WAIT_MS` (constant, lines 282-285)
  - `CHAT_UPLOAD_AUTO_LIBRARY_INGEST` (constant, lines 286-289)
  - `CHAT_UPLOAD_INGEST_QUEUE_MAX` (constant, lines 290-293)
  - `SESSION_SUBMIT_LOCK_TIMEOUT_SECONDS` (constant, lines 294-297)
  - `SESSION_DEFERRED_START_QUEUE_MAX` (constant, lines 298-301)
  - `SESSION_WATCHDOG_INTERVAL_SECONDS` (constant, lines 302-305)
  - `SESSION_HEARTBEAT_STALE_SECONDS` (constant, lines 306-309)
  - `SESSION_LIST_DEFAULT_LIMIT` (constant, lines 310-313)
  - `IDLE_TIMEOUT` (constant, lines 314-314)
  - `POLL_INTERVAL` (constant, lines 315-315)
  - `SSE_HEARTBEAT_SECONDS` (constant, lines 316-316)
  - `MODEL_CALL_PROGRESS_DELAY` (constant, lines 317-317)
  - `MODEL_CALL_PROGRESS_INTERVAL` (constant, lines 318-318)
  - `RUN_COMPLETION_SUMMARY_ENABLED` (constant, lines 319-322)
  - `LLM_HTTP_RETRY_MAX_ATTEMPTS` (constant, lines 323-326)
  - `LLM_HTTP_RETRY_DELAY_SECONDS` (constant, lines 327-330)
  - `LLM_HTTP_RETRY_MAX_SECONDS` (constant, lines 331-334)
  - `LLM_HTTP_RETRY_404_ON_VLLM` (constant, lines 335-338)
  - `LLM_HTTP_RETRY_STATUSES` (constant, lines 339-339)
  - `MAX_AGENT_ROUNDS` (constant, lines 340-340)
  - `MIN_AGENT_ROUNDS` (constant, lines 341-341)
  - `MAX_AGENT_ROUNDS_CAP` (constant, lines 342-342)
  - `REPEATED_TOOL_LOOP_THRESHOLD` (constant, lines 343-343)
  - `BASH_READ_LOOP_THRESHOLD` (constant, lines 344-344)
  - `HARD_BREAK_TOOL_ERROR_THRESHOLD` (constant, lines 345-345)
  - `HARD_BREAK_RECOVERY_ROUND_THRESHOLD` (constant, lines 346-346)
  - `FUSED_FAULT_BREAK_THRESHOLD` (constant, lines 347-347)
  - `STALL_SEVERITY_ESCALATION_THRESHOLD` (constant, lines 348-348)
  - `STALL_SEVERITY_WEIGHT_BASH_READ_LOOP` (constant, lines 349-349)
  - `STALL_SEVERITY_WEIGHT_REPEATED_TOOL` (constant, lines 350-350)
  - `STALL_SEVERITY_WEIGHT_FAULT` (constant, lines 351-351)
  - `STALL_SEVERITY_WEIGHT_RECOVERY_RETRY` (constant, lines 352-352)
  - `STALL_SEVERITY_WEIGHT_WATCHDOG` (constant, lines 353-353)
  - `STALL_SEVERITY_DECAY_ON_SUCCESS` (constant, lines 354-354)
  - `STALL_ESCALATION_MIN_LEVEL` (constant, lines 355-355)
  - `STALL_PLAN_SYNTHESIS_MAX_TOKENS` (constant, lines 356-356)
  - `STALL_ESCALATION_CONTEXT_MAX_CHARS` (constant, lines 357-357)
  - `MAX_RUN_SECONDS` (constant, lines 358-358)
  - `MIN_RUN_TIMEOUT_SECONDS` (constant, lines 359-359)
  - `MAX_RUN_TIMEOUT_SECONDS` (constant, lines 360-360)
  - `DEFAULT_REQUEST_TIMEOUT` (constant, lines 370-370)
  - `_SHELL_AUTO_CONFIRM_PATTERNS` (assignment, lines 373-386)
  - `MIN_SHELL_COMMAND_TIMEOUT_SECONDS` (constant, lines 387-387)
  - `MAX_SHELL_COMMAND_TIMEOUT_SECONDS` (constant, lines 388-388)
  - `DEFAULT_SHELL_COMMAND_TIMEOUT_SECONDS` (constant, lines 389-403)
  - `AUTO_CONTINUE_BUDGET_DEFAULT` (constant, lines 404-404)
  - `AGENT_MAX_OUTPUT_TOKENS` (constant, lines 405-405)
  - `OLLAMA_THINKING_TOOL_BUFFER` (constant, lines 406-406)
  - `WATCHDOG_INTENT_NO_TOOL_THRESHOLD` (constant, lines 407-407)
  - `WATCHDOG_REPEAT_NO_TOOL_THRESHOLD` (constant, lines 408-408)
  - `WATCHDOG_INTENT_NO_TOOL_THRESHOLD_SINGLE` (constant, lines 409-409)
  - `WATCHDOG_REPEAT_NO_TOOL_THRESHOLD_SINGLE` (constant, lines 410-410)
  - `WATCHDOG_STATE_STALL_THRESHOLD` (constant, lines 411-411)
  - `WATCHDOG_CONTEXT_STALL_THRESHOLD` (constant, lines 412-412)
  - `WATCHDOG_REPEAT_SIMILARITY_THRESHOLD` (constant, lines 413-413)
  - `WATCHDOG_CONTEXT_NEAR_RATIO` (constant, lines 414-414)
  - `WATCHDOG_MAX_DECOMPOSE_STEPS` (constant, lines 415-415)
  - `WATCHDOG_STEP_MAX_ATTEMPTS` (constant, lines 416-416)
  - `EMPTY_ACTION_MIN_CONTENT_CHARS` (constant, lines 417-417)
  - `EMPTY_ACTION_WAKEUP_RETRY_LIMIT` (constant, lines 418-418)
  - `THINKING_BUDGET_FORCE_RATIO` (constant, lines 419-419)
  - `_TOOL_TIMEOUT_MAP` (assignment, lines 421-437)
  - `_DEFAULT_TOOL_TIMEOUT` (assignment, lines 438-438)
  - `TRUNCATION_CONTINUATION_MAX_PASSES` (constant, lines 439-439)
  - `TRUNCATION_CONTINUATION_MAX_TOKENS` (constant, lines 440-440)
  - `TRUNCATION_CONTINUATION_TAIL_CHARS` (constant, lines 441-441)
  - `TRUNCATION_CONTINUATION_ECHO_CHARS` (constant, lines 442-442)
  - `TRUNCATION_OVERLAP_SCAN_CHARS` (constant, lines 443-443)
  - `TRUNCATION_PAIR_SCAN_CHARS` (constant, lines 444-444)
  - `TRUNCATION_LIVE_BUFFER_MAX_CHARS` (constant, lines 445-445)
  - `MIN_CONTEXT_TOKEN_LIMIT` (constant, lines 446-446)
  - `COMPACT_TIER1_PCT` (constant, lines 448-448)
  - `COMPACT_TIER2_PCT` (constant, lines 449-449)
  - `COMPACT_TIER3_PCT` (constant, lines 450-450)
  - `COMPACT_TIER1_ABS` (constant, lines 452-452)
  - `COMPACT_TIER2_ABS` (constant, lines 453-453)
  - `CONTEXT_COMPACT_INEFFECTIVE_COOLDOWN_SECONDS` (constant, lines 454-460)
  - `FILE_BUFFER_CONTENT_THRESHOLD` (constant, lines 462-462)
  - `FILE_BUFFER_MAX_FILES` (constant, lines 463-463)
  - `AGENT_MSG_LIMIT_TIER0` (constant, lines 465-465)
  - `AGENT_MSG_LIMIT_TIER1` (constant, lines 466-466)
  - `AGENT_MSG_LIMIT_TIER2` (constant, lines 467-467)
  - `AGENT_MSG_LIMIT_TIER3` (constant, lines 468-468)
  - `AGENT_CTX_LIMIT_TIER0` (constant, lines 469-469)
  - `AGENT_CTX_LIMIT_TIER1` (constant, lines 470-470)
  - `AGENT_CTX_LIMIT_TIER2` (constant, lines 471-471)
  - `AGENT_CTX_LIMIT_TIER3` (constant, lines 472-472)
  - `MANAGER_CTX_LIMIT_TIER0` (constant, lines 473-473)
  - `MANAGER_CTX_LIMIT_TIER1` (constant, lines 474-474)
  - `MANAGER_CTX_LIMIT_TIER2` (constant, lines 475-475)
  - `MANAGER_CTX_LIMIT_TIER3` (constant, lines 476-476)
  - `MAX_CONTEXT_ARCHIVE_SEGMENTS` (constant, lines 477-477)
  - `MODEL_OUTPUT_RETRY_TIMES` (constant, lines 478-478)
  - `ARBITER_TRIGGER_MIN_CONTENT_CHARS` (constant, lines 479-479)
  - `ARBITER_VALID_PLANNING_STREAK_LIMIT` (constant, lines 480-480)
  - `ARBITER_DEFAULT_TIMEOUT_SECONDS` (constant, lines 481-481)
  - `ARBITER_DEFAULT_MAX_TOKENS` (constant, lines 482-482)
  - `ARBITER_DEFAULT_TEMPERATURE` (constant, lines 483-483)
  - `LIVE_INPUT_DELAY_WRITE_ROUNDS` (constant, lines 484-484)
  - `LIVE_INPUT_DELAY_TOOL_ROUNDS` (constant, lines 485-485)
  - `LIVE_INPUT_DELAY_NORMAL_ROUNDS` (constant, lines 486-486)
  - `LIVE_INPUT_MAX_INJECTIONS` (constant, lines 487-487)
  - `LIVE_INPUT_REINJECT_INTERVAL` (constant, lines 488-488)
  - `LIVE_INPUT_WEIGHT_BASE_DELAYED` (constant, lines 489-489)
  - `LIVE_INPUT_WEIGHT_BASE_NORMAL` (constant, lines 490-490)
  - `LIVE_INPUT_WEIGHT_STEP_DELAYED` (constant, lines 491-491)
  - `LIVE_INPUT_WEIGHT_STEP_NORMAL` (constant, lines 492-492)
  - `FINAL_SUMMARY_MIN_CHARS` (constant, lines 507-507)
  - `FINAL_SUMMARY_STRICT_MIN_CHARS` (constant, lines 508-508)
  - `RUNTIME_CONTROL_HINT_PREFIXES` (constant, lines 509-526)
  - `RETRY_RUNTIME_HINT_PREFIXES` (constant, lines 527-541)
  - `EXECUTION_MODE_SINGLE` (constant, lines 542-542)
  - `EXECUTION_MODE_SEQUENTIAL` (constant, lines 543-543)
  - `EXECUTION_MODE_SYNC` (constant, lines 544-544)
  - `EXECUTION_MODE_CHOICES` (constant, lines 545-549)
  - `AGENT_ROLES` (constant, lines 550-550)
  - `AGENT_BUBBLE_ROLES` (constant, lines 551-551)
  - `AGENT_ROLE_LABELS` (constant, lines 552-558)
  - `AGENT_ROLE_BUBBLE_COLORS` (constant, lines 559-565)
  - `BLACKBOARD_STATUSES` (constant, lines 566-575)
  - `TASK_COMPLEXITY_LEVELS` (constant, lines 576-576)
  - `TASK_COMPLEXITY_RANKS` (constant, lines 577-582)
  - `TASK_PROFILE_TYPES` (constant, lines 583-589)
  - `TASK_LEVEL_CHOICES` (constant, lines 590-590)
  - `TASK_SCALE_PREFERENCES` (constant, lines 591-591)
  - `SEMANTIC_CONFIDENCE_CHOICES` (constant, lines 592-592)
  - `TASK_LEVEL_POLICIES` (constant, lines 593-639)
  - `MANAGER_ROUTE_TARGETS` (constant, lines 640-640)
  - `BLACKBOARD_MAX_LOG_ENTRIES` (constant, lines 641-641)
  - `BLACKBOARD_MAX_TEXT` (constant, lines 642-642)
  - `SKILL_REFRESH_MIN_INTERVAL_SECONDS` (constant, lines 643-643)
  - `SKILL_PROMPT_MAX_ITEMS` (constant, lines 644-644)
  - `SKILL_PROMPT_MAX_CHARS` (constant, lines 645-645)
  - `SKILL_RUNTIME_CACHE_MAX_ENTRIES` (constant, lines 646-646)
  - `SKILL_RUNTIME_CACHE_MAX_BYTES` (constant, lines 647-647)
  - `AUTO_SKILLS_ROOT_CANDIDATES` (constant, lines 648-648)
  - `SKILL_DEFAULT_ATTACHMENT_GLOBS` (constant, lines 649-679)
  - `SKILL_INLINE_ATTACHMENT_MAX_FILES` (constant, lines 680-680)
  - `SKILL_INLINE_ATTACHMENT_MAX_CHARS` (constant, lines 681-681)
  - `SKILL_RESOURCE_MANIFEST_MAX_ITEMS` (constant, lines 682-682)
  - `SKILL_BODY_COMPACT_THRESHOLD_CHARS` (constant, lines 683-683)
  - `SKILL_BODY_PREVIEW_CHARS` (constant, lines 684-684)
  - `SKILLS_VIRTUAL_PREFIX` (constant, lines 685-685)
  - `SKILLS_EXTERNAL_MOUNT` (constant, lines 686-686)
  - `PLAN_MODE_ENABLED_LEVELS` (constant, lines 687-687)
  - `PLAN_MODE_FORCED_LEVELS` (constant, lines 688-688)
  - `PLAN_MODE_USER_CHOICES` (constant, lines 689-689)
  - `TASK_PHASES` (constant, lines 691-691)
  - `TASK_PHASE_ROUTING` (constant, lines 692-699)
  - `COMPLEXITY_KEYWORDS` (constant, lines 701-706)
  - `USER_COMPLEXITY_SIMPLE_TOKENS` (constant, lines 707-711)
  - `USER_COMPLEXITY_MODERATE_TOKENS` (constant, lines 712-716)
  - `USER_COMPLEXITY_COMPLEX_TOKENS` (constant, lines 717-721)
  - `USER_COMPLEXITY_EXPERT_TOKENS` (constant, lines 722-726)
  - `PLAN_MODE_EXPLORER_MAX_ROUNDS` (constant, lines 727-727)
  - `PLAN_MODE_SYNTHESIS_MAX_ATTEMPTS` (constant, lines 728-728)
  - `REVIEWER_DEBUG_MODE_MAX_ROUNDS` (constant, lines 730-730)
  - `REVIEWER_DEBUG_TOOL_ALLOWLIST` (constant, lines 731-735)
  - `EXPLORER_STALL_THRESHOLD` (constant, lines 736-736)
  - `DEVELOPER_EDIT_STALL_THRESHOLD` (constant, lines 737-737)
  - `PLAN_MODE_MANAGER_SYNTHESIS_MAX_TOKENS` (constant, lines 738-738)
  - `PLAN_MODE_MAX_OPTIONS` (constant, lines 739-739)
  - `PLAN_FILE_RELATIVE_PATH` (constant, lines 740-740)
  - `PLAN_BUBBLE_MAX_CHARS` (constant, lines 741-741)
  - `PLAN_NOTICE_BODY_MAX_CHARS` (constant, lines 742-742)
  - `PLAN_MESSAGE_EVENT_MAX_CHARS` (constant, lines 743-743)
  - `PLAN_STEP_FULL_CONTENT_MAX_CHARS` (constant, lines 744-744)
  - `PLAN_MODE_RESEARCH_TOOL_ALLOWLIST` (constant, lines 745-749)
  - `FAILURE_LEDGER_MAX_FIXES` (constant, lines 750-750)
  - `FAILURE_LEDGER_MAX_COMPILE_ERRORS` (constant, lines 751-751)
  - `FAILURE_LEDGER_MAX_DELEGATIONS` (constant, lines 752-752)
  - `FAILURE_LEDGER_MAX_STALLS` (constant, lines 753-753)
  - `FAILURE_LEDGER_MAX_TOOL_FPS` (constant, lines 754-754)
  - `FAILURE_LEDGER_MAX_ERRORS` (constant, lines 755-755)
  - `ERROR_CATEGORY_DEFS` (constant, lines 758-795)
  - `CHECKPOINT_MAX_COUNT` (constant, lines 796-796)
  - `CHECKPOINT_INTERVAL_ROUNDS` (constant, lines 797-797)
  - `PERSISTED_ROUTES_MAX` (constant, lines 798-798)
  - `HTML_FRONTEND_REQUEST_KEYWORDS` (constant, lines 799-838)
  - `DEEP_RESEARCH_REQUEST_KEYWORDS` (constant, lines 839-861)
  - `DEEP_RESEARCH_RETRIEVAL_KEYWORDS` (constant, lines 862-881)
  - `DEEP_RESEARCH_TEXT_ONLY_HINT_KEYWORDS` (constant, lines 882-899)
  - `DANGEROUS_PATTERNS` (constant, lines 901-901)
  - `VALID_MSG_TYPES` (constant, lines 902-908)
  - `SUPPORTED_UI_LANGUAGES` (constant, lines 910-915)
  - `UI_LANGUAGE_LABELS` (constant, lines 916-916)
  - `DEFAULT_UI_LANGUAGE` (constant, lines 917-917)
  - `UI_STYLE_CHOICES` (constant, lines 918-918)
  - `UI_STYLE_LABELS` (constant, lines 919-919)
  - `DEFAULT_UI_STYLE` (constant, lines 920-920)
  - `DEFAULT_WEB_UI_DIR` (constant, lines 921-921)
  - `DEFAULT_WEB_UI_CONFIG` (constant, lines 922-922)
  - `WEB_UI_REQUIRED_FILES` (constant, lines 923-930)
  - `WEB_UI_OPTIONAL_FILES` (constant, lines 931-931)
  - `IMAGE_EXTS` (constant, lines 933-946)
  - `IMAGE_FORMATS_NEED_CONVERSION` (constant, lines 947-947)
  - `IMAGE_SAFE_FORMATS` (constant, lines 948-948)
  - `AUDIO_EXTS` (constant, lines 949-959)
  - `VIDEO_EXTS` (constant, lines 960-970)
  - `CODE_PREVIEW_STAGE_MAX_BYTES` (constant, lines 971-971)
  - `CODE_PREVIEW_STAGE_MAX_ROWS` (constant, lines 972-972)
  - `CODE_PREVIEW_STAGE_MAX_PER_FILE` (constant, lines 973-973)
  - `CODE_PREVIEW_STAGE_MAX_TOTAL` (constant, lines 974-974)
  - `CODE_PREVIEW_DIFF_CONTEXT_LINES` (constant, lines 975-975)
  - `CODE_PREVIEW_DIFF_MERGE_GAP` (constant, lines 976-976)
  - `PREVIEW_DOWNLOAD_MAX_FILES` (constant, lines 977-977)
  - `PREVIEW_DOWNLOAD_MAX_BYTES` (constant, lines 978-978)
  - `RENDER_FRAME_MAX_B64_CHARS` (constant, lines 979-979)
  - `RENDER_FRAME_MAX_POINTS` (constant, lines 980-980)
  - `RENDER_FRAME_MAX_LINES` (constant, lines 981-981)
  - `RENDER_FRAME_MAX_LINE_POINTS` (constant, lines 982-982)
  - `RENDER_FRAME_ACTIVITY_INTERVAL_SECONDS` (constant, lines 983-983)
  - `RAW_TOOLCALL_TEXT_FILTER_THRESHOLD` (constant, lines 984-984)
  - `ASSISTANT_TEXT_PERSIST_MAX_CHARS` (constant, lines 985-985)
  - `ASSISTANT_MESSAGE_EVENT_MAX_CHARS` (constant, lines 986-986)
  - `CODE_PREVIEW_EXTS` (constant, lines 987-1076)
  - `CODE_PREVIEW_FILENAMES` (constant, lines 1077-1088)
  - `MEDIA_CAPABILITY_KEYS` (constant, lines 1089-1096)
  - `SAMPLE_IMAGE_PNG_B64` (constant, lines 1097-1100)
  - `SAMPLE_AUDIO_WAV_B64` (constant, lines 1101-1103)
  - `SAMPLE_VIDEO_MP4_B64` (constant, lines 1104-1106)
  - `OFFLINE_JS_LIB_CATALOG` (constant, lines 1108-1366)
  - `OFFLINE_JS_LIB_INDEX_FILE` (constant, lines 1367-1367)
  - `OFFLINE_JS_LIB_README_FILE` (constant, lines 1368-1368)
  - `BACKEND_I18N` (constant, lines 1554-1623)
  - `call_backend_i18n_en_update_l1625` (expression, lines 1625-1718)
  - `call_backend_i18n_zh_cn_update_l1719` (expression, lines 1719-1812)
  - `call_backend_i18n_zh_tw_update_l1813` (expression, lines 1813-1906)
  - `call_backend_i18n_ja_update_l1907` (expression, lines 1907-2000)
  - `OPENAI_COMPAT_PROVIDER_NAMES` (constant, lines 4032-4040)
  - `OPENAI_LIKE_PROVIDER_NAMES` (constant, lines 4042-4042)
  - `TABULAR_PREVIEW_EXTS` (constant, lines 5573-5573)
  - `EXCEL_PREVIEW_EXTS` (constant, lines 5574-5574)
  - `PRESENTATION_PREVIEW_EXTS` (constant, lines 5575-5575)
  - `DOCUMENT_PREVIEW_EXTS` (constant, lines 5576-5576)
  - `EMBEDDED_SKILLS_ARCHIVE_B64` (constant, lines 5977-6496)
  - `EMBEDDED_SKILLS_ARCHIVE_SHA256` (constant, lines 6497-6497)
  - `EMBEDDED_SKILLS_ARCHIVE_FILES` (constant, lines 6498-6521)
  - `BUILTIN_CLAWHUB_SKILLS_VERSION` (constant, lines 9678-9678)
  - `EMBEDDED_CLAWHUB_SKILLS_ARCHIVE_B64` (constant, lines 9680-9924)
  - `SKILL_PROTOCOL_LOCAL` (constant, lines 9990-9990)
  - `SKILL_PROTOCOL_CLAWHUB` (constant, lines 9991-9991)
  - `SKILL_PROTOCOL_HTTP_JSON` (constant, lines 9992-9992)
  - `SKILL_PROTOCOL_SPECS` (constant, lines 9994-10025)
  - `AGENT_TOOL_ALLOWLIST` (constant, lines 13753-13796)
  - `INDEX_HTML` (constant, lines 43535-43724)
  - `APP_CSS` (constant, lines 43726-44138)
  - `APP_JS` (constant, lines 44140-47457)
  - `APP_TS` (constant, lines 47459-47486)
  - `SKILLS_INDEX_HTML` (constant, lines 47488-47642)
  - `SKILLS_EXTRA_CSS` (constant, lines 47644-47739)
  - `SKILLS_APP_JS` (constant, lines 47741-47882)
  - `RAG_TERM_GROUPS` (constant, lines 47884-52516)
  - `RAG_RESEARCH_HINTS` (constant, lines 52517-52538)
  - `RAG_CODE_HINTS` (constant, lines 52539-52549)
  - `RAG_SHORT_TOKEN_ALLOWLIST` (constant, lines 52550-52565)
  - `RAG_EN_STOPWORDS` (constant, lines 52566-52638)
  - `RAG_ZH_STOPWORDS` (constant, lines 52639-52675)
  - `RAG_GENERIC_ENTITY_TERMS_EN` (constant, lines 52676-52754)
  - `RAG_GENERIC_ENTITY_TERMS_ZH` (constant, lines 52755-52797)
  - `RAG_STRUCTURAL_ENTITY_PATTERNS` (constant, lines 52798-52816)
  - `CODE_LIBRARY_IGNORED_DIRS` (constant, lines 53509-53514)
  - `CODE_LIBRARY_LANGUAGE_BY_EXT` (constant, lines 53515-53571)
  - `CODE_LIBRARY_SPECIAL_FILENAMES` (constant, lines 53572-53578)
  - `RAG_ADMIN_INDEX_HTML` (constant, lines 59502-59675)
  - `RAG_ADMIN_CSS` (constant, lines 59677-59767)
  - `RAG_ADMIN_JS` (constant, lines 59769-61532)
  - `CODE_ADMIN_INDEX_HTML` (constant, lines 61534-61545)
  - `CODE_ADMIN_CSS` (constant, lines 61546-61576)
  - `CODE_ADMIN_JS` (constant, lines 61577-61581)

### `config/paths.py`

- Routed symbols: 8
- Cross-module imports: `utils/text.py`: `trim`
- Symbols:
  - `SCRIPT_DIR` (constant, lines 62-62)
  - `_resolve_default_agent_workdir` (function, lines 98-102)
  - `_migrate_legacy_runtime_roots` (function, lines 104-132)
  - `WORKDIR` (constant, lines 134-134)
  - `CODES_ROOT` (constant, lines 135-135)
  - `LLM_CONFIG_PATH` (constant, lines 136-136)
  - `detect_repo_root` (function, lines 2627-2641)
  - `REPO_ROOT` (constant, lines 2643-2643)

### `config/settings.py`

- Routed symbols: 33
- Cross-module imports: `config/constants.py`: `AUTO_SKILLS_ROOT_CANDIDATES`, `BACKEND_I18N`, `DEFAULT_REQUEST_TIMEOUT`, `DEFAULT_SHELL_COMMAND_TIMEOUT_SECONDS`, `DEFAULT_UI_LANGUAGE`, `DEFAULT_UI_STYLE`, `DEFAULT_WEB_UI_CONFIG`, `DEFAULT_WEB_UI_DIR`, `EXECUTION_MODE_CHOICES`, `EXECUTION_MODE_SEQUENTIAL`, `EXECUTION_MODE_SINGLE`, `EXECUTION_MODE_SYNC`, `MAX_SHELL_COMMAND_TIMEOUT_SECONDS`, `MEDIA_CAPABILITY_KEYS`, `MIN_SHELL_COMMAND_TIMEOUT_SECONDS`, `SUPPORTED_UI_LANGUAGES`, `TASK_COMPLEXITY_LEVELS`, `TASK_COMPLEXITY_RANKS`, `UI_LANGUAGE_LABELS`, `UI_STYLE_CHOICES`, `USER_COMPLEXITY_COMPLEX_TOKENS`, `USER_COMPLEXITY_EXPERT_TOKENS`, `USER_COMPLEXITY_MODERATE_TOKENS`, `USER_COMPLEXITY_SIMPLE_TOKENS`; `config/paths.py`: `WORKDIR`; `llm/utils.py`: `_is_http_url`, `_resolve_local_path`, `complete_chat_endpoint`, `extract_base_url`, `is_openai_like_provider`, `normalize_openai_compat_provider_name`, `strip_thinking_content`; `skills/store.py`: `ensure_embedded_skills`; `utils/http.py`: `urlopen`; `utils/json_utils.py`: `parse_json_object`; `utils/misc.py`: `MAX_TIMEOUT_SECONDS`, `MIN_TIMEOUT_SECONDS`, `normalize_timeout_seconds`, `sanitize_profile_id`; `utils/text.py`: `trim`
- Symbols:
  - `normalize_ui_language` (function, lines 1452-1474)
  - `normalize_ui_style` (function, lines 1477-1494)
  - `supported_ui_languages_payload` (function, lines 1497-1498)
  - `normalize_execution_mode` (function, lines 1501-1520)
  - `model_language_instruction` (function, lines 1523-1551)
  - `backend_i18n_text` (function, lines 2003-2013)
  - `backend_role_label` (function, lines 2016-2020)
  - `_detect_os_shell_instruction` (function, lines 2023-2062)
  - `resolve_web_ui_dir_path` (function, lines 2064-2071)
  - `resolve_optional_file_path` (function, lines 2074-2081)
  - `resolve_skills_root_path` (function, lines 2084-2091)
  - `_count_skill_markdown_files` (function, lines 2094-2105)
  - `select_preferred_skills_root` (function, lines 2108-2142)
  - `load_web_ui_config_file` (function, lines 2145-2159)
  - `extract_show_upload_list_setting` (function, lines 2162-2176)
  - `extract_ui_style_setting` (function, lines 2179-2193)
  - `extract_js_lib_download_setting` (function, lines 2196-2215)
  - `extract_daily_session_limit_setting` (function, lines 2218-2261)
  - `extract_shell_command_timeout_setting` (function, lines 2264-2310)
  - `default_multimodal_capabilities` (function, lines 2319-2327)
  - `_to_bool_like` (function, lines 2330-2340)
  - `infer_model_multimodal_capabilities` (function, lines 2343-2387)
  - `parse_capability_overrides` (function, lines 2390-2427)
  - `merge_multimodal_capabilities` (function, lines 2430-2437)
  - `parse_media_endpoints` (function, lines 2440-2454)
  - `infer_user_complexity_value` (function, lines 3950-3966)
  - `normalize_task_complexity` (function, lines 3968-3996)
  - `task_complexity_rank` (function, lines 3998-3999)
  - `task_complexity_at_least` (function, lines 4001-4002)
  - `max_task_complexity` (function, lines 4004-4013)
  - `load_llm_config_from_source` (function, lines 4164-4198)
  - `parse_llm_config_profiles` (function, lines 4200-4786)
  - `looks_like_llm_config` (function, lines 4788-4862)

### `llm/client.py`

- Routed symbols: 2
- Cross-module imports: `config/constants.py`: `DEFAULT_REQUEST_TIMEOUT`, `LLM_HTTP_RETRY_404_ON_VLLM`, `LLM_HTTP_RETRY_DELAY_SECONDS`, `LLM_HTTP_RETRY_MAX_ATTEMPTS`, `LLM_HTTP_RETRY_MAX_SECONDS`, `LLM_HTTP_RETRY_STATUSES`, `OLLAMA_THINKING_TOOL_BUFFER`, `SAMPLE_AUDIO_WAV_B64`, `SAMPLE_IMAGE_PNG_B64`, `SAMPLE_VIDEO_MP4_B64`; `config/settings.py`: `default_multimodal_capabilities`, `infer_model_multimodal_capabilities`, `merge_multimodal_capabilities`, `parse_capability_overrides`, `parse_media_endpoints`; `llm/utils.py`: `complete_chat_endpoint`, `is_openai_compat_provider`, `is_openai_like_provider`, `normalize_openai_compat_provider_name`, `split_thinking_content`; `utils/http.py`: `urlopen`; `utils/json_utils.py`: `canonicalize_tool_name`, `json_dumps`, `parse_json_object`, `parse_tool_arguments`, `parse_tool_arguments_with_error`; `utils/misc.py`: `MAX_TIMEOUT_SECONDS`, `MIN_TIMEOUT_SECONDS`, `make_id`, `normalize_timeout_seconds`, `now_ts`; `utils/text.py`: `trim`
- Symbols:
  - `OllamaError` (class, lines 11923-11943)
  - `OllamaClient` (class, lines 11945-13412)

### `llm/utils.py`

- Routed symbols: 25
- Cross-module imports: `config/constants.py`: `OPENAI_COMPAT_PROVIDER_NAMES`, `OPENAI_LIKE_PROVIDER_NAMES`; `utils/http.py`: `urlopen`; `utils/json_utils.py`: `json_dumps`, `parse_json_object`; `utils/text.py`: `trim`
- Symbols:
  - `probe_ollama_environment` (function, lines 3634-3647)
  - `list_ollama_models` (function, lines 3649-3651)
  - `_OLLAMA_TAG_CACHE_LOCK` (assignment, lines 3653-3653)
  - `_OLLAMA_TAG_CACHE` (assignment, lines 3654-3654)
  - `list_ollama_models_cached` (function, lines 3664-3701)
  - `resolve_ollama_model` (function, lines 3703-3713)
  - `infer_thinking_model` (function, lines 3715-3717)
  - `split_thinking_content` (function, lines 3719-3762)
  - `strip_thinking_content` (function, lines 3764-3765)
  - `check_ollama_model_ready` (function, lines 3767-3791)
  - `list_loaded_ollama_models` (function, lines 3793-3806)
  - `wake_ollama_model` (function, lines 3808-3838)
  - `try_pull_ollama_model` (function, lines 3840-3858)
  - `ordered_model_candidates` (function, lines 3860-3878)
  - `pick_working_ollama_model` (function, lines 3880-3896)
  - `extract_base_url` (function, lines 3929-3937)
  - `complete_chat_endpoint` (function, lines 3939-3948)
  - `normalize_openai_compat_provider_name` (function, lines 4015-4030)
  - `is_openai_compat_provider` (function, lines 4044-4045)
  - `is_openai_like_provider` (function, lines 4047-4048)
  - `openai_compat_probe_headers` (function, lines 4050-4061)
  - `openai_compat_model_list_urls` (function, lines 4063-4095)
  - `extract_openai_compat_model_ids` (function, lines 4097-4130)
  - `_is_http_url` (function, lines 4139-4144)
  - `_resolve_local_path` (function, lines 4146-4162)

### `rag/index.py`

- Routed symbols: 5
- Cross-module imports: `config/constants.py`: `RAG_DYNAMIC_NOISE_HARD_COMMUNITY_RATIO`, `RAG_DYNAMIC_NOISE_HARD_DOC_RATIO`, `RAG_DYNAMIC_NOISE_MIN_COMMUNITY_FREQ`, `RAG_DYNAMIC_NOISE_MIN_DOC_FREQ`, `RAG_DYNAMIC_NOISE_SOFT_COMMUNITY_RATIO`, `RAG_DYNAMIC_NOISE_SOFT_DOC_RATIO`, `RAG_EN_STOPWORDS`, `RAG_GRAPH_MAX_NODES`, `RAG_INCLUDE_FILENAME_ENTITIES_DEFAULT`, `RAG_MAX_COMMUNITY_MAP_SUPPORT`, `RAG_MAX_GLOBAL_COMMUNITIES`, `RAG_MAX_QUERY_RESULTS`, `RAG_MIN_SYNTHESIS_SCORE`, `RAG_WEAK_MATCH_SCORE_CAP`; `rag/ingestion.py`: `_rag_focused_excerpt`, `_rag_mmr_select`, `_rag_window_for_query`; `rag/parsers.py`: `_code_is_test_path`, `_rag_apply_filename_entity_policy`, `_rag_choose_community`, `_rag_classify_document`, `_rag_expand_tokens`, `_rag_extract_entities`, `_rag_filter_entities`, `_rag_tokenize`; `utils/misc.py`: `now_ts`; `utils/text.py`: `trim`
- Symbols:
  - `_code_module_name` (function, lines 53605-53619)
  - `_code_choose_community` (function, lines 53622-53629)
  - `_code_query_terms` (function, lines 53632-53644)
  - `TFGraphIDFIndex` (class, lines 54697-56263)
  - `CodeGraphIndex` (class, lines 58681-59146)

### `rag/ingestion.py`

- Routed symbols: 12
- Cross-module imports: `config/constants.py`: `CODE_IMPORT_WORKER_COUNT`, `CODE_LIBRARY_IGNORED_DIRS`, `CODE_PARSE_TIMEOUT_SECONDS`, `RAG_IMPORT_WORKER_COUNT`, `RAG_MAX_IMPORT_BATCH_ITEMS`, `RAG_MAX_IMPORT_FILES`, `RAG_MODEL_MEDIA_MAX_BYTES`, `RAG_PARSE_TIMEOUT_SECONDS`, `RAG_PDF_IMAGE_LIMIT`, `RAG_RETRIEVAL_MAX_PER_DOC`; `config/settings.py`: `default_multimodal_capabilities`; `rag/parsers.py`: `CodeContentParser`, `RAGContentParser`, `_rag_expand_tokens`, `_rag_extract_entities`, `_rag_is_noise_token`, `_rag_safe_name`, `_rag_tokenize`; `rag/store.py`: `CodeLibraryStore`, `RAGLibraryStore`, `WikiStore`; `session/state.py`: `SessionState`; `utils/files.py`: `try_read_text`; `utils/json_utils.py`: `_read_json_file`, `_write_json_file`, `parse_json_object`; `utils/media.py`: `guess_mime_from_name`; `utils/misc.py`: `make_id`, `now_ts`; `utils/text.py`: `trim`
- Symbols:
  - `_rag_trigram_set` (function, lines 53029-53034)
  - `_rag_jaccard_sim` (function, lines 53037-53044)
  - `_rag_mmr_select` (function, lines 53047-53094)
  - `_rag_embed_text` (function, lines 53231-53252)
  - `_rag_embed_batch` (function, lines 53255-53261)
  - `_rag_window_for_query` (function, lines 53264-53276)
  - `_rag_focused_excerpt` (function, lines 53279-53319)
  - `_rag_query_variants` (function, lines 53322-53359)
  - `_rag_parse_segments` (function, lines 53362-53422)
  - `_rag_parse_file_worker` (function, lines 57785-57799)
  - `RAGIngestionService` (class, lines 57802-58678)
  - `CodeIngestionService` (class, lines 59415-59500)

### `rag/parsers.py`

- Routed symbols: 28
- Cross-module imports: `config/constants.py`: `AUDIO_EXTS`, `CODE_CHUNK_CHARS`, `CODE_CHUNK_OVERLAP`, `CODE_LIBRARY_LANGUAGE_BY_EXT`, `CODE_LIBRARY_SPECIAL_FILENAMES`, `CODE_MAX_CHUNKS_PER_DOC`, `CODE_PREVIEW_DIFF_CONTEXT_LINES`, `CODE_PREVIEW_DIFF_MERGE_GAP`, `CODE_PREVIEW_EXTS`, `CODE_PREVIEW_FILENAMES`, `CODE_PREVIEW_STAGE_MAX_ROWS`, `DOCUMENT_PREVIEW_EXTS`, `EXCEL_PREVIEW_EXTS`, `IMAGE_EXTS`, `PRESENTATION_PREVIEW_EXTS`, `RAG_CHUNK_CHARS`, `RAG_CHUNK_OVERLAP`, `RAG_CODE_HINTS`, `RAG_EN_STOPWORDS`, `RAG_GENERIC_ENTITY_TERMS_EN`, `RAG_GENERIC_ENTITY_TERMS_ZH`, `RAG_INCLUDE_FILENAME_ENTITIES_DEFAULT`, `RAG_MAX_CHUNKS_PER_DOC`, `RAG_PDF_IMAGE_LIMIT`, `RAG_RESEARCH_HINTS`, `RAG_SHORT_TOKEN_ALLOWLIST`, `RAG_STRUCTURAL_ENTITY_PATTERNS`, `RAG_TERM_GROUPS`, `RAG_ZH_STOPWORDS`, `TABULAR_PREVIEW_EXTS`, `VIDEO_EXTS`; `rag/ingestion.py`: `_rag_parse_segments`; `utils/files.py`: `_sha256_bytes`, `_sha256_file`; `utils/json_utils.py`: `parse_json_object`; `utils/media.py`: `guess_mime_from_name`; `utils/text.py`: `_focused_diff_rows_from_opcodes`, `_skip_row`, `trim`
- Symbols:
  - `normalize_rel_preview_path` (function, lines 5548-5559)
  - `is_code_preview_candidate` (function, lines 5562-5570)
  - `preview_kind_for_path` (function, lines 5579-5608)
  - `build_code_preview_rows` (function, lines 5611-5657)
  - `_rag_safe_name` (function, lines 52828-52831)
  - `_rag_detect_language` (function, lines 52834-52848)
  - `_rag_cjk_ngrams` (function, lines 52851-52863)
  - `_rag_is_noise_token` (function, lines 52866-52885)
  - `_rag_entity_allowed` (function, lines 52888-52900)
  - `_rag_filter_entities` (function, lines 52903-52917)
  - `_rag_filename_entity_aliases` (function, lines 52920-52953)
  - `_rag_apply_filename_entity_policy` (function, lines 52956-52986)
  - `_rag_choose_community` (function, lines 52989-53026)
  - `_rag_tokenize` (function, lines 53097-53148)
  - `_rag_expand_tokens` (function, lines 53151-53172)
  - `_rag_extract_entities` (function, lines 53175-53191)
  - `_rag_classify_document` (function, lines 53194-53228)
  - `_rag_chunk_text` (function, lines 53425-53504)
  - `_code_language_from_name` (function, lines 53581-53597)
  - `_code_is_test_path` (function, lines 53600-53602)
  - `_CallCollector` (class, lines 53647-53659)
  - `_ALGO_COMPLEXITY_RE` (assignment, lines 53662-53662)
  - `_ALGO_STEP_RE` (assignment, lines 53663-53663)
  - `_ALGO_MATH_VARS` (assignment, lines 53664-53664)
  - `_ALGO_DOC_KEYWORDS` (assignment, lines 53665-53665)
  - `_detect_algo_chunk` (function, lines 53668-53691)
  - `CodeContentParser` (class, lines 53694-54184)
  - `RAGContentParser` (class, lines 54187-54694)

### `rag/store.py`

- Routed symbols: 4
- Cross-module imports: `config/constants.py`: `CODE_CHUNK_CHARS`, `CODE_CHUNK_OVERLAP`, `CODE_MAX_CHUNKS_PER_DOC`, `RAG_INCLUDE_FILENAME_ENTITIES_DEFAULT`, `RAG_MAX_QUERY_RESULTS`, `RAG_RETRIEVAL_MAX_PER_DOC`, `RAG_TASK_HISTORY_LIMIT`, `RAG_WEAK_MATCH_SCORE_CAP`, `RAG_WORKFLOW_ACCEPT_SCORE`; `rag/index.py`: `CodeGraphIndex`, `TFGraphIDFIndex`, `_code_choose_community`, `_code_module_name`; `rag/ingestion.py`: `_rag_focused_excerpt`, `_rag_mmr_select`, `_rag_window_for_query`; `rag/parsers.py`: `_code_is_test_path`, `_rag_apply_filename_entity_policy`, `_rag_choose_community`, `_rag_chunk_text`, `_rag_entity_allowed`, `_rag_expand_tokens`, `_rag_extract_entities`, `_rag_filter_entities`, `_rag_safe_name`, `_rag_tokenize`; `skills/store.py`: `_write_text_if_changed`; `utils/files.py`: `_sha256_bytes`, `_sha256_file`, `try_read_text`; `utils/json_utils.py`: `_read_json_file`, `_write_json_file`, `json_dumps`; `utils/media.py`: `guess_mime_from_name`; `utils/misc.py`: `make_id`, `now_ts`; `utils/text.py`: `trim`
- Symbols:
  - `RAGLibraryStore` (class, lines 56275-56849)
  - `WikiStore` (class, lines 56852-57381)
  - `WorkflowMemoryStore` (class, lines 57384-57782)
  - `CodeLibraryStore` (class, lines 59149-59412)

### `server/handlers.py`

- Routed symbols: 5
- Cross-module imports: `app/context.py`: `AppContext`; `config/constants.py`: `APP_VERSION`, `DEFAULT_REQUEST_TIMEOUT`, `DEFAULT_SHELL_COMMAND_TIMEOUT_SECONDS`, `DEFAULT_UI_LANGUAGE`, `DEFAULT_UI_STYLE`, `EXECUTION_MODE_CHOICES`, `EXECUTION_MODE_SYNC`, `MIN_RUN_TIMEOUT_SECONDS`, `PLAN_MODE_USER_CHOICES`, `RAG_GRAPH_MAX_NODES`, `SESSION_LIST_DEFAULT_LIMIT`, `SSE_HEARTBEAT_SECONDS`, `TASK_COMPLEXITY_LEVELS`, `TASK_LEVEL_CHOICES`, `TASK_LEVEL_POLICIES`, `UI_STYLE_LABELS`; `config/paths.py`: `LLM_CONFIG_PATH`, `REPO_ROOT`, `WORKDIR`; `config/settings.py`: `_to_bool_like`, `infer_user_complexity_value`, `looks_like_llm_config`, `normalize_execution_mode`, `normalize_task_complexity`, `normalize_ui_language`, `normalize_ui_style`, `resolve_web_ui_dir_path`, `supported_ui_languages_payload`; `llm/utils.py`: `extract_base_url`, `extract_openai_compat_model_ids`, `list_ollama_models`, `normalize_openai_compat_provider_name`, `openai_compat_model_list_urls`, `openai_compat_probe_headers`; `rag/parsers.py`: `normalize_rel_preview_path`; `session/manager.py`: `SessionCreationLimitExceeded`, `SessionManager`; `session/state.py`: `SessionState`; `skills/store.py`: `analyze_skill_building_knowledge`; `utils/files.py`: `safe_path`, `try_read_text`; `utils/http.py`: `urlopen`; `utils/json_utils.py`: `json_dumps`, `parse_json_object`; `utils/media.py`: `guess_mime_from_name`; `utils/misc.py`: `now_ts`, `swallow_benign_socket_error`, `user_id_from_ip`; `utils/text.py`: `trim`
- Symbols:
  - `AgentHTTPServer` (class, lines 64966-64994)
  - `Handler` (class, lines 64998-65899)
  - `SkillsHandler` (class, lines 65901-66097)
  - `RagAdminHandler` (class, lines 66099-66267)
  - `CodeAdminHandler` (class, lines 66270-66456)

### `session/manager.py`

- Routed symbols: 2
- Cross-module imports: `config/constants.py`: `AGENT_MAX_OUTPUT_TOKENS`, `ARBITER_DEFAULT_MAX_TOKENS`, `ARBITER_DEFAULT_TEMPERATURE`, `ARBITER_DEFAULT_TIMEOUT_SECONDS`, `DEFAULT_REQUEST_TIMEOUT`, `DEFAULT_SHELL_COMMAND_TIMEOUT_SECONDS`, `DEFAULT_UI_LANGUAGE`, `EXECUTION_MODE_SYNC`, `MAX_AGENT_ROUNDS`, `MAX_AGENT_ROUNDS_CAP`, `MAX_RUN_SECONDS`, `MAX_RUN_TIMEOUT_SECONDS`, `MAX_SHELL_COMMAND_TIMEOUT_SECONDS`, `MIN_AGENT_ROUNDS`, `MIN_CONTEXT_TOKEN_LIMIT`, `MIN_RUN_TIMEOUT_SECONDS`, `MIN_SHELL_COMMAND_TIMEOUT_SECONDS`, `SESSION_LIST_DEFAULT_LIMIT`, `TOKEN_THRESHOLD`; `config/paths.py`: `LLM_CONFIG_PATH`; `config/settings.py`: `infer_model_multimodal_capabilities`, `merge_multimodal_capabilities`, `normalize_execution_mode`, `normalize_ui_language`, `parse_capability_overrides`, `parse_llm_config_profiles`; `llm/client.py`: `OllamaClient`; `llm/utils.py`: `complete_chat_endpoint`, `extract_base_url`, `is_openai_compat_provider`, `list_ollama_models_cached`, `probe_ollama_environment`; `session/state.py`: `SessionState`; `utils/crypto.py`: `CryptoBox`; `utils/files.py`: `try_read_text`; `utils/json_utils.py`: `parse_json_object`; `utils/misc.py`: `make_id`, `normalize_timeout_seconds`, `now_ts`, `sanitize_profile_id`
- Symbols:
  - `SessionCreationLimitExceeded` (class, lines 2313-2316)
  - `SessionManager` (class, lines 42598-43533)

### `session/state.py`

- Routed symbols: 1
- Cross-module imports: `agent/background.py`: `BackgroundManager`; `agent/bus.py`: `MessageBus`; `agent/events.py`: `EventHub`; `agent/tasks.py`: `TaskManager`; `agent/todo.py`: `TodoManager`; `agent/worktree.py`: `WorktreeManager`; `config/constants.py`: `AGENT_BUBBLE_ROLES`, `AGENT_CTX_LIMIT_TIER0`, `AGENT_CTX_LIMIT_TIER1`, `AGENT_CTX_LIMIT_TIER2`, `AGENT_CTX_LIMIT_TIER3`, `AGENT_MAX_OUTPUT_TOKENS`, `AGENT_MSG_LIMIT_TIER0`, `AGENT_MSG_LIMIT_TIER1`, `AGENT_MSG_LIMIT_TIER2`, `AGENT_MSG_LIMIT_TIER3`, `AGENT_ROLES`, `AGENT_TOOL_ALLOWLIST`, `ARBITER_DEFAULT_MAX_TOKENS`, `ARBITER_DEFAULT_TEMPERATURE`, `ARBITER_DEFAULT_TIMEOUT_SECONDS`, `ARBITER_TRIGGER_MIN_CONTENT_CHARS`, `ARBITER_VALID_PLANNING_STREAK_LIMIT`, `ASSISTANT_MESSAGE_EVENT_MAX_CHARS`, `ASSISTANT_TEXT_PERSIST_MAX_CHARS`, `AUDIO_EXTS`, `AUTO_CONTINUE_BUDGET_DEFAULT`, `BASH_READ_LOOP_THRESHOLD`, `BLACKBOARD_MAX_LOG_ENTRIES`, `BLACKBOARD_MAX_TEXT`, `BLACKBOARD_STATUSES`, `CHAT_UPLOAD_AUTO_LIBRARY_INGEST`, `CHAT_UPLOAD_INGEST_QUEUE_MAX`, `CHAT_UPLOAD_INLINE_TEXT_BYTES`, `CHAT_UPLOAD_PARSE_MAX_BYTES`, `CHAT_UPLOAD_PARSE_QUEUE_MAX`, `CHAT_UPLOAD_PARSE_TIMEOUT_SECONDS`, `CHAT_UPLOAD_PROMPT_MAX_CHARS`, `CHAT_UPLOAD_PROMPT_MAX_FILES`, `CHAT_UPLOAD_PROMPT_PER_FILE_CHARS`, `CHAT_UPLOAD_TEXT_CONTEXT_CHARS`, `CHAT_UPLOAD_ZIP_ENTRY_MAX_BYTES`, `CHECKPOINT_INTERVAL_ROUNDS`, `CHECKPOINT_MAX_COUNT`, `CODE_PREVIEW_STAGE_MAX_BYTES`, `CODE_PREVIEW_STAGE_MAX_PER_FILE`, `CODE_PREVIEW_STAGE_MAX_ROWS`, `CODE_PREVIEW_STAGE_MAX_TOTAL`, `COMPACT_TIER1_ABS`, `COMPACT_TIER1_PCT`, `COMPACT_TIER2_ABS`, `COMPACT_TIER2_PCT`, `COMPACT_TIER3_PCT`, `CONTEXT_ACTUAL_USAGE_RECENT_SECONDS`, `CONTEXT_AUTO_COMPACT_RESERVE_RATIO`, `CONTEXT_COMPACT_INEFFECTIVE_COOLDOWN_SECONDS`, `CONTEXT_ESTIMATE_SAFETY_MULTIPLIER`, `CONTEXT_USAGE_CALIBRATION_MAX`, `DANGEROUS_PATTERNS`, `DEEP_RESEARCH_REQUEST_KEYWORDS`, `DEEP_RESEARCH_RETRIEVAL_KEYWORDS`, `DEEP_RESEARCH_TEXT_ONLY_HINT_KEYWORDS`, `DEFAULT_REQUEST_TIMEOUT`, `DEFAULT_SHELL_COMMAND_TIMEOUT_SECONDS`, `DEFAULT_UI_LANGUAGE`, `DEVELOPER_EDIT_STALL_THRESHOLD`, `EMPTY_ACTION_MIN_CONTENT_CHARS`, `EMPTY_ACTION_WAKEUP_RETRY_LIMIT`, `ERROR_CATEGORY_DEFS`, `EXECUTION_MODE_CHOICES`, `EXECUTION_MODE_SEQUENTIAL`, `EXECUTION_MODE_SINGLE`, `EXECUTION_MODE_SYNC`, `EXPLORER_STALL_THRESHOLD`, `FAILURE_LEDGER_MAX_COMPILE_ERRORS`, `FAILURE_LEDGER_MAX_DELEGATIONS`, `FAILURE_LEDGER_MAX_ERRORS`, `FAILURE_LEDGER_MAX_FIXES`, `FAILURE_LEDGER_MAX_STALLS`, `FAILURE_LEDGER_MAX_TOOL_FPS`, `FILE_BUFFER_CONTENT_THRESHOLD`, `FILE_BUFFER_MAX_FILES`, `FINAL_SUMMARY_MIN_CHARS`, `FINAL_SUMMARY_STRICT_MIN_CHARS`, `FUSED_FAULT_BREAK_THRESHOLD`, `HARD_BREAK_RECOVERY_ROUND_THRESHOLD`, `HARD_BREAK_TOOL_ERROR_THRESHOLD`, `HTML_FRONTEND_REQUEST_KEYWORDS`, `IMAGE_EXTS`, `IMAGE_FORMATS_NEED_CONVERSION`, `LARGE_FILE_AUTO_PAGE_BYTES`, `LARGE_FILE_AUTO_PAGE_LINES`, `LARGE_SOURCE_UPLOAD_EXCERPT_CHARS`, `LIVE_INPUT_DELAY_NORMAL_ROUNDS`, `LIVE_INPUT_DELAY_TOOL_ROUNDS`, `LIVE_INPUT_DELAY_WRITE_ROUNDS`, `LIVE_INPUT_MAX_INJECTIONS`, `LIVE_INPUT_REINJECT_INTERVAL`, `LIVE_INPUT_WEIGHT_BASE_DELAYED`, `LIVE_INPUT_WEIGHT_BASE_NORMAL`, `LIVE_INPUT_WEIGHT_STEP_DELAYED`, `LIVE_INPUT_WEIGHT_STEP_NORMAL`, `LONG_OUTPUT_LISTING_OFFLOAD_CHARS`, `LONG_OUTPUT_MODEL_PAGE_CHARS`, `LONG_OUTPUT_READ_PAGE_LINES`, `LONG_OUTPUT_TEMP_MAX_FILES`, `LONG_OUTPUT_UI_PAGE_CHARS`, `LONG_OUTPUT_UI_PREVIEW_MAX_PAGES`, `MANAGER_CTX_LIMIT_TIER0`, `MANAGER_CTX_LIMIT_TIER1`, `MANAGER_CTX_LIMIT_TIER2`, `MANAGER_CTX_LIMIT_TIER3`, `MANAGER_ROUTE_TARGETS`, `MAX_AGENT_ROUNDS`, `MAX_AGENT_ROUNDS_CAP`, `MAX_CONTEXT_ARCHIVE_SEGMENTS`, `MAX_RUN_SECONDS`, `MAX_RUN_TIMEOUT_SECONDS`, `MAX_SHELL_COMMAND_TIMEOUT_SECONDS`, `MIN_AGENT_ROUNDS`, `MIN_CONTEXT_TOKEN_LIMIT`, `MIN_RUN_TIMEOUT_SECONDS`, `MIN_SHELL_COMMAND_TIMEOUT_SECONDS`, `MODEL_CALL_PROGRESS_DELAY`, `MODEL_CALL_PROGRESS_INTERVAL`, `MODEL_OUTPUT_RETRY_TIMES`, `PERSISTED_ROUTES_MAX`, `PLAN_BUBBLE_MAX_CHARS`, `PLAN_FILE_RELATIVE_PATH`, `PLAN_MESSAGE_EVENT_MAX_CHARS`, `PLAN_MODE_ENABLED_LEVELS`, `PLAN_MODE_EXPLORER_MAX_ROUNDS`, `PLAN_MODE_FORCED_LEVELS`, `PLAN_MODE_MANAGER_SYNTHESIS_MAX_TOKENS`, `PLAN_MODE_MAX_OPTIONS`, `PLAN_MODE_RESEARCH_TOOL_ALLOWLIST`, `PLAN_MODE_SYNTHESIS_MAX_ATTEMPTS`, `PLAN_MODE_USER_CHOICES`, `PLAN_NOTICE_BODY_MAX_CHARS`, `PLAN_STEP_FULL_CONTENT_MAX_CHARS`, `PREVIEW_DOWNLOAD_MAX_BYTES`, `PREVIEW_DOWNLOAD_MAX_FILES`, `READ_FILE_DEFAULT_MAX_CHARS`, `READ_FILE_HARD_MAX_CHARS`, `READ_FILE_OVERVIEW_HEAD_LINES`, `READ_FILE_SEARCH_MAX_MATCHES`, `RENDER_FRAME_ACTIVITY_INTERVAL_SECONDS`, `RENDER_FRAME_MAX_B64_CHARS`, `RENDER_FRAME_MAX_LINES`, `RENDER_FRAME_MAX_LINE_POINTS`, `RENDER_FRAME_MAX_POINTS`, `REPEATED_TOOL_LOOP_THRESHOLD`, `RETRY_RUNTIME_HINT_PREFIXES`, `REVIEWER_DEBUG_MODE_MAX_ROUNDS`, `RUNTIME_CONTROL_HINT_PREFIXES`, `RUN_COMPLETION_SUMMARY_ENABLED`, `SEMANTIC_CONFIDENCE_CHOICES`, `SESSION_DEFERRED_START_QUEUE_MAX`, `SESSION_HEARTBEAT_STALE_SECONDS`, `SESSION_SUBMIT_LOCK_TIMEOUT_SECONDS`, `SKILLS_VIRTUAL_PREFIX`, `SKILL_REFRESH_MIN_INTERVAL_SECONDS`, `SKILL_RUNTIME_CACHE_MAX_BYTES`, `SKILL_RUNTIME_CACHE_MAX_ENTRIES`, `STALL_ESCALATION_CONTEXT_MAX_CHARS`, `STALL_ESCALATION_MIN_LEVEL`, `STALL_PLAN_SYNTHESIS_MAX_TOKENS`, `STALL_SEVERITY_DECAY_ON_SUCCESS`, `STALL_SEVERITY_ESCALATION_THRESHOLD`, `STALL_SEVERITY_WEIGHT_BASH_READ_LOOP`, `STALL_SEVERITY_WEIGHT_FAULT`, `STALL_SEVERITY_WEIGHT_RECOVERY_RETRY`, `STALL_SEVERITY_WEIGHT_REPEATED_TOOL`, `STALL_SEVERITY_WEIGHT_WATCHDOG`, `TASK_COMPLEXITY_LEVELS`, `TASK_LEVEL_CHOICES`, `TASK_LEVEL_POLICIES`, `TASK_PHASE_ROUTING`, `TASK_PROFILE_TYPES`, `TASK_SCALE_PREFERENCES`, `THINKING_BUDGET_FORCE_RATIO`, `TOKEN_THRESHOLD`, `TRUNCATION_CONTINUATION_ECHO_CHARS`, `TRUNCATION_CONTINUATION_MAX_PASSES`, `TRUNCATION_CONTINUATION_MAX_TOKENS`, `TRUNCATION_CONTINUATION_TAIL_CHARS`, `TRUNCATION_LIVE_BUFFER_MAX_CHARS`, `TRUNCATION_OVERLAP_SCAN_CHARS`, `TRUNCATION_PAIR_SCAN_CHARS`, `VIDEO_EXTS`, `WATCHDOG_CONTEXT_NEAR_RATIO`, `WATCHDOG_CONTEXT_STALL_THRESHOLD`, `WATCHDOG_INTENT_NO_TOOL_THRESHOLD`, `WATCHDOG_INTENT_NO_TOOL_THRESHOLD_SINGLE`, `WATCHDOG_MAX_DECOMPOSE_STEPS`, `WATCHDOG_REPEAT_NO_TOOL_THRESHOLD`, `WATCHDOG_REPEAT_NO_TOOL_THRESHOLD_SINGLE`, `WATCHDOG_REPEAT_SIMILARITY_THRESHOLD`, `WATCHDOG_STATE_STALL_THRESHOLD`, `WATCHDOG_STEP_MAX_ATTEMPTS`, `_DEFAULT_TOOL_TIMEOUT`, `_SHELL_AUTO_CONFIRM_PATTERNS`, `_TOOL_TIMEOUT_MAP`; `config/paths.py`: `WORKDIR`; `config/settings.py`: `_detect_os_shell_instruction`, `_to_bool_like`, `backend_i18n_text`, `backend_role_label`, `default_multimodal_capabilities`, `infer_model_multimodal_capabilities`, `infer_user_complexity_value`, `looks_like_llm_config`, `max_task_complexity`, `merge_multimodal_capabilities`, `model_language_instruction`, `normalize_execution_mode`, `normalize_task_complexity`, `normalize_ui_language`, `parse_capability_overrides`, `parse_llm_config_profiles`, `task_complexity_at_least`, `task_complexity_rank`; `llm/client.py`: `OllamaClient`, `OllamaError`; `llm/utils.py`: `complete_chat_endpoint`, `extract_base_url`, `is_openai_compat_provider`, `list_loaded_ollama_models`, `list_ollama_models`, `list_ollama_models_cached`, `probe_ollama_environment`, `resolve_ollama_model`, `split_thinking_content`, `strip_thinking_content`, `wake_ollama_model`; `rag/parsers.py`: `CodeContentParser`, `build_code_preview_rows`, `is_code_preview_candidate`, `normalize_rel_preview_path`, `preview_kind_for_path`; `skills/store.py`: `SkillStore`, `ensure_runtime_skills`; `utils/compress.py`: `compress_text_blob`, `decompress_text_blob`; `utils/crypto.py`: `CryptoBox`; `utils/errors.py`: `CircuitBreakerTriggered`, `EmptyActionError`; `utils/files.py`: `_normalize_external_js_url`, `_safe_js_filename`, `cache_external_js_url`, `ensure_offline_js_libs`, `is_external_js_src`, `load_offline_js_lib_index`, `match_offline_js_catalog_by_url`, `offline_js_lib_root`, `safe_path`, `try_read_text`; `utils/http.py`: `urlopen`; `utils/json_utils.py`: `TOOLS`, `TOOL_REQUIRED_ARGS`, `canonicalize_tool_name`, `extract_json_object_from_text`, `json_dumps`, `parse_json_object`, `parse_tool_arguments_with_error`, `repair_truncated_json_object`, `tool_def`; `utils/media.py`: `_convert_image_to_safe_format`, `guess_ext_from_mime`, `guess_mime_from_name`; `utils/misc.py`: `MAX_TIMEOUT_SECONDS`, `MIN_TIMEOUT_SECONDS`, `is_benign_socket_error`, `make_id`, `normalize_timeout_seconds`, `now_ts`, `sanitize_profile_id`; `utils/text.py`: `MAX_TOOL_OUTPUT`, `_fmt_export_ts`, `_html_esc`, `_text_to_minimal_pdf`, `extract_todo_rows_from_text`, `filter_runtime_noise_lines`, `make_numbered_diff`, `make_unified_diff`, `normalize_embedded_newlines`, `normalize_work_text`, `parse_front_matter`, `render_numbered_diff_text`, `split_structured_todo_content`, `split_todo_status_text`, `trim`
- Symbols:
  - `SessionState` (class, lines 13807-42596)

### `skills/store.py`

- Routed symbols: 26
- Cross-module imports: `config/constants.py`: `BUILTIN_CLAWHUB_SKILLS_VERSION`, `EMBEDDED_CLAWHUB_SKILLS_ARCHIVE_B64`, `EMBEDDED_SKILLS_ARCHIVE_B64`, `EMBEDDED_SKILLS_ARCHIVE_FILES`, `EMBEDDED_SKILLS_ARCHIVE_SHA256`, `SKILLS_EXTERNAL_MOUNT`, `SKILLS_VIRTUAL_PREFIX`, `SKILL_BODY_COMPACT_THRESHOLD_CHARS`, `SKILL_BODY_PREVIEW_CHARS`, `SKILL_DEFAULT_ATTACHMENT_GLOBS`, `SKILL_INLINE_ATTACHMENT_MAX_CHARS`, `SKILL_INLINE_ATTACHMENT_MAX_FILES`, `SKILL_PROMPT_MAX_CHARS`, `SKILL_PROMPT_MAX_ITEMS`, `SKILL_PROTOCOL_CLAWHUB`, `SKILL_PROTOCOL_HTTP_JSON`, `SKILL_PROTOCOL_LOCAL`, `SKILL_PROTOCOL_SPECS`, `SKILL_REFRESH_MIN_INTERVAL_SECONDS`, `SKILL_RESOURCE_MANIFEST_MAX_ITEMS`; `config/paths.py`: `WORKDIR`; `llm/utils.py`: `_is_http_url`; `utils/files.py`: `_render_offline_js_catalog_md`, `safe_path`, `try_read_text`; `utils/http.py`: `urlopen`; `utils/json_utils.py`: `json_dumps`, `parse_json_object`; `utils/misc.py`: `_meta_string_list`, `_module_exists`, `now_ts`; `utils/text.py`: `parse_front_matter`, `trim`
- Symbols:
  - `ensure_embedded_skills_at_root` (function, lines 6524-6576)
  - `ensure_embedded_skills` (function, lines 6579-6580)
  - `detect_upload_parser_capabilities` (function, lines 6588-6603)
  - `_render_cap_markdown` (function, lines 6605-6619)
  - `_write_text_if_changed` (function, lines 6621-6626)
  - `ensure_generated_document_skills` (function, lines 6628-6716)
  - `ensure_generated_image_coding_feedback_skill` (function, lines 6718-6817)
  - `_skill_knowledge_files` (function, lines 6819-6838)
  - `analyze_skill_building_knowledge` (function, lines 6840-6894)
  - `_sanitize_skill_slug` (function, lines 6896-6898)
  - `_build_skills_gen_skill_content` (function, lines 6900-6931)
  - `ensure_generated_skills_gen_skill` (function, lines 6933-6937)
  - `ensure_generated_execution_recovery_skill` (function, lines 6939-7017)
  - `ensure_generated_systematic_debugging_skill` (function, lines 7019-7291)
  - `ensure_generated_code_engineering_mastery_skill` (function, lines 7293-7411)
  - `ensure_generated_smart_file_navigation_skill` (function, lines 7413-7528)
  - `ensure_generated_html_frontend_report_skills` (function, lines 7530-7737)
  - `ensure_generated_deep_research_skills` (function, lines 7739-8007)
  - `ensure_generated_research_scientific_skills` (function, lines 8009-8645)
  - `ensure_generated_rag_mastery_skills` (function, lines 8651-8947)
  - `ensure_generated_multimodal_comprehension_skills` (function, lines 8953-9642)
  - `ensure_generated_runtime_skills_manifest` (function, lines 9645-9676)
  - `ensure_embedded_clawhub_skills` (function, lines 9934-9971)
  - `ensure_runtime_skills` (function, lines 9973-9988)
  - `_BUILTIN_SKILLS` (assignment, lines 10030-10118)
  - `SkillStore` (class, lines 10127-11421)

### `utils/compress.py`

- Routed symbols: 2
- Cross-module imports: none
- Symbols:
  - `compress_text_blob` (function, lines 3268-3273)
  - `decompress_text_blob` (function, lines 3275-3283)

### `utils/crypto.py`

- Routed symbols: 1
- Cross-module imports: `utils/json_utils.py`: `json_dumps`
- Symbols:
  - `CryptoBox` (class, lines 4872-4989)

### `utils/errors.py`

- Routed symbols: 2
- Cross-module imports: none
- Symbols:
  - `EmptyActionError` (class, lines 3657-3658)
  - `CircuitBreakerTriggered` (class, lines 3661-3662)

### `utils/files.py`

- Routed symbols: 25
- Cross-module imports: `config/constants.py`: `OFFLINE_JS_LIB_CATALOG`, `OFFLINE_JS_LIB_INDEX_FILE`, `OFFLINE_JS_LIB_README_FILE`; `config/paths.py`: `WORKDIR`; `utils/http.py`: `urlopen`; `utils/json_utils.py`: `json_dumps`; `utils/misc.py`: `now_ts`; `utils/text.py`: `trim`
- Symbols:
  - `_normalize_js_lib_asset_ref` (function, lines 1371-1384)
  - `_resolve_js_lib_asset_path` (function, lines 1387-1416)
  - `_discover_extra_js_lib_files` (function, lines 1419-1449)
  - `safe_path` (function, lines 2645-2654)
  - `_safe_js_filename` (function, lines 2656-2663)
  - `_sha256_bytes` (function, lines 2665-2666)
  - `_sha256_file` (function, lines 2668-2676)
  - `_download_http_bytes` (function, lines 2678-2686)
  - `offline_js_lib_root` (function, lines 2688-2689)
  - `_offline_js_entry_relative_path` (function, lines 2691-2695)
  - `_archive_member_relative_path` (function, lines 2697-2706)
  - `_path_size_bytes` (function, lines 2708-2723)
  - `_extract_archive_to_dir` (function, lines 2725-2765)
  - `_package_required_paths` (function, lines 2767-2773)
  - `_package_install_ready` (function, lines 2775-2783)
  - `_postprocess_offline_js_package` (function, lines 2785-2820)
  - `_ensure_offline_js_package` (function, lines 2822-2861)
  - `_render_offline_js_catalog_md` (function, lines 2863-2879)
  - `load_offline_js_lib_index` (function, lines 2881-2890)
  - `ensure_offline_js_libs` (function, lines 2892-3036)
  - `_normalize_external_js_url` (function, lines 3038-3042)
  - `is_external_js_src` (function, lines 3044-3046)
  - `match_offline_js_catalog_by_url` (function, lines 3048-3064)
  - `cache_external_js_url` (function, lines 3066-3098)
  - `try_read_text` (function, lines 5194-5202)

### `utils/http.py`

- Routed symbols: 4
- Cross-module imports: none
- Symbols:
  - `_URL_OPEN_ORIGINAL` (assignment, lines 57-57)
  - `_HTTP_SSL_CONTEXT` (assignment, lines 58-58)
  - `_shared_http_ssl_context` (function, lines 71-86)
  - `urlopen` (function, lines 88-96)

### `utils/json_utils.py`

- Routed symbols: 16
- Cross-module imports: `utils/text.py`: `trim`
- Symbols:
  - `JSON_FSYNC_ENABLED` (constant, lines 149-149)
  - `json_dumps` (function, lines 2617-2618)
  - `parse_tool_arguments` (function, lines 3536-3545)
  - `repair_truncated_json_object` (function, lines 3547-3600)
  - `parse_tool_arguments_with_error` (function, lines 3602-3632)
  - `parse_json_object` (function, lines 3898-3903)
  - `extract_json_object_from_text` (function, lines 3905-3927)
  - `_json_default_copy` (function, lines 5204-5209)
  - `_read_json_file` (function, lines 5211-5231)
  - `_write_json_file` (function, lines 5233-5260)
  - `tool_def` (function, lines 13414-13426)
  - `TOOLS` (constant, lines 13428-13707)
  - `TOOL_REQUIRED_ARGS` (constant, lines 13709-13709)
  - `TOOL_SPEC_BY_NAME` (constant, lines 13710-13710)
  - `TOOL_NAME_FUZZY_MAP` (constant, lines 13722-13722)
  - `canonicalize_tool_name` (function, lines 13740-13751)

### `utils/media.py`

- Routed symbols: 3
- Cross-module imports: none
- Symbols:
  - `guess_mime_from_name` (function, lines 2457-2459)
  - `_convert_image_to_safe_format` (function, lines 2462-2479)
  - `guess_ext_from_mime` (function, lines 2482-2488)

### `utils/misc.py`

- Routed symbols: 19
- Cross-module imports: none
- Symbols:
  - `MIN_TIMEOUT_SECONDS` (constant, lines 361-361)
  - `MAX_TIMEOUT_SECONDS` (constant, lines 362-362)
  - `DEFAULT_TIMEOUT_SECONDS` (constant, lines 363-369)
  - `BENIGN_SOCKET_DEBUG_LOG_ENABLED` (constant, lines 499-505)
  - `BENIGN_SOCKET_LOG_INTERVAL_SECONDS` (constant, lines 506-506)
  - `now_ts` (function, lines 2490-2491)
  - `_benign_socket_log_lock` (assignment, lines 2494-2494)
  - `_benign_socket_log_state` (assignment, lines 2495-2495)
  - `is_benign_socket_error` (function, lines 2513-2531)
  - `_socket_error_code` (function, lines 2534-2543)
  - `_log_benign_socket_error_limited` (function, lines 2546-2580)
  - `swallow_benign_socket_error` (function, lines 2583-2587)
  - `normalize_timeout_seconds` (function, lines 2590-2603)
  - `detect_local_lan_ip` (function, lines 2605-2615)
  - `make_id` (function, lines 2620-2621)
  - `sanitize_profile_id` (function, lines 2623-2625)
  - `user_id_from_ip` (function, lines 4864-4870)
  - `_meta_string_list` (function, lines 5181-5192)
  - `_module_exists` (function, lines 6582-6586)

### `utils/text.py`

- Routed symbols: 23
- Cross-module imports: `config/constants.py`: `CODE_PREVIEW_DIFF_CONTEXT_LINES`, `CODE_PREVIEW_DIFF_MERGE_GAP`
- Symbols:
  - `MAX_TOOL_OUTPUT` (constant, lines 137-137)
  - `SOCKET_NOISE_LINE_PATTERNS` (constant, lines 493-498)
  - `filter_runtime_noise_lines` (function, lines 2498-2510)
  - `trim` (function, lines 3100-3102)
  - `_fmt_export_ts` (function, lines 3105-3113)
  - `_html_esc` (function, lines 3116-3117)
  - `_text_to_minimal_pdf` (function, lines 3120-3266)
  - `normalize_embedded_newlines` (function, lines 3285-3293)
  - `_map_todo_status_token` (function, lines 3296-3311)
  - `split_todo_status_text` (function, lines 3314-3369)
  - `extract_todo_rows_from_text` (function, lines 3372-3439)
  - `infer_todo_status_from_text` (function, lines 3442-3448)
  - `split_structured_todo_content` (function, lines 3451-3504)
  - `normalize_work_text` (function, lines 3507-3534)
  - `parse_front_matter` (function, lines 4991-5178)
  - `make_unified_diff` (function, lines 5262-5279)
  - `_skip_row` (function, lines 5281-5285)
  - `_row_is_hot` (function, lines 5288-5289)
  - `_hotspot_index` (function, lines 5292-5313)
  - `_compress_rows_keep_hotspot` (function, lines 5316-5363)
  - `_focused_diff_rows_from_opcodes` (function, lines 5366-5498)
  - `make_numbered_diff` (function, lines 5501-5531)
  - `render_numbered_diff_text` (function, lines 5533-5545)
