$(document).ready(function() {
    var indiceActual = 0;
    var indicePop = 0;
    var indiceExplicacion = 0;

    // segunda parte
    var btnLike = document.getElementById('btn-like');
    var btnCheck = document.getElementById('btn-check');
    var btnRep = document.getElementById('btn-rep');
    var btnEnviar = document.getElementById('btn-enviar');

    var selecciones = [];

    var nombre = document.getElementById('nombre').dataset.nombre;
    var artista = document.getElementById('artista').dataset.artista;
    var elementoId = document.getElementById('id').dataset.id;

    var playlistId = document.getElementById('playlistId').dataset.playlistid;
    //indica si la primera canción es de favoritos o de populares (populares: 0, favoritos: 1)
    var primer = document.getElementById('primer').dataset.primer; 

    if (primer == 0)
        $("#explanation").text("Te la recomendamos porque esta canción es popular");
    else
        $("#explanation").text("Te la recomendamos porque está en tu lista de favoritos");

    console.log("Nombre:", nombre);
    console.log("Artista:", artista);
    console.log("Id:", elementoId);
    console.log("PlaylistId:", playlistId);

    btnLike.setAttribute("estado", "vacio");

    //miro a ver si el usuario tiene la canción en favoritos
    estaEnFavoritos(elementoId)

    var resultadosDiv = $("#resultados-seleccion");
    resultadosDiv.empty(); // Limpiar contenido anterior

    // Si le damos el check, metemos la cancion en la playlist y mostramos otra en función de las canciones que tengamos en la playlist hasta ahora
    btnCheck.addEventListener('click', function() {    
        console.log("Metemos la cancion en la playlist:", nombre, elementoId)
        $.ajax({
            type: "POST",
            url: "/paginaPrincipal/meterCancionPlaylist/",
            data: {
                cancion: elementoId,
                playlistId: playlistId,
                // csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
            },
            success: function(response) {
                //metemos el elemento en la lista de las canciones que tenemos en la playlist
                selecciones.push(elementoId)
                $.ajax({
                    type: "POST",
                    url: "/paginaPrincipal/recomendar_canciones/",  
                    data: {
                        canciones: selecciones,
                        csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
                    },
                    success: function(response) {            
                        var cancionesRecomendadas = response.recomendaciones;
                        var explicacion = response.explicacion;
            
                        var jsonArray = JSON.parse(cancionesRecomendadas);
                        console.log("JSON")
                        console.log(jsonArray);

                        var song = jsonArray[indiceActual];
                        
                        // Incrementar el índice actual para la próxima canción
                        indiceActual++;
        
                        console.log("jsonArray longitud")
                        console.log(jsonArray.length)
                
                        console.log("Check")
                        console.log(song)

                        indiceExplicacion = 0;

                        var explanationText = explicacion[indiceExplicacion]; // Obtener la explicación correspondiente

                        console.log(explanationText)
            
                        // Ponemos la nueva canción
                        $("#nombre").text(song.track_name);
                        $("#artista").text(song.artist_name);
                        $("#id").text(song.id).hide();
                        $("#explanation").text(explicacion[indiceExplicacion]);
        
                        nombre = song.track_name
                        artista = song.artist_name
                        elementoId = song.id 

                        //miro a ver si el usuario tiene la canción en favoritos
                        estaEnFavoritos(elementoId)

                        indiceExplicacion++;

                        console.log("Indice explicacion: ", indiceExplicacion)

                        console.log("Nombre:", nombre);
                        console.log("Artista:", artista);
                        console.log("Id:", elementoId);
                        console.log("PlaylistId:", playlistId);

                    },
                    error: function(xhr, status, error) {
                        console.error("Error en la solicitud AJAX:", error);
                    }
                });
                console.log("La canción se ha añadido a la playlist");      
            },
            error: function(xhr, status, error) {
                console.error("La canción no se ha añadido a la playlist", error);
            }
        });          
    });

    console.log("selecciones")
    console.log(selecciones)

    //Si le doy al botón de repetir, me saca otra canción
    btnRep.addEventListener('click', function() {
    
        console.log("le he dado a rep")

        contarCancionesEnPlaylist(playlistId);
    });   

    // Si le doy al botón de enviar, creo la playlist
    btnEnviar.addEventListener('click', function() {
        var confirmacion = confirm("¿Deseas crear la playlist con las canciones seleccionadas?");

            if (confirmacion) {
                window.close()
                var left = (window.innerWidth - 1000) / 2;
                var top = (window.innerHeight - 1000) / 2;
                var opciones = 'width=1000,height=1000, left=' + left + ',top=' + top; 
    
                // Abre una nueva ventana con la URL especificada y las opciones definidas
                var nuevaVentana = window.open('/usuarios/mostrar_playlists/', '_blank', opciones);
                nuevaVentana.focus();
            } else {
                // // Si el usuario cancela, no se realiza ninguna acción adicional
                // console.log("El usuario canceló la redirección.");
            }

    });

    btnLike.addEventListener('click', function() {  
        console.log("le he dado al icono del corazón")  
        manejarClicCorazon(btnLike, nombre, elementoId);
    });

    function contarCancionesEnPlaylist(playlistId) {
        //Si no hay canciones en la playlist, mostrar por popularidad
        if (selecciones.length === 0) {
            console.log("La playlist no tiene canciones, mostramos por popularidad")

            $.ajax({
                type: "POST",
                url: "/paginaPrincipal/crear_playlist/contarCancionesPlaylist/porPopularidad",
                data: {
                    csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
                },
                success: function(response) {
                    var canciones = response.canciones;
                    
                    // Obtener la canción en el índice actual
                    var song = canciones[indicePop];
                    
                    // Incrementar el índice actual para la próxima canción
                    indicePop++;
        
                    // Ponemos la nueva canción
                    $("#nombre").text(song.track_name);
                    $("#artista").text(song.artist_name);
                    $("#id").text(song.id).hide();
                    $("#explanation").text("Te la recomendamos porque esta canción es popular");

                    nombre = song.track_name
                    artista = song.artist_name
                    elementoId = song.id

                    console.log("canciones aleatorias")
                    console.log(canciones)

                    estaEnFavoritos(elementoId)  
                },
                error: function(xhr, status, error) {
                    console.error("Error al mostrar canciones aleatorias:", error);
                }
            });
        } else { //si hay canciones en la playlist, mostrar canciones basadas en las que ya hay en la playlist
            console.log("La playlist tiene canciones, mostramos la canción a partir de las canciones de la playlist");

            $.ajax({
                type: "POST",
                url: "/paginaPrincipal/recomendar_canciones/",  
                data: {
                    canciones: selecciones,
                    csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
                },
                success: function(response) {
                    var cancionesRecomendadas = response.recomendaciones;
                    var explicacion = response.explicacion;
                    console.log("La solicitud AJAX se ha completado con éxito");
                    console.log(cancionesRecomendadas);
        
                    var jsonArray = JSON.parse(cancionesRecomendadas);
                    console.log("JSON")
                    console.log(jsonArray);
        
                    // mostrarResultadosRecomendacion(respuesta);

                    var song = jsonArray[indiceActual];
                    
                    // Incrementar el índice actual para la próxima canción
                    indiceActual++;
    
                    console.log("jsonArray longitud")
                    console.log(jsonArray.length)
            
                    console.log("Rep")
                    console.log(song)
        
                    // Ponemos la nueva canción
                    $("#nombre").text(song.track_name);
                    $("#artista").text(song.artist_name);
                    $("#id").text(song.id).hide();

            
                    $("#explanation").text(explicacion[indiceExplicacion]);
                    indiceExplicacion++;
    
                    nombre = song.track_name
                    artista = song.artist_name
                    elementoId = song.id 

                    //miro a ver si el usuario tiene la canción en favoritos
                    estaEnFavoritos(elementoId)
                    
                },
                error: function(xhr, status, error) {
                    console.error("Error en la solicitud AJAX:", error);
                }
            });
        }
    }    

    function estaEnFavoritos(elementoId) {
        //miro a ver si el usuario tiene la canción en favoritos
        $.ajax({
            url: '/paginaPrincipal/crear_playlist/estaEnFavoritos',
            type: 'POST',
            data: {
                idCancion: elementoId
            },
            success: function(response) {
                console.log(response);
                //la canción está en mis favoritos, muestro el corazón lleno
                if (response.mensaje === '0') {
                    console.log("hemos determinado que la canción está")
                    btnLike.classList.remove("far");
                    btnLike.classList.add("fas");
                    btnLike.setAttribute("estado", "lleno");
                }
                else{
                    console.log("hemos determinado que la canción no está")
                    btnLike.classList.remove("fas");
                    btnLike.classList.add("far");
                    btnLike.setAttribute("estado", "vacio");
                }
            },
            error: function(error) {
                console.error(error);
            }
        });
    }

    function manejarClicCorazon(corazon, nombreCancion, idCancion) {
        // Verificar el estado actual del corazón
        var estadoActual = corazon.getAttribute("estado");
    
        // Alternar entre los estados lleno/vacío
        if (estadoActual === "vacio") {
            corazon.classList.remove("far");
            corazon.classList.add("fas");
            corazon.setAttribute("estado", "lleno");
            console.log("Le gusta la canción:", nombreCancion);
            console.log("id de la cancion que le gusta", idCancion);
    
            $.ajax({
                url: '/usuarios/mostrar_favoritos/anadir_cancion_fav/',
                type: 'POST',
                data: {
                    idCancion: idCancion
                },
                success: function(response) {
                    console.log(response);
                },
                error: function(error) {
                    console.error(error);
                }
            });
        } else {
            corazon.classList.remove("fas");
            corazon.classList.add("far");
            corazon.setAttribute("estado", "vacio");
            console.log("No le gusta la canción:", idCancion);
    
            $.ajax({
                url: '/usuarios/mostrar_favoritos/eliminar_cancion_fav/',
                type: 'POST',
                data: {
                    idCancion: idCancion
                },
                success: function(response) {
                    console.log(response);
                },
                error: function(error) {
                    console.error(error);
                }
            });
        }
    }
});