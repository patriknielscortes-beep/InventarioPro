// ==========================
// BUSCADOR
// ==========================

const buscador = document.getElementById("buscarProducto");

buscador.addEventListener("keyup", function(){

    let texto = buscador.value.toLowerCase();

    document.querySelectorAll(".tarjeta-producto").forEach(card=>{

        let nombre = card.innerText.toLowerCase();

        card.style.display = nombre.includes(texto)
            ? "block"
            : "none";

    });

});



// ==========================
// CARRITO
// ==========================

let carrito = [];



document.querySelectorAll(".agregar").forEach(boton=>{

    boton.addEventListener("click", ()=>{

        let id = boton.dataset.id;

        let nombre = boton.dataset.nombre;

        let precio = parseFloat(boton.dataset.precio);

        let stock = parseInt(boton.dataset.stock);


        let existe = carrito.find(p=>p.id==id);


        if(existe){

            if(existe.cantidad < stock){

                existe.cantidad++;

            }

        }else{

            carrito.push({

                id:id,

                nombre:nombre,

                precio:precio,

                stock:stock,

                cantidad:1

            });

        }


        pintarCarrito();

    });

});



// ==========================
// DIBUJAR CARRITO
// ==========================

function pintarCarrito(){

    let lista = document.getElementById("listaCarrito");

    lista.innerHTML="";


    let total=0;


    carrito.forEach((item,index)=>{

        total += item.precio*item.cantidad;


        lista.innerHTML += `

        <div class="border rounded p-2 mb-2">

            <strong>${item.nombre}</strong>

            <div class="d-flex justify-content-between mt-2">

                <div>

                    <button
                        class="btn btn-sm btn-secondary"
                        onclick="restar(${index})">

                        -

                    </button>


                    <span class="mx-2">

                        ${item.cantidad}

                    </span>


                    <button
                        class="btn btn-sm btn-secondary"
                        onclick="sumar(${index})">

                        +

                    </button>

                </div>


                <strong>

                    $${(item.precio*item.cantidad).toLocaleString("es-CL")}

                </strong>


            </div>


            <button
                class="btn btn-danger btn-sm mt-2"

                onclick="eliminar(${index})">

                <i class="bi bi-trash"></i>

            </button>

        </div>

        `;

    });


    if(carrito.length==0){

        lista.innerHTML=`

        <div class="text-center text-secondary p-5">

            <i class="bi bi-cart display-1"></i>

            <p>No hay productos</p>

        </div>

        `;

    }


    document.getElementById("totalVenta").innerHTML=

        "$"+total.toLocaleString("es-CL");

}



// ==========================
// +
// ==========================

function sumar(i){

    if(carrito[i].cantidad < carrito[i].stock){

        carrito[i].cantidad++;

    }

    pintarCarrito();

}



// ==========================
// -
// ==========================

function restar(i){

    carrito[i].cantidad--;

    if(carrito[i].cantidad<=0){

        carrito.splice(i,1);

    }

    pintarCarrito();

}



// ==========================
// ELIMINAR
// ==========================

function eliminar(i){

    carrito.splice(i,1);

    pintarCarrito();

}