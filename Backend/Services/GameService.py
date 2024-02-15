from flask_sqlalchemy import SQLAlchemy
from Backend._DatabaseCall import GameDB, RoundDB, PlayerDB, RoundPlayerCardsDB, RoundCardsDB, CardsDB, RoundPlayerDB


class GameService:
    @staticmethod
    def create_game_db(id, db_context: SQLAlchemy):
        game = GameDB(
            id=id
        )
        try:
            db_context.session.add(game)
            db_context.session.commit()
            return True
        except:
            return False

    @staticmethod
    def create_round_db(id, max_raise, game_id, db_context: SQLAlchemy):
        round = RoundDB(
            id=id,
            max_raise=max_raise,
            game_id=game_id
        )
        try:
            db_context.session.add(round)
            db_context.session.commit()
            return True
        except:
            return False

    @staticmethod
    def create_player_db(id, position, chips, db_context: SQLAlchemy):
        player = PlayerDB(
            id=id,
            position=position,
            chips=chips
        )
        try:
            db_context.session.add(player)
            db_context.session.commit()
            return True
        except:
            return False

    @staticmethod
    def create_round_player_db(id, id_round, id_player, at_play, set_chips, db_context: SQLAlchemy):
        round_player = RoundPlayerDB(
            id=id,
            id_round=id_round,
            id_player=id_player,
            at_play=at_play,
            set_chips=set_chips
        )
        try:
            db_context.session.add(round_player)
            db_context.session.commit()
            return True
        except:
            return False

    @staticmethod
    def create_card_db(id, color, value, db_context: SQLAlchemy):
        card = CardsDB(
            id=id,
            color=color,
            value=value
        )
        try:
            db_context.session.add(card)
            db_context.session.commit()
            return True
        except:
            return False

    @staticmethod
    def create_round_cards_db(id_round, id_cards, position, db_context: SQLAlchemy):
        round_cards = RoundCardsDB(
            id_round=id_round,
            id_cards=id_cards,
            position=position
        )
        try:
            db_context.session.add(round_cards)
            db_context.session.commit()
            return True
        except:
            return False

    @staticmethod
    def create_round_player_cards_db(id_round_player, id_cards, db_context: SQLAlchemy):
        round_player_cards = RoundPlayerCardsDB(
            id_round_player=id_round_player,
            id_cards=id_cards
        )
        try:
            db_context.session.add(round_player_cards)
            db_context.session.commit()
            return True
        except:
            return False

    @staticmethod
    def get_all_games(db_context: SQLAlchemy):
        games = db_context.session.query(GameDB).all()
        returnList = []
        for game in games:
            returnList.append(game)
        return returnList

    @staticmethod
    def set_max_raise_round(id, max_raise, db_context: SQLAlchemy):
        round = db_context.session.query(RoundDB).filter_by(id=id).all()
        if len(round) == 0:
            return False
        round = round[0]
        round.max_raise = max_raise
        db_context.session.commit()
        return True

    @staticmethod
    def set_chips_player(id, chips, db_context: SQLAlchemy):
        player = db_context.session.query(PlayerDB).filter_by(id=id).all()
        if len(player) == 0:
            return False
        player = player[0]
        player.chips = chips
        db_context.session.commit()
        return True

    @staticmethod
    def set_at_play(id, at_play, db_context: SQLAlchemy):
        round_player = db_context.session.query(RoundPlayerDB).filter_by(id=id).all()
        if len(round_player) == 0:
            return False
        round_player = round_player[0]
        round_player.at_play = at_play
        db_context.session.commit()
        return True

    @staticmethod
    def set_player_set_chips(id, set_chips, db_context: SQLAlchemy):
        round_player = db_context.session.query(RoundPlayerDB).filter_by(id=id).all()
        if len(round_player) == 0:
            return False
        round_player = round_player[0]
        round_player.set_chips = set_chips
        db_context.session.commit()
        return True




