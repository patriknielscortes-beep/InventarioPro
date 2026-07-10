from flask import Blueprint, render_template, request, redirect, session

from models.movimiento_model import registrar_movimiento

from models.compra_model import (
    listar_compras,
    crear_compra,
    agregar_detalle
)

from models.carrito_model import (
    listar_carrito,
    agregar_carrito,
    eliminar_carrito,
    vaciar_carrito
)

from models.carrito_model import (
    listar_carrito,
    agregar_carrito,
    eliminar_carrito,
    vaciar_carrito,
    obtener_total_carrito
)

from models.proveedor_model import listar_proveedores

from models.producto_model import listar_productos

from utils.helpers import login_required

from models.compra_model import detalle_compra

from models.producto_model import actualizar_stock_compra

from models.movimiento_model import registrar_movimiento


compras = Blueprint("compras", __name__)


# ==========================================
# LISTAR COMPRAS
# ==========================================

@compras.route("/compras")
@login_required
def lista():

    datos = listar_compras()

    proveedores = listar_proveedores()

    productos = listar_productos()

    carrito = listar_carrito(session["usuario"])


    return render_template(
        "compras.html",
        compras=datos,
        proveedores=proveedores,
        productos=productos,
        carrito=carrito
    )

# ==========================================
# CARRITO AGREGAR
# ==========================================

@compras.route("/compras/carrito/agregar", methods=["POST"])
@login_required
def agregar():

    producto_id = request.form["producto_id"]

    cantidad = request.form["cantidad"]

    precio = request.form["precio"]

    usuario = session["usuario"]


    agregar_carrito(
        producto_id,
        cantidad,
        precio,
        usuario
    )


    return redirect("/compras")

# ==========================================
# CARRITO ELIMINAR
# ==========================================

@compras.route("/compras/carrito/eliminar/<int:id>")
@login_required
def eliminar(id):

    eliminar_carrito(id)

    return redirect("/compras")


# ==========================================
# REGISTRAR COMPRA
# ==========================================

@compras.route("/compras/crear", methods=["POST"])
@login_required
def crear():

    proveedor_id = request.form["proveedor_id"]

    producto_id = request.form["producto_id"]

    cantidad = request.form["cantidad"]

    precio = request.form["precio"]

    usuario = session["usuario"]


    total = int(cantidad) * float(precio)


    compra_id = crear_compra(
        proveedor_id,
        total,
        usuario
    )

    agregar_detalle(
        compra_id,
        producto_id,
        cantidad,
        precio,
        usuario
    )


    return redirect("/compras")

# ==========================================
# CONFIRMAR COMPRA
# ==========================================


@compras.route("/compras/confirmar", methods=["POST"])
@login_required
def confirmar():

    usuario = session["usuario"]

    proveedor_id = request.form["proveedor_id"]


    carrito = listar_carrito(usuario)


    total = obtener_total_carrito(usuario)


    compra_id = crear_compra(
        proveedor_id,
        total,
        usuario
    )


    for item in carrito:

        agregar_detalle(
            compra_id,
            item["producto_id"],
            item["cantidad"],
            item["precio"],
            usuario
        )

         # ACTUALIZAR STOCK

        actualizar_stock_compra(
            item["producto_id"],
            item["cantidad"]
        )


        # CREAR MOVIMIENTO ENTRADA

        registrar_movimiento(
            item["producto_id"],
            "Entrada",
            item["cantidad"],
            usuario
        )


    vaciar_carrito(usuario)


    return redirect("/compras")


# ==========================================
# DETALLE COMPRA
# ==========================================


@compras.route("/compras/detalle/<int:id>")
@login_required
def detalle(id):

    datos = detalle_compra(id)


    return render_template(
        "detalle_compra.html",
        detalle=datos,
        compra_id=id
    )