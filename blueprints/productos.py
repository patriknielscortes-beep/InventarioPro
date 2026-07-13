from flask import Blueprint, render_template, request, redirect, url_for, flash

from utils.helpers import login_required, role_required

from models.producto_model import obtener_producto

from models.categoria_model import listar_categorias
from models.marca_model import listar_marcas

from models.producto_model import (
    listar_productos,
    crear_producto,
    buscar_producto,
    editar_producto,
    eliminar_producto
)

productos = Blueprint("productos", __name__)


# ==========================================
# LISTAR PRODUCTOS
# ==========================================

@productos.route("/productos")
@login_required
@role_required("Administrador", "Vendedor")
def lista():

    productos_lista = listar_productos()

    categorias = listar_categorias()

    marcas = listar_marcas()


    return render_template(
        "productos.html",
        productos=productos_lista,
        categorias=categorias,
        marcas=marcas
    )


# ==========================================
# CREAR PRODUCTO
# ==========================================

@productos.route("/productos/nuevo", methods=["GET", "POST"])
@login_required
@role_required("Administrador")
def nuevo():

    if request.method == "POST":

        nombre = request.form["nombre"]
        categoria_id = request.form["categoria_id"]
        marca_id = request.form["marca_id"]
        stock = request.form["stock"]
        precio = request.form["precio"]
        archivo = request.files.get("imagen")
        imagen = "default.png"

        if archivo and archivo.filename != "":
            
            nombre_archivo = archivo.filename

            ruta = "static/img/productos/" + nombre_archivo

            archivo.save(ruta)

            imagen = nombre_archivo


        crear_producto(
            nombre,
            categoria_id,
            marca_id,
            stock,
            precio,
            imagen
        )


        flash(
            "Producto creado correctamente",
            "success"
        )


        return redirect(
            url_for("productos.lista")
        )


    return render_template(
    "crear_producto.html",
    categorias=listar_categorias(),
    marcas=listar_marcas()
    )


# ==========================================
# VER CODIGO DE BARRAS
# ==========================================

@productos.route("/productos/barcode/<int:id>")
@login_required
@role_required("Administrador")
def barcode_producto(id):

    producto = obtener_producto(id)


    return render_template(
        "barcode.html",
        producto=producto
    )

# ==========================================
# EDITAR PRODUCTO
# ==========================================

@productos.route("/productos/editar/<int:id>", methods=["GET", "POST"])
@login_required
@role_required("Administrador")
def editar(id):

    print("MÉTODO:", request.method)
    print("ID:", id)

    producto = buscar_producto(id)

    if not producto:

        flash(
            "Producto no encontrado",
            "danger"
        )

        return redirect(
            url_for("productos.lista")
        )


    if request.method == "POST":

        nombre = request.form["nombre"]
        categoria_id = request.form["categoria_id"]
        marca_id = request.form["marca_id"]
        stock = request.form["stock"]
        precio = request.form["precio"]


        editar_producto(
            id,
            nombre,
            categoria_id,
            marca_id,
            stock,
            precio
        )


        flash(
            "Producto actualizado correctamente",
            "success"
        )


        return redirect(
            url_for("productos.lista")
        )


    return render_template(
          "editar_producto.html",
           producto=producto,
           categorias=listar_categorias(),
           marcas=listar_marcas(),
    )


# ==========================================
# ELIMINAR PRODUCTO
# ==========================================

@productos.route("/productos/eliminar/<int:id>")
@login_required
@role_required("Administrador")
def eliminar(id):

    eliminar_producto(id)


    flash(
        "Producto eliminado correctamente",
        "success"
    )


    return redirect(
        url_for("productos.lista")
    )