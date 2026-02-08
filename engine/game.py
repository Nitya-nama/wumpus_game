import random

SIZE = 4

class Game:
    def __init__(self):
        self.player = [0,0]
        self.arrow = True
        self.gold = False
        self.alive = True
        self.score = 0
        self.generate_world()

    def generate_world(self):
        self.pits = set()
        self.wumpus = (random.randint(1,3), random.randint(1,3))
        self.gold_pos = (random.randint(1,3), random.randint(1,3))

        while len(self.pits) < 3:
            p = (random.randint(0,3), random.randint(0,3))
            if p != (0,0):
                self.pits.add(p)

    def move(self, direction):
        if not self.alive:
            return self.get_state()

        x,y = self.player

        if direction=="up": x-=1
        if direction=="down": x+=1
        if direction=="left": y-=1
        if direction=="right": y+=1

        if 0<=x<4 and 0<=y<4:
            self.player=[x,y]
            self.score-=1

        if tuple(self.player) in self.pits:
            self.alive=False
            self.score-=1000

        if tuple(self.player)==self.wumpus:
            self.alive=False
            self.score-=1000

        return self.get_state()

    def grab(self):
        if tuple(self.player)==self.gold_pos:
            self.gold=True
            self.score+=1000
        return self.get_state()

    def shoot(self):
        if self.arrow:
            self.arrow=False
            self.score-=10
            if self.player[0]==self.wumpus[0] or self.player[1]==self.wumpus[1]:
                self.wumpus=(-1,-1)
        return self.get_state()

    def climb(self):
        if self.player==[0,0] and self.gold:
            self.score+=1000
            self.alive=False
        return self.get_state()

    def get_state(self):
        return {
            "player":self.player,
            "alive":self.alive,
            "score":self.score,
            "gold":self.gold
        }
