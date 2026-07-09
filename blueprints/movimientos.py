from flask import Blueprint, render_template, request, redirect, session

from models.movimiento_model import (
    listar_movimientos,
    registrar_movimiento
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

    registrar_movimiento(
        producto_id,
        tipo,
        cantidad,
        usuario
    )

    return redirect("/movimientos")