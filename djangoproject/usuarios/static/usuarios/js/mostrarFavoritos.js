$(document).ready(function() {

    var cancionesContainer = document.getElementById("cancionesContainer");

    var longitud = nombresCanciones.length;


    // Llena la lista de canciones
    for (var i = 0; i < longitud; i++) {
        var cancionElement = document.createElement("div");
        cancionElement.classList.add("cancion"); // Agrega la clase 'cancion'

        // Icono de música
        var iconoMusica = document.createElement("i");
        iconoMusica.classList.add("fas", "fa-music", "icono-musica");
        cancionElement.appendChild(iconoMusica);

        // Nombre de la canción
        var nombreCancion = document.createElement("span");
        nombreCancion.textContent = cancion.nombre;
        cancionElement.appendChild(nombreCancion);

        // Artista
        var nombreArtista = document.createElement("span");
        nombreArtista.textContent = cancion.artista;
        cancionElement.appendChild(nombreArtista);

        // Corazón (para marcar como favorita)
        var corazon = document.createElement("i");
        corazon.classList.add("far", "fa-music", "corazon");
        corazon.addEventListener("click", function() {
            corazon.classList.toggle("favorita");
        });
        cancionElement.appendChild(corazon);

        // Duración de la canción
        var duracionCancion = document.createElement("span");
        duracionCancion.textContent = cancion.duracion;
        cancionElement.appendChild(duracionCancion);

        // Agrega la canción al contenedor
        cancionesContainer.appendChild(cancionElement);
    }
});
