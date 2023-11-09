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
            var resultadosHTML = "<h2>Canciones seleccionadas:</h2><ul>";
            selecciones.forEach(function(valor) {
                resultadosHTML += "<li>" + valor + "</li>";
            });
            resultadosHTML += "</ul>";
            resultadosDiv.append(resultadosHTML);
        } else {
            resultadosDiv.html("<p>Ninguna casilla seleccionada.</p>");
        }
    });
});
