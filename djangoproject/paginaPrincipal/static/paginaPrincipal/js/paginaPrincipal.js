$(document).ready(function() {

    function abrirPopup(url, width, height) {
        var left = (window.innerWidth - width) / 2;
        var top = (window.innerHeight - height) / 2;
        var popupWindow = window.open(url, "popupWindow", 'width=' + width + ', height=' + height + ', top=' + top + ', left=' + left);
        popupWindow.focus();
    }
    
    var crearPlaylist = document.getElementById("crear_playlist");
    crearPlaylist.addEventListener("click", function() {
        abrirPopup('/paginaPrincipal/crear_playlist_inicio/', 600, 1000);
    });
    
    var openPopupButton = document.getElementById("abrirFavoritos");
    openPopupButton.addEventListener("click", function() {
        abrirPopup("/usuarios/mostrar_favoritos/", 1000, 1000);
    });

    var openPopupButton = document.getElementById("abrirPlaylists");
    openPopupButton.addEventListener("click", function() {
        abrirPopup("/usuarios/mostrar_playlists/", 1000, 1000);
    });
 
});
