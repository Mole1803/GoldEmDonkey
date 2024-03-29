import math
import queue
import random

from Backend.Services.CardService import CardService
from Backend.Services.GameService import GameService
from Backend._DatabaseCall import Serializer, GameDB


class PokerHandler:
    def __init__(self, db_context):
        self.db_context = db_context
        self.instructionQueue = queue.Queue()

    def join_game(self, player_id: str, game_id: str):
        # check if user is already in game
        player = GameService.is_player_in_game(player_id, game_id, self.db_context)
        if player is not None:
            return player
        # Todo: implement join game
        position = GameService.select_player_get_highest_position(id_game=game_id, db_context=self.db_context)
        return GameService.insert_player_db(position=position + 1, user_id=player_id, game_id=game_id, chips=1000,
                                            db_context=self.db_context)

    def run_game(self, game_id: str):
        # Todo:
        #GameService.update_game_is_active(game_id, True, self.db_context)
        GameService.update_game_has_started(game_id, True, self.db_context)
        self.create_round(game_id)

        # raise NotImplementedError

    def create_round(self, game_id: str):
        game_ = GameService.get_game_by_id(game_id, self.db_context)
        round_ = GameService.insert_round_db(game_id=game_id, db_context=self.db_context)
        GameService.update_game_active_round(game_id,round_.id,self.db_context)

        players = GameService.select_player_get_all_players_by_game(id_game=game_id, db_context=self.db_context)
        if game_.dealer is None:
            GameService.update_game_set_dealer(game_id, players[0].id, self.db_context)

        cards = self.shuffle_cards(len(players))
        self.deal_cards(cards, players, round_.id, game_)
        self.instructionQueue.put({"gamestate": 0, "kwargs": {}})
        self.perform_next_action(players[0], round_.id, game_id=game_id)

    def shuffle_cards(self, num_players):
        erg = random.sample(range(0, 52), 2 * num_players + 5)
        return erg

    def deal_cards(self, cards, players, round_id, game: GameDB):
        card_index = 0
        dealer_index = 0

        if game.dealer is not None:
            for player in players:
                if player.id == game.dealer:
                    dealer_index = player.position
        for i, player in enumerate(players):
            if i == dealer_index:
                GameService.insert_round_player_db(round_id, player.id, True, False, 0, True, 0, cards[card_index],
                                                   cards[card_index + 1], self.db_context)
            else:
                GameService.insert_round_player_db(round_id, player.id, False, False, 0, True,
                                                   (i - dealer_index + len(players)) % len(players), cards[card_index],
                                                   cards[card_index + 1], self.db_context)
            card_index += 2
        for i in range(5):
            GameService.insert_round_cards_db(round_id, cards[card_index + i], i, self.db_context)

    def on_player_check(self, user_id, game_id):
        player=GameService.select_player_by_user_id_and_game_id(user_id,game_id,self.db_context)
        self.after_action(game_id, player.id)

    def on_player_call(self, user_id, game_id):
        player_id = GameService.select_player_by_user_id_and_game_id(user_id, game_id, self.db_context).id
        game=GameService.select_game_by_id(game_id,self.db_context)
        max_chips=GameService.select_round_player_current_max_set_chips(game.active_round,self.db_context)
        player_round = GameService.select_round_player_by_round_id_and_player_id(game.active_round,player_id, self.db_context)
        diff=max_chips-player_round.set_chips
        player=GameService.select_player_by_player_id(player_round.id_player,self.db_context)
        GameService.update_player_set_chips_player(player_round.id_player,player.chips-diff,self.db_context)
        self.after_action(game_id, player_id)

    def on_player_raise(self, user_id, game_id, amount):
        player_id = GameService.select_player_by_user_id_and_game_id(user_id, game_id, self.db_context).id
        game = GameService.select_game_by_id(game_id, self.db_context)
        max_chips = GameService.select_round_player_current_max_set_chips(game.active_round, self.db_context)
        player_round = GameService.select_round_player_by_round_id_and_player_id(game.active_round,player_id, self.db_context)
        diff = max_chips + amount - player_round.set_chips
        player = GameService.select_player_by_player_id(player_round.id_player, self.db_context)
        GameService.update_game_set_chips(game_id, max_chips+amount, self.db_context),
        GameService.update_player_set_chips_player(player_round.id_player, player.chips - diff, self.db_context)
        self.after_action(game_id, player_id)

    def on_player_fold(self, user_id, game_id):
        player_id = GameService.select_player_by_user_id_and_game_id(user_id, game_id, self.db_context).id
        game=GameService.select_game_by_id(game_id,self.db_context)
        GameService.update_round_player_is_active(game.active_round,player_id,False,self.db_context)
        self.after_action(game_id, player_id)


    def after_action(self, game_id, player_id):
        round_id = GameService.select_game_by_id(game_id, self.db_context).active_round
        round_player = GameService.update_round_player_has_played(round_id, player_id, True, self.db_context)
        players = GameService.select_round_player_get_players_with_status_is_active_from_round_order_by_position(
            round_id, self.db_context)
        max_chips = GameService.select_round_player_current_max_set_chips(round_id, self.db_context)
        for player in players:
            print("player:",player,"roundPlayer:",round_player)
            if player.position > round_player.position:
                if not player.has_played or player.set_chips < max_chips:
                    playerplayer=GameService.select_player_by_player_id(player.id_player,self.db_context)
                    return self.perform_next_action(playerplayer, round_id, game_id=game_id)
        for player in players:
            if player.set_chips < max_chips:
                playerplayer = GameService.select_player_by_player_id(player.id_player, self.db_context)
                return self.perform_next_action(playerplayer, round_id, game_id=game_id)
        round = GameService.select_round_by_round_id(round_id, self.db_context)
        GameService.update_round_set_status(round_id, round.status + 1, self.db_context)
        GameService.update_round_player_has_played_all(round_id,self.db_context)
        playerplayer = GameService.select_player_by_player_id(players[0].id_player, self.db_context)
        self.perform_next_action(playerplayer, round_id, game_id=game_id)

    def perform_next_action(self, player, round_id, game_id: str):

        round = GameService.select_round_by_round_id(round_id, self.db_context)

        # Todo: implement
        players = GameService.select_round_player_by_round_id(round_id, self.db_context)

        game_players = GameService.select_player_get_all_players_by_game(id_game=game_id, db_context=self.db_context)
        data = {"gamestate": round.status, "kwargs": {}}

        #next_player=GameService.select_player_by_player_id(player.id_player,self.db_context)
        data["kwargs"]["nextPlayer"] = Serializer.serialize(player)
        data["kwargs"]["roundPlayers"] = Serializer.serialize_query_set(players)
        data["kwargs"]["gamePlayers"] = Serializer.serialize_query_set(game_players)
        # for i,player in enumerate(players):
        #    data["kwargs"]["players"][i]=Serializer.serialize(player)

        round_cards = GameService.select_round_cards_by_round_id(round_id, self.db_context)
        data["kwargs"]["cards"] = []
        if round.status > 0:
            data["kwargs"]["cards"].append(Serializer.serializeDTO(CardService.parse_card_object_from_db(round_cards[0].id_cards)))
            data["kwargs"]["cards"].append(Serializer.serializeDTO(CardService.parse_card_object_from_db(round_cards[1].id_cards)))
            data["kwargs"]["cards"].append(Serializer.serializeDTO(CardService.parse_card_object_from_db(round_cards[2].id_cards)))
        if round.status > 1:
            data["kwargs"]["cards"].append(Serializer.serializeDTO(CardService.parse_card_object_from_db(round_cards[3].id_cards)))
        if round.status > 2:
            data["kwargs"]["cards"].append(Serializer.serializeDTO(CardService.parse_card_object_from_db(round_cards[4].id_cards)))
        if round.status == 4:
            self.perform_after_round(round_id, players, round_cards,data,game_id)
        # TODO sende data an Mole Funktion

        self.instructionQueue.put(data)

    def perform_after_round(self, round_id, players, round_cards,data,game_id):
        player_cards = [[]for i in range(len(players))]
        for i,player in enumerate(players):
            player_cards[i].append(CardService.parse_card_object_from_db(player.card_1))
            player_cards[i].append(CardService.parse_card_object_from_db(player.card_2))
        board_cards=[]
        for card in round_cards:
            board_cards.append(CardService.parse_card_object_from_db(card.id_cards))
        best_players = BestHandEvaluator.evaluate_all_hands(board_cards, player_cards)
        pott = GameService.select_round_player_get_all_set_chips(round_id, self.db_context)
        for player_index in best_players:
            player = players[player_index]
            winner=player
            chips=GameService.select_player_by_player_id(player.id_player,self.db_context).chips
            GameService.update_player_set_chips_player(player.id_player, chips + pott / len(best_players),
                                                       self.db_context)

        GameService.delete_round_player_by_round_id(round_id,self.db_context)
        GameService.delete_round_cards_by_round_id(round_id,self.db_context)
        GameService.delete_round_by_round_id(round_id,self.db_context)
        game = GameService.select_game_by_id(game_id, self.db_context)
        for i,player in enumerate(players):
            if player.id_player == game.dealer:
                new_dealer = players[(i + 1) % len(players)].id_player
                break
        GameService.update_game_set_dealer(game.id, new_dealer, self.db_context)

        data["kwargs"]["round_winner"]=winner.id_player
        #self.instructionQueue.queue()

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
