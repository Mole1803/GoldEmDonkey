from flask import Flask, render_template, request
from flask_swagger_ui import get_swaggerui_blueprint
from flasgger import Swagger
from Backend.Injector.DependencyInjector import DependencyInjector
from Backend.Controller.BaseController import BaseController
from Backend.Helper.SetupHelper import SetupHelper
from _DatabaseCall import DatabaseManager
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from Backend.Controller import AuthentificationController
from flask_cors import CORS

settings = {
    #"database_url": 'sqlite:///project.db',
}


class GoldEmDonkeyMain:
    def __init__(self):
        self.app = Flask(__name__)
        self.swagger = None
        self.db = None

        self.module_controllers: list[BaseController] = []
        self.dependencyInjector = DependencyInjector()
        self.DatabaseManager: DatabaseManager = DatabaseManager(self.app)

    def run(self):
        self.configure()
        self.app.run(debug=True, host="0.0.0.0", port=8080)

    def configure(self):
        self.setup_database()
        self.configure_swagger()
        self.configure_cors()

        self.setup_dependy_injector()
        self.init_all_controllers()

    def setup_database(self):
        self.DatabaseManager.init_database()

    def setup_dependy_injector(self):
        self.dependencyInjector.db_context = self.DatabaseManager.db

    def configure_swagger(self):
        # Swagger can be found at http://localhost:8080/api/docs/
        self.swagger = Swagger(self.app, template={
            "info": {
                "title": "My Flask API",
                "description": "An example API using Flask and Swagger",
                "version": "1.0.0"
            }
        })

    def configure_cors(self):
        CORS(self.app, resources={r"/*": {"origins": "http://localhost:4200"}})

    def init_all_controllers(self):
        self.module_controllers.append(AuthentificationController.LoginController(self.app))

        for controller in self.module_controllers:
            controller.set_dependencies(self.dependencyInjector)


if __name__ == '__main__':
    gold_em_donkey = GoldEmDonkeyMain()
    gold_em_donkey.run()
