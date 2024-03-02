from django.shortcuts import render
from .models import Cancion 
from .models import Rating 
from random import sample
from django.http import HttpResponse
from .recomendador_v2 import recommender
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from usuarios.models import Playlist, Usuario

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

    usuario = Usuario.objects.get(userId=user.userId)

    

    # Crear una nueva instancia de Playlist
    # nueva_playlist = Playlist(
    #     playlistId= 2,  # Asigna el ID de la nueva playlist (puedes ajustarlo según sea necesario)
    #     playlistName="playlist de prueba 2",  # Asigna el nombre de la nueva playlist
    #     listaCanciones=[1, 2, 3]  # Lista de IDs de canciones (ajusta según sea necesario)
    # )

    # # # Guardar la nueva instancia en la base de datos
    # nueva_playlist.save()

    # playlist_existente = Playlist.objects.get(playlistId=1)

    # # Agregar canciones a la lista de canciones existente
    # canciones_a_agregar = [4, 5, 6]  # IDs de las nuevas canciones
    # playlist_existente.listaCanciones.extend(canciones_a_agregar)
    # playlist_existente.save()

    playlists_usuario = usuario.playlists

    nombres_playlists = []

    for playlist in playlists_usuario:
        p = Playlist.objects.get(playlistId=playlist)
        nombres_playlists.append(p.playlistName)


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

def crear_playlist(request):
    return render(request, 'crearPlaylist.html')

def cargar_csv(request):
    archivo_csv = os.path.join(os.path.dirname(__file__), 'songs_dataset.csv')
    
    with open(archivo_csv, 'r', newline='', encoding='utf-8') as csvfile:
        csv_data = csv.reader(csvfile)
        
        #salta la primera linea
        next(csv_data, None)
        for row in csv_data:

            cancion = Cancion(
                title=row[1],
                artist=row[2],
                top_genre = row[3],
                year = row[4],
                bpm = row[5],
                nrgy = row[6],
                dnce = row[7],
                dB = row[8],
                live = row[9],
                val = row[10],
                dur = row[11],
                acous = row[12],
                spch = row[13],
                pop = row[14],
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