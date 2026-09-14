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

- Every path you hand Blender is absolute. Blender resolves a relative path against
  its own working directory, not this workspace, and says nothing when frames land
  elsewhere. Build paths from the workspace root (the `CLAUDE_PROJECT_DIR`
  environment variable, else the current directory).
- Scene: save to `ride/ride.blend` under that root.
- A still, when the student asks to see the scene: engine `BLENDER_WORKBENCH`, 640 x 360,
  PNG to `ride/still.png`, then show it or tell the student where it is.
- Render: engine `BLENDER_WORKBENCH`, resolution 640 x 360, output as PNG frames
  into `ride/frames/` (file path `ride/frames/f_####`). Render the full frame
  range. This Blender build has no video encoder, so after the frames are written, join
  them yourself with the installed ffmpeg into `ride/ride.mp4` (24 frames a second,
  H.264, yuv420p). The checker does the same only if the file is missing.
- Nothing is written anywhere else: not `/tmp`, not the home directory. `viewport.png` is the
  student's live view, written by the container; never write or delete it.

## What the student submits from your work

The scene file, the render, and this session's transcript. `checker.py` collects
them; you do not need to.
