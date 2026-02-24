import requests
import json
import re
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
MODEL = os.getenv("MODEL")

url = f"https://api.bytez.com/models/v2/{MODEL}"

def process_response(response):
    data = response.json()

    content = data["output"]["content"]

    think_match = re.search(r"<think>(.*?)</think>", content, re.DOTALL)

    if think_match:
        thought = think_match.group(1).strip()
        answer = re.sub(r"<think>.*?</think>", "", content, flags=re.DOTALL).strip()
    else:
        thought = None
        answer = content.strip()

    return (thought, answer)

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

payload = {
    "messages": [
        { "role": "system", "content": "You are a helpful assistant." },
        { "role": "user", "content": "What's the weather like today?" }
    ],
    # "stream": True
}

# response = requests.post(url, headers=headers, json=payload, stream=True)
# for line in response.iter_lines():
#     if line:
#         print(line.decode("utf-8"))

response = requests.post(url, headers=headers, json=payload)
thought, answer = process_response(response)

print(thought)
print(answer)