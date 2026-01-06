from abc import ABC
from abc import abstractclassmethod

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
    

#Listo para definir eventos concretos
class Espectaculo_Humoristico(Event):
    depend = ["mesas", "sillas", "organizador"]
    nam = 'Espectaculo Humoristico'
    def __init__(self, start_date, end_date, resources, depen = depend, name = nam):
        super().__init__(start_date, end_date, resources, depen, name)

class Evento_Cultural(Event):
    depend = ["mesas", "sillas", "organizador"]
    nam = 'Evento Cultural'
    def __init__(self, start_date, end_date, resources, depen = depend, name = nam):
        super().__init__(start_date, end_date, resources, depen, name)

class Evento_Personalizado(Event):
    pass #Se personalizan las dependencias y el nombre



