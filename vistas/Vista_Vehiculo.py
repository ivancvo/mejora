from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from cloudinary.uploader import upload
from ..modelos.modelos import db, Vehiculo, VehiculoSchema, Usuario

Vehiculo_Schema = VehiculoSchema()

class Vista_Vehiculo(Resource):
    
    @jwt_required()
    def get(self):
        vehiculos = Vehiculo.query.all()
        return [Vehiculo_Schema.dump(vehiculo) for vehiculo in vehiculos]

    # Crear un nuevo vehículo solo el rol admin
    @jwt_required()
    def post(self):
        # Verificar si el usuario tiene el rol admin
        current_user = get_jwt_identity()
        usuario = Usuario.query.get(current_user)

        if usuario.rol.Nombre != 'admin':
            return {'message': 'No tienes permisos para realizar esta acción'}, 403
        
        # Subir la foto a Cloudinary
        file = request.files.get('Foto_Vehiculo') 
        if file:
            result = upload(file)
            foto_url = result['secure_url']
        else:
            return {'message': 'Se requiere una imagen'}, 400

        # Crear el nuevo vehículo
        vehiculo = Vehiculo(
            Marca=request.json.get('Marca'),
            Modelo=request.json.get('Modelo'),
            Estado=request.json.get('Estado'),
            Foto_Vehiculo=foto_url  #guardamos la url de la imagen
        )
        
        
        db.session.add(vehiculo)
        db.session.commit()
        
       
        return Vehiculo_Schema.dump(vehiculo), 201

   
    @jwt_required()
    def put(self, Id_vehiculo):
        # Verificar si el usuario tiene el rol admin
        current_user = get_jwt_identity()
        usuario = Usuario.query.get(current_user)

        if usuario.rol.Nombre != 'admin':
            return {'message': 'No tienes permisos para realizar esta acción'}, 403

        # llamamos el vehiculo que necesitamops
        vehiculo = Vehiculo.query.get_or_404(Id_vehiculo)

        # Subir la foto a Cloudinary s cambia
        file = request.files.get('Foto_Vehiculo')
        if file:
            result = upload(file)
            foto_url = result['secure_url']
            vehiculo.Foto_Vehiculo = foto_url  

        
        vehiculo.Marca = request.json.get('Marca', vehiculo.Marca)
        vehiculo.Modelo = request.json.get('Modelo', vehiculo.Modelo)
        vehiculo.Estado = request.json.get('Estado', vehiculo.Estado)

        
        db.session.commit()

        return Vehiculo_Schema.dump(vehiculo)

    
    @jwt_required()
    def delete(self, Id_vehiculo):
       
        current_user = get_jwt_identity()
        usuario = Usuario.query.get(current_user)

        if usuario.rol.Nombre != 'admin':
            return {'message': 'No tienes permisos para realizar esta acción'}, 403

        
        vehiculo = Vehiculo.query.get_or_404(Id_vehiculo)
        
       
        db.session.delete(vehiculo)
        db.session.commit()

        return {'message': 'Vehículo eliminado exitosamente'}, 204
