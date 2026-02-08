import random

class WumpusWorld:
    def __init__(self, size=4):
        self.size = size
        self.player_pos = (0, 0)
        self.has_gold = False
        self.arrow = 1
        self.game_over = False
        self.message = ""

        occupied=set()

        self.wumpus_pos=self.random_empty_cell(occupied)
        occupied.add(self.wumpus_pos)

        self.gold_pos=self.random_empty_cell(occupied)
        occupied.add(self.gold_pos)

        self.pits_pos=set()
        for _ in range(2):
            pit=self.random_empty_cell(occupied)
            self.pits_pos.add(pit)
            occupied.add(pit)

    def random_empty_cell(self, occupied):
        while True:
            pos=(random.randint(0,self.size-1),random.randint(0,self.size-1))
            if pos!=(0,0) and pos not in occupied:
                return pos

    def perceptions(self):
        r,c=self.player_pos
        adjacent={(r+1,c),(r-1,c),(r,c+1),(r,c-1)}
        p=[]

        if self.wumpus_pos and self.wumpus_pos in adjacent:
            p.append("stench")

        if any(pit in adjacent for pit in self.pits_pos):
            p.append("breeze")

        if self.player_pos==self.gold_pos:
            p.append("glitter")

        return p

    def move(self, direction):
        if self.game_over:
            return

        r,c=self.player_pos
        if direction=="up" and r<self.size-1: r+=1
        elif direction=="down" and r>0: r-=1
        elif direction=="left" and c>0: c-=1
        elif direction=="right" and c<self.size-1: c+=1
        else:
            self.message="Invalid move"
            return

        self.player_pos=(r,c)
        self.check_status()

    def shoot(self,direction):
        if self.arrow==0:
            self.message="No arrows left"
            return

        self.arrow-=1
        r,c=self.player_pos

        while True:
            if direction=="up": r+=1
            elif direction=="down": r-=1
            elif direction=="left": c-=1
            elif direction=="right": c+=1

            if not(0<=r<self.size and 0<=c<self.size):
                break

            if (r,c)==self.wumpus_pos:
                self.wumpus_pos=None
                self.message="Wumpus killed"
                return

        self.message="Missed"

    def check_status(self):
        if self.player_pos in self.pits_pos:
            self.game_over=True
            self.message="Fell into pit"

        elif self.player_pos==self.wumpus_pos:
            self.game_over=True
            self.message="Eaten by wumpus"

        elif self.player_pos==self.gold_pos:
            self.has_gold=True
            self.message="Gold collected"

        elif self.player_pos==(0,0) and self.has_gold:
            self.game_over=True
            self.message="You win!"

    def state(self):
        return {
            "position":self.player_pos,
            "percepts":self.perceptions(),
            "arrow":self.arrow,
            "gold":self.has_gold,
            "game_over":self.game_over,
            "message":self.message
        }
