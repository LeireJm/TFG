$(document).ready(function() {
    $("#iniciarSesion").on("click", function(event) {
        var form = $(this);
        var campos = form.find("input[required]");
        for (var i = 0; i < campos.length; i++) {
            if (!campos[i].value) {
                event.preventDefault();
                alert("Por favor, rellene todos los campos obligatorios.");
                return;
            }
        }
    });
});
