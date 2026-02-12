import streamlit as st
import interface_back
from interface_back import events
import datetime
from datetime import timedelta, datetime
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
            
            c = st.columns([1, 1])
            with c[0]:
                periodicity = st.number_input(
                    'Personalice la periodicidad de su evento (dias)',
                    value= 1,
                    step= 1,
                    min_value= 1
                )
            with c[1]:
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
            
            if st.button('Guardar'):
                st.success('Se presiono el boton de guardar')
                validation_main = interface_back.Try_event(event_type, start_date, end_date, selected_resources, depe)
                events_list = []
                st.session_state.modified_events = []
                only_global_resources = validation_main[0][0] and validation_main[1][0] and validation_main[2][0] and validation_main[4] and not validation_main[3][0]
                old_events = interface_back.Load_date_base('events')

                if validation_main[-1] or only_global_resources:
                    for i in range(stack):
                        st.success('Entro en el bucle')
                        event_attributes = {
                            'sd': start_date,
                            'ed': end_date,
                            'dp': depe,
                            're': selected_resources,
                            'na': name,
                            'ty': event_type
                        }
                        
                        st.success('Va a hacer la primera validacion')
                        if not interface_back.Try_event_shadow(event_attributes, total_resources, old_events)[0]: #El problema se da en esta verificacion
                            nice_dates = interface_back.Find_Date(event_attributes['ty'], event_attributes['sd'], event_attributes['ed'], event_attributes['re'], event_attributes['dp'])
                            st.warning(f'''La fecha en la que se ha intentado crear el evento esta ocupada, insuficiencia de los \n\r
                                       recursos {interface_back.Try_event_shadow(event_attributes, total_resources, old_events)[1]}, le recomendaremos \n\r
                                       la fecha ({nice_dates[0]} --> {nice_dates[1]}) en la cual se ecnuentran disponibles dichos \n\r
                                       recursos''')
                        
                            
                            event_attributes['sd'] = nice_dates[0]
                            event_attributes['ed'] = nice_dates[1]
                            st.session_state.modified_events.append(event_attributes.copy())


                        else:
                            st.success('Comnezo a agregar los atributos a la lista')
                            events_list.append(event_attributes.copy())
                            st.success('Agrego los atributos a la lista')

                        #Modificando fecha
                        start_date = datetime.strptime(start_date, '%d/%m/%Y') + timedelta(days= periodicity)
                        start_date = start_date.strftime('%d/%m/%Y')
                        end_date = datetime.strptime(end_date, '%d/%m/%Y') + timedelta(days= periodicity)
                        end_date = end_date.strftime('%d/%m/%Y')

                    #Cuando termine el bucle:
                    else:
                        st.success('Llego a la parte de guardar eventos')
                        interface_back.Button_save_func(events_list)

                else:
                    depen_resources = ''
                    for c in validation_main[2][1]:
                        for r in validation_main[2][2]:
                            depen_resources += f'                                     {c}  <-//-  {r} \n\r'
                    message = f'''Ha ocurrido un error: 
                        
                        
            -Recursos minimos necesarios: {validation_main[0]}\n\r
            -Coliciones entre recursos: {validation_main[1]}\n\r
            -Las dependencias de los recursos fallidas: \n{depen_resources} \n\r
            -Insuficiencia de recursos globales: {validation_main[3]} \n\r
            -Validez de intervalo de fecha: {validation_main[4]}
                        '''
                        #Estilizando mensaje
                    message = message.replace('[', '').replace(']', '').replace("'", '').replace('False', 'Error').replace('True', 'Ok').replace('Ok, ', 'Ok').replace('Error, ', 'Error: ')

                    st.error(message)


                if len(st.session_state.modified_events) > 0:
                    if st.button('Aceptar sugerencias'):
                        for e in st.session_state.modified_events:
                            interface_back.Button_save_func(st.session_state.modified_events)
                            st.session_state.modified_events = []
                        st.rerun()

                    if st.button('Rechazar sugerencias'):
                        st.session_state.modified_events = []
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


            if st.button('Limpiar eventos'):
                interface_back.Delete_all_events()
    


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

