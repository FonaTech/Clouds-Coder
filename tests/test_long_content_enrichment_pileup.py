"""Long-content semantic enrichment must not pile up model requests.

Every long read used to start one more background enrichment call while the
previous one was still in flight, and a finished call wrote its result onto a
dict that ``_merge_long_content_observation`` had already replaced.
"""

import threading
import time
import unittest
from unittest import mock

import test_context_memory_recall as recall_tests

import Clouds_Coder as cc

SEMANTIC_JSON = (
    '{"summary":"compact meaning","key_points":["p1"],"definitions":{},'
    '"relations":[],"evidence":["s0001 lines=1-180"]}'
)


class BlockingChat:
    """Mock ``chat`` that holds each call until released and tracks overlap."""

    def __init__(self, content=SEMANTIC_JSON):
        self.content = content
        self.release = threading.Event()
        self.lock = threading.Lock()
        self.calls = 0
        self.in_flight = 0
        self.peak_in_flight = 0
        self.kwargs = []

    def __call__(self, messages, **kwargs):
        with self.lock:
            self.calls += 1
            self.in_flight += 1
            self.peak_in_flight = max(self.peak_in_flight, self.in_flight)
            self.kwargs.append(dict(kwargs))
        try:
            if not self.release.wait(10):
                raise TimeoutError("test chat was never released")
            return {"content": self.content}
        finally:
            with self.lock:
                self.in_flight -= 1


def wait_until(predicate, timeout=5.0):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if predicate():
            return True
        time.sleep(0.01)
    return False


class LongContentEnrichmentPileupTests(unittest.TestCase):
    def setUp(self):
        self.session = recall_tests.ContextMemoryRecallTests().bare_session()
        self.session.lock = threading.RLock()
        self.body = "\n".join(["# Intro"] + [f"fact line {idx}" for idx in range(230)])
        self.source = self.session.files_root / "long.md"
        self.source.write_text(self.body, encoding="utf-8")
        self.lines = self.body.splitlines()
        self.chat = BlockingChat()
        self.session.ollama.chat = self.chat

    def tearDown(self):
        self.chat.release.set()
        worker = getattr(self.session, "_semantic_enrichment_worker", None)
        if worker is not None:
            worker.join(5)

    def read_segment(self):
        out = self.session._run_read("long.md", mode="segment", segment_id="s0001", fresh=True)
        self.session._mark_long_content_read(
            "long.md", self.source, self.lines, {"mode": "segment", "segment_id": "s0001"}, out
        )
        return out

    def memory(self):
        return next(iter(self.session.long_content_memory.values()))

    def test_repeated_reads_keep_at_most_one_enrichment_in_flight(self):
        # A short join timeout makes the first call "time out" while its
        # request is still blocked; previously each later read then started
        # another request for the same file.
        with mock.patch.object(cc, "LONG_CONTENT_SEMANTIC_TIMEOUT_SECONDS", 0.05):
            for _ in range(5):
                self.read_segment()
                # Each read rebuilds the store, as in a real session.
                self.assertLessEqual(self.chat.in_flight, 1)
                time.sleep(0.1)
        self.assertTrue(wait_until(lambda: self.chat.calls >= 1))
        self.assertEqual(self.chat.calls, 1)
        self.assertEqual(self.chat.peak_in_flight, 1)
        # Tagged as an auxiliary call with a socket timeout aligned to the
        # worker's join timeout.
        call = self.chat.kwargs[0]
        self.assertTrue(call["auxiliary"])
        self.assertEqual(call["label"], "semantic_enrichment")
        self.assertAlmostEqual(call["request_timeout"], 0.05 + 2.0)
        self.assertEqual(self.memory()["semantic_status"], "pending")

    def test_result_lands_in_current_entry_after_store_rebuild(self):
        self.read_segment()
        self.assertTrue(wait_until(lambda: self.chat.calls == 1))
        started_with = self.memory()
        # Later reads rebuild long_content_memory with fresh dict objects.
        self.read_segment()
        self.read_segment()
        current = self.memory()
        self.assertIsNot(current, started_with)
        self.chat.release.set()
        self.session._semantic_enrichment_worker.join(5)
        self.assertFalse(self.session._semantic_enrichment_worker.is_alive())
        current = self.memory()
        self.assertEqual(current["semantic_status"], "ready")
        self.assertEqual(current["semantic"]["summary"], "compact meaning")
        self.assertEqual(current["semantic_started_at"], 0.0)
        # Normalizing the store again (as every read does) keeps the card.
        rebuilt = self.session._normalize_long_content_memory(self.session.long_content_memory)
        self.assertEqual(rebuilt[current["content_id"]]["semantic"]["summary"], "compact meaning")
        self.assertEqual(self.chat.calls, 1)

    def test_failed_card_waits_for_retry_at(self):
        self.chat.release.set()
        self.session.ollama.chat = mock.Mock(side_effect=RuntimeError("offline"))
        self.read_segment()
        self.session._semantic_enrichment_worker.join(5)
        memory = self.memory()
        self.assertEqual(memory["semantic_status"], "failed")
        self.assertGreater(memory["semantic_retry_at"], cc.now_ts())
        self.assertEqual(self.session.ollama.chat.call_count, 1)
        # Before retry_at no new request starts, however often it is read.
        for _ in range(3):
            self.read_segment()
        self.assertEqual(self.session.ollama.chat.call_count, 1)
        self.assertEqual(self.memory()["semantic_status"], "failed")
        # Once retry_at has passed, the next read tries again.
        self.memory()["semantic_retry_at"] = cc.now_ts() - 1.0
        self.session.ollama.chat = mock.Mock(return_value={"content": SEMANTIC_JSON})
        self.read_segment()
        self.session._semantic_enrichment_worker.join(5)
        self.assertEqual(self.session.ollama.chat.call_count, 1)
        self.assertEqual(self.memory()["semantic_status"], "ready")

    def run_slow_call(self, outcome):
        def slow_chat(messages, **kwargs):
            time.sleep(0.3)
            if isinstance(outcome, Exception):
                raise outcome
            return {"content": outcome}

        self.session.ollama.chat = slow_chat
        with mock.patch.object(cc, "LONG_CONTENT_SEMANTIC_TIMEOUT_SECONDS", 0.05):
            self.read_segment()
            started_with = self.memory()
            self.read_segment()  # rebuilds the store while the call is in flight
            self.assertIsNot(self.memory(), started_with)
            self.session._semantic_enrichment_worker.join(5)
        self.assertFalse(self.session._semantic_enrichment_worker.is_alive())
        return self.memory()

    def test_socket_timeout_after_join_timeout_marks_current_entry_failed(self):
        current = self.run_slow_call(TimeoutError("timed out"))
        self.assertEqual(current["semantic_status"], "failed")
        self.assertGreater(current["semantic_retry_at"], cc.now_ts())

    def test_late_answer_within_socket_timeout_is_kept(self):
        current = self.run_slow_call(SEMANTIC_JSON)
        self.assertEqual(current["semantic_status"], "ready")
        self.assertEqual(current["semantic"]["summary"], "compact meaning")


if __name__ == "__main__":
    unittest.main()
