from flask import Blueprint, render_template, session, redirect
from models.dashboard_model import (
    obtener_estadisticas,
    productos_por_categoria
)


dashboard = Blueprint("dashboard", __name__)


@dashboard.route("/dashboard")
def inicio():

    if "usuario" not in session:
        return redirect("/")


    datos = obtener_estadisticas()

    categorias = productos_por_categoria()


    return render_template(
        "dashboard.html",
        usuario=session["usuario"],
        rol=session["rol"],
        datos=datos,
        categorias=categorias
    )