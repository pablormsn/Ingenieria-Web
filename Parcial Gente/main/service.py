import json
import os

import pymongo
import requests
from bson import json_util
from bson.objectid import ObjectId
from dotenv import load_dotenv
from flask import Blueprint, jsonify, request

load_dotenv()
MONGO_URL = os.getenv("MONGO_URL")

tareas_bp = Blueprint("tareas_bp", __name__)
colaboradores_bp = Blueprint("colaboradores_bp", __name__)

#CONEXION A LA BASE DE DATOS
client = pymongo.MongoClient(MONGO_URL)
db = client.Gente
tareas = db.tareas
colaboradores = db.colaboradores

#CRUD de tareas
#GET /tareas (Get all)
@tareas_bp.route("/", methods=["GET"])
def get_tareas():
    try:
        resultado = tareas.find()
    except Exception as e:
        return jsonify({"error": "Error al consultar la base de datos"}), 404
    
    try:
        resultado = json.loads(json_util.dumps(resultado))
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({"error": "Error al procesar la información"}), 400
    
#GET /tareas/<id> (Get one)
@tareas_bp.route("/<id>", methods=["GET"])
def get_tarea(id):
    try:
        tarea = tareas.find_one({"_id": ObjectId(id)})
        if tarea:
            return jsonify(json.loads(json_util.dumps(tarea))), 200
        else:
            return jsonify({"error": "Tarea no encontrada"}), 404
    except Exception as e:
        return jsonify({"error": f"Error al buscar la tarea: {str(e)}"}), 400
    
#POST /tareas
@tareas_bp.route("/", methods=["POST"])
def create_tarea():
    try:
        datos = request.json

        if "responsable" not in datos:
            return jsonify({"error": "Falta el responsable"}), 400
        if "descripcion" not in datos:
            return jsonify({"error": "Falta la descripción"}), 400
        if "segmentos" not in datos:
            return jsonify({"error": "Falta la duración estimada de la tarea"}), 400
        if "habilidades" not in datos:
            return jsonify({"error": "Faltan las habilidades necesarias"}), 400
        
        tareas.insert_one(datos)
        return jsonify({"mensaje": "Tarea creada"}), 201
    except Exception as e:
        return jsonify({"error": f"Error al crear la tarea: {str(e)}"}), 400
    
#PUT /tareas/<id>
@tareas_bp.route("/<id>", methods=["PUT"])
def update_tarea(id):
    try:
        datos = request.json
        if not datos:
            return jsonify({"error": "No se enviaron datos"}), 400
        
        filtro = {"_id": ObjectId(id)}
        tarea_existente = tareas.find_one(filtro)
        if not tarea_existente:
            return jsonify({"error": "Tarea no encontrada"}), 404
        
        tareas.update_one(filtro, {"$set": datos})
        return jsonify({"mensaje": "Tarea actualizada"}), 200
    except Exception as e:
        return jsonify({"error": f"Error al actualizar la tarea: {str(e)}"}), 400
    
#DELETE /tareas/<id>
@tareas_bp.route("/<id>", methods=["DELETE"])
def delete_tarea(id):
    try:
        filtro = {"_id": ObjectId(id)}
        tarea_existente = tareas.find_one(filtro)
        if tarea_existente:
            tareas.delete_one(filtro)
            return jsonify({"mensaje": "Tarea eliminada"}), 200
        else:
            return jsonify({"error": "Tarea no encontrada"}), 404
    except Exception as e:
        return jsonify({"error": f"Error al eliminar la tarea: {str(e)}"}), 400
    
#CRUD de colaboradores
#GET /colaboradores (Get all)
@colaboradores_bp.route("/", methods=["GET"])
def get_colaboradores():
    try:
        resultado = colaboradores.find()
    except Exception as e:
        return jsonify({"error": "Error al consultar la base de datos"}), 404
    
    try:
        resultado = json.loads(json_util.dumps(resultado))
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({"error": "Error al procesar la información"}), 400
    
#GET /colaboradores/<id> (Get one)
@colaboradores_bp.route("/<id>", methods=["GET"])
def get_colaborador(id):
    try:
        colaborador = colaboradores.find_one({"_id": ObjectId(id)})
        if colaborador:
            return jsonify(json.loads(json_util.dumps(colaborador))), 200
        else:
            return jsonify({"error": "Colaborador no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": f"Error al buscar el colaborador: {str(e)}"}), 400
    
#POST /colaboradores
@colaboradores_bp.route("/", methods=["POST"])
def create_colaborador():
    try:
        datos = request.json

        if "email" not in datos:
            return jsonify({"error": "Falta el email"}), 400
        if "nombre" not in datos:
            return jsonify({"error": "Falta el nombre"}), 400
        if "habilidades" not in datos:
            return jsonify({"error": "Faltan las habilidades"}), 400
        
        colaboradores.insert_one(datos)
        return jsonify({"mensaje": "Colaborador creado"}), 201
    except Exception as e:
        return jsonify({"error": f"Error al crear el colaborador: {str(e)}"}), 400
    
#DELETE /colaboradores/<id>
@colaboradores_bp.route("/<id>", methods=["DELETE"])
def delete_colaborador(id):
    try:
        filtro = {"_id": ObjectId(id)}
        colaborador_existente = colaboradores.find_one(filtro)
        if colaborador_existente:
            colaboradores.delete_one(filtro)
            return jsonify({"mensaje": "Colaborador eliminado"}), 200
        else:
            return jsonify({"error": "Colaborador no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": f"Error al eliminar el colaborador: {str(e)}"}), 400
    
#GET /colaboradores/<id>/habilidades
@colaboradores_bp.route("/<id>/habilidades", methods=["GET"])
def get_habilidades(id):
    try:
        filtro = {"_id": ObjectId(id)}
        colaborador = colaboradores.find_one(filtro, {"habilidades": 1, "_id": 0})
        if colaborador:
            return jsonify({"habilidades": colaborador.get("habilidades", [])}), 200
        else:
            return jsonify({"error": "Colaborador no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": f"Error al obtener las habilidades: {str(e)}"}), 400
    
# POST /colaboradores/<id>/habilidades
@colaboradores_bp.route("/<id>/habilidades", methods=["POST"])
def add_habilidad(id):
    try:
        nueva_habilidad = request.json.get("habilidad")
        if not nueva_habilidad:
            return jsonify({"error": "No se proporcionó ninguna habilidad"}), 400

        filtro = {"_id": ObjectId(id)}
        colaborador = colaboradores.find_one(filtro)
        if colaborador:
            colaboradores.update_one(filtro, {"$push": {"habilidades": nueva_habilidad}})
            return jsonify({"mensaje": "Habilidad añadida"}), 200
        else:
            return jsonify({"error": "Colaborador no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": f"Error al añadir la habilidad: {str(e)}"}), 400
    
# DELETE /colaboradores/<id>/habilidades
@colaboradores_bp.route("/<id>/habilidades", methods=["DELETE"])
def delete_habilidad(id):
    try:
        habilidad_a_eliminar = request.json.get("habilidad")
        if not habilidad_a_eliminar:
            return jsonify({"error": "No se proporcionó ninguna habilidad"}), 400

        filtro = {"_id": ObjectId(id)}
        colaborador = colaboradores.find_one(filtro)
        if colaborador:
            if habilidad_a_eliminar in colaborador.get("habilidades", []):
                colaboradores.update_one(filtro, {"$pull": {"habilidades": habilidad_a_eliminar}})
                return jsonify({"mensaje": "Habilidad eliminada"}), 200
            else:
                return jsonify({"error": "Habilidad no encontrada en el colaborador"}), 404
        else:
            return jsonify({"error": "Colaborador no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": f"Error al eliminar la habilidad: {str(e)}"}), 400
    
#FUNCIONES ADICIONALES
# GET /tareas/habilidad/<habilidad>
@tareas_bp.route("/habilidad/<habilidad>", methods=["GET"])
def get_tareas_por_habilidad(habilidad):
    try:
        habilidad = habilidad.replace("_", " ")
        filtro = {"habilidades": {"$in": [habilidad]}}
        tareas_encontradas = tareas.find(filtro, {"_id": 0})
        tareas_lista = list(tareas_encontradas)
        if tareas_lista:
            return jsonify({"tareas": tareas_lista}), 200
        else:
            return jsonify({"mensaje": "No se encontraron tareas con la habilidad especificada"}), 404
    except Exception as e:
        return jsonify({"error": f"Error al obtener las tareas: {str(e)}"}), 400
    
# POST /tareas/<tarea_id>/asignar/<colaborador_id>
@tareas_bp.route("/<tarea_id>/asignar/<colaborador_id>", methods=["POST"])
def asignar_colaborador_a_tarea(tarea_id, colaborador_id):
    try:
        # Buscar la tarea por su ID
        tarea = tareas.find_one({"_id": ObjectId(tarea_id)})
        if not tarea:
            return jsonify({"error": "Tarea no encontrada"}), 404

        # Buscar el colaborador por su ID
        colaborador = colaboradores.find_one({"_id": ObjectId(colaborador_id)})
        if not colaborador:
            return jsonify({"error": "Colaborador no encontrado"}), 404

        # Obtener las habilidades requeridas por la tarea
        habilidades_requeridas = tarea.get("habilidades", [])
        # Obtener las habilidades del colaborador
        habilidades_colaborador = colaborador.get("habilidades", [])

        # Comprobar si el colaborador posee al menos una de las habilidades requeridas
        if not any(habilidad in habilidades_colaborador for habilidad in habilidades_requeridas):
            return jsonify({"error": "El colaborador no posee ninguna de las habilidades requeridas"}), 400

        # Asignar el colaborador a la tarea
        tareas.update_one(
            {"_id": ObjectId(tarea_id)},
            {"$addToSet": {"colaboradores": ObjectId(colaborador_id)}}
        )
        return jsonify({"mensaje": "Colaborador asignado a la tarea"}), 200

    except Exception as e:
        return jsonify({"error": f"Error al asignar el colaborador a la tarea: {str(e)}"}), 400
    
# GET /tareas/<tarea_id>/candidatos
@tareas_bp.route("/<tarea_id>/candidatos", methods=["GET"])
def get_candidatos_para_tarea(tarea_id):
    try:
        # Buscar la tarea por su ID
        tarea = tareas.find_one({"_id": ObjectId(tarea_id)})
        if not tarea:
            return jsonify({"error": "Tarea no encontrada"}), 404

        # Obtener las habilidades requeridas por la tarea
        habilidades_requeridas = tarea.get("habilidades", [])
        if not habilidades_requeridas:
            return jsonify({"error": "La tarea no tiene habilidades requeridas"}), 400

        # Buscar colaboradores que posean al menos una de las habilidades requeridas
        filtro = {"habilidades": {"$in": habilidades_requeridas}}
        colaboradores_encontrados = colaboradores.find(filtro, {"email": 1, "_id": 0})
        emails_colaboradores = [colaborador["email"] for colaborador in colaboradores_encontrados]

        if emails_colaboradores:
            return jsonify({"emails": emails_colaboradores}), 200
        else:
            return jsonify({"mensaje": "No se encontraron colaboradores con las habilidades requeridas"}), 404

    except Exception as e:
        return jsonify({"error": f"Error al buscar candidatos para la tarea: {str(e)}"}), 400
    
# GET /tareas/completamente_asignadas
@tareas_bp.route("/completamente_asignadas", methods=["GET"])
def get_tareas_completamente_asignadas():
    try:
        # Buscar tareas que tengan asignados tantos colaboradores como segmentos
        filtro = {
            "$expr": {
                "$eq": [{"$size": {"$ifNull": ["$colaboradores", []]}}, "$segmentos"]
            }
        }
        tareas_encontradas = tareas.find(filtro, {"_id": 0, "nombre": 1, "colaboradores": 1, "segmentos": 1})
        tareas_lista = list(tareas_encontradas)

        if tareas_lista:
            return jsonify({"tareas": tareas_lista}), 200
        else:
            return jsonify({"mensaje": "No se encontraron tareas completamente asignadas"}), 404

    except Exception as e:
        return jsonify({"error": f"Error al obtener las tareas completamente asignadas: {str(e)}"}), 400
    
# # GET /tareas/<usuario_id>/colaboradores
# @tareas_bp.route("<usuario_id>/colaboradores", methods=["GET"])
# def get_colaboradores_de_usuario(usuario_id):
#     try:
#         # Buscar tareas de las que el usuario es responsable
#         tareas_usuario = tareas.find({"responsable_id": ObjectId(usuario_id)}, {"colaboradores": 1, "_id": 0})
#         colaboradores_ids = set()
        
#         # Recopilar todos los IDs de colaboradores de las tareas del usuario
#         for tarea in tareas_usuario:
#             colaboradores_ids.update(tarea.get("colaboradores", []))
        
#         # Buscar los correos electrónicos de los colaboradores
#         colaboradores_encontrados = colaboradores.find({"_id": {"$in": list(colaboradores_ids)}}, {"email": 1, "_id": 0})
#         emails_colaboradores = [colaborador["email"] for colaborador in colaboradores_encontrados]

#         if emails_colaboradores:
#             return jsonify({"emails": emails_colaboradores}), 200
#         else:
#             return jsonify({"mensaje": "No se encontraron colaboradores para las tareas del usuario"}), 404

#     except Exception as e:
#         return jsonify({"error": f"Error al buscar colaboradores para el usuario: {str(e)}"}), 400
    

