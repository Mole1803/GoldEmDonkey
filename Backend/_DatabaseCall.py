from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///project.db'
db.init_app(app)


class UserDB(db.Model):
    username: Mapped[str] = mapped_column(db.String, nullable=False, primary_key=True)
    password: Mapped[str] = mapped_column(db.String, nullable=False)
    salt: Mapped[str] = mapped_column(db.String, nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password
        }


class RoundDB(db.Model):
    id: Mapped[str] = mapped_column(db.String, nullable=False, primary_key=True)
    max_raise: Mapped[int] = mapped_column(db.Integer, nullable=False)
    game_id: Mapped[str] = mapped_column(db.String, nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'max_raise': self.max_raise,
            'game_id': self.game_id
        }


class GameDB(db.Model):
    id: Mapped[str] = mapped_column(db.String, nullable=False, primary_key=True)

    def serialize(self):
        return {
            'id': self.id
        }


class PlayerDB(db.Model):
    id: Mapped[str] = mapped_column(db.String, nullable=False, primary_key=True)
    position: Mapped[int] = mapped_column(db.Integer, nullable=False)
    chips: Mapped[int] = mapped_column(db.Integer, nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'position': self.position,
            'chips': self.chips
        }


class RoundPlayerDB(db.Model):
    id: Mapped[str] = mapped_column(db.String, nullable=False, primary_key=True)
    id_round: Mapped[str] = mapped_column(db.String, nullable=False)
    id_player: Mapped[str] = mapped_column(db.String, nullable=False)
    at_play: Mapped[bool] = mapped_column(db.Boolean, nullable=False)
    set_chips: Mapped[int] = mapped_column(db.Integer, nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'id_round': self.id_round,
            'id_player': self.id_player,
            'at_play': self.at_play,
            'set_chips': self.set_chips
        }


class CardsDB(db.Model):
    id: Mapped[str] = mapped_column(db.String, nullable=False, primary_key=True)
    color: Mapped[str] = mapped_column(db.String, nullable=False)
    value: Mapped[int] = mapped_column(db.Integer, nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'color': self.color,
            'value': self.value
        }


class RoundCardsDB(db.Model):
    id_round: Mapped[str] = mapped_column(db.String, nullable=False, primary_key=True)
    id_cards: Mapped[str] = mapped_column(db.String, nullable=False, primary_key=True)
    position: Mapped[int] = mapped_column(db.Integer, nullable=False)

    def serialize(self):
        return {
            'id_round': self.id_round,
            'id_cards': self.id_cards,
            'position': self.position,
        }


class RoundPlayerCardsDB(db.Model):
    id_round_player: Mapped[str] = mapped_column(db.String, nullable=False, primary_key=True)
    id_cards: Mapped[str] = mapped_column(db.String, nullable=False, primary_key=True)

    def serialize(self):
        return {
            'id_round_player': self.id_round_player,
            'id_cards': self.id_cards
        }


with app.app_context():
    db.create_all()
