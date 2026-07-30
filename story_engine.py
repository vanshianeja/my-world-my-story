import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "google/gemma-4-31b-it:free"

MODELS = [
    "google/gemma-4-31b-it:free",
    "google/gemma-4-26b-a4b-it:free",
    "mistralai/devstral-small:free",
    "qwen/qwen3-8b:free",
]

def call_ai(prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    for model in MODELS:
        body = {
            "model": model,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
        response = requests.post(API_URL, headers=headers, json=body)
        data = response.json()
        
        if "choices" in data:
            return data["choices"][0]["message"]["content"]
    
    return "Sorry, all AI models are currently busy. Please try again in a moment."

def build_prompt(name, quirk, characters, mood, genre, narrator, predetails=""):
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

{f"ADDITIONAL DETAILS THE USER WANTS INCLUDED:{chr(10)}{predetails}{chr(10)}{chr(10)}" if predetails else ""}Begin the story now."""
    
    return prompt

def generate_title(story_text, genre, mood):
    prompt = f"""Based on this story excerpt, generate a short, evocative, literary title.

GENRE: {genre}
MOOD: {mood}
STORY EXCERPT: {story_text[:500]}

Rules:
- 2 to 5 words maximum
- Should feel like a real novel title
- Mysterious, poetic, or intriguing
- Do NOT use the protagonist's name
- Return ONLY the title, nothing else, no quotes, no explanation

Examples of good titles: The Midnight Theory, Last Train to Nowhere, What the Rain Remembers, Letters She Never Sent"""

    return call_ai(prompt)


def generate_story(name, quirk, characters, mood, genre, narrator, predetails=""):
    prompt = build_prompt(name, quirk, characters, mood, genre, narrator, predetails)
    story = call_ai(prompt)
    title = generate_title(story, genre, mood)
    return story, title

def continue_story(existing_story, user_direction):
    prompt = f"""Here is a story so far:

{existing_story}

The reader wants this to happen next: "{user_direction}"

Continue the story in the same style, mood, and voice.
Write the next chapter - at least 400 words.
End with another cliffhanger."""
    
    return call_ai(prompt)