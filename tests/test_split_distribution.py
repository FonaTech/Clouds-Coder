"""The split runtime must work without reading the original monolith."""
import ast
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class SplitDistributionTests(unittest.TestCase):
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
