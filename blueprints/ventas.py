from flask import Blueprint, render_template, request, redirect, session, url_for

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
    actualizar_stock_venta
)

from models.movimiento_model import registrar_movimiento

import os

from utils.helpers import login_required, role_required

from models.cliente_model import listar_clientes

from flask import request

from models.empresa_model import obtener_empresa

from flask import make_response

from playwright.sync_api import sync_playwright
import tempfile

from models.producto_model import (
    listar_productos,
    actualizar_stock_venta
)

import qrcode
import os
from flask import send_file
from playwright.sync_api import sync_playwright
from flask import send_file
import tempfile


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
# CONFIRMAR VENTA
# ==========================================

@ventas.route("/ventas/confirmar", methods=["POST"])
@login_required
@role_required("Administrador", "Vendedor")
def confirmar():

    cliente = request.form["cliente"]

    forma_pago = request.form["forma_pago"]

    usuario = session["usuario"]


    carrito = listar_carrito(usuario)


    if not carrito:

        return redirect("/ventas")



    total = sum(
        item["subtotal"]
        for item in carrito
    )



    # Crear venta

    venta_id = crear_venta(
        cliente,
        total,
        usuario,
        forma_pago
    )



    # Guardar detalle y descontar stock

    for item in carrito:


        agregar_detalle_venta(
            venta_id,
            item["producto_id"],
            item["cantidad"],
            item["precio"]
        )


        actualizar_stock_venta(
            item["producto_id"],
            item["cantidad"]
        )


        registrar_movimiento(
            item["producto_id"],
            "Salida",
            item["cantidad"],
            usuario
        )



    # Limpiar carrito

    vaciar_carrito(usuario)



    return redirect(
    url_for(
        "ventas.pdf_boleta",
        id=venta_id
    )

    )


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

    empresa = obtener_empresa()


    carpeta_qr = os.path.join(
        "static",
        "qr"
    )


    if not os.path.exists(carpeta_qr):
        os.makedirs(carpeta_qr)



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

# ==========================================
# COMPROBANTE INTERNO PARA PDF
# ==========================================

@ventas.route("/ventas/comprobante_pdf/<int:id>")
def comprobante_pdf(id):

    venta = obtener_venta(id)

    detalle = detalle_venta(id)

    empresa = obtener_empresa()


    return render_template(
        "comprobante.html",
        venta=venta,
        detalle=detalle,
        empresa=empresa,
        qr=f"qr/venta_{venta['id']}.png",
        pdf=True
    )



# ==========================================
# PDF PROFESIONAL BOLETA
# ==========================================

@ventas.route("/ventas/pdf/<int:id>")
@login_required
def pdf_boleta(id):

    venta = obtener_venta(id)


    carpeta_boletas = os.path.join(
        "static",
        "boletas"
    )


    if not os.path.exists(carpeta_boletas):
        os.makedirs(carpeta_boletas)



    ruta_pdf = os.path.abspath(
        os.path.join(
            carpeta_boletas,
            f"boleta_{venta['folio']}.pdf"
        )
    )


    url = request.host_url + f"ventas/comprobante_pdf/{id}"



    with sync_playwright() as p:

        navegador = p.chromium.launch(
            headless=True
        )


        pagina = navegador.new_page(
            viewport={
                "width":302,
                "height":900
            }
        )


        pagina.goto(
            url,
            wait_until="networkidle"
        )


        pagina.wait_for_timeout(3000)



        pagina.pdf(
            path=ruta_pdf,
            width="80mm",
            print_background=True
        )


        navegador.close()



    if not os.path.exists(ruta_pdf):

        return "Error: No se pudo generar el PDF"



    return send_file(
        ruta_pdf,
        as_attachment=True,
        download_name=f"boleta_{venta['folio']}.pdf",
        mimetype="application/pdf"
    )


# ============================
# CREAR CODIGO DE BARRAS
# ============================

    carpeta_barcode = os.path.join(
        "static",
        "barcodes"
    )

    if not os.path.exists(carpeta_barcode):
        os.makedirs(carpeta_barcode)



    nombre_barcode = f"venta_{venta['folio']}"


    ruta_barcode = os.path.join(
        carpeta_barcode,
        nombre_barcode
    )



    codigo = barcode.get(
        "code128",
        venta["folio"],
        writer=ImageWriter()
    )


    codigo.save(ruta_barcode)


    return render_template(
        "comprobante.html",
        venta=venta,
        detalle=detalle,
        empresa=empresa,
        qr=f"qr/{nombre_qr}",
        barcode=f"barcodes/{nombre_barcode}.png"
    )

