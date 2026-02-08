from flask import Flask, render_template, request, jsonify, session
from engine.game import Game
import uuid

app = Flask(__name__)
app.secret_key = "supersecret"

# server-side memory store
games = {}

# ---------------- HOME ----------------
@app.route("/")
def index():
    return render_template("index.html")

# ---------------- NEW GAME ----------------
@app.route("/new")
def new_game():
    gid = str(uuid.uuid4())
    games[gid] = Game()
    session["gid"] = gid
    return jsonify(games[gid].state())

# ---------------- MOVE ----------------
@app.route("/move", methods=["POST"])
def move():
    gid = session.get("gid")
    if gid not in games:
        return jsonify({"error":"no game"}),400

    direction = request.json["direction"]
    return jsonify(games[gid].move(direction))

# ---------------- SHOOT ----------------
@app.route("/shoot", methods=["POST"])
def shoot():
    gid = session.get("gid")
    direction = request.json["direction"]
    return jsonify(games[gid].shoot(direction))

# ---------------- GRAB ----------------
@app.route("/grab", methods=["POST"])
def grab():
    gid = session.get("gid")
    return jsonify(games[gid].grab())

# ---------------- CLIMB ----------------
@app.route("/climb", methods=["POST"])
def climb():
    gid = session.get("gid")
    return jsonify(games[gid].climb())

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)
