from collections import defaultdict

dirs=[(1,0),(-1,0),(0,1),(0,-1)]

class WumpusAgent:

    def __init__(self,size=4):
        self.size=size
        self.visited=set()
        self.safe={(0,0)}
        self.possible_pits=defaultdict(set)
        self.possible_wumpus=defaultdict(set)
        self.confirmed_pits=set()
        self.confirmed_wumpus=None

    def neighbors(self,pos):
        r,c=pos
        for dr,dc in dirs:
            nr,nc=r+dr,c+dc
            if 0<=nr<self.size and 0<=nc<self.size:
                yield (nr,nc)

    # ------------ KNOWLEDGE UPDATE ------------

    def update(self,pos,percepts):

        self.visited.add(pos)

        neigh=list(self.neighbors(pos))

        if "breeze" not in percepts:
            for n in neigh:
                self.safe.add(n)
                self.confirmed_pits.discard(n)
        else:
            for n in neigh:
                if n not in self.safe:
                    self.possible_pits[n].add(pos)

        if "stench" not in percepts:
            for n in neigh:
                if n==self.confirmed_wumpus: continue
                self.safe.add(n)
        else:
            for n in neigh:
                if n not in self.safe:
                    self.possible_wumpus[n].add(pos)

        # deduce single candidates
        for cell,cause in self.possible_pits.items():
            if len(cause)>=2:
                self.confirmed_pits.add(cell)

        for cell,cause in self.possible_wumpus.items():
            if len(cause)>=2:
                self.confirmed_wumpus=cell

    # ------------ ACTION SELECTION ------------

    def next_move(self,current):

        # prefer safe unexplored
        for n in self.neighbors(current):
            if n in self.safe and n not in self.visited:
                return n

        # else go any safe visited (backtrack)
        for n in self.neighbors(current):
            if n in self.safe:
                return n

        return None
