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

    #Menu lateral
    seccion = st.sidebar.selectbox(
        '',
        ['Inicio', 'Administrar eventos','Administrar recursos', 'Ver eventos', 'Info']
    )

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
