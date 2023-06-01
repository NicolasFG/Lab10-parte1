
import requests
import csv

# Abrir el archivo en modo lectura
with open("worldcities-2.csv", 'r', encoding='utf-8') as archivo_csv:
    # Crear un objeto lector de CSV
    lector_csv = csv.reader(archivo_csv)

    # Omitir la primera fila de encabezados
    next(lector_csv)

    # Iterar sobre las filas del archivo CSV
    contador = 0
    for fila in lector_csv:
        # Acceder a cada valor de la fila
        print(fila)
        #fila = fila.strip().split(",")
        nombre_ciudad = fila[0]
        latitud = float(fila[2])
        longitud = float(fila[3])
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
            
        contador = contador + 1
        if contador == 2:
            break

    
            
    
    

    