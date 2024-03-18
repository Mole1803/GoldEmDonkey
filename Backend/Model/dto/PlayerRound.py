from Backend.Model.dto import Player, Round


class PlayerRound:
    at_play: bool
    in_round: bool
    set_chips: int
    player: Player
    round: Round
    id: int

    def __init__(self, set_chips, player, round, id):
        self.set_chips = set_chips
        self.at_play = False
        self.in_round = True
        self.player = player
        self.round = round
        self. id = id
