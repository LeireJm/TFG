$(document).ready(function() {
    var indiceActual = 0;

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

    selecciones.push(elementoId)

    // $(".cancion-checkbox:checked").each(function() {
    //     selecciones.push($(this).val());
    // });

    var resultadosDiv = $("#resultados-seleccion");
    resultadosDiv.empty(); // Limpiar contenido anterior

    // Meter la cancion en la playlist y mostrar otra
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
                console.log("Los datos se enviaron correctamente a views.py");
                console.log(response); // Puedes manejar la respuesta si es necesario
            },
            error: function(xhr, status, error) {
                console.error("Error al enviar datos a views.py:", error);
            }
        });          
    });

    //si hemos marcado alguna casilla, la muestra
    // if (selecciones.length > 0) {
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

            

            btnRep.addEventListener('click', function() {

                // var indiceAleatorio = Math.floor(Math.random() * 10);
        
                // // Obtener la canción en el índice aleatorio
                // var song = jsonArray[indiceAleatorio];

                // Obtener la canción en el índice actual
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
        
            });
            
        },
        error: function(xhr, status, error) {
            console.error("Error en la solicitud AJAX:", error);
            console.log("Estado de la respuesta:", xhr.status);
            console.log("Respuesta del servidor:", xhr.responseText);
        }
    });

    

    // Crear la playlist
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

    function abrirPopup(url, width, height) {
        var left = (window.innerWidth - width) / 2;
        var top = (window.innerHeight - height) / 2;
        var popupWindow = window.open(url, "popupWindow", 'width=' + width + ', height=' + height + ', top=' + top + ', left=' + left);
        popupWindow.focus();
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