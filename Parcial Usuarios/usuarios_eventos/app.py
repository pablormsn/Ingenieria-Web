import os

from dotenv import load_dotenv
from flask import Flask
from service import eventos_bp
from service import usuarios_bp

load_dotenv()

app = Flask(__name__)

# Registrar los microservicios como Blueprints
app.register_blueprint(eventos_bp, url_prefix="/eventos")
app.register_blueprint(usuarios_bp, url_prefix="/usuarios")

@app.route("/")
def main_route():
    return f"<a href='http://localhost:{os.getenv('SERVICE_USERS_PORT')}/usuarios'>CLICK AQUI PARA IR AL APARTADO DE LOS USUARIOS</a>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.getenv("SERVICE_USERS_PORT"), debug=True)