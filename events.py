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
    depend = E_h_depe
    nam = 'Espectaculo Humoristico'
    def __init__(self, start_date, end_date, resources, depen = depend, name = nam):
        super().__init__(start_date, end_date, resources, depen, name)

class Evento_Cultural(Event):
    depend = E_c_depe
    nam = 'Evento Cultural'
    def __init__(self, start_date, end_date, resources, depen = depend, name = nam):
        super().__init__(start_date, end_date, resources, depen, name)

class Evento_Personalizado(Event):
    def __init__(self, start_date, end_date, resources, depen, name):
        super().__init__(start_date, end_date, resources, depen, name)



