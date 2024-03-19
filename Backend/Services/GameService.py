from flask_sqlalchemy import SQLAlchemy
import uuid
from sqlalchemy import func
from Backend._DatabaseCall import GameDB, RoundDB, PlayerDB, RoundCardsDB, RoundPlayerDB


class GameService:
    # Game
    @staticmethod
    def insert_game_db(db_context: SQLAlchemy):
        id_ = str(uuid.uuid4())
        game = GameDB(
            id=id_,
            is_active=True,
            name="TestGame",
            has_started=False,
            active_round=None,
            dealer=None
        )

        db_context.session.add(game)
        db_context.session.commit()
        return game

    @staticmethod
    def update_game_set_dealer(game_id: str, dealer: str, db_context: SQLAlchemy):
        game = db_context.session.query(GameDB).filter_by(id=game_id).first()
        if game is None:
            return False
        game.dealer = dealer
        db_context.session.commit()
        return True

    @staticmethod
    def update_game_is_active(game_id: str, is_active: bool, db_context: SQLAlchemy):
        game = db_context.session.query(GameDB).filter_by(id=game_id).first()
        if game is None:
            return False
        game.is_active = is_active
        db_context.session.commit()
        return True

    @staticmethod
    def update_game_active_round(game_id: str, active_round: str, db_context: SQLAlchemy):
        game = db_context.session.query(GameDB).filter_by(id=game_id).first()
        if game is None:
            return False
        game.active_round = active_round
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

    @staticmethod
    def select_game_by_id(id_game: str, db_context: SQLAlchemy):
        game = db_context.session.query(GameDB).filter_by(id=id_game).first()
        return game

    @staticmethod
    def select_game_get_game_by_round_id(id_round: str, db_context: SQLAlchemy):
        game_id = db_context.session.query(RoundDB.game_id).filter_by(id=id_round).first()
        game = GameService.select_game_by_id(game_id, db_context)
        return game

    # Round
    @staticmethod
    def insert_round_db(game_id, db_context: SQLAlchemy) -> RoundDB or None:
        id_ = str(uuid.uuid4())
        round_ = RoundDB(
            id=id_,
            game_id=game_id,
            status=0
        )
        db_context.session.add(round_)
        db_context.session.commit()
        return round_

    @staticmethod
    def select_round_by_round_id(round_id, db_context: SQLAlchemy):
        round = db_context.session.query(RoundDB).filter_by(id=round_id).first()
        return round

    @staticmethod
    def update_round_set_status(round_id, status, db_context: SQLAlchemy):
        round = GameService.select_round_by_round_id(round_id, db_context)
        if round is None:
            return False
        round.status = status
        db_context.session.commit()
        return round

    @staticmethod
    def delete_round_by_round_id(round_id: str, db_context: SQLAlchemy):
        rounds = db_context.session.query(RoundDB).filter_by(id_round=round_id).all()
        if len(rounds) == 0:
            return None
        for round in rounds:
            db_context.session.delete(rounds)
        db_context.session.commit()
        return rounds

    # Player
    @staticmethod
    def insert_player_db(position, chips, game_id, user_id, db_context: SQLAlchemy):
        id_ = str(uuid.uuid4())
        player = PlayerDB(
            id=id_,
            position=position,
            chips=chips,
            game_id=game_id,
            user_id=user_id
        )

        db_context.session.add(player)
        db_context.session.commit()
        return player

    @staticmethod
    def update_player_set_chips_player(id_player: str, chips: int, db_context: SQLAlchemy):
        player = db_context.session.query(PlayerDB).filter_by(id=id_player).first()
        if player is None:
            return False
        player.chips = chips
        db_context.session.commit()
        return True

    @staticmethod
    def select_player_by_player_id(player_id: str, db_context: SQLAlchemy):
        player = db_context.session.query(PlayerDB).filter_by(id=player_id).first()
        return player

    @staticmethod
    def select_player_get_highest_position(id_game, db_context: SQLAlchemy):
        player = db_context.session.query(PlayerDB).filter_by(game_id=id_game).order_by(PlayerDB.position.desc()).first()
        return player.position if player else 0

    @staticmethod
    def select_player_get_all_players_by_game(id_game: str, db_context: SQLAlchemy):
        players = db_context.session.query(PlayerDB).filter_by(game_id=id_game).all()
        return players

    @staticmethod
    def delete_players_with_no_coins(id_game: str, db_context: SQLAlchemy):
        players = db_context.session.query(PlayerDB).filter_by(game_id=id_game).filter(PlayerDB.chips <= 0).all()
        for player in players:
            GameService.delete_player_by_player_id(player.id, db_context)
        return players

    @staticmethod
    def delete_player_by_player_id(id_player: str, db_context: SQLAlchemy):
        player = db_context.session.query(PlayerDB).filter_by(id=id_player).first()
        if player is None:
            return None
        db_context.session.delete(player)
        db_context.session.commit()
        return player

    # Round Player
    @staticmethod
    def insert_round_player_db(id_round: str, id_player: str, at_play: bool, has_played: bool, set_chips: int,
                               is_active: bool, position: int, card_1: int, card_2: int, db_context: SQLAlchemy):
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
        db_context.session.add(round_player)
        db_context.session.commit()
        return True

    @staticmethod
    def update_round_player_set_at_play(id_round: str, id_player: str, at_play: bool, db_context: SQLAlchemy):
        round_player = db_context.session.query(RoundPlayerDB).filter_by(id_round=id_round, id_player=id_player).first()
        if round_player is None:
            return False
        round_player.at_play = at_play
        db_context.session.commit()
        return True

    @staticmethod
    def update_round_player_set_chips(id_round: str, id_player: str, set_chips: int, db_context: SQLAlchemy):
        round_player = db_context.session.query(RoundPlayerDB).filter_by(id_round=id_round, id_player=id_player).first()
        if round_player is None:
            return False
        round_player.set_chips = set_chips
        db_context.session.commit()
        return True

    @staticmethod
    def update_round_player_is_active(id_round: str, id_player: str, is_active: bool, db_context: SQLAlchemy):
        round_player = db_context.session.query(RoundPlayerDB).filter_by(id_round=id_round, id_player=id_player).first()
        if round_player is None:
            return False
        round_player.is_active = is_active
        db_context.session.commit()
        return True

    @staticmethod
    def update_round_player_has_played(id_round, id_player, has_played, db_context: SQLAlchemy):
        round_player = db_context.session.query(RoundPlayerDB).filter_by(id_round=id_round, id_player=id_player).all()
        if len(round_player) == 0:
            return False
        round_player = round_player[0]
        round_player.has_played = has_played
        db_context.session.commit()
        return round_player


    @staticmethod
    def select_round_player_chips(id_round: str, id_player: str, db_context: SQLAlchemy):
        chips = db_context.session.query(RoundPlayerDB.set_chips).filter_by(id_round=id_round,
                                                                            id_player=id_player).first()
        return chips

    @staticmethod
    def select_round_player_current_max_set_chips(id_round: str, db_context: SQLAlchemy):
        max_set_chips = db_context.session.query(func.max(RoundPlayerDB.set_chips)).filter_by(id_round=id_round).all()
        return max_set_chips

    @staticmethod
    def select_round_player_get_all_set_chips(id_round: str, db_context: SQLAlchemy):
        sum_of_chips_in_round = db_context.session.query(func.sum(RoundPlayerDB.set_chips)).filter_by(
            id_round=id_round).all()
        return sum_of_chips_in_round

    @staticmethod
    def select_round_player_get_players_with_status_is_active_from_round_order_by_position(id_round: str,
                                                                                           db_context: SQLAlchemy):
        player = db_context.session.query(RoundPlayerDB).filter_by(id_round=id_round, is_active=True).order_by(
            RoundPlayerDB.position).all()
        return player

    @staticmethod
    def select_round_player_by_round_id(round_id: str, db_context: SQLAlchemy):
        round_players = db_context.session.query(RoundPlayerDB).filter_by(id_round=round_id).order_by(RoundPlayerDB.position).all()
        return round_players

    @staticmethod
    def select_round_player_by_round_id_inner_join_player(round_id: str, db_context: SQLAlchemy):
        round_player = db_context.session.query(RoundPlayerDB, PlayerDB).filter_by(id_round=round_id).join(PlayerDB,
                                                                                                           RoundPlayerDB.id_player == PlayerDB.id).all()
        return round_player


    @staticmethod
    def select_round_player_by_round_id_and_player_id(round_id: str, player_id: str, db_context: SQLAlchemy):
        raise NotImplementedError

    @staticmethod
    def delete_round_player_by_round_id(round_id: str, db_context: SQLAlchemy):
        round_player = db_context.session.query(RoundPlayerDB).filter_by(id_round=round_id).all()
        if len(round_player) == 0:
            return None
        for round_play in round_player:
            db_context.session.delete(round_play)
        db_context.session.commit()
        return round_player

    # Round Card
    @staticmethod
    def insert_round_cards_db(id_round: str, id_cards: int, position: int, db_context: SQLAlchemy):
        round_cards = RoundCardsDB(
            id_round=id_round,
            id_cards=id_cards,
            position=position
        )
        db_context.session.add(round_cards)
        db_context.session.commit()
        return True

    @staticmethod
    def select_round_cards_by_round_id(id_round: str, db_context: SQLAlchemy):
        round_cards = db_context.session.query().filter_by(id_round=id_round).order_by(RoundCardsDB.position).all()
        return round_cards

    @staticmethod
    def delete_round_cards_by_round_id(round_id: str, db_context: SQLAlchemy):
        round_cards = db_context.session.query(RoundCardsDB).filter_by(id_round=round_id).all()
        if len(round_cards) == 0:
            return None
        for round_card in round_cards:
            db_context.session.delete(round_card)
        db_context.session.commit()
        return round_cards




