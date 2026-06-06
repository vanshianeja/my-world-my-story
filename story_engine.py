import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "google/gemma-4-31b-it:free"

def call_ai(prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    body = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    response = requests.post(API_URL, headers=headers, json=body)
    data = response.json()
    return data["choices"][0]["message"]["content"]

def build_prompt(name, quirk, characters, mood, genre, narrator):
    character_list = ""
    for char in characters:
        character_list += f"- {char['name']} ({char['role']}): {char['traits']}\n"

    prompt = f"""You are a literary novelist. Write Chapter 1 of a {genre} story.

PROTAGONIST: {name}
THEIR QUIRK: {quirk}

SUPPORTING CHARATERS: 
{character_list}

MOOD: {mood}
NARRATOR STYLE: {narrator}

RULES:
- Write in vivid, immersive prose - literary quality, not game-like
- Naturally weave the protagonist's quirk into the plot as a key moment
- Every supporting character must appear or be meaningfully mentioned
- Match the mood in every sentence - word choice, pacing, atmosphere
- End with a cliffhanger that makes the reader desperate for Chapter 2
- Write at least 500 words
- Do not use chapter title or headings, just pure prose

Begin the story now."""
    
    return prompt

def generate_story(name, quirk, characters, mood, genre, narrator):
    prompt = build_prompt(name, quirk, characters, mood, genre, narrator)
    return call_ai(prompt)
        

def continue_story(existing_story, user_direction):
    prompt = f"""Here is a story so far:

{existing_story}

The reader wants this to happen next: "{user_direction}"

Continue the story in the same style, mood, and voice.
Write the next chapter - at least 400 words.
End with another cliffhanger."""
    
    return call_ai(prompt)