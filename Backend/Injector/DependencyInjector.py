from flask_sqlalchemy import SQLAlchemy
from Backend.Logic.PokerHandler import PokerHandler


class DependencyInjector:
    def __init__(self, db_context: SQLAlchemy = None, jwt=None, poker_handler: PokerHandler=None):
        self.db_context = db_context
        self.jwt = jwt
        self.poker_handler: PokerHandler = poker_handler
