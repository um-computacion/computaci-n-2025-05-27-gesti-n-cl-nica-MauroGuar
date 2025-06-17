
from datetime import datetime
from src.clinica_gestion.modelo.excepciones import PacienteDuplicadoException, PacienteNoEncontradoException, \
    MedicoDuplicadoException, MedicoNoEncontradoException, MedicoNoDisponibleException, \
    EspecialidadNoValidaParaDiaException, TurnoOcupadoException, RecetaInvalidaException
from src.clinica_gestion.modelo.historia_clinica import HistoriaClinica
from src.clinica_gestion.modelo.medico import Medico
from src.clinica_gestion.modelo.paciente import Paciente
from src.clinica_gestion.modelo.receta import Receta
from src.clinica_gestion.modelo.turno import Turno


class Clinica:
    DIAS_SEMANA_ES = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]

    def __init__(self):
        self.__pacientes__: dict[str, Paciente] = {}
        self.__medicos__: dict[str, Medico] = {}
        self.__turnos__: list[Turno] = []
        self.__historias_clinicas__: dict[str, HistoriaClinica] = {}


    # Paciente
    def agregar_paciente(self, paciente: Paciente) -> None:
        dni_paciente = paciente.obtener_dni()
        if dni_paciente in self.__pacientes__:
            raise PacienteDuplicadoException(f"El paciente con DNI {dni_paciente} ya existe.")
        self.__pacientes__[dni_paciente] = paciente
        self.__historias_clinicas__[dni_paciente] = HistoriaClinica(paciente)

    def obtener_pacientes(self) -> list[Paciente]:
        return list(self.__pacientes__.values())

    def obtener_paciente_por_matricula(self, dni: str) -> Paciente:
        if dni in self.__pacientes__:
            return self.__pacientes__[dni]
        else:
            raise PacienteNoEncontradoException(f"No se encontró el paciente con DNI {dni}.")


    # Medico
    def agregar_medico(self, medico: Medico) -> None:
        matricula_medico = medico.obtener_matricula()
        if matricula_medico in self.__medicos__:
            raise MedicoDuplicadoException(f"El médico con matrícula {matricula_medico} ya existe.")

        self.__medicos__[matricula_medico] = medico

    def obtener_medicos(self) -> list[Medico]:
        return list(self.__medicos__.values())

    def obtener_medico_por_matricula(self, matricula: str) -> Medico:
        if matricula in self.__medicos__:
            return self.__medicos__[matricula]
        else:
            raise MedicoNoEncontradoException(f"No se encontró el médico con matrícula {matricula}.")


    # Historia clinica
    def obtener_historia_clinica(self, dni_paciente: str) -> HistoriaClinica:
        self.obtener_paciente_por_matricula(dni_paciente)
        return self.__historias_clinicas__[dni_paciente]


    # Receta
    def emitir_receta(self, dni_paciente: str, matricula_medico: str, medicamentos: list[str] ) -> Receta:
        paciente = self.obtener_paciente_por_matricula(dni_paciente)
        medico = self.obtener_medico_por_matricula(matricula_medico)

        nueva_receta = Receta(paciente, medico, medicamentos)

        historia_paciente = self.obtener_historia_clinica(dni_paciente)
        historia_paciente.agregar_receta(nueva_receta)

        return nueva_receta


    # Turno
    def obtener_turnos(self) -> list[Turno]:
        return list(self.__turnos__)

    def agendar_turno(self, dni_paciente: str, matricula_medico: str, fecha_hora_str: str, nombre_especialidad_deseada: str) -> Turno:
        paciente = self.obtener_paciente_por_matricula(dni_paciente) # Lanza PacienteNoEncontradoException
        medico = self.obtener_medico_por_matricula(matricula_medico) # Lanza MedicoNoEncontradoException

        fecha_hora_dt = self._parse_fecha_hora(fecha_hora_str)
        if not fecha_hora_dt:
            raise ValueError("Formato de fecha y hora inválido. Use YYYY-MM-DD HH:MM.")

        if fecha_hora_dt < datetime.now():
            raise ValueError("No se pueden agendar turnos en el pasado.")

        dia_semana = self._obtener_dia_semana_en_espanol(fecha_hora_dt)

        especialidad_medico_ese_dia = medico.obtener_especialidades_para_dia(dia_semana)

        if not especialidad_medico_ese_dia:
            raise MedicoNoDisponibleException(f"El médico {medico.obtener_nombre()} no atiende ningún día {dia_semana}.")


        if nombre_especialidad_deseada not in especialidad_medico_ese_dia:
            raise EspecialidadNoValidaParaDiaException(
                f"El médico {medico.obtener_nombre()} no atiende la especialidad '{nombre_especialidad_deseada}' los días {dia_semana}."
            )

        for turno_existente in self.__turnos__:
            if turno_existente.obtener_medico() == medico and turno_existente.obtener_fecha_hora() == fecha_hora_dt:
                raise TurnoOcupadoException(
                    f"El médico {medico.obtener_nombre()} ya tiene un turno agendado para {fecha_hora_dt.strftime('%Y-%m-%d %H:%M')}."
                )

        nuevo_turno = Turno(paciente, medico, fecha_hora_dt, nombre_especialidad_deseada)
        self.__turnos__.append(nuevo_turno)

        historia_paciente = self.obtener_historia_clinica(dni_paciente)
        historia_paciente.agregar_turno(nuevo_turno)

        return nuevo_turno


    # Fechas
    def _parse_fecha_hora(self, fecha_hora_str: str) -> datetime | None:
        try:
            return datetime.strptime(fecha_hora_str, "%Y-%m-%d %H:%M")
        except ValueError:
            return None

    def _obtener_dia_semana_en_espanol(self, fecha_hora: datetime) -> str:
        return self.DIAS_SEMANA_ES[fecha_hora.weekday()]