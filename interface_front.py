import streamlit as st
from streamlit_calendar import calendar as cal
import interface_back
from interface_back import events
import pandas as pd
import plotly.express as px
from pathlib import Path


total_resources = interface_back.Load_date_base('resources')
st.set_page_config(layout= "wide")
def main():
    st.title("LuxAlbert Hotel")
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
    st.session_state.Save = False
    st.header('Bienvenido a LuxAlbert Hotel')
    st.markdown("""
    El objetivo de esta pagina es que tengas el poder de administrar los eventos de LuxAlbert Hotel
    """)
    st.video(
        'Media/Luxury.mp4',
        autoplay= True,
        loop= True,
        muted= True,
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
            st.session_state['typ'] = st.selectbox('Que tipo de evento quiere crear ?',
                                        [e1, e2, e3, e4, e5, e6, e7, e8])
            event_type = st.session_state['typ']
            start_date = st.text_input('Ingrese la fecha de inicio del evento')
            end_date = st.text_input('Ingrese la fecha de finalizacion del evento')
            selected_resources = st.multiselect('Que recursos requerira para su evento ?', options= total_resources)

            if event_type == e8:
                name = st.text_input('Nombre del evento')
                depe = st.multiselect('Que recursos necesita tu evento ?', options= total_resources)
            
            if 'Save' not in st.session_state:
                st.session_state.Save = False

            if st.button('Save'):
                st.session_state.Save = not st.session_state.Save
            
            if st.session_state.Save:
                st.session_state.Save = not st.session_state.Save
                validation = interface_back.Try_event(event_type, start_date, end_date, selected_resources, depe)
                
                onj = None

                if validation[-1]:
                    if event_type == e1:
                        obj = events.Espectaculo_Humoristico(start_date, end_date, selected_resources)
                    elif event_type == e2:
                        obj = events.Evento_Cultural(start_date, end_date, selected_resources)
                    elif event_type == e3:
                        obj = events.Reunion_De_Negocios(start_date, end_date, selected_resources)
                    elif event_type == e4:
                        obj = events.Remodelacion(start_date, end_date, selected_resources)
                    elif event_type == e5:
                        obj = events.Excurcion(start_date, end_date, selected_resources)
                    elif event_type == e6:
                        obj = events.Torneo_Gamer(start_date, end_date, selected_resources)
                    elif event_type == e7:
                        obj = events.Temporada_De_Ofertas(start_date, end_date, selected_resources)
                    elif event_type == e8:
                        obj = events.Evento_Personalizado(start_date, end_date, selected_resources, depe, name)
                    
                    interface_back.Refresh_data_base_event(obj)
                    st.success('Evento agregado exitosamente')
                
                elif validation[4] and validation[0][0] and validation[1][0] and validation[2][0] and not validation[3][0]:
                    suggested_date = interface_back.Find_Date(event_type, start_date, end_date, selected_resources, depe)


                    if not suggested_date == False:
                        st.warning(f"""Para la fecha que requiere su evento no tenemos dsponibles los recursos ({validation[3][1]}).\r\n
    Le sugerimos que planifique el evento en la siguiente fecha disponible ({suggested_date})""")

                    #TENGO QUE VERIFICAR POR QUE CUANDO PRESIONO ESTE BOTNO NO HACE ABSOLUTAMENTE NADA

                    if st.button('Ok'):
                        if event_type == e1:
                            obj = events.Espectaculo_Humoristico(suggested_date[0], suggested_date[1], selected_resources)
                        elif event_type == e2:
                            obj = events.Evento_Cultural(suggested_date[0], suggested_date[1], selected_resources)
                        elif event_type == e3:
                            obj = events.Reunion_De_Negocios(suggested_date[0], suggested_date[1], selected_resources)
                        elif event_type == e4:
                            obj = events.Remodelacion(suggested_date[0], suggested_date[1], selected_resources)
                        elif event_type == e5:
                            obj = events.Excurcion(suggested_date[0], suggested_date[1], selected_resources)
                        elif event_type == e6:
                            obj = events.Torneo_Gamer(suggested_date[0], suggested_date[1], selected_resources)
                        elif event_type == e7:
                            obj = events.Temporada_De_Ofertas(suggested_date[0], suggested_date[1], selected_resources)
                        elif event_type == e8:
                            obj = events.Evento_Personalizado(suggested_date[0], suggested_date[1], selected_resources, depe, name)

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


#-----------------------------------------------------------------------------------------------------------------------------------------------------
def Administrar_recursos():
    st.session_state.Save = False
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


            if st.button('save', key= 'save1'):
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
                
                if key1 in resources:
                    st.error('No puedes crear un recurso ya existente')
                    result = False

                elif result:
                    interface_back.Refresh_data_base_logic(action, 'resources', key1, stack1)
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

            if st.button('save', key= 'save2'):
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
                b = False #Variable para unicamente que no te salga el cartel de error mas de una vez
                for l in interface_back.dependencias_eventos_definidos:
                    if b: break
                    for r in l:
                        if key3 == r:
                            result = False
                            st.error('No puedes eliminar un recurso de un evento inmutable')
                            b = True
                            
                
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
    st.session_state.Save = False
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
    st.session_state.Save = False
    
    # Encabezado principal del tutorial
    st.markdown(""".
    # 📖 Tutorial de LuxAlbert Hotel
    ### Tu guía completa para administrar eventos de hotel
    ---
    """)
    
    # Menú de navegación del tutorial
    tutorial_section = st.selectbox(
        '🎯 ¿Qué quieres aprender?',
        ['🏠 Introducción', '📅 Crear Eventos', '🗑️ Eliminar Eventos', '🔧 Administrar Recursos', '📆 Ver Calendario de Eventos', '💡 Conceptos Clave', '⚠️ Errores Comunes']
    )
    
    if tutorial_section == '🏠 Introducción':
        st.info("""
        ### 🏠 Bienvenido a LuxAlbert Hotel
        
        Esta aplicación te permite **administrar completamente** los eventos de LuxAlbert Hotel. 
        Desde la creación de eventos hasta la gestión de recursos, todo está diseñado para ser intuitivo y eficiente.
        """)
        
        # Panel de navegación
        with st.expander('📋 Panel de Navegación (Sidebar)', expanded=True):
            col1, col2 = st.columns([1, 4])
            with col1:
                st.markdown("""
                ### 📍
                **Sidebar**
                """)
            with col2:
                st.markdown("""
                El **menú lateral** (sidebar) es tu herramienta principal de navegación:
                
                - 📌 **Inicio**: Página de bienvenida
                - 📅 **Administrar eventos**: Crear y eliminar eventos
                - 🔧 **Administrar recursos**: Gestionar recursos del hotel
                - 📆 **Ver eventos**: Visualizar calendario y detalles
                - ℹ️ **Info**: Este tutorial
                """)
        
        st.markdown("--- ")
        
        # Flujo de trabajo
        with st.expander('🔄 Flujo de Trabajo General', expanded=True):
            col1, col2, col3, col4 = st.columns(4)
            
            steps = [
                ('1️⃣', 'Planificar', 'Define tipo de evento y recursos'),
                ('2️⃣', 'Crear', 'Ingresa fechas y selecciona recursos'),
                ('3️⃣', 'Validar', 'Sistema verifica disponibilidad'),
                ('4️⃣', 'Confirmar', 'Evento agregado exitosamente')
            ]
            
            for idx, (emoji, title, desc) in enumerate(steps):
                if idx == 0:
                    with col1:
                        st.markdown(f"""
                        <div style="text-align: center; padding: 15px; background: linear-gradient(145deg, #f8f9fa 0%, #e9ecef 100%); 
                                    border-radius: 12px; border-left: 4px solid #667eea;">
                            <div style="font-size: 2em;">{emoji}</div>
                            <h4 style="margin: 5px 0; color: #667eea;">{title}</h4>
                            <p style="font-size: 0.85em; color: #666;">{desc}</p>
                        </div>
                        """, unsafe_allow_html=True)
                elif idx == 1:
                    with col2:
                        st.markdown(f"""
                        <div style="text-align: center; padding: 15px; background: linear-gradient(145deg, #f8f9fa 0%, #e9ecef 100%); 
                                    border-radius: 12px; border-left: 4px solid #667eea;">
                            <div style="font-size: 2em;">{emoji}</div>
                            <h4 style="margin: 5px 0; color: #667eea;">{title}</h4>
                            <p style="font-size: 0.85em; color: #666;">{desc}</p>
                        </div>
                        """, unsafe_allow_html=True)
                elif idx == 2:
                    with col3:
                        st.markdown(f"""
                        <div style="text-align: center; padding: 15px; background: linear-gradient(145deg, #f8f9fa 0%, #e9ecef 100%); 
                                    border-radius: 12px; border-left: 4px solid #667eea;">
                            <div style="font-size: 2em;">{emoji}</div>
                            <h4 style="margin: 5px 0; color: #667eea;">{title}</h4>
                            <p style="font-size: 0.85em; color: #666;">{desc}</p>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    with col4:
                        st.markdown(f"""
                        <div style="text-align: center; padding: 15px; background: linear-gradient(145deg, #f8f9fa 0%, #e9ecef 100%); 
                                    border-radius: 12px; border-left: 4px solid #667eea;">
                            <div style="font-size: 2em;">{emoji}</div>
                            <h4 style="margin: 5px 0; color: #667eea;">{title}</h4>
                            <p style="font-size: 0.85em; color: #666;">{desc}</p>
                        </div>
                        """, unsafe_allow_html=True)
    
    elif tutorial_section == '📅 Crear Eventos':
        st.info("""
        ### 📅 Cómo Crear un Evento
        Aprende a crear eventos de manera sencilla y efectiva.
        """)
        
        # Tipos de eventos
        with st.expander('🎭 Tipos de Eventos Disponibles', expanded=True):
            event_types = [
                ('Espectaculo Humoristico', '🎭', 'Entretenimiento cómico para huéspedes', ['mesas', 'sillas', 'organizador', 'Enanos']),
                ('Evento Cultural', '🎨', 'Actividades artísticas y culturales', ['mesas', 'sillas', 'organizador', 'comida']),
                ('Reunion de negocios', '💼', 'Encuentros empresariales', ['USD', 'mesas', 'organizador', 'comida', 'Bus']),
                ('Remodelacion', '🔨', 'Trabajos de mejora en instalaciones', ['Obrero', 'Arquitecto', 'Material de construccion', 'Camion', 'USD', 'guardias']),
                ('Excurcion', '🚌', 'Salidas turísticas para huéspedes', ['Bus', 'guardias', 'comida']),
                ('Torneo gamer', '🎮', 'Competencias de videojuegos', ['organizador', 'Articulos gamers', 'mesas', 'sillas', 'comida']),
                ('Temporada de ofertas', '💰', 'Promociones especiales del hotel', ['USD', 'Economista', 'organizador']),
                ('Personalizado', '✨', 'Crear tu propio tipo de evento', ['Personalizable'])
            ]
            
            type_cols = st.columns(2)
            for idx, (name, emoji, desc, deps) in enumerate(event_types):
                with type_cols[idx % 2]:
                    st.markdown(f"""
                    <div style="background: white; padding: 15px; border-radius: 10px; margin: 8px 0; 
                                border: 1px solid #e0e0e0; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
                        <h4 style="margin: 0 0 8px 0; color: #333;">{emoji} {name}</h4>
                        <p style="margin: 0; color: #666; font-size: 0.9em;">{desc}</p>
                        <p style="margin: 8px 0 0 0; color: #667eea; font-size: 0.85em;"><strong>Recursos base:</strong> {', '.join(deps[:3])}{'...' if len(deps) > 3 else ''}</p>
                    </div>
                    """, unsafe_allow_html=True)
        
        st.markdown("--- ")
        
        # Pasos detallados
        with st.expander('📝 Paso a Paso: Crear tu Evento', expanded=True):
            st.markdown("""
            ### 📌 Paso 1: Seleccionar la Opción
            En el menú lateral, selecciona **"Administrar eventos"**. Luego, haz clic en el botón **"Crear"** en la columna izquierda.
            
            ### 📌 Paso 2: Elegir el Tipo de Evento
            Usa el menú desplegable para seleccionar el tipo de evento que deseas crear. Cada tipo tiene recursos predefinidos.
            
            ### 📌 Paso 3: Definir las Fechas
            Ingresa la fecha de inicio y finalización del evento en formato **dd/mm/AAAA** (ejemplo: 25/12/2025).
            
            ### 📌 Paso 4: Seleccionar Recursos
            Elige los recursos adicionales que necesitarás para tu evento. El sistema validará automáticamente:
            - Recursos mínimos requeridos
            - Coliciones entre recursos
            - Dependencias de recursos
            - Disponibilidad en las fechas
            
            ### 📌 Paso 5: Guardar
            Haz clic en **"Save"**. El sistema validará tu evento y te informará el resultado.
            """)
            
            st.success("✅ **Resultado Exitoso:** Tu evento será agregado y podrás verlo en la sección 'Ver eventos'")
            st.warning("⚠️ **Fecha No Disponible:** Si los recursos no están disponibles en tu fecha preferida, el sistema te sugerirá una fecha alternativa automáticamente.")
    
    elif tutorial_section == '🗑️ Eliminar Eventos':
        st.info("""
        ### 🗑️ Cómo Eliminar un Evento
        Aprende a eliminar eventos de manera segura.
        """)
        
        with st.expander('🗑️ Pasos para Eliminar', expanded=True):
            st.markdown("""
            ### 📌 Paso 1: Acceder a Administración
            Ve a **"Administrar eventos"** en el menú lateral.
            
            ### 📌 Paso 2: Seleccionar Eliminar
            Haz clic en el botón **"Eliminar"** en la columna izquierda.
            
            ### 📌 Paso 3: Elegir el Evento
            Selecciona el/los evento(s) que deseas eliminar usando el menú desplegable. 
            Cada opción muestra: **ID - Nombre (Fecha inicio - Fecha fin)**
            
            ### 📌 Paso 4: Confirmar
            Haz clic en **"OK"** para eliminar permanentemente el evento.
            """)
            
            st.warning("⚠️ **Importante:** La eliminación es permanente y no se puede deshacer.")
    
    elif tutorial_section == '🔧 Administrar Recursos':
        st.info("""
        ### 🔧 Administración de Recursos
        Los recursos son los elementos disponibles en el hotel para tus eventos (mesas, sillas, comida, etc.)
        """)
        
        # Acciones
        with st.expander('⚙️ Acciones Disponibles', expanded=True):
            action_cols = st.columns(3)
            
            with action_cols[0]:
                st.success("""
                ### ➕ Crear
                Agregar nuevos recursos al hotel
                """)
                
            with action_cols[1]:
                st.info("""
                ### ✏️ Modificar
                Cambiar cantidad y propiedades
                """)
                
            with action_cols[2]:
                st.warning("""
                ### 🗑️ Eliminar
                Quitar recursos del sistema
                """)
        
        st.markdown("--- ")
        
        with st.expander('📋 Visualización de Recursos', expanded=True):
            st.markdown("""
            La sección de recursos incluye tres tablas importantes:
            
            - 📦 **Recursos**: Muestra la cantidad disponible de cada recurso
            - ⚡ **Coliciones**: Indica qué recursos NO pueden estar juntos
            - 🔗 **Dependencias**: Muestra qué recursos necesitan otros para funcionar
            
            Además, un gráfico circular muestra la distribución de recursos del hotel.
            """)
    
    elif tutorial_section == '📆 Ver Calendario de Eventos':
        st.info("""
        ### 📆 Visualización del Calendario
        Aprende a navegar y utilizar el calendario de eventos.
        """)
        
        with st.expander('📅 El Calendario', expanded=True):
            st.markdown("""
            ### 📌 Navegación
            - **◀️ ▶️**: Mes anterior / Mes siguiente
            - **Hoy**: Ir a la fecha actual
            - **Scroll**: Zoom in/out
            
            ### 📌 Colores
            Cada evento tiene un color único para facilitar su identificación.
            """)
        
        with st.expander('📋 Tabla de Detalles', expanded=True):
            st.markdown("""
            ### 📌 Ver Detalles
            Selecciona cualquier celda de la tabla de eventos para ver información detallada:
            
            - Nombre del evento
            - Fecha de inicio y fin
            - Recursos utilizados
            - Dependencias del evento
            """)
    
    elif tutorial_section == '💡 Conceptos Clave':
        st.info("""
        ### 💡 Conceptos Fundamentales
        Comprende los pilares de la administración de eventos en LuxAlbert Hotel
        """)
        
        # Concepto 1: Recursos
        with st.expander('📦 Recursos', expanded=True):
            st.markdown("""
            ### 📦 ¿Qué son?
            Los recursos son todos los elementos físicos y servicios disponibles en el hotel para la realización de eventos.
            
            **Ejemplos:**
            - 🪑 Mesas
            - 💺 Sillas
            - 🍽️ Comida
            - 🚌 Bus
            - 💰 USD
            - 👷 Guardias
            """)
        
        # Concepto 2: Coliciones
        with st.expander('⚡ Coliciones', expanded=True):
            st.markdown("""
            ### ⚡ ¿Qué son?
            Las coliciones son recursos que **NO pueden estar juntos** en un mismo evento.
            
            **Ejemplos:**
            - El **organizador** no puede estar con **ingenieros** ni **prostitutas**
            - Las **prostitutas** no pueden estar con **ingenieros**, **ciberneticos** ni **mesas**
            - Los **ciberneticos** no pueden estar con **ingenieros**
            """)
            st.warning("⚠️ **Importante:** Si seleccionas recursos en colición, el sistema rechazará la creación del evento.")
        
        # Concepto 3: Dependencias
        with st.expander('🔗 Dependencias', expanded=True):
            st.markdown("""
            ### 🔗 ¿Qué son?
            Las dependencias son recursos que **necesitan otros recursos** para poder funcionar correctamente.
            
            **Ejemplos:**
            - Las **mesas** necesitan **sillas**
            - El **organizador** necesita **USD**
            - Los **guardias** necesitan **USD**
            - Los **ingenieros** necesitan **USD** y **mesas**
            - El **Bus** necesita **USD**, **organizador** y **Chofer**
            """)
            st.success("✅ **Solución:** Si falta una dependencia, el sistema te indicará exactamente qué recurso necesitas agregar.")
        
        # Concepto 4: Disponibilidad
        with st.expander('📅 Disponibilidad', expanded=True):
            st.markdown("""
            ### 📅 ¿Qué significa?
            La disponibilidad verifica que los recursos que necesitas estén **libres** en las fechas de tu evento.
            
            **¿Cómo funciona?**
            1. El sistema revisa todos los eventos programados
            2. Identifica eventos con fechas que se solapan con las tuyas
            3. Resta los recursos utilizados por esos eventos
            4. Verifica si quedan suficientes recursos para tu evento
            """)
            st.info("💡 **Recomendación Inteligente:** Si solo falla la disponibilidad, el sistema te sugerirá automáticamente la próxima fecha disponible cercana a tu fecha preferida.")
    
    elif tutorial_section == '⚠️ Errores Comunes':
        st.info("""
        ### ⚠️ Errores Comunes y Soluciones
        Aprende a identificar y resolver los problemas más frecuentes
        """)
        
        # Error 1
        with st.expander('❌ Error en Formato de Fecha', expanded=True):
            st.error("🚫 **Problema:** El sistema rechaza las fechas ingresadas")
            st.markdown("""
            **Solución:**
            Asegúrate de usar el formato correcto: **dd/mm/AAAA**
            
            - ✅ **Correcto:** 25/12/2025, 01/01/2026, 31/03/2026
            - ❌ **Incorrecto:** 2025-12-25, 12/25/2025, 25-12-2025
            """)
        
        # Error 2
        with st.expander('❌ Recursos en Colición', expanded=True):
            st.error("🚫 **Problema:** 'Hay una interseccion entre las dependencias y las coliciones de tu recurso'")
            st.markdown("""
            **Causa:**
            Seleccionaste dos recursos que no pueden estar juntos según las reglas del hotel.
            
            **Solución:**
            Revisa qué recursos tienen colición entre sí y elimina uno de ellos de tu selección.
            Consulta la sección **"Conceptos Clave > Coliciones"** para ver qué recursos son incompatibles.
            """)
        
        # Error 3
        with st.expander('❌ Dependencias No Satisfechas', expanded=True):
            st.error("🚫 **Problema:** Error por dependencias de recursos fallidas")
            st.markdown("""
            **Causa:**
            Falta un recurso que depende de otro para funcionar.
            
            **Solución:**
            Agrega los recursos que el sistema indica como faltantes. 
            Por ejemplo, si necesitas **mesas**, probablemente también necesites **sillas**.
            """)
        
        # Error 4
        with st.expander('❌ Recursos No Disponibles', expanded=True):
            st.error("🚫 **Problema:** 'No tenemos disponibles los recursos... Le sugerimos...'")
            st.markdown("""
            **Causa:**
            Los recursos que necesitas ya están reservados para otros eventos en las fechas solicitadas.
            
            **Soluciones:**
            1. **Aceptar la sugerencia:** El sistema propone automáticamente la próxima fecha disponible
            2. **Cambiar fecha:** Elige fechas donde haya disponibilidad
            3. **Reducir recursos:** Usa menos recursos o alternativos
            """)
        
        # Error 5
        with st.expander('❌ No se Puede Eliminar Recurso', expanded=True):
            st.error("🚫 **Problema:** 'No puedes eliminar un recurso de un evento inmutable'")
            st.markdown("""
            **Causa:**
            Estás intentando eliminar un recurso que está protegido porque es necesario para eventos predefinidos del sistema.
            
            **Solución:**
            No puedes eliminar estos recursos. Consulta la sección **"Administrar recursos"** para ver qué recursos están protegidos.
            """)
        
        # Error 6
        with st.expander('❌ Rango de Fechas Inválido', expanded=True):
            st.error("🚫 **Problema:** 'Validez de intervalo de fecha: False'")
            st.markdown("""
            **Causa:**
            La fecha de finalización es anterior a la fecha de inicio.
            
            **Solución:**
            Asegúrate de que **fecha_fin ≥ fecha_inicio**
            """)
    
    # Footer del tutorial
    st.markdown("""
    <div style="text-align: center; padding: 30px; margin-top: 30px; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                border-radius: 15px; color: white; box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
        <h3 style="margin: 0 0 10px 0;">🎉 ¡Listo para usar LuxAlbert Hotel!</h3>
        <p style="margin: 0; font-size: 1.1em;">Ahora tienes todo el conocimiento para administrar eventos como un profesional.</p>
        <p style="margin: 15px 0 0 0; font-size: 0.9em; opacity: 0.8;">
            Si tienes dudas, revisa las secciones de este tutorial o contacta al equipo de soporte.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
######################################################################################################################################################
    
######################################################################################################################################################

main()
