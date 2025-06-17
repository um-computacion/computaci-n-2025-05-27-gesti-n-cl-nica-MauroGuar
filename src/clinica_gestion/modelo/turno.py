from datetime import datetime
from .paciente import Paciente
from .medico import Medico

class Turno:
    def __init__(self, paciente: Paciente, medico: Medico, fecha_hora: datetime, nombre_especialidad: str):
        self.__paciente__: Paciente = paciente
        self.__medico__: Medico = medico
        self.__fecha_hora__: datetime = fecha_hora
        self.__nombre_especialidad_atendida__: str = nombre_especialidad

    def obtener_paciente(self) -> Paciente:
        return self.__paciente__

    def obtener_medico(self) -> Medico:
        return self.__medico__

    def obtener_fecha_hora(self) -> datetime:
        return self.__fecha_hora__

    def obtener_especialidad_atendida(self) -> str:
        return self.__nombre_especialidad_atendida__

    def __str__(self) -> str:
        return (
            f"Turno(\n"
            f"  Paciente: {str(self.__paciente__)},\n"
            f"  {str(self.__medico__)},\n"
            f"  {str(self.__fecha_hora__)},\n"
            f"  {self.__nombre_especialidad_atendida__}\n"
            f")"
        )