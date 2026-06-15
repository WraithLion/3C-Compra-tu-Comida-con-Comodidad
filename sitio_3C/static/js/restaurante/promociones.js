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

    // Referencias de Imagen
    const imagePreview = document.getElementById('promo-image-preview');
    const imageUploadText = document.getElementById('image-upload-text');
    const imageFileInput = document.getElementById('image-file-input');
    const imageUploadContainer = document.getElementById('imageUpload');

    // Estado
    let isSelectionMode = false;
    let selectedDishData = null;
    let originalCardHTMLs = [];
    let isEditMode = false;
    let editingCard = null;
    let newImageFile = null;

    // --- 2. Iniciar Selección (Modo Crear) ---
    if (openModalBtn) {
        openModalBtn.addEventListener('click', function() {
            if (isSelectionMode) return;

            isSelectionMode = true;
            openModalBtn.classList.add('in-selection-mode');

            const dishCards = document.querySelectorAll('.dish-card');
            originalCardHTMLs = [];

            dishCards.forEach((card, index) => {
                originalCardHTMLs.push(card.innerHTML);

                const h3Element = card.querySelector('h3');
                const priceElement = card.querySelector('.price');
                const imgElement = card.querySelector('img');

                const name = h3Element ? h3Element.textContent : 'Platillo sin nombre';
                const priceText = priceElement ? priceElement.textContent : '$0';
                const priceValue = priceText.replace('$', '').replace(',', '').trim();
                const id = card.getAttribute('data-dish-id') || `TEMP-${index + 1}`;
                const imgSrc = imgElement ? imgElement.src : '/static/restaurante/placeholder-icon.png';

                card.innerHTML = `
                <div style="height: 180px; overflow: hidden;">
                <img src="${imgSrc}" alt="Platillo" style="width: 100%; height: 100%; object-fit: cover;">
                </div>
                <div style="padding: 15px; text-align: center;">
                <h3 style="font-size: 16px; margin-bottom: 5px;">${name}</h3>
                <p style="font-weight: bold; color: #4a90e2;">$${parseFloat(priceValue).toFixed(2)}</p>
                </div>
                `;

                card.setAttribute('data-price-real', priceValue);
                card.classList.add('selectable', 'mostrar-seleccion');
                card.style.cursor = 'pointer';
            });
        });
    }

    // --- 3. Selección de Platillo ---
    if (menuGrid) {
        menuGrid.addEventListener('click', function(e) {
            if (!isSelectionMode) return;

            const card = e.target.closest('.dish-card');

            if (card) {
                document.querySelectorAll('.dish-card').forEach(c => c.classList.remove('selected-for-promotion'));
                card.classList.add('selected-for-promotion');

                const name = card.querySelector('h3').textContent;
                const id = card.getAttribute('data-dish-id');
                const imgElement = card.querySelector('img');
                const imgSrc = imgElement ? imgElement.src : '';
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
    }

    // --- 4. Funciones del Modal ---

    // Abrir modal para CREAR
    function openModalForPromotion() {
        form.reset();
        if (selectedDishInput) selectedDishInput.value = selectedDishData.id;

        // Configurar imagen para CREACIÓN (Placeholder y activado)
        if (imagePreview) {
            imagePreview.src = selectedDishData.img; // Usamos la imagen del platillo seleccionado
        }
        if (imageUploadText) imageUploadText.textContent = "";
        if (imageUploadContainer) imageUploadContainer.style.cursor = 'default'; // Activar clic

        newImageFile = null;
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

    // --- 5. Manejo de Imagen (Clic y Cambio) ---



    // Cuando el usuario selecciona un archivo nuevo
    if (imageFileInput) {
        imageFileInput.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                newImageFile = file;
                const reader = new FileReader();
                reader.onload = function(event) {
                    if (imagePreview) {
                        imagePreview.src = event.target.result;
                    }
                    if (imageUploadText) {
                        imageUploadText.textContent = "";
                    }
                };
                reader.readAsDataURL(file);
            }
        });
    }

    // --- 6. Guardar (Crear o Modificar) ---
    if (saveBtn) {
        saveBtn.addEventListener('click', function (e) {
            e.preventDefault();

            const tipo = tipoSelect.value;
            let valorPromo = '';

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

            if (isEditMode) {
                // --- MODO EDICIÓN ---
                if (!editingCard) return;

                const promoId = editingCard.getAttribute('data-current-promo-id');
                if (!promoId) {
                    alert('Error: No se encontró el ID de la promoción.');
                    return;
                }

                const updatedData = {
                    tipo: tipo,
                    valor: valorPromo
                };

                fetch(`/restaurante/promociones/${promoId}/modificar/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken')
                    },
                    body: JSON.stringify(updatedData)
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        alert(data.message || 'La promoción se ha modificado con éxito');
                        location.reload();
                    } else {
                        alert(data.error || 'Error al modificar la promoción.');
                    }
                })
                .catch(error => {
                    console.error('Error de red:', error);
                    alert('Error de conexión al servidor.');
                });

            } else {
                // --- MODO CREACIÓN ---
                if (!selectedDishData) return;

                const dataToSend = {
                    platillo_id: selectedDishData.id,
                    tipo: tipo,
                    valor: valorPromo
                };

                fetch('/restaurante/promociones/agregar/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken')
                    },
                    body: JSON.stringify(dataToSend)
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        alert(data.message || 'La promoción se ha creado con éxito');
                        location.reload();
                    } else {
                        alert(data.error || 'Ocurrió un error al procesar la solicitud.');
                    }
                })
                .catch(error => {
                    console.error('Error de red:', error);
                    alert('Error de conexión al servidor.');
                });
            }

            closeModal();
            resetSelectionMode();
        });
    }

    // --- 7. Resetear y Cerrar ---
    function resetSelectionMode() {
        isSelectionMode = false;
        selectedDishData = null;
        editingCard = null;
        isEditMode = false;

        if (openModalBtn) openModalBtn.classList.remove('in-selection-mode');

        const dishCards = document.querySelectorAll('.dish-card');
        dishCards.forEach((card, index) => {
            if (originalCardHTMLs[index]) {
                card.innerHTML = originalCardHTMLs[index];
            }
            card.classList.remove('selectable', 'selected-for-promotion');
            card.style.cursor = 'default';
            card.classList.remove('mostrar-seleccion');
        });

        originalCardHTMLs = [];
    }

    function closeModal() {
        if (modal) modal.style.display = 'none';
        if (form) form.reset();

        // Resetear imagen y estados visuales
        if (imagePreview) {
            imagePreview.src = '/static/restaurante/placeholder-icon.png';
        }
        if (imageUploadText) imageUploadText.textContent = "";
        if (imageUploadContainer) imageUploadContainer.style.cursor = '';
        if (imageFileInput) imageFileInput.value = '';

        newImageFile = null;
    }

    // Eventos de Cierre
    if (closeBtn) closeBtn.addEventListener('click', () => { resetSelectionMode(); closeModal(); });
    if (cancelBtn) cancelBtn.addEventListener('click', () => { resetSelectionMode(); closeModal(); });
    window.addEventListener('click', (e) => {
        if (e.target === modal) { resetSelectionMode(); closeModal(); }
    });

    // --- 8. Eventos de Modificar/Eliminar (Context Menus) ---
    if (menuGrid) {
        menuGrid.addEventListener('click', function(e) {
            if (isSelectionMode) return;

            const card = e.target.closest('.card');
            if (!card || card.classList.contains('add-card') || card.classList.contains('dish-card')) return;

            // ACCIÓN: ELIMINAR
            if (e.target.classList.contains('borrar-btn')) {
                if (confirm('¿Eliminar esta promoción?')) {
                    const promoId = card.getAttribute('data-promo-id');

                    fetch('/restaurante/promociones/eliminar/', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': getCookie('csrftoken')
                        },
                        body: JSON.stringify({ promo_id: promoId })
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            card.remove();
                            alert(data.message);
                            location.reload();
                        } else {
                            alert('Error: ' + data.error);
                        }
                    })
                    .catch(error => {
                        console.error('Error de red:', error);
                        alert('Hubo un error de conexión al intentar eliminar.');
                    });
                }
            }

            // ACCIÓN: MODIFICAR
            if (e.target.classList.contains('modificar-btn')) {
                isEditMode = true;
                editingCard = card;
                newImageFile = null;

                const promoId = card.getAttribute('data-promo-id');
                editingCard.setAttribute('data-current-promo-id', promoId);

                // 1. Cargar imagen actual (SOLO LECTURA)
                const currentImgElement = card.querySelector('img');
                if (currentImgElement && imagePreview) {
                    imagePreview.src = currentImgElement.src;
                    // Forzar estilos en línea si el CSS no está surtiendo efecto
                    imagePreview.style.width = '100%';
                    imagePreview.style.height = '100%';
                    imagePreview.style.objectFit = 'cover'; // O 'contain' si prefieres verla completa sin recortes
                    imagePreview.style.objectPosition = 'center';
                }

                // 2. Bloquear interacción visual
                if (imageUploadText) {
                    imageUploadText.textContent = "";
                }
                if (imageUploadContainer) {
                    imageUploadContainer.style.cursor = 'default'; // Cursor normal (no mano)
                }
                if (imageFileInput) imageFileInput.value = '';

                // 3. Rellenar campos
                const promoText = card.querySelector('p').textContent.trim();
                const partes = promoText.split(': ');
                const tipoActual = partes[0] ? partes[0].trim() : 'combo';
                const valorActual = partes[1] ? partes[1].trim() : '';

                if (selectedDishInput) selectedDishInput.value = card.getAttribute('data-dish-id');

                if (tipoActual.toLowerCase() === 'combo') {
                    tipoSelect.value = 'combo';
                    togglePromotionFields('combo');
                    comboValueSelect.value = valorActual;
                } else {
                    tipoSelect.value = 'descuento';
                    togglePromotionFields('descuento');
                    discountValueInput.value = valorActual.replace('%', '');
                }

                saveBtn.textContent = 'Aplicar';
                modal.style.display = 'flex';
            }
        });
    }
});

// --- FUNCIÓN COOKIE ---
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
