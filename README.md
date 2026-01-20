# Sistema de Gestión de Riesgos Cibernéticos

Este proyecto es una herramienta para la identificación, evaluación y tratamiento de riesgos de seguridad de la información, alineado con la normativa ISO/IEC 27002:2022.

## Características Principales

1.  **Valoración de Activos**: Registro y clasificación de activos de información (Confidencialidad, Integridad, Disponibilidad).
2.  **Identificación de Riesgos**: Asociación de amenazas y vulnerabilidades a los activos.
3.  **Evaluación de Riesgos**: Cálculo del riesgo inherente basado en Probabilidad x Impacto.
4.  **Tratamiento del Riesgo**:
    *   Selección de estrategia (Mitigar, Transferir, Aceptar, Evitar).
    *   Asignación de controles ISO 27002.
    *   Cálculo del riesgo residual.
5.  **Monitoreo y KPIs**: Simulación de incidentes y visualización de métricas como MTTD y MTTR.
6.  **Reportes**: Exportación de la matriz de riesgos a CSV.

## Requisitos Previos

*   Python 3.10 o superior.
*   Navegador web (Chrome, Firefox, Edge).

## Instalación

1.  Clonar o descargar este repositorio.
2.  Abrir una terminal en la carpeta del proyecto.
3.  Instalar las dependencias:
    ```bash
    pip install -r requirements.txt
    ```

## Ejecución

1.  Ejecutar el servidor Flask:
    ```bash
    python main.py
    ```
2.  Abrir el navegador y visitar: `http://127.0.0.1:5000`

## Estructura del Proyecto

*   `main.py`: Archivo principal de la aplicación Flask.
*   `data/`: Almacena la base de datos en archivos JSON (Activos, Riesgos, Amenazas).
*   `templates/`: Archivos HTML de la interfaz de usuario.
*   `core/`: Lógica de negocio y simulaciones.

## Uso del Sistema

1.  **Inicio**: Vista general del sistema.
2.  **Activos**: Registre los activos de información de su organización.
3.  **Amenazas**: Identifique las amenazas que afectan a sus activos.
4.  **Evaluar**: Realice la evaluación de riesgos inherentes.
5.  **Tratamiento**: Aplique controles y estrategias para mitigar los riesgos.
6.  **KPIs**: Monitoree el desempeño de la seguridad.
