from flask import Blueprint, render_template, request, redirect, url_for, session, flash

from utils.helpers import login_required, role_required

from models.producto_model import buscar_por_sku

from models.producto_model import (
    listar_productos,
    buscar_productos
)
from models.cliente_model import listar_clientes
from models.carrito_venta_model import vaciar_carrito

from models.carrito_venta_model import (
    agregar_carrito,
    listar_carrito,
    eliminar_carrito,
    obtener_total_carrito,
    aumentar_cantidad,
    disminuir_cantidad
)

from models.venta_model import (
    crear_venta,
    agregar_detalle_venta
)

from models.producto_model import actualizar_stock_venta

from models.movimiento_model import registrar_movimiento


pos = Blueprint("pos", __name__)



# ==========================================
# PUNTO DE VENTA
# ==========================================

@pos.route("/pos")
@login_required
@role_required("Administrador", "Vendedor")
def punto_venta():

    usuario = session["usuario"]


    productos = listar_productos()

    clientes = listar_clientes()

    carrito = listar_carrito(usuario)

    total = obtener_total_carrito(usuario)


    return render_template(
        "pos.html",
        productos=productos,
        clientes=clientes,
        carrito=carrito,
        total=total
    )


# ==========================================
# BUSCAR PRODUCTOS POS
# ==========================================

@pos.route("/buscar_productos")
@login_required
@role_required("Administrador", "Vendedor")
def buscar_productos_pos():

    texto = request.args.get("q", "")

    productos = buscar_productos(texto)

    return render_template(
        "pos.html",
        productos=productos,
        clientes=listar_clientes(),
        carrito=listar_carrito(session["usuario"]),
        total=obtener_total_carrito(session["usuario"])
    )


# ==========================================
# AGREGAR AL CARRITO
# ==========================================

@pos.route("/agregar_carrito", methods=["POST"])
@login_required
@role_required("Administrador", "Vendedor")
def agregar_carrito_pos():

    producto_id = request.form["producto_id"]

    precio = request.form["precio"]

    usuario = session["usuario"]


    resultado = agregar_carrito(
        producto_id,
        1,
        precio,
        usuario
    )


    if resultado == False:

        flash(
            "Stock insuficiente para agregar producto",
            "danger"
        )

    else:

        flash(
            "Producto agregado al carrito",
            "success"
        )


    return redirect(
        url_for("pos.punto_venta")
    )


# ==========================================
# ELIMINAR DEL CARRITO
# ==========================================

@pos.route("/pos/carrito/eliminar/<int:id>")
@login_required
@role_required("Administrador", "Vendedor")
def eliminar_carrito_pos(id):

    eliminar_carrito(id)


    return redirect(
        url_for("pos.punto_venta")
    )

# ==========================================
# BUSCAR PRODUCTO POR SKU
# ==========================================

@pos.route("/buscar_sku")
@login_required
@role_required("Administrador", "Vendedor")
def buscar_sku():

    sku = request.args.get("sku")


    producto = buscar_por_sku(sku)


    if producto:

        return render_template(
            "pos.html",
            productos=[producto],
            clientes=listar_clientes(),
            carrito=listar_carrito(session["usuario"]),
            total=obtener_total_carrito(session["usuario"])
        )


    flash(
        "Producto no encontrado",
        "danger"
    )


    return redirect(
        url_for("pos.punto_venta")
    )

# ==========================================
# AUMENTAR CANTIDAD CARRITO
# ==========================================

@pos.route("/pos/carrito/aumentar/<int:id>")
@login_required
@role_required("Administrador", "Vendedor")
def aumentar_carrito_pos(id):

    aumentar_cantidad(id)

    return redirect(
        url_for("pos.punto_venta")
    )



# ==========================================
# DISMINUIR CANTIDAD CARRITO
# ==========================================

@pos.route("/pos/carrito/disminuir/<int:id>")
@login_required
@role_required("Administrador", "Vendedor")
def disminuir_carrito_pos(id):

    disminuir_cantidad(id)

    return redirect(
        url_for("pos.punto_venta")
    )

# ==========================================
# COBRAR
# ==========================================
@pos.route("/cobrar", methods=["POST"])
@login_required
@role_required("Administrador", "Vendedor")
def cobrar():

    print("========== ENTRO A COBRAR ==========")

    usuario = session["usuario"]

    cliente = request.form["cliente"]

    forma_pago = request.form["forma_pago"]

    carrito = listar_carrito(usuario)

    total = obtener_total_carrito(usuario)


    print("Cliente:", cliente)
    print("Carrito:", carrito)
    print("Total:", total)



    venta_id = crear_venta(
    cliente,
    total,
    usuario,
    forma_pago
    )

    print("VENTA CREADA ID:", venta_id)

    print("=================================")
    print("TOTAL ITEMS:", len(carrito))

    for i, item in enumerate(carrito, start=1):
        print(f"ITEM {i}:", dict(item))

    for item in carrito:

        print("==============================")
        print("PROCESANDO PRODUCTO")
        print("ID:", item["producto_id"])
        print("CANTIDAD:", item["cantidad"])
        print("==============================")


        agregar_detalle_venta(
            venta_id,
            item["producto_id"],
            item["cantidad"],
            item["precio"]
        )


        print("DETALLE GUARDADO")

        print(">>> EJECUTANDO DESCUENTO STOCK <<<")


        actualizar_stock_venta(
            item["producto_id"],
            item["cantidad"]
        )


        print("STOCK ACTUALIZADO")



        registrar_movimiento(
            item["producto_id"],
            "Salida",
            item["cantidad"],
            usuario
        )


        print("MOVIMIENTO REGISTRADO")



    print("VACIANDO CARRITO DEL USUARIO:", usuario)

    vaciar_carrito(usuario)

    print("CARRITO DESPUÉS:", listar_carrito(usuario))

    flash(
    f"Venta N° {venta_id} realizada correctamente.",
    "success"
    )



    return redirect(
        url_for("ventas.comprobante", id=venta_id)
    )

    