# Code_Structure Framework

## Overview

- Source file: `/Users/Fona/Downloads/Clouds_Coder/Clouds_Coder.py`
- Output directory: `/Users/Fona/Downloads/Clouds_Coder/Code_Structure`
- Generated modules: 32
- Top-level symbols: 766
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
├── mcp
│   └── driver.py
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
| `app/context.py` | 1 | `config/constants.py`, `config/paths.py`, `config/settings.py`, `llm/client.py`, `llm/utils.py`, `mcp/driver.py`, `rag/ingestion.py`, `rag/parsers.py`, `rag/store.py`, `session/manager.py`, `session/state.py`, `skills/store.py`, `utils/crypto.py`, `utils/files.py`, `utils/json_utils.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py` |
| `config/constants.py` | 453 | `utils/json_utils.py`, `utils/misc.py` |
| `config/paths.py` | 8 | `utils/text.py` |
| `config/settings.py` | 49 | `config/constants.py`, `config/paths.py`, `llm/utils.py`, `skills/store.py`, `utils/http.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` |
| `llm/client.py` | 2 | `config/constants.py`, `config/settings.py`, `llm/utils.py`, `utils/http.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` |
| `llm/utils.py` | 28 | `config/constants.py`, `utils/http.py`, `utils/json_utils.py`, `utils/text.py` |
| `mcp/driver.py` | 8 | `config/constants.py`, `utils/files.py`, `utils/json_utils.py` |
| `rag/index.py` | 5 | `config/constants.py`, `rag/ingestion.py`, `rag/parsers.py`, `utils/misc.py`, `utils/text.py` |
| `rag/ingestion.py` | 13 | `config/constants.py`, `config/settings.py`, `rag/parsers.py`, `rag/store.py`, `session/state.py`, `utils/files.py`, `utils/json_utils.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py` |
| `rag/parsers.py` | 28 | `config/constants.py`, `rag/ingestion.py`, `utils/files.py`, `utils/json_utils.py`, `utils/media.py`, `utils/text.py` |
| `rag/store.py` | 7 | `config/constants.py`, `config/settings.py`, `rag/index.py`, `rag/ingestion.py`, `rag/parsers.py`, `skills/store.py`, `utils/files.py`, `utils/json_utils.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py` |
| `rag/web_search.py` | 15 | `config/constants.py`, `config/paths.py`, `utils/http.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` |
| `server/handlers.py` | 7 | `app/context.py`, `config/constants.py`, `config/paths.py`, `config/settings.py`, `llm/utils.py`, `rag/parsers.py`, `session/manager.py`, `session/state.py`, `skills/store.py`, `utils/files.py`, `utils/http.py`, `utils/json_utils.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py` |
| `session/manager.py` | 2 | `config/constants.py`, `config/paths.py`, `config/settings.py`, `llm/client.py`, `llm/utils.py`, `rag/store.py`, `session/state.py`, `utils/crypto.py`, `utils/files.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` |
| `session/state.py` | 1 | `agent/background.py`, `agent/bus.py`, `agent/events.py`, `agent/tasks.py`, `agent/todo.py`, `agent/worktree.py`, `config/constants.py`, `config/paths.py`, `config/settings.py`, `llm/client.py`, `llm/utils.py`, `mcp/driver.py`, `rag/parsers.py`, `rag/web_search.py`, `skills/store.py`, `utils/compress.py`, `utils/crypto.py`, `utils/errors.py`, `utils/files.py`, `utils/http.py`, `utils/json_utils.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py` |
| `skills/store.py` | 28 | `config/constants.py`, `config/paths.py`, `llm/utils.py`, `utils/files.py`, `utils/http.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` |
| `utils/compress.py` | 2 | — |
| `utils/crypto.py` | 1 | `utils/json_utils.py` |
| `utils/errors.py` | 2 | — |
| `utils/files.py` | 25 | `config/constants.py`, `config/paths.py`, `utils/http.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` |
| `utils/http.py` | 4 | — |
| `utils/json_utils.py` | 20 | `config/constants.py`, `utils/text.py` |
| `utils/media.py` | 3 | — |
| `utils/misc.py` | 21 | — |
| `utils/text.py` | 25 | `config/constants.py` |

## Module Details

### `__main__.py`

- Routed symbols: 2
- Cross-module imports: `app/context.py`: `AppContext`; `config/constants.py`: `AGENT_MAX_OUTPUT_TOKENS`, `ARBITER_DEFAULT_MAX_TOKENS`, `ARBITER_DEFAULT_TEMPERATURE`, `ARBITER_DEFAULT_TIMEOUT_SECONDS`, `CODE_ADMIN_PORT_OFFSET`, `DEFAULT_AUTO_TASK_LEVEL_CEILING`, `DEFAULT_CONTEXT_TOKEN_LIMIT`, `DEFAULT_OLLAMA_BASE_URL`, `DEFAULT_OLLAMA_MODEL`, `DEFAULT_READ_CONTEXT_POLICY`, `DEFAULT_SHELL_COMMAND_TIMEOUT_SECONDS`, `DEFAULT_TOOL_MEMORY_POLICY`, `DEFAULT_UI_LANGUAGE`, `DEFAULT_UI_STYLE`, `DEFAULT_USER_MEMORY_MODE`, `DEFAULT_WEB_SEARCH_ENABLED`, `DEFAULT_WEB_UI_CONFIG`, `DEFAULT_WEB_UI_DIR`, `EXECUTION_MODE_SYNC`, `IDE_PORT_OFFSET`, `LIVE_INPUT_DELAY_NORMAL_ROUNDS`, `LIVE_INPUT_DELAY_TOOL_ROUNDS`, `LIVE_INPUT_DELAY_WRITE_ROUNDS`, `LIVE_INPUT_MAX_INJECTIONS`, `LIVE_INPUT_REINJECT_INTERVAL`, `LIVE_INPUT_WEIGHT_BASE_DELAYED`, `LIVE_INPUT_WEIGHT_BASE_NORMAL`, `LIVE_INPUT_WEIGHT_STEP_DELAYED`, `LIVE_INPUT_WEIGHT_STEP_NORMAL`, `MAX_AGENT_ROUNDS`, `MAX_AGENT_ROUNDS_CAP`, `MAX_RUN_SECONDS`, `MAX_RUN_TIMEOUT_SECONDS`, `MAX_SHELL_COMMAND_TIMEOUT_SECONDS`, `MCP_SERVICE_PORT_OFFSET`, `MIN_AGENT_ROUNDS`, `MIN_CONTEXT_TOKEN_LIMIT`, `MIN_RUN_TIMEOUT_SECONDS`, `MIN_SHELL_COMMAND_TIMEOUT_SECONDS`, `OFFLINE_JS_LIB_CATALOG`, `RAG_ADMIN_PORT_OFFSET`, `RAG_INCLUDE_FILENAME_ENTITIES_DEFAULT`, `TOKEN_THRESHOLD`, `UI_LANGUAGE_LABELS`, `UI_STYLE_LABELS`, `USER_MEMORY_MODE_CHOICES`; `config/paths.py`: `LLM_CONFIG_PATH`, `REPO_ROOT`, `WORKDIR`; `config/settings.py`: `_to_bool_like`, `extract_auto_task_level_ceiling_setting`, `extract_context_token_limit_setting`, `extract_daily_session_limit_setting`, `extract_js_lib_download_setting`, `extract_read_context_policy_setting`, `extract_shell_command_timeout_setting`, `extract_show_upload_list_setting`, `extract_tool_memory_policy_setting`, `extract_ui_style_setting`, `extract_user_memory_mode_setting`, `extract_web_search_enabled_setting`, `load_llm_config_from_source`, `load_web_ui_config_file`, `normalize_auto_task_level_ceiling`, `normalize_execution_mode`, `normalize_read_context_policy`, `normalize_tool_memory_policy`, `normalize_ui_language`, `normalize_ui_style`, `normalize_user_memory_mode`, `parse_llm_config_profiles`, `resolve_optional_file_path`, `resolve_web_ui_dir_path`, `select_preferred_skills_root`; `llm/utils.py`: `list_ollama_models`; `server/handlers.py`: `AgentHTTPServer`, `CodeAdminHandler`, `Handler`, `IdeHandler`, `McpServiceHandler`, `RagAdminHandler`, `SkillsHandler`; `skills/store.py`: `ensure_embedded_skills_at_root`, `ensure_runtime_skills`; `utils/files.py`: `ensure_offline_js_libs`; `utils/json_utils.py`: `TOOLS`, `filter_tool_specs_for_runtime`; `utils/misc.py`: `BENIGN_SOCKET_DEBUG_LOG_ENABLED`, `detect_local_lan_ip`, `normalize_timeout_seconds`, `now_ts`, `swallow_benign_socket_error`; `utils/text.py`: `trim`
- Symbols:
  - `main` (function, lines 86945-88343)
  - `_main_guard_88345` (main_guard, lines 88345-88346)

### `agent/background.py`

- Routed symbols: 1
- Cross-module imports: `utils/misc.py`: `make_id`, `now_ts`; `utils/text.py`: `trim`
- Symbols:
  - `BackgroundManager` (class, lines 13764-13844)

### `agent/bus.py`

- Routed symbols: 1
- Cross-module imports: `config/constants.py`: `VALID_MSG_TYPES`; `utils/crypto.py`: `CryptoBox`; `utils/misc.py`: `now_ts`
- Symbols:
  - `MessageBus` (class, lines 13846-13910)

### `agent/events.py`

- Routed symbols: 1
- Cross-module imports: none
- Symbols:
  - `EventHub` (class, lines 8090-8135)

### `agent/tasks.py`

- Routed symbols: 1
- Cross-module imports: `utils/crypto.py`: `CryptoBox`; `utils/json_utils.py`: `json_dumps`; `utils/misc.py`: `now_ts`
- Symbols:
  - `TaskManager` (class, lines 13636-13762)

### `agent/todo.py`

- Routed symbols: 1
- Cross-module imports: `config/constants.py`: `DEFAULT_UI_LANGUAGE`; `config/settings.py`: `backend_i18n_text`, `backend_role_label`, `normalize_ui_language`; `utils/misc.py`: `now_ts`; `utils/text.py`: `infer_todo_status_from_text`, `normalize_work_text`, `split_structured_todo_content`, `trim`
- Symbols:
  - `TodoManager` (class, lines 8137-8420)

### `agent/worktree.py`

- Routed symbols: 1
- Cross-module imports: `agent/tasks.py`: `TaskManager`; `config/constants.py`: `DANGEROUS_PATTERNS`; `utils/crypto.py`: `CryptoBox`; `utils/json_utils.py`: `json_dumps`; `utils/misc.py`: `now_ts`; `utils/text.py`: `trim`
- Symbols:
  - `WorktreeManager` (class, lines 13912-14127)

### `app/context.py`

- Routed symbols: 1
- Cross-module imports: `config/constants.py`: `AGENT_MAX_OUTPUT_TOKENS`, `APP_CSS`, `APP_JS`, `APP_TS`, `APP_VERSION`, `ARBITER_DEFAULT_MAX_TOKENS`, `ARBITER_DEFAULT_TEMPERATURE`, `ARBITER_DEFAULT_TIMEOUT_SECONDS`, `CODE_ADMIN_CSS`, `CODE_ADMIN_INDEX_HTML`, `CODE_ADMIN_JS`, `CODE_IMPORT_WORKER_COUNT`, `CODE_LIBRARY_DIRNAME`, `CODE_PARSE_TIMEOUT_SECONDS`, `DEFAULT_AUTO_TASK_LEVEL_CEILING`, `DEFAULT_CONTEXT_TOKEN_LIMIT`, `DEFAULT_READ_CONTEXT_POLICY`, `DEFAULT_REQUEST_TIMEOUT`, `DEFAULT_SHELL_COMMAND_TIMEOUT_SECONDS`, `DEFAULT_TOOL_MEMORY_POLICY`, `DEFAULT_UI_LANGUAGE`, `DEFAULT_UI_STYLE`, `DEFAULT_USER_MEMORY_MODE`, `DEFAULT_WEB_SEARCH_ENABLED`, `DEFAULT_WEB_UI_DIR`, `EXECUTION_MODE_SYNC`, `IDE_COMMAND_TIMEOUT_DEFAULT`, `IDE_CSS`, `IDE_DEFAULT_PORT`, `IDE_FILE_MAX_BYTES`, `IDE_INDEX_HTML`, `IDE_JS`, `IDE_TREE_DEFAULT_MAX_NODES`, `IDE_TREE_MAX_NODES`, `IDE_TREE_SKIP_DIRS`, `IDE_UPLOAD_MAX_BYTES`, `IDE_UPLOAD_MAX_ITEMS`, `IDE_UPLOAD_TOTAL_MAX_BYTES`, `INDEX_HTML`, `MAX_AGENT_ROUNDS`, `MAX_AGENT_ROUNDS_CAP`, `MAX_RUN_SECONDS`, `MAX_RUN_TIMEOUT_SECONDS`, `MAX_SHELL_COMMAND_TIMEOUT_SECONDS`, `MIN_AGENT_ROUNDS`, `MIN_CONTEXT_TOKEN_LIMIT`, `MIN_RUN_TIMEOUT_SECONDS`, `MIN_SHELL_COMMAND_TIMEOUT_SECONDS`, `RAG_ADMIN_CSS`, `RAG_ADMIN_INDEX_HTML`, `RAG_ADMIN_JS`, `RAG_CONTEXT_BUDGETS`, `RAG_DENSE_DEFAULT_ENABLED`, `RAG_EMBEDDING_MODE_VALUES`, `RAG_GRAPH_MAX_NODES`, `RAG_HIGH_RECALL_MIN_POOL`, `RAG_HIGH_RECALL_POOL_MULTIPLIER`, `RAG_IMPORT_WORKER_COUNT`, `RAG_INCLUDE_FILENAME_ENTITIES_DEFAULT`, `RAG_LIBRARY_DIRNAME`, `RAG_MAX_GLOBAL_COMMUNITIES`, `RAG_MAX_IMPORT_BATCH_BYTES`, `RAG_MAX_IMPORT_BATCH_ITEMS`, `RAG_MAX_IMPORT_FILES`, `RAG_MAX_QUERY_RESULTS`, `RAG_MIN_SYNTHESIS_SCORE`, `RAG_NO_EVIDENCE_MESSAGE`, `RAG_NO_EVIDENCE_THRESHOLD`, `RAG_PARSE_TIMEOUT_SECONDS`, `RAG_QUERY_CONTEXT_CHARS`, `RAG_RETRIEVAL_MAX_PER_DOC`, `RAG_SYNTHESIS_MAX_PER_DOC`, `RAG_WEAK_EVIDENCE_MESSAGE`, `RAG_WEAK_MATCH_SCORE_CAP`, `SESSION_HEARTBEAT_STALE_SECONDS`, `SESSION_WATCHDOG_INTERVAL_SECONDS`, `SKILLS_APP_JS`, `SKILLS_EXTRA_CSS`, `SKILLS_INDEX_HTML`, `SKILL_REFRESH_MIN_INTERVAL_SECONDS`, `TOKEN_THRESHOLD`, `WEB_UI_OPTIONAL_FILES`, `WEB_UI_REQUIRED_FILES`; `config/paths.py`: `LLM_CONFIG_PATH`, `REPO_ROOT`, `_migrate_legacy_runtime_roots`; `config/settings.py`: `_to_bool_like`, `default_multimodal_capabilities`, `extract_auto_task_level_ceiling_setting`, `extract_read_context_policy_setting`, `extract_tool_memory_policy_setting`, `extract_user_memory_mode_setting`, `extract_web_search_enabled_setting`, `infer_model_multimodal_capabilities`, `merge_multimodal_capabilities`, `model_language_instruction`, `normalize_auto_task_level_ceiling`, `normalize_execution_mode`, `normalize_read_context_policy`, `normalize_tool_memory_policy`, `normalize_ui_language`, `normalize_ui_style`, `normalize_user_memory_mode`, `parse_capability_overrides`, `parse_llm_config_profiles`, `resolve_optional_file_path`, `resolve_web_ui_dir_path`; `llm/client.py`: `OllamaClient`; `llm/utils.py`: `extract_base_url`, `list_ollama_models_cached`; `mcp/driver.py`: `MCPManager`, `mcp_extract_server_configs`; `rag/ingestion.py`: `CodeIngestionService`, `RAGIngestionService`, `_rag_embed_batch`, `_rag_embed_text`, `_rag_mmr_select`, `_rag_query_variants`; `rag/parsers.py`: `CodeContentParser`, `RAGContentParser`, `normalize_rel_preview_path`, `preview_kind_for_path`; `rag/store.py`: `CodeLibraryStore`, `RAGLibraryStore`, `WikiStore`, `WorkflowMemoryStore`; `session/manager.py`: `SessionCreationLimitExceeded`, `SessionManager`; `session/state.py`: `SessionState`; `skills/store.py`: `SkillStore`, `_sanitize_skill_slug`, `analyze_skill_building_knowledge`, `ensure_runtime_skills`; `utils/crypto.py`: `CryptoBox`; `utils/files.py`: `_resolve_js_lib_asset_path`, `ensure_offline_js_libs`, `load_offline_js_lib_index`, `offline_js_lib_root`, `safe_path`, `try_read_text`; `utils/json_utils.py`: `TOOLS`, `extract_json_object_from_text`, `filter_tool_specs_for_runtime`, `json_dumps`, `parse_json_object`; `utils/media.py`: `guess_mime_from_name`; `utils/misc.py`: `DEFAULT_TIMEOUT_SECONDS`, `MAX_TIMEOUT_SECONDS`, `MIN_TIMEOUT_SECONDS`, `normalize_timeout_seconds`, `now_ts`; `utils/text.py`: `parse_front_matter`, `trim`
- Symbols:
  - `AppContext` (class, lines 80676-84892)

### `config/constants.py`

- Routed symbols: 453
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
  - `MCP_SERVICE_PORT_OFFSET` (constant, lines 158-158)
  - `IDE_PORT_OFFSET` (constant, lines 162-162)
  - `IDE_DEFAULT_PORT` (constant, lines 163-163)
  - `WEB_SEARCH_INDEX_DIRNAME` (constant, lines 164-164)
  - `DEFAULT_WEB_SEARCH_ENABLED` (constant, lines 165-165)
  - `USER_MEMORY_DIRNAME` (constant, lines 166-166)
  - `USER_MEMORY_DB_FILENAME` (constant, lines 167-167)
  - `USER_MEMORY_PROFILE_FILENAME` (constant, lines 168-168)
  - `USER_MEMORY_MODE_CHOICES` (constant, lines 169-169)
  - `DEFAULT_USER_MEMORY_MODE` (constant, lines 170-170)
  - `USER_MEMORY_WEAK_CAPSULE_CHARS` (constant, lines 171-171)
  - `USER_MEMORY_ON_CAPSULE_CHARS` (constant, lines 172-172)
  - `USER_MEMORY_CAPSULE_INJECT_CHARS` (constant, lines 176-176)
  - `USER_MEMORY_MAX_SUMMARY_CHARS` (constant, lines 177-177)
  - `USER_MEMORY_QUERY_LIMIT` (constant, lines 178-178)
  - `USER_MEMORY_DECAY_HALFLIFE_DAYS` (constant, lines 179-179)
  - `USER_MEMORY_PROFILE_SCHEMA_VERSION` (constant, lines 180-180)
  - `AGENT_WEB_SEARCH_USER_AGENT` (constant, lines 181-181)
  - `AGENT_WEB_SEARCH_DEFAULT_MAX_RESULTS` (constant, lines 182-182)
  - `AGENT_WEB_SEARCH_DEFAULT_MAX_PAGES` (constant, lines 183-183)
  - `AGENT_WEB_SEARCH_HARD_MAX_PAGES` (constant, lines 184-184)
  - `AGENT_WEB_SEARCH_DEFAULT_DEPTH` (constant, lines 185-185)
  - `AGENT_WEB_SEARCH_HARD_DEPTH` (constant, lines 186-186)
  - `AGENT_WEB_SEARCH_FETCH_TIMEOUT` (constant, lines 187-187)
  - `AGENT_WEB_SEARCH_TOOL_SOFT_TIMEOUT` (constant, lines 188-188)
  - `AGENT_WEB_SEARCH_MAX_PAGE_BYTES` (constant, lines 189-189)
  - `AGENT_WEB_SEARCH_MAX_TEXT_CHARS` (constant, lines 190-190)
  - `WEB_SEARCH_CONTEXT_REGISTRY_MAX` (constant, lines 191-191)
  - `WEB_SEARCH_CONTEXT_PROMPT_MAX_ITEMS` (constant, lines 192-192)
  - `WEB_SEARCH_CONTEXT_PROMPT_MAX_CHARS` (constant, lines 193-193)
  - `WEB_SEARCH_CONTEXT_NODE_MAX` (constant, lines 194-194)
  - `WEB_SEARCH_CONTEXT_URL_MAX` (constant, lines 195-195)
  - `RAG_CHUNK_CHARS` (constant, lines 196-196)
  - `RAG_CHUNK_OVERLAP` (constant, lines 197-197)
  - `RAG_MAX_CHUNKS_PER_DOC` (constant, lines 200-200)
  - `RAG_MAX_DOCUMENT_CHARS` (constant, lines 205-211)
  - `CODE_CHUNK_CHARS` (constant, lines 212-212)
  - `CODE_CHUNK_OVERLAP` (constant, lines 213-213)
  - `CODE_MAX_CHUNKS_PER_DOC` (constant, lines 214-214)
  - `RAG_MAX_QUERY_RESULTS` (constant, lines 215-215)
  - `RAG_HIGH_RECALL_POOL_MULTIPLIER` (constant, lines 216-216)
  - `RAG_HIGH_RECALL_MIN_POOL` (constant, lines 217-217)
  - `RAG_RETRIEVAL_MAX_PER_DOC` (constant, lines 218-218)
  - `RAG_BM25_K1` (constant, lines 222-222)
  - `RAG_BM25_B` (constant, lines 223-223)
  - `RAG_BM25_SATURATION` (constant, lines 230-230)
  - `RAG_SYMBOL_EXACT_BOOST` (constant, lines 234-234)
  - `RAG_INDEX_SNAPSHOT_FORMAT` (constant, lines 238-238)
  - `RAG_GRAPH_MAX_NODES` (constant, lines 239-239)
  - `RAG_TASK_HISTORY_LIMIT` (constant, lines 240-240)
  - `RAG_MODEL_MEDIA_MAX_BYTES` (constant, lines 241-241)
  - `RAG_MAX_IMPORT_FILES` (constant, lines 242-242)
  - `RAG_MAX_IMPORT_BATCH_ITEMS` (constant, lines 243-243)
  - `RAG_MAX_IMPORT_BATCH_BYTES` (constant, lines 244-244)
  - `RAG_PDF_IMAGE_LIMIT` (constant, lines 245-245)
  - `RAG_QUERY_CONTEXT_CHARS` (constant, lines 246-246)
  - `RAG_MAX_GLOBAL_COMMUNITIES` (constant, lines 247-247)
  - `RAG_MAX_COMMUNITY_MAP_SUPPORT` (constant, lines 248-248)
  - `RAG_INCLUDE_FILENAME_ENTITIES_DEFAULT` (constant, lines 249-249)
  - `RAG_DYNAMIC_NOISE_MIN_DOC_FREQ` (constant, lines 250-250)
  - `RAG_DYNAMIC_NOISE_MIN_COMMUNITY_FREQ` (constant, lines 251-251)
  - `RAG_DYNAMIC_NOISE_SOFT_DOC_RATIO` (constant, lines 252-252)
  - `RAG_DYNAMIC_NOISE_HARD_DOC_RATIO` (constant, lines 253-253)
  - `RAG_DYNAMIC_NOISE_SOFT_COMMUNITY_RATIO` (constant, lines 254-254)
  - `RAG_DYNAMIC_NOISE_HARD_COMMUNITY_RATIO` (constant, lines 255-255)
  - `RAG_MIN_SYNTHESIS_SCORE` (constant, lines 256-256)
  - `RAG_NO_EVIDENCE_THRESHOLD` (constant, lines 257-257)
  - `RAG_WEAK_MATCH_SCORE_CAP` (constant, lines 258-258)
  - `RAG_SYNTHESIS_MAX_PER_DOC` (constant, lines 259-259)
  - `RAG_WORKFLOW_ACCEPT_SCORE` (constant, lines 260-260)
  - `RAG_NO_EVIDENCE_MESSAGE` (constant, lines 261-261)
  - `RAG_CONTEXT_BUDGETS` (constant, lines 262-266)
  - `RAG_WEAK_EVIDENCE_MESSAGE` (constant, lines 267-267)
  - `RAG_DENSE_DEFAULT_ENABLED` (constant, lines 268-268)
  - `RAG_EMBEDDING_MODE_VALUES` (constant, lines 269-269)
  - `RAG_IMPORT_WORKER_COUNT` (constant, lines 270-273)
  - `CODE_IMPORT_WORKER_COUNT` (constant, lines 274-277)
  - `RAG_PARSE_TIMEOUT_SECONDS` (constant, lines 278-281)
  - `CODE_PARSE_TIMEOUT_SECONDS` (constant, lines 282-285)
  - `DEFAULT_CONTEXT_TOKEN_LIMIT` (constant, lines 286-286)
  - `TOKEN_THRESHOLD` (constant, lines 287-287)
  - `CONTEXT_AUTO_COMPACT_RESERVE_RATIO` (constant, lines 288-291)
  - `CONTEXT_ESTIMATE_SAFETY_MULTIPLIER` (constant, lines 292-295)
  - `CONTEXT_USAGE_CALIBRATION_MAX` (constant, lines 296-299)
  - `CONTEXT_ACTUAL_USAGE_RECENT_SECONDS` (constant, lines 300-303)
  - `LARGE_FILE_AUTO_PAGE_BYTES` (constant, lines 304-307)
  - `LARGE_FILE_AUTO_PAGE_LINES` (constant, lines 308-311)
  - `LARGE_SOURCE_UPLOAD_EXCERPT_CHARS` (constant, lines 312-315)
  - `CHAT_UPLOAD_PARSE_QUEUE_MAX` (constant, lines 316-319)
  - `CHAT_UPLOAD_PARSE_TIMEOUT_SECONDS` (constant, lines 320-323)
  - `CHAT_UPLOAD_INLINE_TEXT_BYTES` (constant, lines 324-327)
  - `CHAT_UPLOAD_PARSE_MAX_BYTES` (constant, lines 328-334)
  - `CHAT_UPLOAD_ZIP_ENTRY_MAX_BYTES` (constant, lines 335-341)
  - `CHAT_UPLOAD_TEXT_CONTEXT_CHARS` (constant, lines 342-345)
  - `CHAT_UPLOAD_PROMPT_MAX_FILES` (constant, lines 346-349)
  - `CHAT_UPLOAD_PROMPT_MAX_CHARS` (constant, lines 350-353)
  - `CHAT_UPLOAD_PROMPT_PER_FILE_CHARS` (constant, lines 354-357)
  - `CHAT_UPLOAD_FRONTEND_WAIT_MS` (constant, lines 358-361)
  - `CHAT_UPLOAD_AUTO_LIBRARY_INGEST` (constant, lines 362-365)
  - `CHAT_UPLOAD_INGEST_QUEUE_MAX` (constant, lines 366-369)
  - `SESSION_SUBMIT_LOCK_TIMEOUT_SECONDS` (constant, lines 370-373)
  - `SESSION_DEFERRED_START_QUEUE_MAX` (constant, lines 374-377)
  - `SESSION_WATCHDOG_INTERVAL_SECONDS` (constant, lines 378-381)
  - `SESSION_HEARTBEAT_STALE_SECONDS` (constant, lines 382-385)
  - `SESSION_LIST_DEFAULT_LIMIT` (constant, lines 386-389)
  - `IDLE_TIMEOUT` (constant, lines 390-390)
  - `POLL_INTERVAL` (constant, lines 391-391)
  - `SSE_HEARTBEAT_SECONDS` (constant, lines 392-392)
  - `MODEL_CALL_PROGRESS_DELAY` (constant, lines 393-393)
  - `MODEL_CALL_PROGRESS_INTERVAL` (constant, lines 394-394)
  - `RUN_COMPLETION_SUMMARY_ENABLED` (constant, lines 395-398)
  - `LLM_HTTP_RETRY_MAX_ATTEMPTS` (constant, lines 399-402)
  - `LLM_HTTP_RETRY_DELAY_SECONDS` (constant, lines 403-406)
  - `LLM_HTTP_RETRY_MAX_SECONDS` (constant, lines 407-410)
  - `LLM_HTTP_RETRY_404_ON_VLLM` (constant, lines 411-414)
  - `LLM_HTTP_RETRY_STATUSES` (constant, lines 415-415)
  - `MAX_AGENT_ROUNDS` (constant, lines 416-416)
  - `MIN_AGENT_ROUNDS` (constant, lines 417-417)
  - `MAX_AGENT_ROUNDS_CAP` (constant, lines 418-418)
  - `REPEATED_TOOL_LOOP_THRESHOLD` (constant, lines 419-419)
  - `BASH_READ_LOOP_THRESHOLD` (constant, lines 420-420)
  - `READ_FILE_LOOP_THRESHOLD` (constant, lines 421-421)
  - `READ_FILE_LOOP_DISTINCT_SOFT_LIMIT` (constant, lines 422-422)
  - `READ_FILE_COMPACT_PIN_DISTINCT` (constant, lines 423-423)
  - `READ_FILE_COMPACT_PIN_MAX_CHARS` (constant, lines 424-424)
  - `READ_CONTEXT_REGISTRY_MAX` (constant, lines 425-425)
  - `READ_CONTEXT_PROMPT_MAX_ITEMS` (constant, lines 426-426)
  - `READ_CONTEXT_PROMPT_MAX_CHARS` (constant, lines 427-427)
  - `READ_CONTEXT_SUMMARY_MAX_CHARS` (constant, lines 428-428)
  - `READ_CONTEXT_SHARED_MAX_ITEMS` (constant, lines 429-429)
  - `READ_CONTEXT_POLICY_CHOICES` (constant, lines 430-430)
  - `DEFAULT_READ_CONTEXT_POLICY` (constant, lines 431-431)
  - `TOOL_MEMORY_REGISTRY_MAX` (constant, lines 432-432)
  - `TOOL_MEMORY_PROMPT_MAX_ITEMS` (constant, lines 433-433)
  - `TOOL_MEMORY_PROMPT_MAX_CHARS` (constant, lines 434-434)
  - `TOOL_MEMORY_SUMMARY_MAX_CHARS` (constant, lines 435-435)
  - `TOOL_MEMORY_SHARED_MAX_ITEMS` (constant, lines 436-436)
  - `TOOL_MEMORY_COMPACT_PIN_DISTINCT` (constant, lines 437-437)
  - `TOOL_MEMORY_COMPACT_PIN_MAX_CHARS` (constant, lines 438-438)
  - `TOOL_MEMORY_POLICY_CHOICES` (constant, lines 439-439)
  - `DEFAULT_TOOL_MEMORY_POLICY` (constant, lines 440-440)
  - `DEFAULT_AUTO_TASK_LEVEL_CEILING` (constant, lines 441-441)
  - `HARD_BREAK_TOOL_ERROR_THRESHOLD` (constant, lines 442-442)
  - `HARD_BREAK_RECOVERY_ROUND_THRESHOLD` (constant, lines 443-443)
  - `FUSED_FAULT_BREAK_THRESHOLD` (constant, lines 444-444)
  - `STALL_SEVERITY_ESCALATION_THRESHOLD` (constant, lines 445-445)
  - `STALL_SEVERITY_WEIGHT_BASH_READ_LOOP` (constant, lines 446-446)
  - `STALL_SEVERITY_WEIGHT_REPEATED_TOOL` (constant, lines 447-447)
  - `STALL_SEVERITY_WEIGHT_FAULT` (constant, lines 448-448)
  - `STALL_SEVERITY_WEIGHT_RECOVERY_RETRY` (constant, lines 449-449)
  - `STALL_SEVERITY_WEIGHT_WATCHDOG` (constant, lines 450-450)
  - `STALL_SEVERITY_DECAY_ON_SUCCESS` (constant, lines 451-451)
  - `STALL_ESCALATION_MIN_LEVEL` (constant, lines 452-452)
  - `STALL_PLAN_SYNTHESIS_MAX_TOKENS` (constant, lines 453-453)
  - `STALL_ESCALATION_CONTEXT_MAX_CHARS` (constant, lines 454-454)
  - `MAX_RUN_SECONDS` (constant, lines 455-455)
  - `MIN_RUN_TIMEOUT_SECONDS` (constant, lines 456-456)
  - `MAX_RUN_TIMEOUT_SECONDS` (constant, lines 457-457)
  - `DEFAULT_REQUEST_TIMEOUT` (constant, lines 467-467)
  - `_SHELL_AUTO_CONFIRM_PATTERNS` (assignment, lines 470-483)
  - `MIN_SHELL_COMMAND_TIMEOUT_SECONDS` (constant, lines 484-484)
  - `MAX_SHELL_COMMAND_TIMEOUT_SECONDS` (constant, lines 485-485)
  - `DEFAULT_SHELL_COMMAND_TIMEOUT_SECONDS` (constant, lines 486-500)
  - `AUTO_CONTINUE_BUDGET_DEFAULT` (constant, lines 501-501)
  - `AGENT_MAX_OUTPUT_TOKENS` (constant, lines 502-502)
  - `OLLAMA_THINKING_TOOL_BUFFER` (constant, lines 503-503)
  - `WATCHDOG_INTENT_NO_TOOL_THRESHOLD` (constant, lines 504-504)
  - `WATCHDOG_REPEAT_NO_TOOL_THRESHOLD` (constant, lines 505-505)
  - `WATCHDOG_INTENT_NO_TOOL_THRESHOLD_SINGLE` (constant, lines 506-506)
  - `WATCHDOG_REPEAT_NO_TOOL_THRESHOLD_SINGLE` (constant, lines 507-507)
  - `WATCHDOG_STATE_STALL_THRESHOLD` (constant, lines 508-508)
  - `WATCHDOG_CONTEXT_STALL_THRESHOLD` (constant, lines 509-509)
  - `WATCHDOG_REPEAT_SIMILARITY_THRESHOLD` (constant, lines 510-510)
  - `WATCHDOG_CONTEXT_NEAR_RATIO` (constant, lines 511-511)
  - `WATCHDOG_MAX_DECOMPOSE_STEPS` (constant, lines 512-512)
  - `WATCHDOG_STEP_MAX_ATTEMPTS` (constant, lines 513-513)
  - `EMPTY_ACTION_MIN_CONTENT_CHARS` (constant, lines 514-514)
  - `EMPTY_ACTION_WAKEUP_RETRY_LIMIT` (constant, lines 515-515)
  - `THINKING_BUDGET_FORCE_RATIO` (constant, lines 516-516)
  - `_TOOL_TIMEOUT_MAP` (assignment, lines 518-535)
  - `_DEFAULT_TOOL_TIMEOUT` (assignment, lines 536-536)
  - `CONVERSATION_VISIBLE_TOOL_EVENTS` (constant, lines 537-547)
  - `PERSIST_ON_EVENT_TYPES` (constant, lines 548-562)
  - `PERSIST_EVENT_MIN_INTERVAL_SECONDS` (constant, lines 563-563)
  - `TRUNCATION_CONTINUATION_MAX_PASSES` (constant, lines 564-564)
  - `TRUNCATION_CONTINUATION_MAX_TOKENS` (constant, lines 565-565)
  - `TRUNCATION_CONTINUATION_TAIL_CHARS` (constant, lines 566-566)
  - `TRUNCATION_CONTINUATION_ECHO_CHARS` (constant, lines 567-567)
  - `TRUNCATION_OVERLAP_SCAN_CHARS` (constant, lines 568-568)
  - `TRUNCATION_PAIR_SCAN_CHARS` (constant, lines 569-569)
  - `TRUNCATION_LIVE_BUFFER_MAX_CHARS` (constant, lines 570-570)
  - `MIN_CONTEXT_TOKEN_LIMIT` (constant, lines 571-571)
  - `COMPACT_TIER1_PCT` (constant, lines 573-573)
  - `COMPACT_TIER2_PCT` (constant, lines 574-574)
  - `COMPACT_TIER3_PCT` (constant, lines 575-575)
  - `COMPACT_TIER1_ABS` (constant, lines 577-577)
  - `COMPACT_TIER2_ABS` (constant, lines 578-578)
  - `CONTEXT_COMPACT_INEFFECTIVE_COOLDOWN_SECONDS` (constant, lines 579-585)
  - `FILE_BUFFER_CONTENT_THRESHOLD` (constant, lines 587-587)
  - `FILE_BUFFER_MAX_FILES` (constant, lines 588-588)
  - `AGENT_MSG_LIMIT_TIER0` (constant, lines 590-590)
  - `AGENT_MSG_LIMIT_TIER1` (constant, lines 591-591)
  - `AGENT_MSG_LIMIT_TIER2` (constant, lines 592-592)
  - `AGENT_MSG_LIMIT_TIER3` (constant, lines 593-593)
  - `AGENT_CTX_LIMIT_TIER0` (constant, lines 594-594)
  - `AGENT_CTX_LIMIT_TIER1` (constant, lines 595-595)
  - `AGENT_CTX_LIMIT_TIER2` (constant, lines 596-596)
  - `AGENT_CTX_LIMIT_TIER3` (constant, lines 597-597)
  - `MANAGER_CTX_LIMIT_TIER0` (constant, lines 598-598)
  - `MANAGER_CTX_LIMIT_TIER1` (constant, lines 599-599)
  - `MANAGER_CTX_LIMIT_TIER2` (constant, lines 600-600)
  - `MANAGER_CTX_LIMIT_TIER3` (constant, lines 601-601)
  - `MAX_CONTEXT_ARCHIVE_SEGMENTS` (constant, lines 602-602)
  - `MAX_USER_BUBBLE_LOG` (constant, lines 604-604)
  - `MANAGER_INSTRUCTION_MAX_CHARS` (constant, lines 609-609)
  - `MANAGER_MOMENTUM_MAX_SKIPS` (constant, lines 615-615)
  - `EXPLORER_CODING_CAP` (constant, lines 620-620)
  - `MODEL_OUTPUT_RETRY_TIMES` (constant, lines 621-621)
  - `ARBITER_TRIGGER_MIN_CONTENT_CHARS` (constant, lines 622-622)
  - `ARBITER_VALID_PLANNING_STREAK_LIMIT` (constant, lines 623-623)
  - `ARBITER_DEFAULT_TIMEOUT_SECONDS` (constant, lines 624-624)
  - `ARBITER_DEFAULT_MAX_TOKENS` (constant, lines 625-625)
  - `ARBITER_DEFAULT_TEMPERATURE` (constant, lines 626-626)
  - `LIVE_INPUT_DELAY_WRITE_ROUNDS` (constant, lines 627-627)
  - `LIVE_INPUT_DELAY_TOOL_ROUNDS` (constant, lines 628-628)
  - `LIVE_INPUT_DELAY_NORMAL_ROUNDS` (constant, lines 629-629)
  - `LIVE_INPUT_MAX_INJECTIONS` (constant, lines 630-630)
  - `LIVE_INPUT_REINJECT_INTERVAL` (constant, lines 631-631)
  - `LIVE_INPUT_WEIGHT_BASE_DELAYED` (constant, lines 632-632)
  - `LIVE_INPUT_WEIGHT_BASE_NORMAL` (constant, lines 633-633)
  - `LIVE_INPUT_WEIGHT_STEP_DELAYED` (constant, lines 634-634)
  - `LIVE_INPUT_WEIGHT_STEP_NORMAL` (constant, lines 635-635)
  - `FINAL_SUMMARY_MIN_CHARS` (constant, lines 650-650)
  - `FINAL_SUMMARY_STRICT_MIN_CHARS` (constant, lines 651-651)
  - `RUNTIME_CONTROL_HINT_PREFIXES` (constant, lines 652-669)
  - `RETRY_RUNTIME_HINT_PREFIXES` (constant, lines 670-684)
  - `EXECUTION_MODE_SINGLE` (constant, lines 685-685)
  - `EXECUTION_MODE_SEQUENTIAL` (constant, lines 686-686)
  - `EXECUTION_MODE_SYNC` (constant, lines 687-687)
  - `EXECUTION_MODE_CHOICES` (constant, lines 688-692)
  - `AGENT_ROLES` (constant, lines 693-693)
  - `AGENT_BUBBLE_ROLES` (constant, lines 694-694)
  - `AGENT_ROLE_LABELS` (constant, lines 695-701)
  - `AGENT_ROLE_BUBBLE_COLORS` (constant, lines 702-708)
  - `BLACKBOARD_STATUSES` (constant, lines 709-718)
  - `TASK_COMPLEXITY_LEVELS` (constant, lines 719-719)
  - `TASK_COMPLEXITY_RANKS` (constant, lines 720-725)
  - `TASK_PROFILE_TYPES` (constant, lines 726-732)
  - `TASK_LEVEL_CHOICES` (constant, lines 733-733)
  - `TASK_SCALE_PREFERENCES` (constant, lines 734-734)
  - `SEMANTIC_CONFIDENCE_CHOICES` (constant, lines 735-735)
  - `TASK_LEVEL_POLICIES` (constant, lines 736-782)
  - `MANAGER_ROUTE_TARGETS` (constant, lines 783-783)
  - `BLACKBOARD_MAX_LOG_ENTRIES` (constant, lines 784-784)
  - `BLACKBOARD_MAX_TEXT` (constant, lines 785-785)
  - `BLACKBOARD_MEMORY_SHORT_MAX` (constant, lines 786-786)
  - `BLACKBOARD_MEMORY_MID_MAX_STEPS` (constant, lines 787-787)
  - `BLACKBOARD_MEMORY_MID_ITEMS_PER_STEP` (constant, lines 788-788)
  - `BLACKBOARD_MEMORY_LONG_MAX` (constant, lines 789-789)
  - `BLACKBOARD_MEMORY_INDEX_MAX` (constant, lines 790-790)
  - `SKILL_REFRESH_MIN_INTERVAL_SECONDS` (constant, lines 791-791)
  - `SKILL_PROMPT_MAX_ITEMS` (constant, lines 792-792)
  - `SKILL_PROMPT_MAX_CHARS` (constant, lines 793-793)
  - `SKILL_RUNTIME_CACHE_MAX_ENTRIES` (constant, lines 794-794)
  - `SKILL_RUNTIME_CACHE_MAX_BYTES` (constant, lines 795-795)
  - `AUTO_SKILLS_ROOT_CANDIDATES` (constant, lines 796-796)
  - `SKILL_DEFAULT_ATTACHMENT_GLOBS` (constant, lines 797-827)
  - `SKILL_INLINE_ATTACHMENT_MAX_FILES` (constant, lines 828-828)
  - `SKILL_INLINE_ATTACHMENT_MAX_CHARS` (constant, lines 829-829)
  - `SKILL_RESOURCE_MANIFEST_MAX_ITEMS` (constant, lines 830-830)
  - `SKILL_BODY_COMPACT_THRESHOLD_CHARS` (constant, lines 831-831)
  - `SKILL_BODY_PREVIEW_CHARS` (constant, lines 832-832)
  - `SKILLS_VIRTUAL_PREFIX` (constant, lines 833-833)
  - `SKILLS_EXTERNAL_MOUNT` (constant, lines 834-834)
  - `PLAN_MODE_ENABLED_LEVELS` (constant, lines 835-835)
  - `PLAN_MODE_FORCED_LEVELS` (constant, lines 836-836)
  - `PLAN_MODE_USER_CHOICES` (constant, lines 837-837)
  - `TASK_PHASES` (constant, lines 839-839)
  - `TASK_PHASE_ROUTING` (constant, lines 840-847)
  - `COMPLEXITY_KEYWORDS` (constant, lines 849-854)
  - `USER_COMPLEXITY_SIMPLE_TOKENS` (constant, lines 855-859)
  - `USER_COMPLEXITY_MODERATE_TOKENS` (constant, lines 860-864)
  - `USER_COMPLEXITY_COMPLEX_TOKENS` (constant, lines 865-869)
  - `USER_COMPLEXITY_EXPERT_TOKENS` (constant, lines 870-874)
  - `PLAN_MODE_EXPLORER_MAX_ROUNDS` (constant, lines 875-875)
  - `PLAN_MODE_SYNTHESIS_MAX_ATTEMPTS` (constant, lines 876-876)
  - `REVIEWER_DEBUG_MODE_MAX_ROUNDS` (constant, lines 878-878)
  - `REVIEWER_DEBUG_TOOL_ALLOWLIST` (constant, lines 879-883)
  - `EXPLORER_STALL_THRESHOLD` (constant, lines 884-884)
  - `DEVELOPER_EDIT_STALL_THRESHOLD` (constant, lines 885-885)
  - `ACCEPTANCE_GATE_STALL_THRESHOLD` (constant, lines 889-889)
  - `ACCEPTANCE_GATE_HARD_CEILING` (constant, lines 894-894)
  - `PLAN_MODE_MANAGER_SYNTHESIS_MAX_TOKENS` (constant, lines 895-895)
  - `PLAN_MODE_MAX_OPTIONS` (constant, lines 896-896)
  - `PLAN_FILE_RELATIVE_PATH` (constant, lines 897-897)
  - `PLAN_BUBBLE_MAX_CHARS` (constant, lines 898-898)
  - `PLAN_NOTICE_BODY_MAX_CHARS` (constant, lines 899-899)
  - `PLAN_MESSAGE_EVENT_MAX_CHARS` (constant, lines 900-900)
  - `PLAN_STEP_FULL_CONTENT_MAX_CHARS` (constant, lines 901-901)
  - `PLAN_MODE_RESEARCH_TOOL_ALLOWLIST` (constant, lines 902-909)
  - `FAILURE_LEDGER_MAX_FIXES` (constant, lines 910-910)
  - `FAILURE_LEDGER_MAX_COMPILE_ERRORS` (constant, lines 911-911)
  - `FAILURE_LEDGER_MAX_DELEGATIONS` (constant, lines 912-912)
  - `FAILURE_LEDGER_MAX_STALLS` (constant, lines 913-913)
  - `FAILURE_LEDGER_MAX_TOOL_FPS` (constant, lines 914-914)
  - `FAILURE_LEDGER_MAX_ERRORS` (constant, lines 915-915)
  - `ERROR_CATEGORY_DEFS` (constant, lines 918-955)
  - `CHECKPOINT_MAX_COUNT` (constant, lines 956-956)
  - `CHECKPOINT_INTERVAL_ROUNDS` (constant, lines 957-957)
  - `PERSISTED_ROUTES_MAX` (constant, lines 958-958)
  - `HTML_FRONTEND_REQUEST_KEYWORDS` (constant, lines 959-998)
  - `DEEP_RESEARCH_REQUEST_KEYWORDS` (constant, lines 999-1021)
  - `DEEP_RESEARCH_RETRIEVAL_KEYWORDS` (constant, lines 1022-1041)
  - `DEEP_RESEARCH_TEXT_ONLY_HINT_KEYWORDS` (constant, lines 1042-1059)
  - `DANGEROUS_PATTERNS` (constant, lines 1061-1061)
  - `VALID_MSG_TYPES` (constant, lines 1062-1068)
  - `SUPPORTED_UI_LANGUAGES` (constant, lines 1070-1075)
  - `UI_LANGUAGE_LABELS` (constant, lines 1076-1076)
  - `DEFAULT_UI_LANGUAGE` (constant, lines 1077-1077)
  - `UI_STYLE_CHOICES` (constant, lines 1078-1078)
  - `UI_STYLE_LABELS` (constant, lines 1079-1079)
  - `DEFAULT_UI_STYLE` (constant, lines 1080-1080)
  - `DEFAULT_WEB_UI_DIR` (constant, lines 1081-1081)
  - `DEFAULT_WEB_UI_CONFIG` (constant, lines 1082-1082)
  - `WEB_UI_REQUIRED_FILES` (constant, lines 1083-1090)
  - `WEB_UI_OPTIONAL_FILES` (constant, lines 1091-1091)
  - `IMAGE_EXTS` (constant, lines 1093-1106)
  - `IMAGE_FORMATS_NEED_CONVERSION` (constant, lines 1107-1107)
  - `IMAGE_SAFE_FORMATS` (constant, lines 1108-1108)
  - `AUDIO_EXTS` (constant, lines 1109-1119)
  - `VIDEO_EXTS` (constant, lines 1120-1130)
  - `CODE_PREVIEW_STAGE_MAX_BYTES` (constant, lines 1131-1131)
  - `CODE_PREVIEW_STAGE_MAX_ROWS` (constant, lines 1132-1132)
  - `CODE_PREVIEW_STAGE_MAX_PER_FILE` (constant, lines 1133-1133)
  - `CODE_PREVIEW_STAGE_MAX_TOTAL` (constant, lines 1134-1134)
  - `CODE_PREVIEW_DIFF_CONTEXT_LINES` (constant, lines 1135-1135)
  - `CODE_PREVIEW_DIFF_MERGE_GAP` (constant, lines 1136-1136)
  - `PREVIEW_DOWNLOAD_MAX_FILES` (constant, lines 1137-1137)
  - `PREVIEW_DOWNLOAD_MAX_BYTES` (constant, lines 1138-1138)
  - `FILES_TREE_DEFAULT_MAX_NODES` (constant, lines 1139-1139)
  - `FILES_TREE_DEFAULT_MAX_DEPTH` (constant, lines 1140-1140)
  - `FILES_TREE_SKIP_DIRS` (constant, lines 1141-1149)
  - `FILES_TREE_SKIP_REL_DIRS` (constant, lines 1150-1152)
  - `IDE_FILE_MAX_BYTES` (constant, lines 1153-1153)
  - `IDE_UPLOAD_MAX_BYTES` (constant, lines 1154-1154)
  - `IDE_UPLOAD_TOTAL_MAX_BYTES` (constant, lines 1155-1155)
  - `IDE_UPLOAD_MAX_ITEMS` (constant, lines 1156-1156)
  - `IDE_COMMAND_TIMEOUT_DEFAULT` (constant, lines 1157-1157)
  - `IDE_TREE_DEFAULT_MAX_NODES` (constant, lines 1158-1158)
  - `IDE_TREE_MAX_NODES` (constant, lines 1159-1159)
  - `IDE_TREE_SKIP_DIRS` (constant, lines 1160-1168)
  - `RENDER_FRAME_MAX_B64_CHARS` (constant, lines 1169-1169)
  - `RENDER_FRAME_MAX_POINTS` (constant, lines 1170-1170)
  - `RENDER_FRAME_MAX_LINES` (constant, lines 1171-1171)
  - `RENDER_FRAME_MAX_LINE_POINTS` (constant, lines 1172-1172)
  - `RENDER_FRAME_ACTIVITY_INTERVAL_SECONDS` (constant, lines 1173-1173)
  - `RAW_TOOLCALL_TEXT_FILTER_THRESHOLD` (constant, lines 1174-1174)
  - `ASSISTANT_TEXT_PERSIST_MAX_CHARS` (constant, lines 1175-1175)
  - `ASSISTANT_MESSAGE_EVENT_MAX_CHARS` (constant, lines 1176-1176)
  - `CODE_PREVIEW_EXTS` (constant, lines 1177-1302)
  - `CODE_PREVIEW_FILENAMES` (constant, lines 1303-1354)
  - `MEDIA_CAPABILITY_KEYS` (constant, lines 1355-1362)
  - `SAMPLE_IMAGE_PNG_B64` (constant, lines 1363-1366)
  - `SAMPLE_AUDIO_WAV_B64` (constant, lines 1367-1369)
  - `SAMPLE_VIDEO_MP4_B64` (constant, lines 1370-1372)
  - `OFFLINE_JS_LIB_CATALOG` (constant, lines 1374-1632)
  - `OFFLINE_JS_LIB_INDEX_FILE` (constant, lines 1633-1633)
  - `OFFLINE_JS_LIB_README_FILE` (constant, lines 1634-1634)
  - `BACKEND_I18N` (constant, lines 1820-1889)
  - `call_backend_i18n_en_update_l1891` (expression, lines 1891-1984)
  - `call_backend_i18n_zh_cn_update_l1985` (expression, lines 1985-2078)
  - `call_backend_i18n_zh_tw_update_l2079` (expression, lines 2079-2172)
  - `call_backend_i18n_ja_update_l2173` (expression, lines 2173-2266)
  - `OPENAI_COMPAT_PROVIDER_NAMES` (constant, lines 6259-6267)
  - `OPENAI_LIKE_PROVIDER_NAMES` (constant, lines 6269-6269)
  - `EFFORT_OFF` (constant, lines 6287-6287)
  - `EFFORT_LOW` (constant, lines 6288-6288)
  - `EFFORT_MEDIUM` (constant, lines 6289-6289)
  - `EFFORT_HIGH` (constant, lines 6290-6290)
  - `EFFORT_MAX` (constant, lines 6291-6291)
  - `EFFORT_LEVELS` (constant, lines 6292-6292)
  - `EFFORT_ORDER` (constant, lines 6293-6293)
  - `EFFORT_DEFAULT` (constant, lines 6294-6294)
  - `EFFORT_ANTHROPIC_BUDGET` (constant, lines 6297-6302)
  - `EFFORT_OPENAI_REASONING` (constant, lines 6304-6309)
  - `TASK_LEVEL_EFFORT` (constant, lines 6313-6319)
  - `ROLE_EFFORT_FLOOR` (constant, lines 6322-6325)
  - `COORDINATION_EFFORT` (constant, lines 6334-6334)
  - `TABULAR_PREVIEW_EXTS` (constant, lines 8004-8004)
  - `EXCEL_PREVIEW_EXTS` (constant, lines 8005-8005)
  - `PRESENTATION_PREVIEW_EXTS` (constant, lines 8006-8006)
  - `DOCUMENT_PREVIEW_EXTS` (constant, lines 8007-8007)
  - `EMBEDDED_SKILLS_ARCHIVE_B64` (constant, lines 8422-8422)
  - `EMBEDDED_SKILLS_ARCHIVE_SHA256` (constant, lines 8423-8423)
  - `EMBEDDED_SKILLS_ARCHIVE_FILES` (constant, lines 8424-8446)
  - `BUILTIN_CLAWHUB_SKILLS_VERSION` (constant, lines 11679-11679)
  - `EMBEDDED_CLAWHUB_SKILLS_ARCHIVE_B64` (constant, lines 11681-11925)
  - `MCP_BUILDER_SKILL_MD` (constant, lines 11974-12147)
  - `SKILL_PROTOCOL_LOCAL` (constant, lines 12180-12180)
  - `SKILL_PROTOCOL_CLAWHUB` (constant, lines 12181-12181)
  - `SKILL_PROTOCOL_HTTP_JSON` (constant, lines 12182-12182)
  - `SKILL_PROTOCOL_SPECS` (constant, lines 12184-12215)
  - `MCP_PROTOCOL_VERSION` (constant, lines 14157-14157)
  - `MCP_NAME_RE` (constant, lines 14158-14158)
  - `MCP_TOOL_PREFIX` (constant, lines 14159-14159)
  - `DEVELOPER_TOOL_DROP` (constant, lines 17540-17545)
  - `AGENT_TOOL_ALLOWLIST` (constant, lines 17547-17606)
  - `INDEX_HTML` (constant, lines 59905-60100)
  - `APP_CSS` (constant, lines 60102-60553)
  - `APP_JS` (constant, lines 60555-64889)
  - `APP_TS` (constant, lines 64891-64918)
  - `SKILLS_INDEX_HTML` (constant, lines 64920-65074)
  - `SKILLS_EXTRA_CSS` (constant, lines 65076-65171)
  - `SKILLS_APP_JS` (constant, lines 65173-65314)
  - `RAG_TERM_GROUPS` (constant, lines 65316-69948)
  - `RAG_RESEARCH_HINTS` (constant, lines 69949-69970)
  - `RAG_CODE_HINTS` (constant, lines 69971-69981)
  - `RAG_SHORT_TOKEN_ALLOWLIST` (constant, lines 69982-69997)
  - `RAG_EN_STOPWORDS` (constant, lines 69998-70070)
  - `RAG_ZH_STOPWORDS` (constant, lines 70071-70107)
  - `RAG_GENERIC_ENTITY_TERMS_EN` (constant, lines 70108-70186)
  - `RAG_GENERIC_ENTITY_TERMS_ZH` (constant, lines 70187-70229)
  - `RAG_STRUCTURAL_ENTITY_PATTERNS` (constant, lines 70230-70248)
  - `CODE_LIBRARY_IGNORED_DIRS` (constant, lines 70997-71002)
  - `CODE_LIBRARY_LANGUAGE_BY_EXT` (constant, lines 71003-71059)
  - `CODE_LIBRARY_SPECIAL_FILENAMES` (constant, lines 71060-71066)
  - `RAG_ADMIN_INDEX_HTML` (constant, lines 77918-78091)
  - `RAG_ADMIN_CSS` (constant, lines 78093-78183)
  - `RAG_ADMIN_JS` (constant, lines 78185-80273)
  - `CODE_ADMIN_INDEX_HTML` (constant, lines 80275-80286)
  - `CODE_ADMIN_CSS` (constant, lines 80287-80317)
  - `CODE_ADMIN_JS` (constant, lines 80318-80322)
  - `IDE_INDEX_HTML` (constant, lines 80324-80403)
  - `IDE_CSS` (constant, lines 80405-80471)
  - `IDE_JS` (constant, lines 80473-80665)

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
  - `detect_repo_root` (function, lines 3297-3311)
  - `REPO_ROOT` (constant, lines 3313-3313)

### `config/settings.py`

- Routed symbols: 49
- Cross-module imports: `config/constants.py`: `AUTO_SKILLS_ROOT_CANDIDATES`, `BACKEND_I18N`, `DEFAULT_AUTO_TASK_LEVEL_CEILING`, `DEFAULT_READ_CONTEXT_POLICY`, `DEFAULT_REQUEST_TIMEOUT`, `DEFAULT_SHELL_COMMAND_TIMEOUT_SECONDS`, `DEFAULT_TOOL_MEMORY_POLICY`, `DEFAULT_UI_LANGUAGE`, `DEFAULT_UI_STYLE`, `DEFAULT_USER_MEMORY_MODE`, `DEFAULT_WEB_SEARCH_ENABLED`, `DEFAULT_WEB_UI_CONFIG`, `DEFAULT_WEB_UI_DIR`, `EXECUTION_MODE_CHOICES`, `EXECUTION_MODE_SEQUENTIAL`, `EXECUTION_MODE_SINGLE`, `EXECUTION_MODE_SYNC`, `MAX_SHELL_COMMAND_TIMEOUT_SECONDS`, `MEDIA_CAPABILITY_KEYS`, `MIN_SHELL_COMMAND_TIMEOUT_SECONDS`, `READ_CONTEXT_POLICY_CHOICES`, `SUPPORTED_UI_LANGUAGES`, `TASK_COMPLEXITY_LEVELS`, `TASK_COMPLEXITY_RANKS`, `TASK_LEVEL_CHOICES`, `UI_LANGUAGE_LABELS`, `UI_STYLE_CHOICES`, `USER_COMPLEXITY_COMPLEX_TOKENS`, `USER_COMPLEXITY_EXPERT_TOKENS`, `USER_COMPLEXITY_MODERATE_TOKENS`, `USER_COMPLEXITY_SIMPLE_TOKENS`, `USER_MEMORY_MODE_CHOICES`; `config/paths.py`: `WORKDIR`; `llm/utils.py`: `_is_http_url`, `_resolve_local_path`, `complete_chat_endpoint`, `extract_base_url`, `is_openai_like_provider`, `normalize_openai_compat_provider_name`, `strip_thinking_content`; `skills/store.py`: `ensure_embedded_skills`; `utils/http.py`: `urlopen`; `utils/json_utils.py`: `TOOLS`, `filter_tool_specs_for_runtime`, `parse_json_object`; `utils/misc.py`: `MAX_TIMEOUT_SECONDS`, `MIN_TIMEOUT_SECONDS`, `detect_local_lan_ip_cached`, `normalize_timeout_seconds`, `now_ts`, `sanitize_profile_id`; `utils/text.py`: `trim`
- Symbols:
  - `normalize_ui_language` (function, lines 1718-1740)
  - `normalize_ui_style` (function, lines 1743-1760)
  - `supported_ui_languages_payload` (function, lines 1763-1764)
  - `normalize_execution_mode` (function, lines 1767-1786)
  - `model_language_instruction` (function, lines 1789-1817)
  - `backend_i18n_text` (function, lines 2269-2279)
  - `backend_role_label` (function, lines 2282-2286)
  - `_detect_os_shell_instruction` (function, lines 2289-2328)
  - `resolve_web_ui_dir_path` (function, lines 2330-2337)
  - `resolve_optional_file_path` (function, lines 2340-2347)
  - `resolve_skills_root_path` (function, lines 2350-2357)
  - `_count_skill_markdown_files` (function, lines 2360-2371)
  - `select_preferred_skills_root` (function, lines 2374-2408)
  - `load_web_ui_config_file` (function, lines 2411-2425)
  - `extract_show_upload_list_setting` (function, lines 2428-2442)
  - `extract_ui_style_setting` (function, lines 2445-2459)
  - `extract_js_lib_download_setting` (function, lines 2462-2481)
  - `extract_daily_session_limit_setting` (function, lines 2484-2527)
  - `extract_shell_command_timeout_setting` (function, lines 2530-2576)
  - `extract_context_token_limit_setting` (function, lines 2579-2611)
  - `normalize_auto_task_level_ceiling` (function, lines 2614-2633)
  - `extract_auto_task_level_ceiling_setting` (function, lines 2636-2663)
  - `normalize_read_context_policy` (function, lines 2666-2684)
  - `normalize_tool_memory_policy` (function, lines 2687-2688)
  - `extract_read_context_policy_setting` (function, lines 2691-2712)
  - `extract_tool_memory_policy_setting` (function, lines 2715-2736)
  - `default_multimodal_capabilities` (function, lines 2745-2753)
  - `_to_bool_like` (function, lines 2756-2766)
  - `extract_web_search_enabled_setting` (function, lines 2769-2779)
  - `normalize_user_memory_mode` (function, lines 2782-2810)
  - `user_memory_enabled_from_mode` (function, lines 2813-2814)
  - `extract_user_memory_mode_setting` (function, lines 2817-2854)
  - `set_web_search_enabled_on_runtime` (function, lines 2857-2870)
  - `infer_model_multimodal_capabilities` (function, lines 2873-2917)
  - `parse_capability_overrides` (function, lines 2920-2957)
  - `merge_multimodal_capabilities` (function, lines 2960-2967)
  - `parse_media_endpoints` (function, lines 2970-2984)
  - `extract_runtime_region_hint_setting` (function, lines 3163-3187)
  - `extract_runtime_timezone_hint_setting` (function, lines 3189-3205)
  - `runtime_environment_context_snapshot` (function, lines 3207-3255)
  - `runtime_environment_context_block` (function, lines 3257-3285)
  - `infer_user_complexity_value` (function, lines 6177-6193)
  - `normalize_task_complexity` (function, lines 6195-6223)
  - `task_complexity_rank` (function, lines 6225-6226)
  - `task_complexity_at_least` (function, lines 6228-6229)
  - `max_task_complexity` (function, lines 6231-6240)
  - `load_llm_config_from_source` (function, lines 6550-6584)
  - `parse_llm_config_profiles` (function, lines 6586-7215)
  - `looks_like_llm_config` (function, lines 7217-7293)

### `llm/client.py`

- Routed symbols: 2
- Cross-module imports: `config/constants.py`: `DEFAULT_REQUEST_TIMEOUT`, `LLM_HTTP_RETRY_404_ON_VLLM`, `LLM_HTTP_RETRY_DELAY_SECONDS`, `LLM_HTTP_RETRY_MAX_ATTEMPTS`, `LLM_HTTP_RETRY_MAX_SECONDS`, `LLM_HTTP_RETRY_STATUSES`, `OLLAMA_THINKING_TOOL_BUFFER`, `SAMPLE_AUDIO_WAV_B64`, `SAMPLE_IMAGE_PNG_B64`, `SAMPLE_VIDEO_MP4_B64`; `config/settings.py`: `default_multimodal_capabilities`, `infer_model_multimodal_capabilities`, `merge_multimodal_capabilities`, `parse_capability_overrides`, `parse_media_endpoints`; `llm/utils.py`: `complete_chat_endpoint`, `is_openai_compat_provider`, `is_openai_like_provider`, `normalize_openai_compat_provider_name`, `resolve_reasoning_payload`, `split_thinking_content`; `utils/http.py`: `urlopen`; `utils/json_utils.py`: `_is_valid_json_object`, `canonicalize_tool_name`, `json_dumps`, `parse_json_object`, `parse_tool_arguments`, `parse_tool_arguments_with_error`, `reconstruct_streamed_tool_args`; `utils/misc.py`: `MAX_TIMEOUT_SECONDS`, `MIN_TIMEOUT_SECONDS`, `make_id`, `normalize_timeout_seconds`, `now_ts`; `utils/text.py`: `trim`
- Symbols:
  - `OllamaError` (class, lines 15003-15023)
  - `OllamaClient` (class, lines 15025-17080)

### `llm/utils.py`

- Routed symbols: 28
- Cross-module imports: `config/constants.py`: `EFFORT_ANTHROPIC_BUDGET`, `EFFORT_DEFAULT`, `EFFORT_LEVELS`, `EFFORT_MAX`, `EFFORT_MEDIUM`, `EFFORT_OFF`, `EFFORT_OPENAI_REASONING`, `EFFORT_ORDER`, `OPENAI_COMPAT_PROVIDER_NAMES`, `OPENAI_LIKE_PROVIDER_NAMES`; `utils/http.py`: `urlopen`; `utils/json_utils.py`: `json_dumps`, `parse_json_object`; `utils/text.py`: `trim`
- Symbols:
  - `probe_ollama_environment` (function, lines 5861-5874)
  - `list_ollama_models` (function, lines 5876-5878)
  - `_OLLAMA_TAG_CACHE_LOCK` (assignment, lines 5880-5880)
  - `_OLLAMA_TAG_CACHE` (assignment, lines 5881-5881)
  - `list_ollama_models_cached` (function, lines 5891-5928)
  - `resolve_ollama_model` (function, lines 5930-5940)
  - `infer_thinking_model` (function, lines 5942-5944)
  - `split_thinking_content` (function, lines 5946-5989)
  - `strip_thinking_content` (function, lines 5991-5992)
  - `check_ollama_model_ready` (function, lines 5994-6018)
  - `list_loaded_ollama_models` (function, lines 6020-6033)
  - `wake_ollama_model` (function, lines 6035-6065)
  - `try_pull_ollama_model` (function, lines 6067-6085)
  - `ordered_model_candidates` (function, lines 6087-6105)
  - `pick_working_ollama_model` (function, lines 6107-6123)
  - `extract_base_url` (function, lines 6156-6164)
  - `complete_chat_endpoint` (function, lines 6166-6175)
  - `normalize_openai_compat_provider_name` (function, lines 6242-6257)
  - `is_openai_compat_provider` (function, lines 6271-6272)
  - `is_openai_like_provider` (function, lines 6274-6275)
  - `clamp_effort` (function, lines 6337-6346)
  - `model_reasoning_style` (function, lines 6349-6383)
  - `resolve_reasoning_payload` (function, lines 6386-6434)
  - `openai_compat_probe_headers` (function, lines 6436-6447)
  - `openai_compat_model_list_urls` (function, lines 6449-6481)
  - `extract_openai_compat_model_ids` (function, lines 6483-6516)
  - `_is_http_url` (function, lines 6525-6530)
  - `_resolve_local_path` (function, lines 6532-6548)

### `mcp/driver.py`

- Routed symbols: 8
- Cross-module imports: `config/constants.py`: `MCP_NAME_RE`, `MCP_PROTOCOL_VERSION`, `MCP_TOOL_PREFIX`; `utils/files.py`: `try_read_text`; `utils/json_utils.py`: `parse_json_object`
- Symbols:
  - `_MCP_DEFAULT_HANDSHAKE_TIMEOUT` (assignment, lines 14160-14160)
  - `_MCP_DEFAULT_CALL_TIMEOUT` (assignment, lines 14161-14161)
  - `_MCP_MAX_RESULT_CHARS` (assignment, lines 14162-14162)
  - `mcp_normalize_name` (function, lines 14165-14172)
  - `mcp_normalize_server_configs` (function, lines 14175-14257)
  - `mcp_extract_server_configs` (function, lines 14260-14277)
  - `MCPServerProcess` (class, lines 14280-14608)
  - `MCPManager` (class, lines 14611-15000)

### `rag/index.py`

- Routed symbols: 5
- Cross-module imports: `config/constants.py`: `RAG_BM25_B`, `RAG_BM25_K1`, `RAG_BM25_SATURATION`, `RAG_DYNAMIC_NOISE_HARD_COMMUNITY_RATIO`, `RAG_DYNAMIC_NOISE_HARD_DOC_RATIO`, `RAG_DYNAMIC_NOISE_MIN_COMMUNITY_FREQ`, `RAG_DYNAMIC_NOISE_MIN_DOC_FREQ`, `RAG_DYNAMIC_NOISE_SOFT_COMMUNITY_RATIO`, `RAG_DYNAMIC_NOISE_SOFT_DOC_RATIO`, `RAG_EN_STOPWORDS`, `RAG_GRAPH_MAX_NODES`, `RAG_INCLUDE_FILENAME_ENTITIES_DEFAULT`, `RAG_INDEX_SNAPSHOT_FORMAT`, `RAG_MAX_COMMUNITY_MAP_SUPPORT`, `RAG_MAX_GLOBAL_COMMUNITIES`, `RAG_MAX_QUERY_RESULTS`, `RAG_MIN_SYNTHESIS_SCORE`, `RAG_SYMBOL_EXACT_BOOST`, `RAG_WEAK_MATCH_SCORE_CAP`; `rag/ingestion.py`: `_rag_focused_excerpt`, `_rag_mmr_select`, `_rag_window_for_query`; `rag/parsers.py`: `_code_is_test_path`, `_rag_apply_filename_entity_policy`, `_rag_choose_community`, `_rag_classify_document`, `_rag_expand_tokens`, `_rag_extract_entities`, `_rag_filter_entities`, `_rag_tokenize`; `utils/misc.py`: `now_ts`; `utils/text.py`: `trim`
- Symbols:
  - `_code_module_name` (function, lines 71093-71107)
  - `_code_choose_community` (function, lines 71110-71117)
  - `_code_query_terms` (function, lines 71120-71132)
  - `TFGraphIDFIndex` (class, lines 72202-73876)
  - `CodeGraphIndex` (class, lines 77079-77562)

### `rag/ingestion.py`

- Routed symbols: 13
- Cross-module imports: `config/constants.py`: `CODE_IMPORT_WORKER_COUNT`, `CODE_LIBRARY_IGNORED_DIRS`, `CODE_PARSE_TIMEOUT_SECONDS`, `RAG_IMPORT_WORKER_COUNT`, `RAG_MAX_DOCUMENT_CHARS`, `RAG_MAX_IMPORT_BATCH_ITEMS`, `RAG_MAX_IMPORT_FILES`, `RAG_MODEL_MEDIA_MAX_BYTES`, `RAG_PARSE_TIMEOUT_SECONDS`, `RAG_PDF_IMAGE_LIMIT`, `RAG_RETRIEVAL_MAX_PER_DOC`; `config/settings.py`: `default_multimodal_capabilities`; `rag/parsers.py`: `CodeContentParser`, `RAGContentParser`, `_rag_expand_tokens`, `_rag_extract_entities`, `_rag_is_noise_token`, `_rag_safe_name`, `_rag_tokenize`; `rag/store.py`: `CodeLibraryStore`, `RAGLibraryStore`, `WikiStore`; `session/state.py`: `SessionState`; `utils/files.py`: `try_read_text`; `utils/json_utils.py`: `_read_json_file`, `_write_json_file`, `parse_json_object`; `utils/media.py`: `guess_mime_from_name`; `utils/misc.py`: `make_id`, `now_ts`; `utils/text.py`: `trim`
- Symbols:
  - `_rag_trigram_set` (function, lines 70461-70466)
  - `_rag_jaccard_sim` (function, lines 70469-70476)
  - `_rag_mmr_select` (function, lines 70479-70526)
  - `_rag_embed_text` (function, lines 70663-70684)
  - `_rag_embed_batch` (function, lines 70687-70693)
  - `_rag_window_for_query` (function, lines 70696-70708)
  - `_rag_focused_excerpt` (function, lines 70711-70751)
  - `_rag_query_variants` (function, lines 70754-70791)
  - `_rag_parse_segments` (function, lines 70794-70854)
  - `_rag_boundary_split` (function, lines 70857-70912)
  - `_rag_parse_file_worker` (function, lines 76183-76197)
  - `RAGIngestionService` (class, lines 76200-77076)
  - `CodeIngestionService` (class, lines 77831-77916)

### `rag/parsers.py`

- Routed symbols: 28
- Cross-module imports: `config/constants.py`: `AUDIO_EXTS`, `CODE_CHUNK_CHARS`, `CODE_CHUNK_OVERLAP`, `CODE_LIBRARY_LANGUAGE_BY_EXT`, `CODE_LIBRARY_SPECIAL_FILENAMES`, `CODE_MAX_CHUNKS_PER_DOC`, `CODE_PREVIEW_DIFF_CONTEXT_LINES`, `CODE_PREVIEW_DIFF_MERGE_GAP`, `CODE_PREVIEW_EXTS`, `CODE_PREVIEW_FILENAMES`, `CODE_PREVIEW_STAGE_MAX_ROWS`, `DOCUMENT_PREVIEW_EXTS`, `EXCEL_PREVIEW_EXTS`, `IMAGE_EXTS`, `PRESENTATION_PREVIEW_EXTS`, `RAG_CHUNK_CHARS`, `RAG_CHUNK_OVERLAP`, `RAG_CODE_HINTS`, `RAG_EN_STOPWORDS`, `RAG_GENERIC_ENTITY_TERMS_EN`, `RAG_GENERIC_ENTITY_TERMS_ZH`, `RAG_INCLUDE_FILENAME_ENTITIES_DEFAULT`, `RAG_MAX_CHUNKS_PER_DOC`, `RAG_MAX_DOCUMENT_CHARS`, `RAG_PARSE_TIMEOUT_SECONDS`, `RAG_PDF_IMAGE_LIMIT`, `RAG_RESEARCH_HINTS`, `RAG_SHORT_TOKEN_ALLOWLIST`, `RAG_STRUCTURAL_ENTITY_PATTERNS`, `RAG_TERM_GROUPS`, `RAG_ZH_STOPWORDS`, `TABULAR_PREVIEW_EXTS`, `VIDEO_EXTS`; `rag/ingestion.py`: `_rag_boundary_split`, `_rag_parse_segments`; `utils/files.py`: `_sha256_bytes`, `_sha256_file`; `utils/json_utils.py`: `parse_json_object`; `utils/media.py`: `guess_mime_from_name`; `utils/text.py`: `_focused_diff_rows_from_opcodes`, `_skip_row`, `trim`
- Symbols:
  - `normalize_rel_preview_path` (function, lines 7979-7990)
  - `is_code_preview_candidate` (function, lines 7993-8001)
  - `preview_kind_for_path` (function, lines 8010-8039)
  - `build_code_preview_rows` (function, lines 8042-8088)
  - `_rag_safe_name` (function, lines 70260-70263)
  - `_rag_detect_language` (function, lines 70266-70280)
  - `_rag_cjk_ngrams` (function, lines 70283-70295)
  - `_rag_is_noise_token` (function, lines 70298-70317)
  - `_rag_entity_allowed` (function, lines 70320-70332)
  - `_rag_filter_entities` (function, lines 70335-70349)
  - `_rag_filename_entity_aliases` (function, lines 70352-70385)
  - `_rag_apply_filename_entity_policy` (function, lines 70388-70418)
  - `_rag_choose_community` (function, lines 70421-70458)
  - `_rag_tokenize` (function, lines 70529-70580)
  - `_rag_expand_tokens` (function, lines 70583-70604)
  - `_rag_extract_entities` (function, lines 70607-70623)
  - `_rag_classify_document` (function, lines 70626-70660)
  - `_rag_chunk_text` (function, lines 70915-70992)
  - `_code_language_from_name` (function, lines 71069-71085)
  - `_code_is_test_path` (function, lines 71088-71090)
  - `_CallCollector` (class, lines 71135-71147)
  - `_ALGO_COMPLEXITY_RE` (assignment, lines 71150-71150)
  - `_ALGO_STEP_RE` (assignment, lines 71151-71151)
  - `_ALGO_MATH_VARS` (assignment, lines 71152-71152)
  - `_ALGO_DOC_KEYWORDS` (assignment, lines 71153-71153)
  - `_detect_algo_chunk` (function, lines 71156-71179)
  - `CodeContentParser` (class, lines 71182-71689)
  - `RAGContentParser` (class, lines 71692-72199)

### `rag/store.py`

- Routed symbols: 7
- Cross-module imports: `config/constants.py`: `CODE_CHUNK_CHARS`, `CODE_CHUNK_OVERLAP`, `CODE_MAX_CHUNKS_PER_DOC`, `DEFAULT_UI_LANGUAGE`, `EXECUTION_MODE_SYNC`, `RAG_INCLUDE_FILENAME_ENTITIES_DEFAULT`, `RAG_MAX_DOCUMENT_CHARS`, `RAG_MAX_QUERY_RESULTS`, `RAG_RETRIEVAL_MAX_PER_DOC`, `RAG_TASK_HISTORY_LIMIT`, `RAG_WEAK_MATCH_SCORE_CAP`, `RAG_WORKFLOW_ACCEPT_SCORE`, `USER_MEMORY_DB_FILENAME`, `USER_MEMORY_DECAY_HALFLIFE_DAYS`, `USER_MEMORY_DIRNAME`, `USER_MEMORY_MAX_SUMMARY_CHARS`, `USER_MEMORY_ON_CAPSULE_CHARS`, `USER_MEMORY_PROFILE_FILENAME`, `USER_MEMORY_PROFILE_SCHEMA_VERSION`, `USER_MEMORY_QUERY_LIMIT`, `USER_MEMORY_WEAK_CAPSULE_CHARS`; `config/settings.py`: `normalize_execution_mode`, `normalize_ui_language`, `normalize_user_memory_mode`; `rag/index.py`: `CodeGraphIndex`, `TFGraphIDFIndex`, `_code_choose_community`, `_code_module_name`; `rag/ingestion.py`: `_rag_focused_excerpt`, `_rag_mmr_select`, `_rag_window_for_query`; `rag/parsers.py`: `_code_is_test_path`, `_rag_apply_filename_entity_policy`, `_rag_choose_community`, `_rag_chunk_text`, `_rag_entity_allowed`, `_rag_expand_tokens`, `_rag_extract_entities`, `_rag_filter_entities`, `_rag_safe_name`, `_rag_tokenize`, `normalize_rel_preview_path`; `skills/store.py`: `_write_text_if_changed`; `utils/files.py`: `_sha256_bytes`, `_sha256_file`, `try_read_text`; `utils/json_utils.py`: `_read_json_file`, `_write_json_file`, `json_dumps`; `utils/media.py`: `guess_mime_from_name`; `utils/misc.py`: `make_id`, `now_ts`; `utils/text.py`: `trim`
- Symbols:
  - `RAGLibraryStore` (class, lines 73888-74462)
  - `WikiStore` (class, lines 74465-74994)
  - `UserMemoryStore` (class, lines 74997-75668)
  - `UserInteractionOptimizer` (class, lines 75671-75737)
  - `UserIntentProfiler` (class, lines 75740-75779)
  - `WorkflowMemoryStore` (class, lines 75782-76180)
  - `CodeLibraryStore` (class, lines 77565-77828)

### `rag/web_search.py`

- Routed symbols: 15
- Cross-module imports: `config/constants.py`: `AGENT_WEB_SEARCH_DEFAULT_DEPTH`, `AGENT_WEB_SEARCH_DEFAULT_MAX_PAGES`, `AGENT_WEB_SEARCH_DEFAULT_MAX_RESULTS`, `AGENT_WEB_SEARCH_FETCH_TIMEOUT`, `AGENT_WEB_SEARCH_HARD_DEPTH`, `AGENT_WEB_SEARCH_HARD_MAX_PAGES`, `AGENT_WEB_SEARCH_MAX_PAGE_BYTES`, `AGENT_WEB_SEARCH_MAX_TEXT_CHARS`, `AGENT_WEB_SEARCH_USER_AGENT`, `WEB_SEARCH_INDEX_DIRNAME`; `config/paths.py`: `WORKDIR`; `utils/http.py`: `urlopen`; `utils/json_utils.py`: `json_dumps`; `utils/misc.py`: `now_ts`; `utils/text.py`: `trim`
- Symbols:
  - `_agent_web_bool` (function, lines 3809-3814)
  - `_agent_web_int` (function, lines 3817-3822)
  - `_agent_web_host_is_local_name` (function, lines 3825-3829)
  - `_agent_web_ip_is_blocked` (function, lines 3832-3844)
  - `_agent_web_canonical_url` (function, lines 3847-3874)
  - `_agent_web_domain_to_seed` (function, lines 3877-3886)
  - `_agent_web_query_terms` (function, lines 3889-3904)
  - `_agent_web_query_domain_hints` (function, lines 3907-3945)
  - `_agent_web_query_needs_fresh_network` (function, lines 3948-3968)
  - `_agent_web_extract_text_snippet` (function, lines 3971-3986)
  - `AgentWebHTMLParser` (class, lines 3989-4066)
  - `_agent_web_decompress_bytes` (function, lines 4069-4090)
  - `_agent_web_charset_candidates` (function, lines 4092-4149)
  - `_agent_web_decode_text_bytes` (function, lines 4151-4184)
  - `AgentWebSearchEngine` (class, lines 4187-5254)

### `server/handlers.py`

- Routed symbols: 7
- Cross-module imports: `app/context.py`: `AppContext`; `config/constants.py`: `APP_VERSION`, `DEFAULT_AUTO_TASK_LEVEL_CEILING`, `DEFAULT_READ_CONTEXT_POLICY`, `DEFAULT_REQUEST_TIMEOUT`, `DEFAULT_SHELL_COMMAND_TIMEOUT_SECONDS`, `DEFAULT_TOOL_MEMORY_POLICY`, `DEFAULT_UI_LANGUAGE`, `DEFAULT_UI_STYLE`, `DEFAULT_USER_MEMORY_MODE`, `EXECUTION_MODE_CHOICES`, `EXECUTION_MODE_SYNC`, `FILES_TREE_DEFAULT_MAX_DEPTH`, `FILES_TREE_DEFAULT_MAX_NODES`, `IDE_TREE_DEFAULT_MAX_NODES`, `MIN_RUN_TIMEOUT_SECONDS`, `PLAN_MODE_USER_CHOICES`, `RAG_GRAPH_MAX_NODES`, `SESSION_LIST_DEFAULT_LIMIT`, `SSE_HEARTBEAT_SECONDS`, `TASK_COMPLEXITY_LEVELS`, `TASK_LEVEL_CHOICES`, `TASK_LEVEL_POLICIES`, `UI_STYLE_LABELS`; `config/paths.py`: `LLM_CONFIG_PATH`, `REPO_ROOT`, `WORKDIR`; `config/settings.py`: `_to_bool_like`, `infer_user_complexity_value`, `looks_like_llm_config`, `normalize_auto_task_level_ceiling`, `normalize_execution_mode`, `normalize_read_context_policy`, `normalize_task_complexity`, `normalize_tool_memory_policy`, `normalize_ui_language`, `normalize_ui_style`, `normalize_user_memory_mode`, `resolve_web_ui_dir_path`, `supported_ui_languages_payload`; `llm/utils.py`: `extract_base_url`, `extract_openai_compat_model_ids`, `list_ollama_models`, `normalize_openai_compat_provider_name`, `openai_compat_model_list_urls`, `openai_compat_probe_headers`; `rag/parsers.py`: `normalize_rel_preview_path`; `session/manager.py`: `SessionCreationLimitExceeded`, `SessionManager`; `session/state.py`: `SessionState`; `skills/store.py`: `analyze_skill_building_knowledge`; `utils/files.py`: `safe_path`, `try_read_text`; `utils/http.py`: `urlopen`; `utils/json_utils.py`: `json_dumps`, `parse_json_object`; `utils/media.py`: `guess_mime_from_name`; `utils/misc.py`: `now_ts`, `swallow_benign_socket_error`, `user_id_from_ip`; `utils/text.py`: `trim`
- Symbols:
  - `AgentHTTPServer` (class, lines 84903-84932)
  - `Handler` (class, lines 84936-85957)
  - `SkillsHandler` (class, lines 85959-86164)
  - `RagAdminHandler` (class, lines 86166-86334)
  - `CodeAdminHandler` (class, lines 86337-86523)
  - `IdeHandler` (class, lines 86526-86787)
  - `McpServiceHandler` (class, lines 86789-86936)

### `session/manager.py`

- Routed symbols: 2
- Cross-module imports: `config/constants.py`: `AGENT_MAX_OUTPUT_TOKENS`, `ARBITER_DEFAULT_MAX_TOKENS`, `ARBITER_DEFAULT_TEMPERATURE`, `ARBITER_DEFAULT_TIMEOUT_SECONDS`, `DEFAULT_AUTO_TASK_LEVEL_CEILING`, `DEFAULT_CONTEXT_TOKEN_LIMIT`, `DEFAULT_READ_CONTEXT_POLICY`, `DEFAULT_REQUEST_TIMEOUT`, `DEFAULT_SHELL_COMMAND_TIMEOUT_SECONDS`, `DEFAULT_TOOL_MEMORY_POLICY`, `DEFAULT_UI_LANGUAGE`, `DEFAULT_USER_MEMORY_MODE`, `DEFAULT_WEB_SEARCH_ENABLED`, `EXECUTION_MODE_SYNC`, `MAX_AGENT_ROUNDS`, `MAX_AGENT_ROUNDS_CAP`, `MAX_RUN_SECONDS`, `MAX_RUN_TIMEOUT_SECONDS`, `MAX_SHELL_COMMAND_TIMEOUT_SECONDS`, `MIN_AGENT_ROUNDS`, `MIN_CONTEXT_TOKEN_LIMIT`, `MIN_RUN_TIMEOUT_SECONDS`, `MIN_SHELL_COMMAND_TIMEOUT_SECONDS`, `SESSION_LIST_DEFAULT_LIMIT`, `TOKEN_THRESHOLD`; `config/paths.py`: `LLM_CONFIG_PATH`; `config/settings.py`: `_to_bool_like`, `extract_auto_task_level_ceiling_setting`, `extract_read_context_policy_setting`, `extract_tool_memory_policy_setting`, `extract_user_memory_mode_setting`, `extract_web_search_enabled_setting`, `infer_model_multimodal_capabilities`, `merge_multimodal_capabilities`, `normalize_auto_task_level_ceiling`, `normalize_execution_mode`, `normalize_read_context_policy`, `normalize_tool_memory_policy`, `normalize_ui_language`, `normalize_user_memory_mode`, `parse_capability_overrides`, `parse_llm_config_profiles`, `set_web_search_enabled_on_runtime`; `llm/client.py`: `OllamaClient`; `llm/utils.py`: `complete_chat_endpoint`, `extract_base_url`, `is_openai_compat_provider`, `list_ollama_models_cached`, `probe_ollama_environment`; `rag/store.py`: `UserIntentProfiler`, `UserInteractionOptimizer`, `UserMemoryStore`; `session/state.py`: `SessionState`; `utils/crypto.py`: `CryptoBox`; `utils/files.py`: `try_read_text`; `utils/json_utils.py`: `parse_json_object`; `utils/misc.py`: `make_id`, `normalize_timeout_seconds`, `now_ts`, `sanitize_profile_id`; `utils/text.py`: `trim`
- Symbols:
  - `SessionCreationLimitExceeded` (class, lines 2739-2742)
  - `SessionManager` (class, lines 58642-59903)

### `session/state.py`

- Routed symbols: 1
- Cross-module imports: `agent/background.py`: `BackgroundManager`; `agent/bus.py`: `MessageBus`; `agent/events.py`: `EventHub`; `agent/tasks.py`: `TaskManager`; `agent/todo.py`: `TodoManager`; `agent/worktree.py`: `WorktreeManager`; `config/constants.py`: `ACCEPTANCE_GATE_HARD_CEILING`, `ACCEPTANCE_GATE_STALL_THRESHOLD`, `AGENT_BUBBLE_ROLES`, `AGENT_CTX_LIMIT_TIER0`, `AGENT_CTX_LIMIT_TIER1`, `AGENT_CTX_LIMIT_TIER2`, `AGENT_CTX_LIMIT_TIER3`, `AGENT_MAX_OUTPUT_TOKENS`, `AGENT_MSG_LIMIT_TIER0`, `AGENT_MSG_LIMIT_TIER1`, `AGENT_MSG_LIMIT_TIER2`, `AGENT_MSG_LIMIT_TIER3`, `AGENT_ROLES`, `AGENT_TOOL_ALLOWLIST`, `AGENT_WEB_SEARCH_DEFAULT_DEPTH`, `AGENT_WEB_SEARCH_DEFAULT_MAX_PAGES`, `AGENT_WEB_SEARCH_DEFAULT_MAX_RESULTS`, `AGENT_WEB_SEARCH_HARD_DEPTH`, `AGENT_WEB_SEARCH_HARD_MAX_PAGES`, `AGENT_WEB_SEARCH_MAX_TEXT_CHARS`, `AGENT_WEB_SEARCH_TOOL_SOFT_TIMEOUT`, `ARBITER_DEFAULT_MAX_TOKENS`, `ARBITER_DEFAULT_TEMPERATURE`, `ARBITER_DEFAULT_TIMEOUT_SECONDS`, `ARBITER_TRIGGER_MIN_CONTENT_CHARS`, `ARBITER_VALID_PLANNING_STREAK_LIMIT`, `ASSISTANT_MESSAGE_EVENT_MAX_CHARS`, `ASSISTANT_TEXT_PERSIST_MAX_CHARS`, `AUDIO_EXTS`, `AUTO_CONTINUE_BUDGET_DEFAULT`, `BASH_READ_LOOP_THRESHOLD`, `BLACKBOARD_MAX_LOG_ENTRIES`, `BLACKBOARD_MAX_TEXT`, `BLACKBOARD_MEMORY_INDEX_MAX`, `BLACKBOARD_MEMORY_LONG_MAX`, `BLACKBOARD_MEMORY_MID_ITEMS_PER_STEP`, `BLACKBOARD_MEMORY_MID_MAX_STEPS`, `BLACKBOARD_MEMORY_SHORT_MAX`, `BLACKBOARD_STATUSES`, `CHAT_UPLOAD_AUTO_LIBRARY_INGEST`, `CHAT_UPLOAD_INGEST_QUEUE_MAX`, `CHAT_UPLOAD_INLINE_TEXT_BYTES`, `CHAT_UPLOAD_PARSE_MAX_BYTES`, `CHAT_UPLOAD_PARSE_QUEUE_MAX`, `CHAT_UPLOAD_PARSE_TIMEOUT_SECONDS`, `CHAT_UPLOAD_PROMPT_MAX_CHARS`, `CHAT_UPLOAD_PROMPT_MAX_FILES`, `CHAT_UPLOAD_PROMPT_PER_FILE_CHARS`, `CHAT_UPLOAD_TEXT_CONTEXT_CHARS`, `CHAT_UPLOAD_ZIP_ENTRY_MAX_BYTES`, `CHECKPOINT_INTERVAL_ROUNDS`, `CHECKPOINT_MAX_COUNT`, `CODE_PREVIEW_STAGE_MAX_BYTES`, `CODE_PREVIEW_STAGE_MAX_PER_FILE`, `CODE_PREVIEW_STAGE_MAX_ROWS`, `CODE_PREVIEW_STAGE_MAX_TOTAL`, `COMPACT_TIER1_ABS`, `COMPACT_TIER1_PCT`, `COMPACT_TIER2_ABS`, `COMPACT_TIER2_PCT`, `COMPACT_TIER3_PCT`, `CONTEXT_ACTUAL_USAGE_RECENT_SECONDS`, `CONTEXT_AUTO_COMPACT_RESERVE_RATIO`, `CONTEXT_COMPACT_INEFFECTIVE_COOLDOWN_SECONDS`, `CONTEXT_ESTIMATE_SAFETY_MULTIPLIER`, `CONTEXT_USAGE_CALIBRATION_MAX`, `CONVERSATION_VISIBLE_TOOL_EVENTS`, `COORDINATION_EFFORT`, `DANGEROUS_PATTERNS`, `DEEP_RESEARCH_REQUEST_KEYWORDS`, `DEEP_RESEARCH_RETRIEVAL_KEYWORDS`, `DEEP_RESEARCH_TEXT_ONLY_HINT_KEYWORDS`, `DEFAULT_AUTO_TASK_LEVEL_CEILING`, `DEFAULT_CONTEXT_TOKEN_LIMIT`, `DEFAULT_READ_CONTEXT_POLICY`, `DEFAULT_REQUEST_TIMEOUT`, `DEFAULT_SHELL_COMMAND_TIMEOUT_SECONDS`, `DEFAULT_TOOL_MEMORY_POLICY`, `DEFAULT_UI_LANGUAGE`, `DEFAULT_USER_MEMORY_MODE`, `DEFAULT_WEB_SEARCH_ENABLED`, `DEVELOPER_EDIT_STALL_THRESHOLD`, `EFFORT_DEFAULT`, `EFFORT_MAX`, `EFFORT_OFF`, `EFFORT_ORDER`, `EMPTY_ACTION_MIN_CONTENT_CHARS`, `EMPTY_ACTION_WAKEUP_RETRY_LIMIT`, `ERROR_CATEGORY_DEFS`, `EXECUTION_MODE_CHOICES`, `EXECUTION_MODE_SEQUENTIAL`, `EXECUTION_MODE_SINGLE`, `EXECUTION_MODE_SYNC`, `EXPLORER_CODING_CAP`, `EXPLORER_STALL_THRESHOLD`, `FAILURE_LEDGER_MAX_COMPILE_ERRORS`, `FAILURE_LEDGER_MAX_DELEGATIONS`, `FAILURE_LEDGER_MAX_ERRORS`, `FAILURE_LEDGER_MAX_FIXES`, `FAILURE_LEDGER_MAX_STALLS`, `FAILURE_LEDGER_MAX_TOOL_FPS`, `FILES_TREE_DEFAULT_MAX_DEPTH`, `FILES_TREE_DEFAULT_MAX_NODES`, `FILES_TREE_SKIP_DIRS`, `FILES_TREE_SKIP_REL_DIRS`, `FILE_BUFFER_CONTENT_THRESHOLD`, `FILE_BUFFER_MAX_FILES`, `FINAL_SUMMARY_MIN_CHARS`, `FINAL_SUMMARY_STRICT_MIN_CHARS`, `FUSED_FAULT_BREAK_THRESHOLD`, `HARD_BREAK_RECOVERY_ROUND_THRESHOLD`, `HARD_BREAK_TOOL_ERROR_THRESHOLD`, `HTML_FRONTEND_REQUEST_KEYWORDS`, `IMAGE_EXTS`, `IMAGE_FORMATS_NEED_CONVERSION`, `LARGE_FILE_AUTO_PAGE_BYTES`, `LARGE_FILE_AUTO_PAGE_LINES`, `LARGE_SOURCE_UPLOAD_EXCERPT_CHARS`, `LIVE_INPUT_DELAY_NORMAL_ROUNDS`, `LIVE_INPUT_DELAY_TOOL_ROUNDS`, `LIVE_INPUT_DELAY_WRITE_ROUNDS`, `LIVE_INPUT_MAX_INJECTIONS`, `LIVE_INPUT_REINJECT_INTERVAL`, `LIVE_INPUT_WEIGHT_BASE_DELAYED`, `LIVE_INPUT_WEIGHT_BASE_NORMAL`, `LIVE_INPUT_WEIGHT_STEP_DELAYED`, `LIVE_INPUT_WEIGHT_STEP_NORMAL`, `LONG_OUTPUT_LISTING_OFFLOAD_CHARS`, `LONG_OUTPUT_MODEL_PAGE_CHARS`, `LONG_OUTPUT_READ_PAGE_LINES`, `LONG_OUTPUT_TEMP_MAX_FILES`, `LONG_OUTPUT_UI_PAGE_CHARS`, `LONG_OUTPUT_UI_PREVIEW_MAX_PAGES`, `MANAGER_CTX_LIMIT_TIER0`, `MANAGER_CTX_LIMIT_TIER1`, `MANAGER_CTX_LIMIT_TIER2`, `MANAGER_CTX_LIMIT_TIER3`, `MANAGER_INSTRUCTION_MAX_CHARS`, `MANAGER_MOMENTUM_MAX_SKIPS`, `MANAGER_ROUTE_TARGETS`, `MAX_AGENT_ROUNDS`, `MAX_AGENT_ROUNDS_CAP`, `MAX_CONTEXT_ARCHIVE_SEGMENTS`, `MAX_RUN_SECONDS`, `MAX_RUN_TIMEOUT_SECONDS`, `MAX_SHELL_COMMAND_TIMEOUT_SECONDS`, `MAX_USER_BUBBLE_LOG`, `MCP_TOOL_PREFIX`, `MIN_AGENT_ROUNDS`, `MIN_CONTEXT_TOKEN_LIMIT`, `MIN_RUN_TIMEOUT_SECONDS`, `MIN_SHELL_COMMAND_TIMEOUT_SECONDS`, `MODEL_CALL_PROGRESS_DELAY`, `MODEL_CALL_PROGRESS_INTERVAL`, `MODEL_OUTPUT_RETRY_TIMES`, `PERSISTED_ROUTES_MAX`, `PERSIST_EVENT_MIN_INTERVAL_SECONDS`, `PERSIST_ON_EVENT_TYPES`, `PLAN_BUBBLE_MAX_CHARS`, `PLAN_FILE_RELATIVE_PATH`, `PLAN_MESSAGE_EVENT_MAX_CHARS`, `PLAN_MODE_ENABLED_LEVELS`, `PLAN_MODE_EXPLORER_MAX_ROUNDS`, `PLAN_MODE_MANAGER_SYNTHESIS_MAX_TOKENS`, `PLAN_MODE_MAX_OPTIONS`, `PLAN_MODE_RESEARCH_TOOL_ALLOWLIST`, `PLAN_MODE_SYNTHESIS_MAX_ATTEMPTS`, `PLAN_MODE_USER_CHOICES`, `PLAN_NOTICE_BODY_MAX_CHARS`, `PLAN_STEP_FULL_CONTENT_MAX_CHARS`, `PREVIEW_DOWNLOAD_MAX_BYTES`, `PREVIEW_DOWNLOAD_MAX_FILES`, `READ_CONTEXT_PROMPT_MAX_CHARS`, `READ_CONTEXT_PROMPT_MAX_ITEMS`, `READ_CONTEXT_REGISTRY_MAX`, `READ_CONTEXT_SHARED_MAX_ITEMS`, `READ_CONTEXT_SUMMARY_MAX_CHARS`, `READ_FILE_COMPACT_PIN_DISTINCT`, `READ_FILE_COMPACT_PIN_MAX_CHARS`, `READ_FILE_DEFAULT_MAX_CHARS`, `READ_FILE_HARD_MAX_CHARS`, `READ_FILE_LOOP_DISTINCT_SOFT_LIMIT`, `READ_FILE_LOOP_THRESHOLD`, `READ_FILE_OVERVIEW_HEAD_LINES`, `READ_FILE_SEARCH_MAX_MATCHES`, `RENDER_FRAME_ACTIVITY_INTERVAL_SECONDS`, `RENDER_FRAME_MAX_B64_CHARS`, `RENDER_FRAME_MAX_LINES`, `RENDER_FRAME_MAX_LINE_POINTS`, `RENDER_FRAME_MAX_POINTS`, `REPEATED_TOOL_LOOP_THRESHOLD`, `RETRY_RUNTIME_HINT_PREFIXES`, `REVIEWER_DEBUG_MODE_MAX_ROUNDS`, `ROLE_EFFORT_FLOOR`, `RUNTIME_CONTROL_HINT_PREFIXES`, `RUN_COMPLETION_SUMMARY_ENABLED`, `SEMANTIC_CONFIDENCE_CHOICES`, `SESSION_DEFERRED_START_QUEUE_MAX`, `SESSION_HEARTBEAT_STALE_SECONDS`, `SESSION_SUBMIT_LOCK_TIMEOUT_SECONDS`, `SKILLS_VIRTUAL_PREFIX`, `SKILL_REFRESH_MIN_INTERVAL_SECONDS`, `SKILL_RUNTIME_CACHE_MAX_BYTES`, `SKILL_RUNTIME_CACHE_MAX_ENTRIES`, `STALL_ESCALATION_CONTEXT_MAX_CHARS`, `STALL_ESCALATION_MIN_LEVEL`, `STALL_PLAN_SYNTHESIS_MAX_TOKENS`, `STALL_SEVERITY_DECAY_ON_SUCCESS`, `STALL_SEVERITY_ESCALATION_THRESHOLD`, `STALL_SEVERITY_WEIGHT_BASH_READ_LOOP`, `STALL_SEVERITY_WEIGHT_FAULT`, `STALL_SEVERITY_WEIGHT_RECOVERY_RETRY`, `STALL_SEVERITY_WEIGHT_REPEATED_TOOL`, `STALL_SEVERITY_WEIGHT_WATCHDOG`, `TASK_COMPLEXITY_LEVELS`, `TASK_LEVEL_CHOICES`, `TASK_LEVEL_EFFORT`, `TASK_LEVEL_POLICIES`, `TASK_PHASE_ROUTING`, `TASK_PROFILE_TYPES`, `TASK_SCALE_PREFERENCES`, `THINKING_BUDGET_FORCE_RATIO`, `TOKEN_THRESHOLD`, `TOOL_MEMORY_COMPACT_PIN_DISTINCT`, `TOOL_MEMORY_COMPACT_PIN_MAX_CHARS`, `TOOL_MEMORY_PROMPT_MAX_CHARS`, `TOOL_MEMORY_PROMPT_MAX_ITEMS`, `TOOL_MEMORY_REGISTRY_MAX`, `TOOL_MEMORY_SHARED_MAX_ITEMS`, `TOOL_MEMORY_SUMMARY_MAX_CHARS`, `TRUNCATION_CONTINUATION_ECHO_CHARS`, `TRUNCATION_CONTINUATION_MAX_PASSES`, `TRUNCATION_CONTINUATION_MAX_TOKENS`, `TRUNCATION_CONTINUATION_TAIL_CHARS`, `TRUNCATION_LIVE_BUFFER_MAX_CHARS`, `TRUNCATION_OVERLAP_SCAN_CHARS`, `TRUNCATION_PAIR_SCAN_CHARS`, `USER_MEMORY_CAPSULE_INJECT_CHARS`, `USER_MEMORY_ON_CAPSULE_CHARS`, `VIDEO_EXTS`, `WATCHDOG_CONTEXT_NEAR_RATIO`, `WATCHDOG_CONTEXT_STALL_THRESHOLD`, `WATCHDOG_INTENT_NO_TOOL_THRESHOLD`, `WATCHDOG_INTENT_NO_TOOL_THRESHOLD_SINGLE`, `WATCHDOG_MAX_DECOMPOSE_STEPS`, `WATCHDOG_REPEAT_NO_TOOL_THRESHOLD`, `WATCHDOG_REPEAT_NO_TOOL_THRESHOLD_SINGLE`, `WATCHDOG_REPEAT_SIMILARITY_THRESHOLD`, `WATCHDOG_STATE_STALL_THRESHOLD`, `WATCHDOG_STEP_MAX_ATTEMPTS`, `WEB_SEARCH_CONTEXT_NODE_MAX`, `WEB_SEARCH_CONTEXT_PROMPT_MAX_CHARS`, `WEB_SEARCH_CONTEXT_PROMPT_MAX_ITEMS`, `WEB_SEARCH_CONTEXT_REGISTRY_MAX`, `WEB_SEARCH_CONTEXT_URL_MAX`, `WEB_SEARCH_INDEX_DIRNAME`, `_DEFAULT_TOOL_TIMEOUT`, `_SHELL_AUTO_CONFIRM_PATTERNS`, `_TOOL_TIMEOUT_MAP`; `config/paths.py`: `WORKDIR`; `config/settings.py`: `_detect_os_shell_instruction`, `_to_bool_like`, `backend_i18n_text`, `backend_role_label`, `default_multimodal_capabilities`, `extract_auto_task_level_ceiling_setting`, `extract_runtime_region_hint_setting`, `extract_runtime_timezone_hint_setting`, `extract_user_memory_mode_setting`, `extract_web_search_enabled_setting`, `infer_model_multimodal_capabilities`, `infer_user_complexity_value`, `looks_like_llm_config`, `max_task_complexity`, `merge_multimodal_capabilities`, `model_language_instruction`, `normalize_auto_task_level_ceiling`, `normalize_execution_mode`, `normalize_read_context_policy`, `normalize_task_complexity`, `normalize_tool_memory_policy`, `normalize_ui_language`, `normalize_user_memory_mode`, `parse_capability_overrides`, `parse_llm_config_profiles`, `runtime_environment_context_block`, `runtime_environment_context_snapshot`, `task_complexity_at_least`, `task_complexity_rank`; `llm/client.py`: `OllamaClient`, `OllamaError`; `llm/utils.py`: `clamp_effort`, `complete_chat_endpoint`, `extract_base_url`, `is_openai_compat_provider`, `list_loaded_ollama_models`, `list_ollama_models`, `list_ollama_models_cached`, `probe_ollama_environment`, `resolve_ollama_model`, `split_thinking_content`, `strip_thinking_content`, `wake_ollama_model`; `mcp/driver.py`: `MCPManager`, `mcp_extract_server_configs`; `rag/parsers.py`: `CodeContentParser`, `build_code_preview_rows`, `is_code_preview_candidate`, `normalize_rel_preview_path`, `preview_kind_for_path`; `rag/web_search.py`: `AgentWebSearchEngine`, `_agent_web_bool`, `_agent_web_extract_text_snippet`, `_agent_web_query_terms`; `skills/store.py`: `SkillStore`, `ensure_runtime_skills`; `utils/compress.py`: `compress_text_blob`, `decompress_text_blob`; `utils/crypto.py`: `CryptoBox`; `utils/errors.py`: `CircuitBreakerTriggered`, `EmptyActionError`; `utils/files.py`: `_normalize_external_js_url`, `_safe_js_filename`, `cache_external_js_url`, `ensure_offline_js_libs`, `is_external_js_src`, `load_offline_js_lib_index`, `match_offline_js_catalog_by_url`, `offline_js_lib_root`, `safe_path`, `try_read_text`; `utils/http.py`: `urlopen`; `utils/json_utils.py`: `TOOLS`, `TOOL_REQUIRED_ARGS`, `canonicalize_tool_name`, `extract_json_object_from_text`, `filter_tool_specs_for_runtime`, `json_dumps`, `parse_json_object`, `parse_tool_arguments_with_error`, `repair_truncated_json_object`, `tool_def`; `utils/media.py`: `_convert_image_to_safe_format`, `guess_ext_from_mime`, `guess_mime_from_name`; `utils/misc.py`: `MAX_TIMEOUT_SECONDS`, `MIN_TIMEOUT_SECONDS`, `is_benign_socket_error`, `make_id`, `normalize_timeout_seconds`, `now_ts`, `sanitize_profile_id`; `utils/text.py`: `MAX_TOOL_OUTPUT`, `_fmt_export_ts`, `_html_esc`, `_text_to_minimal_pdf`, `display_clean`, `extract_todo_rows_from_text`, `filter_runtime_noise_lines`, `make_numbered_diff`, `make_unified_diff`, `normalize_embedded_newlines`, `normalize_work_text`, `parse_front_matter`, `render_numbered_diff_text`, `short_title_from`, `split_structured_todo_content`, `split_todo_status_text`, `trim`
- Symbols:
  - `SessionState` (class, lines 17617-58640)

### `skills/store.py`

- Routed symbols: 28
- Cross-module imports: `config/constants.py`: `BUILTIN_CLAWHUB_SKILLS_VERSION`, `EMBEDDED_CLAWHUB_SKILLS_ARCHIVE_B64`, `EMBEDDED_SKILLS_ARCHIVE_B64`, `EMBEDDED_SKILLS_ARCHIVE_FILES`, `EMBEDDED_SKILLS_ARCHIVE_SHA256`, `MCP_BUILDER_SKILL_MD`, `SKILLS_EXTERNAL_MOUNT`, `SKILLS_VIRTUAL_PREFIX`, `SKILL_BODY_COMPACT_THRESHOLD_CHARS`, `SKILL_BODY_PREVIEW_CHARS`, `SKILL_DEFAULT_ATTACHMENT_GLOBS`, `SKILL_INLINE_ATTACHMENT_MAX_CHARS`, `SKILL_INLINE_ATTACHMENT_MAX_FILES`, `SKILL_PROMPT_MAX_CHARS`, `SKILL_PROMPT_MAX_ITEMS`, `SKILL_PROTOCOL_CLAWHUB`, `SKILL_PROTOCOL_HTTP_JSON`, `SKILL_PROTOCOL_LOCAL`, `SKILL_PROTOCOL_SPECS`, `SKILL_REFRESH_MIN_INTERVAL_SECONDS`, `SKILL_RESOURCE_MANIFEST_MAX_ITEMS`; `config/paths.py`: `WORKDIR`; `llm/utils.py`: `_is_http_url`; `utils/files.py`: `_render_offline_js_catalog_md`, `safe_path`, `try_read_text`; `utils/http.py`: `urlopen`; `utils/json_utils.py`: `json_dumps`, `parse_json_object`; `utils/misc.py`: `_meta_string_list`, `_module_exists`, `now_ts`; `utils/text.py`: `parse_front_matter`, `trim`
- Symbols:
  - `ensure_embedded_skills_at_root` (function, lines 8449-8512)
  - `ensure_embedded_skills` (function, lines 8515-8516)
  - `detect_upload_parser_capabilities` (function, lines 8524-8539)
  - `_render_cap_markdown` (function, lines 8541-8555)
  - `_write_text_if_changed` (function, lines 8557-8562)
  - `ensure_generated_document_skills` (function, lines 8564-8652)
  - `ensure_generated_image_coding_feedback_skill` (function, lines 8654-8753)
  - `_skill_knowledge_files` (function, lines 8755-8774)
  - `analyze_skill_building_knowledge` (function, lines 8776-8830)
  - `_sanitize_skill_slug` (function, lines 8832-8834)
  - `_build_skills_gen_skill_content` (function, lines 8836-8867)
  - `ensure_generated_skills_gen_skill` (function, lines 8869-8873)
  - `ensure_generated_execution_recovery_skill` (function, lines 8875-8953)
  - `ensure_generated_systematic_debugging_skill` (function, lines 8955-9227)
  - `ensure_generated_code_engineering_mastery_skill` (function, lines 9229-9347)
  - `ensure_generated_smart_file_navigation_skill` (function, lines 9349-9464)
  - `ensure_generated_html_frontend_report_skills` (function, lines 9466-9673)
  - `ensure_generated_deep_research_skills` (function, lines 9675-9943)
  - `ensure_generated_research_scientific_skills` (function, lines 9945-10581)
  - `ensure_generated_rag_mastery_skills` (function, lines 10587-10883)
  - `ensure_generated_multimodal_comprehension_skills` (function, lines 10889-11578)
  - `ensure_generated_runtime_skills_manifest` (function, lines 11581-11613)
  - `ensure_generated_agent_web_search_skill` (function, lines 11616-11676)
  - `ensure_embedded_clawhub_skills` (function, lines 11935-11972)
  - `ensure_generated_mcp_builder_skill` (function, lines 12149-12159)
  - `ensure_runtime_skills` (function, lines 12161-12178)
  - `_BUILTIN_SKILLS` (assignment, lines 12220-12324)
  - `SkillStore` (class, lines 12333-13627)

### `utils/compress.py`

- Routed symbols: 2
- Cross-module imports: none
- Symbols:
  - `compress_text_blob` (function, lines 5420-5425)
  - `decompress_text_blob` (function, lines 5427-5435)

### `utils/crypto.py`

- Routed symbols: 1
- Cross-module imports: `utils/json_utils.py`: `json_dumps`
- Symbols:
  - `CryptoBox` (class, lines 7303-7420)

### `utils/errors.py`

- Routed symbols: 2
- Cross-module imports: none
- Symbols:
  - `EmptyActionError` (class, lines 5884-5885)
  - `CircuitBreakerTriggered` (class, lines 5888-5889)

### `utils/files.py`

- Routed symbols: 25
- Cross-module imports: `config/constants.py`: `OFFLINE_JS_LIB_CATALOG`, `OFFLINE_JS_LIB_INDEX_FILE`, `OFFLINE_JS_LIB_README_FILE`; `config/paths.py`: `WORKDIR`; `utils/http.py`: `urlopen`; `utils/json_utils.py`: `json_dumps`; `utils/misc.py`: `now_ts`; `utils/text.py`: `trim`
- Symbols:
  - `_normalize_js_lib_asset_ref` (function, lines 1637-1650)
  - `_resolve_js_lib_asset_path` (function, lines 1653-1682)
  - `_discover_extra_js_lib_files` (function, lines 1685-1715)
  - `safe_path` (function, lines 3315-3324)
  - `_safe_js_filename` (function, lines 3326-3333)
  - `_sha256_bytes` (function, lines 3335-3336)
  - `_sha256_file` (function, lines 3338-3346)
  - `_download_http_bytes` (function, lines 3348-3356)
  - `offline_js_lib_root` (function, lines 3358-3359)
  - `_offline_js_entry_relative_path` (function, lines 3361-3365)
  - `_archive_member_relative_path` (function, lines 3367-3376)
  - `_path_size_bytes` (function, lines 3378-3393)
  - `_extract_archive_to_dir` (function, lines 3395-3435)
  - `_package_required_paths` (function, lines 3437-3443)
  - `_package_install_ready` (function, lines 3445-3453)
  - `_postprocess_offline_js_package` (function, lines 3455-3490)
  - `_ensure_offline_js_package` (function, lines 3492-3531)
  - `_render_offline_js_catalog_md` (function, lines 3533-3549)
  - `load_offline_js_lib_index` (function, lines 3551-3560)
  - `ensure_offline_js_libs` (function, lines 3562-3706)
  - `_normalize_external_js_url` (function, lines 3708-3712)
  - `is_external_js_src` (function, lines 3714-3716)
  - `match_offline_js_catalog_by_url` (function, lines 3718-3734)
  - `cache_external_js_url` (function, lines 3736-3768)
  - `try_read_text` (function, lines 7625-7633)

### `utils/http.py`

- Routed symbols: 4
- Cross-module imports: none
- Symbols:
  - `_URL_OPEN_ORIGINAL` (assignment, lines 61-61)
  - `_HTTP_SSL_CONTEXT` (assignment, lines 62-62)
  - `_shared_http_ssl_context` (function, lines 75-90)
  - `urlopen` (function, lines 92-100)

### `utils/json_utils.py`

- Routed symbols: 20
- Cross-module imports: `config/constants.py`: `DEFAULT_WEB_SEARCH_ENABLED`; `utils/text.py`: `trim`
- Symbols:
  - `JSON_FSYNC_ENABLED` (constant, lines 153-153)
  - `json_dumps` (function, lines 3287-3288)
  - `parse_tool_arguments` (function, lines 5688-5697)
  - `repair_truncated_json_object` (function, lines 5699-5752)
  - `parse_tool_arguments_with_error` (function, lines 5754-5784)
  - `_is_valid_json_object` (function, lines 5786-5790)
  - `_scan_top_level_json_objects` (function, lines 5792-5814)
  - `reconstruct_streamed_tool_args` (function, lines 5816-5859)
  - `parse_json_object` (function, lines 6125-6130)
  - `extract_json_object_from_text` (function, lines 6132-6154)
  - `_json_default_copy` (function, lines 7635-7640)
  - `_read_json_file` (function, lines 7642-7662)
  - `_write_json_file` (function, lines 7664-7691)
  - `tool_def` (function, lines 17082-17094)
  - `TOOLS` (constant, lines 17096-17477)
  - `TOOL_REQUIRED_ARGS` (constant, lines 17479-17479)
  - `TOOL_SPEC_BY_NAME` (constant, lines 17480-17480)
  - `TOOL_NAME_FUZZY_MAP` (constant, lines 17492-17492)
  - `canonicalize_tool_name` (function, lines 17510-17521)
  - `filter_tool_specs_for_runtime` (function, lines 17524-17534)

### `utils/media.py`

- Routed symbols: 3
- Cross-module imports: none
- Symbols:
  - `guess_mime_from_name` (function, lines 2987-2989)
  - `_convert_image_to_safe_format` (function, lines 2992-3009)
  - `guess_ext_from_mime` (function, lines 3012-3018)

### `utils/misc.py`

- Routed symbols: 21
- Cross-module imports: none
- Symbols:
  - `MIN_TIMEOUT_SECONDS` (constant, lines 458-458)
  - `MAX_TIMEOUT_SECONDS` (constant, lines 459-459)
  - `DEFAULT_TIMEOUT_SECONDS` (constant, lines 460-466)
  - `BENIGN_SOCKET_DEBUG_LOG_ENABLED` (constant, lines 642-648)
  - `BENIGN_SOCKET_LOG_INTERVAL_SECONDS` (constant, lines 649-649)
  - `now_ts` (function, lines 3020-3021)
  - `_benign_socket_log_lock` (assignment, lines 3024-3024)
  - `_benign_socket_log_state` (assignment, lines 3025-3025)
  - `is_benign_socket_error` (function, lines 3043-3061)
  - `_socket_error_code` (function, lines 3064-3073)
  - `_log_benign_socket_error_limited` (function, lines 3076-3110)
  - `swallow_benign_socket_error` (function, lines 3113-3117)
  - `normalize_timeout_seconds` (function, lines 3120-3133)
  - `detect_local_lan_ip` (function, lines 3135-3145)
  - `_LOCAL_LAN_IP_CACHE` (assignment, lines 3147-3147)
  - `detect_local_lan_ip_cached` (function, lines 3149-3161)
  - `make_id` (function, lines 3290-3291)
  - `sanitize_profile_id` (function, lines 3293-3295)
  - `user_id_from_ip` (function, lines 7295-7301)
  - `_meta_string_list` (function, lines 7612-7623)
  - `_module_exists` (function, lines 8518-8522)

### `utils/text.py`

- Routed symbols: 25
- Cross-module imports: `config/constants.py`: `CODE_PREVIEW_DIFF_CONTEXT_LINES`, `CODE_PREVIEW_DIFF_MERGE_GAP`
- Symbols:
  - `MAX_TOOL_OUTPUT` (constant, lines 141-141)
  - `SOCKET_NOISE_LINE_PATTERNS` (constant, lines 636-641)
  - `filter_runtime_noise_lines` (function, lines 3028-3040)
  - `trim` (function, lines 3770-3772)
  - `display_clean` (function, lines 3774-3787)
  - `short_title_from` (function, lines 3789-3806)
  - `_fmt_export_ts` (function, lines 5257-5265)
  - `_html_esc` (function, lines 5268-5269)
  - `_text_to_minimal_pdf` (function, lines 5272-5418)
  - `normalize_embedded_newlines` (function, lines 5437-5445)
  - `_map_todo_status_token` (function, lines 5448-5463)
  - `split_todo_status_text` (function, lines 5466-5521)
  - `extract_todo_rows_from_text` (function, lines 5524-5591)
  - `infer_todo_status_from_text` (function, lines 5594-5600)
  - `split_structured_todo_content` (function, lines 5603-5656)
  - `normalize_work_text` (function, lines 5659-5686)
  - `parse_front_matter` (function, lines 7422-7609)
  - `make_unified_diff` (function, lines 7693-7710)
  - `_skip_row` (function, lines 7712-7716)
  - `_row_is_hot` (function, lines 7719-7720)
  - `_hotspot_index` (function, lines 7723-7744)
  - `_compress_rows_keep_hotspot` (function, lines 7747-7794)
  - `_focused_diff_rows_from_opcodes` (function, lines 7797-7929)
  - `make_numbered_diff` (function, lines 7932-7962)
  - `render_numbered_diff_text` (function, lines 7964-7976)
