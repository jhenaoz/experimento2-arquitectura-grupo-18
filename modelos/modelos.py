from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
import enum
db = SQLAlchemy()


class EnumTipoUsuario(enum.Enum):
    ADMIN: str = 'ADMIN'
    VENDEDOR: str = 'VENDEDOR'

class Estado(enum.Enum):
    CREADO = 1,
    PAGADO = 2,
    MORA = 3

class OrdenCompra(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    direccion = db.Column(db.String(255), nullable=True)
    fecha = db.Column(db.DateTime(timezone=True), server_default=func.now())
    # vendedor = db.Column(db.String(255), nullable=True)
    detalle_orden = db.Column(db.String(255), nullable=True)
    estado = db.Column(db.Enum(Estado))
    vendedor_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    vendedor = db.relationship(
        'Usuario', back_populates='ordenes')

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(100))
    email = db.Column(db.String(100))
    blocked_account = db.Column(db.Boolean())
    blocked_time = db.Column(db.DateTime(), server_default=None)
    rol = db.Column(db.Enum(EnumTipoUsuario))
    ordenes = db.relationship('OrdenCompra', back_populates='vendedor')
