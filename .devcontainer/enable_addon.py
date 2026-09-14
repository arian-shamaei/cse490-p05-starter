"""Runs inside Blender at every launch (start-blender.sh passes it with --python).

Enables the MCP for Blender add-on, switches its telemetry consent off, hides the splash,
makes sure the server socket on localhost:9876 is listening, and keeps the live view
current: every two seconds it writes a screenshot of the 3D view to viewport.png in the
workspace, which the editor opens beside the assignment. Doing that from inside Blender
means the view lives exactly as long as Blender does; a separate process started from the
codespace's start command was killed when that command finished (2026-09-14).
Prints P05-BLENDER lines to /tmp/blender.log so a failure can be read without clicking in
the window.
"""
import os
import socket
import time

import bpy

T0 = time.time()
WORKSPACE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VIEW = os.path.join(WORKSPACE, "viewport.png")
VIEW_TMP = os.path.join(WORKSPACE, ".viewport.tmp.png")
VIEW_EVERY = float(os.environ.get("VIEWPORT_EVERY", "2"))
VIEW_MAX = int(os.environ.get("VIEWPORT_MAX", "1280"))


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


def live_view():
    """Write the 3D view to viewport.png. The view is rendered off screen the way the
    add-on's own screenshot tool does it: a grab of the window is black whenever the
    window is not composited in front, which on the codespace desktop is always.
    Temp name then rename, so the editor never reads a half-written file. Never raises:
    a failed frame is skipped and the next one comes."""
    try:
        import gpu
        import numpy as np

        win = bpy.context.window_manager.windows[0]
        area = next((a for a in win.screen.areas if a.type == "VIEW_3D"), None)
        if area is None:
            return VIEW_EVERY
        space = area.spaces.active
        region = next((r for r in area.regions if r.type == "WINDOW"), None)
        if region is None or region.width < 8 or region.height < 8:
            return VIEW_EVERY
        w, h = region.width, region.height
        if max(w, h) > VIEW_MAX:
            k = VIEW_MAX / max(w, h)
            w, h = max(1, int(w * k)), max(1, int(h * k))
        off = gpu.types.GPUOffScreen(w, h)
        try:
            off.draw_view3d(bpy.context.scene, bpy.context.view_layer, space, region,
                            space.region_3d.view_matrix, space.region_3d.window_matrix,
                            do_color_management=True)
            buf = off.texture_color.read()
        finally:
            off.free()
        buf.dimensions = w * h * 4
        img = bpy.data.images.new("p05_live_view", w, h, alpha=True)
        try:
            img.pixels.foreach_set((np.asarray(buf, dtype=np.float32) / 255.0).ravel())
            img.filepath_raw = VIEW_TMP
            img.file_format = "PNG"
            img.save()
        finally:
            bpy.data.images.remove(img)
        if os.path.exists(VIEW_TMP):
            os.replace(VIEW_TMP, VIEW)
            if not live_view.first:
                live_view.first = True
                log(f"live view writing {VIEW} ({w}x{h})")
    except Exception as e:  # noqa: BLE001 - the view is a convenience, never a stop
        if not live_view.warned:
            live_view.warned = True
            log(f"live view: {e}")
    return VIEW_EVERY


live_view.first = False
live_view.warned = False

bpy.app.timers.register(ensure_server, first_interval=1.5)
bpy.app.timers.register(live_view, first_interval=3.0, persistent=True)
log(f"blender {bpy.app.version_string} startup script done")
