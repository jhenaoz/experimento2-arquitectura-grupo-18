import requests
import os

from flask import Flask, request
from flask_jwt_extended import JWTManager
from flask_restful import Resource, Api
from modelos import db
from vistas import VistaOrdenCompra, ViewLogIn, VistaSignIn, ViewRecover
# from app import create_app

# app = create_app('default')
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///experimiento_dos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'frase-secreta'
app.config['PROPAGATE_EXCEPTIONS'] = True

app_context = app.app_context()
app_context.push()

api = Api(app)

db.init_app(app)
db.create_all()

api.add_resource(VistaOrdenCompra, '/orden')
api.add_resource(VistaSignIn, '/signin')
api.add_resource(ViewLogIn, '/login')
api.add_resource(ViewRecover, '/credenciales')

print('Starting server')


@app.route('/ping')
def ping():
    return "ok"


@app.route('/kill-program')
def fail():
    os._exit(12)

jwt = JWTManager(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
