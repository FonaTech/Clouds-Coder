"""Replay independent review on unchanged real rollouts; never execute or deploy tasks."""
import argparse
import json
import sys
import tempfile
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import Clouds_Coder as cc  # noqa: E402
from liquid_kernel import LiquidKernelControlPlane, normalize_evolution_config  # noqa: E402
from liquid_kernel.agentic import digest  # noqa: E402
from liquid_kernel.control import BASELINE_KERNEL_FILES  # noqa: E402


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', type=Path, required=True)
    parser.add_argument('--profile', required=True)
    parser.add_argument('--evidence', type=Path, required=True)
    parser.add_argument('--run-report', type=Path, required=True)
    parser.add_argument('--report', type=Path, required=True)
    args = parser.parse_args()
    source = json.loads(args.run_report.read_text())
    bank = json.loads((args.evidence / 'task_bank.json').read_text())
    assert digest(bank['tasks']) == bank['fingerprint']
    observations = {label: json.loads((args.evidence / name).read_text()) for label, name in
                    [('incumbent', 'incumbent_rollouts.json'), ('candidate', 'candidate_1_rollouts.json')]}
    profiles = {p['id']: p for p in cc.parse_llm_config_profiles(json.loads(args.config.read_text()), 'http://127.0.0.1:11434', '')['profiles']}
    calls = []
    report = {'scope': 'independent review replay of unchanged real rollout artifacts', 'task_reexecuted': False,
              'deployed': False, 'origin_run': source['run_id'], 'task_bank_fingerprint': bank['fingerprint'],
              'model': profiles[args.profile]['model']}
    with tempfile.TemporaryDirectory(prefix='clouds-frozen-review-') as temp:
        app = cc.AppContext.__new__(cc.AppContext)
        app.global_profiles, app.global_active_profile_id = profiles, args.profile
        app.codes_root = Path(temp) / 'Codes'
        app.crypto = cc.CryptoBox(app.codes_root)
        app.ide_auth = cc.IDEAuthStore(Path(temp) / 'ide.sqlite')
        app.liquid_kernel = plane = LiquidKernelControlPlane(Path(temp) / 'kernel',
            model_callback=app._liquid_kernel_model_call, judge_callback=app._liquid_kernel_judge_call)
        ref = {'source': 'global', 'owner': '', 'profile_id': args.profile, 'model': profiles[args.profile]['model']}
        cfg = normalize_evolution_config({'mode': 'Thinking', 'deployment_policy': 'manual', 'judge_model_ref': ref,
                                          'task_benchmark': source['effective_config']['task_benchmark']})
        plane._active_run_config = cfg
        plane._active_deadline = time.monotonic() + 1200
        plane._token_limit, plane._tokens_used = 0, 0
        original = cc.OllamaClient.chat

        def observe(client, *positional, **kwargs):
            result = original(client, *positional, **kwargs)
            calls.append({'tool_calls': len(result.get('tool_calls') or []), 'usage': client._usage_tokens(result)})
            print(json.dumps({'real_review_call': len(calls)}), flush=True)
            return result

        cc.OllamaClient.chat = observe
        try:
            scores = plane._soft_score(BASELINE_KERNEL_FILES, BASELINE_KERNEL_FILES, bank['tasks'], cfg, observations=observations)
            archives = list(plane.registry.experience_root.glob('standalone-review/review-*/full_history.jsonl'))
            report.update(passed=True, scores={k: scores[k] for k in ('incumbent', 'candidate')},
                          host_evidence_deliveries=sum('"scope":"review_host_recall"' in line.replace(' ', '') for p in archives for line in p.read_text().splitlines()))
        except Exception as exc:
            report.update(passed=False, error_code=getattr(exc, 'code', type(exc).__name__))
        finally:
            cc.OllamaClient.chat = original
            report.update(model_call_count=len(calls), calls=calls, tokens_used=plane._tokens_used)
            args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
            print(json.dumps({k: report.get(k) for k in ('passed', 'scores', 'model_call_count', 'host_evidence_deliveries')}, ensure_ascii=False))
    return 0 if report.get('passed') else 1


if __name__ == '__main__':
    raise SystemExit(main())
