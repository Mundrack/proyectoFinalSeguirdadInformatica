from dataclasses import dataclass, asdict, field
from typing import Optional, Dict, Any

@dataclass
class Riesgo:
    activo: str
    amenaza: str
    vulnerabilidad: str = ""
    controles_existentes: str = ""
    probabilidad: int = 1
    impacto: int = 1
    puntaje: int = 1
    nivel: str = "Bajo"
    
    # Fechas para KPIs MERC-PD
    fecha_identificacion: str = ""
    fecha_tratamiento: str = ""
    
    # Tratamiento
    tratamiento_estrategia: str = ""  # Mitigar, Transferir, Aceptar, Evitar
    control_iso: str = ""
    responsable: str = ""
    
    # Riesgo Residual
    probabilidad_residual: int = 0
    impacto_residual: int = 0
    puntaje_residual: int = 0
    nivel_residual: str = ""
    
    # Soporte Multi-tenant
    empresa_id: str = "GLOBAL"

    def calcular_nivel(self, puntaje: int) -> str:
        """
        Calcula el nivel de riesgo según la matriz MERC-PD.
        
        Matriz de Riesgo (Probabilidad × Impacto):
        - Bajo: puntaje <= 4
        - Medio: puntaje 5-9
        - Alto: puntaje 10-14
        - Crítico: puntaje >= 15
        
        Basado en: Metodología MERC-PD, Matriz de Riesgo (Mapa de Calor)
        """
        if puntaje <= 4:
            return "Bajo"
        elif puntaje <= 9:
            return "Medio"
        elif puntaje <= 14:
            return "Alto"
        else:  # puntaje >= 15
            return "Crítico"

    def evaluar_riesgo_inherente(self):
        self.puntaje = self.probabilidad * self.impacto
        self.nivel = self.calcular_nivel(self.puntaje)

    def evaluar_riesgo_residual(self, prob_res: int, imp_res: int):
        self.probabilidad_residual = prob_res
        self.impacto_residual = imp_res
        self.puntaje_residual = prob_res * imp_res
        self.nivel_residual = self.calcular_nivel(self.puntaje_residual)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Riesgo':
        # Filter keys that describe the fields of the class to avoid errors with extra keys
        valid_keys = {k: v for k, v in data.items() if k in cls.__annotations__}
        return cls(**valid_keys)
