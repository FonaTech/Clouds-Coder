# Code_Structure Framework

## Overview

- Source file: `/Users/Fona/Downloads/Clouds_Coder/Clouds_Coder.py`
- Output directory: `/Users/Fona/Downloads/Clouds_Coder/Code_Structure`
- Generated modules: 31
- Top-level symbols: 714
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
│   ├── store.py
│   └── web_search.py
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
| `__main__.py` | 2 | `app/context.py`, `config/constants.py`, `config/paths.py`, `config/settings.py`, `llm/utils.py`, `server/handlers.py`, `skills/store.py`, `utils/files.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` |
| `agent/background.py` | 1 | `utils/misc.py`, `utils/text.py` |
| `agent/bus.py` | 1 | `config/constants.py`, `utils/crypto.py`, `utils/misc.py` |
| `agent/events.py` | 1 | — |
| `agent/tasks.py` | 1 | `utils/crypto.py`, `utils/json_utils.py`, `utils/misc.py` |
| `agent/todo.py` | 1 | `config/constants.py`, `config/settings.py`, `utils/misc.py`, `utils/text.py` |
| `agent/worktree.py` | 1 | `agent/tasks.py`, `config/constants.py`, `utils/crypto.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` |
| `app/context.py` | 1 | `config/constants.py`, `config/paths.py`, `config/settings.py`, `llm/client.py`, `llm/utils.py`, `rag/ingestion.py`, `rag/parsers.py`, `rag/store.py`, `session/manager.py`, `session/state.py`, `skills/store.py`, `utils/crypto.py`, `utils/files.py`, `utils/json_utils.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py` |
| `config/constants.py` | 420 | `utils/json_utils.py`, `utils/misc.py` |
| `config/paths.py` | 8 | `utils/text.py` |
| `config/settings.py` | 49 | `config/constants.py`, `config/paths.py`, `llm/utils.py`, `skills/store.py`, `utils/http.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` |
| `llm/client.py` | 2 | `config/constants.py`, `config/settings.py`, `llm/utils.py`, `utils/http.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` |
| `llm/utils.py` | 25 | `config/constants.py`, `utils/http.py`, `utils/json_utils.py`, `utils/text.py` |
| `rag/index.py` | 5 | `config/constants.py`, `rag/ingestion.py`, `rag/parsers.py`, `utils/misc.py`, `utils/text.py` |
| `rag/ingestion.py` | 12 | `config/constants.py`, `config/settings.py`, `rag/parsers.py`, `rag/store.py`, `session/state.py`, `utils/files.py`, `utils/json_utils.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py` |
| `rag/parsers.py` | 28 | `config/constants.py`, `rag/ingestion.py`, `utils/files.py`, `utils/json_utils.py`, `utils/media.py`, `utils/text.py` |
| `rag/store.py` | 7 | `config/constants.py`, `config/settings.py`, `rag/index.py`, `rag/ingestion.py`, `rag/parsers.py`, `skills/store.py`, `utils/files.py`, `utils/json_utils.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py` |
| `rag/web_search.py` | 15 | `config/constants.py`, `config/paths.py`, `utils/http.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` |
| `server/handlers.py` | 6 | `app/context.py`, `config/constants.py`, `config/paths.py`, `config/settings.py`, `llm/utils.py`, `rag/parsers.py`, `session/manager.py`, `session/state.py`, `skills/store.py`, `utils/files.py`, `utils/http.py`, `utils/json_utils.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py` |
| `session/manager.py` | 2 | `config/constants.py`, `config/paths.py`, `config/settings.py`, `llm/client.py`, `llm/utils.py`, `rag/store.py`, `session/state.py`, `utils/crypto.py`, `utils/files.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` |
| `session/state.py` | 1 | `agent/background.py`, `agent/bus.py`, `agent/events.py`, `agent/tasks.py`, `agent/todo.py`, `agent/worktree.py`, `config/constants.py`, `config/paths.py`, `config/settings.py`, `llm/client.py`, `llm/utils.py`, `rag/parsers.py`, `rag/web_search.py`, `skills/store.py`, `utils/compress.py`, `utils/crypto.py`, `utils/errors.py`, `utils/files.py`, `utils/http.py`, `utils/json_utils.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py` |
| `skills/store.py` | 27 | `config/constants.py`, `config/paths.py`, `llm/utils.py`, `utils/files.py`, `utils/http.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` |
| `utils/compress.py` | 2 | — |
| `utils/crypto.py` | 1 | `utils/json_utils.py` |
| `utils/errors.py` | 2 | — |
| `utils/files.py` | 25 | `config/constants.py`, `config/paths.py`, `utils/http.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` |
| `utils/http.py` | 4 | — |
| `utils/json_utils.py` | 17 | `config/constants.py`, `utils/text.py` |
| `utils/media.py` | 3 | — |
| `utils/misc.py` | 21 | — |
| `utils/text.py` | 23 | `config/constants.py` |

## Module Details

### `__main__.py`

- Routed symbols: 2
- Cross-module imports: `app/context.py`: `AppContext`; `config/constants.py`: `AGENT_MAX_OUTPUT_TOKENS`, `ARBITER_DEFAULT_MAX_TOKENS`, `ARBITER_DEFAULT_TEMPERATURE`, `ARBITER_DEFAULT_TIMEOUT_SECONDS`, `CODE_ADMIN_PORT_OFFSET`, `DEFAULT_AUTO_TASK_LEVEL_CEILING`, `DEFAULT_CONTEXT_TOKEN_LIMIT`, `DEFAULT_OLLAMA_BASE_URL`, `DEFAULT_OLLAMA_MODEL`, `DEFAULT_READ_CONTEXT_POLICY`, `DEFAULT_SHELL_COMMAND_TIMEOUT_SECONDS`, `DEFAULT_TOOL_MEMORY_POLICY`, `DEFAULT_UI_LANGUAGE`, `DEFAULT_UI_STYLE`, `DEFAULT_USER_MEMORY_MODE`, `DEFAULT_WEB_SEARCH_ENABLED`, `DEFAULT_WEB_UI_CONFIG`, `DEFAULT_WEB_UI_DIR`, `EXECUTION_MODE_SYNC`, `IDE_DEFAULT_PORT`, `LIVE_INPUT_DELAY_NORMAL_ROUNDS`, `LIVE_INPUT_DELAY_TOOL_ROUNDS`, `LIVE_INPUT_DELAY_WRITE_ROUNDS`, `LIVE_INPUT_MAX_INJECTIONS`, `LIVE_INPUT_REINJECT_INTERVAL`, `LIVE_INPUT_WEIGHT_BASE_DELAYED`, `LIVE_INPUT_WEIGHT_BASE_NORMAL`, `LIVE_INPUT_WEIGHT_STEP_DELAYED`, `LIVE_INPUT_WEIGHT_STEP_NORMAL`, `MAX_AGENT_ROUNDS`, `MAX_AGENT_ROUNDS_CAP`, `MAX_RUN_SECONDS`, `MAX_RUN_TIMEOUT_SECONDS`, `MAX_SHELL_COMMAND_TIMEOUT_SECONDS`, `MIN_AGENT_ROUNDS`, `MIN_CONTEXT_TOKEN_LIMIT`, `MIN_RUN_TIMEOUT_SECONDS`, `MIN_SHELL_COMMAND_TIMEOUT_SECONDS`, `OFFLINE_JS_LIB_CATALOG`, `RAG_ADMIN_PORT_OFFSET`, `RAG_INCLUDE_FILENAME_ENTITIES_DEFAULT`, `TOKEN_THRESHOLD`, `UI_LANGUAGE_LABELS`, `UI_STYLE_LABELS`, `USER_MEMORY_MODE_CHOICES`; `config/paths.py`: `LLM_CONFIG_PATH`, `REPO_ROOT`, `WORKDIR`; `config/settings.py`: `_to_bool_like`, `extract_auto_task_level_ceiling_setting`, `extract_context_token_limit_setting`, `extract_daily_session_limit_setting`, `extract_js_lib_download_setting`, `extract_read_context_policy_setting`, `extract_shell_command_timeout_setting`, `extract_show_upload_list_setting`, `extract_tool_memory_policy_setting`, `extract_ui_style_setting`, `extract_user_memory_mode_setting`, `extract_web_search_enabled_setting`, `load_llm_config_from_source`, `load_web_ui_config_file`, `normalize_auto_task_level_ceiling`, `normalize_execution_mode`, `normalize_read_context_policy`, `normalize_tool_memory_policy`, `normalize_ui_language`, `normalize_ui_style`, `normalize_user_memory_mode`, `parse_llm_config_profiles`, `resolve_optional_file_path`, `resolve_web_ui_dir_path`, `select_preferred_skills_root`; `llm/utils.py`: `list_ollama_models`; `server/handlers.py`: `AgentHTTPServer`, `CodeAdminHandler`, `Handler`, `IdeHandler`, `RagAdminHandler`, `SkillsHandler`; `skills/store.py`: `ensure_embedded_skills_at_root`, `ensure_runtime_skills`; `utils/files.py`: `ensure_offline_js_libs`; `utils/json_utils.py`: `TOOLS`, `filter_tool_specs_for_runtime`; `utils/misc.py`: `BENIGN_SOCKET_DEBUG_LOG_ENABLED`, `detect_local_lan_ip`, `normalize_timeout_seconds`, `now_ts`, `swallow_benign_socket_error`; `utils/text.py`: `trim`
- Symbols:
  - `main` (function, lines 81760-83065)
  - `_main_guard_83067` (main_guard, lines 83067-83068)

### `agent/background.py`

- Routed symbols: 1
- Cross-module imports: `utils/misc.py`: `make_id`, `now_ts`; `utils/text.py`: `trim`
- Symbols:
  - `BackgroundManager` (class, lines 13685-13765)

### `agent/bus.py`

- Routed symbols: 1
- Cross-module imports: `config/constants.py`: `VALID_MSG_TYPES`; `utils/crypto.py`: `CryptoBox`; `utils/misc.py`: `now_ts`
- Symbols:
  - `MessageBus` (class, lines 13767-13831)

### `agent/events.py`

- Routed symbols: 1
- Cross-module imports: none
- Symbols:
  - `EventHub` (class, lines 7705-7750)

### `agent/tasks.py`

- Routed symbols: 1
- Cross-module imports: `utils/crypto.py`: `CryptoBox`; `utils/json_utils.py`: `json_dumps`; `utils/misc.py`: `now_ts`
- Symbols:
  - `TaskManager` (class, lines 13557-13683)

### `agent/todo.py`

- Routed symbols: 1
- Cross-module imports: `config/constants.py`: `DEFAULT_UI_LANGUAGE`; `config/settings.py`: `backend_i18n_text`, `backend_role_label`, `normalize_ui_language`; `utils/misc.py`: `now_ts`; `utils/text.py`: `infer_todo_status_from_text`, `normalize_work_text`, `split_structured_todo_content`, `trim`
- Symbols:
  - `TodoManager` (class, lines 7752-8035)

### `agent/worktree.py`

- Routed symbols: 1
- Cross-module imports: `agent/tasks.py`: `TaskManager`; `config/constants.py`: `DANGEROUS_PATTERNS`; `utils/crypto.py`: `CryptoBox`; `utils/json_utils.py`: `json_dumps`; `utils/misc.py`: `now_ts`; `utils/text.py`: `trim`
- Symbols:
  - `WorktreeManager` (class, lines 13833-14048)

### `app/context.py`

- Routed symbols: 1
- Cross-module imports: `config/constants.py`: `AGENT_MAX_OUTPUT_TOKENS`, `APP_CSS`, `APP_JS`, `APP_TS`, `APP_VERSION`, `ARBITER_DEFAULT_MAX_TOKENS`, `ARBITER_DEFAULT_TEMPERATURE`, `ARBITER_DEFAULT_TIMEOUT_SECONDS`, `CODE_ADMIN_CSS`, `CODE_ADMIN_INDEX_HTML`, `CODE_ADMIN_JS`, `CODE_IMPORT_WORKER_COUNT`, `CODE_LIBRARY_DIRNAME`, `CODE_PARSE_TIMEOUT_SECONDS`, `DEFAULT_AUTO_TASK_LEVEL_CEILING`, `DEFAULT_CONTEXT_TOKEN_LIMIT`, `DEFAULT_READ_CONTEXT_POLICY`, `DEFAULT_REQUEST_TIMEOUT`, `DEFAULT_SHELL_COMMAND_TIMEOUT_SECONDS`, `DEFAULT_TOOL_MEMORY_POLICY`, `DEFAULT_UI_LANGUAGE`, `DEFAULT_UI_STYLE`, `DEFAULT_USER_MEMORY_MODE`, `DEFAULT_WEB_SEARCH_ENABLED`, `DEFAULT_WEB_UI_DIR`, `EXECUTION_MODE_SYNC`, `IDE_COMMAND_TIMEOUT_DEFAULT`, `IDE_CSS`, `IDE_DEFAULT_PORT`, `IDE_FILE_MAX_BYTES`, `IDE_INDEX_HTML`, `IDE_JS`, `IDE_TREE_DEFAULT_MAX_NODES`, `IDE_TREE_MAX_NODES`, `IDE_TREE_SKIP_DIRS`, `IDE_UPLOAD_MAX_BYTES`, `IDE_UPLOAD_MAX_ITEMS`, `IDE_UPLOAD_TOTAL_MAX_BYTES`, `INDEX_HTML`, `MAX_AGENT_ROUNDS`, `MAX_AGENT_ROUNDS_CAP`, `MAX_RUN_SECONDS`, `MAX_RUN_TIMEOUT_SECONDS`, `MAX_SHELL_COMMAND_TIMEOUT_SECONDS`, `MIN_AGENT_ROUNDS`, `MIN_CONTEXT_TOKEN_LIMIT`, `MIN_RUN_TIMEOUT_SECONDS`, `MIN_SHELL_COMMAND_TIMEOUT_SECONDS`, `RAG_ADMIN_CSS`, `RAG_ADMIN_INDEX_HTML`, `RAG_ADMIN_JS`, `RAG_CONTEXT_BUDGETS`, `RAG_DENSE_DEFAULT_ENABLED`, `RAG_EMBEDDING_MODE_VALUES`, `RAG_GRAPH_MAX_NODES`, `RAG_HIGH_RECALL_MIN_POOL`, `RAG_HIGH_RECALL_POOL_MULTIPLIER`, `RAG_IMPORT_WORKER_COUNT`, `RAG_INCLUDE_FILENAME_ENTITIES_DEFAULT`, `RAG_LIBRARY_DIRNAME`, `RAG_MAX_GLOBAL_COMMUNITIES`, `RAG_MAX_IMPORT_BATCH_BYTES`, `RAG_MAX_IMPORT_BATCH_ITEMS`, `RAG_MAX_IMPORT_FILES`, `RAG_MAX_QUERY_RESULTS`, `RAG_MIN_SYNTHESIS_SCORE`, `RAG_NO_EVIDENCE_MESSAGE`, `RAG_NO_EVIDENCE_THRESHOLD`, `RAG_PARSE_TIMEOUT_SECONDS`, `RAG_QUERY_CONTEXT_CHARS`, `RAG_RETRIEVAL_MAX_PER_DOC`, `RAG_SYNTHESIS_MAX_PER_DOC`, `RAG_WEAK_EVIDENCE_MESSAGE`, `RAG_WEAK_MATCH_SCORE_CAP`, `SESSION_HEARTBEAT_STALE_SECONDS`, `SESSION_WATCHDOG_INTERVAL_SECONDS`, `SKILLS_APP_JS`, `SKILLS_EXTRA_CSS`, `SKILLS_INDEX_HTML`, `SKILL_REFRESH_MIN_INTERVAL_SECONDS`, `TOKEN_THRESHOLD`, `WEB_UI_OPTIONAL_FILES`, `WEB_UI_REQUIRED_FILES`; `config/paths.py`: `LLM_CONFIG_PATH`, `REPO_ROOT`, `_migrate_legacy_runtime_roots`; `config/settings.py`: `_to_bool_like`, `default_multimodal_capabilities`, `extract_auto_task_level_ceiling_setting`, `extract_read_context_policy_setting`, `extract_tool_memory_policy_setting`, `extract_user_memory_mode_setting`, `extract_web_search_enabled_setting`, `infer_model_multimodal_capabilities`, `merge_multimodal_capabilities`, `model_language_instruction`, `normalize_auto_task_level_ceiling`, `normalize_execution_mode`, `normalize_read_context_policy`, `normalize_tool_memory_policy`, `normalize_ui_language`, `normalize_ui_style`, `normalize_user_memory_mode`, `parse_capability_overrides`, `parse_llm_config_profiles`, `resolve_optional_file_path`, `resolve_web_ui_dir_path`; `llm/client.py`: `OllamaClient`; `llm/utils.py`: `extract_base_url`, `list_ollama_models_cached`; `rag/ingestion.py`: `CodeIngestionService`, `RAGIngestionService`, `_rag_embed_batch`, `_rag_embed_text`, `_rag_mmr_select`, `_rag_query_variants`; `rag/parsers.py`: `CodeContentParser`, `RAGContentParser`, `normalize_rel_preview_path`, `preview_kind_for_path`; `rag/store.py`: `CodeLibraryStore`, `RAGLibraryStore`, `WikiStore`, `WorkflowMemoryStore`; `session/manager.py`: `SessionCreationLimitExceeded`, `SessionManager`; `session/state.py`: `SessionState`; `skills/store.py`: `SkillStore`, `_sanitize_skill_slug`, `analyze_skill_building_knowledge`, `ensure_runtime_skills`; `utils/crypto.py`: `CryptoBox`; `utils/files.py`: `_resolve_js_lib_asset_path`, `ensure_offline_js_libs`, `load_offline_js_lib_index`, `offline_js_lib_root`, `safe_path`, `try_read_text`; `utils/json_utils.py`: `TOOLS`, `extract_json_object_from_text`, `filter_tool_specs_for_runtime`, `json_dumps`, `parse_json_object`; `utils/media.py`: `guess_mime_from_name`; `utils/misc.py`: `DEFAULT_TIMEOUT_SECONDS`, `MAX_TIMEOUT_SECONDS`, `MIN_TIMEOUT_SECONDS`, `normalize_timeout_seconds`, `now_ts`; `utils/text.py`: `parse_front_matter`, `trim`
- Symbols:
  - `AppContext` (class, lines 75829-79859)

### `config/constants.py`

- Routed symbols: 420
- Cross-module imports: `utils/json_utils.py`: `TOOL_SPEC_BY_NAME`; `utils/misc.py`: `DEFAULT_TIMEOUT_SECONDS`
- Symbols:
  - `APP_VERSION` (constant, lines 63-63)
  - `DEFAULT_OLLAMA_BASE_URL` (constant, lines 64-64)
  - `DEFAULT_OLLAMA_MODEL` (constant, lines 65-65)
  - `LONG_OUTPUT_MODEL_PAGE_CHARS` (constant, lines 142-142)
  - `LONG_OUTPUT_UI_PAGE_CHARS` (constant, lines 143-143)
  - `LONG_OUTPUT_UI_PREVIEW_MAX_PAGES` (constant, lines 144-144)
  - `LONG_OUTPUT_LISTING_OFFLOAD_CHARS` (constant, lines 145-145)
  - `LONG_OUTPUT_READ_PAGE_LINES` (constant, lines 146-146)
  - `LONG_OUTPUT_READ_PAGE_MAX_CHARS` (constant, lines 147-147)
  - `LONG_OUTPUT_TEMP_MAX_FILES` (constant, lines 148-148)
  - `READ_FILE_DEFAULT_MAX_CHARS` (constant, lines 149-149)
  - `READ_FILE_HARD_MAX_CHARS` (constant, lines 150-150)
  - `READ_FILE_OVERVIEW_HEAD_LINES` (constant, lines 151-151)
  - `READ_FILE_SEARCH_MAX_MATCHES` (constant, lines 152-152)
  - `RAG_LIBRARY_DIRNAME` (constant, lines 154-154)
  - `RAG_ADMIN_PORT_OFFSET` (constant, lines 155-155)
  - `CODE_LIBRARY_DIRNAME` (constant, lines 156-156)
  - `CODE_ADMIN_PORT_OFFSET` (constant, lines 157-157)
  - `IDE_DEFAULT_PORT` (constant, lines 158-158)
  - `WEB_SEARCH_INDEX_DIRNAME` (constant, lines 159-159)
  - `DEFAULT_WEB_SEARCH_ENABLED` (constant, lines 160-160)
  - `USER_MEMORY_DIRNAME` (constant, lines 161-161)
  - `USER_MEMORY_DB_FILENAME` (constant, lines 162-162)
  - `USER_MEMORY_PROFILE_FILENAME` (constant, lines 163-163)
  - `USER_MEMORY_MODE_CHOICES` (constant, lines 164-164)
  - `DEFAULT_USER_MEMORY_MODE` (constant, lines 165-165)
  - `USER_MEMORY_WEAK_CAPSULE_CHARS` (constant, lines 166-166)
  - `USER_MEMORY_ON_CAPSULE_CHARS` (constant, lines 167-167)
  - `USER_MEMORY_MAX_SUMMARY_CHARS` (constant, lines 168-168)
  - `USER_MEMORY_QUERY_LIMIT` (constant, lines 169-169)
  - `USER_MEMORY_DECAY_HALFLIFE_DAYS` (constant, lines 170-170)
  - `USER_MEMORY_PROFILE_SCHEMA_VERSION` (constant, lines 171-171)
  - `AGENT_WEB_SEARCH_USER_AGENT` (constant, lines 172-172)
  - `AGENT_WEB_SEARCH_DEFAULT_MAX_RESULTS` (constant, lines 173-173)
  - `AGENT_WEB_SEARCH_DEFAULT_MAX_PAGES` (constant, lines 174-174)
  - `AGENT_WEB_SEARCH_HARD_MAX_PAGES` (constant, lines 175-175)
  - `AGENT_WEB_SEARCH_DEFAULT_DEPTH` (constant, lines 176-176)
  - `AGENT_WEB_SEARCH_HARD_DEPTH` (constant, lines 177-177)
  - `AGENT_WEB_SEARCH_FETCH_TIMEOUT` (constant, lines 178-178)
  - `AGENT_WEB_SEARCH_TOOL_SOFT_TIMEOUT` (constant, lines 179-179)
  - `AGENT_WEB_SEARCH_MAX_PAGE_BYTES` (constant, lines 180-180)
  - `AGENT_WEB_SEARCH_MAX_TEXT_CHARS` (constant, lines 181-181)
  - `WEB_SEARCH_CONTEXT_REGISTRY_MAX` (constant, lines 182-182)
  - `WEB_SEARCH_CONTEXT_PROMPT_MAX_ITEMS` (constant, lines 183-183)
  - `WEB_SEARCH_CONTEXT_PROMPT_MAX_CHARS` (constant, lines 184-184)
  - `WEB_SEARCH_CONTEXT_NODE_MAX` (constant, lines 185-185)
  - `WEB_SEARCH_CONTEXT_URL_MAX` (constant, lines 186-186)
  - `RAG_CHUNK_CHARS` (constant, lines 187-187)
  - `RAG_CHUNK_OVERLAP` (constant, lines 188-188)
  - `RAG_MAX_CHUNKS_PER_DOC` (constant, lines 189-189)
  - `CODE_CHUNK_CHARS` (constant, lines 190-190)
  - `CODE_CHUNK_OVERLAP` (constant, lines 191-191)
  - `CODE_MAX_CHUNKS_PER_DOC` (constant, lines 192-192)
  - `RAG_MAX_QUERY_RESULTS` (constant, lines 193-193)
  - `RAG_HIGH_RECALL_POOL_MULTIPLIER` (constant, lines 194-194)
  - `RAG_HIGH_RECALL_MIN_POOL` (constant, lines 195-195)
  - `RAG_RETRIEVAL_MAX_PER_DOC` (constant, lines 196-196)
  - `RAG_GRAPH_MAX_NODES` (constant, lines 197-197)
  - `RAG_TASK_HISTORY_LIMIT` (constant, lines 198-198)
  - `RAG_MODEL_MEDIA_MAX_BYTES` (constant, lines 199-199)
  - `RAG_MAX_IMPORT_FILES` (constant, lines 200-200)
  - `RAG_MAX_IMPORT_BATCH_ITEMS` (constant, lines 201-201)
  - `RAG_MAX_IMPORT_BATCH_BYTES` (constant, lines 202-202)
  - `RAG_PDF_IMAGE_LIMIT` (constant, lines 203-203)
  - `RAG_QUERY_CONTEXT_CHARS` (constant, lines 204-204)
  - `RAG_MAX_GLOBAL_COMMUNITIES` (constant, lines 205-205)
  - `RAG_MAX_COMMUNITY_MAP_SUPPORT` (constant, lines 206-206)
  - `RAG_INCLUDE_FILENAME_ENTITIES_DEFAULT` (constant, lines 207-207)
  - `RAG_DYNAMIC_NOISE_MIN_DOC_FREQ` (constant, lines 208-208)
  - `RAG_DYNAMIC_NOISE_MIN_COMMUNITY_FREQ` (constant, lines 209-209)
  - `RAG_DYNAMIC_NOISE_SOFT_DOC_RATIO` (constant, lines 210-210)
  - `RAG_DYNAMIC_NOISE_HARD_DOC_RATIO` (constant, lines 211-211)
  - `RAG_DYNAMIC_NOISE_SOFT_COMMUNITY_RATIO` (constant, lines 212-212)
  - `RAG_DYNAMIC_NOISE_HARD_COMMUNITY_RATIO` (constant, lines 213-213)
  - `RAG_MIN_SYNTHESIS_SCORE` (constant, lines 214-214)
  - `RAG_NO_EVIDENCE_THRESHOLD` (constant, lines 215-215)
  - `RAG_WEAK_MATCH_SCORE_CAP` (constant, lines 216-216)
  - `RAG_SYNTHESIS_MAX_PER_DOC` (constant, lines 217-217)
  - `RAG_WORKFLOW_ACCEPT_SCORE` (constant, lines 218-218)
  - `RAG_NO_EVIDENCE_MESSAGE` (constant, lines 219-219)
  - `RAG_CONTEXT_BUDGETS` (constant, lines 220-224)
  - `RAG_WEAK_EVIDENCE_MESSAGE` (constant, lines 225-225)
  - `RAG_DENSE_DEFAULT_ENABLED` (constant, lines 226-226)
  - `RAG_EMBEDDING_MODE_VALUES` (constant, lines 227-227)
  - `RAG_IMPORT_WORKER_COUNT` (constant, lines 228-231)
  - `CODE_IMPORT_WORKER_COUNT` (constant, lines 232-235)
  - `RAG_PARSE_TIMEOUT_SECONDS` (constant, lines 236-239)
  - `CODE_PARSE_TIMEOUT_SECONDS` (constant, lines 240-243)
  - `DEFAULT_CONTEXT_TOKEN_LIMIT` (constant, lines 244-244)
  - `TOKEN_THRESHOLD` (constant, lines 245-245)
  - `CONTEXT_AUTO_COMPACT_RESERVE_RATIO` (constant, lines 246-249)
  - `CONTEXT_ESTIMATE_SAFETY_MULTIPLIER` (constant, lines 250-253)
  - `CONTEXT_USAGE_CALIBRATION_MAX` (constant, lines 254-257)
  - `CONTEXT_ACTUAL_USAGE_RECENT_SECONDS` (constant, lines 258-261)
  - `LARGE_FILE_AUTO_PAGE_BYTES` (constant, lines 262-265)
  - `LARGE_FILE_AUTO_PAGE_LINES` (constant, lines 266-269)
  - `LARGE_SOURCE_UPLOAD_EXCERPT_CHARS` (constant, lines 270-273)
  - `CHAT_UPLOAD_PARSE_QUEUE_MAX` (constant, lines 274-277)
  - `CHAT_UPLOAD_PARSE_TIMEOUT_SECONDS` (constant, lines 278-281)
  - `CHAT_UPLOAD_INLINE_TEXT_BYTES` (constant, lines 282-285)
  - `CHAT_UPLOAD_PARSE_MAX_BYTES` (constant, lines 286-292)
  - `CHAT_UPLOAD_ZIP_ENTRY_MAX_BYTES` (constant, lines 293-299)
  - `CHAT_UPLOAD_TEXT_CONTEXT_CHARS` (constant, lines 300-303)
  - `CHAT_UPLOAD_PROMPT_MAX_FILES` (constant, lines 304-307)
  - `CHAT_UPLOAD_PROMPT_MAX_CHARS` (constant, lines 308-311)
  - `CHAT_UPLOAD_PROMPT_PER_FILE_CHARS` (constant, lines 312-315)
  - `CHAT_UPLOAD_FRONTEND_WAIT_MS` (constant, lines 316-319)
  - `CHAT_UPLOAD_AUTO_LIBRARY_INGEST` (constant, lines 320-323)
  - `CHAT_UPLOAD_INGEST_QUEUE_MAX` (constant, lines 324-327)
  - `SESSION_SUBMIT_LOCK_TIMEOUT_SECONDS` (constant, lines 328-331)
  - `SESSION_DEFERRED_START_QUEUE_MAX` (constant, lines 332-335)
  - `SESSION_WATCHDOG_INTERVAL_SECONDS` (constant, lines 336-339)
  - `SESSION_HEARTBEAT_STALE_SECONDS` (constant, lines 340-343)
  - `SESSION_LIST_DEFAULT_LIMIT` (constant, lines 344-347)
  - `IDLE_TIMEOUT` (constant, lines 348-348)
  - `POLL_INTERVAL` (constant, lines 349-349)
  - `SSE_HEARTBEAT_SECONDS` (constant, lines 350-350)
  - `MODEL_CALL_PROGRESS_DELAY` (constant, lines 351-351)
  - `MODEL_CALL_PROGRESS_INTERVAL` (constant, lines 352-352)
  - `RUN_COMPLETION_SUMMARY_ENABLED` (constant, lines 353-356)
  - `LLM_HTTP_RETRY_MAX_ATTEMPTS` (constant, lines 357-360)
  - `LLM_HTTP_RETRY_DELAY_SECONDS` (constant, lines 361-364)
  - `LLM_HTTP_RETRY_MAX_SECONDS` (constant, lines 365-368)
  - `LLM_HTTP_RETRY_404_ON_VLLM` (constant, lines 369-372)
  - `LLM_HTTP_RETRY_STATUSES` (constant, lines 373-373)
  - `MAX_AGENT_ROUNDS` (constant, lines 374-374)
  - `MIN_AGENT_ROUNDS` (constant, lines 375-375)
  - `MAX_AGENT_ROUNDS_CAP` (constant, lines 376-376)
  - `REPEATED_TOOL_LOOP_THRESHOLD` (constant, lines 377-377)
  - `BASH_READ_LOOP_THRESHOLD` (constant, lines 378-378)
  - `READ_FILE_LOOP_THRESHOLD` (constant, lines 379-379)
  - `READ_FILE_LOOP_DISTINCT_SOFT_LIMIT` (constant, lines 380-380)
  - `READ_FILE_COMPACT_PIN_DISTINCT` (constant, lines 381-381)
  - `READ_FILE_COMPACT_PIN_MAX_CHARS` (constant, lines 382-382)
  - `READ_CONTEXT_REGISTRY_MAX` (constant, lines 383-383)
  - `READ_CONTEXT_PROMPT_MAX_ITEMS` (constant, lines 384-384)
  - `READ_CONTEXT_PROMPT_MAX_CHARS` (constant, lines 385-385)
  - `READ_CONTEXT_SUMMARY_MAX_CHARS` (constant, lines 386-386)
  - `READ_CONTEXT_SHARED_MAX_ITEMS` (constant, lines 387-387)
  - `READ_CONTEXT_POLICY_CHOICES` (constant, lines 388-388)
  - `DEFAULT_READ_CONTEXT_POLICY` (constant, lines 389-389)
  - `TOOL_MEMORY_REGISTRY_MAX` (constant, lines 390-390)
  - `TOOL_MEMORY_PROMPT_MAX_ITEMS` (constant, lines 391-391)
  - `TOOL_MEMORY_PROMPT_MAX_CHARS` (constant, lines 392-392)
  - `TOOL_MEMORY_SUMMARY_MAX_CHARS` (constant, lines 393-393)
  - `TOOL_MEMORY_SHARED_MAX_ITEMS` (constant, lines 394-394)
  - `TOOL_MEMORY_COMPACT_PIN_DISTINCT` (constant, lines 395-395)
  - `TOOL_MEMORY_COMPACT_PIN_MAX_CHARS` (constant, lines 396-396)
  - `TOOL_MEMORY_POLICY_CHOICES` (constant, lines 397-397)
  - `DEFAULT_TOOL_MEMORY_POLICY` (constant, lines 398-398)
  - `DEFAULT_AUTO_TASK_LEVEL_CEILING` (constant, lines 399-399)
  - `HARD_BREAK_TOOL_ERROR_THRESHOLD` (constant, lines 400-400)
  - `HARD_BREAK_RECOVERY_ROUND_THRESHOLD` (constant, lines 401-401)
  - `FUSED_FAULT_BREAK_THRESHOLD` (constant, lines 402-402)
  - `STALL_SEVERITY_ESCALATION_THRESHOLD` (constant, lines 403-403)
  - `STALL_SEVERITY_WEIGHT_BASH_READ_LOOP` (constant, lines 404-404)
  - `STALL_SEVERITY_WEIGHT_REPEATED_TOOL` (constant, lines 405-405)
  - `STALL_SEVERITY_WEIGHT_FAULT` (constant, lines 406-406)
  - `STALL_SEVERITY_WEIGHT_RECOVERY_RETRY` (constant, lines 407-407)
  - `STALL_SEVERITY_WEIGHT_WATCHDOG` (constant, lines 408-408)
  - `STALL_SEVERITY_DECAY_ON_SUCCESS` (constant, lines 409-409)
  - `STALL_ESCALATION_MIN_LEVEL` (constant, lines 410-410)
  - `STALL_PLAN_SYNTHESIS_MAX_TOKENS` (constant, lines 411-411)
  - `STALL_ESCALATION_CONTEXT_MAX_CHARS` (constant, lines 412-412)
  - `MAX_RUN_SECONDS` (constant, lines 413-413)
  - `MIN_RUN_TIMEOUT_SECONDS` (constant, lines 414-414)
  - `MAX_RUN_TIMEOUT_SECONDS` (constant, lines 415-415)
  - `DEFAULT_REQUEST_TIMEOUT` (constant, lines 425-425)
  - `_SHELL_AUTO_CONFIRM_PATTERNS` (assignment, lines 428-441)
  - `MIN_SHELL_COMMAND_TIMEOUT_SECONDS` (constant, lines 442-442)
  - `MAX_SHELL_COMMAND_TIMEOUT_SECONDS` (constant, lines 443-443)
  - `DEFAULT_SHELL_COMMAND_TIMEOUT_SECONDS` (constant, lines 444-458)
  - `AUTO_CONTINUE_BUDGET_DEFAULT` (constant, lines 459-459)
  - `AGENT_MAX_OUTPUT_TOKENS` (constant, lines 460-460)
  - `OLLAMA_THINKING_TOOL_BUFFER` (constant, lines 461-461)
  - `WATCHDOG_INTENT_NO_TOOL_THRESHOLD` (constant, lines 462-462)
  - `WATCHDOG_REPEAT_NO_TOOL_THRESHOLD` (constant, lines 463-463)
  - `WATCHDOG_INTENT_NO_TOOL_THRESHOLD_SINGLE` (constant, lines 464-464)
  - `WATCHDOG_REPEAT_NO_TOOL_THRESHOLD_SINGLE` (constant, lines 465-465)
  - `WATCHDOG_STATE_STALL_THRESHOLD` (constant, lines 466-466)
  - `WATCHDOG_CONTEXT_STALL_THRESHOLD` (constant, lines 467-467)
  - `WATCHDOG_REPEAT_SIMILARITY_THRESHOLD` (constant, lines 468-468)
  - `WATCHDOG_CONTEXT_NEAR_RATIO` (constant, lines 469-469)
  - `WATCHDOG_MAX_DECOMPOSE_STEPS` (constant, lines 470-470)
  - `WATCHDOG_STEP_MAX_ATTEMPTS` (constant, lines 471-471)
  - `EMPTY_ACTION_MIN_CONTENT_CHARS` (constant, lines 472-472)
  - `EMPTY_ACTION_WAKEUP_RETRY_LIMIT` (constant, lines 473-473)
  - `THINKING_BUDGET_FORCE_RATIO` (constant, lines 474-474)
  - `_TOOL_TIMEOUT_MAP` (assignment, lines 476-493)
  - `_DEFAULT_TOOL_TIMEOUT` (assignment, lines 494-494)
  - `CONVERSATION_VISIBLE_TOOL_EVENTS` (constant, lines 495-505)
  - `PERSIST_ON_EVENT_TYPES` (constant, lines 506-520)
  - `PERSIST_EVENT_MIN_INTERVAL_SECONDS` (constant, lines 521-521)
  - `TRUNCATION_CONTINUATION_MAX_PASSES` (constant, lines 522-522)
  - `TRUNCATION_CONTINUATION_MAX_TOKENS` (constant, lines 523-523)
  - `TRUNCATION_CONTINUATION_TAIL_CHARS` (constant, lines 524-524)
  - `TRUNCATION_CONTINUATION_ECHO_CHARS` (constant, lines 525-525)
  - `TRUNCATION_OVERLAP_SCAN_CHARS` (constant, lines 526-526)
  - `TRUNCATION_PAIR_SCAN_CHARS` (constant, lines 527-527)
  - `TRUNCATION_LIVE_BUFFER_MAX_CHARS` (constant, lines 528-528)
  - `MIN_CONTEXT_TOKEN_LIMIT` (constant, lines 529-529)
  - `COMPACT_TIER1_PCT` (constant, lines 531-531)
  - `COMPACT_TIER2_PCT` (constant, lines 532-532)
  - `COMPACT_TIER3_PCT` (constant, lines 533-533)
  - `COMPACT_TIER1_ABS` (constant, lines 535-535)
  - `COMPACT_TIER2_ABS` (constant, lines 536-536)
  - `CONTEXT_COMPACT_INEFFECTIVE_COOLDOWN_SECONDS` (constant, lines 537-543)
  - `FILE_BUFFER_CONTENT_THRESHOLD` (constant, lines 545-545)
  - `FILE_BUFFER_MAX_FILES` (constant, lines 546-546)
  - `AGENT_MSG_LIMIT_TIER0` (constant, lines 548-548)
  - `AGENT_MSG_LIMIT_TIER1` (constant, lines 549-549)
  - `AGENT_MSG_LIMIT_TIER2` (constant, lines 550-550)
  - `AGENT_MSG_LIMIT_TIER3` (constant, lines 551-551)
  - `AGENT_CTX_LIMIT_TIER0` (constant, lines 552-552)
  - `AGENT_CTX_LIMIT_TIER1` (constant, lines 553-553)
  - `AGENT_CTX_LIMIT_TIER2` (constant, lines 554-554)
  - `AGENT_CTX_LIMIT_TIER3` (constant, lines 555-555)
  - `MANAGER_CTX_LIMIT_TIER0` (constant, lines 556-556)
  - `MANAGER_CTX_LIMIT_TIER1` (constant, lines 557-557)
  - `MANAGER_CTX_LIMIT_TIER2` (constant, lines 558-558)
  - `MANAGER_CTX_LIMIT_TIER3` (constant, lines 559-559)
  - `MAX_CONTEXT_ARCHIVE_SEGMENTS` (constant, lines 560-560)
  - `MODEL_OUTPUT_RETRY_TIMES` (constant, lines 561-561)
  - `ARBITER_TRIGGER_MIN_CONTENT_CHARS` (constant, lines 562-562)
  - `ARBITER_VALID_PLANNING_STREAK_LIMIT` (constant, lines 563-563)
  - `ARBITER_DEFAULT_TIMEOUT_SECONDS` (constant, lines 564-564)
  - `ARBITER_DEFAULT_MAX_TOKENS` (constant, lines 565-565)
  - `ARBITER_DEFAULT_TEMPERATURE` (constant, lines 566-566)
  - `LIVE_INPUT_DELAY_WRITE_ROUNDS` (constant, lines 567-567)
  - `LIVE_INPUT_DELAY_TOOL_ROUNDS` (constant, lines 568-568)
  - `LIVE_INPUT_DELAY_NORMAL_ROUNDS` (constant, lines 569-569)
  - `LIVE_INPUT_MAX_INJECTIONS` (constant, lines 570-570)
  - `LIVE_INPUT_REINJECT_INTERVAL` (constant, lines 571-571)
  - `LIVE_INPUT_WEIGHT_BASE_DELAYED` (constant, lines 572-572)
  - `LIVE_INPUT_WEIGHT_BASE_NORMAL` (constant, lines 573-573)
  - `LIVE_INPUT_WEIGHT_STEP_DELAYED` (constant, lines 574-574)
  - `LIVE_INPUT_WEIGHT_STEP_NORMAL` (constant, lines 575-575)
  - `FINAL_SUMMARY_MIN_CHARS` (constant, lines 590-590)
  - `FINAL_SUMMARY_STRICT_MIN_CHARS` (constant, lines 591-591)
  - `RUNTIME_CONTROL_HINT_PREFIXES` (constant, lines 592-609)
  - `RETRY_RUNTIME_HINT_PREFIXES` (constant, lines 610-624)
  - `EXECUTION_MODE_SINGLE` (constant, lines 625-625)
  - `EXECUTION_MODE_SEQUENTIAL` (constant, lines 626-626)
  - `EXECUTION_MODE_SYNC` (constant, lines 627-627)
  - `EXECUTION_MODE_CHOICES` (constant, lines 628-632)
  - `AGENT_ROLES` (constant, lines 633-633)
  - `AGENT_BUBBLE_ROLES` (constant, lines 634-634)
  - `AGENT_ROLE_LABELS` (constant, lines 635-641)
  - `AGENT_ROLE_BUBBLE_COLORS` (constant, lines 642-648)
  - `BLACKBOARD_STATUSES` (constant, lines 649-658)
  - `TASK_COMPLEXITY_LEVELS` (constant, lines 659-659)
  - `TASK_COMPLEXITY_RANKS` (constant, lines 660-665)
  - `TASK_PROFILE_TYPES` (constant, lines 666-672)
  - `TASK_LEVEL_CHOICES` (constant, lines 673-673)
  - `TASK_SCALE_PREFERENCES` (constant, lines 674-674)
  - `SEMANTIC_CONFIDENCE_CHOICES` (constant, lines 675-675)
  - `TASK_LEVEL_POLICIES` (constant, lines 676-722)
  - `MANAGER_ROUTE_TARGETS` (constant, lines 723-723)
  - `BLACKBOARD_MAX_LOG_ENTRIES` (constant, lines 724-724)
  - `BLACKBOARD_MAX_TEXT` (constant, lines 725-725)
  - `BLACKBOARD_MEMORY_SHORT_MAX` (constant, lines 726-726)
  - `BLACKBOARD_MEMORY_MID_MAX_STEPS` (constant, lines 727-727)
  - `BLACKBOARD_MEMORY_MID_ITEMS_PER_STEP` (constant, lines 728-728)
  - `BLACKBOARD_MEMORY_LONG_MAX` (constant, lines 729-729)
  - `BLACKBOARD_MEMORY_INDEX_MAX` (constant, lines 730-730)
  - `SKILL_REFRESH_MIN_INTERVAL_SECONDS` (constant, lines 731-731)
  - `SKILL_PROMPT_MAX_ITEMS` (constant, lines 732-732)
  - `SKILL_PROMPT_MAX_CHARS` (constant, lines 733-733)
  - `SKILL_RUNTIME_CACHE_MAX_ENTRIES` (constant, lines 734-734)
  - `SKILL_RUNTIME_CACHE_MAX_BYTES` (constant, lines 735-735)
  - `AUTO_SKILLS_ROOT_CANDIDATES` (constant, lines 736-736)
  - `SKILL_DEFAULT_ATTACHMENT_GLOBS` (constant, lines 737-767)
  - `SKILL_INLINE_ATTACHMENT_MAX_FILES` (constant, lines 768-768)
  - `SKILL_INLINE_ATTACHMENT_MAX_CHARS` (constant, lines 769-769)
  - `SKILL_RESOURCE_MANIFEST_MAX_ITEMS` (constant, lines 770-770)
  - `SKILL_BODY_COMPACT_THRESHOLD_CHARS` (constant, lines 771-771)
  - `SKILL_BODY_PREVIEW_CHARS` (constant, lines 772-772)
  - `SKILLS_VIRTUAL_PREFIX` (constant, lines 773-773)
  - `SKILLS_EXTERNAL_MOUNT` (constant, lines 774-774)
  - `PLAN_MODE_ENABLED_LEVELS` (constant, lines 775-775)
  - `PLAN_MODE_FORCED_LEVELS` (constant, lines 776-776)
  - `PLAN_MODE_USER_CHOICES` (constant, lines 777-777)
  - `TASK_PHASES` (constant, lines 779-779)
  - `TASK_PHASE_ROUTING` (constant, lines 780-787)
  - `COMPLEXITY_KEYWORDS` (constant, lines 789-794)
  - `USER_COMPLEXITY_SIMPLE_TOKENS` (constant, lines 795-799)
  - `USER_COMPLEXITY_MODERATE_TOKENS` (constant, lines 800-804)
  - `USER_COMPLEXITY_COMPLEX_TOKENS` (constant, lines 805-809)
  - `USER_COMPLEXITY_EXPERT_TOKENS` (constant, lines 810-814)
  - `PLAN_MODE_EXPLORER_MAX_ROUNDS` (constant, lines 815-815)
  - `PLAN_MODE_SYNTHESIS_MAX_ATTEMPTS` (constant, lines 816-816)
  - `REVIEWER_DEBUG_MODE_MAX_ROUNDS` (constant, lines 818-818)
  - `REVIEWER_DEBUG_TOOL_ALLOWLIST` (constant, lines 819-823)
  - `EXPLORER_STALL_THRESHOLD` (constant, lines 824-824)
  - `DEVELOPER_EDIT_STALL_THRESHOLD` (constant, lines 825-825)
  - `PLAN_MODE_MANAGER_SYNTHESIS_MAX_TOKENS` (constant, lines 826-826)
  - `PLAN_MODE_MAX_OPTIONS` (constant, lines 827-827)
  - `PLAN_FILE_RELATIVE_PATH` (constant, lines 828-828)
  - `PLAN_BUBBLE_MAX_CHARS` (constant, lines 829-829)
  - `PLAN_NOTICE_BODY_MAX_CHARS` (constant, lines 830-830)
  - `PLAN_MESSAGE_EVENT_MAX_CHARS` (constant, lines 831-831)
  - `PLAN_STEP_FULL_CONTENT_MAX_CHARS` (constant, lines 832-832)
  - `PLAN_MODE_RESEARCH_TOOL_ALLOWLIST` (constant, lines 833-837)
  - `FAILURE_LEDGER_MAX_FIXES` (constant, lines 838-838)
  - `FAILURE_LEDGER_MAX_COMPILE_ERRORS` (constant, lines 839-839)
  - `FAILURE_LEDGER_MAX_DELEGATIONS` (constant, lines 840-840)
  - `FAILURE_LEDGER_MAX_STALLS` (constant, lines 841-841)
  - `FAILURE_LEDGER_MAX_TOOL_FPS` (constant, lines 842-842)
  - `FAILURE_LEDGER_MAX_ERRORS` (constant, lines 843-843)
  - `ERROR_CATEGORY_DEFS` (constant, lines 846-883)
  - `CHECKPOINT_MAX_COUNT` (constant, lines 884-884)
  - `CHECKPOINT_INTERVAL_ROUNDS` (constant, lines 885-885)
  - `PERSISTED_ROUTES_MAX` (constant, lines 886-886)
  - `HTML_FRONTEND_REQUEST_KEYWORDS` (constant, lines 887-926)
  - `DEEP_RESEARCH_REQUEST_KEYWORDS` (constant, lines 927-949)
  - `DEEP_RESEARCH_RETRIEVAL_KEYWORDS` (constant, lines 950-969)
  - `DEEP_RESEARCH_TEXT_ONLY_HINT_KEYWORDS` (constant, lines 970-987)
  - `DANGEROUS_PATTERNS` (constant, lines 989-989)
  - `VALID_MSG_TYPES` (constant, lines 990-996)
  - `SUPPORTED_UI_LANGUAGES` (constant, lines 998-1003)
  - `UI_LANGUAGE_LABELS` (constant, lines 1004-1004)
  - `DEFAULT_UI_LANGUAGE` (constant, lines 1005-1005)
  - `UI_STYLE_CHOICES` (constant, lines 1006-1006)
  - `UI_STYLE_LABELS` (constant, lines 1007-1007)
  - `DEFAULT_UI_STYLE` (constant, lines 1008-1008)
  - `DEFAULT_WEB_UI_DIR` (constant, lines 1009-1009)
  - `DEFAULT_WEB_UI_CONFIG` (constant, lines 1010-1010)
  - `WEB_UI_REQUIRED_FILES` (constant, lines 1011-1018)
  - `WEB_UI_OPTIONAL_FILES` (constant, lines 1019-1019)
  - `IMAGE_EXTS` (constant, lines 1021-1034)
  - `IMAGE_FORMATS_NEED_CONVERSION` (constant, lines 1035-1035)
  - `IMAGE_SAFE_FORMATS` (constant, lines 1036-1036)
  - `AUDIO_EXTS` (constant, lines 1037-1047)
  - `VIDEO_EXTS` (constant, lines 1048-1058)
  - `CODE_PREVIEW_STAGE_MAX_BYTES` (constant, lines 1059-1059)
  - `CODE_PREVIEW_STAGE_MAX_ROWS` (constant, lines 1060-1060)
  - `CODE_PREVIEW_STAGE_MAX_PER_FILE` (constant, lines 1061-1061)
  - `CODE_PREVIEW_STAGE_MAX_TOTAL` (constant, lines 1062-1062)
  - `CODE_PREVIEW_DIFF_CONTEXT_LINES` (constant, lines 1063-1063)
  - `CODE_PREVIEW_DIFF_MERGE_GAP` (constant, lines 1064-1064)
  - `PREVIEW_DOWNLOAD_MAX_FILES` (constant, lines 1065-1065)
  - `PREVIEW_DOWNLOAD_MAX_BYTES` (constant, lines 1066-1066)
  - `FILES_TREE_DEFAULT_MAX_NODES` (constant, lines 1067-1067)
  - `FILES_TREE_DEFAULT_MAX_DEPTH` (constant, lines 1068-1068)
  - `FILES_TREE_SKIP_DIRS` (constant, lines 1069-1077)
  - `FILES_TREE_SKIP_REL_DIRS` (constant, lines 1078-1080)
  - `IDE_FILE_MAX_BYTES` (constant, lines 1081-1081)
  - `IDE_UPLOAD_MAX_BYTES` (constant, lines 1082-1082)
  - `IDE_UPLOAD_TOTAL_MAX_BYTES` (constant, lines 1083-1083)
  - `IDE_UPLOAD_MAX_ITEMS` (constant, lines 1084-1084)
  - `IDE_COMMAND_TIMEOUT_DEFAULT` (constant, lines 1085-1085)
  - `IDE_TREE_DEFAULT_MAX_NODES` (constant, lines 1086-1086)
  - `IDE_TREE_MAX_NODES` (constant, lines 1087-1087)
  - `IDE_TREE_SKIP_DIRS` (constant, lines 1088-1096)
  - `RENDER_FRAME_MAX_B64_CHARS` (constant, lines 1097-1097)
  - `RENDER_FRAME_MAX_POINTS` (constant, lines 1098-1098)
  - `RENDER_FRAME_MAX_LINES` (constant, lines 1099-1099)
  - `RENDER_FRAME_MAX_LINE_POINTS` (constant, lines 1100-1100)
  - `RENDER_FRAME_ACTIVITY_INTERVAL_SECONDS` (constant, lines 1101-1101)
  - `RAW_TOOLCALL_TEXT_FILTER_THRESHOLD` (constant, lines 1102-1102)
  - `ASSISTANT_TEXT_PERSIST_MAX_CHARS` (constant, lines 1103-1103)
  - `ASSISTANT_MESSAGE_EVENT_MAX_CHARS` (constant, lines 1104-1104)
  - `CODE_PREVIEW_EXTS` (constant, lines 1105-1230)
  - `CODE_PREVIEW_FILENAMES` (constant, lines 1231-1282)
  - `MEDIA_CAPABILITY_KEYS` (constant, lines 1283-1290)
  - `SAMPLE_IMAGE_PNG_B64` (constant, lines 1291-1294)
  - `SAMPLE_AUDIO_WAV_B64` (constant, lines 1295-1297)
  - `SAMPLE_VIDEO_MP4_B64` (constant, lines 1298-1300)
  - `OFFLINE_JS_LIB_CATALOG` (constant, lines 1302-1560)
  - `OFFLINE_JS_LIB_INDEX_FILE` (constant, lines 1561-1561)
  - `OFFLINE_JS_LIB_README_FILE` (constant, lines 1562-1562)
  - `BACKEND_I18N` (constant, lines 1748-1817)
  - `call_backend_i18n_en_update_l1819` (expression, lines 1819-1912)
  - `call_backend_i18n_zh_cn_update_l1913` (expression, lines 1913-2006)
  - `call_backend_i18n_zh_tw_update_l2007` (expression, lines 2007-2100)
  - `call_backend_i18n_ja_update_l2101` (expression, lines 2101-2194)
  - `OPENAI_COMPAT_PROVIDER_NAMES` (constant, lines 6078-6086)
  - `OPENAI_LIKE_PROVIDER_NAMES` (constant, lines 6088-6088)
  - `TABULAR_PREVIEW_EXTS` (constant, lines 7619-7619)
  - `EXCEL_PREVIEW_EXTS` (constant, lines 7620-7620)
  - `PRESENTATION_PREVIEW_EXTS` (constant, lines 7621-7621)
  - `DOCUMENT_PREVIEW_EXTS` (constant, lines 7622-7622)
  - `EMBEDDED_SKILLS_ARCHIVE_B64` (constant, lines 8037-8556)
  - `EMBEDDED_SKILLS_ARCHIVE_SHA256` (constant, lines 8557-8557)
  - `EMBEDDED_SKILLS_ARCHIVE_FILES` (constant, lines 8558-8581)
  - `BUILTIN_CLAWHUB_SKILLS_VERSION` (constant, lines 11803-11803)
  - `EMBEDDED_CLAWHUB_SKILLS_ARCHIVE_B64` (constant, lines 11805-12049)
  - `SKILL_PROTOCOL_LOCAL` (constant, lines 12116-12116)
  - `SKILL_PROTOCOL_CLAWHUB` (constant, lines 12117-12117)
  - `SKILL_PROTOCOL_HTTP_JSON` (constant, lines 12118-12118)
  - `SKILL_PROTOCOL_SPECS` (constant, lines 12120-12151)
  - `AGENT_TOOL_ALLOWLIST` (constant, lines 15965-16012)
  - `INDEX_HTML` (constant, lines 55840-56032)
  - `APP_CSS` (constant, lines 56034-56474)
  - `APP_JS` (constant, lines 56476-60695)
  - `APP_TS` (constant, lines 60697-60724)
  - `SKILLS_INDEX_HTML` (constant, lines 60726-60880)
  - `SKILLS_EXTRA_CSS` (constant, lines 60882-60977)
  - `SKILLS_APP_JS` (constant, lines 60979-61120)
  - `RAG_TERM_GROUPS` (constant, lines 61122-65754)
  - `RAG_RESEARCH_HINTS` (constant, lines 65755-65776)
  - `RAG_CODE_HINTS` (constant, lines 65777-65787)
  - `RAG_SHORT_TOKEN_ALLOWLIST` (constant, lines 65788-65803)
  - `RAG_EN_STOPWORDS` (constant, lines 65804-65876)
  - `RAG_ZH_STOPWORDS` (constant, lines 65877-65913)
  - `RAG_GENERIC_ENTITY_TERMS_EN` (constant, lines 65914-65992)
  - `RAG_GENERIC_ENTITY_TERMS_ZH` (constant, lines 65993-66035)
  - `RAG_STRUCTURAL_ENTITY_PATTERNS` (constant, lines 66036-66054)
  - `CODE_LIBRARY_IGNORED_DIRS` (constant, lines 66747-66752)
  - `CODE_LIBRARY_LANGUAGE_BY_EXT` (constant, lines 66753-66809)
  - `CODE_LIBRARY_SPECIAL_FILENAMES` (constant, lines 66810-66816)
  - `RAG_ADMIN_INDEX_HTML` (constant, lines 73396-73569)
  - `RAG_ADMIN_CSS` (constant, lines 73571-73661)
  - `RAG_ADMIN_JS` (constant, lines 73663-75426)
  - `CODE_ADMIN_INDEX_HTML` (constant, lines 75428-75439)
  - `CODE_ADMIN_CSS` (constant, lines 75440-75470)
  - `CODE_ADMIN_JS` (constant, lines 75471-75475)
  - `IDE_INDEX_HTML` (constant, lines 75477-75556)
  - `IDE_CSS` (constant, lines 75558-75624)
  - `IDE_JS` (constant, lines 75626-75818)

### `config/paths.py`

- Routed symbols: 8
- Cross-module imports: `utils/text.py`: `trim`
- Symbols:
  - `SCRIPT_DIR` (constant, lines 66-66)
  - `_resolve_default_agent_workdir` (function, lines 102-106)
  - `_migrate_legacy_runtime_roots` (function, lines 108-136)
  - `WORKDIR` (constant, lines 138-138)
  - `CODES_ROOT` (constant, lines 139-139)
  - `LLM_CONFIG_PATH` (constant, lines 140-140)
  - `detect_repo_root` (function, lines 3225-3239)
  - `REPO_ROOT` (constant, lines 3241-3241)

### `config/settings.py`

- Routed symbols: 49
- Cross-module imports: `config/constants.py`: `AUTO_SKILLS_ROOT_CANDIDATES`, `BACKEND_I18N`, `DEFAULT_AUTO_TASK_LEVEL_CEILING`, `DEFAULT_READ_CONTEXT_POLICY`, `DEFAULT_REQUEST_TIMEOUT`, `DEFAULT_SHELL_COMMAND_TIMEOUT_SECONDS`, `DEFAULT_TOOL_MEMORY_POLICY`, `DEFAULT_UI_LANGUAGE`, `DEFAULT_UI_STYLE`, `DEFAULT_USER_MEMORY_MODE`, `DEFAULT_WEB_SEARCH_ENABLED`, `DEFAULT_WEB_UI_CONFIG`, `DEFAULT_WEB_UI_DIR`, `EXECUTION_MODE_CHOICES`, `EXECUTION_MODE_SEQUENTIAL`, `EXECUTION_MODE_SINGLE`, `EXECUTION_MODE_SYNC`, `MAX_SHELL_COMMAND_TIMEOUT_SECONDS`, `MEDIA_CAPABILITY_KEYS`, `MIN_SHELL_COMMAND_TIMEOUT_SECONDS`, `READ_CONTEXT_POLICY_CHOICES`, `SUPPORTED_UI_LANGUAGES`, `TASK_COMPLEXITY_LEVELS`, `TASK_COMPLEXITY_RANKS`, `TASK_LEVEL_CHOICES`, `UI_LANGUAGE_LABELS`, `UI_STYLE_CHOICES`, `USER_COMPLEXITY_COMPLEX_TOKENS`, `USER_COMPLEXITY_EXPERT_TOKENS`, `USER_COMPLEXITY_MODERATE_TOKENS`, `USER_COMPLEXITY_SIMPLE_TOKENS`, `USER_MEMORY_MODE_CHOICES`; `config/paths.py`: `WORKDIR`; `llm/utils.py`: `_is_http_url`, `_resolve_local_path`, `complete_chat_endpoint`, `extract_base_url`, `is_openai_like_provider`, `normalize_openai_compat_provider_name`, `strip_thinking_content`; `skills/store.py`: `ensure_embedded_skills`; `utils/http.py`: `urlopen`; `utils/json_utils.py`: `TOOLS`, `filter_tool_specs_for_runtime`, `parse_json_object`; `utils/misc.py`: `MAX_TIMEOUT_SECONDS`, `MIN_TIMEOUT_SECONDS`, `detect_local_lan_ip_cached`, `normalize_timeout_seconds`, `now_ts`, `sanitize_profile_id`; `utils/text.py`: `trim`
- Symbols:
  - `normalize_ui_language` (function, lines 1646-1668)
  - `normalize_ui_style` (function, lines 1671-1688)
  - `supported_ui_languages_payload` (function, lines 1691-1692)
  - `normalize_execution_mode` (function, lines 1695-1714)
  - `model_language_instruction` (function, lines 1717-1745)
  - `backend_i18n_text` (function, lines 2197-2207)
  - `backend_role_label` (function, lines 2210-2214)
  - `_detect_os_shell_instruction` (function, lines 2217-2256)
  - `resolve_web_ui_dir_path` (function, lines 2258-2265)
  - `resolve_optional_file_path` (function, lines 2268-2275)
  - `resolve_skills_root_path` (function, lines 2278-2285)
  - `_count_skill_markdown_files` (function, lines 2288-2299)
  - `select_preferred_skills_root` (function, lines 2302-2336)
  - `load_web_ui_config_file` (function, lines 2339-2353)
  - `extract_show_upload_list_setting` (function, lines 2356-2370)
  - `extract_ui_style_setting` (function, lines 2373-2387)
  - `extract_js_lib_download_setting` (function, lines 2390-2409)
  - `extract_daily_session_limit_setting` (function, lines 2412-2455)
  - `extract_shell_command_timeout_setting` (function, lines 2458-2504)
  - `extract_context_token_limit_setting` (function, lines 2507-2539)
  - `normalize_auto_task_level_ceiling` (function, lines 2542-2561)
  - `extract_auto_task_level_ceiling_setting` (function, lines 2564-2591)
  - `normalize_read_context_policy` (function, lines 2594-2612)
  - `normalize_tool_memory_policy` (function, lines 2615-2616)
  - `extract_read_context_policy_setting` (function, lines 2619-2640)
  - `extract_tool_memory_policy_setting` (function, lines 2643-2664)
  - `default_multimodal_capabilities` (function, lines 2673-2681)
  - `_to_bool_like` (function, lines 2684-2694)
  - `extract_web_search_enabled_setting` (function, lines 2697-2707)
  - `normalize_user_memory_mode` (function, lines 2710-2738)
  - `user_memory_enabled_from_mode` (function, lines 2741-2742)
  - `extract_user_memory_mode_setting` (function, lines 2745-2782)
  - `set_web_search_enabled_on_runtime` (function, lines 2785-2798)
  - `infer_model_multimodal_capabilities` (function, lines 2801-2845)
  - `parse_capability_overrides` (function, lines 2848-2885)
  - `merge_multimodal_capabilities` (function, lines 2888-2895)
  - `parse_media_endpoints` (function, lines 2898-2912)
  - `extract_runtime_region_hint_setting` (function, lines 3091-3115)
  - `extract_runtime_timezone_hint_setting` (function, lines 3117-3133)
  - `runtime_environment_context_snapshot` (function, lines 3135-3183)
  - `runtime_environment_context_block` (function, lines 3185-3213)
  - `infer_user_complexity_value` (function, lines 5996-6012)
  - `normalize_task_complexity` (function, lines 6014-6042)
  - `task_complexity_rank` (function, lines 6044-6045)
  - `task_complexity_at_least` (function, lines 6047-6048)
  - `max_task_complexity` (function, lines 6050-6059)
  - `load_llm_config_from_source` (function, lines 6210-6244)
  - `parse_llm_config_profiles` (function, lines 6246-6832)
  - `looks_like_llm_config` (function, lines 6834-6908)

### `llm/client.py`

- Routed symbols: 2
- Cross-module imports: `config/constants.py`: `DEFAULT_REQUEST_TIMEOUT`, `LLM_HTTP_RETRY_404_ON_VLLM`, `LLM_HTTP_RETRY_DELAY_SECONDS`, `LLM_HTTP_RETRY_MAX_ATTEMPTS`, `LLM_HTTP_RETRY_MAX_SECONDS`, `LLM_HTTP_RETRY_STATUSES`, `OLLAMA_THINKING_TOOL_BUFFER`, `SAMPLE_AUDIO_WAV_B64`, `SAMPLE_IMAGE_PNG_B64`, `SAMPLE_VIDEO_MP4_B64`; `config/settings.py`: `default_multimodal_capabilities`, `infer_model_multimodal_capabilities`, `merge_multimodal_capabilities`, `parse_capability_overrides`, `parse_media_endpoints`; `llm/utils.py`: `complete_chat_endpoint`, `is_openai_compat_provider`, `is_openai_like_provider`, `normalize_openai_compat_provider_name`, `split_thinking_content`; `utils/http.py`: `urlopen`; `utils/json_utils.py`: `canonicalize_tool_name`, `json_dumps`, `parse_json_object`, `parse_tool_arguments`, `parse_tool_arguments_with_error`; `utils/misc.py`: `MAX_TIMEOUT_SECONDS`, `MIN_TIMEOUT_SECONDS`, `make_id`, `normalize_timeout_seconds`, `now_ts`; `utils/text.py`: `trim`
- Symbols:
  - `OllamaError` (class, lines 14050-14070)
  - `OllamaClient` (class, lines 14072-15539)

### `llm/utils.py`

- Routed symbols: 25
- Cross-module imports: `config/constants.py`: `OPENAI_COMPAT_PROVIDER_NAMES`, `OPENAI_LIKE_PROVIDER_NAMES`; `utils/http.py`: `urlopen`; `utils/json_utils.py`: `json_dumps`, `parse_json_object`; `utils/text.py`: `trim`
- Symbols:
  - `probe_ollama_environment` (function, lines 5680-5693)
  - `list_ollama_models` (function, lines 5695-5697)
  - `_OLLAMA_TAG_CACHE_LOCK` (assignment, lines 5699-5699)
  - `_OLLAMA_TAG_CACHE` (assignment, lines 5700-5700)
  - `list_ollama_models_cached` (function, lines 5710-5747)
  - `resolve_ollama_model` (function, lines 5749-5759)
  - `infer_thinking_model` (function, lines 5761-5763)
  - `split_thinking_content` (function, lines 5765-5808)
  - `strip_thinking_content` (function, lines 5810-5811)
  - `check_ollama_model_ready` (function, lines 5813-5837)
  - `list_loaded_ollama_models` (function, lines 5839-5852)
  - `wake_ollama_model` (function, lines 5854-5884)
  - `try_pull_ollama_model` (function, lines 5886-5904)
  - `ordered_model_candidates` (function, lines 5906-5924)
  - `pick_working_ollama_model` (function, lines 5926-5942)
  - `extract_base_url` (function, lines 5975-5983)
  - `complete_chat_endpoint` (function, lines 5985-5994)
  - `normalize_openai_compat_provider_name` (function, lines 6061-6076)
  - `is_openai_compat_provider` (function, lines 6090-6091)
  - `is_openai_like_provider` (function, lines 6093-6094)
  - `openai_compat_probe_headers` (function, lines 6096-6107)
  - `openai_compat_model_list_urls` (function, lines 6109-6141)
  - `extract_openai_compat_model_ids` (function, lines 6143-6176)
  - `_is_http_url` (function, lines 6185-6190)
  - `_resolve_local_path` (function, lines 6192-6208)

### `rag/index.py`

- Routed symbols: 5
- Cross-module imports: `config/constants.py`: `RAG_DYNAMIC_NOISE_HARD_COMMUNITY_RATIO`, `RAG_DYNAMIC_NOISE_HARD_DOC_RATIO`, `RAG_DYNAMIC_NOISE_MIN_COMMUNITY_FREQ`, `RAG_DYNAMIC_NOISE_MIN_DOC_FREQ`, `RAG_DYNAMIC_NOISE_SOFT_COMMUNITY_RATIO`, `RAG_DYNAMIC_NOISE_SOFT_DOC_RATIO`, `RAG_EN_STOPWORDS`, `RAG_GRAPH_MAX_NODES`, `RAG_INCLUDE_FILENAME_ENTITIES_DEFAULT`, `RAG_MAX_COMMUNITY_MAP_SUPPORT`, `RAG_MAX_GLOBAL_COMMUNITIES`, `RAG_MAX_QUERY_RESULTS`, `RAG_MIN_SYNTHESIS_SCORE`, `RAG_WEAK_MATCH_SCORE_CAP`; `rag/ingestion.py`: `_rag_focused_excerpt`, `_rag_mmr_select`, `_rag_window_for_query`; `rag/parsers.py`: `_code_is_test_path`, `_rag_apply_filename_entity_policy`, `_rag_choose_community`, `_rag_classify_document`, `_rag_expand_tokens`, `_rag_extract_entities`, `_rag_filter_entities`, `_rag_tokenize`; `utils/misc.py`: `now_ts`; `utils/text.py`: `trim`
- Symbols:
  - `_code_module_name` (function, lines 66843-66857)
  - `_code_choose_community` (function, lines 66860-66867)
  - `_code_query_terms` (function, lines 66870-66882)
  - `TFGraphIDFIndex` (class, lines 67935-69501)
  - `CodeGraphIndex` (class, lines 72575-73040)

### `rag/ingestion.py`

- Routed symbols: 12
- Cross-module imports: `config/constants.py`: `CODE_IMPORT_WORKER_COUNT`, `CODE_LIBRARY_IGNORED_DIRS`, `CODE_PARSE_TIMEOUT_SECONDS`, `RAG_IMPORT_WORKER_COUNT`, `RAG_MAX_IMPORT_BATCH_ITEMS`, `RAG_MAX_IMPORT_FILES`, `RAG_MODEL_MEDIA_MAX_BYTES`, `RAG_PARSE_TIMEOUT_SECONDS`, `RAG_PDF_IMAGE_LIMIT`, `RAG_RETRIEVAL_MAX_PER_DOC`; `config/settings.py`: `default_multimodal_capabilities`; `rag/parsers.py`: `CodeContentParser`, `RAGContentParser`, `_rag_expand_tokens`, `_rag_extract_entities`, `_rag_is_noise_token`, `_rag_safe_name`, `_rag_tokenize`; `rag/store.py`: `CodeLibraryStore`, `RAGLibraryStore`, `WikiStore`; `session/state.py`: `SessionState`; `utils/files.py`: `try_read_text`; `utils/json_utils.py`: `_read_json_file`, `_write_json_file`, `parse_json_object`; `utils/media.py`: `guess_mime_from_name`; `utils/misc.py`: `make_id`, `now_ts`; `utils/text.py`: `trim`
- Symbols:
  - `_rag_trigram_set` (function, lines 66267-66272)
  - `_rag_jaccard_sim` (function, lines 66275-66282)
  - `_rag_mmr_select` (function, lines 66285-66332)
  - `_rag_embed_text` (function, lines 66469-66490)
  - `_rag_embed_batch` (function, lines 66493-66499)
  - `_rag_window_for_query` (function, lines 66502-66514)
  - `_rag_focused_excerpt` (function, lines 66517-66557)
  - `_rag_query_variants` (function, lines 66560-66597)
  - `_rag_parse_segments` (function, lines 66600-66660)
  - `_rag_parse_file_worker` (function, lines 71679-71693)
  - `RAGIngestionService` (class, lines 71696-72572)
  - `CodeIngestionService` (class, lines 73309-73394)

### `rag/parsers.py`

- Routed symbols: 28
- Cross-module imports: `config/constants.py`: `AUDIO_EXTS`, `CODE_CHUNK_CHARS`, `CODE_CHUNK_OVERLAP`, `CODE_LIBRARY_LANGUAGE_BY_EXT`, `CODE_LIBRARY_SPECIAL_FILENAMES`, `CODE_MAX_CHUNKS_PER_DOC`, `CODE_PREVIEW_DIFF_CONTEXT_LINES`, `CODE_PREVIEW_DIFF_MERGE_GAP`, `CODE_PREVIEW_EXTS`, `CODE_PREVIEW_FILENAMES`, `CODE_PREVIEW_STAGE_MAX_ROWS`, `DOCUMENT_PREVIEW_EXTS`, `EXCEL_PREVIEW_EXTS`, `IMAGE_EXTS`, `PRESENTATION_PREVIEW_EXTS`, `RAG_CHUNK_CHARS`, `RAG_CHUNK_OVERLAP`, `RAG_CODE_HINTS`, `RAG_EN_STOPWORDS`, `RAG_GENERIC_ENTITY_TERMS_EN`, `RAG_GENERIC_ENTITY_TERMS_ZH`, `RAG_INCLUDE_FILENAME_ENTITIES_DEFAULT`, `RAG_MAX_CHUNKS_PER_DOC`, `RAG_PDF_IMAGE_LIMIT`, `RAG_RESEARCH_HINTS`, `RAG_SHORT_TOKEN_ALLOWLIST`, `RAG_STRUCTURAL_ENTITY_PATTERNS`, `RAG_TERM_GROUPS`, `RAG_ZH_STOPWORDS`, `TABULAR_PREVIEW_EXTS`, `VIDEO_EXTS`; `rag/ingestion.py`: `_rag_parse_segments`; `utils/files.py`: `_sha256_bytes`, `_sha256_file`; `utils/json_utils.py`: `parse_json_object`; `utils/media.py`: `guess_mime_from_name`; `utils/text.py`: `_focused_diff_rows_from_opcodes`, `_skip_row`, `trim`
- Symbols:
  - `normalize_rel_preview_path` (function, lines 7594-7605)
  - `is_code_preview_candidate` (function, lines 7608-7616)
  - `preview_kind_for_path` (function, lines 7625-7654)
  - `build_code_preview_rows` (function, lines 7657-7703)
  - `_rag_safe_name` (function, lines 66066-66069)
  - `_rag_detect_language` (function, lines 66072-66086)
  - `_rag_cjk_ngrams` (function, lines 66089-66101)
  - `_rag_is_noise_token` (function, lines 66104-66123)
  - `_rag_entity_allowed` (function, lines 66126-66138)
  - `_rag_filter_entities` (function, lines 66141-66155)
  - `_rag_filename_entity_aliases` (function, lines 66158-66191)
  - `_rag_apply_filename_entity_policy` (function, lines 66194-66224)
  - `_rag_choose_community` (function, lines 66227-66264)
  - `_rag_tokenize` (function, lines 66335-66386)
  - `_rag_expand_tokens` (function, lines 66389-66410)
  - `_rag_extract_entities` (function, lines 66413-66429)
  - `_rag_classify_document` (function, lines 66432-66466)
  - `_rag_chunk_text` (function, lines 66663-66742)
  - `_code_language_from_name` (function, lines 66819-66835)
  - `_code_is_test_path` (function, lines 66838-66840)
  - `_CallCollector` (class, lines 66885-66897)
  - `_ALGO_COMPLEXITY_RE` (assignment, lines 66900-66900)
  - `_ALGO_STEP_RE` (assignment, lines 66901-66901)
  - `_ALGO_MATH_VARS` (assignment, lines 66902-66902)
  - `_ALGO_DOC_KEYWORDS` (assignment, lines 66903-66903)
  - `_detect_algo_chunk` (function, lines 66906-66929)
  - `CodeContentParser` (class, lines 66932-67422)
  - `RAGContentParser` (class, lines 67425-67932)

### `rag/store.py`

- Routed symbols: 7
- Cross-module imports: `config/constants.py`: `CODE_CHUNK_CHARS`, `CODE_CHUNK_OVERLAP`, `CODE_MAX_CHUNKS_PER_DOC`, `DEFAULT_UI_LANGUAGE`, `EXECUTION_MODE_SYNC`, `RAG_INCLUDE_FILENAME_ENTITIES_DEFAULT`, `RAG_MAX_QUERY_RESULTS`, `RAG_RETRIEVAL_MAX_PER_DOC`, `RAG_TASK_HISTORY_LIMIT`, `RAG_WEAK_MATCH_SCORE_CAP`, `RAG_WORKFLOW_ACCEPT_SCORE`, `USER_MEMORY_DB_FILENAME`, `USER_MEMORY_DECAY_HALFLIFE_DAYS`, `USER_MEMORY_DIRNAME`, `USER_MEMORY_MAX_SUMMARY_CHARS`, `USER_MEMORY_ON_CAPSULE_CHARS`, `USER_MEMORY_PROFILE_FILENAME`, `USER_MEMORY_PROFILE_SCHEMA_VERSION`, `USER_MEMORY_QUERY_LIMIT`, `USER_MEMORY_WEAK_CAPSULE_CHARS`; `config/settings.py`: `normalize_execution_mode`, `normalize_ui_language`, `normalize_user_memory_mode`; `rag/index.py`: `CodeGraphIndex`, `TFGraphIDFIndex`, `_code_choose_community`, `_code_module_name`; `rag/ingestion.py`: `_rag_focused_excerpt`, `_rag_mmr_select`, `_rag_window_for_query`; `rag/parsers.py`: `_code_is_test_path`, `_rag_apply_filename_entity_policy`, `_rag_choose_community`, `_rag_chunk_text`, `_rag_entity_allowed`, `_rag_expand_tokens`, `_rag_extract_entities`, `_rag_filter_entities`, `_rag_safe_name`, `_rag_tokenize`, `normalize_rel_preview_path`; `skills/store.py`: `_write_text_if_changed`; `utils/files.py`: `_sha256_bytes`, `_sha256_file`, `try_read_text`; `utils/json_utils.py`: `_read_json_file`, `_write_json_file`, `json_dumps`; `utils/media.py`: `guess_mime_from_name`; `utils/misc.py`: `make_id`, `now_ts`; `utils/text.py`: `trim`
- Symbols:
  - `RAGLibraryStore` (class, lines 69513-70087)
  - `WikiStore` (class, lines 70090-70619)
  - `UserMemoryStore` (class, lines 70622-71168)
  - `UserInteractionOptimizer` (class, lines 71171-71233)
  - `UserIntentProfiler` (class, lines 71236-71275)
  - `WorkflowMemoryStore` (class, lines 71278-71676)
  - `CodeLibraryStore` (class, lines 73043-73306)

### `rag/web_search.py`

- Routed symbols: 15
- Cross-module imports: `config/constants.py`: `AGENT_WEB_SEARCH_DEFAULT_DEPTH`, `AGENT_WEB_SEARCH_DEFAULT_MAX_PAGES`, `AGENT_WEB_SEARCH_DEFAULT_MAX_RESULTS`, `AGENT_WEB_SEARCH_FETCH_TIMEOUT`, `AGENT_WEB_SEARCH_HARD_DEPTH`, `AGENT_WEB_SEARCH_HARD_MAX_PAGES`, `AGENT_WEB_SEARCH_MAX_PAGE_BYTES`, `AGENT_WEB_SEARCH_MAX_TEXT_CHARS`, `AGENT_WEB_SEARCH_USER_AGENT`, `WEB_SEARCH_INDEX_DIRNAME`; `config/paths.py`: `WORKDIR`; `utils/http.py`: `urlopen`; `utils/json_utils.py`: `json_dumps`; `utils/misc.py`: `now_ts`; `utils/text.py`: `trim`
- Symbols:
  - `_agent_web_bool` (function, lines 3703-3708)
  - `_agent_web_int` (function, lines 3711-3716)
  - `_agent_web_host_is_local_name` (function, lines 3719-3723)
  - `_agent_web_ip_is_blocked` (function, lines 3726-3738)
  - `_agent_web_canonical_url` (function, lines 3741-3768)
  - `_agent_web_domain_to_seed` (function, lines 3771-3780)
  - `_agent_web_query_terms` (function, lines 3783-3798)
  - `_agent_web_query_domain_hints` (function, lines 3801-3839)
  - `_agent_web_query_needs_fresh_network` (function, lines 3842-3862)
  - `_agent_web_extract_text_snippet` (function, lines 3865-3880)
  - `AgentWebHTMLParser` (class, lines 3883-3960)
  - `_agent_web_decompress_bytes` (function, lines 3963-3984)
  - `_agent_web_charset_candidates` (function, lines 3986-4043)
  - `_agent_web_decode_text_bytes` (function, lines 4045-4078)
  - `AgentWebSearchEngine` (class, lines 4081-5148)

### `server/handlers.py`

- Routed symbols: 6
- Cross-module imports: `app/context.py`: `AppContext`; `config/constants.py`: `APP_VERSION`, `DEFAULT_AUTO_TASK_LEVEL_CEILING`, `DEFAULT_READ_CONTEXT_POLICY`, `DEFAULT_REQUEST_TIMEOUT`, `DEFAULT_SHELL_COMMAND_TIMEOUT_SECONDS`, `DEFAULT_TOOL_MEMORY_POLICY`, `DEFAULT_UI_LANGUAGE`, `DEFAULT_UI_STYLE`, `DEFAULT_USER_MEMORY_MODE`, `EXECUTION_MODE_CHOICES`, `EXECUTION_MODE_SYNC`, `FILES_TREE_DEFAULT_MAX_DEPTH`, `FILES_TREE_DEFAULT_MAX_NODES`, `IDE_TREE_DEFAULT_MAX_NODES`, `MIN_RUN_TIMEOUT_SECONDS`, `PLAN_MODE_USER_CHOICES`, `RAG_GRAPH_MAX_NODES`, `SESSION_LIST_DEFAULT_LIMIT`, `SSE_HEARTBEAT_SECONDS`, `TASK_COMPLEXITY_LEVELS`, `TASK_LEVEL_CHOICES`, `TASK_LEVEL_POLICIES`, `UI_STYLE_LABELS`; `config/paths.py`: `LLM_CONFIG_PATH`, `REPO_ROOT`, `WORKDIR`; `config/settings.py`: `_to_bool_like`, `infer_user_complexity_value`, `looks_like_llm_config`, `normalize_auto_task_level_ceiling`, `normalize_execution_mode`, `normalize_read_context_policy`, `normalize_task_complexity`, `normalize_tool_memory_policy`, `normalize_ui_language`, `normalize_ui_style`, `normalize_user_memory_mode`, `resolve_web_ui_dir_path`, `supported_ui_languages_payload`; `llm/utils.py`: `extract_base_url`, `extract_openai_compat_model_ids`, `list_ollama_models`, `normalize_openai_compat_provider_name`, `openai_compat_model_list_urls`, `openai_compat_probe_headers`; `rag/parsers.py`: `normalize_rel_preview_path`; `session/manager.py`: `SessionCreationLimitExceeded`, `SessionManager`; `session/state.py`: `SessionState`; `skills/store.py`: `analyze_skill_building_knowledge`; `utils/files.py`: `safe_path`, `try_read_text`; `utils/http.py`: `urlopen`; `utils/json_utils.py`: `json_dumps`, `parse_json_object`; `utils/media.py`: `guess_mime_from_name`; `utils/misc.py`: `now_ts`, `swallow_benign_socket_error`, `user_id_from_ip`; `utils/text.py`: `trim`
- Symbols:
  - `AgentHTTPServer` (class, lines 79870-79899)
  - `Handler` (class, lines 79903-80919)
  - `SkillsHandler` (class, lines 80921-81126)
  - `RagAdminHandler` (class, lines 81128-81296)
  - `CodeAdminHandler` (class, lines 81299-81485)
  - `IdeHandler` (class, lines 81488-81749)

### `session/manager.py`

- Routed symbols: 2
- Cross-module imports: `config/constants.py`: `AGENT_MAX_OUTPUT_TOKENS`, `ARBITER_DEFAULT_MAX_TOKENS`, `ARBITER_DEFAULT_TEMPERATURE`, `ARBITER_DEFAULT_TIMEOUT_SECONDS`, `DEFAULT_AUTO_TASK_LEVEL_CEILING`, `DEFAULT_CONTEXT_TOKEN_LIMIT`, `DEFAULT_READ_CONTEXT_POLICY`, `DEFAULT_REQUEST_TIMEOUT`, `DEFAULT_SHELL_COMMAND_TIMEOUT_SECONDS`, `DEFAULT_TOOL_MEMORY_POLICY`, `DEFAULT_UI_LANGUAGE`, `DEFAULT_USER_MEMORY_MODE`, `DEFAULT_WEB_SEARCH_ENABLED`, `EXECUTION_MODE_SYNC`, `MAX_AGENT_ROUNDS`, `MAX_AGENT_ROUNDS_CAP`, `MAX_RUN_SECONDS`, `MAX_RUN_TIMEOUT_SECONDS`, `MAX_SHELL_COMMAND_TIMEOUT_SECONDS`, `MIN_AGENT_ROUNDS`, `MIN_CONTEXT_TOKEN_LIMIT`, `MIN_RUN_TIMEOUT_SECONDS`, `MIN_SHELL_COMMAND_TIMEOUT_SECONDS`, `SESSION_LIST_DEFAULT_LIMIT`, `TOKEN_THRESHOLD`; `config/paths.py`: `LLM_CONFIG_PATH`; `config/settings.py`: `_to_bool_like`, `extract_auto_task_level_ceiling_setting`, `extract_read_context_policy_setting`, `extract_tool_memory_policy_setting`, `extract_user_memory_mode_setting`, `extract_web_search_enabled_setting`, `infer_model_multimodal_capabilities`, `merge_multimodal_capabilities`, `normalize_auto_task_level_ceiling`, `normalize_execution_mode`, `normalize_read_context_policy`, `normalize_tool_memory_policy`, `normalize_ui_language`, `normalize_user_memory_mode`, `parse_capability_overrides`, `parse_llm_config_profiles`, `set_web_search_enabled_on_runtime`; `llm/client.py`: `OllamaClient`; `llm/utils.py`: `complete_chat_endpoint`, `extract_base_url`, `is_openai_compat_provider`, `list_ollama_models_cached`, `probe_ollama_environment`; `rag/store.py`: `UserIntentProfiler`, `UserInteractionOptimizer`, `UserMemoryStore`; `session/state.py`: `SessionState`; `utils/crypto.py`: `CryptoBox`; `utils/files.py`: `try_read_text`; `utils/json_utils.py`: `parse_json_object`; `utils/misc.py`: `make_id`, `normalize_timeout_seconds`, `now_ts`, `sanitize_profile_id`; `utils/text.py`: `trim`
- Symbols:
  - `SessionCreationLimitExceeded` (class, lines 2667-2670)
  - `SessionManager` (class, lines 54594-55838)

### `session/state.py`

- Routed symbols: 1
- Cross-module imports: `agent/background.py`: `BackgroundManager`; `agent/bus.py`: `MessageBus`; `agent/events.py`: `EventHub`; `agent/tasks.py`: `TaskManager`; `agent/todo.py`: `TodoManager`; `agent/worktree.py`: `WorktreeManager`; `config/constants.py`: `AGENT_BUBBLE_ROLES`, `AGENT_CTX_LIMIT_TIER0`, `AGENT_CTX_LIMIT_TIER1`, `AGENT_CTX_LIMIT_TIER2`, `AGENT_CTX_LIMIT_TIER3`, `AGENT_MAX_OUTPUT_TOKENS`, `AGENT_MSG_LIMIT_TIER0`, `AGENT_MSG_LIMIT_TIER1`, `AGENT_MSG_LIMIT_TIER2`, `AGENT_MSG_LIMIT_TIER3`, `AGENT_ROLES`, `AGENT_TOOL_ALLOWLIST`, `AGENT_WEB_SEARCH_DEFAULT_DEPTH`, `AGENT_WEB_SEARCH_DEFAULT_MAX_PAGES`, `AGENT_WEB_SEARCH_DEFAULT_MAX_RESULTS`, `AGENT_WEB_SEARCH_HARD_DEPTH`, `AGENT_WEB_SEARCH_HARD_MAX_PAGES`, `AGENT_WEB_SEARCH_MAX_TEXT_CHARS`, `AGENT_WEB_SEARCH_TOOL_SOFT_TIMEOUT`, `ARBITER_DEFAULT_MAX_TOKENS`, `ARBITER_DEFAULT_TEMPERATURE`, `ARBITER_DEFAULT_TIMEOUT_SECONDS`, `ARBITER_TRIGGER_MIN_CONTENT_CHARS`, `ARBITER_VALID_PLANNING_STREAK_LIMIT`, `ASSISTANT_MESSAGE_EVENT_MAX_CHARS`, `ASSISTANT_TEXT_PERSIST_MAX_CHARS`, `AUDIO_EXTS`, `AUTO_CONTINUE_BUDGET_DEFAULT`, `BASH_READ_LOOP_THRESHOLD`, `BLACKBOARD_MAX_LOG_ENTRIES`, `BLACKBOARD_MAX_TEXT`, `BLACKBOARD_MEMORY_INDEX_MAX`, `BLACKBOARD_MEMORY_LONG_MAX`, `BLACKBOARD_MEMORY_MID_ITEMS_PER_STEP`, `BLACKBOARD_MEMORY_MID_MAX_STEPS`, `BLACKBOARD_MEMORY_SHORT_MAX`, `BLACKBOARD_STATUSES`, `CHAT_UPLOAD_AUTO_LIBRARY_INGEST`, `CHAT_UPLOAD_INGEST_QUEUE_MAX`, `CHAT_UPLOAD_INLINE_TEXT_BYTES`, `CHAT_UPLOAD_PARSE_MAX_BYTES`, `CHAT_UPLOAD_PARSE_QUEUE_MAX`, `CHAT_UPLOAD_PARSE_TIMEOUT_SECONDS`, `CHAT_UPLOAD_PROMPT_MAX_CHARS`, `CHAT_UPLOAD_PROMPT_MAX_FILES`, `CHAT_UPLOAD_PROMPT_PER_FILE_CHARS`, `CHAT_UPLOAD_TEXT_CONTEXT_CHARS`, `CHAT_UPLOAD_ZIP_ENTRY_MAX_BYTES`, `CHECKPOINT_INTERVAL_ROUNDS`, `CHECKPOINT_MAX_COUNT`, `CODE_PREVIEW_STAGE_MAX_BYTES`, `CODE_PREVIEW_STAGE_MAX_PER_FILE`, `CODE_PREVIEW_STAGE_MAX_ROWS`, `CODE_PREVIEW_STAGE_MAX_TOTAL`, `COMPACT_TIER1_ABS`, `COMPACT_TIER1_PCT`, `COMPACT_TIER2_ABS`, `COMPACT_TIER2_PCT`, `COMPACT_TIER3_PCT`, `CONTEXT_ACTUAL_USAGE_RECENT_SECONDS`, `CONTEXT_AUTO_COMPACT_RESERVE_RATIO`, `CONTEXT_COMPACT_INEFFECTIVE_COOLDOWN_SECONDS`, `CONTEXT_ESTIMATE_SAFETY_MULTIPLIER`, `CONTEXT_USAGE_CALIBRATION_MAX`, `CONVERSATION_VISIBLE_TOOL_EVENTS`, `DANGEROUS_PATTERNS`, `DEEP_RESEARCH_REQUEST_KEYWORDS`, `DEEP_RESEARCH_RETRIEVAL_KEYWORDS`, `DEEP_RESEARCH_TEXT_ONLY_HINT_KEYWORDS`, `DEFAULT_AUTO_TASK_LEVEL_CEILING`, `DEFAULT_CONTEXT_TOKEN_LIMIT`, `DEFAULT_READ_CONTEXT_POLICY`, `DEFAULT_REQUEST_TIMEOUT`, `DEFAULT_SHELL_COMMAND_TIMEOUT_SECONDS`, `DEFAULT_TOOL_MEMORY_POLICY`, `DEFAULT_UI_LANGUAGE`, `DEFAULT_USER_MEMORY_MODE`, `DEFAULT_WEB_SEARCH_ENABLED`, `DEVELOPER_EDIT_STALL_THRESHOLD`, `EMPTY_ACTION_MIN_CONTENT_CHARS`, `EMPTY_ACTION_WAKEUP_RETRY_LIMIT`, `ERROR_CATEGORY_DEFS`, `EXECUTION_MODE_CHOICES`, `EXECUTION_MODE_SEQUENTIAL`, `EXECUTION_MODE_SINGLE`, `EXECUTION_MODE_SYNC`, `EXPLORER_STALL_THRESHOLD`, `FAILURE_LEDGER_MAX_COMPILE_ERRORS`, `FAILURE_LEDGER_MAX_DELEGATIONS`, `FAILURE_LEDGER_MAX_ERRORS`, `FAILURE_LEDGER_MAX_FIXES`, `FAILURE_LEDGER_MAX_STALLS`, `FAILURE_LEDGER_MAX_TOOL_FPS`, `FILES_TREE_DEFAULT_MAX_DEPTH`, `FILES_TREE_DEFAULT_MAX_NODES`, `FILES_TREE_SKIP_DIRS`, `FILES_TREE_SKIP_REL_DIRS`, `FILE_BUFFER_CONTENT_THRESHOLD`, `FILE_BUFFER_MAX_FILES`, `FINAL_SUMMARY_MIN_CHARS`, `FINAL_SUMMARY_STRICT_MIN_CHARS`, `FUSED_FAULT_BREAK_THRESHOLD`, `HARD_BREAK_RECOVERY_ROUND_THRESHOLD`, `HARD_BREAK_TOOL_ERROR_THRESHOLD`, `HTML_FRONTEND_REQUEST_KEYWORDS`, `IMAGE_EXTS`, `IMAGE_FORMATS_NEED_CONVERSION`, `LARGE_FILE_AUTO_PAGE_BYTES`, `LARGE_FILE_AUTO_PAGE_LINES`, `LARGE_SOURCE_UPLOAD_EXCERPT_CHARS`, `LIVE_INPUT_DELAY_NORMAL_ROUNDS`, `LIVE_INPUT_DELAY_TOOL_ROUNDS`, `LIVE_INPUT_DELAY_WRITE_ROUNDS`, `LIVE_INPUT_MAX_INJECTIONS`, `LIVE_INPUT_REINJECT_INTERVAL`, `LIVE_INPUT_WEIGHT_BASE_DELAYED`, `LIVE_INPUT_WEIGHT_BASE_NORMAL`, `LIVE_INPUT_WEIGHT_STEP_DELAYED`, `LIVE_INPUT_WEIGHT_STEP_NORMAL`, `LONG_OUTPUT_LISTING_OFFLOAD_CHARS`, `LONG_OUTPUT_MODEL_PAGE_CHARS`, `LONG_OUTPUT_READ_PAGE_LINES`, `LONG_OUTPUT_TEMP_MAX_FILES`, `LONG_OUTPUT_UI_PAGE_CHARS`, `LONG_OUTPUT_UI_PREVIEW_MAX_PAGES`, `MANAGER_CTX_LIMIT_TIER0`, `MANAGER_CTX_LIMIT_TIER1`, `MANAGER_CTX_LIMIT_TIER2`, `MANAGER_CTX_LIMIT_TIER3`, `MANAGER_ROUTE_TARGETS`, `MAX_AGENT_ROUNDS`, `MAX_AGENT_ROUNDS_CAP`, `MAX_CONTEXT_ARCHIVE_SEGMENTS`, `MAX_RUN_SECONDS`, `MAX_RUN_TIMEOUT_SECONDS`, `MAX_SHELL_COMMAND_TIMEOUT_SECONDS`, `MIN_AGENT_ROUNDS`, `MIN_CONTEXT_TOKEN_LIMIT`, `MIN_RUN_TIMEOUT_SECONDS`, `MIN_SHELL_COMMAND_TIMEOUT_SECONDS`, `MODEL_CALL_PROGRESS_DELAY`, `MODEL_CALL_PROGRESS_INTERVAL`, `MODEL_OUTPUT_RETRY_TIMES`, `PERSISTED_ROUTES_MAX`, `PERSIST_EVENT_MIN_INTERVAL_SECONDS`, `PERSIST_ON_EVENT_TYPES`, `PLAN_BUBBLE_MAX_CHARS`, `PLAN_FILE_RELATIVE_PATH`, `PLAN_MESSAGE_EVENT_MAX_CHARS`, `PLAN_MODE_ENABLED_LEVELS`, `PLAN_MODE_EXPLORER_MAX_ROUNDS`, `PLAN_MODE_MANAGER_SYNTHESIS_MAX_TOKENS`, `PLAN_MODE_MAX_OPTIONS`, `PLAN_MODE_RESEARCH_TOOL_ALLOWLIST`, `PLAN_MODE_SYNTHESIS_MAX_ATTEMPTS`, `PLAN_MODE_USER_CHOICES`, `PLAN_NOTICE_BODY_MAX_CHARS`, `PLAN_STEP_FULL_CONTENT_MAX_CHARS`, `PREVIEW_DOWNLOAD_MAX_BYTES`, `PREVIEW_DOWNLOAD_MAX_FILES`, `READ_CONTEXT_PROMPT_MAX_CHARS`, `READ_CONTEXT_PROMPT_MAX_ITEMS`, `READ_CONTEXT_REGISTRY_MAX`, `READ_CONTEXT_SHARED_MAX_ITEMS`, `READ_CONTEXT_SUMMARY_MAX_CHARS`, `READ_FILE_COMPACT_PIN_DISTINCT`, `READ_FILE_COMPACT_PIN_MAX_CHARS`, `READ_FILE_DEFAULT_MAX_CHARS`, `READ_FILE_HARD_MAX_CHARS`, `READ_FILE_LOOP_DISTINCT_SOFT_LIMIT`, `READ_FILE_LOOP_THRESHOLD`, `READ_FILE_OVERVIEW_HEAD_LINES`, `READ_FILE_SEARCH_MAX_MATCHES`, `RENDER_FRAME_ACTIVITY_INTERVAL_SECONDS`, `RENDER_FRAME_MAX_B64_CHARS`, `RENDER_FRAME_MAX_LINES`, `RENDER_FRAME_MAX_LINE_POINTS`, `RENDER_FRAME_MAX_POINTS`, `REPEATED_TOOL_LOOP_THRESHOLD`, `RETRY_RUNTIME_HINT_PREFIXES`, `REVIEWER_DEBUG_MODE_MAX_ROUNDS`, `RUNTIME_CONTROL_HINT_PREFIXES`, `RUN_COMPLETION_SUMMARY_ENABLED`, `SEMANTIC_CONFIDENCE_CHOICES`, `SESSION_DEFERRED_START_QUEUE_MAX`, `SESSION_HEARTBEAT_STALE_SECONDS`, `SESSION_SUBMIT_LOCK_TIMEOUT_SECONDS`, `SKILLS_VIRTUAL_PREFIX`, `SKILL_REFRESH_MIN_INTERVAL_SECONDS`, `SKILL_RUNTIME_CACHE_MAX_BYTES`, `SKILL_RUNTIME_CACHE_MAX_ENTRIES`, `STALL_ESCALATION_CONTEXT_MAX_CHARS`, `STALL_ESCALATION_MIN_LEVEL`, `STALL_PLAN_SYNTHESIS_MAX_TOKENS`, `STALL_SEVERITY_DECAY_ON_SUCCESS`, `STALL_SEVERITY_ESCALATION_THRESHOLD`, `STALL_SEVERITY_WEIGHT_BASH_READ_LOOP`, `STALL_SEVERITY_WEIGHT_FAULT`, `STALL_SEVERITY_WEIGHT_RECOVERY_RETRY`, `STALL_SEVERITY_WEIGHT_REPEATED_TOOL`, `STALL_SEVERITY_WEIGHT_WATCHDOG`, `TASK_COMPLEXITY_LEVELS`, `TASK_LEVEL_CHOICES`, `TASK_LEVEL_POLICIES`, `TASK_PHASE_ROUTING`, `TASK_PROFILE_TYPES`, `TASK_SCALE_PREFERENCES`, `THINKING_BUDGET_FORCE_RATIO`, `TOKEN_THRESHOLD`, `TOOL_MEMORY_COMPACT_PIN_DISTINCT`, `TOOL_MEMORY_COMPACT_PIN_MAX_CHARS`, `TOOL_MEMORY_PROMPT_MAX_CHARS`, `TOOL_MEMORY_PROMPT_MAX_ITEMS`, `TOOL_MEMORY_REGISTRY_MAX`, `TOOL_MEMORY_SHARED_MAX_ITEMS`, `TOOL_MEMORY_SUMMARY_MAX_CHARS`, `TRUNCATION_CONTINUATION_ECHO_CHARS`, `TRUNCATION_CONTINUATION_MAX_PASSES`, `TRUNCATION_CONTINUATION_MAX_TOKENS`, `TRUNCATION_CONTINUATION_TAIL_CHARS`, `TRUNCATION_LIVE_BUFFER_MAX_CHARS`, `TRUNCATION_OVERLAP_SCAN_CHARS`, `TRUNCATION_PAIR_SCAN_CHARS`, `USER_MEMORY_ON_CAPSULE_CHARS`, `VIDEO_EXTS`, `WATCHDOG_CONTEXT_NEAR_RATIO`, `WATCHDOG_CONTEXT_STALL_THRESHOLD`, `WATCHDOG_INTENT_NO_TOOL_THRESHOLD`, `WATCHDOG_INTENT_NO_TOOL_THRESHOLD_SINGLE`, `WATCHDOG_MAX_DECOMPOSE_STEPS`, `WATCHDOG_REPEAT_NO_TOOL_THRESHOLD`, `WATCHDOG_REPEAT_NO_TOOL_THRESHOLD_SINGLE`, `WATCHDOG_REPEAT_SIMILARITY_THRESHOLD`, `WATCHDOG_STATE_STALL_THRESHOLD`, `WATCHDOG_STEP_MAX_ATTEMPTS`, `WEB_SEARCH_CONTEXT_NODE_MAX`, `WEB_SEARCH_CONTEXT_PROMPT_MAX_CHARS`, `WEB_SEARCH_CONTEXT_PROMPT_MAX_ITEMS`, `WEB_SEARCH_CONTEXT_REGISTRY_MAX`, `WEB_SEARCH_CONTEXT_URL_MAX`, `WEB_SEARCH_INDEX_DIRNAME`, `_DEFAULT_TOOL_TIMEOUT`, `_SHELL_AUTO_CONFIRM_PATTERNS`, `_TOOL_TIMEOUT_MAP`; `config/paths.py`: `WORKDIR`; `config/settings.py`: `_detect_os_shell_instruction`, `_to_bool_like`, `backend_i18n_text`, `backend_role_label`, `default_multimodal_capabilities`, `extract_auto_task_level_ceiling_setting`, `extract_runtime_region_hint_setting`, `extract_runtime_timezone_hint_setting`, `extract_user_memory_mode_setting`, `extract_web_search_enabled_setting`, `infer_model_multimodal_capabilities`, `infer_user_complexity_value`, `looks_like_llm_config`, `max_task_complexity`, `merge_multimodal_capabilities`, `model_language_instruction`, `normalize_auto_task_level_ceiling`, `normalize_execution_mode`, `normalize_read_context_policy`, `normalize_task_complexity`, `normalize_tool_memory_policy`, `normalize_ui_language`, `normalize_user_memory_mode`, `parse_capability_overrides`, `parse_llm_config_profiles`, `runtime_environment_context_block`, `runtime_environment_context_snapshot`, `task_complexity_at_least`, `task_complexity_rank`; `llm/client.py`: `OllamaClient`, `OllamaError`; `llm/utils.py`: `complete_chat_endpoint`, `extract_base_url`, `is_openai_compat_provider`, `list_loaded_ollama_models`, `list_ollama_models`, `list_ollama_models_cached`, `probe_ollama_environment`, `resolve_ollama_model`, `split_thinking_content`, `strip_thinking_content`, `wake_ollama_model`; `rag/parsers.py`: `CodeContentParser`, `build_code_preview_rows`, `is_code_preview_candidate`, `normalize_rel_preview_path`, `preview_kind_for_path`; `rag/web_search.py`: `AgentWebSearchEngine`, `_agent_web_bool`, `_agent_web_extract_text_snippet`, `_agent_web_query_terms`; `skills/store.py`: `SkillStore`, `ensure_runtime_skills`; `utils/compress.py`: `compress_text_blob`, `decompress_text_blob`; `utils/crypto.py`: `CryptoBox`; `utils/errors.py`: `CircuitBreakerTriggered`, `EmptyActionError`; `utils/files.py`: `_normalize_external_js_url`, `_safe_js_filename`, `cache_external_js_url`, `ensure_offline_js_libs`, `is_external_js_src`, `load_offline_js_lib_index`, `match_offline_js_catalog_by_url`, `offline_js_lib_root`, `safe_path`, `try_read_text`; `utils/http.py`: `urlopen`; `utils/json_utils.py`: `TOOLS`, `TOOL_REQUIRED_ARGS`, `canonicalize_tool_name`, `extract_json_object_from_text`, `filter_tool_specs_for_runtime`, `json_dumps`, `parse_json_object`, `parse_tool_arguments_with_error`, `repair_truncated_json_object`, `tool_def`; `utils/media.py`: `_convert_image_to_safe_format`, `guess_ext_from_mime`, `guess_mime_from_name`; `utils/misc.py`: `MAX_TIMEOUT_SECONDS`, `MIN_TIMEOUT_SECONDS`, `is_benign_socket_error`, `make_id`, `normalize_timeout_seconds`, `now_ts`, `sanitize_profile_id`; `utils/text.py`: `MAX_TOOL_OUTPUT`, `_fmt_export_ts`, `_html_esc`, `_text_to_minimal_pdf`, `extract_todo_rows_from_text`, `filter_runtime_noise_lines`, `make_numbered_diff`, `make_unified_diff`, `normalize_embedded_newlines`, `normalize_work_text`, `parse_front_matter`, `render_numbered_diff_text`, `split_structured_todo_content`, `split_todo_status_text`, `trim`
- Symbols:
  - `SessionState` (class, lines 16023-54592)

### `skills/store.py`

- Routed symbols: 27
- Cross-module imports: `config/constants.py`: `BUILTIN_CLAWHUB_SKILLS_VERSION`, `EMBEDDED_CLAWHUB_SKILLS_ARCHIVE_B64`, `EMBEDDED_SKILLS_ARCHIVE_B64`, `EMBEDDED_SKILLS_ARCHIVE_FILES`, `EMBEDDED_SKILLS_ARCHIVE_SHA256`, `SKILLS_EXTERNAL_MOUNT`, `SKILLS_VIRTUAL_PREFIX`, `SKILL_BODY_COMPACT_THRESHOLD_CHARS`, `SKILL_BODY_PREVIEW_CHARS`, `SKILL_DEFAULT_ATTACHMENT_GLOBS`, `SKILL_INLINE_ATTACHMENT_MAX_CHARS`, `SKILL_INLINE_ATTACHMENT_MAX_FILES`, `SKILL_PROMPT_MAX_CHARS`, `SKILL_PROMPT_MAX_ITEMS`, `SKILL_PROTOCOL_CLAWHUB`, `SKILL_PROTOCOL_HTTP_JSON`, `SKILL_PROTOCOL_LOCAL`, `SKILL_PROTOCOL_SPECS`, `SKILL_REFRESH_MIN_INTERVAL_SECONDS`, `SKILL_RESOURCE_MANIFEST_MAX_ITEMS`; `config/paths.py`: `WORKDIR`; `llm/utils.py`: `_is_http_url`; `utils/files.py`: `_render_offline_js_catalog_md`, `safe_path`, `try_read_text`; `utils/http.py`: `urlopen`; `utils/json_utils.py`: `json_dumps`, `parse_json_object`; `utils/misc.py`: `_meta_string_list`, `_module_exists`, `now_ts`; `utils/text.py`: `parse_front_matter`, `trim`
- Symbols:
  - `ensure_embedded_skills_at_root` (function, lines 8584-8636)
  - `ensure_embedded_skills` (function, lines 8639-8640)
  - `detect_upload_parser_capabilities` (function, lines 8648-8663)
  - `_render_cap_markdown` (function, lines 8665-8679)
  - `_write_text_if_changed` (function, lines 8681-8686)
  - `ensure_generated_document_skills` (function, lines 8688-8776)
  - `ensure_generated_image_coding_feedback_skill` (function, lines 8778-8877)
  - `_skill_knowledge_files` (function, lines 8879-8898)
  - `analyze_skill_building_knowledge` (function, lines 8900-8954)
  - `_sanitize_skill_slug` (function, lines 8956-8958)
  - `_build_skills_gen_skill_content` (function, lines 8960-8991)
  - `ensure_generated_skills_gen_skill` (function, lines 8993-8997)
  - `ensure_generated_execution_recovery_skill` (function, lines 8999-9077)
  - `ensure_generated_systematic_debugging_skill` (function, lines 9079-9351)
  - `ensure_generated_code_engineering_mastery_skill` (function, lines 9353-9471)
  - `ensure_generated_smart_file_navigation_skill` (function, lines 9473-9588)
  - `ensure_generated_html_frontend_report_skills` (function, lines 9590-9797)
  - `ensure_generated_deep_research_skills` (function, lines 9799-10067)
  - `ensure_generated_research_scientific_skills` (function, lines 10069-10705)
  - `ensure_generated_rag_mastery_skills` (function, lines 10711-11007)
  - `ensure_generated_multimodal_comprehension_skills` (function, lines 11013-11702)
  - `ensure_generated_runtime_skills_manifest` (function, lines 11705-11737)
  - `ensure_generated_agent_web_search_skill` (function, lines 11740-11800)
  - `ensure_embedded_clawhub_skills` (function, lines 12059-12096)
  - `ensure_runtime_skills` (function, lines 12098-12114)
  - `_BUILTIN_SKILLS` (assignment, lines 12156-12245)
  - `SkillStore` (class, lines 12254-13548)

### `utils/compress.py`

- Routed symbols: 2
- Cross-module imports: none
- Symbols:
  - `compress_text_blob` (function, lines 5314-5319)
  - `decompress_text_blob` (function, lines 5321-5329)

### `utils/crypto.py`

- Routed symbols: 1
- Cross-module imports: `utils/json_utils.py`: `json_dumps`
- Symbols:
  - `CryptoBox` (class, lines 6918-7035)

### `utils/errors.py`

- Routed symbols: 2
- Cross-module imports: none
- Symbols:
  - `EmptyActionError` (class, lines 5703-5704)
  - `CircuitBreakerTriggered` (class, lines 5707-5708)

### `utils/files.py`

- Routed symbols: 25
- Cross-module imports: `config/constants.py`: `OFFLINE_JS_LIB_CATALOG`, `OFFLINE_JS_LIB_INDEX_FILE`, `OFFLINE_JS_LIB_README_FILE`; `config/paths.py`: `WORKDIR`; `utils/http.py`: `urlopen`; `utils/json_utils.py`: `json_dumps`; `utils/misc.py`: `now_ts`; `utils/text.py`: `trim`
- Symbols:
  - `_normalize_js_lib_asset_ref` (function, lines 1565-1578)
  - `_resolve_js_lib_asset_path` (function, lines 1581-1610)
  - `_discover_extra_js_lib_files` (function, lines 1613-1643)
  - `safe_path` (function, lines 3243-3252)
  - `_safe_js_filename` (function, lines 3254-3261)
  - `_sha256_bytes` (function, lines 3263-3264)
  - `_sha256_file` (function, lines 3266-3274)
  - `_download_http_bytes` (function, lines 3276-3284)
  - `offline_js_lib_root` (function, lines 3286-3287)
  - `_offline_js_entry_relative_path` (function, lines 3289-3293)
  - `_archive_member_relative_path` (function, lines 3295-3304)
  - `_path_size_bytes` (function, lines 3306-3321)
  - `_extract_archive_to_dir` (function, lines 3323-3363)
  - `_package_required_paths` (function, lines 3365-3371)
  - `_package_install_ready` (function, lines 3373-3381)
  - `_postprocess_offline_js_package` (function, lines 3383-3418)
  - `_ensure_offline_js_package` (function, lines 3420-3459)
  - `_render_offline_js_catalog_md` (function, lines 3461-3477)
  - `load_offline_js_lib_index` (function, lines 3479-3488)
  - `ensure_offline_js_libs` (function, lines 3490-3634)
  - `_normalize_external_js_url` (function, lines 3636-3640)
  - `is_external_js_src` (function, lines 3642-3644)
  - `match_offline_js_catalog_by_url` (function, lines 3646-3662)
  - `cache_external_js_url` (function, lines 3664-3696)
  - `try_read_text` (function, lines 7240-7248)

### `utils/http.py`

- Routed symbols: 4
- Cross-module imports: none
- Symbols:
  - `_URL_OPEN_ORIGINAL` (assignment, lines 61-61)
  - `_HTTP_SSL_CONTEXT` (assignment, lines 62-62)
  - `_shared_http_ssl_context` (function, lines 75-90)
  - `urlopen` (function, lines 92-100)

### `utils/json_utils.py`

- Routed symbols: 17
- Cross-module imports: `config/constants.py`: `DEFAULT_WEB_SEARCH_ENABLED`; `utils/text.py`: `trim`
- Symbols:
  - `JSON_FSYNC_ENABLED` (constant, lines 153-153)
  - `json_dumps` (function, lines 3215-3216)
  - `parse_tool_arguments` (function, lines 5582-5591)
  - `repair_truncated_json_object` (function, lines 5593-5646)
  - `parse_tool_arguments_with_error` (function, lines 5648-5678)
  - `parse_json_object` (function, lines 5944-5949)
  - `extract_json_object_from_text` (function, lines 5951-5973)
  - `_json_default_copy` (function, lines 7250-7255)
  - `_read_json_file` (function, lines 7257-7277)
  - `_write_json_file` (function, lines 7279-7306)
  - `tool_def` (function, lines 15541-15553)
  - `TOOLS` (constant, lines 15555-15905)
  - `TOOL_REQUIRED_ARGS` (constant, lines 15907-15907)
  - `TOOL_SPEC_BY_NAME` (constant, lines 15908-15908)
  - `TOOL_NAME_FUZZY_MAP` (constant, lines 15920-15920)
  - `canonicalize_tool_name` (function, lines 15938-15949)
  - `filter_tool_specs_for_runtime` (function, lines 15952-15962)

### `utils/media.py`

- Routed symbols: 3
- Cross-module imports: none
- Symbols:
  - `guess_mime_from_name` (function, lines 2915-2917)
  - `_convert_image_to_safe_format` (function, lines 2920-2937)
  - `guess_ext_from_mime` (function, lines 2940-2946)

### `utils/misc.py`

- Routed symbols: 21
- Cross-module imports: none
- Symbols:
  - `MIN_TIMEOUT_SECONDS` (constant, lines 416-416)
  - `MAX_TIMEOUT_SECONDS` (constant, lines 417-417)
  - `DEFAULT_TIMEOUT_SECONDS` (constant, lines 418-424)
  - `BENIGN_SOCKET_DEBUG_LOG_ENABLED` (constant, lines 582-588)
  - `BENIGN_SOCKET_LOG_INTERVAL_SECONDS` (constant, lines 589-589)
  - `now_ts` (function, lines 2948-2949)
  - `_benign_socket_log_lock` (assignment, lines 2952-2952)
  - `_benign_socket_log_state` (assignment, lines 2953-2953)
  - `is_benign_socket_error` (function, lines 2971-2989)
  - `_socket_error_code` (function, lines 2992-3001)
  - `_log_benign_socket_error_limited` (function, lines 3004-3038)
  - `swallow_benign_socket_error` (function, lines 3041-3045)
  - `normalize_timeout_seconds` (function, lines 3048-3061)
  - `detect_local_lan_ip` (function, lines 3063-3073)
  - `_LOCAL_LAN_IP_CACHE` (assignment, lines 3075-3075)
  - `detect_local_lan_ip_cached` (function, lines 3077-3089)
  - `make_id` (function, lines 3218-3219)
  - `sanitize_profile_id` (function, lines 3221-3223)
  - `user_id_from_ip` (function, lines 6910-6916)
  - `_meta_string_list` (function, lines 7227-7238)
  - `_module_exists` (function, lines 8642-8646)

### `utils/text.py`

- Routed symbols: 23
- Cross-module imports: `config/constants.py`: `CODE_PREVIEW_DIFF_CONTEXT_LINES`, `CODE_PREVIEW_DIFF_MERGE_GAP`
- Symbols:
  - `MAX_TOOL_OUTPUT` (constant, lines 141-141)
  - `SOCKET_NOISE_LINE_PATTERNS` (constant, lines 576-581)
  - `filter_runtime_noise_lines` (function, lines 2956-2968)
  - `trim` (function, lines 3698-3700)
  - `_fmt_export_ts` (function, lines 5151-5159)
  - `_html_esc` (function, lines 5162-5163)
  - `_text_to_minimal_pdf` (function, lines 5166-5312)
  - `normalize_embedded_newlines` (function, lines 5331-5339)
  - `_map_todo_status_token` (function, lines 5342-5357)
  - `split_todo_status_text` (function, lines 5360-5415)
  - `extract_todo_rows_from_text` (function, lines 5418-5485)
  - `infer_todo_status_from_text` (function, lines 5488-5494)
  - `split_structured_todo_content` (function, lines 5497-5550)
  - `normalize_work_text` (function, lines 5553-5580)
  - `parse_front_matter` (function, lines 7037-7224)
  - `make_unified_diff` (function, lines 7308-7325)
  - `_skip_row` (function, lines 7327-7331)
  - `_row_is_hot` (function, lines 7334-7335)
  - `_hotspot_index` (function, lines 7338-7359)
  - `_compress_rows_keep_hotspot` (function, lines 7362-7409)
  - `_focused_diff_rows_from_opcodes` (function, lines 7412-7544)
  - `make_numbered_diff` (function, lines 7547-7577)
  - `render_numbered_diff_text` (function, lines 7579-7591)
