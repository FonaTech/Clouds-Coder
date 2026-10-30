"""Run real session-derived tasks through Admin HTTP and configured remote models.

--sources is an explicitly selected JSON list of redacted session records. Only
human requests should be included; never include API keys or private attachments.
The selected requests are sent to the configured task designer. No generated
proposal is approved, promoted, or deployed by this verifier.
"""
import argparse
import copy
import http.client
import json
import shutil
import sys
import tempfile
import threading
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import Clouds_Coder as cc  # noqa: E402
from liquid_kernel import LiquidKernelControlPlane  # noqa: E402
from liquid_kernel.agentic import source_sessions  # noqa: E402
from liquid_kernel.agentic import digest  # noqa: E402
import liquid_kernel.control as control  # noqa: E402


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', type=Path, required=True)
    parser.add_argument('--sources', type=Path, required=True, help='Explicitly selected redacted human session records; sent to the remote model')
    parser.add_argument('--frozen-task-bank', type=Path, help='Reuse a real task bank with explicit interpreter normalization and fingerprint lineage; skips task design only')
    parser.add_argument('--runtime-config', type=Path, help='Admin startup_config.json; defaults beside the supplied model config')
    parser.add_argument('--generator', required=True)
    parser.add_argument('--judge', required=True)
    parser.add_argument('--mode', choices=['Tuning', 'Thinking', 'Aggressive'], default='Thinking')
    parser.add_argument('--candidates', type=int, default=1)
    parser.add_argument('--max-tokens', type=int, default=0, help='Explicit total token quota; 0 is unlimited')
    parser.add_argument('--max-task-tokens', type=int, default=0)
    parser.add_argument('--control-reserve-percent', type=int, default=35)
    parser.add_argument('--evidence-dir', type=Path, help='Preserve complete protected task/review archives locally')
    parser.add_argument('--timeout', type=int, default=0, help='Explicit total time cap; 0 is unlimited, like Admin')
    parser.add_argument('--report', type=Path, required=True)
    args = parser.parse_args()
    parsed = cc.parse_llm_config_profiles(json.loads(args.config.read_text(encoding='utf-8')), 'http://127.0.0.1:11434', '')
    profiles = {p['id']: p for p in parsed['profiles']}
    records = json.loads(args.sources.read_text(encoding='utf-8'))
    if not isinstance(records, list) or len(source_sessions({'records': records}, 120)) < 2:
        parser.error('At least two distinct sessions containing substantive human requests are required')
    frozen = json.loads(args.frozen_task_bank.read_text(encoding='utf-8')) if args.frozen_task_bank else None
    if frozen is not None:
        tasks = frozen.get('tasks', [])
        if (len(tasks) < 2 or digest(tasks) != frozen.get('fingerprint')
                or {task.get('split') for task in tasks} != {'train', 'holdout'}
                or len({task.get('source_id') for task in tasks}) != len(tasks)
                or any(digest({k: v for k, v in task.items() if k != 'fingerprint'}) != task.get('fingerprint') for task in tasks)):
            parser.error('Frozen task bank fingerprint, task fingerprints or source-separated split is invalid')
    runtime_path = args.runtime_config or args.config.parent / '.clouds_coder_admin' / 'startup_config.json'
    runtime = json.loads(runtime_path.read_text(encoding='utf-8')) if runtime_path.is_file() else {}
    runtime = runtime.get('defaults', runtime.get('draft', runtime))
    rounds = max(cc.MIN_AGENT_ROUNDS, min(cc.MAX_AGENT_ROUNDS_CAP, int(runtime.get('max_rounds', cc.MAX_AGENT_ROUNDS))))
    seconds = max(1, int(runtime.get('max_run_seconds', runtime.get('run_timeout', cc.MAX_RUN_SECONDS))))
    report = {'transport': 'real configured remote services', 'source_count': len(records),
              'task_design': 'reused frozen real tasks' if frozen is not None else 'real model-generated tasks',
              'max_rounds': rounds, 'turn_max_tokens': int(runtime.get('max_output_tokens', cc.AGENT_MAX_OUTPUT_TOKENS)), 'round_limit_source': str(runtime_path) if runtime_path.is_file() else 'host default',
              'task_timeout_seconds': seconds, 'deployed': False, 'remote_calls': []}
    with tempfile.TemporaryDirectory(prefix='clouds-evolution-live-') as temp:
        app = cc.AppContext.__new__(cc.AppContext)
        app.global_profiles = profiles
        app.global_active_profile_id = args.generator
        app.codes_root = Path(temp) / 'Codes'
        app.crypto = cc.CryptoBox(app.codes_root)
        app.ide_auth = cc.IDEAuthStore(Path(temp) / 'ide.sqlite')
        token = 'live-acceptance-' + cc.secrets.token_hex(24)
        app.verify_admin_token = lambda candidate: candidate == token
        app.liquid_kernel = LiquidKernelControlPlane(
            Path(temp) / 'evolution', model_callback=app._liquid_kernel_model_call,
            judge_callback=app._liquid_kernel_judge_call,
            experience_provider=lambda *_: {'task_source_records': records},
            task_runtime_limits=lambda: {'max_rounds': rounds, 'max_run_seconds': seconds,
                                         'max_output_tokens': int(runtime.get('max_output_tokens', cc.AGENT_MAX_OUTPUT_TOKENS)),
                                         'context_token_limit': int(runtime.get('ctx_limit', runtime.get('context_token_limit', cc.DEFAULT_CONTEXT_TOKEN_LIMIT))),
                                         'max_run_tokens': int(runtime.get('max_run_tokens', 0) or 0)},
            model_resolver=lambda cfg: app._evolution_models().bind_run(cfg),
            config_validator=lambda cfg, **kwargs: app._evolution_models().validate_config(cfg, **kwargs),
        )
        plane = app.liquid_kernel
        initial = plane.registry.active_version()
        original_chat = cc.OllamaClient.chat

        def observed_chat(client, *positional, **kwargs):
            started = time.monotonic()
            result = original_chat(client, *positional, **kwargs)
            report['remote_calls'].append({'model': client.model, 'seconds': round(time.monotonic() - started, 2),
                                           'content_chars': len(result.get('content', '') or ''),
                                           'thinking_chars': len(result.get('thinking', '') or ''),
                                           'usage': client._usage_tokens(result)})
            print(json.dumps({'remote_call': len(report['remote_calls']), 'model': client.model}), flush=True)
            return result

        cc.OllamaClient.chat = observed_chat
        original_designer = control.build_task_bank
        if frozen is not None:
            control.build_task_bank = lambda *_args, **_kwargs: copy.deepcopy(frozen)
        server = cc.AgentHTTPServer(('127.0.0.1', 0), cc.Handler, app)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()

        def request(path, payload):
            conn = http.client.HTTPConnection('127.0.0.1', server.server_port, timeout=15)
            try:
                conn.request('POST', '/api/admin/evolution' + path, json.dumps(payload),
                             {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token})
                response = conn.getresponse()
                data = json.loads(response.read())
                if response.status >= 400:
                    raise RuntimeError(data.get('code', 'admin_request_failed'))
                return data
            finally:
                conn.close()

        try:
            refs = {role + '_model_ref': {'source': 'global', 'owner': '', 'profile_id': pid, 'model': profiles[pid]['model']}
                    for role, pid in [('generator', args.generator), ('judge', args.judge)]}
            cfg = request('/config', {'revision': plane.config()['revision'], 'values': {
                'mode': args.mode, 'schedule': 'off', 'deployment_policy': 'manual', **refs,
            }})['config']
            cfg = request('/config', {'revision': cfg['revision'], 'values': {
                'task_benchmark': {'max_tasks': 2, 'max_task_tokens': args.max_task_tokens,
                                   'control_reserve_percent': args.control_reserve_percent},
                'budget': {**cfg['budget'], 'candidate_limit': args.candidates,
                           'max_tokens': args.max_tokens, 'timeout_seconds': args.timeout},
            }})['config']
            report['models'] = {role: cfg[role + '_model_ref']['model'] for role in ('generator', 'judge')}
            run_id = request('/runs', {'revision': cfg['revision']})['run_id']
            report['run_id'] = run_id
            report['effective_config'] = {key: cfg[key] for key in ('budget', 'task_benchmark')}
            deadline = time.monotonic() + args.timeout + 10 if args.timeout else 0
            stage = ''
            while plane.active_run_id == run_id:
                detail = plane.registry.run_detail(run_id)
                if detail['status'] != stage:
                    stage = detail['status']
                    print(json.dumps({'stage': stage}), flush=True)
                if deadline and time.monotonic() > deadline:
                    plane.cancel(run_id)
                time.sleep(.25)
            detail = plane.registry.run_detail(run_id)
            result = detail.get('result') or {}
            report['score_summary'] = detail.get('score_summary') or {}
            report.update(status=detail['status'], error=detail.get('error', ''),
                          result_code=result.get('code'), error_details=result.get('details'), evaluated=result.get('evaluated'),
                          task_manifest=result.get('task_manifest'), scores=result.get('scores'),
                          model_call_count=len(report['remote_calls']))
            report['evaluations'] = [{key: row.get(key) for key in ('candidate_index', 'candidate_version', 'decision', 'code', 'reason', 'gain', 'measured_task_gain', 'incumbent', 'candidate', 'flow_comparison', 'confirmation')}
                                     for row in result.get('evaluations', [])]
            report['events'] = [{'kind': e['kind'], 'stage': e['payload'].get('stage')}
                                for e in detail['events'] if e['kind'].startswith('model_call_')]
            report['budget_events'] = [e['payload'] for e in detail['events'] if e['kind'] in {'task_budget_allocated', 'model_budget_consumed'}]
            report['reviews'] = [e['payload'] for e in detail['events'] if e['kind'] == 'independent_review_completed']
            report['compactions'] = [e['payload'] for e in detail['events'] if e['kind'] == 'task_context_compacted']
            report['candidate_version'] = detail.get('candidate_version', '')
            report['versions'] = plane.registry.list_versions()['versions']
            for version in report['versions']:
                if version.get('run_id') == run_id:
                    retained = plane.registry.version_detail(version['version'])
                    report.setdefault('retained_candidates', []).append(retained)
                    if args.evidence_dir:
                        args.evidence_dir.mkdir(parents=True, exist_ok=True)
                        (args.evidence_dir / (version['version'] + '.json')).write_text(json.dumps(retained, ensure_ascii=False, indent=2), encoding='utf-8')
            report['deployed'] = plane.registry.active_version() != initial or bool(plane.registry.active_state()['canary'])
            if report['deployed']:
                raise RuntimeError('acceptance unexpectedly changed deployment')
            evidence = plane.registry.experience_root / run_id
            bank_path, baseline_path = evidence / 'task_bank.json', evidence / 'incumbent_rollouts.json'
            bank = json.loads(bank_path.read_text(encoding='utf-8')) if bank_path.is_file() else {}
            baseline = json.loads(baseline_path.read_text(encoding='utf-8')) if baseline_path.is_file() else {}
            report['task_bank'] = {key: bank.get(key) for key in ('fingerprint', 'train_count', 'holdout_count', 'evaluator_protocol_version', 'evaluator_lineage')}
            report['baseline'] = {'score': baseline.get('score'), 'success_rate': baseline.get('success_rate'),
                                  'tasks': [{key: row.get(key) for key in ('task_id', 'split', 'score', 'success', 'rounds', 'tool_calls', 'error', 'budget', 'context', 'stop_reason', 'execution_backend')}
                                            for row in baseline.get('rows', [])]}
            report['judge_exercised'] = any(e['kind'] == 'model_call_completed' and e['stage'] == 'judge' for e in report['events'])
            report['passed'] = (detail.get('score_summary', {}).get('evaluation_valid') is not False and detail['status'] in {'no_change', 'rejected', 'awaiting_approval'}
                                and len(baseline.get('rows', [])) >= 2 and bool(bank.get('holdout_count')))
            report['acceptance_scope'] = 'harness_pipeline'
            report['pipeline_passed'] = report['passed']
            report['baseline_task_acceptance_passed'] = bool(baseline.get('rows')) and all(
                row.get('success') for row in baseline['rows'])
            report['measured_improvement'] = any(
                float(row.get('measured_task_gain') or 0) > 0 and bool((row.get('confirmation') or {}).get('passed')) for row in result.get('evaluations', []))

        except Exception as exc:
            report.update(passed=False, acceptance_error=str(exc) if isinstance(exc, cc.LiquidKernelError) else type(exc).__name__)
        finally:
            cc.OllamaClient.chat = original_chat
            control.build_task_bank = original_designer
            server.shutdown()
            server.server_close()
            thread.join(2)
            if args.evidence_dir and report.get('run_id'):
                source = plane.registry.experience_root / report['run_id']
                if source.is_dir():
                    shutil.copytree(source, args.evidence_dir, dirs_exist_ok=True)
                    args.evidence_dir.chmod(0o700)
                    report['protected_evidence'] = str(args.evidence_dir)
            args.report.parent.mkdir(parents=True, exist_ok=True)
            args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
            print(json.dumps({k: report.get(k) for k in ('status', 'models', 'max_rounds', 'model_call_count', 'deployed', 'passed')}, ensure_ascii=False), flush=True)
    return 0 if report.get('passed') else 1


if __name__ == '__main__':
    raise SystemExit(main())
