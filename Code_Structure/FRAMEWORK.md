# Code_Structure Framework

## Overview

- Source file: `/Users/macbookair/Downloads/Split Coder/Clouds_Coder.py`
- Output directory: `/Users/macbookair/Downloads/Split Coder/Code_Structure`
- Generated modules: 30
- Top-level symbols: 546
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
| `config/constants.py` | 297 | `utils/json_utils.py`, `utils/misc.py` |
| `config/paths.py` | 8 | `utils/text.py` |
| `config/settings.py` | 33 | `config/constants.py`, `config/paths.py`, `llm/utils.py`, `skills/store.py`, `utils/http.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` |
| `llm/client.py` | 2 | `config/constants.py`, `config/settings.py`, `llm/utils.py`, `utils/http.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` |
| `llm/utils.py` | 25 | `config/constants.py`, `utils/http.py`, `utils/json_utils.py`, `utils/text.py` |
| `rag/index.py` | 8 | `config/constants.py`, `rag/parsers.py`, `utils/json_utils.py`, `utils/misc.py`, `utils/text.py` |
| `rag/ingestion.py` | 5 | `config/constants.py`, `config/settings.py`, `rag/parsers.py`, `rag/store.py`, `session/state.py`, `utils/files.py`, `utils/json_utils.py`, `utils/media.py`, `utils/misc.py`, `utils/text.py` |
| `rag/parsers.py` | 29 | `config/constants.py`, `utils/files.py`, `utils/json_utils.py`, `utils/media.py`, `utils/text.py` |
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
  - `main` (function, lines 60342-61323)
  - `_main_guard_61325` (main_guard, lines 61325-61326)

### `agent/background.py`

- Routed symbols: 1
- Cross-module imports: `utils/misc.py`: `make_id`, `now_ts`; `utils/text.py`: `trim`
- Symbols:
  - `BackgroundManager` (class, lines 11462-11542)

### `agent/bus.py`

- Routed symbols: 1
- Cross-module imports: `config/constants.py`: `VALID_MSG_TYPES`; `utils/crypto.py`: `CryptoBox`; `utils/misc.py`: `now_ts`
- Symbols:
  - `MessageBus` (class, lines 11544-11598)

### `agent/events.py`

- Routed symbols: 1
- Cross-module imports: none
- Symbols:
  - `EventHub` (class, lines 5560-5605)

### `agent/tasks.py`

- Routed symbols: 1
- Cross-module imports: `utils/crypto.py`: `CryptoBox`; `utils/json_utils.py`: `json_dumps`; `utils/misc.py`: `now_ts`
- Symbols:
  - `TaskManager` (class, lines 11334-11460)

### `agent/todo.py`

- Routed symbols: 1
- Cross-module imports: `config/constants.py`: `DEFAULT_UI_LANGUAGE`; `config/settings.py`: `backend_i18n_text`, `backend_role_label`, `normalize_ui_language`; `utils/text.py`: `infer_todo_status_from_text`, `normalize_work_text`, `split_structured_todo_content`, `trim`
- Symbols:
  - `TodoManager` (class, lines 5607-5876)

### `agent/worktree.py`

- Routed symbols: 1
- Cross-module imports: `agent/tasks.py`: `TaskManager`; `config/constants.py`: `DANGEROUS_PATTERNS`; `utils/crypto.py`: `CryptoBox`; `utils/json_utils.py`: `json_dumps`; `utils/misc.py`: `now_ts`; `utils/text.py`: `trim`
- Symbols:
  - `WorktreeManager` (class, lines 11600-11811)

### `app/context.py`

- Routed symbols: 1
- Cross-module imports: `config/constants.py`: `AGENT_MAX_OUTPUT_TOKENS`, `APP_CSS`, `APP_JS`, `APP_TS`, `ARBITER_DEFAULT_MAX_TOKENS`, `ARBITER_DEFAULT_TEMPERATURE`, `ARBITER_DEFAULT_TIMEOUT_SECONDS`, `CODE_ADMIN_CSS`, `CODE_ADMIN_INDEX_HTML`, `CODE_ADMIN_JS`, `CODE_IMPORT_WORKER_COUNT`, `CODE_LIBRARY_DIRNAME`, `CODE_PARSE_TIMEOUT_SECONDS`, `DEFAULT_REQUEST_TIMEOUT`, `DEFAULT_SHELL_COMMAND_TIMEOUT_SECONDS`, `DEFAULT_UI_LANGUAGE`, `DEFAULT_UI_STYLE`, `DEFAULT_WEB_UI_DIR`, `EXECUTION_MODE_SYNC`, `INDEX_HTML`, `MAX_AGENT_ROUNDS`, `MAX_AGENT_ROUNDS_CAP`, `MAX_RUN_SECONDS`, `MAX_RUN_TIMEOUT_SECONDS`, `MAX_SHELL_COMMAND_TIMEOUT_SECONDS`, `MIN_AGENT_ROUNDS`, `MIN_CONTEXT_TOKEN_LIMIT`, `MIN_RUN_TIMEOUT_SECONDS`, `MIN_SHELL_COMMAND_TIMEOUT_SECONDS`, `RAG_ADMIN_CSS`, `RAG_ADMIN_INDEX_HTML`, `RAG_ADMIN_JS`, `RAG_GRAPH_MAX_NODES`, `RAG_IMPORT_WORKER_COUNT`, `RAG_INCLUDE_FILENAME_ENTITIES_DEFAULT`, `RAG_LIBRARY_DIRNAME`, `RAG_MAX_GLOBAL_COMMUNITIES`, `RAG_MAX_IMPORT_BATCH_BYTES`, `RAG_MAX_IMPORT_BATCH_ITEMS`, `RAG_MAX_IMPORT_FILES`, `RAG_MAX_QUERY_RESULTS`, `RAG_MIN_SYNTHESIS_SCORE`, `RAG_NO_EVIDENCE_THRESHOLD`, `RAG_PARSE_TIMEOUT_SECONDS`, `RAG_QUERY_CONTEXT_CHARS`, `SKILLS_APP_JS`, `SKILLS_EXTRA_CSS`, `SKILLS_INDEX_HTML`, `SKILL_REFRESH_MIN_INTERVAL_SECONDS`, `TOKEN_THRESHOLD`, `WEB_UI_OPTIONAL_FILES`, `WEB_UI_REQUIRED_FILES`; `config/paths.py`: `LLM_CONFIG_PATH`, `REPO_ROOT`, `_migrate_legacy_runtime_roots`; `config/settings.py`: `default_multimodal_capabilities`, `infer_model_multimodal_capabilities`, `merge_multimodal_capabilities`, `model_language_instruction`, `normalize_execution_mode`, `normalize_ui_language`, `normalize_ui_style`, `parse_capability_overrides`, `parse_llm_config_profiles`, `resolve_optional_file_path`, `resolve_web_ui_dir_path`; `llm/client.py`: `OllamaClient`; `llm/utils.py`: `extract_base_url`, `list_ollama_models_cached`; `rag/ingestion.py`: `CodeIngestionService`, `RAGIngestionService`, `_rag_embed_batch`, `_rag_embed_text`; `rag/parsers.py`: `CodeContentParser`, `RAGContentParser`; `rag/store.py`: `CodeLibraryStore`, `RAGLibraryStore`; `session/manager.py`: `SessionCreationLimitExceeded`, `SessionManager`; `session/state.py`: `SessionState`; `skills/store.py`: `SkillStore`, `_sanitize_skill_slug`, `analyze_skill_building_knowledge`, `ensure_runtime_skills`; `utils/crypto.py`: `CryptoBox`; `utils/files.py`: `_resolve_js_lib_asset_path`, `ensure_offline_js_libs`, `load_offline_js_lib_index`, `offline_js_lib_root`, `safe_path`, `try_read_text`; `utils/json_utils.py`: `TOOLS`, `extract_json_object_from_text`, `json_dumps`, `parse_json_object`; `utils/misc.py`: `DEFAULT_TIMEOUT_SECONDS`, `MAX_TIMEOUT_SECONDS`, `MIN_TIMEOUT_SECONDS`, `normalize_timeout_seconds`, `now_ts`, `sanitize_profile_id`; `utils/text.py`: `parse_front_matter`, `trim`
- Symbols:
  - `AppContext` (class, lines 56364-58918)

### `config/constants.py`

- Routed symbols: 297
- Cross-module imports: `utils/json_utils.py`: `TOOL_SPEC_BY_NAME`; `utils/misc.py`: `DEFAULT_TIMEOUT_SECONDS`
- Symbols:
  - `APP_VERSION` (constant, lines 58-58)
  - `DEFAULT_OLLAMA_BASE_URL` (constant, lines 59-59)
  - `DEFAULT_OLLAMA_MODEL` (constant, lines 60-60)
  - `LONG_OUTPUT_MODEL_PAGE_CHARS` (constant, lines 137-137)
  - `LONG_OUTPUT_UI_PAGE_CHARS` (constant, lines 138-138)
  - `LONG_OUTPUT_UI_PREVIEW_MAX_PAGES` (constant, lines 139-139)
  - `LONG_OUTPUT_LISTING_OFFLOAD_CHARS` (constant, lines 140-140)
  - `LONG_OUTPUT_READ_PAGE_LINES` (constant, lines 141-141)
  - `LONG_OUTPUT_READ_PAGE_MAX_CHARS` (constant, lines 142-142)
  - `LONG_OUTPUT_TEMP_MAX_FILES` (constant, lines 143-143)
  - `RAG_LIBRARY_DIRNAME` (constant, lines 145-145)
  - `RAG_ADMIN_PORT_OFFSET` (constant, lines 146-146)
  - `CODE_LIBRARY_DIRNAME` (constant, lines 147-147)
  - `CODE_ADMIN_PORT_OFFSET` (constant, lines 148-148)
  - `RAG_CHUNK_CHARS` (constant, lines 149-149)
  - `RAG_CHUNK_OVERLAP` (constant, lines 150-150)
  - `RAG_MAX_CHUNKS_PER_DOC` (constant, lines 151-151)
  - `CODE_CHUNK_CHARS` (constant, lines 152-152)
  - `CODE_CHUNK_OVERLAP` (constant, lines 153-153)
  - `CODE_MAX_CHUNKS_PER_DOC` (constant, lines 154-154)
  - `RAG_MAX_QUERY_RESULTS` (constant, lines 155-155)
  - `RAG_GRAPH_MAX_NODES` (constant, lines 156-156)
  - `RAG_TASK_HISTORY_LIMIT` (constant, lines 157-157)
  - `RAG_MODEL_MEDIA_MAX_BYTES` (constant, lines 158-158)
  - `RAG_MAX_IMPORT_FILES` (constant, lines 159-159)
  - `RAG_MAX_IMPORT_BATCH_ITEMS` (constant, lines 160-160)
  - `RAG_MAX_IMPORT_BATCH_BYTES` (constant, lines 161-161)
  - `RAG_PDF_IMAGE_LIMIT` (constant, lines 162-162)
  - `RAG_QUERY_CONTEXT_CHARS` (constant, lines 163-163)
  - `RAG_MAX_GLOBAL_COMMUNITIES` (constant, lines 164-164)
  - `RAG_MAX_COMMUNITY_MAP_SUPPORT` (constant, lines 165-165)
  - `RAG_INCLUDE_FILENAME_ENTITIES_DEFAULT` (constant, lines 166-166)
  - `RAG_DYNAMIC_NOISE_MIN_DOC_FREQ` (constant, lines 167-167)
  - `RAG_DYNAMIC_NOISE_MIN_COMMUNITY_FREQ` (constant, lines 168-168)
  - `RAG_DYNAMIC_NOISE_SOFT_DOC_RATIO` (constant, lines 169-169)
  - `RAG_DYNAMIC_NOISE_HARD_DOC_RATIO` (constant, lines 170-170)
  - `RAG_DYNAMIC_NOISE_SOFT_COMMUNITY_RATIO` (constant, lines 171-171)
  - `RAG_DYNAMIC_NOISE_HARD_COMMUNITY_RATIO` (constant, lines 172-172)
  - `RAG_MIN_SYNTHESIS_SCORE` (constant, lines 173-173)
  - `RAG_NO_EVIDENCE_THRESHOLD` (constant, lines 174-174)
  - `RAG_SYNTHESIS_MAX_PER_DOC` (constant, lines 175-175)
  - `RAG_IMPORT_WORKER_COUNT` (constant, lines 176-179)
  - `CODE_IMPORT_WORKER_COUNT` (constant, lines 180-183)
  - `RAG_PARSE_TIMEOUT_SECONDS` (constant, lines 184-187)
  - `CODE_PARSE_TIMEOUT_SECONDS` (constant, lines 188-191)
  - `TOKEN_THRESHOLD` (constant, lines 192-192)
  - `IDLE_TIMEOUT` (constant, lines 193-193)
  - `POLL_INTERVAL` (constant, lines 194-194)
  - `SSE_HEARTBEAT_SECONDS` (constant, lines 195-195)
  - `MODEL_CALL_PROGRESS_DELAY` (constant, lines 196-196)
  - `MODEL_CALL_PROGRESS_INTERVAL` (constant, lines 197-197)
  - `MAX_AGENT_ROUNDS` (constant, lines 198-198)
  - `MIN_AGENT_ROUNDS` (constant, lines 199-199)
  - `MAX_AGENT_ROUNDS_CAP` (constant, lines 200-200)
  - `REPEATED_TOOL_LOOP_THRESHOLD` (constant, lines 201-201)
  - `BASH_READ_LOOP_THRESHOLD` (constant, lines 202-202)
  - `HARD_BREAK_TOOL_ERROR_THRESHOLD` (constant, lines 203-203)
  - `HARD_BREAK_RECOVERY_ROUND_THRESHOLD` (constant, lines 204-204)
  - `FUSED_FAULT_BREAK_THRESHOLD` (constant, lines 205-205)
  - `STALL_SEVERITY_ESCALATION_THRESHOLD` (constant, lines 206-206)
  - `STALL_SEVERITY_WEIGHT_BASH_READ_LOOP` (constant, lines 207-207)
  - `STALL_SEVERITY_WEIGHT_REPEATED_TOOL` (constant, lines 208-208)
  - `STALL_SEVERITY_WEIGHT_FAULT` (constant, lines 209-209)
  - `STALL_SEVERITY_WEIGHT_RECOVERY_RETRY` (constant, lines 210-210)
  - `STALL_SEVERITY_WEIGHT_WATCHDOG` (constant, lines 211-211)
  - `STALL_SEVERITY_DECAY_ON_SUCCESS` (constant, lines 212-212)
  - `STALL_ESCALATION_MIN_LEVEL` (constant, lines 213-213)
  - `STALL_PLAN_SYNTHESIS_MAX_TOKENS` (constant, lines 214-214)
  - `STALL_ESCALATION_CONTEXT_MAX_CHARS` (constant, lines 215-215)
  - `MAX_RUN_SECONDS` (constant, lines 216-216)
  - `MIN_RUN_TIMEOUT_SECONDS` (constant, lines 217-217)
  - `MAX_RUN_TIMEOUT_SECONDS` (constant, lines 218-218)
  - `DEFAULT_REQUEST_TIMEOUT` (constant, lines 228-228)
  - `_SHELL_AUTO_CONFIRM_PATTERNS` (assignment, lines 231-244)
  - `MIN_SHELL_COMMAND_TIMEOUT_SECONDS` (constant, lines 245-245)
  - `MAX_SHELL_COMMAND_TIMEOUT_SECONDS` (constant, lines 246-246)
  - `DEFAULT_SHELL_COMMAND_TIMEOUT_SECONDS` (constant, lines 247-261)
  - `AUTO_CONTINUE_BUDGET_DEFAULT` (constant, lines 262-262)
  - `AGENT_MAX_OUTPUT_TOKENS` (constant, lines 263-263)
  - `OLLAMA_THINKING_TOOL_BUFFER` (constant, lines 264-264)
  - `WATCHDOG_INTENT_NO_TOOL_THRESHOLD` (constant, lines 265-265)
  - `WATCHDOG_REPEAT_NO_TOOL_THRESHOLD` (constant, lines 266-266)
  - `WATCHDOG_INTENT_NO_TOOL_THRESHOLD_SINGLE` (constant, lines 267-267)
  - `WATCHDOG_REPEAT_NO_TOOL_THRESHOLD_SINGLE` (constant, lines 268-268)
  - `WATCHDOG_STATE_STALL_THRESHOLD` (constant, lines 269-269)
  - `WATCHDOG_CONTEXT_STALL_THRESHOLD` (constant, lines 270-270)
  - `WATCHDOG_REPEAT_SIMILARITY_THRESHOLD` (constant, lines 271-271)
  - `WATCHDOG_CONTEXT_NEAR_RATIO` (constant, lines 272-272)
  - `WATCHDOG_MAX_DECOMPOSE_STEPS` (constant, lines 273-273)
  - `WATCHDOG_STEP_MAX_ATTEMPTS` (constant, lines 274-274)
  - `EMPTY_ACTION_MIN_CONTENT_CHARS` (constant, lines 275-275)
  - `EMPTY_ACTION_WAKEUP_RETRY_LIMIT` (constant, lines 276-276)
  - `THINKING_BUDGET_FORCE_RATIO` (constant, lines 277-277)
  - `_TOOL_TIMEOUT_MAP` (assignment, lines 279-295)
  - `_DEFAULT_TOOL_TIMEOUT` (assignment, lines 296-296)
  - `TRUNCATION_CONTINUATION_MAX_PASSES` (constant, lines 297-297)
  - `TRUNCATION_CONTINUATION_MAX_TOKENS` (constant, lines 298-298)
  - `TRUNCATION_CONTINUATION_TAIL_CHARS` (constant, lines 299-299)
  - `TRUNCATION_CONTINUATION_ECHO_CHARS` (constant, lines 300-300)
  - `TRUNCATION_OVERLAP_SCAN_CHARS` (constant, lines 301-301)
  - `TRUNCATION_PAIR_SCAN_CHARS` (constant, lines 302-302)
  - `TRUNCATION_LIVE_BUFFER_MAX_CHARS` (constant, lines 303-303)
  - `MIN_CONTEXT_TOKEN_LIMIT` (constant, lines 304-304)
  - `COMPACT_TIER1_PCT` (constant, lines 306-306)
  - `COMPACT_TIER2_PCT` (constant, lines 307-307)
  - `COMPACT_TIER3_PCT` (constant, lines 308-308)
  - `COMPACT_TIER1_ABS` (constant, lines 310-310)
  - `COMPACT_TIER2_ABS` (constant, lines 311-311)
  - `FILE_BUFFER_CONTENT_THRESHOLD` (constant, lines 313-313)
  - `FILE_BUFFER_MAX_FILES` (constant, lines 314-314)
  - `AGENT_MSG_LIMIT_TIER0` (constant, lines 316-316)
  - `AGENT_MSG_LIMIT_TIER1` (constant, lines 317-317)
  - `AGENT_MSG_LIMIT_TIER2` (constant, lines 318-318)
  - `AGENT_MSG_LIMIT_TIER3` (constant, lines 319-319)
  - `AGENT_CTX_LIMIT_TIER0` (constant, lines 320-320)
  - `AGENT_CTX_LIMIT_TIER1` (constant, lines 321-321)
  - `AGENT_CTX_LIMIT_TIER2` (constant, lines 322-322)
  - `AGENT_CTX_LIMIT_TIER3` (constant, lines 323-323)
  - `MANAGER_CTX_LIMIT_TIER0` (constant, lines 324-324)
  - `MANAGER_CTX_LIMIT_TIER1` (constant, lines 325-325)
  - `MANAGER_CTX_LIMIT_TIER2` (constant, lines 326-326)
  - `MANAGER_CTX_LIMIT_TIER3` (constant, lines 327-327)
  - `MAX_CONTEXT_ARCHIVE_SEGMENTS` (constant, lines 328-328)
  - `MODEL_OUTPUT_RETRY_TIMES` (constant, lines 329-329)
  - `ARBITER_TRIGGER_MIN_CONTENT_CHARS` (constant, lines 330-330)
  - `ARBITER_VALID_PLANNING_STREAK_LIMIT` (constant, lines 331-331)
  - `ARBITER_DEFAULT_TIMEOUT_SECONDS` (constant, lines 332-332)
  - `ARBITER_DEFAULT_MAX_TOKENS` (constant, lines 333-333)
  - `ARBITER_DEFAULT_TEMPERATURE` (constant, lines 334-334)
  - `LIVE_INPUT_DELAY_WRITE_ROUNDS` (constant, lines 335-335)
  - `LIVE_INPUT_DELAY_TOOL_ROUNDS` (constant, lines 336-336)
  - `LIVE_INPUT_DELAY_NORMAL_ROUNDS` (constant, lines 337-337)
  - `LIVE_INPUT_MAX_INJECTIONS` (constant, lines 338-338)
  - `LIVE_INPUT_REINJECT_INTERVAL` (constant, lines 339-339)
  - `LIVE_INPUT_WEIGHT_BASE_DELAYED` (constant, lines 340-340)
  - `LIVE_INPUT_WEIGHT_BASE_NORMAL` (constant, lines 341-341)
  - `LIVE_INPUT_WEIGHT_STEP_DELAYED` (constant, lines 342-342)
  - `LIVE_INPUT_WEIGHT_STEP_NORMAL` (constant, lines 343-343)
  - `FINAL_SUMMARY_MIN_CHARS` (constant, lines 358-358)
  - `FINAL_SUMMARY_STRICT_MIN_CHARS` (constant, lines 359-359)
  - `RUNTIME_CONTROL_HINT_PREFIXES` (constant, lines 360-377)
  - `RETRY_RUNTIME_HINT_PREFIXES` (constant, lines 378-392)
  - `EXECUTION_MODE_SINGLE` (constant, lines 393-393)
  - `EXECUTION_MODE_SEQUENTIAL` (constant, lines 394-394)
  - `EXECUTION_MODE_SYNC` (constant, lines 395-395)
  - `EXECUTION_MODE_CHOICES` (constant, lines 396-400)
  - `AGENT_ROLES` (constant, lines 401-401)
  - `AGENT_BUBBLE_ROLES` (constant, lines 402-402)
  - `AGENT_ROLE_LABELS` (constant, lines 403-409)
  - `AGENT_ROLE_BUBBLE_COLORS` (constant, lines 410-416)
  - `BLACKBOARD_STATUSES` (constant, lines 417-426)
  - `TASK_COMPLEXITY_LEVELS` (constant, lines 427-427)
  - `TASK_COMPLEXITY_RANKS` (constant, lines 428-433)
  - `TASK_PROFILE_TYPES` (constant, lines 434-440)
  - `TASK_LEVEL_CHOICES` (constant, lines 441-441)
  - `TASK_SCALE_PREFERENCES` (constant, lines 442-442)
  - `SEMANTIC_CONFIDENCE_CHOICES` (constant, lines 443-443)
  - `TASK_LEVEL_POLICIES` (constant, lines 444-490)
  - `MANAGER_ROUTE_TARGETS` (constant, lines 491-491)
  - `BLACKBOARD_MAX_LOG_ENTRIES` (constant, lines 492-492)
  - `BLACKBOARD_MAX_TEXT` (constant, lines 493-493)
  - `SKILL_REFRESH_MIN_INTERVAL_SECONDS` (constant, lines 494-494)
  - `SKILL_PROMPT_MAX_ITEMS` (constant, lines 495-495)
  - `SKILL_PROMPT_MAX_CHARS` (constant, lines 496-496)
  - `SKILL_RUNTIME_CACHE_MAX_ENTRIES` (constant, lines 497-497)
  - `SKILL_RUNTIME_CACHE_MAX_BYTES` (constant, lines 498-498)
  - `AUTO_SKILLS_ROOT_CANDIDATES` (constant, lines 499-499)
  - `SKILL_DEFAULT_ATTACHMENT_GLOBS` (constant, lines 500-530)
  - `SKILL_INLINE_ATTACHMENT_MAX_FILES` (constant, lines 531-531)
  - `SKILL_INLINE_ATTACHMENT_MAX_CHARS` (constant, lines 532-532)
  - `SKILL_RESOURCE_MANIFEST_MAX_ITEMS` (constant, lines 533-533)
  - `SKILL_BODY_COMPACT_THRESHOLD_CHARS` (constant, lines 534-534)
  - `SKILL_BODY_PREVIEW_CHARS` (constant, lines 535-535)
  - `SKILLS_VIRTUAL_PREFIX` (constant, lines 536-536)
  - `SKILLS_EXTERNAL_MOUNT` (constant, lines 537-537)
  - `PLAN_MODE_ENABLED_LEVELS` (constant, lines 538-538)
  - `PLAN_MODE_FORCED_LEVELS` (constant, lines 539-539)
  - `PLAN_MODE_USER_CHOICES` (constant, lines 540-540)
  - `TASK_PHASES` (constant, lines 542-542)
  - `TASK_PHASE_ROUTING` (constant, lines 543-550)
  - `COMPLEXITY_KEYWORDS` (constant, lines 552-557)
  - `USER_COMPLEXITY_SIMPLE_TOKENS` (constant, lines 558-562)
  - `USER_COMPLEXITY_MODERATE_TOKENS` (constant, lines 563-567)
  - `USER_COMPLEXITY_COMPLEX_TOKENS` (constant, lines 568-572)
  - `USER_COMPLEXITY_EXPERT_TOKENS` (constant, lines 573-577)
  - `PLAN_MODE_EXPLORER_MAX_ROUNDS` (constant, lines 578-578)
  - `PLAN_MODE_SYNTHESIS_MAX_ATTEMPTS` (constant, lines 579-579)
  - `REVIEWER_DEBUG_MODE_MAX_ROUNDS` (constant, lines 581-581)
  - `REVIEWER_DEBUG_TOOL_ALLOWLIST` (constant, lines 582-586)
  - `EXPLORER_STALL_THRESHOLD` (constant, lines 587-587)
  - `DEVELOPER_EDIT_STALL_THRESHOLD` (constant, lines 588-588)
  - `PLAN_MODE_MANAGER_SYNTHESIS_MAX_TOKENS` (constant, lines 589-589)
  - `PLAN_MODE_MAX_OPTIONS` (constant, lines 590-590)
  - `PLAN_FILE_RELATIVE_PATH` (constant, lines 591-591)
  - `PLAN_BUBBLE_MAX_CHARS` (constant, lines 592-592)
  - `PLAN_NOTICE_BODY_MAX_CHARS` (constant, lines 593-593)
  - `PLAN_MESSAGE_EVENT_MAX_CHARS` (constant, lines 594-594)
  - `PLAN_STEP_FULL_CONTENT_MAX_CHARS` (constant, lines 595-595)
  - `PLAN_MODE_RESEARCH_TOOL_ALLOWLIST` (constant, lines 596-600)
  - `FAILURE_LEDGER_MAX_FIXES` (constant, lines 601-601)
  - `FAILURE_LEDGER_MAX_COMPILE_ERRORS` (constant, lines 602-602)
  - `FAILURE_LEDGER_MAX_DELEGATIONS` (constant, lines 603-603)
  - `FAILURE_LEDGER_MAX_STALLS` (constant, lines 604-604)
  - `FAILURE_LEDGER_MAX_TOOL_FPS` (constant, lines 605-605)
  - `FAILURE_LEDGER_MAX_ERRORS` (constant, lines 606-606)
  - `ERROR_CATEGORY_DEFS` (constant, lines 609-646)
  - `CHECKPOINT_MAX_COUNT` (constant, lines 647-647)
  - `CHECKPOINT_INTERVAL_ROUNDS` (constant, lines 648-648)
  - `PERSISTED_ROUTES_MAX` (constant, lines 649-649)
  - `HTML_FRONTEND_REQUEST_KEYWORDS` (constant, lines 650-689)
  - `DEEP_RESEARCH_REQUEST_KEYWORDS` (constant, lines 690-712)
  - `DEEP_RESEARCH_RETRIEVAL_KEYWORDS` (constant, lines 713-732)
  - `DEEP_RESEARCH_TEXT_ONLY_HINT_KEYWORDS` (constant, lines 733-750)
  - `DANGEROUS_PATTERNS` (constant, lines 752-752)
  - `VALID_MSG_TYPES` (constant, lines 753-759)
  - `SUPPORTED_UI_LANGUAGES` (constant, lines 761-766)
  - `UI_LANGUAGE_LABELS` (constant, lines 767-767)
  - `DEFAULT_UI_LANGUAGE` (constant, lines 768-768)
  - `UI_STYLE_CHOICES` (constant, lines 769-769)
  - `UI_STYLE_LABELS` (constant, lines 770-770)
  - `DEFAULT_UI_STYLE` (constant, lines 771-771)
  - `DEFAULT_WEB_UI_DIR` (constant, lines 772-772)
  - `DEFAULT_WEB_UI_CONFIG` (constant, lines 773-773)
  - `WEB_UI_REQUIRED_FILES` (constant, lines 774-781)
  - `WEB_UI_OPTIONAL_FILES` (constant, lines 782-782)
  - `IMAGE_EXTS` (constant, lines 784-797)
  - `IMAGE_FORMATS_NEED_CONVERSION` (constant, lines 798-798)
  - `IMAGE_SAFE_FORMATS` (constant, lines 799-799)
  - `AUDIO_EXTS` (constant, lines 800-810)
  - `VIDEO_EXTS` (constant, lines 811-821)
  - `CODE_PREVIEW_STAGE_MAX_BYTES` (constant, lines 822-822)
  - `CODE_PREVIEW_STAGE_MAX_ROWS` (constant, lines 823-823)
  - `CODE_PREVIEW_STAGE_MAX_PER_FILE` (constant, lines 824-824)
  - `CODE_PREVIEW_STAGE_MAX_TOTAL` (constant, lines 825-825)
  - `RENDER_FRAME_MAX_B64_CHARS` (constant, lines 826-826)
  - `RENDER_FRAME_MAX_POINTS` (constant, lines 827-827)
  - `RENDER_FRAME_MAX_LINES` (constant, lines 828-828)
  - `RENDER_FRAME_MAX_LINE_POINTS` (constant, lines 829-829)
  - `RENDER_FRAME_ACTIVITY_INTERVAL_SECONDS` (constant, lines 830-830)
  - `RAW_TOOLCALL_TEXT_FILTER_THRESHOLD` (constant, lines 831-831)
  - `ASSISTANT_TEXT_PERSIST_MAX_CHARS` (constant, lines 832-832)
  - `ASSISTANT_MESSAGE_EVENT_MAX_CHARS` (constant, lines 833-833)
  - `CODE_PREVIEW_EXTS` (constant, lines 834-923)
  - `CODE_PREVIEW_FILENAMES` (constant, lines 924-935)
  - `MEDIA_CAPABILITY_KEYS` (constant, lines 936-943)
  - `SAMPLE_IMAGE_PNG_B64` (constant, lines 944-947)
  - `SAMPLE_AUDIO_WAV_B64` (constant, lines 948-950)
  - `SAMPLE_VIDEO_MP4_B64` (constant, lines 951-953)
  - `OFFLINE_JS_LIB_CATALOG` (constant, lines 955-1213)
  - `OFFLINE_JS_LIB_INDEX_FILE` (constant, lines 1214-1214)
  - `OFFLINE_JS_LIB_README_FILE` (constant, lines 1215-1215)
  - `BACKEND_I18N` (constant, lines 1401-1470)
  - `call_backend_i18n_en_update_l1472` (expression, lines 1472-1565)
  - `call_backend_i18n_zh_cn_update_l1566` (expression, lines 1566-1659)
  - `call_backend_i18n_zh_tw_update_l1660` (expression, lines 1660-1753)
  - `call_backend_i18n_ja_update_l1754` (expression, lines 1754-1847)
  - `OPENAI_COMPAT_PROVIDER_NAMES` (constant, lines 3877-3885)
  - `OPENAI_LIKE_PROVIDER_NAMES` (constant, lines 3887-3887)
  - `TABULAR_PREVIEW_EXTS` (constant, lines 5338-5338)
  - `EXCEL_PREVIEW_EXTS` (constant, lines 5339-5339)
  - `PRESENTATION_PREVIEW_EXTS` (constant, lines 5340-5340)
  - `DOCUMENT_PREVIEW_EXTS` (constant, lines 5341-5341)
  - `EMBEDDED_SKILLS_ARCHIVE_B64` (constant, lines 5878-6397)
  - `EMBEDDED_SKILLS_ARCHIVE_SHA256` (constant, lines 6398-6398)
  - `EMBEDDED_SKILLS_ARCHIVE_FILES` (constant, lines 6399-6422)
  - `BUILTIN_CLAWHUB_SKILLS_VERSION` (constant, lines 9582-9582)
  - `EMBEDDED_CLAWHUB_SKILLS_ARCHIVE_B64` (constant, lines 9584-9828)
  - `SKILL_PROTOCOL_LOCAL` (constant, lines 9894-9894)
  - `SKILL_PROTOCOL_CLAWHUB` (constant, lines 9895-9895)
  - `SKILL_PROTOCOL_HTTP_JSON` (constant, lines 9896-9896)
  - `SKILL_PROTOCOL_SPECS` (constant, lines 9898-9929)
  - `AGENT_TOOL_ALLOWLIST` (constant, lines 13151-13194)
  - `INDEX_HTML` (constant, lines 40164-40351)
  - `APP_CSS` (constant, lines 40353-40741)
  - `APP_JS` (constant, lines 40743-43850)
  - `APP_TS` (constant, lines 43852-43879)
  - `SKILLS_INDEX_HTML` (constant, lines 43881-44035)
  - `SKILLS_EXTRA_CSS` (constant, lines 44037-44132)
  - `SKILLS_APP_JS` (constant, lines 44134-44275)
  - `RAG_TERM_GROUPS` (constant, lines 44277-48909)
  - `RAG_RESEARCH_HINTS` (constant, lines 48910-48931)
  - `RAG_CODE_HINTS` (constant, lines 48932-48942)
  - `RAG_SHORT_TOKEN_ALLOWLIST` (constant, lines 48943-48958)
  - `RAG_EN_STOPWORDS` (constant, lines 48959-49031)
  - `RAG_ZH_STOPWORDS` (constant, lines 49032-49068)
  - `RAG_GENERIC_ENTITY_TERMS_EN` (constant, lines 49069-49147)
  - `RAG_GENERIC_ENTITY_TERMS_ZH` (constant, lines 49148-49190)
  - `RAG_STRUCTURAL_ENTITY_PATTERNS` (constant, lines 49191-49209)
  - `CODE_LIBRARY_IGNORED_DIRS` (constant, lines 49797-49802)
  - `CODE_LIBRARY_LANGUAGE_BY_EXT` (constant, lines 49803-49859)
  - `CODE_LIBRARY_SPECIAL_FILENAMES` (constant, lines 49860-49866)
  - `RAG_ADMIN_INDEX_HTML` (constant, lines 54806-54969)
  - `RAG_ADMIN_CSS` (constant, lines 54971-55061)
  - `RAG_ADMIN_JS` (constant, lines 55063-56306)
  - `CODE_ADMIN_INDEX_HTML` (constant, lines 56308-56317)
  - `CODE_ADMIN_CSS` (constant, lines 56318-56348)
  - `CODE_ADMIN_JS` (constant, lines 56349-56353)

### `config/paths.py`

- Routed symbols: 8
- Cross-module imports: `utils/text.py`: `trim`
- Symbols:
  - `SCRIPT_DIR` (constant, lines 61-61)
  - `_resolve_default_agent_workdir` (function, lines 97-101)
  - `_migrate_legacy_runtime_roots` (function, lines 103-131)
  - `WORKDIR` (constant, lines 133-133)
  - `CODES_ROOT` (constant, lines 134-134)
  - `LLM_CONFIG_PATH` (constant, lines 135-135)
  - `detect_repo_root` (function, lines 2474-2488)
  - `REPO_ROOT` (constant, lines 2490-2490)

### `config/settings.py`

- Routed symbols: 33
- Cross-module imports: `config/constants.py`: `AUTO_SKILLS_ROOT_CANDIDATES`, `BACKEND_I18N`, `DEFAULT_REQUEST_TIMEOUT`, `DEFAULT_SHELL_COMMAND_TIMEOUT_SECONDS`, `DEFAULT_UI_LANGUAGE`, `DEFAULT_UI_STYLE`, `DEFAULT_WEB_UI_CONFIG`, `DEFAULT_WEB_UI_DIR`, `EXECUTION_MODE_CHOICES`, `EXECUTION_MODE_SEQUENTIAL`, `EXECUTION_MODE_SINGLE`, `EXECUTION_MODE_SYNC`, `MAX_SHELL_COMMAND_TIMEOUT_SECONDS`, `MEDIA_CAPABILITY_KEYS`, `MIN_SHELL_COMMAND_TIMEOUT_SECONDS`, `SUPPORTED_UI_LANGUAGES`, `TASK_COMPLEXITY_LEVELS`, `TASK_COMPLEXITY_RANKS`, `UI_LANGUAGE_LABELS`, `UI_STYLE_CHOICES`, `USER_COMPLEXITY_COMPLEX_TOKENS`, `USER_COMPLEXITY_EXPERT_TOKENS`, `USER_COMPLEXITY_MODERATE_TOKENS`, `USER_COMPLEXITY_SIMPLE_TOKENS`; `config/paths.py`: `WORKDIR`; `llm/utils.py`: `_is_http_url`, `_resolve_local_path`, `complete_chat_endpoint`, `extract_base_url`, `is_openai_like_provider`, `normalize_openai_compat_provider_name`, `strip_thinking_content`; `skills/store.py`: `ensure_embedded_skills`; `utils/http.py`: `urlopen`; `utils/json_utils.py`: `parse_json_object`; `utils/misc.py`: `MAX_TIMEOUT_SECONDS`, `MIN_TIMEOUT_SECONDS`, `normalize_timeout_seconds`, `sanitize_profile_id`; `utils/text.py`: `trim`
- Symbols:
  - `normalize_ui_language` (function, lines 1299-1321)
  - `normalize_ui_style` (function, lines 1324-1341)
  - `supported_ui_languages_payload` (function, lines 1344-1345)
  - `normalize_execution_mode` (function, lines 1348-1367)
  - `model_language_instruction` (function, lines 1370-1398)
  - `backend_i18n_text` (function, lines 1850-1860)
  - `backend_role_label` (function, lines 1863-1867)
  - `_detect_os_shell_instruction` (function, lines 1870-1909)
  - `resolve_web_ui_dir_path` (function, lines 1911-1918)
  - `resolve_optional_file_path` (function, lines 1921-1928)
  - `resolve_skills_root_path` (function, lines 1931-1938)
  - `_count_skill_markdown_files` (function, lines 1941-1952)
  - `select_preferred_skills_root` (function, lines 1955-1989)
  - `load_web_ui_config_file` (function, lines 1992-2006)
  - `extract_show_upload_list_setting` (function, lines 2009-2023)
  - `extract_ui_style_setting` (function, lines 2026-2040)
  - `extract_js_lib_download_setting` (function, lines 2043-2062)
  - `extract_daily_session_limit_setting` (function, lines 2065-2108)
  - `extract_shell_command_timeout_setting` (function, lines 2111-2157)
  - `default_multimodal_capabilities` (function, lines 2166-2174)
  - `_to_bool_like` (function, lines 2177-2187)
  - `infer_model_multimodal_capabilities` (function, lines 2190-2234)
  - `parse_capability_overrides` (function, lines 2237-2274)
  - `merge_multimodal_capabilities` (function, lines 2277-2284)
  - `parse_media_endpoints` (function, lines 2287-2301)
  - `infer_user_complexity_value` (function, lines 3795-3811)
  - `normalize_task_complexity` (function, lines 3813-3841)
  - `task_complexity_rank` (function, lines 3843-3844)
  - `task_complexity_at_least` (function, lines 3846-3847)
  - `max_task_complexity` (function, lines 3849-3858)
  - `load_llm_config_from_source` (function, lines 4009-4043)
  - `parse_llm_config_profiles` (function, lines 4045-4631)
  - `looks_like_llm_config` (function, lines 4633-4707)

### `llm/client.py`

- Routed symbols: 2
- Cross-module imports: `config/constants.py`: `DEFAULT_REQUEST_TIMEOUT`, `OLLAMA_THINKING_TOOL_BUFFER`, `SAMPLE_AUDIO_WAV_B64`, `SAMPLE_IMAGE_PNG_B64`, `SAMPLE_VIDEO_MP4_B64`; `config/settings.py`: `default_multimodal_capabilities`, `infer_model_multimodal_capabilities`, `merge_multimodal_capabilities`, `parse_capability_overrides`, `parse_media_endpoints`; `llm/utils.py`: `complete_chat_endpoint`, `is_openai_compat_provider`, `is_openai_like_provider`, `split_thinking_content`; `utils/http.py`: `urlopen`; `utils/json_utils.py`: `canonicalize_tool_name`, `json_dumps`, `parse_json_object`, `parse_tool_arguments`, `parse_tool_arguments_with_error`; `utils/misc.py`: `MAX_TIMEOUT_SECONDS`, `MIN_TIMEOUT_SECONDS`, `make_id`, `normalize_timeout_seconds`, `now_ts`; `utils/text.py`: `trim`
- Symbols:
  - `OllamaError` (class, lines 11813-11816)
  - `OllamaClient` (class, lines 11818-12913)

### `llm/utils.py`

- Routed symbols: 25
- Cross-module imports: `config/constants.py`: `OPENAI_COMPAT_PROVIDER_NAMES`, `OPENAI_LIKE_PROVIDER_NAMES`; `utils/http.py`: `urlopen`; `utils/json_utils.py`: `json_dumps`, `parse_json_object`; `utils/text.py`: `trim`
- Symbols:
  - `probe_ollama_environment` (function, lines 3481-3494)
  - `list_ollama_models` (function, lines 3496-3498)
  - `_OLLAMA_TAG_CACHE_LOCK` (assignment, lines 3500-3500)
  - `_OLLAMA_TAG_CACHE` (assignment, lines 3501-3501)
  - `list_ollama_models_cached` (function, lines 3511-3548)
  - `resolve_ollama_model` (function, lines 3550-3560)
  - `infer_thinking_model` (function, lines 3562-3564)
  - `split_thinking_content` (function, lines 3566-3607)
  - `strip_thinking_content` (function, lines 3609-3610)
  - `check_ollama_model_ready` (function, lines 3612-3636)
  - `list_loaded_ollama_models` (function, lines 3638-3651)
  - `wake_ollama_model` (function, lines 3653-3683)
  - `try_pull_ollama_model` (function, lines 3685-3703)
  - `ordered_model_candidates` (function, lines 3705-3723)
  - `pick_working_ollama_model` (function, lines 3725-3741)
  - `extract_base_url` (function, lines 3774-3782)
  - `complete_chat_endpoint` (function, lines 3784-3793)
  - `normalize_openai_compat_provider_name` (function, lines 3860-3875)
  - `is_openai_compat_provider` (function, lines 3889-3890)
  - `is_openai_like_provider` (function, lines 3892-3893)
  - `openai_compat_probe_headers` (function, lines 3895-3906)
  - `openai_compat_model_list_urls` (function, lines 3908-3940)
  - `extract_openai_compat_model_ids` (function, lines 3942-3975)
  - `_is_http_url` (function, lines 3984-3989)
  - `_resolve_local_path` (function, lines 3991-4007)

### `rag/index.py`

- Routed symbols: 8
- Cross-module imports: `config/constants.py`: `RAG_DYNAMIC_NOISE_HARD_COMMUNITY_RATIO`, `RAG_DYNAMIC_NOISE_HARD_DOC_RATIO`, `RAG_DYNAMIC_NOISE_MIN_COMMUNITY_FREQ`, `RAG_DYNAMIC_NOISE_MIN_DOC_FREQ`, `RAG_DYNAMIC_NOISE_SOFT_COMMUNITY_RATIO`, `RAG_DYNAMIC_NOISE_SOFT_DOC_RATIO`, `RAG_EN_STOPWORDS`, `RAG_GRAPH_MAX_NODES`, `RAG_INCLUDE_FILENAME_ENTITIES_DEFAULT`, `RAG_MAX_COMMUNITY_MAP_SUPPORT`, `RAG_MAX_GLOBAL_COMMUNITIES`, `RAG_MAX_QUERY_RESULTS`, `RAG_SYNTHESIS_MAX_PER_DOC`; `rag/parsers.py`: `_code_is_test_path`, `_rag_apply_filename_entity_policy`, `_rag_choose_community`, `_rag_classify_document`, `_rag_expand_tokens`, `_rag_extract_entities`, `_rag_filter_entities`, `_rag_tokenize`; `utils/json_utils.py`: `json_dumps`; `utils/misc.py`: `now_ts`; `utils/text.py`: `trim`
- Symbols:
  - `_rag_trigram_set` (function, lines 49422-49427)
  - `_rag_jaccard_sim` (function, lines 49430-49437)
  - `_rag_mmr_select` (function, lines 49440-49487)
  - `_code_module_name` (function, lines 49893-49907)
  - `_code_choose_community` (function, lines 49910-49917)
  - `_code_query_terms` (function, lines 49920-49932)
  - `TFGraphIDFIndex` (class, lines 50985-52511)
  - `CodeGraphIndex` (class, lines 53987-54451)

### `rag/ingestion.py`

- Routed symbols: 5
- Cross-module imports: `config/constants.py`: `CODE_IMPORT_WORKER_COUNT`, `CODE_LIBRARY_IGNORED_DIRS`, `CODE_PARSE_TIMEOUT_SECONDS`, `RAG_IMPORT_WORKER_COUNT`, `RAG_MAX_IMPORT_BATCH_ITEMS`, `RAG_MAX_IMPORT_FILES`, `RAG_MODEL_MEDIA_MAX_BYTES`, `RAG_PARSE_TIMEOUT_SECONDS`, `RAG_PDF_IMAGE_LIMIT`; `config/settings.py`: `default_multimodal_capabilities`; `rag/parsers.py`: `CodeContentParser`, `RAGContentParser`, `_rag_extract_entities`, `_rag_safe_name`; `rag/store.py`: `CodeLibraryStore`, `RAGLibraryStore`; `session/state.py`: `SessionState`; `utils/files.py`: `try_read_text`; `utils/json_utils.py`: `_read_json_file`, `_write_json_file`, `parse_json_object`; `utils/media.py`: `guess_mime_from_name`; `utils/misc.py`: `make_id`, `now_ts`; `utils/text.py`: `trim`
- Symbols:
  - `_rag_embed_text` (function, lines 49617-49638)
  - `_rag_embed_batch` (function, lines 49641-49647)
  - `_rag_parse_file_worker` (function, lines 53100-53114)
  - `RAGIngestionService` (class, lines 53117-53984)
  - `CodeIngestionService` (class, lines 54720-54804)

### `rag/parsers.py`

- Routed symbols: 29
- Cross-module imports: `config/constants.py`: `AUDIO_EXTS`, `CODE_CHUNK_CHARS`, `CODE_CHUNK_OVERLAP`, `CODE_LIBRARY_LANGUAGE_BY_EXT`, `CODE_LIBRARY_SPECIAL_FILENAMES`, `CODE_MAX_CHUNKS_PER_DOC`, `CODE_PREVIEW_EXTS`, `CODE_PREVIEW_FILENAMES`, `CODE_PREVIEW_STAGE_MAX_ROWS`, `DOCUMENT_PREVIEW_EXTS`, `EXCEL_PREVIEW_EXTS`, `IMAGE_EXTS`, `PRESENTATION_PREVIEW_EXTS`, `RAG_CHUNK_CHARS`, `RAG_CHUNK_OVERLAP`, `RAG_CODE_HINTS`, `RAG_EN_STOPWORDS`, `RAG_GENERIC_ENTITY_TERMS_EN`, `RAG_GENERIC_ENTITY_TERMS_ZH`, `RAG_INCLUDE_FILENAME_ENTITIES_DEFAULT`, `RAG_MAX_CHUNKS_PER_DOC`, `RAG_PDF_IMAGE_LIMIT`, `RAG_RESEARCH_HINTS`, `RAG_SHORT_TOKEN_ALLOWLIST`, `RAG_STRUCTURAL_ENTITY_PATTERNS`, `RAG_TERM_GROUPS`, `RAG_ZH_STOPWORDS`, `TABULAR_PREVIEW_EXTS`, `VIDEO_EXTS`; `utils/files.py`: `_sha256_bytes`, `_sha256_file`; `utils/json_utils.py`: `parse_json_object`; `utils/media.py`: `guess_mime_from_name`; `utils/text.py`: `_compress_rows_keep_hotspot`, `_skip_row`, `trim`
- Symbols:
  - `normalize_rel_preview_path` (function, lines 5313-5324)
  - `is_code_preview_candidate` (function, lines 5327-5335)
  - `preview_kind_for_path` (function, lines 5344-5371)
  - `build_code_preview_rows` (function, lines 5374-5558)
  - `_rag_safe_name` (function, lines 49221-49224)
  - `_rag_detect_language` (function, lines 49227-49241)
  - `_rag_cjk_ngrams` (function, lines 49244-49256)
  - `_rag_is_noise_token` (function, lines 49259-49278)
  - `_rag_entity_allowed` (function, lines 49281-49293)
  - `_rag_filter_entities` (function, lines 49296-49310)
  - `_rag_filename_entity_aliases` (function, lines 49313-49346)
  - `_rag_apply_filename_entity_policy` (function, lines 49349-49379)
  - `_rag_choose_community` (function, lines 49382-49419)
  - `_rag_tokenize` (function, lines 49490-49541)
  - `_rag_expand_tokens` (function, lines 49544-49558)
  - `_rag_extract_entities` (function, lines 49561-49577)
  - `_rag_classify_document` (function, lines 49580-49614)
  - `_rag_parse_segments` (function, lines 49650-49710)
  - `_rag_chunk_text` (function, lines 49713-49792)
  - `_code_language_from_name` (function, lines 49869-49885)
  - `_code_is_test_path` (function, lines 49888-49890)
  - `_CallCollector` (class, lines 49935-49947)
  - `_ALGO_COMPLEXITY_RE` (assignment, lines 49950-49950)
  - `_ALGO_STEP_RE` (assignment, lines 49951-49951)
  - `_ALGO_MATH_VARS` (assignment, lines 49952-49952)
  - `_ALGO_DOC_KEYWORDS` (assignment, lines 49953-49953)
  - `_detect_algo_chunk` (function, lines 49956-49979)
  - `CodeContentParser` (class, lines 49982-50472)
  - `RAGContentParser` (class, lines 50475-50982)

### `rag/store.py`

- Routed symbols: 2
- Cross-module imports: `config/constants.py`: `CODE_CHUNK_CHARS`, `CODE_CHUNK_OVERLAP`, `CODE_MAX_CHUNKS_PER_DOC`, `RAG_INCLUDE_FILENAME_ENTITIES_DEFAULT`, `RAG_TASK_HISTORY_LIMIT`; `rag/index.py`: `CodeGraphIndex`, `TFGraphIDFIndex`, `_code_choose_community`, `_code_module_name`; `rag/parsers.py`: `_code_is_test_path`, `_rag_apply_filename_entity_policy`, `_rag_choose_community`, `_rag_chunk_text`, `_rag_entity_allowed`, `_rag_extract_entities`, `_rag_safe_name`; `utils/files.py`: `_sha256_bytes`, `_sha256_file`; `utils/json_utils.py`: `_read_json_file`, `_write_json_file`; `utils/media.py`: `guess_mime_from_name`; `utils/misc.py`: `make_id`, `now_ts`; `utils/text.py`: `trim`
- Symbols:
  - `RAGLibraryStore` (class, lines 52523-53097)
  - `CodeLibraryStore` (class, lines 54454-54717)

### `server/handlers.py`

- Routed symbols: 5
- Cross-module imports: `app/context.py`: `AppContext`; `config/constants.py`: `APP_VERSION`, `DEFAULT_REQUEST_TIMEOUT`, `DEFAULT_SHELL_COMMAND_TIMEOUT_SECONDS`, `DEFAULT_UI_LANGUAGE`, `DEFAULT_UI_STYLE`, `EXECUTION_MODE_CHOICES`, `EXECUTION_MODE_SYNC`, `MIN_RUN_TIMEOUT_SECONDS`, `PLAN_MODE_USER_CHOICES`, `RAG_GRAPH_MAX_NODES`, `SSE_HEARTBEAT_SECONDS`, `TASK_COMPLEXITY_LEVELS`, `TASK_LEVEL_CHOICES`, `TASK_LEVEL_POLICIES`, `UI_STYLE_LABELS`; `config/paths.py`: `LLM_CONFIG_PATH`, `REPO_ROOT`, `WORKDIR`; `config/settings.py`: `_to_bool_like`, `infer_user_complexity_value`, `looks_like_llm_config`, `normalize_execution_mode`, `normalize_task_complexity`, `normalize_ui_language`, `normalize_ui_style`, `resolve_web_ui_dir_path`, `supported_ui_languages_payload`; `llm/utils.py`: `extract_base_url`, `extract_openai_compat_model_ids`, `list_ollama_models`, `normalize_openai_compat_provider_name`, `openai_compat_model_list_urls`, `openai_compat_probe_headers`; `session/manager.py`: `SessionCreationLimitExceeded`, `SessionManager`; `session/state.py`: `SessionState`; `skills/store.py`: `analyze_skill_building_knowledge`; `utils/files.py`: `safe_path`, `try_read_text`; `utils/http.py`: `urlopen`; `utils/json_utils.py`: `json_dumps`, `parse_json_object`; `utils/media.py`: `guess_mime_from_name`; `utils/misc.py`: `now_ts`, `swallow_benign_socket_error`, `user_id_from_ip`; `utils/text.py`: `trim`
- Symbols:
  - `AgentHTTPServer` (class, lines 58929-58957)
  - `Handler` (class, lines 58961-59820)
  - `SkillsHandler` (class, lines 59822-60018)
  - `RagAdminHandler` (class, lines 60020-60174)
  - `CodeAdminHandler` (class, lines 60177-60331)

### `session/manager.py`

- Routed symbols: 2
- Cross-module imports: `config/constants.py`: `AGENT_MAX_OUTPUT_TOKENS`, `ARBITER_DEFAULT_MAX_TOKENS`, `ARBITER_DEFAULT_TEMPERATURE`, `ARBITER_DEFAULT_TIMEOUT_SECONDS`, `DEFAULT_REQUEST_TIMEOUT`, `DEFAULT_SHELL_COMMAND_TIMEOUT_SECONDS`, `DEFAULT_UI_LANGUAGE`, `EXECUTION_MODE_SYNC`, `MAX_AGENT_ROUNDS`, `MAX_AGENT_ROUNDS_CAP`, `MAX_RUN_SECONDS`, `MAX_RUN_TIMEOUT_SECONDS`, `MAX_SHELL_COMMAND_TIMEOUT_SECONDS`, `MIN_AGENT_ROUNDS`, `MIN_CONTEXT_TOKEN_LIMIT`, `MIN_RUN_TIMEOUT_SECONDS`, `MIN_SHELL_COMMAND_TIMEOUT_SECONDS`, `TOKEN_THRESHOLD`; `config/paths.py`: `LLM_CONFIG_PATH`; `config/settings.py`: `infer_model_multimodal_capabilities`, `merge_multimodal_capabilities`, `normalize_execution_mode`, `normalize_ui_language`, `parse_capability_overrides`, `parse_llm_config_profiles`; `llm/client.py`: `OllamaClient`; `llm/utils.py`: `complete_chat_endpoint`, `extract_base_url`, `is_openai_compat_provider`, `list_ollama_models_cached`, `probe_ollama_environment`; `session/state.py`: `SessionState`; `utils/crypto.py`: `CryptoBox`; `utils/files.py`: `try_read_text`; `utils/json_utils.py`: `parse_json_object`; `utils/misc.py`: `make_id`, `normalize_timeout_seconds`, `now_ts`, `sanitize_profile_id`
- Symbols:
  - `SessionCreationLimitExceeded` (class, lines 2160-2163)
  - `SessionManager` (class, lines 39275-40162)

### `session/state.py`

- Routed symbols: 1
- Cross-module imports: `agent/background.py`: `BackgroundManager`; `agent/bus.py`: `MessageBus`; `agent/events.py`: `EventHub`; `agent/tasks.py`: `TaskManager`; `agent/todo.py`: `TodoManager`; `agent/worktree.py`: `WorktreeManager`; `config/constants.py`: `AGENT_BUBBLE_ROLES`, `AGENT_CTX_LIMIT_TIER0`, `AGENT_CTX_LIMIT_TIER1`, `AGENT_CTX_LIMIT_TIER2`, `AGENT_CTX_LIMIT_TIER3`, `AGENT_MAX_OUTPUT_TOKENS`, `AGENT_MSG_LIMIT_TIER0`, `AGENT_MSG_LIMIT_TIER1`, `AGENT_MSG_LIMIT_TIER2`, `AGENT_MSG_LIMIT_TIER3`, `AGENT_ROLES`, `AGENT_TOOL_ALLOWLIST`, `ARBITER_DEFAULT_MAX_TOKENS`, `ARBITER_DEFAULT_TEMPERATURE`, `ARBITER_DEFAULT_TIMEOUT_SECONDS`, `ARBITER_TRIGGER_MIN_CONTENT_CHARS`, `ARBITER_VALID_PLANNING_STREAK_LIMIT`, `ASSISTANT_MESSAGE_EVENT_MAX_CHARS`, `ASSISTANT_TEXT_PERSIST_MAX_CHARS`, `AUDIO_EXTS`, `AUTO_CONTINUE_BUDGET_DEFAULT`, `BASH_READ_LOOP_THRESHOLD`, `BLACKBOARD_MAX_LOG_ENTRIES`, `BLACKBOARD_MAX_TEXT`, `BLACKBOARD_STATUSES`, `CHECKPOINT_INTERVAL_ROUNDS`, `CHECKPOINT_MAX_COUNT`, `CODE_PREVIEW_STAGE_MAX_BYTES`, `CODE_PREVIEW_STAGE_MAX_PER_FILE`, `CODE_PREVIEW_STAGE_MAX_ROWS`, `CODE_PREVIEW_STAGE_MAX_TOTAL`, `COMPACT_TIER1_ABS`, `COMPACT_TIER1_PCT`, `COMPACT_TIER2_ABS`, `COMPACT_TIER2_PCT`, `COMPACT_TIER3_PCT`, `DANGEROUS_PATTERNS`, `DEEP_RESEARCH_REQUEST_KEYWORDS`, `DEEP_RESEARCH_RETRIEVAL_KEYWORDS`, `DEEP_RESEARCH_TEXT_ONLY_HINT_KEYWORDS`, `DEFAULT_REQUEST_TIMEOUT`, `DEFAULT_SHELL_COMMAND_TIMEOUT_SECONDS`, `DEFAULT_UI_LANGUAGE`, `DEVELOPER_EDIT_STALL_THRESHOLD`, `EMPTY_ACTION_MIN_CONTENT_CHARS`, `EMPTY_ACTION_WAKEUP_RETRY_LIMIT`, `ERROR_CATEGORY_DEFS`, `EXECUTION_MODE_CHOICES`, `EXECUTION_MODE_SEQUENTIAL`, `EXECUTION_MODE_SINGLE`, `EXECUTION_MODE_SYNC`, `EXPLORER_STALL_THRESHOLD`, `FAILURE_LEDGER_MAX_COMPILE_ERRORS`, `FAILURE_LEDGER_MAX_DELEGATIONS`, `FAILURE_LEDGER_MAX_ERRORS`, `FAILURE_LEDGER_MAX_FIXES`, `FAILURE_LEDGER_MAX_STALLS`, `FAILURE_LEDGER_MAX_TOOL_FPS`, `FILE_BUFFER_CONTENT_THRESHOLD`, `FILE_BUFFER_MAX_FILES`, `FINAL_SUMMARY_MIN_CHARS`, `FINAL_SUMMARY_STRICT_MIN_CHARS`, `FUSED_FAULT_BREAK_THRESHOLD`, `HARD_BREAK_RECOVERY_ROUND_THRESHOLD`, `HARD_BREAK_TOOL_ERROR_THRESHOLD`, `HTML_FRONTEND_REQUEST_KEYWORDS`, `IMAGE_EXTS`, `IMAGE_FORMATS_NEED_CONVERSION`, `LIVE_INPUT_DELAY_NORMAL_ROUNDS`, `LIVE_INPUT_DELAY_TOOL_ROUNDS`, `LIVE_INPUT_DELAY_WRITE_ROUNDS`, `LIVE_INPUT_MAX_INJECTIONS`, `LIVE_INPUT_REINJECT_INTERVAL`, `LIVE_INPUT_WEIGHT_BASE_DELAYED`, `LIVE_INPUT_WEIGHT_BASE_NORMAL`, `LIVE_INPUT_WEIGHT_STEP_DELAYED`, `LIVE_INPUT_WEIGHT_STEP_NORMAL`, `LONG_OUTPUT_LISTING_OFFLOAD_CHARS`, `LONG_OUTPUT_MODEL_PAGE_CHARS`, `LONG_OUTPUT_READ_PAGE_LINES`, `LONG_OUTPUT_READ_PAGE_MAX_CHARS`, `LONG_OUTPUT_TEMP_MAX_FILES`, `LONG_OUTPUT_UI_PAGE_CHARS`, `LONG_OUTPUT_UI_PREVIEW_MAX_PAGES`, `MANAGER_CTX_LIMIT_TIER0`, `MANAGER_CTX_LIMIT_TIER1`, `MANAGER_CTX_LIMIT_TIER2`, `MANAGER_CTX_LIMIT_TIER3`, `MANAGER_ROUTE_TARGETS`, `MAX_AGENT_ROUNDS`, `MAX_AGENT_ROUNDS_CAP`, `MAX_CONTEXT_ARCHIVE_SEGMENTS`, `MAX_RUN_SECONDS`, `MAX_RUN_TIMEOUT_SECONDS`, `MAX_SHELL_COMMAND_TIMEOUT_SECONDS`, `MIN_AGENT_ROUNDS`, `MIN_CONTEXT_TOKEN_LIMIT`, `MIN_RUN_TIMEOUT_SECONDS`, `MIN_SHELL_COMMAND_TIMEOUT_SECONDS`, `MODEL_CALL_PROGRESS_DELAY`, `MODEL_CALL_PROGRESS_INTERVAL`, `MODEL_OUTPUT_RETRY_TIMES`, `PERSISTED_ROUTES_MAX`, `PLAN_BUBBLE_MAX_CHARS`, `PLAN_FILE_RELATIVE_PATH`, `PLAN_MESSAGE_EVENT_MAX_CHARS`, `PLAN_MODE_ENABLED_LEVELS`, `PLAN_MODE_EXPLORER_MAX_ROUNDS`, `PLAN_MODE_FORCED_LEVELS`, `PLAN_MODE_MANAGER_SYNTHESIS_MAX_TOKENS`, `PLAN_MODE_MAX_OPTIONS`, `PLAN_MODE_RESEARCH_TOOL_ALLOWLIST`, `PLAN_MODE_SYNTHESIS_MAX_ATTEMPTS`, `PLAN_MODE_USER_CHOICES`, `PLAN_NOTICE_BODY_MAX_CHARS`, `PLAN_STEP_FULL_CONTENT_MAX_CHARS`, `RENDER_FRAME_ACTIVITY_INTERVAL_SECONDS`, `RENDER_FRAME_MAX_B64_CHARS`, `RENDER_FRAME_MAX_LINES`, `RENDER_FRAME_MAX_LINE_POINTS`, `RENDER_FRAME_MAX_POINTS`, `REPEATED_TOOL_LOOP_THRESHOLD`, `RETRY_RUNTIME_HINT_PREFIXES`, `REVIEWER_DEBUG_MODE_MAX_ROUNDS`, `RUNTIME_CONTROL_HINT_PREFIXES`, `SEMANTIC_CONFIDENCE_CHOICES`, `SKILLS_VIRTUAL_PREFIX`, `SKILL_REFRESH_MIN_INTERVAL_SECONDS`, `SKILL_RUNTIME_CACHE_MAX_BYTES`, `SKILL_RUNTIME_CACHE_MAX_ENTRIES`, `STALL_ESCALATION_CONTEXT_MAX_CHARS`, `STALL_ESCALATION_MIN_LEVEL`, `STALL_PLAN_SYNTHESIS_MAX_TOKENS`, `STALL_SEVERITY_DECAY_ON_SUCCESS`, `STALL_SEVERITY_ESCALATION_THRESHOLD`, `STALL_SEVERITY_WEIGHT_BASH_READ_LOOP`, `STALL_SEVERITY_WEIGHT_FAULT`, `STALL_SEVERITY_WEIGHT_RECOVERY_RETRY`, `STALL_SEVERITY_WEIGHT_REPEATED_TOOL`, `STALL_SEVERITY_WEIGHT_WATCHDOG`, `TASK_COMPLEXITY_LEVELS`, `TASK_LEVEL_CHOICES`, `TASK_LEVEL_POLICIES`, `TASK_PHASE_ROUTING`, `TASK_PROFILE_TYPES`, `TASK_SCALE_PREFERENCES`, `THINKING_BUDGET_FORCE_RATIO`, `TOKEN_THRESHOLD`, `TRUNCATION_CONTINUATION_ECHO_CHARS`, `TRUNCATION_CONTINUATION_MAX_PASSES`, `TRUNCATION_CONTINUATION_MAX_TOKENS`, `TRUNCATION_CONTINUATION_TAIL_CHARS`, `TRUNCATION_LIVE_BUFFER_MAX_CHARS`, `TRUNCATION_OVERLAP_SCAN_CHARS`, `TRUNCATION_PAIR_SCAN_CHARS`, `VIDEO_EXTS`, `WATCHDOG_CONTEXT_NEAR_RATIO`, `WATCHDOG_CONTEXT_STALL_THRESHOLD`, `WATCHDOG_INTENT_NO_TOOL_THRESHOLD`, `WATCHDOG_INTENT_NO_TOOL_THRESHOLD_SINGLE`, `WATCHDOG_MAX_DECOMPOSE_STEPS`, `WATCHDOG_REPEAT_NO_TOOL_THRESHOLD`, `WATCHDOG_REPEAT_NO_TOOL_THRESHOLD_SINGLE`, `WATCHDOG_REPEAT_SIMILARITY_THRESHOLD`, `WATCHDOG_STATE_STALL_THRESHOLD`, `WATCHDOG_STEP_MAX_ATTEMPTS`, `_DEFAULT_TOOL_TIMEOUT`, `_SHELL_AUTO_CONFIRM_PATTERNS`, `_TOOL_TIMEOUT_MAP`; `config/paths.py`: `WORKDIR`; `config/settings.py`: `_detect_os_shell_instruction`, `_to_bool_like`, `backend_i18n_text`, `backend_role_label`, `default_multimodal_capabilities`, `infer_model_multimodal_capabilities`, `infer_user_complexity_value`, `looks_like_llm_config`, `max_task_complexity`, `merge_multimodal_capabilities`, `model_language_instruction`, `normalize_execution_mode`, `normalize_task_complexity`, `normalize_ui_language`, `parse_capability_overrides`, `parse_llm_config_profiles`, `task_complexity_at_least`, `task_complexity_rank`; `llm/client.py`: `OllamaClient`, `OllamaError`; `llm/utils.py`: `complete_chat_endpoint`, `extract_base_url`, `is_openai_compat_provider`, `list_loaded_ollama_models`, `list_ollama_models`, `list_ollama_models_cached`, `probe_ollama_environment`, `resolve_ollama_model`, `split_thinking_content`, `strip_thinking_content`, `wake_ollama_model`; `rag/parsers.py`: `build_code_preview_rows`, `is_code_preview_candidate`, `normalize_rel_preview_path`, `preview_kind_for_path`; `skills/store.py`: `SkillStore`, `ensure_runtime_skills`; `utils/compress.py`: `compress_text_blob`, `decompress_text_blob`; `utils/crypto.py`: `CryptoBox`; `utils/errors.py`: `CircuitBreakerTriggered`, `EmptyActionError`; `utils/files.py`: `_normalize_external_js_url`, `_safe_js_filename`, `cache_external_js_url`, `ensure_offline_js_libs`, `is_external_js_src`, `load_offline_js_lib_index`, `match_offline_js_catalog_by_url`, `offline_js_lib_root`, `safe_path`, `try_read_text`; `utils/http.py`: `urlopen`; `utils/json_utils.py`: `TOOLS`, `TOOL_REQUIRED_ARGS`, `canonicalize_tool_name`, `extract_json_object_from_text`, `json_dumps`, `parse_json_object`, `parse_tool_arguments_with_error`, `repair_truncated_json_object`, `tool_def`; `utils/media.py`: `_convert_image_to_safe_format`, `guess_ext_from_mime`, `guess_mime_from_name`; `utils/misc.py`: `MAX_TIMEOUT_SECONDS`, `MIN_TIMEOUT_SECONDS`, `is_benign_socket_error`, `make_id`, `normalize_timeout_seconds`, `now_ts`, `sanitize_profile_id`; `utils/text.py`: `MAX_TOOL_OUTPUT`, `_fmt_export_ts`, `_html_esc`, `_text_to_minimal_pdf`, `extract_todo_rows_from_text`, `filter_runtime_noise_lines`, `make_numbered_diff`, `make_unified_diff`, `normalize_embedded_newlines`, `normalize_work_text`, `parse_front_matter`, `render_numbered_diff_text`, `split_structured_todo_content`, `split_todo_status_text`, `trim`
- Symbols:
  - `SessionState` (class, lines 13205-39273)

### `skills/store.py`

- Routed symbols: 26
- Cross-module imports: `config/constants.py`: `BUILTIN_CLAWHUB_SKILLS_VERSION`, `EMBEDDED_CLAWHUB_SKILLS_ARCHIVE_B64`, `EMBEDDED_SKILLS_ARCHIVE_B64`, `EMBEDDED_SKILLS_ARCHIVE_FILES`, `EMBEDDED_SKILLS_ARCHIVE_SHA256`, `SKILLS_EXTERNAL_MOUNT`, `SKILLS_VIRTUAL_PREFIX`, `SKILL_BODY_COMPACT_THRESHOLD_CHARS`, `SKILL_BODY_PREVIEW_CHARS`, `SKILL_DEFAULT_ATTACHMENT_GLOBS`, `SKILL_INLINE_ATTACHMENT_MAX_CHARS`, `SKILL_INLINE_ATTACHMENT_MAX_FILES`, `SKILL_PROMPT_MAX_CHARS`, `SKILL_PROMPT_MAX_ITEMS`, `SKILL_PROTOCOL_CLAWHUB`, `SKILL_PROTOCOL_HTTP_JSON`, `SKILL_PROTOCOL_LOCAL`, `SKILL_PROTOCOL_SPECS`, `SKILL_REFRESH_MIN_INTERVAL_SECONDS`, `SKILL_RESOURCE_MANIFEST_MAX_ITEMS`; `config/paths.py`: `WORKDIR`; `llm/utils.py`: `_is_http_url`; `utils/files.py`: `_render_offline_js_catalog_md`, `safe_path`, `try_read_text`; `utils/http.py`: `urlopen`; `utils/json_utils.py`: `json_dumps`, `parse_json_object`; `utils/misc.py`: `_meta_string_list`, `_module_exists`, `now_ts`; `utils/text.py`: `parse_front_matter`, `trim`
- Symbols:
  - `ensure_embedded_skills_at_root` (function, lines 6425-6477)
  - `ensure_embedded_skills` (function, lines 6480-6481)
  - `detect_upload_parser_capabilities` (function, lines 6489-6504)
  - `_render_cap_markdown` (function, lines 6506-6520)
  - `_write_text_if_changed` (function, lines 6522-6527)
  - `ensure_generated_document_skills` (function, lines 6529-6617)
  - `ensure_generated_image_coding_feedback_skill` (function, lines 6619-6718)
  - `_skill_knowledge_files` (function, lines 6720-6739)
  - `analyze_skill_building_knowledge` (function, lines 6741-6795)
  - `_sanitize_skill_slug` (function, lines 6797-6799)
  - `_build_skills_gen_skill_content` (function, lines 6801-6832)
  - `ensure_generated_skills_gen_skill` (function, lines 6834-6838)
  - `ensure_generated_execution_recovery_skill` (function, lines 6840-6918)
  - `ensure_generated_systematic_debugging_skill` (function, lines 6920-7192)
  - `ensure_generated_code_engineering_mastery_skill` (function, lines 7194-7312)
  - `ensure_generated_smart_file_navigation_skill` (function, lines 7314-7432)
  - `ensure_generated_html_frontend_report_skills` (function, lines 7434-7641)
  - `ensure_generated_deep_research_skills` (function, lines 7643-7911)
  - `ensure_generated_research_scientific_skills` (function, lines 7913-8549)
  - `ensure_generated_rag_mastery_skills` (function, lines 8555-8851)
  - `ensure_generated_multimodal_comprehension_skills` (function, lines 8857-9546)
  - `ensure_generated_runtime_skills_manifest` (function, lines 9549-9580)
  - `ensure_embedded_clawhub_skills` (function, lines 9838-9875)
  - `ensure_runtime_skills` (function, lines 9877-9892)
  - `_BUILTIN_SKILLS` (assignment, lines 9934-10022)
  - `SkillStore` (class, lines 10031-11325)

### `utils/compress.py`

- Routed symbols: 2
- Cross-module imports: none
- Symbols:
  - `compress_text_blob` (function, lines 3115-3120)
  - `decompress_text_blob` (function, lines 3122-3130)

### `utils/crypto.py`

- Routed symbols: 1
- Cross-module imports: `utils/json_utils.py`: `json_dumps`
- Symbols:
  - `CryptoBox` (class, lines 4717-4834)

### `utils/errors.py`

- Routed symbols: 2
- Cross-module imports: none
- Symbols:
  - `EmptyActionError` (class, lines 3504-3505)
  - `CircuitBreakerTriggered` (class, lines 3508-3509)

### `utils/files.py`

- Routed symbols: 25
- Cross-module imports: `config/constants.py`: `OFFLINE_JS_LIB_CATALOG`, `OFFLINE_JS_LIB_INDEX_FILE`, `OFFLINE_JS_LIB_README_FILE`; `config/paths.py`: `WORKDIR`; `utils/http.py`: `urlopen`; `utils/json_utils.py`: `json_dumps`; `utils/misc.py`: `now_ts`; `utils/text.py`: `trim`
- Symbols:
  - `_normalize_js_lib_asset_ref` (function, lines 1218-1231)
  - `_resolve_js_lib_asset_path` (function, lines 1234-1263)
  - `_discover_extra_js_lib_files` (function, lines 1266-1296)
  - `safe_path` (function, lines 2492-2501)
  - `_safe_js_filename` (function, lines 2503-2510)
  - `_sha256_bytes` (function, lines 2512-2513)
  - `_sha256_file` (function, lines 2515-2523)
  - `_download_http_bytes` (function, lines 2525-2533)
  - `offline_js_lib_root` (function, lines 2535-2536)
  - `_offline_js_entry_relative_path` (function, lines 2538-2542)
  - `_archive_member_relative_path` (function, lines 2544-2553)
  - `_path_size_bytes` (function, lines 2555-2570)
  - `_extract_archive_to_dir` (function, lines 2572-2612)
  - `_package_required_paths` (function, lines 2614-2620)
  - `_package_install_ready` (function, lines 2622-2630)
  - `_postprocess_offline_js_package` (function, lines 2632-2667)
  - `_ensure_offline_js_package` (function, lines 2669-2708)
  - `_render_offline_js_catalog_md` (function, lines 2710-2726)
  - `load_offline_js_lib_index` (function, lines 2728-2737)
  - `ensure_offline_js_libs` (function, lines 2739-2883)
  - `_normalize_external_js_url` (function, lines 2885-2889)
  - `is_external_js_src` (function, lines 2891-2893)
  - `match_offline_js_catalog_by_url` (function, lines 2895-2911)
  - `cache_external_js_url` (function, lines 2913-2945)
  - `try_read_text` (function, lines 5039-5047)

### `utils/http.py`

- Routed symbols: 4
- Cross-module imports: none
- Symbols:
  - `_URL_OPEN_ORIGINAL` (assignment, lines 56-56)
  - `_HTTP_SSL_CONTEXT` (assignment, lines 57-57)
  - `_shared_http_ssl_context` (function, lines 70-85)
  - `urlopen` (function, lines 87-95)

### `utils/json_utils.py`

- Routed symbols: 16
- Cross-module imports: `utils/text.py`: `trim`
- Symbols:
  - `JSON_FSYNC_ENABLED` (constant, lines 144-144)
  - `json_dumps` (function, lines 2464-2465)
  - `parse_tool_arguments` (function, lines 3383-3392)
  - `repair_truncated_json_object` (function, lines 3394-3447)
  - `parse_tool_arguments_with_error` (function, lines 3449-3479)
  - `parse_json_object` (function, lines 3743-3748)
  - `extract_json_object_from_text` (function, lines 3750-3772)
  - `_json_default_copy` (function, lines 5049-5054)
  - `_read_json_file` (function, lines 5056-5076)
  - `_write_json_file` (function, lines 5078-5105)
  - `tool_def` (function, lines 12915-12927)
  - `TOOLS` (constant, lines 12929-13105)
  - `TOOL_REQUIRED_ARGS` (constant, lines 13107-13107)
  - `TOOL_SPEC_BY_NAME` (constant, lines 13108-13108)
  - `TOOL_NAME_FUZZY_MAP` (constant, lines 13120-13120)
  - `canonicalize_tool_name` (function, lines 13138-13149)

### `utils/media.py`

- Routed symbols: 3
- Cross-module imports: none
- Symbols:
  - `guess_mime_from_name` (function, lines 2304-2306)
  - `_convert_image_to_safe_format` (function, lines 2309-2326)
  - `guess_ext_from_mime` (function, lines 2329-2335)

### `utils/misc.py`

- Routed symbols: 19
- Cross-module imports: none
- Symbols:
  - `MIN_TIMEOUT_SECONDS` (constant, lines 219-219)
  - `MAX_TIMEOUT_SECONDS` (constant, lines 220-220)
  - `DEFAULT_TIMEOUT_SECONDS` (constant, lines 221-227)
  - `BENIGN_SOCKET_DEBUG_LOG_ENABLED` (constant, lines 350-356)
  - `BENIGN_SOCKET_LOG_INTERVAL_SECONDS` (constant, lines 357-357)
  - `now_ts` (function, lines 2337-2338)
  - `_benign_socket_log_lock` (assignment, lines 2341-2341)
  - `_benign_socket_log_state` (assignment, lines 2342-2342)
  - `is_benign_socket_error` (function, lines 2360-2378)
  - `_socket_error_code` (function, lines 2381-2390)
  - `_log_benign_socket_error_limited` (function, lines 2393-2427)
  - `swallow_benign_socket_error` (function, lines 2430-2434)
  - `normalize_timeout_seconds` (function, lines 2437-2450)
  - `detect_local_lan_ip` (function, lines 2452-2462)
  - `make_id` (function, lines 2467-2468)
  - `sanitize_profile_id` (function, lines 2470-2472)
  - `user_id_from_ip` (function, lines 4709-4715)
  - `_meta_string_list` (function, lines 5026-5037)
  - `_module_exists` (function, lines 6483-6487)

### `utils/text.py`

- Routed symbols: 22
- Cross-module imports: none
- Symbols:
  - `MAX_TOOL_OUTPUT` (constant, lines 136-136)
  - `SOCKET_NOISE_LINE_PATTERNS` (constant, lines 344-349)
  - `filter_runtime_noise_lines` (function, lines 2345-2357)
  - `trim` (function, lines 2947-2949)
  - `_fmt_export_ts` (function, lines 2952-2960)
  - `_html_esc` (function, lines 2963-2964)
  - `_text_to_minimal_pdf` (function, lines 2967-3113)
  - `normalize_embedded_newlines` (function, lines 3132-3140)
  - `_map_todo_status_token` (function, lines 3143-3158)
  - `split_todo_status_text` (function, lines 3161-3216)
  - `extract_todo_rows_from_text` (function, lines 3219-3286)
  - `infer_todo_status_from_text` (function, lines 3289-3295)
  - `split_structured_todo_content` (function, lines 3298-3351)
  - `normalize_work_text` (function, lines 3354-3381)
  - `parse_front_matter` (function, lines 4836-5023)
  - `make_unified_diff` (function, lines 5107-5124)
  - `_skip_row` (function, lines 5126-5130)
  - `_row_is_hot` (function, lines 5133-5134)
  - `_hotspot_index` (function, lines 5137-5158)
  - `_compress_rows_keep_hotspot` (function, lines 5161-5208)
  - `make_numbered_diff` (function, lines 5211-5296)
  - `render_numbered_diff_text` (function, lines 5298-5310)
