from marshmallow import fields
from flask_sqlalchemy import SQLAlchemy
import enum
from werkzeug.security import generate_password_hash, check_password_hash

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

db = SQLAlchemy()


class Rol(db.Model):
    Id_Rol = db.Column(db.Integer, primary_key=True)
    Nombre = db.Column(db.String(180))
    usuario = db.relationship("Usuario", back_populates="rol")

class Usuario(db.Model):
    Id_Usuario = db.Column(db.Integer, primary_key=True)
    Nombre_Usu = db.Column(db.String(250))
    Contraseña_hash = db.Column(db.String(255))
    Cedula_Usu = db.Column(db.String(20))
    Email_Usu = db.Column(db.String(250))
    Telefono_Usu = db.Column(db.String(15))
    rol_id = db.Column(db.Integer, db.ForeignKey('rol.Id_Rol'))
    rol = db.relationship("Rol", back_populates="usuario")
    reserva = db.relationship("Reserva", back_populates="usuario") 

class Reserva(db.Model):
    Id_Reserva = db.Column(db.Integer, primary_key=True)
    Fecha_Reserva = db.Column(db.Date)
    Fin_Reserva = db.Column(db.Date)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.Id_Usuario'))  
    usuario = db.relationship("Usuario", back_populates="reserva")  
    vehiculo_id = db.Column(db.Integer, db.ForeignKey('vehiculo.Id_vehiculo'))
    vehiculo = db.relationship("Vehiculo", back_populates="reserva")



class Vehiculo(db.Model):
    Id_vehiculo = db.Column(db.Integer, primary_key=True)
    Marca = db.Column(db.String(100))
    Modelo = db.Column(db.String(100))
    Estado = db.Column(db.Enum('disponible', 'alquilado'))
    Foto_Vehiculo = db.Column(db.String(255))  # Almacenar la ruta de la imagen
    reserva = db.relationship("Reserva", uselist=False, back_populates="vehiculo")



#SERIALIZACION


class RolSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Rol
        include_relationships = True
        load_instance = True


class UsuarioSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario
        # Excluir la contraseña por seguridad
        exclude = ('Contraseña_hash',)
        include_relationships = True
        load_instance = True

class ReservaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Reserva
        include_relationships = True
        load_instance = True

class VehiculoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Vehiculo
        include_relationships = True
        load_instance = True