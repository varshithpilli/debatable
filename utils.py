import json
import re

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