#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PYTHON_BIN="${PYTHON:-python3}"

echo "[build] PyInstaller onefile on Linux"
echo "[build] root=${ROOT}"

"${PYTHON_BIN}" -m PyInstaller \
  --noconfirm \
  --clean \
  --onefile \
  --name web-session-agent-pyinstaller-onefile \
  --distpath "${ROOT}/dist/pyinstaller" \
  --workpath "${ROOT}/build/pyinstaller_onefile" \
  --specpath "${ROOT}/build/pyinstaller_onefile" \
  "${ROOT}/Clouds_Coder.py"

BIN="${ROOT}/dist/pyinstaller/web-session-agent-pyinstaller-onefile"
if [[ ! -x "${BIN}" ]]; then
  echo "[error] Built executable not found: ${BIN}" >&2
  exit 1
fi

"${BIN}" --help >/dev/null
echo "[ok] PyInstaller onefile build complete"
echo "[ok] executable=${BIN}"
