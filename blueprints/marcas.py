from flask import Blueprint, render_template, request, redirect

from models.marca_model import (
    listar_marcas,
    crear_marca,
    buscar_marca,
    editar_marca,
    eliminar_marca
)

from utils.helpers import login_required


marcas = Blueprint("marcas", __name__)


# ==========================================
# LISTAR MARCAS
# ==========================================

@marcas.route("/marcas")
@login_required
def lista():

    datos = listar_marcas()

    return render_template(
        "marcas.html",
        marcas=datos
    )


# ==========================================
# CREAR MARCA
# ==========================================

@marcas.route("/marcas/crear", methods=["POST"])
@login_required
def crear():

    nombre = request.form["nombre"]

    descripcion = request.form["descripcion"]


    crear_marca(
        nombre,
        descripcion
    )


    return redirect("/marcas")


# ==========================================
# FORMULARIO EDITAR
# ==========================================

@marcas.route("/marcas/editar/<int:id>")
@login_required
def formulario_editar(id):

    marca = buscar_marca(id)

    return render_template(
        "editar_marca.html",
        marca=marca
    )


# ==========================================
# ACTUALIZAR MARCA
# ==========================================

@marcas.route("/marcas/actualizar/<int:id>", methods=["POST"])
@login_required
def actualizar(id):

    nombre = request.form["nombre"]

    descripcion = request.form["descripcion"]


    editar_marca(
        id,
        nombre,
        descripcion
    )


    return redirect("/marcas")


# ==========================================
# ELIMINAR MARCA
# ==========================================

@marcas.route("/marcas/eliminar/<int:id>")
@login_required
def eliminar(id):

    eliminar_marca(id)

    return redirect("/marcas")