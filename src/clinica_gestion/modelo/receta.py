from datetime import datetime
from .paciente import Paciente
from .medico import Medico

class Receta:
    def __init__(self, paciente: Paciente, medico: Medico, medicamentos: list[str], fecha: datetime = datetime.now()):
        self.__paciente__: Paciente = paciente
        self.__medico__: Medico = medico
        self.__medicamentos__: list[str] = medicamentos
        self.__fecha__: datetime = fecha

    def obtener_fecha_emision(self) -> datetime:
        return self.__fecha__

    def __str__(self) -> str:
        return (
            f"Receta(\n"
            f"  {str(self.__paciente__)},\n"
            f"  {str(self.__medico__)},\n"
            f"  [{", ".join(self.__medicamentos__)}],\n"
            f"  {str(self.__fecha__)},\n"
            f")"
        )
