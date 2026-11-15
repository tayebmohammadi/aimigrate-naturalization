#!/usr/bin/env bash
# Launch the local Streamlit app with the project environment and saved index.
set -Eeuo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PYTHON="$PROJECT_DIR/.venv/bin/python"
APP_PORT="${AIMIGRATE_PORT:-8502}"

fail() {
    printf 'ERROR: %s\n' "$1" >&2
    exit 1
}

if [[ ! -f "$PROJECT_DIR/setup.sh" ]]; then
    fail "setup.sh is missing from $PROJECT_DIR. Restore the project files before launching."
fi

if [[ ! -x "$VENV_PYTHON" ]]; then
    fail "Project environment is missing. Run: bash \"$PROJECT_DIR/setup.sh\""
fi

if ! "$VENV_PYTHON" -c 'import streamlit' >/dev/null 2>&1; then
    fail "Streamlit is unavailable in .venv. Run: bash \"$PROJECT_DIR/setup.sh\""
fi

for resource in \
    "$PROJECT_DIR/data/processed/sources.jsonl" \
    "$PROJECT_DIR/data/index/manifest.json" \
    "$PROJECT_DIR/data/index/passages.jsonl" \
    "$PROJECT_DIR/data/index/embeddings.npy"; do
    if [[ ! -f "$resource" ]]; then
        fail "Required index resource is missing: $resource. Run: bash \"$PROJECT_DIR/setup.sh\""
    fi
done

case "$APP_PORT" in
    ''|*[!0-9]*) fail "AIMIGRATE_PORT must contain only digits." ;;
esac

cd "$PROJECT_DIR"
printf 'Opening AImigrate at http://127.0.0.1:%s\n' "$APP_PORT"
exec env HF_HUB_OFFLINE=1 TOKENIZERS_PARALLELISM=false \
    "$VENV_PYTHON" -m streamlit run "$PROJECT_DIR/app.py" \
    --server.address 127.0.0.1 \
    --server.port "$APP_PORT" \
    --server.headless true \
    --server.fileWatcherType none \
    --browser.gatherUsageStats false
