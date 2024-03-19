import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from Backend.Services.CardService import CardService
from sqlalchemy import inspect

class Base(DeclarativeBase):
    pass


#db = SQLAlchemy(model_class=Base)

class Serializer:
    @staticmethod
    def serialize_query_set(query_set):
        return [Serializer.serialize(i) for i in query_set]

    @staticmethod
    def serialize(self):
        i: dict = {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}#vars(self)
        copy_dict = {}
        for key, value in i.items():
            if key == "_sa_instance_state":
                continue
            copy_dict[Serializer.underscore_to_camel_case(key)] = value
        return copy_dict

    @staticmethod
    def underscore_to_camel_case(key: str):
        # find underscore and convert next letter to uppercase
        return key[0] + key.title().replace("_", "")[1:]



class DatabaseManager:
    db = SQLAlchemy(model_class=Base)

    def __init__(self, app: Flask):
        self.app = app

    def init_database(self):
        db_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "LocalStorage"))
        os.makedirs(db_folder, exist_ok=True)
        self.app.config["SQLALCHEMY_DATABASE_URI"] = f'sqlite:///{os.path.join(db_folder, "project.db")}'
        self.db.init_app(self.app)
        with self.app.app_context():
            self.db.create_all()


class UserDB(DatabaseManager.db.Model):
    username: Mapped[str] = mapped_column(DatabaseManager.db.String, nullable=False, primary_key=True)
    password: Mapped[str] = mapped_column(DatabaseManager.db.String, nullable=False)
    salt: Mapped[str] = mapped_column(DatabaseManager.db.String, nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password
        }


class RoundDB(DatabaseManager.db.Model):
    id: Mapped[str] = mapped_column(DatabaseManager.db.String, nullable=False, primary_key=True)
    game_id: Mapped[str] = mapped_column(DatabaseManager.db.String, nullable=False)
    status: Mapped[int] = mapped_column(DatabaseManager.db.Integer, nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'game_id': self.game_id,
            'status': self.status
        }


class GameDB(DatabaseManager.db.Model):
    id: Mapped[str] = mapped_column(DatabaseManager.db.String, nullable=False, primary_key=True)
    is_active: Mapped[bool] = mapped_column(DatabaseManager.db.Boolean, nullable=False, default=True)
    name: Mapped[str] = mapped_column(DatabaseManager.db.String, nullable=False)
    has_started: Mapped[bool] = mapped_column(DatabaseManager.db.Boolean, nullable=False, default=False)
    active_round: Mapped[str] = mapped_column(DatabaseManager.db.String, nullable=True, default=None)
    dealer: Mapped[str] = mapped_column(DatabaseManager.db.String, nullable=True, default=None)

    def serialize(self):
        return {
            'id': self.id,
            'isActive': self.is_active,
            'name': self.name,
            'has_started': self.has_started,
            'active_round': self.active_round,
            'dealer': self.dealer
        }


class PlayerDB(DatabaseManager.db.Model):
    id: Mapped[str] = mapped_column(DatabaseManager.db.String, nullable=False, primary_key=True)
    position: Mapped[int] = mapped_column(DatabaseManager.db.Integer, nullable=False)
    chips: Mapped[int] = mapped_column(DatabaseManager.db.Integer, nullable=False)
    game_id: Mapped[str] = mapped_column(DatabaseManager.db.String, nullable=False)
    user_id: Mapped[str] = mapped_column(DatabaseManager.db.String, nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'position': self.position,
            'chips': self.chips,
            'game_id': self.game_id,
            'user_id': self.user_id
        }


class RoundPlayerDB(DatabaseManager.db.Model):
    id_round: Mapped[str] = mapped_column(DatabaseManager.db.String, nullable=False, primary_key=True)
    id_player: Mapped[str] = mapped_column(DatabaseManager.db.String, nullable=False, primary_key=True)
    at_play: Mapped[bool] = mapped_column(DatabaseManager.db.Boolean, nullable=False)
    has_played: Mapped[bool] = mapped_column(DatabaseManager.db.Boolean, nullable=False)
    set_chips: Mapped[int] = mapped_column(DatabaseManager.db.Integer, nullable=False)
    is_active: Mapped[bool] = mapped_column(DatabaseManager.db.Boolean, nullable=False)
    position: Mapped[int] = mapped_column(DatabaseManager.db.Integer, nullable=False)
    card_1: Mapped[int] = mapped_column(DatabaseManager.db.Integer)
    card_2: Mapped[int] = mapped_column(DatabaseManager.db.Integer)

    def serialize(self):
        return {
            'id_round': self.id_round,
            'id_player': self.id_player,
            'at_play': self.at_play,
            'set_chips': self.set_chips,
            'is_active': self.is_active,
            'position': self.position,
            'card_1': CardService.parse_card_object_from_db(self.card_1),
            'card_2': CardService.parse_card_object_from_db(self.card_2)
        }


class RoundCardsDB(DatabaseManager.db.Model):
    id_round: Mapped[str] = mapped_column(DatabaseManager.db.String, nullable=False, primary_key=True)
    id_cards: Mapped[int] = mapped_column(DatabaseManager.db.Integer, nullable=False, primary_key=True)
    position: Mapped[int] = mapped_column(DatabaseManager.db.Integer, nullable=False)

    def serialize(self):
        return {
            'id_round': self.id_round,
            'id_cards': CardService.parse_card_object_from_db(self.id_cards),
            'position': self.position,
        }
