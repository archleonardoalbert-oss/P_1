#SE PUEDE CONSIDERAR LA OPCION DE QUE TODOS LOS METODOS DE LA CLASE VALIDATION NECESITEN EL PASE DE PARAMETROS, DE ESTA MANERA SERIA 
#SUFICIENTE CON CREAR UN SOLO OBJETO DE DICHA CLASE PARA VALIDAR TODOS LOS EVENTOS
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

        #Es necesario guardar los eventos en el .json con el siguiente formato:
        #{
        #   start_date: ...,
        #   end_date: ...,
        #   resources: ...,
        #}

        for event in all_events:
            #Los entervalos de ocurrencia de los eventos tienen alguna interseccion
            if event['start_date'] <= self.s_d <= event['end-date'] or event['start_date'] <= self.e_d <= event['end_date']:
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

    def Check_r_d(self, formate = "%Y-%m-%d") -> bool:
        "Verifica si el intervalo de la fecha del evento es valido"

        try:
            #Intentamos convertir la cadena en un objeto datetime real
            a = datetime.strptime(self.s_d, formate)
            b = datetime.strptime(self.e_d, formate)

            return True if b >= a else False
        
        except ValueError:
            return False

    def Valid(self, result: tuple) -> bool:
        "True si el evento es valido, False si no (basandose en las validaciones anteriores)"

        for i in result:
            if len(i) >= 1:
                if not i[0]:
                    return False
            
            if not i:
                return False
        
    
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

        result = (
            self.Check_min_resources(),
            self.Check_collitions(),
            self.Check_global_resources(),
            self.Check_r_d()
        )

        result.append(self.Valid(result))

        return result

