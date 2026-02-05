import streamlit as st
import interface_back
from interface_back import events
import datetime
from datetime import timedelta
from datetime import date
from pathlib import Path
import sys

# Subir al directorio P_1
ruta_base = Path(__file__).parent.parent  # Esto te lleva a P_1
sys.path.insert(0, str(ruta_base))


total_resources = interface_back.Load_date_base('resources')
def Administrar():
    st.header('Administracion de Eventos')

    #Creando 3 columnas para mejor visualizacion de la interfaz
    col_left, col_mid, col_right = st.columns([1, 5, 2], border= True)

    #Inicializando st.session_state 
    if 'Crear' not in st.session_state:
        st.session_state.Crear = False
    
    if 'Eliminar' not in st.session_state:
        st.session_state.Eliminar = False

    if 'Ok' not in st.session_state:
        st.session_state.Ok = False

    if 'typ' not in st.session_state:
        st.session_state['typ'] = None

    e1 = 'Espectaculo Humoristico'
    e2 = 'Evento Cultural'
    e3 = 'Reunion de negocios'
    e4 = 'Remodelacion'
    e5 = 'Excurcion'
    e6 = 'Torneo gamer'
    e7 = 'Temporada de ofertas'
    e8 = 'Personalizado'
    

    #Al precionar los botones activa su respectivo "espacio de widgets" y desactiva el del otro boton
    with col_left:
        if st.button('Crear'):
            st.session_state.Crear = not st.session_state.Crear
            if st.session_state.Eliminar:
                st.session_state.Eliminar = False

        if st.button('Eliminar'):
            st.session_state.Eliminar = not st.session_state.Eliminar
            if st.session_state.Crear:
                st.session_state.Crear = False


    with col_mid:
        #Crear
        if st.session_state.Crear:

            name = None
            depe = None
            
            st.session_state['typ'] = st.selectbox(
                'Que tipo de evento quiere crear ?',
                [e1, e2, e3, e4, e5, e6, e7, e8])
            
            event_type = st.session_state['typ']
            start_date = st.date_input(
                'Ingrese la fecha de inicio del evento',
                  value= date.today(),
                    format= 'DD/MM/YYYY').strftime('%d/%m/%Y')
            
            end_date = st.date_input(
                'Ingrese la fecha de finalizacion del evento',
                  value= date.today(),
                    format= 'DD/MM/YYYY').strftime('%d/%m/%Y')
            
            periodicity = st.number_input(
                'Personalice la periodicidad de su evento (dias)',
                value= 1,
                step= 1,
                min_value= 1
            )

            stack = st.session_state.Stack = st.number_input(
                'Especifique la cantidad de ciclos de su evento',
                value= 1,
                step= 1,
                min_value= 1
            )

            
            selected_resources = st.multiselect(
                'Que recursos requerira para su evento ?',
                  options= total_resources,
                    key= 'multiselect1')


            if event_type == e8:
                name = st.text_input('Nombre del evento')
                depe = st.multiselect('Que recursos necesita tu evento ?', options= total_resources)
            
            if 'Save' not in st.session_state:
                st.session_state.Save = False

            if st.button('Save'):
                st.session_state.Save = not st.session_state.Save
            
            if st.session_state.Save:
                st.session_state.Save = not st.session_state.Save
                validation = st.session_state.Validation =  interface_back.Try_event(event_type, start_date, end_date, selected_resources, depe)
                
                onj = None

                for m in range(stack):
                    st.session_state.Stack_pass = m #Para mantener informacion global sobre que tanto se ha recorrido del stack 
                    validation = interface_back.Try_event(event_type, start_date, end_date, selected_resources, depe)

                    if validation[-1]:
                        if event_type == e1:
                            obj = events.Espectaculo_Humoristico(start_date, end_date, selected_resources)
                        elif event_type == e2:
                            obj = events.Evento_Cultural(start_date, end_date, selected_resources)
                        elif event_type == e3:
                            obj = events.Reunion_De_Negocios(start_date, end_date, selected_resources)
                        elif event_type == e4:
                            obj = events.Remodelacion(start_date, end_date, selected_resources)
                        elif event_type == e5:
                            obj = events.Excurcion(start_date, end_date, selected_resources)
                        elif event_type == e6:
                            obj = events.Torneo_Gamer(start_date, end_date, selected_resources)
                        elif event_type == e7:
                            obj = events.Temporada_De_Ofertas(start_date, end_date, selected_resources)
                        elif event_type == e8:
                            obj = events.Evento_Personalizado(start_date, end_date, selected_resources, depe, name)
                        
                        interface_back.Refresh_data_base_event(obj)
                        st.success('Evento agregado exitosamente')

                        if not stack == 1:
                            start_date = datetime.datetime.strptime(start_date, '%d/%m/%Y') + timedelta(days= periodicity)
                            start_date = start_date.strftime('%d/%m/%Y')

                            end_date = datetime.datetime.strptime(end_date, '%d/%m/%Y') + timedelta(days= periodicity)
                            end_date = end_date.strftime('%d/%m/%Y')
                    
                    if validation[4] and validation[0][0] and validation[1][0] and validation[2][0] and not validation[3][0]:
                        st.session_state.Ok = True
                        break
                    
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
                        st.error(message)
                
                #IMPLEMENTAR PROGRAMACION DE EVENTOS POR STACK IGUALMENTE EN LA SUGERENCIA
                if st.session_state.Ok:
                        validation = st.session_state.Validation
                        #for m in range(st.session_state.Stack - st.session_state.Stack_pass):
                        suggested_date = interface_back.Find_Date(event_type, start_date, end_date, selected_resources, depe)

                        if not suggested_date == False:
                            st.warning(f"""Para la fecha que requiere su evento no tenemos dsponibles los recursos ({validation[3][1]}).\r\n
        Le sugerimos que planifique el evento en la siguiente fecha disponible ({suggested_date})""")
                            
                            if event_type == e1:
                                obj = events.Espectaculo_Humoristico(suggested_date[0], suggested_date[1], selected_resources)
                            elif event_type == e2:
                                obj = events.Evento_Cultural(suggested_date[0], suggested_date[1], selected_resources)
                            elif event_type == e3:
                                obj = events.Reunion_De_Negocios(suggested_date[0], suggested_date[1], selected_resources)
                            elif event_type == e4:
                                obj = events.Remodelacion(suggested_date[0], suggested_date[1], selected_resources)
                            elif event_type == e5:
                                obj = events.Excurcion(suggested_date[0], suggested_date[1], selected_resources)
                            elif event_type == e6:
                                obj = events.Torneo_Gamer(suggested_date[0], suggested_date[1], selected_resources)
                            elif event_type == e7:
                                obj = events.Temporada_De_Ofertas(suggested_date[0], suggested_date[1], selected_resources)
                            elif event_type == e8:
                                obj = events.Evento_Personalizado(suggested_date[0], suggested_date[1], selected_resources, depe, name)

                            if st.button('Ok', key= 'confirmar_fecha_sugerida'):
                                st.session_state.Ok = False
                                interface_back.Refresh_data_base_event(obj)
                                st.rerun()


        #Eliminar
        if st.session_state.Eliminar:
            ESPACIO_NO_QUEBRANTABLE = '\u00A0'
            ids = {}
            _events = interface_back.Load_date_base('events')

            for e in _events:
                ids.update({ e['id'] : f'{e['id']}{ESPACIO_NO_QUEBRANTABLE * 8}------>{ESPACIO_NO_QUEBRANTABLE * 8}{e['name']} ({e['start_date']} - {e['end_date']})'})

            id = st.multiselect(
                'Seleccione el ID del elemento que desea eliminar',
                 options = ids.keys(),
                 format_func= lambda k: ids[k],
                 key= 'multiselect2'
                 )


            if st.button('OK'):
                interface_back.Delete_event(id)
                st.rerun()

    


    with col_right:
        event_type = st.session_state['typ']

        if event_type == e1:
            st.image('Media/creacion_eventos/Espectaculo_Humoristico.jpg', width= 450)
        elif event_type == e2:
            st.image('Media/creacion_eventos/Evento_cultural.jpg', width= 370)
        elif event_type == e3:
            st.image('Media/creacion_eventos/Reunion_de_negocios.jpg', width= 370)
        elif event_type == e4:
            st.image('Media/creacion_eventos/Remodelacion.jpg', width= 370)
        elif event_type == e5:
            st.image('Media/creacion_eventos/Excursion.jpg', width= 370)
        elif event_type == e6:
            st.image('Media/creacion_eventos/Gamer.jpg', width= 370)
        elif event_type == e7:
            st.image('Media/creacion_eventos/Ofertas.jpg', width= 370)
        elif event_type == e8:
            st.image('Media/creacion_eventos/Personalizado.jpg')

