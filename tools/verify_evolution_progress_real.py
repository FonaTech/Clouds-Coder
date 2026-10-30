"""Verify progress using a real configured model and actual multi-turn tools.

The task is declared public compatibility data, not a private historical session.
No architecture candidate is proposed or deployed.
"""
import argparse
import json
import sys
import threading
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import Clouds_Coder as cc  # noqa: E402
from liquid_kernel import LiquidKernelControlPlane, normalize_evolution_config  # noqa: E402
from liquid_kernel.agentic import AgenticBenchmark  # noqa: E402
from liquid_kernel.control import BASELINE_KERNEL_FILES  # noqa: E402
from tools.verify_model_compatibility_real import compatibility_task  # noqa: E402


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', type=Path, required=True)
    parser.add_argument('--profile', default='qwen')
    parser.add_argument('--runtime-config', type=Path)
    parser.add_argument('--report', type=Path, required=True)
    parser.add_argument('--evidence-dir', type=Path, required=True)
    args = parser.parse_args()
    raw = json.loads(args.config.read_text())
    profiles = {p['id']: p for p in cc.parse_llm_config_profiles(raw, 'http://127.0.0.1:11434', '')['profiles']}
    runtime = json.loads(args.runtime_config.read_text()) if args.runtime_config else {}
    runtime = runtime.get('defaults', runtime.get('draft', runtime))
    root = args.evidence_dir.resolve()
    root.mkdir(parents=True, exist_ok=True, mode=0o700)
    app = cc.AppContext.__new__(cc.AppContext)
    app.global_profiles, app.global_active_profile_id = profiles, args.profile
    app.codes_root, app.crypto = root/'Codes', cc.CryptoBox(root/'Codes')
    app.ide_auth = cc.IDEAuthStore(root/'ide.sqlite')
    app.liquid_kernel = plane = LiquidKernelControlPlane(root/'evolution', model_callback=app._liquid_kernel_model_call,
        task_runtime_limits=lambda: {'max_rounds': int(runtime.get('max_rounds', cc.MAX_AGENT_ROUNDS)),
                                     'context_token_limit': int(runtime.get('ctx_limit', cc.DEFAULT_CONTEXT_TOKEN_LIMIT))})
    config = normalize_evolution_config({'mode': 'Tuning', 'budget': {'max_tokens': 500000}})
    config = plane._apply_task_runtime_limits(config)
    plane.save_config(config, plane.config()['revision'])
    config = plane.config()
    run = plane.registry.create_run(config, 'declared_public_progress_verification')
    plane.active_run_id, plane._token_limit, plane._tokens_used = run, 500000, 0
    plane._active_deadline = time.monotonic()+1200
    plane.run_lock.acquire()
    snapshots, stop = [], threading.Event()
    def sample():
        while not stop.wait(.2):
            snapshots.append(plane.registry.run_detail(run)['progress'])
    observer = threading.Thread(target=sample, daemon=True)
    observer.start()
    ref = {'source': 'global', 'owner': '', 'profile_id': args.profile, 'model': profiles[args.profile]['model']}
    def model(system, payload, tokens=4096, *, deadline=None):
        plane._call_deadline = min(plane._active_deadline, deadline or plane._active_deadline)
        try:
            return plane._call_model(system, json.dumps(payload, ensure_ascii=False), ref, tokens)
        finally:
            plane._call_deadline = 0
    def progress(kind, payload):
        plane.registry.event(run, kind, payload)
        snapshots.append(plane.registry.run_detail(run)['progress'])
    report = {'model': profiles[args.profile]['model'], 'source': 'declared public compatibility task', 'deployed': False,
              'max_rounds': config['task_benchmark']['max_rounds'], 'run_id': run}
    try:
        result = AgenticBenchmark(model, lambda: plane._check_cancel(run), progress,
                                  archive_root=root/'full_history').run(BASELINE_KERNEL_FILES, [compatibility_task()], config['task_benchmark'], 'incumbent')
        outcome = result['rows'][0]
        detail = plane.registry.run_detail(run)
        state = detail['progress']
        report.update(outcome={k: outcome[k] for k in ('success', 'rounds', 'tool_calls', 'score', 'error')}, progress=state,
                      sampled_states=len(snapshots), waiting_observed=any(p.get('model', {}).get('state')=='waiting' for p in snapshots),
                      heartbeat_observed=any(p.get('model', {}).get('state')=='waiting' and p.get('heartbeat_at', 0)>p.get('last_activity_at', 0) for p in snapshots))
        assert outcome['success'], outcome['error']
        assert report['waiting_observed']
        assert state['execution']['round']==outcome['rounds']
        assert state['execution']['tool_calls']==outcome['tool_calls']
        assert state['model']['completed']>0 and state['model']['completed']==state['model']['started']
        plane.registry.update_run(run, 'no_change', completed_at=time.time(), result_json={'verification_only': True, 'evaluated': True, 'candidate_deployed': False})
        report['passed'] = True
    except Exception as exc:
        report.update(passed=False, error=type(exc).__name__+': '+str(exc)[:1000])
    finally:
        stop.set()
        observer.join(2)
        plane.active_run_id=''
        plane.run_lock.release()
        args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
        (root/'progress.snapshots.json').write_text(json.dumps(snapshots, ensure_ascii=False)+'\n')
        print(json.dumps({k: report.get(k) for k in ('passed','model','outcome','sampled_states','heartbeat_observed','error')},ensure_ascii=False))
    return 0 if report.get('passed') else 1


if __name__=='__main__':
    raise SystemExit(main())
