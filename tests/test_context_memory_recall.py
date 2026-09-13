import pathlib
import tempfile
import types
import unittest
from unittest import mock

import Clouds_Coder as cc


def bind(instance, name, function):
    setattr(instance, name, types.MethodType(function, instance))


class ContextMemoryRecallTests(unittest.TestCase):
    def bare_session(self):
        root = pathlib.Path(tempfile.mkdtemp(prefix="clouds-context-test-"))
        session = cc.SessionState.__new__(cc.SessionState)
        session.root = root
        session.files_root = root / "files"
        session.files_root.mkdir()
        session.file_buffer_dir = root / "file_buffer"
        session.file_buffer_dir.mkdir()
        session.context_archive_dir = root / "context_archive"
        session.context_archive_dir.mkdir()
        session.file_buffer_index = {}
        session.context_archives = []
        session.messages = []
        session.read_context_registry = {}
        session.tool_memory_registry = {}
        session.long_content_memory = {}
        session.long_content_memory_version = cc.LONG_CONTENT_MEMORY_VERSION
        session.read_context_policy = "balanced"
        session.tool_memory_policy = "balanced"
        session._context_estimate_depth = 0
        session.context_last_next_call_estimate = 0
        session.context_token_upper_bound = 200_000
        session.max_context_token_limit = 200_000
        session.context_estimate_calibration = 1.18
        session.context_compaction_metrics = {
            "runs": 0,
            "effective_runs": 0,
            "archived_messages": 0,
            "input_chars": 0,
            "summary_chars": 0,
            "last_ratio": 0.0,
            "cache_searches": 0,
            "cache_hits": 0,
        }
        session.ollama = mock.Mock()
        bind(session, "_session_path", lambda self, rel: self.files_root / rel)
        bind(session, "_session_rel", lambda self, fp: str(pathlib.Path(fp).relative_to(self.files_root)))
        bind(session, "_sanitize_agent_role", lambda self, role: str(role or "").strip().lower())
        bind(session, "_context_budget_tier_for_dynamic_memory", lambda self: 0)
        bind(session, "_context_budget_metrics", lambda self, token_estimate=None: {"left": 1, "left_percent": 100})
        bind(session, "_tool_memory_budget", cc.SessionState._tool_memory_budget)
        bind(session, "_read_context_budget", cc.SessionState._read_context_budget)
        bind(session, "_schedule_persist", lambda self: None)
        return session

    def test_long_content_structure_and_segment_reads_preserve_coverage(self):
        session = self.bare_session()
        lines = []
        for section in range(4):
            lines.append(f"## Section {section}")
            lines.extend(f"section {section} fact line {idx}" for idx in range(90))
        source = session.files_root / "long.md"
        source.write_text("\n".join(lines), encoding="utf-8")

        structure = session._run_read("long.md", mode="structure")
        self.assertIn("read_file structure", structure)
        memory = next(iter(session.long_content_memory.values()))
        self.assertEqual(memory["coverage"], 0.0)
        self.assertGreaterEqual(len(memory["segments"]), 4)

        segment = session._run_read("long.md", mode="segment", segment_id="s0002")
        self.assertIn("segment_id=s0002", segment)
        self.assertIn("Evidence window", segment)
        memory = next(iter(session.long_content_memory.values()))
        self.assertGreater(memory["coverage"], 0.0)
        self.assertLess(memory["coverage"], 1.0)

    def test_long_code_memory_uses_symbols_and_is_invalidated_on_change(self):
        session = self.bare_session()
        rows = ["import os", ""]
        for idx in range(12):
            rows.extend([f"def function_{idx}(value):", f"    return value + {idx}", ""])
        rows.extend("# filler" for _ in range(200))
        source = session.files_root / "large.py"
        source.write_text("\n".join(rows), encoding="utf-8")

        structure = session._run_read("large.py", mode="structure")
        self.assertIn("function_0", structure)
        memory = next(iter(session.long_content_memory.values()))
        self.assertEqual(memory["content_type"], "code")
        self.assertTrue(any("function_7" in row.get("symbols", []) for row in memory["segments"]))

        self.assertEqual(session._invalidate_long_content_memory_path("large.py"), 1)
        self.assertEqual(session._long_content_memory_prompt_block(), "")

    def test_long_code_symbol_locator_keeps_declarations_beyond_chunk_budget(self):
        session = self.bare_session()
        rows = []
        for idx in range(340):
            rows.extend([f"def function_{idx}(value):", f"    return value + {idx}", ""])
        source = session.files_root / "huge.py"
        source.write_text("\n".join(rows), encoding="utf-8")

        # The parser's prompt chunks/structure display remain bounded, but
        # symbol lookup must still reach declarations after the historical
        # 160/200/240 limits.
        session._run_read("huge.py", mode="structure")
        data = session._read_file_code_data(source, rows)
        self.assertTrue(any(row.get("name") == "function_339" for row in data.get("symbols", [])))
        located = session._run_read("huge.py", mode="symbol", target="function_339")
        self.assertIn("target='function_339'", located)
        self.assertIn("function_339", located)

    def test_code_parser_keeps_large_source_symbols_beyond_legacy_300k_cap(self):
        root = pathlib.Path(tempfile.mkdtemp(prefix="clouds-code-parser-test-"))
        source = root / "large.py"
        rows = []
        for idx in range(7000):
            rows.extend([f"def tail_function_{idx}(value):", f"    return value + {idx}", ""])
        source.write_text("\n".join(rows), encoding="utf-8")
        self.assertGreater(source.stat().st_size, 300_000)
        parsed = cc.CodeContentParser().parse_file(source)
        self.assertGreaterEqual(parsed.get("text_chars", 0), source.stat().st_size * 0.9)
        self.assertTrue(any(row.get("name") == "tail_function_6999" for row in parsed.get("symbols", [])))

    def test_overlapping_windows_return_only_uncovered_delta_and_fresh_bypasses_it(self):
        session = self.bare_session()
        source = session.files_root / "windows.txt"
        source.write_text("\n".join(f"line {idx}" for idx in range(500)), encoding="utf-8")

        first = session._run_read("windows.txt", mode="window", offset=0, limit=180)
        session._mark_long_content_read("windows.txt", source, source.read_text().splitlines(), {"mode": "window", "offset": 0, "limit": 180}, first)
        second = session._run_read("windows.txt", mode="window", offset=100, limit=180)
        self.assertIn("read_file delta", second)
        self.assertIn("uncovered_lines=181-280", second)
        self.assertNotIn("line 100", second)
        fresh = session._run_read("windows.txt", mode="window", offset=100, limit=180, fresh=True)
        self.assertIn("read_file window", fresh)
        self.assertIn("line 100", fresh)

    def test_reuse_marker_does_not_replace_exact_read_context(self):
        session = self.bare_session()
        source = session.files_root / "reuse.txt"
        source.write_text("\n".join(f"line {idx}" for idx in range(500)), encoding="utf-8")
        args = {"mode": "window", "offset": 0, "limit": 180}
        first = session._run_read("reuse.txt", **args)
        session._record_read_context("reuse.txt", args, first, role="developer", source_text=source.read_text())
        session._mark_long_content_read("reuse.txt", source, source.read_text().splitlines(), args, first)
        original_sha = next(iter(session.read_context_registry.values()))["sha256"]
        reused = session._run_read("reuse.txt", **args)
        self.assertIn("read_file reused", reused)
        entry = next(iter(session.read_context_registry.values()))
        self.assertEqual(entry["sha256"], original_sha)

    def test_auto_window_records_concrete_range_for_reuse(self):
        session = self.bare_session()
        source = session.files_root / "auto.txt"
        source.write_text("\n".join(f"line {idx}" for idx in range(500)), encoding="utf-8")
        args = {"mode": "auto", "offset": 0, "limit": 100}
        first = session._run_read("auto.txt", **args)
        session._mark_long_content_read("auto.txt", source, source.read_text().splitlines(), args, first)
        memory = next(iter(session.long_content_memory.values()))
        self.assertEqual(memory["read_ranges"], [[1, 100]])
        repeated = session._run_read("auto.txt", **args)
        self.assertIn("read_file reused", repeated)

    def test_long_content_read_cache_distinguishes_segments(self):
        session = self.bare_session()
        first = session._read_file_signature_from_args(
            {"path": "book.md", "mode": "segment", "segment_id": "s0001"}
        )
        second = session._read_file_signature_from_args(
            {"path": "book.md", "mode": "segment", "segment_id": "s0002"}
        )
        self.assertNotEqual(first, second)
        normalized = session._normalize_read_context_registry(
            {
                "k": {
                    "signature": second,
                    "path": "book.md",
                    "args": {"mode": "segment", "segment_id": "s0002"},
                }
            }
        )
        self.assertEqual(next(iter(normalized.values()))["args"]["segment_id"], "s0002")

    def test_long_content_prompt_only_injects_read_cards(self):
        session = self.bare_session()
        rows = ["# Overview"] + [f"overview filler {idx}" for idx in range(190)]
        rows += ["# Hidden Result", "KEY RESULT: efficiency improved by 42 percent."]
        rows += [f"tail filler {idx}" for idx in range(190)]
        source = session.files_root / "study.md"
        source.write_text("\n".join(rows), encoding="utf-8")

        session._run_read("study.md", mode="structure")
        before = session._long_content_memory_prompt_block()
        self.assertIn("Hidden Result", before)
        self.assertNotIn("KEY RESULT", before)

        session._run_read("study.md", mode="segment", segment_id="s0003")
        after = session._long_content_memory_prompt_block()
        self.assertIn("read_card", after)
        self.assertIn("KEY RESULT", after)

    def test_long_content_identity_reuses_same_source_across_aliases(self):
        session = self.bare_session()
        body = "\n".join(f"same content line {idx}" for idx in range(220))
        first = session.files_root / "a.txt"
        second = session.files_root / "b.txt"
        first.write_text(body, encoding="utf-8")
        second.write_text(body, encoding="utf-8")

        session._run_read("a.txt", mode="structure")
        session._run_read("b.txt", mode="structure")
        self.assertEqual(len(session.long_content_memory), 1)
        memory = next(iter(session.long_content_memory.values()))
        self.assertEqual(set(memory["source_paths"]), {"a.txt", "b.txt"})

    def test_changing_one_shared_alias_keeps_other_alias_memory(self):
        session = self.bare_session()
        body = "\n".join(f"same content line {idx}" for idx in range(220))
        (session.files_root / "a.txt").write_text(body, encoding="utf-8")
        (session.files_root / "b.txt").write_text(body, encoding="utf-8")
        session._run_read("a.txt", mode="structure")
        session._run_read("b.txt", mode="structure")
        self.assertEqual(session._invalidate_long_content_memory_path("a.txt"), 0)
        memory = next(iter(session.long_content_memory.values()))
        self.assertEqual(memory["source_path"], "b.txt")
        self.assertFalse(memory["stale"])

    def test_semantic_card_is_bounded_and_called_once_per_source(self):
        session = self.bare_session()
        body = "\n".join(["# Intro"] + [f"fact line {idx}" for idx in range(230)])
        source = session.files_root / "semantic.md"
        source.write_text(body, encoding="utf-8")
        session.ollama.chat = mock.Mock(
            return_value={
                "content": (
                    '{"summary":"compact meaning","key_points":["p1","p2"],'
                    '"definitions":{"term":"meaning"},"relations":["a -> b"],'
                    '"evidence":["s0001 lines=1-180"]}'
                )
            }
        )
        out = session._run_read("semantic.md", mode="segment", segment_id="s0001")
        session._mark_long_content_read("semantic.md", source, body.splitlines(), {"mode": "segment", "segment_id": "s0001"}, out)
        memory = next(iter(session.long_content_memory.values()))
        self.assertEqual(memory["semantic_status"], "ready")
        self.assertEqual(memory["semantic"]["summary"], "compact meaning")
        self.assertEqual(session.ollama.chat.call_count, 1)
        session._mark_long_content_read("semantic.md", source, body.splitlines(), {"mode": "segment", "segment_id": "s0001"}, out)
        self.assertEqual(session.ollama.chat.call_count, 1)

    def test_semantic_failure_preserves_extractive_cards(self):
        session = self.bare_session()
        source = session.files_root / "semantic-fail.md"
        body = "\n".join(["# Intro"] + [f"fact line {idx}" for idx in range(230)])
        source.write_text(body, encoding="utf-8")
        session.ollama.chat = mock.Mock(side_effect=RuntimeError("offline"))
        out = session._run_read("semantic-fail.md", mode="segment", segment_id="s0001")
        session._mark_long_content_read("semantic-fail.md", source, body.splitlines(), {"mode": "segment", "segment_id": "s0001"}, out)
        memory = next(iter(session.long_content_memory.values()))
        self.assertEqual(memory["semantic_status"], "failed")
        self.assertTrue(any(card.get("text") for card in memory["cards"]))

    def test_long_read_is_recalled_from_cached_body_with_line_numbers(self):
        session = self.bare_session()
        body = "\n".join(f"background line {idx}" for idx in range(1200))
        body += "\n关键结论：量子效率为 42%，见表 3。\n"
        (session.files_root / "paper.txt").write_text(body, encoding="utf-8")

        session._record_read_context("paper.txt", {"mode": "full"}, body, role="developer")
        payload = cc.parse_json_object(
            session._tool_memory_tool(
                {"mode": "search", "query": "量子效率", "limit": 4}, role="developer"
            ),
            {},
        )
        item = payload["items"][0]
        self.assertGreater(item["cache_match_score"], 0)
        self.assertTrue(any("量子效率为 42%" in row for row in item["cached_matches"]))
        self.assertTrue(any("关键结论" in row for row in item["cached_matches"]))
        self.assertEqual(payload["cache_search"]["matched_entries"], 1)
        self.assertGreaterEqual(session.context_compaction_metrics["cache_hits"], 1)

    def test_cache_uses_source_not_clipped_rendered_output(self):
        session = self.bare_session()
        body = "head\n" + "\n".join(f"filler {idx}" for idx in range(800)) + "\nTAIL FACT: 98765\n"
        source = session.files_root / "paper.txt"
        source.write_text(body, encoding="utf-8")
        clipped = body[:1200] + "\n[read_file clipped chars=1-1200 of 10000]"
        session._record_read_context("paper.txt", {"mode": "full", "max_chars": 1200}, clipped, role="developer")
        payload = cc.parse_json_object(
            session._tool_memory_tool({"mode": "search", "query": "TAIL FACT", "limit": 2}, role="developer"),
            {},
        )
        self.assertEqual(payload["returned"], 1)
        self.assertIn("98765", payload["items"][0]["cached_matches"][0])

    def test_legacy_registry_normalization_keeps_entries_usable(self):
        session = self.bare_session()
        legacy = {
            "legacy": {
                "signature": "path=paper.txt|mode=full",
                "path": "paper.txt",
                "summary": "legacy evidence",
            }
        }
        normalized = session._normalize_read_context_registry(legacy)
        self.assertEqual(len(normalized), 1)
        self.assertTrue(session._read_context_entry_is_fresh(next(iter(normalized.values()))))

    def test_external_source_change_marks_cached_evidence_stale(self):
        session = self.bare_session()
        body = "\n".join(f"line {idx}" for idx in range(1000)) + "\nTARGET FACT 123\n"
        source = session.files_root / "paper.txt"
        source.write_text(body, encoding="utf-8")
        session._record_read_context("paper.txt", {"mode": "full"}, body, role="developer")

        source.write_text(body.replace("123", "999"), encoding="utf-8")
        session._tool_memory_tool({"mode": "summary"}, role="developer")
        read_entry = next(iter(session.read_context_registry.values()))
        self.assertEqual(read_entry["status"], "stale")
        self.assertIn("changed", read_entry["stale_reason"])
        result = cc.parse_json_object(
            session._tool_memory_tool(
                {"mode": "search", "query": "TARGET FACT", "limit": 4}, role="developer"
            ),
            {},
        )
        self.assertEqual(result["returned"], 0)

    def test_deterministic_summary_preserves_high_signal_evidence_when_llm_unavailable(self):
        session = self.bare_session()
        rows = [
            {"role": "user", "content": "Analyze the uploaded paper and report the causal mechanism."},
            {"role": "tool", "name": "read_file", "content": "path=paper.txt\nKEY RESULT: treatment reduced error by 42%."},
            {"role": "tool", "name": "bash", "content": "pytest -q\n2 passed"},
        ] * 20
        with mock.patch.object(session, "ollama", mock.Mock(chat=mock.Mock(side_effect=RuntimeError("offline")))):
            summary = session._summarize_compact_rows(rows)
        self.assertIn("KEY RESULT", summary)
        self.assertIn("paper.txt", summary)
        self.assertLess(len(summary), 4001)
        self.assertGreater(len(cc.json_dumps(rows)) / max(1, len(summary)), 5.0)

    def test_repeated_command_keeps_failed_and_successful_results_distinct_after_compaction(self):
        session = self.bare_session()
        command = "cd _build && python3 gen.py p008"
        args = {"command": command}
        failed = "Traceback (most recent call last):\nTypeError: cannot unpack non-iterable value"
        succeeded = "OK p008.html 44014 bytes"
        session._record_tool_memory(
            "bash", args, failed, role="single",
            evidence_kind="command_error", result_status="error",
        )
        session._record_tool_memory(
            "bash", args, succeeded, role="single",
            evidence_kind="validation", result_status="ok",
        )
        session.messages = [
            {
                "role": "assistant",
                "tool_calls": [{
                    "id": "failed-call",
                    "type": "function",
                    "function": {"name": "bash", "arguments": cc.json_dumps(args)},
                }],
            },
            {
                "role": "tool", "name": "bash", "tool_call_id": "failed-call",
                "content": failed, "result_ok": False, "result_status": "error",
            },
            {
                "role": "assistant",
                "tool_calls": [{
                    "id": "success-call",
                    "type": "function",
                    "function": {"name": "bash", "arguments": cc.json_dumps(args)},
                }],
            },
            {
                "role": "tool", "name": "bash", "tool_call_id": "success-call",
                "content": succeeded, "result_ok": True, "result_status": "ok",
            },
        ]
        failed_placeholder = session._compact_tool_memory_content(session.messages, 1, session.messages[1])
        success_placeholder = session._compact_tool_memory_content(session.messages, 3, session.messages[3])
        self.assertIn("result=error", failed_placeholder)
        self.assertIn("TypeError", failed_placeholder)
        self.assertNotIn("OK p008.html", failed_placeholder)
        self.assertIn("result=ok", success_placeholder)
        self.assertIn("OK p008.html", success_placeholder)

        # Older archives may already contain a contradictory summary.  The
        # immutable output digest repairs it at recall time.
        failed_sha = cc.hashlib.sha256(failed.encode("utf-8")).hexdigest()[:12]
        legacy = (
            f"[tool_memory cached tool=bash chars={len(failed)} sha256={failed_sha}]\n"
            f"signature: tool=bash|command={command}\n"
            "summary: bash: python3 gen.py p008 :: OK p008.html 44014 bytes"
        )
        repaired = session._refresh_archived_tool_memory_placeholder(legacy)
        self.assertIn("result=error", repaired)
        self.assertIn("TypeError", repaired)
        self.assertNotIn("OK p008.html", repaired)

    def test_context_recall_excludes_runtime_control_rows_by_default(self):
        session = self.bare_session()
        rows = [
            {"role": "user", "content": "real request about p008", "ts": 1},
            session._runtime_control_message(
                "<auto-continue>secret runtime retry</auto-continue>",
                control_tag="auto-continue",
            ),
        ]
        session._archive_context_segment(rows, "test")
        normal = cc.parse_json_object(
            session._context_recall({"mode": "search", "query": "secret runtime retry"}),
            {},
        )
        self.assertEqual(normal.get("returned"), 0)
        included = cc.parse_json_object(
            session._context_recall(
                {"mode": "search", "query": "secret runtime retry", "include_runtime": True}
            ),
            {},
        )
        self.assertEqual(included.get("returned"), 1)

    def test_auto_recall_keeps_model_evidence_and_projects_structured_ui_event(self):
        session = self.bare_session()
        session._archive_context_segment(
            [{"role": "user", "content": "missing calibration evidence", "ts": 1}],
            "test",
        )
        bind(session, "_emit", lambda self, *_args, **_kwargs: None)
        self.assertFalse(session._auto_context_recall_for_recovery())
        self.assertEqual(session.messages, [])
        self.assertTrue(session._auto_context_recall_for_recovery("calibration"))
        injected = session.messages[-1]
        self.assertEqual(injected["role"], "user")
        self.assertEqual(injected["origin"], "runtime")
        self.assertEqual(injected["type"], "runtime_control")
        self.assertFalse(injected["_ui_hidden"])
        self.assertTrue(session._is_runtime_internal_message(injected))
        projected = session._runtime_message_ui_projection(injected)
        self.assertEqual(projected["role"], "system")
        self.assertEqual(projected["type"], "runtime_hint")
        self.assertEqual(projected["data"]["control_tag"], "auto-context-recall")
        self.assertEqual(projected["data"]["query"], "calibration")
        self.assertEqual(projected["data"]["returned"], 1)
        self.assertTrue(projected["data"]["default_collapsed"])
        self.assertNotIn("secret", cc.json_dumps(projected))

    def test_dynamic_recall_uses_unresolved_locator_not_task_keywords(self):
        session = self.bare_session()
        session._archive_context_segment(
            [{"role": "tool", "name": "read_file", "content": "src/engine.py: invariant failure", "ts": 1}],
            "compact",
        )
        session.blackboard = {
            "failure_ledger": {
                "errors": [
                    {"file": "src/engine.py", "error_msg": "invariant failure", "count": 1}
                ]
            }
        }
        bind(session, "_emit", lambda self, *_args, **_kwargs: None)
        gap = session._dynamic_context_evidence_gap()
        self.assertTrue(gap["needed"])
        self.assertEqual(gap["query"], "src/engine.py")
        self.assertEqual(gap["reason"], "unresolved-evidence-not-in-active-context")
        self.assertTrue(session._auto_context_recall_for_recovery())

    def test_dynamic_recall_does_not_run_for_generic_failure_without_missing_locator(self):
        session = self.bare_session()
        session._archive_context_segment(
            [{"role": "user", "content": "historical evidence", "ts": 1}],
            "compact",
        )
        session.blackboard = {"failure_ledger": {"errors": []}}
        bind(session, "_emit", lambda self, *_args, **_kwargs: None)
        self.assertFalse(session._auto_context_recall_for_recovery())
        self.assertEqual(session.messages, [])

    def test_shell_pipeline_read_is_aligned_to_original_source_ranges(self):
        session = self.bare_session()
        rows = [f"ordinary source line {idx}" for idx in range(1, 281)]
        for idx in range(9, len(rows), 11):
            rows[idx] = ""
        rows[120] = "CRITICAL RESULT alpha connects mechanism A to outcome B"
        rows[220] = "CRITICAL RESULT beta confirms the same relationship"
        source = session.files_root / "docs" / "paper.txt"
        source.parent.mkdir()
        source.write_text("\n".join(rows), encoding="utf-8")
        filtered = [(idx, value) for idx, value in enumerate(rows, 1) if value]
        matches = [(pos, value) for pos, (_idx, value) in enumerate(filtered, 1) if "CRITICAL RESULT" in value]
        output = "\n".join(f"{pos}:{value}" for pos, value in matches)
        command = (
            f'cd "{session.files_root}" && grep -v "^$" docs/paper.txt '
            '| grep -n "CRITICAL RESULT" | sed -n "1,80p"'
        )

        with mock.patch.object(cc, "LONG_CONTENT_SEMANTIC_ENABLED", False):
            observed = session._ingest_shell_read_observations(
                "bash", {"command": command}, output, role="developer"
            )

        self.assertEqual([row["path"] for row in observed], ["docs/paper.txt"])
        memory = next(iter(session.long_content_memory.values()))
        self.assertIn([121, 121], memory["read_ranges"])
        self.assertIn([221, 221], memory["read_ranges"])
        self.assertIn("bash", memory["source_tools"])
        self.assertTrue(memory["observations"])
        self.assertTrue(memory["observed_segments"])
        self.assertEqual(memory["seen_segments"], [])
        prompt = session._long_content_memory_prompt_block()
        self.assertIn("verified_observation tool=bash", prompt)
        self.assertIn("CRITICAL RESULT", prompt)

    def test_custom_local_reader_contributes_without_command_specific_rules(self):
        session = self.bare_session()
        extractor = session.files_root / "extract.py"
        extractor.write_text("print('reader')\n", encoding="utf-8")
        rows = [f"book statement {idx}" for idx in range(1, 321)]
        rows[188] = "linked evidence emitted by a custom extractor"
        source = session.files_root / "book.txt"
        source.write_text("\n".join(rows), encoding="utf-8")
        output = "\n".join(rows[180:200])

        with mock.patch.object(cc, "LONG_CONTENT_SEMANTIC_ENABLED", False):
            observed = session._ingest_shell_read_observations(
                "bash",
                {"command": "python3 extract.py book.txt"},
                output,
                role="developer",
            )

        self.assertEqual([row["path"] for row in observed], ["book.txt"])
        memory = next(iter(session.long_content_memory.values()))
        self.assertTrue(session._long_content_range_is_covered(memory, 181, 200))
        self.assertEqual(memory["observations"][0]["source_tool"], "bash")

    def test_shell_fragment_projection_is_verified_without_full_line_output(self):
        session = self.bare_session()
        rows = [f"ordinary fact row {idx}" for idx in range(1, 220)]
        rows[146] = "prefix UNIQUE PROJECTED EVIDENCE connects state A and state B suffix"
        source = session.files_root / "facts.txt"
        source.write_text("\n".join(rows), encoding="utf-8")
        command = "grep -n -o 'UNIQUE PROJECTED EVIDENCE connects state A and state B' facts.txt"
        output = "147:UNIQUE PROJECTED EVIDENCE connects state A and state B"

        with mock.patch.object(cc, "LONG_CONTENT_SEMANTIC_ENABLED", False):
            observed = session._ingest_shell_read_observations(
                "bash", {"command": command}, output, role="developer"
            )

        self.assertEqual([row["path"] for row in observed], ["facts.txt"])
        memory = next(iter(session.long_content_memory.values()))
        self.assertIn([147, 147], memory["read_ranges"])
        self.assertAlmostEqual(memory["observations"][0]["confidence"], 0.72)

    def test_embedded_source_path_is_discovered_for_opaque_reader_expression(self):
        session = self.bare_session()
        rows = [f"embedded reader line {idx}" for idx in range(1, 240)]
        source = session.files_root / "notes.txt"
        source.write_text("\n".join(rows), encoding="utf-8")
        command = "python3 -c 'print(open(\"notes.txt\").read())'"
        output = "\n".join(rows[70:90])

        with mock.patch.object(cc, "LONG_CONTENT_SEMANTIC_ENABLED", False):
            observed = session._ingest_shell_read_observations(
                "bash", {"command": command}, output, role="developer"
            )

        self.assertEqual([row["path"] for row in observed], ["notes.txt"])
        memory = next(iter(session.long_content_memory.values()))
        self.assertTrue(session._long_content_range_is_covered(memory, 71, 90))

    def test_program_output_literal_does_not_become_fragment_read_of_script(self):
        session = self.bare_session()
        script = session.files_root / "emit.py"
        script.write_text("print('UNIQUE PROGRAM STATUS FROM SCRIPT')\n", encoding="utf-8")

        with mock.patch.object(cc, "LONG_CONTENT_SEMANTIC_ENABLED", False):
            observed = session._ingest_shell_read_observations(
                "bash",
                {"command": "python3 emit.py"},
                "UNIQUE PROGRAM STATUS FROM SCRIPT",
                role="developer",
            )

        self.assertEqual(observed, [])
        self.assertEqual(session.long_content_memory, {})

    def test_unrelated_command_output_does_not_claim_file_comprehension(self):
        session = self.bare_session()
        script = session.files_root / "large_test.py"
        script.write_text("\n".join(f"def case_{idx}(): return {idx}" for idx in range(240)), encoding="utf-8")

        with mock.patch.object(cc, "LONG_CONTENT_SEMANTIC_ENABLED", False):
            observed = session._ingest_shell_read_observations(
                "bash",
                {"command": "python3 large_test.py"},
                "240 tests passed in 0.42s",
                role="developer",
            )

        self.assertEqual(observed, [])
        self.assertEqual(session.long_content_memory, {})

    def test_tool_memory_search_finds_shell_linked_exact_evidence(self):
        session = self.bare_session()
        rows = [f"record {idx}" for idx in range(1, 260)]
        rows[210] = "UNIQUE SHELL FACT: retention improved by 42 percent"
        source = session.files_root / "records.txt"
        source.write_text("\n".join(rows), encoding="utf-8")
        command = "grep -n 'UNIQUE SHELL FACT' records.txt"
        output = "211:UNIQUE SHELL FACT: retention improved by 42 percent"

        with mock.patch.object(cc, "LONG_CONTENT_SEMANTIC_ENABLED", False):
            session._maybe_record_tool_memory_after_result(
                "bash", {"command": command}, output, role="developer"
            )
        payload = cc.parse_json_object(
            session._tool_memory_tool(
                {"mode": "search", "query": "retention improved", "limit": 4},
                role="developer",
            ),
            {},
        )

        self.assertEqual(payload["returned"], 1)
        self.assertEqual(payload["items"][0]["tool"], "bash")
        self.assertTrue(any("42 percent" in row for row in payload["items"][0]["cached_matches"]))

    def test_semantic_input_connects_verified_reads_across_sources(self):
        session = self.bare_session()
        first_rows = [f"first source line {idx}" for idx in range(1, 240)]
        second_rows = [f"second source line {idx}" for idx in range(1, 240)]
        first = session.files_root / "first.txt"
        second = session.files_root / "second.txt"
        first.write_text("\n".join(first_rows), encoding="utf-8")
        second.write_text("\n".join(second_rows), encoding="utf-8")
        with mock.patch.object(cc, "LONG_CONTENT_SEMANTIC_ENABLED", False):
            first_memory = session._merge_long_content_observation(
                "first.txt", first, first_rows, [[40, 42]], source_tool="read_file",
                locator="first evidence", excerpts=["L41: shared mechanism"],
            )
            second_memory = session._merge_long_content_observation(
                "second.txt", second, second_rows, [[80, 82]], source_tool="bash",
                locator="second evidence", excerpts=["L81: related outcome"],
            )
        first_memory["semantic_status"] = "ready"
        first_memory["semantic"] = {
            "summary": "The first source establishes a shared mechanism.",
            "key_points": ["shared mechanism"],
            "relations": [],
        }
        session.long_content_memory[first_memory["content_id"]] = first_memory

        prompt = session._long_content_semantic_input(second_memory, second_rows, {"s0001"})

        self.assertIn("VERIFIED_READ_OBSERVATIONS", prompt)
        self.assertIn("related outcome", prompt)
        self.assertIn("RELATED_SOURCE_CARDS", prompt)
        self.assertIn("first.txt", prompt)
        self.assertIn("shared mechanism", prompt)


if __name__ == "__main__":
    unittest.main()
