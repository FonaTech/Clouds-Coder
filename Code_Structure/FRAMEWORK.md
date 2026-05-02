# Code_Structure Framework

## Overview

- Source file: `/Users/Fona/Downloads/Clouds_Coder/Clouds_Coder.py`
- Output directory: `/Users/Fona/Downloads/Clouds_Coder/Code_Structure`
- Generated modules: 30
- Top-level symbols: 596
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
| `config/constants.py` | 341 | `utils/json_utils.py`, `utils/misc.py` |
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
  - `main` (function, lines 64808-65789)
  - `_main_guard_65791` (main_guard, lines 65791-65792)

### `agent/background.py`

- Routed symbols: 1
- Cross-module imports: `utils/misc.py`: `make_id`, `now_ts`; `utils/text.py`: `trim`
- Symbols:
  - `BackgroundManager` (class, lines 11551-11631)

### `agent/bus.py`

- Routed symbols: 1
- Cross-module imports: `config/constants.py`: `VALID_MSG_TYPES`; `utils/crypto.py`: `CryptoBox`; `utils/misc.py`: `now_ts`
- Symbols:
  - `MessageBus` (class, lines 11633-11687)

### `agent/events.py`

- Routed symbols: 1
- Cross-module imports: none
- Symbols:
  - `EventHub` (class, lines 5649-5694)

### `agent/tasks.py`

- Routed symbols: 1
- Cross-module imports: `utils/crypto.py`: `CryptoBox`; `utils/json_utils.py`: `json_dumps`; `utils/misc.py`: `now_ts`
- Symbols:
  - `TaskManager` (class, lines 11423-11549)

### `agent/todo.py`

- Routed symbols: 1
- Cross-module imports: `config/constants.py`: `DEFAULT_UI_LANGUAGE`; `config/settings.py`: `backend_i18n_text`, `backend_role_label`, `normalize_ui_language`; `utils/text.py`: `infer_todo_status_from_text`, `normalize_work_text`, `split_structured_todo_content`, `trim`
- Symbols:
  - `TodoManager` (class, lines 5696-5965)

### `agent/worktree.py`

- Routed symbols: 1
- Cross-module imports: `agent/tasks.py`: `TaskManager`; `config/constants.py`: `DANGEROUS_PATTERNS`; `utils/crypto.py`: `CryptoBox`; `utils/json_utils.py`: `json_dumps`; `utils/misc.py`: `now_ts`; `utils/text.py`: `trim`
- Symbols:
  - `WorktreeManager` (class, lines 11689-11900)

### `app/context.py`

- Routed symbols: 1
- Cross-module imports: `config/constants.py`: `AGENT_MAX_OUTPUT_TOKENS`, `APP_CSS`, `APP_JS`, `APP_TS`, `ARBITER_DEFAULT_MAX_TOKENS`, `ARBITER_DEFAULT_TEMPERATURE`, `ARBITER_DEFAULT_TIMEOUT_SECONDS`, `CODE_ADMIN_CSS`, `CODE_ADMIN_INDEX_HTML`, `CODE_ADMIN_JS`, `CODE_IMPORT_WORKER_COUNT`, `CODE_LIBRARY_DIRNAME`, `CODE_PARSE_TIMEOUT_SECONDS`, `DEFAULT_REQUEST_TIMEOUT`, `DEFAULT_SHELL_COMMAND_TIMEOUT_SECONDS`, `DEFAULT_UI_LANGUAGE`, `DEFAULT_UI_STYLE`, `DEFAULT_WEB_UI_DIR`, `EXECUTION_MODE_SYNC`, `INDEX_HTML`, `MAX_AGENT_ROUNDS`, `MAX_AGENT_ROUNDS_CAP`, `MAX_RUN_SECONDS`, `MAX_RUN_TIMEOUT_SECONDS`, `MAX_SHELL_COMMAND_TIMEOUT_SECONDS`, `MIN_AGENT_ROUNDS`, `MIN_CONTEXT_TOKEN_LIMIT`, `MIN_RUN_TIMEOUT_SECONDS`, `MIN_SHELL_COMMAND_TIMEOUT_SECONDS`, `RAG_ADMIN_CSS`, `RAG_ADMIN_INDEX_HTML`, `RAG_ADMIN_JS`, `RAG_CONTEXT_BUDGETS`, `RAG_DENSE_DEFAULT_ENABLED`, `RAG_EMBEDDING_MODE_VALUES`, `RAG_GRAPH_MAX_NODES`, `RAG_HIGH_RECALL_MIN_POOL`, `RAG_HIGH_RECALL_POOL_MULTIPLIER`, `RAG_IMPORT_WORKER_COUNT`, `RAG_INCLUDE_FILENAME_ENTITIES_DEFAULT`, `RAG_LIBRARY_DIRNAME`, `RAG_MAX_GLOBAL_COMMUNITIES`, `RAG_MAX_IMPORT_BATCH_BYTES`, `RAG_MAX_IMPORT_BATCH_ITEMS`, `RAG_MAX_IMPORT_FILES`, `RAG_MAX_QUERY_RESULTS`, `RAG_MIN_SYNTHESIS_SCORE`, `RAG_NO_EVIDENCE_MESSAGE`, `RAG_NO_EVIDENCE_THRESHOLD`, `RAG_PARSE_TIMEOUT_SECONDS`, `RAG_QUERY_CONTEXT_CHARS`, `RAG_RETRIEVAL_MAX_PER_DOC`, `RAG_SYNTHESIS_MAX_PER_DOC`, `RAG_WEAK_EVIDENCE_MESSAGE`, `RAG_WEAK_MATCH_SCORE_CAP`, `SESSION_HEARTBEAT_STALE_SECONDS`, `SESSION_WATCHDOG_INTERVAL_SECONDS`, `SKILLS_APP_JS`, `SKILLS_EXTRA_CSS`, `SKILLS_INDEX_HTML`, `SKILL_REFRESH_MIN_INTERVAL_SECONDS`, `TOKEN_THRESHOLD`, `WEB_UI_OPTIONAL_FILES`, `WEB_UI_REQUIRED_FILES`; `config/paths.py`: `LLM_CONFIG_PATH`, `REPO_ROOT`, `_migrate_legacy_runtime_roots`; `config/settings.py`: `_to_bool_like`, `default_multimodal_capabilities`, `infer_model_multimodal_capabilities`, `merge_multimodal_capabilities`, `model_language_instruction`, `normalize_execution_mode`, `normalize_ui_language`, `normalize_ui_style`, `parse_capability_overrides`, `parse_llm_config_profiles`, `resolve_optional_file_path`, `resolve_web_ui_dir_path`; `llm/client.py`: `OllamaClient`; `llm/utils.py`: `extract_base_url`, `list_ollama_models_cached`; `rag/ingestion.py`: `CodeIngestionService`, `RAGIngestionService`, `_rag_embed_batch`, `_rag_embed_text`, `_rag_mmr_select`, `_rag_query_variants`; `rag/parsers.py`: `CodeContentParser`, `RAGContentParser`; `rag/store.py`: `CodeLibraryStore`, `RAGLibraryStore`, `WikiStore`, `WorkflowMemoryStore`; `session/manager.py`: `SessionCreationLimitExceeded`, `SessionManager`; `session/state.py`: `SessionState`; `skills/store.py`: `SkillStore`, `_sanitize_skill_slug`, `analyze_skill_building_knowledge`, `ensure_runtime_skills`; `utils/crypto.py`: `CryptoBox`; `utils/files.py`: `_resolve_js_lib_asset_path`, `ensure_offline_js_libs`, `load_offline_js_lib_index`, `offline_js_lib_root`, `safe_path`, `try_read_text`; `utils/json_utils.py`: `TOOLS`, `extract_json_object_from_text`, `json_dumps`, `parse_json_object`; `utils/misc.py`: `DEFAULT_TIMEOUT_SECONDS`, `MAX_TIMEOUT_SECONDS`, `MIN_TIMEOUT_SECONDS`, `normalize_timeout_seconds`, `now_ts`, `sanitize_profile_id`; `utils/text.py`: `parse_front_matter`, `trim`
- Symbols:
  - `AppContext` (class, lines 59935-63296)

### `config/constants.py`

- Routed symbols: 341
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
  - `RAG_LIBRARY_DIRNAME` (constant, lines 146-146)
  - `RAG_ADMIN_PORT_OFFSET` (constant, lines 147-147)
  - `CODE_LIBRARY_DIRNAME` (constant, lines 148-148)
  - `CODE_ADMIN_PORT_OFFSET` (constant, lines 149-149)
  - `RAG_CHUNK_CHARS` (constant, lines 150-150)
  - `RAG_CHUNK_OVERLAP` (constant, lines 151-151)
  - `RAG_MAX_CHUNKS_PER_DOC` (constant, lines 152-152)
  - `CODE_CHUNK_CHARS` (constant, lines 153-153)
  - `CODE_CHUNK_OVERLAP` (constant, lines 154-154)
  - `CODE_MAX_CHUNKS_PER_DOC` (constant, lines 155-155)
  - `RAG_MAX_QUERY_RESULTS` (constant, lines 156-156)
  - `RAG_HIGH_RECALL_POOL_MULTIPLIER` (constant, lines 157-157)
  - `RAG_HIGH_RECALL_MIN_POOL` (constant, lines 158-158)
  - `RAG_RETRIEVAL_MAX_PER_DOC` (constant, lines 159-159)
  - `RAG_GRAPH_MAX_NODES` (constant, lines 160-160)
  - `RAG_TASK_HISTORY_LIMIT` (constant, lines 161-161)
  - `RAG_MODEL_MEDIA_MAX_BYTES` (constant, lines 162-162)
  - `RAG_MAX_IMPORT_FILES` (constant, lines 163-163)
  - `RAG_MAX_IMPORT_BATCH_ITEMS` (constant, lines 164-164)
  - `RAG_MAX_IMPORT_BATCH_BYTES` (constant, lines 165-165)
  - `RAG_PDF_IMAGE_LIMIT` (constant, lines 166-166)
  - `RAG_QUERY_CONTEXT_CHARS` (constant, lines 167-167)
  - `RAG_MAX_GLOBAL_COMMUNITIES` (constant, lines 168-168)
  - `RAG_MAX_COMMUNITY_MAP_SUPPORT` (constant, lines 169-169)
  - `RAG_INCLUDE_FILENAME_ENTITIES_DEFAULT` (constant, lines 170-170)
  - `RAG_DYNAMIC_NOISE_MIN_DOC_FREQ` (constant, lines 171-171)
  - `RAG_DYNAMIC_NOISE_MIN_COMMUNITY_FREQ` (constant, lines 172-172)
  - `RAG_DYNAMIC_NOISE_SOFT_DOC_RATIO` (constant, lines 173-173)
  - `RAG_DYNAMIC_NOISE_HARD_DOC_RATIO` (constant, lines 174-174)
  - `RAG_DYNAMIC_NOISE_SOFT_COMMUNITY_RATIO` (constant, lines 175-175)
  - `RAG_DYNAMIC_NOISE_HARD_COMMUNITY_RATIO` (constant, lines 176-176)
  - `RAG_MIN_SYNTHESIS_SCORE` (constant, lines 177-177)
  - `RAG_NO_EVIDENCE_THRESHOLD` (constant, lines 178-178)
  - `RAG_WEAK_MATCH_SCORE_CAP` (constant, lines 179-179)
  - `RAG_SYNTHESIS_MAX_PER_DOC` (constant, lines 180-180)
  - `RAG_WORKFLOW_ACCEPT_SCORE` (constant, lines 181-181)
  - `RAG_NO_EVIDENCE_MESSAGE` (constant, lines 182-182)
  - `RAG_CONTEXT_BUDGETS` (constant, lines 183-187)
  - `RAG_WEAK_EVIDENCE_MESSAGE` (constant, lines 188-188)
  - `RAG_DENSE_DEFAULT_ENABLED` (constant, lines 189-189)
  - `RAG_EMBEDDING_MODE_VALUES` (constant, lines 190-190)
  - `RAG_IMPORT_WORKER_COUNT` (constant, lines 191-194)
  - `CODE_IMPORT_WORKER_COUNT` (constant, lines 195-198)
  - `RAG_PARSE_TIMEOUT_SECONDS` (constant, lines 199-202)
  - `CODE_PARSE_TIMEOUT_SECONDS` (constant, lines 203-206)
  - `TOKEN_THRESHOLD` (constant, lines 207-207)
  - `CONTEXT_AUTO_COMPACT_RESERVE_RATIO` (constant, lines 208-211)
  - `CONTEXT_ESTIMATE_SAFETY_MULTIPLIER` (constant, lines 212-215)
  - `CONTEXT_USAGE_CALIBRATION_MAX` (constant, lines 216-219)
  - `CONTEXT_ACTUAL_USAGE_RECENT_SECONDS` (constant, lines 220-223)
  - `LARGE_FILE_AUTO_PAGE_BYTES` (constant, lines 224-227)
  - `LARGE_FILE_AUTO_PAGE_LINES` (constant, lines 228-231)
  - `LARGE_SOURCE_UPLOAD_EXCERPT_CHARS` (constant, lines 232-235)
  - `CHAT_UPLOAD_PARSE_QUEUE_MAX` (constant, lines 236-239)
  - `CHAT_UPLOAD_PARSE_TIMEOUT_SECONDS` (constant, lines 240-243)
  - `CHAT_UPLOAD_INLINE_TEXT_BYTES` (constant, lines 244-247)
  - `CHAT_UPLOAD_PARSE_MAX_BYTES` (constant, lines 248-254)
  - `CHAT_UPLOAD_ZIP_ENTRY_MAX_BYTES` (constant, lines 255-261)
  - `CHAT_UPLOAD_TEXT_CONTEXT_CHARS` (constant, lines 262-265)
  - `CHAT_UPLOAD_PROMPT_MAX_FILES` (constant, lines 266-269)
  - `CHAT_UPLOAD_PROMPT_MAX_CHARS` (constant, lines 270-273)
  - `CHAT_UPLOAD_PROMPT_PER_FILE_CHARS` (constant, lines 274-277)
  - `CHAT_UPLOAD_FRONTEND_WAIT_MS` (constant, lines 278-281)
  - `CHAT_UPLOAD_AUTO_LIBRARY_INGEST` (constant, lines 282-285)
  - `CHAT_UPLOAD_INGEST_QUEUE_MAX` (constant, lines 286-289)
  - `SESSION_SUBMIT_LOCK_TIMEOUT_SECONDS` (constant, lines 290-293)
  - `SESSION_DEFERRED_START_QUEUE_MAX` (constant, lines 294-297)
  - `SESSION_WATCHDOG_INTERVAL_SECONDS` (constant, lines 298-301)
  - `SESSION_HEARTBEAT_STALE_SECONDS` (constant, lines 302-305)
  - `SESSION_LIST_DEFAULT_LIMIT` (constant, lines 306-309)
  - `IDLE_TIMEOUT` (constant, lines 310-310)
  - `POLL_INTERVAL` (constant, lines 311-311)
  - `SSE_HEARTBEAT_SECONDS` (constant, lines 312-312)
  - `MODEL_CALL_PROGRESS_DELAY` (constant, lines 313-313)
  - `MODEL_CALL_PROGRESS_INTERVAL` (constant, lines 314-314)
  - `RUN_COMPLETION_SUMMARY_ENABLED` (constant, lines 315-318)
  - `LLM_HTTP_RETRY_MAX_ATTEMPTS` (constant, lines 319-322)
  - `LLM_HTTP_RETRY_DELAY_SECONDS` (constant, lines 323-326)
  - `LLM_HTTP_RETRY_MAX_SECONDS` (constant, lines 327-330)
  - `LLM_HTTP_RETRY_404_ON_VLLM` (constant, lines 331-334)
  - `LLM_HTTP_RETRY_STATUSES` (constant, lines 335-335)
  - `MAX_AGENT_ROUNDS` (constant, lines 336-336)
  - `MIN_AGENT_ROUNDS` (constant, lines 337-337)
  - `MAX_AGENT_ROUNDS_CAP` (constant, lines 338-338)
  - `REPEATED_TOOL_LOOP_THRESHOLD` (constant, lines 339-339)
  - `BASH_READ_LOOP_THRESHOLD` (constant, lines 340-340)
  - `HARD_BREAK_TOOL_ERROR_THRESHOLD` (constant, lines 341-341)
  - `HARD_BREAK_RECOVERY_ROUND_THRESHOLD` (constant, lines 342-342)
  - `FUSED_FAULT_BREAK_THRESHOLD` (constant, lines 343-343)
  - `STALL_SEVERITY_ESCALATION_THRESHOLD` (constant, lines 344-344)
  - `STALL_SEVERITY_WEIGHT_BASH_READ_LOOP` (constant, lines 345-345)
  - `STALL_SEVERITY_WEIGHT_REPEATED_TOOL` (constant, lines 346-346)
  - `STALL_SEVERITY_WEIGHT_FAULT` (constant, lines 347-347)
  - `STALL_SEVERITY_WEIGHT_RECOVERY_RETRY` (constant, lines 348-348)
  - `STALL_SEVERITY_WEIGHT_WATCHDOG` (constant, lines 349-349)
  - `STALL_SEVERITY_DECAY_ON_SUCCESS` (constant, lines 350-350)
  - `STALL_ESCALATION_MIN_LEVEL` (constant, lines 351-351)
  - `STALL_PLAN_SYNTHESIS_MAX_TOKENS` (constant, lines 352-352)
  - `STALL_ESCALATION_CONTEXT_MAX_CHARS` (constant, lines 353-353)
  - `MAX_RUN_SECONDS` (constant, lines 354-354)
  - `MIN_RUN_TIMEOUT_SECONDS` (constant, lines 355-355)
  - `MAX_RUN_TIMEOUT_SECONDS` (constant, lines 356-356)
  - `DEFAULT_REQUEST_TIMEOUT` (constant, lines 366-366)
  - `_SHELL_AUTO_CONFIRM_PATTERNS` (assignment, lines 369-382)
  - `MIN_SHELL_COMMAND_TIMEOUT_SECONDS` (constant, lines 383-383)
  - `MAX_SHELL_COMMAND_TIMEOUT_SECONDS` (constant, lines 384-384)
  - `DEFAULT_SHELL_COMMAND_TIMEOUT_SECONDS` (constant, lines 385-399)
  - `AUTO_CONTINUE_BUDGET_DEFAULT` (constant, lines 400-400)
  - `AGENT_MAX_OUTPUT_TOKENS` (constant, lines 401-401)
  - `OLLAMA_THINKING_TOOL_BUFFER` (constant, lines 402-402)
  - `WATCHDOG_INTENT_NO_TOOL_THRESHOLD` (constant, lines 403-403)
  - `WATCHDOG_REPEAT_NO_TOOL_THRESHOLD` (constant, lines 404-404)
  - `WATCHDOG_INTENT_NO_TOOL_THRESHOLD_SINGLE` (constant, lines 405-405)
  - `WATCHDOG_REPEAT_NO_TOOL_THRESHOLD_SINGLE` (constant, lines 406-406)
  - `WATCHDOG_STATE_STALL_THRESHOLD` (constant, lines 407-407)
  - `WATCHDOG_CONTEXT_STALL_THRESHOLD` (constant, lines 408-408)
  - `WATCHDOG_REPEAT_SIMILARITY_THRESHOLD` (constant, lines 409-409)
  - `WATCHDOG_CONTEXT_NEAR_RATIO` (constant, lines 410-410)
  - `WATCHDOG_MAX_DECOMPOSE_STEPS` (constant, lines 411-411)
  - `WATCHDOG_STEP_MAX_ATTEMPTS` (constant, lines 412-412)
  - `EMPTY_ACTION_MIN_CONTENT_CHARS` (constant, lines 413-413)
  - `EMPTY_ACTION_WAKEUP_RETRY_LIMIT` (constant, lines 414-414)
  - `THINKING_BUDGET_FORCE_RATIO` (constant, lines 415-415)
  - `_TOOL_TIMEOUT_MAP` (assignment, lines 417-433)
  - `_DEFAULT_TOOL_TIMEOUT` (assignment, lines 434-434)
  - `TRUNCATION_CONTINUATION_MAX_PASSES` (constant, lines 435-435)
  - `TRUNCATION_CONTINUATION_MAX_TOKENS` (constant, lines 436-436)
  - `TRUNCATION_CONTINUATION_TAIL_CHARS` (constant, lines 437-437)
  - `TRUNCATION_CONTINUATION_ECHO_CHARS` (constant, lines 438-438)
  - `TRUNCATION_OVERLAP_SCAN_CHARS` (constant, lines 439-439)
  - `TRUNCATION_PAIR_SCAN_CHARS` (constant, lines 440-440)
  - `TRUNCATION_LIVE_BUFFER_MAX_CHARS` (constant, lines 441-441)
  - `MIN_CONTEXT_TOKEN_LIMIT` (constant, lines 442-442)
  - `COMPACT_TIER1_PCT` (constant, lines 444-444)
  - `COMPACT_TIER2_PCT` (constant, lines 445-445)
  - `COMPACT_TIER3_PCT` (constant, lines 446-446)
  - `COMPACT_TIER1_ABS` (constant, lines 448-448)
  - `COMPACT_TIER2_ABS` (constant, lines 449-449)
  - `FILE_BUFFER_CONTENT_THRESHOLD` (constant, lines 451-451)
  - `FILE_BUFFER_MAX_FILES` (constant, lines 452-452)
  - `AGENT_MSG_LIMIT_TIER0` (constant, lines 454-454)
  - `AGENT_MSG_LIMIT_TIER1` (constant, lines 455-455)
  - `AGENT_MSG_LIMIT_TIER2` (constant, lines 456-456)
  - `AGENT_MSG_LIMIT_TIER3` (constant, lines 457-457)
  - `AGENT_CTX_LIMIT_TIER0` (constant, lines 458-458)
  - `AGENT_CTX_LIMIT_TIER1` (constant, lines 459-459)
  - `AGENT_CTX_LIMIT_TIER2` (constant, lines 460-460)
  - `AGENT_CTX_LIMIT_TIER3` (constant, lines 461-461)
  - `MANAGER_CTX_LIMIT_TIER0` (constant, lines 462-462)
  - `MANAGER_CTX_LIMIT_TIER1` (constant, lines 463-463)
  - `MANAGER_CTX_LIMIT_TIER2` (constant, lines 464-464)
  - `MANAGER_CTX_LIMIT_TIER3` (constant, lines 465-465)
  - `MAX_CONTEXT_ARCHIVE_SEGMENTS` (constant, lines 466-466)
  - `MODEL_OUTPUT_RETRY_TIMES` (constant, lines 467-467)
  - `ARBITER_TRIGGER_MIN_CONTENT_CHARS` (constant, lines 468-468)
  - `ARBITER_VALID_PLANNING_STREAK_LIMIT` (constant, lines 469-469)
  - `ARBITER_DEFAULT_TIMEOUT_SECONDS` (constant, lines 470-470)
  - `ARBITER_DEFAULT_MAX_TOKENS` (constant, lines 471-471)
  - `ARBITER_DEFAULT_TEMPERATURE` (constant, lines 472-472)
  - `LIVE_INPUT_DELAY_WRITE_ROUNDS` (constant, lines 473-473)
  - `LIVE_INPUT_DELAY_TOOL_ROUNDS` (constant, lines 474-474)
  - `LIVE_INPUT_DELAY_NORMAL_ROUNDS` (constant, lines 475-475)
  - `LIVE_INPUT_MAX_INJECTIONS` (constant, lines 476-476)
  - `LIVE_INPUT_REINJECT_INTERVAL` (constant, lines 477-477)
  - `LIVE_INPUT_WEIGHT_BASE_DELAYED` (constant, lines 478-478)
  - `LIVE_INPUT_WEIGHT_BASE_NORMAL` (constant, lines 479-479)
  - `LIVE_INPUT_WEIGHT_STEP_DELAYED` (constant, lines 480-480)
  - `LIVE_INPUT_WEIGHT_STEP_NORMAL` (constant, lines 481-481)
  - `FINAL_SUMMARY_MIN_CHARS` (constant, lines 496-496)
  - `FINAL_SUMMARY_STRICT_MIN_CHARS` (constant, lines 497-497)
  - `RUNTIME_CONTROL_HINT_PREFIXES` (constant, lines 498-515)
  - `RETRY_RUNTIME_HINT_PREFIXES` (constant, lines 516-530)
  - `EXECUTION_MODE_SINGLE` (constant, lines 531-531)
  - `EXECUTION_MODE_SEQUENTIAL` (constant, lines 532-532)
  - `EXECUTION_MODE_SYNC` (constant, lines 533-533)
  - `EXECUTION_MODE_CHOICES` (constant, lines 534-538)
  - `AGENT_ROLES` (constant, lines 539-539)
  - `AGENT_BUBBLE_ROLES` (constant, lines 540-540)
  - `AGENT_ROLE_LABELS` (constant, lines 541-547)
  - `AGENT_ROLE_BUBBLE_COLORS` (constant, lines 548-554)
  - `BLACKBOARD_STATUSES` (constant, lines 555-564)
  - `TASK_COMPLEXITY_LEVELS` (constant, lines 565-565)
  - `TASK_COMPLEXITY_RANKS` (constant, lines 566-571)
  - `TASK_PROFILE_TYPES` (constant, lines 572-578)
  - `TASK_LEVEL_CHOICES` (constant, lines 579-579)
  - `TASK_SCALE_PREFERENCES` (constant, lines 580-580)
  - `SEMANTIC_CONFIDENCE_CHOICES` (constant, lines 581-581)
  - `TASK_LEVEL_POLICIES` (constant, lines 582-628)
  - `MANAGER_ROUTE_TARGETS` (constant, lines 629-629)
  - `BLACKBOARD_MAX_LOG_ENTRIES` (constant, lines 630-630)
  - `BLACKBOARD_MAX_TEXT` (constant, lines 631-631)
  - `SKILL_REFRESH_MIN_INTERVAL_SECONDS` (constant, lines 632-632)
  - `SKILL_PROMPT_MAX_ITEMS` (constant, lines 633-633)
  - `SKILL_PROMPT_MAX_CHARS` (constant, lines 634-634)
  - `SKILL_RUNTIME_CACHE_MAX_ENTRIES` (constant, lines 635-635)
  - `SKILL_RUNTIME_CACHE_MAX_BYTES` (constant, lines 636-636)
  - `AUTO_SKILLS_ROOT_CANDIDATES` (constant, lines 637-637)
  - `SKILL_DEFAULT_ATTACHMENT_GLOBS` (constant, lines 638-668)
  - `SKILL_INLINE_ATTACHMENT_MAX_FILES` (constant, lines 669-669)
  - `SKILL_INLINE_ATTACHMENT_MAX_CHARS` (constant, lines 670-670)
  - `SKILL_RESOURCE_MANIFEST_MAX_ITEMS` (constant, lines 671-671)
  - `SKILL_BODY_COMPACT_THRESHOLD_CHARS` (constant, lines 672-672)
  - `SKILL_BODY_PREVIEW_CHARS` (constant, lines 673-673)
  - `SKILLS_VIRTUAL_PREFIX` (constant, lines 674-674)
  - `SKILLS_EXTERNAL_MOUNT` (constant, lines 675-675)
  - `PLAN_MODE_ENABLED_LEVELS` (constant, lines 676-676)
  - `PLAN_MODE_FORCED_LEVELS` (constant, lines 677-677)
  - `PLAN_MODE_USER_CHOICES` (constant, lines 678-678)
  - `TASK_PHASES` (constant, lines 680-680)
  - `TASK_PHASE_ROUTING` (constant, lines 681-688)
  - `COMPLEXITY_KEYWORDS` (constant, lines 690-695)
  - `USER_COMPLEXITY_SIMPLE_TOKENS` (constant, lines 696-700)
  - `USER_COMPLEXITY_MODERATE_TOKENS` (constant, lines 701-705)
  - `USER_COMPLEXITY_COMPLEX_TOKENS` (constant, lines 706-710)
  - `USER_COMPLEXITY_EXPERT_TOKENS` (constant, lines 711-715)
  - `PLAN_MODE_EXPLORER_MAX_ROUNDS` (constant, lines 716-716)
  - `PLAN_MODE_SYNTHESIS_MAX_ATTEMPTS` (constant, lines 717-717)
  - `REVIEWER_DEBUG_MODE_MAX_ROUNDS` (constant, lines 719-719)
  - `REVIEWER_DEBUG_TOOL_ALLOWLIST` (constant, lines 720-724)
  - `EXPLORER_STALL_THRESHOLD` (constant, lines 725-725)
  - `DEVELOPER_EDIT_STALL_THRESHOLD` (constant, lines 726-726)
  - `PLAN_MODE_MANAGER_SYNTHESIS_MAX_TOKENS` (constant, lines 727-727)
  - `PLAN_MODE_MAX_OPTIONS` (constant, lines 728-728)
  - `PLAN_FILE_RELATIVE_PATH` (constant, lines 729-729)
  - `PLAN_BUBBLE_MAX_CHARS` (constant, lines 730-730)
  - `PLAN_NOTICE_BODY_MAX_CHARS` (constant, lines 731-731)
  - `PLAN_MESSAGE_EVENT_MAX_CHARS` (constant, lines 732-732)
  - `PLAN_STEP_FULL_CONTENT_MAX_CHARS` (constant, lines 733-733)
  - `PLAN_MODE_RESEARCH_TOOL_ALLOWLIST` (constant, lines 734-738)
  - `FAILURE_LEDGER_MAX_FIXES` (constant, lines 739-739)
  - `FAILURE_LEDGER_MAX_COMPILE_ERRORS` (constant, lines 740-740)
  - `FAILURE_LEDGER_MAX_DELEGATIONS` (constant, lines 741-741)
  - `FAILURE_LEDGER_MAX_STALLS` (constant, lines 742-742)
  - `FAILURE_LEDGER_MAX_TOOL_FPS` (constant, lines 743-743)
  - `FAILURE_LEDGER_MAX_ERRORS` (constant, lines 744-744)
  - `ERROR_CATEGORY_DEFS` (constant, lines 747-784)
  - `CHECKPOINT_MAX_COUNT` (constant, lines 785-785)
  - `CHECKPOINT_INTERVAL_ROUNDS` (constant, lines 786-786)
  - `PERSISTED_ROUTES_MAX` (constant, lines 787-787)
  - `HTML_FRONTEND_REQUEST_KEYWORDS` (constant, lines 788-827)
  - `DEEP_RESEARCH_REQUEST_KEYWORDS` (constant, lines 828-850)
  - `DEEP_RESEARCH_RETRIEVAL_KEYWORDS` (constant, lines 851-870)
  - `DEEP_RESEARCH_TEXT_ONLY_HINT_KEYWORDS` (constant, lines 871-888)
  - `DANGEROUS_PATTERNS` (constant, lines 890-890)
  - `VALID_MSG_TYPES` (constant, lines 891-897)
  - `SUPPORTED_UI_LANGUAGES` (constant, lines 899-904)
  - `UI_LANGUAGE_LABELS` (constant, lines 905-905)
  - `DEFAULT_UI_LANGUAGE` (constant, lines 906-906)
  - `UI_STYLE_CHOICES` (constant, lines 907-907)
  - `UI_STYLE_LABELS` (constant, lines 908-908)
  - `DEFAULT_UI_STYLE` (constant, lines 909-909)
  - `DEFAULT_WEB_UI_DIR` (constant, lines 910-910)
  - `DEFAULT_WEB_UI_CONFIG` (constant, lines 911-911)
  - `WEB_UI_REQUIRED_FILES` (constant, lines 912-919)
  - `WEB_UI_OPTIONAL_FILES` (constant, lines 920-920)
  - `IMAGE_EXTS` (constant, lines 922-935)
  - `IMAGE_FORMATS_NEED_CONVERSION` (constant, lines 936-936)
  - `IMAGE_SAFE_FORMATS` (constant, lines 937-937)
  - `AUDIO_EXTS` (constant, lines 938-948)
  - `VIDEO_EXTS` (constant, lines 949-959)
  - `CODE_PREVIEW_STAGE_MAX_BYTES` (constant, lines 960-960)
  - `CODE_PREVIEW_STAGE_MAX_ROWS` (constant, lines 961-961)
  - `CODE_PREVIEW_STAGE_MAX_PER_FILE` (constant, lines 962-962)
  - `CODE_PREVIEW_STAGE_MAX_TOTAL` (constant, lines 963-963)
  - `CODE_PREVIEW_DIFF_CONTEXT_LINES` (constant, lines 964-964)
  - `CODE_PREVIEW_DIFF_MERGE_GAP` (constant, lines 965-965)
  - `PREVIEW_DOWNLOAD_MAX_FILES` (constant, lines 966-966)
  - `PREVIEW_DOWNLOAD_MAX_BYTES` (constant, lines 967-967)
  - `RENDER_FRAME_MAX_B64_CHARS` (constant, lines 968-968)
  - `RENDER_FRAME_MAX_POINTS` (constant, lines 969-969)
  - `RENDER_FRAME_MAX_LINES` (constant, lines 970-970)
  - `RENDER_FRAME_MAX_LINE_POINTS` (constant, lines 971-971)
  - `RENDER_FRAME_ACTIVITY_INTERVAL_SECONDS` (constant, lines 972-972)
  - `RAW_TOOLCALL_TEXT_FILTER_THRESHOLD` (constant, lines 973-973)
  - `ASSISTANT_TEXT_PERSIST_MAX_CHARS` (constant, lines 974-974)
  - `ASSISTANT_MESSAGE_EVENT_MAX_CHARS` (constant, lines 975-975)
  - `CODE_PREVIEW_EXTS` (constant, lines 976-1065)
  - `CODE_PREVIEW_FILENAMES` (constant, lines 1066-1077)
  - `MEDIA_CAPABILITY_KEYS` (constant, lines 1078-1085)
  - `SAMPLE_IMAGE_PNG_B64` (constant, lines 1086-1089)
  - `SAMPLE_AUDIO_WAV_B64` (constant, lines 1090-1092)
  - `SAMPLE_VIDEO_MP4_B64` (constant, lines 1093-1095)
  - `OFFLINE_JS_LIB_CATALOG` (constant, lines 1097-1355)
  - `OFFLINE_JS_LIB_INDEX_FILE` (constant, lines 1356-1356)
  - `OFFLINE_JS_LIB_README_FILE` (constant, lines 1357-1357)
  - `BACKEND_I18N` (constant, lines 1543-1612)
  - `call_backend_i18n_en_update_l1614` (expression, lines 1614-1707)
  - `call_backend_i18n_zh_cn_update_l1708` (expression, lines 1708-1801)
  - `call_backend_i18n_zh_tw_update_l1802` (expression, lines 1802-1895)
  - `call_backend_i18n_ja_update_l1896` (expression, lines 1896-1989)
  - `OPENAI_COMPAT_PROVIDER_NAMES` (constant, lines 4021-4029)
  - `OPENAI_LIKE_PROVIDER_NAMES` (constant, lines 4031-4031)
  - `TABULAR_PREVIEW_EXTS` (constant, lines 5562-5562)
  - `EXCEL_PREVIEW_EXTS` (constant, lines 5563-5563)
  - `PRESENTATION_PREVIEW_EXTS` (constant, lines 5564-5564)
  - `DOCUMENT_PREVIEW_EXTS` (constant, lines 5565-5565)
  - `EMBEDDED_SKILLS_ARCHIVE_B64` (constant, lines 5967-6486)
  - `EMBEDDED_SKILLS_ARCHIVE_SHA256` (constant, lines 6487-6487)
  - `EMBEDDED_SKILLS_ARCHIVE_FILES` (constant, lines 6488-6511)
  - `BUILTIN_CLAWHUB_SKILLS_VERSION` (constant, lines 9671-9671)
  - `EMBEDDED_CLAWHUB_SKILLS_ARCHIVE_B64` (constant, lines 9673-9917)
  - `SKILL_PROTOCOL_LOCAL` (constant, lines 9983-9983)
  - `SKILL_PROTOCOL_CLAWHUB` (constant, lines 9984-9984)
  - `SKILL_PROTOCOL_HTTP_JSON` (constant, lines 9985-9985)
  - `SKILL_PROTOCOL_SPECS` (constant, lines 9987-10018)
  - `AGENT_TOOL_ALLOWLIST` (constant, lines 13635-13678)
  - `INDEX_HTML` (constant, lines 41905-42094)
  - `APP_CSS` (constant, lines 42096-42486)
  - `APP_JS` (constant, lines 42488-45800)
  - `APP_TS` (constant, lines 45802-45829)
  - `SKILLS_INDEX_HTML` (constant, lines 45831-45985)
  - `SKILLS_EXTRA_CSS` (constant, lines 45987-46082)
  - `SKILLS_APP_JS` (constant, lines 46084-46225)
  - `RAG_TERM_GROUPS` (constant, lines 46227-50859)
  - `RAG_RESEARCH_HINTS` (constant, lines 50860-50881)
  - `RAG_CODE_HINTS` (constant, lines 50882-50892)
  - `RAG_SHORT_TOKEN_ALLOWLIST` (constant, lines 50893-50908)
  - `RAG_EN_STOPWORDS` (constant, lines 50909-50981)
  - `RAG_ZH_STOPWORDS` (constant, lines 50982-51018)
  - `RAG_GENERIC_ENTITY_TERMS_EN` (constant, lines 51019-51097)
  - `RAG_GENERIC_ENTITY_TERMS_ZH` (constant, lines 51098-51140)
  - `RAG_STRUCTURAL_ENTITY_PATTERNS` (constant, lines 51141-51159)
  - `CODE_LIBRARY_IGNORED_DIRS` (constant, lines 51852-51857)
  - `CODE_LIBRARY_LANGUAGE_BY_EXT` (constant, lines 51858-51914)
  - `CODE_LIBRARY_SPECIAL_FILENAMES` (constant, lines 51915-51921)
  - `RAG_ADMIN_INDEX_HTML` (constant, lines 57845-58018)
  - `RAG_ADMIN_CSS` (constant, lines 58020-58110)
  - `RAG_ADMIN_JS` (constant, lines 58112-59875)
  - `CODE_ADMIN_INDEX_HTML` (constant, lines 59877-59888)
  - `CODE_ADMIN_CSS` (constant, lines 59889-59919)
  - `CODE_ADMIN_JS` (constant, lines 59920-59924)

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
  - `detect_repo_root` (function, lines 2616-2630)
  - `REPO_ROOT` (constant, lines 2632-2632)

### `config/settings.py`

- Routed symbols: 33
- Cross-module imports: `config/constants.py`: `AUTO_SKILLS_ROOT_CANDIDATES`, `BACKEND_I18N`, `DEFAULT_REQUEST_TIMEOUT`, `DEFAULT_SHELL_COMMAND_TIMEOUT_SECONDS`, `DEFAULT_UI_LANGUAGE`, `DEFAULT_UI_STYLE`, `DEFAULT_WEB_UI_CONFIG`, `DEFAULT_WEB_UI_DIR`, `EXECUTION_MODE_CHOICES`, `EXECUTION_MODE_SEQUENTIAL`, `EXECUTION_MODE_SINGLE`, `EXECUTION_MODE_SYNC`, `MAX_SHELL_COMMAND_TIMEOUT_SECONDS`, `MEDIA_CAPABILITY_KEYS`, `MIN_SHELL_COMMAND_TIMEOUT_SECONDS`, `SUPPORTED_UI_LANGUAGES`, `TASK_COMPLEXITY_LEVELS`, `TASK_COMPLEXITY_RANKS`, `UI_LANGUAGE_LABELS`, `UI_STYLE_CHOICES`, `USER_COMPLEXITY_COMPLEX_TOKENS`, `USER_COMPLEXITY_EXPERT_TOKENS`, `USER_COMPLEXITY_MODERATE_TOKENS`, `USER_COMPLEXITY_SIMPLE_TOKENS`; `config/paths.py`: `WORKDIR`; `llm/utils.py`: `_is_http_url`, `_resolve_local_path`, `complete_chat_endpoint`, `extract_base_url`, `is_openai_like_provider`, `normalize_openai_compat_provider_name`, `strip_thinking_content`; `skills/store.py`: `ensure_embedded_skills`; `utils/http.py`: `urlopen`; `utils/json_utils.py`: `parse_json_object`; `utils/misc.py`: `MAX_TIMEOUT_SECONDS`, `MIN_TIMEOUT_SECONDS`, `normalize_timeout_seconds`, `sanitize_profile_id`; `utils/text.py`: `trim`
- Symbols:
  - `normalize_ui_language` (function, lines 1441-1463)
  - `normalize_ui_style` (function, lines 1466-1483)
  - `supported_ui_languages_payload` (function, lines 1486-1487)
  - `normalize_execution_mode` (function, lines 1490-1509)
  - `model_language_instruction` (function, lines 1512-1540)
  - `backend_i18n_text` (function, lines 1992-2002)
  - `backend_role_label` (function, lines 2005-2009)
  - `_detect_os_shell_instruction` (function, lines 2012-2051)
  - `resolve_web_ui_dir_path` (function, lines 2053-2060)
  - `resolve_optional_file_path` (function, lines 2063-2070)
  - `resolve_skills_root_path` (function, lines 2073-2080)
  - `_count_skill_markdown_files` (function, lines 2083-2094)
  - `select_preferred_skills_root` (function, lines 2097-2131)
  - `load_web_ui_config_file` (function, lines 2134-2148)
  - `extract_show_upload_list_setting` (function, lines 2151-2165)
  - `extract_ui_style_setting` (function, lines 2168-2182)
  - `extract_js_lib_download_setting` (function, lines 2185-2204)
  - `extract_daily_session_limit_setting` (function, lines 2207-2250)
  - `extract_shell_command_timeout_setting` (function, lines 2253-2299)
  - `default_multimodal_capabilities` (function, lines 2308-2316)
  - `_to_bool_like` (function, lines 2319-2329)
  - `infer_model_multimodal_capabilities` (function, lines 2332-2376)
  - `parse_capability_overrides` (function, lines 2379-2416)
  - `merge_multimodal_capabilities` (function, lines 2419-2426)
  - `parse_media_endpoints` (function, lines 2429-2443)
  - `infer_user_complexity_value` (function, lines 3939-3955)
  - `normalize_task_complexity` (function, lines 3957-3985)
  - `task_complexity_rank` (function, lines 3987-3988)
  - `task_complexity_at_least` (function, lines 3990-3991)
  - `max_task_complexity` (function, lines 3993-4002)
  - `load_llm_config_from_source` (function, lines 4153-4187)
  - `parse_llm_config_profiles` (function, lines 4189-4775)
  - `looks_like_llm_config` (function, lines 4777-4851)

### `llm/client.py`

- Routed symbols: 2
- Cross-module imports: `config/constants.py`: `DEFAULT_REQUEST_TIMEOUT`, `LLM_HTTP_RETRY_404_ON_VLLM`, `LLM_HTTP_RETRY_DELAY_SECONDS`, `LLM_HTTP_RETRY_MAX_ATTEMPTS`, `LLM_HTTP_RETRY_MAX_SECONDS`, `LLM_HTTP_RETRY_STATUSES`, `OLLAMA_THINKING_TOOL_BUFFER`, `SAMPLE_AUDIO_WAV_B64`, `SAMPLE_IMAGE_PNG_B64`, `SAMPLE_VIDEO_MP4_B64`; `config/settings.py`: `default_multimodal_capabilities`, `infer_model_multimodal_capabilities`, `merge_multimodal_capabilities`, `parse_capability_overrides`, `parse_media_endpoints`; `llm/utils.py`: `complete_chat_endpoint`, `is_openai_compat_provider`, `is_openai_like_provider`, `normalize_openai_compat_provider_name`, `split_thinking_content`; `utils/http.py`: `urlopen`; `utils/json_utils.py`: `canonicalize_tool_name`, `json_dumps`, `parse_json_object`, `parse_tool_arguments`, `parse_tool_arguments_with_error`; `utils/misc.py`: `MAX_TIMEOUT_SECONDS`, `MIN_TIMEOUT_SECONDS`, `make_id`, `normalize_timeout_seconds`, `now_ts`; `utils/text.py`: `trim`
- Symbols:
  - `OllamaError` (class, lines 11902-11922)
  - `OllamaClient` (class, lines 11924-13391)

### `llm/utils.py`

- Routed symbols: 25
- Cross-module imports: `config/constants.py`: `OPENAI_COMPAT_PROVIDER_NAMES`, `OPENAI_LIKE_PROVIDER_NAMES`; `utils/http.py`: `urlopen`; `utils/json_utils.py`: `json_dumps`, `parse_json_object`; `utils/text.py`: `trim`
- Symbols:
  - `probe_ollama_environment` (function, lines 3623-3636)
  - `list_ollama_models` (function, lines 3638-3640)
  - `_OLLAMA_TAG_CACHE_LOCK` (assignment, lines 3642-3642)
  - `_OLLAMA_TAG_CACHE` (assignment, lines 3643-3643)
  - `list_ollama_models_cached` (function, lines 3653-3690)
  - `resolve_ollama_model` (function, lines 3692-3702)
  - `infer_thinking_model` (function, lines 3704-3706)
  - `split_thinking_content` (function, lines 3708-3751)
  - `strip_thinking_content` (function, lines 3753-3754)
  - `check_ollama_model_ready` (function, lines 3756-3780)
  - `list_loaded_ollama_models` (function, lines 3782-3795)
  - `wake_ollama_model` (function, lines 3797-3827)
  - `try_pull_ollama_model` (function, lines 3829-3847)
  - `ordered_model_candidates` (function, lines 3849-3867)
  - `pick_working_ollama_model` (function, lines 3869-3885)
  - `extract_base_url` (function, lines 3918-3926)
  - `complete_chat_endpoint` (function, lines 3928-3937)
  - `normalize_openai_compat_provider_name` (function, lines 4004-4019)
  - `is_openai_compat_provider` (function, lines 4033-4034)
  - `is_openai_like_provider` (function, lines 4036-4037)
  - `openai_compat_probe_headers` (function, lines 4039-4050)
  - `openai_compat_model_list_urls` (function, lines 4052-4084)
  - `extract_openai_compat_model_ids` (function, lines 4086-4119)
  - `_is_http_url` (function, lines 4128-4133)
  - `_resolve_local_path` (function, lines 4135-4151)

### `rag/index.py`

- Routed symbols: 5
- Cross-module imports: `config/constants.py`: `RAG_DYNAMIC_NOISE_HARD_COMMUNITY_RATIO`, `RAG_DYNAMIC_NOISE_HARD_DOC_RATIO`, `RAG_DYNAMIC_NOISE_MIN_COMMUNITY_FREQ`, `RAG_DYNAMIC_NOISE_MIN_DOC_FREQ`, `RAG_DYNAMIC_NOISE_SOFT_COMMUNITY_RATIO`, `RAG_DYNAMIC_NOISE_SOFT_DOC_RATIO`, `RAG_EN_STOPWORDS`, `RAG_GRAPH_MAX_NODES`, `RAG_INCLUDE_FILENAME_ENTITIES_DEFAULT`, `RAG_MAX_COMMUNITY_MAP_SUPPORT`, `RAG_MAX_GLOBAL_COMMUNITIES`, `RAG_MAX_QUERY_RESULTS`, `RAG_MIN_SYNTHESIS_SCORE`, `RAG_WEAK_MATCH_SCORE_CAP`; `rag/ingestion.py`: `_rag_focused_excerpt`, `_rag_mmr_select`, `_rag_window_for_query`; `rag/parsers.py`: `_code_is_test_path`, `_rag_apply_filename_entity_policy`, `_rag_choose_community`, `_rag_classify_document`, `_rag_expand_tokens`, `_rag_extract_entities`, `_rag_filter_entities`, `_rag_tokenize`; `utils/misc.py`: `now_ts`; `utils/text.py`: `trim`
- Symbols:
  - `_code_module_name` (function, lines 51948-51962)
  - `_code_choose_community` (function, lines 51965-51972)
  - `_code_query_terms` (function, lines 51975-51987)
  - `TFGraphIDFIndex` (class, lines 53040-54606)
  - `CodeGraphIndex` (class, lines 57024-57489)

### `rag/ingestion.py`

- Routed symbols: 12
- Cross-module imports: `config/constants.py`: `CODE_IMPORT_WORKER_COUNT`, `CODE_LIBRARY_IGNORED_DIRS`, `CODE_PARSE_TIMEOUT_SECONDS`, `RAG_IMPORT_WORKER_COUNT`, `RAG_MAX_IMPORT_BATCH_ITEMS`, `RAG_MAX_IMPORT_FILES`, `RAG_MODEL_MEDIA_MAX_BYTES`, `RAG_PARSE_TIMEOUT_SECONDS`, `RAG_PDF_IMAGE_LIMIT`, `RAG_RETRIEVAL_MAX_PER_DOC`; `config/settings.py`: `default_multimodal_capabilities`; `rag/parsers.py`: `CodeContentParser`, `RAGContentParser`, `_rag_expand_tokens`, `_rag_extract_entities`, `_rag_is_noise_token`, `_rag_safe_name`, `_rag_tokenize`; `rag/store.py`: `CodeLibraryStore`, `RAGLibraryStore`, `WikiStore`; `session/state.py`: `SessionState`; `utils/files.py`: `try_read_text`; `utils/json_utils.py`: `_read_json_file`, `_write_json_file`, `parse_json_object`; `utils/media.py`: `guess_mime_from_name`; `utils/misc.py`: `make_id`, `now_ts`; `utils/text.py`: `trim`
- Symbols:
  - `_rag_trigram_set` (function, lines 51372-51377)
  - `_rag_jaccard_sim` (function, lines 51380-51387)
  - `_rag_mmr_select` (function, lines 51390-51437)
  - `_rag_embed_text` (function, lines 51574-51595)
  - `_rag_embed_batch` (function, lines 51598-51604)
  - `_rag_window_for_query` (function, lines 51607-51619)
  - `_rag_focused_excerpt` (function, lines 51622-51662)
  - `_rag_query_variants` (function, lines 51665-51702)
  - `_rag_parse_segments` (function, lines 51705-51765)
  - `_rag_parse_file_worker` (function, lines 56128-56142)
  - `RAGIngestionService` (class, lines 56145-57021)
  - `CodeIngestionService` (class, lines 57758-57843)

### `rag/parsers.py`

- Routed symbols: 28
- Cross-module imports: `config/constants.py`: `AUDIO_EXTS`, `CODE_CHUNK_CHARS`, `CODE_CHUNK_OVERLAP`, `CODE_LIBRARY_LANGUAGE_BY_EXT`, `CODE_LIBRARY_SPECIAL_FILENAMES`, `CODE_MAX_CHUNKS_PER_DOC`, `CODE_PREVIEW_DIFF_CONTEXT_LINES`, `CODE_PREVIEW_DIFF_MERGE_GAP`, `CODE_PREVIEW_EXTS`, `CODE_PREVIEW_FILENAMES`, `CODE_PREVIEW_STAGE_MAX_ROWS`, `DOCUMENT_PREVIEW_EXTS`, `EXCEL_PREVIEW_EXTS`, `IMAGE_EXTS`, `PRESENTATION_PREVIEW_EXTS`, `RAG_CHUNK_CHARS`, `RAG_CHUNK_OVERLAP`, `RAG_CODE_HINTS`, `RAG_EN_STOPWORDS`, `RAG_GENERIC_ENTITY_TERMS_EN`, `RAG_GENERIC_ENTITY_TERMS_ZH`, `RAG_INCLUDE_FILENAME_ENTITIES_DEFAULT`, `RAG_MAX_CHUNKS_PER_DOC`, `RAG_PDF_IMAGE_LIMIT`, `RAG_RESEARCH_HINTS`, `RAG_SHORT_TOKEN_ALLOWLIST`, `RAG_STRUCTURAL_ENTITY_PATTERNS`, `RAG_TERM_GROUPS`, `RAG_ZH_STOPWORDS`, `TABULAR_PREVIEW_EXTS`, `VIDEO_EXTS`; `rag/ingestion.py`: `_rag_parse_segments`; `utils/files.py`: `_sha256_bytes`, `_sha256_file`; `utils/json_utils.py`: `parse_json_object`; `utils/media.py`: `guess_mime_from_name`; `utils/text.py`: `_focused_diff_rows_from_opcodes`, `_skip_row`, `trim`
- Symbols:
  - `normalize_rel_preview_path` (function, lines 5537-5548)
  - `is_code_preview_candidate` (function, lines 5551-5559)
  - `preview_kind_for_path` (function, lines 5568-5597)
  - `build_code_preview_rows` (function, lines 5600-5647)
  - `_rag_safe_name` (function, lines 51171-51174)
  - `_rag_detect_language` (function, lines 51177-51191)
  - `_rag_cjk_ngrams` (function, lines 51194-51206)
  - `_rag_is_noise_token` (function, lines 51209-51228)
  - `_rag_entity_allowed` (function, lines 51231-51243)
  - `_rag_filter_entities` (function, lines 51246-51260)
  - `_rag_filename_entity_aliases` (function, lines 51263-51296)
  - `_rag_apply_filename_entity_policy` (function, lines 51299-51329)
  - `_rag_choose_community` (function, lines 51332-51369)
  - `_rag_tokenize` (function, lines 51440-51491)
  - `_rag_expand_tokens` (function, lines 51494-51515)
  - `_rag_extract_entities` (function, lines 51518-51534)
  - `_rag_classify_document` (function, lines 51537-51571)
  - `_rag_chunk_text` (function, lines 51768-51847)
  - `_code_language_from_name` (function, lines 51924-51940)
  - `_code_is_test_path` (function, lines 51943-51945)
  - `_CallCollector` (class, lines 51990-52002)
  - `_ALGO_COMPLEXITY_RE` (assignment, lines 52005-52005)
  - `_ALGO_STEP_RE` (assignment, lines 52006-52006)
  - `_ALGO_MATH_VARS` (assignment, lines 52007-52007)
  - `_ALGO_DOC_KEYWORDS` (assignment, lines 52008-52008)
  - `_detect_algo_chunk` (function, lines 52011-52034)
  - `CodeContentParser` (class, lines 52037-52527)
  - `RAGContentParser` (class, lines 52530-53037)

### `rag/store.py`

- Routed symbols: 4
- Cross-module imports: `config/constants.py`: `CODE_CHUNK_CHARS`, `CODE_CHUNK_OVERLAP`, `CODE_MAX_CHUNKS_PER_DOC`, `RAG_INCLUDE_FILENAME_ENTITIES_DEFAULT`, `RAG_MAX_QUERY_RESULTS`, `RAG_RETRIEVAL_MAX_PER_DOC`, `RAG_TASK_HISTORY_LIMIT`, `RAG_WEAK_MATCH_SCORE_CAP`, `RAG_WORKFLOW_ACCEPT_SCORE`; `rag/index.py`: `CodeGraphIndex`, `TFGraphIDFIndex`, `_code_choose_community`, `_code_module_name`; `rag/ingestion.py`: `_rag_focused_excerpt`, `_rag_mmr_select`, `_rag_window_for_query`; `rag/parsers.py`: `_code_is_test_path`, `_rag_apply_filename_entity_policy`, `_rag_choose_community`, `_rag_chunk_text`, `_rag_entity_allowed`, `_rag_expand_tokens`, `_rag_extract_entities`, `_rag_filter_entities`, `_rag_safe_name`, `_rag_tokenize`; `skills/store.py`: `_write_text_if_changed`; `utils/files.py`: `_sha256_bytes`, `_sha256_file`, `try_read_text`; `utils/json_utils.py`: `_read_json_file`, `_write_json_file`, `json_dumps`; `utils/media.py`: `guess_mime_from_name`; `utils/misc.py`: `make_id`, `now_ts`; `utils/text.py`: `trim`
- Symbols:
  - `RAGLibraryStore` (class, lines 54618-55192)
  - `WikiStore` (class, lines 55195-55724)
  - `WorkflowMemoryStore` (class, lines 55727-56125)
  - `CodeLibraryStore` (class, lines 57492-57755)

### `server/handlers.py`

- Routed symbols: 5
- Cross-module imports: `app/context.py`: `AppContext`; `config/constants.py`: `APP_VERSION`, `DEFAULT_REQUEST_TIMEOUT`, `DEFAULT_SHELL_COMMAND_TIMEOUT_SECONDS`, `DEFAULT_UI_LANGUAGE`, `DEFAULT_UI_STYLE`, `EXECUTION_MODE_CHOICES`, `EXECUTION_MODE_SYNC`, `MIN_RUN_TIMEOUT_SECONDS`, `PLAN_MODE_USER_CHOICES`, `RAG_GRAPH_MAX_NODES`, `SESSION_LIST_DEFAULT_LIMIT`, `SSE_HEARTBEAT_SECONDS`, `TASK_COMPLEXITY_LEVELS`, `TASK_LEVEL_CHOICES`, `TASK_LEVEL_POLICIES`, `UI_STYLE_LABELS`; `config/paths.py`: `LLM_CONFIG_PATH`, `REPO_ROOT`, `WORKDIR`; `config/settings.py`: `_to_bool_like`, `infer_user_complexity_value`, `looks_like_llm_config`, `normalize_execution_mode`, `normalize_task_complexity`, `normalize_ui_language`, `normalize_ui_style`, `resolve_web_ui_dir_path`, `supported_ui_languages_payload`; `llm/utils.py`: `extract_base_url`, `extract_openai_compat_model_ids`, `list_ollama_models`, `normalize_openai_compat_provider_name`, `openai_compat_model_list_urls`, `openai_compat_probe_headers`; `rag/parsers.py`: `normalize_rel_preview_path`; `session/manager.py`: `SessionCreationLimitExceeded`, `SessionManager`; `session/state.py`: `SessionState`; `skills/store.py`: `analyze_skill_building_knowledge`; `utils/files.py`: `safe_path`, `try_read_text`; `utils/http.py`: `urlopen`; `utils/json_utils.py`: `json_dumps`, `parse_json_object`; `utils/media.py`: `guess_mime_from_name`; `utils/misc.py`: `now_ts`, `swallow_benign_socket_error`, `user_id_from_ip`; `utils/text.py`: `trim`
- Symbols:
  - `AgentHTTPServer` (class, lines 63307-63335)
  - `Handler` (class, lines 63339-64240)
  - `SkillsHandler` (class, lines 64242-64438)
  - `RagAdminHandler` (class, lines 64440-64608)
  - `CodeAdminHandler` (class, lines 64611-64797)

### `session/manager.py`

- Routed symbols: 2
- Cross-module imports: `config/constants.py`: `AGENT_MAX_OUTPUT_TOKENS`, `ARBITER_DEFAULT_MAX_TOKENS`, `ARBITER_DEFAULT_TEMPERATURE`, `ARBITER_DEFAULT_TIMEOUT_SECONDS`, `DEFAULT_REQUEST_TIMEOUT`, `DEFAULT_SHELL_COMMAND_TIMEOUT_SECONDS`, `DEFAULT_UI_LANGUAGE`, `EXECUTION_MODE_SYNC`, `MAX_AGENT_ROUNDS`, `MAX_AGENT_ROUNDS_CAP`, `MAX_RUN_SECONDS`, `MAX_RUN_TIMEOUT_SECONDS`, `MAX_SHELL_COMMAND_TIMEOUT_SECONDS`, `MIN_AGENT_ROUNDS`, `MIN_CONTEXT_TOKEN_LIMIT`, `MIN_RUN_TIMEOUT_SECONDS`, `MIN_SHELL_COMMAND_TIMEOUT_SECONDS`, `SESSION_LIST_DEFAULT_LIMIT`, `TOKEN_THRESHOLD`; `config/paths.py`: `LLM_CONFIG_PATH`; `config/settings.py`: `infer_model_multimodal_capabilities`, `merge_multimodal_capabilities`, `normalize_execution_mode`, `normalize_ui_language`, `parse_capability_overrides`, `parse_llm_config_profiles`; `llm/client.py`: `OllamaClient`; `llm/utils.py`: `complete_chat_endpoint`, `extract_base_url`, `is_openai_compat_provider`, `list_ollama_models_cached`, `probe_ollama_environment`; `session/state.py`: `SessionState`; `utils/crypto.py`: `CryptoBox`; `utils/files.py`: `try_read_text`; `utils/json_utils.py`: `parse_json_object`; `utils/misc.py`: `make_id`, `normalize_timeout_seconds`, `now_ts`, `sanitize_profile_id`
- Symbols:
  - `SessionCreationLimitExceeded` (class, lines 2302-2305)
  - `SessionManager` (class, lines 40968-41903)

### `session/state.py`

- Routed symbols: 1
- Cross-module imports: `agent/background.py`: `BackgroundManager`; `agent/bus.py`: `MessageBus`; `agent/events.py`: `EventHub`; `agent/tasks.py`: `TaskManager`; `agent/todo.py`: `TodoManager`; `agent/worktree.py`: `WorktreeManager`; `config/constants.py`: `AGENT_BUBBLE_ROLES`, `AGENT_CTX_LIMIT_TIER0`, `AGENT_CTX_LIMIT_TIER1`, `AGENT_CTX_LIMIT_TIER2`, `AGENT_CTX_LIMIT_TIER3`, `AGENT_MAX_OUTPUT_TOKENS`, `AGENT_MSG_LIMIT_TIER0`, `AGENT_MSG_LIMIT_TIER1`, `AGENT_MSG_LIMIT_TIER2`, `AGENT_MSG_LIMIT_TIER3`, `AGENT_ROLES`, `AGENT_TOOL_ALLOWLIST`, `ARBITER_DEFAULT_MAX_TOKENS`, `ARBITER_DEFAULT_TEMPERATURE`, `ARBITER_DEFAULT_TIMEOUT_SECONDS`, `ARBITER_TRIGGER_MIN_CONTENT_CHARS`, `ARBITER_VALID_PLANNING_STREAK_LIMIT`, `ASSISTANT_MESSAGE_EVENT_MAX_CHARS`, `ASSISTANT_TEXT_PERSIST_MAX_CHARS`, `AUDIO_EXTS`, `AUTO_CONTINUE_BUDGET_DEFAULT`, `BASH_READ_LOOP_THRESHOLD`, `BLACKBOARD_MAX_LOG_ENTRIES`, `BLACKBOARD_MAX_TEXT`, `BLACKBOARD_STATUSES`, `CHAT_UPLOAD_AUTO_LIBRARY_INGEST`, `CHAT_UPLOAD_INGEST_QUEUE_MAX`, `CHAT_UPLOAD_INLINE_TEXT_BYTES`, `CHAT_UPLOAD_PARSE_MAX_BYTES`, `CHAT_UPLOAD_PARSE_QUEUE_MAX`, `CHAT_UPLOAD_PARSE_TIMEOUT_SECONDS`, `CHAT_UPLOAD_PROMPT_MAX_CHARS`, `CHAT_UPLOAD_PROMPT_MAX_FILES`, `CHAT_UPLOAD_PROMPT_PER_FILE_CHARS`, `CHAT_UPLOAD_TEXT_CONTEXT_CHARS`, `CHAT_UPLOAD_ZIP_ENTRY_MAX_BYTES`, `CHECKPOINT_INTERVAL_ROUNDS`, `CHECKPOINT_MAX_COUNT`, `CODE_PREVIEW_STAGE_MAX_BYTES`, `CODE_PREVIEW_STAGE_MAX_PER_FILE`, `CODE_PREVIEW_STAGE_MAX_ROWS`, `CODE_PREVIEW_STAGE_MAX_TOTAL`, `COMPACT_TIER1_ABS`, `COMPACT_TIER1_PCT`, `COMPACT_TIER2_ABS`, `COMPACT_TIER2_PCT`, `COMPACT_TIER3_PCT`, `CONTEXT_ACTUAL_USAGE_RECENT_SECONDS`, `CONTEXT_AUTO_COMPACT_RESERVE_RATIO`, `CONTEXT_ESTIMATE_SAFETY_MULTIPLIER`, `CONTEXT_USAGE_CALIBRATION_MAX`, `DANGEROUS_PATTERNS`, `DEEP_RESEARCH_REQUEST_KEYWORDS`, `DEEP_RESEARCH_RETRIEVAL_KEYWORDS`, `DEEP_RESEARCH_TEXT_ONLY_HINT_KEYWORDS`, `DEFAULT_REQUEST_TIMEOUT`, `DEFAULT_SHELL_COMMAND_TIMEOUT_SECONDS`, `DEFAULT_UI_LANGUAGE`, `DEVELOPER_EDIT_STALL_THRESHOLD`, `EMPTY_ACTION_MIN_CONTENT_CHARS`, `EMPTY_ACTION_WAKEUP_RETRY_LIMIT`, `ERROR_CATEGORY_DEFS`, `EXECUTION_MODE_CHOICES`, `EXECUTION_MODE_SEQUENTIAL`, `EXECUTION_MODE_SINGLE`, `EXECUTION_MODE_SYNC`, `EXPLORER_STALL_THRESHOLD`, `FAILURE_LEDGER_MAX_COMPILE_ERRORS`, `FAILURE_LEDGER_MAX_DELEGATIONS`, `FAILURE_LEDGER_MAX_ERRORS`, `FAILURE_LEDGER_MAX_FIXES`, `FAILURE_LEDGER_MAX_STALLS`, `FAILURE_LEDGER_MAX_TOOL_FPS`, `FILE_BUFFER_CONTENT_THRESHOLD`, `FILE_BUFFER_MAX_FILES`, `FINAL_SUMMARY_MIN_CHARS`, `FINAL_SUMMARY_STRICT_MIN_CHARS`, `FUSED_FAULT_BREAK_THRESHOLD`, `HARD_BREAK_RECOVERY_ROUND_THRESHOLD`, `HARD_BREAK_TOOL_ERROR_THRESHOLD`, `HTML_FRONTEND_REQUEST_KEYWORDS`, `IMAGE_EXTS`, `IMAGE_FORMATS_NEED_CONVERSION`, `LARGE_FILE_AUTO_PAGE_BYTES`, `LARGE_FILE_AUTO_PAGE_LINES`, `LARGE_SOURCE_UPLOAD_EXCERPT_CHARS`, `LIVE_INPUT_DELAY_NORMAL_ROUNDS`, `LIVE_INPUT_DELAY_TOOL_ROUNDS`, `LIVE_INPUT_DELAY_WRITE_ROUNDS`, `LIVE_INPUT_MAX_INJECTIONS`, `LIVE_INPUT_REINJECT_INTERVAL`, `LIVE_INPUT_WEIGHT_BASE_DELAYED`, `LIVE_INPUT_WEIGHT_BASE_NORMAL`, `LIVE_INPUT_WEIGHT_STEP_DELAYED`, `LIVE_INPUT_WEIGHT_STEP_NORMAL`, `LONG_OUTPUT_LISTING_OFFLOAD_CHARS`, `LONG_OUTPUT_MODEL_PAGE_CHARS`, `LONG_OUTPUT_READ_PAGE_LINES`, `LONG_OUTPUT_READ_PAGE_MAX_CHARS`, `LONG_OUTPUT_TEMP_MAX_FILES`, `LONG_OUTPUT_UI_PAGE_CHARS`, `LONG_OUTPUT_UI_PREVIEW_MAX_PAGES`, `MANAGER_CTX_LIMIT_TIER0`, `MANAGER_CTX_LIMIT_TIER1`, `MANAGER_CTX_LIMIT_TIER2`, `MANAGER_CTX_LIMIT_TIER3`, `MANAGER_ROUTE_TARGETS`, `MAX_AGENT_ROUNDS`, `MAX_AGENT_ROUNDS_CAP`, `MAX_CONTEXT_ARCHIVE_SEGMENTS`, `MAX_RUN_SECONDS`, `MAX_RUN_TIMEOUT_SECONDS`, `MAX_SHELL_COMMAND_TIMEOUT_SECONDS`, `MIN_AGENT_ROUNDS`, `MIN_CONTEXT_TOKEN_LIMIT`, `MIN_RUN_TIMEOUT_SECONDS`, `MIN_SHELL_COMMAND_TIMEOUT_SECONDS`, `MODEL_CALL_PROGRESS_DELAY`, `MODEL_CALL_PROGRESS_INTERVAL`, `MODEL_OUTPUT_RETRY_TIMES`, `PERSISTED_ROUTES_MAX`, `PLAN_BUBBLE_MAX_CHARS`, `PLAN_FILE_RELATIVE_PATH`, `PLAN_MESSAGE_EVENT_MAX_CHARS`, `PLAN_MODE_ENABLED_LEVELS`, `PLAN_MODE_EXPLORER_MAX_ROUNDS`, `PLAN_MODE_FORCED_LEVELS`, `PLAN_MODE_MANAGER_SYNTHESIS_MAX_TOKENS`, `PLAN_MODE_MAX_OPTIONS`, `PLAN_MODE_RESEARCH_TOOL_ALLOWLIST`, `PLAN_MODE_SYNTHESIS_MAX_ATTEMPTS`, `PLAN_MODE_USER_CHOICES`, `PLAN_NOTICE_BODY_MAX_CHARS`, `PLAN_STEP_FULL_CONTENT_MAX_CHARS`, `PREVIEW_DOWNLOAD_MAX_BYTES`, `PREVIEW_DOWNLOAD_MAX_FILES`, `RENDER_FRAME_ACTIVITY_INTERVAL_SECONDS`, `RENDER_FRAME_MAX_B64_CHARS`, `RENDER_FRAME_MAX_LINES`, `RENDER_FRAME_MAX_LINE_POINTS`, `RENDER_FRAME_MAX_POINTS`, `REPEATED_TOOL_LOOP_THRESHOLD`, `RETRY_RUNTIME_HINT_PREFIXES`, `REVIEWER_DEBUG_MODE_MAX_ROUNDS`, `RUNTIME_CONTROL_HINT_PREFIXES`, `RUN_COMPLETION_SUMMARY_ENABLED`, `SEMANTIC_CONFIDENCE_CHOICES`, `SESSION_DEFERRED_START_QUEUE_MAX`, `SESSION_HEARTBEAT_STALE_SECONDS`, `SESSION_SUBMIT_LOCK_TIMEOUT_SECONDS`, `SKILLS_VIRTUAL_PREFIX`, `SKILL_REFRESH_MIN_INTERVAL_SECONDS`, `SKILL_RUNTIME_CACHE_MAX_BYTES`, `SKILL_RUNTIME_CACHE_MAX_ENTRIES`, `STALL_ESCALATION_CONTEXT_MAX_CHARS`, `STALL_ESCALATION_MIN_LEVEL`, `STALL_PLAN_SYNTHESIS_MAX_TOKENS`, `STALL_SEVERITY_DECAY_ON_SUCCESS`, `STALL_SEVERITY_ESCALATION_THRESHOLD`, `STALL_SEVERITY_WEIGHT_BASH_READ_LOOP`, `STALL_SEVERITY_WEIGHT_FAULT`, `STALL_SEVERITY_WEIGHT_RECOVERY_RETRY`, `STALL_SEVERITY_WEIGHT_REPEATED_TOOL`, `STALL_SEVERITY_WEIGHT_WATCHDOG`, `TASK_COMPLEXITY_LEVELS`, `TASK_LEVEL_CHOICES`, `TASK_LEVEL_POLICIES`, `TASK_PHASE_ROUTING`, `TASK_PROFILE_TYPES`, `TASK_SCALE_PREFERENCES`, `THINKING_BUDGET_FORCE_RATIO`, `TOKEN_THRESHOLD`, `TRUNCATION_CONTINUATION_ECHO_CHARS`, `TRUNCATION_CONTINUATION_MAX_PASSES`, `TRUNCATION_CONTINUATION_MAX_TOKENS`, `TRUNCATION_CONTINUATION_TAIL_CHARS`, `TRUNCATION_LIVE_BUFFER_MAX_CHARS`, `TRUNCATION_OVERLAP_SCAN_CHARS`, `TRUNCATION_PAIR_SCAN_CHARS`, `VIDEO_EXTS`, `WATCHDOG_CONTEXT_NEAR_RATIO`, `WATCHDOG_CONTEXT_STALL_THRESHOLD`, `WATCHDOG_INTENT_NO_TOOL_THRESHOLD`, `WATCHDOG_INTENT_NO_TOOL_THRESHOLD_SINGLE`, `WATCHDOG_MAX_DECOMPOSE_STEPS`, `WATCHDOG_REPEAT_NO_TOOL_THRESHOLD`, `WATCHDOG_REPEAT_NO_TOOL_THRESHOLD_SINGLE`, `WATCHDOG_REPEAT_SIMILARITY_THRESHOLD`, `WATCHDOG_STATE_STALL_THRESHOLD`, `WATCHDOG_STEP_MAX_ATTEMPTS`, `_DEFAULT_TOOL_TIMEOUT`, `_SHELL_AUTO_CONFIRM_PATTERNS`, `_TOOL_TIMEOUT_MAP`; `config/paths.py`: `WORKDIR`; `config/settings.py`: `_detect_os_shell_instruction`, `_to_bool_like`, `backend_i18n_text`, `backend_role_label`, `default_multimodal_capabilities`, `infer_model_multimodal_capabilities`, `infer_user_complexity_value`, `looks_like_llm_config`, `max_task_complexity`, `merge_multimodal_capabilities`, `model_language_instruction`, `normalize_execution_mode`, `normalize_task_complexity`, `normalize_ui_language`, `parse_capability_overrides`, `parse_llm_config_profiles`, `task_complexity_at_least`, `task_complexity_rank`; `llm/client.py`: `OllamaClient`, `OllamaError`; `llm/utils.py`: `complete_chat_endpoint`, `extract_base_url`, `is_openai_compat_provider`, `list_loaded_ollama_models`, `list_ollama_models`, `list_ollama_models_cached`, `probe_ollama_environment`, `resolve_ollama_model`, `split_thinking_content`, `strip_thinking_content`, `wake_ollama_model`; `rag/parsers.py`: `build_code_preview_rows`, `is_code_preview_candidate`, `normalize_rel_preview_path`, `preview_kind_for_path`; `skills/store.py`: `SkillStore`, `ensure_runtime_skills`; `utils/compress.py`: `compress_text_blob`, `decompress_text_blob`; `utils/crypto.py`: `CryptoBox`; `utils/errors.py`: `CircuitBreakerTriggered`, `EmptyActionError`; `utils/files.py`: `_normalize_external_js_url`, `_safe_js_filename`, `cache_external_js_url`, `ensure_offline_js_libs`, `is_external_js_src`, `load_offline_js_lib_index`, `match_offline_js_catalog_by_url`, `offline_js_lib_root`, `safe_path`, `try_read_text`; `utils/http.py`: `urlopen`; `utils/json_utils.py`: `TOOLS`, `TOOL_REQUIRED_ARGS`, `canonicalize_tool_name`, `extract_json_object_from_text`, `json_dumps`, `parse_json_object`, `parse_tool_arguments_with_error`, `repair_truncated_json_object`, `tool_def`; `utils/media.py`: `_convert_image_to_safe_format`, `guess_ext_from_mime`, `guess_mime_from_name`; `utils/misc.py`: `MAX_TIMEOUT_SECONDS`, `MIN_TIMEOUT_SECONDS`, `is_benign_socket_error`, `make_id`, `normalize_timeout_seconds`, `now_ts`, `sanitize_profile_id`; `utils/text.py`: `MAX_TOOL_OUTPUT`, `_fmt_export_ts`, `_html_esc`, `_text_to_minimal_pdf`, `extract_todo_rows_from_text`, `filter_runtime_noise_lines`, `make_numbered_diff`, `make_unified_diff`, `normalize_embedded_newlines`, `normalize_work_text`, `parse_front_matter`, `render_numbered_diff_text`, `split_structured_todo_content`, `split_todo_status_text`, `trim`
- Symbols:
  - `SessionState` (class, lines 13689-40966)

### `skills/store.py`

- Routed symbols: 26
- Cross-module imports: `config/constants.py`: `BUILTIN_CLAWHUB_SKILLS_VERSION`, `EMBEDDED_CLAWHUB_SKILLS_ARCHIVE_B64`, `EMBEDDED_SKILLS_ARCHIVE_B64`, `EMBEDDED_SKILLS_ARCHIVE_FILES`, `EMBEDDED_SKILLS_ARCHIVE_SHA256`, `SKILLS_EXTERNAL_MOUNT`, `SKILLS_VIRTUAL_PREFIX`, `SKILL_BODY_COMPACT_THRESHOLD_CHARS`, `SKILL_BODY_PREVIEW_CHARS`, `SKILL_DEFAULT_ATTACHMENT_GLOBS`, `SKILL_INLINE_ATTACHMENT_MAX_CHARS`, `SKILL_INLINE_ATTACHMENT_MAX_FILES`, `SKILL_PROMPT_MAX_CHARS`, `SKILL_PROMPT_MAX_ITEMS`, `SKILL_PROTOCOL_CLAWHUB`, `SKILL_PROTOCOL_HTTP_JSON`, `SKILL_PROTOCOL_LOCAL`, `SKILL_PROTOCOL_SPECS`, `SKILL_REFRESH_MIN_INTERVAL_SECONDS`, `SKILL_RESOURCE_MANIFEST_MAX_ITEMS`; `config/paths.py`: `WORKDIR`; `llm/utils.py`: `_is_http_url`; `utils/files.py`: `_render_offline_js_catalog_md`, `safe_path`, `try_read_text`; `utils/http.py`: `urlopen`; `utils/json_utils.py`: `json_dumps`, `parse_json_object`; `utils/misc.py`: `_meta_string_list`, `_module_exists`, `now_ts`; `utils/text.py`: `parse_front_matter`, `trim`
- Symbols:
  - `ensure_embedded_skills_at_root` (function, lines 6514-6566)
  - `ensure_embedded_skills` (function, lines 6569-6570)
  - `detect_upload_parser_capabilities` (function, lines 6578-6593)
  - `_render_cap_markdown` (function, lines 6595-6609)
  - `_write_text_if_changed` (function, lines 6611-6616)
  - `ensure_generated_document_skills` (function, lines 6618-6706)
  - `ensure_generated_image_coding_feedback_skill` (function, lines 6708-6807)
  - `_skill_knowledge_files` (function, lines 6809-6828)
  - `analyze_skill_building_knowledge` (function, lines 6830-6884)
  - `_sanitize_skill_slug` (function, lines 6886-6888)
  - `_build_skills_gen_skill_content` (function, lines 6890-6921)
  - `ensure_generated_skills_gen_skill` (function, lines 6923-6927)
  - `ensure_generated_execution_recovery_skill` (function, lines 6929-7007)
  - `ensure_generated_systematic_debugging_skill` (function, lines 7009-7281)
  - `ensure_generated_code_engineering_mastery_skill` (function, lines 7283-7401)
  - `ensure_generated_smart_file_navigation_skill` (function, lines 7403-7521)
  - `ensure_generated_html_frontend_report_skills` (function, lines 7523-7730)
  - `ensure_generated_deep_research_skills` (function, lines 7732-8000)
  - `ensure_generated_research_scientific_skills` (function, lines 8002-8638)
  - `ensure_generated_rag_mastery_skills` (function, lines 8644-8940)
  - `ensure_generated_multimodal_comprehension_skills` (function, lines 8946-9635)
  - `ensure_generated_runtime_skills_manifest` (function, lines 9638-9669)
  - `ensure_embedded_clawhub_skills` (function, lines 9927-9964)
  - `ensure_runtime_skills` (function, lines 9966-9981)
  - `_BUILTIN_SKILLS` (assignment, lines 10023-10111)
  - `SkillStore` (class, lines 10120-11414)

### `utils/compress.py`

- Routed symbols: 2
- Cross-module imports: none
- Symbols:
  - `compress_text_blob` (function, lines 3257-3262)
  - `decompress_text_blob` (function, lines 3264-3272)

### `utils/crypto.py`

- Routed symbols: 1
- Cross-module imports: `utils/json_utils.py`: `json_dumps`
- Symbols:
  - `CryptoBox` (class, lines 4861-4978)

### `utils/errors.py`

- Routed symbols: 2
- Cross-module imports: none
- Symbols:
  - `EmptyActionError` (class, lines 3646-3647)
  - `CircuitBreakerTriggered` (class, lines 3650-3651)

### `utils/files.py`

- Routed symbols: 25
- Cross-module imports: `config/constants.py`: `OFFLINE_JS_LIB_CATALOG`, `OFFLINE_JS_LIB_INDEX_FILE`, `OFFLINE_JS_LIB_README_FILE`; `config/paths.py`: `WORKDIR`; `utils/http.py`: `urlopen`; `utils/json_utils.py`: `json_dumps`; `utils/misc.py`: `now_ts`; `utils/text.py`: `trim`
- Symbols:
  - `_normalize_js_lib_asset_ref` (function, lines 1360-1373)
  - `_resolve_js_lib_asset_path` (function, lines 1376-1405)
  - `_discover_extra_js_lib_files` (function, lines 1408-1438)
  - `safe_path` (function, lines 2634-2643)
  - `_safe_js_filename` (function, lines 2645-2652)
  - `_sha256_bytes` (function, lines 2654-2655)
  - `_sha256_file` (function, lines 2657-2665)
  - `_download_http_bytes` (function, lines 2667-2675)
  - `offline_js_lib_root` (function, lines 2677-2678)
  - `_offline_js_entry_relative_path` (function, lines 2680-2684)
  - `_archive_member_relative_path` (function, lines 2686-2695)
  - `_path_size_bytes` (function, lines 2697-2712)
  - `_extract_archive_to_dir` (function, lines 2714-2754)
  - `_package_required_paths` (function, lines 2756-2762)
  - `_package_install_ready` (function, lines 2764-2772)
  - `_postprocess_offline_js_package` (function, lines 2774-2809)
  - `_ensure_offline_js_package` (function, lines 2811-2850)
  - `_render_offline_js_catalog_md` (function, lines 2852-2868)
  - `load_offline_js_lib_index` (function, lines 2870-2879)
  - `ensure_offline_js_libs` (function, lines 2881-3025)
  - `_normalize_external_js_url` (function, lines 3027-3031)
  - `is_external_js_src` (function, lines 3033-3035)
  - `match_offline_js_catalog_by_url` (function, lines 3037-3053)
  - `cache_external_js_url` (function, lines 3055-3087)
  - `try_read_text` (function, lines 5183-5191)

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
  - `JSON_FSYNC_ENABLED` (constant, lines 145-145)
  - `json_dumps` (function, lines 2606-2607)
  - `parse_tool_arguments` (function, lines 3525-3534)
  - `repair_truncated_json_object` (function, lines 3536-3589)
  - `parse_tool_arguments_with_error` (function, lines 3591-3621)
  - `parse_json_object` (function, lines 3887-3892)
  - `extract_json_object_from_text` (function, lines 3894-3916)
  - `_json_default_copy` (function, lines 5193-5198)
  - `_read_json_file` (function, lines 5200-5220)
  - `_write_json_file` (function, lines 5222-5249)
  - `tool_def` (function, lines 13393-13405)
  - `TOOLS` (constant, lines 13407-13589)
  - `TOOL_REQUIRED_ARGS` (constant, lines 13591-13591)
  - `TOOL_SPEC_BY_NAME` (constant, lines 13592-13592)
  - `TOOL_NAME_FUZZY_MAP` (constant, lines 13604-13604)
  - `canonicalize_tool_name` (function, lines 13622-13633)

### `utils/media.py`

- Routed symbols: 3
- Cross-module imports: none
- Symbols:
  - `guess_mime_from_name` (function, lines 2446-2448)
  - `_convert_image_to_safe_format` (function, lines 2451-2468)
  - `guess_ext_from_mime` (function, lines 2471-2477)

### `utils/misc.py`

- Routed symbols: 19
- Cross-module imports: none
- Symbols:
  - `MIN_TIMEOUT_SECONDS` (constant, lines 357-357)
  - `MAX_TIMEOUT_SECONDS` (constant, lines 358-358)
  - `DEFAULT_TIMEOUT_SECONDS` (constant, lines 359-365)
  - `BENIGN_SOCKET_DEBUG_LOG_ENABLED` (constant, lines 488-494)
  - `BENIGN_SOCKET_LOG_INTERVAL_SECONDS` (constant, lines 495-495)
  - `now_ts` (function, lines 2479-2480)
  - `_benign_socket_log_lock` (assignment, lines 2483-2483)
  - `_benign_socket_log_state` (assignment, lines 2484-2484)
  - `is_benign_socket_error` (function, lines 2502-2520)
  - `_socket_error_code` (function, lines 2523-2532)
  - `_log_benign_socket_error_limited` (function, lines 2535-2569)
  - `swallow_benign_socket_error` (function, lines 2572-2576)
  - `normalize_timeout_seconds` (function, lines 2579-2592)
  - `detect_local_lan_ip` (function, lines 2594-2604)
  - `make_id` (function, lines 2609-2610)
  - `sanitize_profile_id` (function, lines 2612-2614)
  - `user_id_from_ip` (function, lines 4853-4859)
  - `_meta_string_list` (function, lines 5170-5181)
  - `_module_exists` (function, lines 6572-6576)

### `utils/text.py`

- Routed symbols: 23
- Cross-module imports: `config/constants.py`: `CODE_PREVIEW_DIFF_CONTEXT_LINES`, `CODE_PREVIEW_DIFF_MERGE_GAP`
- Symbols:
  - `MAX_TOOL_OUTPUT` (constant, lines 137-137)
  - `SOCKET_NOISE_LINE_PATTERNS` (constant, lines 482-487)
  - `filter_runtime_noise_lines` (function, lines 2487-2499)
  - `trim` (function, lines 3089-3091)
  - `_fmt_export_ts` (function, lines 3094-3102)
  - `_html_esc` (function, lines 3105-3106)
  - `_text_to_minimal_pdf` (function, lines 3109-3255)
  - `normalize_embedded_newlines` (function, lines 3274-3282)
  - `_map_todo_status_token` (function, lines 3285-3300)
  - `split_todo_status_text` (function, lines 3303-3358)
  - `extract_todo_rows_from_text` (function, lines 3361-3428)
  - `infer_todo_status_from_text` (function, lines 3431-3437)
  - `split_structured_todo_content` (function, lines 3440-3493)
  - `normalize_work_text` (function, lines 3496-3523)
  - `parse_front_matter` (function, lines 4980-5167)
  - `make_unified_diff` (function, lines 5251-5268)
  - `_skip_row` (function, lines 5270-5274)
  - `_row_is_hot` (function, lines 5277-5278)
  - `_hotspot_index` (function, lines 5281-5302)
  - `_compress_rows_keep_hotspot` (function, lines 5305-5352)
  - `_focused_diff_rows_from_opcodes` (function, lines 5355-5487)
  - `make_numbered_diff` (function, lines 5490-5520)
  - `render_numbered_diff_text` (function, lines 5522-5534)
