class PokerHandler:
    def shuffle_cards(self, cards):
        raise NotImplementedError

    def deal_cards(self, cards, players):
        raise NotImplementedError

    def evaluate_winner(self, players):
        raise NotImplementedError

    def get_hand_rank(self, cards):
        raise NotImplementedError


class BestHandEvaluator:
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
