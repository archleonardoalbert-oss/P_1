import abc
from abc import abstractclassmethod

class Event(abc):
    def __inti__(self, start_date, end_date, depen, resources, name):
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.depen = depen
        self.resources = resources

    def __repr__(self):
        info = {
            "start_date" : self.start_date,
            "end_date" : self.end_date,
            "depem" : self.depen,
            "resources" : self.resources 
        }

        return f"{info}"
    

#Listo para definir eventos concretos
class Espectaculo_Humoristico(Event):
    depen = ["mesas", "sillas", "organizador"]
    name = 'Espectaculo Humoristico'
    pass

class Evento_Cultural(Event):
    depen = ["mesas", "sillas", "organizadpr"]
    name = 'Evento Cultural'
    pass

class Evento_Personalizado(Event):
    pass #Se personalizan las dependencias y el nombre



