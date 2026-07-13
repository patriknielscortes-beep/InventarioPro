from flask import Blueprint, render_template, request, redirect, session

from models.venta_model import (
    listar_ventas,
    crear_venta,
    agregar_detalle_venta,
    detalle_venta,
    obtener_venta,
    anular_venta
)

from models.carrito_venta_model import (
    listar_carrito,
    agregar_carrito,
    eliminar_carrito,
    vaciar_carrito,
    obtener_total_carrito
)

from models.producto_model import (
    listar_productos,
    actualizar_stock_venta
)

from models.movimiento_model import registrar_movimiento

from utils.helpers import login_required, role_required

from models.cliente_model import listar_clientes

from models.empresa_model import obtener_empresa

import qrcode
import os


ventas = Blueprint("ventas", __name__)


# ==========================================
# LISTAR VENTAS
# ==========================================

@ventas.route("/ventas")
@login_required
@role_required("Administrador", "Vendedor")
def lista():

    datos = listar_ventas()

    productos = listar_productos()

    carrito = listar_carrito(session["usuario"])


    return render_template(
        "ventas.html",
        ventas=datos,
        productos=productos,
        carrito=carrito,
        clientes = listar_clientes()
    )


# ==========================================
# AGREGAR PRODUCTO AL CARRITO
# ==========================================

@ventas.route("/ventas/carrito/agregar", methods=["POST"])
@login_required
@role_required("Administrador","Vendedor")
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


    return redirect("/ventas")


# ==========================================
# ANULAR VENTA
# ==========================================

@ventas.route("/ventas/anular/<int:id>")
@login_required
@role_required("Administrador")
def anular(id):

    usuario = session["usuario"]


    detalle = anular_venta(id)



    for item in detalle:

        registrar_movimiento(
            item["producto_id"],
            "Entrada",
            item["cantidad"],
            usuario
        )


    return redirect("/ventas")


# ==========================================
# ELIMINAR PRODUCTO CARRITO
# ==========================================

@ventas.route("/ventas/carrito/eliminar/<int:id>")
@login_required
def eliminar(id):

    eliminar_carrito(id)

    return redirect("/ventas")


# ==========================================
# DETALLE DE VENTA
# ==========================================

@ventas.route("/ventas/detalle/<int:id>")
@login_required
def detalle(id):

    datos = detalle_venta(id)


    return render_template(
        "detalle_venta.html",
        detalle=datos,
        venta_id=id
    )

# ==========================================
# COMPROBANTE
# ==========================================

@ventas.route("/ventas/comprobante/<int:id>")
@login_required
def comprobante(id):

    venta = obtener_venta(id)

    detalle = detalle_venta(id)

    print("VENTA:", id)
    print("DETALLE:", detalle)

    empresa = obtener_empresa()


    # Crear carpeta QR si no existe

    carpeta_qr = os.path.join(
        "static",
        "qr"
    )

    if not os.path.exists(carpeta_qr):
        os.makedirs(carpeta_qr)


    # Datos QR

    datos = f"""
    InventarioPro

    Venta: {venta['folio']}
    Cliente: {venta['cliente']}
    Total: {venta['total']}
    Fecha: {venta['fecha']}
    """


    nombre_qr = f"venta_{venta['id']}.png"


    ruta_qr = os.path.join(
        carpeta_qr,
        nombre_qr
    )


    qr = qrcode.make(datos)

    qr.save(ruta_qr)


    return render_template(
        "comprobante.html",
        venta=venta,
        detalle=detalle,
        empresa=empresa,
        qr=f"qr/{nombre_qr}"
    )