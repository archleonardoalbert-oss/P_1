import abc
from abc import abstractclassmethod

class Event(abc):
    def __inti__(self, start_date, end_date, depen, resources):
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
    



