from flask import Flask, jsonify, request, session, render_template
import uuid
from wumpus_engine import WumpusWorld
from ai_agent import WumpusAgent

app = Flask(__name__)
app.secret_key="secret"

games={}
agents={}

def get_game():
    gid=session.get("gid")
    if not gid or gid not in games:
        gid=str(uuid.uuid4())
        session["gid"]=gid
        games[gid]=WumpusWorld()
        agents[gid]=WumpusAgent()
    return games[gid],agents[gid]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/start")
def start():
    session.clear()
    g,a=get_game()
    return jsonify(g.state())

@app.route("/state")
def state():
    g,a=get_game()
    a.update(g.player_pos,g.percepts())
    s = g.state()
    s["safe"] = list(a.safe)
    s["visited"] = list(a.visited)
    return jsonify(s)

@app.route("/move",methods=["POST"])
def move():
    g,a=get_game()
    g.move(request.json["direction"])
    a.update(g.player_pos,g.percepts())
    return jsonify(g.state())

@app.route("/shoot",methods=["POST"])
def shoot():
    g,a=get_game()
    g.shoot(request.json["direction"])
    return jsonify(g.state())

@app.route("/auto")
def auto():
    g,a=get_game()
    m=a.next_move(g.player_pos)
    if m:
        r,c=g.player_pos
        nr,nc=m
        if nr>r: g.move("up")
        elif nr<r: g.move("down")
        elif nc>c: g.move("right")
        elif nc<c: g.move("left")
    return jsonify(g.state())
