import json
from datetime import datetime, timedelta

def load_json(path):
    """Helper para cargar archivos JSON"""
    try:
        with open(path, "r") as f:
            return json.load(f)
    except:
        return []

def save_json(path, data):
    """Helper para guardar archivos JSON"""
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

# ============================================================================
# KPI 1: % de riesgos críticos mitigados en < 30 días
# ============================================================================
def calcular_kpi_riesgos_criticos(empresa_id="GLOBAL"):
    """
    Según MERC-PD: "% de riesgos críticos mitigados en < 30 días"
    """
    riesgos = load_json("data/riesgos.json")
    
    # Filtrar por empresa y riesgos críticos
    criticos = [r for r in riesgos if r.get('empresa_id') == empresa_id and r.get('nivel') == 'Crítico']
    total_criticos = len(criticos)
    
    if total_criticos == 0:
        return {
            'total_criticos': 0,
            'mitigados_30_dias': 0,
            'porcentaje': 100,
            'estado': 'excelente'
        }
    
    # Contar los que tienen tratamiento aplicado en < 30 días
    mitigados = 0
    for riesgo in criticos:
        if riesgo.get('tratamiento_estrategia') and riesgo.get('fecha_tratamiento'):
            fecha_id = riesgo.get('fecha_identificacion', '')
            fecha_trat = riesgo.get('fecha_tratamiento', '')
            
            if fecha_id and fecha_trat:
                try:
                    f_id = datetime.strptime(fecha_id, "%Y-%m-%d")
                    f_trat = datetime.strptime(fecha_trat, "%Y-%m-%d")
                    dias = (f_trat - f_id).days
                    
                    if dias <= 30:
                        mitigados += 1
                except:
                    pass
    
    porcentaje = (mitigados / total_criticos) * 100 if total_criticos > 0 else 0
    
    if porcentaje >= 80:
        estado = 'excelente'
    elif porcentaje >= 60:
        estado = 'bueno'
    elif porcentaje >= 40:
        estado = 'regular'
    else:
        estado = 'critico'
    
    return {
        'total_criticos': total_criticos,
        'mitigados_30_dias': mitigados,
        'porcentaje': round(porcentaje, 1),
        'estado': estado
    }

# ============================================================================
# KPI 2: Número de incidentes de seguridad reportados vs. prevenidos
# ============================================================================
def obtener_datos_incidentes(empresa_id="GLOBAL"):
    """
    Según MERC-PD: "Número de incidentes de seguridad reportados vs. prevenidos"
    """
    all_kpis = load_json("data/kpis.json")
    # Si kpis.json es una lista de dicts con empresa_id
    if isinstance(all_kpis, list):
        kpis = next((k for k in all_kpis if k.get('empresa_id') == empresa_id), {})
    else:
        kpis = {} # Fallback for old structure
    
    reportados = kpis.get('incidentes_reportados', 0)
    prevenidos = kpis.get('incidentes_prevenidos', 0)
    
    ratio = prevenidos / reportados if reportados > 0 else 0
    
    return {
        'reportados': reportados,
        'prevenidos': prevenidos,
        'ratio': round(ratio, 2)
    }

def guardar_datos_incidentes(reportados, prevenidos, empresa_id="GLOBAL"):
    """
    Guardar datos de incidentes ingresados manualmente por el usuario
    """
    all_kpis = load_json("data/kpis.json")
    if not isinstance(all_kpis, list): all_kpis = []
    
    found = False
    for k in all_kpis:
        if k.get('empresa_id') == empresa_id:
            k['incidentes_reportados'] = reportados
            k['incidentes_prevenidos'] = prevenidos
            found = True
            break
    
    if not found:
        all_kpis.append({
            'empresa_id': empresa_id,
            'incidentes_reportados': reportados,
            'incidentes_prevenidos': prevenidos,
            'total_empleados': 0,
            'empleados_capacitados': 0
        })
        
    save_json("data/kpis.json", all_kpis)

# ============================================================================
# KPI 3: Nivel de cobertura de capacitación en protección de datos
# ============================================================================
def obtener_datos_capacitacion(empresa_id="GLOBAL"):
    """
    Según MERC-PD: "Nivel de cobertura de capacitación en protección de datos"
    """
    # Cargar usuarios reales
    users = load_json("data/users.json")
    
    # Filtrar empleados de la empresa
    empleados = [u for u in users if u.get('empresa_id') == empresa_id]
    total = len(empleados)
    
    # Contar capacitados (propiedad 'capacitado' == True)
    capacitados = len([u for u in empleados if u.get('capacitado', False) is True])
    
    porcentaje = (capacitados / total) * 100 if total > 0 else 0
    
    if porcentaje >= 80:
        estado = 'excelente'
    elif porcentaje >= 60:
        estado = 'bueno'
    elif porcentaje >= 40:
        estado = 'regular'
    else:
        estado = 'critico'
    
    return {
        'total_empleados': total,
        'capacitados': capacitados,
        'porcentaje': round(porcentaje, 1),
        'estado': estado
    }

def guardar_datos_capacitacion(total, capacitados, empresa_id="GLOBAL"):
    """
    Guardar datos de capacitación ingresados manualmente por el usuario
    """
    all_kpis = load_json("data/kpis.json")
    if not isinstance(all_kpis, list): all_kpis = []
    
    found = False
    for k in all_kpis:
        if k.get('empresa_id') == empresa_id:
            k['total_empleados'] = total
            k['empleados_capacitados'] = capacitados
            found = True
            break
            
    if not found:
        all_kpis.append({
            'empresa_id': empresa_id,
            'incidentes_reportados': 0,
            'incidentes_prevenidos': 0,
            'total_empleados': total,
            'empleados_capacitados': capacitados
        })
        
    save_json("data/kpis.json", all_kpis)

# ============================================================================
# Datos adicionales para visualización
# ============================================================================
def obtener_distribucion_riesgos(empresa_id="GLOBAL"):
    """
    Obtener distribución de riesgos por nivel para gráficos
    """
    riesgos = load_json("data/riesgos.json")
    
    distribucion = {
        'Bajo': 0,
        'Medio': 0,
        'Alto': 0,
        'Crítico': 0
    }
    
    for riesgo in riesgos:
        if riesgo.get('empresa_id') == empresa_id:
            nivel = riesgo.get('nivel', 'Bajo')
            if nivel in distribucion:
                distribucion[nivel] += 1
    
    return distribucion

def obtener_resumen_dashboard(empresa_id="GLOBAL"):
    """
    Obtener todos los datos para el dashboard de KPIs (filtrados por empresa)
    """
    return {
        'kpi1': calcular_kpi_riesgos_criticos(empresa_id),
        'kpi2': obtener_datos_incidentes(empresa_id),
        'kpi3': obtener_datos_capacitacion(empresa_id),
        'distribucion': obtener_distribucion_riesgos(empresa_id)
    }

