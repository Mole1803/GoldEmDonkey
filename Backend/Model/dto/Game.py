class Game:
    is_active: bool
    name: str
    has_started: bool
    id: int
    players: []
    currentBlind: int
    password: str
    blindOptions: int

    def __init__(self, id, name):
        self.id = id
        self.is_active = True
        self.name = name
        self.has_started = False
