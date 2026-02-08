from flask import Flask, render_template, request, jsonify, session
from engine.game import Game
import uuid

app = Flask(__name__)
app.secret_key = "supersecret"

games = {}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/new")
def new_game():
    gid = str(uuid.uuid4())
    games[gid] = Game()
    session["gid"] = gid
    return jsonify(games[gid].get_state())

@app.route("/move", methods=["POST"])
def move():
    gid = session.get("gid")
    direction = request.json["direction"]

    state = games[gid].move(direction)
    return jsonify(state)

@app.route("/shoot", methods=["POST"])
def shoot():
    gid = session.get("gid")
    state = games[gid].shoot()
    return jsonify(state)

@app.route("/grab", methods=["POST"])
def grab():
    gid = session.get("gid")
    state = games[gid].grab()
    return jsonify(state)

@app.route("/climb", methods=["POST"])
def climb():
    gid = session.get("gid")
    state = games[gid].climb()
    return jsonify(state)

if __name__ == "__main__":
    app.run(debug=True)
