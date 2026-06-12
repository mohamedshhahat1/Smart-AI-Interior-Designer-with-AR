#!/bin/sh
set -eu

model_cache_dir="${MODEL_CACHE_DIR:-/models}"
design_output_dir="${DESIGN_OUTPUT_DIR:-/app/designs}"
config_home="${XDG_CONFIG_HOME:-/home/appuser/.config}"

mkdir -p "$model_cache_dir" "$design_output_dir" "$config_home"

if [ "$(id -u)" = "0" ]; then
    chown appuser:appuser "$model_cache_dir" "$design_output_dir" "$config_home"
    chown -R appuser:appuser "$design_output_dir" "$config_home"
    exec setpriv --reuid=1001 --regid=999 --init-groups -- "$@"
fi

if [ ! -w "$model_cache_dir" ] || \
   [ ! -w "$design_output_dir" ] || \
   [ ! -w "$config_home" ]; then
    echo "AI service cache directories are not writable" >&2
    exit 1
fi

exec "$@"
