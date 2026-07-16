from flask import Blueprint, render_template, request, redirect, flash

from models.cliente_model import (
    listar_clientes,
    crear_cliente,
    eliminar_cliente,
    editar_cliente,
    buscar_email
)

from utils.helpers import login_required, role_required


clientes = Blueprint("clientes", __name__)



# ==========================================
# LISTAR
# ==========================================

@clientes.route("/clientes")
@login_required
@role_required("Administrador","Vendedor")
def lista():

    datos = listar_clientes()

    return render_template(
        "clientes.html",
        clientes=datos
    )



# ==========================================
# CREAR
# ==========================================

@clientes.route("/clientes/crear", methods=["POST"])
@login_required
@role_required("Administrador","Vendedor")
def crear():


    email = request.form["email"]


    existe = buscar_email(email)


    if existe:

        flash(
            "⚠️ El correo ya está registrado",
            "warning"
        )

        return redirect("/clientes")



    crear_cliente(

        request.form["nombre"],

        request.form["rut"],

        request.form["telefono"],

        email,

        request.form["direccion"]

    )


    flash(
        "✅ Cliente creado correctamente",
        "success"
    )


    return redirect("/clientes")



# ==========================================
# EDITAR
# ==========================================

@clientes.route("/clientes/editar/<int:id>", methods=["POST"])
@login_required
@role_required("Administrador","Vendedor")
def editar(id):

    editar_cliente(
        id,
        request.form["nombre"],
        request.form["rut"],
        request.form["telefono"],
        request.form["email"],
        request.form["direccion"]
    )


    flash(
        "✅ Cliente actualizado",
        "success"
    )


    return redirect("/clientes")



# ==========================================
# ELIMINAR
# ==========================================

@clientes.route("/clientes/eliminar/<int:id>")
@login_required
@role_required("Administrador")
def eliminar(id):

    eliminar_cliente(id)


    flash(
        "🗑️ Cliente eliminado",
        "success"
    )


    return redirect("/clientes")