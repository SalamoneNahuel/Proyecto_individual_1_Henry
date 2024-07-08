from fastapi import FastAPI, HTTPException
from enum import Enum
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

app = FastAPI()

# Define la ruta del archivo Parquet
parquet_eda = "Datasets/dataset_peliculas.parquet"
parquet_vect = pd.read_parquet("Datasets/dataset_vect.parquet")

vec_tfidf = {}
tfidf_lis = []

columnas_vectorizar = ['genres', 'overview', 'production_companies', 'production_countries', 'cast', 'crew', 'title_key']

for column in columnas_vectorizar:
    vectorizador = TfidfVectorizer(max_features=30000)
    matris_tfidf = vectorizador.fit_transform(parquet_vect[column])
    vec_tfidf[column] = vectorizador
    tfidf_lis.append(matris_tfidf)

# Funcion numero de peliculas estrenadas en el mes
def cantidad_filmaciones_mes(df, mes):
    
    """
    Hace un recuento de todas las peliculas que se estrenaron en un determinado mes
    :param mes: Mes del cual se quiere obtener el numero de peliculas
    :param df: El dataframe a consultar
    :return: Int con el total del recuento
    """

    # Creamos un diccionario con los meses que funciona como referencia iterable y se le asigna un valor a cada uno
    meses_dict = {
        'Enero': 1,
        'Febrero': 2,
        'Marzo': 3,
        'Abril': 4,
        'Mayo': 5,
        'Junio': 6,
        'Julio': 7,
        'Agosto': 8,
        'Septiembre': 9,
        'Octubre': 10,
        'Noviembre': 11,
        'Diciembre': 12
        }
    
    selector = meses_dict[mes] # Variable a referenciar igualada al valor correspondiente al mes
    count = df['release_date'].dt.month.value_counts().get(selector, 0) # Contamos las veces que aparece el valor en el dataset

    return(f"{count} películas fueron estrenadas en el mes de {mes}")
    
# Funcion numero de peliculas estrenadas en el día de semana
def cantidad_filmaciones_día(df, día):

    """
    Hace un recuento de todas las peliculas que se estrenaron en un determinado día de la semana
    :param día: Día del cual se quiere obtener el numero de peliculas
    :param df: El dataframe a consultar
    :return: Int con el total del recuento
    """

    # Creamos un diccionario con los días que funciona como referencia iterable y se le asigna un valor a cada uno
    días_semana = {
        'Lunes': 0,
        'Martes': 1,
        'Miércoles': 2,
        'Jueves': 3,
        'Viernes': 4,
        'Sábado': 5,
        'Domingo': 6
        }

    selector = días_semana[día] # Variable a referenciar igualada al valor correspondiente al día
    count = df['release_date'].dt.weekday.value_counts().get(selector, 0) # Contamos las veces que aparece el valor en el dataset
    
    return(f"{count} películas fueron estrenadas en un día {día}")



# Funcion score de pelicula
def score_titulo(df, titulo_de_la_filmación):
   
    """
    Busca la pelicula en base al titulo proporcionado y retorna el año de salida y el score de popularidad
    :param titulo_de_la_filmación: Titulo de la pelicula de la cual se quiere obtener la informacion
    :param df: El dataframe a consultar
    :return: Str con el titulo de la pelicula como aparece en la base de datos, int con el año de estreno y float con el score
    """

    # Se estandariza el string en minusculas para evitar errores
    title = titulo_de_la_filmación.lower()

    # Generamos un Data Frame nuevo con las filas que contengan el input en el titulo
    result = df[df['title'].str.lower().str.contains(title, na=False)]
   
    # Condicional si se encuentra un titulo similar al input
    if not result.empty:

        # Extraemos el title (título), popularity (score) y release_year (año de estreno) del primer resultado encontrado unicamente
        found_title = result['title'].iloc[0]
        found_score = round(result['popularity'].iloc[0], 2)
        found_release_year = result['release_year'].iloc[0]
        
        return (f"La pelicula '{found_title}' fue estrenada en el año {found_release_year} con un score/popularidad de {found_score}")

    # Return en caso de no encontrar un titulo que contenga el input
    else:
        return (f"No se encontraron peliculas que contengan '{titulo_de_la_filmación}' en el titulo")
   


# Funcion promedio de votacion
def votos_titulo(df, titulo_de_la_filmación):

    """
    Busca la pelicula en base al titulo proporcionado y retorna el año de salida y el valor de votacion promedio pero solo si la cantidad de votos es mayor a 2000
    :param titulo_de_la_filmación: Titulo de la pelicula de la cual se quiere obtener la informacion
    :param df: El dataframe a consultar
    :return: Str con el titulo de la pelicula como aparece en la base de datos, int con el año de estreno y float con el score
    """

    # Se estandariza el string en minusculas para evitar errores
    title = titulo_de_la_filmación.lower()

    # Generamos un Data Frame nuevo con las filas que contengan el input en el titulo
    result = df[df['title'].str.lower().str.contains(title, na=False)]

    # Condicional si se encuentra un titulo similar al input
    if not result.empty:

        # Extraer el title (título), popularity (promedio de valoraciones) y release_year (año de estreno) del primer resultado encontrado
        found_title = result['title'].iloc[0]
        found_vote = round(result['vote_average'].iloc[0], 2)
        found_release_year = result['release_year'].iloc[0]
        found_vote_count = result['vote_count'].iloc[0]
        
        # Condicional si la pelicula tuvo mas de 2000 votos
        if found_vote_count < 2000:

            return (f"La pelicula '{found_title}' fue estrenada en el año {found_release_year}, pero tiene menos de 2000 valoraciones por lo que no se puede dar una valoracion promedio fiable.")
        
        # Return en caso de que la pelicula no cumpla con el numero de votos necesarios
        else:
            return (f"La pelicula '{found_title}' fue estrenada en el año {found_release_year} con una valoracion promedio de {found_vote}")
    
        # Return en caso de no encontrar un titulo que contenga el input
    else:
        return (f"No se encontraron peliculas que contengan '{titulo_de_la_filmación}' en el titulo") 
   

# Funcion info del actor
def get_actor(df, nombre_actor):

    """
    Busca un actor y hace un recuento de las peliculas en las que trabajo y cuanto porcentaje de retorno tuvieron sus peliculas en total y en promedio
    :param nombre_actor: Nombre del actor del cual se quiere obtener la informacion
    :param df: El dataframe a consultar
    :return: Str con el nombre del actor, int con el numero de peliculas en las que participo, float con el retorno total y float con el retorno promedio
    """
    # Se estandariza el string en minusculas para evitar errores
    actor = nombre_actor.lower()

    # Filtramos en un nuevo Data Frame las filas donde el actor figure en la columna 'cast'
    actor_movies = df[df['cast'].apply(lambda x: actor in [a.lower() for a in x])]

    # Condicional si se encontraron coincidencias con el input
    if not actor_movies.empty:

        actor_movies = actor_movies[actor_movies['crew'].apply(lambda x: actor not in [a.lower() for a in x])]

        # Se almacena la info a retornar en variables
        num_movies = len(actor_movies)
        total_return = round(actor_movies['return'].sum(), 2)
        avg_return = round(actor_movies['return'].mean(), 2)

        return(f"El actor {nombre_actor} ha participado de {num_movies} filmaciones solo como actor, consiguiendo un retorno del {total_return}%, con un promedio de {avg_return}% por filmación.")
    
    # Retorno en caso de no encontrar coincidencias
    else:
        return (f"No se encontro el actor '{nombre_actor}'. Asegurate que el nombre esté bien escrito.")    

# Funcion info del director
def get_director(df, nombre_director):

    """
    Busca un director y hace un recuento de las peliculas en las que trabajo y cuanto porcentaje de retorno tuvieron sus peliculas en total y en promedio
    Tambien lista todas las peliculas que dirigio con su fecha de salida, retorno, costo y ganancia
    :param nombre_director: Nombre del director del cual se quiere obtener la informacion
    :param df: El dataframe a consultar
    :return: Diccionario con la informacion solicitada
    """

    # Se estandariza el string en minusculas para evitar errores
    director = nombre_director.lower()

    # Filtramos en un nuevo Data Frame las filas donde el director figure en la columna 'crew'
    director_movies = df[df['crew'].apply(lambda x: director in [a.lower() for a in x])]

    # Condicional si se encontraron coincidencias con el input
    if not director_movies.empty:

        # Se almacena la info a retornar en variables
        num_movies = len(director_movies)
        total_return = round(director_movies['return'].sum(), 2)
        avg_return = round(director_movies['return'].mean(), 2)

        # Construimos el diccionario con la informacion del director
        director_info = {
            nombre_director: f"El director {nombre_director} ha dirigido {num_movies} filmaciones, consiguiendo un retorno del {total_return}%, con un promedio de {avg_return}% por filmación."
        }

        # Añadimos la informacion de cada pelicula
        for i, (index, row) in enumerate(director_movies.iterrows(), 1):
            movnum = 1
            pelicula_info = {
                "Titulo": row['title'],
                "Fecha de estreno": row['release_date'].strftime('%Y-%m-%d'),
                "Retorno": f"{row['return']}%",
                "Presupuesto": row['budget'],
                "Ingresos": row['revenue']
            }
            director_info[f"Pelicula {i}"] = pelicula_info
            movnum += 1

        return director_info
     
    # Retorno en caso de no encontrar coincidencias
    else:
        return (f"No se encontro un director que contenga '{nombre_director}' en el nombre.")

class month(str, Enum):
    enero = 'Enero'
    febrero = 'Febrero'
    marzo = 'Marzo'
    abril = 'Abril'
    mayo = 'Mayo'
    junio = 'Junio'
    julio = 'Julio'
    agosto = 'Agosto'
    septiembre = 'Septiembre'
    octubre = 'Octubre'
    noviembre = 'Noviembre'
    diciembre = 'Diciembre'

    # Ruta para obtener numero de peliculas estrenadas en el mes desde el archivo Parquet

def get_recomendations(df, titulo_de_la_filmación, top_n=5):
    
    title = titulo_de_la_filmación.lower()
    result = df[df['title'].str.lower().str.contains(title, na=False)]

    if not result.empty:
    
        idx = result.index[0]
        pelicula = result.iloc[0]['title']

        combined_similarities = np.zeros(len(df))

        for matris_tfidf in tfidf_lis:
            combined_similarities += cosine_similarity(matris_tfidf, matris_tfidf[idx]).flatten()

        combined_similarities /= len(tfidf_lis)

        similarity_scores = list(enumerate(combined_similarities))
        similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
        
        recommendations = [df.iloc[i[0]] for i in similarity_scores[1:top_n+1]]
        recommendations = sorted(recommendations, key=lambda x: x['vote_average'], reverse=True)

        recomendaciones_info = {
            "Si te gusto": pelicula,
            "Quizas te pueda gustar": {}
        }

        for i, pelicula_recomendada in enumerate(recommendations, 1):
            pelicula_info = {
                "La pelicula": pelicula_recomendada['title'],
                "con un puntaje de": pelicula_recomendada['vote_average']
            }
            recomendaciones_info["Quizas te pueda gustar"][f"Recomendación {i}"] = pelicula_info
        
        return recomendaciones_info
    else:
        return (f"No se encontraron peliculas que contengan '{titulo_de_la_filmación}' en el titulo")

@app.get("/estrenos_en_mes/{mes}")
async def estrenos_en_mes(mes: month):

    try:
        df = pd.read_parquet(parquet_eda)

        result = cantidad_filmaciones_mes(df,mes.value)
        return {"result": result}

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Archivo Parquet no encontrado, revisa si la ruta del archivo es correcta.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al leer el archivo Parquet: {str(e)}")
    
class weekday(str, Enum):
    lunes = 'Lunes'
    martes = 'Martes'
    miércoles = 'Miércoles'
    jueves = 'Jueves'
    viernes = 'Viernes'
    sábado = 'Sábado'
    domingo = 'Domingo'

    # Ruta para obtener numero de peliculas estrenadas en el día desde el archivo Parquet
@app.get("/estrenos_en_día/{día}")
async def estrenos_en_día_semana(día: weekday):

    try:
        df = pd.read_parquet(parquet_eda)

        result = cantidad_filmaciones_día(df,día.value)
        return {"result": result}

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Archivo Parquet no encontrado, revisa si la ruta del archivo es correcta.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al leer el archivo Parquet: {str(e)}")
    
    # Ruta para obtener el score de peliculas desde el archivo Parquet
@app.get("/score_pelicula/{titulo}")
async def score_pelicula(titulo_de_la_filmación: str):

    try:
        df = pd.read_parquet(parquet_eda)

        result = score_titulo(df, titulo_de_la_filmación)
        return {"result": result}

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Archivo Parquet no encontrado, revisa si la ruta del archivo es correcta.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al leer el archivo Parquet: {str(e)}")
    
    # Ruta para obtener el promedio de voto de peliculas desde el archivo Parquet
@app.get("/votos_pelicula/{titulo}")
async def votos_pelicula(titulo_de_la_filmación: str):

    try:
        df = pd.read_parquet(parquet_eda)

        result = votos_titulo(df, titulo_de_la_filmación)
        return {"result": result}

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Archivo Parquet no encontrado, revisa si la ruta del archivo es correcta.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al leer el archivo Parquet: {str(e)}")
    
    # Ruta para obtener info de un actor desde el archivo Parquet
@app.get("/info_actor/{nombre}")
async def info_actor(nombre_actor: str):

    try:
        df = pd.read_parquet(parquet_eda)

        result = get_actor(df, nombre_actor)
        return {"result": result}

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Archivo Parquet no encontrado, revisa si la ruta del archivo es correcta.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al leer el archivo Parquet: {str(e)}")
    
    # Ruta para obtener info de un directo desde el archivo Parquet
@app.get("/info_director/{nombre}")
async def info_director(nombre_director: str):

    try:
        df = pd.read_parquet(parquet_eda)

        result = get_director(df, nombre_director)
        return {"result": result}

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Archivo Parquet no encontrado, revisa si la ruta del archivo es correcta.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al leer el archivo Parquet: {str(e)}")

    # Ruta para obtener recomendacion desde el archivo Parquet
@app.get("/recomendacion/{titulo}")
async def votos_pelicula(titulo_de_la_filmación: str):

    try:
        df = parquet_vect

        result = votos_titulo(df, titulo_de_la_filmación)
        return {"result": result}

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Archivo Parquet no encontrado, revisa si la ruta del archivo es correcta.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al leer el archivo Parquet: {str(e)}")
    
    