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
                
                //hacer otra consulta de ajax para mandar los resultados a views y tratarlos
            },
            error: function(xhr, status, error) {
                console.error("No se han podido recomendar canciones a partir de las seleccionadas", error);
            }
        });   
    });
    
});

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
