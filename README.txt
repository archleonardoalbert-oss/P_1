LuxAlbert Hotel Event Planner
DESCRIPCION
LuxAlbert Hotel Event Planner es una aplicación web desarrollada en Python para la gestión inteligente de eventos en un hotel. Permite planificar actividades como espectáculos humorísticos, reuniones de negocios o remodelaciones, asegurando que no haya conflictos en la asignación de recursos limitados (por ejemplo, mesas, personal o vehículos). El sistema valida automáticamente restricciones como dependencias entre recursos, colisiones mutuas y disponibilidad en intervalos de tiempo, cumpliendo con los requisitos de un planificador de eventos real.
El proyecto modela un dominio hotelero, donde los eventos consumen recursos finitos y deben respetar reglas personalizadas para inclusión (co-requisitos) y exclusión mutua. Utiliza Streamlit para la interfaz gráfica, persistencia en JSON para datos y lógica backend para validaciones y búsqueda de horarios disponibles.



USO
Ejecuta la aplicación con Streamlit:
        streamlit run interface_front.py
Abre tu navegador en http://localhost:8501 (o la URL indicada).
Funcionalidades Principales

Inicio: Página de bienvenida con multimedia para contextualizar el hotel.
Administrar Eventos: Crea o elimina eventos, seleccionando tipo, fechas y recursos. Valida automáticamente conflictos y sugiere fechas alternativas si es necesario.
Administrar Recursos: Agrega, modifica o elimina recursos, colisiones y dependencias. Incluye visualizaciones como gráficos de pastel para distribución de recursos.
Ver Eventos: Calendario interactivo con eventos coloreados, detalles y selección para inspección.
Info: Información sobre la aplicación.

Ejemplo de uso:

Ve a "Administrar Eventos" > "Crear".
Selecciona un tipo (e.g., "Espectáculo Humorístico"), ingresa fechas (d/m/a) y recursos.
El sistema valida y guarda si es viable; de lo contrario, muestra errores detallados.


ESTRUCTURA

interface_front.py: Interfaz gráfica con Streamlit (frontend).
interface_back.py: Lógica backend para validaciones, persistencia y procesamiento.
events.py: Clases para modelar eventos con herencia OOP.
dependencias.py: Configuración de dependencias para eventos predefinidos.
Database.json: Archivo de persistencia para datos.
Media/: Carpeta con imágenes y videos para la UI.
Proyecto 1.md: Especificación original del proyecto.



DEPENDENCIAS

Python 3.8+
Streamlit: Para la interfaz web.
Pandas y Plotly: Para dataframes y visualizaciones.
ULID: Para generación de IDs únicos.
Datetime: Para manejo de fechas (incluido en Python estándar).

Ver requirements.txt para versiones exactas (crea uno con pip freeze > requirements.txt si no existe).



RESTRICCIONES IMPLEMENTADAS
Siguiendo el diseño del proyecto:

Co-requisitos (Inclusión): Recursos que deben usarse juntos (e.g., "mesas" requiere "sillas"). Definidos en depen_resources de Database.json.
Exclusión Mutua: Recursos incompatibles (e.g., "prostitutas" no puede con "ingenieros"). Definidos en collitions.
Disponibilidad Global: Chequea conflictos en fechas y cantidades limitadas de recursos.

Ejemplos:

Un "Espectáculo Humorístico" requiere al menos mesas, sillas, organizador y enanos.
No se permite combinar "Enanos" con "ciberneticos" en un evento.

Estas reglas se validan en la clase Validation para prevenir asignaciones inválidas.
