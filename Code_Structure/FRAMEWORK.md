# Code_Structure Framework

## Overview

- Source file: `/Users/Fona/Downloads/Clouds_Coder/Clouds_Coder.py`
- Output directory: `/Users/Fona/Downloads/Clouds_Coder/Code_Structure`
- Generated modules: 30
- Top-level symbols: 619
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
| `config/constants.py` | 359 | `utils/json_utils.py`, `utils/misc.py` |
| `config/paths.py` | 8 | `utils/text.py` |
| `config/settings.py` | 38 | `config/constants.py`, `config/paths.py`, `llm/utils.py`, `skills/store.py`, `utils/http.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` |
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
- Cross-module imports: `app/context.py`: `AppContext`; `config/constants.py`: `AGENT_MAX_OUTPUT_TOKENS`, `ARBITER_DEFAULT_MAX_TOKENS`, `ARBITER_DEFAULT_TEMPERATURE`, `ARBITER_DEFAULT_TIMEOUT_SECONDS`, `CODE_ADMIN_PORT_OFFSET`, `DEFAULT_AUTO_TASK_LEVEL_CEILING`, `DEFAULT_CONTEXT_TOKEN_LIMIT`, `DEFAULT_OLLAMA_BASE_URL`, `DEFAULT_OLLAMA_MODEL`, `DEFAULT_READ_CONTEXT_POLICY`, `DEFAULT_SHELL_COMMAND_TIMEOUT_SECONDS`, `DEFAULT_UI_LANGUAGE`, `DEFAULT_UI_STYLE`, `DEFAULT_WEB_UI_CONFIG`, `DEFAULT_WEB_UI_DIR`, `EXECUTION_MODE_SYNC`, `LIVE_INPUT_DELAY_NORMAL_ROUNDS`, `LIVE_INPUT_DELAY_TOOL_ROUNDS`, `LIVE_INPUT_DELAY_WRITE_ROUNDS`, `LIVE_INPUT_MAX_INJECTIONS`, `LIVE_INPUT_REINJECT_INTERVAL`, `LIVE_INPUT_WEIGHT_BASE_DELAYED`, `LIVE_INPUT_WEIGHT_BASE_NORMAL`, `LIVE_INPUT_WEIGHT_STEP_DELAYED`, `LIVE_INPUT_WEIGHT_STEP_NORMAL`, `MAX_AGENT_ROUNDS`, `MAX_AGENT_ROUNDS_CAP`, `MAX_RUN_SECONDS`, `MAX_RUN_TIMEOUT_SECONDS`, `MAX_SHELL_COMMAND_TIMEOUT_SECONDS`, `MIN_AGENT_ROUNDS`, `MIN_CONTEXT_TOKEN_LIMIT`, `MIN_RUN_TIMEOUT_SECONDS`, `MIN_SHELL_COMMAND_TIMEOUT_SECONDS`, `OFFLINE_JS_LIB_CATALOG`, `RAG_ADMIN_PORT_OFFSET`, `RAG_INCLUDE_FILENAME_ENTITIES_DEFAULT`, `TOKEN_THRESHOLD`, `UI_LANGUAGE_LABELS`, `UI_STYLE_LABELS`; `config/paths.py`: `LLM_CONFIG_PATH`, `REPO_ROOT`, `WORKDIR`; `config/settings.py`: `_to_bool_like`, `extract_auto_task_level_ceiling_setting`, `extract_context_token_limit_setting`, `extract_daily_session_limit_setting`, `extract_js_lib_download_setting`, `extract_read_context_policy_setting`, `extract_shell_command_timeout_setting`, `extract_show_upload_list_setting`, `extract_ui_style_setting`, `load_llm_config_from_source`, `load_web_ui_config_file`, `normalize_auto_task_level_ceiling`, `normalize_execution_mode`, `normalize_read_context_policy`, `normalize_ui_language`, `normalize_ui_style`, `parse_llm_config_profiles`, `resolve_optional_file_path`, `resolve_web_ui_dir_path`, `select_preferred_skills_root`; `llm/utils.py`: `list_ollama_models`; `server/handlers.py`: `AgentHTTPServer`, `CodeAdminHandler`, `Handler`, `RagAdminHandler`, `SkillsHandler`; `skills/store.py`: `ensure_embedded_skills_at_root`, `ensure_runtime_skills`; `utils/files.py`: `ensure_offline_js_libs`; `utils/misc.py`: `BENIGN_SOCKET_DEBUG_LOG_ENABLED`, `detect_local_lan_ip`, `normalize_timeout_seconds`, `now_ts`, `swallow_benign_socket_error`; `utils/text.py`: `trim`
- Symbols:
  - `main` (function, lines 67548-68620)
  - `_main_guard_68622` (main_guard, lines 68622-68623)

### `agent/background.py`

- Routed symbols: 1
- Cross-module imports: `utils/misc.py`: `make_id`, `now_ts`; `utils/text.py`: `trim`
- Symbols:
  - `BackgroundManager` (class, lines 11703-11783)

### `agent/bus.py`

- Routed symbols: 1
- Cross-module imports: `config/constants.py`: `VALID_MSG_TYPES`; `utils/crypto.py`: `CryptoBox`; `utils/misc.py`: `now_ts`
- Symbols:
  - `MessageBus` (class, lines 11785-11849)

### `agent/events.py`

- Routed symbols: 1
- Cross-module imports: none
- Symbols:
  - `EventHub` (class, lines 5804-5849)

### `agent/tasks.py`

- Routed symbols: 1
- Cross-module imports: `utils/crypto.py`: `CryptoBox`; `utils/json_utils.py`: `json_dumps`; `utils/misc.py`: `now_ts`
- Symbols:
  - `TaskManager` (class, lines 11575-11701)

### `agent/todo.py`

- Routed symbols: 1
- Cross-module imports: `config/constants.py`: `DEFAULT_UI_LANGUAGE`; `config/settings.py`: `backend_i18n_text`, `backend_role_label`, `normalize_ui_language`; `utils/text.py`: `infer_todo_status_from_text`, `normalize_work_text`, `split_structured_todo_content`, `trim`
- Symbols:
  - `TodoManager` (class, lines 5851-6120)

### `agent/worktree.py`

- Routed symbols: 1
- Cross-module imports: `agent/tasks.py`: `TaskManager`; `config/constants.py`: `DANGEROUS_PATTERNS`; `utils/crypto.py`: `CryptoBox`; `utils/json_utils.py`: `json_dumps`; `utils/misc.py`: `now_ts`; `utils/text.py`: `trim`
- Symbols:
  - `WorktreeManager` (class, lines 11851-12066)

### `app/context.py`

- Routed symbols: 1
- Cross-module imports: `config/constants.py`: `AGENT_MAX_OUTPUT_TOKENS`, `APP_CSS`, `APP_JS`, `APP_TS`, `ARBITER_DEFAULT_MAX_TOKENS`, `ARBITER_DEFAULT_TEMPERATURE`, `ARBITER_DEFAULT_TIMEOUT_SECONDS`, `CODE_ADMIN_CSS`, `CODE_ADMIN_INDEX_HTML`, `CODE_ADMIN_JS`, `CODE_IMPORT_WORKER_COUNT`, `CODE_LIBRARY_DIRNAME`, `CODE_PARSE_TIMEOUT_SECONDS`, `DEFAULT_AUTO_TASK_LEVEL_CEILING`, `DEFAULT_CONTEXT_TOKEN_LIMIT`, `DEFAULT_READ_CONTEXT_POLICY`, `DEFAULT_REQUEST_TIMEOUT`, `DEFAULT_SHELL_COMMAND_TIMEOUT_SECONDS`, `DEFAULT_UI_LANGUAGE`, `DEFAULT_UI_STYLE`, `DEFAULT_WEB_UI_DIR`, `EXECUTION_MODE_SYNC`, `INDEX_HTML`, `MAX_AGENT_ROUNDS`, `MAX_AGENT_ROUNDS_CAP`, `MAX_RUN_SECONDS`, `MAX_RUN_TIMEOUT_SECONDS`, `MAX_SHELL_COMMAND_TIMEOUT_SECONDS`, `MIN_AGENT_ROUNDS`, `MIN_CONTEXT_TOKEN_LIMIT`, `MIN_RUN_TIMEOUT_SECONDS`, `MIN_SHELL_COMMAND_TIMEOUT_SECONDS`, `RAG_ADMIN_CSS`, `RAG_ADMIN_INDEX_HTML`, `RAG_ADMIN_JS`, `RAG_CONTEXT_BUDGETS`, `RAG_DENSE_DEFAULT_ENABLED`, `RAG_EMBEDDING_MODE_VALUES`, `RAG_GRAPH_MAX_NODES`, `RAG_HIGH_RECALL_MIN_POOL`, `RAG_HIGH_RECALL_POOL_MULTIPLIER`, `RAG_IMPORT_WORKER_COUNT`, `RAG_INCLUDE_FILENAME_ENTITIES_DEFAULT`, `RAG_LIBRARY_DIRNAME`, `RAG_MAX_GLOBAL_COMMUNITIES`, `RAG_MAX_IMPORT_BATCH_BYTES`, `RAG_MAX_IMPORT_BATCH_ITEMS`, `RAG_MAX_IMPORT_FILES`, `RAG_MAX_QUERY_RESULTS`, `RAG_MIN_SYNTHESIS_SCORE`, `RAG_NO_EVIDENCE_MESSAGE`, `RAG_NO_EVIDENCE_THRESHOLD`, `RAG_PARSE_TIMEOUT_SECONDS`, `RAG_QUERY_CONTEXT_CHARS`, `RAG_RETRIEVAL_MAX_PER_DOC`, `RAG_SYNTHESIS_MAX_PER_DOC`, `RAG_WEAK_EVIDENCE_MESSAGE`, `RAG_WEAK_MATCH_SCORE_CAP`, `SESSION_HEARTBEAT_STALE_SECONDS`, `SESSION_WATCHDOG_INTERVAL_SECONDS`, `SKILLS_APP_JS`, `SKILLS_EXTRA_CSS`, `SKILLS_INDEX_HTML`, `SKILL_REFRESH_MIN_INTERVAL_SECONDS`, `TOKEN_THRESHOLD`, `WEB_UI_OPTIONAL_FILES`, `WEB_UI_REQUIRED_FILES`; `config/paths.py`: `LLM_CONFIG_PATH`, `REPO_ROOT`, `_migrate_legacy_runtime_roots`; `config/settings.py`: `_to_bool_like`, `default_multimodal_capabilities`, `extract_auto_task_level_ceiling_setting`, `extract_read_context_policy_setting`, `infer_model_multimodal_capabilities`, `merge_multimodal_capabilities`, `model_language_instruction`, `normalize_auto_task_level_ceiling`, `normalize_execution_mode`, `normalize_read_context_policy`, `normalize_ui_language`, `normalize_ui_style`, `parse_capability_overrides`, `parse_llm_config_profiles`, `resolve_optional_file_path`, `resolve_web_ui_dir_path`; `llm/client.py`: `OllamaClient`; `llm/utils.py`: `extract_base_url`, `list_ollama_models_cached`; `rag/ingestion.py`: `CodeIngestionService`, `RAGIngestionService`, `_rag_embed_batch`, `_rag_embed_text`, `_rag_mmr_select`, `_rag_query_variants`; `rag/parsers.py`: `CodeContentParser`, `RAGContentParser`; `rag/store.py`: `CodeLibraryStore`, `RAGLibraryStore`, `WikiStore`, `WorkflowMemoryStore`; `session/manager.py`: `SessionCreationLimitExceeded`, `SessionManager`; `session/state.py`: `SessionState`; `skills/store.py`: `SkillStore`, `_sanitize_skill_slug`, `analyze_skill_building_knowledge`, `ensure_runtime_skills`; `utils/crypto.py`: `CryptoBox`; `utils/files.py`: `_resolve_js_lib_asset_path`, `ensure_offline_js_libs`, `load_offline_js_lib_index`, `offline_js_lib_root`, `safe_path`, `try_read_text`; `utils/json_utils.py`: `TOOLS`, `extract_json_object_from_text`, `json_dumps`, `parse_json_object`; `utils/misc.py`: `DEFAULT_TIMEOUT_SECONDS`, `MAX_TIMEOUT_SECONDS`, `MIN_TIMEOUT_SECONDS`, `normalize_timeout_seconds`, `now_ts`, `sanitize_profile_id`; `utils/text.py`: `parse_front_matter`, `trim`
- Symbols:
  - `AppContext` (class, lines 62615-66018)

### `config/constants.py`

- Routed symbols: 359
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
  - `DEFAULT_AUTO_TASK_LEVEL_CEILING` (constant, lines 357-357)
  - `HARD_BREAK_TOOL_ERROR_THRESHOLD` (constant, lines 358-358)
  - `HARD_BREAK_RECOVERY_ROUND_THRESHOLD` (constant, lines 359-359)
  - `FUSED_FAULT_BREAK_THRESHOLD` (constant, lines 360-360)
  - `STALL_SEVERITY_ESCALATION_THRESHOLD` (constant, lines 361-361)
  - `STALL_SEVERITY_WEIGHT_BASH_READ_LOOP` (constant, lines 362-362)
  - `STALL_SEVERITY_WEIGHT_REPEATED_TOOL` (constant, lines 363-363)
  - `STALL_SEVERITY_WEIGHT_FAULT` (constant, lines 364-364)
  - `STALL_SEVERITY_WEIGHT_RECOVERY_RETRY` (constant, lines 365-365)
  - `STALL_SEVERITY_WEIGHT_WATCHDOG` (constant, lines 366-366)
  - `STALL_SEVERITY_DECAY_ON_SUCCESS` (constant, lines 367-367)
  - `STALL_ESCALATION_MIN_LEVEL` (constant, lines 368-368)
  - `STALL_PLAN_SYNTHESIS_MAX_TOKENS` (constant, lines 369-369)
  - `STALL_ESCALATION_CONTEXT_MAX_CHARS` (constant, lines 370-370)
  - `MAX_RUN_SECONDS` (constant, lines 371-371)
  - `MIN_RUN_TIMEOUT_SECONDS` (constant, lines 372-372)
  - `MAX_RUN_TIMEOUT_SECONDS` (constant, lines 373-373)
  - `DEFAULT_REQUEST_TIMEOUT` (constant, lines 383-383)
  - `_SHELL_AUTO_CONFIRM_PATTERNS` (assignment, lines 386-399)
  - `MIN_SHELL_COMMAND_TIMEOUT_SECONDS` (constant, lines 400-400)
  - `MAX_SHELL_COMMAND_TIMEOUT_SECONDS` (constant, lines 401-401)
  - `DEFAULT_SHELL_COMMAND_TIMEOUT_SECONDS` (constant, lines 402-416)
  - `AUTO_CONTINUE_BUDGET_DEFAULT` (constant, lines 417-417)
  - `AGENT_MAX_OUTPUT_TOKENS` (constant, lines 418-418)
  - `OLLAMA_THINKING_TOOL_BUFFER` (constant, lines 419-419)
  - `WATCHDOG_INTENT_NO_TOOL_THRESHOLD` (constant, lines 420-420)
  - `WATCHDOG_REPEAT_NO_TOOL_THRESHOLD` (constant, lines 421-421)
  - `WATCHDOG_INTENT_NO_TOOL_THRESHOLD_SINGLE` (constant, lines 422-422)
  - `WATCHDOG_REPEAT_NO_TOOL_THRESHOLD_SINGLE` (constant, lines 423-423)
  - `WATCHDOG_STATE_STALL_THRESHOLD` (constant, lines 424-424)
  - `WATCHDOG_CONTEXT_STALL_THRESHOLD` (constant, lines 425-425)
  - `WATCHDOG_REPEAT_SIMILARITY_THRESHOLD` (constant, lines 426-426)
  - `WATCHDOG_CONTEXT_NEAR_RATIO` (constant, lines 427-427)
  - `WATCHDOG_MAX_DECOMPOSE_STEPS` (constant, lines 428-428)
  - `WATCHDOG_STEP_MAX_ATTEMPTS` (constant, lines 429-429)
  - `EMPTY_ACTION_MIN_CONTENT_CHARS` (constant, lines 430-430)
  - `EMPTY_ACTION_WAKEUP_RETRY_LIMIT` (constant, lines 431-431)
  - `THINKING_BUDGET_FORCE_RATIO` (constant, lines 432-432)
  - `_TOOL_TIMEOUT_MAP` (assignment, lines 434-450)
  - `_DEFAULT_TOOL_TIMEOUT` (assignment, lines 451-451)
  - `TRUNCATION_CONTINUATION_MAX_PASSES` (constant, lines 452-452)
  - `TRUNCATION_CONTINUATION_MAX_TOKENS` (constant, lines 453-453)
  - `TRUNCATION_CONTINUATION_TAIL_CHARS` (constant, lines 454-454)
  - `TRUNCATION_CONTINUATION_ECHO_CHARS` (constant, lines 455-455)
  - `TRUNCATION_OVERLAP_SCAN_CHARS` (constant, lines 456-456)
  - `TRUNCATION_PAIR_SCAN_CHARS` (constant, lines 457-457)
  - `TRUNCATION_LIVE_BUFFER_MAX_CHARS` (constant, lines 458-458)
  - `MIN_CONTEXT_TOKEN_LIMIT` (constant, lines 459-459)
  - `COMPACT_TIER1_PCT` (constant, lines 461-461)
  - `COMPACT_TIER2_PCT` (constant, lines 462-462)
  - `COMPACT_TIER3_PCT` (constant, lines 463-463)
  - `COMPACT_TIER1_ABS` (constant, lines 465-465)
  - `COMPACT_TIER2_ABS` (constant, lines 466-466)
  - `CONTEXT_COMPACT_INEFFECTIVE_COOLDOWN_SECONDS` (constant, lines 467-473)
  - `FILE_BUFFER_CONTENT_THRESHOLD` (constant, lines 475-475)
  - `FILE_BUFFER_MAX_FILES` (constant, lines 476-476)
  - `AGENT_MSG_LIMIT_TIER0` (constant, lines 478-478)
  - `AGENT_MSG_LIMIT_TIER1` (constant, lines 479-479)
  - `AGENT_MSG_LIMIT_TIER2` (constant, lines 480-480)
  - `AGENT_MSG_LIMIT_TIER3` (constant, lines 481-481)
  - `AGENT_CTX_LIMIT_TIER0` (constant, lines 482-482)
  - `AGENT_CTX_LIMIT_TIER1` (constant, lines 483-483)
  - `AGENT_CTX_LIMIT_TIER2` (constant, lines 484-484)
  - `AGENT_CTX_LIMIT_TIER3` (constant, lines 485-485)
  - `MANAGER_CTX_LIMIT_TIER0` (constant, lines 486-486)
  - `MANAGER_CTX_LIMIT_TIER1` (constant, lines 487-487)
  - `MANAGER_CTX_LIMIT_TIER2` (constant, lines 488-488)
  - `MANAGER_CTX_LIMIT_TIER3` (constant, lines 489-489)
  - `MAX_CONTEXT_ARCHIVE_SEGMENTS` (constant, lines 490-490)
  - `MODEL_OUTPUT_RETRY_TIMES` (constant, lines 491-491)
  - `ARBITER_TRIGGER_MIN_CONTENT_CHARS` (constant, lines 492-492)
  - `ARBITER_VALID_PLANNING_STREAK_LIMIT` (constant, lines 493-493)
  - `ARBITER_DEFAULT_TIMEOUT_SECONDS` (constant, lines 494-494)
  - `ARBITER_DEFAULT_MAX_TOKENS` (constant, lines 495-495)
  - `ARBITER_DEFAULT_TEMPERATURE` (constant, lines 496-496)
  - `LIVE_INPUT_DELAY_WRITE_ROUNDS` (constant, lines 497-497)
  - `LIVE_INPUT_DELAY_TOOL_ROUNDS` (constant, lines 498-498)
  - `LIVE_INPUT_DELAY_NORMAL_ROUNDS` (constant, lines 499-499)
  - `LIVE_INPUT_MAX_INJECTIONS` (constant, lines 500-500)
  - `LIVE_INPUT_REINJECT_INTERVAL` (constant, lines 501-501)
  - `LIVE_INPUT_WEIGHT_BASE_DELAYED` (constant, lines 502-502)
  - `LIVE_INPUT_WEIGHT_BASE_NORMAL` (constant, lines 503-503)
  - `LIVE_INPUT_WEIGHT_STEP_DELAYED` (constant, lines 504-504)
  - `LIVE_INPUT_WEIGHT_STEP_NORMAL` (constant, lines 505-505)
  - `FINAL_SUMMARY_MIN_CHARS` (constant, lines 520-520)
  - `FINAL_SUMMARY_STRICT_MIN_CHARS` (constant, lines 521-521)
  - `RUNTIME_CONTROL_HINT_PREFIXES` (constant, lines 522-539)
  - `RETRY_RUNTIME_HINT_PREFIXES` (constant, lines 540-554)
  - `EXECUTION_MODE_SINGLE` (constant, lines 555-555)
  - `EXECUTION_MODE_SEQUENTIAL` (constant, lines 556-556)
  - `EXECUTION_MODE_SYNC` (constant, lines 557-557)
  - `EXECUTION_MODE_CHOICES` (constant, lines 558-562)
  - `AGENT_ROLES` (constant, lines 563-563)
  - `AGENT_BUBBLE_ROLES` (constant, lines 564-564)
  - `AGENT_ROLE_LABELS` (constant, lines 565-571)
  - `AGENT_ROLE_BUBBLE_COLORS` (constant, lines 572-578)
  - `BLACKBOARD_STATUSES` (constant, lines 579-588)
  - `TASK_COMPLEXITY_LEVELS` (constant, lines 589-589)
  - `TASK_COMPLEXITY_RANKS` (constant, lines 590-595)
  - `TASK_PROFILE_TYPES` (constant, lines 596-602)
  - `TASK_LEVEL_CHOICES` (constant, lines 603-603)
  - `TASK_SCALE_PREFERENCES` (constant, lines 604-604)
  - `SEMANTIC_CONFIDENCE_CHOICES` (constant, lines 605-605)
  - `TASK_LEVEL_POLICIES` (constant, lines 606-652)
  - `MANAGER_ROUTE_TARGETS` (constant, lines 653-653)
  - `BLACKBOARD_MAX_LOG_ENTRIES` (constant, lines 654-654)
  - `BLACKBOARD_MAX_TEXT` (constant, lines 655-655)
  - `SKILL_REFRESH_MIN_INTERVAL_SECONDS` (constant, lines 656-656)
  - `SKILL_PROMPT_MAX_ITEMS` (constant, lines 657-657)
  - `SKILL_PROMPT_MAX_CHARS` (constant, lines 658-658)
  - `SKILL_RUNTIME_CACHE_MAX_ENTRIES` (constant, lines 659-659)
  - `SKILL_RUNTIME_CACHE_MAX_BYTES` (constant, lines 660-660)
  - `AUTO_SKILLS_ROOT_CANDIDATES` (constant, lines 661-661)
  - `SKILL_DEFAULT_ATTACHMENT_GLOBS` (constant, lines 662-692)
  - `SKILL_INLINE_ATTACHMENT_MAX_FILES` (constant, lines 693-693)
  - `SKILL_INLINE_ATTACHMENT_MAX_CHARS` (constant, lines 694-694)
  - `SKILL_RESOURCE_MANIFEST_MAX_ITEMS` (constant, lines 695-695)
  - `SKILL_BODY_COMPACT_THRESHOLD_CHARS` (constant, lines 696-696)
  - `SKILL_BODY_PREVIEW_CHARS` (constant, lines 697-697)
  - `SKILLS_VIRTUAL_PREFIX` (constant, lines 698-698)
  - `SKILLS_EXTERNAL_MOUNT` (constant, lines 699-699)
  - `PLAN_MODE_ENABLED_LEVELS` (constant, lines 700-700)
  - `PLAN_MODE_FORCED_LEVELS` (constant, lines 701-701)
  - `PLAN_MODE_USER_CHOICES` (constant, lines 702-702)
  - `TASK_PHASES` (constant, lines 704-704)
  - `TASK_PHASE_ROUTING` (constant, lines 705-712)
  - `COMPLEXITY_KEYWORDS` (constant, lines 714-719)
  - `USER_COMPLEXITY_SIMPLE_TOKENS` (constant, lines 720-724)
  - `USER_COMPLEXITY_MODERATE_TOKENS` (constant, lines 725-729)
  - `USER_COMPLEXITY_COMPLEX_TOKENS` (constant, lines 730-734)
  - `USER_COMPLEXITY_EXPERT_TOKENS` (constant, lines 735-739)
  - `PLAN_MODE_EXPLORER_MAX_ROUNDS` (constant, lines 740-740)
  - `PLAN_MODE_SYNTHESIS_MAX_ATTEMPTS` (constant, lines 741-741)
  - `REVIEWER_DEBUG_MODE_MAX_ROUNDS` (constant, lines 743-743)
  - `REVIEWER_DEBUG_TOOL_ALLOWLIST` (constant, lines 744-748)
  - `EXPLORER_STALL_THRESHOLD` (constant, lines 749-749)
  - `DEVELOPER_EDIT_STALL_THRESHOLD` (constant, lines 750-750)
  - `PLAN_MODE_MANAGER_SYNTHESIS_MAX_TOKENS` (constant, lines 751-751)
  - `PLAN_MODE_MAX_OPTIONS` (constant, lines 752-752)
  - `PLAN_FILE_RELATIVE_PATH` (constant, lines 753-753)
  - `PLAN_BUBBLE_MAX_CHARS` (constant, lines 754-754)
  - `PLAN_NOTICE_BODY_MAX_CHARS` (constant, lines 755-755)
  - `PLAN_MESSAGE_EVENT_MAX_CHARS` (constant, lines 756-756)
  - `PLAN_STEP_FULL_CONTENT_MAX_CHARS` (constant, lines 757-757)
  - `PLAN_MODE_RESEARCH_TOOL_ALLOWLIST` (constant, lines 758-762)
  - `FAILURE_LEDGER_MAX_FIXES` (constant, lines 763-763)
  - `FAILURE_LEDGER_MAX_COMPILE_ERRORS` (constant, lines 764-764)
  - `FAILURE_LEDGER_MAX_DELEGATIONS` (constant, lines 765-765)
  - `FAILURE_LEDGER_MAX_STALLS` (constant, lines 766-766)
  - `FAILURE_LEDGER_MAX_TOOL_FPS` (constant, lines 767-767)
  - `FAILURE_LEDGER_MAX_ERRORS` (constant, lines 768-768)
  - `ERROR_CATEGORY_DEFS` (constant, lines 771-808)
  - `CHECKPOINT_MAX_COUNT` (constant, lines 809-809)
  - `CHECKPOINT_INTERVAL_ROUNDS` (constant, lines 810-810)
  - `PERSISTED_ROUTES_MAX` (constant, lines 811-811)
  - `HTML_FRONTEND_REQUEST_KEYWORDS` (constant, lines 812-851)
  - `DEEP_RESEARCH_REQUEST_KEYWORDS` (constant, lines 852-874)
  - `DEEP_RESEARCH_RETRIEVAL_KEYWORDS` (constant, lines 875-894)
  - `DEEP_RESEARCH_TEXT_ONLY_HINT_KEYWORDS` (constant, lines 895-912)
  - `DANGEROUS_PATTERNS` (constant, lines 914-914)
  - `VALID_MSG_TYPES` (constant, lines 915-921)
  - `SUPPORTED_UI_LANGUAGES` (constant, lines 923-928)
  - `UI_LANGUAGE_LABELS` (constant, lines 929-929)
  - `DEFAULT_UI_LANGUAGE` (constant, lines 930-930)
  - `UI_STYLE_CHOICES` (constant, lines 931-931)
  - `UI_STYLE_LABELS` (constant, lines 932-932)
  - `DEFAULT_UI_STYLE` (constant, lines 933-933)
  - `DEFAULT_WEB_UI_DIR` (constant, lines 934-934)
  - `DEFAULT_WEB_UI_CONFIG` (constant, lines 935-935)
  - `WEB_UI_REQUIRED_FILES` (constant, lines 936-943)
  - `WEB_UI_OPTIONAL_FILES` (constant, lines 944-944)
  - `IMAGE_EXTS` (constant, lines 946-959)
  - `IMAGE_FORMATS_NEED_CONVERSION` (constant, lines 960-960)
  - `IMAGE_SAFE_FORMATS` (constant, lines 961-961)
  - `AUDIO_EXTS` (constant, lines 962-972)
  - `VIDEO_EXTS` (constant, lines 973-983)
  - `CODE_PREVIEW_STAGE_MAX_BYTES` (constant, lines 984-984)
  - `CODE_PREVIEW_STAGE_MAX_ROWS` (constant, lines 985-985)
  - `CODE_PREVIEW_STAGE_MAX_PER_FILE` (constant, lines 986-986)
  - `CODE_PREVIEW_STAGE_MAX_TOTAL` (constant, lines 987-987)
  - `CODE_PREVIEW_DIFF_CONTEXT_LINES` (constant, lines 988-988)
  - `CODE_PREVIEW_DIFF_MERGE_GAP` (constant, lines 989-989)
  - `PREVIEW_DOWNLOAD_MAX_FILES` (constant, lines 990-990)
  - `PREVIEW_DOWNLOAD_MAX_BYTES` (constant, lines 991-991)
  - `RENDER_FRAME_MAX_B64_CHARS` (constant, lines 992-992)
  - `RENDER_FRAME_MAX_POINTS` (constant, lines 993-993)
  - `RENDER_FRAME_MAX_LINES` (constant, lines 994-994)
  - `RENDER_FRAME_MAX_LINE_POINTS` (constant, lines 995-995)
  - `RENDER_FRAME_ACTIVITY_INTERVAL_SECONDS` (constant, lines 996-996)
  - `RAW_TOOLCALL_TEXT_FILTER_THRESHOLD` (constant, lines 997-997)
  - `ASSISTANT_TEXT_PERSIST_MAX_CHARS` (constant, lines 998-998)
  - `ASSISTANT_MESSAGE_EVENT_MAX_CHARS` (constant, lines 999-999)
  - `CODE_PREVIEW_EXTS` (constant, lines 1000-1089)
  - `CODE_PREVIEW_FILENAMES` (constant, lines 1090-1101)
  - `MEDIA_CAPABILITY_KEYS` (constant, lines 1102-1109)
  - `SAMPLE_IMAGE_PNG_B64` (constant, lines 1110-1113)
  - `SAMPLE_AUDIO_WAV_B64` (constant, lines 1114-1116)
  - `SAMPLE_VIDEO_MP4_B64` (constant, lines 1117-1119)
  - `OFFLINE_JS_LIB_CATALOG` (constant, lines 1121-1379)
  - `OFFLINE_JS_LIB_INDEX_FILE` (constant, lines 1380-1380)
  - `OFFLINE_JS_LIB_README_FILE` (constant, lines 1381-1381)
  - `BACKEND_I18N` (constant, lines 1567-1636)
  - `call_backend_i18n_en_update_l1638` (expression, lines 1638-1731)
  - `call_backend_i18n_zh_cn_update_l1732` (expression, lines 1732-1825)
  - `call_backend_i18n_zh_tw_update_l1826` (expression, lines 1826-1919)
  - `call_backend_i18n_ja_update_l1920` (expression, lines 1920-2013)
  - `OPENAI_COMPAT_PROVIDER_NAMES` (constant, lines 4177-4185)
  - `OPENAI_LIKE_PROVIDER_NAMES` (constant, lines 4187-4187)
  - `TABULAR_PREVIEW_EXTS` (constant, lines 5718-5718)
  - `EXCEL_PREVIEW_EXTS` (constant, lines 5719-5719)
  - `PRESENTATION_PREVIEW_EXTS` (constant, lines 5720-5720)
  - `DOCUMENT_PREVIEW_EXTS` (constant, lines 5721-5721)
  - `EMBEDDED_SKILLS_ARCHIVE_B64` (constant, lines 6122-6641)
  - `EMBEDDED_SKILLS_ARCHIVE_SHA256` (constant, lines 6642-6642)
  - `EMBEDDED_SKILLS_ARCHIVE_FILES` (constant, lines 6643-6666)
  - `BUILTIN_CLAWHUB_SKILLS_VERSION` (constant, lines 9823-9823)
  - `EMBEDDED_CLAWHUB_SKILLS_ARCHIVE_B64` (constant, lines 9825-10069)
  - `SKILL_PROTOCOL_LOCAL` (constant, lines 10135-10135)
  - `SKILL_PROTOCOL_CLAWHUB` (constant, lines 10136-10136)
  - `SKILL_PROTOCOL_HTTP_JSON` (constant, lines 10137-10137)
  - `SKILL_PROTOCOL_SPECS` (constant, lines 10139-10170)
  - `AGENT_TOOL_ALLOWLIST` (constant, lines 13914-13957)
  - `INDEX_HTML` (constant, lines 44558-44747)
  - `APP_CSS` (constant, lines 44749-45161)
  - `APP_JS` (constant, lines 45163-48480)
  - `APP_TS` (constant, lines 48482-48509)
  - `SKILLS_INDEX_HTML` (constant, lines 48511-48665)
  - `SKILLS_EXTRA_CSS` (constant, lines 48667-48762)
  - `SKILLS_APP_JS` (constant, lines 48764-48905)
  - `RAG_TERM_GROUPS` (constant, lines 48907-53539)
  - `RAG_RESEARCH_HINTS` (constant, lines 53540-53561)
  - `RAG_CODE_HINTS` (constant, lines 53562-53572)
  - `RAG_SHORT_TOKEN_ALLOWLIST` (constant, lines 53573-53588)
  - `RAG_EN_STOPWORDS` (constant, lines 53589-53661)
  - `RAG_ZH_STOPWORDS` (constant, lines 53662-53698)
  - `RAG_GENERIC_ENTITY_TERMS_EN` (constant, lines 53699-53777)
  - `RAG_GENERIC_ENTITY_TERMS_ZH` (constant, lines 53778-53820)
  - `RAG_STRUCTURAL_ENTITY_PATTERNS` (constant, lines 53821-53839)
  - `CODE_LIBRARY_IGNORED_DIRS` (constant, lines 54532-54537)
  - `CODE_LIBRARY_LANGUAGE_BY_EXT` (constant, lines 54538-54594)
  - `CODE_LIBRARY_SPECIAL_FILENAMES` (constant, lines 54595-54601)
  - `RAG_ADMIN_INDEX_HTML` (constant, lines 60525-60698)
  - `RAG_ADMIN_CSS` (constant, lines 60700-60790)
  - `RAG_ADMIN_JS` (constant, lines 60792-62555)
  - `CODE_ADMIN_INDEX_HTML` (constant, lines 62557-62568)
  - `CODE_ADMIN_CSS` (constant, lines 62569-62599)
  - `CODE_ADMIN_JS` (constant, lines 62600-62604)

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
  - `detect_repo_root` (function, lines 2772-2786)
  - `REPO_ROOT` (constant, lines 2788-2788)

### `config/settings.py`

- Routed symbols: 38
- Cross-module imports: `config/constants.py`: `AUTO_SKILLS_ROOT_CANDIDATES`, `BACKEND_I18N`, `DEFAULT_AUTO_TASK_LEVEL_CEILING`, `DEFAULT_READ_CONTEXT_POLICY`, `DEFAULT_REQUEST_TIMEOUT`, `DEFAULT_SHELL_COMMAND_TIMEOUT_SECONDS`, `DEFAULT_UI_LANGUAGE`, `DEFAULT_UI_STYLE`, `DEFAULT_WEB_UI_CONFIG`, `DEFAULT_WEB_UI_DIR`, `EXECUTION_MODE_CHOICES`, `EXECUTION_MODE_SEQUENTIAL`, `EXECUTION_MODE_SINGLE`, `EXECUTION_MODE_SYNC`, `MAX_SHELL_COMMAND_TIMEOUT_SECONDS`, `MEDIA_CAPABILITY_KEYS`, `MIN_SHELL_COMMAND_TIMEOUT_SECONDS`, `READ_CONTEXT_POLICY_CHOICES`, `SUPPORTED_UI_LANGUAGES`, `TASK_COMPLEXITY_LEVELS`, `TASK_COMPLEXITY_RANKS`, `TASK_LEVEL_CHOICES`, `UI_LANGUAGE_LABELS`, `UI_STYLE_CHOICES`, `USER_COMPLEXITY_COMPLEX_TOKENS`, `USER_COMPLEXITY_EXPERT_TOKENS`, `USER_COMPLEXITY_MODERATE_TOKENS`, `USER_COMPLEXITY_SIMPLE_TOKENS`; `config/paths.py`: `WORKDIR`; `llm/utils.py`: `_is_http_url`, `_resolve_local_path`, `complete_chat_endpoint`, `extract_base_url`, `is_openai_like_provider`, `normalize_openai_compat_provider_name`, `strip_thinking_content`; `skills/store.py`: `ensure_embedded_skills`; `utils/http.py`: `urlopen`; `utils/json_utils.py`: `parse_json_object`; `utils/misc.py`: `MAX_TIMEOUT_SECONDS`, `MIN_TIMEOUT_SECONDS`, `normalize_timeout_seconds`, `sanitize_profile_id`; `utils/text.py`: `trim`
- Symbols:
  - `normalize_ui_language` (function, lines 1465-1487)
  - `normalize_ui_style` (function, lines 1490-1507)
  - `supported_ui_languages_payload` (function, lines 1510-1511)
  - `normalize_execution_mode` (function, lines 1514-1533)
  - `model_language_instruction` (function, lines 1536-1564)
  - `backend_i18n_text` (function, lines 2016-2026)
  - `backend_role_label` (function, lines 2029-2033)
  - `_detect_os_shell_instruction` (function, lines 2036-2075)
  - `resolve_web_ui_dir_path` (function, lines 2077-2084)
  - `resolve_optional_file_path` (function, lines 2087-2094)
  - `resolve_skills_root_path` (function, lines 2097-2104)
  - `_count_skill_markdown_files` (function, lines 2107-2118)
  - `select_preferred_skills_root` (function, lines 2121-2155)
  - `load_web_ui_config_file` (function, lines 2158-2172)
  - `extract_show_upload_list_setting` (function, lines 2175-2189)
  - `extract_ui_style_setting` (function, lines 2192-2206)
  - `extract_js_lib_download_setting` (function, lines 2209-2228)
  - `extract_daily_session_limit_setting` (function, lines 2231-2274)
  - `extract_shell_command_timeout_setting` (function, lines 2277-2323)
  - `extract_context_token_limit_setting` (function, lines 2326-2358)
  - `normalize_auto_task_level_ceiling` (function, lines 2361-2380)
  - `extract_auto_task_level_ceiling_setting` (function, lines 2383-2410)
  - `normalize_read_context_policy` (function, lines 2413-2431)
  - `extract_read_context_policy_setting` (function, lines 2434-2455)
  - `default_multimodal_capabilities` (function, lines 2464-2472)
  - `_to_bool_like` (function, lines 2475-2485)
  - `infer_model_multimodal_capabilities` (function, lines 2488-2532)
  - `parse_capability_overrides` (function, lines 2535-2572)
  - `merge_multimodal_capabilities` (function, lines 2575-2582)
  - `parse_media_endpoints` (function, lines 2585-2599)
  - `infer_user_complexity_value` (function, lines 4095-4111)
  - `normalize_task_complexity` (function, lines 4113-4141)
  - `task_complexity_rank` (function, lines 4143-4144)
  - `task_complexity_at_least` (function, lines 4146-4147)
  - `max_task_complexity` (function, lines 4149-4158)
  - `load_llm_config_from_source` (function, lines 4309-4343)
  - `parse_llm_config_profiles` (function, lines 4345-4931)
  - `looks_like_llm_config` (function, lines 4933-5007)

### `llm/client.py`

- Routed symbols: 2
- Cross-module imports: `config/constants.py`: `DEFAULT_REQUEST_TIMEOUT`, `LLM_HTTP_RETRY_404_ON_VLLM`, `LLM_HTTP_RETRY_DELAY_SECONDS`, `LLM_HTTP_RETRY_MAX_ATTEMPTS`, `LLM_HTTP_RETRY_MAX_SECONDS`, `LLM_HTTP_RETRY_STATUSES`, `OLLAMA_THINKING_TOOL_BUFFER`, `SAMPLE_AUDIO_WAV_B64`, `SAMPLE_IMAGE_PNG_B64`, `SAMPLE_VIDEO_MP4_B64`; `config/settings.py`: `default_multimodal_capabilities`, `infer_model_multimodal_capabilities`, `merge_multimodal_capabilities`, `parse_capability_overrides`, `parse_media_endpoints`; `llm/utils.py`: `complete_chat_endpoint`, `is_openai_compat_provider`, `is_openai_like_provider`, `normalize_openai_compat_provider_name`, `split_thinking_content`; `utils/http.py`: `urlopen`; `utils/json_utils.py`: `canonicalize_tool_name`, `json_dumps`, `parse_json_object`, `parse_tool_arguments`, `parse_tool_arguments_with_error`; `utils/misc.py`: `MAX_TIMEOUT_SECONDS`, `MIN_TIMEOUT_SECONDS`, `make_id`, `normalize_timeout_seconds`, `now_ts`; `utils/text.py`: `trim`
- Symbols:
  - `OllamaError` (class, lines 12068-12088)
  - `OllamaClient` (class, lines 12090-13557)

### `llm/utils.py`

- Routed symbols: 25
- Cross-module imports: `config/constants.py`: `OPENAI_COMPAT_PROVIDER_NAMES`, `OPENAI_LIKE_PROVIDER_NAMES`; `utils/http.py`: `urlopen`; `utils/json_utils.py`: `json_dumps`, `parse_json_object`; `utils/text.py`: `trim`
- Symbols:
  - `probe_ollama_environment` (function, lines 3779-3792)
  - `list_ollama_models` (function, lines 3794-3796)
  - `_OLLAMA_TAG_CACHE_LOCK` (assignment, lines 3798-3798)
  - `_OLLAMA_TAG_CACHE` (assignment, lines 3799-3799)
  - `list_ollama_models_cached` (function, lines 3809-3846)
  - `resolve_ollama_model` (function, lines 3848-3858)
  - `infer_thinking_model` (function, lines 3860-3862)
  - `split_thinking_content` (function, lines 3864-3907)
  - `strip_thinking_content` (function, lines 3909-3910)
  - `check_ollama_model_ready` (function, lines 3912-3936)
  - `list_loaded_ollama_models` (function, lines 3938-3951)
  - `wake_ollama_model` (function, lines 3953-3983)
  - `try_pull_ollama_model` (function, lines 3985-4003)
  - `ordered_model_candidates` (function, lines 4005-4023)
  - `pick_working_ollama_model` (function, lines 4025-4041)
  - `extract_base_url` (function, lines 4074-4082)
  - `complete_chat_endpoint` (function, lines 4084-4093)
  - `normalize_openai_compat_provider_name` (function, lines 4160-4175)
  - `is_openai_compat_provider` (function, lines 4189-4190)
  - `is_openai_like_provider` (function, lines 4192-4193)
  - `openai_compat_probe_headers` (function, lines 4195-4206)
  - `openai_compat_model_list_urls` (function, lines 4208-4240)
  - `extract_openai_compat_model_ids` (function, lines 4242-4275)
  - `_is_http_url` (function, lines 4284-4289)
  - `_resolve_local_path` (function, lines 4291-4307)

### `rag/index.py`

- Routed symbols: 5
- Cross-module imports: `config/constants.py`: `RAG_DYNAMIC_NOISE_HARD_COMMUNITY_RATIO`, `RAG_DYNAMIC_NOISE_HARD_DOC_RATIO`, `RAG_DYNAMIC_NOISE_MIN_COMMUNITY_FREQ`, `RAG_DYNAMIC_NOISE_MIN_DOC_FREQ`, `RAG_DYNAMIC_NOISE_SOFT_COMMUNITY_RATIO`, `RAG_DYNAMIC_NOISE_SOFT_DOC_RATIO`, `RAG_EN_STOPWORDS`, `RAG_GRAPH_MAX_NODES`, `RAG_INCLUDE_FILENAME_ENTITIES_DEFAULT`, `RAG_MAX_COMMUNITY_MAP_SUPPORT`, `RAG_MAX_GLOBAL_COMMUNITIES`, `RAG_MAX_QUERY_RESULTS`, `RAG_MIN_SYNTHESIS_SCORE`, `RAG_WEAK_MATCH_SCORE_CAP`; `rag/ingestion.py`: `_rag_focused_excerpt`, `_rag_mmr_select`, `_rag_window_for_query`; `rag/parsers.py`: `_code_is_test_path`, `_rag_apply_filename_entity_policy`, `_rag_choose_community`, `_rag_classify_document`, `_rag_expand_tokens`, `_rag_extract_entities`, `_rag_filter_entities`, `_rag_tokenize`; `utils/misc.py`: `now_ts`; `utils/text.py`: `trim`
- Symbols:
  - `_code_module_name` (function, lines 54628-54642)
  - `_code_choose_community` (function, lines 54645-54652)
  - `_code_query_terms` (function, lines 54655-54667)
  - `TFGraphIDFIndex` (class, lines 55720-57286)
  - `CodeGraphIndex` (class, lines 59704-60169)

### `rag/ingestion.py`

- Routed symbols: 12
- Cross-module imports: `config/constants.py`: `CODE_IMPORT_WORKER_COUNT`, `CODE_LIBRARY_IGNORED_DIRS`, `CODE_PARSE_TIMEOUT_SECONDS`, `RAG_IMPORT_WORKER_COUNT`, `RAG_MAX_IMPORT_BATCH_ITEMS`, `RAG_MAX_IMPORT_FILES`, `RAG_MODEL_MEDIA_MAX_BYTES`, `RAG_PARSE_TIMEOUT_SECONDS`, `RAG_PDF_IMAGE_LIMIT`, `RAG_RETRIEVAL_MAX_PER_DOC`; `config/settings.py`: `default_multimodal_capabilities`; `rag/parsers.py`: `CodeContentParser`, `RAGContentParser`, `_rag_expand_tokens`, `_rag_extract_entities`, `_rag_is_noise_token`, `_rag_safe_name`, `_rag_tokenize`; `rag/store.py`: `CodeLibraryStore`, `RAGLibraryStore`, `WikiStore`; `session/state.py`: `SessionState`; `utils/files.py`: `try_read_text`; `utils/json_utils.py`: `_read_json_file`, `_write_json_file`, `parse_json_object`; `utils/media.py`: `guess_mime_from_name`; `utils/misc.py`: `make_id`, `now_ts`; `utils/text.py`: `trim`
- Symbols:
  - `_rag_trigram_set` (function, lines 54052-54057)
  - `_rag_jaccard_sim` (function, lines 54060-54067)
  - `_rag_mmr_select` (function, lines 54070-54117)
  - `_rag_embed_text` (function, lines 54254-54275)
  - `_rag_embed_batch` (function, lines 54278-54284)
  - `_rag_window_for_query` (function, lines 54287-54299)
  - `_rag_focused_excerpt` (function, lines 54302-54342)
  - `_rag_query_variants` (function, lines 54345-54382)
  - `_rag_parse_segments` (function, lines 54385-54445)
  - `_rag_parse_file_worker` (function, lines 58808-58822)
  - `RAGIngestionService` (class, lines 58825-59701)
  - `CodeIngestionService` (class, lines 60438-60523)

### `rag/parsers.py`

- Routed symbols: 28
- Cross-module imports: `config/constants.py`: `AUDIO_EXTS`, `CODE_CHUNK_CHARS`, `CODE_CHUNK_OVERLAP`, `CODE_LIBRARY_LANGUAGE_BY_EXT`, `CODE_LIBRARY_SPECIAL_FILENAMES`, `CODE_MAX_CHUNKS_PER_DOC`, `CODE_PREVIEW_DIFF_CONTEXT_LINES`, `CODE_PREVIEW_DIFF_MERGE_GAP`, `CODE_PREVIEW_EXTS`, `CODE_PREVIEW_FILENAMES`, `CODE_PREVIEW_STAGE_MAX_ROWS`, `DOCUMENT_PREVIEW_EXTS`, `EXCEL_PREVIEW_EXTS`, `IMAGE_EXTS`, `PRESENTATION_PREVIEW_EXTS`, `RAG_CHUNK_CHARS`, `RAG_CHUNK_OVERLAP`, `RAG_CODE_HINTS`, `RAG_EN_STOPWORDS`, `RAG_GENERIC_ENTITY_TERMS_EN`, `RAG_GENERIC_ENTITY_TERMS_ZH`, `RAG_INCLUDE_FILENAME_ENTITIES_DEFAULT`, `RAG_MAX_CHUNKS_PER_DOC`, `RAG_PDF_IMAGE_LIMIT`, `RAG_RESEARCH_HINTS`, `RAG_SHORT_TOKEN_ALLOWLIST`, `RAG_STRUCTURAL_ENTITY_PATTERNS`, `RAG_TERM_GROUPS`, `RAG_ZH_STOPWORDS`, `TABULAR_PREVIEW_EXTS`, `VIDEO_EXTS`; `rag/ingestion.py`: `_rag_parse_segments`; `utils/files.py`: `_sha256_bytes`, `_sha256_file`; `utils/json_utils.py`: `parse_json_object`; `utils/media.py`: `guess_mime_from_name`; `utils/text.py`: `_focused_diff_rows_from_opcodes`, `_skip_row`, `trim`
- Symbols:
  - `normalize_rel_preview_path` (function, lines 5693-5704)
  - `is_code_preview_candidate` (function, lines 5707-5715)
  - `preview_kind_for_path` (function, lines 5724-5753)
  - `build_code_preview_rows` (function, lines 5756-5802)
  - `_rag_safe_name` (function, lines 53851-53854)
  - `_rag_detect_language` (function, lines 53857-53871)
  - `_rag_cjk_ngrams` (function, lines 53874-53886)
  - `_rag_is_noise_token` (function, lines 53889-53908)
  - `_rag_entity_allowed` (function, lines 53911-53923)
  - `_rag_filter_entities` (function, lines 53926-53940)
  - `_rag_filename_entity_aliases` (function, lines 53943-53976)
  - `_rag_apply_filename_entity_policy` (function, lines 53979-54009)
  - `_rag_choose_community` (function, lines 54012-54049)
  - `_rag_tokenize` (function, lines 54120-54171)
  - `_rag_expand_tokens` (function, lines 54174-54195)
  - `_rag_extract_entities` (function, lines 54198-54214)
  - `_rag_classify_document` (function, lines 54217-54251)
  - `_rag_chunk_text` (function, lines 54448-54527)
  - `_code_language_from_name` (function, lines 54604-54620)
  - `_code_is_test_path` (function, lines 54623-54625)
  - `_CallCollector` (class, lines 54670-54682)
  - `_ALGO_COMPLEXITY_RE` (assignment, lines 54685-54685)
  - `_ALGO_STEP_RE` (assignment, lines 54686-54686)
  - `_ALGO_MATH_VARS` (assignment, lines 54687-54687)
  - `_ALGO_DOC_KEYWORDS` (assignment, lines 54688-54688)
  - `_detect_algo_chunk` (function, lines 54691-54714)
  - `CodeContentParser` (class, lines 54717-55207)
  - `RAGContentParser` (class, lines 55210-55717)

### `rag/store.py`

- Routed symbols: 4
- Cross-module imports: `config/constants.py`: `CODE_CHUNK_CHARS`, `CODE_CHUNK_OVERLAP`, `CODE_MAX_CHUNKS_PER_DOC`, `RAG_INCLUDE_FILENAME_ENTITIES_DEFAULT`, `RAG_MAX_QUERY_RESULTS`, `RAG_RETRIEVAL_MAX_PER_DOC`, `RAG_TASK_HISTORY_LIMIT`, `RAG_WEAK_MATCH_SCORE_CAP`, `RAG_WORKFLOW_ACCEPT_SCORE`; `rag/index.py`: `CodeGraphIndex`, `TFGraphIDFIndex`, `_code_choose_community`, `_code_module_name`; `rag/ingestion.py`: `_rag_focused_excerpt`, `_rag_mmr_select`, `_rag_window_for_query`; `rag/parsers.py`: `_code_is_test_path`, `_rag_apply_filename_entity_policy`, `_rag_choose_community`, `_rag_chunk_text`, `_rag_entity_allowed`, `_rag_expand_tokens`, `_rag_extract_entities`, `_rag_filter_entities`, `_rag_safe_name`, `_rag_tokenize`; `skills/store.py`: `_write_text_if_changed`; `utils/files.py`: `_sha256_bytes`, `_sha256_file`, `try_read_text`; `utils/json_utils.py`: `_read_json_file`, `_write_json_file`, `json_dumps`; `utils/media.py`: `guess_mime_from_name`; `utils/misc.py`: `make_id`, `now_ts`; `utils/text.py`: `trim`
- Symbols:
  - `RAGLibraryStore` (class, lines 57298-57872)
  - `WikiStore` (class, lines 57875-58404)
  - `WorkflowMemoryStore` (class, lines 58407-58805)
  - `CodeLibraryStore` (class, lines 60172-60435)

### `server/handlers.py`

- Routed symbols: 5
- Cross-module imports: `app/context.py`: `AppContext`; `config/constants.py`: `APP_VERSION`, `DEFAULT_AUTO_TASK_LEVEL_CEILING`, `DEFAULT_READ_CONTEXT_POLICY`, `DEFAULT_REQUEST_TIMEOUT`, `DEFAULT_SHELL_COMMAND_TIMEOUT_SECONDS`, `DEFAULT_UI_LANGUAGE`, `DEFAULT_UI_STYLE`, `EXECUTION_MODE_CHOICES`, `EXECUTION_MODE_SYNC`, `MIN_RUN_TIMEOUT_SECONDS`, `PLAN_MODE_USER_CHOICES`, `RAG_GRAPH_MAX_NODES`, `SESSION_LIST_DEFAULT_LIMIT`, `SSE_HEARTBEAT_SECONDS`, `TASK_COMPLEXITY_LEVELS`, `TASK_LEVEL_CHOICES`, `TASK_LEVEL_POLICIES`, `UI_STYLE_LABELS`; `config/paths.py`: `LLM_CONFIG_PATH`, `REPO_ROOT`, `WORKDIR`; `config/settings.py`: `_to_bool_like`, `infer_user_complexity_value`, `looks_like_llm_config`, `normalize_auto_task_level_ceiling`, `normalize_execution_mode`, `normalize_read_context_policy`, `normalize_task_complexity`, `normalize_ui_language`, `normalize_ui_style`, `resolve_web_ui_dir_path`, `supported_ui_languages_payload`; `llm/utils.py`: `extract_base_url`, `extract_openai_compat_model_ids`, `list_ollama_models`, `normalize_openai_compat_provider_name`, `openai_compat_model_list_urls`, `openai_compat_probe_headers`; `rag/parsers.py`: `normalize_rel_preview_path`; `session/manager.py`: `SessionCreationLimitExceeded`, `SessionManager`; `session/state.py`: `SessionState`; `skills/store.py`: `analyze_skill_building_knowledge`; `utils/files.py`: `safe_path`, `try_read_text`; `utils/http.py`: `urlopen`; `utils/json_utils.py`: `json_dumps`, `parse_json_object`; `utils/media.py`: `guess_mime_from_name`; `utils/misc.py`: `now_ts`, `swallow_benign_socket_error`, `user_id_from_ip`; `utils/text.py`: `trim`
- Symbols:
  - `AgentHTTPServer` (class, lines 66029-66057)
  - `Handler` (class, lines 66061-66974)
  - `SkillsHandler` (class, lines 66976-67178)
  - `RagAdminHandler` (class, lines 67180-67348)
  - `CodeAdminHandler` (class, lines 67351-67537)

### `session/manager.py`

- Routed symbols: 2
- Cross-module imports: `config/constants.py`: `AGENT_MAX_OUTPUT_TOKENS`, `ARBITER_DEFAULT_MAX_TOKENS`, `ARBITER_DEFAULT_TEMPERATURE`, `ARBITER_DEFAULT_TIMEOUT_SECONDS`, `DEFAULT_AUTO_TASK_LEVEL_CEILING`, `DEFAULT_CONTEXT_TOKEN_LIMIT`, `DEFAULT_READ_CONTEXT_POLICY`, `DEFAULT_REQUEST_TIMEOUT`, `DEFAULT_SHELL_COMMAND_TIMEOUT_SECONDS`, `DEFAULT_UI_LANGUAGE`, `EXECUTION_MODE_SYNC`, `MAX_AGENT_ROUNDS`, `MAX_AGENT_ROUNDS_CAP`, `MAX_RUN_SECONDS`, `MAX_RUN_TIMEOUT_SECONDS`, `MAX_SHELL_COMMAND_TIMEOUT_SECONDS`, `MIN_AGENT_ROUNDS`, `MIN_CONTEXT_TOKEN_LIMIT`, `MIN_RUN_TIMEOUT_SECONDS`, `MIN_SHELL_COMMAND_TIMEOUT_SECONDS`, `SESSION_LIST_DEFAULT_LIMIT`, `TOKEN_THRESHOLD`; `config/paths.py`: `LLM_CONFIG_PATH`; `config/settings.py`: `extract_auto_task_level_ceiling_setting`, `infer_model_multimodal_capabilities`, `merge_multimodal_capabilities`, `normalize_auto_task_level_ceiling`, `normalize_execution_mode`, `normalize_read_context_policy`, `normalize_ui_language`, `parse_capability_overrides`, `parse_llm_config_profiles`; `llm/client.py`: `OllamaClient`; `llm/utils.py`: `complete_chat_endpoint`, `extract_base_url`, `is_openai_compat_provider`, `list_ollama_models_cached`, `probe_ollama_environment`; `session/state.py`: `SessionState`; `utils/crypto.py`: `CryptoBox`; `utils/files.py`: `try_read_text`; `utils/json_utils.py`: `parse_json_object`; `utils/misc.py`: `make_id`, `normalize_timeout_seconds`, `now_ts`, `sanitize_profile_id`
- Symbols:
  - `SessionCreationLimitExceeded` (class, lines 2458-2461)
  - `SessionManager` (class, lines 43582-44556)

### `session/state.py`

- Routed symbols: 1
- Cross-module imports: `agent/background.py`: `BackgroundManager`; `agent/bus.py`: `MessageBus`; `agent/events.py`: `EventHub`; `agent/tasks.py`: `TaskManager`; `agent/todo.py`: `TodoManager`; `agent/worktree.py`: `WorktreeManager`; `config/constants.py`: `AGENT_BUBBLE_ROLES`, `AGENT_CTX_LIMIT_TIER0`, `AGENT_CTX_LIMIT_TIER1`, `AGENT_CTX_LIMIT_TIER2`, `AGENT_CTX_LIMIT_TIER3`, `AGENT_MAX_OUTPUT_TOKENS`, `AGENT_MSG_LIMIT_TIER0`, `AGENT_MSG_LIMIT_TIER1`, `AGENT_MSG_LIMIT_TIER2`, `AGENT_MSG_LIMIT_TIER3`, `AGENT_ROLES`, `AGENT_TOOL_ALLOWLIST`, `ARBITER_DEFAULT_MAX_TOKENS`, `ARBITER_DEFAULT_TEMPERATURE`, `ARBITER_DEFAULT_TIMEOUT_SECONDS`, `ARBITER_TRIGGER_MIN_CONTENT_CHARS`, `ARBITER_VALID_PLANNING_STREAK_LIMIT`, `ASSISTANT_MESSAGE_EVENT_MAX_CHARS`, `ASSISTANT_TEXT_PERSIST_MAX_CHARS`, `AUDIO_EXTS`, `AUTO_CONTINUE_BUDGET_DEFAULT`, `BASH_READ_LOOP_THRESHOLD`, `BLACKBOARD_MAX_LOG_ENTRIES`, `BLACKBOARD_MAX_TEXT`, `BLACKBOARD_STATUSES`, `CHAT_UPLOAD_AUTO_LIBRARY_INGEST`, `CHAT_UPLOAD_INGEST_QUEUE_MAX`, `CHAT_UPLOAD_INLINE_TEXT_BYTES`, `CHAT_UPLOAD_PARSE_MAX_BYTES`, `CHAT_UPLOAD_PARSE_QUEUE_MAX`, `CHAT_UPLOAD_PARSE_TIMEOUT_SECONDS`, `CHAT_UPLOAD_PROMPT_MAX_CHARS`, `CHAT_UPLOAD_PROMPT_MAX_FILES`, `CHAT_UPLOAD_PROMPT_PER_FILE_CHARS`, `CHAT_UPLOAD_TEXT_CONTEXT_CHARS`, `CHAT_UPLOAD_ZIP_ENTRY_MAX_BYTES`, `CHECKPOINT_INTERVAL_ROUNDS`, `CHECKPOINT_MAX_COUNT`, `CODE_PREVIEW_STAGE_MAX_BYTES`, `CODE_PREVIEW_STAGE_MAX_PER_FILE`, `CODE_PREVIEW_STAGE_MAX_ROWS`, `CODE_PREVIEW_STAGE_MAX_TOTAL`, `COMPACT_TIER1_ABS`, `COMPACT_TIER1_PCT`, `COMPACT_TIER2_ABS`, `COMPACT_TIER2_PCT`, `COMPACT_TIER3_PCT`, `CONTEXT_ACTUAL_USAGE_RECENT_SECONDS`, `CONTEXT_AUTO_COMPACT_RESERVE_RATIO`, `CONTEXT_COMPACT_INEFFECTIVE_COOLDOWN_SECONDS`, `CONTEXT_ESTIMATE_SAFETY_MULTIPLIER`, `CONTEXT_USAGE_CALIBRATION_MAX`, `DANGEROUS_PATTERNS`, `DEEP_RESEARCH_REQUEST_KEYWORDS`, `DEEP_RESEARCH_RETRIEVAL_KEYWORDS`, `DEEP_RESEARCH_TEXT_ONLY_HINT_KEYWORDS`, `DEFAULT_AUTO_TASK_LEVEL_CEILING`, `DEFAULT_CONTEXT_TOKEN_LIMIT`, `DEFAULT_READ_CONTEXT_POLICY`, `DEFAULT_REQUEST_TIMEOUT`, `DEFAULT_SHELL_COMMAND_TIMEOUT_SECONDS`, `DEFAULT_UI_LANGUAGE`, `DEVELOPER_EDIT_STALL_THRESHOLD`, `EMPTY_ACTION_MIN_CONTENT_CHARS`, `EMPTY_ACTION_WAKEUP_RETRY_LIMIT`, `ERROR_CATEGORY_DEFS`, `EXECUTION_MODE_CHOICES`, `EXECUTION_MODE_SEQUENTIAL`, `EXECUTION_MODE_SINGLE`, `EXECUTION_MODE_SYNC`, `EXPLORER_STALL_THRESHOLD`, `FAILURE_LEDGER_MAX_COMPILE_ERRORS`, `FAILURE_LEDGER_MAX_DELEGATIONS`, `FAILURE_LEDGER_MAX_ERRORS`, `FAILURE_LEDGER_MAX_FIXES`, `FAILURE_LEDGER_MAX_STALLS`, `FAILURE_LEDGER_MAX_TOOL_FPS`, `FILE_BUFFER_CONTENT_THRESHOLD`, `FILE_BUFFER_MAX_FILES`, `FINAL_SUMMARY_MIN_CHARS`, `FINAL_SUMMARY_STRICT_MIN_CHARS`, `FUSED_FAULT_BREAK_THRESHOLD`, `HARD_BREAK_RECOVERY_ROUND_THRESHOLD`, `HARD_BREAK_TOOL_ERROR_THRESHOLD`, `HTML_FRONTEND_REQUEST_KEYWORDS`, `IMAGE_EXTS`, `IMAGE_FORMATS_NEED_CONVERSION`, `LARGE_FILE_AUTO_PAGE_BYTES`, `LARGE_FILE_AUTO_PAGE_LINES`, `LARGE_SOURCE_UPLOAD_EXCERPT_CHARS`, `LIVE_INPUT_DELAY_NORMAL_ROUNDS`, `LIVE_INPUT_DELAY_TOOL_ROUNDS`, `LIVE_INPUT_DELAY_WRITE_ROUNDS`, `LIVE_INPUT_MAX_INJECTIONS`, `LIVE_INPUT_REINJECT_INTERVAL`, `LIVE_INPUT_WEIGHT_BASE_DELAYED`, `LIVE_INPUT_WEIGHT_BASE_NORMAL`, `LIVE_INPUT_WEIGHT_STEP_DELAYED`, `LIVE_INPUT_WEIGHT_STEP_NORMAL`, `LONG_OUTPUT_LISTING_OFFLOAD_CHARS`, `LONG_OUTPUT_MODEL_PAGE_CHARS`, `LONG_OUTPUT_READ_PAGE_LINES`, `LONG_OUTPUT_TEMP_MAX_FILES`, `LONG_OUTPUT_UI_PAGE_CHARS`, `LONG_OUTPUT_UI_PREVIEW_MAX_PAGES`, `MANAGER_CTX_LIMIT_TIER0`, `MANAGER_CTX_LIMIT_TIER1`, `MANAGER_CTX_LIMIT_TIER2`, `MANAGER_CTX_LIMIT_TIER3`, `MANAGER_ROUTE_TARGETS`, `MAX_AGENT_ROUNDS`, `MAX_AGENT_ROUNDS_CAP`, `MAX_CONTEXT_ARCHIVE_SEGMENTS`, `MAX_RUN_SECONDS`, `MAX_RUN_TIMEOUT_SECONDS`, `MAX_SHELL_COMMAND_TIMEOUT_SECONDS`, `MIN_AGENT_ROUNDS`, `MIN_CONTEXT_TOKEN_LIMIT`, `MIN_RUN_TIMEOUT_SECONDS`, `MIN_SHELL_COMMAND_TIMEOUT_SECONDS`, `MODEL_CALL_PROGRESS_DELAY`, `MODEL_CALL_PROGRESS_INTERVAL`, `MODEL_OUTPUT_RETRY_TIMES`, `PERSISTED_ROUTES_MAX`, `PLAN_BUBBLE_MAX_CHARS`, `PLAN_FILE_RELATIVE_PATH`, `PLAN_MESSAGE_EVENT_MAX_CHARS`, `PLAN_MODE_ENABLED_LEVELS`, `PLAN_MODE_EXPLORER_MAX_ROUNDS`, `PLAN_MODE_FORCED_LEVELS`, `PLAN_MODE_MANAGER_SYNTHESIS_MAX_TOKENS`, `PLAN_MODE_MAX_OPTIONS`, `PLAN_MODE_RESEARCH_TOOL_ALLOWLIST`, `PLAN_MODE_SYNTHESIS_MAX_ATTEMPTS`, `PLAN_MODE_USER_CHOICES`, `PLAN_NOTICE_BODY_MAX_CHARS`, `PLAN_STEP_FULL_CONTENT_MAX_CHARS`, `PREVIEW_DOWNLOAD_MAX_BYTES`, `PREVIEW_DOWNLOAD_MAX_FILES`, `READ_CONTEXT_PROMPT_MAX_CHARS`, `READ_CONTEXT_PROMPT_MAX_ITEMS`, `READ_CONTEXT_REGISTRY_MAX`, `READ_CONTEXT_SHARED_MAX_ITEMS`, `READ_CONTEXT_SUMMARY_MAX_CHARS`, `READ_FILE_COMPACT_PIN_DISTINCT`, `READ_FILE_COMPACT_PIN_MAX_CHARS`, `READ_FILE_DEFAULT_MAX_CHARS`, `READ_FILE_HARD_MAX_CHARS`, `READ_FILE_LOOP_DISTINCT_SOFT_LIMIT`, `READ_FILE_LOOP_THRESHOLD`, `READ_FILE_OVERVIEW_HEAD_LINES`, `READ_FILE_SEARCH_MAX_MATCHES`, `RENDER_FRAME_ACTIVITY_INTERVAL_SECONDS`, `RENDER_FRAME_MAX_B64_CHARS`, `RENDER_FRAME_MAX_LINES`, `RENDER_FRAME_MAX_LINE_POINTS`, `RENDER_FRAME_MAX_POINTS`, `REPEATED_TOOL_LOOP_THRESHOLD`, `RETRY_RUNTIME_HINT_PREFIXES`, `REVIEWER_DEBUG_MODE_MAX_ROUNDS`, `RUNTIME_CONTROL_HINT_PREFIXES`, `RUN_COMPLETION_SUMMARY_ENABLED`, `SEMANTIC_CONFIDENCE_CHOICES`, `SESSION_DEFERRED_START_QUEUE_MAX`, `SESSION_HEARTBEAT_STALE_SECONDS`, `SESSION_SUBMIT_LOCK_TIMEOUT_SECONDS`, `SKILLS_VIRTUAL_PREFIX`, `SKILL_REFRESH_MIN_INTERVAL_SECONDS`, `SKILL_RUNTIME_CACHE_MAX_BYTES`, `SKILL_RUNTIME_CACHE_MAX_ENTRIES`, `STALL_ESCALATION_CONTEXT_MAX_CHARS`, `STALL_ESCALATION_MIN_LEVEL`, `STALL_PLAN_SYNTHESIS_MAX_TOKENS`, `STALL_SEVERITY_DECAY_ON_SUCCESS`, `STALL_SEVERITY_ESCALATION_THRESHOLD`, `STALL_SEVERITY_WEIGHT_BASH_READ_LOOP`, `STALL_SEVERITY_WEIGHT_FAULT`, `STALL_SEVERITY_WEIGHT_RECOVERY_RETRY`, `STALL_SEVERITY_WEIGHT_REPEATED_TOOL`, `STALL_SEVERITY_WEIGHT_WATCHDOG`, `TASK_COMPLEXITY_LEVELS`, `TASK_LEVEL_CHOICES`, `TASK_LEVEL_POLICIES`, `TASK_PHASE_ROUTING`, `TASK_PROFILE_TYPES`, `TASK_SCALE_PREFERENCES`, `THINKING_BUDGET_FORCE_RATIO`, `TOKEN_THRESHOLD`, `TRUNCATION_CONTINUATION_ECHO_CHARS`, `TRUNCATION_CONTINUATION_MAX_PASSES`, `TRUNCATION_CONTINUATION_MAX_TOKENS`, `TRUNCATION_CONTINUATION_TAIL_CHARS`, `TRUNCATION_LIVE_BUFFER_MAX_CHARS`, `TRUNCATION_OVERLAP_SCAN_CHARS`, `TRUNCATION_PAIR_SCAN_CHARS`, `VIDEO_EXTS`, `WATCHDOG_CONTEXT_NEAR_RATIO`, `WATCHDOG_CONTEXT_STALL_THRESHOLD`, `WATCHDOG_INTENT_NO_TOOL_THRESHOLD`, `WATCHDOG_INTENT_NO_TOOL_THRESHOLD_SINGLE`, `WATCHDOG_MAX_DECOMPOSE_STEPS`, `WATCHDOG_REPEAT_NO_TOOL_THRESHOLD`, `WATCHDOG_REPEAT_NO_TOOL_THRESHOLD_SINGLE`, `WATCHDOG_REPEAT_SIMILARITY_THRESHOLD`, `WATCHDOG_STATE_STALL_THRESHOLD`, `WATCHDOG_STEP_MAX_ATTEMPTS`, `_DEFAULT_TOOL_TIMEOUT`, `_SHELL_AUTO_CONFIRM_PATTERNS`, `_TOOL_TIMEOUT_MAP`; `config/paths.py`: `WORKDIR`; `config/settings.py`: `_detect_os_shell_instruction`, `_to_bool_like`, `backend_i18n_text`, `backend_role_label`, `default_multimodal_capabilities`, `extract_auto_task_level_ceiling_setting`, `infer_model_multimodal_capabilities`, `infer_user_complexity_value`, `looks_like_llm_config`, `max_task_complexity`, `merge_multimodal_capabilities`, `model_language_instruction`, `normalize_auto_task_level_ceiling`, `normalize_execution_mode`, `normalize_read_context_policy`, `normalize_task_complexity`, `normalize_ui_language`, `parse_capability_overrides`, `parse_llm_config_profiles`, `task_complexity_at_least`, `task_complexity_rank`; `llm/client.py`: `OllamaClient`, `OllamaError`; `llm/utils.py`: `complete_chat_endpoint`, `extract_base_url`, `is_openai_compat_provider`, `list_loaded_ollama_models`, `list_ollama_models`, `list_ollama_models_cached`, `probe_ollama_environment`, `resolve_ollama_model`, `split_thinking_content`, `strip_thinking_content`, `wake_ollama_model`; `rag/parsers.py`: `CodeContentParser`, `build_code_preview_rows`, `is_code_preview_candidate`, `normalize_rel_preview_path`, `preview_kind_for_path`; `skills/store.py`: `SkillStore`, `ensure_runtime_skills`; `utils/compress.py`: `compress_text_blob`, `decompress_text_blob`; `utils/crypto.py`: `CryptoBox`; `utils/errors.py`: `CircuitBreakerTriggered`, `EmptyActionError`; `utils/files.py`: `_normalize_external_js_url`, `_safe_js_filename`, `cache_external_js_url`, `ensure_offline_js_libs`, `is_external_js_src`, `load_offline_js_lib_index`, `match_offline_js_catalog_by_url`, `offline_js_lib_root`, `safe_path`, `try_read_text`; `utils/http.py`: `urlopen`; `utils/json_utils.py`: `TOOLS`, `TOOL_REQUIRED_ARGS`, `canonicalize_tool_name`, `extract_json_object_from_text`, `json_dumps`, `parse_json_object`, `parse_tool_arguments_with_error`, `repair_truncated_json_object`, `tool_def`; `utils/media.py`: `_convert_image_to_safe_format`, `guess_ext_from_mime`, `guess_mime_from_name`; `utils/misc.py`: `MAX_TIMEOUT_SECONDS`, `MIN_TIMEOUT_SECONDS`, `is_benign_socket_error`, `make_id`, `normalize_timeout_seconds`, `now_ts`, `sanitize_profile_id`; `utils/text.py`: `MAX_TOOL_OUTPUT`, `_fmt_export_ts`, `_html_esc`, `_text_to_minimal_pdf`, `extract_todo_rows_from_text`, `filter_runtime_noise_lines`, `make_numbered_diff`, `make_unified_diff`, `normalize_embedded_newlines`, `normalize_work_text`, `parse_front_matter`, `render_numbered_diff_text`, `split_structured_todo_content`, `split_todo_status_text`, `trim`
- Symbols:
  - `SessionState` (class, lines 13968-43580)

### `skills/store.py`

- Routed symbols: 26
- Cross-module imports: `config/constants.py`: `BUILTIN_CLAWHUB_SKILLS_VERSION`, `EMBEDDED_CLAWHUB_SKILLS_ARCHIVE_B64`, `EMBEDDED_SKILLS_ARCHIVE_B64`, `EMBEDDED_SKILLS_ARCHIVE_FILES`, `EMBEDDED_SKILLS_ARCHIVE_SHA256`, `SKILLS_EXTERNAL_MOUNT`, `SKILLS_VIRTUAL_PREFIX`, `SKILL_BODY_COMPACT_THRESHOLD_CHARS`, `SKILL_BODY_PREVIEW_CHARS`, `SKILL_DEFAULT_ATTACHMENT_GLOBS`, `SKILL_INLINE_ATTACHMENT_MAX_CHARS`, `SKILL_INLINE_ATTACHMENT_MAX_FILES`, `SKILL_PROMPT_MAX_CHARS`, `SKILL_PROMPT_MAX_ITEMS`, `SKILL_PROTOCOL_CLAWHUB`, `SKILL_PROTOCOL_HTTP_JSON`, `SKILL_PROTOCOL_LOCAL`, `SKILL_PROTOCOL_SPECS`, `SKILL_REFRESH_MIN_INTERVAL_SECONDS`, `SKILL_RESOURCE_MANIFEST_MAX_ITEMS`; `config/paths.py`: `WORKDIR`; `llm/utils.py`: `_is_http_url`; `utils/files.py`: `_render_offline_js_catalog_md`, `safe_path`, `try_read_text`; `utils/http.py`: `urlopen`; `utils/json_utils.py`: `json_dumps`, `parse_json_object`; `utils/misc.py`: `_meta_string_list`, `_module_exists`, `now_ts`; `utils/text.py`: `parse_front_matter`, `trim`
- Symbols:
  - `ensure_embedded_skills_at_root` (function, lines 6669-6721)
  - `ensure_embedded_skills` (function, lines 6724-6725)
  - `detect_upload_parser_capabilities` (function, lines 6733-6748)
  - `_render_cap_markdown` (function, lines 6750-6764)
  - `_write_text_if_changed` (function, lines 6766-6771)
  - `ensure_generated_document_skills` (function, lines 6773-6861)
  - `ensure_generated_image_coding_feedback_skill` (function, lines 6863-6962)
  - `_skill_knowledge_files` (function, lines 6964-6983)
  - `analyze_skill_building_knowledge` (function, lines 6985-7039)
  - `_sanitize_skill_slug` (function, lines 7041-7043)
  - `_build_skills_gen_skill_content` (function, lines 7045-7076)
  - `ensure_generated_skills_gen_skill` (function, lines 7078-7082)
  - `ensure_generated_execution_recovery_skill` (function, lines 7084-7162)
  - `ensure_generated_systematic_debugging_skill` (function, lines 7164-7436)
  - `ensure_generated_code_engineering_mastery_skill` (function, lines 7438-7556)
  - `ensure_generated_smart_file_navigation_skill` (function, lines 7558-7673)
  - `ensure_generated_html_frontend_report_skills` (function, lines 7675-7882)
  - `ensure_generated_deep_research_skills` (function, lines 7884-8152)
  - `ensure_generated_research_scientific_skills` (function, lines 8154-8790)
  - `ensure_generated_rag_mastery_skills` (function, lines 8796-9092)
  - `ensure_generated_multimodal_comprehension_skills` (function, lines 9098-9787)
  - `ensure_generated_runtime_skills_manifest` (function, lines 9790-9821)
  - `ensure_embedded_clawhub_skills` (function, lines 10079-10116)
  - `ensure_runtime_skills` (function, lines 10118-10133)
  - `_BUILTIN_SKILLS` (assignment, lines 10175-10263)
  - `SkillStore` (class, lines 10272-11566)

### `utils/compress.py`

- Routed symbols: 2
- Cross-module imports: none
- Symbols:
  - `compress_text_blob` (function, lines 3413-3418)
  - `decompress_text_blob` (function, lines 3420-3428)

### `utils/crypto.py`

- Routed symbols: 1
- Cross-module imports: `utils/json_utils.py`: `json_dumps`
- Symbols:
  - `CryptoBox` (class, lines 5017-5134)

### `utils/errors.py`

- Routed symbols: 2
- Cross-module imports: none
- Symbols:
  - `EmptyActionError` (class, lines 3802-3803)
  - `CircuitBreakerTriggered` (class, lines 3806-3807)

### `utils/files.py`

- Routed symbols: 25
- Cross-module imports: `config/constants.py`: `OFFLINE_JS_LIB_CATALOG`, `OFFLINE_JS_LIB_INDEX_FILE`, `OFFLINE_JS_LIB_README_FILE`; `config/paths.py`: `WORKDIR`; `utils/http.py`: `urlopen`; `utils/json_utils.py`: `json_dumps`; `utils/misc.py`: `now_ts`; `utils/text.py`: `trim`
- Symbols:
  - `_normalize_js_lib_asset_ref` (function, lines 1384-1397)
  - `_resolve_js_lib_asset_path` (function, lines 1400-1429)
  - `_discover_extra_js_lib_files` (function, lines 1432-1462)
  - `safe_path` (function, lines 2790-2799)
  - `_safe_js_filename` (function, lines 2801-2808)
  - `_sha256_bytes` (function, lines 2810-2811)
  - `_sha256_file` (function, lines 2813-2821)
  - `_download_http_bytes` (function, lines 2823-2831)
  - `offline_js_lib_root` (function, lines 2833-2834)
  - `_offline_js_entry_relative_path` (function, lines 2836-2840)
  - `_archive_member_relative_path` (function, lines 2842-2851)
  - `_path_size_bytes` (function, lines 2853-2868)
  - `_extract_archive_to_dir` (function, lines 2870-2910)
  - `_package_required_paths` (function, lines 2912-2918)
  - `_package_install_ready` (function, lines 2920-2928)
  - `_postprocess_offline_js_package` (function, lines 2930-2965)
  - `_ensure_offline_js_package` (function, lines 2967-3006)
  - `_render_offline_js_catalog_md` (function, lines 3008-3024)
  - `load_offline_js_lib_index` (function, lines 3026-3035)
  - `ensure_offline_js_libs` (function, lines 3037-3181)
  - `_normalize_external_js_url` (function, lines 3183-3187)
  - `is_external_js_src` (function, lines 3189-3191)
  - `match_offline_js_catalog_by_url` (function, lines 3193-3209)
  - `cache_external_js_url` (function, lines 3211-3243)
  - `try_read_text` (function, lines 5339-5347)

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
  - `json_dumps` (function, lines 2762-2763)
  - `parse_tool_arguments` (function, lines 3681-3690)
  - `repair_truncated_json_object` (function, lines 3692-3745)
  - `parse_tool_arguments_with_error` (function, lines 3747-3777)
  - `parse_json_object` (function, lines 4043-4048)
  - `extract_json_object_from_text` (function, lines 4050-4072)
  - `_json_default_copy` (function, lines 5349-5354)
  - `_read_json_file` (function, lines 5356-5376)
  - `_write_json_file` (function, lines 5378-5405)
  - `tool_def` (function, lines 13559-13571)
  - `TOOLS` (constant, lines 13573-13868)
  - `TOOL_REQUIRED_ARGS` (constant, lines 13870-13870)
  - `TOOL_SPEC_BY_NAME` (constant, lines 13871-13871)
  - `TOOL_NAME_FUZZY_MAP` (constant, lines 13883-13883)
  - `canonicalize_tool_name` (function, lines 13901-13912)

### `utils/media.py`

- Routed symbols: 3
- Cross-module imports: none
- Symbols:
  - `guess_mime_from_name` (function, lines 2602-2604)
  - `_convert_image_to_safe_format` (function, lines 2607-2624)
  - `guess_ext_from_mime` (function, lines 2627-2633)

### `utils/misc.py`

- Routed symbols: 19
- Cross-module imports: none
- Symbols:
  - `MIN_TIMEOUT_SECONDS` (constant, lines 374-374)
  - `MAX_TIMEOUT_SECONDS` (constant, lines 375-375)
  - `DEFAULT_TIMEOUT_SECONDS` (constant, lines 376-382)
  - `BENIGN_SOCKET_DEBUG_LOG_ENABLED` (constant, lines 512-518)
  - `BENIGN_SOCKET_LOG_INTERVAL_SECONDS` (constant, lines 519-519)
  - `now_ts` (function, lines 2635-2636)
  - `_benign_socket_log_lock` (assignment, lines 2639-2639)
  - `_benign_socket_log_state` (assignment, lines 2640-2640)
  - `is_benign_socket_error` (function, lines 2658-2676)
  - `_socket_error_code` (function, lines 2679-2688)
  - `_log_benign_socket_error_limited` (function, lines 2691-2725)
  - `swallow_benign_socket_error` (function, lines 2728-2732)
  - `normalize_timeout_seconds` (function, lines 2735-2748)
  - `detect_local_lan_ip` (function, lines 2750-2760)
  - `make_id` (function, lines 2765-2766)
  - `sanitize_profile_id` (function, lines 2768-2770)
  - `user_id_from_ip` (function, lines 5009-5015)
  - `_meta_string_list` (function, lines 5326-5337)
  - `_module_exists` (function, lines 6727-6731)

### `utils/text.py`

- Routed symbols: 23
- Cross-module imports: `config/constants.py`: `CODE_PREVIEW_DIFF_CONTEXT_LINES`, `CODE_PREVIEW_DIFF_MERGE_GAP`
- Symbols:
  - `MAX_TOOL_OUTPUT` (constant, lines 137-137)
  - `SOCKET_NOISE_LINE_PATTERNS` (constant, lines 506-511)
  - `filter_runtime_noise_lines` (function, lines 2643-2655)
  - `trim` (function, lines 3245-3247)
  - `_fmt_export_ts` (function, lines 3250-3258)
  - `_html_esc` (function, lines 3261-3262)
  - `_text_to_minimal_pdf` (function, lines 3265-3411)
  - `normalize_embedded_newlines` (function, lines 3430-3438)
  - `_map_todo_status_token` (function, lines 3441-3456)
  - `split_todo_status_text` (function, lines 3459-3514)
  - `extract_todo_rows_from_text` (function, lines 3517-3584)
  - `infer_todo_status_from_text` (function, lines 3587-3593)
  - `split_structured_todo_content` (function, lines 3596-3649)
  - `normalize_work_text` (function, lines 3652-3679)
  - `parse_front_matter` (function, lines 5136-5323)
  - `make_unified_diff` (function, lines 5407-5424)
  - `_skip_row` (function, lines 5426-5430)
  - `_row_is_hot` (function, lines 5433-5434)
  - `_hotspot_index` (function, lines 5437-5458)
  - `_compress_rows_keep_hotspot` (function, lines 5461-5508)
  - `_focused_diff_rows_from_opcodes` (function, lines 5511-5643)
  - `make_numbered_diff` (function, lines 5646-5676)
  - `render_numbered_diff_text` (function, lines 5678-5690)
