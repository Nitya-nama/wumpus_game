class WumpusAgent:
    def __init__(self):
        self.safe=set([(0,0)])
        self.visited=set()

    def update(self,pos,percepts):
        self.visited.add(pos)
        if "breeze" not in percepts and "stench" not in percepts:
            r,c=pos
            for n in [(r+1,c),(r-1,c),(r,c+1),(r,c-1)]:
                if 0<=n[0]<4 and 0<=n[1]<4:
                    self.safe.add(n)

    def next_move(self,pos):
        for s in self.safe:
            if s not in self.visited:
                return s
        return None
