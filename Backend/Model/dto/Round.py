from Backend.Model.dto import Game, Player


class Round:
    id: int
    max_raise: int
    game: Game
    dealer: Player
    currentBlind: int

    def __init__(self, id, max_raise, game, currentBlind, dealer):
        self.id = id
        self.max_raise = max_raise
        self.game = game
        self.currentBlind = currentBlind
        self.dealer = dealer
