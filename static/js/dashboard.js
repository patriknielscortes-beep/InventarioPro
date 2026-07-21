// ======================================
// DASHBOARD INVENTARIO PRO
// ======================================


// ======================================
// RELOJ
// ======================================

function actualizarReloj() {

    const reloj = document.getElementById("reloj");

    if (reloj) {

        reloj.textContent =
            new Date().toLocaleTimeString("es-CL");

    }

}

actualizarReloj();

setInterval(actualizarReloj, 1000);




// ======================================
// CONTADORES KPI
// ======================================

document.querySelectorAll(".contador").forEach(contador => {


    const objetivo = Number(contador.dataset.valor) || 0;

    let actual = 0;

    const incremento = Math.max(1, objetivo / 80);



    const timer = setInterval(() => {


        actual += incremento;



        if (actual >= objetivo) {

            actual = objetivo;

            clearInterval(timer);

        }



        contador.textContent =
            Math.floor(actual)
            .toLocaleString("es-CL");



    },20);


});






// ======================================
// CONFIGURACIÓN CHART PRO
// ======================================

const opcionesPro = {


    responsive:true,

    maintainAspectRatio:false,


    animation:{

        duration:1200,

        easing:"easeOutQuart"

    },


    plugins:{


        legend:{

            position:"bottom",

            labels:{

                padding:20,

                boxWidth:12

            }

        },


        tooltip:{

            backgroundColor:"#111",

            padding:12

        }


    },


    scales:{


        y:{

            beginAtZero:true

        },


        x:{

            grid:{

                display:false

            }

        }


    }


};





// ======================================
// PRODUCTOS POR CATEGORÍA
// ======================================

const canvasCategorias =
document.getElementById("graficoCategorias");


if(canvasCategorias && categorias.length > 0){


    new Chart(canvasCategorias,{


        type:"bar",


        data:{


            labels:
            categorias.map(c=>c[0]),


            datasets:[{

                label:"Productos",

                data:
                categorias.map(c=>c[1]),

                borderRadius:10

            }]


        },


        options:opcionesPro


    });


}







// ======================================
// MOVIMIENTOS INVENTARIO
// ======================================

const canvasMovimientos =
document.getElementById("graficoMovimientos");



if(canvasMovimientos && movimientos.length > 0){


    new Chart(canvasMovimientos,{


        type:"doughnut",


        data:{


            labels:
            movimientos.map(m=>m[0]),


            datasets:[{


                data:
                movimientos.map(m=>m[1]),


                borderWidth:2


            }]


        },


        options:{


            ...opcionesPro,

            cutout:"65%"


        }


    });


}






// ======================================
// VENTAS ÚLTIMOS 7 DÍAS
// ======================================

const canvasVentas =
document.getElementById("graficoVentas");


let graficoVentas;



if(canvasVentas && ventas7dias.length > 0){


    graficoVentas = new Chart(canvasVentas,{


        type:"line",


        data:{


            labels:
            ventas7dias.map(v=>v[0]),


            datasets:[{

                label:"Ventas $",


                data:
                ventas7dias.map(v=>v[1]),


                tension:0.4,

                fill:true,

                pointRadius:5


            }]


        },


        options:{


            ...opcionesPro,


            scales:{


                y:{


                    ticks:{


                        callback:function(valor){

                            return "$" +
                            valor.toLocaleString("es-CL");

                        }


                    }


                }


            }


        }


    });


}







// ======================================
// VENTAS VS COMPRAS
// ======================================

const canvasComparativo =
document.getElementById("graficoComparativo");



if(canvasComparativo && comparativo.length > 0){


    new Chart(canvasComparativo,{


        type:"bar",


        data:{


            labels:
            comparativo.map(c=>c[0]),


            datasets:[

                {

                    label:"Ventas",

                    data:
                    comparativo.map(c=>c[1]),

                    borderRadius:10

                },


                {

                    label:"Compras",

                    data:
                    comparativo.map(c=>c[2]),

                    borderRadius:10

                }


            ]


        },


        options:opcionesPro


    });


}






// ======================================
// GANANCIAS
// ======================================

const canvasGanancias =
document.getElementById("graficoGanancias");



if(canvasGanancias && ganancias.length > 0){


    new Chart(canvasGanancias,{


        type:"line",


        data:{


            labels:
            ganancias.map(g=>g[0]),


            datasets:[{

                label:"Ganancia",

                data:
                ganancias.map(g=>g[3]),


                tension:0.4,

                fill:true,

                pointRadius:6


            }]


        },


        options:{


            ...opcionesPro,


            scales:{


                y:{


                    ticks:{


                        callback:function(valor){

                            return "$" +
                            valor.toLocaleString("es-CL");

                        }


                    }


                }


            }


        }


    });


}







// ======================================
// FILTRO DE FECHAS
// ======================================

const filtroFecha =
document.getElementById("filtroFecha");



if(filtroFecha){


    filtroFecha.addEventListener(
        "change",
        async function(){


            const periodo =
            this.value;



            const respuesta =
            await fetch(
                `/dashboard/datos?periodo=${periodo}`
            );



            const datos =
            await respuesta.json();



            actualizarGraficoVentas(
                datos.ventas
            );


        }

    );


}




// ======================================
// ACTUALIZAR GRÁFICO VENTAS
// ======================================

function actualizarGraficoVentas(datos){


    if(!graficoVentas){

        return;

    }



    graficoVentas.data.labels =
    datos.map(v=>v[0]);



    graficoVentas.data.datasets[0].data =
    datos.map(v=>v[1]);



    graficoVentas.update();


}