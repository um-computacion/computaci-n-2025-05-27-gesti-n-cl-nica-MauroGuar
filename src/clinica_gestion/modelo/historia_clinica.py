from .paciente import Paciente
from .turno import Turno
from .receta import Receta

class HistoriaClinica:
    def __init__(self, paciente: Paciente):
        self.__paciente__: Paciente = paciente
        self.__turnos__: list[Turno] = []
        self.__recetas__: list[Receta] = []

    def agregar_turno(self, turno: Turno) -> None:
        if isinstance(turno, Turno):
            self.__turnos__.append(turno)
            # Mantener los turnos ordenados por fecha, del más antiguo al más reciente
            self.__turnos__.sort(key=lambda t: t.obtener_fecha_hora())

    def obtener_turnos(self) -> list[Turno]:
        return list(self.__turnos__)

    def agregar_receta(self, receta: Receta) -> None:
        if isinstance(receta, Receta):
            self.__recetas__.append(receta)
            # Mantener las recetas ordenadas por fecha de emisión, de la más reciente a la más antigua
            self.__recetas__.sort(key=lambda r: r.obtener_fecha_emision(), reverse=True)

    def obtener_recetas(self) -> list[Receta]:
        return list(self.__recetas__)

    def __str__(self) -> str:
        return (
            f"HistoriaClinica("
            f"  Paciente({self.__paciente__}),\n"
            f"  {str(self.__turnos__)},\n"
            f"  {str(self.__recetas__)}\n"
            f")"
        )
