from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
import json
import csv
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from flask import send_file
from core.sim import simular_incidente, cargar_kpis, reiniciar_kpis
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
        with open(path, "r") as f:
            return json.load(f)
    return []

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_confirm = request.form['password_confirm']
        name = request.form['name']
        
        # Check if passwords match
        if password != password_confirm:
            flash('Las contraseñas no coinciden')
            return redirect(url_for('register'))
        
        users = load_json("data/users.json")
        
        # Check if user exists
        for u in users:
            if u['username'] == username:
                flash('El usuario ya existe')
                return redirect(url_for('register'))
        
        # Create new user
        new_user = {
            "username": username,
            "password_hash": generate_password_hash(password),
            "name": name
        }
        users.append(new_user)
        save_json("data/users.json", users)
        
        flash('Registro exitoso. Por favor inicia sesión.')
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
    return render_template('index.html')

@app.route("/activos", methods=["GET", "POST"])
@login_required
def activos():
    path = "data/risk_register.json"
    if request.method == "POST":
        nombre = request.form["nombre"]
        categoria = request.form["categoria"]
        c = int(request.form["confidencialidad"])
        i = int(request.form["integridad"])
        d = int(request.form["disponibilidad"])
        criticidad = c + i + d

        data = {"nombre": nombre, "categoria": categoria, "criticidad": criticidad}
        registros = load_json(path)
        registros.append(data)
        save_json(path, registros)

        return render_template("success.html", 
                             message=f"Activo '{nombre}' registrado con éxito.",
                             primary_action="Registrar Otro Activo",
                             primary_action_url="/activos")
    return render_template("activos.html")


@app.route("/amenazas", methods=["GET", "POST"])
@login_required
def amenazas():
    path = "data/threats.json"
    if request.method == "POST":
        nombre = request.form["nombre"]
        tipo = request.form["tipo"]
        activo = request.form["activo"]

        amenaza = {"nombre": nombre, "tipo": tipo, "activo": activo}
        amenazas = load_json(path)
        amenazas.append(amenaza)
        save_json(path, amenazas)

        return render_template("success.html", 
                             message=f"Amenaza '{nombre}' registrada para activo '{activo}'.",
                             primary_action="Registrar Otra Amenaza",
                             primary_action_url="/amenazas")

    activos = load_json("data/risk_register.json")
    amenazas = load_json(path)
    return render_template("amenazas.html", amenazas=amenazas, activos=activos)


@app.route("/evaluar", methods=["GET", "POST"])
@login_required
def evaluar():
    riesgos_path = "data/riesgos.json"
    
    if request.method == "POST":
        # Capture form data
        activo = request.form["activo"]
        amenaza = request.form["amenaza"]
        vulnerabilidad = request.form.get("vulnerabilidad", "No especificada")
        controles = request.form.get("controles", "Ninguno")
        probabilidad = int(request.form["probabilidad"])
        impacto = int(request.form["impacto"])

        # Create Risk Object
        riesgo = Riesgo(
            activo=activo,
            amenaza=amenaza,
            vulnerabilidad=vulnerabilidad,
            controles_existentes=controles,
            probabilidad=probabilidad,
            impacto=impacto
        )
        riesgo.evaluar_riesgo_inherente()

        # Save
        riesgos_data = load_json(riesgos_path)
        riesgos_data.append(riesgo.to_dict())
        save_json(riesgos_path, riesgos_data)

    activos = load_json("data/risk_register.json")
    amenazas = load_json("data/threats.json")
    riesgos_data = load_json(riesgos_path)
    
    # Convert dicts back to objects for display if needed, or pass dicts
    # Passing dicts is fine for Jinja
    return render_template("evaluar.html", activos=activos, amenazas=amenazas, riesgos=riesgos_data)


@app.route("/tratamiento", methods=["GET"])
@login_required
def tratamiento():
    riesgos_data = load_json("data/riesgos.json")
    # Pass index to allow editing specific items
    for idx, r in enumerate(riesgos_data):
        r["id"] = idx
    return render_template("tratamiento.html", riesgos=riesgos_data)

@app.route("/tratamiento/guardar", methods=["POST"])
@login_required
def guardar_tratamiento():
    riesgos_path = "data/riesgos.json"
    riesgos_data = load_json(riesgos_path)
    
    risk_id = int(request.form["risk_id"])
    estrategia = request.form["estrategia"]
    control = request.form["control"]
    responsable = request.form["responsable"]
    
    # Probability/Impact Residual might be same or lower
    prob_res = int(request.form["probabilidad_residual"])
    imp_res = int(request.form["impacto_residual"])

    if 0 <= risk_id < len(riesgos_data):
        # Rehydrate object
        riesgo = Riesgo.from_dict(riesgos_data[risk_id])
        
        # Apply treatment
        riesgo.tratamiento_estrategia = estrategia
        riesgo.control_iso = control
        riesgo.responsable = responsable
        riesgo.evaluar_riesgo_residual(prob_res, imp_res)
        
        # Save back
        riesgos_data[risk_id] = riesgo.to_dict()
        save_json(riesgos_path, riesgos_data)
        
    return redirect(url_for("tratamiento"))

@app.route("/exportar_csv")
@login_required
def exportar_csv():
    filename = "riesgos_exportados.csv"
    riesgos_data = load_json("data/riesgos.json")
    
    # Convert to objects for easy access
    riesgos = [Riesgo.from_dict(r) for r in riesgos_data]

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
    data = cargar_kpis()
    return render_template("kpis.html", mttd=data["mttd"], mttr=data["mttr"], incidentes=data["incidentes"])

@app.route("/simular_incidente", methods=["POST"])
@login_required
def simular():
    simular_incidente()
    return redirect("/kpis")

@app.route("/reiniciar_kpis", methods=["POST"])
@login_required
def reiniciar():
    reiniciar_kpis()
    return redirect("/kpis")

@app.route("/reporte")
@login_required
def reporte():
    riesgos_data = load_json("data/riesgos.json")
    return render_template("reporte.html", registro=riesgos_data)


if __name__ == '__main__':
    app.run(debug=True)
