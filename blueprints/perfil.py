from flask import Blueprint, render_template, session, redirect, request
from utils.helpers import login_required
from models.usuario_model import buscar_usuario, actualizar_foto
from models.usuario_model import cambiar_password

import os
from werkzeug.utils import secure_filename


perfil = Blueprint("perfil", __name__)


CARPETA_FOTOS = "static/perfiles"


# ==========================================
# VER PERFIL
# ==========================================

@perfil.route("/perfil")
@login_required
def ver_perfil():

    usuario = buscar_usuario(session["usuario"])

    return render_template(
        "perfil.html",
        usuario=usuario
    )



# ==========================================
# CAMBIAR FOTO
# ==========================================

@perfil.route("/perfil/foto", methods=["POST"])
@login_required
def cambiar_foto():


    archivo = request.files["foto"]


    if archivo:


        nombre = secure_filename(archivo.filename)


        ruta = os.path.join(
            CARPETA_FOTOS,
            nombre
        )


        archivo.save(ruta)



        actualizar_foto(
            session["usuario"],
            nombre
        )


        session["foto"] = nombre



    return redirect("/perfil")

# ==========================================
# CAMBIAR PASSWORD
# ==========================================

@perfil.route("/cambiar_password", methods=["GET","POST"])
@login_required
def password():


    mensaje = None


    if request.method == "POST":


        actual = request.form["actual"]

        nueva = request.form["nueva"]

        confirmar = request.form["confirmar"]



        if nueva != confirmar:

            mensaje = "Las contraseñas no coinciden"



        else:


            resultado = cambiar_password(
                session["usuario"],
                actual,
                nueva
            )


            if resultado:

                mensaje = "Contraseña actualizada correctamente"

            else:

                mensaje = "La contraseña actual no es correcta"



    return render_template(
        "cambiar_password.html",
        mensaje=mensaje
    )