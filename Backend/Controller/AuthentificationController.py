from flask import request, jsonify
from Backend.Services.AuthentificationService import AuthService
from flask import Blueprint
from Backend.Model.Login.LoginParser import LoginParser

from flask_jwt_extended import (
    #JWTManager,
    create_access_token
)

login_controller = Blueprint('login_controller', __name__, url_prefix='/auth')


class LogInRouting:
    login = "/login"
    register = "/register"



class LoginController:
    def __init__(self, app):
        app.register_blueprint(login_controller)

    @staticmethod
    @login_controller.route(LogInRouting.login, methods=['POST'])
    def login():
        login = LoginParser.parse_from_request(request)
        user = AuthService().verify_user(login)
        if not user:
            return jsonify({"msg": "Bad username or password"}), 401
        access_token = create_access_token(identity=login.username)
        return jsonify(access_token=access_token), 200

    @staticmethod
    @login_controller.route(rule=LogInRouting.register, methods=['POST'])
    def register():
        raise NotImplementedError
