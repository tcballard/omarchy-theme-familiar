"""Isolated config tests; shell IPC is mocked, not live Omarchy evidence."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

BASE = Path(__file__).resolve().parent
DEFAULT = {"version": 1, "idle": {"lock": 300}, "plugins": [{"id": "custom.service"}],
           "bar": {"position": "top", "layout": {
               "left": [{"id": "omarchy.menu"}, {"id": "custom.widget", "secretOption": "keep"}],
               "center": [{"id": "omarchy.clock", "timezone": "Europe/London"}],
               "right": [{"id": "omarchy.audio"}]}}}


def scenario(present=True):
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        config = root / ".config/omarchy/shell.json"
        defaults = root / "upstream/config/omarchy/shell.json"
        defaults.parent.mkdir(parents=True)
        defaults.write_text(json.dumps(DEFAULT))
        if present:
            config.parent.mkdir(parents=True)
            config.write_text(json.dumps(DEFAULT))
        mock = root / "bin"
        mock.mkdir()
        (mock / "omarchy-shell").write_text('#!/bin/sh\nif [ "$2" = reloadConfig ] && [ "${FAIL_RELOAD:-}" = 1 ]; then exit 1; fi\necho ok\n')
        (mock / "omarchy-shell").chmod(0o755)
        env = dict(os.environ, HOME=str(root), XDG_STATE_HOME=str(root / "state"),
                   OMARCHY_PATH=str(root / "upstream"), PATH=str(mock) + ":" + os.environ["PATH"])

        def run(mode, success=True, extra=None):
            result = subprocess.run([str(BASE / "familiar-preset"), mode], env=env | (extra or {}), capture_output=True, text=True)
            assert (result.returncode == 0) == success, (mode, result.stdout, result.stderr)
            return result

        before = config.read_bytes() if present else None
        plan = json.loads(run("plan").stdout)
        assert (config.read_bytes() if config.exists() else None) == before
        assert plan["bar"]["position"] == "bottom"
        assert plan["idle"] == DEFAULT["idle"]
        assert plan["plugins"] == DEFAULT["plugins"]
        assert {"id": "custom.widget", "secretOption": "keep"} in plan["bar"]["layout"]["right"]
        assert plan["bar"]["layout"]["right"][-1]["timezone"] == "Europe/London"
        run("apply")
        assert json.loads(config.read_text()) == plan
        run("apply", False)
        # Unrelated post-apply edits survive restoration.
        changed = json.loads(config.read_text())
        changed["idle"]["lock"] = 600
        config.write_text(json.dumps(changed))
        run("restore")
        restored = json.loads(config.read_text())
        assert restored["bar"] == DEFAULT["bar"]
        assert restored["idle"]["lock"] == 600
        # Reapplication reuses unchanged installed widget files.
        run("apply")
        changed = json.loads(config.read_text())
        changed["bar"]["position"] = "left"
        config.write_text(json.dumps(changed))
        before = config.read_bytes()
        run("restore", False)
        assert config.read_bytes() == before
        changed["bar"] = plan["bar"]
        config.write_text(json.dumps(changed))
        run("restore")
        # Failed reload retains a recoverable snapshot.
        run("apply", False, {"FAIL_RELOAD": "1"})
        run("restore")
        assert json.loads(config.read_text())["bar"] == DEFAULT["bar"]
        # Malformed input is rejected before mutation.
        config.write_text('{"version":2}')
        run("apply", False)
        assert config.read_text() == '{"version":2}'


scenario(True)
scenario(False)
print("PASS: existing/default config, read-only plan, unknown settings, repeat apply, restore, conflicts, reload recovery, malformed input")
