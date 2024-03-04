from django.urls import path
from paginaPrincipal import views as viewsPaginaPrincipal

#rutas -> poner carpeta y archivo import nombre de la funcion
from . import views

#path ('lo de aquí es la ruta en la url', ), es decir, si pongo perfil/ significa que en la web es noseque/perfil

urlpatterns = [
    path('', views.index, name='index'),
    
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('miPerfil/', views.perfil, name='miPerfil'),


    path('registro/', views.registro, name='registro'),
    path('registro/validarRegistro/', views.validarRegistro, name='validar_registro'),

    path('mostrar_favoritos/', views.mostrarFavoritos, name='mostrar_favoritos'),
    path('mostrar_playlists/', views.mostrarPlaylists, name='mostrar_playlists'),

    #si el inicio es correcto, lleva a la página principal de la aplicación
    path('paginaPrincipal/', viewsPaginaPrincipal.pagina_principal, name='paginaPrincipal')
    
]