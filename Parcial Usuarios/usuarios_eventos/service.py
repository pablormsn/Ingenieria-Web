import json
import os

import pymongo
import requests
from bson import json_util
from bson.objectid import ObjectId
from dotenv import load_dotenv
from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta

load_dotenv()
MONGO_URL = os.getenv("MONGO_URL")

eventos_bp = Blueprint("eventos_bp", __name__)
usuarios_bp = Blueprint("usuarios_bp", __name__)

# Conexión a la base de datos
client = pymongo.MongoClient(MONGO_URL)
db = client.Kalendas
eventos = db.eventos
usuarios = db.usuarios
contactos = db.contactos

#CRUD de usuarios
# GET /usuarios
@usuarios_bp.route("/", methods=["GET"])
def get_usuarios():
    try:
        print("GET ALL USUARIOS")
        resultado = usuarios.find()
    except Exception as e:
        return jsonify({"error": "Error al consultar la base de datos"}), 404
    
    try:
        resultado = json.loads(json_util.dumps(resultado))
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({"error": "Error al procesar la respuesta"}), 400
    
# GET /usuarios/<email>
@usuarios_bp.route("/<email>", methods=["GET"])
def get_usuario(email):
    try:
        usuario = usuarios.find_one({"email": email})
        if usuario:
            return jsonify(json.loads(json_util.dumps(usuario))), 200
        else:
            return jsonify({"error": "Usuario no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": f"Error al buscar el usuario: {str(e)}"}), 400
    
# POST /usuarios
@usuarios_bp.route("/", methods=["POST"])
def post_usuario():
    try:
        datos = request.json

        if "email" not in datos:
            return jsonify({"error": "Falta el campo 'email'"}), 400
        if "nombre" not in datos:
            return jsonify({"error": "Falta el campo 'nombre'"}), 400
            
        usuarios.insert_one(datos)
        return jsonify({"mensaje": "Usuario creado"}), 200
    except Exception as e:
        return jsonify({"error": f"Error al crear el usuario: {str(e)}"}), 400
    
# PUT /usuarios/<email>
@usuarios_bp.route("/<email>", methods=["PUT"])
def update_usuario(email):
    try:
        datos = request.json
        if not datos:
            return jsonify({"error": "No se han enviado datos"}), 400
        
        filtro = {"email": email}
        usuario_existente = usuarios.find_one(filtro)
        if not usuario_existente:
            return jsonify({"error": "Usuario no encontrado"}), 404

        usuarios.update_one(filtro, {"$set": datos})
        return jsonify({"mensaje": f"Usuario con email {email} actualizado"}), 200
    except Exception as e:
        return jsonify({"error": f"Error al actualizar el usuario: {str(e)}"}), 400
    
# DELETE /usuarios/<email>
@usuarios_bp.route("/<email>", methods=["DELETE"])
def delete_usuario(email):
    try:
        filtro = {"email": email}
        usuario = usuarios.find_one(filtro)
        if usuario:
            usuarios.delete_one(filtro)
            return jsonify({"mensaje": f"Usuario con email {email} eliminado"}), 200
        else:
            return jsonify({"error": "Usuario no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": f"Error al eliminar el usuario: {str(e)}"}), 400
    
#CRUD de contactos
# GET /usuarios/<email>/contactos
@usuarios_bp.route("/<email>/contactos", methods=["GET"])
def get_contactos(email):
    usuario = usuarios.find_one({"email": email})
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404

    try:
        contacto = contactos.find({"email": email})
    except Exception as e:
        return jsonify({"error": "Error al consultar la base de datos"}), 404
    
    try:
        contacto_json = json.loads(json_util.dumps(contacto))
        return jsonify(contacto_json), 200
    except Exception as e:
        return jsonify({"error": "Error al procesar la respuesta"}), 400
    
#POST /usuarios/<email>/contactos
@usuarios_bp.route("/<email>/contactos", methods=["POST"])
def post_contacto(email):
    try:
        usuario = usuarios.find_one({"email": email})
        if not usuario:
            return jsonify({"error": "Usuario no encontrado"}), 404
        
        datos = request.json
        datos["email_usuario"] = email

        if "email" not in datos:
            return jsonify({"error": "Falta el campo 'email'"}), 400
            
        contactos.insert_one(datos)
        return jsonify({"mensaje": "Contacto creado"}), 200
    except Exception as e:
        return jsonify({"error": f"Error al crear el contacto: {str(e)}"}), 400
    
#DELETE /usuarios/<email>/contactos/<email_contacto>
@usuarios_bp.route("/<email>/contactos/<email_contacto>", methods=["DELETE"])
def delete_contacto(email, email_contacto):
    usuario = usuarios.find_one({"email": email})
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404
    try:
        filtro = {"email_usuario": email, "email": email_contacto}
        contacto = contactos.find_one(filtro)
        if contacto:
            contactos.delete_one(filtro)
            return jsonify({"mensaje": f"Contacto con email {email_contacto} eliminado"}), 200
        else:
            return jsonify({"error": "Contacto no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": f"Error al eliminar el contacto: {str(e)}"}), 400

#CRUD de eventos
# GET /eventos
@eventos_bp.route("/", methods=["GET"])
def get_eventos():
    try:
        print("GET ALL EVENTOS")
        resultado = eventos.find()
    except Exception as e:
        return jsonify({"error": "Error al consultar la base de datos"}), 404
    
    try:
        resultado = json.loads(json_util.dumps(resultado))
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({"error": "Error al procesar la respuesta"}), 400
    
# GET /eventos/<id>
@eventos_bp.route("/<id>", methods=["GET"])
def get_evento(id):
    try:
        evento = eventos.find_one({"_id": ObjectId(id)})
        if evento:
            return jsonify(json.loads(json_util.dumps(evento))), 200
        else:
            return jsonify({"error": "Evento no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": f"Error al buscar el evento: {str(e)}"}), 400
    
# POST /eventos
@eventos_bp.route("/", methods=["POST"])
def post_evento():
    try:
        datos = request.json

        if "anfitrion" not in datos:
            return jsonify({"error": "Falta el campo 'anfitrion'"}), 400
        if "descripcion" not in datos:
            return jsonify({"error": "Falta el campo 'descripcion'"}), 400
        if "inicio" not in datos:
            return jsonify({"error": "Falta el campo 'inicio'"}), 400
        if "duracion" not in datos:
            return jsonify({"error": "Falta el campo 'duracion'"}), 400
        if "invitados" not in datos:
            return jsonify({"error": "Falta el campo 'invitados'"}), 400
        
        for invitado in datos["invitados"]:
            if "email" not in invitado:
                return jsonify({"error": "Falta el campo 'email' en uno de los invitados"}), 400
            if "estado" not in invitado:
                return jsonify({"error": "Falta el campo 'estado' en uno de los invitados"}), 400
            
        inicioDateTime = datetime.strptime(datos["inicio"], "%Y-%m-%dT%H:%M:%SZ")
        if inicioDateTime.minute % 15 != 0:
            return jsonify({"error": "El inicio del evento debe ser un multiplo de 15 minutos"}), 400
            
        eventos.insert_one(datos)
        return jsonify({"mensaje": "Evento creado"}), 200
    except Exception as e:
        return jsonify({"error": f"Error al crear el evento: {str(e)}"}), 400
    
# PUT /eventos/<id>
@eventos_bp.route("/<id>", methods=["PUT"])
def update_evento(id):
    try:
        datos = request.json
        if not datos:
            return jsonify({"error": "No se han enviado datos"}), 400
        
        filtro = {"_id": ObjectId(id)}
        evento_existente = eventos.find_one(filtro)
        if not evento_existente:
            return jsonify({"error": "Evento no encontrado"}), 404

        if "anfitrion" in datos:
            #Comprobamos que el anfitrion sea un usuario
            usuario = usuarios.find_one({"email": datos["anfitrion"]})
            if not usuario:
                return jsonify({"error": "El anfitrion no es un usuario"}), 400
            
        if datos.get("inicio"):
            inicioDateTime = datetime.strptime(datos["inicio"], "%Y-%m-%dT%H:%M:%SZ")
            if inicioDateTime.minute % 15 != 0:
                return jsonify({"error": "El inicio del evento debe ser un multiplo de 15 minutos"}), 400
            
        if datos.get("invitados"):
            for invitado in datos["invitados"]:
                if "email" not in invitado:
                    return jsonify({"error": "Falta el campo 'email' en uno de los invitados"}), 400
                if "estado" not in invitado:
                    return jsonify({"error": "Falta el campo 'estado' en uno de los invitados"}), 400
                
        eventos.update_one(filtro, {"$set": datos})
        return jsonify({"mensaje": f"Evento con id {id} actualizado"}), 200
    except Exception as e:
        return jsonify({"error": f"Error al actualizar el evento: {str(e)}"}), 400
    
# DELETE /eventos/<id>
@eventos_bp.route("/<id>", methods=["DELETE"])
def delete_evento(id):
    try:
        filtro = {"_id": ObjectId(id)}
        evento = eventos.find_one(filtro)
        if evento:
            eventos.delete_one(filtro)
            return jsonify({"mensaje": f"Evento con id {id} eliminado"}), 200
        else:
            return jsonify({"error": "Evento no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": f"Error al eliminar el evento: {str(e)}"}), 400

#Funciones adicionales
# GET /usuarios/<email>/contactos/buscar/<cadena>
@usuarios_bp.route("/<email>/contactos/buscar/<cadena>", methods=["GET"])
def buscar_contactos(email, cadena):
    usuario = usuarios.find_one({"email": email})
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404

    try:
        filtro = {"email_usuario": email, "email": {"$regex": cadena, "$options": "i"}}
        contactos_encontrados = contactos.find(filtro, {"email": 1, "email_usuario": 1, "_id": 0}) 
        contactos_lista = list(contactos_encontrados)
        return jsonify(contactos_lista), 200
    except Exception as e:
        return jsonify({"error": f"Error al buscar contactos: {str(e)}"}), 400
    
# POST /eventos/<id>/invitar/<email_usuario>/<email_contacto>
@eventos_bp.route("/<id>/invitar/<email_usuario>/<email_contacto>", methods=["POST"])
def invitar_contacto(id, email_usuario, email_contacto):
    try:
        # Verificar si el usuario existe
        usuario = usuarios.find_one({"email": email_usuario})
        if not usuario:
            return jsonify({"error": "Usuario no encontrado"}), 404

        # Verificar si el contacto existe
        contacto = contactos.find_one({"email_usuario": email_usuario, "email": email_contacto})
        if not contacto:
            return jsonify({"error": "Contacto no encontrado"}), 404

        # Verificar si el evento existe
        evento = eventos.find_one({"_id": ObjectId(id)})
        if not evento:
            return jsonify({"error": "Evento no encontrado"}), 404

        # Agregar el contacto a la lista de invitados del evento
        invitado = {"email": email_contacto, "estado": "pendiente"}
        eventos.update_one(
            {"_id": ObjectId(id)},
            {"$addToSet": {"invitados": invitado}}
        )

        return jsonify({"mensaje": f"Contacto {email_contacto} invitado al evento {id}"}), 200
    except Exception as e:
        return jsonify({"error": f"Error al invitar al contacto: {str(e)}"}), 400
    
# PUT /eventos/<id>/aceptar/<email_contacto>
@eventos_bp.route("/<id>/aceptar/<email_contacto>", methods=["PUT"])
def aceptar_invitacion(id, email_contacto):
    try:
        # Verificar si el evento existe
        evento = eventos.find_one({"_id": ObjectId(id)})
        if not evento:
            return jsonify({"error": "Evento no encontrado"}), 404

        # Verificar si el contacto está invitado al evento
        invitado = next((invitado for invitado in evento.get("invitados", []) if invitado["email"] == email_contacto), None)
        if not invitado:
            return jsonify({"error": "Invitación no encontrada"}), 404

        # Actualizar el estado de la invitación a "aceptada"
        eventos.update_one(
            {"_id": ObjectId(id), "invitados.email": email_contacto},
            {"$set": {"invitados.$.estado": "aceptada"}}
        )

        return jsonify({"mensaje": f"Invitación aceptada para el contacto {email_contacto} en el evento {id}"}), 200
    except Exception as e:
        return jsonify({"error": f"Error al aceptar la invitación: {str(e)}"}), 400

# POST /eventos/<id>/reprogramar
@eventos_bp.route("/<id>/reprogramar", methods=["POST"])
def reprogramar_evento(id):
    try:
        datos = request.json
        if "desplazamiento" not in datos or "unidad" not in datos:
            return jsonify({"error": "Faltan los campos 'desplazamiento' y 'unidad'"}), 400

        desplazamiento = datos["desplazamiento"]
        unidad = datos["unidad"]

        # Verificar si el evento existe
        evento = eventos.find_one({"_id": ObjectId(id)})
        if not evento:
            return jsonify({"error": "Evento no encontrado"}), 404

        # Calcular la nueva fecha
        inicioDateTime = datetime.strptime(evento["inicio"], "%Y-%m-%dT%H:%M:%SZ")
        if unidad == "dias":
            nueva_fecha = inicioDateTime + timedelta(days=desplazamiento)
        elif unidad == "semanas":
            nueva_fecha = inicioDateTime + timedelta(weeks=desplazamiento)
        elif unidad == "meses":
            nueva_fecha = inicioDateTime + timedelta(months=desplazamiento)
        elif unidad == "años":
            nueva_fecha = inicioDateTime + timedelta(years=desplazamiento)
        else:
            return jsonify({"error": "Unidad de tiempo no válida"}), 400

        # Crear el nuevo evento con la nueva fecha y el resto de valores iguales
        nuevo_evento = evento.copy()
        nuevo_evento["inicio"] = nueva_fecha.strftime("%Y-%m-%dT%H:%M:%SZ")
        del nuevo_evento["_id"]  # Eliminar el _id para que MongoDB genere uno nuevo

        eventos.insert_one(nuevo_evento)
        return jsonify({"mensaje": "Evento reprogramado", "nuevo_evento": json.loads(json_util.dumps(nuevo_evento))}), 200
    except Exception as e:
        return jsonify({"error": f"Error al reprogramar el evento: {str(e)}"}), 400
    
# GET /usuarios/<email>/agenda
@usuarios_bp.route("/<email>/agenda", methods=["GET"])
def obtener_agenda(email):
    try:
        # Buscar eventos donde el usuario es el anfitrión
        eventos_propios = list(eventos.find({"anfitrion": email}).sort("inicio", pymongo.ASCENDING))

        # Buscar eventos donde el usuario es un invitado
        eventos_invitado = list(eventos.find({"invitados.email": email}).sort("inicio", pymongo.ASCENDING))

        # Combinar y ordenar los eventos por fecha de inicio
        agenda = sorted(eventos_propios + eventos_invitado, key=lambda evento: evento["inicio"])

        return jsonify(json.loads(json_util.dumps(agenda))), 200
    except Exception as e:
        return jsonify({"error": f"Error al obtener la agenda: {str(e)}"}), 400