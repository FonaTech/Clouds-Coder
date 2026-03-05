#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PYTHON_BIN="${PYTHON:-python3}"

echo "[build] PyInstaller on Linux"
echo "[build] root=${ROOT}"

"${PYTHON_BIN}" -m PyInstaller \
  --noconfirm \
  --clean \
  --onedir \
  --name web-session-agent-pyinstaller \
  --distpath "${ROOT}/dist/pyinstaller" \
  --workpath "${ROOT}/build/pyinstaller" \
  --specpath "${ROOT}/build/pyinstaller" \
  "${ROOT}/Clouds_Coder.py"

BIN="${ROOT}/dist/pyinstaller/web-session-agent-pyinstaller/web-session-agent-pyinstaller"
if [[ ! -x "${BIN}" ]]; then
  echo "[error] Built executable not found: ${BIN}" >&2
  exit 1
fi

"${BIN}" --help >/dev/null
echo "[ok] PyInstaller build complete"
echo "[ok] executable=${BIN}"
