# 🧠 Wumpus World – Full-Stack AI Environment Simulator

A browser-based implementation of the classic **Wumpus World** from Artificial Intelligence, built using a **Flask backend + JavaScript frontend**.

This project simulates a knowledge-based agent environment where the player navigates an unknown cave using percepts (Breeze, Stench, Glitter, Scream, Bump) instead of direct visibility.

The backend acts as the authoritative game engine, while the frontend renders the world state returned by the server — similar to real AI simulation architectures.

---

## 🎮 Features

### Core Gameplay

* 4×4 hidden cave grid
* Randomized world generation
* Wumpus, pits, and gold placement
* Arrow shooting mechanic
* Exit and win condition
* Score tracking system

### Percept-Based Exploration

The player cannot see the world — only senses it:

| Percept   | Meaning              |
| --------- | -------------------- |
| 💨 Breeze | Pit nearby           |
| 💀 Stench | Wumpus nearby        |
| ✨ Glitter | Gold in current tile |
| 😱 Scream | Wumpus killed        |
| 🧱 Bump   | Hit wall             |

### UI/UX Features

* Fog-of-war exploration
* Dark / Light theme (Gold-themed)
* Score animations
* Arrow shooting effects
* Death & victory status banners
* Real-time percept panel

---

## 🏗 Architecture

This project follows a **state-driven client-server model**:

```
Frontend (JS UI)
      ↓ actions
Flask API Routes
      ↓
Game Engine (Python)
      ↓ state JSON
Frontend Renderer
```

The browser never controls the game logic —
the server maintains the authoritative world state.

This mirrors architectures used in:

* Multiplayer games
* Robotics simulations
* Reinforcement learning environments

---

## 🧩 Tech Stack

**Frontend**

* HTML
* CSS
* Vanilla JavaScript

**Backend**

* Python
* Flask

**Deployment**

* Render (Gunicorn WSGI server)

---

## 📂 Project Structure

```
wumpus_game/
│
├── app.py
├── engine/
│   └── game.py
│
├── static/
│   ├── style.css
│   └── game.js
│
├── templates/
│   └── index.html
│
├── requirements.txt
└── Procfile
```

---

## 🚀 Running Locally

### 1. Clone repo

```
git clone https://github.com/yourusername/wumpus-world.git
cd wumpus-world
```

### 2. Install dependencies

```
pip install -r requirements.txt
```

### 3. Run server

```
python app.py
```

Open in browser:

```
http://127.0.0.1:5000
```

---

## ☁ Deployment (Render)

This project is configured for Render:

**Procfile**

```
web: gunicorn app:app
```

**requirements.txt**

```
Flask
gunicorn
```

---

## 🧠 Educational Purpose

This project demonstrates:

* State synchronization between client and server
* REST API driven game logic
* Environment simulation for intelligent agents
* Separation of rendering vs world logic
* Debugging real production issues (serialization, caching, routing)

---

## 📜 Game Rules

* Find the gold
* Avoid pits
* Kill the Wumpus (optional)
* Return to the start
* Climb out to win

Scoring:

| Action      | Score |
| ----------- | ----- |
| Move        | -1    |
| Shoot       | -10   |
| Kill Wumpus | +500  |
| Grab Gold   | +1000 |
| Escape      | +2000 |
| Death       | -1000 |

---

## 👤 Author

Nitya Nama

---

## ⭐ Future Improvements

* AI agent autoplay
* Map reveal after death
* Sound effects
* Mobile controls
* Reinforcement learning integration

---

If you found this project interesting, consider starring ⭐ the repository!
