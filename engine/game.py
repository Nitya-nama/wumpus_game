import random

SIZE = 4

DIR = {
    "up":(-1,0),
    "down":(1,0),
    "left":(0,-1),
    "right":(0,1)
}

class Game:
    def __init__(self):
        self.reset()

    def reset(self):
        self.player = (3,0)
        self.arrow = True
        self.has_gold = False
        self.alive = True
        self.won = False
        self.score = 0
        self.scream = False
        self.bump = False

        cells=[(i,j) for i in range(4) for j in range(4) if (i,j)!=(3,0)]
        self.wumpus=random.choice(cells)
        cells.remove(self.wumpus)
        self.gold=random.choice(cells)

        self.pits=set(random.sample([c for c in cells if c!=self.gold],3))

        self.visited=set([self.player])
        
    def shoot(self, direction):
        if not self.arrow:
            return self.state()

        self.arrow = False
        self.score -= 10

        px, py = self.player
        wx, wy = self.wumpus

        if direction == "up" and py == wy and wx < px:
            self.kill()
        if direction == "down" and py == wy and wx > px:
            self.kill()
        if direction == "left" and px == wx and wy < py:
            self.kill()
        if direction == "right" and px == wx and wy > py:
            self.kill()

        return self.state()
    

    # ---------- PERCEPT SYSTEM ----------
    def percepts(self,pos):
        x,y=pos
        adj=[(x+1,y),(x-1,y),(x,y+1),(x,y-1)]

        breeze=any(p in self.pits for p in adj)
        stench=self.wumpus in adj
        glitter=pos==self.gold and not self.has_gold

        return {
            "breeze":breeze,
            "stench":stench,
            "glitter":glitter,
            "scream":self.scream,
            "bump":self.bump
        }
    def state(self):
        return {
            "player": list(self.player),
            "visited": [list(p) for p in self.visited],
            "alive": self.alive,
            "won": self.won,
            "score": self.score,
            "has_gold": self.has_gold,
            "percepts": {
                "breeze": self.percepts(self.player)["breeze"],
                "stench": self.percepts(self.player)["stench"],
                "glitter": self.percepts(self.player)["glitter"],
                "scream": self.percepts(self.player)["scream"],
                "bump": self.percepts(self.player)["bump"]
            }
        }

    # ---------- MOVE ----------
    def move(self,direction):
        if not self.alive: return self.state()

        dx,dy=DIR[direction]
        x,y=self.player
        nx,ny=x+dx,y+dy

        self.bump=False
        self.scream=False
        self.score-=1

        if not (0<=nx<4 and 0<=ny<4):
            self.bump=True
            return self.state()

        self.player=(nx,ny)
        self.visited.add(self.player)

        if self.player in self.pits:
            self.alive=False
            self.score-=1000

        if self.player==self.wumpus:
            self.alive=False
            self.score-=1000

        return self.state()
    
    def kill(self):
        self.wumpus = (-1,-1)
        self.scream = True
        self.score += 500      # reward for killing Wumpus
        
    def grab(self):
    # player standing on gold
        if self.player == self.gold and not self.has_gold:
            self.has_gold = True
            self.score += 1000
        return self.state()
    
    def climb(self):
    # start tile is (3,0)
        if self.player == (3,0):
            if self.has_gold:
                self.won = True
                self.alive = False
                self.score += 2000
        return self.state()


