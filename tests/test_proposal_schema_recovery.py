"""Regression coverage for evo_70a4dbfad3ca4610a3df3ffb307fcf89."""
import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import Clouds_Coder as cc
from liquid_kernel import LiquidKernelControlPlane, LiquidKernelError
from liquid_kernel.agentic import AgenticBenchmark, compare_agentic_flows
from liquid_kernel.context import HistoryArchive, RECALL_TOOL, structured_packet_view
from liquid_kernel.control import BASELINE_KERNEL_FILES, normalize_proposal_output
from test_agentic_evolution import TaskModel, experiences, judge, wait


class ProposalSchemaTests(unittest.TestCase):
    def root(self):
        temp=tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        return Path(temp.name)

    def test_observed_nested_patch_reason_is_moved_without_changing_code(self):
        raw={'decision':'change','changelog':'bounded evidence','patch':{'decision':'change','reason':'Measured redundant reads',
             'files':[{'path':'context_policy.py','operation':'replace_file','content':'def f(): return "reason"'}]}}
        before=copy.deepcopy(raw)
        result=normalize_proposal_output(raw)
        self.assertEqual(result['reason'],raw['patch']['reason'])
        self.assertEqual(result['patch']['files'],raw['patch']['files'])
        self.assertEqual(raw,before)

    def test_wrappers_are_unwrapped_but_missing_or_conflicting_decisions_are_not_invented(self):
        valid={'decision':'no_change','reason':'No measured mechanism improvement'}
        self.assertEqual(normalize_proposal_output({'result':valid})['decision'],'no_change')
        for raw in ({'patch':{'files':[],'reason':'Reason without a decision'}},
                    {'decision':'change','reason':'a','patch':{'decision':'no_change'}},
                    {'decision':{},'reason':'reason'},
                    {'decision':'no_change','reason':'same','patch':{'files':[{'content':'a'}]}}):
            with self.subTest(raw=raw),self.assertRaises(LiquidKernelError):
                normalize_proposal_output(raw)

    def test_schema_repair_is_bounded_and_charged_to_normal_ledger(self):
        calls=[]
        def model(system,prompt,*args):
            calls.append(json.loads(prompt))
            return ({'patch':{},'reason':'Missing decision'} if len(calls)==1 else {'decision':'no_change','reason':'Insufficient improvement'})
        plane=LiquidKernelControlPlane(self.root(),model_callback=model)
        result=plane._call_proposal_model('Return a proposal',{'task':'improve'},'',4096)
        self.assertEqual(result['decision'],'no_change')
        self.assertEqual(len(calls),2)
        self.assertIn('validation_errors',calls[-1])
        self.assertGreater(plane._tokens_used,0)
        with mock.patch.object(plane,'model_callback',return_value={'reason':'still missing'}) as bad:
            with self.assertRaises(LiquidKernelError) as caught:
                plane._call_proposal_model('proposal',{'task':'improve'},'',4096)
        self.assertEqual(caught.exception.code,'invalid_proposal_schema')
        self.assertEqual(bad.call_count,3)

    def test_invalid_proposal_preserves_baseline_and_is_not_reported_as_no_change(self):
        base=TaskModel()
        def model(system,prompt,*args):
            payload=json.loads(prompt)
            if payload.get('task','').startswith(('Improve the executable','Repair the proposal JSON')):
                return {'reason':'No explicit decision'}
            return base(system,payload,*args)
        plane=LiquidKernelControlPlane(self.root(),model_callback=model,judge_callback=judge,experience_provider=lambda *_:experiences(2))
        cfg=plane.apply_startup_config('Thinking','off')['config']
        plane.save_config({'budget':{**cfg['budget'],'candidate_limit':1}},cfg['revision'])
        detail=wait(plane,plane.trigger()['run_id'],timeout=20)
        self.assertEqual(detail['status'],'rejected',detail)
        evaluation=detail['result']['evaluations'][0]
        self.assertEqual(detail['proposal']['candidates'][0]['generation_diagnostic']['code'],'invalid_proposal_schema')
        self.assertEqual(evaluation['candidate']['score_status'],'completed')
        self.assertTrue(evaluation['incumbent']['task_execution_measured'])
        self.assertTrue(detail['candidate_version'])
        self.assertTrue(evaluation['candidate']['task_execution_measured'])

    def test_structured_view_retains_metrics_and_schema_with_indexed_exact_fields(self):
        archive=HistoryArchive(self.root()/'packet.jsonl')
        body='head\n'+'full source\n'*2000+'tail'
        payload={'output_schema':{'decision':'change|no_change','reason':'top level'},
                 'kernel_files':{'context_policy.py':body},
                 'baseline_training_rollouts':[{'accounted_tokens':15619724,'rounds':200,'score':96,
                     'context':{'compactions':154},'trace':[{'name':'read_file','output':'data'*2000,'ok':i!=100} for i in range(200)],
                     'flow_contracts':[str(i)*64 for i in range(400)]}]}
        before=copy.deepcopy(payload)
        view=structured_packet_view(archive,payload)
        row=view['baseline_training_rollouts'][0]
        self.assertEqual(row['rounds'],200)
        self.assertEqual(row['accounted_tokens'],15619724)
        self.assertEqual(row['context']['compactions'],154)
        self.assertEqual(row['trace']['total_items'],200)
        self.assertTrue(any(item['index']==100 for item in row['trace']['sample']))
        self.assertEqual(view['output_schema'],payload['output_schema'])
        self.assertLess(len(json.dumps(view)),len(json.dumps(payload))/4)
        exact=archive.recall({'path':'kernel_files/context_policy.py','max_chars':32000,'line_count':200})
        self.assertTrue(exact['matches'])
        self.assertIn('full source',exact['matches'][0]['content'])
        self.assertEqual(payload,before)

    def test_minified_json_can_page_by_character_and_search_includes_the_match(self):
        archive=HistoryArchive(self.root()/'long.jsonl')
        text='a'*10000+'"compactions":154'+'b'*12000
        archive.record([{'role':'tool','path':'packet','content':text}])
        result=archive.recall({'path':'packet','query':'compactions','max_chars':1800})
        self.assertIn('compactions',result['matches'][0]['content'])
        window=archive.recall({'path':'packet','start_char':10000,'char_count':600,'max_chars':4000})['matches'][0]
        self.assertEqual(window['content'],text[10000:10600])
        following=archive.recall({'path':'packet','start_char':window['next_start_char'],'char_count':600,'max_chars':4000})['matches'][0]
        self.assertEqual(following['start_char'],10600)
        self.assertEqual(following['content'],text[10600:11200])
        self.assertIn('start_char',RECALL_TOOL['function']['parameters']['properties'])

    def test_ordinary_tool_schema_advertises_shared_character_pagination(self):
        descriptor=next(row for row in cc.TOOLS if row['function']['name']=='context_recall')
        self.assertIn('start_char',descriptor['function']['parameters']['properties'])
        self.assertIn('char_count',descriptor['function']['parameters']['properties'])

    def test_structured_driver_exposes_exact_field_index_without_repeated_global_scanning(self):
        app=cc.AppContext.__new__(cc.AppContext)
        app.liquid_kernel=LiquidKernelControlPlane(self.root())
        payload={'task':'propose','kernel_files':{'context_policy.py':'module source\n'*5000},
                 'baseline_training_rollouts':[{'rounds':200,'score':96,'trace':[{'output':'x'*10000} for _ in range(60)]}]}
        calls=[]
        def transport(system,prompt,*args):
            packet=json.loads(prompt)
            calls.append(packet)
            self.assertIn('_structured_evidence_index',packet['messages'][0]['content'])
            return {'decision':'no_change','reason':'No proven gain'}
        with mock.patch.object(app,'_liquid_kernel_transport_call',side_effect=transport):
            result=app._liquid_kernel_model_call('Return proposal JSON',json.dumps(payload),'',4096)
        self.assertEqual(result['decision'],'no_change')
        self.assertEqual(len(calls),1)

    def test_artifact_success_at_round_ceiling_is_not_a_completed_workflow(self):
        task={'id':'round-cap','split':'train','fingerprint':'round-cap','goal':'Write out.txt',
              'starter_files':{},'followups':[{'after_round':2,'content':'Ensure it is correct.'}],
              'checks':[{'kind':'contains','path':'out.txt','value':'ok'}],'minimum_tool_calls':3}
        def model(*args,**kwargs):return {'tool_calls':[{'name':'write_file','arguments':{'path':'out.txt','content':'ok'}}]}
        observed=AgenticBenchmark(model,lambda:None).run(BASELINE_KERNEL_FILES,[task],{'max_rounds':3,'max_tool_calls':10,'task_timeout_seconds':20,'turn_max_tokens':4096})
        row=observed['rows'][0]
        self.assertTrue(all(item['ok'] for item in row['checks']))
        self.assertFalse(row['success'])
        self.assertEqual(row['stop_reason'],'round_limit')
        self.assertFalse(compare_agentic_flows(observed,observed)['complete'])


if __name__=='__main__':
    unittest.main()
