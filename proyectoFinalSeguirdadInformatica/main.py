from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
import json
import csv
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from flask import send_file
from core.kpis_merc_pd import obtener_resumen_dashboard, guardar_datos_incidentes, guardar_datos_capacitacion
from models.risk_model import Riesgo

app = Flask(__name__)
app.secret_key = 'super_secret_key_change_this_for_production' # Necesario para sesiones

# Decorador para requerir login
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Helper to load/save JSON
def load_json(path):
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if not content:
                    return []
                return json.loads(content)
        except (json.JSONDecodeError, ValueError):
            return []
    return []

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_confirm = request.form['password_confirm']
        name = request.form['name']
        role = request.form['role']
        
        if password != password_confirm:
            flash('Las contraseñas no coinciden')
            return redirect(url_for('register'))
        
        users = load_json("data/users.json")
        empresas = load_json("data/empresas.json")
        
        for u in users:
            if u['username'] == username:
                flash('El usuario ya existe')
                return redirect(url_for('register'))
        
        empresa_id = None
        
        if role == 'empresario':
            company_name = request.form.get('company_name')
            # Generate a simple ID for the company
            import uuid
            empresa_id = str(uuid.uuid4())[:8].upper()
            new_empresa = {
                "id": empresa_id,
                "nombre": company_name,
                "fundador": username
            }
            empresas.append(new_empresa)
            save_json("data/empresas.json", empresas)
        else:
            # For employee, check if company exists
            empresa_id = request.form.get('company_id').upper()
            empresa_existe = False
            for emp in empresas:
                if emp['id'] == empresa_id:
                    empresa_existe = True
                    break
            
            if not empresa_existe:
                flash(f'La empresa con ID {empresa_id} no existe')
                return redirect(url_for('register'))

        # Create new user
        new_user = {
            "username": username,
            "password_hash": generate_password_hash(password),
            "name": name,
            "role": role,
            "empresa_id": empresa_id,
            "status": "activo" if role == "empresario" else "pendiente" # Empresario is active by default
        }
        users.append(new_user)
        save_json("data/users.json", users)
        
        flash(f'Registro exitoso. Tu ID de empresa es: {empresa_id}' if role == 'empresario' else 'Registro exitoso.')
        return redirect(url_for('login'))
        
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        users = load_json("data/users.json")
        user = next((u for u in users if u['username'] == username), None)
        
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['username']
            session['user_name'] = user['name']
            session['role'] = user.get('role', 'empresario')
            session['empresa_id'] = user.get('empresa_id', 'GLOBAL')
            return redirect(url_for('index'))
        
        flash('Usuario o contraseña incorrectos')
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    user_empresa = session.get('empresa_id')
    users = load_json("data/users.json")
    user = next((u for u in users if u['username'] == session['user_id']), None)
    
    if user and user.get('status') == 'pendiente':
        return render_template('pending.html')
    
    # Calcular estadísticas dinámicas
    activos_data = load_json("data/risk_register.json")
    riesgos_data = load_json("data/riesgos.json")
    
    # Filtrar por empresa
    mis_activos = [a for a in activos_data if a.get('empresa_id') == user_empresa]
    mis_riesgos = [r for r in riesgos_data if r.get('empresa_id') == user_empresa]
    
    stats = {
        'total_activos': len(mis_activos),
        'total_riesgos': len(mis_riesgos),
        'activos_criticos': len([a for a in mis_activos if a.get('criticidad', 0) >= 12]),
        'riesgos_altos': len([r for r in mis_riesgos if r.get('puntaje', 0) >= 10]),
        'riesgos_mitigados': len([r for r in mis_riesgos if r.get('tratamiento_estrategia')]),
        'cumplimiento': 0
    }
    
    if len(mis_riesgos) > 0:
        stats['cumplimiento'] = round((stats['riesgos_mitigados'] / len(mis_riesgos)) * 100)

    return render_template('index.html', stats=stats)

@app.route('/empresa')
@login_required
def empresa():
    user_empresa_id = session.get('empresa_id')
    empresas = load_json("data/empresas.json")
    empresa = next((e for e in empresas if e['id'] == user_empresa_id), {"nombre": "N/A", "id": user_empresa_id, "fundador": "N/A"})
    
    all_users = load_json("data/users.json")
    miembros = [u for u in all_users if u.get('empresa_id') == user_empresa_id]
    
    return render_template('empresa.html', empresa=empresa, miembros=miembros)

@app.route('/empresa/miembros/aprobar', methods=['POST'])
@login_required
def aprobar_miembro():
    if session.get('role') != 'empresario':
        flash('No tienes permiso para esta acción')
        return redirect(url_for('empresa'))
        
    username_to_approve = request.form.get('username')
    users = load_json("data/users.json")
    
    for u in users:
        if u['username'] == username_to_approve and u.get('empresa_id') == session.get('empresa_id'):
            u['status'] = 'activo'
            break
            
    save_json("data/users.json", users)
    flash(f'Usuario {username_to_approve} aprobado')
    return redirect(url_for('empresa'))

@app.route('/empresa/miembros/eliminar', methods=['POST'])
@login_required
def eliminar_miembro():
    if session.get('role') != 'empresario':
        flash('No tienes permiso para esta acción')
        return redirect(url_for('empresa'))
        
    username_to_delete = request.form.get('username')
    if username_to_delete == session.get('user_id'):
        flash('No puedes eliminarte a ti mismo')
        return redirect(url_for('empresa'))
        
    users = load_json("data/users.json")
    new_users = [u for u in users if not (u['username'] == username_to_delete and u.get('empresa_id') == session.get('empresa_id'))]
    
    save_json("data/users.json", new_users)
    flash(f'Usuario {username_to_delete} eliminado')
    return redirect(url_for('empresa'))

@app.route('/empresa/miembros/capacitar', methods=['POST'])
@login_required
def capacitar_miembro():
    if session.get('role') != 'empresario':
        flash('No tienes permiso para esta acción')
        # return redirect to dashboard or wherever appropriate
        return redirect(url_for('empresa'))
        
    username_to_train = request.form.get('username')
    action = request.form.get('action') # 'train' or 'untrain'
    
    users = load_json("data/users.json")
    for u in users:
        if u['username'] == username_to_train and u.get('empresa_id') == session.get('empresa_id'):
            u['capacitado'] = (action == 'train')
            break
            
    save_json("data/users.json", users)
    flash(f'Estado de capacitación actualizado para {username_to_train}')
    return redirect(url_for('empresa'))

@app.route("/activos", methods=["GET", "POST"])
@login_required
def activos():
    path = "data/risk_register.json"
    user_empresa = session.get('empresa_id', 'GLOBAL')
    
    if request.method == "POST":
        nombre = request.form["nombre"]
        categoria = request.form["categoria"]
        c = int(request.form["confidencialidad"])
        i = int(request.form["integridad"])
        d = int(request.form["disponibilidad"])
        responsable = request.form["responsable"]
        id_manual = request.form["id_manual"]
        criticidad = c + i + d
        
        # Generar ID automático (scoped by company)
        registros = load_json(path)
        empresa_registros = [r for r in registros if r.get('empresa_id') == user_empresa]
        id_auto = len(empresa_registros) + 1

        data = {
            "id_auto": id_auto,
            "id_manual": id_manual,
            "nombre": nombre, 
            "categoria": categoria,
            "confidencialidad": c,
            "integridad": i,
            "disponibilidad": d,
            "criticidad": criticidad,
            "responsable": responsable,
            "empresa_id": user_empresa # Save company ID
        }
        registros.append(data)
        save_json(path, registros)

        return render_template("success.html", 
                             message=f"Activo '{nombre}' registrado con éxito (ID: {id_auto}).",
                             primary_action="Registrar Otro Activo",
                             primary_action_url="/activos")
    
    # GET request - mostrar solo activos de la empresa actual
    all_activos = load_json(path)
    mis_activos = [a for a in all_activos if a.get('empresa_id') == user_empresa]
    return render_template("activos.html", activos=mis_activos)


@app.route("/amenazas", methods=["GET", "POST"])
@login_required
def amenazas():
    path = "data/threats.json"
    user_empresa = session.get('empresa_id', 'GLOBAL')
    
    if request.method == "POST":
        nombre = request.form["nombre"]
        tipo = request.form["tipo"]
        activo = request.form["activo"]

        amenaza = {
            "nombre": nombre, 
            "tipo": tipo, 
            "activo": activo,
            "empresa_id": user_empresa
        }
        amenazas = load_json(path)
        amenazas.append(amenaza)
        save_json(path, amenazas)

        return render_template("success.html", 
                             message=f"Amenaza '{nombre}' registrada para activo '{activo}'.",
                             primary_action="Registrar Otra Amenaza",
                             primary_action_url="/amenazas")

    # Filter assets and threats by company
    all_activos = load_json("data/risk_register.json")
    mis_activos = [a for a in all_activos if a.get('empresa_id') == user_empresa]
    
    all_amenazas = load_json(path)
    mis_amenazas = [t for t in all_amenazas if t.get('empresa_id') == user_empresa]
    
    return render_template("amenazas.html", amenazas=mis_amenazas, activos=mis_activos)


@app.route("/evaluar", methods=["GET", "POST"])
@login_required
def evaluar():
    riesgos_path = "data/riesgos.json"
    user_empresa = session.get('empresa_id', 'GLOBAL')
    
    if request.method == "POST":
        # Capture form data
        activo = request.form["activo"]
        amenaza = request.form["amenaza"]
        vulnerabilidad = request.form.get("vulnerabilidad", "No especificada")
        controles = request.form.get("controles", "Ninguno")
        probabilidad = int(request.form["probabilidad"])
        impacto = int(request.form["impacto"])
        
        # Capturar fecha de identificación automáticamente
        from datetime import datetime
        fecha_actual = datetime.now().strftime("%Y-%m-%d")

        # Create Risk Object with company isolation
        riesgo = Riesgo(
            activo=activo,
            amenaza=amenaza,
            vulnerabilidad=vulnerabilidad,
            controles_existentes=controles,
            probabilidad=probabilidad,
            impacto=impacto,
            fecha_identificacion=fecha_actual,
            empresa_id=user_empresa
        )
        riesgo.evaluar_riesgo_inherente()

        # Save to database
        riesgos_data = load_json(riesgos_path)
        riesgos_data.append(riesgo.to_dict())
        save_json(riesgos_path, riesgos_data)
        
        return render_template("success.html", 
                             message="Evaluación de riesgo completada.",
                             primary_action="Evaluar Otro Riesgo",
                             primary_action_url="/evaluar")

    # Filter by company for display
    all_activos = load_json("data/risk_register.json")
    mis_activos = [a for a in all_activos if a.get('empresa_id') == user_empresa]
    
    all_amenazas = load_json("data/threats.json")
    mis_amenazas = [t for t in all_amenazas if t.get('empresa_id') == user_empresa]
    
    all_riesgos = load_json(riesgos_path)
    mis_riesgos = [r for r in all_riesgos if r.get('empresa_id') == user_empresa]
    
    return render_template("evaluar.html", activos=mis_activos, amenazas=mis_amenazas, riesgos=mis_riesgos)


@app.route("/tratamiento", methods=["GET"])
@login_required
def tratamiento():
    user_empresa = session.get('empresa_id', 'GLOBAL')
    all_riesgos = load_json("data/riesgos.json")
    # Filter risks by company
    mis_riesgos = [r for r in all_riesgos if r.get('empresa_id') == user_empresa]
    
    # Pass index of original list to allow editing
    for r in mis_riesgos:
        for idx, orig in enumerate(all_riesgos):
            if orig == r:
                r["id"] = idx
                break

    # Pass controls catalog for the multi-select
    iso_controls_raw = load_json("data/iso_controls.json")
    all_iso_controls = []
    for group in iso_controls_raw:
        for ctrl in group['controles']:
            all_iso_controls.append(ctrl)

    return render_template("tratamiento.html", riesgos=mis_riesgos, iso_controls=all_iso_controls)

@app.route("/catalogo")
@login_required
def catalogo():
    iso_controls = load_json("data/iso_controls.json")
    return render_template("catalogo.html", iso_groups=iso_controls)

@app.route("/tratamiento/guardar", methods=["POST"])
@login_required
def guardar_tratamiento():
    riesgos_path = "data/riesgos.json"
    riesgos_data = load_json(riesgos_path)
    
    risk_id = int(request.form["risk_id"])
    
    # Get multiple strategies from checkboxes (returns list)
    estrategias_list = request.form.getlist("estrategia")
    estrategia = ", ".join(estrategias_list) if estrategias_list else "Sin estrategia"
    
    # Get multiple ISO controls
    controles_list = request.form.getlist("control")
    control = ", ".join(controles_list) if controles_list else "Sin control específico"
    
    responsable = request.form["responsable"]
    
    # Probability/Impact Residual might be same or lower
    prob_res = int(request.form["probabilidad_residual"])
    imp_res = int(request.form["impacto_residual"])
    
    # Capturar fecha de tratamiento
    from datetime import datetime
    fecha_tratamiento = datetime.now().strftime("%Y-%m-%d")


    if 0 <= risk_id < len(riesgos_data):
        # Rehydrate object
        riesgo = Riesgo.from_dict(riesgos_data[risk_id])
        
        # Verificar pertenencia para seguridad
        if riesgo.empresa_id != session.get('empresa_id', 'GLOBAL'):
            flash('Acceso denegado a este riesgo')
            return redirect(url_for("tratamiento"))
        
        # Apply treatment
        riesgo.tratamiento_estrategia = estrategia
        riesgo.control_iso = control
        riesgo.responsable = responsable
        riesgo.fecha_tratamiento = fecha_tratamiento
        riesgo.evaluar_riesgo_residual(prob_res, imp_res)
        
        # Save back
        riesgos_data[risk_id] = riesgo.to_dict()
        save_json(riesgos_path, riesgos_data)
        
    return redirect(url_for("tratamiento"))

@app.route("/exportar_csv")
@login_required
def exportar_csv():
    user_empresa = session.get('empresa_id', 'GLOBAL')
    filename = f"riesgos_{user_empresa}.csv"
    all_riesgos = load_json("data/riesgos.json")
    mis_riesgos_data = [r for r in all_riesgos if r.get('empresa_id') == user_empresa]
    
    # Convert to objects for easy access
    riesgos = [Riesgo.from_dict(r) for r in mis_riesgos_data]

    with open(filename, "w", newline="", encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Activo", "Amenaza", "Vulnerabilidad", "Nivel Inherente", "Estrategia", "Control ISO", "Nivel Residual", "Responsable"])
        for r in riesgos:
            writer.writerow([
                r.activo, 
                r.amenaza, 
                r.vulnerabilidad, 
                r.nivel, 
                r.tratamiento_estrategia, 
                r.control_iso, 
                r.nivel_residual,
                r.responsable
            ])

    return send_file(filename, as_attachment=True)


@app.route("/kpis")
@login_required
def kpis():
    """Dashboard de KPIs MERC-PD con datos reales (Filtrados por empresa)"""
    user_empresa = session.get('empresa_id', 'GLOBAL')
    data = obtener_resumen_dashboard(empresa_id=user_empresa)
    return render_template("kpis.html", **data)

@app.route("/kpis/incidentes", methods=["POST"])
@login_required
def guardar_kpis_incidentes():
    """Guardar datos de incidentes ingresados manualmente (Filtrado por empresa)"""
    user_empresa = session.get('empresa_id', 'GLOBAL')
    reportados = int(request.form["incidentes_reportados"])
    prevenidos = int(request.form["incidentes_prevenidos"])
    guardar_datos_incidentes(reportados, prevenidos, empresa_id=user_empresa)
    return redirect("/kpis")

@app.route("/kpis/capacitacion", methods=["POST"])
@login_required
def guardar_kpis_capacitacion():
    """Guardar datos de capacitación ingresados manualmente (Filtrado por empresa)"""
    user_empresa = session.get('empresa_id', 'GLOBAL')
    total = int(request.form["total_empleados"])
    capacitados = int(request.form["empleados_capacitados"])
    guardar_datos_capacitacion(total, capacitados, empresa_id=user_empresa)
    return redirect("/kpis")


@app.route("/reporte")
@login_required
def reporte():
    user_empresa = session.get('empresa_id', 'GLOBAL')
    all_riesgos = load_json("data/riesgos.json")
    mis_riesgos = [r for r in all_riesgos if r.get('empresa_id') == user_empresa]
    return render_template("reporte.html", registro=mis_riesgos)


if __name__ == '__main__':
    app.run(debug=True)
