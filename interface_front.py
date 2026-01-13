import streamlit as st
from streamlit_calendar import calendar as cal
import interface_back
from interface_back import events
import json
import datetime

total_resources = interface_back.resources.keys()
st.set_page_config(layout= "wide")
def main():
    st.title("Albert Hotel")

    #Menu lateral
    seccion = st.sidebar.selectbox(
        'Que quieres hacer ?',
        ['Inicio', 'Administrar eventos', 'Ver eventos', 'Info']
    )

    if seccion == 'Inicio':
        Inicio()
    elif seccion == 'Administrar eventos':
        Administrar()
    elif seccion == 'Ver eventos':
        Visualizacion()
    elif seccion == 'Info':
        Info()

######################################################################################################################################################
def Inicio():
    st.header('Bienvenido a Albert Hotel')
    st.markdown("""
    El objetivo de esta pagina es que tengas el poder de administrar los eventos de Albert Hotel
    """)

#-----------------------------------------------------------------------------------------------------------------------------------------------------

def Administrar():
    st.header('Administracion de Eventos')

    #Creando 3 columnas para mejor visualizacion de la interfaz
    col_left, col_mid, col_right = st.columns([1, 5, 1], border= True)

    #Inicializando st.session_state 
    if 'Crear' not in st.session_state:
        st.session_state.Crear = False
    
    if 'Eliminar' not in st.session_state:
        st.session_state.Eliminar = False
    
    

    #Al precionar los botones activa su respectivo "espacio de widgets" y desactiva el del otro boton
    with col_left:
        if st.button('Crear'):
            st.session_state.Crear = not st.session_state.Crear
            if st.session_state.Eliminar:
                st.session_state.Eliminar = False

    with col_right:
        if st.button('Eliminar'):
            st.session_state.Eliminar = not st.session_state.Eliminar
            if st.session_state.Crear:
                st.session_state.Crear = False

    #Columnas auxiliares para centrar la columna del medio:

    with col_mid:
        #Crear
        if st.session_state.Crear:
            e1 = 'Espectaculo Humoristico'
            e2 = 'Evento Cultural'
            e3 = 'Personalizado'

            name = None
            depe = None
            event_type = st.selectbox('Que tipo de evento quiere crear ?',
                                        [e1, e2, e3])
            start_date = st.text_input('Ingrese la fecha de inicio del evento')
            end_date = st.text_input('Ingrese la fecha de finalizacion del evento')
            selected_resources = st.multiselect('Que recursos requerira para su evento ?', options= total_resources)

            if event_type == e1:
                pass
            elif event_type == e2:
                pass
            elif event_type == e3:
                name = st.text_input('Nombre del evento')
                depe = st.multiselect('Que recursos necesita tu evento ?', options= total_resources)
            
            if st.button('Save'):
                validation = interface_back.Try_event(event_type, start_date, end_date, selected_resources, depe)
                
                onj = None

                if validation[-1]:
                    if event_type == e1:
                        obj = events.Espectaculo_Humoristico(start_date, end_date, selected_resources)
                    elif event_type == e2:
                        obj = events.Evento_Cultural(start_date, end_date, selected_resources)
                    elif event_type == e3:
                        obj = events.Evento_Personalizado(start_date, end_date, selected_resources, depe, name)
                    
                    interface_back.Refresh_data_base(obj)
                    st.success('Evento agregado exitosamente')
                
                else:
                    st.error(f'''Ha ocurrido un error: 

                    
                    -Recursos minimos necesarios: {validation[0]}\n\r
                    -Coliciones entre recursos: {validation[1]}\n\r
                    -Validez de intervalo: {validation[3]}''')


        #Eliminar
        if st.session_state.Eliminar:
            id = st.number_input('Ingrese el ID del evento que desea eliminar')

            if st.button('Delete'):
                pass

        




#-----------------------------------------------------------------------------------------------------------------------------------------------------

def Visualizacion():
    st.header('Visualizacion')

    #Eventos que se visualizaran en el calendario
    events = interface_back.Refresh_visualization()

    calendar_options = {
        'initialView': 'dayGridMonth',  # Vista de cuadricula mensual
        'headerToolbar': {
        'left': 'prev,next', # Botones del mes_anterior/mes_siguiente
        'center': 'title',  # Titulo del mes/anio en el centro
        'right': 'today'    # Boton para ir a la fecha actual
        },
        'locale': 'es', #Idioma
        'height': '650px' #Altura
    }

    selected = cal(events= events, options= calendar_options)
    st.subheader('Eventos asignados')
    #Mostrar los eventos actuales 
    st.markdown('Color - Nombre - Fecha(anio-mes-dia)')
    for event in events:
        st.markdown(f'<div style="display:inline-block; width:20px; height:20px; background-color:{event["color"]}; border:1px solid black; margin-right:10px;"></div> {event["title"]}: {event["start"]}', unsafe_allow_html=True)

#-----------------------------------------------------------------------------------------------------------------------------------------------------

def Info():
    st.header('Info de la Web')
    st.markdown("""
    En esta seccion podras obtener informacion del funcionamiento de la web (Un mini tutorial)
    """)
######################################################################################################################################################

main()
