import streamlit as st
from streamlit_calendar import calendar as cal
import interface_back
from interface_back import events
import json
import datetime
import pandas as pd
import plotly.express as px

total_resources = interface_back.resources.keys()
st.set_page_config(layout= "wide")
def main():
    st.title("Albert Hotel")

    #Menu lateral
    seccion = st.sidebar.selectbox(
        'Que quieres hacer ?',
        ['Inicio', 'Administrar eventos','Administrar recursos', 'Ver eventos', 'Info']
    )

    if seccion == 'Inicio':
        Inicio()
    elif seccion == 'Administrar eventos':
        Administrar()
    elif seccion == 'Administrar recursos':
        Administrar_recursos()
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
                    
                    interface_back.Refresh_data_base_event(obj)
                    st.success('Evento agregado exitosamente')
                
                else:
                    depen_resources = ''
                    #Preparando el str de las dependencias de recursos fallidas si es que las hay
                    for c in validation[2][1]:
                        for r in validation[2][2]:
                            depen_resources += f'                                     {c}  <-//-  {r} \n\r'

                    st.error(f'''Ha ocurrido un error: 
                    

                    
                    -Recursos minimos necesarios: {validation[0]}\n\r
                    -Coliciones entre recursos: {validation[1]}\n\r
                    -Las dependencias de los recursos fallidas: \n{depen_resources} \n\r
                    -Insuficiencia de recursos globales: {validation[3]} \n\r
                    -Validez de intervalo de fecha: {validation[4]}
                    ''')


        #Eliminar
        if st.session_state.Eliminar:
            id = st.number_input('Ingrese el ID del evento que desea eliminar')

            if st.button('Delete'):
                pass

        




#-----------------------------------------------------------------------------------------------------------------------------------------------------
def Administrar_recursos():
    col_left, col_mid, col_right = st.columns([1, 4, 6], border= True)

    #Inicializando st.session_state 
    if 'Crear' not in st.session_state:
        st.session_state.Crear = False
    
    if 'Eliminar' not in st.session_state:
        st.session_state.Eliminar = False

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
        resources = interface_back.Load_date_base('resources').keys()
        if st.session_state.Crear:
            result = True
            action = 'a'
            key = st.text_input('Nombre del recurso')
            stack = st.number_input('Cantidad', min_value= 1, step= 1)
            collitions = st.multiselect('Coliciones', resources)
            depen = st.multiselect('Dependencias', resources)


            if st.button('save'):
                result = True

                #Validacion de la creacion del recurso:
                for r in resources:
                    if r in collitions:
                        break
                else:
                    collitions = []

                for r in resources:
                    if r in depen:
                        break
                else:
                    depen = []

                for c in collitions:
                    if c in depen:
                        st.error('No puedes crear un recurso el cual tenga recursos en comun entre sus dependencias y coliciones')
                        result = False
                        break
                
                if key in resources:
                    st.error('No puedes crear un recurso ya existente')
                    result = False

                elif result:
                    interface_back.Refresh_data_base_logic(action, 'resources', key, stack)
                    interface_back.Refresh_data_base_logic(action, 'collitions', key, collitions)
                    interface_back.Refresh_data_base_logic(action, 'depen_resources', key, depen)


        if st.session_state.Eliminar:
            result = True
            action = 'd'
            key = st.selectbox('Nombre del recurso', interface_back.Load_date_base('resources').keys())

            if st.button('OK'):
                result = True
                for l in interface_back.dependencias_eventos_definidos:
                    for r in l:
                        if key == r:
                            result = False
                            st.error('No puedes eliminar un recurso de un evento inmutable')
                
                if result:
                    if not interface_back.Refresh_data_base_logic(action, 'resources', key):
                        st.error('No se pudo eliminar de los recursos')
                    if not interface_back.Refresh_data_base_logic(action, 'collitions', key):
                        st.error('No se pudo eliminar de las coliciones')
                    if not interface_back.Refresh_data_base_logic(action, 'depen_resources', key):
                        st.error('No se pudo eliminar de las dependencias')

    
    # GRAFICO 
    with col_right:
        r = interface_back.Load_date_base('resources')
        data = {
            'Categoria' : r.keys(),
            'Valor' : r.values()
        }

        df = pd.DataFrame(data)

        fig = px.pie(
            df,
            values= 'Valor',
            names= 'Categoria',
            title= 'Distribucion de recursos',
            hole= 0.3,
            color_discrete_sequence= px.colors.qualitative.Set3
        )

        fig.update_traces(
            textposition = 'inside',
            textinfo = 'percent+label'
        )

        fig.update_layout(
            showlegend = True,
            legend_title_text = 'Categorias'
        )

        st.plotly_chart(
            fig,
            use_container_width= True,
            config = {
                'displayModeBar' : True,
                "modeBatButtonsToRemove" : ['lasso2d', 'select2d'],
                'toImageButtonOptions': {
                    'format': 'png',
                    'filename': 'mi_grafico',
                    'width' : 100,
                    'height' : 100
                },
                'responsive': True
            }
        )
    

    #COLUMNAS DE TABLAS
    c1, c2, c3 = st.columns([1, 1, 1], border= True)

    with c1:
        st.subheader('Recursos')
        r = interface_back.Load_date_base('resources')
        df = pd.DataFrame.from_dict(r, orient= 'index', columns=['Valor'])
        df.index.name = 'Nombre'
        st.dataframe(
            df,
            use_container_width= True,
            hide_index= False,
            column_config= {
                'Nombre': st.column_config.TextColumn('Clave', width= 'medium'),
                'Cantidad' : st.column_config.TextColumn('Cantidad', width= 'large')
            }
        )
    
    with c2:
        st.subheader('Coliciones')
        c = interface_back.Load_date_base('collitions')
        c_str = {k: str(v) for k,v in c.items()}
        df = pd.DataFrame.from_dict(c_str, orient= 'index')
        df.index.name = 'Nombre'
        st.dataframe(
            df,
            use_container_width= True,
            hide_index= False,
            column_config= {
                'Nombre': st.column_config.TextColumn('Clave', width= 'medium'),
                'Coliciones' : st.column_config.TextColumn('Coliciones', width= 'large')
            }
        )

    with c3:
        st.subheader('Dependencias')
        d = interface_back.Load_date_base('depen_resources')
        d_str = {k: str(v) for k,v in d.items()}
        df = pd.DataFrame.from_dict(d_str, orient= 'index')
        df.index.name = 'Nombre'
        st.dataframe(
            df,
            use_container_width= True,
            hide_index= False,
            column_config= {
                'Nombre': st.column_config.TextColumn('Clave', width= 'medium'),
                'Dependencias' : st.column_config.TextColumn('Dependencias', width= 'large')
            }
        )



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

    st.subheader('Eventos en curso:')
    #Detalles de eventos:
    names = []
    colors = []
    dates = []
    id = []

    for e in events:
        #Corrigiendo el adelanto de fecha de la fecha de fin
        end = e['end'].split('-')
        end[-1] = str(int(end[-1]) - 1)
        end = '-'.join(end)

        names.append(e['title'])
        colors.append(e['color'])
        dates.append(f'{e['start']} / {end}')
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


#-----------------------------------------------------------------------------------------------------------------------------------------------------

def Info():
    st.header('Info de la Web')
    st.markdown("""
    En esta seccion podras obtener informacion del funcionamiento de la web (Un mini tutorial)
    """)
######################################################################################################################################################

main()
