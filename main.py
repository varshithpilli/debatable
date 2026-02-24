import requests
import os
from dotenv import load_dotenv

from utils import process_response

load_dotenv()

API_KEY = os.getenv("API_KEY")
MODEL = os.getenv("MODEL")

url = f"https://api.bytez.com/models/v2/{MODEL}"

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