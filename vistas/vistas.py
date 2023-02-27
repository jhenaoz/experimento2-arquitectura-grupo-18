from flask import request
from ..modelos import db, OrdenCompra
from flask_restful import Resource

class VistaOrdenCompra(Resource):
    def post(self):
        nueva_orden = OrdenCompra(direccion=request.json['direccion'],           
            vendedor=request.json['vendedor'],
            detalle_orden=request.json['detalle_orden'],
            estado=request.json['estado']
        )
        db.session.add(nueva_orden)
        db.session.commit()
        return "Orden generada exitosamente", 201