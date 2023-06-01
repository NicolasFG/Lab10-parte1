from pymongo import MongoClient
import requests
from flask import Flask, request, jsonify
import csv

# Establecer conexión con MongoDB
client = MongoClient("mongodb://10.100.169.138:30000")
db = client["test"]
#Creo mi coleccion datos_clima
coleccion = db["datos_clima"]


# Leer los datos de las ciudades desde el archivo worldcities.csv
with open("worldcities-2.csv", 'r', encoding='utf-8') as archivo:
    lineas = csv.reader(archivo)

# Omitir la primera fila de encabezados
    next(lineas)

# Iterar sobre las líneas y consultar la API de OpenMeteo para insertar los datos en la colección
    for linea in lineas:

        nombre_ciudad = linea[0]
        latitud = float(linea[2])
        longitud = float(linea[3])
        #print(nombre_ciudad)
        #print(latitud)
        #print(longitud)

        # Consultar la API de OpenMeteo para obtener los datos de temperatura
        url = f"https://api.open-meteo.com/v1/forecast?latitude={latitud}&longitude={longitud}&forecast_days=7&daily=temperature_2m_max,temperature_2m_min&timezone=PST"
        response = requests.get(url)
        data = response.json()
        #print(response)
        #print(data)

        # Iterar sobre los datos y insertarlos en la colección
        temperature_2m_min=""
        temperature_2m_max=""
        time=""
        for forecast in data['daily']:
           
            if forecast == "time":
                time = data['daily'][forecast]
                print("time")
                print(time)
            elif forecast == "temperature_2m_min":
                temperature_2m_min = data['daily'][forecast]
                print("temperature_2m_min")
                print(temperature_2m_min)
            elif forecast == "temperature_2m_max":
                temperature_2m_max = data['daily'][forecast]
                print("temperature_2m_max")
                print(temperature_2m_max)

        clima = {
                "fecha": time[0],
                "nombre_ciudad": nombre_ciudad,
                "latitud": latitud,
                "longitud": longitud,
                "temperatura_maxima": temperature_2m_max[0],
                "temperatura_minima": temperature_2m_min[0]
            }

            # Insertar el documento en la colección
        coleccion.insert_one(clima)


# app = Flask(__name__)

# @app.route("/clima", methods=["GET"])
# def obtener_datos_clima():
#     temperatura = request.args.get("temperatura")
#     dia = request.args.get("dia")

#     # Aquí puedes realizar la lógica de consulta a la colección "datos_clima" en MongoDB
#     # utilizando los parámetros de temperatura y día

#     # Ejemplo de lógica para consultar datos en MongoDB y devolver los resultados
#     resultados = db.datos_clima.find({
#         "temperatura_maxima": {"$gte": float(temperatura), "$lt": float(temperatura) + 1},
#         "fecha": dia
#     })

#     datos_clima = []
#     for resultado in resultados:
#         datos_clima.append({
#             "nombre_ciudad": resultado["nombre_ciudad"],
#             "latitud": resultado["latitud"],
#             "longitud": resultado["longitud"],
#             "temperatura_maxima": resultado["temperatura_maxima"],
#             "temperatura_minima": resultado["temperatura_minima"]
#         })

#     return jsonify(datos_clima)

# if __name__ == "__main__":
#     app.run()




