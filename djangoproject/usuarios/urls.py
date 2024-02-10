from django.urls import path

#rutas -> poner carpeta y archivo import nombre de la funcion
from . import views

#path ('lo de aquí es la ruta en la url', ), es decir, si pongo perfil/ significa que en la web es noseque/perfil

urlpatterns = [
    path('', views.index, name='index'),
]