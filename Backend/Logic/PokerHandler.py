import math
import random
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

    def shuffle_cards(self, num_players):
        erg=random.sample(range(0, 52), 2*num_players+5)
        return erg

    def deal_cards(self, cards, players, round_id):
        card_index=0
        dealer_index=0

        game=GameService.select_game_get_game_by_round_id(round_id,self.db_context)
        if game["dealer"] is not None:
            for player in players:
                if player["id"]==game["dealer"]:
                    dealer_index=player["position"]
        for player,i in enumerate(players):
            if i==dealer_index:
                GameService.insert_round_player_db(round_id, player["id"], True, False, 0, True, 0, cards[card_index],
                                                   cards[card_index+1], self.db_context)
            else:
                GameService.insert_round_player_db(round_id, player["id"], False, False, 0, True,
                                                   (i-dealer_index+len(players))%len(players), cards[card_index],
                                                   cards[card_index+1], self.db_context)
            card_index+=2
        for i in range(5):
            GameService.insert_round_cards_db(round_id,cards[card_index+i],i,self.db_context)


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

    def after_action(self,round_id,player_id):
        round_player = GameService.update_round_player_has_played(round_id,player_id,True,self.db_context)
        players = GameService.select_round_player_get_players_with_status_is_active_from_round_order_by_position(round_id,self.db_context)
        for player in players:
            if player.position>round_player.position:
                if not player.has_played:
                    return self.perform_next_action(player,round_id)
        max_chips = GameService.select_round_player_current_max_set_chips(round_id,self.db_context)
        for player in players:
            if player.set_chips<max_chips:
                return self.perform_next_action(player,round_id)
        state = GameService.select_round_by_round_id(round_id,self.db_context).status
        GameService.update_round_set_status(round_id,state+1, self.db_context)
        self.perform_next_action(players[0],round_id)

    def perform_next_action(self,player,round_id):
        state = GameService.select_round_by_round_id(round_id, self.db_context).status
        data={}
        data["gamestate"]=state
        players=GameService.select_round_player_by_round_id_inner_join_player(round_id,self.db_context)
        data["args"]={}
        data["args"]["players"]=[]
        for player,i in enumerate(players):
            data["args"]["players"][i]=player.serialize()
        round_cards=GameService.select_round_cards_by_round_id(round_id,self.db_context)
        data["args"]["cards"] = []
        if state == 1:
            data["args"]["cards"][0] = round_cards[0].id_cards
            data["args"]["cards"][1] = round_cards[1].id_cards
            data["args"]["cards"][2] = round_cards[2].id_cards
        elif state == 2:
            data["args"]["cards"][0] = round_cards[3].id_cards
        elif state == 3:
            data["args"]["cards"][0] = round_cards[4].id_cards
        elif state == 4:
            return self.perform_after_round(round_id,players,round_cards)
        # TODO sende data an Mole Funktion
    def perform_after_round(self,round_id,players,round_cards):
        player_cards=[]
        for player,i in enumerate(players):
            player_cards[i]=[player.card1,player.card2]
        best_players = BestHandEvaluator.evaluate_all_hands(round_cards,player_cards)
        pott=GameService.select_round_player_get_all_set_chips(round_id,self.db_context)
        for player_index in best_players:
            player=players[player_index]
            GameService.update_player_set_chips_player(player.id,player.chips+pott/len(best_players),self.db_context)
        GameService.delete_round(round_id)
        game = GameService.select_game_get_game_by_round_id(round_id,self.db_context)
        for player,i in enumerate(players):
            if player.id==game.dealer:
                new_dealer=players[(i+1)%len(players)]
                break
        GameService.update_game_set_dealer(game.id,new_dealer,self.db_context)
        self.create_round(game.id)

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
