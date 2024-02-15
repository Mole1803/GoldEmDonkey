from flask_sqlalchemy import SQLAlchemy


class DependencyInjector:
    def __init__(self, db_context:SQLAlchemy=None, jwt=None):
        self.db_context = db_context
        self.jwt = jwt
