from flask import Flask, render_template, request
from flask_swagger_ui import get_swaggerui_blueprint
from _DatabaseCall import app
# from crypt import methods
from flask import Flask,jsonify,request
from flask_sqlalchemy import SQLAlchemy
from Backend.Controller import AuthentificationController
from flask_cors import CORS

#app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:4200"}})

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'

#swaggerui_blueprint = get_swaggerui_blueprint(
#    SWAGGER_URL,
#    API_URL,
#    config={
#        'app_name': "Access API"
#    }
#)





#app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
authentification_controller = AuthentificationController.LoginController(app)

@app.route("/")
def home():
    return jsonify({
        "Message": "app up and running successfully"
    })


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8080)
