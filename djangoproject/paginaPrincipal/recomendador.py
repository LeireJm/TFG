#!/usr/bin/env python
# coding: utf-8

# ## Recomendador básico


# Importamos las bibliotecas necesarias para nuestro recomendador

# In[2]:


# Cargamos las librerías necesarias de Pandas
import pandas as pd
import numpy as np

# In[3]:


# Cargamos las librerías necesarias de Surprise
from surprise import Dataset
from surprise import Reader
from surprise import KNNBasic
from surprise.model_selection import train_test_split
from surprise.model_selection import cross_validate
from surprise import accuracy

from .models import Cancion


# Cargamos el dataset en pandas para luego pasarlo a surprise

# In[4]:


# Cargamos el CSV con el dataframe de Pandas
df = pd.read_csv('songs_dataset.csv')

reader = Reader(rating_scale=(1, 30))

# Vamos a transformar los distintos géneros a números para que el recomendador funcione por recomendación por género
# Con esto evitamos los repetidos
distinct_genres = df['top genre'].unique()

# Asignamos números a los géneros
value_to_number = {genre: i+1 for i, genre in enumerate(distinct_genres)}

# Creamos una nueva columna que es la misma que géneros pero en números
df['genre number'] = df['top genre'].map(value_to_number)

# Load the Pandas DataFrame into a Surprise Dataset
data = Dataset.load_from_df(df[['artist', 'title', 'genre number']], reader)


# In[107]:


df


# Entrenar los datos

# In[108]:


# Crear un modelo modelo k-NN
sim_options = {
    'name': 'cosine',  
    'user_based': False  # Recomendador basado en contenidos
}
clf = KNNBasic(sim_options=sim_options, k=50, verbose=True)


# In[ ]:


#Measures probar con RMSE o MAE, cuál sea el mejor
cv = cross_validate(clf, data, measures=['RMSE', 'MAE'], cv=7, verbose=True)


# Función para determinar canciones similares

# In[ ]:


#Para hacer la búsqueda si la canción está en los datos entrenados
items_ids = [clf.trainset.to_raw_iid(iid) for iid in clf.trainset.all_items()]


# In[ ]:


def get_similar_songs(song_title, k=10):
    try: 
        # Comprueba si la canción está en los datos entrenados
        if song_title not in items_ids:
            return []  # Devuelve una lista vacía si no está entre los datos entrenados

        # Obtiene el id de la canción para luego pasarlo al algoritmo
        song_id = clf.trainset.to_inner_iid(song_title)

        # Usa el modelo k-NN para encontrar canciones similares
        similar_items = clf.get_neighbors(song_id, k)

        # Una vez tiene los ids de las canciones similares se pasa a los nombres reales de las canciones
        similar_songs = [clf.trainset.to_raw_iid(item_id) for item_id in similar_items]

        return similar_songs

    except IndexError as e:
        return []


# Generar una "playlist" random con 10 canciones

# In[ ]:


import random

random_songs = df.sample(n=10)


# In[ ]:


random_songs


# Conseguir las recomendaciones 

# In[ ]:


similar_songs = []

for song_title in random_songs['title']:
    sim_songs = get_similar_songs(song_title, k=10)    
    
    #Para evitar canciones ya recomendadas antes
    for s in sim_songs:
        if s not in similar_songs:
            similar_songs.append(s)


# In[ ]:


similar_songs


# Vamos a probar recomendación con una canción

# In[ ]:


similar_songs = get_similar_songs('Find U Again (feat. Camila Cabello)', k=10)
similar_songs


# #### Recomendador sin surprise
# Dado una canción o el nombre de un artista, se recomienda más canciones del artista (en el caso de por canción no se recomienda esa canción)

# In[5]:


df = df.sort_values(by='pop') # ordena por popularidad
df2_grouped = df.groupby('artist') # pone las canciones del mismo artista juntos
df3_grouped = df.groupby('top genre') # por géneros porque en el caso de que no haya suficientes del mismo artista será por las canciones más populares del género

df2 = pd.DataFrame()
for key, group in df2_grouped:
    df2 = pd.concat([df2, group], axis=0)

df3 = pd.DataFrame()
for key, group in df3_grouped:
    df3 = pd.concat([df3, group], axis=0)


# In[6]:


df2.loc[df2['top genre'] == "dance pop"]


# In[7]:


def recommender_by_artist(artist, song_excl):
    songs = df2.loc[df2['artist'] == artist]
    if song_excl != None: 
        songs_ret = songs.loc[songs['title'] != song_excl, ['id', 'title', 'artist', 'top genre']]
        return songs_ret
    else: 
        return songs[['id', 'title', 'artist', 'top genre']]


# In[8]:


def recommender_by_genre(genre, song_excl):
    songs = df3.loc[df3['top genre'] == genre]
    if song_excl != None: 
        songs_ret = songs.loc[songs['title'] != song_excl, ['id', 'title', 'artist', 'top genre']]
        return songs_ret
    else: 
        return songs[['id', 'title', 'artist', 'top genre']]


# In[15]:


def get_id(songs):
    return songs.id  


# In[16]:


def recommender_manual(song_artist):
    if Cancion.objects.filter(id=song_artist).exists(): #lo que se ha pasado por parámetro es el título de la canción
        print("11111111111111\n")
        cancion = Cancion.objects.get(id=song_artist)
        artist = cancion.artist
        song_name = cancion.title
        
        songs = recommender_by_artist(artist, song_name)

        if len(songs) < 10:
            genre = cancion.top_genre
            songs_genre = recommender_by_genre(genre, song_name)
            
            songs_ret = pd.concat([songs, songs_genre])[:10]

            return get_id(songs_ret)
        
        elif len(songs) > 10:
            return get_id(songs[:10])
        
        else:
            return get_id(songs)
        
    elif song_artist in df['artist'].values: #se ha pasado por parámetro el nombre del artista
        print("2222222222222222222222\n")
        songs = recommender_by_artist(song_artist, None)

        return get_id(songs[:10]) #no hay genero asociado por artista, lo que muestre si hay 15 o menos del artista 
    else: #no exista tal artista o canción
        print("Error: no existe tal artista o canción en la base de datos\n")
        return []


# In[17]:


def recommender_no_surprise(songs_arists):
    songs = []
    for song_artist in songs_arists:
        songs_aux = recommender_manual(song_artist)
        songs.extend(songs_aux)
    
    return songs


# In[18]:


# recommender_manual(174) # "#thatPower"


# In[23]:
#

#recommender_manual('Rihanna')


# In[22]:


#recommender_no_surprise([174, 'Rihanna'])

