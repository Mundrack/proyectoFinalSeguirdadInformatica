# 📔 Manual de Usuario - SecureManager SGSI
## Sistema de Gestión de Riesgos bajo Estándares ISO 27001 y MERC-PD

¡Bienvenido a **SecureManager**! Esta guía te ayudará a navegar y utilizar todas las funciones de la plataforma para proteger la información de tu organización.

---

## 1. Acceso y Registro (Multi-tenant)

### registro de Empresa (Rol: Empresario)
1. Ve a la pantalla de **Registro**.
2. Selecciona el rol **"Empresario"**.
3. Ingresa el nombre de tu empresa y tus datos personales.
4. Al finalizar, el sistema te entregará un **ID de Empresa** (ej: `A1B2C3D4`). **¡Guárdalo!** Es el código que tus empleados necesitarán para unirse.

### Registro de Empleados (Rol: Empleado)
1. Selecciona el rol **"Empleado"**.
2. Ingresa el **ID de Empresa** que te proporcionó tu jefe.
3. Tu cuenta quedará en estado **"Pendiente"** hasta que el empresario te apruebe en el módulo "Mi Empresa".

---

## 2. Gestión de Activos y Amenazas

### Registro de Activos
- En el menú **"💻 Activos"**, registra los recursos valiosos (servidores, laptops, bases de datos).
- Clasifícalos según su **Confidencialidad, Integridad y Disponibilidad (CID)**. El sistema calculará automáticamente la criticidad.

### Identificación de Amenazas
- En **"⚠️ Amenazas"**, asocia riesgos específicos (ej: Incendio, Hackeo, Error Humano) a tus activos registrados.

---

## 3. Evaluación y Tratamiento (ISO 27001)

### Evaluación de Riesgo Inherente
- En **"🔍 Evaluar Riesgo"**, define la **Probabilidad** y el **Impacto** de cada amenaza.
- El sistema generará una alerta si el nivel de riesgo es **Crítico** o **Alto**.

### Tratamiento de Riesgos y Controles ISO
- En el módulo **"🛡️ Tratamiento"**, podrás definir cómo responder al riesgo:
    1. **Estrategia**: Selecciona si vas a Mitigar, Transferir, Evitar o Aceptar.
    2. **Controles ISO 27001**: Selecciona uno o varios controles de la lista oficial (ej: A.5.1, A.8.24). 
    *💡 Tip: Mantén presionada la tecla **Ctrl** para elegir varios controles.*
    3. **Cálculo Residual**: Define qué tan bajo bajará el riesgo después de aplicar estos controles.

---

## 4. Consulta de Estándares

### Catálogo de Controles ISO 27001
Si no sabes qué medida de seguridad aplicar, visita el módulo **"📖 Catálogo ISO 27001"**. Allí encontrarás:
- Descripciones claras de cada control.
- Guías de **¿Cuándo usar?** para facilitarte la toma de decisiones.

---

## 5. Monitoreo y Reportes

### Dashboard Principal
Visualiza de forma gráfica el estado de tu empresa:
- Cantidad de activos críticos.
- Riesgos mitigados vs. pendientes.
- Porcentaje de cumplimiento general.

### KPIs MERC-PD
En el módulo **"📈 KPIs & Simulación"**, monitorea los 3 indicadores clave:
1. **Eficiencia de Mitigación**: % de riesgos críticos resueltos en menos de 30 días.
2. **Ratio de Incidentes**: Comparación entre ataques prevenidos y reales.
3. **Cobertura de Capacitación**: Nivel de entrenamiento de tu personal.

### Exportación
En **"📑 Reportes"**, puedes descargar toda tu matriz de riesgos en formato **CSV** para abrir en Excel o presentar informes a la dirección.

---
© 2026 Plataforma SecureManager - Gestión de Seguridad de Alto Nivel.
