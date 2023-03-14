from flask import request
from modelos import db, OrdenCompra, Usuario, EnumTipoUsuario
from flask_restful import Resource
from flask_jwt_extended import jwt_required, create_access_token
import hashlib


class VistaOrdenCompra(Resource):
    def post(self):
        nueva_orden = OrdenCompra(
            direccion=request.json['direccion'],
            vendedor=request.json['vendedor'],
            detalle_orden=request.json['detalle_orden'],
            estado=request.json['estado']
        )
        db.session.add(nueva_orden)
        db.session.commit()
        return "Orden generada exitosamente", 201


class VistaSignIn(Resource):

    def post(self):
        found = Usuario.query.filter(
            Usuario.username == request.json["username"]).first()
        if found is None:
            password_encrypted = hashlib.md5(
                request.json["password"].encode('utf-8')).hexdigest()
            new_usuario = Usuario(
                username=request.json["username"], password=password_encrypted, email=request.json["email"], rol=EnumTipoUsuario.VENDEDOR.value)
            db.session.add(new_usuario)
            db.session.commit()
            return {"mensaje": "usuario creado exitosamente", "id": new_usuario.id}
        else:
            return "El usuario ya existe", 404


class ViewLogIn(Resource):
    def post(self):
        password_encrypted = hashlib.md5(
            request.json["password"].encode('utf-8')).hexdigest()
        user = Usuario.query.filter(Usuario.username == request.json["username"],
                                    Usuario.password == password_encrypted).first()
        db.session.commit()

        rol = None
        if user.rol is None:
            rol = ''
        else:
            rol = user.rol.value

        if user is None:
            return "El usuario no existe", 404
        else:
            token_de_acceso = create_access_token(identity=user.id)
            return {"mensaje": "Inicio de sesión exitoso", "token": token_de_acceso, "id": user.id, "rol": rol}
