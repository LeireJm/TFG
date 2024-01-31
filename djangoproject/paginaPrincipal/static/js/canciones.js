$(document).ready(function() {
    $("#btn-enviar").on("click", function() {
        var selecciones = [];

        $(".cancion-checkbox:checked").each(function() {
            selecciones.push($(this).val());
        });

        var resultadosDiv = $("#resultados-seleccion");
        resultadosDiv.empty(); // Limpiar contenido anterior

        //si hemos marcado alguna casilla, la muestra
        if (selecciones.length > 0) {
            // var resultadosHTML = "<h2>Canciones seleccionadas:</h2><ul>";
            // selecciones.forEach(function(valor) {
            //     resultadosHTML += "<li>" + valor + "</li>";
            // });
            // resultadosHTML += "</ul>";
            // resultadosDiv.append(resultadosHTML);
            $.ajax({
                type: "POST",
                url: "/recomendar_canciones/",  
                data: {
                    canciones: selecciones,
                    csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
                },
                success: function(respuesta) {
                    console.log("La solicitud AJAX se ha completado con éxito");
                    console.log(respuesta);
                    mostrarResultadosRecomendacion(respuesta);
                },
                error: function(xhr, status, error) {
                    console.error("Error en la solicitud AJAX:", error);
                    console.log("Estado de la respuesta:", xhr.status);
                    console.log("Respuesta del servidor:", xhr.responseText);
                }
            });
        } else {
            resultadosDiv.html("<p>Ninguna casilla seleccionada.</p>");
        }
    });

    function mostrarResultadosRecomendacion(resultados) {
        console.log(resultados);
        var cancionesRecomendadas = resultados.recomendaciones;
    
        // Limpiar el contenido anterior en #resultados-seleccion
        var resultadosDiv = $("#resultados-seleccion");
        resultadosDiv.empty();

        //AQUI ME HE QUEDADO
        if (cancionesRecomendadas.length > 0) {
            console.log(cancionesRecomendadas);
            console.log(cancionesRecomendadas.length);
            var resultadosHTML = "<h2>Canciones recomendadas:</h2><ul>";
            
            var jsonArray = JSON.parse(cancionesRecomendadas);
            console.log(jsonArray);

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