from flask import Blueprint, render_template, request, redirect, session

from models.usuario_model import validar_usuario
from models.auditoria_model import registrar_auditoria


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


        usuario_validado = validar_usuario(
            usuario,
            password
        )



        if usuario_validado:


            session["usuario"] = usuario_validado["usuario"]

            session["nombre"] = usuario_validado["nombre"]

            session["rol"] = usuario_validado["rol"]

            session["foto"] = usuario_validado["foto"]



            registrar_auditoria(
                session["usuario"],
                "Login",
                "Inicio de sesión"
            )



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


    registrar_auditoria(
        session.get("usuario"),
        "Login",
        "Cierre de sesión"
    )


    session.clear()


    return redirect("/")