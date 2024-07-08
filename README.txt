# Proyecto Individual 1: Machine Learning Operations.
## Introduccion:
Este proyecto tenia como objetivo personal poner en practica el amplio abanico de conocimientos adquiridos durante el curso de Data Science Full Time en SoyHenry.
Como objetivo profesional, el 'Cliente' nos pidio tener desarrollado un MVP de un Modelo de Recomendacion de Peliculas para plataformas de Streaming en una semana.
Los desafios que se pueden identificar a simple vista son dos:
1. La baja calidad y madurez de la base de datos.
2. La velocidad con la que se tiene que llevar a cabo el proyecto.
Dada la circunstancias, mejor sera que nos pongamos manos a la obra!

## Indice
[TOC]

## Consideraciones iniciales
Contamos con una base de datos compuesta por dos archivos CSV (**movies_dataset.csv y credits.csv**) de al rededor de 45.000 filas de datos brutos que deben ser procesados para su uso en 6 funciones minimas (detalladas mas adelante) pedidas explicitamente por el cliente.
Dichas funciones deben ser posteriormente implementadas mediante una API y presentadas haciendo uso de [Render](https://dashboard.render.com/) para su accesibilidad.
Es necesario tambien un Analisis Exploratorio de los Datos (EDA) que sera usado por el departamento de Analitycs del cliente para mejorar la implementacion del modelo.

A continuacion se hace un resumen del proceso completo.

## Extraccion, Carga y Transformacion de los Datos. (ETL)

Dentro de los Notebooks se encuentra el archivo ETL que contiene el proceso detallado mediante el cual se dio forma a los datos.
La informacion se encontraba separada en dos archivos: **movies_dataset.csv** contiene informacion general de las peliculas, mientras que **credits.csv** esta orientado a las personas que participaron de la filmacion de los metrajes.
Los datos dentro de los archivos no estaban normalizados por lo que no estaban listos para ser trabajados. Se tuvo que hacer un proceso de desanidado de columnas y extraccion de la informacion, asi como tambien la eliminacion de columnas que no aportaban valor y traian complejidad al proyecto.
Ademas se crearon nuevas columnas que iban a ser necesarias para el correcto funcionamiento de las funciones y se hizo un manejo preeliminar de valores nulos y/o duplicados.

img/movies_dataset_anidados.png
img/df_etl.png
img/credits_anidados.png

## Creacion de funciones
En el archivo **main.py** se pueden ver las funciones creadas en detalle.
Se utiliza la libreria FastAPI para crear la API que permitira acceder a ellas. Cada una hace una consulta a la base de datos procesada en el paso anterior que le permite extraer informacion relevante.
Los 6 endpoints dan acceso a las funciones acontinuacion:
- Peliculas por mes: Se selecciona un mes del año y se hace un conteo del numero de filmaciones estrenadas en el.
- Peliculas por dia: Se selecciona un dia de la semana y se hace un conteo del numero de filmaciones estrenadas en el.
- Score de pelicula: Se escribe el titulo de una filmacion y retorna su año de estreno y un valor numerico en representacion de su popularidad.
- Votacion de pelicula: Se escribe el titulo de una filmacion y retorna su año de estreno y, si cumple con un minimo de valoraciones, el promedio de las mismas.
- Informacion de actor: Se escribe el nombre de un actor y retorna el numero de filmaciones en las que ah participado, el porcentaje de retorno de sus peliculas total y promedio a lo largo de su carrera.
- Informacion de director: Se escribe el nombre de un director y retorna el numero y lista de filmaciones en las que ah participado solo como director, junto con su porcentaje de retorno.
img/api_main.png
Terminadas las funciones se hizo un deploy en Render.
[Aqui](https://proyecto-individual-1-henry-k9qg.onrender.com/docs) puedes acceder a ella.
img/api_page.png