from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_cors import CORS
from flaskr.modelos.modelos import db, Usuario, Rol
from flaskr.vistas import Vista_Usuario, Vista_Rol, Vista_Vehiculo, Vista_Login
from werkzeug.security import generate_password_hash

from flaskr import create_app


app = create_app('default')  


app_context = app.app_context()
app_context.push()

# Iniciar bd
db.init_app(app)

# Iniciar migraciones
migrate = Migrate(app, db)

# Iniciar la api
api = Api(app)

# Iniciar jwt
jwt = JWTManager(app)

# Iniciar cors
CORS(app)


api.add_resource(Vista_Usuario, '/usuarios')
api.add_resource(Vista_Rol, '/rol')
api.add_resource(Vista_Vehiculo, '/vehiculos', '/vehiculos/<int:Id_vehiculo>')
api.add_resource(Vista_Login, '/login')

# Crear el superadmin si no existe
def create_superadmin():
    admin_role = Rol.query.filter_by(Nombre='admin').first()
    if not admin_role:
        admin_role = Rol(Nombre='admin')
        db.session.add(admin_role)
        db.session.commit()

    superadmin = Usuario.query.filter_by(Email_Usu='superadmin@admin.com').first()
    if not superadmin:
        superadmin = Usuario(
            Nombre_Usu='Super Admin',
            Cedula_Usu='123456789',
            Email_Usu='superadmin@admin.com',
            Telefono_Usu='123456789',
            Contraseña_hash=generate_password_hash('superadminpassword'),
            rol_id=admin_role.Id_Rol
        )
        db.session.add(superadmin)
        db.session.commit()

# Ejecutar la función fdel super admin despues que la app inicie
with app.app_context():
    create_superadmin()


if __name__ == '__main__':
    app.run(debug=True, port=5001)  
