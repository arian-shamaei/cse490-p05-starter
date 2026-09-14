#!/usr/bin/env bash
# Starts Blender's window on the codespace desktop every time the codespace starts
# (postStartCommand). The MCP for Blender add-on opens its socket on localhost:9876
# as soon as Blender is up, so nothing else has to be clicked.
#
# See the window: the Blender window port (6080) opens in a browser tab on its own;
# if it does not, open the Ports tab in VS Code and click the globe next to 6080.
set -uo pipefail
export DISPLAY=:1
export LIBGL_ALWAYS_SOFTWARE=1

# wait for the desktop (desktop-lite) to bring up display :1
for _ in $(seq 1 60); do
  [ -S /tmp/.X11-unix/X1 ] && break
  sleep 1
done

if pgrep -x blender >/dev/null 2>&1; then
  echo "Blender is already running."
  exit 0
fi

nohup blender --window-geometry 0 0 1280 800 >/tmp/blender.log 2>&1 &
echo "Blender starting (log: /tmp/blender.log). The server listens on localhost:9876 once the window is up."
