from django.urls import path
from paginaPrincipal import views as viewsPaginaPrincipal

#rutas -> poner carpeta y archivo import nombre de la funcion
from . import views

#path ('lo de aquí es la ruta en la url', ), es decir, si pongo perfil/ significa que en la web es noseque/perfil

urlpatterns = [
    path('', views.index, name='index'),
    path('registro/', views.registro, name='registro'),
    path('login/', views.login, name='login'),

    #si el inicio es correcto, lleva a la página principal de la aplicación
    path('pagina_principal/', viewsPaginaPrincipal.pagina_principal, name='paginaPrincipal')
    
]