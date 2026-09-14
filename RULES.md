# The rules surface

Two files make up Claude Code's rules for this project. Both are yours to write;
the starter ships them empty.

## .claude/settings.json - permissions

`allow` and `deny` are lists of tool names. The Blender server's tools, as Claude
Code names them (server `blender`, version 1.9.1):

    mcp__blender__get_scene_info
    mcp__blender__get_object_info
    mcp__blender__get_viewport_screenshot
    mcp__blender__execute_blender_code
    mcp__blender__set_texture
    mcp__blender__get_polyhaven_status
    mcp__blender__get_polyhaven_categories
    mcp__blender__search_polyhaven_assets
    mcp__blender__download_polyhaven_asset
    mcp__blender__get_sketchfab_status
    mcp__blender__search_sketchfab_models
    mcp__blender__get_sketchfab_model_preview
    mcp__blender__download_sketchfab_model
    mcp__blender__get_hyper3d_status
    mcp__blender__generate_hyper3d_model_via_text
    mcp__blender__generate_hyper3d_model_via_images
    mcp__blender__poll_rodin_job_status
    mcp__blender__import_generated_asset

One of them runs any Python it is handed. A deny list can name a tool; it cannot
read a script. That is what the hook is for.

## hooks/gate.py - the hook

Runs before every Blender tool call. Write `offends`: return a reason to refuse,
or `None` to let the call through. Every decision lands in `trail.jsonl`.

## Already on, leave it on

`.mcp.json` starts the server in safe mode with telemetry off. The grader checks
that both are still set.
