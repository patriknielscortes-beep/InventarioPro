from flask import Blueprint, render_template, session, redirect

from models.dashboard_model import (
    obtener_estadisticas,
    productos_por_categoria,
    valor_inventario,
    movimientos_tipo,
    productos_stock_bajo,
    ventas_hoy,
    ventas_mes,
    productos_mas_vendidos,
    ultimas_ventas
)

dashboard = Blueprint("dashboard", __name__)


# ==========================================
# DASHBOARD
# ==========================================

@dashboard.route("/dashboard")
def inicio():

    if "usuario" not in session:
        return redirect("/")


    datos = obtener_estadisticas()

    categorias = productos_por_categoria()

    valor = valor_inventario()

    movimientos = movimientos_tipo()

    stock_bajo = productos_stock_bajo()

    ventas_dia = ventas_hoy()

    ventas_mensuales = ventas_mes()

    mas_vendidos = productos_mas_vendidos()

    ventas_recientes = ultimas_ventas() 


    # NUEVAS ESTADÍSTICAS

    ventas_dia = ventas_hoy()

    ventas_mensuales = ventas_mes()

    mas_vendidos = productos_mas_vendidos()

    ultimas = ultimas_ventas()



    return render_template(
        "dashboard.html",
        usuario=session["usuario"],
        rol=session["rol"],
        datos=datos,
        categorias=categorias,
        valor=valor,
        movimientos=movimientos,
        stock_bajo=stock_bajo,
        ventas_recientes=ventas_recientes,
        ventas_dia=ventas_dia,
        ventas_mes=ventas_mensuales,
        mas_vendidos=mas_vendidos,
        ultimas=ultimas
    )