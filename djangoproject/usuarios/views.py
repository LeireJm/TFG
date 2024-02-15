from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from .models import Usuario 

#muestra la pantalla de inicio de sesión
def index(request):
    usuarios = Usuario.objects.all()  # Consulta la base de datos

    cantidad_canciones = usuarios.count() 

    return render(request, 'inicioSesion.html', {'usuarios': usuarios, 'cantidad_usuarios': cantidad_canciones})

#muestra la pantalla de registro
def registro(request):
    return render(request, 'registro.html')

def login(request):
    error_message = ''
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        print("email", email)
        print("password", password)
        
        # Autenticar al usuario
        #user = authenticate(request, email=email, password=password)

        try:
            user = Usuario.objects.get(email=email)
            # El usuario se encontró en la base de datos
        except Usuario.DoesNotExist:
            # El usuario no se encontró en la base de datos
            user = None  # o cualquier otra acción que desees realizar en este caso

        print("user", user)

        if password == user.password:
            return redirect('/lista_canciones') #si es correcto, se inicia la sesión
        else:
            error_message = 'Credenciales inválidas. Por favor, inténtalo de nuevo.' #no se ha conseguido iniciar sesión

        # if user is not None:
        #     if user.is_authenticated:
        #         login(request, user)
        #         return redirect('/')
        # else:
        #     error_message = 'Credenciales inválidas. Por favor, inténtalo de nuevo.' #no se ha conseguido iniciar sesión
    
    return render(request, 'inicioSesion.html', {'error_message': error_message})