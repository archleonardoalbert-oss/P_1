import streamlit as st
from GUI import home
from GUI import info
from GUI import manage_events
from GUI import manage_resources
from GUI import visualization

st.set_page_config(layout= "wide")

def main():

    col = st.columns([10, 1])
    st.title("LuxAlbert Hotel")
    with col[0]:
        st.image('Media/360_F_381799100_YOZ0uoR7Wz3YIGZHRYhEjlqTkGn8EMMd.jpg', width= 180)

    if 'Critic' not in st.session_state:
        st.session_state.Critic = False

    if 'modified_events' not in st.session_state:
        st.session_state.modified_events = []

    if 'Max_events' not in st.session_state:
        st.session_state.Max_events = 150
    
    with col[1]:
        st.session_state.Max_events = st.number_input(min_value= 10, value= st.session_state.Max_events, step= 10, label= 'Cantidad maxima de eventos')


    #Menu lateral
    seccion = st.sidebar.selectbox(
        '',
        ['Inicio', 'Administrar eventos','Administrar recursos', 'Ver eventos', 'Info'],
        disabled= st.session_state.Critic
    )

    message1 = '''Los cambios de seccion mientras se reestructura la base de datos podrian causar problemas incomodos, por favor espere'''


    if seccion == 'Inicio':
        try:
            home.Inicio()
        except Exception as e:
            st.rerun()
            home.Inicio()
            st.toast(f'Ha ocurrido un error:\n\r {e}')
    elif seccion == 'Administrar eventos':
        try:
            manage_events.Administrar()
        except Exception as e:
            st.rerun()
            manage_events.Administrar()
            st.toast(f'Ha ocurrido un error:\n\r {e}')
    elif seccion == 'Administrar recursos':
        try:
            manage_resources.Administrar_recursos()
        except Exception as e:
            st.rerun()
            manage_resources.Administrar_recursos()
            st.toast(f'Ha ocurrido un error:\n\r {e}')
    elif seccion == 'Ver eventos':
        try:
            visualization.Visualizacion()
        except Exception as e:
            st.rerun()
            visualization.Visualizacion()
            st.toast(f'Ha ocurrido un error:\n\r {e}')
    elif seccion == 'Info':
        try:
            info.Info()
        except Exception as e:
            st.rerun()
            info.Info()
            st.toast(f'Ha ocurrido un error:\n\r {e}')
    
main()
