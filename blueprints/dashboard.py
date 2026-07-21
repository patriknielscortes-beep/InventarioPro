from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    request,
    jsonify,
    send_file
)

import os
from datetime import datetime

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    Table,
    TableStyle,
    PageBreak
)

from models.dashboard_model import (
    obtener_estadisticas,
    productos_por_categoria,
    valor_inventario,
    movimientos_tipo,
    productos_stock_bajo,
    ventas_hoy,
    ventas_mes,
    productos_mas_vendidos,
    ultimas_ventas,
    total_clientes,
    total_ventas,
    productos_agotados,
    ventas_ultimos_7_dias,
    compras_mes,
    ventas_compras_mes,
    ganancias_por_mes,
    top_vendedores,
    obtener_notificaciones,
    ultimo_producto,
    ultimo_cliente,
    actividad_reciente,
    lista_productos_agotados,
    obtener_usuario,
    ultima_compra,
    ventas_por_periodo
)

dashboard = Blueprint(
    "dashboard",
    __name__
)


# ==========================================
# DASHBOARD INVENTARIOPRO
# BLOQUE 1/5
# IMPORTS + BLUEPRINT + DASHBOARD PRINCIPAL
# ==========================================


from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    request,
    jsonify,
    send_file
)

import os

from datetime import datetime


import matplotlib.pyplot as plt


from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet


from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    Table,
    TableStyle,
    PageBreak
)



# ==========================================
# MODELOS DASHBOARD
# ==========================================


from models.dashboard_model import (

    obtener_estadisticas,

    productos_por_categoria,

    valor_inventario,

    movimientos_tipo,

    productos_stock_bajo,

    ventas_hoy,

    ventas_mes,

    productos_mas_vendidos,

    ultimas_ventas,

    total_clientes,

    total_ventas,

    productos_agotados,

    ventas_ultimos_7_dias,

    compras_mes,

    ventas_compras_mes,

    ganancias_por_mes,

    top_vendedores,

    obtener_notificaciones,

    ultimo_producto,

    ultimo_cliente,

    actividad_reciente,

    lista_productos_agotados,

    obtener_usuario,

    ultima_compra,

    ventas_por_periodo

)



# ==========================================
# BLUEPRINT
# ==========================================


dashboard = Blueprint(
    "dashboard",
    __name__
)



# ==========================================
# DASHBOARD PRINCIPAL
# ==========================================


@dashboard.route("/dashboard")
def inicio():


    if "usuario" not in session:

        return redirect("/")



    # ======================================
    # DATOS GRÁFICOS
    # ======================================


    categorias = [

        list(x)

        for x in productos_por_categoria()

    ]


    movimientos = [

        list(x)

        for x in movimientos_tipo()

    ]


    comparativo = [

        list(x)

        for x in ventas_compras_mes()

    ]


    ganancias = [

        list(x)

        for x in ganancias_por_mes()

    ]


    grafico_ventas = [

        list(x)

        for x in ventas_ultimos_7_dias()

    ]



    # ======================================
    # DATOS GENERALES
    # ======================================


    actividad = actividad_reciente()


    usuario_info = obtener_usuario(
        session["usuario"]
    )


    notificaciones = obtener_notificaciones()


    agotados_lista = lista_productos_agotados()



    return render_template(

        "dashboard.html",



        # ==============================
        # SESIÓN
        # ==============================

        usuario=session["usuario"],

        rol=session["rol"],



        # ==============================
        # GENERALES
        # ==============================

        datos=obtener_estadisticas(),

        clientes_total=total_clientes(),

        ventas_total=total_ventas(),

        agotados=productos_agotados(),

        usuario_info=usuario_info,

        notificaciones=notificaciones,

        agotados_lista=agotados_lista,



        # ==============================
        # INVENTARIO
        # ==============================

        categorias=categorias,

        valor=valor_inventario(),

        movimientos=movimientos,

        stock_bajo=productos_stock_bajo(),



        # ==============================
        # VENTAS
        # ==============================

        ventas_dia=ventas_hoy(),

        ventas_mes=ventas_mes(),

        compras=compras_mes(),

        mas_vendidos=productos_mas_vendidos(),

        ultimas=ultimas_ventas(),

        ultimo_producto=ultimo_producto(),

        ultimo_cliente=ultimo_cliente(),

        ultima_compra=ultima_compra(),



        # ==============================
        # GRÁFICOS
        # ==============================

        comparativo=comparativo,

        ganancias=ganancias,

        grafico_ventas=grafico_ventas,

        actividad=actividad,



        # ==============================
        # RANKING
        # ==============================

        top_vendedores=top_vendedores()

    )





# ==========================================
# DATOS DINÁMICOS DEL DASHBOARD
# ==========================================


@dashboard.route("/dashboard/datos")
def dashboard_datos():


    periodo = request.args.get(

        "periodo",

        "mes"

    )


    datos = ventas_por_periodo(
        periodo
    )



    return jsonify({

        "ventas": datos

    })


# ==========================================
# GENERAR GRÁFICOS PARA PDF
# ==========================================


def generar_graficos_pdf():


    carpeta = "static/reportes"


    os.makedirs(
        carpeta,
        exist_ok=True
    )



    # ======================================
    # GRÁFICO VENTAS ÚLTIMOS 7 DÍAS
    # ======================================


    ventas = ventas_ultimos_7_dias()



    if ventas:


        fechas = [

            v[0]

            for v in ventas

        ]


        valores = [

            float(v[1])

            for v in ventas

        ]



        plt.figure(
            figsize=(8,4)
        )


        plt.plot(

            fechas,

            valores,

            marker="o",

            linewidth=2

        )


        plt.title(
            "Ventas últimos 7 días"
        )


        plt.xlabel(
            "Fecha"
        )


        plt.ylabel(
            "Monto vendido"
        )


        plt.xticks(
            rotation=30
        )


        plt.grid(
            True
        )


        plt.tight_layout()



        plt.savefig(

            os.path.join(

                carpeta,

                "ventas.png"

            ),

            dpi=200

        )



        plt.close()




    # ======================================
    # GRÁFICO PRODUCTOS POR CATEGORÍA
    # ======================================


    categorias = productos_por_categoria()



    if categorias:


        nombres = [

            c[0]

            for c in categorias

        ]



        cantidades = [

            c[1]

            for c in categorias

        ]



        plt.figure(
            figsize=(8,4)
        )



        plt.bar(

            nombres,

            cantidades

        )



        plt.title(
            "Productos por categoría"
        )


        plt.xlabel(
            "Categoría"
        )


        plt.ylabel(
            "Cantidad"
        )



        plt.xticks(

            rotation=30

        )


        plt.tight_layout()



        plt.savefig(

            os.path.join(

                carpeta,

                "categorias.png"

            ),

            dpi=200

        )


        plt.close()




    # ======================================
    # GRÁFICO MOVIMIENTOS INVENTARIO
    # ======================================


    movimientos = movimientos_tipo()



    if movimientos:


        tipos = [

            m[0]

            for m in movimientos

        ]



        cantidades = [

            m[1]

            for m in movimientos

        ]



        plt.figure(
            figsize=(6,6)
        )



        plt.pie(

            cantidades,

            labels=tipos,

            autopct="%1.1f%%",

            startangle=90

        )



        plt.title(
            "Movimientos de Inventario"
        )


        plt.tight_layout()



        plt.savefig(

            os.path.join(

                carpeta,

                "movimientos.png"

            ),

            dpi=200

        )



        plt.close()



    return carpeta






# ==========================================
# ENCABEZADO Y PIE DEL PDF
# ==========================================


def encabezado_pie(
    canvas,
    doc
):


    canvas.saveState()



    ancho, alto = letter




    # ======================================
    # LÍNEA SUPERIOR
    # ======================================


    canvas.setStrokeColor(

        colors.HexColor(
            "#0d6efd"
        )

    )


    canvas.setLineWidth(
        2
    )


    canvas.line(

        40,

        alto - 45,

        ancho - 40,

        alto - 45

    )





    # ======================================
    # LOGO
    # ======================================


    logo = "static/img/logo.png"



    if os.path.exists(logo):


        canvas.drawImage(

            logo,

            45,

            alto - 75,

            width=30,

            height=30,

            preserveAspectRatio=True,

            mask="auto"

        )




    # ======================================
    # TITULO
    # ======================================


    canvas.setFont(

        "Helvetica-Bold",

        16

    )



    canvas.drawString(

        85,

        alto - 60,

        "InventarioPro"

    )




    # ======================================
    # FECHA
    # ======================================


    canvas.setFont(

        "Helvetica",

        9

    )


    canvas.drawRightString(

        ancho - 45,

        alto - 60,

        datetime.now().strftime(

            "%d/%m/%Y %H:%M"

        )

    )





    # ======================================
    # LINEA INFERIOR
    # ======================================


    canvas.setStrokeColor(
        colors.grey
    )


    canvas.setLineWidth(
        1
    )


    canvas.line(

        40,

        40,

        ancho - 40,

        40

    )





    # ======================================
    # TEXTO PIE
    # ======================================


    canvas.setFont(

        "Helvetica",

        9

    )



    canvas.drawString(

        45,

        25,

        "Reporte generado automáticamente por InventarioPro"

    )




    canvas.drawRightString(

        ancho - 45,

        25,

        f"Página {doc.page}"

    )




    canvas.restoreState()


@dashboard.route("/dashboard/pdf")
def exportar_dashboard_pdf():


    if "usuario" not in session:

        return redirect("/")



    carpeta = "static/reportes"


    os.makedirs(

        carpeta,

        exist_ok=True

    )



    archivo_pdf = os.path.join(

        carpeta,

        "Dashboard_InventarioPro.pdf"

    )



    # ======================================
    # GENERAR GRÁFICOS
    # ======================================


    generar_graficos_pdf()



    estilos = getSampleStyleSheet()



    doc = SimpleDocTemplate(

        archivo_pdf,

        pagesize=letter,

        rightMargin=40,

        leftMargin=40,

        topMargin=80,

        bottomMargin=60

    )



    contenido = []





    # ======================================
    # PORTADA
    # ======================================


    logo = "static/img/logo.png"



    if os.path.exists(logo):


        contenido.append(

            Image(

                logo,

                width=180,

                height=120

            )

        )



    contenido.append(

        Spacer(

            1,

            30

        )

    )




    contenido.append(

        Paragraph(

            "<font size=28><b>InventarioPro</b></font>",

            estilos["Title"]

        )

    )




    contenido.append(

        Paragraph(

            "Reporte Ejecutivo del Dashboard",

            estilos["Heading2"]

        )

    )




    contenido.append(

        Spacer(

            1,

            40

        )

    )




    contenido.append(

        Paragraph(

            f"""
            <b>Fecha generación:</b>
            {datetime.now().strftime("%d/%m/%Y %H:%M")}
            """,

            estilos["Normal"]

        )

    )




    contenido.append(

        Paragraph(

            f"""
            <b>Usuario:</b>
            session["usuario"]
            """,

            estilos["Normal"]

        )

    )




    contenido.append(

        Paragraph(

            f"""
            <b>Rol:</b>
            session["rol"]
            """,

            estilos["Normal"]

        )

    )




    contenido.append(

        Spacer(

            1,

            40

        )

    )




    contenido.append(

        Paragraph(

            """
            Informe ejecutivo del sistema InventarioPro.
            Este reporte contiene indicadores de ventas,
            inventario, productos, clientes y movimientos
            comerciales.
            """,

            estilos["BodyText"]

        )

    )




    contenido.append(

        PageBreak()

    )





    # ======================================
    # RESUMEN EJECUTIVO
    # ======================================


    contenido.append(

        Paragraph(

            "Resumen Ejecutivo",

            estilos["Heading1"]

        )

    )



    datos = obtener_estadisticas()



    resumen = [

        [

            "Indicador",

            "Resultado"

        ],


        [

            "Productos registrados",

            str(datos["productos"])

        ],


        [

            "Clientes",

            str(total_clientes())

        ],


        [

            "Ventas acumuladas",

            str(total_ventas())

        ],


        [

            "Productos agotados",

            str(productos_agotados())

        ]

    ]




    tabla = Table(

        resumen,

        colWidths=[220,180]

    )



    tabla.setStyle(

        TableStyle([


            (

                "BACKGROUND",

                (0,0),

                (-1,0),

                colors.HexColor("#0d6efd")

            ),



            (

                "TEXTCOLOR",

                (0,0),

                (-1,0),

                colors.white

            ),



            (

                "FONTNAME",

                (0,0),

                (-1,0),

                "Helvetica-Bold"

            ),



            (

                "GRID",

                (0,0),

                (-1,-1),

                0.5,

                colors.grey

            ),



            (

                "ALIGN",

                (0,0),

                (-1,-1),

                "CENTER"

            )



        ])

    )



    contenido.append(tabla)



    contenido.append(

        Spacer(

            1,

            30

        )

    )





    # ======================================
    # KPIs
    # ======================================


    contenido.append(

        Paragraph(

            "Indicadores Clave (KPIs)",

            estilos["Heading1"]

        )

    )




    ganancias = ganancias_por_mes()



    ganancia_total = sum(

        fila[3]

        for fila in ganancias

        if fila[3] is not None

    )




    kpis = [

        [

            "Indicador",

            "Valor"

        ],


        [

            "Ventas del mes",

            f"$ {ventas_mes():,.0f}"

        ],


        [

            "Compras del mes",

            f"$ {compras_mes():,.0f}"

        ],


        [

            "Valor inventario",

            f"$ {valor_inventario():,.0f}"

        ],


        [

            "Ganancias",

            f"$ {ganancia_total:,.0f}"

        ],


        [

            "Stock agotado",

            str(productos_agotados())

        ]

    ]




    tabla = Table(

        kpis,

        colWidths=[220,180]

    )



    tabla.setStyle(

        TableStyle([


            (

                "BACKGROUND",

                (0,0),

                (-1,0),

                colors.HexColor("#198754")

            ),


            (

                "TEXTCOLOR",

                (0,0),

                (-1,0),

                colors.white

            ),


            (

                "FONTNAME",

                (0,0),

                (-1,0),

                "Helvetica-Bold"

            ),


            (

                "GRID",

                (0,0),

                (-1,-1),

                0.5,

                colors.grey

            ),


            (

                "ALIGN",

                (0,0),

                (-1,-1),

                "CENTER"

            )

        ])

    )



    contenido.append(tabla)


    # ======================================
    # ÚLTIMAS VENTAS
    # ======================================


    contenido.append(

        Spacer(
            1,
            25
        )

    )


    contenido.append(

        Paragraph(

            "Últimas ventas",

            estilos["Heading2"]

        )

    )



    ventas = ultimas_ventas()



    tabla_ventas = [

        [

            "ID",

            "Cliente",

            "Total",

            "Fecha"

        ]

    ]

    for venta in ventas:

        cliente = (
        venta["cliente"]
        if "cliente" in venta.keys()
        and venta["cliente"]
        else "Consumidor Final"
    )


    tabla_ventas.append(

        [

            str(venta["id"]),

            cliente,

            f"$ {venta['total']:,.0f}",

            venta["fecha"]

        ]

    )




    tabla = Table(

        tabla_ventas,

        colWidths=[50,200,100,120]

    )




    tabla.setStyle(

        TableStyle([


            (

                "BACKGROUND",

                (0,0),

                (-1,0),

                colors.HexColor("#198754")

            ),



            (

                "TEXTCOLOR",

                (0,0),

                (-1,0),

                colors.white

            ),



            (

                "FONTNAME",

                (0,0),

                (-1,0),

                "Helvetica-Bold"

            ),



            (

                "GRID",

                (0,0),

                (-1,-1),

                0.5,

                colors.grey

            ),



            (

                "ALIGN",

                (0,0),

                (-1,-1),

                "CENTER"

            )

        ])

    )



    contenido.append(tabla)






    # ======================================
    # STOCK BAJO
    # ======================================



    contenido.append(

        Spacer(
            1,
            25
        )

    )



    contenido.append(

        Paragraph(

            "Productos con stock bajo",

            estilos["Heading2"]

        )

    )



    stock = productos_stock_bajo()

    tabla_stock = [

        [

            "Producto",

            "Stock"

        ]

    ]



    for producto in stock:


        tabla_stock.append(

            [

                producto["nombre"],

                str(producto["stock"])

            ]

        )





    tabla = Table(

        tabla_stock,

        colWidths=[360,100]

    )




    tabla.setStyle(

        TableStyle([


            (

                "BACKGROUND",

                (0,0),

                (-1,0),

                colors.HexColor("#dc3545")

            ),


            (

                "TEXTCOLOR",

                (0,0),

                (-1,0),

                colors.white

            ),



            (

                "FONTNAME",

                (0,0),

                (-1,0),

                "Helvetica-Bold"

            ),



            (

                "GRID",

                (0,0),

                (-1,-1),

                0.5,

                colors.grey

            ),



            (

                "ALIGN",

                (0,0),

                (-1,-1),

                "CENTER"

            )

        ])

    )



    contenido.append(tabla)







    # ======================================
    # TOP PRODUCTOS
    # ======================================



    contenido.append(

        Spacer(
            1,
            25
        )

    )



    contenido.append(

        Paragraph(

            "Top productos más vendidos",

            estilos["Heading2"]

        )

    )



    productos = productos_mas_vendidos()

    tabla_productos = [

        [

            "Producto",

            "Cantidad"

        ]

    ]




    for producto in productos:


        tabla_productos.append(

            [

                producto["nombre"],

                str(producto["cantidad"])

            ]

        )





    tabla = Table(

        tabla_productos,

        colWidths=[360,100]

    )




    tabla.setStyle(

        TableStyle([


            (

                "BACKGROUND",

                (0,0),

                (-1,0),

                colors.HexColor("#0d6efd")

            ),



            (

                "TEXTCOLOR",

                (0,0),

                (-1,0),

                colors.white

            ),



            (

                "FONTNAME",

                (0,0),

                (-1,0),

                "Helvetica-Bold"

            ),



            (

                "GRID",

                (0,0),

                (-1,-1),

                0.5,

                colors.grey

            ),



            (

                "ALIGN",

                (0,0),

                (-1,-1),

                "CENTER"

            )

        ])

    )



    contenido.append(tabla)







    # ======================================
    # TOP VENDEDORES
    # ======================================



    contenido.append(

        Spacer(
            1,
            25
        )

    )



    contenido.append(

        Paragraph(

            "Top vendedores",

            estilos["Heading2"]

        )

    )



    vendedores = top_vendedores()

    tabla_vendedores = [

    [
        "Vendedor",
        "Ventas realizadas"
    ]

]



    for vendedor in vendedores:

        tabla_vendedores.append(

        [

            vendedor["usuario"],

            str(vendedor["vendido"])

        ]

    )





    tabla = Table(

    tabla_vendedores,

    colWidths=[250,150]

    )




    tabla.setStyle(

        TableStyle([


            (

                "BACKGROUND",

                (0,0),

                (-1,0),

                colors.HexColor("#6f42c1")

            ),



            (

                "TEXTCOLOR",

                (0,0),

                (-1,0),

                colors.white

            ),



            (

                "FONTNAME",

                (0,0),

                (-1,0),

                "Helvetica-Bold"

            ),



            (

                "GRID",

                (0,0),

                (-1,-1),

                0.5,

                colors.grey

            ),



            (

                "ALIGN",

                (0,0),

                (-1,-1),

                "CENTER"

            )

        ])

    )



    contenido.append(tabla)


    # ======================================
    # GRÁFICOS DEL DASHBOARD
    # ======================================


    contenido.append(

        PageBreak()

    )



    contenido.append(

        Paragraph(

            "Gráficos del Dashboard",

            estilos["Heading1"]

        )

    )



    graficos = [

        (

            "Ventas últimos 7 días",

            "static/reportes/ventas.png"

        ),

        (

            "Productos por categoría",

            "static/reportes/categorias.png"

        ),

        (

            "Movimientos de inventario",

            "static/reportes/movimientos.png"

        )

    ]




    for titulo, ruta in graficos:



        if os.path.exists(ruta):


            contenido.append(

                Paragraph(

                    titulo,

                    estilos["Heading2"]

                )

            )



            contenido.append(

                Spacer(

                    1,

                    15

                )

            )



            contenido.append(

                Image(

                    ruta,

                    width=350,

                    height=180

                )

            )



            contenido.append(

                Spacer(

                    1,

                    25

                )

            )





    # ======================================
    # CONSTRUIR PDF
    # ======================================



    doc.build(

        contenido,

        onFirstPage=encabezado_pie,

        onLaterPages=encabezado_pie

    )




    # ======================================
    # DESCARGAR PDF
    # ======================================



    return send_file(

        archivo_pdf,

        as_attachment=True,

        download_name="Dashboard_InventarioPro.pdf"

    )
    