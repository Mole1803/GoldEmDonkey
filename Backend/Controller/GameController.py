import functools

from flask import request,Blueprint, jsonify

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

    @staticmethod
    @jwt_required()
    @game_controller.route('/hasActiveGame', methods=['GET'])
    def get_active_game():
        # Todo checks if user has a game -> if so check if game is running -> join_room else

        return jsonify(),200
        raise NotImplementedError


    @staticmethod
    @SocketIOController.socketio.on('joinGame')
    def join_game(data):
        print(data)
        #if "username" not in data or "gameId" not in data:
        #    return
        username = data['username']
        gameId = data['gameId']
        player = BaseController.dependencies.poker_handler.join_game(username, gameId)
        user_list = GameService.select_player_get_all_players_by_game(gameId, BaseController.dependencies.db_context)
        game_ = GameService.select_game_by_id(gameId, BaseController.dependencies.db_context)
        join_room(room=gameId)
        json_ = {"player": Serializer.serialize(player),"game": Serializer.serialize(game_), "players": Serializer.serialize_query_set(user_list), "gameId": gameId}
        emit('joinedGame', json_, room=gameId,include_self=True)
        #return "Joined game successfully."

    @staticmethod
    @SocketIOController.socketio.on('startGame')
    def start_game(data):
        print("startGame", data)
        gameId = data['gameId']
        #username = data['username']
        BaseController.dependencies.poker_handler.run_game(gameId)
        emit('startGame', room=gameId)
        GameController.send_instruction_messages(gameId)



    @staticmethod
    @SocketIOController.socketio.on('performCheck')
    def receive_perform_check(data):
        print("performCheck", data)
        gameId = data['gameId']
        username = data['username']
        BaseController.dependencies.poker_handler.on_player_check(username, gameId)
        emit('performCheck', {"username": username}, room=gameId)
        GameController.send_instruction_messages(gameId)



    @staticmethod
    @SocketIOController.socketio.on('performFold')
    def receive_perform_fold(data):
        print("performFold", data)
        gameId = data['gameId']
        username = data['username']
        BaseController.dependencies.poker_handler.on_player_fold(username, gameId)
        GameController.send_instruction_messages(gameId)


    @staticmethod
    @SocketIOController.socketio.on('performRaise')
    def receive_perform_raise(data):
        print("performRaise", data)
        gameId = data['gameId']
        username = data['username']
        raise_value = data['raise_value']
        BaseController.dependencies.poker_handler.on_player_raise(username, gameId, raise_value)
        GameController.send_instruction_messages(gameId)


    @staticmethod
    @SocketIOController.socketio.on('performCall')
    def receive_perform_call(data):
        print("performCall", data)
        gameId = data['gameId']
        username = data['username']
        BaseController.dependencies.poker_handler.on_player_call(username, gameId)
        GameController.send_instruction_messages(gameId)



    @staticmethod
    @SocketIOController.socketio.on('leave')
    def on_leave_room(data):
        username = data['username']
        # Todo find active room and disconnect
        gameId = data['gameId']
        leave_room(gameId)
        send(username + ' has left the room.', to=gameId)

    @staticmethod
    @SocketIOController.socketio.on('disconnect')
    def on_disconnect():
        return
        playerId = GameService
        emit('disconnect', {'playerId': playerId})
        print('Client disconnected')

    @staticmethod
    def send_instruction_messages(gameId):
        while BaseController.dependencies.poker_handler.instructionQueue.not_empty():
            instruction = BaseController.dependencies.poker_handler.instructionQueue.get()
            emit('instruction', instruction, room=gameId)

