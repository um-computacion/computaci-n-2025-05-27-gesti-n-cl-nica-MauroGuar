class Paciente:
    def __init__(self, nombre: str, dni: str, fecha_nacimiento: str):
        self.__nombre__: str = nombre
        self.__dni__: str = dni
        self.__fecha_nacimiento__: str = fecha_nacimiento

    def obtener_dni(self) -> str:
        return self.__dni__

    def __str__(self) -> str:
        return f"{self.__nombre__}, {self.__dni__}, {self.__fecha_nacimiento__}"
