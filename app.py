from flask import Flask, jsonify, request, render_template, session
from wumpus_engine import WumpusWorld
from ai_agent import WumpusAgent
from flask_cors import CORS

import uuid

app = Flask(__name__)
app.secret_key = "secret123"

# IMPORTANT FOR VERCEL FRONTEND COOKIES
app.config.update(
    SESSION_COOKIE_SAMESITE="None",
    SESSION_COOKIE_SECURE=True
)

# Allow cross-origin requests with credentials
CORS(app,
     supports_credentials=True,
     origins=["https://wumpus-game.vercel.app", "http://localhost:3000", "http://127.0.0.1:5500"])


games = {}
agents = {}

# ---------------- GAME SESSION ----------------

def get_game():
    gid = session.get("gid")

    if not gid or gid not in games:
        gid = str(uuid.uuid4())
        session["gid"] = gid
        games[gid] = WumpusWorld()
        agents[gid] = WumpusAgent()

    return games[gid], agents[gid]


# ---------------- ROUTES ----------------

@app.route("/")
def home():
    return {
        "service": "Wumpus AI backend",
        "status": "running",
        "message": "Use /state endpoint"
    }



@app.route("/start")
def start():
    gid = str(uuid.uuid4())
    session["gid"] = gid
    games[gid] = WumpusWorld()
    agents[gid] = WumpusAgent()

    g = games[gid]
    return jsonify(g.state())


@app.route("/state")
def state():
    g, a = get_game()

    # agent updates knowledge
    a.update(g.player_pos, g.perceptions())

    s = g.state()
    s["safe"] = list(a.safe)
    s["visited"] = list(a.visited)

    return jsonify(s)


@app.route("/move", methods=["POST"])
def move():
    g, a = get_game()
    data = request.get_json()
    if not data or "direction" not in data:
        return jsonify({"error":"Direction missing"}),400
    direction = data["direction"]


    g.move(direction)
    a.update(g.player_pos, g.perceptions())

    return jsonify(g.state())


@app.route("/shoot", methods=["POST"])
def shoot():
    g, a = get_game()
    data = request.get_json()
    if not data or "direction" not in data:
        return jsonify({"error":"Direction missing"}),400
    direction = data["direction"]


    g.shoot(direction)
    a.update(g.player_pos, g.perceptions())

    return jsonify(g.state())


@app.route("/grab", methods=["POST"])
def grab():
    g, a = get_game()
    g.grab()
    return jsonify(g.state())


@app.route("/climb", methods=["POST"])
def climb():
    g, a = get_game()
    g.climb()
    return jsonify(g.state())


# -------- AUTO SOLVE (AI AGENT) --------

@app.route("/auto")
def auto():
    g, a = get_game()

    if g.game_over:
        state = g.state()
    state["safe"] = list(a.safe)
    state["visited"] = list(a.visited)
    return jsonify(state)


    a.update(g.player_pos, g.perceptions())
    move = a.next_move(g.player_pos)

    if move:
        r, c = g.player_pos
        nr, nc = move

        if nr > r: g.move("up")
        elif nr < r: g.move("down")
        elif nc > c: g.move("right")
        elif nc < c: g.move("left")

    return jsonify(g.state())


# -------- REVEAL MAP --------

@app.route("/reveal")
def reveal():
    g, _ = get_game()
    return jsonify(g.reveal())


# ---------------- RUN ----------------

if __name__=="__main__":
    app.run(host="0.0.0.0", port=10000)
