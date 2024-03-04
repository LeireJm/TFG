$(document).ready(function() {
    // Datos de ejemplo para las canciones
    var canciones = [
        { nombre: "Canción 1", artista: "Artista 1", duracion: "3:30" },
        { nombre: "Canción 2", artista: "Artista 2", duracion: "4:15" },
        { nombre: "Canción 3", artista: "Artista 3", duracion: "2:45" },
        { nombre: "Canción 1", artista: "Artista 1", duracion: "3:30" },
        { nombre: "Canción 2", artista: "Artista 2", duracion: "4:15" },
        { nombre: "Canción 3", artista: "Artista 3", duracion: "2:45" },
        { nombre: "Canción 1", artista: "Artista 1", duracion: "3:30" },
        { nombre: "Canción 2", artista: "Artista 2", duracion: "4:15" },
        { nombre: "Canción 3", artista: "Artista 3", duracion: "2:45" },
        { nombre: "Canción 1", artista: "Artista 1", duracion: "3:30" },
        { nombre: "Canción 2", artista: "Artista 2", duracion: "4:15" },
        { nombre: "Canción 3", artista: "Artista 3", duracion: "2:45" }
        // Agrega más canciones según sea necesario
    ];

    var cancionesContainer = document.getElementById("cancionesContainer");

    // Llena la lista de canciones
    canciones.forEach(function(cancion) {
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
        corazon.classList.add("far", "fa-heart", "corazon");
        corazon.addEventListener("click", function() {
            // Lógica para marcar como favorita
            corazon.classList.toggle("favorita");
        });
        cancionElement.appendChild(corazon);

        // Duración de la canción
        var duracionCancion = document.createElement("span");
        duracionCancion.textContent = cancion.duracion;
        cancionElement.appendChild(duracionCancion);

        // Agrega la canción al contenedor
        cancionesContainer.appendChild(cancionElement);
    });
});
