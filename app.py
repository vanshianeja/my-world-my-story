from flask import Flask, request, jsonify, render_template
from story_engine import generate_story, continue_story
from word_lookup import lookup_word

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()

    name = data["name"]
    quirk = data["quirk"]
    characters = data["characters"]
    mood = data["mood"]
    genre = data["genre"]
    narrator = data["narrator"]

    story = generate_story(name, quirk, characters, mood, genre, narrator)
    return jsonify({"story": story})

@app.route("/continue", methods=["POST"])
def continue_chapter():

    data = request.get_json()

    existing_story = data["existing_story"]
    user_direction = data["user_direction"]

    next_chapter = continue_story(existing_story, user_direction)

    return jsonify({"story": next_chapter})

@app.route("/lookup", methods=["POST"])
def lookup():

    data = request.get_json()
    word = data["word"]

    result = lookup_word(word)

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)


