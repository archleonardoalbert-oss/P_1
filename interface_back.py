import json
import events
from datetime import datetime as date, timedelta
from dependencias import *
import ulid

e1 = 'Espectaculo Humoristico'
e2 = 'Evento Cultural'
e3 = 'Reunion de negocios'
e4 = 'Remodelacion'
e5 = 'Excurcion'
e6 = 'Torneo gamer'
e7 = 'Temporada de ofertas'
e8 = 'Personalizado'

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
        f = "%d/%m/%Y"

        try:
            for event in all_events:
                #Los intervalos de ocurrencia de los eventos tienen alguna interseccion
                start_date_intersection = date.strptime(event['start_date'], f) <= date.strptime(self.s_d, f) <= date.strptime(event['end_date'], f)
                end_date_intersection = date.strptime(event['start_date'], f) <= date.strptime(self.e_d, f) <= date.strptime(event['end_date'], f)
                if start_date_intersection or end_date_intersection:
                    for resource in event['resources']:
                        all_resources[resource] -= 1 
        
        except ValueError:
            return ("Imposible determinar", [])
        
        mistake = []
        for r in self.resources:
            if all_resources[r] <= 0: #No deberia dar nueca < 0 pero por si acaso
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

    def Check_depen_resources(self) -> tuple:
        "Verifica si todos los recursos que exige el evento son consistentes entre si"

        depen = Load_date_base('depen_resources')
        mistake_cause = []
        mistake_reason = []
        result = True
        for r in self.resources:
            for d in depen[r]:
                if not d in self.resources:
                    result = False
                    mistake_cause.append(r)
                    mistake_reason.append(d)

        return (result, mistake_cause, mistake_reason)

    def Check_r_d(self, formate = "%d/%m/%Y") -> bool:
        "Verifica si el intervalo de la fecha del evento es valido"

        try:
            #Intentamos convertir la cadena en un objeto datetime real
            a = date.strptime(self.s_d, formate)
            b = date.strptime(self.e_d, formate)

            return True if b >= a else False
        
        except ValueError:
            return False

    def Valid(self, result: list) -> bool:
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
        3) Check_depen_resources():
                                - bool de si los recursos del evento son consistentes entre si (se respetan las dependencias de los recursos)
                                - mistake_cause: los recursos los cuales no estan satisfechas sus dependencias
                                - mistake_reason: los recursos que faltan para satisfacer las dependencias de mistake_cause   
        4) Check_global_resources():
                                - bool de si para la fecha planificada del evento estan disponibles los recursos que este pide (True) o si no (False)
                                - lista de los recursos que faltan en dicha fecha para que el evento se pueda llevar a cabo 
        5)Check_r_d():
                                - bool de si la fecha introducida por el usuario esta en un formato correcto  (True) o no (False)    
                                
        6)Valid():              
                                - bool de si el evento pasa todas las validaciones (True) o no (False)
        """

        result = [
            self.Check_min_resources(),
            self.Check_collitions(),
            self.Check_depen_resources(),
            self.Check_global_resources(),
            self.Check_r_d()
        ]

        result.append(self.Valid(result))

        return result

def Refresh_data_base_event(event):
    with open('Database.json', 'r', encoding= 'utf-8') as db:
        db_dict = json.load(db)

    events = db_dict['events']
    event_dict = event.__dict__
    event_dict.update({"id" : str(ulid.new())})
    events.append(event_dict)
    

    with open("Database.json", "w", encoding= "utf-8") as db:
        json.dump(db_dict, db, indent= 4) #json.dump(datos, file, indent = 4) ident = 4 -> autoformater

def Refresh_data_base_logic(action: str,typ: str, key, value: int = None, a: list = None, d: list = None):
    with open('Database.json', 'r', encoding= 'utf-8') as db:
        db_dict = json.load(db)

    if typ == 'resources':
        if action == 'a':
            db_dict['resources'].update({key: value})
        elif action == 'd':
            try:
                del db_dict['resources'][key]
            except KeyError:
                return False
        elif action == 'm':
            try:
                db_dict['resources'][key] = value
            except KeyError:
                return False

    elif typ == 'collitions':
        if action == 'a':
            db_dict['collitions'].update({key: value}) 
        elif action == 'd':
            try:
                del db_dict['collitions'][key]
                for coll in db_dict['collitions'].values():
                    if key in coll:
                        coll.remove(key)
            except KeyError:
                return False
        elif action == 'm':
            try:
                for c_a in a:
                    db_dict['collitions'][key].append(c_a)
                
                for c_d in d:
                    db_dict['collitions'][key].remove(c_d)
            except KeyError:
                return False
        

    elif typ == 'depen_resources':
        if action == 'a':
            db_dict['depen_resources'].update({key: value})
        elif action == 'd':
            try:
                del db_dict['depen_resources'][key]
                for dep in db_dict['depen_resources'].values():
                    if key in dep:
                        dep.remove(key)
            except KeyError:
                return False
        elif action == 'm':
            try:
                for d_a in a:
                    db_dict['depen_resources'][key].append(d_a)
                
                for d_d in d:
                    db_dict['depen_resources'][key].remove(d_d)
            except KeyError:
                return False

    #Por pura robustez
    else :
        return False


    with open('Database.json', 'w', encoding= 'utf-8') as db:
        json.dump(db_dict, db, indent= 4)

    return True


def Refresh_visualization():
    events = Load_date_base('events')
    colors = ['#FF0000', '#00FF00', '#0000FF', '#FFFF00', '#FF00FF']
    processed_events = []

    for i in range(len(events)):
        event = events[i]
        #Procesamiento de fechas
        f_start_date = event['start_date'].split('/')
        f_end_date = event['end_date'].split('/')
        for date in [f_start_date, f_end_date]:
            if len(date[0]) == 1:
                date[0] = '0' + date[0]
            
            if len(date[1]) == 1:
                date[1] = '0' + date[1]
            
            date[0], date[2] = date[2], date[0]


        f_start_date = '-'.join(f_start_date)
        f_end_date = '-'.join(f_end_date)

        color = colors[i % len(colors)] #Asignandole un color al evento

        processed_events.append({
            'title': event['name'],
            'start': f_start_date,
            'end': f_end_date,
            'color': color,
            'id' : event['id'],
            'resources' : event['resources'],
            'depen': event['depen'] })

    return processed_events


def Load_date_base(element): #elements da indicaciones para decidir lo que voy a importar concretamente
    with open("Database.json", "r", encoding = "utf-8") as file:
        datos_leidos = json.load(file) #json.load() construye una estructura de python

    return datos_leidos[element]


def Delete_event(ID: list):
    with open('Database.json', 'r', encoding = 'utf-8') as db:
        db_dict = json.load(db)
    
    events, coll, dep = db_dict['events'], db_dict['collitions'], db_dict['depen_resources']
    for id in ID:
        for e in events:
            if id == e['id']:
                events.remove(e)     
            
        with open('Database.json', 'w', encoding = 'utf-8') as db:
            json.dump(db_dict, db, indent = 4)


def Delete_all_events():
    with open('Database.json', 'r', encoding= 'utf-8') as db:
        db_dict = json.load(db)

    db_dict['events'] = []


    with open('Database.json', 'w', encoding = 'utf-8') as db:
            json.dump(db_dict, db, indent = 4)

def Try_event(event_type: str, start_date: str, end_date: str, resources: list,  depen: list) -> list:
    if event_type == 'Espectaculo Humoristico':
        validation = Validation(start_date, end_date, dependencias_eventos_definidos[0], resources)
    
    elif event_type == 'Evento Cultural':
        validation = Validation(start_date, end_date, dependencias_eventos_definidos[1], resources)

    elif event_type == 'Reunion de negocios':
        validation = Validation(start_date, end_date, dependencias_eventos_definidos[2], resources)

    elif event_type == 'Remodelacion':
        validation = Validation(start_date, end_date, dependencias_eventos_definidos[3], resources)

    elif event_type == 'Excurcion':
        validation = Validation(start_date, end_date, dependencias_eventos_definidos[4], resources)

    elif event_type == 'Torneo gamer':
        validation = Validation(start_date, end_date, dependencias_eventos_definidos[5], resources)

    elif event_type == 'Temporada de ofertas':
        validation = Validation(start_date, end_date, dependencias_eventos_definidos[6], resources)

    elif event_type == 'Personalizado':
        validation = Validation(start_date, end_date, depen, resources)
    return validation.Details()


def Find_Date(event_type: str, start_date: str, end_date: str, resources: list,  depen: list):
    format = '%d/%m/%Y'
    try:
        start_date_D = date.strptime(start_date, format)
        end_date_D = date.strptime(end_date, format)
    except:
        return False

    while not Try_event(event_type, start_date, end_date, resources, depen)[-1]:
        start_date_D = start_date_D + timedelta(days= 1)
        end_date_D = end_date_D + timedelta(days= 1)

        start_date = start_date_D.strftime(format)
        end_date = end_date_D.strftime(format)

    return (start_date, end_date)

    
def Button_save_func(sd: str, ed: str, ty: str, depe: list, re: list, name: str) -> tuple:
                validation = Try_event(ty, sd, ed, re, depe)
                
                onj = None

                if validation[-1]:
                    if ty == e1:
                        obj = events.Espectaculo_Humoristico(sd, ed, re)
                    elif ty == e2:
                        obj = events.Evento_Cultural(sd, ed, re)
                    elif ty == e3:
                        obj = events.Reunion_De_Negocios(sd, ed, re)
                    elif ty == e4:
                        obj = events.Remodelacion(sd, ed, re)
                    elif ty == e5:
                        obj = events.Excurcion(sd, ed, re)
                    elif ty == e6:
                        obj = events.Torneo_Gamer(sd, ed, re)
                    elif ty == e7:
                        obj = events.Temporada_De_Ofertas(sd, ed, re)
                    elif ty == e8:
                        obj = events.Evento_Personalizado(sd, ed, re, depe, name)
                    
                    Refresh_data_base_event(obj)
                    return ('success',)
                    #ESTO VA PARA EL FRONT
                    #st.success('Evento agregado exitosamente')
                    # if not stack == 1:
                    #     start_date = datetime.datetime.strptime(start_date, '%d/%m/%Y') + timedelta(days= periodicity)
                    #     start_date = start_date.strftime('%d/%m/%Y')
                    #     end_date = datetime.datetime.strptime(end_date, '%d/%m/%Y') + timedelta(days= periodicity)
                    #     end_date = end_date.strftime('%d/%m/%Y')
                
                elif validation[4] and validation[0][0] and validation[1][0] and validation[2][0] and not validation[3][0]:
                    message = f"""Para la fecha que requiere su evento no tenemos dsponibles los recursos ({validation[3][1]}).\r\n
        Le sugerimos que planifique el evento en la siguiente fecha disponible ())"""
                    return ('suggested', message)
                    
                
                elif not validation[4] or not validation[0][0] or not validation[1][0] or not validation[2][0] or not validation[3][0]:
                    depen_resources = ''
                    #Preparando el str de las dependencias de recursos fallidas si es que las hay
                    for c in validation[2][1]:
                        for r in validation[2][2]:
                            depen_resources += f'                                     {c}  <-//-  {r} \n\r'
                    message = f'''Ha ocurrido un error: 
                        

                        
            -Recursos minimos necesarios: {validation[0]}\n\r
            -Coliciones entre recursos: {validation[1]}\n\r
            -Las dependencias de los recursos fallidas: \n{depen_resources} \n\r
            -Insuficiencia de recursos globales: {validation[3]} \n\r
            -Validez de intervalo de fecha: {validation[4]}
                        '''

                        #Estilizando mensaje
                    message = message.replace('[', '').replace(']', '').replace("'", '').replace('False', 'Error').replace('True', 'Ok').replace('Ok, ', 'Ok').replace('Error, ', 'Error: ')
                    return ('error', message)


