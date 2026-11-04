"""Selected skill resources run inside the task without mutating their source."""
import tempfile
import shlex
import unittest
from pathlib import Path
from unittest import mock

import Clouds_Coder as cc


class SkillExecutionPermissionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='skill-permissions-中文-')
        self.root = Path(self.temp.name)
        skills = self.root / 'repository' / 'skills'
        skill = skills / 'ledger'
        (skill / 'scripts').mkdir(parents=True)
        (skill / 'SKILL.md').write_text(
            '---\nname: ledger\ndescription: Audit local ledgers\nattachments: [scripts/*.py]\n---\n'
            'Use scripts/run.py. Preserve the source.\n', encoding='utf-8')
        (skill / 'scripts' / 'run.py').write_text('print("中文🔥")\n', encoding='utf-8')
        self.skills_root, self.skill = skills, skill
        self.store = cc.SkillStore(skills)
        self.session = cc.SessionState(
            'permissions', 'permissions', self.root / 'sessions', 'http://127.0.0.1:9', 'unused',
            skills, cc.CryptoBox(self.root / 'Codes'), self.root / 'repository',
            skills_snapshot=self.store, defer_initial_persist=True,
            js_lib_root=self.root / 'js_lib', js_lib_download_enabled=False, web_search_enabled=False)

    def tearDown(self):
        self.temp.cleanup()

    def test_advertised_absolute_application_source_can_be_read(self):
        s = self.session
        s.skill_mode = 'hard'
        s.bound_skill_ids = ['local:ledger']
        snapshot = s.files_root / '.application_skills' / '01'
        snapshot.mkdir(parents=True)
        (snapshot / 'SKILL.md').write_text('immutable complete workflow 中文🔥', encoding='utf-8')
        result = s._dispatch_tool('read_file', {'path': '/workspace/.application_skills/01/SKILL.md', 'mode': 'full'})
        self.assertIn('immutable complete workflow 中文🔥', result)
        self.assertNotIn('Error:', result)

    def test_absolute_virtual_workspace_does_not_follow_nested_cwd(self):
        s = self.session
        nested = s.files_root / 'nested'
        nested.mkdir()
        result = s._rewrite_shell_virtual_paths('cat /workspace/rules.json', nested)
        parts = shlex.split(result)
        self.assertEqual(len(parts), 2)
        self.assertEqual(Path(parts[1]).resolve(), (s.files_root / 'rules.json').resolve())
        self.assertNotEqual(Path(parts[1]).resolve(), (nested / 'rules.json').resolve())

    def assert_task_environment(self, backend_name):
        s = self.session
        s.skill_mode = 'hard'
        env = s._shell_process_env()
        virtual = backend_name in {'bubblewrap', 'docker', 'podman'}
        host_paths = {
            'HOME': s.files_root,
            'TMPDIR': s.files_root / '.clouds_coder/tmp',
            'TMP': s.files_root / '.clouds_coder/tmp',
            'TEMP': s.files_root / '.clouds_coder/tmp',
            'XDG_CACHE_HOME': s.files_root / '.clouds_coder/cache/xdg',
            'MPLCONFIGDIR': s.files_root / '.clouds_coder/cache/matplotlib',
        }
        for key in ('HOME', 'TMPDIR', 'TMP', 'TEMP', 'XDG_CACHE_HOME', 'MPLCONFIGDIR'):
            with self.subTest(variable=key):
                self.assertIn(key, tuple(env), 'Required task-local variable is absent: ' + key)
                host_path = host_paths[key].resolve()
                self.assertTrue(host_path.is_relative_to(s.files_root.resolve()))
                self.assertTrue(host_path.is_dir())
                if virtual:
                    # These paths are resolved inside the sandbox namespace,
                    # not by pathlib on the pytest host. Its /tmp is tmpfs.
                    expected = '/tmp' if key in {'TMPDIR', 'TMP', 'TEMP'} else (
                        '/workspace' if key == 'HOME' else '/workspace/' + host_paths[key].relative_to(s.files_root).as_posix())
                    self.assertEqual(env[key], expected)
                else:
                    self.assertEqual(Path(env[key]).resolve(), host_path)
        if not virtual:
            self.assertNotEqual(Path(env['TMPDIR']).resolve(), Path(tempfile.gettempdir()).resolve())
        self.assertEqual(env['PYTHONIOENCODING'], 'utf-8')

    def test_hard_application_uses_writable_task_home_tmp_and_cache(self):
        self.assert_task_environment(cc._detect_ide_sandbox_backend().get('name', ''))

    def test_application_environment_contract_covers_virtual_and_host_backends(self):
        for name in ('sandbox-exec', 'windows-job', 'bubblewrap', 'docker', 'podman'):
            with self.subTest(backend=name), mock.patch.object(cc, '_detect_ide_sandbox_backend', return_value={'name': name}):
                self.assert_task_environment(name)

    def test_virtual_backend_tmp_is_private_and_workspace_is_bound(self):
        s = self.session
        s.skill_mode = 'hard'
        for name in ('bubblewrap', 'docker', 'podman'):
            backend = {'name': name, 'available': True, 'processes': True, 'image': 'public-test-image'}
            with self.subTest(backend=name), mock.patch.object(cc, '_detect_ide_sandbox_backend', return_value=backend), mock.patch.object(cc.shutil, 'which', side_effect=lambda binary: '/usr/bin/' + binary), mock.patch.object(s, '_remote_runtime_read_roots', return_value=[]), mock.patch.object(s, '_remote_shared_read_mounts', return_value=[]):
                prefix = s._workspace_sandbox_shell_prefix(s.files_root)
            self.assertIn('--tmpfs', prefix)
            temporary_mount = prefix[prefix.index('--tmpfs') + 1]
            self.assertEqual(temporary_mount.split(':', 1)[0], '/tmp')
            if name == 'bubblewrap':
                self.assertIn(('--bind', str(s.files_root.resolve()), '/workspace'), list(zip(prefix, prefix[1:], prefix[2:])))
                self.assertNotIn(('--bind', '/tmp', '/tmp'), list(zip(prefix, prefix[1:], prefix[2:])))
            else:
                self.assertIn(f'type=bind,src={s.files_root.resolve()},dst=/workspace,rw', prefix)
                self.assertIn('--read-only', prefix)

    def test_selected_resources_get_a_verified_task_local_layout(self):
        s = self.session
        original = (self.skill / 'scripts/run.py').read_bytes()
        text = s._load_skill_with_cache('local:ledger', load_source='model:developer')
        self.assertIn('SELECTED SKILL EXECUTION RESOURCES', text)
        row = s._skill_execution_workspaces['local:ledger']
        root = s.files_root / row['relative_root']
        self.assertEqual((root / 'scripts/run.py').read_bytes(), original)
        self.assertEqual((root / 'SKILL.md').read_bytes(), (self.skill / 'SKILL.md').read_bytes())
        (root / 'scripts/cache.txt').write_text('generated 中文🔥', encoding='utf-8')
        self.assertEqual(s._verify_skill_execution_workspaces(), '')
        self.assertEqual((self.skill / 'scripts/run.py').read_bytes(), original)
        self.assertFalse((self.skill / 'scripts/cache.txt').exists())
        self.assertEqual(s._prepare_skill_execution_workspace('local:ledger')['root'], row['root'])
        command = 'python3 /skills/ledger/scripts/run.py'
        self.assertFalse(s._command_targets_global_skills(command))
        rewritten = s._rewrite_shell_virtual_paths(command, s.files_root)
        self.assertIn('.skill_runtime/', rewritten)
        self.assertNotIn(str(self.skill.resolve()), rewritten)
        self.assertTrue(s._command_targets_global_skills('cat /skills/unselected/SKILL.md'))

    def test_modified_mirror_source_is_not_accepted_as_the_approved_skill(self):
        s = self.session
        row = s._prepare_skill_execution_workspace('local:ledger')
        path = s.files_root / row['relative_root'] / 'scripts/run.py'
        path.chmod(0o600)
        path.write_text('print("changed")', encoding='utf-8')
        self.assertIn('source changed', s._verify_skill_execution_workspaces())
        with self.assertRaisesRegex(ValueError, 'source changed'):
            s._prepare_skill_execution_workspace('local:ledger')
        self.assertEqual((self.skill / 'scripts/run.py').read_text(encoding='utf-8'), 'print("中文🔥")\n')

    def test_mirror_symlink_cannot_redirect_resource_copy_outside_the_task(self):
        s = self.session
        mirror = s.files_root / '.skill_runtime'
        mirror.symlink_to(self.root / 'repository', target_is_directory=True)
        with self.assertRaises(ValueError):
            s._prepare_skill_execution_workspace('local:ledger')
        self.assertFalse(any(self.root.glob('repository/skill-*')))

    def active_task(self):
        s = self.session
        s.runtime_task_level = 3
        s.runtime_execution_mode = s.execution_mode = 'single'
        s.runtime_assigned_expert = 'developer'
        s.active_agent_role = 'developer'
        s.runtime_authoritative_goal = 'Inspect the supplied data and implement the current goal.'
        s._blackboard_reset_for_goal(s.runtime_authoritative_goal)
        return s

    @staticmethod
    def preparation(**changes):
        return {'goal': 'Implement the requested data check', 'state': 'User supplied all inputs',
                'skills': 'Considered the metadata; no specialized skill matches this simple check',
                'ready': True, 'basis': 'user_context', 'missing': [], **changes}

    def test_first_observation_does_not_automatically_authorize_todos(self):
        s = self.active_task()
        (s.files_root / 'request.json').write_text('{"rules":"rules.json"}', encoding='utf-8')
        s._dispatch_tool('read_file', {'path': 'request.json', 'mode': 'full'})
        result = s._dispatch_tool('TodoWrite', {'items': [{'content': 'Make a guess', 'status': 'in_progress'}]})
        self.assertIn('task_preparation_required', result)
        self.assertEqual(s.todo.snapshot(), [])
        result = s._dispatch_tool('TodoWrite', {'items': [{'content': 'Make a guess'}],
            'preparation': self.preparation(ready=False, missing=['Need the actual rules'])})
        self.assertIn('task_preparation_pending', result)
        self.assertEqual(s.todo.snapshot(), [])

    def test_user_provided_context_can_be_sufficient_without_a_read_quota(self):
        s = self.active_task()
        result = s._dispatch_tool('TodoWrite', {'items': [{'content': 'Implement the supplied check', 'status': 'in_progress'}],
            'preparation': self.preparation()})
        self.assertNotIn('Error:', result)
        self.assertEqual(len(s.todo.snapshot()), 1)
        row = s.todo.snapshot()[0]
        result = s._dispatch_tool('TodoWrite', {'items': [{'id': row['short_id'], 'status': 'in_progress'}]})
        self.assertNotIn('task_preparation_required', result)
        self.assertEqual(len(s.todo.snapshot()), 1)

    def test_unanswered_question_cannot_be_hidden_by_a_ready_boolean(self):
        s = self.active_task()
        s.pending_user_question = {'question': 'Which label should be used?'}
        result = s._dispatch_tool('TodoWrite', {'items': [{'content': 'Assume a label'}], 'preparation': self.preparation()})
        self.assertIn('task_preparation_pending', result)
        self.assertEqual(s.todo.snapshot(), [])

    def test_plan_research_receives_the_actual_user_clarification(self):
        s = self.active_task()
        s.messages = [{'role': 'user', 'content': s.runtime_authoritative_goal},
                      {'role': 'user', 'content': 'Context already provided. ' * 20 + 'Use label 中文🔥-verified; continue the original task.'}]
        prompt = s._plan_mode_research_prompt()
        self.assertIn('Use label 中文🔥-verified', prompt)
        self.assertIn(s.runtime_authoritative_goal, prompt)

    def test_unread_long_selected_workflow_must_be_observed_before_initial_plan(self):
        s = self.active_task()
        source = self.skill / 'SKILL.md'
        source.write_text(source.read_text(encoding='utf-8') + '\nDetailed operating rule.\n' * 200 + '\nTAIL_REQUIREMENT_72\n', encoding='utf-8')
        s.skills.reload(force=True)
        s._load_skill_with_cache('local:ledger', load_source='model:developer')
        gaps = s._selected_skill_reading_gaps('developer')
        self.assertEqual([g['skill_id'] for g in gaps], ['local:ledger'])
        s._dispatch_tool('read_file', {'path': gaps[0]['workflow'], 'mode': 'full'}, tool_call_id='read-complete-skill')
        self.assertEqual(s._selected_skill_reading_gaps('developer'), [])

    def test_clarification_stays_available_during_l2_preparation(self):
        s = self.active_task()
        s.runtime_task_level = 2
        names = {tool['function']['name'] for tool in s._single_no_plan_todo_perception_tools()}
        self.assertIn('ask_user', names)
        self.assertIn('read_file', names)
        self.assertNotIn('write_file', names)

    def test_read_only_reviewer_can_compare_values_without_shell_redirection(self):
        s = self.session
        command = 'python3 -c "import json; r=json.load(open(\'result.json\')); print(\'mismatches\', 1 if abs(r[\'gross_total\']-41)>1e-6 else 0)"'
        self.assertEqual(s._guard_role_shell_mutation('reviewer', 'bash', {'command': command}), '')
        for command in ('echo changed > result.json', 'python3 -c "print(41 > 0)" > result.json', 'python3 -c "open(\'result.json\',\'w\').write(\'changed\')"'):
            with self.subTest(command=command):
                self.assertIn('shell mutation', s._guard_role_shell_mutation('reviewer', 'bash', {'command': command}))

    def test_snapshot_source_copy_and_unrelated_output_are_not_snapshot_mutations(self):
        s = self.session
        for command in (
            'mkdir -p exec && cp .application_skills/01/scripts/run.py exec/run.py',
            'python3 .skill_runtime/script.py > result.txt\nls .application_skills/01/scripts',
            'cat .application_skills/01/SKILL.md > source-copy.txt',
            'for f in scripts/run.py; do\nif diff -q ".skill_runtime/$f" ".application_skills/01/$f" >/dev/null 2>&1; then echo identical; fi\ndone',
        ):
            with self.subTest(command=command):
                self.assertFalse(s._command_targets_application_snapshot_mutation(command))
        for command in (
            'cp changed.py .application_skills/01/scripts/run.py',
            'rm -rf .application_skills',
            'echo changed > .application_skills/01/SKILL.md',
            'cd .application_skills/01 && touch cache.txt',
            'python3 -c "from pathlib import Path; Path(\'.application_skills/01/SKILL.md\').unlink()"',
        ):
            with self.subTest(command=command):
                self.assertTrue(s._command_targets_application_snapshot_mutation(command))

    def test_plan_research_does_not_infer_readiness_from_productive_rounds(self):
        s = self.active_task()
        s.max_agent_rounds = 12
        s.runtime_round_budget = 0
        turns = iter([{'status': 'ok', 'text': 'additional necessary observation'}] * 6 + [{'status': 'ready'}])
        proposal = {'context': 'Ready after required observations', 'options': [{'id': 'A', 'title': 'Implement', 'summary': 'Complete the objective', 'steps': ['1. Implement and verify']}], 'recommended': 'A'}
        with mock.patch.object(s, '_auto_discover_and_load_skills'), mock.patch.object(s, '_plan_mode_explorer_turn', side_effect=lambda *a, **kw: next(turns)) as research, mock.patch.object(s, '_plan_mode_research_signature', side_effect=[str(i) for i in range(8)]), mock.patch.object(s, '_plan_mode_synthesize_proposal', return_value=proposal) as synthesize:
            result = s._plan_mode_worker('')
        self.assertEqual(result['status'], 'awaiting_choice')
        self.assertEqual(research.call_count, 7)
        synthesize.assert_called_once()

    def test_exhausted_plan_research_does_not_fabricate_an_executable_plan(self):
        s = self.active_task()
        s.max_agent_rounds = 2
        s.runtime_round_budget = 0
        with mock.patch.object(s, '_auto_discover_and_load_skills'), mock.patch.object(s, '_plan_mode_explorer_turn', return_value={'status': 'findings-only', 'text': 'Some context, still missing required rules'}), mock.patch.object(s, '_plan_mode_synthesize_proposal') as synthesize:
            result = s._plan_mode_worker('')
        self.assertEqual(result['status'], 'preparation_pending')
        self.assertEqual(s.blackboard['plan']['phase'], 'research')
        self.assertEqual(s.blackboard['plan']['preparation_state'], 'pending')
        self.assertEqual(s._evaluate_finish_gate()['reason'], 'plan-approval-pending')
        self.assertEqual(s.todo.snapshot(), [])
        synthesize.assert_not_called()


if __name__ == '__main__':
    unittest.main()
