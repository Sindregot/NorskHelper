from flask import Flask, request, jsonify, render_template
import pandas as pd
import random
import json
import os

app = Flask(__name__)

# Base directory of this file
BASE_DIR = os.path.dirname(__file__)

# Load CSV with absolute path
df = pd.read_csv(os.path.join(BASE_DIR, "static", "words.csv"))
words = df.to_dict(orient="records")

# Leaderboard file with absolute path
LEADERBOARD_FILE = os.path.join(BASE_DIR, "leaderboard.json")

# Load leaderboard from file if exists, else empty list
if os.path.exists(LEADERBOARD_FILE):
    with open(LEADERBOARD_FILE, "r") as f:
        leaderboard = json.load(f)
else:
    leaderboard = []

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_word")
def get_word():
    return jsonify(random.choice(words))

@app.route("/check_answer", methods=["POST"])
def check_answer():
    data = request.get_json()
    answer = data["answer"].strip().lower()
    correct_answer = next((w["english"] for w in words if w["norwegian"] == data["current_word"]), "")
    streak = data["streak"]
    lives = data["lives"]

    if answer == correct_answer.lower():
        streak += 1
        correct = True
    else:
        lives -= 1
        correct = False
        if lives <= 0:
            # Only add score if it's higher than any in current top 5
            if len(leaderboard) < 5 or streak > min(leaderboard):
                leaderboard.append(streak)
                leaderboard.sort(reverse=True)
                leaderboard[:] = leaderboard[:5]  # keep top 5
                # Save to JSON
                with open(LEADERBOARD_FILE, "w") as f:
                    json.dump(leaderboard, f)
            streak = 0
            lives = 3

    return jsonify({"correct": correct, "answer": correct_answer, "streak": streak, "lives": lives})

@app.route("/get_leaderboard")
def get_leaderboard():
    top_scores = sorted(leaderboard, reverse=True)[:5]
    return jsonify({"leaderboard": top_scores})

if __name__ == "__main__":
    app.run(debug=True)
