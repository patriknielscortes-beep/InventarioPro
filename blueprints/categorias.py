from flask import Blueprint, render_template, request, redirect, url_for

from models.categoria_model import (
    listar_categorias,
    crear_categoria,
    eliminar_categoria
)


categorias = Blueprint("categorias", __name__)


# ==========================================
# LISTAR CATEGORIAS
# ==========================================

@categorias.route("/categorias")
def lista():

    datos = listar_categorias()

    return render_template(
        "categorias.html",
        categorias=datos
    )



# ==========================================
# CREAR CATEGORIA
# ==========================================

@categorias.route("/categorias/crear", methods=["POST"])
def crear():

    nombre = request.form["nombre"]

    descripcion = request.form["descripcion"]


    crear_categoria(
        nombre,
        descripcion
    )


    return redirect("/categorias")



# ==========================================
# ELIMINAR CATEGORIA
# ==========================================

@categorias.route("/categorias/eliminar/<int:id>")
def eliminar(id):

    eliminar_categoria(id)

    return redirect("/categorias")