#!/usr/bin/env python3
"""Progress renders: one small Workbench still of the scene after every script
Claude Code runs in Blender, into ride/progress/, so the build's history can be
watched and the checker can join it into a timelapse. Claude Code runs this after
each execute_blender_code call (PostToolUse, see .claude/settings.json).

Not the student's to write; leave it alone. It never blocks a call: any failure
is logged to ride/progress/log.txt and the hook exits 0.

The render settings the student's agent chose are saved before the still and
restored after it, so this never changes the render the ride is judged on.
Paths handed to Blender are absolute: Blender resolves relative ones against its
own working directory, silently.
"""
import json
import os
import socket
import sys
import time

ROOT = os.path.abspath(os.environ.get("CLAUDE_PROJECT_DIR", "."))
OUT = os.path.join(ROOT, "ride", "progress")

SCRIPT = r'''
import bpy, os
s = bpy.context.scene
r = s.render
keep = (r.engine, r.resolution_x, r.resolution_y, r.resolution_percentage, r.filepath,
        r.image_settings.file_format, s.frame_current)
try:
    r.engine = "BLENDER_WORKBENCH"
    r.resolution_x, r.resolution_y, r.resolution_percentage = 640, 360, 100
    r.image_settings.file_format = "PNG"
    r.filepath = %(path)r
    bpy.ops.render.render(write_still=True)
    print("PROGRESS_OK")
finally:
    (r.engine, r.resolution_x, r.resolution_y, r.resolution_percentage, r.filepath,
     r.image_settings.file_format, s.frame_current) = keep
'''


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0
    if data.get("tool_name") != "mcp__blender__execute_blender_code":
        return 0
    os.makedirs(OUT, exist_ok=True)
    n = len([f for f in os.listdir(OUT) if f.endswith(".png")]) + 1
    path = os.path.join(OUT, "%04d.png" % n)
    try:
        s = socket.create_connection(("localhost", 9876), timeout=30)
        s.sendall(json.dumps({"type": "execute_code", "params": {"code": SCRIPT % {"path": path}}}).encode())
        buf = b""
        t0 = time.time()
        while time.time() - t0 < 30:
            chunk = s.recv(65536)
            if not chunk:
                break
            buf += chunk
            try:
                json.loads(buf.decode())
                break
            except ValueError:
                continue
        s.close()
        with open(os.path.join(OUT, "log.txt"), "a", encoding="utf-8") as f:
            f.write("%s %s %s\n" % (time.strftime("%H:%M:%S"), os.path.basename(path),
                                    "ok" if os.path.exists(path) else "no file: " + buf[:120].decode(errors="replace")))
    except Exception as e:  # noqa: BLE001 - never block the student's call
        with open(os.path.join(OUT, "log.txt"), "a", encoding="utf-8") as f:
            f.write("%s error %s\n" % (time.strftime("%H:%M:%S"), e))
    return 0


if __name__ == "__main__":
    sys.exit(main())
