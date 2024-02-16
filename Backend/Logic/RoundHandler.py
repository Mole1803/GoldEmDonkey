import json
import queue


class RoundHandler:
    max_bet = 0
    small_blind = 1

    def start_game(self):
        raise NotImplementedError

    def play_next_round(self):
        self.deal_player_cards()
        self.play_bet_round()
        self.deal_flop()
        self.play_bet_round()
        self.deal_turn()
        self.play_bet_round()
        self.deal_river()
        self.play_bet_round()
        self.evaluate_winner()

    def deal_player_cards(self):
        raise NotImplementedError

    def deal_flop(self):
        raise NotImplementedError

    def deal_turn(self):
        raise NotImplementedError

    def deal_river(self):
        raise NotImplementedError

    def play_bet_round(self, players: []):
        to_play_queue = queue.Queue()
        for player in players:
            to_play_queue.put_nowait(player)
        active_players = []
        while (True):
            player = to_play_queue.get_nowait()
            if player is None or (len(active_players) == 0 and to_play_queue.empty()):
                return active_players
            response = player.getResponse()
            json_response = json.loads(response)
            if json_response["action"] == "fold":
                player.setActive(False)
                continue
            elif json_response["action"] == "call":
                player.remove_chips(self.max_bet - player.active_bet)
                player.active_bet = self.max_bet
            elif json_response["action"] == "raise":
                value = json_response["amount"]
                if player.getChips < self.max_bet + value - player.active_bet and value > self.small_blind:
                    self.max_bet += (value - player.active_bet)
                    player.remove_chips(self.max_bet)
                    player.active_bet = self.max_bet
                for a_player in active_players:
                    to_play_queue.put_nowait(a_player)
                active_players = []
            active_players.append(player)

    def evaluate_winner(self):
        raise NotImplementedError
