"""Regressions from IMG_2191–2195: fair assertions and truthful command hints."""
import ast
import shlex
import tempfile
import unittest
from pathlib import Path
from unittest import mock
from liquid_kernel.agentic import (TaskWorkspace, command_runtime_contract,
                                   normalize_task_design, build_task_bank)
from liquid_kernel.context import normalize_executable_command
from liquid_kernel import normalize_evolution_config
from test_agentic_evolution import TaskModel, experiences


class AcceptancePortabilityTests(unittest.TestCase):
    def test_python_heredoc_and_utf8_read_are_canonical_and_keep_assertions(self):
        source = "from pathlib import Path\np=Path('报告.txt')\nassert p.read_text() == '中文🔥'\nassert '<svg' not in 'dynamic JS'"
        command = "python3 - <<'PY'\n" + source + "\nPY"
        normalized = normalize_executable_command(command, validate_shell=True)
        actual = shlex.split(normalized['command'])[-1]
        self.assertIn("read_text(encoding='utf-8')", actual)
        self.assertEqual([ast.dump(node) for node in ast.parse(source).body if isinstance(node, ast.Assert) and not any(isinstance(x, ast.Call) for x in ast.walk(node))],
                         [ast.dump(node) for node in ast.parse(actual).body if isinstance(node, ast.Assert) and not any(isinstance(x, ast.Call) for x in ast.walk(node))])
        self.assertIn('source_sha256', normalized)
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); (root/'报告.txt').write_text('中文🔥', encoding='utf-8')
            workspace = TaskWorkspace(root, lambda: None); workspace.backend = 'portable_workspace'
            result = workspace.command(normalized['command'])
            self.assertEqual(result['exit_code'], 0, result)
        self.assertEqual(normalize_executable_command(normalized['command'])['command'], normalized['command'])

    def test_explicit_encoding_and_custom_methods_are_never_rewritten(self):
        for source in ["from pathlib import Path; s=Path('a').read_text(encoding='gbk')", "value=custom.read_text()", "s='read_text() 中文' # read_text()"]:
            command = 'python3 -c ' + shlex.quote(source)
            self.assertEqual(normalize_executable_command(command, validate_shell=True)['command'], command)

    def test_tag_only_check_rejected_but_explicit_static_requirement_supported(self):
        cfg = normalize_evolution_config({'mode': 'Tuning'})['task_benchmark']
        task = {'goal': 'Create chart.html with an embedded SVG or Canvas chart.', 'starter_files': {},
                'followups': [{'after_round': 3, 'content': 'Keep it self-contained.'}],
                'checks': [{'kind': 'file_exists', 'path': 'chart.html'},
                           {'kind': 'command', 'language': 'python', 'command': "from pathlib import Path; html=Path('chart.html').read_text(); assert '<svg' in html or '<canvas' in html"}]}
        with self.assertRaisesRegex(ValueError, 'Representation-specific'): normalize_task_design(task, cfg)
        task['goal'] += ' Use static SVG markup in the source code.'
        self.assertEqual(len(normalize_task_design(task, cfg)[2]), 2)

    def test_windows_runtime_hints_describe_protected_interpreter_not_cmd_or_sh(self):
        with mock.patch('liquid_kernel.agentic.sys.platform', 'win32'):
            contract = command_runtime_contract('portable_workspace')
        self.assertEqual(contract['available_command_runtimes'], ['workspace_python'])
        self.assertIn('not Windows cmd', contract['shell'])
        self.assertNotIn('sh', contract['available_command_runtimes'])

    def test_generation_and_independent_audit_receive_same_runtime_rules(self):
        model = TaskModel()
        with mock.patch('liquid_kernel.agentic.task_execution_backend', return_value='portable_workspace'):
            build_task_bank(experiences(2), normalize_evolution_config({'mode': 'Tuning'}), lambda system, payload: model(system, payload), 42)
        prompts = [row for row in model.calls if row.get('source') or row.get('task_definition')]
        self.assertTrue(prompts)
        self.assertTrue(all(row['command_runtime_contract']['available_command_runtimes'] == ['workspace_python'] for row in prompts))
