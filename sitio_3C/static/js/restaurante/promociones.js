document.addEventListener('DOMContentLoaded', function () {
    // --- 1. Referencias ---
    const openModalBtn = document.getElementById('openModal');
    const modal = document.getElementById('addItemModal');
    const closeBtn = modal.querySelector('.close');
    const cancelBtn = modal.querySelector('.btn-cancelar');
    const saveBtn = modal.querySelector('.btn-guardar');
    const form = document.getElementById('addItemForm');
    const menuGrid = document.getElementById('menu-grid');

    // Inputs del formulario
    const tipoSelect = document.getElementById('tipo-Promocion');
    const comboFields = document.getElementById('combo-fields');
    const discountFields = document.getElementById('discount-fields');
    const selectedDishInput = document.getElementById('selected-dish-id');
    const discountValueInput = document.getElementById('discount-value');
    const comboValueSelect = document.getElementById('combo-value');

    // Estado
    let isSelectionMode = false;
    let selectedDishData = null;
    let originalCardHTMLs = [];

    // NUEVO: Estado para el control de la modificación
    let isEditMode = false;
    let editingCard = null;

    // --- 2. Iniciar Selección (Cambiar apariencia de tarjetas Y botón) ---
    openModalBtn.addEventListener('click', function() {
        if (isSelectionMode) return;

        isSelectionMode = true;

        // CAMBIO: Activar clase para cambiar el contenido del botón
        openModalBtn.classList.add('in-selection-mode');

        const dishCards = document.querySelectorAll('.dish-card');
        originalCardHTMLs = [];

        dishCards.forEach((card, index) => {
            // 1. Guardar HTML original
            originalCardHTMLs.push(card.innerHTML);

            // 2. Extraer datos
            const name = card.querySelector('h3').textContent;
            const priceText = card.querySelector('.price').textContent;
            const priceValue = priceText.replace('$', '').replace(',', '');
            const id = card.getAttribute('data-dish-id') || (index + 1);
            const imgSrc = card.querySelector('img').src;

            // 3. REEMPLAZAR contenido (Prototipo 2)
            card.innerHTML = `
            <div style="height: 180px; overflow: hidden;">
            <img src="${imgSrc}" alt="Platillo" style="width: 100%; height: 100%; object-fit: cover;">
            </div>
            <div style="padding: 15px; text-align: center;">
            <h3 style="font-size: 16px; margin-bottom: 5px;">${name}</h3>
            <p style="font-weight: bold; color: #4a90e2;">$${priceValue}</p>
            </div>
            `;

            // 4. Guardar precio real en atributo data
            card.setAttribute('data-price-real', priceValue);

            card.classList.add('selectable');
            card.style.cursor = 'pointer';
        });
    });

    // --- 3. Selección de Platillo (Solo al CREAR) ---
    menuGrid.addEventListener('click', function(e) {
        if (!isSelectionMode) return;

        const card = e.target.closest('.dish-card');

        if (card) {
            document.querySelectorAll('.dish-card').forEach(c => c.classList.remove('selected-for-promotion'));
            card.classList.add('selected-for-promotion');

            const name = card.querySelector('h3').textContent;
            const id = card.getAttribute('data-dish-id');
            const imgSrc = card.querySelector('img').src;
            const priceReal = card.getAttribute('data-price-real');

            selectedDishData = {
                id: id,
                name: name,
                img: imgSrc,
                price: `$${parseFloat(priceReal).toFixed(2)}`,
                              priceValue: parseFloat(priceReal)
            };

            openModalForPromotion();
        }
    });

    // --- 4. Modal y Formulario ---
    function openModalForPromotion() {
        form.reset();
        if (selectedDishInput) selectedDishInput.value = selectedDishData.id;

        // Ajustar interfaz del modal para el modo de creación por defecto
        isEditMode = false;
        saveBtn.textContent = 'Crear';

        modal.style.display = 'flex';
        togglePromotionFields('combo');
    }

    if (tipoSelect) {
        tipoSelect.addEventListener('change', function(e) {
            togglePromotionFields(e.target.value);
        });
    }

    function togglePromotionFields(type) {
        if (type === 'combo') {
            if (comboFields) comboFields.style.display = 'block';
            if (discountFields) discountFields.style.display = 'none';
        } else {
            if (comboFields) comboFields.style.display = 'none';
            if (discountFields) discountFields.style.display = 'block';
        }
    }

    // --- 5. Guardar (Creación o Modificación Directa) ---
    if (saveBtn) {
        saveBtn.addEventListener('click', function(e) {
            e.preventDefault();

            const tipo = tipoSelect.value;
            let valorPromo = '';

            // Validaciones según el tipo de promoción
            if (tipo === 'combo') {
                valorPromo = comboValueSelect.value;
            } else {
                const pct = discountValueInput.value;
                if (!pct || pct < 1 || pct > 100) {
                    alert('Ingresa un porcentaje válido (1-100).');
                    return;
                }
                valorPromo = `${pct}%`;
            }

            // NUEVO: Bifurcación basada en si estamos editando o creando
            if (isEditMode) {
                // ACTUALIZAR TARJETA EXISTENTE
                if (!editingCard) return;

                // 1. Actualizar el texto del tipo de promoción
                const promoTextElement = editingCard.querySelector('p');
                if (promoTextElement) {
                    promoTextElement.textContent = `${tipo.toUpperCase()}: ${valorPromo}`;
                }

                // 2. Actualizar el contenedor de precios dinámicamente si es Descuento o regresarlo a Combo
                // Buscamos si ya tiene un contenedor de precios o la clase clásica .price
                let priceContainer = editingCard.querySelector('.price-container');
                let singlePrice = editingCard.querySelector('.price');

                // Extraer precio original base guardado en el atributo de la tarjeta
                const precioOriginalTexto = editingCard.getAttribute('data-price');
                const precioOriginalNum = parseFloat(precioOriginalTexto.replace('$', ''));

                if (tipo === 'descuento') {
                    const porcentaje = parseFloat(valorPromo.replace('%', ''));
                    const precioConDescuento = precioOriginalNum * (1 - (porcentaje / 100));

                    const nuevoHTMLPrecios = `
                    <del style="color: #666; font-size: 14px;">$${precioOriginalNum.toFixed(2)}</del>
                    <div class="price" style="font-weight: bold; font-size: 20px; color: #000; margin-top: 5px;">
                    $${precioConDescuento.toFixed(2)}
                    </div>
                    `;

                    if (priceContainer) {
                        priceContainer.innerHTML = nuevoHTMLPrecios;
                    } else if (singlePrice) {
                        // Si antes era combo, transformamos el contenedor estático al nuevo formato
                        const container = document.createElement('div');
                        container.classList.add('price-container');
                        container.style.cssText = "text-align: center; margin-top: 10px;";
                        container.innerHTML = nuevoHTMLPrecios;
                        singlePrice.replaceWith(container);
                    }
                } else {
                    // Si se cambió de Descuento a Combo, reestablecemos el precio único normal
                    if (priceContainer) {
                        const normalPriceDiv = document.createElement('div');
                        normalPriceDiv.classList.add('price');
                        normalPriceDiv.textContent = precioOriginalTexto;
                        priceContainer.replaceWith(normalPriceDiv);
                    } else if (singlePrice) {
                        singlePrice.textContent = precioOriginalTexto;
                    }
                }

                alert('La promoción se ha modificado con éxito');
            }else {
                // CREAR NUEVA TARJETA
                if (!selectedDishData) return;
                crearPromocion(selectedDishData, tipo, valorPromo);
                alert('La promoción se ha creado con éxito');
            }

            closeModal();
            resetSelectionMode();
        });
    }

    // --- 6. Crear Tarjeta Final ---
    function crearPromocion(dish, tipo, valor) {
        const newCard = document.createElement('div');
        newCard.classList.add('card');
        newCard.setAttribute('data-dish-id', dish.id);
        newCard.setAttribute('data-price', dish.price);

        let priceHTML = '';

        if (tipo.toLowerCase() === 'descuento') {
            // 1. Obtener el precio numérico original (ej: "$120.00" -> 120)
            const precioOriginal = dish.priceValue;

            // 2. Extraer el porcentaje (ej: "20%" -> 20)
            const porcentaje = parseFloat(valor.replace('%', ''));

            // 3. Calcular el nuevo precio con descuento aplicado
            const precioConDescuento = precioOriginal * (1 - (porcentaje / 100));

            // 4. Formato como en tu imagen: Precio original tachado arriba y el nuevo abajo en negrita
            priceHTML = `
            <div class="price-container" style="text-align: center; margin-top: 10px;">
            <del style="color: #666; font-size: 14px;">$${precioOriginal.toFixed(2)}</del>
            <div class="price" style="font-weight: bold; font-size: 20px; color: #000; margin-top: 5px;">
            $${precioConDescuento.toFixed(2)}
            </div>
            </div>
            `;
        } else {
            // Si es COMBO, mantiene consistencia en el formato del precio
            priceHTML = `<div class="price">${dish.price}</div>`;
        }

        newCard.innerHTML = `
        <img src="${dish.img}" alt="${dish.name}">
        <h3>${dish.name}</h3>
        <p style="color: #007bff; font-weight: bold; padding: 0 15px; text-align: center;">
        ${tipo.toUpperCase()}: ${valor}
        </p>
        ${priceHTML}
        <div class="context-menu">
        <div class="menu-option modificar-btn">Modificar</div>
        <div class="menu-option borrar-btn">Eliminar</div>
        </div>
        `;

        menuGrid.insertBefore(newCard, openModalBtn.nextSibling);
    }

    // --- 7. RESTAURAR ESTADO ---
    function resetSelectionMode() {
        isSelectionMode = false;
        selectedDishData = null;
        editingCard = null; // Limpiar referencia de edición
        isEditMode = false;
        openModalBtn.classList.remove('in-selection-mode');

        const dishCards = document.querySelectorAll('.dish-card');

        dishCards.forEach((card, index) => {
            if (originalCardHTMLs[index]) {
                card.innerHTML = originalCardHTMLs[index];
            }
            card.classList.remove('selectable', 'selected-for-promotion');
            card.style.cursor = 'default';
        });

        originalCardHTMLs = [];
    }

    // --- Utilidades ---
    function closeModal() {
        modal.style.display = 'none';
        form.reset();
    }

    // --- Eventos de Cierre ---
    if (closeBtn) closeBtn.addEventListener('click', () => { resetSelectionMode(); closeModal(); });
    if (cancelBtn) cancelBtn.addEventListener('click', () => { resetSelectionMode(); closeModal(); });
    window.addEventListener('click', (e) => {
        if (e.target === modal) { resetSelectionMode(); closeModal(); }
    });

    // --- 8. Eventos de Modificar/Eliminar (Context Menus) ---
    menuGrid.addEventListener('click', function(e) {
        if (isSelectionMode) return;
        const card = e.target.closest('.card');
        if (!card) return;

        // ACCIÓN: ELIMINAR
        if (e.target.classList.contains('borrar-btn')) {
            if (confirm('¿Eliminar esta promoción?')) {
                card.remove();
                alert('La promoción se ha eliminado');
            }
        }

        // ACCIÓN: MODIFICAR (NUEVO)
        if (e.target.classList.contains('modificar-btn')) {
            isEditMode = true;
            editingCard = card; // Guardamos la referencia de la tarjeta que vamos a mutar

            // Extraer los datos actuales de la tarjeta creada
            const promoText = card.querySelector('p').textContent.trim(); // Ej: "COMBO: 2x1" o "DESCUENTO: 15%"
            const [tipoActual, valorActual] = promoText.split(': ');

            // Rellenar el ID del platillo en el formulario
            if (selectedDishInput) selectedDishInput.value = card.getAttribute('data-dish-id');

            // Ajustar el formulario según el tipo actual de promoción
            if (tipoActual.toLowerCase() === 'combo') {
                tipoSelect.value = 'combo';
                togglePromotionFields('combo');
                comboValueSelect.value = valorActual;
            } else {
                tipoSelect.value = 'descuento';
                togglePromotionFields('descuento');
                // Limpiar el símbolo '%' para dejar sólo el número en el input
                discountValueInput.value = valorActual.replace('%', '');
            }

            // Cambiar dinámicamente el texto del botón del modal
            saveBtn.textContent = 'Aplicar';

            // Mostrar el modal en pantalla
            modal.style.display = 'flex';
        }
    });
});
