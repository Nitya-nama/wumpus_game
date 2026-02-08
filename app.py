from flask import Flask, jsonify, request, render_template, session
from wumpus_engine import WumpusWorld
import uuid

app = Flask(__name__)
app.secret_key = "wumpus-secret-key"   # required for session storage

# Store games per user session
games = {}

# --------------------------------------------------
# Utility
# --------------------------------------------------

def get_game():
    """Return current user's game instance"""
    gid = session.get("game_id")

    if not gid or gid not in games:
        gid = str(uuid.uuid4())
        session["game_id"] = gid
        games[gid] = WumpusWorld()

    return games[gid]


def response(game):
    """Standard JSON response format"""
    return jsonify({
        "position": game.player_pos,
        "percepts": game.perceptions(),
        "arrow": game.arrow,
        "gold": game.has_gold,
        "game_over": game.game_over,
        "message": game.message
    })


# --------------------------------------------------
# Routes
# --------------------------------------------------

@app.route("/")
def home():
    return render_template("index.html")


# Start / Reset game
@app.route("/start", methods=["GET"])
def start():
    gid = str(uuid.uuid4())
    session["game_id"] = gid
    games[gid] = WumpusWorld()
    return response(games[gid])


# Get state
@app.route("/state", methods=["GET"])
def state():
    game = get_game()
    return response(game)


# Move player
@app.route("/move", methods=["POST"])
def move():
    game = get_game()
    data = request.get_json()

    if not data or "direction" not in data:
        return jsonify({"error": "Direction required"}), 400

    direction = data["direction"].lower()

    if game.game_over:
        return response(game)

    game.move(direction)
    return response(game)


# Shoot arrow
@app.route("/shoot", methods=["POST"])
def shoot():
    game = get_game()
    data = request.get_json()

    if not data or "direction" not in data:
        return jsonify({"error": "Direction required"}), 400

    direction = data["direction"].lower()

    if game.game_over:
        return response(game)

    game.shoot(direction)
    return response(game)


# --------------------------------------------------
# Debug endpoint (optional — remove in production)
# Reveals full map after game over
# --------------------------------------------------

@app.route("/reveal", methods=["GET"])
def reveal():
    game = get_game()

    return jsonify({
        "player": game.player_pos,
        "wumpus": game.wumpus_pos,
        "gold": game.gold_pos,
        "pits": list(game.pits_pos)
    })


# --------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)
