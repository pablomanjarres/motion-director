#!/usr/bin/env bash
# Run the HyperFrames CLI pinned, with telemetry, update checks and global skill
# installs switched off. Refuses subcommands that read agent credentials, install
# or update skills, change the pinned version, or send project data to remote
# services. Version: $HYPERFRAMES_VERSION, else the pin in ./package.json, else
# the release the motion library was audited against.
set -euo pipefail

AUDITED_VERSION="0.8.144"

case "${1:-}" in
  usage|feedback|events|skills|upgrade|auth|open|catch-up|telemetry|publish|cloud|cloudrun|lambda)
    echo "hf.sh: refusing 'hyperframes $1': it reads agent credentials, changes installed skills or" \
      "versions, or sends data off this machine. Run the CLI directly only if that is intended." >&2
    exit 2
    ;;
esac

version="${HYPERFRAMES_VERSION:-}"
if [ -z "$version" ] && [ -f package.json ]; then
  version="$(grep -oE 'hyperframes@[0-9]+\.[0-9]+\.[0-9]+' package.json | head -n 1 | cut -d@ -f2 || true)"
fi
version="${version:-$AUDITED_VERSION}"

export HYPERFRAMES_NO_TELEMETRY=1 DO_NOT_TRACK=1 HYPERFRAMES_SKIP_SKILLS=1 \
  HYPERFRAMES_NO_UPDATE_CHECK=1 HYPERFRAMES_NO_AUTO_INSTALL=1
exec npx --yes "hyperframes@${version}" "$@"
