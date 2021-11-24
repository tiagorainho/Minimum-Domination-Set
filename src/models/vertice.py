
class Vertice:
    name: str
    x: int
    y: int

    def __init__(self, name:str, x:int, y:int):
        self.name = name
        self.x = x
        self.y = y

    def distance(self, other):
        return self.distance_manhattan(other)
    
    def distance_euclidean(self, other):
        return ((self.x-other.x)**2 +(self.y-other.y)**2)**0.5

    def distance_manhattan(self, other):
        return abs(self.x-other.x) + abs(self.y-other.y)

    def __eq__(self, other):
        return self.name == other.name #self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash(self.name) #self.x*701+self.y*7079
    
    def __repr__(self):
        return f'{self.name}'
        #return f'{self.name}: ({self.x}, {self.y})'