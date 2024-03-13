from django.shortcuts import render
from .models import Cancion 
from .models import Rating 
from random import sample
from django.http import HttpResponse
from .Recomendador_v2_antiguo import recommender
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from usuarios.models import Playlist, Usuario

import random
import csv
import os
import json
import pandas as pd

opciones_globales = []


def index(request):
    return render(request, 'index.html')

#página principal
def pagina_principal(request):
    user = request.user

    if user.is_authenticated:
        usuario = Usuario.objects.get(userId=user.userId)
        playlists_usuario = usuario.playlists

        nombres_playlists = []

        for playlist in playlists_usuario:
            p = Playlist.objects.get(playlistId=playlist)
            nombres_playlists.append(p.playlistName)
    else:
        return render(request, 'paginaPrincipal.html')

   

    return render(request, 'paginaPrincipal.html', {'playlists': nombres_playlists})

#lista de canciones (recomendador)
def lista_canciones(request):
    global opciones_globales

    #para mostrar todas las canciones desde la base de datos
    canciones = Cancion.objects.all()  # Consulta la base de datos
    cantidad_canciones = canciones.count() 

    opciones_globales = request.GET.getlist("options")

    #lo que queremos es mostrar diez canciones aleatorias.
    random_songs = sample(list(Cancion.objects.all()), 10)

    # songs = pd.read_csv('spotify_data_mod3.csv')
    # cantidad_canciones = songs.count() 
    # random_songs = sample(list(songs), 10)
    # print("RANDOM SONGS")
    # print(songs)

    return render(request, 'canciones.html', {'canciones': random_songs, 'cantidad_canciones': cantidad_canciones})

def crear_playlist_inicio(request):
    return render(request, 'crearPlaylist.html', {"opcion": 0})

def crear_playlist(request):

    user = request.user

    usuario = Usuario.objects.get(userId=user.userId)

    if request.method == 'POST':
        nombre = request.POST.get('nombre')

        # Crear una nueva playlist en la base de datos
        ultima_playlist = Playlist.objects.order_by('-playlistId').first()

        nueva_id = ultima_playlist.playlistId + 1 if ultima_playlist else 1

        print("nueva ID: ",  nueva_id)

        nueva_playlist = Playlist( playlistId= nueva_id, playlistName=nombre, listaCanciones=[])

        nueva_playlist.save()

        #meto la playlist nueva en las playlists del usuario
        usuario.playlists.append(nueva_id)
        usuario.save()
   

    favoritos_usuario = usuario.favoritos
    
    #una canción aleatoria de entre las favoritas del usuario
    cancionAMostrar = random.choice(favoritos_usuario)

    cancion = Cancion.objects.get(id=cancionAMostrar)
    idCancion = cancion.id
    nombre = cancion.track_name
    artista = cancion.artist_name

    return render(request, 'crearPlaylist.html', {"nombre": nombre, "artista": artista, "id": idCancion , "opcion": 1, 'playlistId': nueva_id})

@csrf_exempt
def contarCancionesPlaylist(request):
    if request.method == "POST" and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        playlist_id = request.POST.get('playlistId')

        print("playlist id newww: ", playlist_id)

        #hasta aqui bien
        
        playlist = Playlist.objects.get(playlistId=playlist_id)

        num_canciones = len(playlist.listaCanciones)

        return JsonResponse({'num_canciones': num_canciones})

    return JsonResponse({'error': 'Se esperaba una solicitud POST y AJAX'})

@csrf_exempt
def porPopularidad(request):
    if request.method == "POST" and request.headers.get('X-Requested-With') == 'XMLHttpRequest':

        #cojo las 50 más populares y saco 20 de ellas de manera aleatoria
        canciones_populares = Cancion.objects.order_by('-popularity')[:50]

        canciones_aleatorias = random.sample(list(canciones_populares), 20)

        datos = []
        for cancion in canciones_aleatorias:
            datos.append({
                'track_name': cancion.track_name,
                'artist_name': cancion.artist_name,
                'id': cancion.id,
            })

        return JsonResponse({'canciones': datos})

    return JsonResponse({'error': 'Se esperaba una solicitud POST y AJAX'})

@csrf_exempt
def meterCancionPlaylist(request):
    if request.method == "POST" and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        idCancionNueva = request.POST.get("cancion")
        playlistId = request.POST.get("playlistId")

        print("cancion nueva:", idCancionNueva)
        print("playlist id:", playlistId)
        
        playlist_actual = Playlist.objects.get(playlistId=playlistId)

        #Agregar canciones a la lista de canciones existente
        playlist_actual.listaCanciones.append(idCancionNueva)

        #luego comentar
        playlist_actual.save()

        return JsonResponse({'mensaje': 'Solicitud AJAX exitosa'})
    else:
        return JsonResponse({'error': 'Solicitud no válida'})




@csrf_exempt
def recomendar_canciones(request):
    global opciones_globales

    if request.method == "POST" and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        canciones_seleccionadas = request.POST.getlist("canciones[]", [])

        opciones = opciones_globales
        print("OPCIONES")
        print(opciones)
        
        print("CANCIONES SELECCIONADAS AHORA")
        print(canciones_seleccionadas)

        canciones_similares = recommender(canciones_seleccionadas, opciones) #pasamos la cancion seleccionada y las opciones

        
        canciones_similares_JSON = canciones_similares.to_json(orient='records')
        print("\nCANCIONES SIMILARES\n")
        print(canciones_similares_JSON)

        # canciones_similares_list = [int(item) for item in canciones_similares]
        # print(canciones_similares_list)

        #recomendaciones_dict = [serie.to_dict() for serie in canciones_similares]
        #return HttpResponse({"recomendaciones": canciones_similares_JSON})

        ####EL PROBLEMA ES QUE SE PASA UN DATAFRAME A UN JSON

        return JsonResponse({"recomendaciones": canciones_similares_JSON})


def cargar_csv(request):
    archivo_csv = os.path.join(os.path.dirname(__file__), 'spotify_data_mod_llaves.csv')
    
    with open(archivo_csv, 'r', newline='', encoding='utf-8') as csvfile:
        csv_data = csv.reader(csvfile)
        
        #salta la primera linea
        next(csv_data, None)
        for row in csv_data:

            cancion = Cancion(
                artist_name=row[1],
                track_name = row[2],
                track_id = row[3],
                popularity = row[4],
                year = row[5],
                genre = row[6],
                danceability = row[7],
                energy = row[8],
                key = row[9],
                loudness = row[10],
                mode = row[11],
                speechiness = row[12],
                acousticness = row[13],
                instrumentalness = row[14],
                liveness = row[15],
                valence = row[16],
                tempo = row[17],
                duration_ms = row[18],
                time_signature = row[19],
                genres = row[20],
            )
            cancion.save()

    return render(request, 'canciones.html')

def cargar_rating(request):
    archivo_csv = os.path.join(os.path.dirname(__file__), 'rating2.csv')
    
    with open(archivo_csv, 'r', newline='', encoding='utf-8') as csvfile:
        csv_data = csv.reader(csvfile)
        
        #salta la primera linea
        next(csv_data, None)
        for row in csv_data:

            rating = Rating(
                userId=row[0],
                songId=row[1],
                rating=row[2],
                timestamp = row[3],   
            )
            rating.save()

    return render(request, 'canciones.html')