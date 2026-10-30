"""Executable regressions from the 2026-10-28 screenshot audit."""

import ast
import copy
import json
import locale
import shlex
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import Clouds_Coder as cc
from liquid_kernel import LiquidKernelControlPlane
from liquid_kernel.agentic import AgenticBenchmark, KernelWorker, TaskWorkspace, compare_agentic_flows, digest
from liquid_kernel.context import HistoryArchive
from liquid_kernel.control import BASELINE_KERNEL_FILES, KernelBenchmark
from test_agentic_evolution import TaskModel, experiences, judge, wait


class ObservationModel(TaskModel):
    def __call__(self, system, prompt, profile=None, max_tokens=4096, **kwargs):
        payload = json.loads(prompt) if isinstance(prompt, str) else prompt
        if payload.get('task', '').startswith('Improve the executable'):
            return {'decision':'change', 'reason':'Propagate structured recovery context after tool results to preserve later user steering.',
                    'patch':{'files':[{'path':'kernel.py','operation':'replace_file',
                                      'content':BASELINE_KERNEL_FILES['kernel.py'] + '''
def after_tool_results(results, *, context=None):
    return [dict(row, recovery_policy=True) for row in results]
'''}]}}
        if 'messages' in payload:
            messages = payload['messages']
            round_index = 1+sum(row['role']=='assistant' for row in messages)
            if round_index==3 and any('"recovery_policy": true' in row.get('content','') for row in messages if row['role']=='tool'):
                return {'tool_calls':[{'name':'write_file','arguments':{'path':'result.txt','content':'revised output'}}]}
        return super().__call__(system,payload,profile,max_tokens,**kwargs)


class ScreenshotRegressionTests(unittest.TestCase):
    def root(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        return Path(temp.name)

    def test_worker_binary_protocol_ignores_forced_gbk_text_streams(self):
        original = subprocess.Popen

        def force_gbk(argv, *args, **kwargs):
            argv = list(argv)
            index = argv.index('-c')+1
            argv[index] = "import sys;sys.stdin.reconfigure(encoding='gbk',errors='surrogateescape');sys.stdout.reconfigure(encoding='gbk',errors='strict')\n" + argv[index]
            return original(argv, *args, **kwargs)

        value = {'name':'read_file','ok':True,'output':{'content':'任务 中文🔥 引号\'\"\n下一行', 'invalid':'\udcaa', 'pair':'\ud83d\udd25'}}
        with mock.patch('liquid_kernel.agentic.subprocess.Popen',side_effect=force_gbk):
            worker = KernelWorker(BASELINE_KERNEL_FILES)
        self.addCleanup(worker.close)
        result = worker.call('after_tool_results',{'results':[value],'context':{}},lambda:None)
        self.assertEqual(result[0]['output']['content'],value['output']['content'])
        self.assertEqual(result[0]['output']['pair'],'🔥')
        self.assertEqual(result[0]['output']['invalid'],'\udcaa')

    def test_shared_http_boundary_removes_actual_surrogates_after_json_decoding(self):
        client = cc.OllamaClient('http://unused.invalid','test')
        captured = []

        def inspect(request, **kwargs):
            captured.append(json.loads(request.data.decode('utf-8')))
            raise RuntimeError('request captured before networking')

        payload = {'messages':[{'role':'tool','content':'中文🔥\udcaa'},
                               {'role':'assistant','content':'\ud83d\udd25',
                                'tool_calls':[{'function':{'arguments':{'content':'\ud800','literal':'\\udcaa'}}}]}],
                   'nested':{'\udfff':['\udc91']}}
        before = copy.deepcopy(payload)
        for mode in ('json','stream','raw'):
            with self.subTest(mode=mode),mock.patch.object(cc,'urlopen',side_effect=inspect):
                with self.assertRaisesRegex(RuntimeError,'request captured'):
                    if mode=='stream':
                        list(client._iter_response_lines_url('http://unused.invalid',payload))
                    elif mode=='raw':
                        client._post_raw_url('http://unused.invalid',payload)
                    else:
                        client._post_json_url('http://unused.invalid',payload)
            decoded = captured[-1]
            # A tokenizer must be able to encode every string AFTER JSON.loads.
            json.dumps(decoded,ensure_ascii=False).encode('utf-8',errors='strict')
            self.assertEqual(decoded['messages'][0]['content'],'中文🔥\\udcaa')
            self.assertEqual(decoded['messages'][1]['content'],'🔥')
            self.assertEqual(decoded['messages'][1]['tool_calls'][0]['function']['arguments']['literal'],'\\udcaa')
        self.assertEqual(payload,before)
        archive = HistoryArchive(self.root()/'archive.jsonl')
        archive.record([{'role':'tool','content':'原始\udcaa'}])
        self.assertEqual(next(iter(HistoryArchive(archive.path).entries()))['row']['content'],'原始\udcaa')

    def test_contract_worker_reads_utf8_even_if_text_stdin_is_gbk(self):
        original=subprocess.run

        def force_gbk(argv,*args,**kwargs):
            argv=list(argv)
            index=argv.index('-c')+1
            argv[index]="import sys;sys.stdin.reconfigure(encoding='gbk',errors='surrogateescape')\n"+argv[index]
            return original(argv,*args,**kwargs)

        with mock.patch('liquid_kernel.control.subprocess.run',side_effect=force_gbk):
            outcome=KernelBenchmark.run_bundle(BASELINE_KERNEL_FILES,[{'id':'中文🔥\udcaa','goal':'任务与修订🔥'}])
        self.assertTrue(outcome['ok'],outcome)
        self.assertEqual(outcome['rows'][0]['id'],'中文🔥\udcaa')

    def test_package_text_io_always_has_an_explicit_encoding(self):
        root = Path(__file__).resolve().parents[1]/'liquid_kernel'
        violations=[]
        for path in root.glob('*.py'):
            for node in ast.walk(ast.parse(path.read_text(encoding='utf-8'))):
                if isinstance(node,ast.Call) and isinstance(node.func,ast.Attribute) and node.func.attr in {'read_text','write_text'}:
                    if not any(item.arg=='encoding' for item in node.keywords):
                        violations.append(f'{path.name}:{node.lineno}')
        self.assertEqual(violations,[])

    def test_bundle_sync_reads_and_writes_utf8_under_gbk_defaults(self):
        from tools.sync_liquid_kernel_bundle import sync
        target=self.root()/'standalone.py'
        target.write_text('title = "中文🔥"\n_EMBEDDED_LIQUID_KERNEL_PACKAGE_B64 = (\n    "old"\n)\n',encoding='utf-8')
        original_read,original_write=Path.read_text,Path.write_text
        seen=[]

        def read(path,*args,**kwargs):
            if path==target:
                seen.append(('read',kwargs.get('encoding')))
                if not kwargs.get('encoding'):
                    return path.read_bytes().decode('cp936')
            return original_read(path,*args,**kwargs)

        def write(path,text,*args,**kwargs):
            if path==target:
                seen.append(('write',kwargs.get('encoding')))
                if not kwargs.get('encoding'):
                    text.encode('cp936')
            return original_write(path,text,*args,**kwargs)

        with mock.patch.object(Path,'read_text',new=read),mock.patch.object(Path,'write_text',new=write):
            sync([str(target)])
        self.assertEqual(seen,[('read','utf-8'),('write','utf-8')])
        self.assertIn('中文🔥',target.read_text(encoding='utf-8'))
        ast.parse(target.read_text(encoding='utf-8'))

    def test_windows_safe_python_assertions_never_launch_cmd_or_host_python(self):
        root = self.root()
        source = '''import json
from pathlib import Path
value = {"说明":"中文🔥", "quote":"it's a \\"quoted\\" value"}
Path("中文结果.json").write_text(json.dumps(value, ensure_ascii=False))
actual = json.loads(Path("中文结果.json").read_text())
assert actual["说明"] == "中文🔥"
assert "quoted" in actual["quote"]
print("通过🔥")
'''
        with mock.patch('liquid_kernel.agentic.sys.platform','win32'),mock.patch.object(locale,'getpreferredencoding',return_value='cp936'),mock.patch('liquid_kernel.agentic.subprocess.Popen') as launch:
            workspace=TaskWorkspace(root,lambda:None)
            success=workspace.command('python3 -c '+shlex.quote(source))
            failed=workspace.command('python3 -c '+shlex.quote("assert False, '中文失败🔥'"))
            ordinary=workspace.command('cat '+shlex.quote('中文结果.json'))
            launch.assert_not_called()
        self.assertEqual(success['exit_code'],0,success)
        self.assertIn('通过🔥',success['output'])
        self.assertEqual(failed['exit_code'],1,failed)
        self.assertIn('AssertionError',failed['output'])
        self.assertEqual(ordinary['exit_code'],0,ordinary)
        self.assertEqual(json.loads(ordinary['output'])['说明'],'中文🔥')

    def plane(self,model):
        plane=LiquidKernelControlPlane(self.root(),model_callback=model,judge_callback=judge,experience_provider=lambda *_:experiences(2))
        cfg=plane.apply_startup_config('Thinking','off')['config']
        plane.save_config({'deployment_policy':'manual','budget':{**cfg['budget'],'candidate_limit':1,'max_tokens':0}},cfg['revision'])
        return plane

    def test_after_tool_results_change_reaches_independent_paired_confirmation(self):
        plane=self.plane(ObservationModel())
        incumbent=plane.registry.active_version()
        original=Path.read_text
        reads=[]

        def cp936_default(path,*args,**kwargs):
            if path.name=='task_bank.json':
                reads.append(kwargs.get('encoding'))
                if not args and not kwargs.get('encoding'):
                    return path.read_bytes().decode('cp936')
            return original(path,*args,**kwargs)

        with mock.patch.object(Path,'read_text',new=cp936_default):
            detail=wait(plane,plane.trigger()['run_id'],timeout=25)
        self.assertEqual(detail['status'],'awaiting_approval',detail)
        self.assertTrue(reads)
        self.assertTrue(all(encoding=='utf-8' for encoding in reads))
        result=detail['result']
        self.assertTrue(result['flow_comparison']['flow_changed'])
        self.assertTrue(result['confirmation']['completed'])
        self.assertTrue(result['confirmation']['passed'])
        self.assertEqual(plane.registry.active_version(),incumbent)
        observed=json.loads((plane.registry.experience_root/detail['run_id']/'candidate_1_rollouts.json').read_text(encoding='utf-8'))
        self.assertTrue(all(row['flow_signature_version']==3 for row in observed['rows']))
        self.assertTrue(all({change['hook'] for change in row['flow_changes']}=={'after_tool_results'} for row in observed['rows']))

    def test_random_tool_content_and_comments_do_not_prove_architecture_change(self):
        task={'id':'observed-content-control','split':'train','goal':'Write and read out.txt.','starter_files':{},
              'followups':[{'after_round':2,'content':'Read the output and finish.'}],
              'checks':[{'kind':'contains','path':'out.txt','value':'nonce'}],'minimum_tool_calls':3}
        task['fingerprint']=digest(task)
        cfg={'max_rounds':5,'task_timeout_seconds':30,'max_tool_calls':10,'turn_max_tokens':4096}

        def run(files,text):
            def model(system,payload,*args,**kwargs):
                round_index=1+sum(row['role']=='assistant' for row in payload['messages'])
                if round_index==1:
                    return {'tool_calls':[{'name':'write_file','arguments':{'path':'out.txt','content':text}}]}
                if round_index==2:
                    return {'tool_calls':[{'name':'read_file','arguments':{'path':'out.txt'}}]}
                return {'tool_calls':[{'name':'finish_task','arguments':{}}],'final':'done'}
            return AgenticBenchmark(model,lambda:None,reference_files=BASELINE_KERNEL_FILES).run(files,[task],cfg)

        baseline=run(BASELINE_KERNEL_FILES,'nonce-one')
        unchanged=copy.deepcopy(BASELINE_KERNEL_FILES)
        unchanged['kernel.py']+='\n# Comment-only edit cannot count as a changed agent flow.\n'
        candidate=run(unchanged,'nonce-two')
        self.assertTrue(baseline['rows'][0]['success'])
        self.assertTrue(candidate['rows'][0]['success'])
        self.assertNotEqual(baseline['rows'][0]['flow_contracts'],candidate['rows'][0]['flow_contracts'])
        comparison=compare_agentic_flows(baseline,candidate)
        self.assertFalse(comparison['flow_changed'])
        self.assertFalse(comparison['eligible'])

        # A hook can return an extra, unconsumed observation. It has no effect
        # on the actual tool messages and must not qualify as a changed flow.
        unused=copy.deepcopy(BASELINE_KERNEL_FILES)
        unused['kernel.py']+='''
def after_tool_results(results, *, context=None):
    return list(results) + [{"name":"not_a_called_tool","output":"unused"}]
'''
        ignored=run(unused,'nonce-three')
        self.assertFalse(compare_agentic_flows(baseline,ignored)['flow_changed'])
        self.assertEqual(ignored['rows'][0]['flow_changes'],[])

    def test_after_only_change_still_requires_successful_independent_rerun(self):
        plane=self.plane(ObservationModel())
        incumbent=plane.registry.active_version()
        original=AgenticBenchmark.run

        def fail_confirmation(benchmark,files,tasks,cfg,arm='kernel'):
            result=original(benchmark,files,tasks,cfg,arm)
            if arm=='candidate_1_confirmation':
                result['rows'][0].update(success=False,score=0)
                result.update(score=0,success_rate=0)
            return result

        with mock.patch.object(AgenticBenchmark,'run',new=fail_confirmation):
            detail=wait(plane,plane.trigger()['run_id'],timeout=25)
        self.assertEqual(detail['status'],'rejected',detail)
        evaluation=detail['result']['evaluations'][0]
        self.assertTrue(evaluation['flow_comparison']['flow_changed'])
        self.assertTrue(evaluation['confirmation']['completed'])
        self.assertFalse(evaluation['confirmation']['passed'])
        self.assertEqual(plane.registry.active_version(),incumbent)
        self.assertTrue(detail['candidate_version'])
        self.assertFalse(plane.registry.version_detail(detail['candidate_version'])['evaluation']['deployment_eligible'])


if __name__=='__main__':
    unittest.main()
