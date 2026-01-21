# 🛡️ SecureManager - SGSI Multi-tenant

**SecureManager** es una plataforma integral de Gestión de Seguridad de la Información (SGSI) diseñada bajo la metodología **MERC-PD**. Permite a múltiples organizaciones gestionar sus activos, evaluar riesgos y monitorear KPIs críticos de seguridad de forma aislada y segura.

## 🚀 Características Principales

- **Arquitectura Multi-tenant**: Aislamiento total de datos. Cada empresa tiene su propio entorno, usuarios y métricas.
- **Alineación MERC-PD**:
  - Evaluación de riesgos basada en Probabilidad e Impacto.
  - 3 KPIs oficiales: % de Riesgos Críticos mitigados en < 30 días, Incidentes Reportados vs Prevenidos, y Nivel de Cobertura de Capacitación.
  - Soporte para estrategias de tratamiento oficiales: Mitigar, Transferir, Evitar y Aceptar.
- **Gestión Organizacional**:
  - Roles de **Empresario** (Administrador) y **Empleado**.
  - Sistema de aprobación de miembros para mayor seguridad.
- **Dashboard Dinámico**: Visualización en tiempo real de activos críticos, riesgos altos y cobertura de tratamiento.
- **UX Avanzada**:
  - Buscadores y filtros en tiempo real en todas las tablas clave.
  - IDs automático y manual para un registro de activos más flexible.
  - Exportación de resultados a CSV.

## 🛠️ Tecnologías Utilizadas

- **Backend**: Python / Flask
- **Frontend**: HTML5, Vanilla CSS, JavaScript (Real-time filtering)
- **Persistencia**: Archivos JSON (Estructura ligera e independiente)
- **Seguridad**: Hashing de contraseñas con Werkzeug, Gestión de sesiones, Aislamiento por `empresa_id`.

## 📦 Instalación y Uso

1. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```
2. Ejecutar la aplicación:
   ```bash
   python main.py
   ```
3. Acceder en el navegador: `http://127.0.0.1:5000`

## 👥 Roles
- **Empresario**: Crea la empresa, recibe un ID único y gestiona a los empleados.
- **Empleado**: Se unirá usando el ID de la empresa y esperará aprobación del empresario.

---
© 2026 Proyecto Final de Seguridad Informática
