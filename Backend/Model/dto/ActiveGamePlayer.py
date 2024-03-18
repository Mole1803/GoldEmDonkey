from Backend.Model.dto import Game, Player


class ActiveGamePlayer:
    game: Game
    player: Player

    def __init__(self, game, player):
        self.game = game
        self.player = player
