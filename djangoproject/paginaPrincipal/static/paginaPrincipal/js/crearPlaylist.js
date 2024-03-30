$(document).ready(function() {
    var indiceActual = 0;
    var indicePop = 0;

    // segunda parte
    var btnLike = document.getElementById('btn-like');
    var btnCheck = document.getElementById('btn-check');
    var btnRep = document.getElementById('btn-rep');
    var btnEnviar = document.getElementById('btn-enviar');

    var selecciones = [];

    //por ahora sólo con una canción
    var nombre = document.getElementById('nombre').dataset.nombre;
    var artista = document.getElementById('artista').dataset.artista;
    var elementoId = document.getElementById('id').dataset.id;

    var playlistId = document.getElementById('playlistId').dataset.playlistid;

    console.log("Nombre:", nombre);
    console.log("Artista:", artista);
    console.log("Id:", elementoId);
    console.log("PlaylistId:", playlistId);

    btnLike.setAttribute("estado", "vacio");

    //miro a ver si el usuario tiene la canción en favoritos
    $.ajax({
        url: '/paginaPrincipal/crear_playlist/estaEnFavoritos',
        type: 'POST',
        data: {
            idCancion: elementoId
        },
        success: function(response) {
            console.log(response);
        },
        error: function(error) {
            console.error(error);
        }
    });

    manejarClicCorazon(btnLike, "canciones[i].nombre", "canciones[i].id");

    function manejarClicCorazon(corazon, nombreCancion, idCancion) {
        corazon.addEventListener("click", function() {
            // Alternar entre los estados lleno/vacío
            if (corazon.getAttribute("estado") === "vacio") {
                corazon.classList.remove("far");
                corazon.classList.add("fas");
                corazon.setAttribute("estado", "lleno");
                console.log("Le gusta la canción:", nombreCancion);

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

            
        });  
    }

    var resultadosDiv = $("#resultados-seleccion");
    resultadosDiv.empty(); // Limpiar contenido anterior

    // Si le damos el check, metemos la cancion en la playlist y mostramos otra en función de las canciones que tengamos en la playlist hasta ahora
    btnCheck.addEventListener('click', function() {    
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
                    success: function(respuesta) {
                        console.log("La solicitud AJAX se ha completado con éxito");
                        console.log(respuesta);
            
                        var cancionesRecomendadas = respuesta.recomendaciones;
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
                
                        console.log("Check")
                        console.log(song)
            
                        // Ponemos la nueva canción
                        $("#nombre").text(song.track_name);
                        $("#artista").text(song.artist_name);
                        $("#id").text(song.id).hide();
        
                        nombre = song.track_name
                        artista = song.artist_name
                        elementoId = song.id 

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

    function contarCancionesEnPlaylist(playlistId) {
        //Si no hay canciones en la playlist, mostrar por popularidad
        if (selecciones.length === 0) {
            $.ajax({
                type: "POST",
                url: "/paginaPrincipal/crear_playlist/contarCancionesPlaylist/porPopularidad",
                data: {
                    csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
                },
                success: function(response) {
                    console.log("no hay canciones en la playlist")
                    var canciones = response.canciones;
                    
                    // Obtener la canción en el índice actual
                    var song = canciones[indicePop];
                    
                    // Incrementar el índice actual para la próxima canción
                    indicePop++;

                    console.log("Rep")
                    console.log(song)
        
                    // Ponemos la nueva canción
                    $("#nombre").text(song.track_name);
                    $("#artista").text(song.artist_name);
                    $("#id").text(song.id).hide();

                    nombre = song.track_name
                    artista = song.artist_name
                    elementoId = song.id

                    console.log("canciones aleatorias")
                    console.log(canciones)
                },
                error: function(xhr, status, error) {
                    console.error("Error al mostrar canciones aleatorias:", error);
                }
            });
        } else { //si hay canciones en la playlist, mostrar canciones basadas en las que ya hay en la playlist
            console.log("La playlist tiene canciones.");

            $.ajax({
                type: "POST",
                url: "/paginaPrincipal/recomendar_canciones/",  
                data: {
                    canciones: selecciones,
                    csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
                },
                success: function(respuesta) {
                    console.log("La solicitud AJAX se ha completado con éxito");
                    console.log(respuesta);
        
                    var cancionesRecomendadas = respuesta.recomendaciones;
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
    
                    nombre = song.track_name
                    artista = song.artist_name
                    elementoId = song.id 
                    
                },
                error: function(xhr, status, error) {
                    console.error("Error en la solicitud AJAX:", error);
                }
            });
        }
    }    
        

    function mostrarResultadosRecomendacion(resultados) {

        console.log("resultados")
        console.log(resultados);
        var cancionesRecomendadas = resultados.recomendaciones;
    
        // Limpiar el contenido anterior en #resultados-seleccion
        var resultadosDiv = $("#resultados-seleccion");
        resultadosDiv.empty();

        if (cancionesRecomendadas.length > 0) {
            console.log(cancionesRecomendadas);
            console.log(cancionesRecomendadas.length);
            var resultadosHTML = "<h2>Canciones recomendadas:</h2><ul>";
            
            var jsonArray = JSON.parse(cancionesRecomendadas);


            for (var i = 0; i < jsonArray.length; i++) {
                var song = jsonArray[i];
                resultadosHTML += "<li>" + song.track_name + " - " + song.artist_name + "</li>";
            }
            resultadosHTML += "</ul>";

            // for (var i = 0; i < cancionesRecomendadas.length; i++) {
            //     var song = cancionesRecomendadas[i];
            //     console.log(cancionesRecomendadas[i]);
            //     resultadosHTML += "<li>" + song.track_name + " - " + song.artist_name + "</li>";
            // }
            // resultadosHTML += "</ul>";
    
            // Agregar la lista al contenedor #resultados-seleccion
            resultadosDiv.html(resultadosHTML);
        } else {
            // Mostrar un mensaje si no hay canciones recomendadas
            resultadosDiv.html("<p>No hay canciones recomendadas.</p>");
        }
    }
    
});