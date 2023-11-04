from django.shortcuts import render
from .models import Cancion  
import csv

# Create your views here.
def index(request):
    return render(request, 'index.html')

def cargar_csv(request):
    cancion = Cancion(title="Cancion de ejemplo", artist="Artista de ejemplo", top_genre="Género de ejemplo", year=2023, dur=180, pop=90)
    cancion.save()

    if request.method == 'POST':
        archivo_csv = request.FILES['songs_dataset.csv']
        
        with archivo_csv.open() as csvfile:
            csv_data = csv.reader(csvfile)
            for row in csv_data:
                cancion = Cancion(
                    title=row['title'],
                    artist=row['artist'],
                    # ... otros campos ...
                )
                cancion.save()


        canciones = Cancion.objects.all()
        return render(request, 'canciones.html', {'canciones': canciones})
    
    canciones = Cancion.objects.all()
    cantidad_canciones = canciones.count() 
    return render(request, 'canciones.html', {'canciones': canciones, 'cantidad_canciones': cantidad_canciones})