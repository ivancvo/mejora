from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from ..modelos.modelos import Reserva, Usuario, Vehiculo
from ..modelos import db

class ReservaVista(Resource):
    def post(self):
        # Usamos request.json.get() para obtener datos del cuerpo de la solicitud
        usuario_id = request.json.get('usuario_id')
        vehiculo_id = request.json.get('vehiculo_id')
        fecha_reserva = request.json.get('Fecha_Reserva')
        fin_reserva = request.json.get('Fin_Reserva')

        # Verificamos que todos los datos necesarios hayan sido enviados
        if not usuario_id or not vehiculo_id or not fecha_reserva or not fin_reserva:
            return {'message': 'Faltan datos requeridos'}, 400

        # Creamos una nueva reserva
        nueva_reserva = Reserva(
            usuario_id=usuario_id,
            vehiculo_id=vehiculo_id,
            Fecha_Reserva=fecha_reserva,
            Fin_Reserva=fin_reserva
        )

        # Guardamos la reserva en la base de datos
        db.session.add(nueva_reserva)
        db.session.commit()

        return {'message': 'Reserva creada con éxito', 'reserva': nueva_reserva.Id_Reserva}, 201

    def delete(self, reserva_id):
        # Borramos una reserva por su ID
        reserva = Reserva.query.get(reserva_id)
        if not reserva:
            return {'message': 'Reserva no encontrada'}, 404

        db.session.delete(reserva)
        db.session.commit()

        return {'message': 'Reserva eliminada con éxito'}, 200

    def put(self, reserva_id):
        # Actualizamos una reserva existente
        reserva = Reserva.query.get(reserva_id)
        if not reserva:
            return {'message': 'Reserva no encontrada'}, 404

        # Obtenemos los nuevos datos
        reserva.Fecha_Reserva = request.json.get('Fecha_Reserva', reserva.Fecha_Reserva)
        reserva.Fin_Reserva = request.json.get('Fin_Reserva', reserva.Fin_Reserva)
        reserva.usuario_id = request.json.get('usuario_id', reserva.usuario_id)
        reserva.vehiculo_id = request.json.get('vehiculo_id', reserva.vehiculo_id)

        db.session.commit()

        return {'message': 'Reserva actualizada con éxito', 'reserva': reserva.Id_Reserva}, 200
