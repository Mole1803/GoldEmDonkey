from flask import Blueprint

from Backend.Controller.BaseController import BaseController
from Backend.Controller.SocketIOController import SocketIOController

game_controller = Blueprint('game_controller', __name__, url_prefix='/auth')


class GameController(BaseController, SocketIOController):
    def __init__(self, app):
        app.register_blueprint(game_controller)

    @staticmethod
    @SocketIOController.socketio.on('message')
    def get_game(msg):
        print("Connected to game!", msg)
        return "Game", 200
