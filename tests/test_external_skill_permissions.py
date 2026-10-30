"""Inaccessible neighboring skill directories must not break ordinary tasks."""
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import Clouds_Coder as cc


class ExternalSkillPermissionTests(unittest.TestCase):
    def test_unreadable_neighbors_and_nested_roots_do_not_abort_discovery(self):
        for inaccessible_relative in ('SKILL.md', 'skills', 'source-code/skills', 'plugins'):
            with self.subTest(path=inaccessible_relative), tempfile.TemporaryDirectory() as directory:
                workspace = Path(directory)
                skills = workspace/'skills'; skills.mkdir()
                local = skills/'local'; local.mkdir()
                (local/'SKILL.md').write_text('---\nname: local\ndescription: Local checks\n---\nworkflow', encoding='utf-8')
                denied = workspace/'snap-private-tmp'; denied.mkdir()
                readable = workspace/'readable'; readable.mkdir()
                (readable/'SKILL.md').write_text('---\nname: neighbor\ndescription: Accessible checks\n---\nworkflow', encoding='utf-8')
                blocked = denied/inaccessible_relative
                original_stat = Path.stat

                def protected_stat(path, *args, **kwargs):
                    if path == blocked:
                        raise PermissionError('simulated inaccessible external skill path')
                    return original_stat(path, *args, **kwargs)

                with mock.patch.object(Path, 'stat', new=protected_stat):
                    store = cc.SkillStore(skills)
                    store.reload(force=True)
                names = {row['name'] for row in store.skills.values()}
                self.assertIn('local', names)
                self.assertIn('neighbor', names)
                self.assertTrue(any('PermissionError' in warning for warning in store.warnings))
