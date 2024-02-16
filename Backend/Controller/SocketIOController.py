from flask_socketio import SocketIO


class SocketIOController:
    socketio: SocketIO = None

    @staticmethod
    def set_socketio(socketio: SocketIO):
        SocketIOController.socketio = socketio
