"""Stream one roleplay reply from TavernAPI with the official OpenAI Python SDK.

    pip install openai
    export TAVERNAPI_API_KEY=sk-tav-...        # PowerShell: $env:TAVERNAPI_API_KEY="sk-tav-..."
    python python_openai.py
"""
import os

from openai import OpenAI

client = OpenAI(base_url="https://tavernapi.com/v1", api_key=os.environ["TAVERNAPI_API_KEY"])

stream = client.chat.completions.create(
    model="gemini-4-argon",
    messages=[
        {"role": "system", "content": "You are Mira, a sharp-tongued tavern keeper. Stay in character."},
        {"role": "user", "content": "A stranger walks in out of the rain and asks for a room."},
    ],
    max_tokens=400,
    stream=True,
)
for chunk in stream:
    if chunk.choices and chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
print()
