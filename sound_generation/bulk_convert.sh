#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INPUT_DIR="$SCRIPT_DIR/output_audio"
OUTPUT_DIR="$SCRIPT_DIR/output_audio_ogg"

mkdir -p "$OUTPUT_DIR"

for input_file in "$INPUT_DIR"/*; do
    [[ -f "$input_file" ]] || continue
    filename="$(basename "$input_file")"
    name="${filename%.*}"
    ffmpeg -i "$input_file" -c:a libvorbis "$OUTPUT_DIR/$name.ogg"
done
