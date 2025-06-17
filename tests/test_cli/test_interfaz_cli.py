import unittest
from unittest.mock import patch, MagicMock

from src.clinica_gestion.cli.interfaz_cli import CLI
from src.clinica_gestion.modelo.clinica import Clinica
from src.clinica_gestion.modelo.especialidad import Especialidad
from src.clinica_gestion.modelo.excepciones import (
    PacienteDuplicadoException,
    PacienteNoEncontradoException,
    MedicoDuplicadoException,
    MedicoNoEncontradoException,
    MedicoNoDisponibleException,
    TurnoOcupadoException,
    EspecialidadNoValidaParaDiaException
)
from src.clinica_gestion.modelo.medico import Medico
from src.clinica_gestion.modelo.paciente import Paciente
from src.clinica_gestion.modelo.turno import Turno


class TestInterfazCLI(unittest.TestCase):

    def setUp(self):
        self.clinica_mock = MagicMock(spec=Clinica)
        self.cli = CLI(self.clinica_mock)

        self.paciente1 = Paciente("Ignacio García", "12345678", "01/01/1980")
        self.medico1 = Medico("Dr. Lawrence Jacoby", "MAT001")
        self.especialidad1 = Especialidad("Cardiología", ["lunes"])
        self.medico1.agregar_especialidad(self.especialidad1)

        # Ensure DIAS_SEMANA_ES is available for tests that might rely on it
        # This is usually set on the Clinica class itself.
        if not hasattr(Clinica, 'DIAS_SEMANA_ES') or not Clinica.DIAS_SEMANA_ES:
            Clinica.DIAS_SEMANA_ES = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]


    @patch('builtins.input', side_effect=["Juan Pérez", "12345678", "01/01/1990"])
    @patch('builtins.print')
    def test_opcion_agregar_paciente(self, mock_print, mock_input):
        self.cli._opcion_agregar_paciente()
        self.clinica_mock.agregar_paciente.assert_called_once()
        paciente_arg = self.clinica_mock.agregar_paciente.call_args[0][0]
        self.assertEqual(paciente_arg.obtener_nombre(), "Juan Pérez")
        self.assertEqual(paciente_arg.obtener_dni(), "12345678")
        mock_print.assert_any_call("Paciente Juan Pérez (DNI: 12345678) agregado exitosamente.")

    @patch('builtins.input', side_effect=["Jane Doe", "87654321", "02/02/1992"])
    def test_opcion_agregar_paciente_duplicado_raises_exception(self, mock_input):
        self.clinica_mock.agregar_paciente.side_effect = PacienteDuplicadoException("DNI ya existe")
        with self.assertRaises(PacienteDuplicadoException):
            self.cli._opcion_agregar_paciente()

    @patch('builtins.print')
    def test_opcion_listar_pacientes_vacio(self, mock_print):
        self.clinica_mock.obtener_pacientes.return_value = []
        self.cli._opcion_listar_pacientes()
        mock_print.assert_any_call("No hay pacientes registrados.")

    @patch('builtins.print')
    def test_opcion_listar_pacientes_con_pacientes(self, mock_print):
        self.clinica_mock.obtener_pacientes.return_value = [self.paciente1]
        self.cli._opcion_listar_pacientes()
        mock_print.assert_any_call(self.paciente1)

    @patch('builtins.input', side_effect=["Dr. Smith", "MED123", "n"])
    @patch('builtins.print')
    def test_opcion_agregar_medico_sin_especialidad(self, mock_print, mock_input):
        self.cli._opcion_agregar_medico()
        self.clinica_mock.agregar_medico.assert_called_once()
        medico_arg = self.clinica_mock.agregar_medico.call_args[0][0]
        self.assertEqual(medico_arg.obtener_nombre(), "Dr. Smith")
        self.assertEqual(medico_arg.obtener_matricula(), "MED123")
        self.assertEqual(len(medico_arg.obtener_especialidades()), 0)
        mock_print.assert_any_call("Médico Dr. Smith (Matrícula: MED123) agregado exitosamente.")

    @patch('builtins.input', side_effect=["Dr. Jones", "MED456", "s", "Cardiología", "lunes,martes", "n"])
    @patch('builtins.print')
    def test_opcion_agregar_medico_con_especialidad(self, mock_print, mock_input):
        self.cli._opcion_agregar_medico()
        self.clinica_mock.agregar_medico.assert_called_once()
        medico_arg = self.clinica_mock.agregar_medico.call_args[0][0]
        self.assertEqual(medico_arg.obtener_nombre(), "Dr. Jones")
        especialidades = medico_arg.obtener_especialidades()
        self.assertEqual(len(especialidades), 1)
        self.assertEqual(especialidades[0].obtener_especialidad(), "Cardiología")
        self.assertIn("lunes", especialidades[0].__dias__)
        self.assertIn("martes", especialidades[0].__dias__)
        mock_print.assert_any_call("Especialidad 'Cardiología' agregada al Dr. Dr. Jones.")

    @patch('builtins.input', side_effect=["Dr. Who", "MED789", "s", "Time Travel", "domingo,invalidday", "n"])
    @patch('builtins.print')
    def test_opcion_agregar_medico_con_especialidad_dias_invalidos(self, mock_print, mock_input):
        self.cli._opcion_agregar_medico()
        mock_print.assert_any_call("Advertencia: Día 'invalidday' no reconocido y será ignorado.")
        medico_arg = self.clinica_mock.agregar_medico.call_args[0][0]
        especialidades = medico_arg.obtener_especialidades()
        self.assertEqual(len(especialidades), 1)
        self.assertEqual(especialidades[0].obtener_especialidad(), "Time Travel")
        self.assertIn("domingo", especialidades[0].__dias__)
        self.assertNotIn("invalidday", especialidades[0].__dias__)

    @patch('builtins.input', side_effect=["Dr. NoDays", "MED000", "s", "No Work", "badday1,badday2", "n"])
    @patch('builtins.print')
    def test_opcion_agregar_medico_con_especialidad_sin_dias_validos(self, mock_print, mock_input):
        self.cli._opcion_agregar_medico()
        mock_print.assert_any_call("Advertencia: Día 'badday1' no reconocido y será ignorado.")
        mock_print.assert_any_call("Advertencia: Día 'badday2' no reconocido y será ignorado.")
        mock_print.assert_any_call("No se ingresaron días válidos para la especialidad. No se agregará.")
        medico_arg = self.clinica_mock.agregar_medico.call_args[0][0]
        self.assertEqual(len(medico_arg.obtener_especialidades()), 0) # Especialidad no se agregó

    @patch('builtins.input', side_effect=["Dr. Duplicate", "MED123", "n"])
    def test_opcion_agregar_medico_duplicado_raises_exception(self, mock_input):
        self.clinica_mock.agregar_medico.side_effect = MedicoDuplicadoException("Matrícula ya existe")
        with self.assertRaises(MedicoDuplicadoException):
            self.cli._opcion_agregar_medico()

    @patch('builtins.print')
    def test_opcion_listar_medicos_vacio(self, mock_print):
        self.clinica_mock.obtener_medicos.return_value = []
        self.cli._opcion_listar_medicos()
        mock_print.assert_any_call("No hay médicos registrados.")

    @patch('builtins.print')
    def test_opcion_listar_medicos_con_medicos(self, mock_print):
        self.clinica_mock.obtener_medicos.return_value = [self.medico1]
        self.cli._opcion_listar_medicos()
        mock_print.assert_any_call(f"- {self.medico1.obtener_nombre()} (Matrícula: {self.medico1.obtener_matricula()})")
        mock_print.assert_any_call(f"    Especialidades: [{str(self.especialidad1)}]")


    @patch('builtins.input', side_effect=["MAT001", "Pediatría", "jueves,viernes"])
    @patch('builtins.print')
    def test_opcion_agregar_especialidad_a_medico_exitoso(self, mock_print, mock_input):
        mock_medico_existente = MagicMock(spec=Medico)
        mock_medico_existente.obtener_nombre.return_value = "Dr. Lawrence Jacoby"
        self.clinica_mock.obtener_medico_por_matricula.return_value = mock_medico_existente

        self.cli._opcion_agregar_especialidad_a_medico()

        self.clinica_mock.obtener_medico_por_matricula.assert_called_once_with("MAT001")
        mock_medico_existente.agregar_especialidad.assert_called_once()
        especialidad_arg = mock_medico_existente.agregar_especialidad.call_args[0][0]
        self.assertIsInstance(especialidad_arg, Especialidad)
        self.assertEqual(especialidad_arg.obtener_especialidad(), "Pediatría")
        self.assertIn("jueves", especialidad_arg.__dias__)
        self.assertIn("viernes", especialidad_arg.__dias__)
        mock_print.assert_any_call("Especialidad 'Pediatría' agregada exitosamente al Dr./Dra. Dr. Lawrence Jacoby.")

    @patch('builtins.input', side_effect=["MAT001", "Neurología", "dia_malo,lunes"])
    @patch('builtins.print')
    def test_opcion_agregar_especialidad_a_medico_dias_invalidos(self, mock_print, mock_input):
        mock_medico_existente = MagicMock(spec=Medico)
        mock_medico_existente.obtener_nombre.return_value = "Dr. Lawrence Jacoby"
        mock_medico_existente.obtener_especialidades.return_value = []
        self.clinica_mock.obtener_medico_por_matricula.return_value = mock_medico_existente

        self.cli._opcion_agregar_especialidad_a_medico()

        mock_print.assert_any_call("Advertencia: Día 'dia_malo' no reconocido y será ignorado.")

        mock_medico_existente.agregar_especialidad.assert_called_once()
        especialidad_arg = mock_medico_existente.agregar_especialidad.call_args[0][0]

        self.assertIsInstance(especialidad_arg, Especialidad)
        self.assertEqual("Neurología", especialidad_arg.obtener_especialidad())
        self.assertIn("lunes", especialidad_arg.__dias__)
        self.assertNotIn("dia_malo", especialidad_arg.__dias__)
        self.assertEqual(1, len(especialidad_arg.__dias__))

    @patch('builtins.input', side_effect=["MAT001", "Dermatología", "invalid1,invalid2"])
    @patch('builtins.print')
    def test_opcion_agregar_especialidad_a_medico_sin_dias_validos(self, mock_print, mock_input):
        mock_medico_existente = MagicMock(spec=Medico)
        mock_medico_existente.obtener_nombre.return_value = "Dr. Lawrence Jacoby"
        self.clinica_mock.obtener_medico_por_matricula.return_value = mock_medico_existente

        self.cli._opcion_agregar_especialidad_a_medico()

        mock_print.assert_any_call("No se ingresaron días válidos para la especialidad. No se agregará.")
        mock_medico_existente.agregar_especialidad.assert_not_called()


    @patch('builtins.input', side_effect=["NONEXISTENT_MAT"])
    def test_opcion_agregar_especialidad_a_medico_no_encontrado_raises_exception(self, mock_input):
        self.clinica_mock.obtener_medico_por_matricula.side_effect = MedicoNoEncontradoException("Médico no existe")
        with self.assertRaises(MedicoNoEncontradoException):
            self.cli._opcion_agregar_especialidad_a_medico()


    @patch('builtins.input', side_effect=["12345678", "MED123", "2023-06-15 10:00", "Cardiología"])
    @patch('builtins.print')
    def test_opcion_agendar_turno(self, mock_print, mock_input):
        turno_mock = MagicMock(spec=Turno)
        turno_mock.__str__.return_value = "Detalles del turno mock"
        self.clinica_mock.agendar_turno.return_value = turno_mock

        self.cli._opcion_agendar_turno()

        self.clinica_mock.agendar_turno.assert_called_once_with(
            "12345678", "MED123", "2023-06-15 10:00", "Cardiología"
        )
        mock_print.assert_any_call("\n¡Turno agendado exitosamente!\n")
        mock_print.assert_any_call("Turno:\nDetalles del turno mock")

    @patch('builtins.input', side_effect=["12345678", "MED123", "2023-06-15 10:00", "Cardiología"])
    def test_opcion_agendar_turno_duplicado_raises_exception(self, mock_input):
        self.clinica_mock.agendar_turno.side_effect = TurnoOcupadoException("Turno ocupado")
        with self.assertRaises(TurnoOcupadoException):
            self.cli._opcion_agendar_turno()

    @patch('builtins.input', side_effect=["DNI_NO_EXISTE", "MED123", "2023-06-15 10:00", "Cardiología"])
    def test_opcion_agendar_turno_paciente_no_encontrado_raises_exception(self, mock_input):
        self.clinica_mock.agendar_turno.side_effect = PacienteNoEncontradoException("Paciente no existe")
        with self.assertRaises(PacienteNoEncontradoException):
            self.cli._opcion_agendar_turno()

    @patch('builtins.input', side_effect=["12345678", "MAT_NO_EXISTE", "2023-06-15 10:00", "Cardiología"])
    def test_opcion_agendar_turno_medico_no_encontrado_raises_exception(self, mock_input):
        self.clinica_mock.agendar_turno.side_effect = MedicoNoEncontradoException("Médico no existe")
        with self.assertRaises(MedicoNoEncontradoException):
            self.cli._opcion_agendar_turno()

    @patch('builtins.input', side_effect=["12345678", "MED123", "2023-06-15 10:00", "EspecialidadRara"])
    def test_opcion_agendar_turno_especialidad_no_valida_raises_exception(self, mock_input):
        self.clinica_mock.agendar_turno.side_effect = EspecialidadNoValidaParaDiaException("Especialidad no válida")
        with self.assertRaises(EspecialidadNoValidaParaDiaException):
            self.cli._opcion_agendar_turno()

    @patch('builtins.input', side_effect=["12345678", "MED123", "2023-06-15 10:00", "Cardiología"])
    def test_opcion_agendar_turno_medico_no_disponible_raises_exception(self, mock_input):
        self.clinica_mock.agendar_turno.side_effect = MedicoNoDisponibleException("Médico no disponible ese día")
        with self.assertRaises(MedicoNoDisponibleException):
            self.cli._opcion_agendar_turno()

    @patch('builtins.input', side_effect=["12345678", "MED123", "2000-01-01 10:00", "Cardiología"]) # Past date
    def test_opcion_agendar_turno_fecha_pasada_raises_exception(self, mock_input):
        # Assuming Clinica.agendar_turno raises ValueError for past dates
        self.clinica_mock.agendar_turno.side_effect = ValueError("No se pueden agendar turnos en el pasado.")
        with self.assertRaises(ValueError):
            self.cli._opcion_agendar_turno()

    @patch('builtins.input', side_effect=["12345678", "MED123", "FECHA_INVALIDA", "Cardiología"])
    def test_opcion_agendar_turno_fecha_formato_invalido_raises_exception(self, mock_input):
        # Assuming Clinica.agendar_turno raises ValueError for invalid format
        self.clinica_mock.agendar_turno.side_effect = ValueError("Formato de fecha y hora inválido.")
        with self.assertRaises(ValueError):
            self.cli._opcion_agendar_turno()


    @patch('builtins.print')
    def test_opcion_listar_turnos_vacio(self, mock_print):
        self.clinica_mock.obtener_turnos.return_value = []
        self.cli._opcion_listar_turnos()
        mock_print.assert_any_call("No hay turnos agendados.")

    @patch('builtins.print')
    def test_opcion_listar_turnos_con_turnos(self, mock_print):
        turno_mock = MagicMock(spec=Turno)
        turno_mock.__str__.return_value = "Detalles del Turno 1"
        self.clinica_mock.obtener_turnos.return_value = [turno_mock]
        self.cli._opcion_listar_turnos()
        mock_print.assert_any_call(turno_mock)


    @patch('builtins.input', side_effect=["12345678", "MED123", "Paracetamol", "Ibuprofeno", ""])
    @patch('builtins.print')
    def test_opcion_emitir_receta(self, mock_print, mock_input):
        receta_mock = MagicMock()
        receta_mock.__str__.return_value = "Detalles de la receta mock"
        self.clinica_mock.emitir_receta.return_value = receta_mock

        self.cli._opcion_emitir_receta()

        self.clinica_mock.emitir_receta.assert_called_once_with(
            "12345678", "MED123", ["Paracetamol", "Ibuprofeno"]
        )
        mock_print.assert_any_call("\n¡Receta emitida exitosamente!\n")
        mock_print.assert_any_call("Receta: Detalles de la receta mock")

    @patch('builtins.input', side_effect=["DNI_NO_EXISTE", "MED123", "Paracetamol", ""])
    def test_opcion_emitir_receta_paciente_no_encontrado_raises_exception(self, mock_input):
        self.clinica_mock.emitir_receta.side_effect = PacienteNoEncontradoException("Paciente no existe")
        with self.assertRaises(PacienteNoEncontradoException):
            self.cli._opcion_emitir_receta()

    @patch('builtins.input', side_effect=["12345678", "MAT_NO_EXISTE", "Paracetamol", ""])
    def test_opcion_emitir_receta_medico_no_encontrado_raises_exception(self, mock_input):
        self.clinica_mock.emitir_receta.side_effect = MedicoNoEncontradoException("Médico no existe")
        with self.assertRaises(MedicoNoEncontradoException):
            self.cli._opcion_emitir_receta()

    @patch('builtins.input', side_effect=["12345678", "MED123", ""]) # No medicamentos
    @patch('builtins.print')
    def test_opcion_emitir_receta_sin_medicamentos(self, mock_print, mock_input):
        self.cli._opcion_emitir_receta()
        mock_print.assert_any_call("No se ingresaron medicamentos. No se emitirá la receta.")
        self.clinica_mock.emitir_receta.assert_not_called()


    @patch('builtins.input', side_effect=["12345678"])
    @patch('builtins.print')
    def test_opcion_ver_historia_clinica(self, mock_print, mock_input):
        historia_mock = MagicMock()
        historia_mock.__str__.return_value = "Contenido de la historia clínica"
        self.clinica_mock.obtener_historia_clinica.return_value = historia_mock

        self.cli._opcion_ver_historia_clinica()

        self.clinica_mock.obtener_historia_clinica.assert_called_once_with("12345678")
        mock_print.assert_any_call(historia_mock)

    @patch('builtins.input', side_effect=["DNI_NO_EXISTE"])
    def test_opcion_ver_historia_clinica_paciente_no_encontrado_raises_exception(self, mock_input):
        self.clinica_mock.obtener_historia_clinica.side_effect = PacienteNoEncontradoException("Paciente no existe")
        with self.assertRaises(PacienteNoEncontradoException):
            self.cli._opcion_ver_historia_clinica()


if __name__ == '__main__':
    unittest.main()