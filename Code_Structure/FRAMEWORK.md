# Code_Structure Framework

## Overview

- Source file: `/Users/Fona/Downloads/Clouds_Upload/Clouds_Coder.py`
- Output directory: `/Users/Fona/Downloads/Clouds_Upload/Code_Structure`
- Generated modules: 30
- Top-level symbols: 635
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
| `config/constants.py` | 373 | `utils/json_utils.py`, `utils/misc.py` |
| `config/paths.py` | 8 | `utils/text.py` |
| `config/settings.py` | 40 | `config/constants.py`, `config/paths.py`, `llm/utils.py`, `skills/store.py`, `utils/http.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` |
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
- Cross-module imports: `app/context.py`: `AppContext`; `config/constants.py`: `AGENT_MAX_OUTPUT_TOKENS`, `ARBITER_DEFAULT_MAX_TOKENS`, `ARBITER_DEFAULT_TEMPERATURE`, `ARBITER_DEFAULT_TIMEOUT_SECONDS`, `CODE_ADMIN_PORT_OFFSET`, `DEFAULT_AUTO_TASK_LEVEL_CEILING`, `DEFAULT_CONTEXT_TOKEN_LIMIT`, `DEFAULT_OLLAMA_BASE_URL`, `DEFAULT_OLLAMA_MODEL`, `DEFAULT_READ_CONTEXT_POLICY`, `DEFAULT_SHELL_COMMAND_TIMEOUT_SECONDS`, `DEFAULT_TOOL_MEMORY_POLICY`, `DEFAULT_UI_LANGUAGE`, `DEFAULT_UI_STYLE`, `DEFAULT_WEB_UI_CONFIG`, `DEFAULT_WEB_UI_DIR`, `EXECUTION_MODE_SYNC`, `LIVE_INPUT_DELAY_NORMAL_ROUNDS`, `LIVE_INPUT_DELAY_TOOL_ROUNDS`, `LIVE_INPUT_DELAY_WRITE_ROUNDS`, `LIVE_INPUT_MAX_INJECTIONS`, `LIVE_INPUT_REINJECT_INTERVAL`, `LIVE_INPUT_WEIGHT_BASE_DELAYED`, `LIVE_INPUT_WEIGHT_BASE_NORMAL`, `LIVE_INPUT_WEIGHT_STEP_DELAYED`, `LIVE_INPUT_WEIGHT_STEP_NORMAL`, `MAX_AGENT_ROUNDS`, `MAX_AGENT_ROUNDS_CAP`, `MAX_RUN_SECONDS`, `MAX_RUN_TIMEOUT_SECONDS`, `MAX_SHELL_COMMAND_TIMEOUT_SECONDS`, `MIN_AGENT_ROUNDS`, `MIN_CONTEXT_TOKEN_LIMIT`, `MIN_RUN_TIMEOUT_SECONDS`, `MIN_SHELL_COMMAND_TIMEOUT_SECONDS`, `OFFLINE_JS_LIB_CATALOG`, `RAG_ADMIN_PORT_OFFSET`, `RAG_INCLUDE_FILENAME_ENTITIES_DEFAULT`, `TOKEN_THRESHOLD`, `UI_LANGUAGE_LABELS`, `UI_STYLE_LABELS`; `config/paths.py`: `LLM_CONFIG_PATH`, `REPO_ROOT`, `WORKDIR`; `config/settings.py`: `_to_bool_like`, `extract_auto_task_level_ceiling_setting`, `extract_context_token_limit_setting`, `extract_daily_session_limit_setting`, `extract_js_lib_download_setting`, `extract_read_context_policy_setting`, `extract_shell_command_timeout_setting`, `extract_show_upload_list_setting`, `extract_tool_memory_policy_setting`, `extract_ui_style_setting`, `load_llm_config_from_source`, `load_web_ui_config_file`, `normalize_auto_task_level_ceiling`, `normalize_execution_mode`, `normalize_read_context_policy`, `normalize_tool_memory_policy`, `normalize_ui_language`, `normalize_ui_style`, `parse_llm_config_profiles`, `resolve_optional_file_path`, `resolve_web_ui_dir_path`, `select_preferred_skills_root`; `llm/utils.py`: `list_ollama_models`; `server/handlers.py`: `AgentHTTPServer`, `CodeAdminHandler`, `Handler`, `RagAdminHandler`, `SkillsHandler`; `skills/store.py`: `ensure_embedded_skills_at_root`, `ensure_runtime_skills`; `utils/files.py`: `ensure_offline_js_libs`; `utils/misc.py`: `BENIGN_SOCKET_DEBUG_LOG_ENABLED`, `detect_local_lan_ip`, `normalize_timeout_seconds`, `now_ts`, `swallow_benign_socket_error`; `utils/text.py`: `trim`
- Symbols:
  - `main` (function, lines 70603-71709)
  - `_main_guard_71711` (main_guard, lines 71711-71712)

### `agent/background.py`

- Routed symbols: 1
- Cross-module imports: `utils/misc.py`: `make_id`, `now_ts`; `utils/text.py`: `trim`
- Symbols:
  - `BackgroundManager` (class, lines 11821-11901)

### `agent/bus.py`

- Routed symbols: 1
- Cross-module imports: `config/constants.py`: `VALID_MSG_TYPES`; `utils/crypto.py`: `CryptoBox`; `utils/misc.py`: `now_ts`
- Symbols:
  - `MessageBus` (class, lines 11903-11967)

### `agent/events.py`

- Routed symbols: 1
- Cross-module imports: none
- Symbols:
  - `EventHub` (class, lines 5922-5967)

### `agent/tasks.py`

- Routed symbols: 1
- Cross-module imports: `utils/crypto.py`: `CryptoBox`; `utils/json_utils.py`: `json_dumps`; `utils/misc.py`: `now_ts`
- Symbols:
  - `TaskManager` (class, lines 11693-11819)

### `agent/todo.py`

- Routed symbols: 1
- Cross-module imports: `config/constants.py`: `DEFAULT_UI_LANGUAGE`; `config/settings.py`: `backend_i18n_text`, `backend_role_label`, `normalize_ui_language`; `utils/text.py`: `infer_todo_status_from_text`, `normalize_work_text`, `split_structured_todo_content`, `trim`
- Symbols:
  - `TodoManager` (class, lines 5969-6238)

### `agent/worktree.py`

- Routed symbols: 1
- Cross-module imports: `agent/tasks.py`: `TaskManager`; `config/constants.py`: `DANGEROUS_PATTERNS`; `utils/crypto.py`: `CryptoBox`; `utils/json_utils.py`: `json_dumps`; `utils/misc.py`: `now_ts`; `utils/text.py`: `trim`
- Symbols:
  - `WorktreeManager` (class, lines 11969-12184)

### `app/context.py`

- Routed symbols: 1
- Cross-module imports: `config/constants.py`: `AGENT_MAX_OUTPUT_TOKENS`, `APP_CSS`, `APP_JS`, `APP_TS`, `ARBITER_DEFAULT_MAX_TOKENS`, `ARBITER_DEFAULT_TEMPERATURE`, `ARBITER_DEFAULT_TIMEOUT_SECONDS`, `CODE_ADMIN_CSS`, `CODE_ADMIN_INDEX_HTML`, `CODE_ADMIN_JS`, `CODE_IMPORT_WORKER_COUNT`, `CODE_LIBRARY_DIRNAME`, `CODE_PARSE_TIMEOUT_SECONDS`, `DEFAULT_AUTO_TASK_LEVEL_CEILING`, `DEFAULT_CONTEXT_TOKEN_LIMIT`, `DEFAULT_READ_CONTEXT_POLICY`, `DEFAULT_REQUEST_TIMEOUT`, `DEFAULT_SHELL_COMMAND_TIMEOUT_SECONDS`, `DEFAULT_TOOL_MEMORY_POLICY`, `DEFAULT_UI_LANGUAGE`, `DEFAULT_UI_STYLE`, `DEFAULT_WEB_UI_DIR`, `EXECUTION_MODE_SYNC`, `INDEX_HTML`, `MAX_AGENT_ROUNDS`, `MAX_AGENT_ROUNDS_CAP`, `MAX_RUN_SECONDS`, `MAX_RUN_TIMEOUT_SECONDS`, `MAX_SHELL_COMMAND_TIMEOUT_SECONDS`, `MIN_AGENT_ROUNDS`, `MIN_CONTEXT_TOKEN_LIMIT`, `MIN_RUN_TIMEOUT_SECONDS`, `MIN_SHELL_COMMAND_TIMEOUT_SECONDS`, `RAG_ADMIN_CSS`, `RAG_ADMIN_INDEX_HTML`, `RAG_ADMIN_JS`, `RAG_CONTEXT_BUDGETS`, `RAG_DENSE_DEFAULT_ENABLED`, `RAG_EMBEDDING_MODE_VALUES`, `RAG_GRAPH_MAX_NODES`, `RAG_HIGH_RECALL_MIN_POOL`, `RAG_HIGH_RECALL_POOL_MULTIPLIER`, `RAG_IMPORT_WORKER_COUNT`, `RAG_INCLUDE_FILENAME_ENTITIES_DEFAULT`, `RAG_LIBRARY_DIRNAME`, `RAG_MAX_GLOBAL_COMMUNITIES`, `RAG_MAX_IMPORT_BATCH_BYTES`, `RAG_MAX_IMPORT_BATCH_ITEMS`, `RAG_MAX_IMPORT_FILES`, `RAG_MAX_QUERY_RESULTS`, `RAG_MIN_SYNTHESIS_SCORE`, `RAG_NO_EVIDENCE_MESSAGE`, `RAG_NO_EVIDENCE_THRESHOLD`, `RAG_PARSE_TIMEOUT_SECONDS`, `RAG_QUERY_CONTEXT_CHARS`, `RAG_RETRIEVAL_MAX_PER_DOC`, `RAG_SYNTHESIS_MAX_PER_DOC`, `RAG_WEAK_EVIDENCE_MESSAGE`, `RAG_WEAK_MATCH_SCORE_CAP`, `SESSION_HEARTBEAT_STALE_SECONDS`, `SESSION_WATCHDOG_INTERVAL_SECONDS`, `SKILLS_APP_JS`, `SKILLS_EXTRA_CSS`, `SKILLS_INDEX_HTML`, `SKILL_REFRESH_MIN_INTERVAL_SECONDS`, `TOKEN_THRESHOLD`, `WEB_UI_OPTIONAL_FILES`, `WEB_UI_REQUIRED_FILES`; `config/paths.py`: `LLM_CONFIG_PATH`, `REPO_ROOT`, `_migrate_legacy_runtime_roots`; `config/settings.py`: `_to_bool_like`, `default_multimodal_capabilities`, `extract_auto_task_level_ceiling_setting`, `extract_read_context_policy_setting`, `extract_tool_memory_policy_setting`, `infer_model_multimodal_capabilities`, `merge_multimodal_capabilities`, `model_language_instruction`, `normalize_auto_task_level_ceiling`, `normalize_execution_mode`, `normalize_read_context_policy`, `normalize_tool_memory_policy`, `normalize_ui_language`, `normalize_ui_style`, `parse_capability_overrides`, `parse_llm_config_profiles`, `resolve_optional_file_path`, `resolve_web_ui_dir_path`; `llm/client.py`: `OllamaClient`; `llm/utils.py`: `extract_base_url`, `list_ollama_models_cached`; `rag/ingestion.py`: `CodeIngestionService`, `RAGIngestionService`, `_rag_embed_batch`, `_rag_embed_text`, `_rag_mmr_select`, `_rag_query_variants`; `rag/parsers.py`: `CodeContentParser`, `RAGContentParser`; `rag/store.py`: `CodeLibraryStore`, `RAGLibraryStore`, `WikiStore`, `WorkflowMemoryStore`; `session/manager.py`: `SessionCreationLimitExceeded`, `SessionManager`; `session/state.py`: `SessionState`; `skills/store.py`: `SkillStore`, `_sanitize_skill_slug`, `analyze_skill_building_knowledge`, `ensure_runtime_skills`; `utils/crypto.py`: `CryptoBox`; `utils/files.py`: `_resolve_js_lib_asset_path`, `ensure_offline_js_libs`, `load_offline_js_lib_index`, `offline_js_lib_root`, `safe_path`, `try_read_text`; `utils/json_utils.py`: `TOOLS`, `extract_json_object_from_text`, `json_dumps`, `parse_json_object`; `utils/misc.py`: `DEFAULT_TIMEOUT_SECONDS`, `MAX_TIMEOUT_SECONDS`, `MIN_TIMEOUT_SECONDS`, `normalize_timeout_seconds`, `now_ts`, `sanitize_profile_id`; `utils/text.py`: `parse_front_matter`, `trim`
- Symbols:
  - `AppContext` (class, lines 65639-69064)

### `config/constants.py`

- Routed symbols: 373
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
  - `DEFAULT_CONTEXT_TOKEN_LIMIT` (constant, lines 211-211)
  - `TOKEN_THRESHOLD` (constant, lines 212-212)
  - `CONTEXT_AUTO_COMPACT_RESERVE_RATIO` (constant, lines 213-216)
  - `CONTEXT_ESTIMATE_SAFETY_MULTIPLIER` (constant, lines 217-220)
  - `CONTEXT_USAGE_CALIBRATION_MAX` (constant, lines 221-224)
  - `CONTEXT_ACTUAL_USAGE_RECENT_SECONDS` (constant, lines 225-228)
  - `LARGE_FILE_AUTO_PAGE_BYTES` (constant, lines 229-232)
  - `LARGE_FILE_AUTO_PAGE_LINES` (constant, lines 233-236)
  - `LARGE_SOURCE_UPLOAD_EXCERPT_CHARS` (constant, lines 237-240)
  - `CHAT_UPLOAD_PARSE_QUEUE_MAX` (constant, lines 241-244)
  - `CHAT_UPLOAD_PARSE_TIMEOUT_SECONDS` (constant, lines 245-248)
  - `CHAT_UPLOAD_INLINE_TEXT_BYTES` (constant, lines 249-252)
  - `CHAT_UPLOAD_PARSE_MAX_BYTES` (constant, lines 253-259)
  - `CHAT_UPLOAD_ZIP_ENTRY_MAX_BYTES` (constant, lines 260-266)
  - `CHAT_UPLOAD_TEXT_CONTEXT_CHARS` (constant, lines 267-270)
  - `CHAT_UPLOAD_PROMPT_MAX_FILES` (constant, lines 271-274)
  - `CHAT_UPLOAD_PROMPT_MAX_CHARS` (constant, lines 275-278)
  - `CHAT_UPLOAD_PROMPT_PER_FILE_CHARS` (constant, lines 279-282)
  - `CHAT_UPLOAD_FRONTEND_WAIT_MS` (constant, lines 283-286)
  - `CHAT_UPLOAD_AUTO_LIBRARY_INGEST` (constant, lines 287-290)
  - `CHAT_UPLOAD_INGEST_QUEUE_MAX` (constant, lines 291-294)
  - `SESSION_SUBMIT_LOCK_TIMEOUT_SECONDS` (constant, lines 295-298)
  - `SESSION_DEFERRED_START_QUEUE_MAX` (constant, lines 299-302)
  - `SESSION_WATCHDOG_INTERVAL_SECONDS` (constant, lines 303-306)
  - `SESSION_HEARTBEAT_STALE_SECONDS` (constant, lines 307-310)
  - `SESSION_LIST_DEFAULT_LIMIT` (constant, lines 311-314)
  - `IDLE_TIMEOUT` (constant, lines 315-315)
  - `POLL_INTERVAL` (constant, lines 316-316)
  - `SSE_HEARTBEAT_SECONDS` (constant, lines 317-317)
  - `MODEL_CALL_PROGRESS_DELAY` (constant, lines 318-318)
  - `MODEL_CALL_PROGRESS_INTERVAL` (constant, lines 319-319)
  - `RUN_COMPLETION_SUMMARY_ENABLED` (constant, lines 320-323)
  - `LLM_HTTP_RETRY_MAX_ATTEMPTS` (constant, lines 324-327)
  - `LLM_HTTP_RETRY_DELAY_SECONDS` (constant, lines 328-331)
  - `LLM_HTTP_RETRY_MAX_SECONDS` (constant, lines 332-335)
  - `LLM_HTTP_RETRY_404_ON_VLLM` (constant, lines 336-339)
  - `LLM_HTTP_RETRY_STATUSES` (constant, lines 340-340)
  - `MAX_AGENT_ROUNDS` (constant, lines 341-341)
  - `MIN_AGENT_ROUNDS` (constant, lines 342-342)
  - `MAX_AGENT_ROUNDS_CAP` (constant, lines 343-343)
  - `REPEATED_TOOL_LOOP_THRESHOLD` (constant, lines 344-344)
  - `BASH_READ_LOOP_THRESHOLD` (constant, lines 345-345)
  - `READ_FILE_LOOP_THRESHOLD` (constant, lines 346-346)
  - `READ_FILE_LOOP_DISTINCT_SOFT_LIMIT` (constant, lines 347-347)
  - `READ_FILE_COMPACT_PIN_DISTINCT` (constant, lines 348-348)
  - `READ_FILE_COMPACT_PIN_MAX_CHARS` (constant, lines 349-349)
  - `READ_CONTEXT_REGISTRY_MAX` (constant, lines 350-350)
  - `READ_CONTEXT_PROMPT_MAX_ITEMS` (constant, lines 351-351)
  - `READ_CONTEXT_PROMPT_MAX_CHARS` (constant, lines 352-352)
  - `READ_CONTEXT_SUMMARY_MAX_CHARS` (constant, lines 353-353)
  - `READ_CONTEXT_SHARED_MAX_ITEMS` (constant, lines 354-354)
  - `READ_CONTEXT_POLICY_CHOICES` (constant, lines 355-355)
  - `DEFAULT_READ_CONTEXT_POLICY` (constant, lines 356-356)
  - `TOOL_MEMORY_REGISTRY_MAX` (constant, lines 357-357)
  - `TOOL_MEMORY_PROMPT_MAX_ITEMS` (constant, lines 358-358)
  - `TOOL_MEMORY_PROMPT_MAX_CHARS` (constant, lines 359-359)
  - `TOOL_MEMORY_SUMMARY_MAX_CHARS` (constant, lines 360-360)
  - `TOOL_MEMORY_SHARED_MAX_ITEMS` (constant, lines 361-361)
  - `TOOL_MEMORY_COMPACT_PIN_DISTINCT` (constant, lines 362-362)
  - `TOOL_MEMORY_COMPACT_PIN_MAX_CHARS` (constant, lines 363-363)
  - `TOOL_MEMORY_POLICY_CHOICES` (constant, lines 364-364)
  - `DEFAULT_TOOL_MEMORY_POLICY` (constant, lines 365-365)
  - `DEFAULT_AUTO_TASK_LEVEL_CEILING` (constant, lines 366-366)
  - `HARD_BREAK_TOOL_ERROR_THRESHOLD` (constant, lines 367-367)
  - `HARD_BREAK_RECOVERY_ROUND_THRESHOLD` (constant, lines 368-368)
  - `FUSED_FAULT_BREAK_THRESHOLD` (constant, lines 369-369)
  - `STALL_SEVERITY_ESCALATION_THRESHOLD` (constant, lines 370-370)
  - `STALL_SEVERITY_WEIGHT_BASH_READ_LOOP` (constant, lines 371-371)
  - `STALL_SEVERITY_WEIGHT_REPEATED_TOOL` (constant, lines 372-372)
  - `STALL_SEVERITY_WEIGHT_FAULT` (constant, lines 373-373)
  - `STALL_SEVERITY_WEIGHT_RECOVERY_RETRY` (constant, lines 374-374)
  - `STALL_SEVERITY_WEIGHT_WATCHDOG` (constant, lines 375-375)
  - `STALL_SEVERITY_DECAY_ON_SUCCESS` (constant, lines 376-376)
  - `STALL_ESCALATION_MIN_LEVEL` (constant, lines 377-377)
  - `STALL_PLAN_SYNTHESIS_MAX_TOKENS` (constant, lines 378-378)
  - `STALL_ESCALATION_CONTEXT_MAX_CHARS` (constant, lines 379-379)
  - `MAX_RUN_SECONDS` (constant, lines 380-380)
  - `MIN_RUN_TIMEOUT_SECONDS` (constant, lines 381-381)
  - `MAX_RUN_TIMEOUT_SECONDS` (constant, lines 382-382)
  - `DEFAULT_REQUEST_TIMEOUT` (constant, lines 392-392)
  - `_SHELL_AUTO_CONFIRM_PATTERNS` (assignment, lines 395-408)
  - `MIN_SHELL_COMMAND_TIMEOUT_SECONDS` (constant, lines 409-409)
  - `MAX_SHELL_COMMAND_TIMEOUT_SECONDS` (constant, lines 410-410)
  - `DEFAULT_SHELL_COMMAND_TIMEOUT_SECONDS` (constant, lines 411-425)
  - `AUTO_CONTINUE_BUDGET_DEFAULT` (constant, lines 426-426)
  - `AGENT_MAX_OUTPUT_TOKENS` (constant, lines 427-427)
  - `OLLAMA_THINKING_TOOL_BUFFER` (constant, lines 428-428)
  - `WATCHDOG_INTENT_NO_TOOL_THRESHOLD` (constant, lines 429-429)
  - `WATCHDOG_REPEAT_NO_TOOL_THRESHOLD` (constant, lines 430-430)
  - `WATCHDOG_INTENT_NO_TOOL_THRESHOLD_SINGLE` (constant, lines 431-431)
  - `WATCHDOG_REPEAT_NO_TOOL_THRESHOLD_SINGLE` (constant, lines 432-432)
  - `WATCHDOG_STATE_STALL_THRESHOLD` (constant, lines 433-433)
  - `WATCHDOG_CONTEXT_STALL_THRESHOLD` (constant, lines 434-434)
  - `WATCHDOG_REPEAT_SIMILARITY_THRESHOLD` (constant, lines 435-435)
  - `WATCHDOG_CONTEXT_NEAR_RATIO` (constant, lines 436-436)
  - `WATCHDOG_MAX_DECOMPOSE_STEPS` (constant, lines 437-437)
  - `WATCHDOG_STEP_MAX_ATTEMPTS` (constant, lines 438-438)
  - `EMPTY_ACTION_MIN_CONTENT_CHARS` (constant, lines 439-439)
  - `EMPTY_ACTION_WAKEUP_RETRY_LIMIT` (constant, lines 440-440)
  - `THINKING_BUDGET_FORCE_RATIO` (constant, lines 441-441)
  - `_TOOL_TIMEOUT_MAP` (assignment, lines 443-459)
  - `_DEFAULT_TOOL_TIMEOUT` (assignment, lines 460-460)
  - `TRUNCATION_CONTINUATION_MAX_PASSES` (constant, lines 461-461)
  - `TRUNCATION_CONTINUATION_MAX_TOKENS` (constant, lines 462-462)
  - `TRUNCATION_CONTINUATION_TAIL_CHARS` (constant, lines 463-463)
  - `TRUNCATION_CONTINUATION_ECHO_CHARS` (constant, lines 464-464)
  - `TRUNCATION_OVERLAP_SCAN_CHARS` (constant, lines 465-465)
  - `TRUNCATION_PAIR_SCAN_CHARS` (constant, lines 466-466)
  - `TRUNCATION_LIVE_BUFFER_MAX_CHARS` (constant, lines 467-467)
  - `MIN_CONTEXT_TOKEN_LIMIT` (constant, lines 468-468)
  - `COMPACT_TIER1_PCT` (constant, lines 470-470)
  - `COMPACT_TIER2_PCT` (constant, lines 471-471)
  - `COMPACT_TIER3_PCT` (constant, lines 472-472)
  - `COMPACT_TIER1_ABS` (constant, lines 474-474)
  - `COMPACT_TIER2_ABS` (constant, lines 475-475)
  - `CONTEXT_COMPACT_INEFFECTIVE_COOLDOWN_SECONDS` (constant, lines 476-482)
  - `FILE_BUFFER_CONTENT_THRESHOLD` (constant, lines 484-484)
  - `FILE_BUFFER_MAX_FILES` (constant, lines 485-485)
  - `AGENT_MSG_LIMIT_TIER0` (constant, lines 487-487)
  - `AGENT_MSG_LIMIT_TIER1` (constant, lines 488-488)
  - `AGENT_MSG_LIMIT_TIER2` (constant, lines 489-489)
  - `AGENT_MSG_LIMIT_TIER3` (constant, lines 490-490)
  - `AGENT_CTX_LIMIT_TIER0` (constant, lines 491-491)
  - `AGENT_CTX_LIMIT_TIER1` (constant, lines 492-492)
  - `AGENT_CTX_LIMIT_TIER2` (constant, lines 493-493)
  - `AGENT_CTX_LIMIT_TIER3` (constant, lines 494-494)
  - `MANAGER_CTX_LIMIT_TIER0` (constant, lines 495-495)
  - `MANAGER_CTX_LIMIT_TIER1` (constant, lines 496-496)
  - `MANAGER_CTX_LIMIT_TIER2` (constant, lines 497-497)
  - `MANAGER_CTX_LIMIT_TIER3` (constant, lines 498-498)
  - `MAX_CONTEXT_ARCHIVE_SEGMENTS` (constant, lines 499-499)
  - `MODEL_OUTPUT_RETRY_TIMES` (constant, lines 500-500)
  - `ARBITER_TRIGGER_MIN_CONTENT_CHARS` (constant, lines 501-501)
  - `ARBITER_VALID_PLANNING_STREAK_LIMIT` (constant, lines 502-502)
  - `ARBITER_DEFAULT_TIMEOUT_SECONDS` (constant, lines 503-503)
  - `ARBITER_DEFAULT_MAX_TOKENS` (constant, lines 504-504)
  - `ARBITER_DEFAULT_TEMPERATURE` (constant, lines 505-505)
  - `LIVE_INPUT_DELAY_WRITE_ROUNDS` (constant, lines 506-506)
  - `LIVE_INPUT_DELAY_TOOL_ROUNDS` (constant, lines 507-507)
  - `LIVE_INPUT_DELAY_NORMAL_ROUNDS` (constant, lines 508-508)
  - `LIVE_INPUT_MAX_INJECTIONS` (constant, lines 509-509)
  - `LIVE_INPUT_REINJECT_INTERVAL` (constant, lines 510-510)
  - `LIVE_INPUT_WEIGHT_BASE_DELAYED` (constant, lines 511-511)
  - `LIVE_INPUT_WEIGHT_BASE_NORMAL` (constant, lines 512-512)
  - `LIVE_INPUT_WEIGHT_STEP_DELAYED` (constant, lines 513-513)
  - `LIVE_INPUT_WEIGHT_STEP_NORMAL` (constant, lines 514-514)
  - `FINAL_SUMMARY_MIN_CHARS` (constant, lines 529-529)
  - `FINAL_SUMMARY_STRICT_MIN_CHARS` (constant, lines 530-530)
  - `RUNTIME_CONTROL_HINT_PREFIXES` (constant, lines 531-548)
  - `RETRY_RUNTIME_HINT_PREFIXES` (constant, lines 549-563)
  - `EXECUTION_MODE_SINGLE` (constant, lines 564-564)
  - `EXECUTION_MODE_SEQUENTIAL` (constant, lines 565-565)
  - `EXECUTION_MODE_SYNC` (constant, lines 566-566)
  - `EXECUTION_MODE_CHOICES` (constant, lines 567-571)
  - `AGENT_ROLES` (constant, lines 572-572)
  - `AGENT_BUBBLE_ROLES` (constant, lines 573-573)
  - `AGENT_ROLE_LABELS` (constant, lines 574-580)
  - `AGENT_ROLE_BUBBLE_COLORS` (constant, lines 581-587)
  - `BLACKBOARD_STATUSES` (constant, lines 588-597)
  - `TASK_COMPLEXITY_LEVELS` (constant, lines 598-598)
  - `TASK_COMPLEXITY_RANKS` (constant, lines 599-604)
  - `TASK_PROFILE_TYPES` (constant, lines 605-611)
  - `TASK_LEVEL_CHOICES` (constant, lines 612-612)
  - `TASK_SCALE_PREFERENCES` (constant, lines 613-613)
  - `SEMANTIC_CONFIDENCE_CHOICES` (constant, lines 614-614)
  - `TASK_LEVEL_POLICIES` (constant, lines 615-661)
  - `MANAGER_ROUTE_TARGETS` (constant, lines 662-662)
  - `BLACKBOARD_MAX_LOG_ENTRIES` (constant, lines 663-663)
  - `BLACKBOARD_MAX_TEXT` (constant, lines 664-664)
  - `BLACKBOARD_MEMORY_SHORT_MAX` (constant, lines 665-665)
  - `BLACKBOARD_MEMORY_MID_MAX_STEPS` (constant, lines 666-666)
  - `BLACKBOARD_MEMORY_MID_ITEMS_PER_STEP` (constant, lines 667-667)
  - `BLACKBOARD_MEMORY_LONG_MAX` (constant, lines 668-668)
  - `BLACKBOARD_MEMORY_INDEX_MAX` (constant, lines 669-669)
  - `SKILL_REFRESH_MIN_INTERVAL_SECONDS` (constant, lines 670-670)
  - `SKILL_PROMPT_MAX_ITEMS` (constant, lines 671-671)
  - `SKILL_PROMPT_MAX_CHARS` (constant, lines 672-672)
  - `SKILL_RUNTIME_CACHE_MAX_ENTRIES` (constant, lines 673-673)
  - `SKILL_RUNTIME_CACHE_MAX_BYTES` (constant, lines 674-674)
  - `AUTO_SKILLS_ROOT_CANDIDATES` (constant, lines 675-675)
  - `SKILL_DEFAULT_ATTACHMENT_GLOBS` (constant, lines 676-706)
  - `SKILL_INLINE_ATTACHMENT_MAX_FILES` (constant, lines 707-707)
  - `SKILL_INLINE_ATTACHMENT_MAX_CHARS` (constant, lines 708-708)
  - `SKILL_RESOURCE_MANIFEST_MAX_ITEMS` (constant, lines 709-709)
  - `SKILL_BODY_COMPACT_THRESHOLD_CHARS` (constant, lines 710-710)
  - `SKILL_BODY_PREVIEW_CHARS` (constant, lines 711-711)
  - `SKILLS_VIRTUAL_PREFIX` (constant, lines 712-712)
  - `SKILLS_EXTERNAL_MOUNT` (constant, lines 713-713)
  - `PLAN_MODE_ENABLED_LEVELS` (constant, lines 714-714)
  - `PLAN_MODE_FORCED_LEVELS` (constant, lines 715-715)
  - `PLAN_MODE_USER_CHOICES` (constant, lines 716-716)
  - `TASK_PHASES` (constant, lines 718-718)
  - `TASK_PHASE_ROUTING` (constant, lines 719-726)
  - `COMPLEXITY_KEYWORDS` (constant, lines 728-733)
  - `USER_COMPLEXITY_SIMPLE_TOKENS` (constant, lines 734-738)
  - `USER_COMPLEXITY_MODERATE_TOKENS` (constant, lines 739-743)
  - `USER_COMPLEXITY_COMPLEX_TOKENS` (constant, lines 744-748)
  - `USER_COMPLEXITY_EXPERT_TOKENS` (constant, lines 749-753)
  - `PLAN_MODE_EXPLORER_MAX_ROUNDS` (constant, lines 754-754)
  - `PLAN_MODE_SYNTHESIS_MAX_ATTEMPTS` (constant, lines 755-755)
  - `REVIEWER_DEBUG_MODE_MAX_ROUNDS` (constant, lines 757-757)
  - `REVIEWER_DEBUG_TOOL_ALLOWLIST` (constant, lines 758-762)
  - `EXPLORER_STALL_THRESHOLD` (constant, lines 763-763)
  - `DEVELOPER_EDIT_STALL_THRESHOLD` (constant, lines 764-764)
  - `PLAN_MODE_MANAGER_SYNTHESIS_MAX_TOKENS` (constant, lines 765-765)
  - `PLAN_MODE_MAX_OPTIONS` (constant, lines 766-766)
  - `PLAN_FILE_RELATIVE_PATH` (constant, lines 767-767)
  - `PLAN_BUBBLE_MAX_CHARS` (constant, lines 768-768)
  - `PLAN_NOTICE_BODY_MAX_CHARS` (constant, lines 769-769)
  - `PLAN_MESSAGE_EVENT_MAX_CHARS` (constant, lines 770-770)
  - `PLAN_STEP_FULL_CONTENT_MAX_CHARS` (constant, lines 771-771)
  - `PLAN_MODE_RESEARCH_TOOL_ALLOWLIST` (constant, lines 772-776)
  - `FAILURE_LEDGER_MAX_FIXES` (constant, lines 777-777)
  - `FAILURE_LEDGER_MAX_COMPILE_ERRORS` (constant, lines 778-778)
  - `FAILURE_LEDGER_MAX_DELEGATIONS` (constant, lines 779-779)
  - `FAILURE_LEDGER_MAX_STALLS` (constant, lines 780-780)
  - `FAILURE_LEDGER_MAX_TOOL_FPS` (constant, lines 781-781)
  - `FAILURE_LEDGER_MAX_ERRORS` (constant, lines 782-782)
  - `ERROR_CATEGORY_DEFS` (constant, lines 785-822)
  - `CHECKPOINT_MAX_COUNT` (constant, lines 823-823)
  - `CHECKPOINT_INTERVAL_ROUNDS` (constant, lines 824-824)
  - `PERSISTED_ROUTES_MAX` (constant, lines 825-825)
  - `HTML_FRONTEND_REQUEST_KEYWORDS` (constant, lines 826-865)
  - `DEEP_RESEARCH_REQUEST_KEYWORDS` (constant, lines 866-888)
  - `DEEP_RESEARCH_RETRIEVAL_KEYWORDS` (constant, lines 889-908)
  - `DEEP_RESEARCH_TEXT_ONLY_HINT_KEYWORDS` (constant, lines 909-926)
  - `DANGEROUS_PATTERNS` (constant, lines 928-928)
  - `VALID_MSG_TYPES` (constant, lines 929-935)
  - `SUPPORTED_UI_LANGUAGES` (constant, lines 937-942)
  - `UI_LANGUAGE_LABELS` (constant, lines 943-943)
  - `DEFAULT_UI_LANGUAGE` (constant, lines 944-944)
  - `UI_STYLE_CHOICES` (constant, lines 945-945)
  - `UI_STYLE_LABELS` (constant, lines 946-946)
  - `DEFAULT_UI_STYLE` (constant, lines 947-947)
  - `DEFAULT_WEB_UI_DIR` (constant, lines 948-948)
  - `DEFAULT_WEB_UI_CONFIG` (constant, lines 949-949)
  - `WEB_UI_REQUIRED_FILES` (constant, lines 950-957)
  - `WEB_UI_OPTIONAL_FILES` (constant, lines 958-958)
  - `IMAGE_EXTS` (constant, lines 960-973)
  - `IMAGE_FORMATS_NEED_CONVERSION` (constant, lines 974-974)
  - `IMAGE_SAFE_FORMATS` (constant, lines 975-975)
  - `AUDIO_EXTS` (constant, lines 976-986)
  - `VIDEO_EXTS` (constant, lines 987-997)
  - `CODE_PREVIEW_STAGE_MAX_BYTES` (constant, lines 998-998)
  - `CODE_PREVIEW_STAGE_MAX_ROWS` (constant, lines 999-999)
  - `CODE_PREVIEW_STAGE_MAX_PER_FILE` (constant, lines 1000-1000)
  - `CODE_PREVIEW_STAGE_MAX_TOTAL` (constant, lines 1001-1001)
  - `CODE_PREVIEW_DIFF_CONTEXT_LINES` (constant, lines 1002-1002)
  - `CODE_PREVIEW_DIFF_MERGE_GAP` (constant, lines 1003-1003)
  - `PREVIEW_DOWNLOAD_MAX_FILES` (constant, lines 1004-1004)
  - `PREVIEW_DOWNLOAD_MAX_BYTES` (constant, lines 1005-1005)
  - `RENDER_FRAME_MAX_B64_CHARS` (constant, lines 1006-1006)
  - `RENDER_FRAME_MAX_POINTS` (constant, lines 1007-1007)
  - `RENDER_FRAME_MAX_LINES` (constant, lines 1008-1008)
  - `RENDER_FRAME_MAX_LINE_POINTS` (constant, lines 1009-1009)
  - `RENDER_FRAME_ACTIVITY_INTERVAL_SECONDS` (constant, lines 1010-1010)
  - `RAW_TOOLCALL_TEXT_FILTER_THRESHOLD` (constant, lines 1011-1011)
  - `ASSISTANT_TEXT_PERSIST_MAX_CHARS` (constant, lines 1012-1012)
  - `ASSISTANT_MESSAGE_EVENT_MAX_CHARS` (constant, lines 1013-1013)
  - `CODE_PREVIEW_EXTS` (constant, lines 1014-1139)
  - `CODE_PREVIEW_FILENAMES` (constant, lines 1140-1191)
  - `MEDIA_CAPABILITY_KEYS` (constant, lines 1192-1199)
  - `SAMPLE_IMAGE_PNG_B64` (constant, lines 1200-1203)
  - `SAMPLE_AUDIO_WAV_B64` (constant, lines 1204-1206)
  - `SAMPLE_VIDEO_MP4_B64` (constant, lines 1207-1209)
  - `OFFLINE_JS_LIB_CATALOG` (constant, lines 1211-1469)
  - `OFFLINE_JS_LIB_INDEX_FILE` (constant, lines 1470-1470)
  - `OFFLINE_JS_LIB_README_FILE` (constant, lines 1471-1471)
  - `BACKEND_I18N` (constant, lines 1657-1726)
  - `call_backend_i18n_en_update_l1728` (expression, lines 1728-1821)
  - `call_backend_i18n_zh_cn_update_l1822` (expression, lines 1822-1915)
  - `call_backend_i18n_zh_tw_update_l1916` (expression, lines 1916-2009)
  - `call_backend_i18n_ja_update_l2010` (expression, lines 2010-2103)
  - `OPENAI_COMPAT_PROVIDER_NAMES` (constant, lines 4295-4303)
  - `OPENAI_LIKE_PROVIDER_NAMES` (constant, lines 4305-4305)
  - `TABULAR_PREVIEW_EXTS` (constant, lines 5836-5836)
  - `EXCEL_PREVIEW_EXTS` (constant, lines 5837-5837)
  - `PRESENTATION_PREVIEW_EXTS` (constant, lines 5838-5838)
  - `DOCUMENT_PREVIEW_EXTS` (constant, lines 5839-5839)
  - `EMBEDDED_SKILLS_ARCHIVE_B64` (constant, lines 6240-6759)
  - `EMBEDDED_SKILLS_ARCHIVE_SHA256` (constant, lines 6760-6760)
  - `EMBEDDED_SKILLS_ARCHIVE_FILES` (constant, lines 6761-6784)
  - `BUILTIN_CLAWHUB_SKILLS_VERSION` (constant, lines 9941-9941)
  - `EMBEDDED_CLAWHUB_SKILLS_ARCHIVE_B64` (constant, lines 9943-10187)
  - `SKILL_PROTOCOL_LOCAL` (constant, lines 10253-10253)
  - `SKILL_PROTOCOL_CLAWHUB` (constant, lines 10254-10254)
  - `SKILL_PROTOCOL_HTTP_JSON` (constant, lines 10255-10255)
  - `SKILL_PROTOCOL_SPECS` (constant, lines 10257-10288)
  - `AGENT_TOOL_ALLOWLIST` (constant, lines 14062-14107)
  - `INDEX_HTML` (constant, lines 47390-47579)
  - `APP_CSS` (constant, lines 47581-47998)
  - `APP_JS` (constant, lines 48000-51504)
  - `APP_TS` (constant, lines 51506-51533)
  - `SKILLS_INDEX_HTML` (constant, lines 51535-51689)
  - `SKILLS_EXTRA_CSS` (constant, lines 51691-51786)
  - `SKILLS_APP_JS` (constant, lines 51788-51929)
  - `RAG_TERM_GROUPS` (constant, lines 51931-56563)
  - `RAG_RESEARCH_HINTS` (constant, lines 56564-56585)
  - `RAG_CODE_HINTS` (constant, lines 56586-56596)
  - `RAG_SHORT_TOKEN_ALLOWLIST` (constant, lines 56597-56612)
  - `RAG_EN_STOPWORDS` (constant, lines 56613-56685)
  - `RAG_ZH_STOPWORDS` (constant, lines 56686-56722)
  - `RAG_GENERIC_ENTITY_TERMS_EN` (constant, lines 56723-56801)
  - `RAG_GENERIC_ENTITY_TERMS_ZH` (constant, lines 56802-56844)
  - `RAG_STRUCTURAL_ENTITY_PATTERNS` (constant, lines 56845-56863)
  - `CODE_LIBRARY_IGNORED_DIRS` (constant, lines 57556-57561)
  - `CODE_LIBRARY_LANGUAGE_BY_EXT` (constant, lines 57562-57618)
  - `CODE_LIBRARY_SPECIAL_FILENAMES` (constant, lines 57619-57625)
  - `RAG_ADMIN_INDEX_HTML` (constant, lines 63549-63722)
  - `RAG_ADMIN_CSS` (constant, lines 63724-63814)
  - `RAG_ADMIN_JS` (constant, lines 63816-65579)
  - `CODE_ADMIN_INDEX_HTML` (constant, lines 65581-65592)
  - `CODE_ADMIN_CSS` (constant, lines 65593-65623)
  - `CODE_ADMIN_JS` (constant, lines 65624-65628)

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
  - `detect_repo_root` (function, lines 2890-2904)
  - `REPO_ROOT` (constant, lines 2906-2906)

### `config/settings.py`

- Routed symbols: 40
- Cross-module imports: `config/constants.py`: `AUTO_SKILLS_ROOT_CANDIDATES`, `BACKEND_I18N`, `DEFAULT_AUTO_TASK_LEVEL_CEILING`, `DEFAULT_READ_CONTEXT_POLICY`, `DEFAULT_REQUEST_TIMEOUT`, `DEFAULT_SHELL_COMMAND_TIMEOUT_SECONDS`, `DEFAULT_TOOL_MEMORY_POLICY`, `DEFAULT_UI_LANGUAGE`, `DEFAULT_UI_STYLE`, `DEFAULT_WEB_UI_CONFIG`, `DEFAULT_WEB_UI_DIR`, `EXECUTION_MODE_CHOICES`, `EXECUTION_MODE_SEQUENTIAL`, `EXECUTION_MODE_SINGLE`, `EXECUTION_MODE_SYNC`, `MAX_SHELL_COMMAND_TIMEOUT_SECONDS`, `MEDIA_CAPABILITY_KEYS`, `MIN_SHELL_COMMAND_TIMEOUT_SECONDS`, `READ_CONTEXT_POLICY_CHOICES`, `SUPPORTED_UI_LANGUAGES`, `TASK_COMPLEXITY_LEVELS`, `TASK_COMPLEXITY_RANKS`, `TASK_LEVEL_CHOICES`, `UI_LANGUAGE_LABELS`, `UI_STYLE_CHOICES`, `USER_COMPLEXITY_COMPLEX_TOKENS`, `USER_COMPLEXITY_EXPERT_TOKENS`, `USER_COMPLEXITY_MODERATE_TOKENS`, `USER_COMPLEXITY_SIMPLE_TOKENS`; `config/paths.py`: `WORKDIR`; `llm/utils.py`: `_is_http_url`, `_resolve_local_path`, `complete_chat_endpoint`, `extract_base_url`, `is_openai_like_provider`, `normalize_openai_compat_provider_name`, `strip_thinking_content`; `skills/store.py`: `ensure_embedded_skills`; `utils/http.py`: `urlopen`; `utils/json_utils.py`: `parse_json_object`; `utils/misc.py`: `MAX_TIMEOUT_SECONDS`, `MIN_TIMEOUT_SECONDS`, `normalize_timeout_seconds`, `sanitize_profile_id`; `utils/text.py`: `trim`
- Symbols:
  - `normalize_ui_language` (function, lines 1555-1577)
  - `normalize_ui_style` (function, lines 1580-1597)
  - `supported_ui_languages_payload` (function, lines 1600-1601)
  - `normalize_execution_mode` (function, lines 1604-1623)
  - `model_language_instruction` (function, lines 1626-1654)
  - `backend_i18n_text` (function, lines 2106-2116)
  - `backend_role_label` (function, lines 2119-2123)
  - `_detect_os_shell_instruction` (function, lines 2126-2165)
  - `resolve_web_ui_dir_path` (function, lines 2167-2174)
  - `resolve_optional_file_path` (function, lines 2177-2184)
  - `resolve_skills_root_path` (function, lines 2187-2194)
  - `_count_skill_markdown_files` (function, lines 2197-2208)
  - `select_preferred_skills_root` (function, lines 2211-2245)
  - `load_web_ui_config_file` (function, lines 2248-2262)
  - `extract_show_upload_list_setting` (function, lines 2265-2279)
  - `extract_ui_style_setting` (function, lines 2282-2296)
  - `extract_js_lib_download_setting` (function, lines 2299-2318)
  - `extract_daily_session_limit_setting` (function, lines 2321-2364)
  - `extract_shell_command_timeout_setting` (function, lines 2367-2413)
  - `extract_context_token_limit_setting` (function, lines 2416-2448)
  - `normalize_auto_task_level_ceiling` (function, lines 2451-2470)
  - `extract_auto_task_level_ceiling_setting` (function, lines 2473-2500)
  - `normalize_read_context_policy` (function, lines 2503-2521)
  - `normalize_tool_memory_policy` (function, lines 2524-2525)
  - `extract_read_context_policy_setting` (function, lines 2528-2549)
  - `extract_tool_memory_policy_setting` (function, lines 2552-2573)
  - `default_multimodal_capabilities` (function, lines 2582-2590)
  - `_to_bool_like` (function, lines 2593-2603)
  - `infer_model_multimodal_capabilities` (function, lines 2606-2650)
  - `parse_capability_overrides` (function, lines 2653-2690)
  - `merge_multimodal_capabilities` (function, lines 2693-2700)
  - `parse_media_endpoints` (function, lines 2703-2717)
  - `infer_user_complexity_value` (function, lines 4213-4229)
  - `normalize_task_complexity` (function, lines 4231-4259)
  - `task_complexity_rank` (function, lines 4261-4262)
  - `task_complexity_at_least` (function, lines 4264-4265)
  - `max_task_complexity` (function, lines 4267-4276)
  - `load_llm_config_from_source` (function, lines 4427-4461)
  - `parse_llm_config_profiles` (function, lines 4463-5049)
  - `looks_like_llm_config` (function, lines 5051-5125)

### `llm/client.py`

- Routed symbols: 2
- Cross-module imports: `config/constants.py`: `DEFAULT_REQUEST_TIMEOUT`, `LLM_HTTP_RETRY_404_ON_VLLM`, `LLM_HTTP_RETRY_DELAY_SECONDS`, `LLM_HTTP_RETRY_MAX_ATTEMPTS`, `LLM_HTTP_RETRY_MAX_SECONDS`, `LLM_HTTP_RETRY_STATUSES`, `OLLAMA_THINKING_TOOL_BUFFER`, `SAMPLE_AUDIO_WAV_B64`, `SAMPLE_IMAGE_PNG_B64`, `SAMPLE_VIDEO_MP4_B64`; `config/settings.py`: `default_multimodal_capabilities`, `infer_model_multimodal_capabilities`, `merge_multimodal_capabilities`, `parse_capability_overrides`, `parse_media_endpoints`; `llm/utils.py`: `complete_chat_endpoint`, `is_openai_compat_provider`, `is_openai_like_provider`, `normalize_openai_compat_provider_name`, `split_thinking_content`; `utils/http.py`: `urlopen`; `utils/json_utils.py`: `canonicalize_tool_name`, `json_dumps`, `parse_json_object`, `parse_tool_arguments`, `parse_tool_arguments_with_error`; `utils/misc.py`: `MAX_TIMEOUT_SECONDS`, `MIN_TIMEOUT_SECONDS`, `make_id`, `normalize_timeout_seconds`, `now_ts`; `utils/text.py`: `trim`
- Symbols:
  - `OllamaError` (class, lines 12186-12206)
  - `OllamaClient` (class, lines 12208-13675)

### `llm/utils.py`

- Routed symbols: 25
- Cross-module imports: `config/constants.py`: `OPENAI_COMPAT_PROVIDER_NAMES`, `OPENAI_LIKE_PROVIDER_NAMES`; `utils/http.py`: `urlopen`; `utils/json_utils.py`: `json_dumps`, `parse_json_object`; `utils/text.py`: `trim`
- Symbols:
  - `probe_ollama_environment` (function, lines 3897-3910)
  - `list_ollama_models` (function, lines 3912-3914)
  - `_OLLAMA_TAG_CACHE_LOCK` (assignment, lines 3916-3916)
  - `_OLLAMA_TAG_CACHE` (assignment, lines 3917-3917)
  - `list_ollama_models_cached` (function, lines 3927-3964)
  - `resolve_ollama_model` (function, lines 3966-3976)
  - `infer_thinking_model` (function, lines 3978-3980)
  - `split_thinking_content` (function, lines 3982-4025)
  - `strip_thinking_content` (function, lines 4027-4028)
  - `check_ollama_model_ready` (function, lines 4030-4054)
  - `list_loaded_ollama_models` (function, lines 4056-4069)
  - `wake_ollama_model` (function, lines 4071-4101)
  - `try_pull_ollama_model` (function, lines 4103-4121)
  - `ordered_model_candidates` (function, lines 4123-4141)
  - `pick_working_ollama_model` (function, lines 4143-4159)
  - `extract_base_url` (function, lines 4192-4200)
  - `complete_chat_endpoint` (function, lines 4202-4211)
  - `normalize_openai_compat_provider_name` (function, lines 4278-4293)
  - `is_openai_compat_provider` (function, lines 4307-4308)
  - `is_openai_like_provider` (function, lines 4310-4311)
  - `openai_compat_probe_headers` (function, lines 4313-4324)
  - `openai_compat_model_list_urls` (function, lines 4326-4358)
  - `extract_openai_compat_model_ids` (function, lines 4360-4393)
  - `_is_http_url` (function, lines 4402-4407)
  - `_resolve_local_path` (function, lines 4409-4425)

### `rag/index.py`

- Routed symbols: 5
- Cross-module imports: `config/constants.py`: `RAG_DYNAMIC_NOISE_HARD_COMMUNITY_RATIO`, `RAG_DYNAMIC_NOISE_HARD_DOC_RATIO`, `RAG_DYNAMIC_NOISE_MIN_COMMUNITY_FREQ`, `RAG_DYNAMIC_NOISE_MIN_DOC_FREQ`, `RAG_DYNAMIC_NOISE_SOFT_COMMUNITY_RATIO`, `RAG_DYNAMIC_NOISE_SOFT_DOC_RATIO`, `RAG_EN_STOPWORDS`, `RAG_GRAPH_MAX_NODES`, `RAG_INCLUDE_FILENAME_ENTITIES_DEFAULT`, `RAG_MAX_COMMUNITY_MAP_SUPPORT`, `RAG_MAX_GLOBAL_COMMUNITIES`, `RAG_MAX_QUERY_RESULTS`, `RAG_MIN_SYNTHESIS_SCORE`, `RAG_WEAK_MATCH_SCORE_CAP`; `rag/ingestion.py`: `_rag_focused_excerpt`, `_rag_mmr_select`, `_rag_window_for_query`; `rag/parsers.py`: `_code_is_test_path`, `_rag_apply_filename_entity_policy`, `_rag_choose_community`, `_rag_classify_document`, `_rag_expand_tokens`, `_rag_extract_entities`, `_rag_filter_entities`, `_rag_tokenize`; `utils/misc.py`: `now_ts`; `utils/text.py`: `trim`
- Symbols:
  - `_code_module_name` (function, lines 57652-57666)
  - `_code_choose_community` (function, lines 57669-57676)
  - `_code_query_terms` (function, lines 57679-57691)
  - `TFGraphIDFIndex` (class, lines 58744-60310)
  - `CodeGraphIndex` (class, lines 62728-63193)

### `rag/ingestion.py`

- Routed symbols: 12
- Cross-module imports: `config/constants.py`: `CODE_IMPORT_WORKER_COUNT`, `CODE_LIBRARY_IGNORED_DIRS`, `CODE_PARSE_TIMEOUT_SECONDS`, `RAG_IMPORT_WORKER_COUNT`, `RAG_MAX_IMPORT_BATCH_ITEMS`, `RAG_MAX_IMPORT_FILES`, `RAG_MODEL_MEDIA_MAX_BYTES`, `RAG_PARSE_TIMEOUT_SECONDS`, `RAG_PDF_IMAGE_LIMIT`, `RAG_RETRIEVAL_MAX_PER_DOC`; `config/settings.py`: `default_multimodal_capabilities`; `rag/parsers.py`: `CodeContentParser`, `RAGContentParser`, `_rag_expand_tokens`, `_rag_extract_entities`, `_rag_is_noise_token`, `_rag_safe_name`, `_rag_tokenize`; `rag/store.py`: `CodeLibraryStore`, `RAGLibraryStore`, `WikiStore`; `session/state.py`: `SessionState`; `utils/files.py`: `try_read_text`; `utils/json_utils.py`: `_read_json_file`, `_write_json_file`, `parse_json_object`; `utils/media.py`: `guess_mime_from_name`; `utils/misc.py`: `make_id`, `now_ts`; `utils/text.py`: `trim`
- Symbols:
  - `_rag_trigram_set` (function, lines 57076-57081)
  - `_rag_jaccard_sim` (function, lines 57084-57091)
  - `_rag_mmr_select` (function, lines 57094-57141)
  - `_rag_embed_text` (function, lines 57278-57299)
  - `_rag_embed_batch` (function, lines 57302-57308)
  - `_rag_window_for_query` (function, lines 57311-57323)
  - `_rag_focused_excerpt` (function, lines 57326-57366)
  - `_rag_query_variants` (function, lines 57369-57406)
  - `_rag_parse_segments` (function, lines 57409-57469)
  - `_rag_parse_file_worker` (function, lines 61832-61846)
  - `RAGIngestionService` (class, lines 61849-62725)
  - `CodeIngestionService` (class, lines 63462-63547)

### `rag/parsers.py`

- Routed symbols: 28
- Cross-module imports: `config/constants.py`: `AUDIO_EXTS`, `CODE_CHUNK_CHARS`, `CODE_CHUNK_OVERLAP`, `CODE_LIBRARY_LANGUAGE_BY_EXT`, `CODE_LIBRARY_SPECIAL_FILENAMES`, `CODE_MAX_CHUNKS_PER_DOC`, `CODE_PREVIEW_DIFF_CONTEXT_LINES`, `CODE_PREVIEW_DIFF_MERGE_GAP`, `CODE_PREVIEW_EXTS`, `CODE_PREVIEW_FILENAMES`, `CODE_PREVIEW_STAGE_MAX_ROWS`, `DOCUMENT_PREVIEW_EXTS`, `EXCEL_PREVIEW_EXTS`, `IMAGE_EXTS`, `PRESENTATION_PREVIEW_EXTS`, `RAG_CHUNK_CHARS`, `RAG_CHUNK_OVERLAP`, `RAG_CODE_HINTS`, `RAG_EN_STOPWORDS`, `RAG_GENERIC_ENTITY_TERMS_EN`, `RAG_GENERIC_ENTITY_TERMS_ZH`, `RAG_INCLUDE_FILENAME_ENTITIES_DEFAULT`, `RAG_MAX_CHUNKS_PER_DOC`, `RAG_PDF_IMAGE_LIMIT`, `RAG_RESEARCH_HINTS`, `RAG_SHORT_TOKEN_ALLOWLIST`, `RAG_STRUCTURAL_ENTITY_PATTERNS`, `RAG_TERM_GROUPS`, `RAG_ZH_STOPWORDS`, `TABULAR_PREVIEW_EXTS`, `VIDEO_EXTS`; `rag/ingestion.py`: `_rag_parse_segments`; `utils/files.py`: `_sha256_bytes`, `_sha256_file`; `utils/json_utils.py`: `parse_json_object`; `utils/media.py`: `guess_mime_from_name`; `utils/text.py`: `_focused_diff_rows_from_opcodes`, `_skip_row`, `trim`
- Symbols:
  - `normalize_rel_preview_path` (function, lines 5811-5822)
  - `is_code_preview_candidate` (function, lines 5825-5833)
  - `preview_kind_for_path` (function, lines 5842-5871)
  - `build_code_preview_rows` (function, lines 5874-5920)
  - `_rag_safe_name` (function, lines 56875-56878)
  - `_rag_detect_language` (function, lines 56881-56895)
  - `_rag_cjk_ngrams` (function, lines 56898-56910)
  - `_rag_is_noise_token` (function, lines 56913-56932)
  - `_rag_entity_allowed` (function, lines 56935-56947)
  - `_rag_filter_entities` (function, lines 56950-56964)
  - `_rag_filename_entity_aliases` (function, lines 56967-57000)
  - `_rag_apply_filename_entity_policy` (function, lines 57003-57033)
  - `_rag_choose_community` (function, lines 57036-57073)
  - `_rag_tokenize` (function, lines 57144-57195)
  - `_rag_expand_tokens` (function, lines 57198-57219)
  - `_rag_extract_entities` (function, lines 57222-57238)
  - `_rag_classify_document` (function, lines 57241-57275)
  - `_rag_chunk_text` (function, lines 57472-57551)
  - `_code_language_from_name` (function, lines 57628-57644)
  - `_code_is_test_path` (function, lines 57647-57649)
  - `_CallCollector` (class, lines 57694-57706)
  - `_ALGO_COMPLEXITY_RE` (assignment, lines 57709-57709)
  - `_ALGO_STEP_RE` (assignment, lines 57710-57710)
  - `_ALGO_MATH_VARS` (assignment, lines 57711-57711)
  - `_ALGO_DOC_KEYWORDS` (assignment, lines 57712-57712)
  - `_detect_algo_chunk` (function, lines 57715-57738)
  - `CodeContentParser` (class, lines 57741-58231)
  - `RAGContentParser` (class, lines 58234-58741)

### `rag/store.py`

- Routed symbols: 4
- Cross-module imports: `config/constants.py`: `CODE_CHUNK_CHARS`, `CODE_CHUNK_OVERLAP`, `CODE_MAX_CHUNKS_PER_DOC`, `RAG_INCLUDE_FILENAME_ENTITIES_DEFAULT`, `RAG_MAX_QUERY_RESULTS`, `RAG_RETRIEVAL_MAX_PER_DOC`, `RAG_TASK_HISTORY_LIMIT`, `RAG_WEAK_MATCH_SCORE_CAP`, `RAG_WORKFLOW_ACCEPT_SCORE`; `rag/index.py`: `CodeGraphIndex`, `TFGraphIDFIndex`, `_code_choose_community`, `_code_module_name`; `rag/ingestion.py`: `_rag_focused_excerpt`, `_rag_mmr_select`, `_rag_window_for_query`; `rag/parsers.py`: `_code_is_test_path`, `_rag_apply_filename_entity_policy`, `_rag_choose_community`, `_rag_chunk_text`, `_rag_entity_allowed`, `_rag_expand_tokens`, `_rag_extract_entities`, `_rag_filter_entities`, `_rag_safe_name`, `_rag_tokenize`; `skills/store.py`: `_write_text_if_changed`; `utils/files.py`: `_sha256_bytes`, `_sha256_file`, `try_read_text`; `utils/json_utils.py`: `_read_json_file`, `_write_json_file`, `json_dumps`; `utils/media.py`: `guess_mime_from_name`; `utils/misc.py`: `make_id`, `now_ts`; `utils/text.py`: `trim`
- Symbols:
  - `RAGLibraryStore` (class, lines 60322-60896)
  - `WikiStore` (class, lines 60899-61428)
  - `WorkflowMemoryStore` (class, lines 61431-61829)
  - `CodeLibraryStore` (class, lines 63196-63459)

### `server/handlers.py`

- Routed symbols: 5
- Cross-module imports: `app/context.py`: `AppContext`; `config/constants.py`: `APP_VERSION`, `DEFAULT_AUTO_TASK_LEVEL_CEILING`, `DEFAULT_READ_CONTEXT_POLICY`, `DEFAULT_REQUEST_TIMEOUT`, `DEFAULT_SHELL_COMMAND_TIMEOUT_SECONDS`, `DEFAULT_TOOL_MEMORY_POLICY`, `DEFAULT_UI_LANGUAGE`, `DEFAULT_UI_STYLE`, `EXECUTION_MODE_CHOICES`, `EXECUTION_MODE_SYNC`, `MIN_RUN_TIMEOUT_SECONDS`, `PLAN_MODE_USER_CHOICES`, `RAG_GRAPH_MAX_NODES`, `SESSION_LIST_DEFAULT_LIMIT`, `SSE_HEARTBEAT_SECONDS`, `TASK_COMPLEXITY_LEVELS`, `TASK_LEVEL_CHOICES`, `TASK_LEVEL_POLICIES`, `UI_STYLE_LABELS`; `config/paths.py`: `LLM_CONFIG_PATH`, `REPO_ROOT`, `WORKDIR`; `config/settings.py`: `_to_bool_like`, `infer_user_complexity_value`, `looks_like_llm_config`, `normalize_auto_task_level_ceiling`, `normalize_execution_mode`, `normalize_read_context_policy`, `normalize_task_complexity`, `normalize_tool_memory_policy`, `normalize_ui_language`, `normalize_ui_style`, `resolve_web_ui_dir_path`, `supported_ui_languages_payload`; `llm/utils.py`: `extract_base_url`, `extract_openai_compat_model_ids`, `list_ollama_models`, `normalize_openai_compat_provider_name`, `openai_compat_model_list_urls`, `openai_compat_probe_headers`; `rag/parsers.py`: `normalize_rel_preview_path`; `session/manager.py`: `SessionCreationLimitExceeded`, `SessionManager`; `session/state.py`: `SessionState`; `skills/store.py`: `analyze_skill_building_knowledge`; `utils/files.py`: `safe_path`, `try_read_text`; `utils/http.py`: `urlopen`; `utils/json_utils.py`: `json_dumps`, `parse_json_object`; `utils/media.py`: `guess_mime_from_name`; `utils/misc.py`: `now_ts`, `swallow_benign_socket_error`, `user_id_from_ip`; `utils/text.py`: `trim`
- Symbols:
  - `AgentHTTPServer` (class, lines 69075-69103)
  - `Handler` (class, lines 69107-70026)
  - `SkillsHandler` (class, lines 70028-70233)
  - `RagAdminHandler` (class, lines 70235-70403)
  - `CodeAdminHandler` (class, lines 70406-70592)

### `session/manager.py`

- Routed symbols: 2
- Cross-module imports: `config/constants.py`: `AGENT_MAX_OUTPUT_TOKENS`, `ARBITER_DEFAULT_MAX_TOKENS`, `ARBITER_DEFAULT_TEMPERATURE`, `ARBITER_DEFAULT_TIMEOUT_SECONDS`, `DEFAULT_AUTO_TASK_LEVEL_CEILING`, `DEFAULT_CONTEXT_TOKEN_LIMIT`, `DEFAULT_READ_CONTEXT_POLICY`, `DEFAULT_REQUEST_TIMEOUT`, `DEFAULT_SHELL_COMMAND_TIMEOUT_SECONDS`, `DEFAULT_TOOL_MEMORY_POLICY`, `DEFAULT_UI_LANGUAGE`, `EXECUTION_MODE_SYNC`, `MAX_AGENT_ROUNDS`, `MAX_AGENT_ROUNDS_CAP`, `MAX_RUN_SECONDS`, `MAX_RUN_TIMEOUT_SECONDS`, `MAX_SHELL_COMMAND_TIMEOUT_SECONDS`, `MIN_AGENT_ROUNDS`, `MIN_CONTEXT_TOKEN_LIMIT`, `MIN_RUN_TIMEOUT_SECONDS`, `MIN_SHELL_COMMAND_TIMEOUT_SECONDS`, `SESSION_LIST_DEFAULT_LIMIT`, `TOKEN_THRESHOLD`; `config/paths.py`: `LLM_CONFIG_PATH`; `config/settings.py`: `extract_auto_task_level_ceiling_setting`, `extract_read_context_policy_setting`, `extract_tool_memory_policy_setting`, `infer_model_multimodal_capabilities`, `merge_multimodal_capabilities`, `normalize_auto_task_level_ceiling`, `normalize_execution_mode`, `normalize_read_context_policy`, `normalize_tool_memory_policy`, `normalize_ui_language`, `parse_capability_overrides`, `parse_llm_config_profiles`; `llm/client.py`: `OllamaClient`; `llm/utils.py`: `complete_chat_endpoint`, `extract_base_url`, `is_openai_compat_provider`, `list_ollama_models_cached`, `probe_ollama_environment`; `session/state.py`: `SessionState`; `utils/crypto.py`: `CryptoBox`; `utils/files.py`: `try_read_text`; `utils/json_utils.py`: `parse_json_object`; `utils/misc.py`: `make_id`, `normalize_timeout_seconds`, `now_ts`, `sanitize_profile_id`
- Symbols:
  - `SessionCreationLimitExceeded` (class, lines 2576-2579)
  - `SessionManager` (class, lines 46254-47388)

### `session/state.py`

- Routed symbols: 1
- Cross-module imports: `agent/background.py`: `BackgroundManager`; `agent/bus.py`: `MessageBus`; `agent/events.py`: `EventHub`; `agent/tasks.py`: `TaskManager`; `agent/todo.py`: `TodoManager`; `agent/worktree.py`: `WorktreeManager`; `config/constants.py`: `AGENT_BUBBLE_ROLES`, `AGENT_CTX_LIMIT_TIER0`, `AGENT_CTX_LIMIT_TIER1`, `AGENT_CTX_LIMIT_TIER2`, `AGENT_CTX_LIMIT_TIER3`, `AGENT_MAX_OUTPUT_TOKENS`, `AGENT_MSG_LIMIT_TIER0`, `AGENT_MSG_LIMIT_TIER1`, `AGENT_MSG_LIMIT_TIER2`, `AGENT_MSG_LIMIT_TIER3`, `AGENT_ROLES`, `AGENT_TOOL_ALLOWLIST`, `ARBITER_DEFAULT_MAX_TOKENS`, `ARBITER_DEFAULT_TEMPERATURE`, `ARBITER_DEFAULT_TIMEOUT_SECONDS`, `ARBITER_TRIGGER_MIN_CONTENT_CHARS`, `ARBITER_VALID_PLANNING_STREAK_LIMIT`, `ASSISTANT_MESSAGE_EVENT_MAX_CHARS`, `ASSISTANT_TEXT_PERSIST_MAX_CHARS`, `AUDIO_EXTS`, `AUTO_CONTINUE_BUDGET_DEFAULT`, `BASH_READ_LOOP_THRESHOLD`, `BLACKBOARD_MAX_LOG_ENTRIES`, `BLACKBOARD_MAX_TEXT`, `BLACKBOARD_MEMORY_INDEX_MAX`, `BLACKBOARD_MEMORY_LONG_MAX`, `BLACKBOARD_MEMORY_MID_ITEMS_PER_STEP`, `BLACKBOARD_MEMORY_MID_MAX_STEPS`, `BLACKBOARD_MEMORY_SHORT_MAX`, `BLACKBOARD_STATUSES`, `CHAT_UPLOAD_AUTO_LIBRARY_INGEST`, `CHAT_UPLOAD_INGEST_QUEUE_MAX`, `CHAT_UPLOAD_INLINE_TEXT_BYTES`, `CHAT_UPLOAD_PARSE_MAX_BYTES`, `CHAT_UPLOAD_PARSE_QUEUE_MAX`, `CHAT_UPLOAD_PARSE_TIMEOUT_SECONDS`, `CHAT_UPLOAD_PROMPT_MAX_CHARS`, `CHAT_UPLOAD_PROMPT_MAX_FILES`, `CHAT_UPLOAD_PROMPT_PER_FILE_CHARS`, `CHAT_UPLOAD_TEXT_CONTEXT_CHARS`, `CHAT_UPLOAD_ZIP_ENTRY_MAX_BYTES`, `CHECKPOINT_INTERVAL_ROUNDS`, `CHECKPOINT_MAX_COUNT`, `CODE_PREVIEW_STAGE_MAX_BYTES`, `CODE_PREVIEW_STAGE_MAX_PER_FILE`, `CODE_PREVIEW_STAGE_MAX_ROWS`, `CODE_PREVIEW_STAGE_MAX_TOTAL`, `COMPACT_TIER1_ABS`, `COMPACT_TIER1_PCT`, `COMPACT_TIER2_ABS`, `COMPACT_TIER2_PCT`, `COMPACT_TIER3_PCT`, `CONTEXT_ACTUAL_USAGE_RECENT_SECONDS`, `CONTEXT_AUTO_COMPACT_RESERVE_RATIO`, `CONTEXT_COMPACT_INEFFECTIVE_COOLDOWN_SECONDS`, `CONTEXT_ESTIMATE_SAFETY_MULTIPLIER`, `CONTEXT_USAGE_CALIBRATION_MAX`, `DANGEROUS_PATTERNS`, `DEEP_RESEARCH_REQUEST_KEYWORDS`, `DEEP_RESEARCH_RETRIEVAL_KEYWORDS`, `DEEP_RESEARCH_TEXT_ONLY_HINT_KEYWORDS`, `DEFAULT_AUTO_TASK_LEVEL_CEILING`, `DEFAULT_CONTEXT_TOKEN_LIMIT`, `DEFAULT_READ_CONTEXT_POLICY`, `DEFAULT_REQUEST_TIMEOUT`, `DEFAULT_SHELL_COMMAND_TIMEOUT_SECONDS`, `DEFAULT_TOOL_MEMORY_POLICY`, `DEFAULT_UI_LANGUAGE`, `DEVELOPER_EDIT_STALL_THRESHOLD`, `EMPTY_ACTION_MIN_CONTENT_CHARS`, `EMPTY_ACTION_WAKEUP_RETRY_LIMIT`, `ERROR_CATEGORY_DEFS`, `EXECUTION_MODE_CHOICES`, `EXECUTION_MODE_SEQUENTIAL`, `EXECUTION_MODE_SINGLE`, `EXECUTION_MODE_SYNC`, `EXPLORER_STALL_THRESHOLD`, `FAILURE_LEDGER_MAX_COMPILE_ERRORS`, `FAILURE_LEDGER_MAX_DELEGATIONS`, `FAILURE_LEDGER_MAX_ERRORS`, `FAILURE_LEDGER_MAX_FIXES`, `FAILURE_LEDGER_MAX_STALLS`, `FAILURE_LEDGER_MAX_TOOL_FPS`, `FILE_BUFFER_CONTENT_THRESHOLD`, `FILE_BUFFER_MAX_FILES`, `FINAL_SUMMARY_MIN_CHARS`, `FINAL_SUMMARY_STRICT_MIN_CHARS`, `FUSED_FAULT_BREAK_THRESHOLD`, `HARD_BREAK_RECOVERY_ROUND_THRESHOLD`, `HARD_BREAK_TOOL_ERROR_THRESHOLD`, `HTML_FRONTEND_REQUEST_KEYWORDS`, `IMAGE_EXTS`, `IMAGE_FORMATS_NEED_CONVERSION`, `LARGE_FILE_AUTO_PAGE_BYTES`, `LARGE_FILE_AUTO_PAGE_LINES`, `LARGE_SOURCE_UPLOAD_EXCERPT_CHARS`, `LIVE_INPUT_DELAY_NORMAL_ROUNDS`, `LIVE_INPUT_DELAY_TOOL_ROUNDS`, `LIVE_INPUT_DELAY_WRITE_ROUNDS`, `LIVE_INPUT_MAX_INJECTIONS`, `LIVE_INPUT_REINJECT_INTERVAL`, `LIVE_INPUT_WEIGHT_BASE_DELAYED`, `LIVE_INPUT_WEIGHT_BASE_NORMAL`, `LIVE_INPUT_WEIGHT_STEP_DELAYED`, `LIVE_INPUT_WEIGHT_STEP_NORMAL`, `LONG_OUTPUT_LISTING_OFFLOAD_CHARS`, `LONG_OUTPUT_MODEL_PAGE_CHARS`, `LONG_OUTPUT_READ_PAGE_LINES`, `LONG_OUTPUT_TEMP_MAX_FILES`, `LONG_OUTPUT_UI_PAGE_CHARS`, `LONG_OUTPUT_UI_PREVIEW_MAX_PAGES`, `MANAGER_CTX_LIMIT_TIER0`, `MANAGER_CTX_LIMIT_TIER1`, `MANAGER_CTX_LIMIT_TIER2`, `MANAGER_CTX_LIMIT_TIER3`, `MANAGER_ROUTE_TARGETS`, `MAX_AGENT_ROUNDS`, `MAX_AGENT_ROUNDS_CAP`, `MAX_CONTEXT_ARCHIVE_SEGMENTS`, `MAX_RUN_SECONDS`, `MAX_RUN_TIMEOUT_SECONDS`, `MAX_SHELL_COMMAND_TIMEOUT_SECONDS`, `MIN_AGENT_ROUNDS`, `MIN_CONTEXT_TOKEN_LIMIT`, `MIN_RUN_TIMEOUT_SECONDS`, `MIN_SHELL_COMMAND_TIMEOUT_SECONDS`, `MODEL_CALL_PROGRESS_DELAY`, `MODEL_CALL_PROGRESS_INTERVAL`, `MODEL_OUTPUT_RETRY_TIMES`, `PERSISTED_ROUTES_MAX`, `PLAN_BUBBLE_MAX_CHARS`, `PLAN_FILE_RELATIVE_PATH`, `PLAN_MESSAGE_EVENT_MAX_CHARS`, `PLAN_MODE_ENABLED_LEVELS`, `PLAN_MODE_EXPLORER_MAX_ROUNDS`, `PLAN_MODE_FORCED_LEVELS`, `PLAN_MODE_MANAGER_SYNTHESIS_MAX_TOKENS`, `PLAN_MODE_MAX_OPTIONS`, `PLAN_MODE_RESEARCH_TOOL_ALLOWLIST`, `PLAN_MODE_SYNTHESIS_MAX_ATTEMPTS`, `PLAN_MODE_USER_CHOICES`, `PLAN_NOTICE_BODY_MAX_CHARS`, `PLAN_STEP_FULL_CONTENT_MAX_CHARS`, `PREVIEW_DOWNLOAD_MAX_BYTES`, `PREVIEW_DOWNLOAD_MAX_FILES`, `READ_CONTEXT_PROMPT_MAX_CHARS`, `READ_CONTEXT_PROMPT_MAX_ITEMS`, `READ_CONTEXT_REGISTRY_MAX`, `READ_CONTEXT_SHARED_MAX_ITEMS`, `READ_CONTEXT_SUMMARY_MAX_CHARS`, `READ_FILE_COMPACT_PIN_DISTINCT`, `READ_FILE_COMPACT_PIN_MAX_CHARS`, `READ_FILE_DEFAULT_MAX_CHARS`, `READ_FILE_HARD_MAX_CHARS`, `READ_FILE_LOOP_DISTINCT_SOFT_LIMIT`, `READ_FILE_LOOP_THRESHOLD`, `READ_FILE_OVERVIEW_HEAD_LINES`, `READ_FILE_SEARCH_MAX_MATCHES`, `RENDER_FRAME_ACTIVITY_INTERVAL_SECONDS`, `RENDER_FRAME_MAX_B64_CHARS`, `RENDER_FRAME_MAX_LINES`, `RENDER_FRAME_MAX_LINE_POINTS`, `RENDER_FRAME_MAX_POINTS`, `REPEATED_TOOL_LOOP_THRESHOLD`, `RETRY_RUNTIME_HINT_PREFIXES`, `REVIEWER_DEBUG_MODE_MAX_ROUNDS`, `RUNTIME_CONTROL_HINT_PREFIXES`, `RUN_COMPLETION_SUMMARY_ENABLED`, `SEMANTIC_CONFIDENCE_CHOICES`, `SESSION_DEFERRED_START_QUEUE_MAX`, `SESSION_HEARTBEAT_STALE_SECONDS`, `SESSION_SUBMIT_LOCK_TIMEOUT_SECONDS`, `SKILLS_VIRTUAL_PREFIX`, `SKILL_REFRESH_MIN_INTERVAL_SECONDS`, `SKILL_RUNTIME_CACHE_MAX_BYTES`, `SKILL_RUNTIME_CACHE_MAX_ENTRIES`, `STALL_ESCALATION_CONTEXT_MAX_CHARS`, `STALL_ESCALATION_MIN_LEVEL`, `STALL_PLAN_SYNTHESIS_MAX_TOKENS`, `STALL_SEVERITY_DECAY_ON_SUCCESS`, `STALL_SEVERITY_ESCALATION_THRESHOLD`, `STALL_SEVERITY_WEIGHT_BASH_READ_LOOP`, `STALL_SEVERITY_WEIGHT_FAULT`, `STALL_SEVERITY_WEIGHT_RECOVERY_RETRY`, `STALL_SEVERITY_WEIGHT_REPEATED_TOOL`, `STALL_SEVERITY_WEIGHT_WATCHDOG`, `TASK_COMPLEXITY_LEVELS`, `TASK_LEVEL_CHOICES`, `TASK_LEVEL_POLICIES`, `TASK_PHASE_ROUTING`, `TASK_PROFILE_TYPES`, `TASK_SCALE_PREFERENCES`, `THINKING_BUDGET_FORCE_RATIO`, `TOKEN_THRESHOLD`, `TOOL_MEMORY_COMPACT_PIN_DISTINCT`, `TOOL_MEMORY_COMPACT_PIN_MAX_CHARS`, `TOOL_MEMORY_PROMPT_MAX_CHARS`, `TOOL_MEMORY_PROMPT_MAX_ITEMS`, `TOOL_MEMORY_REGISTRY_MAX`, `TOOL_MEMORY_SHARED_MAX_ITEMS`, `TOOL_MEMORY_SUMMARY_MAX_CHARS`, `TRUNCATION_CONTINUATION_ECHO_CHARS`, `TRUNCATION_CONTINUATION_MAX_PASSES`, `TRUNCATION_CONTINUATION_MAX_TOKENS`, `TRUNCATION_CONTINUATION_TAIL_CHARS`, `TRUNCATION_LIVE_BUFFER_MAX_CHARS`, `TRUNCATION_OVERLAP_SCAN_CHARS`, `TRUNCATION_PAIR_SCAN_CHARS`, `VIDEO_EXTS`, `WATCHDOG_CONTEXT_NEAR_RATIO`, `WATCHDOG_CONTEXT_STALL_THRESHOLD`, `WATCHDOG_INTENT_NO_TOOL_THRESHOLD`, `WATCHDOG_INTENT_NO_TOOL_THRESHOLD_SINGLE`, `WATCHDOG_MAX_DECOMPOSE_STEPS`, `WATCHDOG_REPEAT_NO_TOOL_THRESHOLD`, `WATCHDOG_REPEAT_NO_TOOL_THRESHOLD_SINGLE`, `WATCHDOG_REPEAT_SIMILARITY_THRESHOLD`, `WATCHDOG_STATE_STALL_THRESHOLD`, `WATCHDOG_STEP_MAX_ATTEMPTS`, `_DEFAULT_TOOL_TIMEOUT`, `_SHELL_AUTO_CONFIRM_PATTERNS`, `_TOOL_TIMEOUT_MAP`; `config/paths.py`: `WORKDIR`; `config/settings.py`: `_detect_os_shell_instruction`, `_to_bool_like`, `backend_i18n_text`, `backend_role_label`, `default_multimodal_capabilities`, `extract_auto_task_level_ceiling_setting`, `infer_model_multimodal_capabilities`, `infer_user_complexity_value`, `looks_like_llm_config`, `max_task_complexity`, `merge_multimodal_capabilities`, `model_language_instruction`, `normalize_auto_task_level_ceiling`, `normalize_execution_mode`, `normalize_read_context_policy`, `normalize_task_complexity`, `normalize_tool_memory_policy`, `normalize_ui_language`, `parse_capability_overrides`, `parse_llm_config_profiles`, `task_complexity_at_least`, `task_complexity_rank`; `llm/client.py`: `OllamaClient`, `OllamaError`; `llm/utils.py`: `complete_chat_endpoint`, `extract_base_url`, `is_openai_compat_provider`, `list_loaded_ollama_models`, `list_ollama_models`, `list_ollama_models_cached`, `probe_ollama_environment`, `resolve_ollama_model`, `split_thinking_content`, `strip_thinking_content`, `wake_ollama_model`; `rag/parsers.py`: `CodeContentParser`, `build_code_preview_rows`, `is_code_preview_candidate`, `normalize_rel_preview_path`, `preview_kind_for_path`; `skills/store.py`: `SkillStore`, `ensure_runtime_skills`; `utils/compress.py`: `compress_text_blob`, `decompress_text_blob`; `utils/crypto.py`: `CryptoBox`; `utils/errors.py`: `CircuitBreakerTriggered`, `EmptyActionError`; `utils/files.py`: `_normalize_external_js_url`, `_safe_js_filename`, `cache_external_js_url`, `ensure_offline_js_libs`, `is_external_js_src`, `load_offline_js_lib_index`, `match_offline_js_catalog_by_url`, `offline_js_lib_root`, `safe_path`, `try_read_text`; `utils/http.py`: `urlopen`; `utils/json_utils.py`: `TOOLS`, `TOOL_REQUIRED_ARGS`, `canonicalize_tool_name`, `extract_json_object_from_text`, `json_dumps`, `parse_json_object`, `parse_tool_arguments_with_error`, `repair_truncated_json_object`, `tool_def`; `utils/media.py`: `_convert_image_to_safe_format`, `guess_ext_from_mime`, `guess_mime_from_name`; `utils/misc.py`: `MAX_TIMEOUT_SECONDS`, `MIN_TIMEOUT_SECONDS`, `is_benign_socket_error`, `make_id`, `normalize_timeout_seconds`, `now_ts`, `sanitize_profile_id`; `utils/text.py`: `MAX_TOOL_OUTPUT`, `_fmt_export_ts`, `_html_esc`, `_text_to_minimal_pdf`, `extract_todo_rows_from_text`, `filter_runtime_noise_lines`, `make_numbered_diff`, `make_unified_diff`, `normalize_embedded_newlines`, `normalize_work_text`, `parse_front_matter`, `render_numbered_diff_text`, `split_structured_todo_content`, `split_todo_status_text`, `trim`
- Symbols:
  - `SessionState` (class, lines 14118-46252)

### `skills/store.py`

- Routed symbols: 26
- Cross-module imports: `config/constants.py`: `BUILTIN_CLAWHUB_SKILLS_VERSION`, `EMBEDDED_CLAWHUB_SKILLS_ARCHIVE_B64`, `EMBEDDED_SKILLS_ARCHIVE_B64`, `EMBEDDED_SKILLS_ARCHIVE_FILES`, `EMBEDDED_SKILLS_ARCHIVE_SHA256`, `SKILLS_EXTERNAL_MOUNT`, `SKILLS_VIRTUAL_PREFIX`, `SKILL_BODY_COMPACT_THRESHOLD_CHARS`, `SKILL_BODY_PREVIEW_CHARS`, `SKILL_DEFAULT_ATTACHMENT_GLOBS`, `SKILL_INLINE_ATTACHMENT_MAX_CHARS`, `SKILL_INLINE_ATTACHMENT_MAX_FILES`, `SKILL_PROMPT_MAX_CHARS`, `SKILL_PROMPT_MAX_ITEMS`, `SKILL_PROTOCOL_CLAWHUB`, `SKILL_PROTOCOL_HTTP_JSON`, `SKILL_PROTOCOL_LOCAL`, `SKILL_PROTOCOL_SPECS`, `SKILL_REFRESH_MIN_INTERVAL_SECONDS`, `SKILL_RESOURCE_MANIFEST_MAX_ITEMS`; `config/paths.py`: `WORKDIR`; `llm/utils.py`: `_is_http_url`; `utils/files.py`: `_render_offline_js_catalog_md`, `safe_path`, `try_read_text`; `utils/http.py`: `urlopen`; `utils/json_utils.py`: `json_dumps`, `parse_json_object`; `utils/misc.py`: `_meta_string_list`, `_module_exists`, `now_ts`; `utils/text.py`: `parse_front_matter`, `trim`
- Symbols:
  - `ensure_embedded_skills_at_root` (function, lines 6787-6839)
  - `ensure_embedded_skills` (function, lines 6842-6843)
  - `detect_upload_parser_capabilities` (function, lines 6851-6866)
  - `_render_cap_markdown` (function, lines 6868-6882)
  - `_write_text_if_changed` (function, lines 6884-6889)
  - `ensure_generated_document_skills` (function, lines 6891-6979)
  - `ensure_generated_image_coding_feedback_skill` (function, lines 6981-7080)
  - `_skill_knowledge_files` (function, lines 7082-7101)
  - `analyze_skill_building_knowledge` (function, lines 7103-7157)
  - `_sanitize_skill_slug` (function, lines 7159-7161)
  - `_build_skills_gen_skill_content` (function, lines 7163-7194)
  - `ensure_generated_skills_gen_skill` (function, lines 7196-7200)
  - `ensure_generated_execution_recovery_skill` (function, lines 7202-7280)
  - `ensure_generated_systematic_debugging_skill` (function, lines 7282-7554)
  - `ensure_generated_code_engineering_mastery_skill` (function, lines 7556-7674)
  - `ensure_generated_smart_file_navigation_skill` (function, lines 7676-7791)
  - `ensure_generated_html_frontend_report_skills` (function, lines 7793-8000)
  - `ensure_generated_deep_research_skills` (function, lines 8002-8270)
  - `ensure_generated_research_scientific_skills` (function, lines 8272-8908)
  - `ensure_generated_rag_mastery_skills` (function, lines 8914-9210)
  - `ensure_generated_multimodal_comprehension_skills` (function, lines 9216-9905)
  - `ensure_generated_runtime_skills_manifest` (function, lines 9908-9939)
  - `ensure_embedded_clawhub_skills` (function, lines 10197-10234)
  - `ensure_runtime_skills` (function, lines 10236-10251)
  - `_BUILTIN_SKILLS` (assignment, lines 10293-10381)
  - `SkillStore` (class, lines 10390-11684)

### `utils/compress.py`

- Routed symbols: 2
- Cross-module imports: none
- Symbols:
  - `compress_text_blob` (function, lines 3531-3536)
  - `decompress_text_blob` (function, lines 3538-3546)

### `utils/crypto.py`

- Routed symbols: 1
- Cross-module imports: `utils/json_utils.py`: `json_dumps`
- Symbols:
  - `CryptoBox` (class, lines 5135-5252)

### `utils/errors.py`

- Routed symbols: 2
- Cross-module imports: none
- Symbols:
  - `EmptyActionError` (class, lines 3920-3921)
  - `CircuitBreakerTriggered` (class, lines 3924-3925)

### `utils/files.py`

- Routed symbols: 25
- Cross-module imports: `config/constants.py`: `OFFLINE_JS_LIB_CATALOG`, `OFFLINE_JS_LIB_INDEX_FILE`, `OFFLINE_JS_LIB_README_FILE`; `config/paths.py`: `WORKDIR`; `utils/http.py`: `urlopen`; `utils/json_utils.py`: `json_dumps`; `utils/misc.py`: `now_ts`; `utils/text.py`: `trim`
- Symbols:
  - `_normalize_js_lib_asset_ref` (function, lines 1474-1487)
  - `_resolve_js_lib_asset_path` (function, lines 1490-1519)
  - `_discover_extra_js_lib_files` (function, lines 1522-1552)
  - `safe_path` (function, lines 2908-2917)
  - `_safe_js_filename` (function, lines 2919-2926)
  - `_sha256_bytes` (function, lines 2928-2929)
  - `_sha256_file` (function, lines 2931-2939)
  - `_download_http_bytes` (function, lines 2941-2949)
  - `offline_js_lib_root` (function, lines 2951-2952)
  - `_offline_js_entry_relative_path` (function, lines 2954-2958)
  - `_archive_member_relative_path` (function, lines 2960-2969)
  - `_path_size_bytes` (function, lines 2971-2986)
  - `_extract_archive_to_dir` (function, lines 2988-3028)
  - `_package_required_paths` (function, lines 3030-3036)
  - `_package_install_ready` (function, lines 3038-3046)
  - `_postprocess_offline_js_package` (function, lines 3048-3083)
  - `_ensure_offline_js_package` (function, lines 3085-3124)
  - `_render_offline_js_catalog_md` (function, lines 3126-3142)
  - `load_offline_js_lib_index` (function, lines 3144-3153)
  - `ensure_offline_js_libs` (function, lines 3155-3299)
  - `_normalize_external_js_url` (function, lines 3301-3305)
  - `is_external_js_src` (function, lines 3307-3309)
  - `match_offline_js_catalog_by_url` (function, lines 3311-3327)
  - `cache_external_js_url` (function, lines 3329-3361)
  - `try_read_text` (function, lines 5457-5465)

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
  - `json_dumps` (function, lines 2880-2881)
  - `parse_tool_arguments` (function, lines 3799-3808)
  - `repair_truncated_json_object` (function, lines 3810-3863)
  - `parse_tool_arguments_with_error` (function, lines 3865-3895)
  - `parse_json_object` (function, lines 4161-4166)
  - `extract_json_object_from_text` (function, lines 4168-4190)
  - `_json_default_copy` (function, lines 5467-5472)
  - `_read_json_file` (function, lines 5474-5494)
  - `_write_json_file` (function, lines 5496-5523)
  - `tool_def` (function, lines 13677-13689)
  - `TOOLS` (constant, lines 13691-14016)
  - `TOOL_REQUIRED_ARGS` (constant, lines 14018-14018)
  - `TOOL_SPEC_BY_NAME` (constant, lines 14019-14019)
  - `TOOL_NAME_FUZZY_MAP` (constant, lines 14031-14031)
  - `canonicalize_tool_name` (function, lines 14049-14060)

### `utils/media.py`

- Routed symbols: 3
- Cross-module imports: none
- Symbols:
  - `guess_mime_from_name` (function, lines 2720-2722)
  - `_convert_image_to_safe_format` (function, lines 2725-2742)
  - `guess_ext_from_mime` (function, lines 2745-2751)

### `utils/misc.py`

- Routed symbols: 19
- Cross-module imports: none
- Symbols:
  - `MIN_TIMEOUT_SECONDS` (constant, lines 383-383)
  - `MAX_TIMEOUT_SECONDS` (constant, lines 384-384)
  - `DEFAULT_TIMEOUT_SECONDS` (constant, lines 385-391)
  - `BENIGN_SOCKET_DEBUG_LOG_ENABLED` (constant, lines 521-527)
  - `BENIGN_SOCKET_LOG_INTERVAL_SECONDS` (constant, lines 528-528)
  - `now_ts` (function, lines 2753-2754)
  - `_benign_socket_log_lock` (assignment, lines 2757-2757)
  - `_benign_socket_log_state` (assignment, lines 2758-2758)
  - `is_benign_socket_error` (function, lines 2776-2794)
  - `_socket_error_code` (function, lines 2797-2806)
  - `_log_benign_socket_error_limited` (function, lines 2809-2843)
  - `swallow_benign_socket_error` (function, lines 2846-2850)
  - `normalize_timeout_seconds` (function, lines 2853-2866)
  - `detect_local_lan_ip` (function, lines 2868-2878)
  - `make_id` (function, lines 2883-2884)
  - `sanitize_profile_id` (function, lines 2886-2888)
  - `user_id_from_ip` (function, lines 5127-5133)
  - `_meta_string_list` (function, lines 5444-5455)
  - `_module_exists` (function, lines 6845-6849)

### `utils/text.py`

- Routed symbols: 23
- Cross-module imports: `config/constants.py`: `CODE_PREVIEW_DIFF_CONTEXT_LINES`, `CODE_PREVIEW_DIFF_MERGE_GAP`
- Symbols:
  - `MAX_TOOL_OUTPUT` (constant, lines 137-137)
  - `SOCKET_NOISE_LINE_PATTERNS` (constant, lines 515-520)
  - `filter_runtime_noise_lines` (function, lines 2761-2773)
  - `trim` (function, lines 3363-3365)
  - `_fmt_export_ts` (function, lines 3368-3376)
  - `_html_esc` (function, lines 3379-3380)
  - `_text_to_minimal_pdf` (function, lines 3383-3529)
  - `normalize_embedded_newlines` (function, lines 3548-3556)
  - `_map_todo_status_token` (function, lines 3559-3574)
  - `split_todo_status_text` (function, lines 3577-3632)
  - `extract_todo_rows_from_text` (function, lines 3635-3702)
  - `infer_todo_status_from_text` (function, lines 3705-3711)
  - `split_structured_todo_content` (function, lines 3714-3767)
  - `normalize_work_text` (function, lines 3770-3797)
  - `parse_front_matter` (function, lines 5254-5441)
  - `make_unified_diff` (function, lines 5525-5542)
  - `_skip_row` (function, lines 5544-5548)
  - `_row_is_hot` (function, lines 5551-5552)
  - `_hotspot_index` (function, lines 5555-5576)
  - `_compress_rows_keep_hotspot` (function, lines 5579-5626)
  - `_focused_diff_rows_from_opcodes` (function, lines 5629-5761)
  - `make_numbered_diff` (function, lines 5764-5794)
  - `render_numbered_diff_text` (function, lines 5796-5808)
