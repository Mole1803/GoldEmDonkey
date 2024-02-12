class PokerHandler:
    def shuffle_cards(self, cards):
        raise NotImplementedError

    def deal_cards(self, cards, players):
        raise NotImplementedError

    def evaluate_winner(self, players):
        raise NotImplementedError

    def get_hand_rank(self, cards):
        raise NotImplementedError
