$(document).ready(function() {
    const sidebar = document.getElementById('sidebar');
    const resizeHandle = document.getElementById('resizeHandle');

    let isResizing = false;
    let lastX = 0;
    let sidebarWidth = 400; // Ancho inicial de la barra lateral

    // Función para iniciar el redimensionamiento
    resizeHandle.addEventListener('mousedown', (e) => {
        isResizing = true;
        lastX = e.clientX;
    });

    // Función para actualizar el ancho de la barra lateral mientras se redimensiona
    document.addEventListener('mousemove', (e) => {
        if (!isResizing) return;
        const deltaX = e.clientX - lastX;
        sidebarWidth += deltaX;
        sidebar.style.width = `${sidebarWidth}px`;
        lastX = e.clientX;
    });

    // Función para detener el redimensionamiento
    document.addEventListener('mouseup', () => {
        isResizing = false;
    });


});
