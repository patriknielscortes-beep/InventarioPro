from flask import Blueprint, render_template, request, redirect

from models.proveedor_model import (
    listar_proveedores,
    crear_proveedor,
    buscar_proveedor,
    editar_proveedor,
    eliminar_proveedor
)

from utils.helpers import login_required


proveedores = Blueprint("proveedores", __name__)


# ==========================================
# LISTAR PROVEEDORES
# ==========================================

@proveedores.route("/proveedores")
@login_required
def lista():

    datos = listar_proveedores()

    return render_template(
        "proveedores.html",
        proveedores=datos
    )


# ==========================================
# CREAR PROVEEDOR
# ==========================================

@proveedores.route("/proveedores/crear", methods=["POST"])
@login_required
def crear():

    nombre = request.form["nombre"]
    rut = request.form["rut"]
    telefono = request.form["telefono"]
    email = request.form["email"]
    direccion = request.form["direccion"]

    crear_proveedor(
        nombre,
        rut,
        telefono,
        email,
        direccion
    )

    return redirect("/proveedores")


# ==========================================
# FORMULARIO EDITAR
# ==========================================

@proveedores.route("/proveedores/editar/<int:id>")
@login_required
def formulario_editar(id):

    proveedor = buscar_proveedor(id)

    return render_template(
        "editar_proveedor.html",
        proveedor=proveedor
    )


# ==========================================
# ACTUALIZAR
# ==========================================

@proveedores.route("/proveedores/actualizar/<int:id>", methods=["POST"])
@login_required
def actualizar(id):

    nombre = request.form["nombre"]
    rut = request.form["rut"]
    telefono = request.form["telefono"]
    email = request.form["email"]
    direccion = request.form["direccion"]

    editar_proveedor(
        id,
        nombre,
        rut,
        telefono,
        email,
        direccion
    )

    return redirect("/proveedores")


# ==========================================
# ELIMINAR
# ==========================================

@proveedores.route("/proveedores/eliminar/<int:id>")
@login_required
def eliminar(id):

    eliminar_proveedor(id)

    return redirect("/proveedores")