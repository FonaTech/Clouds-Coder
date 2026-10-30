import inspect
import types
import unittest
from unittest import mock

import Clouds_Coder as cc


def bind(instance, name, function):
    setattr(instance, name, types.MethodType(function, instance))


def metrics(*, left_percent, used=80_000, effective_limit=100_000):
    return {
        "used": used,
        "effective_limit": effective_limit,
        "limit": effective_limit + 5_000,
        "left": max(0, effective_limit - used),
        "left_percent": left_percent,
    }


class ContextAutoCompactTests(unittest.TestCase):
    def bare_session(self, metric_rows):
        session = cc.SessionState.__new__(cc.SessionState)
        session.active_agent_role = ""
        session.agent_round_index = 4
        session.last_compact_ts = 0.0
        session.context_last_compact_effective = True
        session.context_last_compact_skip_ts = 0.0
        session.context_last_compact_used_reduction = 0
        session.events = []
        rows = iter(metric_rows)
        bind(session, "_active_next_call_context_metrics", lambda self, **kwargs: dict(next(rows)))
        bind(session, "_microcompact", lambda self, **kwargs: None)
        bind(session, "_compact_agent_contexts", lambda self, tier: None)
        bind(session, "_role_specific_context_is_live_call", lambda self, role: False)
        bind(session, "_emit", lambda self, kind, data: self.events.append((kind, data)))
        session._auto_compact = mock.Mock()
        return session

    def test_tier2_runs_full_compact_before_effective_limit_is_exhausted(self):
        before = metrics(left_percent=15.0, used=85_000)
        after_micro = metrics(left_percent=14.0, used=86_000)
        session = self.bare_session([before, after_micro])

        compacted = session._apply_auto_compact_if_needed("auto")

        self.assertTrue(compacted)
        session._auto_compact.assert_called_once_with(
            "auto", metrics=after_micro, role="", media_inputs=None
        )

    def test_tier1_remains_microcompact_only(self):
        before = metrics(left_percent=30.0, used=70_000)
        after_micro = metrics(left_percent=31.0, used=69_000)
        session = self.bare_session([before, after_micro])

        compacted = session._apply_auto_compact_if_needed("auto")

        self.assertFalse(compacted)
        session._auto_compact.assert_not_called()

    def test_post_micro_metrics_can_deescalate_tier2_without_full_compact(self):
        before = metrics(left_percent=15.0, used=85_000)
        after_micro = metrics(left_percent=25.0, used=75_000)
        session = self.bare_session([before, after_micro])

        compacted = session._apply_auto_compact_if_needed("auto")

        self.assertFalse(compacted)
        session._auto_compact.assert_not_called()

    def test_tier3_bypasses_ineffective_compact_cooldown(self):
        before = metrics(left_percent=5.0, used=95_000)
        after_micro = metrics(left_percent=5.0, used=95_000)
        session = self.bare_session([before, after_micro])
        session.context_last_compact_effective = False
        session.context_last_compact_skip_ts = 9_990.0

        with mock.patch.object(cc, "now_ts", return_value=10_000.0):
            compacted = session._apply_auto_compact_if_needed("auto")

        self.assertTrue(compacted)
        session._auto_compact.assert_called_once()

    def test_all_execution_loops_recheck_context_before_model_calls(self):
        single = inspect.getsource(cc.SessionState._agent_worker)
        sync = inspect.getsource(cc.SessionState._multi_agent_sync_blackboard_worker)
        sequential = inspect.getsource(cc.SessionState._multi_agent_worker)
        worker = inspect.getsource(cc.SessionState._multi_agent_turn)
        plan = inspect.getsource(cc.SessionState._plan_mode_explorer_turn)

        self.assertIn('_apply_auto_compact_if_needed("auto", role=single_role)', single)
        self.assertIn('_apply_auto_compact_if_needed("auto:multi-sync", role="manager")', sync)
        self.assertIn('_apply_auto_compact_if_needed("auto:multi-seq", role=current_role)', sequential)
        self.assertIn('f"auto:agent:{role_key}"', worker)
        self.assertIn('_apply_auto_compact_if_needed("auto:plan-explorer", role="explorer")', plan)

    def test_empty_action_recovery_is_evaluated_after_auto_compact(self):
        single = inspect.getsource(cc.SessionState._agent_worker)

        compact_check = single.index('_apply_auto_compact_if_needed("auto", role=single_role)')
        empty_action_check = single.index("consecutive_empty_action_rounds += 1")

        self.assertLess(compact_check, empty_action_check)


if __name__ == "__main__":
    unittest.main()
