"""
main.py
Punto de entrada de la aplicación. Define las rutas (endpoints) y
los verbos HTTP que atiende cada una. No contiene lógica de negocio
ni de base de datos: eso vive en backend/services.py y backend/repositories.py.
"""
from flask import Flask, render_template, request, jsonify, session, redirect

from backend.services import AuthService, TareaService

app = Flask(__name__)
app.secret_key = "cambia-esta-clave-en-produccion"

auth_service = AuthService()
tarea_service = TareaService()


# ---------- Páginas (front) ----------

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login")
def pagina_login():
    return render_template("login.html")


@app.route("/registro")
def pagina_registro():
    return render_template("registro.html")


@app.route("/dashboard")
def pagina_dashboard():
    if "usuario_id" not in session:
        return redirect("/login")
    return render_template("dashboard.html")


# ---------- API: autenticación ----------

@app.route("/api/registro", methods=["POST"])
def api_registro():
    datos = request.get_json(force=True)
    try:
        usuario = auth_service.registrar(
            datos.get("nombre", "").strip(),
            datos.get("email", "").strip().lower(),
            datos.get("password", ""),
        )
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    return jsonify({"id": usuario.id, "nombre": usuario.nombre}), 201


@app.route("/api/login", methods=["POST"])
def api_login():
    datos = request.get_json(force=True)
    try:
        usuario = auth_service.iniciar_sesion(
            datos.get("email", "").strip().lower(),
            datos.get("password", ""),
        )
    except ValueError as e:
        return jsonify({"error": str(e)}), 401
    session["usuario_id"] = usuario.id
    session["usuario_nombre"] = usuario.nombre
    return jsonify({"id": usuario.id, "nombre": usuario.nombre})


@app.route("/api/logout", methods=["POST"])
def api_logout():
    session.clear()
    return jsonify({"ok": True})


@app.route("/api/sesion")
def api_sesion():
    if "usuario_id" not in session:
        return jsonify({"error": "No autenticado"}), 401
    return jsonify({"id": session["usuario_id"], "nombre": session["usuario_nombre"]})


# ---------- API: tareas ----------

def _requerir_sesion():
    if "usuario_id" not in session:
        return None
    return session["usuario_id"]


@app.route("/api/tareas", methods=["GET"])
def api_listar_tareas():
    usuario_id = _requerir_sesion()
    if not usuario_id:
        return jsonify({"error": "No autenticado"}), 401
    tareas = tarea_service.listar_tareas(usuario_id)
    return jsonify([
        {"id": t.id, "titulo": t.titulo, "materia": t.materia, "fecha": t.fecha}
        for t in tareas
    ])


@app.route("/api/tareas", methods=["POST"])
def api_crear_tarea():
    usuario_id = _requerir_sesion()
    if not usuario_id:
        return jsonify({"error": "No autenticado"}), 401
    datos = request.get_json(force=True)
    try:
        tarea = tarea_service.crear_tarea(
            usuario_id,
            datos.get("titulo", "").strip(),
            datos.get("materia", "").strip(),
            datos.get("fecha", "").strip(),
        )
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    return jsonify({"id": tarea.id}), 201


@app.route("/api/tareas/<int:tarea_id>", methods=["DELETE"])
def api_eliminar_tarea(tarea_id):
    usuario_id = _requerir_sesion()
    if not usuario_id:
        return jsonify({"error": "No autenticado"}), 401
    tarea_service.eliminar_tarea(tarea_id, usuario_id)
    return jsonify({"ok": True})


if __name__ == "__main__":
    app.run(debug=True)
