import streamlit as st
import interface_back
import pandas as pd
import plotly.express as px
from pathlib import Path
import sys

# Subir al directorio P_1
ruta_base = Path(__file__).parent.parent  # Esto te lleva a P_1
sys.path.insert(0, str(ruta_base))

def Administrar_recursos():
    st.session_state.Save = False
    col_left, col_mid, col_right = st.columns([1, 4, 5], border= True)

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
