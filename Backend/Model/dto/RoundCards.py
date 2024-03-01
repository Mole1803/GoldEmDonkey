from Backend.Model.dto import Round, Card


class RoundCards:
    round: Round
    card: Card
    position: int

    def __init__(self, round, card, position):
        self.round = round
        self.card = card
        self.position = position
