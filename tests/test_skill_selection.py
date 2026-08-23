import tempfile
import types
import unittest
from pathlib import Path

import Clouds_Coder as cc


def _write_skill(
    root: Path, folder: str, frontmatter: str, body: str = "workflow"
) -> None:
    skill_dir = root / folder
    skill_dir.mkdir(parents=True, exist_ok=True)
    (skill_dir / "SKILL.md").write_text(
        f"---\n{frontmatter.strip()}\n---\n{body}\n",
        encoding="utf-8",
    )


class SkillSelectionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name) / "skills"
        self.root.mkdir()

    def tearDown(self):
        self.tmp.cleanup()

    def test_recall_searches_all_metadata_not_first_thirty(self):
        for index in range(35):
            _write_skill(
                self.root,
                f"generic-{index:02d}",
                f"name: generic-{index:02d}\ndescription: Generic unrelated workflow {index}",  # noqa: E501
            )
        _write_skill(
            self.root,
            "z-special",
            "name: z-special\ndescription: Specialized quasar telemetry\ntriggers: [quasar telemetry]",  # noqa: E501
        )
        store = cc.SkillStore(self.root)

        recalled = store.recall_metadata("diagnose quasar telemetry", limit=12)

        self.assertIn("local:z-special", [row["id"] for row in recalled])

    def test_canonicalization_accepts_id_name_alias_and_case(self):
        _write_skill(
            self.root,
            "frontend",
            "name: Frontend-Pro\ndescription: Browser UI workflow\naliases: [UI Builder]",  # noqa: E501
        )
        store = cc.SkillStore(self.root)

        for requested in (
            "local:Frontend-Pro",
            "Frontend-Pro",
            "frontend-pro",
            "UI Builder",
            "ui builder",
        ):
            with self.subTest(requested=requested):
                result = store.canonicalize_id(requested)
                self.assertTrue(result["ok"])
                self.assertEqual(result["canonical_id"], "local:Frontend-Pro")

    def test_unknown_and_ambiguous_names_are_structured_errors(self):
        _write_skill(
            self.root, "one", "name: one\ndescription: First\naliases: [shared]"
        )
        _write_skill(
            self.root, "two", "name: two\ndescription: Second\naliases: [shared]"
        )
        store = cc.SkillStore(self.root)

        self.assertEqual(store.canonicalize_id("missing")["code"], "unknown")
        ambiguous = store.canonicalize_id("shared")
        self.assertEqual(ambiguous["code"], "ambiguous")
        self.assertEqual(set(ambiguous["candidates"]), {"local:one", "local:two"})

    def test_negative_trigger_filters_candidate(self):
        _write_skill(
            self.root,
            "browser",
            "name: browser\ndescription: Browser report workflow\ntriggers: [report]\nnot_for: [PDF]",  # noqa: E501
        )
        store = cc.SkillStore(self.root)

        self.assertEqual(store.recall_metadata("make a PDF report"), [])
        self.assertEqual(
            store.recall_metadata("make a browser report")[0]["id"], "local:browser"
        )

    def test_recall_deduplicates_tokens_and_does_not_substring_match_ide(self):
        _write_skill(
            self.root,
            "video-comprehension",
            "name: video-comprehension\ndescription: Analyze video and screen recordings",  # noqa: E501
        )
        _write_skill(
            self.root,
            "telemetry",
            "name: telemetry\ndescription: Quasar telemetry workflow\ntriggers: [quasar telemetry]",  # noqa: E501
        )
        store = cc.SkillStore(self.root)

        self.assertEqual(store.recall_metadata("IDE programming request"), [])
        once = store.recall_metadata("quasar telemetry")[0]["score"]
        repeated = store.recall_metadata("quasar quasar telemetry telemetry")[0][
            "score"
        ]
        self.assertEqual(once, repeated)

    def test_declared_entrypoint_is_recalled_without_loading_body(self):
        _write_skill(
            self.root,
            "analysis-engine",
            "name: analysis-engine\n"
            "description: Domain analysis workflow\n"
            "triggers: [simulation analysis]\n"
            "entrypoints: [guides/analysis.md]",
            body="The full workflow body is intentionally not loaded for recall.",
        )
        store = cc.SkillStore(self.root)

        recalled = store.recall_metadata("run a simulation analysis", limit=12)

        self.assertEqual(recalled[0]["id"], "local:analysis-engine")
        self.assertGreaterEqual(recalled[0]["score"], 6.0)
        self.assertIn("guides/analysis.md", recalled[0]["entrypoints"])

    def test_selector_rejects_malformed_and_unknown_llm_output(self):
        _write_skill(
            self.root,
            "api",
            "name: api\ndescription: API integration\ntriggers: [API integration]",
        )
        store = cc.SkillStore(self.root)

        malformed = store.select_skills(
            "implement API integration",
            llm_selector=lambda _rows: "{not-json",
        )
        unknown = store.select_skills(
            "implement API integration",
            llm_selector=lambda _rows: '{"selected":[{"id":"invented"}]}',
        )

        self.assertEqual(malformed["selected"], [])
        self.assertEqual(malformed["fallback_type"], "invalid_output")
        self.assertEqual(unknown["selected"], [])
        self.assertEqual(unknown["filtered"][0]["reason"], "unknown")

    def test_selector_canonicalizes_alias_and_reports_relations(self):
        _write_skill(
            self.root,
            "api",
            "name: api\ndescription: API integration\naliases: [service]\ntriggers: [API integration]\nrequires: [auth]",  # noqa: E501
        )
        _write_skill(
            self.root,
            "auth",
            "name: auth\ndescription: API authentication\ntriggers: [API authentication]\nconflicts: [api-alt]",  # noqa: E501
        )
        _write_skill(
            self.root,
            "api-alt",
            "name: api-alt\ndescription: Alternative API integration\ntriggers: [API integration]\nconflicts: [auth]",  # noqa: E501
        )
        store = cc.SkillStore(self.root)
        selected = store.select_skills(
            "implement API integration and API authentication",
            llm_selector=lambda _rows: {
                "selected": ["service", "auth", "api-alt"],
            },
        )

        self.assertEqual(selected["selection_order"], ["local:api", "local:auth"])
        self.assertEqual(selected["conflicts"][0]["id"], "local:api-alt")
        self.assertEqual(selected["requires"], [])

        missing = store.select_skills(
            "implement API integration",
            llm_selector=lambda _rows: {"selected": ["service"]},
        )
        self.assertEqual(missing["selected"], [])
        self.assertEqual(missing["requires"][0]["missing"], ["local:auth"])

        pinned_conflict = store.select_skills(
            "implement alternative API integration",
            llm_selector=lambda _rows: {"selected": ["api-alt"]},
            active_ids=["auth"],
        )
        self.assertEqual(pinned_conflict["selected"], [])
        self.assertEqual(pinned_conflict["conflicts"][0]["with"], "local:auth")

    def _bare_session(self, store: cc.SkillStore):
        session = cc.SessionState.__new__(cc.SessionState)
        session.skill_mode = "dynamic"
        session.skills = store
        session.skills_runtime_prepared = True
        session.skills_last_refresh_ts = cc.now_ts()
        session.skill_load_cache = {}
        session.blackboard = {"loaded_skills": {}, "project_todos": []}
        session.messages = []
        session.agent_messages = []
        session.contexts = {role: [] for role in cc.AGENT_ROLES}
        session.manager_context = []
        session.events = []
        session.updated_at = cc.now_ts()
        session.bound_skill_ids = []
        session._persist = lambda: None
        session._blackboard_touch = types.MethodType(lambda self: None, session)
        session._ensure_blackboard = types.MethodType(
            lambda self: self.blackboard, session
        )
        session._ensure_skills_ready = types.MethodType(
            lambda self, force=False: None, session
        )
        session._emit = types.MethodType(
            lambda self, kind, payload: self.events.append((kind, payload)), session
        )
        session._active_skill_step_id = types.MethodType(
            lambda self, board=None: "step-1", session
        )
        session._tier_agent_context_limits = types.MethodType(
            lambda self, _tier: {"agent_messages": 100}, session
        )
        session._context_budget_tier_for_dynamic_memory = types.MethodType(
            lambda self: 1, session
        )
        return session

    def _runtime_session(self, store: cc.SkillStore, *, mode: str, plan: bool):
        session = self._bare_session(store)
        session.ui_language = "zh-CN"
        session.todo = cc.TodoManager("zh-CN")
        session.runtime_reclassify_goal = "Build a scientific simulation application"
        session.runtime_execution_mode = mode
        session.execution_mode = mode
        session.runtime_plan_approved = plan
        session.runtime_plan_mode_needed = plan
        session.ollama = None
        session._latest_user_goal_text = types.MethodType(
            lambda self: "Build a scientific simulation application",
            session,
        )
        session._active_skill_step_id = types.MethodType(
            cc.SessionState._active_skill_step_id, session
        )
        if plan:
            session.blackboard["project_todos"] = [
                {
                    "id": "plan:cfd",
                    "key": "bb:proj:plan:cfd",
                    "content": "实现 Navier-Stokes 压力投影流体求解器",
                    "full_content": "实现 Navier-Stokes 压力投影流体求解器与可视化",
                    "category": "plan_step",
                    "status": "in_progress",
                    "plan_step_index": 0,
                }
            ]
            session.blackboard["plan_step_total"] = 1
        else:
            session.todo.update(
                [
                    {
                        "content": "实现 Navier-Stokes 压力投影流体求解器",
                        "status": "in_progress",
                        "owner": "developer",
                    }
                ]
            )
        return session

    def test_manual_load_pins_duplicate_does_not_reinject_and_unload_works(self):
        _write_skill(self.root, "api", "name: api\ndescription: API integration")
        store = cc.SkillStore(self.root)
        session = self._bare_session(store)

        first = session._load_skill_with_cache("API", load_source="manual:developer")
        message_count = len(session.messages)
        second = session._load_skill_with_cache(
            "local:api", load_source="manual:developer"
        )
        row = session.blackboard["loaded_skills"]["local:api"]

        self.assertEqual(first, second)
        self.assertEqual(row["scope"], "pinned")
        self.assertEqual(len(session.messages), message_count)
        self.assertIn("unloaded", session._unload_skill("api"))
        self.assertEqual(session.blackboard["loaded_skills"], {})

    def test_hard_bound_skill_cannot_be_unloaded(self):
        session = cc.SessionState.__new__(cc.SessionState)
        session.skill_mode = "hard"
        self.assertIn("cannot be unloaded", session._unload_skill("bound"))

    def test_auto_selection_applies_in_all_plan_and_execution_modes(self):
        _write_skill(
            self.root,
            "fluid-solver",
            "name: fluid-solver\ndescription: Fluid solver workflow\ntriggers: [Navier-Stokes]",  # noqa: E501
            body="Use pressure projection and verify divergence.",
        )
        store = cc.SkillStore(self.root)

        for plan in (False, True):
            for mode in (cc.EXECUTION_MODE_SINGLE, cc.EXECUTION_MODE_SYNC):
                with self.subTest(plan=plan, mode=mode):
                    session = self._runtime_session(store, mode=mode, plan=plan)
                    selection = session._refresh_loaded_skills_for_execution_focus(
                        trigger="run-start"
                    )

                    self.assertIn(
                        "local:fluid-solver", session.blackboard["loaded_skills"]
                    )
                    row = session.blackboard["loaded_skills"]["local:fluid-solver"]
                    self.assertEqual(row["scope"], "active")
                    self.assertEqual(row["step_id"], session._active_skill_step_id())
                    self.assertEqual(
                        selection["selection_order"], ["local:fluid-solver"]
                    )
                    diagnostics = [
                        payload
                        for kind, payload in session.events
                        if kind == "skill_selection"
                    ][-1]
                    self.assertEqual(diagnostics["execution_mode"], mode)
                    self.assertEqual(diagnostics["plan_focus_active"], plan)
                    self.assertEqual(diagnostics["todo_focus_active"], not plan)
                    manager_context = session._loaded_skills_context_block(
                        for_role="manager"
                    )
                    worker_context = session._loaded_skills_context_block(
                        for_role="developer"
                    )
                    self.assertIn("Use pressure projection", manager_context)
                    self.assertIn("Use pressure projection", worker_context)

                    event_count = len(
                        [
                            event
                            for event in session.events
                            if event[0] == "skill_selection"
                        ]
                    )
                    repeated = session._refresh_loaded_skills_for_execution_focus(
                        trigger="manager-round"
                    )
                    self.assertTrue(repeated["skipped"])
                    self.assertEqual(
                        len(
                            [
                                event
                                for event in session.events
                                if event[0] == "skill_selection"
                            ]
                        ),
                        event_count,
                    )

    def test_no_plan_todo_transition_replaces_active_skill(self):
        _write_skill(
            self.root,
            "fluid-solver",
            "name: fluid-solver\ndescription: Fluid solver\ntriggers: [Navier-Stokes]",
        )
        _write_skill(
            self.root,
            "slides",
            "name: slides\ndescription: Presentation workflow\ntriggers: [PowerPoint deck]",  # noqa: E501
        )
        store = cc.SkillStore(self.root)
        session = self._runtime_session(
            store, mode=cc.EXECUTION_MODE_SINGLE, plan=False
        )

        session._refresh_loaded_skills_for_execution_focus(trigger="first-todo")
        self.assertEqual(
            set(session.blackboard["loaded_skills"]), {"local:fluid-solver"}
        )
        session.todo.update(
            [
                {
                    "content": "实现 Navier-Stokes 压力投影流体求解器",
                    "status": "completed",
                },
                {"content": "Create a PowerPoint deck", "status": "in_progress"},
            ]
        )
        session._refresh_loaded_skills_for_execution_focus(
            trigger="todo-focus-transition"
        )

        self.assertEqual(set(session.blackboard["loaded_skills"]), {"local:slides"})

    def test_todo_dispatch_refreshes_when_no_plan_focus_changes(self):
        _write_skill(
            self.root,
            "fluid",
            "name: fluid\ndescription: Fluid\ntriggers: [Navier-Stokes]",
        )
        store = cc.SkillStore(self.root)
        session = self._runtime_session(
            store, mode=cc.EXECUTION_MODE_SINGLE, plan=False
        )
        session.todo.items = []
        refreshes = []
        session._capture_todo_write_transaction = types.MethodType(
            lambda self, *args, **kwargs: {}, session
        )
        session._get_active_plan_step = types.MethodType(
            lambda self, board=None: None, session
        )
        session._todo_route_kind = types.MethodType(
            lambda self, **kwargs: "pure_single", session
        )
        session._merge_flat_todo_items = types.MethodType(
            lambda self, items, **kwargs: self.todo.update(items),
            session,
        )
        session._refresh_loaded_skills_for_execution_focus = types.MethodType(
            lambda self, trigger="": refreshes.append(trigger),
            session,
        )

        session._dispatch_todo_update(
            {
                "items": [
                    {"content": "实现 Navier-Stokes 求解器", "status": "in_progress"}
                ]
            },
            role="developer",
        )

        self.assertEqual(refreshes, ["todo-focus-transition"])


if __name__ == "__main__":
    unittest.main()
