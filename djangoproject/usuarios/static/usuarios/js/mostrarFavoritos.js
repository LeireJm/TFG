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
        nombreCancion.textContent = canciones[i].nombre; // Utiliza el índice 'i' para obtener el nombre de la canción actual
        cancionElement.appendChild(nombreCancion);

        // Guion
        var guion = document.createElement("span");
        guion.textContent = " - ";
        cancionElement.appendChild(guion);

        // Artista
        var nombreArtista = document.createElement("span");
        nombreArtista.textContent = canciones[i].artista; // Utiliza el índice 'i' para obtener el artista de la canción actual
        cancionElement.appendChild(nombreArtista);

        // Corazón (para marcar como favorita)
        var corazon = document.createElement("i");
        corazon.classList.add("fas", "fa-heart", "corazon");
        corazon.setAttribute("estado", "vacio"); // Agregar un atributo personalizado para rastrear el estado
        manejarClicCorazon(corazon, canciones[i].nombre, canciones[i].id); // Pasa el nombre de la canción como parámetro
        cancionElement.appendChild(corazon);

        // Duración de la canción
        var duracionCancion = document.createElement("span");
        duracionCancion.textContent = canciones[i].duracion; // Utiliza el índice 'i' para obtener la duración de la canción actual
        cancionElement.appendChild(duracionCancion);

        // Agrega la canción al contenedor
        cancionesContainer.appendChild(cancionElement);
    }

    function manejarClicCorazon(corazon, nombreCancion, idCancion) {
        corazon.addEventListener("click", function() {
            // Alternar entre los estados lleno/vacío
            if (corazon.getAttribute("estado") === "vacio") {
                corazon.classList.remove("far");
                corazon.classList.add("fas");
                corazon.setAttribute("estado", "lleno");
                console.log("Le gusta la canción:", nombreCancion);
            } else {
                corazon.classList.remove("fas");
                corazon.classList.add("far");
                corazon.setAttribute("estado", "vacio");
                console.log("No le gusta la canción:", nombreCancion);
            }

            $.ajax({
                url: '/usuarios/mostrar_favoritos/eliminar_cancion_fav/',
                type: 'POST',
                data: {
                    'cancion_id': idCancion
                },
                success: function(response) {
                    console.log(response);
                    // Eliminar la canción de la página después de eliminarla de la base de datos
                    // $('#cancion_' + idCancion).remove();
                },
                error: function(error) {
                    console.error(error);
                }
            });
        });  
    }
});
