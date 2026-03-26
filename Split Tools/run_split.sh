#!/usr/bin/env bash
set -u

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

if command -v python3 >/dev/null 2>&1; then
  PYTHON_BIN="python3"
elif command -v python >/dev/null 2>&1; then
  PYTHON_BIN="python"
else
  echo "[run_split.sh] Python 3 not found."
  exit 2
fi

exec "$PYTHON_BIN" "$SCRIPT_DIR/run_split.py" "$@"
