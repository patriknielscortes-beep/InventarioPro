from flask import Blueprint
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

from models.reporte_model import inventario_pdf

reportes = Blueprint("reportes", __name__)

@reportes.route("/reportes/inventario")
def reporte_inventario():

    productos = inventario_pdf()

    pdf = SimpleDocTemplate("inventario.pdf")

    estilos = getSampleStyleSheet()

    elementos = []

    elementos.append(
        Paragraph("<b>REPORTE DE INVENTARIO</b>", estilos["Title"])
    )

    datos = [
        ["SKU", "Producto", "Categoría", "Marca", "Stock", "Precio"]
    ]

    for p in productos:

        datos.append([
            p["sku"],
            p["nombre"],
            p["categoria"],
            p["marca"],
            p["stock"],
            f"${p['precio']:,.0f}"
        ])

    tabla = Table(datos)

    tabla.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),colors.darkblue),
        ("TEXTCOLOR",(0,0),(-1,0),colors.white),
        ("GRID",(0,0),(-1,-1),1,colors.grey),
        ("BACKGROUND",(0,1),(-1,-1),colors.beige),
        ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
        ("ALIGN",(0,0),(-1,-1),"CENTER"),
    ]))

    elementos.append(tabla)

    pdf.build(elementos)

    return "PDF generado correctamente."