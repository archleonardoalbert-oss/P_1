import json
import events
from datetime import datetime as date


class Validation(): 
    def __init__(self, s_d, e_d, depe, resources):
        self.s_d = s_d
        self.e_d = e_d
        self.depe = depe
        self.resources = resources

    def Check_min_resources(self) -> tuple:
        "Verifica si se cumplen los recursos minimos que tiene asociado el evento para funcionar"

        result = True
        mistake = []
        for d in self.depe:
            if not d in self.resources:
                result = False
                mistake.append(d)

        return (result, mistake)

    def Check_global_resources(self) -> tuple:
        all_events = Load_date_base("events")
        all_resources = Load_date_base("resources")
        result = True
        f = "%Y/%m/%d"

        for event in all_events:
            #Los intervalos de ocurrencia de los eventos tienen alguna interseccion
            start_date_intersection = date.strptime(event['start_date'], f) <= date.strptime(self.s_d, f) <= date.strptime(event['end_date'], f)
            end_date_intersection = date.strptime(event['start_date'], f) <= date.strptime(self.e_d, f) <= date.strptime(event['end_date'], f)
            if start_date_intersection or end_date_intersection:
                for resource in event['resources']:
                    all_resources[resource] -= 1 
        
        mistake = []
        for r in self.depe:
            if all_resources[r] == 0:
                result = False
                mistake.append(r)
        
        return (result, mistake)

    def Check_collitions(self) -> tuple:
        "Verifica si algunos de los recursos del evento se repelen entre si"

        collitions = Load_date_base("collitions")
        result = True
        mistake = []
        for r in self.resources:
            for i in collitions[r]:
                if i in self.resources:
                    result = False
                    if not (r, i) in mistake: #Porque el orden no importa
                        mistake.append((i, r)) #Tantas veces como aparezca es la cantidad de veces que se viola la colicion
                                               # con el objeto i
        
        return (result, mistake)

    def Check_r_d(self, formate = "%Y/%m/%d") -> bool:
        "Verifica si el intervalo de la fecha del evento es valido"

        try:
            #Intentamos convertir la cadena en un objeto datetime real
            a = date.strptime(self.s_d, formate)
            b = date.strptime(self.e_d, formate)

            return True if b >= a else False
        
        except ValueError:
            return False

    def Valid(self, result: tuple) -> bool:
        "True si el evento es valido, False si no (basandose en las validaciones anteriores)"

        for i in result:
            if type(i) == tuple:
                if not i[0]:
                    return False
            
            elif not i:
                return False
        
        return True
    
    def Details(self) -> tuple:
        """Informacion completa y detallada de la validacion del evento:
        1) Check_min_resources():
                                - bool de si se satisfacen los recursos minimos para que el evento funcione (True) o no (False)
                                - lista de los recursos que faltan para que el evento funcione
        2) Check_collitions():
                                - bool de si ninguno de los recursos repele a otro (True) o si existe alguno que lo haga (False)
                                - lista de tuplas *[(a, b)]* donde *a* y *b* son recursos que se repelen entre si 
                                    (Si *a* aparece n veces en los recursos del evento (a, b) aparecera n veces en la lista)      
        3) Check_global_resources():
                                - bool de si para la fecha planificada del evento estan disponibles los recursos que este pide (True) o si no (False)
                                - lista de los recursos que faltan en dicha fecha para que el evento se pueda llevar a cabo 
        4)Check_r_d():
                                - bool de si la fecha introducida por el usuario esta en un formato correcto  (True) o no (False)    
                                """

        result = [
            self.Check_min_resources(),
            self.Check_collitions(),
            self.Check_global_resources(),
            self.Check_r_d()
        ]

        result.append(self.Valid(result))

        return result


resources = {
             "mesas" : 4,
             "sillas" : 12,
             "organizador" : 15,
             "comida" : 10000
}
collitions = {
            "mesas" : ('mesas'),
            "sillas" : ('sillas'),
            "organizador" : ('organizador'),
            "comida" : ('comida')
}

def Refresh_data_base(event):
    events = Load_date_base('events')
    events.append(event.__dict__)
    info = {
        "collitions" : collitions,
        "resources" : resources,
        "events" : events
    }

    with open("Database.json", "w", encoding= "utf-8") as file:
        json.dump(info, file, indent= 4) #json.dump(datos, file, indent = 4) ident = 4 -> autoformater

    

def Load_date_base(element): #elements da indicaciones para decidir lo que voy a importar concretamente
    with open("Database.json", "r", encoding = "utf-8") as file:
        datos_leidos = json.load(file) #json.load() construye una estructura de python

    return datos_leidos[element]



def Try_event(event_type: str, start_date: str, end_date: str, resources: list) -> bool:
    validation = Validation(start_date, end_date, ["mesas", "sillas", "organizador"], resources) #Tengo que implementar un mecanismo para manejar dinamicamente las dependencias
    event_details = validation.Details()
    if event_details[-1]:
        obj = events.Espectaculo_Humoristico(start_date, end_date, resources)
        Refresh_data_base(obj)

    return event_details
