from flask import Blueprint, render_template, request, redirect

from models.cliente_model import (
    listar_clientes,
    crear_cliente,
    eliminar_cliente
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

    crear_cliente(

        request.form["nombre"],

        request.form["rut"],

        request.form["telefono"],

        request.form["email"],

        request.form["direccion"]

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

    return redirect("/clientes")