import streamlit as st
from streamlit_calendar import calendar as cal
import interface_back



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

def Inicio():
    st.header('Bienvenido a Albert Hotel')
    st.markdown("""
    El objetivo de esta pagina es que tengas el poder de administrar los eventos de Albert Hotel
    """)

def Administrar():
    st.header('Administracion de Eventos')
    st.markdown("""
    En esta seccion podras crear eventos predefinidos, personalizados y eliminar los mismos
    """)

def Visualizacion():
    st.header('Visualizacion')
    st.markdown("""
    En esta seccion podras ver los eventos que hay en curso y algunos detalles de los mismos
    """)

    #Eventos que se visualizaran en el calendario
    events = [
        #{'title': 'Evento_n', 'start': fecha_de_inicio, 'end': fecha_de_fin}
        #interface_back.Load_date_base('events') -> retorna los eventos
    ]

    calendar_options = {
        'initialView': 'dayGridMonth',  # Vista de cuadricula mensual
        'headerToolbar': {
        'left': 'prev,next', # Botones del mes_anterior/mes_siguiente
        'center': 'title',  # Titulo del mes/anio en el centro
        'right': 'today'    # Boton para ir a la fecha actual
        },
        'locale': 'es' #Idioma
    }

    selected = cal(events= events, options= calendar_options)
    st.subheader('Eventos asignados')
    #Mostrar los eventos actuales 

def Info():
    st.header('Info de la Web')
    st.markdown("""
    En esta seccion podras obtener informacion del funcionamiento de la web (Un mini tutorial)
    """)


main()
