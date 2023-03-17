import hashlib
from flask import request
from modelos import db, OrdenCompra, Usuario, EnumTipoUsuario
from flask_restful import Resource
from flask_jwt_extended import jwt_required, create_access_token
from datetime import datetime, timedelta


class VistaOrdenesCompra(Resource):
    @jwt_required()
    def post(self):
        nueva_orden = OrdenCompra(
            direccion=request.json['direccion'],
            vendedor_id=request.json['vendedor_id'],
            detalle_orden=request.json['detalle_orden'],
            estado=request.json['estado']
        )
        db.session.add(nueva_orden)
        db.session.commit()
        return "Orden generada exitosamente", 201
    
class VistaOrdenCompra(Resource):       
    @jwt_required()
    def put(self,id_orden,id_usuario):
        orden = OrdenCompra.query.filter(OrdenCompra.id == id_orden).first()        
        if (orden.vendedor_id != id_usuario):  
             return "El usuario no tiene permitido modificar esa compra", 401
        else:
            usuario = Usuario.query.filter(Usuario.id == id_usuario).first()          
            if (usuario is None):
                return "El usuario no existe", 401
            orden.direccion = request.json["direccion"]
            orden.detalle_orden = request.json["detalle_orden"]
            orden.estado = request.json["estado"]     
            db.session.add(orden)
            db.session.commit()      
            return "Orden actualizada exitosamente", 200
        
class VistaSignIn(Resource):

    def post(self):
        found = Usuario.query.filter(
            Usuario.username == request.json["username"]).first()
        if found is None:
            password_encrypted = hashlib.md5(
                request.json["password"].encode('utf-8')).hexdigest()
            new_usuario = Usuario(
                username=request.json["username"],
                password=password_encrypted,
                email=request.json["email"],
                rol=EnumTipoUsuario.DIRECTOR_COMPRAS.value,
                login_attempts=0,
                blocked_account=0
            )
            db.session.add(new_usuario)
            db.session.commit()
            return {"mensaje": "usuario creado exitosamente", "id": new_usuario.id}
        else:
            return "El usuario ya existe", 404


class ViewLogIn(Resource):
    def post(self):
        password_encrypted = hashlib.md5(
            request.json["password"].encode('utf-8')).hexdigest()

        user = Usuario.query.filter(
            Usuario.username == request.json["username"]
        ).first()

        db.session.commit()

        account_blocked = user.blocked_account

        # verificar si la no cuenta esta bloqueda o si ya pasó más de un día del bloqueo actual
        now = datetime.now()
        if user.blocked_time is None:
            difference = True
        else:            
            difference = datetime.utcnow() - user.blocked_time

        available = account_blocked != True or difference.days >= 1

        if user is not None:
            if available == True:
                if user.password == password_encrypted:
                    # Reiniciar las variables de control de acceso
                    if account_blocked == True:
                        user.login_attempts = 0
                        user.blocked_time = None
                        user.blocked_account = False
                        db.session.commit()

                    token_de_acceso = create_access_token(identity=user.id)
                    return {"mensaje": "Inicio de sesión exitoso", "token": token_de_acceso, "id": user.id, "rol": user.rol.value}

                else:
                    # Si la cuenta no esta bloqueada aun, debe contar los intentos
                    if account_blocked == False:
                        attempts = user.login_attempts or 0
                        attempts = attempts + 1
                        user.login_attempts = attempts

                        if attempts == 3:
                            user.blocked_account = True
                            user.blocked_time = datetime.today()

                        db.session.commit()
                    return "Login fallido", 404

            else:
                return "Cuenta bloqueada", 404

        else:
            return "El usuario no existe", 404
