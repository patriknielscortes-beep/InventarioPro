from flask import Blueprint, render_template, request, redirect, session

from models.movimiento_model import (
    listar_movimientos,
    registrar_movimiento
)

from models.movimiento_model import (
    listar_movimientos,
    registrar_movimiento,
    movimientos_por_producto,
    resumen_producto
)

from models.producto_model import listar_productos

from utils.helpers import login_required


movimientos = Blueprint("movimientos", __name__)


# ==========================================
# LISTAR MOVIMIENTOS
# ==========================================

@movimientos.route("/movimientos")
@login_required
def lista():

    datos = listar_movimientos()

    productos = listar_productos()

    return render_template(
        "movimientos.html",
        movimientos=datos,
        productos=productos
    )


# ==========================================
# REGISTRAR MOVIMIENTO
# ==========================================

@movimientos.route("/movimientos/registrar", methods=["POST"])
@login_required
def registrar():

    producto_id = request.form["producto_id"]
    tipo = request.form["tipo"]
    cantidad = request.form["cantidad"]
    usuario = session["usuario"]


    resultado = registrar_movimiento(
        producto_id,
        tipo,
        cantidad,
        usuario
    )


    if not resultado:

        return "Error: stock insuficiente o producto inexistente"


    return redirect("/movimientos")

# ==========================================
# DETALLE MOVIMIENTOS PRODUCTO
# ==========================================

@movimientos.route("/movimientos/producto/<int:id>")
@login_required
def detalle_producto(id):

    datos = movimientos_por_producto(id)

    producto, resumen = resumen_producto(id)


    return render_template(
        "detalle_movimientos.html",
        movimientos=datos,
        producto=producto,
        resumen=resumen
    )