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
        assert result.dealer is None
