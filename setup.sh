#!/usr/bin/env bash
# Create the local environment, download project data/models, and build the index.
set -Eeuo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_BIN="python3.11"
VENV_PYTHON="$PROJECT_DIR/.venv/bin/python"

fail() {
    printf 'ERROR: %s\n' "$1" >&2
    exit 1
}

run_step() {
    step="$1"
    shift
    printf '\n== %s ==\n' "$step"
    if "$@"; then
        return 0
    else
        status=$?
        fail "$step failed (exit status $status). Fix the issue above and run bash setup.sh again."
    fi
}

if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
    fail "Python 3.11 is required. Install Python 3.11 from https://www.python.org/downloads/ or your operating system's Python package source, then rerun bash setup.sh."
fi

if ! "$PYTHON_BIN" -c 'import sys; sys.exit(0 if sys.version_info[:2] == (3, 11) else 1)'; then
    fail "The python3.11 command did not start Python 3.11. Check your Python installation and rerun setup."
fi

cd "$PROJECT_DIR"
if [[ ! -e .venv ]]; then
    run_step "Create project virtual environment" "$PYTHON_BIN" -m venv .venv
elif [[ ! -x "$VENV_PYTHON" ]]; then
    fail ".venv exists but has no executable Python. Repair or move that environment, then rerun bash setup.sh."
fi

if ! "$VENV_PYTHON" -c 'import sys; sys.exit(0 if sys.version_info[:2] == (3, 11) else 1)'; then
    fail ".venv must use Python 3.11. We will not replace an existing environment; repair or move .venv and rerun setup."
fi

run_step "Install pinned project dependencies" "$VENV_PYTHON" -m pip install -r "$PROJECT_DIR/requirements.txt"
run_step "Download and verify the pinned dataset" "$VENV_PYTHON" -m scripts.download_data
run_step "Prepare QA and source records" "$VENV_PYTHON" -m scripts.prepare_data
run_step "Check packages and MiniLM" "$VENV_PYTHON" -m scripts.smoke_check
run_step "Build or reuse the retrieval index" "$VENV_PYTHON" "$PROJECT_DIR/build_index.py"
run_step "Download or verify the pinned Qwen model" "$VENV_PYTHON" "$PROJECT_DIR/answer.py" --download

printf '\nSetup complete. Start the app with:\n  bash "%s/run.sh"\n' "$PROJECT_DIR"
