from flask import Blueprint, render_template, session, redirect
from models.dashboard_model import (
    obtener_estadisticas,
    productos_por_categoria,
    valor_inventario,
    movimientos_tipo,
    productos_stock_bajo
)


dashboard = Blueprint("dashboard", __name__)


@dashboard.route("/dashboard")
def inicio():

    if "usuario" not in session:
        return redirect("/")


    datos = obtener_estadisticas()

    categorias = productos_por_categoria()

    valor = valor_inventario()

    movimientos = movimientos_tipo()

    stock_bajo = productos_stock_bajo()


    return render_template(
        "dashboard.html",
        usuario=session["usuario"],
        rol=session["rol"],
        datos=datos,
        categorias=categorias,
        valor=valor,
        movimientos=movimientos,
         stock_bajo=stock_bajo
    )