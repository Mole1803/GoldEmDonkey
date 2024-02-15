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
            last_value = colour[0].value
            counter = 1
            index = 0
            for i in range(1, len(colour)):
                if colour[i].value + 1 == last_value:
                    counter += 1
                else:
                    counter = 1
                    index = i
                last_value = colour[i].value
                if counter > 4:
                    return colour[index: index + 5]
            if last_value == 2 and counter == 4:
                if colour[0].value == 14:
                    return_cards = colour[index: index + 4]
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
                return cards_value[index: index + 4]
        return None

    @staticmethod
    def sort_cards(cards):
        cards_value_sorted = sorted(cards.copy(), key=lambda x: (x.value, x.colour), reverse=True)
        cards_colour_sorted = sorted(cards.copy(), key=lambda x: (x.colour, x.value), reverse=True)
        cards_colour_sorted_new = [[], [], [], []]
        for card in cards_colour_sorted:
            cards_colour_sorted_new[card.colour].append(card)

        return cards_value_sorted, cards_colour_sorted_new
