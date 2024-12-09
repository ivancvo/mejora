from flask_restful import Resource
from flask import request
from ..modelos.modelos import db, Usuario, UsuarioSchema
from werkzeug.security import generate_password_hash

Usuario_Schema = UsuarioSchema()

class Vista_Usuario(Resource):
    def get(self):
        return [Usuario_Schema.dump(Usuario) for Usuario in Usuario.query.all()]
    
    def post(self):
        # Obtener los valores desde la solicitud JSON
        username = request.json.get("Nombre_Usu")
        password = request.json.get("Contraseña_hash")  # Asegúrate de que el nombre sea "Contraseña_hash"
        
        # Verificar si la contraseña está presente
        if not password:
            return {"error": "La contraseña es requerida."}, 400  # Respuesta de error si no se recibe contraseña
        
        # Hashear la contraseña
        hashed_password = generate_password_hash(password)
        
        # Crear el nuevo usuario
        nuevo_usuario = Usuario(
            Nombre_Usu=username,
            Contraseña_hash=hashed_password,
            Cedula_Usu=request.json.get('Cedula_Usu'),
            Email_Usu=request.json.get('Email_Usu'),
            Telefono_Usu=request.json.get('Telefono_Usu'),
            rol_id=request.json.get('rol_id')  # Asegúrate de que el JSON tiene 'rol_id'
        )

        # Agregar a la base de datos
        db.session.add(nuevo_usuario)
        db.session.commit()
        
        # Retornar el usuario creado
        return Usuario_Schema.dump(nuevo_usuario), 201
    
    def put(self, Id_Usuario):
        # Obtener el usuario mediante el ID
        usuario = Usuario.query.get_or_404(Id_Usuario)
        
        # Actualizar campos
        usuario.Nombre_Usu = request.json.get('Nombre_Usu', usuario.Nombre_Usu)
        usuario.Contraseña_hash = request.json.get('Contraseña_hash', usuario.Contraseña_hash)  # Cambié 'contraseña_hash' por 'Contraseña_hash'
        usuario.Cedula_Usu = request.json.get('Cedula_Usu', usuario.Cedula_Usu)
        usuario.Email_Usu = request.json.get('Email_Usu', usuario.Email_Usu)
        usuario.Telefono_Usu = request.json.get('Telefono_Usu', usuario.Telefono_Usu)
        usuario.rol_id = request.json.get('rol_id', usuario.rol_id)  # Asegúrate de que el JSON tiene 'rol_id'

        # Si la contraseña se actualiza, debe ser hasheada nuevamente
        if request.json.get('Contraseña_hash'):
            usuario.Contraseña_hash = generate_password_hash(request.json['Contraseña_hash'])
        
        db.session.commit()
        return Usuario_Schema.dump(usuario)
    
    def delete(self, Id_Usuario):
        usuario = Usuario.query.get_or_404(Id_Usuario)  # Obtener el usuario
        db.session.delete(usuario)  # Eliminar el usuario
        db.session.commit()  # Guardar los cambios
        return 'Se eliminó el usuario exitosamente.', 204
