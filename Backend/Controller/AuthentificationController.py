from flask import request, jsonify
from Backend.Services.AuthentificationService import AuthService
from flask import Blueprint

from flask_jwt_extended import (
    #JWTManager,
    create_access_token
)

login_controller = Blueprint('login_controller', __name__, url_prefix='/auth')

class LoginController:
    def __init__(self, app):
        app.register_blueprint(login_controller)

    @staticmethod
    @login_controller.route('/login', methods=['POST'])
    def login():
        username = request.json.get('username', None)
        password = request.json.get('password', None)
        user = AuthService().verify_user(username, password)
        if not user:
            return jsonify({"msg": "Bad username or password"}), 401
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200


