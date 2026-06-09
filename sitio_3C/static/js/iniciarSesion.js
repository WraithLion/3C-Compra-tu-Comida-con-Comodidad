// Elementos del DOM
const modal = document.getElementById("modal");
const modalTitle = document.getElementById("modalTitle");
const iniciarSesion = document.getElementById("iniciarSesionIH");
const cancelarBoton = document.getElementById("cancelar")
const cerrarBoton = document.querySelector(".close");

// Abrir modal como "Iniciar sesión"
iniciarSesion.onclick = function() {
    modal.style.display = "flex";
}


// Cerrar formulario al hacer clic en botón Cancelar
cancelarBoton.onclick = function() {
    modal.style.display = "none";
}


// Cerrar modal
cerrarBoton.onclick = function() {
    modal.style.display = "none";
}

// Cerrar al hacer clic fuera del contenido
window.onclick = function(event) {
    if (event.target === modal) {
        modal.style.display = "none";
    }
}


