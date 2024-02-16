from flask import Blueprint

from Backend.Controller.BaseController import BaseController
from Backend.Controller.SocketIOController import SocketIOController
from Backend.Services.GameService import GameService

game_controller = Blueprint('game_controller', __name__, url_prefix='/game')

class GameRouting:
    create_game = "/createGame"
    list_active_games = "/listActiveGames"

class GameController(BaseController, SocketIOController):
    def __init__(self, app):
        app.register_blueprint(game_controller)

    @staticmethod
    @game_controller.route(GameRouting.list_active_games, methods=['GET'])
    def list_active_games():
        games = GameService.get_all_active_games(BaseController.dependencies.db_context)
        return games, 200

    @staticmethod
    @game_controller.route(GameRouting.create_game, methods=['GET'])
    def create_game():

        return "Game created", 200



    @staticmethod
    @SocketIOController.socketio.on('message')
    def get_game(msg):

        print("Connected to game!", msg)
        return "Game", 200


