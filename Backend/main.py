import os

from dotenv import load_dotenv
from flasgger import Swagger
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO, join_room, emit

from Backend.Controller.BaseController import BaseController
from Backend.Controller.SocketIOController import SocketIOController
from Backend.Injector.DependencyInjector import DependencyInjector
from _DatabaseCall import DatabaseManager, Serializer
from Logic.PokerHandler import PokerHandler
import logging
#import eventlet
#eventlet.monkey_patch()
load_dotenv()
#from gevent import monkey
#monkey.patch_all()

settings = {}

logging.basicConfig(filename='socketio.log', level=logging.DEBUG)


class GoldEmDonkeyMain:
    def __init__(self, socketio: SocketIO = None):
        self.app = Flask(__name__)
        self.swagger = None
        self.db = None
        self.jwt = None
        self.socketio = socketio

        self.module_controllers: list[BaseController] = []
        self.dependencyInjector = DependencyInjector()
        self.DatabaseManager: DatabaseManager = DatabaseManager(self.app)
        self.PokerHandler: PokerHandler = PokerHandler(self.DatabaseManager.db)


    def run(self):
        self.socketio.run(self.app, port=8080)
        # self.app.run(debug=True, host="0.0.0.0", port=8080)

    def configure(self):
        self.configure_cors()
        self.setup_socketio()

        self.setup_database()
        self.configure_swagger()

        self.setup_jwt()
        self.setup_socketio_controller()
        self.setup_dependency_injector()

        self.init_all_controllers()
        self.configure_all_controllers()

    def setup_jwt(self):
        self.app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")
        self.jwt = JWTManager(self.app)

    def setup_socketio(self):
        self.app.config['DEBUG'] = True
        self.app.config['SECRET_KEY'] = os.environ.get("JWT_SECRET_KEY")
        if self.socketio is None:
            self.socketio = SocketIO(self.app,ping_timeout=60, ping_interval=30, cors_allowed_origins="*",always_connect=False,  manage_session=False, engineio_logger=True ) #, cors_allowed_origins="*"

    def setup_database(self):
        self.DatabaseManager.init_database()

    def setup_dependency_injector(self):
        self.dependencyInjector.db_context = self.DatabaseManager.db
        self.dependencyInjector.poker_handler = self.PokerHandler

    def configure_swagger(self):
        # Swagger can be found at http://localhost:8080/api/docs/
        self.swagger = Swagger(self.app, template={
            "info": {
                "title": "My Flask API",
                "description": "An example API using Flask and Swagger",
                "version": "1.0.0"
            }
        })

    def setup_socketio_controller(self):
        SocketIOController.set_socketio(self.socketio)

    def configure_cors(self):
        CORS(self.app, resources={r"/*": {"origins": "http://localhost:4200"}})

    def configure_all_controllers(self):
        for controller in self.module_controllers:
            if isinstance(controller, BaseController):
                controller.set_dependencies(self.dependencyInjector)
            if isinstance(controller, SocketIOController):
                controller.set_socketio(self.socketio)

    def init_all_controllers(self):
        from Backend.Controller import GameController
        from Backend.Controller import AuthentificationController

        self.module_controllers.append(AuthentificationController.LoginController(self.app))
        self.module_controllers.append(GameController.GameController(self.app))





if __name__ == '__main__':
    gold_em_donkey = GoldEmDonkeyMain()
    gold_em_donkey.configure()
    gold_em_donkey.run()
