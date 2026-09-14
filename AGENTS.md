# Brief for the agent building the Project 5 scene

You are building a short 3D animation in Blender through the `blender` MCP server.
The student asks; you build. Read `fixtures/scene_brief.md` first: it is the
student's brief for the scene and the setting they chose.

## How to build

- Build only through the Blender server's tools. Never ask the student to click
  in Blender.
- One object or one motion per script. Keep each `execute_blender_code` script
  short; a long script is cut off on its way back from the model.
- Model everything from primitives (cubes, cylinders, spheres, cones, planes).
  No downloaded assets, no generated models.
- Animate with keyframes or drivers on separate objects. Never join the pelican,
  the bicycle, or its wheels into one mesh; the grader reads motion per object.
- Scene settings: 24 frames per second; a frame range that covers two to five
  seconds of motion; one camera that frames the pelican and the bicycle on the
  first and last frame; at least one light.

## Files, all inside this workspace

- Scene: save to `scene/ride.blend` (relative to the workspace root; get the
  root from the `CLAUDE_PROJECT_DIR` environment variable or the current
  directory).
- Render: engine `BLENDER_WORKBENCH`, resolution 640 x 360, output as an MP4
  (FFmpeg container, H.264) to `renders/ride.mp4`. Render the full frame range.
- Nothing is written anywhere else: not `/tmp`, not the home directory. `viewport.png` is the
  student's live view, written by the container; never write or delete it.

## What the student submits from your work

The scene file, the render, and this session's transcript. `checker.py` collects
them; you do not need to.
