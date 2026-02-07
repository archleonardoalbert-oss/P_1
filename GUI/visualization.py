import streamlit as st
from streamlit_calendar import calendar as cal
import interface_back
import pandas as pd
from pathlib import Path
import sys

# Subir al directorio P_1
ruta_base = Path(__file__).parent.parent  # Esto te lleva a P_1
sys.path.insert(0, str(ruta_base))

def Visualizacion():
    st.session_state.Critic = False
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
        'height': '650px', #Altura
        "eventTextColor": "#000000"
    }

    selected = cal(events= events, options= calendar_options)

    st.subheader('Eventos en curso:')
    #Detalles de eventos:
    names = []
    colors = []
    dates = []
    id = []

    for e in events:
        names.append(e['title'])
        colors.append(e['color'])
        dates.append(f'{e['start']} / {e['end']}')
        id.append(e['id'])
    
    #columnas
    col_left, col_right = st.columns([1, 1], border= True)

    df = pd.DataFrame({
        'Nombre': names,
        'Color': colors,
        'Fecha': dates,
        'ID': id
    })

    def Color(value):
        if isinstance(value, str) and value.startswith("#"):
            return f'background-color: {value}; color: transparent'
        
        return

    df_plus = df.style.applymap(Color, subset=['Color'])

    with col_left: #Tabla
        data_frame = st.dataframe(
            df_plus,
            on_select = 'rerun', #Rerrunea la app al seleccionar
            selection_mode = 'single-cell', #Modo de seleccion en cuestion de cantidad de celdas
            use_container_width = True, #Ajusta el ancho del contenedor
            hide_index = False #Muestra indices si lo necesitas
            )
        
    
    with col_right:
        if data_frame and data_frame.selection.cells:
            row, column = data_frame.selection.cells[0]

            all_row = df.iloc[row]
            all_row = dict(all_row)
            for e in events:
                if e['id'] == all_row['ID']:
                    all_row.update({
                        'Recursos' : e['resources'],
                        'Dependencias' : e['depen']
                        }
                    )
                    break

            st.dataframe(all_row)

