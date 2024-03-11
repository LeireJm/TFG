#!/usr/bin/env python
# coding: utf-8

# ## Recomendador con filtrado colaborativo

# Recomendador sin usar el framework de Surprise

# ### Carga de datos

# Es necesario importar las librerías para nuestro recomendador.


import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import euclidean_distances

# Comenzamos cargando los datasets de las canciones junto a los ratings. El archivo original del dataset de las canciones incluía 1.2 millones de canciones por lo que se ha reducido el dataset a 50000 porque al no usar librerías específicas como Surprise no es eficiente y sobrepasa el uso de la memoria si utilizamos el dataset no reducido.

import os

# script_dir = os.path.dirname('C:/hlocal/TFG CODIGO/TFG/djangoproject/paginaPrincipal/spotify_data_mod3.csv')
# file_path = os.path.join(script_dir, 'spotify_data_mod3.csv')

# songs = pd.read_csv(file_path)

# #songs = pd.read_csv('spotify_data_mod3.csv')
# #songs = pd.read_csv('spotify_data_red.csv') Solo un género
# #songs = pd.read_csv('spotify_data.csv') Dataset original

# script_dir2 = os.path.dirname('C:/hlocal/TFG CODIGO/TFG/djangoproject/paginaPrincipal/rating2.csv')
# file_path2 = os.path.join(script_dir2, 'rating2.csv')

# ratings = pd.read_csv(file_path2)


###REALMENTE NO HACE FALTA QUE COGER LOS DATOS DEL CSV PORQUE YA LOS HEMOS CARGADO
songs = pd.read_csv('spotify_data_mod_llaves.csv')
ratings = pd.read_csv('rating2.csv')


# ### Explicación de los atributos de las canciones

# cargamos las primeras filas para ver las columnas del dataset
# songs.head()

# Definición de los atributos
# - artist_name: nombre del artista
# - track_name: nombre de la canción
# - track_id: id único de la canción es Spotify
# - popularity: cuanto más alto es el valor, más popular es la canción (0-100)
# - year: año de lanzamiento de la canción
# - genre: género de la canción
# - danceability: describe lo adecuada que es una pista para bailar basándose en una combinación de elementos musicales como el tempo, la estabilidad del ritmo, la fuerza del compás y la regularidad general. Un valor de 0.0 es el menos bailable y 1.0 el más bailable (0.0-1.0)
# - energy: medida que representa una medida perceptiva de intensidad y actividad (0.0-1.0)
# - key: tonalidad de la pista y los números enteros se asignan a tonos utilizando la notación estándar Pitch Class. Por ejemplo, 0 = C, 1 = C♯/D♭, 2 = D, y así sucesivamente. Si no se detectó ninguna clave, el valor es -1 (-1-10)
# - loudness: en decibelios (dB). Los valores de sonoridad se promedian en toda la pista y son útiles para comparar la sonoridad relativa de las pistas. La sonoridad es la cualidad de un sonido que es el principal correlato psicológico de la fuerza física (amplitud). Los valores suelen oscilar entre -60 y 0 db (-60-0dB)
# - mode: indica la modalidad (mayor o menor) de una pista, el tipo de escala del que se deriva su contenido melódico. Mayor se representa con 1 y menor con 0
# - speechiness: detecta la presencia de palabras habladas en una pista. Cuanto más exclusivamente hablada sea la grabación (por ejemplo, programa de entrevistas, audiolibro, poesía), más se acercará a 1.0 el valor del atributo. Los valores superiores a 0,66 describen pistas que probablemente estén compuestas en su totalidad por palabras habladas. Los valores entre 0.33 y 0.66 describen pistas que pueden contener tanto música como voz, ya sea en secciones o en capas, incluyendo casos como la música rap. Los valores inferiores a 0.33 representan probablemente música y otras pistas no habladas
# - acousticness: medida de confianza de 0.0 a 1.0 de si la pista es acústica. 1,0 representa una confianza alta en que la pista es acústica (0.0-1.0)
# - instrumentalness: predice si una pista no contiene voces. Los sonidos "ooh" y "aah" se consideran instrumentales en este contexto. Las pistas de rap o spoken word son claramente "vocales". Cuanto más se acerque el valor de instrumental a 1.0, mayor será la probabilidad de que la pista no contenga voces. Los valores superiores a 0.5 representan pistas instrumentales, pero la confianza es mayor a medida que el valor se acerca a 1.0 (0.0-1.0)
# - liveness: detecta la presencia de público en la grabación. Los valores de liveness más altos representan una mayor probabilidad de que la pista se haya interpretado en directo. Un valor superior a 0.8 indica una gran probabilidad de que la pista se haya grabado en directo (0.0-1.0)
# - valence: medida de 0.0 a 1.0 que describe la positividad musical que transmite una pista. Las pistas con valencia alta suenan más positivas (por ejemplo, felices, alegres, eufóricas), mientras que las pistas con valencia baja suenan más negativas (por ejemplo, tristes, deprimidas, enfadadas) (0.0-1.0)
# - tempo: en pulsaciones por minuto (BPM). En terminología musical, el tempo es la velocidad o el ritmo de una pieza determinada y se deriva directamente de la duración media del compás
# - duration_ms: duración de la pista en milisegundos
# - time_signature: convención notacional para especificar cuántos tiempos hay en cada compás (3-7)

# ### Recomendación de géneros


# Hay que llamar esta función al iniciar la aplicación
def cosine_genre():
    # Eliminar los caracteres "{" y "}"
    songs['genres'] = songs['genres'].str.replace('{', '').str.replace('}', '')
    #print(songs['genres'])

    # Dividir la columna 'genres' por comas
    songs['genres'] = songs['genres'].apply(lambda x: x.split(","))
    #songs['genres'] = songs['genres'].apply(lambda x: x.split("|"))
    
    col_del = ["songId",	"artist_name",	"track_name",	"track_id", "popularity", "year", "genre",	"danceability",	"energy",	"key",	"loudness",	"mode",	"speechiness",	"acousticness",	"instrumentalness",	"liveness",	"valence",	"tempo",	"duration_ms",	"time_signature", "genres"]

    songsAux = songs.copy()

    genre = set(g for G in songsAux['genres'] for g in G)

    for g in genre:
        songsAux[g] = songsAux.genres.transform(lambda x: int(g in x))
        
    song_genre = songsAux.drop(columns=col_del)

    cosine_sim_genre = cosine_similarity(song_genre, song_genre)

    return cosine_sim_genre

# song_genre.head()


cosine_sim_genre = cosine_genre()
#print(f"Dimensiones de la matriz de similitud del coseno entre los géneros: {cosine_sim_genre.shape}")


# ### Recomendador Filtrado Colaborativo

# Código tomado de los apuntes de la directora del TFG.

# El filtrado colaborativo se basa en recomendaciones por personas de gustos similares.
# 
# Vamos a crear una matriz de dispersión o de utilidad (usuario-elemento), para ello hemos creado la función create_X().


def create_X(df):
    """
    Genera una matriz dispersa a partir del marco de datos de calificaciones.
    
    Argumentos:
        df: dataframe de pandas que contiene 3 columnas (userId, songId, rating)
    
    Devoluciones:
        X: matriz dispersa
        user_mapper: dict que asigna las identificaciones de usuario a los índices de usuario
        user_inv_mapper: dict que asigna índices de usuario a ID de usuario
        song_mapper: dict que asigna las identificaciones de canciones a los índices de canciones
        song_inv_mapper: dict que asigna índices de canciones a ID de canciones
        
    """
    print(df.columns)
    
    M = df["userId"].nunique()
    N = df["songId"].nunique()

    user_mapper = dict(zip(np.unique(df["userId"]), list(range(M))))
    song_mapper = dict(zip(np.unique(df["songId"]), list(range(N))))
    
    user_inv_mapper = dict(zip(list(range(M)), np.unique(df["userId"])))
    song_inv_mapper = dict(zip(list(range(N)), np.unique(df["songId"])))
    
    user_index = [user_mapper[i] for i in df["userId"]]
    item_index = [song_mapper[i] for i in df["songId"]]

    X = csr_matrix((df["rating"], (user_index,item_index)), shape=(M,N))
    
    return X, user_mapper, song_mapper, user_inv_mapper, song_inv_mapper

X, user_mapper, song_mapper, user_inv_mapper, song_inv_mapper = create_X(ratings)


# #### Dispersión

# La dispersión se calcula dividiendo el número de elementos almacenados en la matriz entre el número total de elementos.

# n_total = X.shape[0]*X.shape[1]
# n_ratings = X.nnz
# sparsity = n_ratings/n_total
# print(f"Matrix sparsity: {round(sparsity*100,2)}%")


# Vemos que hay un 6% de dispersión que no es mucho y eso indica que el resto tienen problema cold-start (no todas las canciones están calificadas y entonces esas canciones se recomiendan menos)

n_ratings_per_song = X.getnnz(axis=0)

# print(f"Hay {len(n_ratings_per_song)} canciones con ratings.")


# #### Normalización de datos

# Vamos a calcular la media de puntuación de cada canción. Hay que recordar que las calificaciones son 0 o 1, es decir, no le gusta o le gusta al usuario.

#Calcula la media por canción
sum_ratings_per_song = X.sum(axis=0)
mean_rating_per_song = sum_ratings_per_song/n_ratings_per_song

#Crear una nueva matriz con la media de valoración
X_mean_song = np.tile(mean_rating_per_song, (X.shape[0],1))
X_mean_song.shape 
#Vamos a ver el tamaño de la matriz que será usuarios x canciones valoradas

#Normalizamos los datos
X_norm = X - csr_matrix(X_mean_song)

# Veamos ahora como están los valores nuevos
# print("Original X:", X[0].todense())
# print("Normalized X:", X_norm[0].todense())


# #### Recomendador filtrado colaborativo Item-Item con k-NN

# Ahora vamos a hacer el recomendador como tal que será mediante el algoritmo de k-NN obtiene las k canciones más similares dado un id de una canción y esa similitud estará definida solamente por las puntuaciones más parecidas

def find_similar_songs(song_id, X, song_mapper, song_inv_mapper, k, metric='cosine'):
    """
    Encuentra los k vecinos más cercanos para una canción dada.
    
    Argumentos:
        song_id: id de la canción de interés
        X: matriz de utilidad user-item
        k: número de canción similares que queremos recuperar
        métrica: métrica de distancia para los cálculos de kNN
    
    Salida: devuelve una lista de k ID de canciones similares
    """
    X = X.T
    neighbour_ids = []
    
    #####EL PROBLEMA ES QUE SONG_ID ES UNA LISTA Y NO LO SOPORTA.
    ##TENGO QUE COGER EL PRIMER ELEMENTO DE ESA LISTA.
    ##CUANDO TENGAMOS MAS CANCIONES VER COMO SE TRATA

    clave_buscada = int(song_id[0])
    song_ind = song_mapper[clave_buscada]

    print(song_ind)
    
    song_vec = X[song_ind]
    if isinstance(song_vec, (np.ndarray)):
        song_vec = song_vec.reshape(1,-1)
    # usamos k+1 porque la salida kNN incluye la canción de ID = song_id
    kNN = NearestNeighbors(n_neighbors=k+1, algorithm="brute", metric=metric)
    kNN.fit(X)
    neighbour = kNN.kneighbors(song_vec, return_distance=False)
    for i in range(0,k):
        n = neighbour.item(i)
        neighbour_ids.append(song_inv_mapper[n])
    neighbour_ids.pop(0)
    return neighbour_ids


# Probemos con la segunda canción del dataset

# similar_songs = find_similar_songs(1, X_norm, song_mapper, song_inv_mapper, k=10)
# similar_songs

# A partir de ids no podemos saber que canciones son las recomendadas por lo que vamos a implementar código para que ese id lo transforme a una lista de información de la canción.

# Probamos la recomendación con dos tipos distintos de métricas
# 
# 1. Métrica de similitud por Coseno
# song_titles = dict(zip(songs['songId'], songs['track_name']))

# song_id = 1

# similar_song = find_similar_songs(song_id, X_norm, song_mapper, song_inv_mapper, metric='cosine', k=10)
# song_title = song_titles[song_id] # Saca el título de la canción
# song_row = songs.loc[songs['songId'] == song_id] # Obtiene la columna que contiene el id de esa canción
# song_artist = song_row['artist_name'].values[0] #Obtiene el nombre del artista
# song_genre = song_row['genre'].values[0] #Obtiene el género de la canción
# song_year = song_row['year'].values[0] #Obtiene el año de la canción

# print(f"porque has escuchado ... {song_title} de {song_artist} ({song_genre}, {song_year}) te recomendamos:")
# for i in similar_song:
#     row_i = songs.loc[songs['songId'] == i]
#     artist_i = row_i['artist_name'].values[0]
#     genre_i = row_i['genre'].values[0]
#     year_i = row_i['year'].values[0]
#     print(f"{song_titles[i]} de {artist_i} ({genre_i}, {year_i})")


# 2. Métrica de similitud por Euclidea
# song_id = 1

# similar_song = find_similar_songs(song_id, X_norm, song_mapper, song_inv_mapper, metric='euclidean', k=10)
# song_title = song_titles[song_id]
# song_row = songs.loc[songs['songId'] == song_id]
# song_artist = song_row['artist_name'].values[0]
# song_genre = song_row['genre'].values[0]
# song_year = song_row['year'].values[0]

# print(f"porque has escuchado ... {song_title} de {song_artist} ({song_genre}, {song_year}) te recomendamos:")
# for i in similar_song:
#     row_i = songs.loc[songs['songId'] == i]
#     artist_i = row_i['artist_name'].values[0]
#     genre_i = row_i['genre'].values[0]
#     year_i = row_i['year'].values[0]
#     print(f"{song_titles[i]} de {artist_i} ({genre_i}, {year_i})")



# #### Cold-start

# Como se ha comentado antes, cold-star es un problema que aparece cuando no todas las canciones tienen valoraciones o tienen muy pocas. Para solucionarlo crearemos otro recomendador pero basado en contenido. La recomendación será acorde con los atributos que escoja el usuario.

# n_songs = songs['songId'].nunique()
# print(f"Hay {n_songs} películas en el dataset.")

# Vamos a hacer una función en la que el usuario pase los atributos (posiciones, ya se verá con la interfaz) que quiere incluir para su recomendación. El campo de género se incluirá en otra versión.

# Los atributos que puede elegir género, año, duración y popularidad. El resto de atributos se tendrán en cuenta pero con menor porcentaje.

#Atributos que usuario puede elegir
col_optional = ["popularity", "year", "genre",	"duration_ms"]
#Atributos restantes y más específicos
col_specific = ["danceability",	"energy",	"key",	"loudness",	"mode",	"speechiness",	"acousticness",	"instrumentalness",	"liveness",	"valence",	"tempo",	"time_signature"]

# Para hacer la matriz de correlación es mejor normalizar los valores ya que son muy dispersos entre sí. Esto se sabe porque hay atributos como loudness que va desde -60 a 0 y liveness de 0.0 a 1.0, por lo que hay que hacer sean más o menos parecidos.

# songs.loc[1]

# Escalar las características para normalizar las escalas
def normalize(col_to_normalize):
    scaler = StandardScaler()

    scaled_features = songs[col_to_normalize]
    #Para evitar un warning
    scaled_features_copy = scaled_features.copy()

    scaled_features_copy.loc[:, col_to_normalize] = scaler.fit_transform(scaled_features_copy.loc[:, col_to_normalize])

    scaled_features = scaled_features_copy

    return scaled_features


# Vamos a observar como han cambiado los valores respecto al original

#Columnas normalizadas
scaled_ft_specific = normalize(col_specific)
scaled_ft_specific.head()

#Columnas originales
songs[col_specific].head()

# Ahora que están normalizados los valores vamos a crear una matriz de similitud del coseno para establecer la relación en los distintos valores y poder usarlos para la recomendación.


cosine_sim_specific = cosine_similarity(scaled_ft_specific, scaled_ft_specific)
# print(f"Dimensiones de la matriz de similitud del coseno entre los atributos: {cosine_sim_specific.shape}")

# Tenemos dos matrices de similitud: una entre géneros (cosine_sim_genre) y otra entre las caracteristicas (cosine_sim_feautures).
# 
# En esta función vamos a usar el de las características en esta función.


def content_based_features(title):
    song_idx = dict(zip(songs['songId'], list(songs.index)))
    n_recommendations = 10

    idx = song_idx[title]
    sim_scores = list(enumerate(cosine_sim_specific[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:(n_recommendations+1)] # (id, puntuacion)
    similar_songs = [i[0] for i in sim_scores]

    return similar_songs


# Vamos obtener el id de una canción cualquiera para poder hacer el ejemplo.

# Mostramos todos los campos para comprobar que se realiza bien la recomendación.

# ### Recomendador general (PARTE IMPORTANTE)

# Las **funciones** anteriormente declaradas que van a ser utilzadas para el recomendador.

# Ahora vamos a hacer una función que se aquella que se llame cuando se le de al botón de recomendadar (***recommender*** es la función).

# La siguiente función ***sim_cosine_total*** calcula la matriz de similitud del coseno total, es decir, tiene en cuenta los atributos pasados y los atributos específicos que usamos con un menor porcentaje para una recomendación algo más exacta. Hacemos una media aritmética y damos la misma importancia a todos los atributos que el usuario elige sin preferencias.

def sim_cosine_total(options):
    # Excluir si una de las opciones es género porque ese ya está calculado
    num_opt = len(options) #para distribuir los porcentaje  

    is_genre = 0

    if "genre" in options:
        print("Opciones después", options)
        options.remove("genre")
        is_genre = 1

        if len(options) == 0:
            is_genre = 2
    
    if is_genre == 2:
        cosine_sim_opt = cosine_sim_genre
    else:
        # Normalizamos los valores ya que son muy dispersos
        scaled_ft_opt = normalize(options)
        cosine_sim_opt_no_genre = cosine_similarity(scaled_ft_opt, scaled_ft_opt) #poco eficiente hacerlo para cada vez que se pida una recomendación?

        if is_genre == 1:
            percent_genre = 1/ num_opt
            print(f"porcentaje género {percent_genre}")

            matrix_genre = np.array(cosine_sim_genre)
            matrix_no_genre = np.array(cosine_sim_opt_no_genre)

            cosine_sim_opt = np.multiply(percent_genre, matrix_genre) + np.multiply(1 - percent_genre, matrix_no_genre)
        else: # no hay género en la lista
            cosine_sim_opt = cosine_sim_opt_no_genre
    
    matrix_opt = np.array(cosine_sim_opt)
    # # matrix_specific = np.array(cosine_sim_specific)

    # # percent_specific = 0.00 # No le damos mucho porque no es lo más importante
    
    # # cosine_sim_final = (1-percent_specific)*matrix_opt + percent_specific*matrix_specific
    cosine_sim_final = matrix_opt


    return cosine_sim_final


# Primera fase (***first_stage***) representa el recomendador basado en contenido, el contenido a tener en cuenta son los atributos que ha seleccionado el usuario, si ha seleccionado.


def first_stage(song_id, options):
    # 1. Hay que comprobar si hay atributos a tener en cuenta (options)
    cosine_sim = sim_cosine_total(options)

    print("cosine_sim: ", cosine_sim)

    song_idx = dict(zip(songs['songId'], list(songs.index)))
    n_recommendations = 20

    #pongo song_id[0] porque solo hay una cancion en la lista song_id
    idx = song_idx.get(song_id[0])
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:(n_recommendations+1)] # (id, puntuacion)

    similar_songs = [i[0] for i in sim_scores]

    return similar_songs


# Segunda fase (***second_stage***) representa el recomendador filtrado colaborativo, se recomienda acorde con las canciones que le han gustando a otros usuarios y tienen, por lo tanto, gustos parecidos entre sí.

def second_stage(song_id): # collaborative_recommender
    similar_songs = find_similar_songs(song_id, X_norm, song_mapper, song_inv_mapper, metric='euclidean', k=20)
    #similar_songs = find_similar_songs(song_id, X_norm, song_mapper, song_inv_mapper, metric='cosine', k=10) # Hemos visto antes que euclides es algo más rápido
    
    return similar_songs

# Tercera fase (***third_stage***) representa basado en conocimiento, que solo se usará en el caso de que el usuario no haya introducido ninguna opción y recomendará por popularidad de la canción, que es algo que el sistema sabe (conocimiento)

def third_stage(song_id):
    # Supongamos que 'df' es tu DataFrame que contiene las características de las canciones
    # Primero, normalizamos los datos
    df = songs.copy();
    
    col_del = ['songId', 'artist_name', 'track_name', 'track_id','genre', 'genres']
    
    df = df.drop(columns=col_del)
    
    scaler = StandardScaler()
    df_scaled = scaler.fit_transform(df)

    # Aplicamos K-means
    kmeans = KMeans(n_clusters=1)
    kmeans.fit(df_scaled)

    # Ahora, cada canción ha sido asignada a un cluster
    df['cluster'] = kmeans.labels_

    # Obtiene el cluster de la canción
    song_cluster = df.loc[song_id, 'cluster']

    # Filtra el DataFrame para incluir solo las canciones en el mismo cluster
    same_cluster_df = df[df['cluster'] == song_cluster]

    # Calcula las distancias euclidianas entre la canción y todas las demás canciones en el mismo cluster
    distances = euclidean_distances(same_cluster_df.drop('cluster', axis=1), same_cluster_df.loc[song_id].drop('cluster').values.reshape(1, -1))

    # Obtiene los índices de las canciones ordenadas por distancia (de menor a mayor)
    closest_song_ids = np.argsort(distances.squeeze())

    # Obtiene los índices de las canciones más cercanas
    closest_songs = same_cluster_df.iloc[closest_song_ids[:20]]

    return closest_songs


# La función ***intercale_lists*** sirve para mezclar los resultados del recomendador basado en contenido y el colaborativo.

def intercalate_lists(l1, l2):
    # Calcula la mitad de la longitud de las listas
    l = len(l1) // 2

    # Utiliza conjuntos para evitar repeticiones
    intercalate_set = set()

    # Intercale los elementos de la primera mitad de cada lista sin repeticiones
    for elem1, elem2 in zip(l1, l2):
        intercalate_set.add(elem1)
        intercalate_set.add(elem2)

    # Convierte el conjunto a una lista para mantener el orden original
    list_final = list(intercalate_set)

    return list_final[:l]

##Función que devuelve la información de una canción a partir del índice
def idANombre(songs_id):
    nombres_canciones = []

    for song_id in songs_id:
        #aquí puedo escoger los campos que quiero devolver
        nombre_cancion = songs.loc[songs.index == song_id, [ 'track_name', 'artist_name']]
        nombres_canciones.append(nombre_cancion)

    #pasar a df
    nombres_canciones_df = pd.concat(nombres_canciones)

    return nombres_canciones_df

# La función ***recommender*** es el recomendador final que devuelve las canciones más parecidas dada una canción seleccionada y los atributos a tener en cuenta, estos últimos pueden ser ninguno y directamente se pasa a un filtrado colaborativo.
# ÚNICA FUNCIÓN A USAR!!!
def recommender(song_id, options):
    # Primera fase: consiste en la obtención de la lista de canciones parecidas que cumplan con los atributos que el usuario ha elegido.
    list_songs_content = [] # Lista de canciones recomendadas basadas
    
    if len(options) != 0:  #si hemos marcado opciones
        list_songs_content = first_stage(song_id, options)

    # Segunda fase: filtrado colaborativo (si la lista es demasiado grande)
    list_songs_collaborative = second_stage(song_id)
    list_final = []

    if len(list_songs_content) > 10: # Es necesario hacer la intersección -> segunda fase
        aux = intercalate_lists(list_songs_content, list_songs_collaborative)
        
        if song_id in aux: aux.remove(song_id)
        list_final = aux.copy()[:10]
        
    elif len(list_songs_content) == 0:
        if len(list_songs_collaborative) == 0:
            aux = third_stage(song_id)
        else: 
            aux = list_songs_collaborative
        
        if song_id in aux: aux.remove(song_id)
        list_final = aux.copy()[:10]
    else:
        aux = list_songs_content
        
        if song_id in aux: aux.remove(song_id)
        list_final = aux.copy()[:10]    

    print("list_final:", list_final)

    #La lista final devuelve los ids de las canciones que se recomiendan.
    #Cambiamos los ids para devolver el nombre de la canción y el artista
    songs = idANombre(list_final)

    songs['id'] = list_final
    
    return songs


# Hacemos unas pruebas y parece ser que funciona bien

# song_titles = dict(zip(songs['songId'], songs['track_name']))

# similar_songs = recommender(1, ['popularity'])

# song_title = song_titles[1]
# song_row = songs.loc[songs['songId'] == 1]
# song_artist = song_row['artist_name'].values[0]
# song_genre = song_row['genres'].values
# song_year = song_row['year'].values[0]

# print(f"porque has escuchado ... {song_title} de {song_artist} ({song_genre}, {song_year}) te recomendamos:")
# for i in similar_songs:
#    row_i = songs.loc[songs['songId'] == i]
#    artist_i = row_i['artist_name'].values[0]
#    genre_i = row_i['genres'].values
#    popularity_i = row_i['popularity'].values[0]
#    year_i = row_i['year'].values[0]
#    print(f"{song_titles[i]} de {artist_i} ({genre_i}, {year_i}). Popularidad: {popularity_i}")


# ### Recomendador para varias canciones (PARTE IMPORTANTE)

# La función ***intersection*** sirve para realizar la intersección entre varias listas dadas. Una canción es común cuando aparece en al menos dos listas, aunque no aparezca en el resto.

# In[95]:


from collections import Counter
from functools import reduce
from operator import add

def intersection(lists):
    # Reduce las listas y cuenta las veces que aparece cada elemento
    counter = Counter(reduce(add, lists))
    
    # Devuelve los elementos que aparecen en más de una lista
    return [item for item, count in counter.items() if count > 1]


# La función ***merge_lists*** evita repetidos de manera eficiente

# In[96]:


def merge_lists(l1, l2, l3):
    # Convertir l1 a un conjunto para búsquedas eficientes
    s1 = set(l1)
    s3 = set(l3)

    # Crear una nueva lista para los elementos de l2 que no están en l1
    l2 = [item for item in l2 if (item not in s1 and item not in s3)]

    # Añadir los elementos de l2 a l1
    l1.extend(l2)

    return l1

# La función ***recommender_songs*** devuelve las canciones similares de una lista de canciones. Consiste en devolver las canciones comunes de las similares de cada canción y así sucesivamente hasta conseguir al menos 10.

# In[97]:


def recommender_songs(songs_id, options):
    ret = []
    
    similar_songs = []
    
    if len(songs_id) == 1: return recommender(songs_id[0],options)
    
    ids = songs_id.copy() # Copiamos los ids pasados
    # Recorremos todas para obtener la lista de canciones similares de cada canción de seleccionada
    # Luego se hace intersección
    # De la intersección si no se ha llegado a 10 canciones en común, con esa intersección se vuelve a buscar las similares y comunes pero a estas y se añaden en la lista final las que no estén ya.
    while len(ret) < 10:
        for song_id in ids: 
            similar_songs.append(recommender(song_id,options))
        
        ids = intersection(similar_songs)
        merge_lists(ret,ids,songs_id)
    
    return ret