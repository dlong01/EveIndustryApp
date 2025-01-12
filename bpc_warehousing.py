class BPC:
    def __init__(self, typeID, me, te, cost):
        self.typeID = typeID
        self.me = me
        self.te = te
        self.cost = cost

    def __str__(self):
        return f"{self.typeID} {self.me} {self.te} {self.cost}"

    def __repr__(self):
        return f"{self.typeID} {self.me} {self.te} {self.cost}"
    
