# Spec: teach the harness the wire

Hand this file to Claude Code together with your `harness.py` from Project 3.
It describes what the harness must do afterward. Claude Code writes the code.

## What changes

The harness keeps its shape from week three: assemble context, call the model,
parse the reply, run a tool, record the result, stop at the turn cap. One thing
is new: some of its tools now come from an MCP server instead of from its own
tool dict.

## Connecting to a server

- Use the official Python SDK, package `mcp` (version 2 or later, already in
  `requirements.txt`). Start the server over stdio with the same command
  `.mcp.json` uses: `uvx blender-mcp==1.9.1`, with the environment variables
  `BLENDER_MCP_SAFE_MODE=1` and `BLENDER_MCP_DISABLE_TELEMETRY=true`.
- At startup, ask the server for its tools (`list_tools`). Each tool has a
  `name`, a `description`, and an `input_schema` (older examples call it
  `inputSchema`; that name no longer exists in the current SDK). Turn each one
  into a tool definition in the format the model API expects, and add them to
  the tools the model is offered.
- When the model calls one of them, forward it to the server (`call_tool`) and
  hand the result text back to the model as the tool result, the same way the
  harness already does for its own tools.

- Keep the whole run inside one async context: start the server, open the session,
  and run every turn within it. Entering the client and the session by hand from a
  separate loop closes the transport on the first call (a first-try failure seen in
  the dry run).

## The gate stays in front of every call

The week-three gate runs before any tool call, server tools included. Extend it
so that it refuses, before the call is made:

1. any of the server's download or generation tools, and
2. any `execute_blender_code` script that switches on or calls a download
   integration (Poly Haven, Sketchfab, Hyper3D) or that saves, exports, or
   renders to a path outside the workspace.

A refusal is a normal tool result that says why; the model reads it and moves on.
The forbidden-tool names are listed in `RULES.md`.

## The trace

Every event lands in `harness/trace.jsonl`, one JSON object per line, as in
week three. New event kinds:

    {"event": "tools_listed", "server": "blender", "tools": ["get_scene_info", ...]}
    {"event": "tool_call", "tool": "...", "args": {...}, "result": "..."}
    {"event": "refused", "tool": "...", "reason": "..."}

## Settings that save you time

- Ask the gateway for up to 8192 output tokens per reply. The default cuts a
  long Blender script in half.
- Retry a call once on an HTTP 502; the gateway drops single replies that run
  past about three minutes.
- Put one line in the system prompt: build in small steps, one object or one
  motion per script.
