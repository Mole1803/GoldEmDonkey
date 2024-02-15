import unittest
from Backend.Logic.PokerHandler import BestHandEvaluator
from Backend.Model.dto.Card import Card


class TestRankHandAlgo(unittest.TestCase):

    def test_bubble_sort(self):
        card1 = Card(2, 14)
        card2 = Card(0, 13)
        card3 = Card(1, 12)
        card4 = Card(3, 11)
        card5 = Card(1, 3)
        card6 = Card(3, 4)
        card7 = Card(1, 4)
        cards = [card1, card2, card3, card4, card5, card6, card7]
        self.assertEqual(BestHandEvaluator.sort_cards(cards), ([card1, card2, card3, card4, card6, card7, card5], [card4, card6, card1, card3, card7, card5, card2]))

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

    def test_four_of_a_kind_correct(self):
        card1 = Card(2, 11)
        card2 = Card(1, 11)
        card3 = Card(3, 11)
        card4 = Card(0, 11)
        card5 = Card(2, 7)
        card6 = Card(2, 4)
        card7 = Card(2, 3)
        cards = BestHandEvaluator.sort_cards([card1, card2, card3, card4, card5, card6, card7])[0]
        self.assertEqual([card3, card1, card2, card4], BestHandEvaluator.check_four_of_a_kind(cards))

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
