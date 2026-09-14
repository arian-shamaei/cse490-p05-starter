#!/usr/bin/env bash
# One-time setup, run when the codespace is created (postCreateCommand). Blender itself is
# already in the image (Dockerfile). This installs the MCP for Blender add-on, uv, warms the
# server, and installs the harness dependencies and Claude Code.
#
# The server version is pinned here, in .mcp.json and in harness/MCP_SPEC.md. Change all
# three or none.
set -uo pipefail
BLENDER_MCP_VERSION="1.9.1"
export PATH="$HOME/.local/bin:$PATH"

log() { printf '\n== %s\n' "$*"; }

log "uv (runs the MCP for Blender server without a Python install)"
if ! command -v uvx >/dev/null 2>&1; then
  curl -LsSf https://astral.sh/uv/install.sh | sh >/dev/null
fi
uvx --version

log "warm the server so the first connect in class is not a cold download"
timeout 120 uvx "blender-mcp==${BLENDER_MCP_VERSION}" --help >/dev/null 2>&1 || true

log "install the add-on into Blender's add-ons folder"
BV="$(blender --version | head -1 | awk '{print $2}' | cut -d. -f1,2)"   # e.g. 5.2
ADDONS="$HOME/.config/blender/${BV}/scripts/addons"
mkdir -p "$ADDONS"
uvx "blender-mcp==${BLENDER_MCP_VERSION}" install-addon || true
ls -1 "$ADDONS"
# The add-on is enabled, with telemetry off, by .devcontainer/enable_addon.py at every
# Blender launch (start-blender.sh), so nothing depends on saved preferences.

log "harness dependencies"
pip install --quiet -r requirements.txt

log "Claude Code"
npm install -g --silent @anthropic-ai/claude-code
claude --version || true

log "folders the build writes into"
mkdir -p scene renders submission record

log "done. Blender's window starts on every codespace start (start-blender.sh)."
