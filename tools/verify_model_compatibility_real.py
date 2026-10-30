"""Exercise every configured model with real JSON, native tools, and blind scoring.

Uses a declared, self-contained compatibility task and actual workspace tools.
It does not claim to replay a historical user session or measure a kernel gain.
"""
import argparse
import json
import shlex
import sys
import tempfile
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import Clouds_Coder as cc  # noqa: E402
from liquid_kernel import (  # noqa: E402
    LiquidKernelControlPlane,
    normalize_evolution_config,
)
from liquid_kernel.agentic import AgenticBenchmark, digest  # noqa: E402
from liquid_kernel.control import BASELINE_KERNEL_FILES  # noqa: E402


def compatibility_task():
    rows = [{'id': 't1', 'content': '读取输入', 'status': 'in_progress'},
            {'id': 't2', 'content': '生成 summary.txt', 'status': 'pending'},
            {'id': 't3', 'content': '修复 TodoWrite 工具解析', 'status': 'pending'},
            'developer', 'TodoWrite', 'chatcmpl-tool-8ed64aafdc82ef', 'dd2c83ff58af5331', '〇']
    revisions = [{'id': 't1', 'status': 'completed'},
                 {'id': 't2', 'content': '生成 summary.json', 'status': 'in_progress'}]
    expected = [{'id': 't1', 'content': '读取输入', 'status': 'completed'},
                {'id': 't2', 'content': '生成 summary.json', 'status': 'in_progress'}, rows[2]]
    assertion = ('import json; from normalize import normalize; '
                 "rows=json.load(open('incoming.json'))['todos']; changes=json.load(open('revisions.json')); "
                 'expected=' + repr(expected) + '; '
                 "assert json.load(open('final.json'))==expected; assert normalize(rows,changes)==expected; "
                 "assert [r['id'] for r in normalize(rows)]==['t1','t2','t3']; "
                 "assert normalize(['tool','assistant','chatcmpl-tool-abcd','a'*32])==[]")
    task = {'id': 'compatibility-todo-revision', 'source_id': 'declared-public-compatibility-task', 'split': 'train',
            'family': 'real Python tool protocol and late task revision',
            'goal': ('Read incoming.json and implement normalize.py with normalize(rows, revisions=None). '
                     'Valid rows are task objects with id, content and status. Discard transport metadata strings and preserve legitimate task prose mentioning tools. '
                     'Return a list of objects containing exactly id/content/status, preserving IDs and input order. Apply partial revisions by id in place, preserving unspecified fields. '
                     'Initially write result.json from incoming.json using this function. Execute meaningful Python checks before finishing.'),
            'starter_files': {'incoming.json': json.dumps({'todos': rows}, ensure_ascii=False),
                              'revisions.json': json.dumps(revisions, ensure_ascii=False)},
            'followups': [{'after_round': 3, 'content': 'Now apply revisions.json to the original rows. Write the revised result to final.json, keep all three task IDs, and verify both the module and actual JSON output by executing Python.'}],
            'checks': [{'kind': 'file_exists', 'path': 'normalize.py'},
                       {'kind': 'json_equals', 'path': 'final.json', 'value': expected},
                       {'kind': 'command', 'command': 'python3 -c ' + shlex.quote(assertion), 'exit_code': 0}],
            'minimum_tool_calls': 3, 'rubric': ['Real files, correct stable-ID updates and a later user revision']}
    task['fingerprint'] = digest(task)
    return task


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', type=Path, required=True)
    parser.add_argument('--report', type=Path, required=True)
    parser.add_argument('--profiles', help='Optional comma-separated profile IDs for a failed-case rerun; default tests all')
    parser.add_argument('--trace-dir', type=Path, help='Optional private directory for public-task request/response diagnostics')
    parser.add_argument('--max-tokens', type=int, default=120000, help='Per-model total input/output quota, including independent review')
    args = parser.parse_args()
    parsed = cc.parse_llm_config_profiles(json.loads(args.config.read_text()), 'http://127.0.0.1:11434', '')
    profiles = {p['id']: p for p in parsed['profiles']}
    targets = [(pid, model) for pid, p in profiles.items() for model in dict.fromkeys([p.get('model'), *(p.get('models') or [])]) if model]
    if args.profiles:
        selected = set(args.profiles.split(','))
        if selected - set(profiles):
            parser.error('Unknown requested profile')
        targets = [target for target in targets if target[0] in selected]
    if args.trace_dir:
        args.trace_dir.mkdir(parents=True, exist_ok=True, mode=0o700)
    runtime_file = args.config.parent / '.clouds_coder_admin' / 'startup_config.json'
    runtime = json.loads(runtime_file.read_text()) if runtime_file.is_file() else {}
    runtime = runtime.get('defaults', runtime.get('draft', runtime))
    rounds = max(cc.MIN_AGENT_ROUNDS, min(cc.MAX_AGENT_ROUNDS_CAP, int(runtime.get('max_rounds', cc.MAX_AGENT_ROUNDS))))
    task = compatibility_task()
    local = threading.local()
    original_chat = cc.OllamaClient.chat
    lock = threading.Lock()
    calls = {}

    def observe(client, *positional, **kwargs):
        started = time.monotonic()
        response = original_chat(client, *positional, **kwargs)
        with lock:
            label = local.label
            calls[label].append({'model': client.model, 'seconds': round(time.monotonic() - started, 2),
                                 'native_tools_offered': bool(kwargs.get('tools')),
                                 'thinking_chars': len(response.get('thinking') or ''),
                                 'content_chars': len(response.get('content') or ''),
                                 'effort': kwargs.get('effort', ''),
                                 'reasoning_history_messages': sum(bool(row.get('reasoning_content') or row.get('thinking')) for row in (positional[0] if positional else kwargs.get('messages', []))),
                                 'native_tool_calls': len(response.get('tool_calls') or []),
                                 'action_names': [c.get('function', {}).get('name') for c in response.get('tool_calls', [])],
                                 'usage': client._usage_tokens(response)})
            if args.trace_dir:
                trace = args.trace_dir / (label.replace('/', '_') + '-' + str(len(calls[label])) + '.json')
                trace.write_text(json.dumps({'messages': positional[0] if positional else kwargs.get('messages'),
                                             'system': kwargs.get('system'), 'response': response}, ensure_ascii=False, indent=2))
                trace.chmod(0o600)
            print(json.dumps({'target': label, 'remote_call': len(calls[label]), 'actions': calls[label][-1]['action_names']}), flush=True)
        return response

    def verify(target):
        pid, model = target
        label = pid + '/' + model
        local.label = label
        calls[label] = []
        row = {'profile': pid, 'model': model, 'max_rounds': rounds, 'json': False, 'task': False, 'judge': False}
        started = time.monotonic()
        with tempfile.TemporaryDirectory(prefix='clouds-model-compat-') as temp:
            app = cc.AppContext.__new__(cc.AppContext)
            app.global_profiles = profiles
            app.global_active_profile_id = pid
            app.codes_root = Path(temp) / 'Codes'
            app.crypto = cc.CryptoBox(app.codes_root)
            app.ide_auth = cc.IDEAuthStore(Path(temp) / 'ide.sqlite')
            app.liquid_kernel = plane = LiquidKernelControlPlane(Path(temp) / 'kernel',
                model_callback=app._liquid_kernel_model_call, judge_callback=app._liquid_kernel_judge_call)
            plane._active_deadline = time.monotonic() + 1200
            plane._token_limit, plane._tokens_used = max(0, args.max_tokens), 0
            ref = {'source': 'global', 'owner': '', 'profile_id': pid, 'model': model}
            try:
                result = plane._call_model('Return a JSON object only.', 'Return {"status":"ok","说明":"中文兼容"}.', ref, 1024)
                row['json'] = result.get('status') == 'ok' and result.get('说明') == '中文兼容'
                cfg = normalize_evolution_config({'mode': 'Thinking'})
                cfg.update(generator_model_ref=ref, judge_model_ref=ref)
                cfg['task_benchmark'].update(max_rounds=rounds, max_tool_calls=rounds * 8,
                                             task_timeout_seconds=int(runtime.get('max_run_seconds', runtime.get('run_timeout', cc.MAX_RUN_SECONDS))), turn_max_tokens=int(runtime.get('max_output_tokens', cc.AGENT_MAX_OUTPUT_TOKENS)))

                def call_model(system, payload, tokens=4096, *, deadline=None):
                    plane._call_deadline = min(plane._active_deadline, deadline or plane._active_deadline)
                    try:
                        return plane._call_model(system, json.dumps(payload, ensure_ascii=False), ref, tokens)
                    finally:
                        plane._call_deadline = 0

                observed = AgenticBenchmark(call_model, lambda: plane._check_cancel('')).run(BASELINE_KERNEL_FILES, [task], cfg['task_benchmark'])
                outcome = observed['rows'][0]
                row['task'] = outcome['success']
                row['outcome'] = {key: outcome[key] for key in ('score', 'success', 'rounds', 'tool_calls', 'checks', 'error')}
                row['user_followups'] = sum(t.get('event') == 'user_followup' for t in outcome['trace'])
                # Identical observed trajectories explicitly test scoring format;
                # this is not an invented candidate or a claimed improvement.
                scoring = plane._soft_score(BASELINE_KERNEL_FILES, BASELINE_KERNEL_FILES, [task], cfg,
                                             observations={'incumbent': observed, 'candidate': observed})
                row['judge'] = all(isinstance(scoring.get(k), (int, float)) for k in ('incumbent', 'candidate'))
                row['judge_scores_identical_control'] = {k: scoring[k] for k in ('incumbent', 'candidate')}
            except Exception as exc:
                row['error'] = {'code': getattr(exc, 'code', type(exc).__name__), 'message': str(exc), 'details': getattr(exc, 'details', {})}
        row.update(passed=all(row[k] for k in ('json', 'task', 'judge')), seconds=round(time.monotonic() - started, 2),
                   remote_calls=calls[label], native_tool_calls=sum(c['native_tool_calls'] for c in calls[label]))
        checkpoint = args.report.with_name(args.report.stem + '-' + pid + '.json')
        checkpoint.parent.mkdir(parents=True, exist_ok=True)
        checkpoint.write_text(json.dumps(row, ensure_ascii=False, indent=2) + '\n')
        print(json.dumps({'complete': label, 'passed': row['passed'], 'error': row.get('error')}), flush=True)
        return row

    cc.OllamaClient.chat = observe
    try:
        with ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(verify, targets))
    finally:
        cc.OllamaClient.chat = original_chat
    report = {'scope': 'all explicitly configured profile/model combinations', 'target_count': len(targets),
              'transport': 'real configured remote services; real file and command tools',
              'task_source': 'declared public compatibility task, not historical session acceptance',
              'task_fingerprint': task['fingerprint'], 'max_rounds': rounds, 'per_model_max_tokens': max(0, args.max_tokens), 'results': results,
              'passed': all(row['passed'] for row in results)}
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'passed': report['passed'], 'target_count': len(targets)}), flush=True)
    return 0 if report['passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
