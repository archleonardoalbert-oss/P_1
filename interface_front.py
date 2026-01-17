import streamlit as st
from streamlit_calendar import calendar as cal
import interface_back
from interface_back import events
import json
import datetime
import pandas as pd
import plotly.express as px
from pathlib import Path


total_resources = interface_back.resources.keys()
st.set_page_config(layout= "wide")
def main():
    st.title("Albert Hotel")
    st.image('Media/360_F_381799100_YOZ0uoR7Wz3YIGZHRYhEjlqTkGn8EMMd.jpg', width= 180)

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
    st.video(
        'Media/Luxury.mp4',
        autoplay= True,
        loop= True,
        
        ) 
    albun = [f'Media/{entry.name}' for entry in Path('Media').iterdir() if entry.is_file() and entry.name != '360_F_381799100_YOZ0uoR7Wz3YIGZHRYhEjlqTkGn8EMMd.jpg' and entry.name != 'Luxury.mp4']

    with st.container():
        st.markdown('<div class = "horizontal-gallery">', unsafe_allow_html= True)
        col1, col2, col3 = st.columns([1, 1, 1])
        max_col = len(albun) // 3
        for i in range(len(albun)):
            image = albun[i]
            if i <= max_col:
                with col1:
                    st.image(image, width= 400)
            elif max_col < i <= 2 * max_col:
                with col2:
                    st.image(image, width= 400)
            else:
                with col3:
                    st.image(image, width= 400)


        st.markdown('</div>', unsafe_allow_html= True)

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
            ESPACIO_NO_QUEBRANTABLE = '\u00A0'
            ids = {}
            _events = interface_back.Load_date_base('events')

            for e in _events:
                ids.update({ e['id'] : f'{e['id']}{ESPACIO_NO_QUEBRANTABLE * 8}------>{ESPACIO_NO_QUEBRANTABLE * 8}{e['name']} ({e['start_date']} - {e['end_date']})'})

            id = st.multiselect(
                'Seleccione el ID del elemento que desea eliminar',
                 options = ids.keys(),
                 format_func= lambda k: ids[k]
                 )


            if st.button('OK'):
                interface_back.Delete_event(id)

        




#-----------------------------------------------------------------------------------------------------------------------------------------------------
def Administrar_recursos():
    col_left, col_mid, col_right = st.columns([1, 4, 6], border= True)

    #Inicializando st.session_state 
    if 'Crear' not in st.session_state:
        st.session_state.Crear = False

    if 'Modificar' not in st.session_state:
        st.session_state.Modificar = False
    
    if 'Eliminar' not in st.session_state:
        st.session_state.Eliminar = False

    with col_left:
        if st.button('Crear'):
            st.session_state.Crear = not st.session_state.Crear
            if st.session_state.Crear:
                st.session_state.Eliminar = False
                st.session_state.Modificar = False

        if st.button('Modificar'):
            st.session_state.Modificar = not st.session_state.Modificar
            if st.session_state.Modificar:
                st.session_state.Crear = False
                st.session_state.Eliminar = False
        
        if st.button('Eliminar'):
            st.session_state.Eliminar = not st.session_state.Eliminar
            if st.session_state.Eliminar:
                st.session_state.Crear = False
                st.session_state.Modificar = False

        
    with col_mid:
        resources = interface_back.Load_date_base('resources').keys()
        if st.session_state.Crear:
            result = True
            action = 'a'
            key1 = st.text_input('Nombre del recurso')
            stack1 = st.number_input('Cantidad', min_value= 1, step= 1, key = 'n1')
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
                    interface_back.Refresh_data_base_logic(action, 'resources', key1, stack)
                    interface_back.Refresh_data_base_logic(action, 'collitions', key1, collitions)
                    interface_back.Refresh_data_base_logic(action, 'depen_resources', key1, depen)
                    st.success(f'Evento {key1} agregado correctamente')


        if st.session_state.Modificar:
            resources = list(interface_back.Load_date_base('resources').keys())

            action = 'm'
            key2 = st.selectbox('Nombre del recurso', resources)
            resources.remove(key2)

            old_collitions = interface_back.Load_date_base('collitions')[key2]
            old_depen  = interface_back.Load_date_base('depen_resources')[key2]

            for c in old_collitions:
                resources.remove(c)
            
            for d in old_depen:
                resources.remove(d)
            
            stack2 = st.number_input('Cantidad', min_value= 1, step= 1, key= 'n2')
            
            collitions_new = st.multiselect('Agregar coliciones nuevas', resources, key= 'm1')
            depen_new = st.multiselect('Agregar dependencias nuevas', resources, key= 'm2')

            collitions_del = st.multiselect('Eliminar coliciones', old_collitions, key= 'm3')
            depen_del = st.multiselect('Eliminar dependencias', old_depen, key= 'm4')

            if st.button('save'):
                result = True

                collitions_real = old_collitions
                depen_real = old_depen

                #Recreando el resultado final de la las coliciones
                for c in collitions_new:
                    collitions_real.append(c)
                
                for c in collitions_del:
                    collitions_real.remove(c)

                #Recreando el resultado final de las dependencias
                for d in depen_new:
                    depen_real.append(d)

                for d in depen_del:
                    depen_real.remove(d)

                for d in depen_real:
                    if d in collitions_real:
                        st.error('Hay una interseccion entre las dependencias y las coliciones de tu recurso')
                        result = False
                        break

                if result:
                    r = interface_back.Refresh_data_base_logic(action, 'resources', key2, stack2)
                    c = interface_back.Refresh_data_base_logic(action, 'collitions', key2, a = collitions_new, d = collitions_del)
                    d = interface_back.Refresh_data_base_logic(action, 'depen_resources', key2, a = depen_new, d = depen_del)

                    if not r:
                        st.error('No se pudo modificar el volumen del recurso')
                    if not c:
                        st.error('No se pudieron modificar las coliciones del recurso')
                    if not d:
                        st.error('No se pudieron modificar las dependencias del recurso')
                    if r and c and d:
                        st.success(f'Recurso "{key2}" modificado correctamente')






        if st.session_state.Eliminar:
            result = True
            action = 'd'
            key3 = st.selectbox('Nombre del recurso', interface_back.Load_date_base('resources').keys(), key= 's3')

            if st.button('OK'):
                result = True
                for l in interface_back.dependencias_eventos_definidos:
                    for r in l:
                        if key3 == r:
                            result = False
                            st.error('No puedes eliminar un recurso de un evento inmutable')
                
                if result:
                    r = interface_back.Refresh_data_base_logic(action, 'resources', key3)
                    c = interface_back.Refresh_data_base_logic(action, 'collitions', key3)
                    d = interface_back.Refresh_data_base_logic(action, 'depen_resources', key3)

                    if not r:
                        st.error('No se pudo eliminar el volumen del recurso')
                    if not c:
                        st.error('No se pudieron eliminar las coliciones del recurso')
                    if not d:
                        st.error('No se pudieron eliminar las dependencias del recurso')
                    if r and c and d:
                        st.success(f'Se ha eliminado el recurso {key3} correctamente')
                    
        

    
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


#-----------------------------------------------------------------------------------------------------------------------------------------------------

def Info():
    st.header('Info de la Web')
    st.markdown("""
    En esta seccion podras obtener informacion del funcionamiento de la web (Un mini tutorial)
    """)
######################################################################################################################################################

main()
