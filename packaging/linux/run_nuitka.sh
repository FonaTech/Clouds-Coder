#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
BIN="${ROOT}/dist/nuitka/Clouds_Coder.dist/web-session-agent-nuitka"
if [[ ! -x "${BIN}" ]]; then
  echo "[error] executable not found: ${BIN}" >&2
  echo "[hint] Run packaging/linux/build_nuitka.sh first." >&2
  exit 1
fi

HOST="0.0.0.0"
PORT="8080"
EXTRA=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    --host)
      HOST="${2:-}"
      if [[ -z "${HOST}" ]]; then
        echo "[error] --host requires a value" >&2
        exit 2
      fi
      shift 2
      ;;
    --port)
      PORT="${2:-}"
      if [[ -z "${PORT}" ]]; then
        echo "[error] --port requires a value" >&2
        exit 2
      fi
      shift 2
      ;;
    *)
      EXTRA+=("$1")
      shift
      ;;
  esac
done

if (( ${#EXTRA[@]} > 0 )); then
  echo "[run] ${BIN} --host ${HOST} --port ${PORT} ${EXTRA[*]}"
  exec "${BIN}" --host "${HOST}" --port "${PORT}" "${EXTRA[@]}"
fi

echo "[run] ${BIN} --host ${HOST} --port ${PORT}"
exec "${BIN}" --host "${HOST}" --port "${PORT}"
