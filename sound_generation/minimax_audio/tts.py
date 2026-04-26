import json
import os
import sys
import argparse
import urllib.request
import urllib.error

HTTP_VOICE_API_URL = "https://api.minimax.io/v1/t2a_v2"

def parse_args():
    parser = argparse.ArgumentParser(description="Generate voice line for given input - using minimax api")

    parser.add_argument("text", help="Text for the voice line")
    parser.add_argument("-o", "--output", help="Output file name without extension", default="output")
    parser.add_argument("-m", "--model", help="Model used for generation", default="speech-2.8-hd")
    parser.add_argument("-v", "--voice", help="Voice ID of voice used for generation", default="geralt_voice_1")
    parser.add_argument("--volume", help="Volume for the generted sound", default=1, type=int)

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    return parser.parse_args()

def load_env(filepath=".env"):
    with open(filepath) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):  # pomijaj komentarze i puste linie
                continue
            key, _, value = line.partition("=")
            os.environ.setdefault(key.strip(), value.strip())

def call_voice_api(text, model, voice_id, volume, api_key):
    if volume < 0 or volume > 10:
        print("Volume not in range [0-10]")
        exit(1)
    
    print("Calling voice api")
    data = {
        "model": model,
        "text": text,
        "stream": False,
        "voice_setting": {
            "voice_id": voice_id,
            "speed": 1,
            "vol": volume,
            "pitch": 0
        },
        "audio_setting": {
            "sample_rate": 32000,
            "bitrate": 128000,
            "format": "mp3",
            "channel": 1
        },
        "language_boost": "Polish",
        "output_format": "hex"
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    req = urllib.request.Request(HTTP_VOICE_API_URL, data=json.dumps(data).encode(), headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            body = json.loads(response.read())
    except urllib.error.HTTPError as e:
        print(f"HTTP error {e.code}: {e.reason}")
        exit(1)

    base_resp = body.get("base_resp", {})
    if base_resp.get("status_code") != 0:
        print(f"API error {base_resp.get('status_code')}: {base_resp.get('status_msg')}")
        exit(1)

    return bytes.fromhex(body["data"]["audio"])

def write_output(output_path, data):
    with open(f"{output_path}.mp3", "wb") as f:
        f.write(data)
    print(f"Saved to {output_path}.mp3")

def main():
    load_env()
    args = parse_args()

    if not args.text:
        print("Text must be supplied")
        exit(1)

    api_key = os.getenv("MINIMAX_API_KEY")
    if not api_key:
        print("Minimax api key missing in env")
        exit(1)

    result = call_voice_api(
            args.text,
            args.model,
            args.voice,
            args.volume,
            api_key
            )
    write_output(args.output, result)


if __name__ == "__main__":
    main();
