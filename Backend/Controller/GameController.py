from flask import Blueprint

from Backend.Controller.BaseController import BaseController
from Backend.Controller.SocketIOController import SocketIOController
from Backend.Services.GameService import GameService
from Backend._DatabaseCall import Serializer
from flask_socketio import join_room, send, leave_room
from flask_jwt_extended import jwt_required

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
        return Serializer.serialize_query_set(games), 200

    @staticmethod
    @game_controller.route(GameRouting.create_game, methods=['GET'])
    def create_game():
        return "Game created", 200

    @staticmethod
    @jwt_required()
    @game_controller.route('/hasActiveGame', methods=['GET'])
    def get_active_game():
        # Todo checks if user has a game -> if so check if game is running -> join_room else
        raise NotImplementedError


    @staticmethod
    @SocketIOController.socketio.on('message')
    def get_game(msg):

        print("Connected to game!", msg)
        return "Game", 200

    @staticmethod
    @SocketIOController.socketio.on('join')
    def on_join_room(data):
        username = data["username"]
        room = data["room"]
        join_room(room)
        send(username + " has joined the room.", to=room)

    @staticmethod
    @SocketIOController.socketio.on('connect')
    def on_connect():
        # Todo checks if user has a game -> if so check if game is running -> join_room else
        raise NotImplementedError

    @staticmethod
    @SocketIOController.socketio.on('leave')
    def on_leave_room(data):
        username = data['username']
        # Todo find active room and disconnect
        room = data['room']
        leave_room(room)
        send(username + ' has left the room.', to=room)
