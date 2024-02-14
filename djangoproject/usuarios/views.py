from django.shortcuts import render
from .models import Usuario 

def index(request):
    usuarios = Usuario.objects.all()  # Consulta la base de datos

    cantidad_canciones = usuarios.count() 

    return render(request, 'inicioSesion.html', {'usuarios': usuarios, 'cantidad_usuarios': cantidad_canciones})

def registro(request):
    return render(request, 'registro.html')