import requests
import urllib.parse

route_url = "https://graphhopper.com/api/1/route?"
key = "9bcaa2e2-49c0-4c1e-932e-9052a756ab01"
idioma = "es"


def es_salida(texto):
    return texto.strip().lower() in ("s", "salir")


def geocoding (location, key):
    while location == "":
        location = input("Ingrese la ubicación nuevamente: ")
    geocode_url = "https://graphhopper.com/api/1/geocode?" 
    url = geocode_url + urllib.parse.urlencode({"q":location, "limit": "1", "locale":idioma, "key":key})

    replydata = requests.get(url)
    json_data = replydata.json()
    json_status = replydata.status_code
    
    if json_status == 200 and len(json_data["hits"]) != 0:
        json_data = requests.get(url).json()
        lat=(json_data["hits"][0]["point"]["lat"])
        lng=(json_data["hits"][0]["point"]["lng"])
        name = json_data["hits"][0]["name"]
        value = json_data["hits"][0]["osm_value"]
        
        if "country" in json_data["hits"][0]:
            country = json_data["hits"][0]["country"]
        else:
            country=""
        
        if "state" in json_data["hits"][0]:
            state = json_data["hits"][0]["state"]
        else:
            state=""
        
        if len(state) !=0 and len(country) !=0:
            new_loc = name + ", " + state + ", " + country
        elif len(state) !=0:
            new_loc = name + ", " + country
        else:
            new_loc = name
        print("URL de la API de geocodificación para " + new_loc + " (Tipo de ubicación: " + value + ")\n" + url)
    else:
        lat="null"
        lng="null"
        new_loc=location
        if json_status != 200:
            print("Estado de la API de geocodificación: " + str(json_status) + "\nMensaje de error: " + json_data["message"])
        else:
            print("No se encontró la ubicación: " + location)
    return json_status,lat,lng,new_loc

while True:
    print("\n+++++++++++++++++++++++++++++++++++++++++++++")
    print("Perfiles de vehículo disponibles en Graphhopper:")
    print("+++++++++++++++++++++++++++++++++++++++++++++")
    print("car (auto), bike (bicicleta), foot (a pie)")
    print("+++++++++++++++++++++++++++++++++++++++++++++")
    profile=["car", "bike", "foot"]
    vehicle = input("Ingrese un perfil de vehículo de la lista anterior (s o salir para terminar): ")
    if es_salida(vehicle):
        break
    elif vehicle in profile:
        vehicle = vehicle
    else: 
        vehicle = "car"
        print("No se ingresó un perfil de vehículo válido. Se usará el perfil car (auto).")

    loc1 = input("Ubicación de origen: ")
    if es_salida(loc1):
        break
    orig = geocoding(loc1, key)
    loc2 = input("Destino: ")
    if es_salida(loc2):
        break
    dest = geocoding(loc2, key)
    print("=================================================")
    if orig[0] == 200 and dest[0] == 200:
        op="&point="+str(orig[1])+"%2C"+str(orig[2])
        dp="&point="+str(dest[1])+"%2C"+str(dest[2])
        paths_url = route_url + urllib.parse.urlencode({"key":key, "vehicle":vehicle, "locale":idioma}) + op + dp
        paths_status = requests.get(paths_url).status_code
        paths_data = requests.get(paths_url).json()
        print("Estado de la API de rutas: " + str(paths_status) + "\nURL de la API de rutas:\n" + paths_url)
        print("=================================================")
        print("Indicaciones desde " + orig[3] + " hasta " + dest[3] + " en modo " + vehicle)
        print("=================================================")
        if paths_status == 200:
            miles = (paths_data["paths"][0]["distance"])/1000/1.61
            km = (paths_data["paths"][0]["distance"])/1000
            sec = int(paths_data["paths"][0]["time"]/1000%60)
            min = int(paths_data["paths"][0]["time"]/1000/60%60)
            hr = int(paths_data["paths"][0]["time"]/1000/60/60)
            print("Distancia recorrida: {0:.2f} millas / {1:.2f} km".format(miles, km))
            print("Duración del viaje: {0:01d}:{1:01d}:{2:01d}".format(hr, min, sec))
            print("=================================================")
            for each in range(len(paths_data["paths"][0]["instructions"])):
                path = paths_data["paths"][0]["instructions"][each]["text"]
                distance = paths_data["paths"][0]["instructions"][each]["distance"]
                print("{0} ( {1:.2f} km / {2:.2f} millas )".format(path, distance/1000, distance/1000/1.61))
            print("=============================================")
        else:
            print("Mensaje de error: " + paths_data["message"])
            print("*************************************************")