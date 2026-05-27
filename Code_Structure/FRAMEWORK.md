# Code_Structure Framework

## Overview

- Source file: `/Users/Fona/Downloads/Clouds_Coder/Clouds_Coder.py`
- Output directory: `/Users/Fona/Downloads/Clouds_Coder/Code_Structure`
- Generated modules: 30
- Top-level symbols: 610
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
| `config/constants.py` | 355 | `utils/json_utils.py`, `utils/misc.py` |
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
  - `main` (function, lines 67133-68114)
  - `_main_guard_68116` (main_guard, lines 68116-68117)

### `agent/background.py`

- Routed symbols: 1
- Cross-module imports: `utils/misc.py`: `make_id`, `now_ts`; `utils/text.py`: `trim`
- Symbols:
  - `BackgroundManager` (class, lines 11567-11647)

### `agent/bus.py`

- Routed symbols: 1
- Cross-module imports: `config/constants.py`: `VALID_MSG_TYPES`; `utils/crypto.py`: `CryptoBox`; `utils/misc.py`: `now_ts`
- Symbols:
  - `MessageBus` (class, lines 11649-11713)

### `agent/events.py`

- Routed symbols: 1
- Cross-module imports: none
- Symbols:
  - `EventHub` (class, lines 5668-5713)

### `agent/tasks.py`

- Routed symbols: 1
- Cross-module imports: `utils/crypto.py`: `CryptoBox`; `utils/json_utils.py`: `json_dumps`; `utils/misc.py`: `now_ts`
- Symbols:
  - `TaskManager` (class, lines 11439-11565)

### `agent/todo.py`

- Routed symbols: 1
- Cross-module imports: `config/constants.py`: `DEFAULT_UI_LANGUAGE`; `config/settings.py`: `backend_i18n_text`, `backend_role_label`, `normalize_ui_language`; `utils/text.py`: `infer_todo_status_from_text`, `normalize_work_text`, `split_structured_todo_content`, `trim`
- Symbols:
  - `TodoManager` (class, lines 5715-5984)

### `agent/worktree.py`

- Routed symbols: 1
- Cross-module imports: `agent/tasks.py`: `TaskManager`; `config/constants.py`: `DANGEROUS_PATTERNS`; `utils/crypto.py`: `CryptoBox`; `utils/json_utils.py`: `json_dumps`; `utils/misc.py`: `now_ts`; `utils/text.py`: `trim`
- Symbols:
  - `WorktreeManager` (class, lines 11715-11930)

### `app/context.py`

- Routed symbols: 1
- Cross-module imports: `config/constants.py`: `AGENT_MAX_OUTPUT_TOKENS`, `APP_CSS`, `APP_JS`, `APP_TS`, `ARBITER_DEFAULT_MAX_TOKENS`, `ARBITER_DEFAULT_TEMPERATURE`, `ARBITER_DEFAULT_TIMEOUT_SECONDS`, `CODE_ADMIN_CSS`, `CODE_ADMIN_INDEX_HTML`, `CODE_ADMIN_JS`, `CODE_IMPORT_WORKER_COUNT`, `CODE_LIBRARY_DIRNAME`, `CODE_PARSE_TIMEOUT_SECONDS`, `DEFAULT_REQUEST_TIMEOUT`, `DEFAULT_SHELL_COMMAND_TIMEOUT_SECONDS`, `DEFAULT_UI_LANGUAGE`, `DEFAULT_UI_STYLE`, `DEFAULT_WEB_UI_DIR`, `EXECUTION_MODE_SYNC`, `INDEX_HTML`, `MAX_AGENT_ROUNDS`, `MAX_AGENT_ROUNDS_CAP`, `MAX_RUN_SECONDS`, `MAX_RUN_TIMEOUT_SECONDS`, `MAX_SHELL_COMMAND_TIMEOUT_SECONDS`, `MIN_AGENT_ROUNDS`, `MIN_CONTEXT_TOKEN_LIMIT`, `MIN_RUN_TIMEOUT_SECONDS`, `MIN_SHELL_COMMAND_TIMEOUT_SECONDS`, `RAG_ADMIN_CSS`, `RAG_ADMIN_INDEX_HTML`, `RAG_ADMIN_JS`, `RAG_CONTEXT_BUDGETS`, `RAG_DENSE_DEFAULT_ENABLED`, `RAG_EMBEDDING_MODE_VALUES`, `RAG_GRAPH_MAX_NODES`, `RAG_HIGH_RECALL_MIN_POOL`, `RAG_HIGH_RECALL_POOL_MULTIPLIER`, `RAG_IMPORT_WORKER_COUNT`, `RAG_INCLUDE_FILENAME_ENTITIES_DEFAULT`, `RAG_LIBRARY_DIRNAME`, `RAG_MAX_GLOBAL_COMMUNITIES`, `RAG_MAX_IMPORT_BATCH_BYTES`, `RAG_MAX_IMPORT_BATCH_ITEMS`, `RAG_MAX_IMPORT_FILES`, `RAG_MAX_QUERY_RESULTS`, `RAG_MIN_SYNTHESIS_SCORE`, `RAG_NO_EVIDENCE_MESSAGE`, `RAG_NO_EVIDENCE_THRESHOLD`, `RAG_PARSE_TIMEOUT_SECONDS`, `RAG_QUERY_CONTEXT_CHARS`, `RAG_RETRIEVAL_MAX_PER_DOC`, `RAG_SYNTHESIS_MAX_PER_DOC`, `RAG_WEAK_EVIDENCE_MESSAGE`, `RAG_WEAK_MATCH_SCORE_CAP`, `SESSION_HEARTBEAT_STALE_SECONDS`, `SESSION_WATCHDOG_INTERVAL_SECONDS`, `SKILLS_APP_JS`, `SKILLS_EXTRA_CSS`, `SKILLS_INDEX_HTML`, `SKILL_REFRESH_MIN_INTERVAL_SECONDS`, `TOKEN_THRESHOLD`, `WEB_UI_OPTIONAL_FILES`, `WEB_UI_REQUIRED_FILES`; `config/paths.py`: `LLM_CONFIG_PATH`, `REPO_ROOT`, `_migrate_legacy_runtime_roots`; `config/settings.py`: `_to_bool_like`, `default_multimodal_capabilities`, `infer_model_multimodal_capabilities`, `merge_multimodal_capabilities`, `model_language_instruction`, `normalize_execution_mode`, `normalize_ui_language`, `normalize_ui_style`, `parse_capability_overrides`, `parse_llm_config_profiles`, `resolve_optional_file_path`, `resolve_web_ui_dir_path`; `llm/client.py`: `OllamaClient`; `llm/utils.py`: `extract_base_url`, `list_ollama_models_cached`; `rag/ingestion.py`: `CodeIngestionService`, `RAGIngestionService`, `_rag_embed_batch`, `_rag_embed_text`, `_rag_mmr_select`, `_rag_query_variants`; `rag/parsers.py`: `CodeContentParser`, `RAGContentParser`; `rag/store.py`: `CodeLibraryStore`, `RAGLibraryStore`, `WikiStore`, `WorkflowMemoryStore`; `session/manager.py`: `SessionCreationLimitExceeded`, `SessionManager`; `session/state.py`: `SessionState`; `skills/store.py`: `SkillStore`, `_sanitize_skill_slug`, `analyze_skill_building_knowledge`, `ensure_runtime_skills`; `utils/crypto.py`: `CryptoBox`; `utils/files.py`: `_resolve_js_lib_asset_path`, `ensure_offline_js_libs`, `load_offline_js_lib_index`, `offline_js_lib_root`, `safe_path`, `try_read_text`; `utils/json_utils.py`: `TOOLS`, `extract_json_object_from_text`, `json_dumps`, `parse_json_object`; `utils/misc.py`: `DEFAULT_TIMEOUT_SECONDS`, `MAX_TIMEOUT_SECONDS`, `MIN_TIMEOUT_SECONDS`, `normalize_timeout_seconds`, `now_ts`, `sanitize_profile_id`; `utils/text.py`: `parse_front_matter`, `trim`
- Symbols:
  - `AppContext` (class, lines 62258-65621)

### `config/constants.py`

- Routed symbols: 355
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
  - `READ_FILE_LOOP_THRESHOLD` (constant, lines 345-345)
  - `READ_FILE_LOOP_DISTINCT_SOFT_LIMIT` (constant, lines 346-346)
  - `READ_FILE_COMPACT_PIN_DISTINCT` (constant, lines 347-347)
  - `READ_FILE_COMPACT_PIN_MAX_CHARS` (constant, lines 348-348)
  - `READ_CONTEXT_REGISTRY_MAX` (constant, lines 349-349)
  - `READ_CONTEXT_PROMPT_MAX_ITEMS` (constant, lines 350-350)
  - `READ_CONTEXT_PROMPT_MAX_CHARS` (constant, lines 351-351)
  - `READ_CONTEXT_SUMMARY_MAX_CHARS` (constant, lines 352-352)
  - `READ_CONTEXT_SHARED_MAX_ITEMS` (constant, lines 353-353)
  - `HARD_BREAK_TOOL_ERROR_THRESHOLD` (constant, lines 354-354)
  - `HARD_BREAK_RECOVERY_ROUND_THRESHOLD` (constant, lines 355-355)
  - `FUSED_FAULT_BREAK_THRESHOLD` (constant, lines 356-356)
  - `STALL_SEVERITY_ESCALATION_THRESHOLD` (constant, lines 357-357)
  - `STALL_SEVERITY_WEIGHT_BASH_READ_LOOP` (constant, lines 358-358)
  - `STALL_SEVERITY_WEIGHT_REPEATED_TOOL` (constant, lines 359-359)
  - `STALL_SEVERITY_WEIGHT_FAULT` (constant, lines 360-360)
  - `STALL_SEVERITY_WEIGHT_RECOVERY_RETRY` (constant, lines 361-361)
  - `STALL_SEVERITY_WEIGHT_WATCHDOG` (constant, lines 362-362)
  - `STALL_SEVERITY_DECAY_ON_SUCCESS` (constant, lines 363-363)
  - `STALL_ESCALATION_MIN_LEVEL` (constant, lines 364-364)
  - `STALL_PLAN_SYNTHESIS_MAX_TOKENS` (constant, lines 365-365)
  - `STALL_ESCALATION_CONTEXT_MAX_CHARS` (constant, lines 366-366)
  - `MAX_RUN_SECONDS` (constant, lines 367-367)
  - `MIN_RUN_TIMEOUT_SECONDS` (constant, lines 368-368)
  - `MAX_RUN_TIMEOUT_SECONDS` (constant, lines 369-369)
  - `DEFAULT_REQUEST_TIMEOUT` (constant, lines 379-379)
  - `_SHELL_AUTO_CONFIRM_PATTERNS` (assignment, lines 382-395)
  - `MIN_SHELL_COMMAND_TIMEOUT_SECONDS` (constant, lines 396-396)
  - `MAX_SHELL_COMMAND_TIMEOUT_SECONDS` (constant, lines 397-397)
  - `DEFAULT_SHELL_COMMAND_TIMEOUT_SECONDS` (constant, lines 398-412)
  - `AUTO_CONTINUE_BUDGET_DEFAULT` (constant, lines 413-413)
  - `AGENT_MAX_OUTPUT_TOKENS` (constant, lines 414-414)
  - `OLLAMA_THINKING_TOOL_BUFFER` (constant, lines 415-415)
  - `WATCHDOG_INTENT_NO_TOOL_THRESHOLD` (constant, lines 416-416)
  - `WATCHDOG_REPEAT_NO_TOOL_THRESHOLD` (constant, lines 417-417)
  - `WATCHDOG_INTENT_NO_TOOL_THRESHOLD_SINGLE` (constant, lines 418-418)
  - `WATCHDOG_REPEAT_NO_TOOL_THRESHOLD_SINGLE` (constant, lines 419-419)
  - `WATCHDOG_STATE_STALL_THRESHOLD` (constant, lines 420-420)
  - `WATCHDOG_CONTEXT_STALL_THRESHOLD` (constant, lines 421-421)
  - `WATCHDOG_REPEAT_SIMILARITY_THRESHOLD` (constant, lines 422-422)
  - `WATCHDOG_CONTEXT_NEAR_RATIO` (constant, lines 423-423)
  - `WATCHDOG_MAX_DECOMPOSE_STEPS` (constant, lines 424-424)
  - `WATCHDOG_STEP_MAX_ATTEMPTS` (constant, lines 425-425)
  - `EMPTY_ACTION_MIN_CONTENT_CHARS` (constant, lines 426-426)
  - `EMPTY_ACTION_WAKEUP_RETRY_LIMIT` (constant, lines 427-427)
  - `THINKING_BUDGET_FORCE_RATIO` (constant, lines 428-428)
  - `_TOOL_TIMEOUT_MAP` (assignment, lines 430-446)
  - `_DEFAULT_TOOL_TIMEOUT` (assignment, lines 447-447)
  - `TRUNCATION_CONTINUATION_MAX_PASSES` (constant, lines 448-448)
  - `TRUNCATION_CONTINUATION_MAX_TOKENS` (constant, lines 449-449)
  - `TRUNCATION_CONTINUATION_TAIL_CHARS` (constant, lines 450-450)
  - `TRUNCATION_CONTINUATION_ECHO_CHARS` (constant, lines 451-451)
  - `TRUNCATION_OVERLAP_SCAN_CHARS` (constant, lines 452-452)
  - `TRUNCATION_PAIR_SCAN_CHARS` (constant, lines 453-453)
  - `TRUNCATION_LIVE_BUFFER_MAX_CHARS` (constant, lines 454-454)
  - `MIN_CONTEXT_TOKEN_LIMIT` (constant, lines 455-455)
  - `COMPACT_TIER1_PCT` (constant, lines 457-457)
  - `COMPACT_TIER2_PCT` (constant, lines 458-458)
  - `COMPACT_TIER3_PCT` (constant, lines 459-459)
  - `COMPACT_TIER1_ABS` (constant, lines 461-461)
  - `COMPACT_TIER2_ABS` (constant, lines 462-462)
  - `CONTEXT_COMPACT_INEFFECTIVE_COOLDOWN_SECONDS` (constant, lines 463-469)
  - `FILE_BUFFER_CONTENT_THRESHOLD` (constant, lines 471-471)
  - `FILE_BUFFER_MAX_FILES` (constant, lines 472-472)
  - `AGENT_MSG_LIMIT_TIER0` (constant, lines 474-474)
  - `AGENT_MSG_LIMIT_TIER1` (constant, lines 475-475)
  - `AGENT_MSG_LIMIT_TIER2` (constant, lines 476-476)
  - `AGENT_MSG_LIMIT_TIER3` (constant, lines 477-477)
  - `AGENT_CTX_LIMIT_TIER0` (constant, lines 478-478)
  - `AGENT_CTX_LIMIT_TIER1` (constant, lines 479-479)
  - `AGENT_CTX_LIMIT_TIER2` (constant, lines 480-480)
  - `AGENT_CTX_LIMIT_TIER3` (constant, lines 481-481)
  - `MANAGER_CTX_LIMIT_TIER0` (constant, lines 482-482)
  - `MANAGER_CTX_LIMIT_TIER1` (constant, lines 483-483)
  - `MANAGER_CTX_LIMIT_TIER2` (constant, lines 484-484)
  - `MANAGER_CTX_LIMIT_TIER3` (constant, lines 485-485)
  - `MAX_CONTEXT_ARCHIVE_SEGMENTS` (constant, lines 486-486)
  - `MODEL_OUTPUT_RETRY_TIMES` (constant, lines 487-487)
  - `ARBITER_TRIGGER_MIN_CONTENT_CHARS` (constant, lines 488-488)
  - `ARBITER_VALID_PLANNING_STREAK_LIMIT` (constant, lines 489-489)
  - `ARBITER_DEFAULT_TIMEOUT_SECONDS` (constant, lines 490-490)
  - `ARBITER_DEFAULT_MAX_TOKENS` (constant, lines 491-491)
  - `ARBITER_DEFAULT_TEMPERATURE` (constant, lines 492-492)
  - `LIVE_INPUT_DELAY_WRITE_ROUNDS` (constant, lines 493-493)
  - `LIVE_INPUT_DELAY_TOOL_ROUNDS` (constant, lines 494-494)
  - `LIVE_INPUT_DELAY_NORMAL_ROUNDS` (constant, lines 495-495)
  - `LIVE_INPUT_MAX_INJECTIONS` (constant, lines 496-496)
  - `LIVE_INPUT_REINJECT_INTERVAL` (constant, lines 497-497)
  - `LIVE_INPUT_WEIGHT_BASE_DELAYED` (constant, lines 498-498)
  - `LIVE_INPUT_WEIGHT_BASE_NORMAL` (constant, lines 499-499)
  - `LIVE_INPUT_WEIGHT_STEP_DELAYED` (constant, lines 500-500)
  - `LIVE_INPUT_WEIGHT_STEP_NORMAL` (constant, lines 501-501)
  - `FINAL_SUMMARY_MIN_CHARS` (constant, lines 516-516)
  - `FINAL_SUMMARY_STRICT_MIN_CHARS` (constant, lines 517-517)
  - `RUNTIME_CONTROL_HINT_PREFIXES` (constant, lines 518-535)
  - `RETRY_RUNTIME_HINT_PREFIXES` (constant, lines 536-550)
  - `EXECUTION_MODE_SINGLE` (constant, lines 551-551)
  - `EXECUTION_MODE_SEQUENTIAL` (constant, lines 552-552)
  - `EXECUTION_MODE_SYNC` (constant, lines 553-553)
  - `EXECUTION_MODE_CHOICES` (constant, lines 554-558)
  - `AGENT_ROLES` (constant, lines 559-559)
  - `AGENT_BUBBLE_ROLES` (constant, lines 560-560)
  - `AGENT_ROLE_LABELS` (constant, lines 561-567)
  - `AGENT_ROLE_BUBBLE_COLORS` (constant, lines 568-574)
  - `BLACKBOARD_STATUSES` (constant, lines 575-584)
  - `TASK_COMPLEXITY_LEVELS` (constant, lines 585-585)
  - `TASK_COMPLEXITY_RANKS` (constant, lines 586-591)
  - `TASK_PROFILE_TYPES` (constant, lines 592-598)
  - `TASK_LEVEL_CHOICES` (constant, lines 599-599)
  - `TASK_SCALE_PREFERENCES` (constant, lines 600-600)
  - `SEMANTIC_CONFIDENCE_CHOICES` (constant, lines 601-601)
  - `TASK_LEVEL_POLICIES` (constant, lines 602-648)
  - `MANAGER_ROUTE_TARGETS` (constant, lines 649-649)
  - `BLACKBOARD_MAX_LOG_ENTRIES` (constant, lines 650-650)
  - `BLACKBOARD_MAX_TEXT` (constant, lines 651-651)
  - `SKILL_REFRESH_MIN_INTERVAL_SECONDS` (constant, lines 652-652)
  - `SKILL_PROMPT_MAX_ITEMS` (constant, lines 653-653)
  - `SKILL_PROMPT_MAX_CHARS` (constant, lines 654-654)
  - `SKILL_RUNTIME_CACHE_MAX_ENTRIES` (constant, lines 655-655)
  - `SKILL_RUNTIME_CACHE_MAX_BYTES` (constant, lines 656-656)
  - `AUTO_SKILLS_ROOT_CANDIDATES` (constant, lines 657-657)
  - `SKILL_DEFAULT_ATTACHMENT_GLOBS` (constant, lines 658-688)
  - `SKILL_INLINE_ATTACHMENT_MAX_FILES` (constant, lines 689-689)
  - `SKILL_INLINE_ATTACHMENT_MAX_CHARS` (constant, lines 690-690)
  - `SKILL_RESOURCE_MANIFEST_MAX_ITEMS` (constant, lines 691-691)
  - `SKILL_BODY_COMPACT_THRESHOLD_CHARS` (constant, lines 692-692)
  - `SKILL_BODY_PREVIEW_CHARS` (constant, lines 693-693)
  - `SKILLS_VIRTUAL_PREFIX` (constant, lines 694-694)
  - `SKILLS_EXTERNAL_MOUNT` (constant, lines 695-695)
  - `PLAN_MODE_ENABLED_LEVELS` (constant, lines 696-696)
  - `PLAN_MODE_FORCED_LEVELS` (constant, lines 697-697)
  - `PLAN_MODE_USER_CHOICES` (constant, lines 698-698)
  - `TASK_PHASES` (constant, lines 700-700)
  - `TASK_PHASE_ROUTING` (constant, lines 701-708)
  - `COMPLEXITY_KEYWORDS` (constant, lines 710-715)
  - `USER_COMPLEXITY_SIMPLE_TOKENS` (constant, lines 716-720)
  - `USER_COMPLEXITY_MODERATE_TOKENS` (constant, lines 721-725)
  - `USER_COMPLEXITY_COMPLEX_TOKENS` (constant, lines 726-730)
  - `USER_COMPLEXITY_EXPERT_TOKENS` (constant, lines 731-735)
  - `PLAN_MODE_EXPLORER_MAX_ROUNDS` (constant, lines 736-736)
  - `PLAN_MODE_SYNTHESIS_MAX_ATTEMPTS` (constant, lines 737-737)
  - `REVIEWER_DEBUG_MODE_MAX_ROUNDS` (constant, lines 739-739)
  - `REVIEWER_DEBUG_TOOL_ALLOWLIST` (constant, lines 740-744)
  - `EXPLORER_STALL_THRESHOLD` (constant, lines 745-745)
  - `DEVELOPER_EDIT_STALL_THRESHOLD` (constant, lines 746-746)
  - `PLAN_MODE_MANAGER_SYNTHESIS_MAX_TOKENS` (constant, lines 747-747)
  - `PLAN_MODE_MAX_OPTIONS` (constant, lines 748-748)
  - `PLAN_FILE_RELATIVE_PATH` (constant, lines 749-749)
  - `PLAN_BUBBLE_MAX_CHARS` (constant, lines 750-750)
  - `PLAN_NOTICE_BODY_MAX_CHARS` (constant, lines 751-751)
  - `PLAN_MESSAGE_EVENT_MAX_CHARS` (constant, lines 752-752)
  - `PLAN_STEP_FULL_CONTENT_MAX_CHARS` (constant, lines 753-753)
  - `PLAN_MODE_RESEARCH_TOOL_ALLOWLIST` (constant, lines 754-758)
  - `FAILURE_LEDGER_MAX_FIXES` (constant, lines 759-759)
  - `FAILURE_LEDGER_MAX_COMPILE_ERRORS` (constant, lines 760-760)
  - `FAILURE_LEDGER_MAX_DELEGATIONS` (constant, lines 761-761)
  - `FAILURE_LEDGER_MAX_STALLS` (constant, lines 762-762)
  - `FAILURE_LEDGER_MAX_TOOL_FPS` (constant, lines 763-763)
  - `FAILURE_LEDGER_MAX_ERRORS` (constant, lines 764-764)
  - `ERROR_CATEGORY_DEFS` (constant, lines 767-804)
  - `CHECKPOINT_MAX_COUNT` (constant, lines 805-805)
  - `CHECKPOINT_INTERVAL_ROUNDS` (constant, lines 806-806)
  - `PERSISTED_ROUTES_MAX` (constant, lines 807-807)
  - `HTML_FRONTEND_REQUEST_KEYWORDS` (constant, lines 808-847)
  - `DEEP_RESEARCH_REQUEST_KEYWORDS` (constant, lines 848-870)
  - `DEEP_RESEARCH_RETRIEVAL_KEYWORDS` (constant, lines 871-890)
  - `DEEP_RESEARCH_TEXT_ONLY_HINT_KEYWORDS` (constant, lines 891-908)
  - `DANGEROUS_PATTERNS` (constant, lines 910-910)
  - `VALID_MSG_TYPES` (constant, lines 911-917)
  - `SUPPORTED_UI_LANGUAGES` (constant, lines 919-924)
  - `UI_LANGUAGE_LABELS` (constant, lines 925-925)
  - `DEFAULT_UI_LANGUAGE` (constant, lines 926-926)
  - `UI_STYLE_CHOICES` (constant, lines 927-927)
  - `UI_STYLE_LABELS` (constant, lines 928-928)
  - `DEFAULT_UI_STYLE` (constant, lines 929-929)
  - `DEFAULT_WEB_UI_DIR` (constant, lines 930-930)
  - `DEFAULT_WEB_UI_CONFIG` (constant, lines 931-931)
  - `WEB_UI_REQUIRED_FILES` (constant, lines 932-939)
  - `WEB_UI_OPTIONAL_FILES` (constant, lines 940-940)
  - `IMAGE_EXTS` (constant, lines 942-955)
  - `IMAGE_FORMATS_NEED_CONVERSION` (constant, lines 956-956)
  - `IMAGE_SAFE_FORMATS` (constant, lines 957-957)
  - `AUDIO_EXTS` (constant, lines 958-968)
  - `VIDEO_EXTS` (constant, lines 969-979)
  - `CODE_PREVIEW_STAGE_MAX_BYTES` (constant, lines 980-980)
  - `CODE_PREVIEW_STAGE_MAX_ROWS` (constant, lines 981-981)
  - `CODE_PREVIEW_STAGE_MAX_PER_FILE` (constant, lines 982-982)
  - `CODE_PREVIEW_STAGE_MAX_TOTAL` (constant, lines 983-983)
  - `CODE_PREVIEW_DIFF_CONTEXT_LINES` (constant, lines 984-984)
  - `CODE_PREVIEW_DIFF_MERGE_GAP` (constant, lines 985-985)
  - `PREVIEW_DOWNLOAD_MAX_FILES` (constant, lines 986-986)
  - `PREVIEW_DOWNLOAD_MAX_BYTES` (constant, lines 987-987)
  - `RENDER_FRAME_MAX_B64_CHARS` (constant, lines 988-988)
  - `RENDER_FRAME_MAX_POINTS` (constant, lines 989-989)
  - `RENDER_FRAME_MAX_LINES` (constant, lines 990-990)
  - `RENDER_FRAME_MAX_LINE_POINTS` (constant, lines 991-991)
  - `RENDER_FRAME_ACTIVITY_INTERVAL_SECONDS` (constant, lines 992-992)
  - `RAW_TOOLCALL_TEXT_FILTER_THRESHOLD` (constant, lines 993-993)
  - `ASSISTANT_TEXT_PERSIST_MAX_CHARS` (constant, lines 994-994)
  - `ASSISTANT_MESSAGE_EVENT_MAX_CHARS` (constant, lines 995-995)
  - `CODE_PREVIEW_EXTS` (constant, lines 996-1085)
  - `CODE_PREVIEW_FILENAMES` (constant, lines 1086-1097)
  - `MEDIA_CAPABILITY_KEYS` (constant, lines 1098-1105)
  - `SAMPLE_IMAGE_PNG_B64` (constant, lines 1106-1109)
  - `SAMPLE_AUDIO_WAV_B64` (constant, lines 1110-1112)
  - `SAMPLE_VIDEO_MP4_B64` (constant, lines 1113-1115)
  - `OFFLINE_JS_LIB_CATALOG` (constant, lines 1117-1375)
  - `OFFLINE_JS_LIB_INDEX_FILE` (constant, lines 1376-1376)
  - `OFFLINE_JS_LIB_README_FILE` (constant, lines 1377-1377)
  - `BACKEND_I18N` (constant, lines 1563-1632)
  - `call_backend_i18n_en_update_l1634` (expression, lines 1634-1727)
  - `call_backend_i18n_zh_cn_update_l1728` (expression, lines 1728-1821)
  - `call_backend_i18n_zh_tw_update_l1822` (expression, lines 1822-1915)
  - `call_backend_i18n_ja_update_l1916` (expression, lines 1916-2009)
  - `OPENAI_COMPAT_PROVIDER_NAMES` (constant, lines 4041-4049)
  - `OPENAI_LIKE_PROVIDER_NAMES` (constant, lines 4051-4051)
  - `TABULAR_PREVIEW_EXTS` (constant, lines 5582-5582)
  - `EXCEL_PREVIEW_EXTS` (constant, lines 5583-5583)
  - `PRESENTATION_PREVIEW_EXTS` (constant, lines 5584-5584)
  - `DOCUMENT_PREVIEW_EXTS` (constant, lines 5585-5585)
  - `EMBEDDED_SKILLS_ARCHIVE_B64` (constant, lines 5986-6505)
  - `EMBEDDED_SKILLS_ARCHIVE_SHA256` (constant, lines 6506-6506)
  - `EMBEDDED_SKILLS_ARCHIVE_FILES` (constant, lines 6507-6530)
  - `BUILTIN_CLAWHUB_SKILLS_VERSION` (constant, lines 9687-9687)
  - `EMBEDDED_CLAWHUB_SKILLS_ARCHIVE_B64` (constant, lines 9689-9933)
  - `SKILL_PROTOCOL_LOCAL` (constant, lines 9999-9999)
  - `SKILL_PROTOCOL_CLAWHUB` (constant, lines 10000-10000)
  - `SKILL_PROTOCOL_HTTP_JSON` (constant, lines 10001-10001)
  - `SKILL_PROTOCOL_SPECS` (constant, lines 10003-10034)
  - `AGENT_TOOL_ALLOWLIST` (constant, lines 13778-13821)
  - `INDEX_HTML` (constant, lines 44201-44390)
  - `APP_CSS` (constant, lines 44392-44804)
  - `APP_JS` (constant, lines 44806-48123)
  - `APP_TS` (constant, lines 48125-48152)
  - `SKILLS_INDEX_HTML` (constant, lines 48154-48308)
  - `SKILLS_EXTRA_CSS` (constant, lines 48310-48405)
  - `SKILLS_APP_JS` (constant, lines 48407-48548)
  - `RAG_TERM_GROUPS` (constant, lines 48550-53182)
  - `RAG_RESEARCH_HINTS` (constant, lines 53183-53204)
  - `RAG_CODE_HINTS` (constant, lines 53205-53215)
  - `RAG_SHORT_TOKEN_ALLOWLIST` (constant, lines 53216-53231)
  - `RAG_EN_STOPWORDS` (constant, lines 53232-53304)
  - `RAG_ZH_STOPWORDS` (constant, lines 53305-53341)
  - `RAG_GENERIC_ENTITY_TERMS_EN` (constant, lines 53342-53420)
  - `RAG_GENERIC_ENTITY_TERMS_ZH` (constant, lines 53421-53463)
  - `RAG_STRUCTURAL_ENTITY_PATTERNS` (constant, lines 53464-53482)
  - `CODE_LIBRARY_IGNORED_DIRS` (constant, lines 54175-54180)
  - `CODE_LIBRARY_LANGUAGE_BY_EXT` (constant, lines 54181-54237)
  - `CODE_LIBRARY_SPECIAL_FILENAMES` (constant, lines 54238-54244)
  - `RAG_ADMIN_INDEX_HTML` (constant, lines 60168-60341)
  - `RAG_ADMIN_CSS` (constant, lines 60343-60433)
  - `RAG_ADMIN_JS` (constant, lines 60435-62198)
  - `CODE_ADMIN_INDEX_HTML` (constant, lines 62200-62211)
  - `CODE_ADMIN_CSS` (constant, lines 62212-62242)
  - `CODE_ADMIN_JS` (constant, lines 62243-62247)

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
  - `detect_repo_root` (function, lines 2636-2650)
  - `REPO_ROOT` (constant, lines 2652-2652)

### `config/settings.py`

- Routed symbols: 33
- Cross-module imports: `config/constants.py`: `AUTO_SKILLS_ROOT_CANDIDATES`, `BACKEND_I18N`, `DEFAULT_REQUEST_TIMEOUT`, `DEFAULT_SHELL_COMMAND_TIMEOUT_SECONDS`, `DEFAULT_UI_LANGUAGE`, `DEFAULT_UI_STYLE`, `DEFAULT_WEB_UI_CONFIG`, `DEFAULT_WEB_UI_DIR`, `EXECUTION_MODE_CHOICES`, `EXECUTION_MODE_SEQUENTIAL`, `EXECUTION_MODE_SINGLE`, `EXECUTION_MODE_SYNC`, `MAX_SHELL_COMMAND_TIMEOUT_SECONDS`, `MEDIA_CAPABILITY_KEYS`, `MIN_SHELL_COMMAND_TIMEOUT_SECONDS`, `SUPPORTED_UI_LANGUAGES`, `TASK_COMPLEXITY_LEVELS`, `TASK_COMPLEXITY_RANKS`, `UI_LANGUAGE_LABELS`, `UI_STYLE_CHOICES`, `USER_COMPLEXITY_COMPLEX_TOKENS`, `USER_COMPLEXITY_EXPERT_TOKENS`, `USER_COMPLEXITY_MODERATE_TOKENS`, `USER_COMPLEXITY_SIMPLE_TOKENS`; `config/paths.py`: `WORKDIR`; `llm/utils.py`: `_is_http_url`, `_resolve_local_path`, `complete_chat_endpoint`, `extract_base_url`, `is_openai_like_provider`, `normalize_openai_compat_provider_name`, `strip_thinking_content`; `skills/store.py`: `ensure_embedded_skills`; `utils/http.py`: `urlopen`; `utils/json_utils.py`: `parse_json_object`; `utils/misc.py`: `MAX_TIMEOUT_SECONDS`, `MIN_TIMEOUT_SECONDS`, `normalize_timeout_seconds`, `sanitize_profile_id`; `utils/text.py`: `trim`
- Symbols:
  - `normalize_ui_language` (function, lines 1461-1483)
  - `normalize_ui_style` (function, lines 1486-1503)
  - `supported_ui_languages_payload` (function, lines 1506-1507)
  - `normalize_execution_mode` (function, lines 1510-1529)
  - `model_language_instruction` (function, lines 1532-1560)
  - `backend_i18n_text` (function, lines 2012-2022)
  - `backend_role_label` (function, lines 2025-2029)
  - `_detect_os_shell_instruction` (function, lines 2032-2071)
  - `resolve_web_ui_dir_path` (function, lines 2073-2080)
  - `resolve_optional_file_path` (function, lines 2083-2090)
  - `resolve_skills_root_path` (function, lines 2093-2100)
  - `_count_skill_markdown_files` (function, lines 2103-2114)
  - `select_preferred_skills_root` (function, lines 2117-2151)
  - `load_web_ui_config_file` (function, lines 2154-2168)
  - `extract_show_upload_list_setting` (function, lines 2171-2185)
  - `extract_ui_style_setting` (function, lines 2188-2202)
  - `extract_js_lib_download_setting` (function, lines 2205-2224)
  - `extract_daily_session_limit_setting` (function, lines 2227-2270)
  - `extract_shell_command_timeout_setting` (function, lines 2273-2319)
  - `default_multimodal_capabilities` (function, lines 2328-2336)
  - `_to_bool_like` (function, lines 2339-2349)
  - `infer_model_multimodal_capabilities` (function, lines 2352-2396)
  - `parse_capability_overrides` (function, lines 2399-2436)
  - `merge_multimodal_capabilities` (function, lines 2439-2446)
  - `parse_media_endpoints` (function, lines 2449-2463)
  - `infer_user_complexity_value` (function, lines 3959-3975)
  - `normalize_task_complexity` (function, lines 3977-4005)
  - `task_complexity_rank` (function, lines 4007-4008)
  - `task_complexity_at_least` (function, lines 4010-4011)
  - `max_task_complexity` (function, lines 4013-4022)
  - `load_llm_config_from_source` (function, lines 4173-4207)
  - `parse_llm_config_profiles` (function, lines 4209-4795)
  - `looks_like_llm_config` (function, lines 4797-4871)

### `llm/client.py`

- Routed symbols: 2
- Cross-module imports: `config/constants.py`: `DEFAULT_REQUEST_TIMEOUT`, `LLM_HTTP_RETRY_404_ON_VLLM`, `LLM_HTTP_RETRY_DELAY_SECONDS`, `LLM_HTTP_RETRY_MAX_ATTEMPTS`, `LLM_HTTP_RETRY_MAX_SECONDS`, `LLM_HTTP_RETRY_STATUSES`, `OLLAMA_THINKING_TOOL_BUFFER`, `SAMPLE_AUDIO_WAV_B64`, `SAMPLE_IMAGE_PNG_B64`, `SAMPLE_VIDEO_MP4_B64`; `config/settings.py`: `default_multimodal_capabilities`, `infer_model_multimodal_capabilities`, `merge_multimodal_capabilities`, `parse_capability_overrides`, `parse_media_endpoints`; `llm/utils.py`: `complete_chat_endpoint`, `is_openai_compat_provider`, `is_openai_like_provider`, `normalize_openai_compat_provider_name`, `split_thinking_content`; `utils/http.py`: `urlopen`; `utils/json_utils.py`: `canonicalize_tool_name`, `json_dumps`, `parse_json_object`, `parse_tool_arguments`, `parse_tool_arguments_with_error`; `utils/misc.py`: `MAX_TIMEOUT_SECONDS`, `MIN_TIMEOUT_SECONDS`, `make_id`, `normalize_timeout_seconds`, `now_ts`; `utils/text.py`: `trim`
- Symbols:
  - `OllamaError` (class, lines 11932-11952)
  - `OllamaClient` (class, lines 11954-13421)

### `llm/utils.py`

- Routed symbols: 25
- Cross-module imports: `config/constants.py`: `OPENAI_COMPAT_PROVIDER_NAMES`, `OPENAI_LIKE_PROVIDER_NAMES`; `utils/http.py`: `urlopen`; `utils/json_utils.py`: `json_dumps`, `parse_json_object`; `utils/text.py`: `trim`
- Symbols:
  - `probe_ollama_environment` (function, lines 3643-3656)
  - `list_ollama_models` (function, lines 3658-3660)
  - `_OLLAMA_TAG_CACHE_LOCK` (assignment, lines 3662-3662)
  - `_OLLAMA_TAG_CACHE` (assignment, lines 3663-3663)
  - `list_ollama_models_cached` (function, lines 3673-3710)
  - `resolve_ollama_model` (function, lines 3712-3722)
  - `infer_thinking_model` (function, lines 3724-3726)
  - `split_thinking_content` (function, lines 3728-3771)
  - `strip_thinking_content` (function, lines 3773-3774)
  - `check_ollama_model_ready` (function, lines 3776-3800)
  - `list_loaded_ollama_models` (function, lines 3802-3815)
  - `wake_ollama_model` (function, lines 3817-3847)
  - `try_pull_ollama_model` (function, lines 3849-3867)
  - `ordered_model_candidates` (function, lines 3869-3887)
  - `pick_working_ollama_model` (function, lines 3889-3905)
  - `extract_base_url` (function, lines 3938-3946)
  - `complete_chat_endpoint` (function, lines 3948-3957)
  - `normalize_openai_compat_provider_name` (function, lines 4024-4039)
  - `is_openai_compat_provider` (function, lines 4053-4054)
  - `is_openai_like_provider` (function, lines 4056-4057)
  - `openai_compat_probe_headers` (function, lines 4059-4070)
  - `openai_compat_model_list_urls` (function, lines 4072-4104)
  - `extract_openai_compat_model_ids` (function, lines 4106-4139)
  - `_is_http_url` (function, lines 4148-4153)
  - `_resolve_local_path` (function, lines 4155-4171)

### `rag/index.py`

- Routed symbols: 5
- Cross-module imports: `config/constants.py`: `RAG_DYNAMIC_NOISE_HARD_COMMUNITY_RATIO`, `RAG_DYNAMIC_NOISE_HARD_DOC_RATIO`, `RAG_DYNAMIC_NOISE_MIN_COMMUNITY_FREQ`, `RAG_DYNAMIC_NOISE_MIN_DOC_FREQ`, `RAG_DYNAMIC_NOISE_SOFT_COMMUNITY_RATIO`, `RAG_DYNAMIC_NOISE_SOFT_DOC_RATIO`, `RAG_EN_STOPWORDS`, `RAG_GRAPH_MAX_NODES`, `RAG_INCLUDE_FILENAME_ENTITIES_DEFAULT`, `RAG_MAX_COMMUNITY_MAP_SUPPORT`, `RAG_MAX_GLOBAL_COMMUNITIES`, `RAG_MAX_QUERY_RESULTS`, `RAG_MIN_SYNTHESIS_SCORE`, `RAG_WEAK_MATCH_SCORE_CAP`; `rag/ingestion.py`: `_rag_focused_excerpt`, `_rag_mmr_select`, `_rag_window_for_query`; `rag/parsers.py`: `_code_is_test_path`, `_rag_apply_filename_entity_policy`, `_rag_choose_community`, `_rag_classify_document`, `_rag_expand_tokens`, `_rag_extract_entities`, `_rag_filter_entities`, `_rag_tokenize`; `utils/misc.py`: `now_ts`; `utils/text.py`: `trim`
- Symbols:
  - `_code_module_name` (function, lines 54271-54285)
  - `_code_choose_community` (function, lines 54288-54295)
  - `_code_query_terms` (function, lines 54298-54310)
  - `TFGraphIDFIndex` (class, lines 55363-56929)
  - `CodeGraphIndex` (class, lines 59347-59812)

### `rag/ingestion.py`

- Routed symbols: 12
- Cross-module imports: `config/constants.py`: `CODE_IMPORT_WORKER_COUNT`, `CODE_LIBRARY_IGNORED_DIRS`, `CODE_PARSE_TIMEOUT_SECONDS`, `RAG_IMPORT_WORKER_COUNT`, `RAG_MAX_IMPORT_BATCH_ITEMS`, `RAG_MAX_IMPORT_FILES`, `RAG_MODEL_MEDIA_MAX_BYTES`, `RAG_PARSE_TIMEOUT_SECONDS`, `RAG_PDF_IMAGE_LIMIT`, `RAG_RETRIEVAL_MAX_PER_DOC`; `config/settings.py`: `default_multimodal_capabilities`; `rag/parsers.py`: `CodeContentParser`, `RAGContentParser`, `_rag_expand_tokens`, `_rag_extract_entities`, `_rag_is_noise_token`, `_rag_safe_name`, `_rag_tokenize`; `rag/store.py`: `CodeLibraryStore`, `RAGLibraryStore`, `WikiStore`; `session/state.py`: `SessionState`; `utils/files.py`: `try_read_text`; `utils/json_utils.py`: `_read_json_file`, `_write_json_file`, `parse_json_object`; `utils/media.py`: `guess_mime_from_name`; `utils/misc.py`: `make_id`, `now_ts`; `utils/text.py`: `trim`
- Symbols:
  - `_rag_trigram_set` (function, lines 53695-53700)
  - `_rag_jaccard_sim` (function, lines 53703-53710)
  - `_rag_mmr_select` (function, lines 53713-53760)
  - `_rag_embed_text` (function, lines 53897-53918)
  - `_rag_embed_batch` (function, lines 53921-53927)
  - `_rag_window_for_query` (function, lines 53930-53942)
  - `_rag_focused_excerpt` (function, lines 53945-53985)
  - `_rag_query_variants` (function, lines 53988-54025)
  - `_rag_parse_segments` (function, lines 54028-54088)
  - `_rag_parse_file_worker` (function, lines 58451-58465)
  - `RAGIngestionService` (class, lines 58468-59344)
  - `CodeIngestionService` (class, lines 60081-60166)

### `rag/parsers.py`

- Routed symbols: 28
- Cross-module imports: `config/constants.py`: `AUDIO_EXTS`, `CODE_CHUNK_CHARS`, `CODE_CHUNK_OVERLAP`, `CODE_LIBRARY_LANGUAGE_BY_EXT`, `CODE_LIBRARY_SPECIAL_FILENAMES`, `CODE_MAX_CHUNKS_PER_DOC`, `CODE_PREVIEW_DIFF_CONTEXT_LINES`, `CODE_PREVIEW_DIFF_MERGE_GAP`, `CODE_PREVIEW_EXTS`, `CODE_PREVIEW_FILENAMES`, `CODE_PREVIEW_STAGE_MAX_ROWS`, `DOCUMENT_PREVIEW_EXTS`, `EXCEL_PREVIEW_EXTS`, `IMAGE_EXTS`, `PRESENTATION_PREVIEW_EXTS`, `RAG_CHUNK_CHARS`, `RAG_CHUNK_OVERLAP`, `RAG_CODE_HINTS`, `RAG_EN_STOPWORDS`, `RAG_GENERIC_ENTITY_TERMS_EN`, `RAG_GENERIC_ENTITY_TERMS_ZH`, `RAG_INCLUDE_FILENAME_ENTITIES_DEFAULT`, `RAG_MAX_CHUNKS_PER_DOC`, `RAG_PDF_IMAGE_LIMIT`, `RAG_RESEARCH_HINTS`, `RAG_SHORT_TOKEN_ALLOWLIST`, `RAG_STRUCTURAL_ENTITY_PATTERNS`, `RAG_TERM_GROUPS`, `RAG_ZH_STOPWORDS`, `TABULAR_PREVIEW_EXTS`, `VIDEO_EXTS`; `rag/ingestion.py`: `_rag_parse_segments`; `utils/files.py`: `_sha256_bytes`, `_sha256_file`; `utils/json_utils.py`: `parse_json_object`; `utils/media.py`: `guess_mime_from_name`; `utils/text.py`: `_focused_diff_rows_from_opcodes`, `_skip_row`, `trim`
- Symbols:
  - `normalize_rel_preview_path` (function, lines 5557-5568)
  - `is_code_preview_candidate` (function, lines 5571-5579)
  - `preview_kind_for_path` (function, lines 5588-5617)
  - `build_code_preview_rows` (function, lines 5620-5666)
  - `_rag_safe_name` (function, lines 53494-53497)
  - `_rag_detect_language` (function, lines 53500-53514)
  - `_rag_cjk_ngrams` (function, lines 53517-53529)
  - `_rag_is_noise_token` (function, lines 53532-53551)
  - `_rag_entity_allowed` (function, lines 53554-53566)
  - `_rag_filter_entities` (function, lines 53569-53583)
  - `_rag_filename_entity_aliases` (function, lines 53586-53619)
  - `_rag_apply_filename_entity_policy` (function, lines 53622-53652)
  - `_rag_choose_community` (function, lines 53655-53692)
  - `_rag_tokenize` (function, lines 53763-53814)
  - `_rag_expand_tokens` (function, lines 53817-53838)
  - `_rag_extract_entities` (function, lines 53841-53857)
  - `_rag_classify_document` (function, lines 53860-53894)
  - `_rag_chunk_text` (function, lines 54091-54170)
  - `_code_language_from_name` (function, lines 54247-54263)
  - `_code_is_test_path` (function, lines 54266-54268)
  - `_CallCollector` (class, lines 54313-54325)
  - `_ALGO_COMPLEXITY_RE` (assignment, lines 54328-54328)
  - `_ALGO_STEP_RE` (assignment, lines 54329-54329)
  - `_ALGO_MATH_VARS` (assignment, lines 54330-54330)
  - `_ALGO_DOC_KEYWORDS` (assignment, lines 54331-54331)
  - `_detect_algo_chunk` (function, lines 54334-54357)
  - `CodeContentParser` (class, lines 54360-54850)
  - `RAGContentParser` (class, lines 54853-55360)

### `rag/store.py`

- Routed symbols: 4
- Cross-module imports: `config/constants.py`: `CODE_CHUNK_CHARS`, `CODE_CHUNK_OVERLAP`, `CODE_MAX_CHUNKS_PER_DOC`, `RAG_INCLUDE_FILENAME_ENTITIES_DEFAULT`, `RAG_MAX_QUERY_RESULTS`, `RAG_RETRIEVAL_MAX_PER_DOC`, `RAG_TASK_HISTORY_LIMIT`, `RAG_WEAK_MATCH_SCORE_CAP`, `RAG_WORKFLOW_ACCEPT_SCORE`; `rag/index.py`: `CodeGraphIndex`, `TFGraphIDFIndex`, `_code_choose_community`, `_code_module_name`; `rag/ingestion.py`: `_rag_focused_excerpt`, `_rag_mmr_select`, `_rag_window_for_query`; `rag/parsers.py`: `_code_is_test_path`, `_rag_apply_filename_entity_policy`, `_rag_choose_community`, `_rag_chunk_text`, `_rag_entity_allowed`, `_rag_expand_tokens`, `_rag_extract_entities`, `_rag_filter_entities`, `_rag_safe_name`, `_rag_tokenize`; `skills/store.py`: `_write_text_if_changed`; `utils/files.py`: `_sha256_bytes`, `_sha256_file`, `try_read_text`; `utils/json_utils.py`: `_read_json_file`, `_write_json_file`, `json_dumps`; `utils/media.py`: `guess_mime_from_name`; `utils/misc.py`: `make_id`, `now_ts`; `utils/text.py`: `trim`
- Symbols:
  - `RAGLibraryStore` (class, lines 56941-57515)
  - `WikiStore` (class, lines 57518-58047)
  - `WorkflowMemoryStore` (class, lines 58050-58448)
  - `CodeLibraryStore` (class, lines 59815-60078)

### `server/handlers.py`

- Routed symbols: 5
- Cross-module imports: `app/context.py`: `AppContext`; `config/constants.py`: `APP_VERSION`, `DEFAULT_REQUEST_TIMEOUT`, `DEFAULT_SHELL_COMMAND_TIMEOUT_SECONDS`, `DEFAULT_UI_LANGUAGE`, `DEFAULT_UI_STYLE`, `EXECUTION_MODE_CHOICES`, `EXECUTION_MODE_SYNC`, `MIN_RUN_TIMEOUT_SECONDS`, `PLAN_MODE_USER_CHOICES`, `RAG_GRAPH_MAX_NODES`, `SESSION_LIST_DEFAULT_LIMIT`, `SSE_HEARTBEAT_SECONDS`, `TASK_COMPLEXITY_LEVELS`, `TASK_LEVEL_CHOICES`, `TASK_LEVEL_POLICIES`, `UI_STYLE_LABELS`; `config/paths.py`: `LLM_CONFIG_PATH`, `REPO_ROOT`, `WORKDIR`; `config/settings.py`: `_to_bool_like`, `infer_user_complexity_value`, `looks_like_llm_config`, `normalize_execution_mode`, `normalize_task_complexity`, `normalize_ui_language`, `normalize_ui_style`, `resolve_web_ui_dir_path`, `supported_ui_languages_payload`; `llm/utils.py`: `extract_base_url`, `extract_openai_compat_model_ids`, `list_ollama_models`, `normalize_openai_compat_provider_name`, `openai_compat_model_list_urls`, `openai_compat_probe_headers`; `rag/parsers.py`: `normalize_rel_preview_path`; `session/manager.py`: `SessionCreationLimitExceeded`, `SessionManager`; `session/state.py`: `SessionState`; `skills/store.py`: `analyze_skill_building_knowledge`; `utils/files.py`: `safe_path`, `try_read_text`; `utils/http.py`: `urlopen`; `utils/json_utils.py`: `json_dumps`, `parse_json_object`; `utils/media.py`: `guess_mime_from_name`; `utils/misc.py`: `now_ts`, `swallow_benign_socket_error`, `user_id_from_ip`; `utils/text.py`: `trim`
- Symbols:
  - `AgentHTTPServer` (class, lines 65632-65660)
  - `Handler` (class, lines 65664-66565)
  - `SkillsHandler` (class, lines 66567-66763)
  - `RagAdminHandler` (class, lines 66765-66933)
  - `CodeAdminHandler` (class, lines 66936-67122)

### `session/manager.py`

- Routed symbols: 2
- Cross-module imports: `config/constants.py`: `AGENT_MAX_OUTPUT_TOKENS`, `ARBITER_DEFAULT_MAX_TOKENS`, `ARBITER_DEFAULT_TEMPERATURE`, `ARBITER_DEFAULT_TIMEOUT_SECONDS`, `DEFAULT_REQUEST_TIMEOUT`, `DEFAULT_SHELL_COMMAND_TIMEOUT_SECONDS`, `DEFAULT_UI_LANGUAGE`, `EXECUTION_MODE_SYNC`, `MAX_AGENT_ROUNDS`, `MAX_AGENT_ROUNDS_CAP`, `MAX_RUN_SECONDS`, `MAX_RUN_TIMEOUT_SECONDS`, `MAX_SHELL_COMMAND_TIMEOUT_SECONDS`, `MIN_AGENT_ROUNDS`, `MIN_CONTEXT_TOKEN_LIMIT`, `MIN_RUN_TIMEOUT_SECONDS`, `MIN_SHELL_COMMAND_TIMEOUT_SECONDS`, `SESSION_LIST_DEFAULT_LIMIT`, `TOKEN_THRESHOLD`; `config/paths.py`: `LLM_CONFIG_PATH`; `config/settings.py`: `infer_model_multimodal_capabilities`, `merge_multimodal_capabilities`, `normalize_execution_mode`, `normalize_ui_language`, `parse_capability_overrides`, `parse_llm_config_profiles`; `llm/client.py`: `OllamaClient`; `llm/utils.py`: `complete_chat_endpoint`, `extract_base_url`, `is_openai_compat_provider`, `list_ollama_models_cached`, `probe_ollama_environment`; `session/state.py`: `SessionState`; `utils/crypto.py`: `CryptoBox`; `utils/files.py`: `try_read_text`; `utils/json_utils.py`: `parse_json_object`; `utils/misc.py`: `make_id`, `normalize_timeout_seconds`, `now_ts`, `sanitize_profile_id`
- Symbols:
  - `SessionCreationLimitExceeded` (class, lines 2322-2325)
  - `SessionManager` (class, lines 43264-44199)

### `session/state.py`

- Routed symbols: 1
- Cross-module imports: `agent/background.py`: `BackgroundManager`; `agent/bus.py`: `MessageBus`; `agent/events.py`: `EventHub`; `agent/tasks.py`: `TaskManager`; `agent/todo.py`: `TodoManager`; `agent/worktree.py`: `WorktreeManager`; `config/constants.py`: `AGENT_BUBBLE_ROLES`, `AGENT_CTX_LIMIT_TIER0`, `AGENT_CTX_LIMIT_TIER1`, `AGENT_CTX_LIMIT_TIER2`, `AGENT_CTX_LIMIT_TIER3`, `AGENT_MAX_OUTPUT_TOKENS`, `AGENT_MSG_LIMIT_TIER0`, `AGENT_MSG_LIMIT_TIER1`, `AGENT_MSG_LIMIT_TIER2`, `AGENT_MSG_LIMIT_TIER3`, `AGENT_ROLES`, `AGENT_TOOL_ALLOWLIST`, `ARBITER_DEFAULT_MAX_TOKENS`, `ARBITER_DEFAULT_TEMPERATURE`, `ARBITER_DEFAULT_TIMEOUT_SECONDS`, `ARBITER_TRIGGER_MIN_CONTENT_CHARS`, `ARBITER_VALID_PLANNING_STREAK_LIMIT`, `ASSISTANT_MESSAGE_EVENT_MAX_CHARS`, `ASSISTANT_TEXT_PERSIST_MAX_CHARS`, `AUDIO_EXTS`, `AUTO_CONTINUE_BUDGET_DEFAULT`, `BASH_READ_LOOP_THRESHOLD`, `BLACKBOARD_MAX_LOG_ENTRIES`, `BLACKBOARD_MAX_TEXT`, `BLACKBOARD_STATUSES`, `CHAT_UPLOAD_AUTO_LIBRARY_INGEST`, `CHAT_UPLOAD_INGEST_QUEUE_MAX`, `CHAT_UPLOAD_INLINE_TEXT_BYTES`, `CHAT_UPLOAD_PARSE_MAX_BYTES`, `CHAT_UPLOAD_PARSE_QUEUE_MAX`, `CHAT_UPLOAD_PARSE_TIMEOUT_SECONDS`, `CHAT_UPLOAD_PROMPT_MAX_CHARS`, `CHAT_UPLOAD_PROMPT_MAX_FILES`, `CHAT_UPLOAD_PROMPT_PER_FILE_CHARS`, `CHAT_UPLOAD_TEXT_CONTEXT_CHARS`, `CHAT_UPLOAD_ZIP_ENTRY_MAX_BYTES`, `CHECKPOINT_INTERVAL_ROUNDS`, `CHECKPOINT_MAX_COUNT`, `CODE_PREVIEW_STAGE_MAX_BYTES`, `CODE_PREVIEW_STAGE_MAX_PER_FILE`, `CODE_PREVIEW_STAGE_MAX_ROWS`, `CODE_PREVIEW_STAGE_MAX_TOTAL`, `COMPACT_TIER1_ABS`, `COMPACT_TIER1_PCT`, `COMPACT_TIER2_ABS`, `COMPACT_TIER2_PCT`, `COMPACT_TIER3_PCT`, `CONTEXT_ACTUAL_USAGE_RECENT_SECONDS`, `CONTEXT_AUTO_COMPACT_RESERVE_RATIO`, `CONTEXT_COMPACT_INEFFECTIVE_COOLDOWN_SECONDS`, `CONTEXT_ESTIMATE_SAFETY_MULTIPLIER`, `CONTEXT_USAGE_CALIBRATION_MAX`, `DANGEROUS_PATTERNS`, `DEEP_RESEARCH_REQUEST_KEYWORDS`, `DEEP_RESEARCH_RETRIEVAL_KEYWORDS`, `DEEP_RESEARCH_TEXT_ONLY_HINT_KEYWORDS`, `DEFAULT_REQUEST_TIMEOUT`, `DEFAULT_SHELL_COMMAND_TIMEOUT_SECONDS`, `DEFAULT_UI_LANGUAGE`, `DEVELOPER_EDIT_STALL_THRESHOLD`, `EMPTY_ACTION_MIN_CONTENT_CHARS`, `EMPTY_ACTION_WAKEUP_RETRY_LIMIT`, `ERROR_CATEGORY_DEFS`, `EXECUTION_MODE_CHOICES`, `EXECUTION_MODE_SEQUENTIAL`, `EXECUTION_MODE_SINGLE`, `EXECUTION_MODE_SYNC`, `EXPLORER_STALL_THRESHOLD`, `FAILURE_LEDGER_MAX_COMPILE_ERRORS`, `FAILURE_LEDGER_MAX_DELEGATIONS`, `FAILURE_LEDGER_MAX_ERRORS`, `FAILURE_LEDGER_MAX_FIXES`, `FAILURE_LEDGER_MAX_STALLS`, `FAILURE_LEDGER_MAX_TOOL_FPS`, `FILE_BUFFER_CONTENT_THRESHOLD`, `FILE_BUFFER_MAX_FILES`, `FINAL_SUMMARY_MIN_CHARS`, `FINAL_SUMMARY_STRICT_MIN_CHARS`, `FUSED_FAULT_BREAK_THRESHOLD`, `HARD_BREAK_RECOVERY_ROUND_THRESHOLD`, `HARD_BREAK_TOOL_ERROR_THRESHOLD`, `HTML_FRONTEND_REQUEST_KEYWORDS`, `IMAGE_EXTS`, `IMAGE_FORMATS_NEED_CONVERSION`, `LARGE_FILE_AUTO_PAGE_BYTES`, `LARGE_FILE_AUTO_PAGE_LINES`, `LARGE_SOURCE_UPLOAD_EXCERPT_CHARS`, `LIVE_INPUT_DELAY_NORMAL_ROUNDS`, `LIVE_INPUT_DELAY_TOOL_ROUNDS`, `LIVE_INPUT_DELAY_WRITE_ROUNDS`, `LIVE_INPUT_MAX_INJECTIONS`, `LIVE_INPUT_REINJECT_INTERVAL`, `LIVE_INPUT_WEIGHT_BASE_DELAYED`, `LIVE_INPUT_WEIGHT_BASE_NORMAL`, `LIVE_INPUT_WEIGHT_STEP_DELAYED`, `LIVE_INPUT_WEIGHT_STEP_NORMAL`, `LONG_OUTPUT_LISTING_OFFLOAD_CHARS`, `LONG_OUTPUT_MODEL_PAGE_CHARS`, `LONG_OUTPUT_READ_PAGE_LINES`, `LONG_OUTPUT_TEMP_MAX_FILES`, `LONG_OUTPUT_UI_PAGE_CHARS`, `LONG_OUTPUT_UI_PREVIEW_MAX_PAGES`, `MANAGER_CTX_LIMIT_TIER0`, `MANAGER_CTX_LIMIT_TIER1`, `MANAGER_CTX_LIMIT_TIER2`, `MANAGER_CTX_LIMIT_TIER3`, `MANAGER_ROUTE_TARGETS`, `MAX_AGENT_ROUNDS`, `MAX_AGENT_ROUNDS_CAP`, `MAX_CONTEXT_ARCHIVE_SEGMENTS`, `MAX_RUN_SECONDS`, `MAX_RUN_TIMEOUT_SECONDS`, `MAX_SHELL_COMMAND_TIMEOUT_SECONDS`, `MIN_AGENT_ROUNDS`, `MIN_CONTEXT_TOKEN_LIMIT`, `MIN_RUN_TIMEOUT_SECONDS`, `MIN_SHELL_COMMAND_TIMEOUT_SECONDS`, `MODEL_CALL_PROGRESS_DELAY`, `MODEL_CALL_PROGRESS_INTERVAL`, `MODEL_OUTPUT_RETRY_TIMES`, `PERSISTED_ROUTES_MAX`, `PLAN_BUBBLE_MAX_CHARS`, `PLAN_FILE_RELATIVE_PATH`, `PLAN_MESSAGE_EVENT_MAX_CHARS`, `PLAN_MODE_ENABLED_LEVELS`, `PLAN_MODE_EXPLORER_MAX_ROUNDS`, `PLAN_MODE_FORCED_LEVELS`, `PLAN_MODE_MANAGER_SYNTHESIS_MAX_TOKENS`, `PLAN_MODE_MAX_OPTIONS`, `PLAN_MODE_RESEARCH_TOOL_ALLOWLIST`, `PLAN_MODE_SYNTHESIS_MAX_ATTEMPTS`, `PLAN_MODE_USER_CHOICES`, `PLAN_NOTICE_BODY_MAX_CHARS`, `PLAN_STEP_FULL_CONTENT_MAX_CHARS`, `PREVIEW_DOWNLOAD_MAX_BYTES`, `PREVIEW_DOWNLOAD_MAX_FILES`, `READ_CONTEXT_PROMPT_MAX_CHARS`, `READ_CONTEXT_PROMPT_MAX_ITEMS`, `READ_CONTEXT_REGISTRY_MAX`, `READ_CONTEXT_SHARED_MAX_ITEMS`, `READ_CONTEXT_SUMMARY_MAX_CHARS`, `READ_FILE_COMPACT_PIN_DISTINCT`, `READ_FILE_COMPACT_PIN_MAX_CHARS`, `READ_FILE_DEFAULT_MAX_CHARS`, `READ_FILE_HARD_MAX_CHARS`, `READ_FILE_LOOP_DISTINCT_SOFT_LIMIT`, `READ_FILE_LOOP_THRESHOLD`, `READ_FILE_OVERVIEW_HEAD_LINES`, `READ_FILE_SEARCH_MAX_MATCHES`, `RENDER_FRAME_ACTIVITY_INTERVAL_SECONDS`, `RENDER_FRAME_MAX_B64_CHARS`, `RENDER_FRAME_MAX_LINES`, `RENDER_FRAME_MAX_LINE_POINTS`, `RENDER_FRAME_MAX_POINTS`, `REPEATED_TOOL_LOOP_THRESHOLD`, `RETRY_RUNTIME_HINT_PREFIXES`, `REVIEWER_DEBUG_MODE_MAX_ROUNDS`, `RUNTIME_CONTROL_HINT_PREFIXES`, `RUN_COMPLETION_SUMMARY_ENABLED`, `SEMANTIC_CONFIDENCE_CHOICES`, `SESSION_DEFERRED_START_QUEUE_MAX`, `SESSION_HEARTBEAT_STALE_SECONDS`, `SESSION_SUBMIT_LOCK_TIMEOUT_SECONDS`, `SKILLS_VIRTUAL_PREFIX`, `SKILL_REFRESH_MIN_INTERVAL_SECONDS`, `SKILL_RUNTIME_CACHE_MAX_BYTES`, `SKILL_RUNTIME_CACHE_MAX_ENTRIES`, `STALL_ESCALATION_CONTEXT_MAX_CHARS`, `STALL_ESCALATION_MIN_LEVEL`, `STALL_PLAN_SYNTHESIS_MAX_TOKENS`, `STALL_SEVERITY_DECAY_ON_SUCCESS`, `STALL_SEVERITY_ESCALATION_THRESHOLD`, `STALL_SEVERITY_WEIGHT_BASH_READ_LOOP`, `STALL_SEVERITY_WEIGHT_FAULT`, `STALL_SEVERITY_WEIGHT_RECOVERY_RETRY`, `STALL_SEVERITY_WEIGHT_REPEATED_TOOL`, `STALL_SEVERITY_WEIGHT_WATCHDOG`, `TASK_COMPLEXITY_LEVELS`, `TASK_LEVEL_CHOICES`, `TASK_LEVEL_POLICIES`, `TASK_PHASE_ROUTING`, `TASK_PROFILE_TYPES`, `TASK_SCALE_PREFERENCES`, `THINKING_BUDGET_FORCE_RATIO`, `TOKEN_THRESHOLD`, `TRUNCATION_CONTINUATION_ECHO_CHARS`, `TRUNCATION_CONTINUATION_MAX_PASSES`, `TRUNCATION_CONTINUATION_MAX_TOKENS`, `TRUNCATION_CONTINUATION_TAIL_CHARS`, `TRUNCATION_LIVE_BUFFER_MAX_CHARS`, `TRUNCATION_OVERLAP_SCAN_CHARS`, `TRUNCATION_PAIR_SCAN_CHARS`, `VIDEO_EXTS`, `WATCHDOG_CONTEXT_NEAR_RATIO`, `WATCHDOG_CONTEXT_STALL_THRESHOLD`, `WATCHDOG_INTENT_NO_TOOL_THRESHOLD`, `WATCHDOG_INTENT_NO_TOOL_THRESHOLD_SINGLE`, `WATCHDOG_MAX_DECOMPOSE_STEPS`, `WATCHDOG_REPEAT_NO_TOOL_THRESHOLD`, `WATCHDOG_REPEAT_NO_TOOL_THRESHOLD_SINGLE`, `WATCHDOG_REPEAT_SIMILARITY_THRESHOLD`, `WATCHDOG_STATE_STALL_THRESHOLD`, `WATCHDOG_STEP_MAX_ATTEMPTS`, `_DEFAULT_TOOL_TIMEOUT`, `_SHELL_AUTO_CONFIRM_PATTERNS`, `_TOOL_TIMEOUT_MAP`; `config/paths.py`: `WORKDIR`; `config/settings.py`: `_detect_os_shell_instruction`, `_to_bool_like`, `backend_i18n_text`, `backend_role_label`, `default_multimodal_capabilities`, `infer_model_multimodal_capabilities`, `infer_user_complexity_value`, `looks_like_llm_config`, `max_task_complexity`, `merge_multimodal_capabilities`, `model_language_instruction`, `normalize_execution_mode`, `normalize_task_complexity`, `normalize_ui_language`, `parse_capability_overrides`, `parse_llm_config_profiles`, `task_complexity_at_least`, `task_complexity_rank`; `llm/client.py`: `OllamaClient`, `OllamaError`; `llm/utils.py`: `complete_chat_endpoint`, `extract_base_url`, `is_openai_compat_provider`, `list_loaded_ollama_models`, `list_ollama_models`, `list_ollama_models_cached`, `probe_ollama_environment`, `resolve_ollama_model`, `split_thinking_content`, `strip_thinking_content`, `wake_ollama_model`; `rag/parsers.py`: `CodeContentParser`, `build_code_preview_rows`, `is_code_preview_candidate`, `normalize_rel_preview_path`, `preview_kind_for_path`; `skills/store.py`: `SkillStore`, `ensure_runtime_skills`; `utils/compress.py`: `compress_text_blob`, `decompress_text_blob`; `utils/crypto.py`: `CryptoBox`; `utils/errors.py`: `CircuitBreakerTriggered`, `EmptyActionError`; `utils/files.py`: `_normalize_external_js_url`, `_safe_js_filename`, `cache_external_js_url`, `ensure_offline_js_libs`, `is_external_js_src`, `load_offline_js_lib_index`, `match_offline_js_catalog_by_url`, `offline_js_lib_root`, `safe_path`, `try_read_text`; `utils/http.py`: `urlopen`; `utils/json_utils.py`: `TOOLS`, `TOOL_REQUIRED_ARGS`, `canonicalize_tool_name`, `extract_json_object_from_text`, `json_dumps`, `parse_json_object`, `parse_tool_arguments_with_error`, `repair_truncated_json_object`, `tool_def`; `utils/media.py`: `_convert_image_to_safe_format`, `guess_ext_from_mime`, `guess_mime_from_name`; `utils/misc.py`: `MAX_TIMEOUT_SECONDS`, `MIN_TIMEOUT_SECONDS`, `is_benign_socket_error`, `make_id`, `normalize_timeout_seconds`, `now_ts`, `sanitize_profile_id`; `utils/text.py`: `MAX_TOOL_OUTPUT`, `_fmt_export_ts`, `_html_esc`, `_text_to_minimal_pdf`, `extract_todo_rows_from_text`, `filter_runtime_noise_lines`, `make_numbered_diff`, `make_unified_diff`, `normalize_embedded_newlines`, `normalize_work_text`, `parse_front_matter`, `render_numbered_diff_text`, `split_structured_todo_content`, `split_todo_status_text`, `trim`
- Symbols:
  - `SessionState` (class, lines 13832-43262)

### `skills/store.py`

- Routed symbols: 26
- Cross-module imports: `config/constants.py`: `BUILTIN_CLAWHUB_SKILLS_VERSION`, `EMBEDDED_CLAWHUB_SKILLS_ARCHIVE_B64`, `EMBEDDED_SKILLS_ARCHIVE_B64`, `EMBEDDED_SKILLS_ARCHIVE_FILES`, `EMBEDDED_SKILLS_ARCHIVE_SHA256`, `SKILLS_EXTERNAL_MOUNT`, `SKILLS_VIRTUAL_PREFIX`, `SKILL_BODY_COMPACT_THRESHOLD_CHARS`, `SKILL_BODY_PREVIEW_CHARS`, `SKILL_DEFAULT_ATTACHMENT_GLOBS`, `SKILL_INLINE_ATTACHMENT_MAX_CHARS`, `SKILL_INLINE_ATTACHMENT_MAX_FILES`, `SKILL_PROMPT_MAX_CHARS`, `SKILL_PROMPT_MAX_ITEMS`, `SKILL_PROTOCOL_CLAWHUB`, `SKILL_PROTOCOL_HTTP_JSON`, `SKILL_PROTOCOL_LOCAL`, `SKILL_PROTOCOL_SPECS`, `SKILL_REFRESH_MIN_INTERVAL_SECONDS`, `SKILL_RESOURCE_MANIFEST_MAX_ITEMS`; `config/paths.py`: `WORKDIR`; `llm/utils.py`: `_is_http_url`; `utils/files.py`: `_render_offline_js_catalog_md`, `safe_path`, `try_read_text`; `utils/http.py`: `urlopen`; `utils/json_utils.py`: `json_dumps`, `parse_json_object`; `utils/misc.py`: `_meta_string_list`, `_module_exists`, `now_ts`; `utils/text.py`: `parse_front_matter`, `trim`
- Symbols:
  - `ensure_embedded_skills_at_root` (function, lines 6533-6585)
  - `ensure_embedded_skills` (function, lines 6588-6589)
  - `detect_upload_parser_capabilities` (function, lines 6597-6612)
  - `_render_cap_markdown` (function, lines 6614-6628)
  - `_write_text_if_changed` (function, lines 6630-6635)
  - `ensure_generated_document_skills` (function, lines 6637-6725)
  - `ensure_generated_image_coding_feedback_skill` (function, lines 6727-6826)
  - `_skill_knowledge_files` (function, lines 6828-6847)
  - `analyze_skill_building_knowledge` (function, lines 6849-6903)
  - `_sanitize_skill_slug` (function, lines 6905-6907)
  - `_build_skills_gen_skill_content` (function, lines 6909-6940)
  - `ensure_generated_skills_gen_skill` (function, lines 6942-6946)
  - `ensure_generated_execution_recovery_skill` (function, lines 6948-7026)
  - `ensure_generated_systematic_debugging_skill` (function, lines 7028-7300)
  - `ensure_generated_code_engineering_mastery_skill` (function, lines 7302-7420)
  - `ensure_generated_smart_file_navigation_skill` (function, lines 7422-7537)
  - `ensure_generated_html_frontend_report_skills` (function, lines 7539-7746)
  - `ensure_generated_deep_research_skills` (function, lines 7748-8016)
  - `ensure_generated_research_scientific_skills` (function, lines 8018-8654)
  - `ensure_generated_rag_mastery_skills` (function, lines 8660-8956)
  - `ensure_generated_multimodal_comprehension_skills` (function, lines 8962-9651)
  - `ensure_generated_runtime_skills_manifest` (function, lines 9654-9685)
  - `ensure_embedded_clawhub_skills` (function, lines 9943-9980)
  - `ensure_runtime_skills` (function, lines 9982-9997)
  - `_BUILTIN_SKILLS` (assignment, lines 10039-10127)
  - `SkillStore` (class, lines 10136-11430)

### `utils/compress.py`

- Routed symbols: 2
- Cross-module imports: none
- Symbols:
  - `compress_text_blob` (function, lines 3277-3282)
  - `decompress_text_blob` (function, lines 3284-3292)

### `utils/crypto.py`

- Routed symbols: 1
- Cross-module imports: `utils/json_utils.py`: `json_dumps`
- Symbols:
  - `CryptoBox` (class, lines 4881-4998)

### `utils/errors.py`

- Routed symbols: 2
- Cross-module imports: none
- Symbols:
  - `EmptyActionError` (class, lines 3666-3667)
  - `CircuitBreakerTriggered` (class, lines 3670-3671)

### `utils/files.py`

- Routed symbols: 25
- Cross-module imports: `config/constants.py`: `OFFLINE_JS_LIB_CATALOG`, `OFFLINE_JS_LIB_INDEX_FILE`, `OFFLINE_JS_LIB_README_FILE`; `config/paths.py`: `WORKDIR`; `utils/http.py`: `urlopen`; `utils/json_utils.py`: `json_dumps`; `utils/misc.py`: `now_ts`; `utils/text.py`: `trim`
- Symbols:
  - `_normalize_js_lib_asset_ref` (function, lines 1380-1393)
  - `_resolve_js_lib_asset_path` (function, lines 1396-1425)
  - `_discover_extra_js_lib_files` (function, lines 1428-1458)
  - `safe_path` (function, lines 2654-2663)
  - `_safe_js_filename` (function, lines 2665-2672)
  - `_sha256_bytes` (function, lines 2674-2675)
  - `_sha256_file` (function, lines 2677-2685)
  - `_download_http_bytes` (function, lines 2687-2695)
  - `offline_js_lib_root` (function, lines 2697-2698)
  - `_offline_js_entry_relative_path` (function, lines 2700-2704)
  - `_archive_member_relative_path` (function, lines 2706-2715)
  - `_path_size_bytes` (function, lines 2717-2732)
  - `_extract_archive_to_dir` (function, lines 2734-2774)
  - `_package_required_paths` (function, lines 2776-2782)
  - `_package_install_ready` (function, lines 2784-2792)
  - `_postprocess_offline_js_package` (function, lines 2794-2829)
  - `_ensure_offline_js_package` (function, lines 2831-2870)
  - `_render_offline_js_catalog_md` (function, lines 2872-2888)
  - `load_offline_js_lib_index` (function, lines 2890-2899)
  - `ensure_offline_js_libs` (function, lines 2901-3045)
  - `_normalize_external_js_url` (function, lines 3047-3051)
  - `is_external_js_src` (function, lines 3053-3055)
  - `match_offline_js_catalog_by_url` (function, lines 3057-3073)
  - `cache_external_js_url` (function, lines 3075-3107)
  - `try_read_text` (function, lines 5203-5211)

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
  - `json_dumps` (function, lines 2626-2627)
  - `parse_tool_arguments` (function, lines 3545-3554)
  - `repair_truncated_json_object` (function, lines 3556-3609)
  - `parse_tool_arguments_with_error` (function, lines 3611-3641)
  - `parse_json_object` (function, lines 3907-3912)
  - `extract_json_object_from_text` (function, lines 3914-3936)
  - `_json_default_copy` (function, lines 5213-5218)
  - `_read_json_file` (function, lines 5220-5240)
  - `_write_json_file` (function, lines 5242-5269)
  - `tool_def` (function, lines 13423-13435)
  - `TOOLS` (constant, lines 13437-13732)
  - `TOOL_REQUIRED_ARGS` (constant, lines 13734-13734)
  - `TOOL_SPEC_BY_NAME` (constant, lines 13735-13735)
  - `TOOL_NAME_FUZZY_MAP` (constant, lines 13747-13747)
  - `canonicalize_tool_name` (function, lines 13765-13776)

### `utils/media.py`

- Routed symbols: 3
- Cross-module imports: none
- Symbols:
  - `guess_mime_from_name` (function, lines 2466-2468)
  - `_convert_image_to_safe_format` (function, lines 2471-2488)
  - `guess_ext_from_mime` (function, lines 2491-2497)

### `utils/misc.py`

- Routed symbols: 19
- Cross-module imports: none
- Symbols:
  - `MIN_TIMEOUT_SECONDS` (constant, lines 370-370)
  - `MAX_TIMEOUT_SECONDS` (constant, lines 371-371)
  - `DEFAULT_TIMEOUT_SECONDS` (constant, lines 372-378)
  - `BENIGN_SOCKET_DEBUG_LOG_ENABLED` (constant, lines 508-514)
  - `BENIGN_SOCKET_LOG_INTERVAL_SECONDS` (constant, lines 515-515)
  - `now_ts` (function, lines 2499-2500)
  - `_benign_socket_log_lock` (assignment, lines 2503-2503)
  - `_benign_socket_log_state` (assignment, lines 2504-2504)
  - `is_benign_socket_error` (function, lines 2522-2540)
  - `_socket_error_code` (function, lines 2543-2552)
  - `_log_benign_socket_error_limited` (function, lines 2555-2589)
  - `swallow_benign_socket_error` (function, lines 2592-2596)
  - `normalize_timeout_seconds` (function, lines 2599-2612)
  - `detect_local_lan_ip` (function, lines 2614-2624)
  - `make_id` (function, lines 2629-2630)
  - `sanitize_profile_id` (function, lines 2632-2634)
  - `user_id_from_ip` (function, lines 4873-4879)
  - `_meta_string_list` (function, lines 5190-5201)
  - `_module_exists` (function, lines 6591-6595)

### `utils/text.py`

- Routed symbols: 23
- Cross-module imports: `config/constants.py`: `CODE_PREVIEW_DIFF_CONTEXT_LINES`, `CODE_PREVIEW_DIFF_MERGE_GAP`
- Symbols:
  - `MAX_TOOL_OUTPUT` (constant, lines 137-137)
  - `SOCKET_NOISE_LINE_PATTERNS` (constant, lines 502-507)
  - `filter_runtime_noise_lines` (function, lines 2507-2519)
  - `trim` (function, lines 3109-3111)
  - `_fmt_export_ts` (function, lines 3114-3122)
  - `_html_esc` (function, lines 3125-3126)
  - `_text_to_minimal_pdf` (function, lines 3129-3275)
  - `normalize_embedded_newlines` (function, lines 3294-3302)
  - `_map_todo_status_token` (function, lines 3305-3320)
  - `split_todo_status_text` (function, lines 3323-3378)
  - `extract_todo_rows_from_text` (function, lines 3381-3448)
  - `infer_todo_status_from_text` (function, lines 3451-3457)
  - `split_structured_todo_content` (function, lines 3460-3513)
  - `normalize_work_text` (function, lines 3516-3543)
  - `parse_front_matter` (function, lines 5000-5187)
  - `make_unified_diff` (function, lines 5271-5288)
  - `_skip_row` (function, lines 5290-5294)
  - `_row_is_hot` (function, lines 5297-5298)
  - `_hotspot_index` (function, lines 5301-5322)
  - `_compress_rows_keep_hotspot` (function, lines 5325-5372)
  - `_focused_diff_rows_from_opcodes` (function, lines 5375-5507)
  - `make_numbered_diff` (function, lines 5510-5540)
  - `render_numbered_diff_text` (function, lines 5542-5554)
