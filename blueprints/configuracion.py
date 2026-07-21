from flask import Blueprint, render_template, request, redirect, flash

from utils.helpers import login_required, role_required

from models.configuracion_model import (
    obtener_empresa,
    actualizar_empresa
)


configuracion = Blueprint("configuracion", __name__)


# ==========================================
# MOSTRAR CONFIGURACIÓN
# ==========================================

@configuracion.route("/configuracion")
@login_required
@role_required("Administrador")
def inicio():

    empresa = obtener_empresa()


    return render_template(
        "configuracion.html",
        empresa=empresa
    )



# ==========================================
# GUARDAR CONFIGURACIÓN
# ==========================================

@configuracion.route(
    "/configuracion/guardar",
    methods=["POST"]
)
@login_required
@role_required("Administrador")
def guardar():

    actualizar_empresa(

        request.form["nombre"],

        request.form["rut"],

        request.form["giro"],

        request.form["direccion"],

        request.form["comuna"],

        request.form["telefono"],

        request.form["email"],

        request.form["logo"],

        request.form["moneda"],

        request.form["iva"]

    )


    flash(
        "Configuración actualizada correctamente.",
        "success"
    )


    return redirect("/configuracion")