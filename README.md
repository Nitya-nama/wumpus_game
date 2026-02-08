# 🧠 Wumpus World — Full Stack Intelligent Agent Simulator

An interactive web-based implementation of the classic **Wumpus World AI environment** from Artificial Intelligence (Russell & Norvig).

This project is not just a game — it is a **knowledge-based agent simulation platform** demonstrating logical inference, environment perception, and autonomous decision making.

The system allows:

* Human player interaction
* Autonomous AI agent solving the cave
* Real-time reasoning visualization
* Reward-based performance evaluation

---

## 🎯 Objectives

* Model a partially observable environment
* Implement a knowledge-based logical agent
* Demonstrate safe/unsafe cell reasoning
* Provide an interactive full-stack visualization
* Show AI decision-making behavior step-by-step

---

## 🏗️ System Architecture

Frontend (HTML + CSS + JavaScript)
⬇
Flask REST API (Controller Layer)
⬇
Wumpus Environment Engine (Environment Model)
⬇
Logical Inference Agent (Knowledge Base + Reasoning)

---

## 🧩 Features

### Game Environment

* 4×4 cave grid
* Hidden (fog-of-war) cells
* Random placement of:

  * Wumpus
  * Gold
  * Pits
* Player actions:

  * Move
  * Shoot Arrow
  * Grab Gold
  * Climb Out

### Perception System

The agent receives percepts instead of full state:

| Percept | Meaning                 |
| ------- | ----------------------- |
| Stench  | Wumpus in adjacent cell |
| Breeze  | Pit nearby              |
| Glitter | Gold in current cell    |

---

### Reward Model (AI Utility Function)

| Action/Event     | Score |
| ---------------- | ----- |
| Move             | −1    |
| Shoot arrow      | −10   |
| Kill Wumpus      | +500  |
| Grab Gold        | +1000 |
| Death            | −1000 |
| Escape with Gold | Win   |

---

### Autonomous AI Agent

The agent uses **logical inference rules**:

* No breeze ⇒ Adjacent cells contain no pits
* No stench ⇒ Adjacent cells contain no wumpus
* Breeze ⇒ At least one neighboring pit
* Stench ⇒ Possible wumpus location
* Deduction ⇒ Safe vs unsafe cells

The AI can automatically solve the cave using reasoning instead of guessing.

---

### User Interface

* Fog-of-war exploration
* Real-time perception display
* Score tracker
* Auto-solve mode
* Dark / Light purple themed UI
* Animated theme toggle
* Session-based independent caves

---

## 📁 Project Structure

```
wumpus_fullstack/
│── app.py                 # Flask API
│── wumpus_engine.py       # Environment model
│── ai_agent.py            # Logical inference agent
│
├── templates/
│   └── index.html         # UI layout
│
└── static/
    ├── style.css          # Themed UI styling
    └── game.js            # Frontend logic
```

---

## ⚙️ Installation & Run

### 1. Clone project

```
git clone <repo-url>
cd wumpus_fullstack
```

### 2. Install dependencies

```
pip install flask
```

### 3. Run server

```
python app.py
```

### 4. Open browser

```
http://127.0.0.1:5000
```

---

## 🤖 AI Demonstration

Click **Auto Solve** to watch the knowledge-based agent:

* explore safely
* deduce hazards
* find gold
* escape optimally

This shows classical AI reasoning instead of random search.

---

## 🧠 Concepts Demonstrated

* Intelligent Agents
* Knowledge Representation
* Propositional Logic Inference
* Partially Observable Environments
* Sequential Decision Making
* Utility Based Evaluation
* Human-AI Interaction

---

## 📚 Educational Relevance

This project visually demonstrates concepts taught in:

* Artificial Intelligence
* Intelligent Agents
* Knowledge-Based Systems
* Autonomous Robotics Planning

---

## 🚀 Future Improvements

* Bayesian probabilistic Wumpus agent
* Reinforcement learning agent
* Larger grid environments
* Multi-agent competition mode

---

## 👩‍💻 Author

Developed as a Full-Stack AI Simulation Project
Demonstrating logical reasoning in interactive environments.

---

## 📝 License

Educational / Academic Use
