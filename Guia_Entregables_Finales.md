# Guía Completa de Preparación de Entregables Finales

Esta guía te ayudará a completar los puntos 4 y 5 de tu proyecto final de manera profesional.

## 1. Documento de Respaldo Técnico (Archivo: `Documento_Respaldo_Tecnico.md`)

Ya he generado la estructura base para ti en el archivo `Documento_Respaldo_Tecnico.md`. Para que sea "un documento bien hecho", sigue estos pasos:

1.  **Convertirlo a PDF (Opcional pero recomendado):** Puedes abrir el archivo `.md` en un editor como VS Code o usar un conversor online para pasarlo a formato PDF para la entrega final.
2.  **Insertar las capturas de pantalla:**
    *   Ejecuta tu aplicación (`python main.py`).
    *   Navega por cada módulo y toma capturas de pantalla claras (puedes usar `Win + Shift + S`).
    *   Asegúrate de que haya datos de prueba visibles para que se vea real.
3.  **Personalizar conclusiones:** Si durante el desarrollo tuviste algún aprendizaje específico, añádelo en la sección de conclusiones para darle un toque personal.

---

## 2. Preparación del Video (Entregable 5)

El video es crucial. Aquí tienes un guion sugerido para explicar los módulos:

### Configuración del Video:
*   **Duración recomendada:** 5 a 8 minutos.
*   **Software sugerido:** OBS Studio, Loom (gratuito y fácil) o la Barra de Juegos de Windows (`Win + G`).

### Guion y Estructura del Video:

1.  **Introducción (30 seg):**
    *   Preséntate y menciona el nombre del proyecto: "Sistema de Gestión de Riesgos Basado en MERC-PD".
    *   Explica brevemente el objetivo: Gestionar la seguridad de la información de PyMEs.

2.  **Módulo de Acceso y Multi-tenancy (1.5 min):**
    *   Muestra el **Registro**. Explica la diferencia entre "Empresario" (crea empresa) y "Empleado" (se une con ID).
    *   Muestra el **Login**.

3.  **Módulo de Activos y Amenazas (1.5 min):**
    *   Entra a "Registrar Activos". Explica cómo se calcula la **Criticidad** sumando Confidencialidad, Integridad y Disponibilidad.
    *   Ve a "Identificación de Amenazas" y asocia una amenaza a un activo.

4.  **Módulo de Evaluación y Tratamiento (2 min):**
    *   Muestra la "Evaluación de Riesgo". Explica la **Matriz de Riesgo** (Probabilidad x Impacto = Riesgo Inherente).
    *   Ve a "Tratamiento de Riesgos". Muestra cómo aplicar una estrategia (Mitigar, Evitar, etc.) y un control ISO, y cómo se reduce al **Riesgo Residual**.

5.  **Dashboard de KPIs MERC-PD (1.5 min) [MUY IMPORTANTE]:**
    *   Explica los 3 KPIs implementados:
        1.  **Eficiencia en Mitigación:** Riesgos críticos resueltos en menos de 30 días.
        2.  **Incidentes:** Comparativa entre reportados y prevenidos.
        3.  **Capacitación:** Nivel de cobertura en el personal.

6.  **Despedida y Conclusión (30 seg):**
    *   Resume el valor de la herramienta y cierra el video.

---

## 3. Checklist de Entrega Final

- [ ] **Carpeta del Proyecto:** Asegúrate de incluir la carpeta `data/` con algunos ejemplos pero sin información sensible real.
- [ ] **requirements.txt:** Verifica que esté actualizado.
- [ ] **Documento de Respaldo:** En formato PDF o MD con las imágenes.
- [ ] **Video:** Sube el video a YouTube (como "No listado") o Drive, y asegúrate de dar los permisos de acceso correctos.

> [!TIP]
> ¡Mucha suerte con tu entrega final! El proyecto está muy sólido técnicamente.
