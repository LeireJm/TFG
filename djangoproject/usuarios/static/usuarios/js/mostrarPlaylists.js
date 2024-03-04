$(document).ready(function() {

    var cancionesContainer = document.getElementById("playlistsContainer");

    // Llena la lista de canciones
    nombresPlaylists.forEach(function(cancion) {
        var cancionElement = document.createElement("div");
        cancionElement.classList.add("cancion"); // Agrega la clase 'cancion'

        // Icono de música
        var iconoMusica = document.createElement("i");
        iconoMusica.classList.add("fas", "fa-layer-group", "icono-playlist");
        cancionElement.appendChild(iconoMusica);

        // Nombre de la playlist
        var nombreCancion = document.createElement("span");
        nombreCancion.textContent = cancion;
        cancionElement.appendChild(nombreCancion);

        // Fecha hacia la derecha (para entrar en la playlist)
        var corazon = document.createElement("i");
        corazon.classList.add("fas", "fa-arrow-right", "corazon");
        corazon.addEventListener("click", function() {
            // Lógica para marcar como favorita
            corazon.classList.toggle("favorita");
        });
        cancionElement.appendChild(corazon);


        // Agrega la canción al contenedor
        cancionesContainer.appendChild(cancionElement);
    });
});
