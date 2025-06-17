import unittest
from datetime import datetime, timedelta
from src.clinica_gestion.modelo.clinica import Clinica
from src.clinica_gestion.modelo.paciente import Paciente
from src.clinica_gestion.modelo.medico import Medico
from src.clinica_gestion.modelo.especialidad import Especialidad
from src.clinica_gestion.modelo.turno import Turno
from src.clinica_gestion.modelo.receta import Receta
from src.clinica_gestion.modelo.excepciones import PacienteDuplicadoException, PacienteNoEncontradoException, \
    MedicoDuplicadoException, MedicoNoEncontradoException, MedicoNoDisponibleException, \
    EspecialidadNoValidaParaDiaException, TurnoOcupadoException

class TestClinica(unittest.TestCase):

    def setUp(self):
        self.clinica = Clinica()

        self.paciente1 = Paciente("Ignacio García", "12345678", "01/01/1980")
        self.paciente2 = Paciente("Laura Palmer", "87654321", "15/07/1990")

        self.medico1 = Medico("Dr. Lawrence Jacoby", "MAT001")
        self.medico1.agregar_especialidad(Especialidad("Psiquiatría", ["lunes", "miércoles"]))

        self.medico2 = Medico("Dr. Will Hayward", "MAT002")
        self.medico2.agregar_especialidad(Especialidad("Clínica Médica", ["martes", "jueves"]))
        self.medico2.agregar_especialidad(Especialidad("Cardiología", ["viernes"]))

        # Fechas futuras para turnos (aseguramos que sean días correctos de la semana)
        hoy = datetime.now()
        dias_hasta_lunes = (7 - hoy.weekday()) % 7
        if dias_hasta_lunes == 0:
            dias_hasta_lunes = 7  # Si hoy es lunes, vamos al próximo

        self.fecha_lunes = hoy + timedelta(days=dias_hasta_lunes)
        self.fecha_lunes = self.fecha_lunes.replace(hour=10, minute=0, second=0, microsecond=0)

        dias_hasta_martes = (8 - hoy.weekday()) % 7
        if dias_hasta_martes == 0:
            dias_hasta_martes = 7

        self.fecha_martes = hoy + timedelta(days=dias_hasta_martes)
        self.fecha_martes = self.fecha_martes.replace(hour=11, minute=0, second=0, microsecond=0)

        # Formato de fecha para string
        self.fecha_lunes_str = self.fecha_lunes.strftime("%Y-%m-%d %H:%M")
        self.fecha_martes_str = self.fecha_martes.strftime("%Y-%m-%d %H:%M")

    def test_inicializacion_clinica(self):
        self.assertEqual(len(self.clinica.obtener_pacientes()), 0)
        self.assertEqual(len(self.clinica.obtener_medicos()), 0)

    def test_agregar_paciente(self):
        self.clinica.agregar_paciente(self.paciente1)
        self.assertEqual(len(self.clinica.obtener_pacientes()), 1)
        self.assertEqual(self.clinica.obtener_pacientes()[0].obtener_dni(), "12345678")

    def test_agregar_paciente_duplicado(self):
        self.clinica.agregar_paciente(self.paciente1)
        with self.assertRaises(PacienteDuplicadoException):
            self.clinica.agregar_paciente(self.paciente1)

    def test_validar_existencia_paciente(self):
        self.clinica.agregar_paciente(self.paciente1)
        paciente = self.clinica.obtener_paciente_por_matricula("12345678")
        self.assertEqual(paciente.obtener_nombre(), "Ignacio García")

        with self.assertRaises(PacienteNoEncontradoException):
            self.clinica.obtener_paciente_por_matricula("99999999")

    def test_agregar_medico(self):
        self.clinica.agregar_medico(self.medico1)
        self.assertEqual(len(self.clinica.obtener_medicos()), 1)
        self.assertEqual(self.clinica.obtener_medicos()[0].obtener_matricula(), "MAT001")

    def test_agregar_medico_duplicado(self):
        self.clinica.agregar_medico(self.medico1)
        with self.assertRaises(MedicoDuplicadoException):
            self.clinica.agregar_medico(self.medico1)

    def test_obtener_medico_por_matricula(self):
        self.clinica.agregar_medico(self.medico1)
        medico = self.clinica.obtener_medico_por_matricula("MAT001")
        self.assertEqual(medico.obtener_nombre(), "Dr. Lawrence Jacoby")

        with self.assertRaises(MedicoNoEncontradoException):
            self.clinica.obtener_medico_por_matricula("MAT999")

    def test_parse_fecha_hora(self):
        fecha_hora = self.clinica._parse_fecha_hora("2025-10-15 14:30")
        self.assertEqual(fecha_hora.year, 2025)
        self.assertEqual(fecha_hora.month, 10)
        self.assertEqual(fecha_hora.day, 15)
        self.assertEqual(fecha_hora.hour, 14)
        self.assertEqual(fecha_hora.minute, 30)

        fecha_invalida = self.clinica._parse_fecha_hora("formato-invalido")
        self.assertIsNone(fecha_invalida)

    def test_obtener_dia_semana_en_espanol(self):
        # Crear una fecha para un lunes (weekday=0)
        fecha_lunes = datetime(2023, 1, 2)  # 2 de enero de 2023 fue lunes
        self.assertEqual(self.clinica._obtener_dia_semana_en_espanol(fecha_lunes), "lunes")

        # Crear una fecha para un domingo (weekday=6)
        fecha_domingo = datetime(2023, 1, 8)  # 8 de enero de 2023 fue domingo
        self.assertEqual(self.clinica._obtener_dia_semana_en_espanol(fecha_domingo), "domingo")

    def test_obtener_historia_clinica(self):
        self.clinica.agregar_paciente(self.paciente1)
        historia = self.clinica.obtener_historia_clinica("12345678")
        self.assertEqual(len(historia.obtener_turnos()), 0)
        self.assertEqual(len(historia.obtener_recetas()), 0)

        with self.assertRaises(PacienteNoEncontradoException):
            self.clinica.obtener_historia_clinica("99999999")

    def test_emitir_receta(self):
        self.clinica.agregar_paciente(self.paciente1)
        self.clinica.agregar_medico(self.medico1)

        medicamentos = ["Paracetamol", "Ibuprofeno"]
        receta = self.clinica.emitir_receta("12345678", "MAT001", medicamentos)

        self.assertEqual(receta.__paciente__.obtener_dni(), "12345678")
        self.assertEqual(receta.__medico__.obtener_matricula(), "MAT001")

        historia = self.clinica.obtener_historia_clinica("12345678")
        self.assertEqual(len(historia.obtener_recetas()), 1)

    def test_agendar_turno(self):
        self.clinica.agregar_paciente(self.paciente1)
        self.clinica.agregar_medico(self.medico1)

        turno = self.clinica.agendar_turno("12345678", "MAT001", self.fecha_lunes_str, "Psiquiatría")

        self.assertEqual(turno.obtener_paciente().obtener_dni(), "12345678")
        self.assertEqual(turno.obtener_medico().obtener_matricula(), "MAT001")
        self.assertEqual(turno.obtener_especialidad_atendida(), "Psiquiatría")

        historia = self.clinica.obtener_historia_clinica("12345678")
        self.assertEqual(len(historia.obtener_turnos()), 1)

    def test_agendar_turno_medico_no_disponible(self):
        self.clinica.agregar_paciente(self.paciente1)
        self.clinica.agregar_medico(self.medico1)

        with self.assertRaises(MedicoNoDisponibleException):
            self.clinica.agendar_turno("12345678", "MAT001", self.fecha_martes_str, "Psiquiatría")

    def test_agendar_turno_especialidad_incorrecta(self):
        self.clinica.agregar_paciente(self.paciente1)
        self.clinica.agregar_medico(self.medico1)

        with self.assertRaises(EspecialidadNoValidaParaDiaException):
            self.clinica.agendar_turno("12345678", "MAT001", self.fecha_lunes_str, "Cardiología")

    def test_agendar_turno_ocupado(self):
        self.clinica.agregar_paciente(self.paciente1)
        self.clinica.agregar_paciente(self.paciente2)
        self.clinica.agregar_medico(self.medico1)

        self.clinica.agendar_turno("12345678", "MAT001", self.fecha_lunes_str, "Psiquiatría")

        with self.assertRaises(TurnoOcupadoException):
            self.clinica.agendar_turno("87654321", "MAT001", self.fecha_lunes_str, "Psiquiatría")
