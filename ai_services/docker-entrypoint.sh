#!/bin/sh
set -eu

model_cache_dir="${MODEL_CACHE_DIR:-/models}"
design_output_dir="${DESIGN_OUTPUT_DIR:-/app/designs}"

mkdir -p "$model_cache_dir" "$design_output_dir"

if [ "$(id -u)" = "0" ]; then
    chown -R appuser:appuser "$model_cache_dir" "$design_output_dir"
    exec setpriv --reuid=1001 --regid=999 --init-groups -- "$@"
fi

if [ ! -w "$model_cache_dir" ] || [ ! -w "$design_output_dir" ]; then
    echo "AI service cache directories are not writable" >&2
    exit 1
fi

exec "$@"
