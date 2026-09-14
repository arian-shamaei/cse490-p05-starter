#!/usr/bin/env bash
# Starts Blender's window on the codespace desktop, every time the codespace starts
# (postStartCommand), and waits for the MCP server socket. Run it by hand if the
# smoke test says the server is not listening:  bash .devcontainer/start-blender.sh
#
# See the window: the Blender window port (6080) opens on its own; if it does not,
# open the Ports tab in VS Code and click the globe next to 6080. Password: vscode.
set -uo pipefail
export DISPLAY="${DISPLAY:-:1}"
export LIBGL_ALWAYS_SOFTWARE=1 GALLIUM_DRIVER=llvmpipe
export LP_NUM_THREADS="${LP_NUM_THREADS:-2}"     # software GL threads; leave cores for the render and the agent
export BLENDER_MCP_SAFE_MODE="${BLENDER_MCP_SAFE_MODE:-1}"
HERE="$(cd "$(dirname "$0")" && pwd)"

# wait for the desktop to bring up display :1
for _ in $(seq 1 60); do
  [ -S /tmp/.X11-unix/X1 ] && break
  sleep 1
done

if pgrep -x blender >/dev/null 2>&1; then
  echo "Blender is already running."
else
  nohup blender --factory-startup -noaudio --window-geometry 0 0 1280 800 \
    --python "$HERE/enable_addon.py" > /tmp/blender.log 2>&1 &
  echo $! > /tmp/blender.pid
fi

# the socket opens only once the window's event loop is running
for i in $(seq 1 120); do
  if (exec 3<>/dev/tcp/127.0.0.1/9876) 2>/dev/null; then
    echo "Blender server listening on localhost:9876 after ${i}s"
    # the live view: viewport.png in the workspace, refreshed every two seconds
    if ! pgrep -f viewport_loop.py >/dev/null 2>&1; then
      nohup python3 "$HERE/viewport_loop.py" >/tmp/viewport.log 2>&1 &
      echo "viewport.png is being refreshed (log: /tmp/viewport.log)"
    fi
    exit 0
  fi
  sleep 1
done
echo "TIMEOUT: the Blender server socket did not open in 120s. See /tmp/blender.log."
exit 1
