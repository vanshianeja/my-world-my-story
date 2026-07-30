from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from story_engine import generate_story, continue_story
from word_lookup import lookup_word
from database import get_db, init_db
from pdf_generator import generate_pdf
from cover_generator import generate_cover
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

#Initialize database on startup
init_db()

#==== AUTH ROUTES ====

@app.route("/")
def index():
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        db = get_db()
        user = db.execute(
            "SELECT * FROM users WHERE email = ?", (email,)
        ).fetchone()
        db.close()

        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            session["user_name"] = user["name"]
            return redirect(url_for("dashboard"))
    
        return render_template("login_html", error="Invalid email or password.")

    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        hashed = generate_password_hash(password)

        try:
            db = get_db()
            db.execute(
                "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                (name, email, hashed)
            )
            db.commit()
            db.close()
            return redirect(url_for("login"))
        except Exception as e:
            return render_template("signup.html", error="Email already exists.")
        
    return render_template("signup.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# ==== DASHBOARD ====
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))
    
    db = get_db()
    stories = db.execute(
        "SELECT * FROM stories WHERE user_id = ? ORDER BY updated_at DESC",
        (session["user_id"],)
    ).fetchall()
    db.close()

    return render_template("dashboard.html",
                           stories=stories,
                           user_name=session["user_name"])

# ==== STORY APP ====

@app.route("/app")
def story_app():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return render_template("index.html")

# ==== API ROUTES ====

@app.route("/generate", methods=["POST"])
def generate():
    if "user_id" not in session:
        return jsonify({"error": "Not logged in"}), 401
    
    data = request.get_json()
    name = data["name"]
    quirk = data["quirk"]
    characters = data["characters"]
    mood = data["mood"]
    genre = data["genre"]
    narrator = data["narrator"]
    predetails = data.get("predetails", "")

    story, title = generate_story(name, quirk, characters, mood, genre, narrator, predetails)

    # Auto-save story to database
    db = get_db()
    cursor = db.execute(
        """INSERT INTO stories (user_id, title, genre, mood, narrator, full_content)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (session["user_id"], f"{name}'s Story", genre, mood, narrator, story)
    )
    story_id = cursor.lastrowid
    db.commit()
    db.close()

    return jsonify({"story": story, "story_id": story_id, "title": title})

@app.route("/continue", methods=["POST"])
def continue_chapter():
    if "user_id" not in session:
        return jsonify({"error": "Not logged in"}), 401

    data = request.get_json()
    existing_story = data["existing_story"]
    user_direction = data["user_direction"]
    story_id = data.get("story_id")

    next_chapter = continue_story(existing_story, user_direction)

    # Update story in database
    if story_id:
        full_content = existing_story + "\n\n" + next_chapter
        db = get_db()
        db.execute(
            """UPDATE stories SET full_content = ?, updated_at = CURRENT_TIMESTAMP
               WHERE id = ? AND user_id = ?""",
            (full_content, story_id, session["user_id"])
        )
        db.commit()
        db.close()

    return jsonify({"story": next_chapter})

@app.route("/lookup", methods=["POST"])
def lookup():

    data = request.get_json()
    word = data["word"]
    result = lookup_word(word)
    return jsonify(result)

@app.route("/story/<int:story_id>")
def view_story(story_id):
    if "user_id" not in session:
        return redirect(url_for("login"))
    
    db = get_db()
    story = db.execute(
        "SELECT * FROM stories WHERE id = ? AND user_id = ?",
        (story_id, session["user_id"])
    ).fetchone()
    db.close()

    if not story:
        return redirect(url_for("dashboard"))
    
    return render_template("index.html",
                           preload_story=dict(story),
                           story_id=story_id)

@app.route("/delete_story/<int:story_id>", methods=["POST"])
def delete_story(story_id):
    if "user_id" not in session:
        return jsonify({"error": "Not logged in"}), 401
    
    db = get_db()
    db.execute(
        "DELETE FROM stories WHERE id = ? AND user_id = ?",
        (story_id, session["user_id"])
    )
    db.commit()
    db.close()

    return redirect(url_for("dashboard"))

@app.route("/download_pdf/<int:story_id>")
def download_pdf(story_id):
    if "user_id" not in session:
        return redirect(url_for("login"))
    
    db = get_db()
    story = db.execute(
        "SELECT * FROM stories WHERE id = ? AND user_id = ?",
        (story_id, session["user_id"])
    ).fetchone()
    db.close()
    
    if not story:
        return redirect(url_for("dashboard"))
    
    pdf_bytes = generate_pdf(
        story["title"],
        story["genre"],
        story["mood"],
        story["full_content"]
    )
    
    from flask import Response
    return Response(
        pdf_bytes,
        mimetype="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename={story['title']}.pdf"
        }
    )

@app.route("/story_cover/<int:story_id>")
def story_cover(story_id):
    if "user_id" not in session:
        return "", 401
    
    db = get_db()
    story = db.execute(
        "SELECT * FROM stories WHERE id = ? AND user_id = ?",
        (story_id, session["user_id"])
    ).fetchone()
    db.close()
    
    if not story:
        return "", 404
    
    svg = generate_cover(
        story["genre"] or "Fantasy",
        story["mood"] or "Dreamy",
        story["title"]
    )
    
    from flask import Response
    return Response(svg, mimetype="image/svg+xml")

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
