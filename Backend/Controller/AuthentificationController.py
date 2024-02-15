from flask import request, jsonify, Flask
from Backend.Services.AuthentificationService import AuthService
from flask import Blueprint
from Backend.Model.Login.LoginParser import LoginParser
from Backend.Controller.BaseController import BaseController

from flask_jwt_extended import (
    # JWTManager,
    create_access_token
)

login_controller = Blueprint('login_controller', __name__, url_prefix='/auth')


class LogInRouting:
    login = "/login"
    register = "/register"
    logout = "/logout"
    username_available = "/isUsernameAvailable"


class LoginController(BaseController):
    def __init__(self, app: Flask):
        app.register_blueprint(login_controller)

    @staticmethod
    @login_controller.route(LogInRouting.login, methods=['POST'])
    def login():
        """
        This is the login endpoint!
        ---
        tags:
            - POST
        parameters:
          - name: username
            in: path
            description: Username for login
            required: true
            type: string
        description: Used for the login!
        responses:
            200:
                description: A successful login
                examples:
                    application/json: "Login, successful!"
        """
        print(LoginController.dependencies.db_context)
        login = LoginParser.parse_from_request(request)
        user = AuthService.verify_user(login, LoginController.dependencies.db_context)
        if not user:
            return jsonify({"msg": "Bad username or password"}), 401
        access_token = create_access_token(identity=login.username)
        return jsonify(access_token=access_token), 200

    @staticmethod
    @login_controller.route(rule=LogInRouting.register, methods=['POST'])
    def register():
        """
        This is the login endpoint!
        ---
        tags:
            - POST
        parameters:
          - name: username
            required: true
            in: path
            type: string
          - name: password
            in: path
            required: true
            type: string
        description: Used for the login!
        responses:
            200:
                description: A successful login
                examples:
                    application/json: "Login, successful!"
                """
        login = LoginParser.parse_from_request(request)
        if AuthService.username_exists(login, LoginController.dependencies.db_context):
            return jsonify({"msg": "Username already exists"}), 400

        user = AuthService.add_user(login, LoginController.dependencies.db_context)
        if not user:
            return jsonify({"msg": "Username already exists"}), 400
        access_token = create_access_token(identity=login.username)
        return jsonify(access_token=access_token), 200

    @staticmethod
    @login_controller.route(rule=LogInRouting.username_available, methods=['POST'])
    def username_available():
        login = LoginParser.parse_from_request(request)
        return jsonify({"isUsernameAvailable": AuthService.username_exists(login, LoginController.dependencies.db_context), "username": login.username}), 200




