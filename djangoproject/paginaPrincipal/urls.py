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
    path('crear_playlist/', views.crear_playlist, name='crear_playlist'),

    path('miPerfil/', viewsUsuarios.perfil, name='miPerfil'),
]