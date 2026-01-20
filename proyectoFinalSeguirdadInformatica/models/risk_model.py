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
    
    # Tratamiento
    tratamiento_estrategia: str = ""  # Mitigar, Transferir, Aceptar, Evitar
    control_iso: str = ""
    responsable: str = ""
    
    # Riesgo Residual
    probabilidad_residual: int = 0
    impacto_residual: int = 0
    puntaje_residual: int = 0
    nivel_residual: str = ""

    def calcular_nivel(self, puntaje: int) -> str:
        if puntaje <= 4: return "Muy Bajo"
        if puntaje <= 8: return "Bajo"
        if puntaje <= 14: return "Medio"
        if puntaje <= 20: return "Alto"
        return "Muy Alto"

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
