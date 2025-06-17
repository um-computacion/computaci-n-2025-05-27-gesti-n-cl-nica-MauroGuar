import unittest
from datetime import datetime
from src.clinica_gestion.modelo.paciente import Paciente
from src.clinica_gestion.modelo.medico import Medico
from src.clinica_gestion.modelo.especialidad import Especialidad
from src.clinica_gestion.modelo.turno import Turno

class TestTurno(unittest.TestCase):

    def setUp(self):
        self.paciente = Paciente("Laura Palmer", "26777888", "10/07/1972")

        self.medico = Medico("Dr. Jacoby", "MAT90210")
        self.especialidad_psiquiatria = Especialidad("Psiquiatría", ["lunes", "miércoles", "viernes"])
        self.medico.agregar_especialidad(self.especialidad_psiquiatria)

        self.fecha_hora_turno_dt = datetime(2025, 11, 21, 10, 30) # Viernes
        self.fecha_hora_turno_str = "2025-11-21 10:30"

        self.turno = Turno(
            paciente=self.paciente,
            medico=self.medico,
            fecha_hora=self.fecha_hora_turno_dt,
            nombre_especialidad="Psiquiatría"
        )

    def test_creacion_turno_y_obtener_atributos(self):
        self.assertEqual(self.turno.obtener_paciente(), self.paciente)
        self.assertEqual(self.turno.obtener_medico(), self.medico)
        self.assertEqual(self.turno.obtener_fecha_hora(), self.fecha_hora_turno_dt)
        self.assertEqual(self.turno.obtener_especialidad_atendida(), "Psiquiatría")

    def test_representacion_str_turno(self):
        representacion = str(self.turno)
        self.assertTrue(representacion.startswith("Turno("))
        self.assertTrue(representacion.endswith(")"))

        self.assertIn(str(self.paciente), representacion)
        self.assertIn(str(self.medico), representacion)
        self.assertIn(str(self.fecha_hora_turno_dt), representacion)
        self.assertIn(self.turno.obtener_especialidad_atendida(), representacion)

        self.assertIn("\n", representacion)

    def test_turno_con_otra_fecha(self):
        fecha_hora_dt = datetime(2025, 12, 24, 16, 00)
        turno_navidad = Turno(self.paciente, self.medico, fecha_hora_dt, "Psiquiatría")
        self.assertEqual(turno_navidad.obtener_fecha_hora(), fecha_hora_dt)

if __name__ == '__main__':
    unittest.main()