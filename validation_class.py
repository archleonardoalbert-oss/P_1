import datetime
from interface_back import Load_date_base
import json


class Validation():
    def __init__(self, s_d, e_d, depe, resources):
        self.s_d = s_d
        self.e_d = e_d
        self.depe = depe
        self.resources = resources

    def Check_date_interval(self) -> bool:
        pass

    def Check_min_resources(self) -> tuple:
        result = True
        mistake = []
        for d in self.depe:
            if not d in self.resources:
                result = False
                mistake.append(d)

        return (result, mistake)

    def Check_global_resources(self) -> tuple:
        pass

    def Check_collitions(self) -> tuple:
        collitions = Load_date_base("collitions")
        result = True
        mistake = []
        for r in self.resources:
            for i in collitions[r]:
                if i in self.resources:
                    result = False
                    if not (r, i) in mistake: #Porque el orden no importa
                        mistake.append((i, r)) #Tantasveces como aparezca es la cantidad de veces que se viola la colicion
                                               # con el objeto i
        
        return (result, mistake)

    def Check_r_d(self, formate = "%Y-%m-%d") -> bool:
        "Verifica si el intervalo de la fecha del evento es valido"

        try:
            #Intentamos convertir la cadena en un objeto datetime real
            datetime.strptime(self.s_d, formate)
            datetime.strptime(self.e_d, formate)

            return True
        
        except ValueError:
            return False

    def Valid(self, result: tuple) -> bool:
        for i in result:
            if len(i) >= 1:
                if not i[0]:
                    return False
            
            if not i:
                return False
        
    
    def Details(self) -> tuple:
        result = (
            self.Check_date_interval(),
            self.check_min_resources(),
            self.Check_collitions(),
            self.Check_global_resources(),
            self.Check_r_d()
        )

        result.append(self.Valid(result))

        return result
