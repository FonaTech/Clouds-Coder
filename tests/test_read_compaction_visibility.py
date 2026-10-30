"""Read results stay usable across compaction, so the model need not re-read.

These cover the root causes of repeated reads:
- microcompact replaced read results every round, even at tier 0;
- results were replaced before the model ever saw them;
- the read pin had a per-message cutoff below read_file's own output cap;
- "already read" bookkeeping did not notice when compaction removed the text,
  so the delta reply dropped lines the model could no longer see.
"""

import types
import unittest

import test_context_memory_recall as recall_fixtures

import Clouds_Coder as cc


def bind(instance, name, function):
    setattr(instance, name, types.MethodType(function, instance))


def tool_pair(call_id, name, args, content):
    """An assistant tool call plus its tool result, in the shape the loops store."""
    return [
        {
            "role": "assistant",
            "content": "",
            "tool_calls": [{"id": call_id, "type": "function", "function": {"name": name, "arguments": args}}],
        },
        {"role": "tool", "tool_call_id": call_id, "name": name, "content": content},
    ]


class ReadCompactionVisibilityTests(unittest.TestCase):
    def session(self):
        session = recall_fixtures.ContextMemoryRecallTests("test_long_content_structure_and_segment_reads_preserve_coverage").bare_session()
        session.agent_messages = []
        session.active_agent_role = ""
        return session

    def big_reads(self, session, count=5, size=20_000):
        for index in range(count):
            body = f"file {index}\n" + ("x" * size)
            session.messages.extend(tool_pair(f"r{index}", "read_file", {"path": f"f{index}.py"}, body))

    # C1: no read compaction at tier 0 -------------------------------------

    def test_tier0_keeps_every_file_read_intact_in_the_single_agent_context(self):
        session = self.session()
        self.big_reads(session, 5)
        session._microcompact(preserve_reads=True)
        bodies = [m["content"] for m in session.messages if m.get("role") == "tool"]
        self.assertTrue(all(body.startswith("file ") for body in bodies), [b[:40] for b in bodies])

    def test_tier0_keeps_reads_in_a_role_context(self):
        session = self.session()
        messages = []
        for index in range(5):
            messages.extend(tool_pair(f"r{index}", "read_file", {"path": f"f{index}.py"}, f"file {index}\n" + "y" * 20_000))
        session._microcompact_agent_messages(messages, keep_recent=3, preserve_reads=True)
        bodies = [m["content"] for m in messages if m.get("role") == "tool"]
        self.assertTrue(all(body.startswith("file ") for body in bodies))

    def test_without_preserve_reads_older_reads_still_compact(self):
        # Under context pressure (tier >= 1) reads can still be compacted.
        # Context growth stays bounded.
        session = self.session()
        bind(session, "_read_context_budget", lambda self, tier=None: {"tier": 3, "pin_distinct": 1})
        self.big_reads(session, 5)
        session._microcompact(keep_recent=1)
        bodies = [m["content"] for m in session.messages if m.get("role") == "tool"]
        self.assertTrue(any(not body.startswith("file ") for body in bodies))

    # C2: unseen results are never compacted ---------------------------------

    def test_unseen_results_survive_microcompact_and_legacy_rows_do_not(self):
        session = self.session()
        bind(session, "_read_context_budget", lambda self, tier=None: {"tier": 3, "pin_distinct": 1})
        for index in range(5):
            pair = tool_pair(f"b{index}", "bash", {"command": f"echo {index}"}, f"out {index}\n" + "z" * 5000)
            if index < 2:
                pair[1]["_unseen"] = True
            session.messages.extend(pair)
        session._microcompact(keep_recent=1)
        tools = [m for m in session.messages if m.get("role") == "tool"]
        self.assertTrue(tools[0]["content"].startswith("out 0"))
        self.assertTrue(tools[1]["content"].startswith("out 1"))
        self.assertFalse(tools[2]["content"].startswith("out 2"))

    def test_seen_flag_is_cleared_after_a_model_call(self):
        messages = [{"role": "tool", "tool_call_id": "a", "content": "x", "_unseen": True}]
        cc.SessionState._mark_tool_messages_seen(messages)
        self.assertNotIn("_unseen", messages[0])

    def test_unseen_flag_never_reaches_the_provider_payload(self):
        client = cc.OllamaClient("http://model.test", "demo", provider="openai_compat")
        history = tool_pair("a", "read_file", {"path": "x.py"}, "body")
        history[1]["_unseen"] = True
        prepared = client._prepare_request_messages(history, "openai_compat")
        self.assertTrue(prepared)
        self.assertTrue(all("_unseen" not in row for row in prepared))

    # C3: a normal-size read can be pinned -----------------------------------

    def test_a_50k_read_can_be_pinned(self):
        session = self.session()
        session.messages.extend(tool_pair("big", "read_file", {"path": "big.py"}, "B" * 50_000))
        pinned = session._read_file_pinned_tool_message_ids(session.messages)
        self.assertIn(id(session.messages[-1]), pinned)

    # C4/C5: "already read" follows what is still visible --------------------

    def read_window(self, session, call_id, offset, limit):
        source = session.files_root / "doc.txt"
        lines = source.read_text().splitlines()
        args = {"mode": "window", "offset": offset, "limit": limit}
        out = session._run_read("doc.txt", **args)
        session._mark_long_content_read("doc.txt", source, lines, args, out, tool_call_id=call_id)
        session.messages.extend(tool_pair(call_id, "read_file", {"path": "doc.txt", **args}, out))
        return out

    def test_visible_range_returns_a_short_unchanged_marker(self):
        session = self.session()
        (session.files_root / "doc.txt").write_text("\n".join(f"line {i}" for i in range(400)), encoding="utf-8")
        self.read_window(session, "w1", 0, 120)
        again = session._run_read("doc.txt", mode="window", offset=0, limit=120)
        self.assertIn("read_file reused", again)
        self.assertIn("already_in_context", again)
        self.assertIn("tool_call_id=w1", again)
        self.assertNotIn("line 5", again)

    def test_compacted_range_is_replayed_not_dropped(self):
        session = self.session()
        (session.files_root / "doc.txt").write_text("\n".join(f"line {i}" for i in range(400)), encoding="utf-8")
        self.read_window(session, "w1", 0, 120)
        for msg in session.messages:
            if msg.get("role") == "tool":
                msg["content"] = "[read_file cached path=doc.txt]"
        again = session._run_read("doc.txt", mode="window", offset=0, limit=120)
        self.assertNotIn("already_in_context", again)
        self.assertIn("line 5", again)

    def test_partial_overlap_returns_only_lines_not_visible(self):
        session = self.session()
        (session.files_root / "doc.txt").write_text("\n".join(f"line {i}" for i in range(400)), encoding="utf-8")
        self.read_window(session, "w1", 0, 120)
        delta = session._run_read("doc.txt", mode="window", offset=60, limit=120)
        self.assertIn("read_file delta", delta)
        self.assertIn("uncovered_lines=121-180", delta)

    # C6: small whole-file reads record coverage ------------------------------

    def test_small_whole_file_read_records_its_range(self):
        session = self.session()
        source = session.files_root / "small.py"
        source.write_text("a = 1\nb = 2\nc = 3\n", encoding="utf-8")
        lines = source.read_text().splitlines()
        out = session._run_read("small.py")
        session._mark_long_content_read("small.py", source, lines, {}, out, tool_call_id="s1", read_range=(1, len(lines)))
        memory = next(iter(session.long_content_memory.values()))
        self.assertEqual(memory["read_ranges"], [[1, 3]])
        self.assertEqual(memory["visible_reads"][-1]["tool_call_id"], "s1")


if __name__ == "__main__":
    unittest.main()


class BashReadAndEditFeedbackTests(unittest.TestCase):
    def session(self):
        session = recall_fixtures.ContextMemoryRecallTests("test_long_content_structure_and_segment_reads_preserve_coverage").bare_session()
        session.agent_messages = []
        session.root = session.files_root.parent
        return session

    # C7: bash reads are recognised and cacheable ------------------------------

    def test_session_root_variable_is_a_read_target_confined_to_files_root(self):
        session = self.session()
        (session.files_root / "pkg").mkdir()
        (session.files_root / "pkg" / "mod.py").write_text("a = 1\n", encoding="utf-8")
        for token in ("$SESSION_ROOT/pkg/mod.py", "${SESSION_ROOT}/pkg/mod.py", "/workspace/pkg/mod.py"):
            self.assertEqual(session._shell_candidate_rel_path(token), "pkg/mod.py", token)
        # Anything that resolves outside files_root is still rejected.
        self.assertEqual(session._shell_candidate_rel_path("$SESSION_ROOT/../outside.py"), "")
        self.assertEqual(session._shell_candidate_rel_path("$HOME/.ssh/id_rsa"), "")

    def test_discarding_stderr_keeps_the_readonly_cache_but_appending_does_not(self):
        session = self.session()
        (session.files_root / "notes.txt").write_text("hello\n", encoding="utf-8")
        cached = session._readonly_bash_cache_key("cat notes.txt 2>/dev/null")
        self.assertTrue(cached)
        self.assertEqual(session._readonly_bash_cache_key("cat notes.txt >> copy.txt"), "")
        self.assertEqual(session._readonly_bash_cache_key("cat notes.txt &> log.txt"), "")
        self.assertEqual(session._readonly_bash_cache_key("cat notes.txt > copy.txt"), "")

    def test_sed_head_tail_ranges_are_parsed_exactly(self):
        rng = cc.SessionState._shell_command_line_range
        self.assertEqual(rng("sed -n '10,40p' a.py", 100), (10, 40))
        self.assertEqual(rng("sed -n 7p a.py 2>/dev/null", 100), (7, 7))
        self.assertEqual(rng("head -n 25 a.py", 100), (1, 25))
        self.assertEqual(rng("tail -20 a.py", 100), (81, 100))
        self.assertIsNone(rng("cat a.py | head -n 5", 100))
        self.assertIsNone(rng("sed -n '1,5p' a.py; rm a.py", 100))

    # C9: edits return the changed region ---------------------------------------

    def test_edit_snippet_shows_numbered_changed_region_with_context(self):
        before = "\n".join(f"line {i}" for i in range(1, 61))
        after = before.replace("line 30", "line 30 changed")
        snippet, span = cc.SessionState._edit_result_snippet(before, after)
        self.assertEqual(span, (22, 38))
        self.assertIn("30: line 30 changed", snippet)
        self.assertTrue(snippet.startswith("22: line 22"))

    def test_edit_snippet_is_empty_when_nothing_changed(self):
        self.assertEqual(cc.SessionState._edit_result_snippet("a\nb", "a\nb"), ("", (0, 0)))
