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
                url: "/recomendar_canciones/",  // Cambia esto a tu URL de Django
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
        var cancionesRecomendadas = resultados.recomendaciones;
    
        // Limpiar el contenido anterior en #resultados-seleccion
        var resultadosDiv = $("#resultados-seleccion");
        resultadosDiv.empty();
    
        if (cancionesRecomendadas.length > 0) {
            var resultadosHTML = "<h2>Canciones recomendadas:</h2><ul>";
    
            // Iterar sobre las canciones recomendadas y construir la lista
            cancionesRecomendadas.forEach(function(cancion) {
                resultadosHTML += "<li>" + cancion.title + " - " + cancion.artist + "</li>";
            });
    
            resultadosHTML += "</ul>";
    
            // Agregar la lista al contenedor #resultados-seleccion
            resultadosDiv.html(resultadosHTML);
        } else {
            // Mostrar un mensaje si no hay canciones recomendadas
            resultadosDiv.html("<p>No hay canciones recomendadas.</p>");
        }
    }
    
});
