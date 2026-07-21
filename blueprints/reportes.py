from flask import Blueprint, send_file, render_template

from io import BytesIO

from models.reporte_model import (
    inventario_pdf,
    reporte_ventas,
    reporte_compras
)

from models.configuracion_model import obtener_empresa




from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
    Image
)


from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch


from datetime import datetime



reportes = Blueprint("reportes", __name__)




# ==========================================
# CENTRO DE REPORTES
# ==========================================

@reportes.route("/reportes")
def centro_reportes():

    return render_template("reportes.html")





# ==========================================
# PDF INVENTARIO
# ==========================================

@reportes.route("/reportes/inventario")
def reporte_inventario():

    productos = inventario_pdf()

    empresa = obtener_empresa()


    buffer = BytesIO()


    pdf = SimpleDocTemplate(
        buffer,
        pagesize=letter
    )


    estilos = getSampleStyleSheet()


    elementos = []



    # LOGO EMPRESA

    try:

        logo = Image(
            "static/img/" + empresa["logo"],
            width=1.2*inch,
            height=1.2*inch
        )

        elementos.append(logo)


    except:

        pass




    # DATOS EMPRESA

    elementos.append(

        Paragraph(

            f"""
            <b>{empresa['nombre']}</b><br/>
            RUT: {empresa['rut']}<br/>
            {empresa['direccion']} - {empresa['comuna']}<br/>
            Teléfono: {empresa['telefono']}<br/>
            Email: {empresa['email']}
            """,

            estilos["Normal"]

        )

    )


    elementos.append(Spacer(1,20))




    elementos.append(

        Paragraph(

            "<b>REPORTE DE INVENTARIO</b>",

            estilos["Title"]

        )

    )



    elementos.append(

        Paragraph(

            f"Fecha emisión: {datetime.now().strftime('%d/%m/%Y %H:%M')}",

            estilos["Normal"]

        )

    )



    elementos.append(Spacer(1,20))





    datos = [

        [
            "SKU",
            "Producto",
            "Categoría",
            "Marca",
            "Stock",
            "Precio"
        ]

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






    tabla = Table(
        datos,
        repeatRows=1
    )



    tabla.setStyle(TableStyle([


        ("BACKGROUND",
         (0,0),
         (-1,0),
         colors.darkblue),


        ("TEXTCOLOR",
         (0,0),
         (-1,0),
         colors.white),


        ("GRID",
         (0,0),
         (-1,-1),
         1,
         colors.grey),


        ("FONTNAME",
         (0,0),
         (-1,0),
         "Helvetica-Bold"),


        ("ALIGN",
         (0,0),
         (-1,-1),
         "CENTER")


    ]))



    elementos.append(tabla)



    pdf.build(elementos)



    buffer.seek(0)



    return send_file(

        buffer,

        as_attachment=True,

        download_name="Inventario.pdf",

        mimetype="application/pdf"

    )

# ==========================================
# PDF REPORTE DE VENTAS
# ==========================================

@reportes.route("/reportes/ventas")
def reporte_ventas_pdf():

    ventas = reporte_ventas()

    empresa = obtener_empresa()


    buffer = BytesIO()


    pdf = SimpleDocTemplate(
        buffer,
        pagesize=letter
    )


    estilos = getSampleStyleSheet()


    elementos = []



    # LOGO

    try:

        logo = Image(
            "static/img/" + empresa["logo"],
            width=1.2*inch,
            height=1.2*inch
        )

        elementos.append(logo)

    except:

        pass




    # DATOS EMPRESA

    elementos.append(

        Paragraph(

            f"""
            <b>{empresa['nombre']}</b><br/>
            RUT: {empresa['rut']}<br/>
            {empresa['direccion']} - {empresa['comuna']}<br/>
            Teléfono: {empresa['telefono']}
            """,

            estilos["Normal"]

        )

    )


    elementos.append(
        Spacer(1,20)
    )



    elementos.append(

        Paragraph(

            "REPORTE DE VENTAS",

            estilos["Title"]

        )

    )


    elementos.append(

        Paragraph(

            f"Fecha emisión: {datetime.now().strftime('%d/%m/%Y %H:%M')}",

            estilos["Normal"]

        )

    )


    elementos.append(
        Spacer(1,20)
    )




    datos = [

        [
            "ID",
            "Cliente",
            "Fecha",
            "Total",
            "Usuario",
            "Pago"
        ]

    ]



    for venta in ventas:


        datos.append([

            venta["id"],

            venta["cliente"],

            venta["fecha"],

            f"${venta['total']:,.0f}",

            venta["usuario"],

            venta["forma_pago"]

        ])




    tabla = Table(
        datos,
        repeatRows=1
    )



    tabla.setStyle(TableStyle([


        ("BACKGROUND",
         (0,0),
         (-1,0),
         colors.darkgreen),


        ("TEXTCOLOR",
         (0,0),
         (-1,0),
         colors.white),


        ("GRID",
         (0,0),
         (-1,-1),
         1,
         colors.grey),


        ("FONTNAME",
         (0,0),
         (-1,0),
         "Helvetica-Bold"),


        ("ALIGN",
         (0,0),
         (-1,-1),
         "CENTER")


    ]))



    elementos.append(tabla)



    pdf.build(elementos)



    buffer.seek(0)



    return send_file(

        buffer,

        as_attachment=True,

        download_name="Ventas.pdf",

        mimetype="application/pdf"

    )

# ==========================================
# PDF REPORTE DE COMPRAS
# ==========================================

@reportes.route("/reportes/compras")
def reporte_compras_pdf():

    compras = reporte_compras()

    empresa = obtener_empresa()


    buffer = BytesIO()


    pdf = SimpleDocTemplate(
        buffer,
        pagesize=letter
    )


    estilos = getSampleStyleSheet()


    elementos = []



    # LOGO

    try:

        logo = Image(
            "static/img/" + empresa["logo"],
            width=1.2*inch,
            height=1.2*inch
        )

        elementos.append(logo)

    except:

        pass




    elementos.append(

        Paragraph(

            f"""
            <b>{empresa['nombre']}</b><br/>
            RUT: {empresa['rut']}<br/>
            {empresa['direccion']} - {empresa['comuna']}<br/>
            Teléfono: {empresa['telefono']}
            """,

            estilos["Normal"]

        )

    )


    elementos.append(
        Spacer(1,20)
    )



    elementos.append(

        Paragraph(

            "REPORTE DE COMPRAS",

            estilos["Title"]

        )

    )


    elementos.append(

        Paragraph(

            f"Fecha emisión: {datetime.now().strftime('%d/%m/%Y %H:%M')}",

            estilos["Normal"]

        )

    )


    elementos.append(
        Spacer(1,20)
    )




    datos = [

        [
            "ID",
            "Proveedor",
            "Fecha",
            "Total",
            "Usuario"
        ]

    ]



    for compra in compras:


        datos.append([

            compra["id"],

            compra["proveedor"],

            compra["fecha"],

            f"${compra['total']:,.0f}",

            compra["usuario"]

        ])




    tabla = Table(
        datos,
        repeatRows=1
    )



    tabla.setStyle(TableStyle([


        ("BACKGROUND",
         (0,0),
         (-1,0),
         colors.orange),


        ("TEXTCOLOR",
         (0,0),
         (-1,0),
         colors.white),


        ("GRID",
         (0,0),
         (-1,-1),
         1,
         colors.grey),


        ("FONTNAME",
         (0,0),
         (-1,0),
         "Helvetica-Bold"),


        ("ALIGN",
         (0,0),
         (-1,-1),
         "CENTER")


    ]))



    elementos.append(tabla)



    pdf.build(elementos)



    buffer.seek(0)



    return send_file(

        buffer,

        as_attachment=True,

        download_name="Compras.pdf",

        mimetype="application/pdf"

    )