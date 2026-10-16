from flask import Flask, render_template, jsonify
import json
import os

app = Flask(__name__)
DATA_FILE = "clicks.json"

ACHIEVEMENTS = [
    {"clicks": 1,       "name": "Первый клик",                 "icon": "👣"},
    {"clicks": 67,      "name": "Сиксевен",                    "icon": "🎯"},
    {"clicks": 100,     "name": "Новичок",                     "icon": "🌱"},
    {"clicks": 1000,    "name": "Разогрев",                    "icon": "🔥"},
    {"clicks": 1488,    "name": "Пасхалко",                    "icon": "🥚"},
    {"clicks": 10000,   "name": "Легенда",                     "icon": "👑"},
    {"clicks": 50000,   "name": "Преданный фанат",             "icon": "💜"},
    {"clicks": 100000,  "name": "ЗАЧЕМ ТЫ СТОЛЬКО КЛИКАЕШЬ??", "icon": "😱"},
    {"clicks": 1000000, "name": "GOD",                         "icon": "⚡"},
]


def load_clicks():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if "unlocked" not in data:
                data["unlocked"] = []
            if "total" not in data:
                data["total"] = 0
            if "visitors" not in data:
                data["visitors"] = 0
            return data
    return {"total": 0, "visitors": 0, "unlocked": []}


def save_clicks(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


@app.route("/")
def index():
    data = load_clicks()
    data["visitors"] += 1
    save_clicks(data)
    return render_template(
        "index.html",
        total=data["total"],
        visitors=data["visitors"],
        achievements=ACHIEVEMENTS,
        unlocked=data["unlocked"],
    )


@app.route("/donate", methods=["POST"])
def donate():
    data = load_clicks()
    data["total"] += 1

    new_unlocked = []
    for ach in ACHIEVEMENTS:
        if data["total"] >= ach["clicks"] and ach["clicks"] not in data["unlocked"]:
            data["unlocked"].append(ach["clicks"])
            new_unlocked.append(ach)

    save_clicks(data)
    return jsonify({
        "total": data["total"],
        "new": new_unlocked,
        "unlocked": data["unlocked"],
    })


if __name__ == "__main__":
    app.run(debug=True)