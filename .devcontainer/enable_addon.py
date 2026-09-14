"""Runs inside Blender at every launch (start-blender.sh passes it with --python).

Enables the MCP for Blender add-on, switches its telemetry consent off, hides the splash,
and makes sure the server socket on localhost:9876 is listening. Prints P05-BLENDER lines
to /tmp/blender.log so a failure can be read without clicking in the window.
"""
import socket
import time

import bpy

T0 = time.time()


def log(msg):
    print(f"P05-BLENDER +{time.time() - T0:5.1f}s {msg}", flush=True)


enabled = None
for name in ("blender_mcp", "blender_mcp_addon", "addon"):
    try:
        bpy.ops.preferences.addon_enable(module=name)
        enabled = name
        log(f"addon enabled: {name}")
        break
    except Exception as e:  # noqa: BLE001 - report every failure, keep trying names
        log(f"enable failed for {name}: {e}")

try:
    bpy.context.preferences.view.show_splash = False
    if enabled:
        ad = bpy.context.preferences.addons.get(enabled)
        if ad and hasattr(ad.preferences, "telemetry_consent"):
            ad.preferences.telemetry_consent = False
            log("telemetry_consent set False")
    bpy.ops.wm.save_userpref()
except Exception as e:  # noqa: BLE001
    log(f"preferences: {e}")


def port_open():
    s = socket.socket()
    s.settimeout(0.5)
    try:
        s.connect(("localhost", 9876))
        return True
    except OSError:
        return False
    finally:
        s.close()


tries = {"n": 0}


def ensure_server():
    tries["n"] += 1
    if port_open():
        log(f"socket localhost:9876 is LISTENING (check {tries['n']})")
        return None
    try:
        bpy.ops.blendermcp.start_server()
        log("start_server operator invoked")
    except Exception as e:  # noqa: BLE001
        log(f"start_server operator: {e}")
    if tries["n"] >= 10:
        log("GAVE UP: socket never opened; see RULES.md and ask the course staff")
        return None
    return 1.0


bpy.app.timers.register(ensure_server, first_interval=1.5)
log(f"blender {bpy.app.version_string} startup script done")
