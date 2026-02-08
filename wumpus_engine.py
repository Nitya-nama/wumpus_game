import random

class WumpusWorld:

    def __init__(self,size=4):
        self.size=size
        self.player_pos=(0,0)
        self.arrow=1
        self.has_gold=False
        self.game_over=False
        self.score=0
        self.message="You enter the cave."
        self.last_event="start"
        self.senses=[]

        occupied=set()

        self.wumpus_pos=self.rand_cell(occupied)
        occupied.add(self.wumpus_pos)

        self.gold_pos=self.rand_cell(occupied)
        occupied.add(self.gold_pos)

        self.pits=set()
        for _ in range(2):
            p=self.rand_cell(occupied)
            self.pits.add(p)
            occupied.add(p)

    def rand_cell(self,occ):
        while True:
            pos=(random.randint(0,self.size-1),random.randint(0,self.size-1))
            if pos!=(0,0) and pos not in occ:
                return pos

    # ---------------- PERCEPTION ----------------

    def perceptions(self):
        r,c=self.player_pos
        adj={(r+1,c),(r-1,c),(r,c+1),(r,c-1)}
        s=[]

        if self.wumpus_pos and self.wumpus_pos in adj:
            s.append("stench")

        if any(p in adj for p in self.pits):
            s.append("breeze")

        if self.player_pos==self.gold_pos and not self.has_gold:
            s.append("glitter")

        self.senses=s
        return s

    # ---------------- ACTIONS ----------------

    def move(self,dir):
        if self.game_over: return

        r,c=self.player_pos
        if dir=="up" and r<self.size-1: r+=1
        elif dir=="down" and r>0: r-=1
        elif dir=="left" and c>0: c-=1
        elif dir=="right" and c<self.size-1: c+=1
        else:
            self.message="Wall!"
            return

        self.player_pos=(r,c)
        self.score-=1
        self.last_event="move"
        self.check()

    def shoot(self,dir):
        if self.game_over: return
        if self.arrow==0:
            self.message="No arrows left"
            return

        self.arrow-=1
        self.score-=10

        r,c=self.player_pos
        while True:
            if dir=="up": r+=1
            elif dir=="down": r-=1
            elif dir=="left": c-=1
            elif dir=="right": c+=1

            if not(0<=r<self.size and 0<=c<self.size):
                break

            if (r,c)==self.wumpus_pos:
                self.wumpus_pos=None
                self.score+=500
                self.message="You hear a scream. Wumpus dead!"
                self.last_event="kill"
                return

        self.message="Arrow missed"
        self.last_event="shoot"

    def grab(self):
        if self.player_pos==self.gold_pos and not self.has_gold:
            self.has_gold=True
            self.score+=1000
            self.message="Gold acquired!"
            self.last_event="gold"

    def climb(self):
        if self.player_pos==(0,0) and self.has_gold:
            self.game_over=True
            self.message="You escaped with gold!"
            self.last_event="win"

    # ---------------- STATUS ----------------

    def check(self):
        if self.player_pos in self.pits:
            self.score-=1000
            self.game_over=True
            self.message="You fall into a bottomless pit!"
            self.last_event="death"

        elif self.player_pos==self.wumpus_pos:
            self.score-=1000
            self.game_over=True
            self.message="The Wumpus ate you!"
            self.last_event="death"

    # ---------------- STATE ----------------

    def state(self):
        return {
            "position":self.player_pos,
            "percepts":self.perceptions(),
            "score":self.score,
            "arrow":self.arrow,
            "gold":self.has_gold,
            "game_over":self.game_over,
            "message":self.message,
            "event":self.last_event
        }

    def reveal(self):
        return {
            "player":self.player_pos,
            "wumpus":self.wumpus_pos,
            "gold":self.gold_pos,
            "pits":list(self.pits)
        }
