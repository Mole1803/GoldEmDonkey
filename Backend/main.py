from flask import Flask, render_template, request
from flask_swagger_ui import get_swaggerui_blueprint
from flasgger import Swagger
from _DatabaseCall import app
from flask import Flask,jsonify,request
from flask_sqlalchemy import SQLAlchemy
from Backend.Controller import AuthentificationController
from flask_cors import CORS



swagger = Swagger(app, template={
    "info": {
        "title": "My Flask API",
        "description": "An example API using Flask and Swagger",
        "version": "1.0.0"
    }
})
CORS(app, resources={r"/*": {"origins": "http://localhost:4200"}})

authentification_controller = AuthentificationController.LoginController(app)

@app.route("/")
def home():
    return jsonify({
        "Message": "app up and running successfully"
    })


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8080)
