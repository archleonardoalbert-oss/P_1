import streamlit as st
from GUI import home
from GUI import info
from GUI import manage_events
from GUI import manage_resources
from GUI import visualization

st.set_page_config(layout= "wide")
def main():
    st.title("LuxAlbert Hotel")
    st.image('Media/360_F_381799100_YOZ0uoR7Wz3YIGZHRYhEjlqTkGn8EMMd.jpg', width= 180)

    if 'Critic' not in st.session_state:
        st.session_state.Critic = False

    if 'modified_events' not in st.session_state:
        st.session_state.modified_events = []
        
    #Menu lateral
    seccion = st.sidebar.selectbox(
        '',
        ['Inicio', 'Administrar eventos','Administrar recursos', 'Ver eventos', 'Info'],
        disabled= st.session_state.Critic
    )

    message1 = '''Los cambios de seccion mientras se reestructura la base de datos podrian causar problemas incomodos, por favor espere'''


    if seccion == 'Inicio':
        home.Inicio()
    elif seccion == 'Administrar eventos':
        manage_events.Administrar()
    elif seccion == 'Administrar recursos':
        manage_resources.Administrar_recursos()
    elif seccion == 'Ver eventos':
        visualization.Visualizacion()
    elif seccion == 'Info':
        info.Info()
    
main()
