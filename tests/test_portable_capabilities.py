"""Bounded regex support and early rejection of unusable acceptance commands."""
import shlex
import tempfile
import unittest
from pathlib import Path
from unittest import mock
from liquid_kernel.context import audit_portable_python, EvaluationDefinitionError, normalize_executable_command
from liquid_kernel.execution import run_portable_command


class PortableCapabilitiesTests(unittest.TestCase):
    def execute(self, source, timeout=10):
        temp = tempfile.TemporaryDirectory(); self.addCleanup(temp.cleanup)
        return run_portable_command(Path(temp.name), 'python3 -c '+shlex.quote(source), timeout=timeout)

    def test_common_regex_flags_patterns_groups_callbacks_and_unicode(self):
        source = r'''import re
assert chr(34)=='"' and ord('🔥')==128293
p=re.compile(r'(?P<word>[a-z]+)-(\d+)',re.I)
m=p.fullmatch('ABC-42')
assert m.group(0)=='ABC-42'
assert m.group('word',2)==('ABC','42')
assert m['word']=='ABC'
assert m.groups()==('ABC','42')
assert m.groupdict()=={'word':'ABC'}
assert m.span(2)==(4,6) and m.start()==0 and m.end()==6
assert m.expand(r'\2-\g<word>')=='42-ABC'
assert p.groups==2 and p.groupindex=={'word':1}
assert re.search(p,' ABC-42 ').group(2)=='42'
assert re.findall(r'(a)(b)','ab ab')==[('a','b'),('a','b')]
assert [m.group() for m in re.finditer(r'\d+','a1 b22')]==['1','22']
assert re.sub(r'\d+',lambda m: '['+m.group()+']','a1 b22')=='a[1] b[22]'
assert re.subn(r'\d','X','a1 b2')==('aX bX',2)
assert re.split(r'\s+','a b')==['a','b']
assert re.fullmatch(rb'\xff',b'\xff').group()==b'\xff'
'''
        result = self.execute(source)
        self.assertEqual(result['exit_code'], 0, result)

    def test_static_audit_accepts_regex_aliases_and_workspace_imports(self):
        for source in ['import re as rx; assert rx.search("a","a")',
                       'from re import fullmatch, I; assert fullmatch("a","A",I)',
                       'from pathlib import Path; import domain_logic; assert Path("a").exists()']:
            audit_portable_python(source)

    def test_unsupported_modules_members_and_escape_constructs_rejected_before_freeze(self):
        for source in ['import re; assert (', 'import subprocess', 'import socket', 'from re import made_up',
                       'import json as j; j.execute("bad")', 'import re; re.__dict__',
                       'class Escape: pass', 'from .unsafe import x', 'from re import *',
                       'async def f(): pass', 'x=().__class__']:
            with self.subTest(source=source), self.assertRaises(EvaluationDefinitionError):audit_portable_python(source)
        with mock.patch('shutil.which', return_value=None):
            with self.assertRaises(EvaluationDefinitionError):normalize_executable_command('import subprocess', 'python', validate_shell=True)

    def test_runtime_escapes_still_blocked_and_regex_timeout_is_bounded(self):
        for source in ['import subprocess; subprocess.run(["echo","bad"])', 'import re; print(re.__dict__)']:
            self.assertNotEqual(self.execute(source)['exit_code'], 0)
        result = self.execute("import re; re.fullmatch('(a+)+', 'a'*60000+'!')", timeout=4)
        self.assertNotEqual(result['exit_code'], 0)
        self.assertIn('time budget', result['output'])
