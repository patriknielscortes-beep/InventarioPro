from flask import Blueprint, render_template, request, redirect, session, url_for, send_file
import os

from playwright.sync_api import sync_playwright
import qrcode

from utils.helpers import login_required, role_required

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
    vaciar_carrito
)

from models.producto_model import (
    listar_productos,
    actualizar_stock_venta
)

from models.movimiento_model import registrar_movimiento

from models.cliente_model import (
    listar_clientes,
    buscar_cliente_nombre
)

from models.empresa_model import obtener_empresa

from models.envio_correo_model import registrar_envio

from email_service import enviar_boleta


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

    carrito = listar_carrito(
        session["usuario"]
    )


    return render_template(
        "ventas.html",
        ventas=datos,
        productos=productos,
        carrito=carrito,
        clientes=listar_clientes()
    )



# ==========================================
# AGREGAR PRODUCTO AL CARRITO
# ==========================================

@ventas.route("/ventas/carrito/agregar", methods=["POST"])
@login_required
@role_required("Administrador", "Vendedor")
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



    venta_id = crear_venta(
        cliente,
        total,
        usuario,
        forma_pago
    )



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



    vaciar_carrito(usuario)



    # ======================================
    # PDF + CORREO AUTOMÁTICO
    # ======================================

    cliente_datos = None


    try:

        ruta_pdf = generar_pdf_venta(venta_id)


        cliente_datos = buscar_cliente_nombre(cliente)



        if cliente_datos and cliente_datos["email"]:


            enviar_boleta(
                cliente_datos["email"],
                cliente_datos["nombre"],
                venta_id,
                ruta_pdf
            )


            registrar_envio(
                venta_id,
                cliente_datos["email"],
                "Enviado",
                "Boleta enviada correctamente"
            )


    except Exception as e:


        print(
            "Error enviando boleta:",
            e
        )


        registrar_envio(
            venta_id,
            cliente_datos["email"] if cliente_datos else "",
            "Error",
            str(e)
        )



    return redirect(
        url_for(
            "ventas.comprobante",
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
# ELIMINAR PRODUCTO DEL CARRITO
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



    datos_qr = f"""
InventarioPro

Venta:
{venta['folio']}

Cliente:
{venta['cliente']}

Total:
{venta['total']}

Fecha:
{venta['fecha']}
"""



    nombre_qr = f"venta_{venta['id']}.png"



    ruta_qr = os.path.join(
        carpeta_qr,
        nombre_qr
    )



    qr = qrcode.make(datos_qr)

    qr.save(ruta_qr)



    return render_template(
        "comprobante.html",
        venta=venta,
        detalle=detalle,
        empresa=empresa,
        qr=f"qr/{nombre_qr}"
    )



# ==========================================
# COMPROBANTE PARA PDF
# ==========================================

@ventas.route("/ventas/comprobante_pdf/<int:id>")
@login_required
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
# DESCARGAR PDF BOLETA
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



        pagina.pdf(
            path=ruta_pdf,
            width="80mm",
            print_background=True
        )



        navegador.close()



    return send_file(
        ruta_pdf,
        as_attachment=True,
        download_name=f"boleta_{venta['folio']}.pdf",
        mimetype="application/pdf"
    )

# ==========================================
# ENVIAR BOLETA POR CORREO
# ==========================================

@ventas.route("/ventas/enviar_correo/<int:id>")
@login_required
@role_required("Administrador", "Vendedor")
def enviar_correo(id):

    venta = obtener_venta(id)


    cliente = buscar_cliente_nombre(
        venta["cliente"]
    )


    if not cliente:

        return "Cliente no encontrado"



    if not cliente["email"]:

        return "El cliente no tiene correo registrado"



    ruta_pdf = os.path.abspath(
        f"static/boletas/boleta_{venta['folio']}.pdf"
    )



    if not os.path.exists(ruta_pdf):

        ruta_pdf = generar_pdf_venta(id)



    try:

        enviar_boleta(
            cliente["email"],
            cliente["nombre"],
            venta["folio"],
            ruta_pdf
        )


        registrar_envio(
            id,
            cliente["email"],
            "Enviado",
            "Correo enviado manualmente"
        )


        return redirect("/envios")



    except Exception as e:


        registrar_envio(
            id,
            cliente["email"],
            "Error",
            str(e)
        )


        return redirect("/envios")




# ==========================================
# REENVIAR BOLETA DESDE HISTORIAL
# ==========================================

@ventas.route("/ventas/reenviar_correo/<int:id>")
@login_required
@role_required("Administrador", "Vendedor")
def reenviar_correo(id):


    venta = obtener_venta(id)



    if not venta:

        return "Venta no encontrada"



    cliente = buscar_cliente_nombre(
        venta["cliente"]
    )



    if not cliente:

        return "Cliente no encontrado"



    if not cliente["email"]:

        return "Cliente sin correo registrado"



    try:


        ruta_pdf = generar_pdf_venta(id)



        enviar_boleta(
            cliente["email"],
            cliente["nombre"],
            venta["folio"],
            ruta_pdf
        )



        registrar_envio(
            id,
            cliente["email"],
            "Enviado",
            "Correo reenviado desde historial"
        )



    except Exception as e:


        registrar_envio(
            id,
            cliente["email"],
            "Error",
            str(e)
        )



    return redirect("/envios")




# ==========================================
# GENERAR PDF AUTOMÁTICO
# ==========================================

def generar_pdf_venta(id):


    venta = obtener_venta(id)


    carpeta = os.path.join(
        "static",
        "boletas"
    )



    if not os.path.exists(carpeta):

        os.makedirs(carpeta)



    ruta_pdf = os.path.abspath(
        os.path.join(
            carpeta,
            f"boleta_{venta['folio']}.pdf"
        )
    )



    url = request.host_url + f"ventas/comprobante_pdf/{id}"



    with sync_playwright() as p:


        navegador = p.chromium.launch(
            headless=True
        )



        pagina = navegador.new_page()



        pagina.goto(
            url,
            wait_until="networkidle"
        )



        pagina.pdf(
            path=ruta_pdf,
            width="80mm",
            print_background=True
        )



        navegador.close()



    return ruta_pdf