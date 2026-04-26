#!/usr/bin/env bash
set -euo pipefail

sound_file="$1"
voice_line="$2"

if [[ "$sound_file" == "" ]]; then
    echo "No arguments passed"
    exit 1
fi
if [[ "$voice_line" == "" ]]; then
    echo "No voice line passed"
    exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

cd "$SCRIPT_DIR/minimax_audio"
python tts.py --volume 5 -o "../output_audio/$sound_file" "$voice_line"
