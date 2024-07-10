# Proyecto Individual 1: Machine Learning Operations.
## Introducción:
Este proyecto tenía como objetivo personal poner en práctica el amplio abanico de conocimientos adquiridos durante el curso de Data Science Full Time en SoyHenry.
Como objetivo profesional, el 'Cliente' nos pidió tener desarrollado un MVP de un Modelo de Recomendación de Películas para plataformas de Streaming en una semana.
Los desafíos que se pueden identificar a simple vista son dos:
1. La baja calidad y madurez de la base de datos.
2. La velocidad con la que se tiene que llevar a cabo el proyecto.

Dada las circunstancias, ¡mejor será que nos pongamos manos a la obra!

## Índice
1. [Introducción](#introducción)
2. [Consideraciones Iniciales](#consideraciones-iniciales)
3. [Extracción, Carga y Transformación de los Datos (ETL)](#extracción-carga-y-transformación-de-los-datos-etl)
4. [Creación de funciones](#creación-de-funciones)
5. [Análisis Exploratorio de los Datos (EDA)](#análisis-exploratorio-de-los-datos-eda)
6. [Modelo de Recomendación](#modelo-de-recomendación)
7. [Consideraciones Finales](#consideraciones-finales)

## Consideraciones iniciales
Contamos con una base de datos compuesta por dos archivos CSV (**movies_dataset.csv y credits.csv**) de alrededor de 45.000 filas de datos brutos que deben ser procesados para su uso en 6 funciones mínimas (detalladas más adelante) pedidas explícitamente por el cliente.
Dichas funciones deben ser posteriormente implementadas mediante una API y presentadas haciendo uso de [Render](https://dashboard.render.com/) para su accesibilidad.
Es necesario también un Análisis Exploratorio de los Datos (EDA) que será usado por el departamento de Analytics del cliente para mejorar la implementación del modelo.

A continuación, se hace un resumen del proceso completo.

## Extracción, Carga y Transformación de los Datos (ETL)
Dentro de los Notebooks se encuentra el archivo ETL que contiene el proceso detallado mediante el cual se dio forma a los datos.
La información se encontraba separada en dos archivos: **movies_dataset.csv** contiene información general de las películas, mientras que **credits.csv** está orientado a las personas que participaron de la filmación de los metrajes.
Los datos dentro de los archivos no estaban normalizados, por lo que no estaban listos para ser trabajados. Se tuvo que hacer un proceso de desanidado de columnas y extracción de la información, así como también la eliminación de columnas que no aportaban valor y traían complejidad al proyecto.
Además, se crearon nuevas columnas que iban a ser necesarias para el correcto funcionamiento de las funciones y se hizo un manejo preliminar de valores nulos y/o duplicados.
Todo esto fue almacenado en un archivo tipo **.parquet**, que será la nueva fuente de los datos solicitados por las funciones.

![Movies Dataset Anidados](img/movies_dataset_anidados.png)
![DataFrame ETL](img/df_etl.png)
![Credits Anidados](img/credits_anidados.png)

## Creación de funciones
En el archivo **main.py** se pueden ver las funciones creadas en detalle.
Se utiliza la librería FastAPI para crear la API que permitirá acceder a ellas. Cada una hace una consulta a la base de datos procesada en el paso anterior que le permite extraer información relevante.
Los 6 endpoints dan acceso a las funciones detalladas a continuación:
- Películas por mes: Se selecciona un mes del año y se hace un conteo del número de filmaciones estrenadas en él.
- Películas por día: Se selecciona un día de la semana y se hace un conteo del número de filmaciones estrenadas en él.
- Score de película: Se escribe el título de una filmación y retorna su año de estreno y un valor numérico en representación de su popularidad.
- Votación de película: Se escribe el título de una filmación y retorna su año de estreno y, si cumple con un mínimo de valoraciones, el promedio de las mismas.
- Información de actor: Se escribe el nombre de un actor y retorna el número de filmaciones en las que ha participado, el porcentaje de retorno de sus películas total y promedio a lo largo de su carrera.
- Información de director: Se escribe el nombre de un director y retorna el número y lista de filmaciones en las que ha participado solo como director, junto con su porcentaje de retorno.

![API Main](img/api_main.png)

Terminadas las funciones se hizo un deploy en Render.
[Aquí](https://proyecto-individual-1-henry-k9qg.onrender.com/docs) puedes acceder a ella.

![API Page](img/api_page.png)

## Análisis Exploratorio de los Datos (EDA)
Dentro de los Notebooks se encuentra el archivo EDA que contiene el proceso detallado mediante el cual se analizó la relevancia de los datos y se hicieron los ajustes necesarios para su funcionamiento.
Una parte de la preparación de datos había sido ejecutada durante el proceso de [ETL](#extracción-carga-y-transformación-de-los-datos-etl), el proceso de limpieza y normalización continuó para asegurarse de que los datos del archivo **.parquet** solicitados por las funciones sean correctos. También se hizo un análisis un poco más profundo de los mismos orientado hacia la producción del sistema de recomendación.
Se utilizaron diversos tipos de ejemplos gráficos para explicar el razonamiento de la inclusión o exclusión de ciertos datos para generar el modelo. Finalmente, se creó un nuevo archivo nuevo que contiene lo mínimo indispensable para su correcto funcionamiento.

![budget piechart](img/eda_budg.png)
![Subsec piechart](img/eda_subsec.png)
![Overview Wordcloud](img/eda_overview_wordcloud.png)
![Languages Ocurrencies](img/eda_original_languages_ocurrencies.png)

## Modelo de Recomendación
Al final del archivo **EDA** se encuentra un análisis del proceso de los datos para el modelo de recomendación.
Se decidió usar **TfidfVectorizer** para vectorizar el texto debido a la inconsistencia de los datos numéricos y **cosine_similarity**.
El código que entrena el modelo puede encontrarse al principio del archivo **main.py**, es decir, dentro de la API misma. De esta manera, la información es preprocesada de manera que reduzca el uso de memoria al ejecutar la función, lo cual puede ser un limitante importante para el servidor.
Al ejecutarse, la función da como resultado un set de 5 películas que puedan tener relación con el título escrito, ordenadas de mejor a peor valorada según el resultado promedio de los votos encontrados en la base de datos misma.

![Vectorización](img/vectorizacion.png)
![Machine Learning](img/machine_learning.png)
![Recomendaciones Toy Story](img/Recomendaciones_toy.png)

## Consideraciones finales
El proyecto ha supuesto un gran reto inicial en la carrera de Ciencia de Datos y me ha permitido comprender e implementar la gran cantidad de información obtenida a lo largo de todo el proceso de aprendizaje. Se hizo una ingesta de datos rigurosa, un análisis de datos profundo y un sistema de recomendación robusto con una API que deja gran espacio a la escalabilidad.
Lo considero un éxito no solo profesional sino personal y un gran escalón en el proceso de aprendizaje.
