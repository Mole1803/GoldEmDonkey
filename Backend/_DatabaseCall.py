from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///project.db'
db.init_app(app)


class User(db.Model):
    name: Mapped[str] = mapped_column(db.String, nullable=False, primary_key=True)
    password: Mapped[str] = mapped_column(db.String, nullable=False)
    salt: Mapped[str] = mapped_column(db.String, nullable=False)

    def serialize(self):
        return {
            'name': self.name,
            'password': self.password,
            'salt': self.salt
        }

class Player(db.Model):
    id: Mapped[str] = mapped_column(db.String, primary_key=True, nullable=False)
    chips: Mapped[int] = mapped_column(db.Integer, nullable=False)
    position: Mapped[int] = mapped_column(db.Integer, nullable=False)

    def serialize(self):
        return {
            'chips': self.chips,
            'position': self.position
        }

class Round(db.Model):
    id: Mapped[str] = mapped_column(db.String, primary_key=True, nullable=False)
    maxStake: Mapped[int] = mapped_column(db.Integer, nullable=False)

    def serialize(self):
        return {
            'maxStake': self.maxStake
        }

class PlayerRound(db.Model):
    playerID: Mapped[str] = mapped_column(db.String, primary_key=True, nullable=False)
    roundID: Mapped[str] = mapped_column(db.String, primary_key=True, nullable=False)
    inRound: Mapped[bool] = mapped_column(db.Boolean, nullable=False)
    atPlay: Mapped[bool] = mapped_column(db.Boolean, nullable=False)
    setChips: Mapped[int] = mapped_column(db.Integer, nullable=False)
    card1: Mapped[str] = mapped_column(db.String, nullable=False)
    card2: Mapped[str] = mapped_column(db.String, nullable=False)

    def serialize(self):
        return {
            'inRound': self.inRound,
            'atPlay': self.atPlay,
            'setChips': self.setChips,
            'card1': self.card1,
            'card2': self.card2
        }

class Game(db.Model):
    gameID: Mapped[str] = mapped_column(db.String, primary_key=True, nullable=False)

class GameRound(db.Model):
    gameID: Mapped[str] = mapped_column(db.String, primary_key=True, nullable=False)
    roundID: Mapped[str] = mapped_column(db.String, primary_key=True, nullable=False)

class Card(db.Model):
    colorID: Mapped[str] = mapped_column(db.String, primary_key=True, nullable=False)
    value: Mapped[str] = mapped_column(db.String, primary_key=True, nullable=False)

    def serialize(self):
        return {
            'colorID': self.colorID,
            'value': self.value
        }

class RoundCards(db.Model):
    roundID: Mapped[str] = mapped_column(db.String, primary_key=True, nullable=False)
    card: Mapped[str] = mapped_column(db.String, nullable=False)
    position: Mapped[int] = mapped_column(db.Integer, nullable=False)

    def serialize(self):
        return {
            'card': self.card,
            'position': self.position
        }


with app.app_context():
    db.create_all()
