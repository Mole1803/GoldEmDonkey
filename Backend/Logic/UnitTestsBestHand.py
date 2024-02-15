import unittest
from Backend.Logic.PokerHandler import BestHandEvaluator
from Backend.Model.dto.Card import Card


class TestCardSort(unittest.TestCase):
    def test_bubble_sort(self):
        card1 = Card(2, 14)
        card2 = Card(0, 13)
        card3 = Card(1, 12)
        card4 = Card(3, 11)
        card5 = Card(1, 3)
        card6 = Card(3, 4)
        card7 = Card(1, 4)
        cards = [card1, card2, card3, card4, card5, card6, card7]
        self.assertEqual(
            (
                [card1, card2, card3, card4, card6, card7, card5],
                [[card4, card6], [card1], [card3, card7, card5], [card2]]
            ),
            BestHandEvaluator.sort_cards(cards)
        )


class TestRoyalFlush(unittest.TestCase):
    def test_royal_flush_correct(self):
        card1 = Card(2, 14)
        card2 = Card(2, 13)
        card3 = Card(2, 12)
        card4 = Card(2, 11)
        card5 = Card(1, 3)
        card6 = Card(3, 4)
        card7 = Card(2, 10)
        cards = BestHandEvaluator.sort_cards([card6, card1, card2, card3, card4, card7, card5])
        self.assertEqual([card1, card2, card3, card4, card7], BestHandEvaluator.check_royal_flush(cards))

    def test_royal_flush_no_ace(self):
        card1 = Card(2, 13)
        card2 = Card(1, 13)
        card3 = Card(2, 12)
        card4 = Card(2, 11)
        card5 = Card(1, 3)
        card6 = Card(3, 4)
        card7 = Card(2, 10)
        cards = BestHandEvaluator.sort_cards([card1, card2, card3, card4, card5, card6, card7])[1]
        self.assertEqual(None, BestHandEvaluator.check_royal_flush(cards))

    def test_royal_flush_missing_card_at_end(self):
        card1 = Card(2, 13)
        card2 = Card(2, 14)
        card3 = Card(2, 12)
        card4 = Card(2, 11)
        card5 = Card(1, 3)
        card6 = Card(3, 4)
        card7 = Card(1, 10)
        cards = BestHandEvaluator.sort_cards([card1, card2, card3, card4, card5, card6, card7])[1]
        self.assertEqual(None, BestHandEvaluator.check_royal_flush(cards))

    def test_royal_flush_just_normal_flush_with_ace(self):
        card1 = Card(2, 13)
        card2 = Card(2, 14)
        card3 = Card(2, 9)
        card4 = Card(2, 11)
        card5 = Card(1, 3)
        card6 = Card(3, 4)
        card7 = Card(2, 10)
        cards = BestHandEvaluator.sort_cards([card1, card2, card3, card4, card5, card6, card7])[1]
        self.assertEqual(None, BestHandEvaluator.check_royal_flush(cards))

    def test_royal_flush_correct_more_cards_with_same_colour(self):
        card1 = Card(2, 13)
        card2 = Card(2, 14)
        card3 = Card(2, 12)
        card4 = Card(2, 11)
        card5 = Card(2, 3)
        card6 = Card(2, 4)
        card7 = Card(2, 10)
        cards = BestHandEvaluator.sort_cards([card1, card2, card3, card4, card5, card6, card7])[1]
        self.assertEqual([card2, card1, card3, card4, card7], BestHandEvaluator.check_royal_flush(cards))

    def test_royal_flush_straight_and_flush(self):
        card1 = Card(2, 14)
        card2 = Card(2, 13)
        card3 = Card(2, 12)
        card4 = Card(1, 11)
        card5 = Card(2, 10)
        card6 = Card(1, 9)
        card7 = Card(2, 7)
        cards = BestHandEvaluator.sort_cards([card1, card2, card3, card4, card5, card6, card7])[1]
        self.assertEqual(None, BestHandEvaluator.check_royal_flush(cards))


class TestStraightFlush(unittest.TestCase):
    def test_straight_flush_correct(self):
        card1 = Card(2, 13)
        card2 = Card(2, 9)
        card3 = Card(2, 8)
        card4 = Card(2, 7)
        card5 = Card(2, 6)
        card6 = Card(2, 5)
        card7 = Card(3, 7)
        cards = BestHandEvaluator.sort_cards([card1, card2, card3, card4, card5, card6, card7])[1]
        self.assertEqual([card2, card3, card4, card5, card6], BestHandEvaluator.check_straight_flush(cards))

    def test_straight_flush_just_flush(self):
        card1 = Card(2, 13)
        card2 = Card(2, 9)
        card3 = Card(3, 8)
        card4 = Card(2, 7)
        card5 = Card(2, 6)
        card6 = Card(2, 5)
        card7 = Card(3, 7)
        cards = BestHandEvaluator.sort_cards([card1, card2, card3, card4, card5, card6, card7])[1]
        self.assertEqual(None, BestHandEvaluator.check_straight_flush(cards))

    def test_straight_flush_ace_2_3_4_5(self):
        card1 = Card(2, 14)
        card2 = Card(2, 2)
        card3 = Card(2, 3)
        card4 = Card(2, 4)
        card5 = Card(2, 5)
        card6 = Card(3, 5)
        card7 = Card(3, 7)
        cards = BestHandEvaluator.sort_cards([card1, card2, card3, card4, card5, card6, card7])[1]
        self.assertEqual([card5, card4, card3, card2, card1], BestHandEvaluator.check_straight_flush(cards))

    def test_straight_flush_no_flush(self):
        card1 = Card(2, 14)
        card2 = Card(2, 2)
        card3 = Card(2, 3)
        card4 = Card(1, 4)
        card5 = Card(0, 5)
        card6 = Card(3, 5)
        card7 = Card(3, 7)
        cards = BestHandEvaluator.sort_cards([card1, card2, card3, card4, card5, card6, card7])[1]
        self.assertEqual(None, BestHandEvaluator.check_straight_flush(cards))

    def test_straight_flush_6_5_4_3_2(self):
        card1 = Card(2, 6)
        card2 = Card(2, 5)
        card3 = Card(2, 4)
        card4 = Card(2, 3)
        card5 = Card(2, 2)
        card6 = Card(3, 5)
        card7 = Card(3, 7)
        cards = BestHandEvaluator.sort_cards([card1, card2, card3, card4, card5, card6, card7])[1]
        self.assertEqual([card1, card2, card3, card4, card5], BestHandEvaluator.check_straight_flush(cards))

    def test_straight_flush_flush_too_many_cards_same_colour(self):
        card1 = Card(2, 6)
        card2 = Card(2, 5)
        card3 = Card(2, 11)
        card4 = Card(2, 3)
        card5 = Card(2, 2)
        card6 = Card(2, 13)
        card7 = Card(2, 7)
        cards = BestHandEvaluator.sort_cards([card1, card2, card3, card4, card5, card6, card7])[1]
        self.assertEqual(None, BestHandEvaluator.check_straight_flush(cards))

    def test_straight_flush_with_lower_numbers(self):
        card1 = Card(2, 11)
        card2 = Card(2, 10)
        card3 = Card(2, 9)
        card4 = Card(2, 8)
        card5 = Card(2, 7)
        card6 = Card(2, 4)
        card7 = Card(2, 3)
        cards = BestHandEvaluator.sort_cards([card1, card2, card3, card4, card5, card6, card7])[1]
        self.assertEqual([card1, card2, card3, card4, card5], BestHandEvaluator.check_straight_flush(cards))

    def test_straight_flush_incorrect_four_in_a_row_and_ace(self):
        card1 = Card(2, 14)
        card2 = Card(2, 12)
        card3 = Card(2, 11)
        card4 = Card(2, 10)
        card5 = Card(2, 9)
        card6 = Card(3, 9)
        card7 = Card(1, 9)
        cards = BestHandEvaluator.sort_cards([card1, card2, card3, card4, card5, card6, card7])[1]
        self.assertEqual(None, BestHandEvaluator.check_straight_flush(cards))


class TestFourOfAKind(unittest.TestCase):
    def test_four_of_a_kind_correct(self):
        card1 = Card(2, 11)
        card2 = Card(1, 11)
        card3 = Card(3, 11)
        card4 = Card(0, 11)
        card5 = Card(2, 7)
        card6 = Card(2, 4)
        card7 = Card(2, 3)
        cards = BestHandEvaluator.sort_cards([card1, card2, card3, card4, card5, card6, card7])[0]
        self.assertEqual([card3, card1, card2, card4, card5], BestHandEvaluator.check_four_of_a_kind(cards))

    def test_four_of_a_kind_not_correct(self):
        card1 = Card(2, 11)
        card2 = Card(1, 11)
        card3 = Card(3, 11)
        card4 = Card(0, 10)
        card5 = Card(2, 7)
        card6 = Card(2, 4)
        card7 = Card(2, 3)
        cards = BestHandEvaluator.sort_cards([card1, card2, card3, card4, card5, card6, card7])[0]
        self.assertEqual(None, BestHandEvaluator.check_four_of_a_kind(cards))

    def test_four_of_a_kind_correct_with_same_card(self):
        card1 = Card(2, 11)
        card2 = Card(1, 11)
        card3 = Card(3, 11)
        card4 = Card(0, 11)
        card5 = Card(3, 2)
        card6 = Card(2, 2)
        card7 = Card(1, 2)
        cards = BestHandEvaluator.sort_cards([card1, card2, card3, card4, card5, card6, card7])[0]
        self.assertEqual([card3, card1, card2, card4, card5], BestHandEvaluator.check_four_of_a_kind(cards))


class TestFullHouse(unittest.TestCase):
    def test_full_house_correct_pair_lower(self):
        card1 = Card(2, 11)
        card2 = Card(1, 11)
        card3 = Card(3, 11)
        card4 = Card(0, 10)
        card5 = Card(3, 2)
        card6 = Card(2, 2)
        card7 = Card(1, 3)
        cards = BestHandEvaluator.sort_cards([card1, card2, card3, card4, card5, card6, card7])[0]
        self.assertEqual([card3, card1, card2, card5, card6], BestHandEvaluator.check_full_house(cards))

    def test_full_house_correct_pair_higher(self):
        card1 = Card(2, 11)
        card2 = Card(1, 11)
        card3 = Card(3, 10)
        card4 = Card(0, 10)
        card5 = Card(3, 2)
        card6 = Card(2, 2)
        card7 = Card(1, 2)
        cards = BestHandEvaluator.sort_cards([card1, card2, card3, card4, card5, card6, card7])[0]
        self.assertEqual([card5, card6, card7, card1, card2], BestHandEvaluator.check_full_house(cards))

    def test_full_house_correct_no_full_house(self):
        card1 = Card(2, 11)
        card2 = Card(1, 11)
        card3 = Card(3, 10)
        card4 = Card(0, 10)
        card5 = Card(3, 2)
        card6 = Card(2, 2)
        card7 = Card(1, 3)
        cards = BestHandEvaluator.sort_cards([card1, card2, card3, card4, card5, card6, card7])[0]
        self.assertEqual(None, BestHandEvaluator.check_full_house(cards))

    def test_flush_correct(self):
        card1 = Card(2, 11)
        card2 = Card(2, 12)
        card3 = Card(2, 4)
        card4 = Card(2, 10)
        card5 = Card(3, 2)
        card6 = Card(2, 2)
        card7 = Card(1, 3)
        cards = BestHandEvaluator.sort_cards([card1, card2, card3, card4, card5, card6, card7])[1]
        self.assertEqual([card2, card1, card4, card3, card6], BestHandEvaluator.check_flush(cards))

    def test_flush_correct_more_cards_than_needed(self):
        card1 = Card(2, 11)
        card2 = Card(2, 12)
        card3 = Card(2, 4)
        card4 = Card(2, 10)
        card5 = Card(2, 5)
        card6 = Card(2, 2)
        card7 = Card(2, 3)
        cards = BestHandEvaluator.sort_cards([card1, card2, card3, card4, card5, card6, card7])[1]
        self.assertEqual([card2, card1, card4, card5, card3], BestHandEvaluator.check_flush(cards))

    def test_flush_incorrect(self):
        card1 = Card(2, 11)
        card2 = Card(1, 12)
        card3 = Card(2, 4)
        card4 = Card(2, 10)
        card5 = Card(3, 2)
        card6 = Card(2, 2)
        card7 = Card(1, 3)
        cards = BestHandEvaluator.sort_cards([card1, card2, card3, card4, card5, card6, card7])[1]
        self.assertEqual(None, BestHandEvaluator.check_flush(cards))


class TestStraight(unittest.TestCase):
    def test_straight_correct(self):
        card1 = Card(2, 11)
        card2 = Card(1, 12)
        card3 = Card(2, 9)
        card4 = Card(2, 10)
        card5 = Card(3, 8)
        card6 = Card(2, 7)
        card7 = Card(1, 6)
        cards = BestHandEvaluator.sort_cards([card1, card2, card3, card4, card5, card6, card7])[0]
        self.assertEqual([card2, card1, card4, card3, card5], BestHandEvaluator.check_straight(cards))

    def test_straight_correct_with_higher_cards(self):
        card1 = Card(2, 2)
        card2 = Card(1, 12)
        card3 = Card(2, 9)
        card4 = Card(2, 10)
        card5 = Card(3, 8)
        card6 = Card(2, 7)
        card7 = Card(1, 6)
        cards = BestHandEvaluator.sort_cards([card1, card2, card3, card4, card5, card6, card7])[0]
        self.assertEqual([card4, card3, card5, card6, card7], BestHandEvaluator.check_straight(cards))

    def test_straight_incorrect(self):
        card1 = Card(2, 11)
        card2 = Card(1, 12)
        card3 = Card(2, 2)
        card4 = Card(2, 10)
        card5 = Card(3, 8)
        card6 = Card(2, 7)
        card7 = Card(1, 6)
        cards = BestHandEvaluator.sort_cards([card1, card2, card3, card4, card5, card6, card7])[0]
        self.assertEqual(None, BestHandEvaluator.check_straight(cards))

    def test_straight_ace_2_3_4_5(self):
        card1 = Card(2, 14)
        card2 = Card(1, 2)
        card3 = Card(2, 9)
        card4 = Card(2, 10)
        card5 = Card(3, 4)
        card6 = Card(2, 3)
        card7 = Card(1, 5)
        cards = BestHandEvaluator.sort_cards([card1, card2, card3, card4, card5, card6, card7])[0]
        self.assertEqual([card7, card5, card6, card2, card1], BestHandEvaluator.check_straight(cards))

    def test_straight_correct_many_cards_from_one(self):
        card1 = Card(2, 11)
        card2 = Card(1, 12)
        card3 = Card(2, 9)
        card4 = Card(2, 10)
        card5 = Card(3, 8)
        card6 = Card(3, 9)
        card7 = Card(1, 9)
        cards = BestHandEvaluator.sort_cards([card1, card2, card3, card4, card5, card6, card7])[0]
        self.assertEqual([card2, card1, card4, card6, card5], BestHandEvaluator.check_straight(cards))

    def test_straight_incorrect_four_in_a_row_and_ace(self):
        card1 = Card(2, 14)
        card2 = Card(1, 12)
        card3 = Card(2, 11)
        card4 = Card(2, 10)
        card5 = Card(0, 9)
        card6 = Card(3, 9)
        card7 = Card(1, 9)
        cards = BestHandEvaluator.sort_cards([card1, card2, card3, card4, card5, card6, card7])[0]
        self.assertEqual(None, BestHandEvaluator.check_straight(cards))

    def test_straight_incorrect_four_in_a_row_and_ace_and_2(self):
        card1 = Card(2, 14)
        card2 = Card(1, 12)
        card3 = Card(2, 11)
        card4 = Card(2, 10)
        card5 = Card(0, 9)
        card6 = Card(3, 9)
        card7 = Card(1, 2)
        cards = BestHandEvaluator.sort_cards([card1, card2, card3, card4, card5, card6, card7])[0]
        self.assertEqual(None, BestHandEvaluator.check_straight(cards))


class TestThreeOfAKind(unittest.TestCase):
    def test_three_of_a_kind_correct(self):
        card1 = Card(3, 11)
        card2 = Card(2, 11)
        card3 = Card(1, 11)
        card4 = Card(0, 9)
        card5 = Card(2, 6)
        card6 = Card(2, 4)
        card7 = Card(2, 3)
        cards = BestHandEvaluator.sort_cards([card1, card2, card3, card4, card5, card6, card7])[0]
        expected = [card1, card2, card3, card4, card5]
        result = BestHandEvaluator.check_three_of_a_kind(cards)
        self.assertEqual(expected, result)

    def test_three_of_a_kind_other_position(self):
        card1 = Card(3, 11)
        card2 = Card(2, 10)
        card3 = Card(1, 8)
        card4 = Card(0, 6)
        card5 = Card(3, 4)
        card6 = Card(2, 4)
        card7 = Card(1, 4)
        cards = BestHandEvaluator.sort_cards([card1, card2, card3, card4, card5, card6, card7])[0]
        expected = [card5, card6, card7, card1, card2]
        result = BestHandEvaluator.check_three_of_a_kind(cards)
        self.assertEqual(expected, result)

    def test_three_of_a_kind_not_three_of_a_kind(self):
        card1 = Card(3, 11)
        card2 = Card(2, 11)
        card3 = Card(1, 8)
        card4 = Card(0, 8)
        card5 = Card(3, 4)
        card6 = Card(2, 4)
        card7 = Card(1, 2)
        cards = BestHandEvaluator.sort_cards([card1, card2, card3, card4, card5, card6, card7])[0]
        expected = None
        result = BestHandEvaluator.check_three_of_a_kind(cards)
        self.assertEqual(expected, result)


class TestTwoPair(unittest.TestCase):
    def test_two_pair_correct(self):
        card1 = Card(2, 11)
        card2 = Card(1, 11)
        card3 = Card(3, 9)
        card4 = Card(0, 9)
        card5 = Card(2, 6)
        card6 = Card(2, 4)
        card7 = Card(2, 3)
        cards = BestHandEvaluator.sort_cards([card1, card2, card3, card4, card5, card6, card7])[0]
        expected = [card1, card2, card3, card4, card5]
        result = BestHandEvaluator.check_two_pair(cards)
        self.assertEqual(expected, result)

    def test_two_pair_other_position(self):
        card1 = Card(2, 11)
        card2 = Card(1, 10)
        card3 = Card(3, 8)
        card4 = Card(0, 8)
        card5 = Card(2, 6)
        card6 = Card(2, 3)
        card7 = Card(1, 3)
        cards = BestHandEvaluator.sort_cards([card1, card2, card3, card4, card5, card6, card7])[0]
        expected = [card3, card4, card6, card7, card1]
        result = BestHandEvaluator.check_two_pair(cards)
        self.assertEqual(expected, result)

    def test_two_pair_not_two_pair(self):
        card1 = Card(2, 11)
        card2 = Card(1, 10)
        card3 = Card(3, 8)
        card4 = Card(0, 7)
        card5 = Card(2, 6)
        card6 = Card(2, 3)
        card7 = Card(1, 2)
        cards = BestHandEvaluator.sort_cards([card1, card2, card3, card4, card5, card6, card7])[0]
        expected = None
        result = BestHandEvaluator.check_two_pair(cards)
        self.assertEqual(expected, result)


class TestOnePair(unittest.TestCase):
    def test_one_pair_correct(self):
        card1 = Card(2, 11)
        card2 = Card(1, 11)
        card3 = Card(3, 9)
        card4 = Card(0, 7)
        card5 = Card(2, 6)
        card6 = Card(2, 4)
        card7 = Card(2, 3)
        cards = BestHandEvaluator.sort_cards([card1, card2, card3, card4, card5, card6, card7])[0]
        expected = [card1, card2, card3, card4, card5]
        result = BestHandEvaluator.check_one_pair(cards)
        self.assertEqual(expected, result)

    def test_one_pair_other_position(self):
        card1 = Card(2, 13)
        card2 = Card(1, 11)
        card3 = Card(3, 9)
        card4 = Card(0, 8)
        card5 = Card(2, 7)
        card6 = Card(2, 4)
        card7 = Card(1, 4)
        cards = BestHandEvaluator.sort_cards([card1, card2, card3, card4, card5, card6, card7])[0]
        expected = [card6, card7, card1, card2, card3]
        result = BestHandEvaluator.check_one_pair(cards)
        self.assertEqual(expected, result)

    def test_one_pair_no_pair(self):
        card1 = Card(2, 11)
        card2 = Card(1, 10)
        card3 = Card(3, 9)
        card4 = Card(0, 8)
        card5 = Card(2, 6)
        card6 = Card(2, 4)
        card7 = Card(2, 3)
        cards = BestHandEvaluator.sort_cards([card1, card2, card3, card4, card5, card6, card7])[0]
        expected = None
        result = BestHandEvaluator.check_one_pair(cards)
        self.assertEqual(expected, result)


class TestHighCard(unittest.TestCase):
    def test_high_card(self):
        card1 = Card(2, 11)
        card2 = Card(1, 11)
        card3 = Card(3, 11)
        card4 = Card(0, 10)
        card5 = Card(2, 7)
        card6 = Card(2, 4)
        card7 = Card(2, 3)
        cards = BestHandEvaluator.sort_cards([card1, card2, card3, card4, card5, card6, card7])[0]
        expected = [card3, card1, card2, card4, card5]
        result = BestHandEvaluator.check_high_card(cards)
        self.assertEqual(expected, result)
