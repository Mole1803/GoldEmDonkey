class Card:
    colour: int
    value: int

    def __init__(self, colour: int, value: int):
        self.colour = colour
        self.value = value

    def __str__(self):
        return str(self.colour) + ' ' + str(self.value)
