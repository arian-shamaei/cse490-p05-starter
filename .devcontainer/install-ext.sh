#!/usr/bin/env bash
# Put the course's workspace extension where the editor's server looks for
# extensions. The editor's own install command only works inside its terminals,
# so at build and start time the extension is unpacked by hand. Idempotent.
set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
VSIX="$HERE/cse490-workspace.vsix"
[ -f "$VSIX" ] || exit 0
for base in "$HOME/.vscode-remote/extensions" "$HOME/.vscode-server/extensions"; do
  mkdir -p "$base"
  python3 - "$VSIX" "$base/cse490.cse490-workspace-0.1.0" <<'PY'
import os, shutil, sys, zipfile
vsix, dst = sys.argv[1], sys.argv[2]
shutil.rmtree(dst, ignore_errors=True); os.makedirs(dst)
with zipfile.ZipFile(vsix) as z:
    for n in z.namelist():
        if n.startswith("extension/") and not n.endswith("/"):
            out = os.path.join(dst, n[len("extension/"):])
            os.makedirs(os.path.dirname(out), exist_ok=True)
            open(out, "wb").write(z.read(n))
print("workspace extension unpacked into", dst)
PY
done
