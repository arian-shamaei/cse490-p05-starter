FROM mcr.microsoft.com/devcontainers/base:ubuntu-24.04

# Blender 5.2 LTS, the release the course pins for students. Pinned here and restated in the
# course setup checklist; change both or neither.
ARG BLENDER_SERIES=5.2
ARG BLENDER_VERSION=5.2.1

# Runtime libraries the Linux tarball expects from the OS, plus Mesa's software rasterizer
# (llvmpipe, in libgl1-mesa-dri) so the GUI runs on a machine with no GPU. Blender bundles
# freetype, png, tiff, openjp2 and sndfile itself. ffmpeg is for the checker's duration probe.
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
      libgl1 libglx-mesa0 libgl1-mesa-dri libegl1 libgles2 libglu1-mesa mesa-utils \
      libx11-6 libxi6 libxxf86vm1 libxfixes3 libxrender1 libxkbcommon0 libxrandr2 libxcursor1 libxinerama1 \
      libsm6 libice6 libdbus-1-3 libpulse0 libgomp1 \
      ffmpeg xz-utils ca-certificates curl \
 && rm -rf /var/lib/apt/lists/*

# download.blender.org answers 403 to non-browser clients (instructor play-test, 2026-09-12);
# the OCF mirror serves the same file, and the browser user agent is the fallback.
RUN set -eux; \
    f="blender-${BLENDER_VERSION}-linux-x64.tar.xz"; \
    ( curl -fsSL -o /tmp/b.tar.xz "https://mirrors.ocf.berkeley.edu/blender/release/Blender${BLENDER_SERIES}/${f}" \
      || curl -fsSL -A "Mozilla/5.0" -o /tmp/b.tar.xz "https://download.blender.org/release/Blender${BLENDER_SERIES}/${f}" ); \
    mkdir -p /opt/blender; \
    tar -xJf /tmp/b.tar.xz -C /opt/blender --strip-components=1; \
    rm /tmp/b.tar.xz; \
    ln -s /opt/blender/blender /usr/local/bin/blender; \
    /opt/blender/blender --version
