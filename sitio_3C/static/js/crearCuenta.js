// Elementos del DOM
const modal = document.getElementById("modal");
const modalTitle = document.getElementById("modalTitle");
const iniciarSesion = document.getElementById("iniciarSesionIH");
const crearCuenta = document.getElementById("crearCuentaIH");
const cerrarBoton = document.querySelector(".close");

// Abrir modal como "Iniciar sesión"
iniciarSesion.onclick = function() {
    modal.style.display = "flex";
}

// Abrir modal como "Crear cuenta"
crearCuenta.onclick = function() {
    modal.style.display = "flex";
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


