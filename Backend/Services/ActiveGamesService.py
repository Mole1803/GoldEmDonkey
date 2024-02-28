from flask_sqlalchemy import SQLAlchemy
from Backend._DatabaseCall import GameDB, RoundDB, PlayerDB, RoundPlayerCardsDB, RoundCardsDB, CardsDB, RoundPlayerDB, ActiveGamePlayerDB
from Backend.Model.dto.Game import Game


class ActiveGameService:
    @staticmethod
    def create_active_game_player_db(id_game, id_player, db_context: SQLAlchemy):
        active_game_player = ActiveGamePlayerDB(
            id_game=id_game,
            id_player=id_player
        )
        try:
            db_context.session.add(active_game_player)
            db_context.session.commit()
            return True
        except:
            return False

    @staticmethod
    def get_room_from_player(id_player, db_context: SQLAlchemy):
        room = db_context.session.query(ActiveGamePlayerDB).join(GameDB, ActiveGamePlayerDB.id_game==GameDB.id).filter_by(id_player=id_player).all()
        if len(room) == 0:
            return None
        room = room[0]
        return Game(room.id)

    @staticmethod
    def end_game_remove_players(id_game, db_context: SQLAlchemy):
        players = db_context.session.query(ActiveGamePlayerDB).filter_by(id_game=id_game).all()
        if len(players) == 0:
            return False
        for player in players:
            try:
                db_context.session.delete(player)
                db_context.session.commit()
            except:
                return False
        return True

    @staticmethod
    def remove_player_from_game(id_player, id_game, db_context: SQLAlchemy):
        player = db_context.session.query(ActiveGamePlayerDB).filter_by(id_player=id_player, id_game=id_game).all()
        if len(player) == 0:
            return False
        player = player[0]
        try:
            db_context.session.delete(player)
            db_context.session.commit()
            return True
        except:
            return False

    @staticmethod
    def get_all_players_from_game(id_game, db_context: SQLAlchemy):
        players = db_context.session.query(ActiveGamePlayerDB).filter_by(id_game=id_game).all()
        return players
