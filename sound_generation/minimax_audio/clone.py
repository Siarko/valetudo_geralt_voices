"""
Example for voice cloning.
Note: Set `MINIMAX_API_KEY` in environment variables,
and replace "<voice_id>", <file_id_of_cloned_voice>, <file_id_of_prompt_audio> with actual values.
"""
import requests
import os
import sys

api_key = os.getenv("MINIMAX_API_KEY")
url = "https://api.minimax.io/v1/voice_clone"

payload = {
    "file_id": sys.argv[1],
    "voice_id": sys.argv[2],
    "text": sys.argv[3],
    "model": "speech-2.8-hd",
    "language_boost": "Polish"
}

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

response = requests.post(url, headers=headers, json=payload)
response.raise_for_status()
print(response.text)
