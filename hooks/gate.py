#!/usr/bin/env python3
"""Your hook: the second gate on the Blender server.

Claude Code runs this before every call to a Blender tool (PreToolUse, see
.claude/settings.json). It reads one JSON object on stdin describing the call,
writes one line to trail.jsonl (the audit trail you submit), and then decides:

    exit 0  -> the call goes through
    exit 2  -> the call is refused; whatever this script prints to stderr is the
               reason, and the model sees it

With --session-start it runs once per session and logs where the session is
running and in which permission mode. Leave that part alone: the grader reads it.

The one function you write is `offends`. The skeleton lets everything through.
"""
import datetime
import json
import os
import sys

TRAIL = os.path.join(os.environ.get("CLAUDE_PROJECT_DIR", "."), "trail.jsonl")
WORKSPACE = os.path.abspath(os.environ.get("CLAUDE_PROJECT_DIR", "."))


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")


def log(entry):
    entry["at"] = now()
    with open(TRAIL, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")


def offends(tool, args):
    """Return a short reason string to refuse this call, or None to allow it.

    `tool` is the tool's full name (for example mcp__blender__execute_blender_code)
    and `args` is the dict the model passed. For execute_blender_code the Python
    the model wants to run is in args["code"].

    Read what the script does, not just which tool is named. A hidden tool is not
    a gate: a script can switch the same thing on from inside Blender.
    """
    return None


def main():
    if "--session-start" in sys.argv:
        data = json.load(sys.stdin) if not sys.stdin.isatty() else {}
        log({
            "event": "session_start",
            "cwd": os.getcwd(),
            "workspace": WORKSPACE,
            "permission_mode": data.get("permission_mode", "unknown"),
            "session_id": data.get("session_id"),
        })
        return 0

    data = json.load(sys.stdin)
    tool = data.get("tool_name", "")
    args = data.get("tool_input", {}) or {}
    reason = offends(tool, args)
    if reason:
        log({"event": "refused", "tool": tool, "reason": reason, "args": args})
        print(f"refused by hooks/gate.py: {reason}", file=sys.stderr)
        return 2
    log({"event": "allowed", "tool": tool, "args": args})
    return 0


if __name__ == "__main__":
    sys.exit(main())
