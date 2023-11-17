from django.shortcuts import render
from .models import Cancion  
from random import sample
from django.http import HttpResponse
from .recomendador import recommender_no_surprise
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import csv
import os


# Create your views here.
def index(request):
    return render(request, 'index.html')

def lista_canciones(request):
    #para mostrar todas las canciones.
    canciones = Cancion.objects.all()  # Consulta la base de datos
    cantidad_canciones = canciones.count() 

    #lo que queremos es mostrar diez canciones aleatorias.
    random_songs = sample(list(Cancion.objects.all()), 10)

    return render(request, 'canciones.html', {'canciones': random_songs, 'cantidad_canciones': cantidad_canciones})

@csrf_exempt
def recomendar_canciones(request):
    if request.method == "POST" and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        canciones_seleccionadas = request.POST.getlist("canciones[]", [])
        print("CANCIONES SELECCIONADAS\n")
        print(canciones_seleccionadas)
        canciones_similares = recommender_no_surprise(canciones_seleccionadas)
        print("CANCIONES SELECCIONADAS\n")

        return JsonResponse({"recomendaciones": canciones_similares})

    # try:
    #     # Lógica principal aquí
    #     canciones_seleccionadas = request.POST.getlist("canciones[]", [])
    #     canciones_similares = recommender_no_surprise(canciones_seleccionadas)

    #     return JsonResponse({"recomendaciones": canciones_similares})

    # except Exception as e:
    #     print(f"Error en la vista recomendar_canciones: {e}")
    #     return JsonResponse({"error": "Error interno del servidor"}, status=500)

def cargar_csv(request):
    #cancion = Cancion(title="Roar", artist="Katty Pe", top_genre="Género de ejemplo", year=2023, dur=180, pop=90)
    #cancion.save()

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