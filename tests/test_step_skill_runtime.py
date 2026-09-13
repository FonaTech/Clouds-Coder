import copy
import json
import threading
import types

import pytest
import test_skill_selection as selection_tests

import Clouds_Coder as cc


def evaluation(payload, *, load=(), keep=(), unload=(), discover=()):
    evidence = payload["step_text"] or payload["original_goal"] or "current Todo focus"
    def action(skill_id):
        return {"skill_id": skill_id, "purpose": "current step workflow decision", "confidence": 0.95, "evidence": [evidence]}
    return {
        "step_id": payload["step_id"], "assessment": "specialized",
        "load": [action(skill_id) for skill_id in load],
        "keep": [{"skill_id": skill_id, "purpose": "still needed by this step"} for skill_id in keep],
        "unload": [action(skill_id) for skill_id in unload],
        "discover": list(discover), "uncertainties": [],
    }


class ScriptedEvaluator:
    def __init__(self, callback=None):
        self.callback = callback or evaluation
        self.calls = []

    def chat(self, messages, **kwargs):
        self.calls.append((copy.deepcopy(messages), kwargs))
        result = self.callback(json.loads(messages[0]["content"]))
        return {"content": result if isinstance(result, str) else json.dumps(result)}


@pytest.fixture
def session(tmp_path):
    root = tmp_path / "skills"
    for name, description in (
        ("research", "Scientific literature and evidence synthesis"),
        ("briefing", "Design polished presentation decks for an audience, with visual hierarchy and speaker notes"),
        ("utility", "Specialized verification workflow"),
    ):
        selection_tests._write_skill(root, name, f"name: {name}\ndescription: {description}", body=f"BODY_ONLY_{name}\n" * 1000)
    instance = selection_tests.SkillSelectionTests()._runtime_session(cc.SkillStore(root), mode="single", plan=True)
    instance.max_agent_rounds = 20
    instance.runtime_authoritative_goal = "Produce a research result and communicate its findings"
    instance.blackboard["original_goal"] = instance.runtime_authoritative_goal
    instance.blackboard["task_epoch"] = 100.0
    instance._ensure_blackboard = types.MethodType(cc.SessionState._ensure_blackboard, instance)
    instance._blackboard_touch = types.MethodType(cc.SessionState._blackboard_touch, instance)
    instance.ollama = ScriptedEvaluator()
    instance._step_skill_restore_pending = False
    return instance


def set_step(session, index, text):
    session.blackboard["project_todos"] = [{
        "id": f"plan:{index}", "category": "plan_step", "status": "in_progress",
        "plan_step_index": index - 1, "content": text, "full_content": text,
        "activated_at": float(index),
    }]
    session.blackboard["plan_worker_todos"] = {}


def active(session):
    return set(session._loaded_skill_rows())


@pytest.mark.parametrize("text", ["研究汇报演示文稿", "答辩 slides", "presentation deck"])
def test_late_step_semantic_candidates_without_initial_selection(session, text):
    set_step(session, 1, "Analyze the scientific literature")
    session.ollama.callback = lambda payload: evaluation(payload, load=["local:research"])
    session._refresh_loaded_skills_for_execution_focus("run-start")
    assert active(session) == {"local:research"}
    set_step(session, 5, text)
    def choose(payload):
        assert "local:briefing" in {row["id"] for row in payload["candidates"]}
        assert payload["step_text"] == text
        return evaluation(payload, load=["local:briefing"])
    session.ollama.callback = choose
    result = session._refresh_loaded_skills_for_execution_focus("plan-step-transition")
    assert result["status"] == "completed"
    assert active(session) == {"local:research", "local:briefing"}
    assert result["state"]["step_id"] == "plan:5"
    assert len(session.ollama.calls) == 2
    assert "BODY_ONLY_research" in session._loaded_skills_context_block()
    session.ollama.callback = lambda payload: evaluation(payload, keep=["local:briefing"], unload=["local:research"])
    session._maybe_recheck_step_skills(force=True)
    assert active(session) == {"local:briefing"}
    assert "local:research" in session.skill_load_cache


def test_model_load_outside_selection_and_two_independent_unload_confirmations(session):
    session._maybe_recheck_step_skills()
    output = session._dispatch_tool_inner("load_skill", {"name": "local:utility", "purpose": "validate current findings"}, "developer")
    meta = json.loads(output.splitlines()[0])
    assert meta["source"] == "model"
    assert meta["active"] and not meta["pinned"] and meta["reevaluation_pending"]
    assert "BODY_ONLY_utility" in output
    assert len(session.ollama.calls) == 1
    session.ollama.callback = lambda payload: evaluation(payload, unload=["local:utility"])
    first = session._maybe_recheck_step_skills()
    assert "local:utility" in active(session)
    assert first["state"]["unload_confirmed"]["local:utility"]["count"] == 1
    assert session._maybe_recheck_step_skills()["skipped"]
    assert len(session.ollama.calls) == 2
    session._maybe_recheck_step_skills(force=True)
    assert "local:utility" not in active(session)
    assert "local:utility" in session.skill_load_cache
    events = session._ensure_blackboard()["skill_runtime_events"]
    unloaded = [row for row in events if row["event"] == "auto_unload"][-1]
    assert unloaded["confirmations"] == 2
    assert unloaded["purpose"] and unloaded["evaluation_id"] and unloaded["step_id"]


def test_model_unload_updates_state_and_does_not_get_immediately_reloaded(session):
    session._dispatch_tool_inner("load_skill", {"name": "local:utility"}, "developer")
    result = session._dispatch_tool_inner("unload_skill", {"name": "local:utility", "purpose": "not useful here"}, "developer")
    assert json.loads(result.splitlines()[0])["active"] is False
    assert not active(session)
    session.ollama.callback = lambda payload: evaluation(payload, load=["local:utility"])
    session._maybe_recheck_step_skills()
    assert not active(session)
    assert any(row["event"] == "model_unload" for row in session.blackboard["skill_runtime_events"])


def test_model_explicit_keep_intent_survives_rechecks_but_not_step_switch(session):
    session._maybe_recheck_step_skills()
    session._load_skill_with_cache("local:utility", load_source="model:developer", keep_for_step=True)
    session.ollama.callback = lambda payload: evaluation(payload, unload=["local:utility"])
    for _ in range(3):
        session._maybe_recheck_step_skills(force=True)
        assert "local:utility" in active(session)
    set_step(session, 2, "Compose the final artifact")
    session._maybe_recheck_step_skills()
    assert not active(session)


def test_cached_model_reload_expresses_step_keep_intent(session):
    session._maybe_recheck_step_skills()
    session._load_skill_with_cache("local:utility", load_source="auto:step-evaluation")
    session._load_skill_with_cache("local:utility", load_source="model:developer", purpose="still validating")
    session.ollama.callback = lambda payload: evaluation(payload, unload=["local:utility"])
    session._maybe_recheck_step_skills(force=True)
    assert "local:utility" in active(session)
    assert session._loaded_skill_rows()["local:utility"]["source"] == "model:developer"


def test_pinned_and_hard_bound_are_not_unloadable(session):
    session._load_skill_with_cache("local:research", load_source="manual")
    session.ollama.callback = lambda payload: evaluation(payload, unload=["local:research"])
    session._maybe_recheck_step_skills()
    assert "cannot be unloaded" in session._unload_skill("local:research", source="model:developer")
    assert active(session) == {"local:research"}
    session.skill_mode = "hard"
    session.bound_skill_ids = ["local:research"]
    assert session._maybe_recheck_step_skills(force=True)["status"] == "hard-bound"
    assert session._maybe_recheck_step_skills()["skipped"]
    assert "Error:" in session._dispatch_tool_inner("unload_skill", {"name": "local:research"}, "developer")
    assert "Error:" in session._dispatch_tool_inner("load_skill", {"name": "local:briefing"}, "developer")
    assert active(session) == {"local:research"}


@pytest.mark.parametrize("requested", ["invented", "research", "LOCAL:RESEARCH", "ambiguous"])
def test_invalid_id_rejects_entire_evaluation_without_mutating_active_set(session, requested):
    session.skills.ambiguous["ambiguous"] = ["local:research", "local:utility"]
    session._load_skill_with_cache("local:research", load_source="auto:step-evaluation")
    before = copy.deepcopy(session._loaded_skill_rows())
    session.ollama.callback = lambda payload: evaluation(payload, load=[requested], unload=["local:research"])
    result = session._maybe_recheck_step_skills()
    assert result["status"] == "unavailable"
    assert session._loaded_skill_rows() == before
    assert "evaluation unavailable" in session._loaded_skills_prompt_hint()


@pytest.mark.parametrize("response", ["{broken", "[]", "{}", '```json\n{}\n```', '{"unload":true}', '{"load":[NaN]}'])
def test_malformed_output_degrades_conservatively(session, response):
    session._load_skill_with_cache("local:research", load_source="auto:step-evaluation")
    session.ollama.callback = lambda payload: response
    assert session._maybe_recheck_step_skills()["status"] == "unavailable"
    assert active(session) == {"local:research"}
    assert session.blackboard["step_skill_state"]["evaluation_error"]


def test_unavailable_model_never_uses_metadata_to_autoload_or_unload(session):
    session._load_skill_with_cache("local:research", load_source="auto:step-evaluation")
    session.ollama = None
    set_step(session, 2, "Design presentation decks")
    session._auto_discover_and_load_skills("Design presentation decks")
    assert active(session) == {"local:research"}
    assert session.blackboard["step_skill_state"]["discovered_candidates"]
    assert session._reconcile_active_skills([]) == []
    session._prepare_loaded_skills_for_goal("Another goal")
    assert active(session) == {"local:research"}
    assert "Error:" in session._unload_skill("local:research", source="auto:legacy")
    assert "load_skill" in session._skills_awareness_block()
    assert "unload_skill" in session._skills_awareness_block()


def test_timeout_late_result_does_not_mutate_and_no_extra_thread_is_spawned(session, monkeypatch):
    started, release = threading.Event(), threading.Event()
    def slow(payload):
        started.set()
        release.wait(2)
        return evaluation(payload, load=["local:briefing"], unload=["local:research"])
    session._load_skill_with_cache("local:research", load_source="auto:step-evaluation")
    session.ollama.callback = slow
    monkeypatch.setattr(cc, "SKILL_RUNTIME_EVALUATION_TIMEOUT_SECONDS", 0.01)
    try:
        assert session._maybe_recheck_step_skills()["status"] == "unavailable"
        assert started.is_set()
        assert session._maybe_recheck_step_skills(force=True)["status"] == "unavailable"
        assert len(session.ollama.calls) == 1
    finally:
        release.set()
        session._step_skill_evaluation_worker.join(2)
    assert active(session) == {"local:research"}


def test_signature_ignores_status_updates_but_tracks_full_step_todo_and_targets(session):
    session._maybe_recheck_step_skills()
    session.current_phase = "agent:developer:tool:bash"
    session.blackboard["status"] = "REVIEWING"
    session.blackboard["task_profile"]["direct_objective"] = "manager routing paraphrase"
    assert session._maybe_recheck_step_skills()["skipped"]
    step = session.blackboard["project_todos"][0]
    step["full_content"] += "\n" + "Long unchanged text " * 200 + "New acceptance at tail"
    assert session._maybe_recheck_step_skills()["status"] == "completed"
    step = session.blackboard["project_todos"][0]
    step["deliverables"] = ["Audience handout"]
    assert session._maybe_recheck_step_skills()["status"] == "completed"
    step_id = session._active_skill_step_id()
    session.blackboard["plan_worker_todos"][step_id] = [{"content": "Explain findings", "status": "in_progress", "subtask_id": step_id + "-a", "owner": "developer"}]
    assert session._maybe_recheck_step_skills()["status"] == "completed"
    assert len(session.ollama.calls) == 4


def test_stateless_input_and_metadata_capsule_are_body_free(session):
    session.messages.append({"role": "assistant", "content": "MAIN_HISTORY_SECRET"})
    session.agent_messages.append({"role": "assistant", "content": "AGENT_HISTORY_SECRET"})
    session.manager_context.append({"role": "user", "content": "MANAGER_SECRET"})
    session._maybe_recheck_step_skills()
    messages, kwargs = session.ollama.calls[0]
    assert len(messages) == 1 and messages[0]["role"] == "user"
    assert "SECRET" not in json.dumps(messages) + kwargs["system"]
    assert "BODY_ONLY" not in json.dumps(messages)
    capsule = session._skill_metadata_capsule(max_chars=1800)
    assert len(capsule) <= 1800 and "local:briefing" in capsule
    assert "BODY_ONLY" not in capsule
    session._load_skill_with_cache("local:research", load_source="model:developer")
    assert "BODY_ONLY" not in session._skill_metadata_capsule()
    assert len(session._loaded_skills_context_block(max_chars=1200)) <= 1200


def test_model_discovery_and_toolchain_events_are_deferred_and_throttled(session):
    session._maybe_recheck_step_skills()
    session._dispatch_tool_inner("list_skills", {"query": "audience presentation decks"}, "developer")
    assert len(session.ollama.calls) == 1
    session._maybe_recheck_step_skills()
    assert len(session.ollama.calls) == 2
    session._dispatch_tool_inner("list_skills", {"query": "audience presentation decks"}, "developer")
    assert session._maybe_recheck_step_skills()["skipped"]
    session._observe_step_skill_tool("write_file", {"path": "results.data"})
    session._maybe_recheck_step_skills()
    session._observe_step_skill_tool("write_file", {"path": "another.data"})
    assert session._maybe_recheck_step_skills()["skipped"]
    assert len(session.ollama.calls) == 3
    session._observe_step_skill_tool("write_file", {"path": "report.unknown_extension"})
    session._maybe_recheck_step_skills()
    assert len(session.ollama.calls) == 4


def test_reload_blackboard_and_legacy_data_preserve_skills_events_and_model_intent(session):
    session._maybe_recheck_step_skills()
    session._load_skill_with_cache("local:utility", load_source="model:developer")
    session.ollama.callback = lambda payload: evaluation(payload, unload=["local:utility"])
    session._maybe_recheck_step_skills()
    saved = json.loads(json.dumps(session.blackboard))
    restored = session._normalize_blackboard(saved)
    assert restored["step_skill_state"] == saved["step_skill_state"]
    assert restored["skill_runtime_events"] == saved["skill_runtime_events"]
    session.blackboard = restored
    session._step_skill_restore_pending = True
    session._maybe_recheck_step_skills()
    assert not active(session)
    assert session.blackboard["step_skill_state"]["last_evaluation_trigger"] == "session-resume"
    legacy = session._normalize_blackboard({"loaded_skills": {"local:research": {"preview": "legacy"}}})
    assert legacy["loaded_skills"]["local:research"]["source"] == "legacy"
    assert legacy["step_skill_state"]["evaluation_status"] == "not_evaluated"
    assert session._normalize_step_skill_state({"revision": "bad", "model_loads": [], "unload_confirmed": {"legacy": 1}})["revision"] == 0


def test_evaluation_stale_during_focus_change_does_not_apply(session):
    def change_focus(payload):
        set_step(session, 2, "Different target while evaluation is pending")
        return evaluation(payload, load=["local:utility"])
    session.ollama.callback = change_focus
    assert session._maybe_recheck_step_skills()["status"] == "unavailable"
    assert not active(session)


def test_dependency_order_and_retained_dependency_protection(session):
    session.skills.skills["local:briefing"]["meta"]["requires"] = ["utility"]
    session.ollama.callback = lambda payload: evaluation(payload, load=["local:briefing"])
    assert session._maybe_recheck_step_skills()["status"] == "completed"
    assert list(session._loaded_skill_rows()) == ["local:utility", "local:briefing"]
    session.ollama.callback = lambda payload: evaluation(payload, keep=["local:briefing"], unload=["local:utility"])
    session._maybe_recheck_step_skills(force=True)
    assert active(session) == {"local:utility", "local:briefing"}


@pytest.mark.parametrize("relation,value", [("requires", "missing"), ("requires", "briefing"), ("conflicts", "research")])
def test_invalid_dependencies_or_conflicts_do_not_mutate_active_set(session, relation, value):
    session._load_skill_with_cache("local:research", load_source="manual")
    session.skills.skills["local:briefing"]["meta"][relation] = [value]
    session.ollama.callback = lambda payload: evaluation(payload, load=["local:briefing"])
    assert session._maybe_recheck_step_skills()["status"] == "unavailable"
    assert active(session) == {"local:research"}


def test_load_failure_is_visible_and_does_not_block_step(session, monkeypatch):
    monkeypatch.setattr(session.skills, "load", lambda name: "Error: remote provider unreachable")
    session.ollama.callback = lambda payload: evaluation(payload, load=["local:briefing"])
    assert session._maybe_recheck_step_skills()["status"] == "completed"
    assert not active(session)
    assert "local:briefing" in session._loaded_skills_prompt_hint()
    assert "unreachable" in session._loaded_skills_prompt_hint()


def test_ttl_expiry_rechecks_without_force(session):
    session._maybe_recheck_step_skills()
    session.blackboard["step_skill_state"]["last_evaluation_at"] -= cc.SKILL_RUNTIME_EVALUATION_TTL_SECONDS + 1
    session._maybe_recheck_step_skills()
    assert len(session.ollama.calls) == 2


def test_keep_decision_and_failure_reset_unload_confirmations(session):
    session._maybe_recheck_step_skills()
    session._load_skill_with_cache("local:utility", load_source="model:developer")
    session.ollama.callback = lambda payload: evaluation(payload, unload=["local:utility"])
    session._maybe_recheck_step_skills(force=True)
    session.ollama.callback = lambda payload: evaluation(payload, keep=["local:utility"])
    session._maybe_recheck_step_skills(force=True)
    assert session.blackboard["step_skill_state"]["unload_confirmed"] == {}
    session.ollama.callback = lambda payload: evaluation(payload, unload=["local:utility"])
    session._maybe_recheck_step_skills(force=True)
    assert "local:utility" in active(session)
    session.ollama.callback = lambda payload: "invalid output"
    session._maybe_recheck_step_skills(force=True)
    session.ollama.callback = lambda payload: evaluation(payload, unload=["local:utility"])
    session._maybe_recheck_step_skills(force=True)
    assert "local:utility" in active(session)


def test_unload_threshold_and_missing_action_fields(session):
    session._load_skill_with_cache("local:research", load_source="auto:step-evaluation")
    def low_confidence(payload):
        result = evaluation(payload, unload=["local:research"])
        result["unload"][0]["confidence"] = 0.79
        return result
    session.ollama.callback = low_confidence
    assert session._maybe_recheck_step_skills()["status"] == "completed"
    assert active(session) == {"local:research"}
    def no_evidence(payload):
        result = evaluation(payload, load=["local:briefing"], unload=["local:research"])
        result["unload"][0]["evidence"] = []
        return result
    session.ollama.callback = no_evidence
    assert session._maybe_recheck_step_skills(force=True)["status"] == "unavailable"
    assert active(session) == {"local:research"}


def test_discover_and_preferred_tool_requests_record_candidates(session):
    session.ollama.callback = lambda payload: evaluation(payload, discover=[{"query": "presentation decks", "purpose": "audience communication"}])
    session._maybe_recheck_step_skills()
    assert not active(session)
    assert any(row["skill_id"] == "local:briefing" for row in session.blackboard["step_skill_state"]["discovered_candidates"])
    session.skills.skills["local:utility"]["meta"]["preferred_tools"] = ["mcp__lab__inspect"]
    session._observe_step_skill_tool("mcp__lab__inspect", {})
    assert "unloaded-capability-requested" in session.blackboard["step_skill_state"]["pending_triggers"]
    session._maybe_recheck_step_skills()
    payload = json.loads(session.ollama.calls[-1][0][0]["content"])
    assert any(row.get("skill_id") == "local:utility" for row in payload["evidence"])


def test_no_plan_signature_ignores_manager_objective_and_todo_timestamps(session):
    session.blackboard["project_todos"] = []
    session.todo.items = []
    session._maybe_recheck_step_skills()
    session.blackboard["task_profile"]["direct_objective"] = "New manager wording, same user task"
    assert session._maybe_recheck_step_skills()["skipped"]
    session.todo.update([{"content": "Inspect the findings", "status": "in_progress"}])
    session._maybe_recheck_step_skills()
    before = session._step_skill_focus_signature()
    session.todo.items[0]["updated_at"] = cc.now_ts() + 100
    assert session._step_skill_focus_signature() == before


def test_encrypted_session_roundtrip_rechecks_once_and_preserves_cache(tmp_path, monkeypatch):
    skills = tmp_path / "skills"
    selection_tests._write_skill(skills, "research", "name: research\ndescription: scientific evidence", body="Persistent full workflow")
    monkeypatch.setattr(cc.SessionState, "_ensure_skills_ready", lambda self, force=False: None)
    args = dict(session_id="runtime-persistence", title="runtime persistence", root=tmp_path / "sessions",
                ollama_base="http://127.0.0.1:9", model="offline-test", skills_root=skills,
                crypto=cc.CryptoBox(tmp_path / "codes"), repo_root=tmp_path, js_lib_root=tmp_path / "js_lib")
    original = cc.SessionState(**args)
    original.blackboard = original._new_blackboard("Analyze scientific evidence")
    original.runtime_authoritative_goal = "Analyze scientific evidence"
    original._load_skill_with_cache("local:research", load_source="model:developer", purpose="research")
    original.ollama = ScriptedEvaluator(lambda payload: evaluation(payload, keep=["local:research"]))
    original._maybe_recheck_step_skills()
    original._persist()
    saved = args["crypto"].read_json(original.state_path, {})
    restored = cc.SessionState(**args)
    assert restored.blackboard["skill_runtime_events"] == saved["blackboard"]["skill_runtime_events"]
    assert restored.blackboard["step_skill_state"]["model_loads"]
    assert "Persistent full workflow" in cc.decompress_text_blob(restored.skill_load_cache["local:research"]["body_z"])
    restored.ollama = ScriptedEvaluator(lambda payload: evaluation(payload, keep=["local:research"]))
    restored._maybe_recheck_step_skills()
    assert len(restored.ollama.calls) == 1
    assert restored._maybe_recheck_step_skills()["skipped"]
    assert restored.blackboard["step_skill_state"]["last_evaluation_trigger"] == "session-resume"


def test_activation_and_plan_advance_evaluate_each_step_once(session, monkeypatch):
    set_step(session, 1, "Analyze the evidence")
    session.blackboard["project_todos"].append({
        "id": "plan:2", "category": "plan_step", "status": "pending",
        "content": "Communicate the findings", "full_content": "Communicate the findings",
        "plan_step_index": 1,
    })
    monkeypatch.setattr(session, "_ensure_worker_todos_available_for_plan_step", lambda *args, **kwargs: {"available": False})
    monkeypatch.setattr(session, "_current_plan_worker_owner", lambda *args: "developer")
    monkeypatch.setattr(session, "_step_subtasks_all_completed", lambda *args: True)
    for method in (
        "_record_plan_step_result", "_retire_plan_step_worker_todos", "_reset_plan_step_execution_boundary",
        "_blackboard_append_memory", "_update_plan_file_step_status", "_sync_todos_from_blackboard",
    ):
        monkeypatch.setattr(session, method, lambda *args, **kwargs: None)
    monkeypatch.setattr(session, "_append_plan_guidance_bubble", lambda *args, **kwargs: False)
    session.ollama.callback = lambda payload: evaluation(payload, load=["local:research"])
    session._activate_plan_step_execution(sync_todos=False)
    assert active(session) == {"local:research"}
    session.ollama.callback = lambda payload: evaluation(payload, load=["local:briefing"], unload=["local:research"])
    assert session._advance_plan_step(evidence="research complete")
    assert len(session.ollama.calls) == 2
    assert active(session) == {"local:briefing"}
    assert session.blackboard["step_skill_state"]["step_id"] == "plan:2"
    starts = [row for row in session.blackboard["skill_runtime_events"] if row["event"] == "step_skill_evaluation_started"]
    assert [row["step_id"] for row in starts] == ["plan:1", "plan:2"]


def test_model_intent_change_during_evaluation_discards_old_decision(session):
    session._load_skill_with_cache("local:research", load_source="auto:step-evaluation")
    def model_intent(payload):
        session._load_skill_with_cache("local:research", load_source="model:developer", purpose="still needed")
        return evaluation(payload, unload=["local:research"])
    session.ollama.callback = model_intent
    assert session._maybe_recheck_step_skills()["status"] == "unavailable"
    assert active(session) == {"local:research"}
    assert session.blackboard["step_skill_state"]["keep_intents"]


def test_same_evaluation_cannot_supply_second_unload_confirmation(session):
    session._maybe_recheck_step_skills()
    session._load_skill_with_cache("local:utility", load_source="model:developer")
    session.ollama.callback = lambda payload: evaluation(payload, unload=["local:utility"])
    result = session._maybe_recheck_step_skills()
    payload = json.loads(session.ollama.calls[-1][0][0]["content"])
    with pytest.raises(ValueError, match="already applied"):
        session._apply_step_skill_evaluation(result["result"], payload=payload, evaluation_id=result["state"]["evaluation_id"])
    assert active(session) == {"local:utility"}


def test_cached_load_does_not_shrink_full_long_skill_body(session):
    data = session.skills.skills["local:research"]
    data["meta"]["runtime_contract"] = "Short runtime contract"
    full_body = data["body"]
    first = session._load_skill_with_cache("local:research", load_source="model:developer")
    second = session._load_skill_with_cache("local:research", load_source="model:developer")
    assert full_body in first and first == second
    assert full_body in cc.decompress_text_blob(session.skill_load_cache["local:research"]["body_z"])
