# Project 5 starter

Everything for the build lives in this codespace: Blender, its server, Claude Code,
and a place for your harness. Your laptop stays outside.

- `bash smoke.sh` tells you whether the codespace is ready.
- Every open arranges the screen: Blender's live view (`viewport.png`, redrawn every two seconds)
  in the middle, Claude Code on the right, the terminal below. Lost it? F1, then
  "CSE 490: Arrange the workspace". Blender's real window is on port 6080 (Ports tab, right-click,
  Preview in Editor; password vscode) when you want to play the animation.
- Claude Code lives in the right-hand sidebar, already signed in to the course gateway. The terminal
  below is for your harness.
- `fixtures/` holds the lecture's pelican prompt and your scene brief.
- `harness/` is where your week-three harness goes; `harness/MCP_SPEC.md` is what
  you hand Claude Code.
- `RULES.md` names the rules surface: `.claude/settings.json` and `hooks/gate.py`.
- `python3 checker.py` tells you which promises hold, and writes your submission
  bundle to `submission/`.

The handout in Canvas is the assignment. This file is only the map.
