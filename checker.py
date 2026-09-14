#!/usr/bin/env python3
"""The Project 5 checker: which promises hold, and the submission bundle.

Run from the workspace root:  python3 checker.py

Every line it prints is one promise from the handout, PASS or NOT YET, in plain
words. It is the student's copy of the grader's checks, not the grader. At the end
it writes submission/p05-bundle.zip with everything the handout asks you to submit
and a manifest of what it found. Download that one file and upload it to Canvas.

The claim text lives here once; the rubric in the project spec is its source.
"""
import datetime
import glob
import json
import os
import re
import shutil
import subprocess
import sys
import zipfile

ROOT = os.path.abspath(os.path.dirname(__file__))
os.chdir(ROOT)

SCENE = "scene/ride.blend"
RENDER = "renders/ride.mp4"
TRAIL = "trail.jsonl"
HARNESS_TRACE = "harness/trace.jsonl"
HARNESS_CODE = "harness/harness.py"
SETTINGS = ".claude/settings.json"
MCP_CONFIG = ".mcp.json"
HOOK = "hooks/gate.py"
BUNDLE_DIR = "submission"
BUNDLE = os.path.join(BUNDLE_DIR, "p05-bundle.zip")

# Fixed targets, owned by the rubric in the project spec (RUBRIC, "Fixed targets").
DENY_TARGETS = [
    "download_polyhaven_asset",
    "download_sketchfab_model",
    "generate_hyper3d_model_via_text",
    "generate_hyper3d_model_via_images",
    "generate_hunyuan3d_model",
    "import_generated_asset",
]
DOWNLOAD_WORDS = ("polyhaven", "sketchfab", "hyper3d", "rodin", "download", "urlopen", "requests.get", "httpx")
OUTSIDE_PATH = re.compile(r"(?<![\w/])(/tmp/|/home/|/etc/|/root/|~/|\.\./)")
SECRET = re.compile(r"\bsk-[A-Za-z0-9_\-]{12,}")

results = []


def check(claim, ok, detail=""):
    results.append((claim, bool(ok), detail))
    tag = "PASS   " if ok else "NOT YET"
    print(f"{tag} {claim}" + (f"  ({detail})" if detail else ""))


def jsonl(path):
    if not os.path.exists(path):
        return []
    out = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    return out


def payload_offends(args):
    text = json.dumps(args).lower()
    if any(w in text for w in DOWNLOAD_WORDS):
        return "download integration"
    if OUTSIDE_PATH.search(json.dumps(args)):
        return "path outside the workspace"
    return None


def blend_probe():
    if not os.path.exists(SCENE):
        return None, "no scene file at " + SCENE
    blender = shutil.which("blender") or "/opt/blender/blender"
    try:
        p = subprocess.run([blender, "-b", SCENE, "--python", "checker_blend.py"],
                           capture_output=True, text=True, timeout=180)
    except (OSError, subprocess.TimeoutExpired) as e:
        return None, f"could not run Blender headless: {e}"
    for line in p.stdout.splitlines():
        if line.startswith("BLENDPROBE "):
            return json.loads(line[len("BLENDPROBE "):]), ""
    return None, "Blender ran but the probe printed nothing"


def video_seconds(path):
    ffprobe = shutil.which("ffprobe")
    if not ffprobe or not os.path.exists(path):
        return None
    p = subprocess.run([ffprobe, "-v", "error", "-show_entries", "format=duration",
                        "-of", "default=nw=1:nk=1", path], capture_output=True, text=True)
    try:
        return float(p.stdout.strip())
    except ValueError:
        return None


def latest_transcript():
    """Claude Code keeps session transcripts under ~/.claude/projects/<cwd slug>/."""
    slug = re.sub(r"[^A-Za-z0-9]", "-", ROOT)
    cands = glob.glob(os.path.expanduser(f"~/.claude/projects/{slug}/*.jsonl"))
    if not cands:
        return None
    return max(cands, key=os.path.getmtime)


def main():
    print("Project 5 checker\n")

    # --- the wire, through your harness
    trace = jsonl(HARNESS_TRACE)
    listed = [e for e in trace if e.get("event") == "tools_listed" and e.get("tools")]
    calls = [e for e in trace if e.get("event") == "tool_call" and e.get("result") is not None]
    check("Your harness received the Blender server's tools and one call came back with a result",
          listed and calls, f"{len(listed)} listings, {len(calls)} calls" if trace else "no harness/trace.jsonl")

    # --- the harness gate
    refused = [e for e in trace if e.get("event") == "refused"]
    good = [e for e in refused if any(t in str(e.get("tool", "")) for t in DENY_TARGETS)
            or payload_offends(e.get("args", {})) or payload_offends({"r": e.get("reason", "")})]
    check("Your harness's gate refused a download or an outside-workspace script before it ran",
          good, f"{len(refused)} refusal(s) in the harness trace")

    # --- the scene
    probe, why = blend_probe()
    if probe:
        geo = probe["geometry_objects"]
        check("The scene has the pelican, the bicycle and a setting: at least three objects, a camera and a light",
              len(geo) >= 3 and probe["cameras"] and probe["lights"],
              f"{len(geo)} objects, {len(probe['cameras'])} camera, {len(probe['lights'])} light")
        span = probe["span_seconds"] or 0
        check("The pelican rides: something turns, something moves forward, over two to five seconds",
              probe["turned"] and probe["moved"] and 2.0 <= span <= 5.5,
              f"turned {len(probe['turned'])}, moved {len(probe['moved'])}, {span} s")
        check("The render engine is Workbench", probe["engine"] == "BLENDER_WORKBENCH", probe["engine"])
    else:
        check("The scene has the pelican, the bicycle and a setting", False, why)
        check("The pelican rides", False, why)
        check("The render engine is Workbench", False, why)

    # --- the render
    secs = video_seconds(RENDER)
    check("The rendered animation exists and runs at least two seconds",
          secs is not None and secs >= 2.0, f"{secs} s" if secs is not None else "no " + RENDER)

    # --- Claude Code's gate
    trail = jsonl(TRAIL)
    starts = [e for e in trail if e.get("event") == "session_start"]
    refusals = [e for e in trail if e.get("event") == "refused"]
    planted = [e for e in refusals if payload_offends(e.get("args", {}))
               or any(t in str(e.get("tool", "")) for t in DENY_TARGETS)]
    check("Your rules refused the temptation: one Blender call blocked, matching a planted action",
          planted, f"{len(refusals)} refusal(s) in trail.jsonl")
    check("The refusal names the tool and the reason",
          any(e.get("tool") and e.get("reason") for e in planted))
    after = False
    if planted:
        idx = trail.index(planted[-1])
        after = any(e.get("event") == "allowed" for e in trail[idx + 1:])
    check("After the refusal, legitimate work still went through", after)
    inside = [s for s in starts if str(s.get("cwd", "")).startswith("/workspaces/")]
    check("The temptation run happened inside the codespace", inside,
          (starts[-1].get("cwd") if starts else "no session_start line in trail.jsonl"))
    bypass = [s for s in starts if "bypass" in str(s.get("permission_mode", "")).lower()]
    check("No session ran in skip-all-permissions mode", not bypass)

    # --- the rules files
    try:
        settings = json.load(open(SETTINGS, encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        settings = {}
    allow = settings.get("permissions", {}).get("allow", [])
    deny = settings.get("permissions", {}).get("deny", [])
    check("Permissions allow the execute tool and deny every download and generation tool",
          any("execute_blender_code" in a for a in allow) and all(any(t in d for d in deny) for t in DENY_TARGETS),
          f"{len(allow)} allow, {len(deny)} deny")
    hooks = json.dumps(settings.get("hooks", {}))
    check("The hook is present and registered for Blender tool calls",
          os.path.exists(HOOK) and "PreToolUse" in hooks and "gate.py" in hooks)
    try:
        mcp = json.load(open(MCP_CONFIG, encoding="utf-8"))
        env = mcp["mcpServers"]["blender"].get("env", {})
    except (OSError, KeyError, json.JSONDecodeError):
        env = {}
    check("Safe mode and telemetry-off are still set on the server",
          env.get("BLENDER_MCP_SAFE_MODE") == "1" and str(env.get("BLENDER_MCP_DISABLE_TELEMETRY")).lower() == "true")

    # --- secrets
    leak = []
    for path in [SETTINGS, MCP_CONFIG, HOOK, HARNESS_CODE, HARNESS_TRACE, TRAIL, "AGENTS.md", "CLAUDE.md"]:
        if os.path.exists(path) and SECRET.search(open(path, encoding="utf-8", errors="ignore").read()):
            leak.append(path)
    check("No key or password in anything you submit", not leak, ", ".join(leak))

    # --- bundle
    os.makedirs(BUNDLE_DIR, exist_ok=True)
    transcript = latest_transcript()
    files = [SCENE, RENDER, TRAIL, HARNESS_TRACE, HARNESS_CODE, SETTINGS, MCP_CONFIG, HOOK]
    manifest = {
        "written": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
        "workspace": ROOT,
        "checks": [{"claim": c, "pass": ok, "detail": d} for c, ok, d in results],
        "files": {},
    }
    with zipfile.ZipFile(BUNDLE, "w", zipfile.ZIP_DEFLATED) as z:
        for f in files:
            manifest["files"][f] = os.path.exists(f)
            if os.path.exists(f):
                z.write(f)
        if transcript:
            z.write(transcript, "record/claude-code-session.jsonl")
            manifest["files"]["record/claude-code-session.jsonl"] = True
        else:
            manifest["files"]["record/claude-code-session.jsonl"] = False
        for extra in glob.glob("record/*"):
            z.write(extra)
            manifest["files"][extra] = True
        z.writestr("manifest.json", json.dumps(manifest, indent=1))
    missing = [f for f, present in manifest["files"].items() if not present]
    passed = sum(1 for _, ok, _ in results if ok)
    print(f"\n{passed} of {len(results)} promises hold.")
    print(f"Bundle written: {BUNDLE}" + (f"  (missing: {', '.join(missing)})" if missing else ""))
    print("Download it from the file explorer and upload it to the Project 5 assignment.")
    return 0 if passed == len(results) and not missing else 1


if __name__ == "__main__":
    sys.exit(main())
