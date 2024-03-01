class Player:
    chips: int
    name: str
    id: int
    position: int

    def __init__(self, chips, name, id, position):
        self.chips = chips
        self.name = name
        self.id = id
        self.position = position
