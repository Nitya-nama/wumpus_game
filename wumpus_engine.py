import random

class WumpusWorld:
    def __init__(self, size=4):
        self.size=size
        self.player_pos=(0,0)
        self.wumpus=self.rand_cell()
        self.gold=self.rand_cell()
        self.pits={self.rand_cell() for _ in range(2)}
        self.has_gold=False
        self.arrow=1
        self.score=0
        self.game_over=False

    def rand_cell(self):
        while True:
            p=(random.randint(0,3),random.randint(0,3))
            if p!=(0,0):
                return p

    def percepts(self):
        r,c=self.player_pos
        adj={(r+1,c),(r-1,c),(r,c+1),(r,c-1)}
        p=[]
        if self.wumpus in adj: p.append("stench")
        if any(x in self.pits for x in adj): p.append("breeze")
        if self.gold==self.player_pos: p.append("glitter")
        return p

    def move(self,d):
        if self.game_over: return
        r,c=self.player_pos
        if d=="up": r=min(3,r+1)
        if d=="down": r=max(0,r-1)
        if d=="right": c=min(3,c+1)
        if d=="left": c=max(0,c-1)
        self.player_pos=(r,c)
        self.score-=1

        if self.player_pos in self.pits:
            self.game_over=True
            self.score-=100
        if self.player_pos==self.wumpus:
            self.game_over=True
            self.score-=100

        if self.player_pos==self.gold:
            self.has_gold=True
            self.score+=1000

    def shoot(self,d):
        if self.arrow==0: return
        self.arrow=0
        r,c=self.player_pos

        while 0<=r<4 and 0<=c<4:
            if (r,c)==self.wumpus:
                self.wumpus=None
                self.score+=500
                return
            if d=="up": r+=1
            if d=="down": r-=1
            if d=="right": c+=1
            if d=="left": c-=1

    def state(self):
        return {
            "position":self.player_pos,
            "percepts":self.percepts(),
            "score":self.score,
            "arrow":self.arrow,
            "game_over":self.game_over,
            "message":"GAME OVER" if self.game_over else ""
        }
