class Card:
    colour: int
    value: int
    id: int

    def __init__(self, colour: int, value: int, id=None):
        self.colour = colour
        self.value = value
        self.id = id

    def __str__(self):
        return str(self.colour) + ' ' + str(self.value)
