from django.urls import path
from usuarios import views as viewsUsuarios

#rutas -> poner carpeta y archivo import nombre de la funcion
from . import views

#path ('lo de aquí es la ruta en la url', ), es decir, si pongo perfil/ significa que en la web es noseque/perfil

urlpatterns = [
    # path('', views.index, name='index'),
    path('carga_csv/', views.cargar_csv, name='carga CSV'),
    path('cargar_rating/', views.cargar_rating, name='carga rating'),
    path('', views.pagina_principal, name='paginaPrincipal'),
    path('lista_canciones/', views.lista_canciones, name='lista_canciones'),
    path('recomendar_canciones/', views.recomendar_canciones, name='recomendar_canciones'),

    path('crear_playlist_inicio/', views.crear_playlist_inicio, name='crear_playlist_inicio'),
    path('crear_playlist/', views.crear_playlist, name='crear_playlist'),
    # path('crear_playlist/contarCancionesPlaylist/', views.contarCancionesPlaylist, name='contar_canciones'),
    path('crear_playlist/contarCancionesPlaylist/porPopularidad', views.porPopularidad, name='por_popularidad'),
    path('crear_playlist/estaEnFavoritos', views.estaEnFavoritos, name='estaEnFavoritos'),

    path('descubrir_opciones/', views.descubrir_opciones, name='descubrir_opciones'),
    path('descubrir_listaCanciones/', views.descubrir_listaCanciones, name='descubrir_listaCanciones'),
    path('descubrir_listaCanciones/tratarResultado', views.descubrir_tratarResultado, name='descubrir_tratarResultado'),
    path('descubrir_listaCanciones/ponerNombre', views.descubrir_ponerNombre, name='descubrir_ponerNombre'),
    path('descubrir_listaCanciones/pasarCanciones', views.descubrir_pasarCanciones, name='descubrir_pasarCanciones'),

    path('meterCancionPlaylist/', views.meterCancionPlaylist, name='meterCancionPlaylist'),

    path('miPerfil/', viewsUsuarios.perfil, name='miPerfil'),
    path('mostrar_favoritos/', viewsUsuarios.mostrarFavoritos, name='mostrar_favoritos'),
    path('mostrar_playlists/', viewsUsuarios.mostrarPlaylists, name='mostrar_playlists'),
]