from flask import Blueprint, render_template, request, redirect

from models.cliente_model import (
    listar_clientes,
    crear_cliente,
    eliminar_cliente,
    editar_cliente,
    obtener_cliente,
    historial_cliente,
    resumen_cliente,
    buscar_email,
    buscar_rut
)

from utils.helpers import login_required, role_required
from flask import flash



clientes = Blueprint("clientes", __name__)



# ==========================================
# LISTAR CLIENTES
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
# CREAR CLIENTE
# ==========================================

@clientes.route("/clientes/crear", methods=["POST"])
@login_required
@role_required("Administrador","Vendedor")
def crear():


    nombre = request.form["nombre"]
    rut = request.form["rut"]
    telefono = request.form["telefono"]
    email = request.form["email"]
    direccion = request.form["direccion"]



    if buscar_email(email):

        flash(
            "⚠️ El correo ya está registrado",
            "warning"
        )

        return redirect("/clientes")



    if rut and buscar_rut(rut):

        flash(
            "⚠️ El RUT ya está registrado",
            "warning"
        )

        return redirect("/clientes")




    crear_cliente(
        nombre,
        rut,
        telefono,
        email,
        direccion
    )


    flash(
        "✅ Cliente creado correctamente",
        "success"
    )


    return redirect("/clientes")



# ==========================================
# EDITAR CLIENTE
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


    return redirect("/clientes")



# ==========================================
# ELIMINAR CLIENTE
# ==========================================

@clientes.route("/clientes/eliminar/<int:id>")
@login_required
@role_required("Administrador")
def eliminar(id):

    eliminar_cliente(id)

    return redirect("/clientes")



# ==========================================
# HISTORIAL DE COMPRAS
# ==========================================

@clientes.route("/clientes/historial/<int:id>")
@login_required
@role_required("Administrador","Vendedor")
def historial(id):

    cliente = obtener_cliente(id)


    if not cliente:

        return redirect("/clientes")



    compras = historial_cliente(
        cliente["nombre"]
    )


    resumen = resumen_cliente(
        cliente["nombre"]
    )



    return render_template(
        "historial_cliente.html",
        cliente=cliente,
        compras=compras,
        resumen=resumen
    )