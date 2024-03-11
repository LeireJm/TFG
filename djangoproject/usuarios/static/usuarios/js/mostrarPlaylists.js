$(document).ready(function() {

    var cancionesContainer = document.getElementById("playlistsContainer");

    console.log("id play")
    console.log(idsPlaylists)

    // Llena la lista de canciones
    nombresPlaylists.forEach(function(cancion, index) {
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

        corazon.setAttribute("data-index", index);
        

        corazon.addEventListener("click", function() {
            var playlistIndex = this.getAttribute("data-index");
            console.log("Playlist seleccionada")
            console.log(playlistIndex)

            idsPlaylists[playlistIndex]

            $.ajax({
                type: "POST",
                url: "/usuarios/mostrar_playlists/mostrarCancionesPlaylist/",
                data: {
                    playlistId: idsPlaylists[playlistIndex],
                    // csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
                },
                success: function(response) {
                    console.log("Los datos se enviaron correctamente");
                },
                error: function(xhr, status, error) {
                    console.error("Error al enviar datos a views.py:", error);
                }
            });    
            // window.location.href = "/canciones/?playlist=" + encodeURIComponent(cancion);
        });
        cancionElement.appendChild(corazon);


        // Agrega la canción al contenedor
        cancionesContainer.appendChild(cancionElement);
    });
});
