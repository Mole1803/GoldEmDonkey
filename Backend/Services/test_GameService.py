from Backend.Services.GameService import GameService
from Backend._DatabaseCall import Base, SQLAlchemy, DatabaseManager

from flask import Flask
import pytest

app = Flask(__name__)
database_manager = DatabaseManager(app)
database_manager.init_database()

db = database_manager.db

with app.app_context():  # This is the required context for Flask-SQLAlchemy operations
    Base.metadata.create_all(bind=db.engine)


@pytest.fixture(scope='module')
def db_context():
    with app.app_context():  # We use Flask application context here
        db.create_all()  # Create the tables
        yield db
        db.session.remove()  # Clean up the session after each test
        db.drop_all()  # Drop all the tables


def test_insert_game_db(db_context):
    with app.app_context():  # We use Flask application context here
        result = GameService.insert_game_db(db_context)
        assert result.id is not None
        assert result.is_active is True
        assert result.name == "TestGame"
        assert result.has_started is False
        assert result.active_round is None
        assert result.dealer is None


def test_select_game_get_all_active_games(db_context):
    with app.app_context():
        GameService.insert_game_db(db_context)
        GameService.insert_game_db(db_context)
        GameService.insert_game_db(db_context)
        GameService.insert_game_db(db_context)
        result = GameService.select_game_get_all_active_games(db_context)
        assert result is not None


def test_update_round_set_status(db_context):
    with app.app_context():
        game = GameService.insert_game_db(db_context)
        round1 = GameService.insert_round_db(game.id, db_context)
        round2 = GameService.insert_round_db(game.id, db_context)
        round3 = GameService.insert_round_db(game.id, db_context)
        round4 = GameService.insert_round_db(game.id, db_context)
        result = GameService.update_round_set_status(round3.id, 4, db_context)
        assert round3.status == 4


def test_delete_players_with_no_coins(db_context):
    with app.app_context():
        game = GameService.insert_game_db(db_context)
        player1 = GameService.insert_player_db(1, 0, game.id, 'fasf', db_context)
        player2 = GameService.insert_player_db(2, 3, game.id, 'fasf', db_context)
        player3 = GameService.insert_player_db(3, 5, game.id, 'fasf', db_context)
        player4 = GameService.insert_player_db(4, 0, game.id, 'fasf', db_context)
        players = GameService.delete_players_with_no_coins(game.id, db_context)
        print(players)
        assert players[1].id == player4.id


def test_delete_player_by_player_id(db_context):
    with app.app_context():
        game = GameService.insert_game_db(db_context)
        player = GameService.insert_player_db(1, 0, game.id, 'asdsa', db_context)
        player = GameService.delete_player_by_player_id(player.id, db_context)
        player2 = GameService.delete_player_by_player_id(player.id, db_context)
        assert player is not None


def test_select_round_player_by_round_id_inner_join_player(db_context):
    with app.app_context():
        round = GameService.insert_round_db('bb', db_context)
        player = GameService.insert_player_db(1, 0, 'bb', round.id, db_context)
        pl = GameService.select_round_player_by_round_id(round.id, db_context)
        assert pl is not None
