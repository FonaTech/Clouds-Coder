"""The split runtime must work without reading the original monolith."""
import ast
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import split_coder as splitter

ROOT = Path(__file__).resolve().parents[1]


class SplitDistributionTests(unittest.TestCase):
    def node(self, name, kind='function'):
        return splitter.NodeInfo(order=0, name=name, kind=kind, lineno=1, end_lineno=1,
                                 source_start=1, source_end=1)

    def test_current_runtime_has_no_unclassified_statements(self):
        analyzer = splitter.ArchitectureAnalyzer(ROOT/'Clouds_Coder.py')
        nodes = analyzer.analyze()
        splitter.ModuleRouter(splitter.DEFAULT_LAYOUT).assign_all(nodes)
        remaining = [node.name for node in nodes if node.target_module == '_unclassified.py']
        self.assertEqual(remaining, [], 'Add explicit subsystem ownership for new runtime declarations')
        self.assertEqual(len(nodes), len({node.order for node in nodes}))
        owners = {node.name: node.target_module for node in nodes}
        for name, module in {
            '_READ_DISPATCH_CONTEXT': 'agent/context.py',
            'EvidenceRetrievalController': 'agent/evidence.py',
            '_TOOL_CANCEL_LOCAL': 'agent/process.py',
            '_IDE_TOOLCHAIN_CACHE': 'ide/toolchains.py',
            '_TODO_SHORT_ID_RE': 'utils/text.py',
            'SessionLLMGate': 'llm/gate.py',
            'TodoLLMBudgetExhausted': 'llm/gate.py',
            '_start_offline_js_warmup': 'utils/files.py',
            'validate_semantic_json_repair': 'utils/json_utils.py',
            'sync_embedded_liquid_kernel_bundle': 'config/bootstrap.py',
        }.items():
            with self.subTest(name=name):self.assertEqual(owners[name], module)

    def test_runtime_family_ownership_matches_default_and_auto_layout(self):
        router = splitter.ModuleRouter(splitter.DEFAULT_LAYOUT)
        auto = splitter.AutoLayoutGenerator()
        for name, kind, owner in [
            ('_IDE_TOOLCHAIN_FUTURE_CACHE', 'assignment', 'ide/toolchains.py'),
            ('SESSION_LLM_CONCURRENCY_FUTURE', 'constant', 'llm/gate.py'),
            ('_TODO_LLM_FUTURE_LOCAL', 'assignment', 'llm/gate.py'),
            ('_skill_recall_future', 'function', 'skills/store.py'),
            ('_TODO_SHORT_ID_FUTURE_RE', 'assignment', 'utils/text.py'),
            ('TodoLLMBudgetExhausted', 'class', 'llm/gate.py'),
        ]:
            with self.subTest(name=name):
                node = self.node(name, kind)
                self.assertEqual(router.route(node), owner)
                self.assertEqual(auto._classify(node), owner)

    def test_unknown_functions_are_reported_instead_of_hidden(self):
        node = self.node('brand_new_unmapped_feature')
        splitter.ModuleRouter(splitter.DEFAULT_LAYOUT).assign_all([node])
        self.assertEqual(node.target_module, '_unclassified.py')

    def test_both_maintained_splitter_locations_are_identical(self):
        self.assertEqual((ROOT/'split_coder.py').read_bytes(), (ROOT/'Split Tools/split_coder.py').read_bytes())

    def test_unicode_bom_ordered_initialization_and_standalone_import(self):
        with tempfile.TemporaryDirectory(prefix='split-中文-') as temp:
            root = Path(temp)
            source = root/'Clouds_Coder.py'
            code = '''from __future__ import annotations
import argparse
VALUES = ["中文🔥"]
for i in range(3):
    VALUES.append(i)
class AppContext:
    @staticmethod
    def source_bundle():
        return b"source"
def main():
    parser=argparse.ArgumentParser()
    parser.parse_args()
if __name__ == "__main__":
    main()
'''
            source.write_text(code, encoding='utf-8-sig')
            output = root/'unicode_split'
            result = subprocess.run([sys.executable,str(ROOT/'split_coder.py'),str(source),'-o',str(output),'--self-check'],
                capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=120,
                env={**os.environ,'PYTHONUTF8':'1','PYTHONIOENCODING':'utf-8'})
            self.assertEqual(result.returncode,0,result.stdout+result.stderr)
            source.unlink()
            script = "import unicode_split._runtime as r; assert r.bootstrap()['VALUES']==['中文🔥',0,1,2]; print('independent')"
            result = subprocess.run([sys.executable,'-c',script],cwd=root,capture_output=True,text=True,
                encoding='utf-8',errors='replace',timeout=60,env={**os.environ,'PYTHONUTF8':'1'})
            self.assertEqual(result.returncode,0,result.stdout+result.stderr)
            self.assertIn('independent',result.stdout)

    def test_capture_subprocess_boundaries_are_explicit_utf8(self):
        tree=ast.parse((ROOT/'split_coder.py').read_text(encoding='utf-8'))
        calls=[node for node in ast.walk(tree) if isinstance(node,ast.Call) and isinstance(node.func,ast.Attribute)
               and isinstance(node.func.value,ast.Name) and node.func.value.id=='subprocess' and node.func.attr=='run']
        self.assertGreaterEqual(len(calls),3)
        for call in calls:
            values={kw.arg:kw.value for kw in call.keywords}
            if 'capture_output' in values:
                self.assertEqual(ast.literal_eval(values['encoding']),'utf-8')
