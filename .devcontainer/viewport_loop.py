#!/usr/bin/env python3
"""Keep viewport.png current: every two seconds, ask Blender's server for a
viewport screenshot written into the workspace. The editor opens that image
at start and redraws it whenever the file changes, so the student watches
the scene without a desktop tab, a password, or a port.

Started by start-blender.sh once the server socket is up. Writes to a temp
name and renames, so the editor never reads a half-written file. Sleeps
longer while Blender is not listening, and never exits on its own.
"""
import json
import os
import socket
import sys
import time

WORKSPACE = os.environ.get("CLAUDE_PROJECT_DIR") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TARGET = os.path.join(WORKSPACE, "viewport.png")
TMP = os.path.join(WORKSPACE, ".viewport.tmp.png")
EVERY = float(os.environ.get("VIEWPORT_EVERY", "2"))
MAX_SIZE = int(os.environ.get("VIEWPORT_MAX", "1280"))


def shot():
    s = socket.create_connection(("localhost", 9876), timeout=15)
    try:
        s.sendall(json.dumps({"type": "get_viewport_screenshot",
                              "params": {"max_size": MAX_SIZE, "filepath": TMP}}).encode())
        buf = b""
        t0 = time.time()
        while time.time() - t0 < 15:
            chunk = s.recv(65536)
            if not chunk:
                break
            buf += chunk
            try:
                reply = json.loads(buf.decode())
                break
            except ValueError:
                continue
        else:
            return False
    finally:
        s.close()
    ok = reply.get("status") == "success" and os.path.exists(TMP)
    if ok:
        os.replace(TMP, TARGET)
    return ok


def main():
    while True:
        try:
            ok = shot()
        except (OSError, ValueError):
            ok = False
        time.sleep(EVERY if ok else 5)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
