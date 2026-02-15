from flask import Flask, render_template, request, jsonify
import whisper
import os
import requests
import json

app = Flask(__name__)

# ------------------------------------------------
# LOAD SCHEMES FROM JSON (ONLY SOURCE OF DATA)
# ------------------------------------------------
with open("schemes.json", "r") as f:
    SCHEMES_DATA = json.load(f)

# ------------------------------------------------
# LOAD WHISPER MODEL
# ------------------------------------------------
model = whisper.load_model("small")

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"

# ------------------------------------------------
# HOME PAGE → SHOW CATEGORIES
# ------------------------------------------------
@app.route("/")
def home():
    return render_template("index.html", schemes=SCHEMES_DATA)

# ------------------------------------------------
# CATEGORY PAGE → SHOW ALL SCHEMES
# ------------------------------------------------
@app.route("/category/<category_key>")
def category_page(category_key):
    category = SCHEMES_DATA.get(category_key)

    if not category:
        return "Category Not Found"

    return render_template(
        "category.html",
        category_key=category_key,
        category_name=category["name"],
        schemes=category.get("schemes", {})
    )

# ------------------------------------------------
# SCHEME DETAIL PAGE
# ------------------------------------------------
@app.route("/scheme/<category_key>/<scheme_id>")
def scheme_detail(category_key, scheme_id):
    category = SCHEMES_DATA.get(category_key)

    if not category:
        return "Category Not Found"

    schemes = category.get("schemes", {})
    scheme = schemes.get(scheme_id)

    if not scheme:
        return "Scheme Not Found"

    return render_template("scheme.html", scheme=scheme)

# ------------------------------------------------
# KEYWORD FILTER
# ------------------------------------------------
ALLOWED_KEYWORDS = [
    "scheme", "yojana", "pm", "government", "bharat",
    "kisan", "loan", "subsidy", "ayushman", "mudra",
    "agriculture", "farmer", "education", "scholarship",
    "ration", "bank", "jan dhan", "health", "insurance",
    "treatment", "hospital", "pension", "benefit",
    "help", "support", "registration"
]

def is_related(text):
    if not text:
        return False
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in ALLOWED_KEYWORDS)

# ------------------------------------------------
# TEXT AI ROUTE
# ------------------------------------------------
@app.route("/ask_text", methods=["POST"])
def ask_text():
    data = request.get_json()
    user_text = data.get("prompt")
    language = data.get("language", "English")

    if not user_text:
        return jsonify({"response": "Please enter a question."})

    if not is_related(user_text):
        return jsonify({
            "response": "❌ This platform only provides information about Indian Government Schemes."
        })

    indian_prompt = f"""
You are Bharat AI Sathi – official AI assistant for Indian Government Schemes.

Answer completely in {language}.

Follow format:
1. Scheme Name
2. Objective
3. Eligibility
4. Benefits
5. How to Apply
6. Required Documents
7. What You Should Do Next
8. Official Helpline

Keep answer under 220 words.

User question:
{user_text}
"""

    response = requests.post(OLLAMA_URL, json={
        "model": "phi3",
        "prompt": indian_prompt,
        "stream": False
    })

    ai_reply = response.json().get("response", "Sorry, unable to generate response.")
    return jsonify({"response": ai_reply})

# ------------------------------------------------
# RUN
# ------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
