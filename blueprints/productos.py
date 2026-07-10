from flask import Blueprint, render_template, request, redirect
import os
from models.producto_model import (
    listar_productos,
    buscar_productos,
    crear_producto,
    buscar_producto,
    editar_producto,
    eliminar_producto
)

from models.categoria_model import listar_categorias

from models.marca_model import listar_marcas

from utils.helpers import login_required


productos = Blueprint("productos", __name__)


# ==========================================
# LISTAR PRODUCTOS
# ==========================================

@productos.route("/productos")
@login_required
def lista():

    buscar = request.args.get("buscar")


    if buscar:

        datos = buscar_productos(buscar)

    else:

        datos = listar_productos()


    categorias = listar_categorias()

    marcas = listar_marcas()


    return render_template(
        "productos.html",
        productos=datos,
        categorias=categorias,
        marcas=marcas
    )

# ==========================================
# CREAR PRODUCTO
# ==========================================

@productos.route("/productos/crear", methods=["POST"])
@login_required
def crear():

    nombre = request.form["nombre"]

    categoria_id = request.form["categoria_id"]

    marca_id = request.form["marca_id"]

    stock = request.form["stock"]

    precio = request.form["precio"]


    imagen = request.files.get("imagen")


    nombre_imagen = None


    if imagen and imagen.filename:

        carpeta = "static/uploads/productos"

        os.makedirs(carpeta, exist_ok=True)


        nombre_imagen = imagen.filename


        ruta = os.path.join(
            carpeta,
            nombre_imagen
        )


        imagen.save(ruta)



    crear_producto(
        nombre,
        categoria_id,
        marca_id,
        stock,
        precio,
        nombre_imagen
    )


    return redirect("/productos")

# ==========================================
# FORMULARIO EDITAR PRODUCTO
# ==========================================

@productos.route("/productos/editar/<int:id>")
@login_required
def formulario_editar(id):

    producto = buscar_producto(id)

    categorias = listar_categorias()

    marcas = listar_marcas()


    return render_template(
        "editar_producto.html",
        producto=producto,
        categorias=categorias,
        marcas=marcas
    )



# ==========================================
# ACTUALIZAR PRODUCTO
# ==========================================

@productos.route("/productos/actualizar/<int:id>", methods=["POST"])
@login_required
def actualizar(id):

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


    return redirect("/productos")



# ==========================================
# ELIMINAR PRODUCTO
# ==========================================

@productos.route("/productos/eliminar/<int:id>")
@login_required
def eliminar(id):

    eliminar_producto(id)

    return redirect("/productos")