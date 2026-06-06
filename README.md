# My World, My Story 📖

An AI-powered personaliized story generator. Tell us about yourself and the people in your life - we'll write your story.

## Features
- Personalized stories based on real people in your life
- Multiple genres: Romcom, Suspense, fantasy, Sci-Fi, Horror, Mystery
- Multiple narrator voices and moods
- Continue your story chapter by chapter
- Plot twist button for unexpected turns
- Word lookup - get definitions without leaving the app
- Save your story as a text file

## Tech Stack
- Python + Flask (backend)
- HTML, CSS, JavaScript (frontend)
- OpenRouter API (AI story generation)
- Free Dictionary API (word lookup)

## How to Run
1. Clone the repo
2. Create a virtual environment: `python -m venv venv`
3. Activate it: `venv\Scripts\activate`
4. Install packages: `pip install -r requirements.txt`
5. Create a `.env` file with your `OPENROUTER_API_KEY`
6. Run: `python app.py`
7. Open `http://127.0.0.1:5000`