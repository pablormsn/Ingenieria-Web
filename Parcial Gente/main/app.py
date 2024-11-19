import os

from dotenv import load_dotenv
from flask import Flask
from service import tareas_bp, colaboradores_bp

load_dotenv()

app = Flask(__name__)

#Registramos el blueprint de usuarios
app.register_blueprint(tareas_bp, url_prefix="/tareas")
app.register_blueprint(colaboradores_bp, url_prefix="/colaboradores")

@app.route('/')
def main_route():
    return f"<a href='http://localhost:{os.getenv('SERVICE_PORT')}/tareas'>Tareas</a> <a href='http://localhost:{os.getenv('SERVICE_PORT')}/colaboradores'>Colaboradores</a>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.getenv("SERVICE_USERS_PORT"), debug=True)