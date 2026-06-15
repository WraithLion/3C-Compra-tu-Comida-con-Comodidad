document.addEventListener('DOMContentLoaded', function () {
  // Rutas estáticas basadas en tu configuración
  const STATIC_URL = '/static';
  const DEFAULT_PLACEHOLDER = `${STATIC_URL}/restaurante/placeholder-icon.png`;
  const DEFAULT_PLATILLO_IMAGE = `${STATIC_URL}/restaurante/default-platillo.png`;

  // Elementos del DOM
  const openModal = document.getElementById('openModal');
  const modal = document.getElementById('addItemModal');
  const closeBtn = modal.querySelector('.close');
  const cancelBtn = modal.querySelector('.btn-cancelar');
  const saveBtn = modal.querySelector('.btn-guardar');
  const form = document.getElementById('addItemForm');
  const menuGrid = document.querySelector('.menu-grid');
  const imageUpload = document.getElementById('imageUpload');
  const imagenInput = document.getElementById('imagenInput');
  const previewImg = document.getElementById('preview-img');

  let editingCard = null;

  // --- Abrir modal ---
  if (openModal) {
    openModal.addEventListener('click', () => {
      editingCard = null;
      form.reset();
      if (previewImg) previewImg.src = DEFAULT_PLACEHOLDER;

      if (imageUpload) imageUpload.querySelector('p').textContent = "Subir imagen";
      modal.style.display = 'flex';
    });
  }

  // --- Cerrar modal ---
  function closeModal() {
    modal.style.display = 'none';
    form.reset();
    editingCard = null;

    if (imagenInput){
      imagenInput.value='';
    }

    if (previewImg) previewImg.src = DEFAULT_PLACEHOLDER;
    if (imageUpload) imageUpload.querySelector('p').textContent = "Subir imagen";
  }

  if (closeBtn) closeBtn.addEventListener('click', closeModal);
  if (cancelBtn) cancelBtn.addEventListener('click', closeModal);
  window.addEventListener('click', (e) => {
    if (e.target === modal) closeModal();
  });

    // --- Subida de imagen (Previsualización) ---
    if (imageUpload) {
      imageUpload.addEventListener('click', () => {
        if (imagenInput) imagenInput.click();
      });
    }

    if (imagenInput) {
      imagenInput.addEventListener('change', function() {
        if (this.files && this.files.length > 0) {
          const archivo = this.files[0]; // <--- Capturamos el archivo individual
          const reader = new FileReader();

          reader.onload = function(e) {
            if (previewImg) previewImg.src = e.target.result;
            if (imageUpload) imageUpload.querySelector('p').textContent = archivo.name; // <--- Usamos el nombre del archivo
          }
          reader.readAsDataURL(archivo); // <--- Leemos el archivo individual
        } else {
          if (previewImg) previewImg.src = DEFAULT_PLACEHOLDER;
          if (imageUpload) imageUpload.querySelector('p').textContent = "Subir imagen";
        }
      });
    }

    // --- Validaciones ---
    function validarFormulario() {
      const nombre = document.getElementById('nombre').value;
      const precio = document.getElementById('precio').value;
      const patronPrecio = /^\d{1,3}(\.\d{1,2})?$/;
      let mensajeError = '';

      if (!nombre) mensajeError += 'El campo "Nombre" es necesario.\n';
      if (nombre.length < 3) mensajeError += 'El campo "Nombre" debe tener mínimo 3 letras.\n';
      if (!precio) mensajeError += 'El campo "Precio" es necesario.\n';
      if (!patronPrecio.test(precio)||precio<=5) mensajeError += 'El precio debe ser mayor a $5.00 y menor a 999.99 (ej. 120 o 120.50).\n';
      // 2. Validación de Imagen (Lógica Corregida)
      const hayNuevaImagen = imagenInput && imagenInput.files && imagenInput.files.length > 0;
      const esModificacion = editingCard !== null; // Si editingCard tiene valor, estamos editando

      // Solo pedimos imagen si:
      // A) Es un platillo NUEVO (no hay imagen previa) Y no han subido ninguna.
      // B) Opcional: Si es edición Y borraron la previa (aunque visualmente ya mostramos la anterior).

      if (!esModificacion && !hayNuevaImagen) {
        // CASO 1: Creando nuevo platillo -> La imagen es OBLIGATORIA
        mensajeError += 'Debes subir una imagen para el platillo.\n';
      }
      return mensajeError;
    }

    // --- Función auxiliar CSRF ---
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

    // --- Enviar datos al servidor ---
    async function enviarDatos(url, formData) {
      try {
        const response = await fetch(url, {
          method: 'POST',
          body: formData,
          headers: {
            'X-CSRFToken': getCookie('csrftoken')
          }
        });

        if (response.ok) {
          const contentType = response.headers.get("content-type");
          if (contentType && contentType.indexOf("application/json") !== -1) {
            const data = await response.json();
            if (data.success) {
              alert(data.message || 'Se ha creado el platillo con éxito.');
              location.reload();
            } else {
              alert(data.error || 'Error en la operación.');
            }
          } else {
            console.warn('Recibido contenido no JSON. Recargando...');
            location.reload();
          }
        } else {
          let errorMsg = 'Error en la solicitud.';
          try {
            const data = await response.json();
            errorMsg = data.error || errorMsg;
          } catch (e) {
            console.error('No se pudo leer la respuesta JSON:', e);
          }
          alert(errorMsg);
        }
      } catch (error) {
        console.error('Error de red o servidor:', error);
        alert('Ocurrió un error de conexión. Revisa la consola.');
      }
    }

    // --- Guardar (Crear o Modificar) ---
    if (saveBtn) {
      saveBtn.addEventListener('click', async (e) => {
        e.preventDefault();

        const mensajeError = validarFormulario();
        if (mensajeError) {
          alert(mensajeError.trim());
          return;
        }

        const nombre = document.getElementById('nombre').value;
        const precio = document.getElementById('precio').value;
        const idPlatillo = editingCard ? editingCard.getAttribute('data-id') : null;

        const formData = new FormData();
        formData.append('nombre', nombre);
        formData.append('precio', precio);


        if (imagenInput && imagenInput.files.length > 0) {
          formData.append('imagen', imagenInput.files[0]); // <--- Agregamos el archivo indexado [0]
        }

        let url = '';
        if (editingCard) {
          if (!idPlatillo) {
            alert('Error: No se encontró el ID del platillo a modificar.');
            return;
          }
          url = `/restaurante/platillos/${idPlatillo}/modificar/`;
        } else {
          url = '/restaurante/platillos/agregar/';
        }

        await enviarDatos(url, formData);
      });
    }

    // --- Delegación de eventos para tarjetas ---
    if (menuGrid) {
      menuGrid.addEventListener('click', (e) => {
        const card = e.target.closest('.card');
        if (!card || card.classList.contains('add-card')) return;

        const idPlatillo = card.getAttribute('data-id');
        const nombrePlatillo = card.querySelector('h3').textContent;

        if (e.target.classList.contains('modificar-btn')) {
          if (!idPlatillo) {
            alert('Error: Este platillo no tiene ID asociado.');
            return;
          }

          const imagenActualSrc=card.querySelector('img').src;

          document.getElementById('nombre').value = nombrePlatillo;
          document.getElementById('precio').value = card.querySelector('.price').textContent.replace('$', '').trim();

          if (previewImg){
            previewImg.src=imagenActualSrc;
          }

          if(imageUpload){
            imageUpload.querySelector('p').textContent="Cambiar imagen";
          }

          editingCard = card;
          modal.style.display = 'flex';
        }

        if (e.target.classList.contains('borrar-btn')) {
          if (!idPlatillo) {
            alert('Error: No se pudo identificar el platillo.');
            return;
          }
          if (confirm(`¿Desea eliminar este platillo?`)) {
            const formData = new FormData();
            enviarDatos(`/restaurante/platillos/${idPlatillo}/eliminar/`, formData);
          }
        }
      });
    }
});
