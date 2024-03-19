import math
from Backend.Services.GameService import GameService


class PokerHandler:
    def __init__(self, db_context):
        self.db_context = db_context
    def join_game(self, player_id: str, game_id: str):
        # Todo: implement join game
        position = GameService.select_player_get_highest_position(id_game=game_id,db_context= self.db_context)
        return GameService.insert_player_db(position=position+1, user_id=player_id, game_id=game_id,chips=1000,db_context=self.db_context)


    def run_game(self, game_id: str):
        # Todo:
        GameService.update_game_is_active(game_id,True, self.db_context)
        self.create_round(game_id)


        raise NotImplementedError

    def create_round(self, game_id: str):
        round_ = GameService.insert_round_db(game_id=game_id,db_context=self.db_context)
        players = GameService.select_player_get_all_players_by_game(id_game=game_id, db_context=self.db_context)

        cards = self.shuffle_cards(len(players))
        self.deal_cards(cards, players, round_.id)

        raise NotImplementedError

    def shuffle_cards(self, number_of_players: int) -> list:
        raise NotImplementedError

    def deal_cards(self, cards, players, round_id):
        raise NotImplementedError

    def evaluate_winner(self, players):
        raise NotImplementedError

    def get_hand_rank(self, cards):
        raise NotImplementedError

    def on_player_check(self, player, game_id):
        # inform next player and set player to not active

        raise NotImplementedError

    def on_player_call(self, player, game_id):
        # inform next player and set player to not active
        raise NotImplementedError

    def on_player_raise(self, player,game_id, amount):
        # inform next player and set player to not active
        raise NotImplementedError

    def on_player_fold(self, player, game_id):

        raise NotImplementedError

    def after_action(self):
        raise NotImplementedError

    def after_round(self, game_id: str):
        pass
        # GameService.



class BestHandEvaluator:
    @staticmethod
    def evaluate_all_hands(board_cards: [], players_cards):
        best_hand_value = math.inf
        best_hands = []
        best_player_indices = []
        for i in range(len(players_cards)):
            cards = board_cards + players_cards[i]
            value, hand = (BestHandEvaluator.evaluate_hand(cards))
            if value < best_hand_value:
                best_hand_value = value
                best_hands = [hand]
                best_player_indices = [i]
            elif value == best_hand_value:
                best_hand = best_hands[0]
                better = False
                for j in range(5):
                    if hand[i].value > best_hand[i].value:
                        best_hands = [hand]
                        best_player_indices = [i]
                        better = True
                        break
                if not better:
                    best_hands.append(hand)
                    best_player_indices.append(i)
        return best_player_indices

    @staticmethod
    def evaluate_hand(all_cards):
        cards_value, cards_colour = BestHandEvaluator.sort_cards(all_cards)
        check_functions = [BestHandEvaluator.check_royal_flush,
                           BestHandEvaluator.check_straight_flush,
                           BestHandEvaluator.check_four_of_a_kind,
                           BestHandEvaluator.check_full_house,
                           BestHandEvaluator.check_flush,
                           BestHandEvaluator.check_straight,
                           BestHandEvaluator.check_three_of_a_kind,
                           BestHandEvaluator.check_two_pair,
                           BestHandEvaluator.check_one_pair,
                           BestHandEvaluator.check_high_card]
        for i in range(len(check_functions)):
            if i in [0, 1, 4]:
                cards = cards_colour
            else:
                cards = cards_value
            res = check_functions[i](cards)
            if res is not None:
                return i, res
        return None

    @staticmethod
    def check_royal_flush(cards_colour):
        for colour in cards_colour:
            if len(colour) < 5:
                continue
            mark_colour = 14
            for card in colour:
                if card.value != mark_colour:
                    break
                mark_colour -= 1
                if mark_colour == 9:
                    return colour[0:5]
        return None

    @staticmethod
    def check_straight_flush(cards_colour):
        for colour in cards_colour:
            if len(colour) < 5:
                continue
            return_cards = [colour[0]]
            counter = 1
            for i in range(1, len(colour)):
                if colour[i].value + 1 == return_cards[-1].value:
                    counter += 1
                    return_cards.append(colour[i])
                else:
                    counter = 1
                    return_cards = [colour[i]]
                if counter > 4:
                    return return_cards
            if return_cards[-1].value == 2 and counter == 4:
                if colour[0].value == 14:
                    return_cards.append(colour[0])
                    return return_cards
        return None

    @staticmethod
    def check_four_of_a_kind(cards_value):
        counter = 1
        last_value = cards_value[0].value
        index = 0
        for i in range(1, len(cards_value)):
            if last_value == cards_value[i].value:
                counter += 1
            else:
                counter = 1
                index = i
            if counter == 4:
                return_cards = cards_value[index: index + 4]
                for card in cards_value:
                    if card not in return_cards:
                        return_cards.append(card)
                        return return_cards
        return None

    @staticmethod
    def check_full_house(cards_value):
        cards_value = cards_value.copy()
        counter = 1
        last_value = cards_value[0].value
        return_cards = []
        index = 0
        for i in range(1, len(cards_value)):
            if last_value == cards_value[i].value:
                counter += 1
            else:
                counter = 1
                index = i
            last_value = cards_value[i].value
            if counter == 3:
                for j in range(3):
                    return_cards.append(cards_value.pop(index))
                break
        if len(return_cards) == 3:
            last_value = cards_value[0].value
            for j in range(1, len(cards_value)):
                if last_value == cards_value[j].value:
                    return_cards += cards_value[j - 1:j + 1]
                    return return_cards
                last_value = cards_value[j].value

        return None

    @staticmethod
    def check_flush(cards_colour):
        for colour in cards_colour:
            if len(colour) < 5:
                continue
            return colour[0:5]
        return None

    @staticmethod
    def check_straight(cards_value):
        return_cards = [cards_value[0]]
        counter = 1
        for i in range(1, len(cards_value)):
            difference = cards_value[i - 1].value - cards_value[i].value
            if difference == 1:
                return_cards.append(cards_value[i])
                counter += 1
            elif difference > 1:
                return_cards = [cards_value[i]]
                counter = 1
            if counter == 5:
                return return_cards
        if counter == 4 and return_cards[-1].value == 2 and cards_value[0].value == 14:
            return_cards.append(cards_value[0])
            return return_cards
        return None

    @staticmethod
    def check_three_of_a_kind(cards_value):
        result = []
        for i in range(2, len(cards_value)):
            if cards_value[i].value == cards_value[i - 1].value and cards_value[i].value == cards_value[i - 2].value:
                result.append(cards_value[i - 2])
                result.append(cards_value[i - 1])
                result.append(cards_value[i])
                break
        if len(result) != 3:
            return None
        for card in cards_value:
            if card not in result and len(result) < 5:
                result.append(card)
        return result

    @staticmethod
    def check_two_pair(cards_value):
        result = []
        counter = 0
        i = 1
        while i < len(cards_value):
            if cards_value[i].value == cards_value[i - 1].value:
                result.append(cards_value[i - 1])
                result.append(cards_value[i])
                i += 1
                counter += 1
            i += 1
        if counter == 2:
            for card in cards_value:
                if card not in result:
                    result.append(card)
                    return result
        return None

    @staticmethod
    def check_one_pair(cards_value):
        result = []
        for i in range(1, len(cards_value)):
            if cards_value[i].value == cards_value[i - 1].value:
                result.append(cards_value[i - 1])
                result.append(cards_value[i])
                break
        if len(result) != 2:
            return None
        for card in cards_value:
            if card not in result and len(result) < 5:
                result.append(card)
        return result

    @staticmethod
    def check_high_card(cards_value):
        return cards_value[0:5]

    @staticmethod
    def sort_cards(cards):
        cards_value_sorted = sorted(cards.copy(), key=lambda x: (x.value, x.colour), reverse=True)
        cards_colour_sorted = sorted(cards.copy(), key=lambda x: (x.colour, x.value), reverse=True)
        cards_colour_sorted_new = [[], [], [], []]
        for card in cards_colour_sorted:
            cards_colour_sorted_new[3 - card.colour].append(card)

        return cards_value_sorted, cards_colour_sorted_new
