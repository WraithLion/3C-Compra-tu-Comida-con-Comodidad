document.addEventListener('DOMContentLoaded', function () {
  // Elementos del DOM
  const openModal = document.getElementById('openModal');
  const modal = document.getElementById('addItemModal');
  const closeBtn = document.querySelector('.close');
  const cancelBtn = document.querySelector('.btn-cancelar');
  const addBtn = document.querySelector('.btn-guardar');
  const form = document.getElementById('addItemForm');
  const menuGrid = document.querySelector('.menu-grid');
  const imageUpload = document.getElementById('imageUpload');

  // Abrir modal
  openModal.addEventListener('click', () => {
    modal.style.display = 'flex';
  });

  // Cerrar modal con la 'X'
  closeBtn.addEventListener('click', () => {
    modal.style.display = 'none';
    form.reset();
  });

  // Cerrar modal
  closeBtn.onclick = function() {
    modal.style.display = "none";
    form.reset(); // <- Esto ya está limpiando el formulario
  }

  // Cerrar modal con botón Cancelar
  cancelBtn.addEventListener('click', () => {
    modal.style.display = 'none';
    form.reset();
  });

  // Cerrar al hacer clic fuera del contenido
  window.onclick = function(event) {
    if (event.target === modal) {
      modal.style.display = "none";
      form.reset(); // <- Esto ya está limpiando el formulario
    }
  }


  // Funcionalidad para el botón 'Agregar'
  addBtn.addEventListener('click', (e) => {
    e.preventDefault();
    const nombre = document.getElementById('nombre').value;
    const precio = document.getElementById('precio').value;

    if (!nombre || !precio) {
      alert('Por favor, completa todos los campos.');
      return;
    }

    const newCard = document.createElement('div');
    newCard.classList.add('card');
    newCard.innerHTML = `
    <img src="https://via.placeholder.com/150" alt="${nombre}">
    <h3>${nombre}</h3>
    <p>Descripción del platillo</p>
    <div class="price">$${parseFloat(precio).toFixed(2)}</div>
    `;

    menuGrid.appendChild(newCard);

    // Limpia el formulario usando reset() y limpieza manual
    if (form.reset) {
      form.reset();
    }
    // Limpieza forzada por si reset() falla
    document.getElementById('nombre').value = '';
    document.getElementById('precio').value = '';

    // Cierra el modal
    modal.style.display = 'none';

    alert('¡Platillo agregado con éxito!');
  });

  // Simular subida de imagen
  imageUpload.addEventListener('click', () => {
    alert('Funcionalidad de subir imagen no implementada aún.');
  });
});
