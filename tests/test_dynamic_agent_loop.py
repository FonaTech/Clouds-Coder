import inspect
import types
import unittest

import Clouds_Coder as cc


def bind(instance, name, function):
    setattr(instance, name, types.MethodType(function, instance))


class DynamicAgentLoopTests(unittest.TestCase):
    def bare_session(self):
        session = cc.SessionState.__new__(cc.SessionState)
        session.ui_language = "zh-CN"
        session.todo = cc.TodoManager("zh-CN")
        session.execution_mode = "sync"
        session.runtime_execution_mode = "sync"
        session.blackboard = {}
        session.runtime_task_type = "general"
        session.agent_loop_progress_state = {}
        session.read_file_loop_state = {}
        session.read_file_loop_recent = []
        session.read_file_loop_count = 0
        session.read_file_loop_last_intervention_ts = 0.0
        session.tool_memory_loop_state = {}
        session.web_search_context_registry = {}
        session.messages = []
        session.events = []
        bind(session, "_ensure_blackboard", lambda self: self.blackboard)
        bind(
            session,
            "_emit",
            lambda self, *args, **kwargs: self.events.append((args, kwargs)),
        )
        bind(session, "_ledger_record_stall", lambda self, *args, **kwargs: None)
        return session

    @staticmethod
    def read_result(command="head -20 papers.txt", output="paper metadata"):
        return {
            "name": "bash",
            "args": {"command": command},
            "output": output,
            "ok": True,
            "exit_code": 0,
        }

    def test_reused_evidence_is_reported_without_selecting_next_action(self):
        session = self.bare_session()
        session.todo.update(
            [
                {"content": "汇总研究证据并编写文章分类报告", "status": "in_progress"},
                {"content": "验证报告", "status": "pending"},
            ]
        )
        result = self.read_result()

        first = session._update_agent_loop_progress_state([result])
        second = session._update_agent_loop_progress_state([result])
        third = session._update_agent_loop_progress_state([result])

        self.assertEqual(first["round_kind"], "evidence_new")
        self.assertEqual(second["round_kind"], "evidence_reused")
        self.assertTrue(third["guidance_active"])
        self.assertNotIn("next_action", third)
        prompt = session._agent_loop_progress_prompt_block()
        self.assertIn("汇总研究证据并编写文章分类报告", prompt)
        self.assertIn("progress_signal=evidence_reused", prompt)
        self.assertIn("mode=observation-only", prompt)
        self.assertIn("Choose autonomously", prompt)
        self.assertNotIn("phase_bias=", prompt)
        self.assertNotIn("next_action=", prompt)

    def test_broad_fresh_reads_eventually_raise_observation_signal(self):
        session = self.bare_session()
        session.todo.update(
            [
                {"content": "收集并总结论文标题", "status": "in_progress"},
            ]
        )

        states = []
        for index in range(4):
            states.append(
                session._update_agent_loop_progress_state(
                    [
                        self.read_result(
                            command=f"head -20 paper_{index}.txt",
                            output=f"metadata {index}",
                        )
                    ]
                )
            )

        self.assertTrue(states[-1]["guidance_active"])
        self.assertEqual(
            states[-1]["guidance_reason"], "evidence_without_todo_progress"
        )
        self.assertNotIn("next_action", states[-1])

    def test_real_mutation_resets_stagnation_without_rewriting_todos(self):
        session = self.bare_session()
        session.todo.update(
            [
                {"content": "实现文章预览页面", "status": "in_progress"},
            ]
        )
        repeated = self.read_result("head -20 app.js", "const app = true")
        for _ in range(3):
            session._update_agent_loop_progress_state([repeated])
        before = session.todo.snapshot()

        state = session._update_agent_loop_progress_state(
            [
                {
                    "name": "write_file",
                    "args": {"path": "index.html", "content": "<main></main>"},
                    "output": "Wrote 13 bytes to index.html",
                    "ok": True,
                }
            ]
        )

        self.assertEqual(state["round_kind"], "mutation")
        self.assertFalse(state["guidance_active"])
        self.assertEqual(state["reused_streak"], 0)
        self.assertEqual(session.todo.snapshot(), before)

    def test_completed_todos_plus_validation_are_reported_without_forcing_finish(self):
        session = self.bare_session()
        session.todo.update(
            [
                {"content": "生成报告", "status": "completed"},
                {"content": "验收报告", "status": "completed"},
            ]
        )
        state = session._update_agent_loop_progress_state(
            [
                {
                    "name": "bash",
                    "args": {"command": "python3 -m pytest -q"},
                    "output": "2 passed",
                    "ok": True,
                    "exit_code": 0,
                }
            ]
        )

        self.assertTrue(state["guidance_active"])
        self.assertTrue(state["seen_validation"])
        self.assertNotIn("next_action", state)
        prompt = session._agent_loop_progress_prompt_block()
        self.assertIn("all_completed=true", prompt)
        self.assertIn("seen_validation=true", prompt)
        self.assertNotIn("finish the overall task", prompt)

    def test_strategy_intervention_uses_internal_state_not_synthetic_user_messages(
        self,
    ):
        session = self.bare_session()
        session.todo.update(
            [
                {"content": "分析资料并写出结论", "status": "in_progress"},
            ]
        )
        result = {
            "name": "query_knowledge_library",
            "args": {"query": "article classification"},
            "output": "results=3 useful evidence",
            "ok": True,
        }

        for _ in range(3):
            session._maybe_inject_tool_strategy_intervention([result])

        self.assertEqual(session.messages, [])
        state = session.agent_loop_progress_state["single"]
        self.assertTrue(state["guidance_active"])
        self.assertEqual(state["guidance_reason"], "repeated_tool_evidence")

    def test_multi_agent_prompt_reads_the_same_worker_scoped_progress_state_it_records(
        self,
    ):
        session = self.bare_session()
        session.runtime_assigned_expert = "developer"
        session.todo.update(
            [
                {
                    "content": "实现当前计划步骤",
                    "status": "in_progress",
                    "owner": "developer",
                },
            ]
        )
        result = self.read_result("head -20 current_step.js", "const ready = true")

        for _ in range(3):
            session._update_agent_loop_progress_state([result], role="developer")

        self.assertIn("developer", session.agent_loop_progress_state)
        prompt = session._agent_loop_progress_prompt_block(
            for_role=session.runtime_assigned_expert
        )
        self.assertIn("progress_signal=evidence_reused", prompt)
        self.assertIn("实现当前计划步骤", prompt)
        self.assertIn("Choose autonomously", prompt)
        self.assertNotIn("phase_bias=", prompt)
        self.assertNotIn("next_action=", prompt)

    def test_single_keeps_autonomous_loop_but_receives_todo_alignment_facts(self):
        session = self.bare_session()
        session.execution_mode = "single"
        session.runtime_execution_mode = "single"
        session.runtime_assigned_expert = "developer"
        session.todo.update(
            [
                {
                    "content": "实现当前计划步骤",
                    "status": "in_progress",
                    "owner": "developer",
                },
            ]
        )
        result = self.read_result("head -20 current_step.js", "const ready = true")

        for _ in range(3):
            session._update_agent_loop_progress_state([result], role="developer")

        self.assertIn("developer", session.agent_loop_progress_state)
        self.assertEqual(
            session._agent_loop_progress_prompt_block(for_role="developer"),
            "",
        )
        prompt = session._single_agent_todo_alignment_prompt_block(for_role="developer")
        self.assertIn("<single-todo-alignment-state>", prompt)
        self.assertIn("实现当前计划步骤", prompt)
        self.assertIn("mode=observation-only", prompt)
        self.assertIn("update_mode='status_update'", prompt)
        self.assertIn("One call may mark every evidence-backed completed row", prompt)
        self.assertNotIn("phase_bias=", prompt)
        self.assertNotIn("next_action=", prompt)

    def test_multi_agent_does_not_receive_single_todo_alignment_block(self):
        session = self.bare_session()
        session.todo.update(
            [
                {
                    "content": "实现当前计划步骤",
                    "status": "in_progress",
                    "owner": "developer",
                },
            ]
        )
        self.assertEqual(
            session._single_agent_todo_alignment_prompt_block(for_role="developer"),
            "",
        )

    def test_single_system_prompt_injects_alignment_without_restoring_phase_classifier(
        self,
    ):
        source = inspect.getsource(cc.SessionState._system_prompt)
        self.assertIn("_single_agent_todo_alignment_prompt_block", source)
        discipline = inspect.getsource(cc.SessionState._plan_todo_discipline_prompt)
        self.assertIn(
            "Observable tool results provide completion evidence but do not close ordinary work rows by themselves",  # noqa: E501
            discipline,
        )
        self.assertIn("update them together in one call", discipline)

        session = self.bare_session()
        session.execution_mode = "single"
        session.runtime_execution_mode = "single"
        session.runtime_assigned_expert = "developer"
        session.runtime_task_level = 2
        session.runtime_round_budget = 0
        session.single_advance_prompt_enhance = False
        session.web_search_enabled = False
        session.skill_mode = "hard"
        session.skills = types.SimpleNamespace(descriptions=lambda: "")
        session.files_root = "/workspace"
        session.context_token_upper_bound = 200_000
        session.todo.update(
            [
                {
                    "content": "检查 Python 运行环境",
                    "status": "completed",
                    "owner": "developer",
                },
                {
                    "content": "验证物理模型数值",
                    "status": "in_progress",
                    "owner": "developer",
                },
                {"content": "编写正式脚本", "status": "pending", "owner": "developer"},
            ]
        )
        bind(session, "_effective_execution_mode", lambda self: "single")
        bind(session, "_ensure_skills_ready", lambda self, force=False: None)
        bind(session, "_ensure_blackboard", lambda self: self.blackboard)
        for method_name in (
            "_uploads_prompt_block",
            "_html_frontend_boost_instruction",
            "_deep_research_boost_instruction",
            "_knowledge_library_prompt_block",
            "_code_library_prompt_block",
            "_engineering_execution_boost_instruction",
            "_runtime_code_reference_prompt_block",
            "_runtime_knowledge_reference_prompt_block",
            "_read_context_prompt_block",
            "_user_profile_capsule_prompt_block",
            "_mcp_prompt_block",
            "_loaded_skills_prompt_hint",
            "_loaded_skills_context_block",
            "_plan_steps_context_for_manager",
            "_plan_todo_discipline_prompt",
            "_todo_contract_prompt_block",
            "_multimodal_capability_block",
            "_public_progress_prompt_instruction",
        ):
            bind(session, method_name, lambda self, *args, **kwargs: "")
        bind(
            session,
            "_blackboard_memory_context_markdown",
            lambda self, max_chars=3200: "",
        )
        bind(
            session,
            "_runtime_environment_context_prompt_block",
            lambda self: "runtime context",
        )

        prompt = session._system_prompt()
        self.assertIn("<single-todo-alignment-state>", prompt)
        self.assertIn("current=验证物理模型数值 status=in_progress", prompt)
        self.assertIn("todo_progress=1/3", prompt)
        self.assertIn("update_mode='status_update'", prompt)
        self.assertNotIn("<dynamic-agent-loop-state>", prompt)
        self.assertNotIn("phase_bias=", prompt)
        self.assertNotIn("next_action=", prompt)


if __name__ == "__main__":
    unittest.main()
