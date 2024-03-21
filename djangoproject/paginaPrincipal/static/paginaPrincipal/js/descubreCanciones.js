var cancionesSeleccionadas = [];

$(document).ready(function() {
    var duraciones = document.querySelectorAll('.duracion');
    duraciones.forEach(function(duracionElement) {
        var duracionMs = parseInt(duracionElement.textContent);
        var segundosTotales = Math.floor(duracionMs / 1000);
        var minutos = Math.floor(segundosTotales / 60);
        var segundos = segundosTotales % 60;
        // Actualiza el contenido del elemento con el formato de minutos y segundos
        duracionElement.textContent = minutos + ":" + segundos;
    });

    $('#botonEnviar').click(function() {
        console.log("Hemos dado a enviar");
        console.log("Canciones seleccionadas:", cancionesSeleccionadas);

        console.log("opciones seleccionadas mal: ")
        console.log(opciones_seleccionadas)

        opciones_seleccionadas = opciones_seleccionadas.replace(/&#x27;/g, "'");

        console.log("opciones seleccionadas bien: ")
        console.log(opciones_seleccionadas)

        // var opciones_JSON = JSON.parse(opciones_seleccionadas);

        // console.log("opciones seleccionadas bien: ")
        // console.log(opciones_JSON)

        $.ajax({
            type: "POST",
            url: "/paginaPrincipal/recomendar_canciones/",
            data: {
                canciones: cancionesSeleccionadas,
                opciones: opciones_seleccionadas,
                // csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
            },
            success: function(response) {     
                var cancionesRecomendadas = response.recomendaciones;
                console.log("La solicitud AJAX se ha completado con éxito");
                console.log(cancionesRecomendadas);
    
                var jsonArray = JSON.parse(cancionesRecomendadas);
                console.log("JSON")
                console.log(jsonArray); 

                $('.canciones-container').empty();

                // $('#resultados-seleccion').empty().append(mostrarResultadosRecomendacion(jsonArray));
                $('#resultados-seleccion').empty();
                mostrarResultadosRecomendacion(jsonArray);

                
   
            },
            error: function(xhr, status, error) {
                console.error("No se han podido recomendar canciones a partir de las seleccionadas", error);
            }
        });   
    });
    
});

function minutosSegundos(duracionMs) {
    var segundosTotales = Math.floor(duracionMs / 1000);
    var minutos = Math.floor(segundosTotales / 60);
    var segundos = segundosTotales % 60;
    return minutos + ":" + (segundos < 10 ? "0" : "") + segundos; // Agrega un cero delante si los segundos son menores que 10
}

function mostrarResultadosRecomendacion(resultados) {

    // Limpiar el contenido anterior en #resultados-seleccion
    var resultadosDiv = $("#resultados-seleccion");
    resultadosDiv.empty();

    if (resultados.length > 0) {
        var resultadosHTML = "<h2>Playlist recomendada: </h2><ul>";;

        for (var i = 0; i < resultados.length; i++) {
            var song = resultados[i];
            resultadosHTML += "<div class='cancion-container'>";
            resultadosHTML += "<h3>" + song.track_name + "</h3>";
            resultadosHTML += "<p>Autor: " + song.artist_name + "</p>";
            resultadosHTML += "</div>";
        }
        resultadosHTML += "</ul>";

        // Agregar la lista al contenedor #resultados-seleccion
        resultadosDiv.append(resultadosHTML);
    } else {
        // Mostrar un mensaje si no hay canciones recomendadas
        resultadosDiv.html("<p>No hay canciones recomendadas.</p>");
    }
}

function seleccionarCancion(elemento) {
    var cancionId = elemento.getAttribute('data-id');

    //comprobamos si la cancioón ya está seleccionada
    var index = cancionesSeleccionadas.indexOf(cancionId);
    if (index === -1) {
        //metemos la canción seleccionada en la lista
        cancionesSeleccionadas.push(cancionId);
        console.log("Canción seleccionada:", cancionId);
        console.log("Canciones seleccionadas:", cancionesSeleccionadas);
        
        elemento.classList.add('cancion-seleccionada');
    } else {
        //la canción ya está en la lista
        cancionesSeleccionadas.splice(index, 1);
        elemento.classList.remove('cancion-seleccionada');
    }
}
