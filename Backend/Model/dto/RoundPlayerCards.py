from Backend.Model.dto import PlayerRound, Card


class RoundPlayerCards:
    player_round: PlayerRound
    card: Card

    def __init__(self, player_round, card):
        self.player_round = player_round
        self.card = card
