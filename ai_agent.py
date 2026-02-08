class WumpusAgent:
    def __init__(self):
        self.visited=set([(0,0)])

    def update(self,pos,percepts):
        self.visited.add(pos)

    def next_move(self,pos):
        r,c=pos
        moves=[(r+1,c),(r-1,c),(r,c+1),(r,c-1)]
        for m in moves:
            if 0<=m[0]<4 and 0<=m[1]<4 and m not in self.visited:
                return m
        return None
