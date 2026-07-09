from flask import Blueprint, render_template, request, redirect, url_for

from models.categoria_model import (
    listar_categorias,
    crear_categoria,
    eliminar_categoria,
    buscar_categoria,
    editar_categoria
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

# ==========================================
# FORMULARIO EDITAR
# ==========================================

@categorias.route("/categorias/editar/<int:id>")
def formulario_editar(id):

    categoria = buscar_categoria(id)

    return render_template(
        "editar_categoria.html",
        categoria=categoria
    )



# ==========================================
# GUARDAR EDICION
# ==========================================

@categorias.route("/categorias/actualizar/<int:id>", methods=["POST"])
def actualizar(id):

    nombre = request.form["nombre"]

    descripcion = request.form["descripcion"]


    editar_categoria(
        id,
        nombre,
        descripcion
    )


    return redirect("/categorias")