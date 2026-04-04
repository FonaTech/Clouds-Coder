# Code_Structure Framework

## Overview

- Source file: `/Users/macbookair/Downloads/Split Coder/Clouds_Coder.py`
- Output directory: `/Users/macbookair/Downloads/Split Coder/Code_Structure`
- Generated modules: 30
- Top-level symbols: 530
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
| `config/constants.py` | 293 | `utils/json_utils.py`, `utils/misc.py` |
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
  - `main` (function, lines 54652-55633)
  - `_main_guard_55635` (main_guard, lines 55635-55636)

### `agent/background.py`

- Routed symbols: 1
- Cross-module imports: `utils/misc.py`: `make_id`, `now_ts`; `utils/text.py`: `trim`
- Symbols:
  - `BackgroundManager` (class, lines 11408-11488)

### `agent/bus.py`

- Routed symbols: 1
- Cross-module imports: `config/constants.py`: `VALID_MSG_TYPES`; `utils/crypto.py`: `CryptoBox`; `utils/misc.py`: `now_ts`
- Symbols:
  - `MessageBus` (class, lines 11490-11544)

### `agent/events.py`

- Routed symbols: 1
- Cross-module imports: none
- Symbols:
  - `EventHub` (class, lines 5527-5572)

### `agent/tasks.py`

- Routed symbols: 1
- Cross-module imports: `utils/crypto.py`: `CryptoBox`; `utils/json_utils.py`: `json_dumps`; `utils/misc.py`: `now_ts`
- Symbols:
  - `TaskManager` (class, lines 11280-11406)

### `agent/todo.py`

- Routed symbols: 1
- Cross-module imports: `config/constants.py`: `DEFAULT_UI_LANGUAGE`; `config/settings.py`: `backend_i18n_text`, `backend_role_label`, `normalize_ui_language`; `utils/text.py`: `infer_todo_status_from_text`, `normalize_work_text`, `split_structured_todo_content`, `trim`
- Symbols:
  - `TodoManager` (class, lines 5574-5843)

### `agent/worktree.py`

- Routed symbols: 1
- Cross-module imports: `agent/tasks.py`: `TaskManager`; `config/constants.py`: `DANGEROUS_PATTERNS`; `utils/crypto.py`: `CryptoBox`; `utils/json_utils.py`: `json_dumps`; `utils/misc.py`: `now_ts`; `utils/text.py`: `trim`
- Symbols:
  - `WorktreeManager` (class, lines 11546-11757)

### `app/context.py`

- Routed symbols: 1
- Cross-module imports: `config/constants.py`: `AGENT_MAX_OUTPUT_TOKENS`, `APP_CSS`, `APP_JS`, `APP_TS`, `ARBITER_DEFAULT_MAX_TOKENS`, `ARBITER_DEFAULT_TEMPERATURE`, `ARBITER_DEFAULT_TIMEOUT_SECONDS`, `CODE_ADMIN_CSS`, `CODE_ADMIN_INDEX_HTML`, `CODE_ADMIN_JS`, `CODE_IMPORT_WORKER_COUNT`, `CODE_LIBRARY_DIRNAME`, `CODE_PARSE_TIMEOUT_SECONDS`, `DEFAULT_REQUEST_TIMEOUT`, `DEFAULT_SHELL_COMMAND_TIMEOUT_SECONDS`, `DEFAULT_UI_LANGUAGE`, `DEFAULT_UI_STYLE`, `DEFAULT_WEB_UI_DIR`, `EXECUTION_MODE_SYNC`, `INDEX_HTML`, `MAX_AGENT_ROUNDS`, `MAX_AGENT_ROUNDS_CAP`, `MAX_RUN_SECONDS`, `MAX_RUN_TIMEOUT_SECONDS`, `MAX_SHELL_COMMAND_TIMEOUT_SECONDS`, `MIN_AGENT_ROUNDS`, `MIN_CONTEXT_TOKEN_LIMIT`, `MIN_RUN_TIMEOUT_SECONDS`, `MIN_SHELL_COMMAND_TIMEOUT_SECONDS`, `RAG_ADMIN_CSS`, `RAG_ADMIN_INDEX_HTML`, `RAG_ADMIN_JS`, `RAG_GRAPH_MAX_NODES`, `RAG_IMPORT_WORKER_COUNT`, `RAG_INCLUDE_FILENAME_ENTITIES_DEFAULT`, `RAG_LIBRARY_DIRNAME`, `RAG_MAX_GLOBAL_COMMUNITIES`, `RAG_MAX_IMPORT_BATCH_BYTES`, `RAG_MAX_IMPORT_BATCH_ITEMS`, `RAG_MAX_IMPORT_FILES`, `RAG_MAX_QUERY_RESULTS`, `RAG_PARSE_TIMEOUT_SECONDS`, `RAG_QUERY_CONTEXT_CHARS`, `SKILLS_APP_JS`, `SKILLS_EXTRA_CSS`, `SKILLS_INDEX_HTML`, `SKILL_REFRESH_MIN_INTERVAL_SECONDS`, `TOKEN_THRESHOLD`, `WEB_UI_OPTIONAL_FILES`, `WEB_UI_REQUIRED_FILES`; `config/paths.py`: `LLM_CONFIG_PATH`, `REPO_ROOT`, `_migrate_legacy_runtime_roots`; `config/settings.py`: `default_multimodal_capabilities`, `infer_model_multimodal_capabilities`, `merge_multimodal_capabilities`, `model_language_instruction`, `normalize_execution_mode`, `normalize_ui_language`, `normalize_ui_style`, `parse_capability_overrides`, `parse_llm_config_profiles`, `resolve_optional_file_path`, `resolve_web_ui_dir_path`; `llm/client.py`: `OllamaClient`; `llm/utils.py`: `extract_base_url`; `rag/ingestion.py`: `CodeIngestionService`, `RAGIngestionService`; `rag/parsers.py`: `CodeContentParser`, `RAGContentParser`; `rag/store.py`: `CodeLibraryStore`, `RAGLibraryStore`; `session/manager.py`: `SessionCreationLimitExceeded`, `SessionManager`; `session/state.py`: `SessionState`; `skills/store.py`: `SkillStore`, `_sanitize_skill_slug`, `analyze_skill_building_knowledge`, `ensure_runtime_skills`; `utils/crypto.py`: `CryptoBox`; `utils/files.py`: `_resolve_js_lib_asset_path`, `ensure_offline_js_libs`, `load_offline_js_lib_index`, `offline_js_lib_root`, `safe_path`, `try_read_text`; `utils/json_utils.py`: `TOOLS`, `extract_json_object_from_text`, `json_dumps`, `parse_json_object`; `utils/misc.py`: `DEFAULT_TIMEOUT_SECONDS`, `MAX_TIMEOUT_SECONDS`, `MIN_TIMEOUT_SECONDS`, `normalize_timeout_seconds`, `now_ts`, `sanitize_profile_id`; `utils/text.py`: `parse_front_matter`, `trim`
- Symbols:
  - `AppContext` (class, lines 50815-53248)

### `config/constants.py`

- Routed symbols: 293
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
  - `MIN_SHELL_COMMAND_TIMEOUT_SECONDS` (constant, lines 219-219)
  - `MAX_SHELL_COMMAND_TIMEOUT_SECONDS` (constant, lines 220-220)
  - `DEFAULT_SHELL_COMMAND_TIMEOUT_SECONDS` (constant, lines 221-235)
  - `AUTO_CONTINUE_BUDGET_DEFAULT` (constant, lines 236-236)
  - `AGENT_MAX_OUTPUT_TOKENS` (constant, lines 237-237)
  - `OLLAMA_THINKING_TOOL_BUFFER` (constant, lines 238-238)
  - `WATCHDOG_INTENT_NO_TOOL_THRESHOLD` (constant, lines 239-239)
  - `WATCHDOG_REPEAT_NO_TOOL_THRESHOLD` (constant, lines 240-240)
  - `WATCHDOG_INTENT_NO_TOOL_THRESHOLD_SINGLE` (constant, lines 241-241)
  - `WATCHDOG_REPEAT_NO_TOOL_THRESHOLD_SINGLE` (constant, lines 242-242)
  - `WATCHDOG_STATE_STALL_THRESHOLD` (constant, lines 243-243)
  - `WATCHDOG_CONTEXT_STALL_THRESHOLD` (constant, lines 244-244)
  - `WATCHDOG_REPEAT_SIMILARITY_THRESHOLD` (constant, lines 245-245)
  - `WATCHDOG_CONTEXT_NEAR_RATIO` (constant, lines 246-246)
  - `WATCHDOG_MAX_DECOMPOSE_STEPS` (constant, lines 247-247)
  - `WATCHDOG_STEP_MAX_ATTEMPTS` (constant, lines 248-248)
  - `EMPTY_ACTION_MIN_CONTENT_CHARS` (constant, lines 249-249)
  - `EMPTY_ACTION_WAKEUP_RETRY_LIMIT` (constant, lines 250-250)
  - `THINKING_BUDGET_FORCE_RATIO` (constant, lines 251-251)
  - `_TOOL_TIMEOUT_MAP` (assignment, lines 253-269)
  - `_DEFAULT_TOOL_TIMEOUT` (assignment, lines 270-270)
  - `TRUNCATION_CONTINUATION_MAX_PASSES` (constant, lines 271-271)
  - `TRUNCATION_CONTINUATION_MAX_TOKENS` (constant, lines 272-272)
  - `TRUNCATION_CONTINUATION_TAIL_CHARS` (constant, lines 273-273)
  - `TRUNCATION_CONTINUATION_ECHO_CHARS` (constant, lines 274-274)
  - `TRUNCATION_OVERLAP_SCAN_CHARS` (constant, lines 275-275)
  - `TRUNCATION_PAIR_SCAN_CHARS` (constant, lines 276-276)
  - `TRUNCATION_LIVE_BUFFER_MAX_CHARS` (constant, lines 277-277)
  - `MIN_CONTEXT_TOKEN_LIMIT` (constant, lines 278-278)
  - `COMPACT_TIER1_PCT` (constant, lines 280-280)
  - `COMPACT_TIER2_PCT` (constant, lines 281-281)
  - `COMPACT_TIER3_PCT` (constant, lines 282-282)
  - `COMPACT_TIER1_ABS` (constant, lines 284-284)
  - `COMPACT_TIER2_ABS` (constant, lines 285-285)
  - `FILE_BUFFER_CONTENT_THRESHOLD` (constant, lines 287-287)
  - `FILE_BUFFER_MAX_FILES` (constant, lines 288-288)
  - `AGENT_MSG_LIMIT_TIER0` (constant, lines 290-290)
  - `AGENT_MSG_LIMIT_TIER1` (constant, lines 291-291)
  - `AGENT_MSG_LIMIT_TIER2` (constant, lines 292-292)
  - `AGENT_MSG_LIMIT_TIER3` (constant, lines 293-293)
  - `AGENT_CTX_LIMIT_TIER0` (constant, lines 294-294)
  - `AGENT_CTX_LIMIT_TIER1` (constant, lines 295-295)
  - `AGENT_CTX_LIMIT_TIER2` (constant, lines 296-296)
  - `AGENT_CTX_LIMIT_TIER3` (constant, lines 297-297)
  - `MANAGER_CTX_LIMIT_TIER0` (constant, lines 298-298)
  - `MANAGER_CTX_LIMIT_TIER1` (constant, lines 299-299)
  - `MANAGER_CTX_LIMIT_TIER2` (constant, lines 300-300)
  - `MANAGER_CTX_LIMIT_TIER3` (constant, lines 301-301)
  - `MAX_CONTEXT_ARCHIVE_SEGMENTS` (constant, lines 302-302)
  - `MODEL_OUTPUT_RETRY_TIMES` (constant, lines 303-303)
  - `ARBITER_TRIGGER_MIN_CONTENT_CHARS` (constant, lines 304-304)
  - `ARBITER_VALID_PLANNING_STREAK_LIMIT` (constant, lines 305-305)
  - `ARBITER_DEFAULT_TIMEOUT_SECONDS` (constant, lines 306-306)
  - `ARBITER_DEFAULT_MAX_TOKENS` (constant, lines 307-307)
  - `ARBITER_DEFAULT_TEMPERATURE` (constant, lines 308-308)
  - `LIVE_INPUT_DELAY_WRITE_ROUNDS` (constant, lines 309-309)
  - `LIVE_INPUT_DELAY_TOOL_ROUNDS` (constant, lines 310-310)
  - `LIVE_INPUT_DELAY_NORMAL_ROUNDS` (constant, lines 311-311)
  - `LIVE_INPUT_MAX_INJECTIONS` (constant, lines 312-312)
  - `LIVE_INPUT_REINJECT_INTERVAL` (constant, lines 313-313)
  - `LIVE_INPUT_WEIGHT_BASE_DELAYED` (constant, lines 314-314)
  - `LIVE_INPUT_WEIGHT_BASE_NORMAL` (constant, lines 315-315)
  - `LIVE_INPUT_WEIGHT_STEP_DELAYED` (constant, lines 316-316)
  - `LIVE_INPUT_WEIGHT_STEP_NORMAL` (constant, lines 317-317)
  - `FINAL_SUMMARY_MIN_CHARS` (constant, lines 332-332)
  - `FINAL_SUMMARY_STRICT_MIN_CHARS` (constant, lines 333-333)
  - `RUNTIME_CONTROL_HINT_PREFIXES` (constant, lines 334-351)
  - `RETRY_RUNTIME_HINT_PREFIXES` (constant, lines 352-366)
  - `EXECUTION_MODE_SINGLE` (constant, lines 367-367)
  - `EXECUTION_MODE_SEQUENTIAL` (constant, lines 368-368)
  - `EXECUTION_MODE_SYNC` (constant, lines 369-369)
  - `EXECUTION_MODE_CHOICES` (constant, lines 370-374)
  - `AGENT_ROLES` (constant, lines 375-375)
  - `AGENT_BUBBLE_ROLES` (constant, lines 376-376)
  - `AGENT_ROLE_LABELS` (constant, lines 377-383)
  - `AGENT_ROLE_BUBBLE_COLORS` (constant, lines 384-390)
  - `BLACKBOARD_STATUSES` (constant, lines 391-400)
  - `TASK_COMPLEXITY_LEVELS` (constant, lines 401-401)
  - `TASK_COMPLEXITY_RANKS` (constant, lines 402-407)
  - `TASK_PROFILE_TYPES` (constant, lines 408-414)
  - `TASK_LEVEL_CHOICES` (constant, lines 415-415)
  - `TASK_SCALE_PREFERENCES` (constant, lines 416-416)
  - `SEMANTIC_CONFIDENCE_CHOICES` (constant, lines 417-417)
  - `TASK_LEVEL_POLICIES` (constant, lines 418-464)
  - `MANAGER_ROUTE_TARGETS` (constant, lines 465-465)
  - `BLACKBOARD_MAX_LOG_ENTRIES` (constant, lines 466-466)
  - `BLACKBOARD_MAX_TEXT` (constant, lines 467-467)
  - `SKILL_REFRESH_MIN_INTERVAL_SECONDS` (constant, lines 468-468)
  - `SKILL_PROMPT_MAX_ITEMS` (constant, lines 469-469)
  - `SKILL_PROMPT_MAX_CHARS` (constant, lines 470-470)
  - `SKILL_RUNTIME_CACHE_MAX_ENTRIES` (constant, lines 471-471)
  - `SKILL_RUNTIME_CACHE_MAX_BYTES` (constant, lines 472-472)
  - `AUTO_SKILLS_ROOT_CANDIDATES` (constant, lines 473-473)
  - `SKILL_DEFAULT_ATTACHMENT_GLOBS` (constant, lines 474-504)
  - `SKILL_INLINE_ATTACHMENT_MAX_FILES` (constant, lines 505-505)
  - `SKILL_INLINE_ATTACHMENT_MAX_CHARS` (constant, lines 506-506)
  - `SKILL_RESOURCE_MANIFEST_MAX_ITEMS` (constant, lines 507-507)
  - `SKILL_BODY_COMPACT_THRESHOLD_CHARS` (constant, lines 508-508)
  - `SKILL_BODY_PREVIEW_CHARS` (constant, lines 509-509)
  - `SKILLS_VIRTUAL_PREFIX` (constant, lines 510-510)
  - `SKILLS_EXTERNAL_MOUNT` (constant, lines 511-511)
  - `PLAN_MODE_ENABLED_LEVELS` (constant, lines 512-512)
  - `PLAN_MODE_FORCED_LEVELS` (constant, lines 513-513)
  - `PLAN_MODE_USER_CHOICES` (constant, lines 514-514)
  - `TASK_PHASES` (constant, lines 516-516)
  - `TASK_PHASE_ROUTING` (constant, lines 517-524)
  - `COMPLEXITY_KEYWORDS` (constant, lines 526-531)
  - `USER_COMPLEXITY_SIMPLE_TOKENS` (constant, lines 532-536)
  - `USER_COMPLEXITY_MODERATE_TOKENS` (constant, lines 537-541)
  - `USER_COMPLEXITY_COMPLEX_TOKENS` (constant, lines 542-546)
  - `USER_COMPLEXITY_EXPERT_TOKENS` (constant, lines 547-551)
  - `PLAN_MODE_EXPLORER_MAX_ROUNDS` (constant, lines 552-552)
  - `PLAN_MODE_SYNTHESIS_MAX_ATTEMPTS` (constant, lines 553-553)
  - `REVIEWER_DEBUG_MODE_MAX_ROUNDS` (constant, lines 555-555)
  - `REVIEWER_DEBUG_TOOL_ALLOWLIST` (constant, lines 556-560)
  - `EXPLORER_STALL_THRESHOLD` (constant, lines 561-561)
  - `DEVELOPER_EDIT_STALL_THRESHOLD` (constant, lines 562-562)
  - `PLAN_MODE_MANAGER_SYNTHESIS_MAX_TOKENS` (constant, lines 563-563)
  - `PLAN_MODE_MAX_OPTIONS` (constant, lines 564-564)
  - `PLAN_FILE_RELATIVE_PATH` (constant, lines 565-565)
  - `PLAN_BUBBLE_MAX_CHARS` (constant, lines 566-566)
  - `PLAN_NOTICE_BODY_MAX_CHARS` (constant, lines 567-567)
  - `PLAN_MESSAGE_EVENT_MAX_CHARS` (constant, lines 568-568)
  - `PLAN_STEP_FULL_CONTENT_MAX_CHARS` (constant, lines 569-569)
  - `PLAN_MODE_RESEARCH_TOOL_ALLOWLIST` (constant, lines 570-574)
  - `FAILURE_LEDGER_MAX_FIXES` (constant, lines 575-575)
  - `FAILURE_LEDGER_MAX_COMPILE_ERRORS` (constant, lines 576-576)
  - `FAILURE_LEDGER_MAX_DELEGATIONS` (constant, lines 577-577)
  - `FAILURE_LEDGER_MAX_STALLS` (constant, lines 578-578)
  - `FAILURE_LEDGER_MAX_TOOL_FPS` (constant, lines 579-579)
  - `FAILURE_LEDGER_MAX_ERRORS` (constant, lines 580-580)
  - `ERROR_CATEGORY_DEFS` (constant, lines 583-620)
  - `CHECKPOINT_MAX_COUNT` (constant, lines 621-621)
  - `CHECKPOINT_INTERVAL_ROUNDS` (constant, lines 622-622)
  - `PERSISTED_ROUTES_MAX` (constant, lines 623-623)
  - `HTML_FRONTEND_REQUEST_KEYWORDS` (constant, lines 624-663)
  - `DEEP_RESEARCH_REQUEST_KEYWORDS` (constant, lines 664-686)
  - `DEEP_RESEARCH_RETRIEVAL_KEYWORDS` (constant, lines 687-706)
  - `DEEP_RESEARCH_TEXT_ONLY_HINT_KEYWORDS` (constant, lines 707-724)
  - `DANGEROUS_PATTERNS` (constant, lines 726-726)
  - `VALID_MSG_TYPES` (constant, lines 727-733)
  - `SUPPORTED_UI_LANGUAGES` (constant, lines 735-740)
  - `UI_LANGUAGE_LABELS` (constant, lines 741-741)
  - `DEFAULT_UI_LANGUAGE` (constant, lines 742-742)
  - `UI_STYLE_CHOICES` (constant, lines 743-743)
  - `UI_STYLE_LABELS` (constant, lines 744-744)
  - `DEFAULT_UI_STYLE` (constant, lines 745-745)
  - `DEFAULT_WEB_UI_DIR` (constant, lines 746-746)
  - `DEFAULT_WEB_UI_CONFIG` (constant, lines 747-747)
  - `WEB_UI_REQUIRED_FILES` (constant, lines 748-755)
  - `WEB_UI_OPTIONAL_FILES` (constant, lines 756-756)
  - `IMAGE_EXTS` (constant, lines 758-771)
  - `IMAGE_FORMATS_NEED_CONVERSION` (constant, lines 772-772)
  - `IMAGE_SAFE_FORMATS` (constant, lines 773-773)
  - `AUDIO_EXTS` (constant, lines 774-784)
  - `VIDEO_EXTS` (constant, lines 785-795)
  - `CODE_PREVIEW_STAGE_MAX_BYTES` (constant, lines 796-796)
  - `CODE_PREVIEW_STAGE_MAX_ROWS` (constant, lines 797-797)
  - `CODE_PREVIEW_STAGE_MAX_PER_FILE` (constant, lines 798-798)
  - `CODE_PREVIEW_STAGE_MAX_TOTAL` (constant, lines 799-799)
  - `RENDER_FRAME_MAX_B64_CHARS` (constant, lines 800-800)
  - `RENDER_FRAME_MAX_POINTS` (constant, lines 801-801)
  - `RENDER_FRAME_MAX_LINES` (constant, lines 802-802)
  - `RENDER_FRAME_MAX_LINE_POINTS` (constant, lines 803-803)
  - `RENDER_FRAME_ACTIVITY_INTERVAL_SECONDS` (constant, lines 804-804)
  - `RAW_TOOLCALL_TEXT_FILTER_THRESHOLD` (constant, lines 805-805)
  - `ASSISTANT_TEXT_PERSIST_MAX_CHARS` (constant, lines 806-806)
  - `ASSISTANT_MESSAGE_EVENT_MAX_CHARS` (constant, lines 807-807)
  - `CODE_PREVIEW_EXTS` (constant, lines 808-897)
  - `CODE_PREVIEW_FILENAMES` (constant, lines 898-909)
  - `MEDIA_CAPABILITY_KEYS` (constant, lines 910-917)
  - `SAMPLE_IMAGE_PNG_B64` (constant, lines 918-921)
  - `SAMPLE_AUDIO_WAV_B64` (constant, lines 922-924)
  - `SAMPLE_VIDEO_MP4_B64` (constant, lines 925-927)
  - `OFFLINE_JS_LIB_CATALOG` (constant, lines 929-1187)
  - `OFFLINE_JS_LIB_INDEX_FILE` (constant, lines 1188-1188)
  - `OFFLINE_JS_LIB_README_FILE` (constant, lines 1189-1189)
  - `BACKEND_I18N` (constant, lines 1375-1444)
  - `call_backend_i18n_en_update_l1446` (expression, lines 1446-1539)
  - `call_backend_i18n_zh_cn_update_l1540` (expression, lines 1540-1633)
  - `call_backend_i18n_zh_tw_update_l1634` (expression, lines 1634-1727)
  - `call_backend_i18n_ja_update_l1728` (expression, lines 1728-1821)
  - `OPENAI_COMPAT_PROVIDER_NAMES` (constant, lines 3851-3859)
  - `OPENAI_LIKE_PROVIDER_NAMES` (constant, lines 3861-3861)
  - `TABULAR_PREVIEW_EXTS` (constant, lines 5305-5305)
  - `EXCEL_PREVIEW_EXTS` (constant, lines 5306-5306)
  - `PRESENTATION_PREVIEW_EXTS` (constant, lines 5307-5307)
  - `DOCUMENT_PREVIEW_EXTS` (constant, lines 5308-5308)
  - `EMBEDDED_SKILLS_ARCHIVE_B64` (constant, lines 5845-6364)
  - `EMBEDDED_SKILLS_ARCHIVE_SHA256` (constant, lines 6365-6365)
  - `EMBEDDED_SKILLS_ARCHIVE_FILES` (constant, lines 6366-6389)
  - `BUILTIN_CLAWHUB_SKILLS_VERSION` (constant, lines 9549-9549)
  - `EMBEDDED_CLAWHUB_SKILLS_ARCHIVE_B64` (constant, lines 9551-9795)
  - `SKILL_PROTOCOL_LOCAL` (constant, lines 9854-9854)
  - `SKILL_PROTOCOL_CLAWHUB` (constant, lines 9855-9855)
  - `SKILL_PROTOCOL_HTTP_JSON` (constant, lines 9856-9856)
  - `SKILL_PROTOCOL_SPECS` (constant, lines 9858-9889)
  - `AGENT_TOOL_ALLOWLIST` (constant, lines 13054-13097)
  - `INDEX_HTML` (constant, lines 39872-40059)
  - `APP_CSS` (constant, lines 40061-40449)
  - `APP_JS` (constant, lines 40451-43553)
  - `APP_TS` (constant, lines 43555-43582)
  - `SKILLS_INDEX_HTML` (constant, lines 43584-43738)
  - `SKILLS_EXTRA_CSS` (constant, lines 43740-43835)
  - `SKILLS_APP_JS` (constant, lines 43837-43978)
  - `RAG_TERM_GROUPS` (constant, lines 43980-43990)
  - `RAG_RESEARCH_HINTS` (constant, lines 43991-44012)
  - `RAG_CODE_HINTS` (constant, lines 44013-44023)
  - `RAG_SHORT_TOKEN_ALLOWLIST` (constant, lines 44024-44039)
  - `RAG_EN_STOPWORDS` (constant, lines 44040-44112)
  - `RAG_ZH_STOPWORDS` (constant, lines 44113-44149)
  - `RAG_GENERIC_ENTITY_TERMS_EN` (constant, lines 44150-44228)
  - `RAG_GENERIC_ENTITY_TERMS_ZH` (constant, lines 44229-44271)
  - `RAG_STRUCTURAL_ENTITY_PATTERNS` (constant, lines 44272-44290)
  - `CODE_LIBRARY_IGNORED_DIRS` (constant, lines 44613-44618)
  - `CODE_LIBRARY_LANGUAGE_BY_EXT` (constant, lines 44619-44675)
  - `CODE_LIBRARY_SPECIAL_FILENAMES` (constant, lines 44676-44682)
  - `RAG_ADMIN_INDEX_HTML` (constant, lines 49289-49446)
  - `RAG_ADMIN_CSS` (constant, lines 49448-49538)
  - `RAG_ADMIN_JS` (constant, lines 49540-50766)
  - `CODE_ADMIN_INDEX_HTML` (constant, lines 50768-50777)
  - `CODE_ADMIN_CSS` (constant, lines 50778-50808)
  - `CODE_ADMIN_JS` (constant, lines 50809-50813)

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
  - `detect_repo_root` (function, lines 2448-2462)
  - `REPO_ROOT` (constant, lines 2464-2464)

### `config/settings.py`

- Routed symbols: 33
- Cross-module imports: `config/constants.py`: `AUTO_SKILLS_ROOT_CANDIDATES`, `BACKEND_I18N`, `DEFAULT_REQUEST_TIMEOUT`, `DEFAULT_SHELL_COMMAND_TIMEOUT_SECONDS`, `DEFAULT_UI_LANGUAGE`, `DEFAULT_UI_STYLE`, `DEFAULT_WEB_UI_CONFIG`, `DEFAULT_WEB_UI_DIR`, `EXECUTION_MODE_CHOICES`, `EXECUTION_MODE_SEQUENTIAL`, `EXECUTION_MODE_SINGLE`, `EXECUTION_MODE_SYNC`, `MAX_SHELL_COMMAND_TIMEOUT_SECONDS`, `MEDIA_CAPABILITY_KEYS`, `MIN_SHELL_COMMAND_TIMEOUT_SECONDS`, `SUPPORTED_UI_LANGUAGES`, `TASK_COMPLEXITY_LEVELS`, `TASK_COMPLEXITY_RANKS`, `UI_LANGUAGE_LABELS`, `UI_STYLE_CHOICES`, `USER_COMPLEXITY_COMPLEX_TOKENS`, `USER_COMPLEXITY_EXPERT_TOKENS`, `USER_COMPLEXITY_MODERATE_TOKENS`, `USER_COMPLEXITY_SIMPLE_TOKENS`; `config/paths.py`: `WORKDIR`; `llm/utils.py`: `_is_http_url`, `_resolve_local_path`, `complete_chat_endpoint`, `extract_base_url`, `is_openai_like_provider`, `normalize_openai_compat_provider_name`, `strip_thinking_content`; `skills/store.py`: `ensure_embedded_skills`; `utils/http.py`: `urlopen`; `utils/json_utils.py`: `parse_json_object`; `utils/misc.py`: `MAX_TIMEOUT_SECONDS`, `MIN_TIMEOUT_SECONDS`, `normalize_timeout_seconds`, `sanitize_profile_id`; `utils/text.py`: `trim`
- Symbols:
  - `normalize_ui_language` (function, lines 1273-1295)
  - `normalize_ui_style` (function, lines 1298-1315)
  - `supported_ui_languages_payload` (function, lines 1318-1319)
  - `normalize_execution_mode` (function, lines 1322-1341)
  - `model_language_instruction` (function, lines 1344-1372)
  - `backend_i18n_text` (function, lines 1824-1834)
  - `backend_role_label` (function, lines 1837-1841)
  - `_detect_os_shell_instruction` (function, lines 1844-1883)
  - `resolve_web_ui_dir_path` (function, lines 1885-1892)
  - `resolve_optional_file_path` (function, lines 1895-1902)
  - `resolve_skills_root_path` (function, lines 1905-1912)
  - `_count_skill_markdown_files` (function, lines 1915-1926)
  - `select_preferred_skills_root` (function, lines 1929-1963)
  - `load_web_ui_config_file` (function, lines 1966-1980)
  - `extract_show_upload_list_setting` (function, lines 1983-1997)
  - `extract_ui_style_setting` (function, lines 2000-2014)
  - `extract_js_lib_download_setting` (function, lines 2017-2036)
  - `extract_daily_session_limit_setting` (function, lines 2039-2082)
  - `extract_shell_command_timeout_setting` (function, lines 2085-2131)
  - `default_multimodal_capabilities` (function, lines 2140-2148)
  - `_to_bool_like` (function, lines 2151-2161)
  - `infer_model_multimodal_capabilities` (function, lines 2164-2208)
  - `parse_capability_overrides` (function, lines 2211-2248)
  - `merge_multimodal_capabilities` (function, lines 2251-2258)
  - `parse_media_endpoints` (function, lines 2261-2275)
  - `infer_user_complexity_value` (function, lines 3769-3785)
  - `normalize_task_complexity` (function, lines 3787-3815)
  - `task_complexity_rank` (function, lines 3817-3818)
  - `task_complexity_at_least` (function, lines 3820-3821)
  - `max_task_complexity` (function, lines 3823-3832)
  - `load_llm_config_from_source` (function, lines 3976-4010)
  - `parse_llm_config_profiles` (function, lines 4012-4598)
  - `looks_like_llm_config` (function, lines 4600-4674)

### `llm/client.py`

- Routed symbols: 2
- Cross-module imports: `config/constants.py`: `DEFAULT_REQUEST_TIMEOUT`, `OLLAMA_THINKING_TOOL_BUFFER`, `SAMPLE_AUDIO_WAV_B64`, `SAMPLE_IMAGE_PNG_B64`, `SAMPLE_VIDEO_MP4_B64`; `config/settings.py`: `default_multimodal_capabilities`, `infer_model_multimodal_capabilities`, `merge_multimodal_capabilities`, `parse_capability_overrides`, `parse_media_endpoints`; `llm/utils.py`: `complete_chat_endpoint`, `is_openai_compat_provider`, `is_openai_like_provider`, `split_thinking_content`; `utils/http.py`: `urlopen`; `utils/json_utils.py`: `canonicalize_tool_name`, `json_dumps`, `parse_json_object`, `parse_tool_arguments`, `parse_tool_arguments_with_error`; `utils/misc.py`: `MAX_TIMEOUT_SECONDS`, `MIN_TIMEOUT_SECONDS`, `make_id`, `normalize_timeout_seconds`, `now_ts`; `utils/text.py`: `trim`
- Symbols:
  - `OllamaError` (class, lines 11759-11762)
  - `OllamaClient` (class, lines 11764-12816)

### `llm/utils.py`

- Routed symbols: 25
- Cross-module imports: `config/constants.py`: `OPENAI_COMPAT_PROVIDER_NAMES`, `OPENAI_LIKE_PROVIDER_NAMES`; `utils/http.py`: `urlopen`; `utils/json_utils.py`: `json_dumps`, `parse_json_object`; `utils/text.py`: `trim`
- Symbols:
  - `probe_ollama_environment` (function, lines 3455-3468)
  - `list_ollama_models` (function, lines 3470-3472)
  - `_OLLAMA_TAG_CACHE_LOCK` (assignment, lines 3474-3474)
  - `_OLLAMA_TAG_CACHE` (assignment, lines 3475-3475)
  - `list_ollama_models_cached` (function, lines 3485-3522)
  - `resolve_ollama_model` (function, lines 3524-3534)
  - `infer_thinking_model` (function, lines 3536-3538)
  - `split_thinking_content` (function, lines 3540-3581)
  - `strip_thinking_content` (function, lines 3583-3584)
  - `check_ollama_model_ready` (function, lines 3586-3610)
  - `list_loaded_ollama_models` (function, lines 3612-3625)
  - `wake_ollama_model` (function, lines 3627-3657)
  - `try_pull_ollama_model` (function, lines 3659-3677)
  - `ordered_model_candidates` (function, lines 3679-3697)
  - `pick_working_ollama_model` (function, lines 3699-3715)
  - `extract_base_url` (function, lines 3748-3756)
  - `complete_chat_endpoint` (function, lines 3758-3767)
  - `normalize_openai_compat_provider_name` (function, lines 3834-3849)
  - `is_openai_compat_provider` (function, lines 3863-3864)
  - `is_openai_like_provider` (function, lines 3866-3867)
  - `openai_compat_probe_headers` (function, lines 3869-3880)
  - `openai_compat_model_list_urls` (function, lines 3882-3914)
  - `extract_openai_compat_model_ids` (function, lines 3916-3949)
  - `_is_http_url` (function, lines 3951-3956)
  - `_resolve_local_path` (function, lines 3958-3974)

### `rag/index.py`

- Routed symbols: 5
- Cross-module imports: `config/constants.py`: `RAG_DYNAMIC_NOISE_HARD_COMMUNITY_RATIO`, `RAG_DYNAMIC_NOISE_HARD_DOC_RATIO`, `RAG_DYNAMIC_NOISE_MIN_COMMUNITY_FREQ`, `RAG_DYNAMIC_NOISE_MIN_DOC_FREQ`, `RAG_DYNAMIC_NOISE_SOFT_COMMUNITY_RATIO`, `RAG_DYNAMIC_NOISE_SOFT_DOC_RATIO`, `RAG_EN_STOPWORDS`, `RAG_GRAPH_MAX_NODES`, `RAG_INCLUDE_FILENAME_ENTITIES_DEFAULT`, `RAG_MAX_COMMUNITY_MAP_SUPPORT`, `RAG_MAX_GLOBAL_COMMUNITIES`, `RAG_MAX_QUERY_RESULTS`; `rag/parsers.py`: `_code_is_test_path`, `_rag_apply_filename_entity_policy`, `_rag_choose_community`, `_rag_classify_document`, `_rag_expand_tokens`, `_rag_extract_entities`, `_rag_filter_entities`, `_rag_tokenize`; `utils/json_utils.py`: `json_dumps`; `utils/misc.py`: `now_ts`; `utils/text.py`: `trim`
- Symbols:
  - `_code_module_name` (function, lines 44709-44723)
  - `_code_choose_community` (function, lines 44726-44733)
  - `_code_query_terms` (function, lines 44736-44748)
  - `TFGraphIDFIndex` (class, lines 45724-47082)
  - `CodeGraphIndex` (class, lines 48522-48934)

### `rag/ingestion.py`

- Routed symbols: 3
- Cross-module imports: `config/constants.py`: `CODE_IMPORT_WORKER_COUNT`, `CODE_LIBRARY_IGNORED_DIRS`, `CODE_PARSE_TIMEOUT_SECONDS`, `RAG_IMPORT_WORKER_COUNT`, `RAG_MAX_IMPORT_BATCH_ITEMS`, `RAG_MAX_IMPORT_FILES`, `RAG_MODEL_MEDIA_MAX_BYTES`, `RAG_PARSE_TIMEOUT_SECONDS`, `RAG_PDF_IMAGE_LIMIT`; `config/settings.py`: `default_multimodal_capabilities`; `rag/parsers.py`: `CodeContentParser`, `RAGContentParser`, `_rag_extract_entities`, `_rag_safe_name`; `rag/store.py`: `CodeLibraryStore`, `RAGLibraryStore`; `session/state.py`: `SessionState`; `utils/files.py`: `try_read_text`; `utils/json_utils.py`: `_read_json_file`, `_write_json_file`, `parse_json_object`; `utils/media.py`: `guess_mime_from_name`; `utils/misc.py`: `make_id`, `now_ts`; `utils/text.py`: `trim`
- Symbols:
  - `_rag_parse_file_worker` (function, lines 47635-47649)
  - `RAGIngestionService` (class, lines 47652-48519)
  - `CodeIngestionService` (class, lines 49203-49287)

### `rag/parsers.py`

- Routed symbols: 22
- Cross-module imports: `config/constants.py`: `AUDIO_EXTS`, `CODE_CHUNK_CHARS`, `CODE_CHUNK_OVERLAP`, `CODE_LIBRARY_LANGUAGE_BY_EXT`, `CODE_LIBRARY_SPECIAL_FILENAMES`, `CODE_MAX_CHUNKS_PER_DOC`, `CODE_PREVIEW_EXTS`, `CODE_PREVIEW_FILENAMES`, `CODE_PREVIEW_STAGE_MAX_ROWS`, `DOCUMENT_PREVIEW_EXTS`, `EXCEL_PREVIEW_EXTS`, `IMAGE_EXTS`, `PRESENTATION_PREVIEW_EXTS`, `RAG_CHUNK_CHARS`, `RAG_CHUNK_OVERLAP`, `RAG_CODE_HINTS`, `RAG_EN_STOPWORDS`, `RAG_GENERIC_ENTITY_TERMS_EN`, `RAG_GENERIC_ENTITY_TERMS_ZH`, `RAG_INCLUDE_FILENAME_ENTITIES_DEFAULT`, `RAG_MAX_CHUNKS_PER_DOC`, `RAG_PDF_IMAGE_LIMIT`, `RAG_RESEARCH_HINTS`, `RAG_SHORT_TOKEN_ALLOWLIST`, `RAG_STRUCTURAL_ENTITY_PATTERNS`, `RAG_TERM_GROUPS`, `RAG_ZH_STOPWORDS`, `TABULAR_PREVIEW_EXTS`, `VIDEO_EXTS`; `utils/files.py`: `_sha256_bytes`, `_sha256_file`; `utils/json_utils.py`: `parse_json_object`; `utils/media.py`: `guess_mime_from_name`; `utils/text.py`: `_compress_rows_keep_hotspot`, `_skip_row`, `trim`
- Symbols:
  - `normalize_rel_preview_path` (function, lines 5280-5291)
  - `is_code_preview_candidate` (function, lines 5294-5302)
  - `preview_kind_for_path` (function, lines 5311-5338)
  - `build_code_preview_rows` (function, lines 5341-5525)
  - `_rag_safe_name` (function, lines 44293-44296)
  - `_rag_detect_language` (function, lines 44299-44313)
  - `_rag_cjk_ngrams` (function, lines 44316-44328)
  - `_rag_is_noise_token` (function, lines 44331-44350)
  - `_rag_entity_allowed` (function, lines 44353-44365)
  - `_rag_filter_entities` (function, lines 44368-44382)
  - `_rag_filename_entity_aliases` (function, lines 44385-44418)
  - `_rag_apply_filename_entity_policy` (function, lines 44421-44451)
  - `_rag_choose_community` (function, lines 44454-44471)
  - `_rag_tokenize` (function, lines 44474-44504)
  - `_rag_expand_tokens` (function, lines 44507-44521)
  - `_rag_extract_entities` (function, lines 44524-44540)
  - `_rag_classify_document` (function, lines 44543-44577)
  - `_rag_chunk_text` (function, lines 44580-44610)
  - `_code_language_from_name` (function, lines 44685-44701)
  - `_code_is_test_path` (function, lines 44704-44706)
  - `CodeContentParser` (class, lines 44751-45211)
  - `RAGContentParser` (class, lines 45214-45721)

### `rag/store.py`

- Routed symbols: 2
- Cross-module imports: `config/constants.py`: `CODE_CHUNK_CHARS`, `CODE_CHUNK_OVERLAP`, `CODE_MAX_CHUNKS_PER_DOC`, `RAG_INCLUDE_FILENAME_ENTITIES_DEFAULT`, `RAG_TASK_HISTORY_LIMIT`; `rag/index.py`: `CodeGraphIndex`, `TFGraphIDFIndex`, `_code_choose_community`, `_code_module_name`; `rag/parsers.py`: `_code_is_test_path`, `_rag_apply_filename_entity_policy`, `_rag_choose_community`, `_rag_chunk_text`, `_rag_entity_allowed`, `_rag_extract_entities`, `_rag_safe_name`; `utils/files.py`: `_sha256_bytes`, `_sha256_file`; `utils/json_utils.py`: `_read_json_file`, `_write_json_file`; `utils/media.py`: `guess_mime_from_name`; `utils/misc.py`: `make_id`, `now_ts`; `utils/text.py`: `trim`
- Symbols:
  - `RAGLibraryStore` (class, lines 47085-47632)
  - `CodeLibraryStore` (class, lines 48937-49200)

### `server/handlers.py`

- Routed symbols: 5
- Cross-module imports: `app/context.py`: `AppContext`; `config/constants.py`: `APP_VERSION`, `DEFAULT_REQUEST_TIMEOUT`, `DEFAULT_SHELL_COMMAND_TIMEOUT_SECONDS`, `DEFAULT_UI_LANGUAGE`, `DEFAULT_UI_STYLE`, `EXECUTION_MODE_CHOICES`, `EXECUTION_MODE_SYNC`, `MIN_RUN_TIMEOUT_SECONDS`, `PLAN_MODE_USER_CHOICES`, `RAG_GRAPH_MAX_NODES`, `SSE_HEARTBEAT_SECONDS`, `TASK_COMPLEXITY_LEVELS`, `TASK_LEVEL_CHOICES`, `TASK_LEVEL_POLICIES`, `UI_STYLE_LABELS`; `config/paths.py`: `LLM_CONFIG_PATH`, `REPO_ROOT`, `WORKDIR`; `config/settings.py`: `_to_bool_like`, `infer_user_complexity_value`, `looks_like_llm_config`, `normalize_execution_mode`, `normalize_task_complexity`, `normalize_ui_language`, `normalize_ui_style`, `resolve_web_ui_dir_path`, `supported_ui_languages_payload`; `llm/utils.py`: `extract_base_url`, `extract_openai_compat_model_ids`, `list_ollama_models`, `normalize_openai_compat_provider_name`, `openai_compat_model_list_urls`, `openai_compat_probe_headers`; `session/manager.py`: `SessionCreationLimitExceeded`, `SessionManager`; `session/state.py`: `SessionState`; `skills/store.py`: `analyze_skill_building_knowledge`; `utils/files.py`: `safe_path`, `try_read_text`; `utils/http.py`: `urlopen`; `utils/json_utils.py`: `json_dumps`, `parse_json_object`; `utils/media.py`: `guess_mime_from_name`; `utils/misc.py`: `now_ts`, `swallow_benign_socket_error`, `user_id_from_ip`; `utils/text.py`: `trim`
- Symbols:
  - `AgentHTTPServer` (class, lines 53250-53278)
  - `Handler` (class, lines 53280-54139)
  - `SkillsHandler` (class, lines 54141-54337)
  - `RagAdminHandler` (class, lines 54339-54493)
  - `CodeAdminHandler` (class, lines 54496-54650)

### `session/manager.py`

- Routed symbols: 2
- Cross-module imports: `config/constants.py`: `AGENT_MAX_OUTPUT_TOKENS`, `ARBITER_DEFAULT_MAX_TOKENS`, `ARBITER_DEFAULT_TEMPERATURE`, `ARBITER_DEFAULT_TIMEOUT_SECONDS`, `DEFAULT_REQUEST_TIMEOUT`, `DEFAULT_SHELL_COMMAND_TIMEOUT_SECONDS`, `DEFAULT_UI_LANGUAGE`, `EXECUTION_MODE_SYNC`, `MAX_AGENT_ROUNDS`, `MAX_AGENT_ROUNDS_CAP`, `MAX_RUN_SECONDS`, `MAX_RUN_TIMEOUT_SECONDS`, `MAX_SHELL_COMMAND_TIMEOUT_SECONDS`, `MIN_AGENT_ROUNDS`, `MIN_CONTEXT_TOKEN_LIMIT`, `MIN_RUN_TIMEOUT_SECONDS`, `MIN_SHELL_COMMAND_TIMEOUT_SECONDS`, `TOKEN_THRESHOLD`; `config/paths.py`: `LLM_CONFIG_PATH`; `config/settings.py`: `infer_model_multimodal_capabilities`, `merge_multimodal_capabilities`, `normalize_execution_mode`, `normalize_ui_language`, `parse_capability_overrides`, `parse_llm_config_profiles`; `llm/client.py`: `OllamaClient`; `llm/utils.py`: `complete_chat_endpoint`, `extract_base_url`, `is_openai_compat_provider`, `list_ollama_models_cached`, `probe_ollama_environment`; `session/state.py`: `SessionState`; `utils/crypto.py`: `CryptoBox`; `utils/files.py`: `try_read_text`; `utils/json_utils.py`: `parse_json_object`; `utils/misc.py`: `make_id`, `normalize_timeout_seconds`, `now_ts`, `sanitize_profile_id`
- Symbols:
  - `SessionCreationLimitExceeded` (class, lines 2134-2137)
  - `SessionManager` (class, lines 38983-39870)

### `session/state.py`

- Routed symbols: 1
- Cross-module imports: `agent/background.py`: `BackgroundManager`; `agent/bus.py`: `MessageBus`; `agent/events.py`: `EventHub`; `agent/tasks.py`: `TaskManager`; `agent/todo.py`: `TodoManager`; `agent/worktree.py`: `WorktreeManager`; `config/constants.py`: `AGENT_BUBBLE_ROLES`, `AGENT_CTX_LIMIT_TIER0`, `AGENT_CTX_LIMIT_TIER1`, `AGENT_CTX_LIMIT_TIER2`, `AGENT_CTX_LIMIT_TIER3`, `AGENT_MAX_OUTPUT_TOKENS`, `AGENT_MSG_LIMIT_TIER0`, `AGENT_MSG_LIMIT_TIER1`, `AGENT_MSG_LIMIT_TIER2`, `AGENT_MSG_LIMIT_TIER3`, `AGENT_ROLES`, `AGENT_TOOL_ALLOWLIST`, `ARBITER_DEFAULT_MAX_TOKENS`, `ARBITER_DEFAULT_TEMPERATURE`, `ARBITER_DEFAULT_TIMEOUT_SECONDS`, `ARBITER_TRIGGER_MIN_CONTENT_CHARS`, `ARBITER_VALID_PLANNING_STREAK_LIMIT`, `ASSISTANT_MESSAGE_EVENT_MAX_CHARS`, `ASSISTANT_TEXT_PERSIST_MAX_CHARS`, `AUDIO_EXTS`, `AUTO_CONTINUE_BUDGET_DEFAULT`, `BASH_READ_LOOP_THRESHOLD`, `BLACKBOARD_MAX_LOG_ENTRIES`, `BLACKBOARD_MAX_TEXT`, `BLACKBOARD_STATUSES`, `CHECKPOINT_INTERVAL_ROUNDS`, `CHECKPOINT_MAX_COUNT`, `CODE_PREVIEW_STAGE_MAX_BYTES`, `CODE_PREVIEW_STAGE_MAX_PER_FILE`, `CODE_PREVIEW_STAGE_MAX_ROWS`, `CODE_PREVIEW_STAGE_MAX_TOTAL`, `COMPACT_TIER1_ABS`, `COMPACT_TIER1_PCT`, `COMPACT_TIER2_ABS`, `COMPACT_TIER2_PCT`, `COMPACT_TIER3_PCT`, `DANGEROUS_PATTERNS`, `DEEP_RESEARCH_REQUEST_KEYWORDS`, `DEEP_RESEARCH_RETRIEVAL_KEYWORDS`, `DEEP_RESEARCH_TEXT_ONLY_HINT_KEYWORDS`, `DEFAULT_REQUEST_TIMEOUT`, `DEFAULT_SHELL_COMMAND_TIMEOUT_SECONDS`, `DEFAULT_UI_LANGUAGE`, `DEVELOPER_EDIT_STALL_THRESHOLD`, `EMPTY_ACTION_MIN_CONTENT_CHARS`, `EMPTY_ACTION_WAKEUP_RETRY_LIMIT`, `ERROR_CATEGORY_DEFS`, `EXECUTION_MODE_CHOICES`, `EXECUTION_MODE_SEQUENTIAL`, `EXECUTION_MODE_SINGLE`, `EXECUTION_MODE_SYNC`, `EXPLORER_STALL_THRESHOLD`, `FAILURE_LEDGER_MAX_COMPILE_ERRORS`, `FAILURE_LEDGER_MAX_DELEGATIONS`, `FAILURE_LEDGER_MAX_ERRORS`, `FAILURE_LEDGER_MAX_FIXES`, `FAILURE_LEDGER_MAX_STALLS`, `FAILURE_LEDGER_MAX_TOOL_FPS`, `FILE_BUFFER_CONTENT_THRESHOLD`, `FILE_BUFFER_MAX_FILES`, `FINAL_SUMMARY_MIN_CHARS`, `FINAL_SUMMARY_STRICT_MIN_CHARS`, `FUSED_FAULT_BREAK_THRESHOLD`, `HARD_BREAK_RECOVERY_ROUND_THRESHOLD`, `HARD_BREAK_TOOL_ERROR_THRESHOLD`, `HTML_FRONTEND_REQUEST_KEYWORDS`, `IMAGE_EXTS`, `IMAGE_FORMATS_NEED_CONVERSION`, `LIVE_INPUT_DELAY_NORMAL_ROUNDS`, `LIVE_INPUT_DELAY_TOOL_ROUNDS`, `LIVE_INPUT_DELAY_WRITE_ROUNDS`, `LIVE_INPUT_MAX_INJECTIONS`, `LIVE_INPUT_REINJECT_INTERVAL`, `LIVE_INPUT_WEIGHT_BASE_DELAYED`, `LIVE_INPUT_WEIGHT_BASE_NORMAL`, `LIVE_INPUT_WEIGHT_STEP_DELAYED`, `LIVE_INPUT_WEIGHT_STEP_NORMAL`, `LONG_OUTPUT_LISTING_OFFLOAD_CHARS`, `LONG_OUTPUT_MODEL_PAGE_CHARS`, `LONG_OUTPUT_READ_PAGE_LINES`, `LONG_OUTPUT_READ_PAGE_MAX_CHARS`, `LONG_OUTPUT_TEMP_MAX_FILES`, `LONG_OUTPUT_UI_PAGE_CHARS`, `LONG_OUTPUT_UI_PREVIEW_MAX_PAGES`, `MANAGER_CTX_LIMIT_TIER0`, `MANAGER_CTX_LIMIT_TIER1`, `MANAGER_CTX_LIMIT_TIER2`, `MANAGER_CTX_LIMIT_TIER3`, `MANAGER_ROUTE_TARGETS`, `MAX_AGENT_ROUNDS`, `MAX_AGENT_ROUNDS_CAP`, `MAX_CONTEXT_ARCHIVE_SEGMENTS`, `MAX_RUN_SECONDS`, `MAX_RUN_TIMEOUT_SECONDS`, `MAX_SHELL_COMMAND_TIMEOUT_SECONDS`, `MIN_AGENT_ROUNDS`, `MIN_CONTEXT_TOKEN_LIMIT`, `MIN_RUN_TIMEOUT_SECONDS`, `MIN_SHELL_COMMAND_TIMEOUT_SECONDS`, `MODEL_CALL_PROGRESS_DELAY`, `MODEL_CALL_PROGRESS_INTERVAL`, `MODEL_OUTPUT_RETRY_TIMES`, `PERSISTED_ROUTES_MAX`, `PLAN_BUBBLE_MAX_CHARS`, `PLAN_FILE_RELATIVE_PATH`, `PLAN_MESSAGE_EVENT_MAX_CHARS`, `PLAN_MODE_ENABLED_LEVELS`, `PLAN_MODE_EXPLORER_MAX_ROUNDS`, `PLAN_MODE_FORCED_LEVELS`, `PLAN_MODE_MANAGER_SYNTHESIS_MAX_TOKENS`, `PLAN_MODE_MAX_OPTIONS`, `PLAN_MODE_RESEARCH_TOOL_ALLOWLIST`, `PLAN_MODE_SYNTHESIS_MAX_ATTEMPTS`, `PLAN_MODE_USER_CHOICES`, `PLAN_NOTICE_BODY_MAX_CHARS`, `PLAN_STEP_FULL_CONTENT_MAX_CHARS`, `RENDER_FRAME_ACTIVITY_INTERVAL_SECONDS`, `RENDER_FRAME_MAX_B64_CHARS`, `RENDER_FRAME_MAX_LINES`, `RENDER_FRAME_MAX_LINE_POINTS`, `RENDER_FRAME_MAX_POINTS`, `REPEATED_TOOL_LOOP_THRESHOLD`, `RETRY_RUNTIME_HINT_PREFIXES`, `REVIEWER_DEBUG_MODE_MAX_ROUNDS`, `RUNTIME_CONTROL_HINT_PREFIXES`, `SEMANTIC_CONFIDENCE_CHOICES`, `SKILLS_VIRTUAL_PREFIX`, `SKILL_REFRESH_MIN_INTERVAL_SECONDS`, `SKILL_RUNTIME_CACHE_MAX_BYTES`, `SKILL_RUNTIME_CACHE_MAX_ENTRIES`, `STALL_ESCALATION_CONTEXT_MAX_CHARS`, `STALL_ESCALATION_MIN_LEVEL`, `STALL_PLAN_SYNTHESIS_MAX_TOKENS`, `STALL_SEVERITY_DECAY_ON_SUCCESS`, `STALL_SEVERITY_ESCALATION_THRESHOLD`, `STALL_SEVERITY_WEIGHT_BASH_READ_LOOP`, `STALL_SEVERITY_WEIGHT_FAULT`, `STALL_SEVERITY_WEIGHT_RECOVERY_RETRY`, `STALL_SEVERITY_WEIGHT_REPEATED_TOOL`, `STALL_SEVERITY_WEIGHT_WATCHDOG`, `TASK_COMPLEXITY_LEVELS`, `TASK_LEVEL_CHOICES`, `TASK_LEVEL_POLICIES`, `TASK_PHASE_ROUTING`, `TASK_PROFILE_TYPES`, `TASK_SCALE_PREFERENCES`, `THINKING_BUDGET_FORCE_RATIO`, `TOKEN_THRESHOLD`, `TRUNCATION_CONTINUATION_ECHO_CHARS`, `TRUNCATION_CONTINUATION_MAX_PASSES`, `TRUNCATION_CONTINUATION_MAX_TOKENS`, `TRUNCATION_CONTINUATION_TAIL_CHARS`, `TRUNCATION_LIVE_BUFFER_MAX_CHARS`, `TRUNCATION_OVERLAP_SCAN_CHARS`, `TRUNCATION_PAIR_SCAN_CHARS`, `VIDEO_EXTS`, `WATCHDOG_CONTEXT_NEAR_RATIO`, `WATCHDOG_CONTEXT_STALL_THRESHOLD`, `WATCHDOG_INTENT_NO_TOOL_THRESHOLD`, `WATCHDOG_INTENT_NO_TOOL_THRESHOLD_SINGLE`, `WATCHDOG_MAX_DECOMPOSE_STEPS`, `WATCHDOG_REPEAT_NO_TOOL_THRESHOLD`, `WATCHDOG_REPEAT_NO_TOOL_THRESHOLD_SINGLE`, `WATCHDOG_REPEAT_SIMILARITY_THRESHOLD`, `WATCHDOG_STATE_STALL_THRESHOLD`, `WATCHDOG_STEP_MAX_ATTEMPTS`, `_DEFAULT_TOOL_TIMEOUT`, `_TOOL_TIMEOUT_MAP`; `config/paths.py`: `WORKDIR`; `config/settings.py`: `_detect_os_shell_instruction`, `_to_bool_like`, `backend_i18n_text`, `backend_role_label`, `default_multimodal_capabilities`, `infer_model_multimodal_capabilities`, `infer_user_complexity_value`, `looks_like_llm_config`, `max_task_complexity`, `merge_multimodal_capabilities`, `model_language_instruction`, `normalize_execution_mode`, `normalize_task_complexity`, `normalize_ui_language`, `parse_capability_overrides`, `parse_llm_config_profiles`, `task_complexity_at_least`, `task_complexity_rank`; `llm/client.py`: `OllamaClient`, `OllamaError`; `llm/utils.py`: `complete_chat_endpoint`, `extract_base_url`, `is_openai_compat_provider`, `list_loaded_ollama_models`, `list_ollama_models`, `list_ollama_models_cached`, `probe_ollama_environment`, `resolve_ollama_model`, `split_thinking_content`, `strip_thinking_content`, `wake_ollama_model`; `rag/parsers.py`: `build_code_preview_rows`, `is_code_preview_candidate`, `normalize_rel_preview_path`, `preview_kind_for_path`; `skills/store.py`: `SkillStore`, `ensure_runtime_skills`; `utils/compress.py`: `compress_text_blob`, `decompress_text_blob`; `utils/crypto.py`: `CryptoBox`; `utils/errors.py`: `CircuitBreakerTriggered`, `EmptyActionError`; `utils/files.py`: `_normalize_external_js_url`, `_safe_js_filename`, `cache_external_js_url`, `ensure_offline_js_libs`, `is_external_js_src`, `load_offline_js_lib_index`, `match_offline_js_catalog_by_url`, `offline_js_lib_root`, `safe_path`, `try_read_text`; `utils/http.py`: `urlopen`; `utils/json_utils.py`: `TOOLS`, `TOOL_REQUIRED_ARGS`, `canonicalize_tool_name`, `extract_json_object_from_text`, `json_dumps`, `parse_json_object`, `parse_tool_arguments_with_error`, `repair_truncated_json_object`, `tool_def`; `utils/media.py`: `_convert_image_to_safe_format`, `guess_ext_from_mime`, `guess_mime_from_name`; `utils/misc.py`: `MAX_TIMEOUT_SECONDS`, `MIN_TIMEOUT_SECONDS`, `is_benign_socket_error`, `make_id`, `normalize_timeout_seconds`, `now_ts`, `sanitize_profile_id`; `utils/text.py`: `MAX_TOOL_OUTPUT`, `_fmt_export_ts`, `_html_esc`, `_text_to_minimal_pdf`, `extract_todo_rows_from_text`, `filter_runtime_noise_lines`, `make_numbered_diff`, `make_unified_diff`, `normalize_embedded_newlines`, `normalize_work_text`, `parse_front_matter`, `render_numbered_diff_text`, `split_structured_todo_content`, `split_todo_status_text`, `trim`
- Symbols:
  - `SessionState` (class, lines 13099-38981)

### `skills/store.py`

- Routed symbols: 26
- Cross-module imports: `config/constants.py`: `BUILTIN_CLAWHUB_SKILLS_VERSION`, `EMBEDDED_CLAWHUB_SKILLS_ARCHIVE_B64`, `EMBEDDED_SKILLS_ARCHIVE_B64`, `EMBEDDED_SKILLS_ARCHIVE_FILES`, `EMBEDDED_SKILLS_ARCHIVE_SHA256`, `SKILLS_EXTERNAL_MOUNT`, `SKILLS_VIRTUAL_PREFIX`, `SKILL_BODY_COMPACT_THRESHOLD_CHARS`, `SKILL_BODY_PREVIEW_CHARS`, `SKILL_DEFAULT_ATTACHMENT_GLOBS`, `SKILL_INLINE_ATTACHMENT_MAX_CHARS`, `SKILL_INLINE_ATTACHMENT_MAX_FILES`, `SKILL_PROMPT_MAX_CHARS`, `SKILL_PROMPT_MAX_ITEMS`, `SKILL_PROTOCOL_CLAWHUB`, `SKILL_PROTOCOL_HTTP_JSON`, `SKILL_PROTOCOL_LOCAL`, `SKILL_PROTOCOL_SPECS`, `SKILL_REFRESH_MIN_INTERVAL_SECONDS`, `SKILL_RESOURCE_MANIFEST_MAX_ITEMS`; `config/paths.py`: `WORKDIR`; `llm/utils.py`: `_is_http_url`; `utils/files.py`: `_render_offline_js_catalog_md`, `safe_path`, `try_read_text`; `utils/http.py`: `urlopen`; `utils/json_utils.py`: `json_dumps`, `parse_json_object`; `utils/misc.py`: `_meta_string_list`, `_module_exists`, `now_ts`; `utils/text.py`: `parse_front_matter`, `trim`
- Symbols:
  - `ensure_embedded_skills_at_root` (function, lines 6392-6444)
  - `ensure_embedded_skills` (function, lines 6447-6448)
  - `detect_upload_parser_capabilities` (function, lines 6456-6471)
  - `_render_cap_markdown` (function, lines 6473-6487)
  - `_write_text_if_changed` (function, lines 6489-6494)
  - `ensure_generated_document_skills` (function, lines 6496-6584)
  - `ensure_generated_image_coding_feedback_skill` (function, lines 6586-6685)
  - `_skill_knowledge_files` (function, lines 6687-6706)
  - `analyze_skill_building_knowledge` (function, lines 6708-6762)
  - `_sanitize_skill_slug` (function, lines 6764-6766)
  - `_build_skills_gen_skill_content` (function, lines 6768-6799)
  - `ensure_generated_skills_gen_skill` (function, lines 6801-6805)
  - `ensure_generated_execution_recovery_skill` (function, lines 6807-6885)
  - `ensure_generated_systematic_debugging_skill` (function, lines 6887-7159)
  - `ensure_generated_code_engineering_mastery_skill` (function, lines 7161-7279)
  - `ensure_generated_smart_file_navigation_skill` (function, lines 7281-7399)
  - `ensure_generated_html_frontend_report_skills` (function, lines 7401-7608)
  - `ensure_generated_deep_research_skills` (function, lines 7610-7878)
  - `ensure_generated_research_scientific_skills` (function, lines 7880-8516)
  - `ensure_generated_rag_mastery_skills` (function, lines 8522-8818)
  - `ensure_generated_multimodal_comprehension_skills` (function, lines 8824-9513)
  - `ensure_generated_runtime_skills_manifest` (function, lines 9516-9547)
  - `ensure_embedded_clawhub_skills` (function, lines 9798-9835)
  - `ensure_runtime_skills` (function, lines 9837-9852)
  - `_BUILTIN_SKILLS` (assignment, lines 9894-9982)
  - `SkillStore` (class, lines 9984-11278)

### `utils/compress.py`

- Routed symbols: 2
- Cross-module imports: none
- Symbols:
  - `compress_text_blob` (function, lines 3089-3094)
  - `decompress_text_blob` (function, lines 3096-3104)

### `utils/crypto.py`

- Routed symbols: 1
- Cross-module imports: `utils/json_utils.py`: `json_dumps`
- Symbols:
  - `CryptoBox` (class, lines 4684-4801)

### `utils/errors.py`

- Routed symbols: 2
- Cross-module imports: none
- Symbols:
  - `EmptyActionError` (class, lines 3478-3479)
  - `CircuitBreakerTriggered` (class, lines 3482-3483)

### `utils/files.py`

- Routed symbols: 25
- Cross-module imports: `config/constants.py`: `OFFLINE_JS_LIB_CATALOG`, `OFFLINE_JS_LIB_INDEX_FILE`, `OFFLINE_JS_LIB_README_FILE`; `config/paths.py`: `WORKDIR`; `utils/http.py`: `urlopen`; `utils/json_utils.py`: `json_dumps`; `utils/misc.py`: `now_ts`; `utils/text.py`: `trim`
- Symbols:
  - `_normalize_js_lib_asset_ref` (function, lines 1192-1205)
  - `_resolve_js_lib_asset_path` (function, lines 1208-1237)
  - `_discover_extra_js_lib_files` (function, lines 1240-1270)
  - `safe_path` (function, lines 2466-2475)
  - `_safe_js_filename` (function, lines 2477-2484)
  - `_sha256_bytes` (function, lines 2486-2487)
  - `_sha256_file` (function, lines 2489-2497)
  - `_download_http_bytes` (function, lines 2499-2507)
  - `offline_js_lib_root` (function, lines 2509-2510)
  - `_offline_js_entry_relative_path` (function, lines 2512-2516)
  - `_archive_member_relative_path` (function, lines 2518-2527)
  - `_path_size_bytes` (function, lines 2529-2544)
  - `_extract_archive_to_dir` (function, lines 2546-2586)
  - `_package_required_paths` (function, lines 2588-2594)
  - `_package_install_ready` (function, lines 2596-2604)
  - `_postprocess_offline_js_package` (function, lines 2606-2641)
  - `_ensure_offline_js_package` (function, lines 2643-2682)
  - `_render_offline_js_catalog_md` (function, lines 2684-2700)
  - `load_offline_js_lib_index` (function, lines 2702-2711)
  - `ensure_offline_js_libs` (function, lines 2713-2857)
  - `_normalize_external_js_url` (function, lines 2859-2863)
  - `is_external_js_src` (function, lines 2865-2867)
  - `match_offline_js_catalog_by_url` (function, lines 2869-2885)
  - `cache_external_js_url` (function, lines 2887-2919)
  - `try_read_text` (function, lines 5006-5014)

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
  - `json_dumps` (function, lines 2438-2439)
  - `parse_tool_arguments` (function, lines 3357-3366)
  - `repair_truncated_json_object` (function, lines 3368-3421)
  - `parse_tool_arguments_with_error` (function, lines 3423-3453)
  - `parse_json_object` (function, lines 3717-3722)
  - `extract_json_object_from_text` (function, lines 3724-3746)
  - `_json_default_copy` (function, lines 5016-5021)
  - `_read_json_file` (function, lines 5023-5043)
  - `_write_json_file` (function, lines 5045-5072)
  - `tool_def` (function, lines 12818-12830)
  - `TOOLS` (constant, lines 12832-13008)
  - `TOOL_REQUIRED_ARGS` (constant, lines 13010-13010)
  - `TOOL_SPEC_BY_NAME` (constant, lines 13011-13011)
  - `TOOL_NAME_FUZZY_MAP` (constant, lines 13023-13023)
  - `canonicalize_tool_name` (function, lines 13041-13052)

### `utils/media.py`

- Routed symbols: 3
- Cross-module imports: none
- Symbols:
  - `guess_mime_from_name` (function, lines 2278-2280)
  - `_convert_image_to_safe_format` (function, lines 2283-2300)
  - `guess_ext_from_mime` (function, lines 2303-2309)

### `utils/misc.py`

- Routed symbols: 19
- Cross-module imports: none
- Symbols:
  - `MIN_TIMEOUT_SECONDS` (constant, lines 209-209)
  - `MAX_TIMEOUT_SECONDS` (constant, lines 210-210)
  - `DEFAULT_TIMEOUT_SECONDS` (constant, lines 211-217)
  - `BENIGN_SOCKET_DEBUG_LOG_ENABLED` (constant, lines 324-330)
  - `BENIGN_SOCKET_LOG_INTERVAL_SECONDS` (constant, lines 331-331)
  - `now_ts` (function, lines 2311-2312)
  - `_benign_socket_log_lock` (assignment, lines 2315-2315)
  - `_benign_socket_log_state` (assignment, lines 2316-2316)
  - `is_benign_socket_error` (function, lines 2334-2352)
  - `_socket_error_code` (function, lines 2355-2364)
  - `_log_benign_socket_error_limited` (function, lines 2367-2401)
  - `swallow_benign_socket_error` (function, lines 2404-2408)
  - `normalize_timeout_seconds` (function, lines 2411-2424)
  - `detect_local_lan_ip` (function, lines 2426-2436)
  - `make_id` (function, lines 2441-2442)
  - `sanitize_profile_id` (function, lines 2444-2446)
  - `user_id_from_ip` (function, lines 4676-4682)
  - `_meta_string_list` (function, lines 4993-5004)
  - `_module_exists` (function, lines 6450-6454)

### `utils/text.py`

- Routed symbols: 22
- Cross-module imports: none
- Symbols:
  - `MAX_TOOL_OUTPUT` (constant, lines 129-129)
  - `SOCKET_NOISE_LINE_PATTERNS` (constant, lines 318-323)
  - `filter_runtime_noise_lines` (function, lines 2319-2331)
  - `trim` (function, lines 2921-2923)
  - `_fmt_export_ts` (function, lines 2926-2934)
  - `_html_esc` (function, lines 2937-2938)
  - `_text_to_minimal_pdf` (function, lines 2941-3087)
  - `normalize_embedded_newlines` (function, lines 3106-3114)
  - `_map_todo_status_token` (function, lines 3117-3132)
  - `split_todo_status_text` (function, lines 3135-3190)
  - `extract_todo_rows_from_text` (function, lines 3193-3260)
  - `infer_todo_status_from_text` (function, lines 3263-3269)
  - `split_structured_todo_content` (function, lines 3272-3325)
  - `normalize_work_text` (function, lines 3328-3355)
  - `parse_front_matter` (function, lines 4803-4990)
  - `make_unified_diff` (function, lines 5074-5091)
  - `_skip_row` (function, lines 5093-5097)
  - `_row_is_hot` (function, lines 5100-5101)
  - `_hotspot_index` (function, lines 5104-5125)
  - `_compress_rows_keep_hotspot` (function, lines 5128-5175)
  - `make_numbered_diff` (function, lines 5178-5263)
  - `render_numbered_diff_text` (function, lines 5265-5277)
