from flask import Flask, render_template, request, redirect, jsonify, abort
from flask_login import LoginManager, login_required
from werkzeug.exceptions import HTTPException
from logging.handlers import RotatingFileHandler
import logging
from models import db, User
from auth import auth
import controllers
from api.routes import api

app = Flask(__name__)
app.config["SECRET_KEY"] = "jijijaja"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:root@localhost/juegos"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = "auth.login"
login_manager.session_protection = "strong"

app.register_blueprint(auth, url_prefix="/auth")
app.register_blueprint(api, url_prefix="/api")

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

@app.route("/")
@app.route("/juegos")
@login_required
def juegos():
    juegos = controllers.obtener_juegos()
    return render_template("juegos.html", juegos=juegos)

@app.route("/agregar_juego")
@login_required
def formulario_agregar_juego():
    return render_template("agregar_juego.html")

@app.route("/guardar_juego", methods=["POST"])
@login_required
def guardar_juego():
    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    precio = request.form["precio"]
    controllers.insertar_juego(nombre, descripcion, precio)
    return redirect("/juegos")

@app.route("/eliminar_juego", methods=["POST"])
@login_required
def eliminar_juego():
    controllers.eliminar_juego(int(request.form["id"]))
    return redirect("/juegos")

@app.route("/formulario_editar_juego/<int:id>")
@login_required
def editar_juego(id):
    juego = controllers.obtener_juego_por_id(id)
    return render_template("editar_juego.html", juego=juego)

@app.route("/actualizar_juego", methods=["POST"])
@login_required
def actualizar_juego():
    id = int(request.form["id"])
    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    precio = request.form["precio"]
    controllers.actualizar_juego(nombre, descripcion, precio, id)
    return redirect("/juegos")

def respuesta_error_api(e):
    response = e.get_response()
    response.data = app.json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description
    })
    response.content_type = "application/json"
    return response

@app.errorhandler(400)
def bad_request(e):
    if request.path.startswith("/api/"):
        return respuesta_error_api(e)
    return render_template("400.html"), 400

@app.errorhandler(404)
def not_found(e):
    if request.path.startswith("/api/"):
        return respuesta_error_api(e)
    return render_template("404.html"), 404

@app.errorhandler(405)
def method_not_allowed(e):
    if request.path.startswith("/api/"):
        return respuesta_error_api(e)
    return render_template("405.html"), 405

@app.errorhandler(500)
def internal_error(e):
    return render_template("500.html"), 500

@app.errorhandler(HTTPException)
def handle_http_exception(e):
    if request.path.startswith("/api/"):
        return respuesta_error_api(e)
    return e

handler = RotatingFileHandler(
    "errors.log",
    maxBytes=1000000,
    backupCount=3
)
handler.setLevel(logging.ERROR)
app.logger.addHandler(handler)

@app.route("/videogame/<int:id>")
@login_required
def consultar_videojuego(id):
    if not request.args.get("nombre"):
        abort(400)
    return redirect("/juegos")

@app.route("/probar_error_500")
@login_required
def probar_error_500():
    return str(1 / 0)

if __name__ == "__main__":
    app.run(port=8000, debug=False)


