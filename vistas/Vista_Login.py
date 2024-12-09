from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash
from flask_restful import Resource
from flask import request
from ..modelos.modelos import Usuario, UsuarioSchema  # Asegúrate de que el modelo Usuario está importado correctamente

Usuario_Schema = UsuarioSchema()

class Vista_Login(Resource):
    def post(self):
      
        username = request.json.get('Nombre_Usu', None)
        password = request.json.get('Contraseña_hash', None)

        # Validamos que el nombre de usuario y la contraseña si estem puestos
        if not username or not password:
            return {'message': 'Falta introducir los datos'}, 400
        
        # Buscamos al usuario en bd
        usuario = Usuario.query.filter_by(Nombre_Usu=username).first()

        # Verificamos si el usuario existe y si la contraseña es correcta
        if not usuario or not check_password_hash(usuario.Contraseña_hash, password):
            return {'message': 'Usuario o contraseña incorrectos'}, 401
        
        # Si el usuario es válido, creamos el token
        acces_token = create_access_token(identity=str(usuario.Id_Usuario)) 


       
        return {'access_token': acces_token}, 200
