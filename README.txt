LuxAlbert Hotel Event Planner

Spanish

DESCRIPCION
LuxAlbert Hotel Event Planner es una aplicación web desarrollada en Python para la gestión inteligente de eventos en un hotel. Permite planificar actividades como espectáculos humorísticos, reuniones de negocios o remodelaciones, asegurando que no haya conflictos en la asignación de recursos limitados (por ejemplo, mesas, personal o vehículos). El sistema valida automáticamente restricciones como dependencias entre recursos, colisiones mutuas y disponibilidad en intervalos de tiempo, cumpliendo con los requisitos de un planificador de eventos real.
El proyecto modela un dominio hotelero, donde los eventos consumen recursos finitos y deben respetar reglas personalizadas para inclusión (co-requisitos) y exclusión mutua. Utiliza Streamlit para la interfaz gráfica, persistencia en JSON para datos y lógica backend para validaciones y búsqueda de horarios disponibles.



USO
Ejecuta la aplicación con Streamlit:
        streamlit run interface_front.py
Abre tu navegador en http://localhost:8501 (o la URL indicada).

FUNCIONALIDADES PRINCIPALES

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


English

DESCRIPTION
LuxAlbert Hotel Event Planner is a web application developed in Python for intelligent event management in a hotel. It allows planning activities such as humorous shows, business meetings, or renovations, ensuring no conflicts in the allocation of limited resources (for example, tables, staff, or vehicles). The system automatically validates restrictions such as resource dependencies, mutual collisions, and availability in time intervals, meeting the requirements of a real event planner.
The project models a hotel domain, where events consume finite resources and must respect customized rules for inclusion (co-requisites) and mutual exclusion. It uses Streamlit for the graphical interface, JSON persistence for data, and backend logic for validations and available schedule searches.
USAGE
Run the application with Streamlit:
        streamlit run interface_front.py
Open your browser at http://localhost:8501 (or the indicated URL).

Main Features

Home: Welcome page with multimedia to contextualize the hotel.
Manage Events: Create or delete events, selecting type, dates, and resources. Automatically validates conflicts and suggests alternative dates if necessary.
Manage Resources: Add, modify, or delete resources, collisions, and dependencies. Includes visualizations such as pie charts for resource distribution.
View Events: Interactive calendar with colored events, details, and selection for inspection.
Info: Information about the application.

Usage Example:
Go to "Manage Events" > "Create".
Select a type (e.g., "Humorous Show"), enter dates (dd/mm/yyyy) and resources.
The system validates and saves if viable; otherwise, it displays detailed errors.
STRUCTURE

interface_front.py: Graphical interface with Streamlit (frontend).
interface_back.py: Backend logic for validations, persistence, and processing.
events.py: Classes to model events with OOP inheritance.
dependencias.py: Configuration of dependencies for predefined events.
Database.json: Data persistence file.
Media/: Folder with images and videos for the UI.
Proyecto 1.md: Original project specification.



DEPENDENCIES


Python 3.8+
Streamlit: For the web interface.
Pandas and Plotly: For dataframes and visualizations.
ULID: For unique ID generation.
Datetime: For date handling (included in Python standard).

See requirements.txt for exact versions (create one with pip freeze > requirements.txt if it doesn't exist).
IMPLEMENTED RESTRICTIONS
Following the project design:

Co-requisites (Inclusion): Resources that must be used together (e.g., "tables" requires "chairs"). Defined in depen_resources of Database.json.
Mutual Exclusion: Incompatible resources (e.g., "prostitutes" cannot be with "engineers"). Defined in collitions.
Global Availability: Checks conflicts in dates and limited resource quantities.

Examples:

A "Humorous Show" requires at least tables, chairs, organizer, and dwarves.
Combining "Dwarves" with "cybernetics" in an event is not allowed.

These rules are validated in the Validation class to prevent invalid assignments.
