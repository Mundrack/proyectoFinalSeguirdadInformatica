import json
from datetime import datetime

def cargar_kpis():
    with open("data/kpis.json", "r") as f:
        data = json.load(f)

    mes_actual = datetime.now().strftime("%Y-%m")
    if data.get("ultimo_mes") != mes_actual:
        data["incidentes"] = 0
        data["ultimo_mes"] = mes_actual
        guardar_kpis(data)

    return data

def guardar_kpis(data):
    with open("data/kpis.json", "w") as f:
        json.dump(data, f, indent=2)

def simular_incidente():
    data = cargar_kpis()
    data["incidentes"] += 1

    data["mttd"] = round(max(0.5, data["mttd"] * 0.95), 2)
    data["mttr"] = round(max(0.5, data["mttr"] * 0.98), 2) 
    data["mfa"] = round(max(0.0, data.get("mfa", 1.0) - 0.02), 2)
    data["parches"] = round(max(0.0, data.get("parches", 1.0) - 0.03), 2)
    data["formacion"] = round(max(0.0, data.get("formacion", 1.0) - 0.01), 2)

    guardar_kpis(data)


def reiniciar_kpis():
    data = cargar_kpis()

    data["mttd"] = 8.0 
    data["mttr"] = 10.0   
    data["incidentes"] = 0
    data["mfa"] = 1.0      
    data["parches"] = 1.0  
    data["formacion"] = 1.0  

    guardar_kpis(data)



