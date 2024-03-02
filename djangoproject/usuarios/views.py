from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Usuario 

#muestra la pantalla de inicio de sesión (cuando /usuarios)
def index(request):
    usuarios = Usuario.objects.all()  # Consulta la base de datos

    cantidad_canciones = usuarios.count() 

    return render(request, 'inicioSesion.html', {'usuarios': usuarios, 'cantidad_usuarios': cantidad_canciones})

#muestra la pantalla de registro
def registro(request):
    return render(request, 'registro.html')

#después de la pantalla de registro, validamos los dato introducidos
def validarRegistro(request):
    error_message = ''
    if request.method == 'POST':
        email = request.POST.get('email')
        userName = request.POST.get('userName')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        
        print("email:", email)
        print("userName:", userName)
        print("password:", password)
        print("password2:", password2)

    
        #no se han rellenado todos los campos
        if email == '' or userName == '' or password == '' or password2 == '': 
            error_message = 'Por favor, rellena todos los campos'

        #el correo ya está en uso
        if Usuario.objects.filter(email=email).exists():
            error_message = 'Ya hay una cuenta con ese correo electrónico'
        else: #el correo no está en uso
            if Usuario.objects.filter(userName=userName).exists(): #el nombre de usuario ya está en uso
                error_message = 'El nombre de usuario ya existe. Intente con otro'
            else: #el nombre de usuario no está en uso
                if password != password2: #si las contraseñas no coinciden
                    error_message = 'Las contraseñas proporcionadas no coinciden'
                else: #está todo perfecto
                    #miramos el id del usuario anterior
                    ultimo_usuario = Usuario.objects.order_by('-userId').first()

                    nuevo_id = ultimo_usuario.userId + 1 if ultimo_usuario else 1

                    new_user = Usuario(userId=nuevo_id, userName=userName, email=email, password=password, favoritos=[], playlists=[])
                    new_user.save()  # Guardar el nuevo usuario en la base de datos

                    #autenticar usuario
                    user = authenticate(request, email=email, password=password)
                    login(request, user)
                    return redirect('/paginaPrincipal')  # Redirige a la página principal si el registro es exitoso



    return render(request, 'registro.html', {'error_message': error_message})

#iniciar sesión
def loginUser(request):
    error_message = ''
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if password == '' and email == '':
            error_message = 'Por favor, escribe correo y contraseña'
        elif password == '':
            error_message = 'Por favor, escribe la contraseña'
        else:
            print("email", email)
            print("password", password)
            try:
                user = Usuario.objects.get(email=email)
                if password == user.password:# El usuario se encontró en la base de datos
                    user = authenticate(request, email=email, password=password)
                    print("USUARIO:", user)
                    print("user id:", user.get_userId())
                    if user is not None:
                        login(request, user)
                        return redirect('/paginaPrincipal')  # Redirige a la página principal si el inicio de sesión es exitoso
                    else:
                        error_message = 'Credenciales inválidas. Por favor, inténtalo de nuevo.'
                else:
                    error_message = 'Credenciales inválidas. Por favor, inténtalo de nuevo.' #no se ha conseguido iniciar sesión     
            except Usuario.DoesNotExist: # El usuario no se encontró en la base de datos
                error_message = 'Credenciales inválidas. Por favor, inténtalo de nuevo.' #no se ha conseguido iniciar sesión    
        
    return render(request, 'inicioSesion.html', {'error_message': error_message})

# cerrar sesión
def logoutUser(request):
    logout(request)
    return redirect('/paginaPrincipal')

# perfil del usuario
def perfil(request):
    usuario = request.user  # Obtén el usuario autenticado
    return render(request, 'miPerfil.html', {'usuario': usuario})
