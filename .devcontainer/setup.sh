#!/usr/bin/env bash
# One-time container setup for Project 5. Runs once when the codespace is created
# (postCreateCommand). Installs Blender 5.2 LTS, uv, the MCP for Blender add-on
# with telemetry off, the harness dependencies, and Claude Code.
#
# Versions are pinned here and restated in the course setup checklist. Change them
# in both places or not at all.
set -euo pipefail

BLENDER_VERSION="5.2.1"
BLENDER_SERIES="5.2"
BLENDER_URL="https://download.blender.org/release/Blender${BLENDER_SERIES}/blender-${BLENDER_VERSION}-linux-x64.tar.xz"
BLENDER_MCP_VERSION="1.9.1"

log() { printf '\n== %s\n' "$*"; }

log "system libraries Blender needs on a display-less machine"
sudo apt-get update -qq
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y -qq --no-install-recommends \
  libgl1 libglu1-mesa libegl1 libgomp1 \
  libxi6 libxxf86vm1 libxfixes3 libxrender1 libxkbcommon0 libxcursor1 libxinerama1 libxrandr2 \
  libsm6 libice6 libopenal1 libsndfile1 \
  ffmpeg xz-utils curl ca-certificates mesa-utils \
  >/dev/null

log "Blender ${BLENDER_VERSION} into /opt/blender"
if [ ! -x /opt/blender/blender ]; then
  sudo mkdir -p /opt/blender
  curl -fsSL "$BLENDER_URL" | sudo tar -xJ -C /opt/blender --strip-components=1
fi
sudo ln -sf /opt/blender/blender /usr/local/bin/blender
blender --version | head -1

log "uv (runs the MCP for Blender server without a Python install)"
if ! command -v uvx >/dev/null 2>&1; then
  curl -LsSf https://astral.sh/uv/install.sh | sh >/dev/null
fi
export PATH="$HOME/.local/bin:$PATH"
uvx --version

log "warm the server cache so the first connect in class is not a cold download"
uvx "blender-mcp==${BLENDER_MCP_VERSION}" --help >/dev/null

log "install the add-on into Blender's add-ons folder and enable it with telemetry off"
ADDONS="$HOME/.config/blender/${BLENDER_SERIES}/scripts/addons"
mkdir -p "$ADDONS"
uvx "blender-mcp==${BLENDER_MCP_VERSION}" install-addon
blender -b --python-expr "
import bpy
bpy.ops.preferences.addon_enable(module='blender_mcp')
prefs = bpy.context.preferences.addons['blender_mcp'].preferences
if hasattr(prefs, 'telemetry_consent'):
    prefs.telemetry_consent = False
bpy.ops.wm.save_userpref()
print('addon enabled; telemetry_consent =', getattr(prefs, 'telemetry_consent', 'n/a'))
"

log "harness dependencies"
pip install --quiet -r requirements.txt

log "Claude Code"
npm install -g --silent @anthropic-ai/claude-code
claude --version || true

log "folders the build writes into"
mkdir -p scene renders submission

log "done. The Blender window starts on every codespace start (start-blender.sh)."
