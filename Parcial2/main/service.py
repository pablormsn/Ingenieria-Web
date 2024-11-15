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

usuarios_bp = Blueprint("usuarios", __name__)

#CONEXION A LA BASE DE DATOS
client = pymongo.MongoClient(MONGO_URL)
db = client.exam
usuarios = db.usuarios