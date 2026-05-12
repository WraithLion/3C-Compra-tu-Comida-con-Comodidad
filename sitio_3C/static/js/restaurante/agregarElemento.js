document.addEventListener('DOMContentLoaded', function () {
  // Elementos del DOM
  const openModal = document.getElementById('openModal');
  const modal = document.getElementById('addItemModal');
  const closeBtn = modal.querySelector('.close');
  const cancelBtn = modal.querySelector('.btn-cancelar');
  const saveBtn = modal.querySelector('.btn-guardar');
  const form = document.getElementById('addItemForm');
  const menuGrid = document.querySelector('.menu-grid');
  const imageUpload = document.getElementById('imageUpload');
  const nombre = document.getElementById('nombre').value;
  const precio = document.getElementById('precio').value;
  let editingCard = null;

  // --- Función: Abrir modal para agregar ---
  openModal.addEventListener('click', () => {
    editingCard = null;
    form.reset();
    modal.style.display = 'flex';
  });

  // --- Función: Cerrar modal ---
  function closeModal() {
    modal.style.display = 'none';
    form.reset();
  }

  closeBtn.addEventListener('click', closeModal);
  cancelBtn.addEventListener('click', closeModal);
  window.addEventListener('click', (e) => {
    if (e.target === modal) closeModal();
  });

    // --- Función: Agregar nuevo platillo ---
    function agregarPlatillo() {
      const nombre = document.getElementById('nombre').value;
      const precio = document.getElementById('precio').value;
      const patronPrecio = /^\d{1,3}(\.\d{1,2})?$/;
      let mensajeError = '';

      // Validar nombre
      if (!nombre) {
        mensajeError += 'El campo "Nombre" es necesario.\n';
      }
      if (nombre.length<3){
        mensajeError += 'El campo "Nombre" debe ser un alimento o bebida de mínimo 3 letras. (Ejemplo: Pan, col, sopa, escamoles).\n';
      }
      // Validar precio
      if(!precio){
        mensajeError += 'El campo "Precio" es necesario.\n';
      }

      // Validar precio (existencia y formato)
      if (!patronPrecio.test(precio)){
        mensajeError += 'El campo "Precio" sólo permite números y no deben ser mayores a 3 cifras y 2 decimales.\n';
      }


      // Mostrar alerta si hay errores
      if (mensajeError) {
        alert(mensajeError.trim());
        return;
      }

      const newCard = document.createElement('div');
      newCard.classList.add('card');
      newCard.innerHTML = `
      <img src="https://via.placeholder.com/150" alt="${nombre}">
      <h3>${nombre}</h3>
      <p>Descripción del platillo</p>
      <div class="price">$${parseFloat(precio).toFixed(2)}</div>
      <div class="context-menu">
      <div class="menu-option modificar-btn">Modificar</div>
      <div class="menu-option borrar-btn">Eliminar</div>
      </div>
      `;
      menuGrid.appendChild(newCard);

      closeModal();
      alert('¡Platillo agregado con éxito!');
    }

    // --- Función: Modificar platillo ---
    function modificarPlatillo() {
      const nombre = document.getElementById('nombre').value;
      const precio = document.getElementById('precio').value;
      const patronPrecio = /^\d{1,3}(\.\d{1,2})?$/;
      let mensajeError = '';

      // Validar nombre
      if (!nombre) {
        mensajeError += 'El campo "Nombre" es necesario.\n';
      }
      if (nombre.length<3){
        mensajeError += 'El campo "Nombre" debe ser un alimento o bebida de mínimo 3 letras. (Ejemplo: Pan, col, sopa, escamoles).\n';
      }
      // Validar precio
      if(!precio){
        mensajeError += 'El campo "Precio" es necesario.\n';
      }

      // Validar precio (existencia y formato)
      if (!patronPrecio.test(precio)){
        mensajeError += 'El campo "Precio" sólo permite números y no deben ser mayores a 3 cifras y 2 decimales.\n';
      }


      // Mostrar alerta si hay errores
      if (mensajeError) {
        alert(mensajeError.trim());
        return;
      }

      editingCard.querySelector('h3').textContent = nombre;
      editingCard.querySelector('.price').textContent = `$${parseFloat(precio).toFixed(2)}`;
      editingCard = null;

      closeModal();
      alert('¡Platillo modificado con éxito!');
    }

    // --- Manejar el botón "Guardar" ---
    saveBtn.addEventListener('click', (e) => {
      e.preventDefault();
      if (editingCard) {
        modificarPlatillo();
      } else {
        agregarPlatillo();
      }
    });

    // --- Simular subida de imagen ---
    imageUpload.addEventListener('click', () => {
      alert('Funcionalidad de subir imagen no implementada aún.');
    });

    // --- Delegación de eventos para todas las tarjetas ---
    menuGrid.addEventListener('click', (e) => {
      const card = e.target.closest('.card');
      if (!card) return;

      // Modificar
      if (e.target.classList.contains('modificar-btn')) {
        document.getElementById('nombre').value = card.querySelector('h3').textContent;
        document.getElementById('precio').value = card.querySelector('.price').textContent.replace('$', '');
        editingCard = card;
        modal.style.display = 'flex';
      }

      // Eliminar
      if (e.target.classList.contains('borrar-btn')) {
        alert('Proximamente...')
        // if (confirm(`¿Eliminar ${card.querySelector('h3').textContent}?`)) {
        //   card.remove();
        // }
      }
    });
});
