from Backend.Model.dto.Card import Card


class CardService:
    @staticmethod
    def parse_card_object_from_db(chiffre):
        colour = int(chiffre / 13)
        value = (chiffre % 13) + 2
        return Card(colour, value)
