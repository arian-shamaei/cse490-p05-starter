# Project 5 starter

Everything for the build lives in this codespace: Blender, its server, Claude Code,
and a place for your harness. You work in it through the same VS Code as week three;
the wizard connects the two. Your laptop runs nothing else.

- `bash smoke.sh` tells you whether the codespace is ready.
- Every open arranges the screen: `ASSIGNMENT.md` on the left, Blender's window beside it,
  Claude Code on the right, the terminal below. Lost it? F1, then "CSE 490: Arrange the
  workspace". The window is the codespace desktop on port 6080; if the tab is blank, open the
  Ports tab, right-click 6080, Preview in Editor (password vscode).
- Claude Code lives in the right-hand sidebar, already signed in to the course gateway. The terminal
  below is for your harness.
- `fixtures/` holds the lecture's pelican prompt and your scene brief.
- `harness/` holds your week-three harness, untouched, and `harness_mcp.py`, the copy Claude Code
  builds from `harness/MCP_SPEC.md` with the Blender connection added.
- `RULES.md` names the rules surface: `.claude/settings.json` and `hooks/gate.py`.
- Your scene, frames and video live in `ride/`; `ride/progress/` fills with one still per script
  your agent runs, and the checker joins them into a timelapse.
- `python3 checker.py` tells you which promises hold, and writes your submission
  bundle to `submission/`.

The handout in Canvas is the assignment. This file is only the map.
