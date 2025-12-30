import json
import events


new_refresh = True

resources = {
             "mesas" : 4,
             "sillas" : 12,
             "organizador" : 15,
             "comida" : 10000
}
collitions = {
            "mesas" : ('mesas'),
            "sillas" : ('sillas'),
            "organizador" : ('organizador')
}

def Refresh_data_base(events, collitions, resources, date_interval):
    info = {
        "events" : events,
        "collitions" : collitions,
        "resources" : resources,
        "date_interval" : date_interval
    }

    with open("Database.json", "w", encoding= "utf-8") as file:
        json.dump(info, file, indent= 4) #json.dump(datos, file, indent = 4) ident = 4 -> autoformater

    


    new_refresh = True


def Load_date_base(element): #elements da indicaciones para decidir lo que voy a importar concretamente
    if new_refresh:
        with open("Database.json", "r", encoding = "utf-8") as file:
            datos_leidos = json.load(file) #json.load() construye una estructura de python

        new_refresh = False

        return datos_leidos[element]