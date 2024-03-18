from flask_sqlalchemy import SQLAlchemy
import uuid
from sqlalchemy import func
from Backend._DatabaseCall import GameDB, RoundDB, PlayerDB, RoundCardsDB, RoundPlayerDB


class GameService:
    # Game
    @staticmethod
    def insert_game_db(is_active, name, has_started, dealer, db_context: SQLAlchemy):
        id_ = str(uuid.uuid4())
        game = GameDB(
            id=id_,
            is_active=is_active,
            name=name,
            has_started=has_started,
            dealer=dealer
        )
        try:
            db_context.session.add(game)
            db_context.session.commit()
            return game
        except:
            return None

    @staticmethod
    def update_game_is_active(game_id: str, is_active: bool, db_context: SQLAlchemy):
        game = db_context.session.query(GameDB).filter_by(id=game_id).all()
        if len(game) == 0:
            return False
        game = game[0]
        game.is_active = is_active
        db_context.session.commit()
        return True

    @staticmethod
    def select_game_get_all_games(db_context: SQLAlchemy):
        games = db_context.session.query(GameDB).all()
        return games

    @staticmethod
    def select_game_get_all_active_games(db_context: SQLAlchemy):
        games = db_context.session.query(GameDB).filter_by(is_active=True).all()
        return games

    # Round
    @staticmethod
    def insert_round_db(id, game_id, status, db_context: SQLAlchemy):
        round_ = RoundDB(
            id=id,
            game_id=game_id,
            status=status
        )
        try:
            db_context.session.add(round_)
            db_context.session.commit()
            return True
        except:
            return False

    # Player
    @staticmethod
    def insert_player_db(id_, position, chips, game_id, user_id, db_context: SQLAlchemy):
        player = PlayerDB(
            id=id_,
            position=position,
            chips=chips,
            game_id=game_id,
            user_id=user_id
        )
        try:
            db_context.session.add(player)
            db_context.session.commit()
            return True
        except:
            return False

    @staticmethod
    def update_player_set_chips_player(id_player, chips, db_context: SQLAlchemy):
        player = db_context.session.query(PlayerDB).filter_by(id=id_player).all()
        if len(player) == 0:
            return False
        player = player[0]
        player.chips = chips
        db_context.session.commit()
        return True

    @staticmethod
    def select_player_get_highest_position(id_game, db_context: SQLAlchemy):
        player = db_context.session.query(func.max(PlayerDB.position)).filter_by(id_game=id_game).all()
        return player

    @staticmethod
    def select_player_get_all_players_by_game(id_game, db_context: SQLAlchemy):
        players = db_context.session.query(PlayerDB).filter_by(id_game=id_game).all()
        return players

    # Round Player
    @staticmethod
    def insert_round_player_db(id_round, id_player, at_play, has_played, set_chips, is_active, position, card_1, card_2, db_context: SQLAlchemy):
        round_player = RoundPlayerDB(
            id_round=id_round,
            id_player=id_player,
            at_play=at_play,
            has_played=has_played,
            set_chips=set_chips,
            is_active=is_active,
            position=position,
            card_1=card_1,
            card_2=card_2
        )
        try:
            db_context.session.add(round_player)
            db_context.session.commit()
            return True
        except:
            return False

    @staticmethod
    def update_round_player_set_at_play(id_round, id_player, at_play, db_context: SQLAlchemy):
        round_player = db_context.session.query(RoundPlayerDB).filter_by(id_round=id_round, id_player=id_player).all()
        if len(round_player) == 0:
            return False
        round_player = round_player[0]
        round_player.at_play = at_play
        db_context.session.commit()
        return True

    @staticmethod
    def update_round_player_set_chips(id_round, id_player, set_chips, db_context: SQLAlchemy):
        round_player = db_context.session.query(RoundPlayerDB).filter_by(id_round=id_round, id_player=id_player).all()
        if len(round_player) == 0:
            return False
        round_player = round_player[0]
        round_player.set_chips = set_chips
        db_context.session.commit()
        return True

    @staticmethod
    def update_round_player_is_active(id_round, id_player, is_active, db_context: SQLAlchemy):
        round_player = db_context.session.query(RoundPlayerDB).filter_by(id_round=id_round, id_player=id_player).all()
        if len(round_player) == 0:
            return False
        round_player = round_player[0]
        round_player.is_active = is_active
        db_context.session.commit()
        return True

    @staticmethod
    def select_round_player_chips(id_round, id_player, db_context: SQLAlchemy):
        chips = db_context.session.query(RoundPlayerDB.set_chips).filter_by(id_round=id_round,
                                                                            id_player=id_player).all()
        return chips

    @staticmethod
    def select_round_player_current_max_set_chips(id_round, db_context: SQLAlchemy):
        max_set_chips = db_context.session.query(func.max(RoundPlayerDB.set_chips)).filter_by(id_round=id_round).all()
        return max_set_chips

    @staticmethod
    def select_round_player_get_all_set_chips(id_round, db_context: SQLAlchemy):
        sum_of_chips_in_round = db_context.session.query(func.sum(RoundPlayerDB.set_chips)).filter_by(
            id_round=id_round).all()
        return sum_of_chips_in_round

    @staticmethod
    def select_round_player_get_players_with_status_is_active_from_round_order_by_position(id_round,
                                                                                           db_context: SQLAlchemy):
        player = db_context.session.query(RoundPlayerDB).filter_by(id_round=id_round, is_active=True).order_by(
            RoundPlayerDB.position).all()
        return player

    # Round Card
    @staticmethod
    def insert_round_cards_db(id_round, id_cards, position, db_context: SQLAlchemy):
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
