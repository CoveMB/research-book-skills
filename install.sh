#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 is required but was not found." >&2
  exit 127
fi

if [[ " $* " != *" --dry-run "* ]]; then
  echo "Tip: run ./install.sh --dry-run to preview changes before installing."
fi

set +e
python3 scripts/install_codex_plugin.py "$@"
status=$?
set -e

if [[ "$status" -ne 0 ]]; then
  echo "Install failed with exit code ${status}." >&2
  exit "$status"
fi
