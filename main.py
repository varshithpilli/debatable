import requests
import os
from dotenv import load_dotenv
import json

from utils import process_response

load_dotenv()

API_KEY = os.getenv("API_KEY")
MODEL = os.getenv("MODEL")
STREAM = True if os.getenv("STREAM") == "1" else False

STARTED = False

url = f"https://api.bytez.com/models/v2/{MODEL}"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def get_system_prompt(a):
    if not STARTED:
        return f"""
            You are an elite, master-level debater engaging in a live intellectual exchange.

            Your goal is not to write an essay or structured bullet points. 
            You are speaking directly to your opponent in a sharp, confident, human conversational tone.

            The provided topic of debate is:
            "{a}"

            - Take a strong and unambiguous stance.
            - Do NOT use bullet points.
            - Do NOT use numbered lists.
            - Do NOT use markdown formatting.
            - Do NOT structure your response like an article.
            - Write in natural, flowing paragraphs.
            - Speak as if you are responding in a real debate.
            - Address the opponent's claims directly.
            - Use rhetorical questions where appropriate.
            - Use logic, real-world examples, and layered reasoning.
            - Maintain intellectual dominance without sounding robotic.
            - DO NOT repeat yourself.
            - Keep the tone confident, composed, and sharp.
            - Always start the argument with new sentences and not by repeating the same opening line like Let me challenge your assertion.
            Since this is the first round, clearly establish your position and define the framing of the debate naturally within your speech.
            
            You are persuasive, articulate, and verbally precise.
            You debate like a human expert — not like formatted lecture notes.
            You are starting the debate, STARTING THE DEBATE.
        """
    else:
        return f"""
            You are an elite, master-level debater engaging in a live intellectual exchange.

            Your goal is not to write an essay or structured bullet points. 
            You are speaking directly to your opponent in a sharp, confident, human conversational tone.

            Below is the history of the debate so far:
            "{a}"

            - Take a strong and unambiguous stance.
            - Do NOT use bullet points.
            - Do NOT use numbered lists.
            - Do NOT use markdown formatting.
            - Do NOT structure your response like an article.
            - Write in natural, flowing paragraphs.
            - Speak as if you are responding in a real debate.
            - Address the opponent's claims directly.
            - Use rhetorical questions where appropriate.
            - Use logic, real-world examples, and layered reasoning.
            - Maintain intellectual dominance without sounding robotic.
            - DO NOT repeat yourself.
            - Keep the tone confident, composed, and sharp.
            - Always start the argument with new sentences and not by repeating the same opening line like Let me challenge your assertion.

            Since this is a continuation, respond directly to the opponent's most recent argument and escalate the reasoning strategically.

            You are persuasive, articulate, and verbally precise.
            You debate like a human expert — not like formatted lecture notes.
        """

def api_call(payload):
    response = requests.post(url, headers=headers, json=payload, stream=STREAM)
    print(response)
    final = ""
    if STREAM:
        for line in response.iter_lines():
            if line:
                final += line.decode("utf-8")
    else:
        thought, answer = process_response(response)
        final += f"{answer}"
    return final

def get_payload(debater, inp, sys):
    return {
        "messages": [
            { "role": "system", "content": f" {sys}. \n\n REMEMBER: You are the DEBATER {debater}." },
            { "role": "user", "content": f"start the debate" }
        ],
        "stream": STREAM
    }

debater = 1

while True:
    if STARTED:
        with open("output.txt", "r") as file:
            content = file.read()
            inp = content
    else:
        # inp = input("Give the topic for the debate: ")
        inp = "Prostitution in INDIA"
        STARTED = True
        with open("output.txt", "w") as file:
            # file.write(f"\n\n---------------- DEBATER {debater} ----------------\n")
            file.write(f"TOPIC: {inp}")
            # file.write("\n-----------------------------------------------\n")

    sys = get_system_prompt(inp)
    # print(sys)
    payload = get_payload(debater, inp, sys)
    result = api_call(payload)
    # print(result)

    with open("output.txt", "a") as file:
        file.write(f"\n\n---------------- DEBATER {debater} ----------------\n")
        file.write(result)
        file.write("\n-----------------------------------------------\n")

    debater = 3 - debater







# result2 = call_api_2(processed_output)   # Trigger next call
# print(result2)

# def run_pipeline(user_input):
#     stage1 = call_api_1(user_input)
#     stage1_output = extract(stage1)

#     stage2 = call_api_2(stage1_output)
#     stage2_output = extract(stage2)

#     stage3 = call_api_3(stage2_output)
    
#     return stage3