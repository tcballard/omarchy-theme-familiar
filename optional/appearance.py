"""Opt-in Hyprland geometry with an independent, conflict-aware rollback."""
import argparse
import fcntl
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

BASE = Path(__file__).resolve().parent
BLOCK = (b'\n\n-- BEGIN Familiar appearance\n'
         b'dofile(os.getenv("HOME") .. "/.config/hypr/familiar-appearance.lua")\n'
         b'-- END Familiar appearance\n')


def fail(message):
    raise RuntimeError(message)


def regular(path):
    if path.is_symlink() or (path.exists() and not path.is_file()):
        fail(f"Expected a regular file: {path}")


def atomic(path, content):
    fd, name = tempfile.mkstemp(prefix=".familiar-", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        os.chmod(name, path.stat().st_mode & 0o777 if path.exists() else 0o600)
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=["plan", "apply", "restore"], nargs="?", default="plan")
    args = parser.parse_args()
    home = Path.home()
    config = home / ".config/hypr/hyprland.lua"
    target = config.with_name("familiar-appearance.lua")
    state = Path(os.environ.get("XDG_STATE_HOME", str(home / ".local/state"))) / "familiar-appearance"
    snapshot = state / "snapshot.json"
    regular(config)
    regular(target)
    if not config.is_file():
        fail("Quattro's ~/.config/hypr/hyprland.lua is required; legacy .conf files are not modified.")
    if args.mode == "plan":
        print("Optional appearance: 12px corners, 8px inner/16px outer gaps, gentle window shadows.")
        print(f"Append a marked include to {config}; install {target}.")
        print("Bar layout, colours, focus borders and animation preferences are preserved.")
        print("Applies across themes until restored. Existing snapshots or unmanaged includes block application.")
        print((BASE / "familiar-appearance.lua").read_text())
        return
    if not shutil.which("hyprctl"):
        fail("hyprctl is required; run this inside your Hyprland session.")
    subprocess.run(["hyprctl", "version"], check=True, capture_output=True)
    state.mkdir(parents=True, exist_ok=True, mode=0o700)
    with (state / "lock").open("w") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        regular(snapshot)
        current = config.read_bytes()
        if args.mode == "apply":
            if snapshot.exists():
                fail("An appearance snapshot exists; restore before reapplying.")
            if target.exists() or b"familiar-appearance.lua" in current or b"Familiar appearance" in current:
                fail("Existing Familiar appearance configuration found; preserve or remove it manually first.")
            payload = (BASE / "familiar-appearance.lua").read_bytes()
            record = {"before": current.decode(), "payload": payload.decode(), "block": BLOCK.decode()}
            atomic(snapshot, json.dumps(record).encode())
            if config.read_bytes() != current:
                fail("Configuration changed; no configuration written. Snapshot retained for recovery.")
            atomic(target, payload)
            atomic(config, current + BLOCK)
        else:
            if not snapshot.exists():
                fail("No appearance snapshot exists.")
            record = json.loads(snapshot.read_text())
            block = record["block"].encode()
            if target.exists() and target.read_bytes() != record["payload"].encode():
                fail(f"Appearance file was edited; nothing restored. Recovery snapshot: {snapshot}")
            if current.count(block) == 1:
                restored = current.replace(block, b"", 1)
            elif b"Familiar appearance" not in current and b"familiar-appearance.lua" not in current:
                restored = current  # interrupted apply, removed include, or failed reload
            else:
                fail(f"Managed include was changed; nothing restored. Recovery snapshot: {snapshot}")
            if b"familiar-appearance.lua" in restored or b"Familiar appearance" in restored:
                fail("Another Familiar include exists; nothing restored.")
            if config.read_bytes() != current:
                fail("Configuration changed during restoration; nothing written.")
            atomic(config, restored)
            target.unlink(missing_ok=True)
        # On failure, keep the snapshot and allow a later restore.
        result = subprocess.run(["hyprctl", "reload"], capture_output=True, text=True)
        if result.returncode:
            fail(f"Files written but reload failed. Snapshot retained at {snapshot}; restore after recovery.")
        if args.mode == "restore":
            snapshot.rename(state / "restored-snapshot.json")
        print("Familiar appearance " + ("applied." if args.mode == "apply" else "restored."))
        print("Check `hyprctl configerrors` and inspect windows and shell popups on your desktop.")


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, OSError, ValueError, subprocess.CalledProcessError) as error:
        raise SystemExit(f"Familiar: {error}")
