from .especialidad import Especialidad

class Medico:
    def __init__(self, nombre: str, matricula: str):
        self.__nombre__: str = nombre
        self.__matricula__: str = matricula
        self.__especialidades__: list[Especialidad] = []

    def obtener_nombre(self) -> str:
        return self.__nombre__

    def obtener_matricula(self) -> str:
        return self.__matricula__

    def agregar_especialidad(self, especialidad: Especialidad) -> None:
        if isinstance(especialidad, Especialidad):
            self.__especialidades__.append(especialidad)

    def obtener_especialidades_para_dia(self, dia: str) -> list[str]:
        especialidades = []
        dia_lower = dia.lower()
        for esp in self.__especialidades__:
            if esp.verificar_dia(dia_lower):
                especialidades.append(esp.obtener_especialidad())
        return especialidades

    def __str__(self) -> str:
        if not self.__especialidades__:
            especialidades_str = "Ninguna"
        else:
            especialidades_str = f"[{', '.join(str(esp) for esp in self.__especialidades__)}]"

        return f"Medico: {self.__nombre__}, {self.__matricula__}, Especialidades: {especialidades_str}"
