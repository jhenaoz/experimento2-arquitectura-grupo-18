import requests
import os

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api
from modelos import db
from vistas.vistas import VistaOrdenesCompra
from vistas import VistaOrdenCompra, ViewLogIn, VistaSignIn, ViewRecover

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

api.add_resource(VistaOrdenesCompra, '/orden')
api.add_resource(VistaOrdenCompra,
                 '/orden/<int:id_orden>/usuario/<int:id_usuario>')
api.add_resource(VistaSignIn, '/signin')
api.add_resource(ViewLogIn, '/login')
api.add_resource(ViewRecover, '/credenciales')

jwt = JWTManager(app)

print('Starting server')


@app.route('/ping')
def ping():
    return "ok"


@app.route('/kill-program')
def fail():
    os._exit(12)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
