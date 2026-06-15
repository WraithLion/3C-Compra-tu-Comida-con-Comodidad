    const btnPerfil = document.getElementById('btn-perfil');
    const contextMenu = document.getElementById('context-menu');

    // Mostrar/Ocultar menú al hacer clic en Perfil
    btnPerfil.addEventListener('click', (e) => {
        e.stopPropagation(); // Evita que el clic se propague inmediatamente
        const isVisible = contextMenu.style.display === 'block';
        contextMenu.style.display = isVisible ? 'none' : 'block';
    });

    // Cerrar menú si se hace clic fuera
    document.addEventListener('click', (e) => {
        if (!btnPerfil.contains(e.target) && !contextMenu.contains(e.target)) {
            contextMenu.style.display = 'none';
        }
    });

    // Acción simulada de cerrar sesión
    document.querySelector('.cerrarSesion-boton').addEventListener('click', () => {
        // Redirigir a la página principal
        window.location.href = '/'; // Cambia '/' por tu ruta específica si es diferente (ej: '/home')
        // window.location.href = '/logout'; // Tu redirección real aquí
    });

