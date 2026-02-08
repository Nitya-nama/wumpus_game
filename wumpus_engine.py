import random

class WumpusWorld:
    def __init__(self, size=4):
        self.size=size
        self.player_pos=(0,0)
        self.wumpus=self.rand()
        self.gold=self.rand()
        self.pits={self.rand() for _ in range(2)}

        self.arrow=1
        self.has_gold=False
        self.game_over=False
        self.score=0
        self.message=""

    def rand(self):
        while True:
            p=(random.randint(0,self.size-1),random.randint(0,self.size-1))
            if p!=(0,0):
                return p

    def percepts(self):
        r,c=self.player_pos
        adj={(r+1,c),(r-1,c),(r,c+1),(r,c-1)}
        p=[]
        if self.wumpus in adj: p.append("stench")
        if any(x in adj for x in self.pits): p.append("breeze")
        if self.player_pos==self.gold: p.append("glitter")
        return p

    def move(self,d):
        if self.game_over: return
        r,c=self.player_pos
        if d=="up" and r<3: r+=1
        if d=="down" and r>0: r-=1
        if d=="left" and c>0: c-=1
        if d=="right" and c<3: c+=1
        self.player_pos=(r,c)
        self.score-=1
        self.check()

    def shoot(self,d):
        if self.arrow==0: return
        self.arrow=0
        r,c=self.player_pos
        while 0<=r<4 and 0<=c<4:
            if (r,c)==self.wumpus:
                self.wumpus=None
                self.message="You killed the Wumpus!"
                return
            if d=="up": r+=1
            if d=="down": r-=1
            if d=="left": c-=1
            if d=="right": c+=1

    def check(self):
        if self.player_pos in self.pits:
            self.game_over=True
            self.score-=100
            self.message="You fell into a pit!"
        elif self.player_pos==self.wumpus:
            self.game_over=True
            self.score-=100
            self.message="Wumpus ate you!"
        elif self.player_pos==self.gold and not self.has_gold:
            self.has_gold=True
            self.gold=None
            self.score+=1000
            self.message="Gold collected! Return to start."
        elif self.player_pos==(0,0) and self.has_gold:
            self.game_over=True
            self.message="You escaped with the gold!"

    def state(self):
        return {
            "position":self.player_pos,
            "percepts":self.percepts(),
            "score":self.score,
            "arrow":self.arrow,
            "game_over":self.game_over,
            "message":self.message
        }
