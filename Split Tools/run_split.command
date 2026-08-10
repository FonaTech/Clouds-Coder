#!/usr/bin/env bash
set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

if command -v python3 >/dev/null 2>&1; then
  PYTHON_BIN="python3"
elif command -v python >/dev/null 2>&1; then
  PYTHON_BIN="python"
else
  echo "[run_split.command] Python 3 not found."
  echo
  read -r -p "Press Enter to close..."
  exit 2
fi

"$PYTHON_BIN" "$SCRIPT_DIR/run_split.py" "$@"
STATUS=$?
echo
if [[ -t 0 ]]; then
  read -r -p "Press Enter to close..."
fi
exit "$STATUS"
