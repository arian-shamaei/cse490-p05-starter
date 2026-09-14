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
# a fixed path for the editor extension, which may not see the node manager's bin folder
CLAUDE_BIN="$(command -v claude || true)"
[ -n "$CLAUDE_BIN" ] && sudo ln -sf "$CLAUDE_BIN" /usr/local/bin/claude

log "the course key, kept private inside the container for shells the secret does not reach"
# Codespaces hands secrets to the editor's terminal and to this setup step, but not to an
# SSH session (instructor play-test, 2026-09-12). A copy under the home folder, readable by
# this user only, lets every shell find it.
if [ -n "${LITELLM_API_KEY:-}" ]; then
  mkdir -p "$HOME/.config/cse490" && chmod 700 "$HOME/.config/cse490"
  printf '%s' "$LITELLM_API_KEY" > "$HOME/.config/cse490/key" && chmod 600 "$HOME/.config/cse490/key"
fi

log "Claude Code talks to the course gateway with the course key, from every shell"
PROFILE_LINE='[ -z "${LITELLM_API_KEY:-}" ] && [ -r "$HOME/.config/cse490/key" ] && export LITELLM_API_KEY="$(cat "$HOME/.config/cse490/key")"; export ANTHROPIC_BASE_URL="${LITELLM_BASE_URL:-https://litellm-test.cs.washington.edu}" ANTHROPIC_AUTH_TOKEN="$LITELLM_API_KEY" ANTHROPIC_MODEL="${ANTHROPIC_MODEL:-claude-sonnet-5}"'
for rc in "$HOME/.bashrc" "$HOME/.zshrc" "$HOME/.profile"; do
  grep -q 'ANTHROPIC_AUTH_TOKEN' "$rc" 2>/dev/null || echo "$PROFILE_LINE" >> "$rc"
done

log "Claude Code first-run answers, so the first launch lands on the prompt"
python3 - <<'PY'
import json, os, pathlib
cfg = pathlib.Path.home() / ".claude.json"
data = {}
if cfg.exists():
    try:
        data = json.loads(cfg.read_text())
    except json.JSONDecodeError:
        data = {}
ws = os.environ.get("CODESPACE_VSCODE_FOLDER") or os.getcwd()
data.setdefault("hasCompletedOnboarding", True)
data.setdefault("theme", "dark")
data.setdefault("shiftEnterKeyBindingInstalled", True)
data.setdefault("hasAcknowledgedCostThreshold", True)
proj = data.setdefault("projects", {}).setdefault(ws, {})
proj.setdefault("hasTrustDialogAccepted", True)
proj.setdefault("hasCompletedProjectOnboarding", True)
enabled = proj.setdefault("enabledMcpjsonServers", [])
if "blender" not in enabled:
    enabled.append("blender")
cfg.write_text(json.dumps(data, indent=1))
print("wrote", cfg, "for", ws)
PY

log "the Blender window connects by itself at the port's bare address"
# The desktop feature serves noVNC; its front page is a connect form. The editor's auto-preview
# opens the bare address, so that page becomes a redirect to the auto-connecting one.
for d in /usr/local/novnc/noVNC-*; do
  [ -d "$d" ] || continue
  printf '%s' '<!doctype html><meta http-equiv="refresh" content="0; url=vnc.html?autoconnect=true&resize=scale&password=vscode"><title>Blender window</title>' \
    | sudo tee "$d/index.html" >/dev/null && echo "auto-connect page in $d"
done

log "folders the build writes into"
mkdir -p scene renders submission record

log "done. Blender's window starts on every codespace start (start-blender.sh)."
