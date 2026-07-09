from flask import Blueprint, render_template, request, redirect

from models.producto_model import (
    listar_productos,
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


    print("PRODUCTO RECIBIDO:")
    print(nombre, categoria_id, marca_id, stock, precio)


    crear_producto(
        nombre,
        categoria_id,
        marca_id,
        stock,
        precio
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