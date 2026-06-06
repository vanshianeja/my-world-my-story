import requests

def lookup_word(word):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()[0]

        meaning = data["meanings"][0]
        definition = meaning["definitions"][0]["definition"]
        synonyms = meaning["definitions"][0].get("synonyms", [])
        part_of_speech = meaning["partOfSpeech"]

        return {
            "word": word,
            "part_of_speech": part_of_speech,
            "definition": definition,
            "synonyms": synonyms[:4]
        }
    
    return {
        "word": word,
        "part_of_speech": "",
        "definition": "Word not found. Please check the spelling.",
        "synonyms": []
    }
