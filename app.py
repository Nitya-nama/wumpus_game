from flask import Flask, jsonify, request, render_template, session
from wumpus_engine import WumpusWorld
import uuid

app=Flask(__name__)
app.secret_key="secret123"
games={}

def get_game():
    gid=session.get("gid")
    if not gid or gid not in games:
        gid=str(uuid.uuid4())
        session["gid"]=gid
        games[gid]=WumpusWorld()
    return games[gid]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/start")
def start():
    gid=str(uuid.uuid4())
    session["gid"]=gid
    games[gid]=WumpusWorld()
    return jsonify(games[gid].state())

@app.route("/state")
def state():
    return jsonify(get_game().state())

@app.route("/move",methods=["POST"])
def move():
    g=get_game()
    g.move(request.json["direction"])
    return jsonify(g.state())

@app.route("/shoot",methods=["POST"])
def shoot():
    g=get_game()
    g.shoot(request.json["direction"])
    return jsonify(g.state())

@app.route("/grab",methods=["POST"])
def grab():
    g=get_game()
    g.grab()
    return jsonify(g.state())

@app.route("/climb",methods=["POST"])
def climb():
    g=get_game()
    g.climb()
    return jsonify(g.state())

@app.route("/reveal")
def reveal():
    return jsonify(get_game().reveal())

if __name__=="__main__":
    app.run(debug=True)
