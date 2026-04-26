"""
Example for obtaining the file_id of the source audio.
Note: Make sure your API key is set in the environment variable `MINIMAX_API_KEY`.
"""
import requests
import os
import os.path
import sys

api_key = os.getenv("MINIMAX_API_KEY")
url = "https://api.minimax.io/v1/files/upload"

if not api_key:
    print("No api key")
    exit()

file_path = sys.argv[1] if len(sys.argv) == 2 else None

print(f"file: {file_path}")
if not file_path or not os.path.isfile(file_path):
    print("Invalid file path passed")
    exit()


payload = {"purpose": "voice_clone"}
files = [
  ("file", (os.path.basename(file_path), open(file_path, "rb")))
]
headers = {"Authorization": f"Bearer {api_key}"}

response = requests.post(url, headers=headers, data=payload, files=files)
response.raise_for_status()
file_id = response.json().get("file", {}).get("file_id")
print(file_id)
