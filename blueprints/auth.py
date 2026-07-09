from flask import Blueprint, render_template, request, redirect, url_for, session
from models.usuario_model import validar_usuario


auth = Blueprint("auth", __name__)


# ==========================================
# LOGIN
# ==========================================

@auth.route("/", methods=["GET", "POST"])
def login():

    mensaje = None

    if request.method == "POST":

        usuario = request.form["usuario"]
        password = request.form["password"]

        usuario_validado = validar_usuario(usuario, password)

        if usuario_validado:

            session["usuario"] = usuario_validado["usuario"]
            session["rol"] = usuario_validado["rol"]

            return redirect("/dashboard")

        else:

            mensaje = "Usuario o contraseña incorrectos"


    return render_template(
        "login.html",
        mensaje=mensaje
    )


# ==========================================
# CERRAR SESIÓN
# ==========================================

@auth.route("/logout")
def logout():

    session.clear()

    return redirect("/")