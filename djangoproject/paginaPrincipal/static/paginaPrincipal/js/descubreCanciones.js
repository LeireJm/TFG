var cancionesSeleccionadas = [];
var jsonArray;

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
                var explicacion = response.explicacion;
                console.log("Canciones recomendadas");
                console.log(cancionesRecomendadas);

                console.log("explicacion canciones")
                console.log(explicacion)
    
                jsonArray = JSON.parse(cancionesRecomendadas);

                console.log("JSON")
                console.log(jsonArray); 

                $('.canciones-container').empty();

                // $('#resultados-seleccion').empty().append(mostrarResultadosRecomendacion(jsonArray));
                $('#resultados-seleccion').empty();
                mostrarResultadosRecomendacion(jsonArray, explicacion);

                
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

function mostrarResultadosRecomendacion(resultados, explicacion) {

    // Limpiar el contenido anterior en #resultados-seleccion
    var resultadosDiv = $("#resultados-seleccion");
    resultadosDiv.empty();

    if (resultados.length > 0) {
        var resultadosHTML = "<h2>Playlist recomendada: </h2><ul>";;
        resultadosHTML += "<p id='explicacion'>A continuación hay una lista con las canciones recomendadas a partir de las seleccionadas.<br> Puedes guardar la playlist o volver a la página principal sin guardarla. </p><ul>";

        for (var i = 0; i < resultados.length; i++) {
            var song = resultados[i];
            var explanationText = explicacion[i]; // Obtener la explicación correspondiente
            resultadosHTML += "<div class='cancion-container'>";
            resultadosHTML += "<h3>" + song.track_name + "</h3>";
            resultadosHTML += "<p>Autor: " + song.artist_name + "</p>";
            resultadosHTML += "<p> " + explanationText + "</p>"; // Agregar la explicación
            resultadosHTML += "</div>";
        }
        resultadosHTML += "</ul>";

        // Agregar la lista al contenedor #resultados-seleccion
        resultadosHTML += "<div class='botones-container'>";
        resultadosHTML += "<button id='irInicio'>Ir al inicio</button>";
        resultadosHTML += "<button id='anadirABiblioteca'>Añadir a la biblioteca</button>";
        resultadosHTML += "</div>";
        resultadosDiv.append(resultadosHTML);
    } else {
        // Mostrar un mensaje si no hay canciones recomendadas
        resultadosDiv.html("<p>No hay canciones recomendadas.</p>");
    }
}

//una vez realizada la recomendación, si el usuario no quiere guardar la playlist, vuelve al inicio
$(document).on('click', '#irInicio', function() {
    window.close();
});

//si el usuario quiere guardar la playlist recomendada
$(document).on('click', '#anadirABiblioteca', function() {
    console.log("añadir a la biblioteca")

    //mandar las canciones recomendadas a views para meterlas en la base de datos.
    
    console.log("JSON que pasamos")
    console.log(jsonArray)

    var listaIds = jsonArray.map(function(objeto) {
        return objeto.id;
    });

    console.log("lista ids")
    console.log(listaIds);

    $.ajax({
        type: "POST",
        url: "/paginaPrincipal/descubrir_listaCanciones/pasarCanciones",
        data: {
            listaIds: listaIds
            // csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
        },
        success: function(response) {     

        },
        error: function(xhr, status, error) {
            console.error("No se han podido pasar las canciones recomendadas a la base de datos", error);
        }
    }); 

    var left = (window.innerWidth - 100) / 2;
    var top = (window.innerHeight - 100) / 2;
    var popupWindow2 = window.open('/paginaPrincipal/descubrir_listaCanciones/ponerNombre', "popupWindow", 'width=' + 100 + ', height=' + 100 + ', top=' + top + ', left=' + left);

    popupWindow2.focus();
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

