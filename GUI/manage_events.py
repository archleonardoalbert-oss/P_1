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

            name = 'Personalizado'
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
            
            if st.button('Guardar'):
                for i in range(stack):
                    st.session_state.Critic = True
                    result = interface_back.Button_save_func(start_date, end_date, event_type, depe, selected_resources, name)
                    if result[0] == 'suggested':
                        date_suggested = interface_back.Find_Date(event_type, start_date, end_date, selected_resources, depe)

                        message = result[1].replace('()', f'{date_suggested}'.replace(',', ' --> '))
                        st.warning(message)

                        st.session_state.modified_events.append({
                                'sd': date_suggested[0],
                                'ed': date_suggested[1],
                                'ty': event_type, 
                                'dp': depe,
                                're': selected_resources,
                                   'na': name})                
                    elif result[0] != 'success' :
                        st.error(result[1])
                        st.session_state.Critic = False
                        break

                    start_date = datetime.strptime(start_date, '%d/%m/%Y') + timedelta(days= periodicity)
                    start_date = start_date.strftime('%d/%m/%Y')

                    end_date = datetime.strptime(end_date, '%d/%m/%Y') + timedelta(days= periodicity)
                    end_date = end_date.strftime('%d/%m/%Y')
                
                else:
                    st.success('Accion ejecutada con exito')
                    st.session_state.Critic = False

            if len(st.session_state.modified_events) > 0:
                if st.button('Aceptar sugerencias'):
                    for e in st.session_state.modified_events:
                        interface_back.Button_save_func(
                            e['sd'],
                            e['ed'],
                            e['ty'],
                            e['dp'],
                            e['re'],
                            e['na']
                        )

                        st.session_state.modified_events.remove(e)
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

