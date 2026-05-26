const tarjetas = document.querySelectorAll('.card');
const contenedorRestaurantes = document.getElementById('lista-restaurantes'); // Contenedor de las tarjetas
const contenedorMenu = document.getElementById('menu-detalle');
const tituloMenu = document.getElementById('titulo-menu');
const listaPlatillos = document.getElementById('lista-platillos');

    // Datos de ejemplo con estructura de objetos
    const menus = {
        restaurante1: [
            {
                nombre: "Hamburguesa Clásica",
                precio: 12.00,
                descripcion: "Carne de res, queso, lechuga y tomate.",
                imagen: "img/hamburguesa.jpg" // Asegúrate de que la ruta sea correcta
            },
            {
                nombre: "Papas Fritas",
                precio: 5.00,
                descripcion: "Crujientes papas con sal.",
                imagen: "img/papas.jpg"
            }
        ],
        restaurante2: [
            {
                nombre: "Tacos al Pastor",
                precio: 8.00,
                descripcion: "Tres piezas con piña y cilantro.",
                imagen: "img/tacos.jpg"
            }
        ]
        // ... otros restaurantes
    };

    // ... (selección de elementos del DOM: tarjetas, contenedores, etc.)

    tarjetas.forEach(tarjeta => {
        tarjeta.addEventListener('click', () => {
            const idRestaurante = tarjeta.getAttribute('data-restaurante');
            const nombreRestaurante = tarjeta.querySelector('h3').innerText;
            const platillos = menus[idRestaurante];

            if (platillos) {
                // 1. Ocultar la lista de restaurantes
                contenedorRestaurantes.style.display = 'none';

                // 2. Mostrar el menú
                contenedorMenu.style.display = 'block';
                tituloMenu.innerText = `Menú de ${nombreRestaurante}`;

                // 3. Limpiar el contenedor de platillos
                listaPlatillos.innerHTML = '';

                // 4. Generar las tarjetas usando las clases de tu CSS
                platillos.forEach(platillo => {
                    const card = document.createElement('div');
                    card.className = 'card'; // Usamos la clase 'card' que ya tienes estilizada

                    // Si no hay imagen, usamos la clase 'image-placeholder'
                    const imageContainer = platillo.imagen
                    ? `<img src="${platillo.imagen}" alt="${platillo.nombre}">`
                    : `<div class="image-placeholder"><p>Sin imagen</p></div>`;

                    card.innerHTML = `
                    ${imageContainer}
                    <h3>${platillo.nombre}</h3>
                    <p class="price">$${platillo.precio.toFixed(2)}</p>
                    <p class="descripcion">${platillo.descripcion}</p>
                    <button class="btn-agregar">Agregar al carrito</button>
                    `;

                    listaPlatillos.appendChild(card);
                });
            }
        });
    });
