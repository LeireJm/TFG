from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from .models import Usuario, Playlist, Cancion
from Recomendador_v2 import add_rating, delete_rating, new_ratings
import json

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

                    new_ratings(user.userId)
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
    user = request.user  # Obtén el usuario autenticado

    usuario = Usuario.objects.get(userId=user.userId)

    playlists_usuario = usuario.playlists

    nombres_playlists = []

    for playlist in playlists_usuario:
        p = Playlist.objects.get(playlistId=playlist)
        nombres_playlists.append(p.playlistName)

    return render(request, 'miPerfil.html', {'usuario': usuario, 'playlists': nombres_playlists})

#mostrar favoritos
def mostrarFavoritos(request):
    #aquí contar la cantidad de canciones favoritas que tiene el usuario y pasarle nombre y duración de cada una
    user = request.user  # Obtén el usuario autenticado

    usuario = Usuario.objects.get(userId=user.userId)

    favoritos_usuario = usuario.favoritos

    nombreCanciones = []
    artistaCanciones = []
    duracionCanciones = []

    print("favoritos_usuario", favoritos_usuario)

    for cancion in favoritos_usuario:
        p = Cancion.objects.get(id=cancion)
        nombreCanciones.append(p.track_name)
        artistaCanciones.append(p.artist_name)
        duracionCanciones.append(p.duration_ms)

    nombres_favoritos_json = json.dumps(nombreCanciones)
    artistas_favoritos_json = json.dumps(artistaCanciones)

    print("nombres canciones", nombres_favoritos_json)
    print("artistas: ", artistas_favoritos_json)
    print("duracion:", duracionCanciones)

    datos = {'id_canciones': favoritos_usuario, 'nombre_canciones': nombres_favoritos_json, 'artistas_canciones': artistas_favoritos_json, 'duracion_canciones': duracionCanciones}

    print("datos: ", datos)

    return render(request, 'mostrarFavoritos.html', {'id_canciones': favoritos_usuario, 'nombre_canciones': nombres_favoritos_json,'artistas_canciones': artistas_favoritos_json, 'duracion_canciones': duracionCanciones, 'datos': datos})

#mostrar playlists
def mostrarPlaylists(request):
    #aquí contar la cantidad de playlists que tiene el usuario y pasarle nombre 
    user = request.user  # Obtén el usuario autenticado

    usuario = Usuario.objects.get(userId=user.userId)

    playlists_usuario = usuario.playlists

    nombres_playlists = []

    for playlist in playlists_usuario:
        p = Playlist.objects.get(playlistId=playlist)
        nombres_playlists.append(p.playlistName)

    nombres_playlists_json = json.dumps(nombres_playlists)

    return render(request, 'mostrarPlaylists.html', {'id_playlists': playlists_usuario,'nombres_playlists': nombres_playlists_json})

#mostrar las canciones que contiene una playlist
@csrf_exempt
def mostrarCancionesPlaylist(request, id):

    playlist = Playlist.objects.get(playlistId=id)

    canciones_playlist = playlist.listaCanciones

    nombre_playlist = playlist.playlistName

    nombreCanciones = []
    artistaCanciones = []
    duracionCanciones = []

    for cancion in canciones_playlist:
        p = Cancion.objects.get(id=cancion)
        nombreCanciones.append(p.track_name)
        artistaCanciones.append(p.artist_name)
        duracionCanciones.append(p.duration_ms)

    nombres_favoritos_json = json.dumps(nombreCanciones)
    artistas_favoritos_json = json.dumps(artistaCanciones)

    print("id canciones: ", canciones_playlist)
    print("nombres canciones", nombres_favoritos_json)
    print("artistas: ", artistas_favoritos_json)
    print("duracion:", duracionCanciones)

    datos = {'id_canciones': canciones_playlist, 'nombre_canciones': nombres_favoritos_json, 'artistas_canciones': artistas_favoritos_json, 'duracion_canciones': duracionCanciones}

    print("datos: ", datos)

    return render(request, 'mostrarCancionesPlaylist.html', {'id_canciones': canciones_playlist, 'nombre_playlist': nombre_playlist, 'nombre_canciones': nombres_favoritos_json,'artistas_canciones': artistas_favoritos_json, 'duracion_canciones': duracionCanciones, 'datos': datos})
    # return JsonResponse({'error': 'Se esperaba una solicitud POST y AJAX'})

#eliminar cancion favorita del usuario
@csrf_exempt
def eliminarCancionFav(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        cancion_id = request.POST.get("idCancion")


        cancion_id = int(cancion_id)

        user = request.user
        usuario = Usuario.objects.get(userId=user.userId)
        
        lista_favoritos = usuario.favoritos

        delete_rating(cancion_id, user.userId)

        if cancion_id in lista_favoritos:
            lista_favoritos.remove(cancion_id)
            usuario.save()
            print("Canción eliminada de la lista de favoritos del usuario correctamente.")
        else:
            print("La canción no está en la lista de favoritos del usuario.")

        return JsonResponse({'mensaje': 'Canción eliminada correctamente'})
    return JsonResponse({'error': 'Se esperaba una solicitud POST y AJAX'})

#añadir cancion favorita del usuario
@csrf_exempt
def anadirCancionFav(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        cancion_id = request.POST.get("idCancion")
        cancion_id = int(cancion_id)

        user = request.user
        usuario = Usuario.objects.get(userId=user.userId)
        lista_favoritos = usuario.favoritos

        print("id de la cancion que vamos a añadir", cancion_id)

        add_rating(cancion_id, user.userId)

        if cancion_id not in lista_favoritos:

            print("lista favoritos antes:", lista_favoritos)
            
            lista_favoritos.append(cancion_id)
            usuario.save()

            print("lista favoritos despues:", lista_favoritos)

            if cancion_id in lista_favoritos:
                print("Canción añadida de la lista de favoritos del usuario correctamente.")
            else:
                print("Canción no añadida a la lista de favoritos del usuario.")
        else:
            print("La canción ya está en favoritos")

        return JsonResponse({'mensaje': 'Canción añadida correctamente'})
    return JsonResponse({'error': 'Se esperaba una solicitud POST y AJAX'})
