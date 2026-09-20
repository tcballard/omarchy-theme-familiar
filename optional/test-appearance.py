"""Filesystem recovery checks with mocked IPC; not a live compositor test."""
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

BASE = Path(__file__).resolve().parent
ORIGINAL = b'-- personal config\nrequire("hypr.looknfeel")\n'


class AppearanceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.config = self.root / '.config/hypr/hyprland.lua'
        self.config.parent.mkdir(parents=True)
        self.config.write_bytes(ORIGINAL)
        self.config.chmod(0o640)
        self.target = self.config.with_name('familiar-appearance.lua')
        self.state = self.root / 'state/familiar-appearance'
        mock = self.root / 'bin'
        mock.mkdir()
        ipc = mock / 'hyprctl'
        ipc.write_text('#!/bin/sh\nif [ "$1" = reload ] && [ "${FAIL_RELOAD:-}" = 1 ]; then exit 1; fi\necho ok\n')
        ipc.chmod(0o755)
        self.env = dict(os.environ, HOME=str(self.root), XDG_STATE_HOME=str(self.root / 'state'),
                        PATH=str(mock) + ':' + os.environ['PATH'])

    def run_mode(self, mode, success=True, **env):
        result = subprocess.run(['bash', str(BASE / 'familiar-preset'), 'appearance', mode],
                                env=self.env | env, capture_output=True, text=True)
        self.assertEqual(result.returncode == 0, success, result.stdout + result.stderr)
        return result

    def test_plan_is_read_only(self):
        self.run_mode('plan')
        self.assertEqual(self.config.read_bytes(), ORIGINAL)
        self.assertFalse(self.target.exists())
        self.assertFalse(self.state.exists())

    def test_roundtrip_and_reapply(self):
        self.run_mode('apply')
        self.assertIn(b'BEGIN Familiar', self.config.read_bytes())
        self.assertEqual(self.config.stat().st_mode & 0o777, 0o640)
        self.assertEqual(self.target.read_bytes(), (BASE / 'familiar-appearance.lua').read_bytes())
        self.run_mode('apply', False)
        self.run_mode('restore')
        self.assertEqual(self.config.read_bytes(), ORIGINAL)
        self.assertFalse(self.target.exists())
        self.run_mode('apply')
        self.run_mode('restore')

    def test_preserves_later_edits(self):
        self.run_mode('apply')
        self.config.write_bytes(self.config.read_bytes() + b'-- later monitor settings\n')
        self.run_mode('restore')
        self.assertEqual(self.config.read_bytes(), ORIGINAL + b'-- later monitor settings\n')

    def test_edited_payload_refused(self):
        self.run_mode('apply')
        self.target.write_text('-- mine now\n')
        before = self.config.read_bytes()
        self.run_mode('restore', False)
        self.assertEqual(self.config.read_bytes(), before)
        self.assertEqual(self.target.read_text(), '-- mine now\n')

    def test_edited_include_refused(self):
        self.run_mode('apply')
        self.config.write_bytes(self.config.read_bytes().replace(b'END Familiar', b'changed Familiar'))
        before = self.config.read_bytes()
        self.run_mode('restore', False)
        self.assertEqual(self.config.read_bytes(), before)
        self.assertTrue(self.target.exists())

    def test_reload_failures_recover(self):
        self.run_mode('apply', False, FAIL_RELOAD='1')
        self.assertTrue((self.state / 'snapshot.json').exists())
        self.config.write_bytes(self.config.read_bytes() + b'-- keep this\n')
        self.run_mode('restore', False, FAIL_RELOAD='1')
        self.assertTrue((self.state / 'snapshot.json').exists())
        self.run_mode('restore')
        self.assertEqual(self.config.read_bytes(), ORIGINAL + b'-- keep this\n')

    def test_partial_apply_recovers(self):
        self.run_mode('apply')
        self.config.write_bytes(ORIGINAL)  # simulate interruption before include write
        self.run_mode('restore')
        self.assertEqual(self.config.read_bytes(), ORIGINAL)
        self.assertFalse(self.target.exists())

    def test_existing_file_and_symlink_refused(self):
        self.target.write_text('-- existing')
        self.run_mode('apply', False)
        self.assertEqual(self.target.read_text(), '-- existing')
        self.target.unlink()
        self.target.symlink_to(self.config)
        self.run_mode('apply', False)
        self.assertEqual(self.config.read_bytes(), ORIGINAL)

    def test_legacy_config_refused(self):
        self.config.rename(self.config.with_suffix('.conf'))
        self.run_mode('apply', False)
        self.assertFalse(self.state.exists())


if __name__ == '__main__':
    unittest.main()
