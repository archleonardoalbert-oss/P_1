from abc import ABC
from abc import abstractclassmethod
from dependencias import *

class Event(ABC):
    def __init__(self, start_date, end_date, resources, depen = None, name = None):
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.depen = depen
        self.resources = resources

    def __repr__(self):
        info = {
            "start_date" : self.start_date,
            "end_date" : self.end_date,
            "depen" : self.depen,
            "resources" : self.resources 
        }

        return f"{info}"
    

class Espectaculo_Humoristico(Event):
    depend = dependencias_eventos_definidos[0]
    nam = 'Espectaculo Humoristico'
    def __init__(self, start_date, end_date, resources, depen = depend, name = nam):
        super().__init__(start_date, end_date, resources, depen, name)

class Evento_Cultural(Event):
    depend = dependencias_eventos_definidos[1]
    nam = 'Evento Cultural'
    def __init__(self, start_date, end_date, resources, depen = depend, name = nam):
        super().__init__(start_date, end_date, resources, depen, name)

class Reunion_De_Negocios(Event):
    depend = dependencias_eventos_definidos[2]
    nam = 'Reunion de Negocios'
    def __init__(self, start_date, end_date, resources, depen = depend, name = nam):
        super().__init__(start_date, end_date, resources, depen, name)

class Remodelacion(Event):
    depend = dependencias_eventos_definidos[3]
    nam = 'Remodelacion'
    def __init__(self, start_date, end_date, resources, depen = depend, name = nam):
        super().__init__(start_date, end_date, resources, depen, name)

class Excurcion(Event):
    depend = dependencias_eventos_definidos[4]
    nam = 'Excursion'
    def __init__(self, start_date, end_date, resources, depen = depend, name = nam):
        super().__init__(start_date, end_date, resources, depen, name)

class Torneo_Gamer(Event):
    depend = dependencias_eventos_definidos[5]
    nam = 'Torneo Gamer'
    def __init__(self, start_date, end_date, resources, depen = depend, name = nam):
        super().__init__(start_date, end_date, resources, depen, name)

class Temporada_De_Ofertas(Event):
    depend = dependencias_eventos_definidos[6]
    nam = 'Temporada de Ofertas'
    def __init__(self, start_date, end_date, resources, depen = depend, name = nam):
        super().__init__(start_date, end_date, resources, depen, name)

class Evento_Personalizado(Event):
    def __init__(self, start_date, end_date, resources, depen, name):
        super().__init__(start_date, end_date, resources, depen, name)



