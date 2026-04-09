#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

VENV_PY="$(pwd)/.venv/bin/python"

if [[ ! -x "$VENV_PY" ]]; then
    echo "Fehler: venv Python nicht gefunden: $VENV_PY"
    exit 1
fi

PYTHONPATH=src "$VENV_PY" -m trsc.init-setup.