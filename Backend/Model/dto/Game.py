class Game:
    id: int
    players: []
    currentBlind: int
    password: str
    blindOptions: int

    def __init__(self, id):
        self.id = id
