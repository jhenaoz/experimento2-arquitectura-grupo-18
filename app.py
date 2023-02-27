from .modelos import db , OrdenCompra
from flask_restful import Resource, Api
from flask import Flask,request
from .vistas import VistaOrdenCompra
import requests
import os
from app import create_app

app = create_app('default')
app_context = app.app_context()
app_context.push()

api = Api(app)
db.init_app(app)
db.create_all()
    
api.add_resource(VistaOrdenCompra, '/orden')

print('Starting server')
@app.route('/ping')
def ping():
    return "ok"



@app.route('/kill-program')
def fail():
    os._exit(12)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
