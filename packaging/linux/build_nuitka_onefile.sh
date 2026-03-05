#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PYTHON_BIN="${PYTHON:-python3}"

echo "[build] Nuitka onefile on Linux"
echo "[build] root=${ROOT}"

"${PYTHON_BIN}" -m nuitka \
  --onefile \
  --assume-yes-for-downloads \
  --remove-output \
  --output-dir="${ROOT}/dist/nuitka" \
  --output-filename=web-session-agent-nuitka-onefile \
  "${ROOT}/Clouds_Coder.py"

BIN="${ROOT}/dist/nuitka/web-session-agent-nuitka-onefile"
if [[ ! -x "${BIN}" ]]; then
  echo "[error] Built executable not found: ${BIN}" >&2
  exit 1
fi

"${BIN}" --help >/dev/null
echo "[ok] Nuitka onefile build complete"
echo "[ok] executable=${BIN}"
