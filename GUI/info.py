import streamlit as st



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
    