import functools

from flask import Blueprint, jsonify

from Backend.Controller.BaseController import BaseController
from Backend.Controller.SocketIOController import SocketIOController
from Backend.Model.dto.Game import Game
from Backend.Services.GameService import GameService
from Backend._DatabaseCall import Serializer
from flask_socketio import join_room, send, leave_room, emit
from flask_jwt_extended import jwt_required

game_controller = Blueprint('game_controller', __name__, url_prefix='/game')


class GameRouting:
    create_game = "/createGame"
    list_active_games = "/listActiveGames"

class GameController(BaseController, SocketIOController):
    def __init__(self, app):
        app.register_blueprint(game_controller)

    @staticmethod
    @jwt_required()
    @game_controller.route(GameRouting.list_active_games, methods=['GET'])
    def list_active_games():
        games = GameService.select_game_get_all_active_games(BaseController.dependencies.db_context)
        return Serializer.serialize_query_set(games), 200

    @staticmethod
    @jwt_required()
    @game_controller.route(GameRouting.create_game, methods=['POST'])
    def create_game():
        BaseController.dependencies.db_context.session.flush()
        game = GameService.insert_game_db(db_context=BaseController.dependencies.db_context)
        game_ = Serializer.serialize(game)
        return jsonify(game_), 200





    #@staticmethod
    #@jwt_required()
    #@game_controller.route('/hasActiveGame', methods=['GET'])
    #def get_active_game():
        # Todo checks if user has a game -> if so check if game is running -> join_room else
    #    return
    #    raise NotImplementedError

    @staticmethod
    @SocketIOController.socketio.on('joinGame')
    def join_game(data):
        print(data)
        username = data['username']
        gameId = data['gameId']
        # Todo: add player to playerDB
        player = BaseController.dependencies.poker_handler.join_game(username, gameId)
        user_list = GameService.select_player_get_all_players_by_game(gameId, BaseController.dependencies.db_context)
        join_room(gameId)
        json_ = {"player": Serializer.serialize(player), "players": Serializer.serialize_query_set(user_list), "room": gameId}
        emit('joinGame', json_, room=gameId)


    @staticmethod
    @SocketIOController.socketio.on('startGame')
    def start_game(data):
        room = data['room']
        username = data['username']
        BaseController.dependencies.poker_handler.run_game(username)

        #send("start game", to=room)


    @staticmethod
    @SocketIOController.socketio.on('performCheck')
    def receive_perform_check(data):
        room = data['room']
        username = data['username']
        BaseController.dependencies.poker_handler.on_player_check(username, room)
        emit('performCheck', {"username": username}, room=room)
        # return next move
        #send("player checked", to=room)

    @staticmethod
    @SocketIOController.socketio.on('performFold')
    def receive_perform_fold(data):
        room = data['room']
        username = data['username']
        BaseController.dependencies.poker_handler.on_player_fold(username, room)
        # return next move
        #send("player folded", to=room)

    @staticmethod
    @SocketIOController.socketio.on('performRaise')
    def receive_perform_raise(data):
        room = data['room']
        username = data['username']
        raise_value = data['raise_value']
        BaseController.dependencies.poker_handler.on_player_raise(username, room, raise_value)
        # return next move
        #send("player raised", to=room)

    @staticmethod
    @SocketIOController.socketio.on('performCall')
    def receive_perform_call(data):
        room = data['room']
        username = data['username']
        BaseController.dependencies.poker_handler.on_player_call(username, room)
        # return next move
        #send("player called", to=room)


    @staticmethod
    def perform_next_action(move, room):
        # Todo: implement
        send(move, to=room)


    @staticmethod
    @SocketIOController.socketio.on('join')
    def on_join_room(data):
        username = data["username"]
        room = data["room"]
        join_room(room)
        send(username + " has joined the room.", to=room)


    @staticmethod
    @SocketIOController.socketio.on('leave')
    def on_leave_room(data):
        username = data['username']
        # Todo find active room and disconnect
        room = data['room']
        leave_room(room)
        send(username + ' has left the room.', to=room)

    @staticmethod
    @SocketIOController.socketio.on('disconnect')
    def on_disconnect():
        return
        playerId = GameService
        emit('disconnect', {'playerId': playerId})
        print('Client disconnected')
