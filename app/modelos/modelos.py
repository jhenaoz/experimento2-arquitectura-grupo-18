from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
import enum
db = SQLAlchemy()

class Estado(enum.Enum):
    CREADO = 1,
    PAGADO = 2,
    MORA = 3

class OrdenCompra(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    direccion = db.Column(db.String(255), nullable=True)
    fecha = db.Column(db.DateTime(timezone=True), server_default=func.now())
    vendedor = db.Column(db.String(255), nullable=True)
    detalle_orden = db.Column(db.String(255), nullable=True)
    estado = db.Column(db.Enum(Estado))



    