"""Use every configured model as the real semantic JSON converter on public damaged responses.

Includes genuine transport calls and an explicitly marked two-response fault
injection to exercise the complete fallback path. No historical sessions sent.
"""
import argparse
import json
import sys
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from unittest import mock

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import Clouds_Coder as cc  # noqa: E402
from liquid_kernel import LiquidKernelControlPlane  # noqa: E402


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', type=Path,required=True)
    parser.add_argument('--report', type=Path,required=True)
    parser.add_argument('--workers',type=int,default=3)
    parser.add_argument('--profiles')
    parser.add_argument('--final-envelope', action='store_true',help='Inject malformed final strings inside native review envelopes.')
    args=parser.parse_args()
    raw=json.loads(args.config.read_text())
    profiles=[p for p in cc.parse_llm_config_profiles(raw,'http://127.0.0.1:11434','')['profiles'] if p.get('model')]
    if args.profiles:
        selected=set(args.profiles.split(','))
        profiles=[p for p in profiles if p['id'] in selected]
    def verify(profile):
        report={'profile':profile['id'],'model':profile['model'],'private_history_sent':False,'cases':[]}
        with tempfile.TemporaryDirectory(prefix='clouds-json-real-') as directory:
            app=cc.AppContext.__new__(cc.AppContext)
            app.global_profiles={profile['id']:profile}
            app.global_active_profile_id=profile['id']
            app.liquid_kernel=plane=LiquidKernelControlPlane(Path(directory)/'kernel')
            plane._token_limit,plane._tokens_used=80000,0
            plane._active_deadline=time.monotonic()+900
            ref={'source':'global','owner':'','profile_id':profile['id'],'model':profile['model']}
            cases=[('semantic_alias_mapping','Return score_a, score_b (numbers), rationale (string).',
                    "Evaluation result: scoreA=97; scoreB=97; rationale='Equivalent observed evidence.'",False),
                   ('truncated_file_must_decline','Return path and the exact complete file content. Missing contents cannot be inferred.',
                    '{"path":"long.html","content":"<html>prefix [OUTPUT TRUNCATED]',True)]
            for name,contract,damaged,decline in cases:
                row={'case':name,'real_transport':True}
                started=time.monotonic()
                try:
                    system,messages=cc.semantic_json_repair_request(contract,damaged,'malformed_public_fixture')
                    result=app._liquid_kernel_transport_call(system,messages[0]['content'],ref,1536)
                    usage=result.pop('_evolution_usage',{})
                    plane._record_model_tokens('',{'_evolution_usage':usage})
                    if decline:
                        assert result.get('repair_status')=='unrecoverable', 'truncated source was not refused'
                    else:
                        result=cc.validate_semantic_json_repair(json.dumps(result),damaged)
                        assert result.get('score_a')==97 and result.get('score_b')==97, 'score mapping changed'
                        assert result.get('rationale')=='Equivalent observed evidence.', 'rationale changed'
                    row.update(passed=True,result=result,tokens=usage.get('total_tokens'))
                except Exception as exc:
                    row.update(passed=False,error=type(exc).__name__+': '+str(exc)[:600])
                row['seconds']=round(time.monotonic()-started,2)
                report['cases'].append(row)
                print(json.dumps({'profile':profile['id'],**row},ensure_ascii=False),flush=True)
            report['passed']=all(c['passed'] for c in report['cases'])
        return report
    with ThreadPoolExecutor(max_workers=max(1,min(args.workers,5))) as pool:
        results=list(pool.map(verify,profiles))
    # One end-to-end fallback per target, sequentially to isolate fault injection.
    for report,profile in zip(results,profiles):
        with tempfile.TemporaryDirectory(prefix='clouds-json-fallback-') as directory:
            app=cc.AppContext.__new__(cc.AppContext)
            app.global_profiles={profile['id']:profile}
            app.global_active_profile_id=profile['id']
            app.liquid_kernel=LiquidKernelControlPlane(Path(directory)/'kernel')
            app.liquid_kernel._token_limit=40000
            app.liquid_kernel._active_deadline=time.monotonic()+300
            original=cc.OllamaClient.chat
            calls=[]
            def inject(client,*positional,**kwargs):
                calls.append(kwargs.get('label'))
                if len(calls)<3:
                    damaged="scoreA=97; scoreB=97; rationale='Equivalent observed evidence.'"
                    return {'content':json.dumps({'final':damaged}) if args.final_envelope else damaged,'tool_calls':[],'raw':{'done_reason':'stop'}}
                return original(client,*positional,**kwargs)
            row={'case':'transport_three_stage_fallback','injected_responses':2,'real_semantic_calls':1,'final_envelope':args.final_envelope}
            try:
                with mock.patch.object(cc.OllamaClient,'chat',new=inject):
                    request='Frozen observed scores: A=97, B=97. Rationale: Equivalent observed evidence.'
                    if args.final_envelope:
                        from liquid_kernel.context import RECALL_TOOL
                        request=json.dumps({'messages':[{'role':'user','content':request}], 'tools':[RECALL_TOOL], 'require_json_final':True})
                    result=app._liquid_kernel_transport_call('Return JSON score_a, score_b, rationale from the supplied evidence.',request,profile['id'],1536)
                assert result['score_a']==result['score_b']==97 and len(calls)==3
                row.update(passed=True,request_labels=calls)
            except Exception as exc:
                row.update(passed=False,error=type(exc).__name__+': '+str(exc)[:600])
            report['cases'].append(row)
            report['passed']=report['passed'] and row['passed']
            print(json.dumps({'profile':profile['id'],**row},ensure_ascii=False),flush=True)
    output={'passed':bool(results) and all(r['passed'] for r in results),'source':'declared public malformed JSON fixtures',
            'models':results,'private_history_sent':False}
    args.report.write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n')
    return 0 if output['passed'] else 1


if __name__=='__main__':
    raise SystemExit(main())
