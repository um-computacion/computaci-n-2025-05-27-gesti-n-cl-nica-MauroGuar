import unittest
from src.clinica_gestion.modelo.paciente import Paciente

class TestPaciente(unittest.TestCase):

    def test_creacion_paciente_y_obtener_dni_y_nombre(self):
        paciente = Paciente("Juan Perez", "12345678", "01/01/1990")
        self.assertEqual(paciente.obtener_dni(), "12345678")
        self.assertEqual(paciente.obtener_nombre(), "Juan Perez")

    def test_representacion_str_paciente(self):
        paciente = Paciente("Ana Lopez", "87654321", "15/05/1985")
        self.assertEqual(str(paciente), "Ana Lopez, 87654321, 15/05/1985")

    def test_creacion_paciente_con_datos_diferentes(self):
        paciente = Paciente("Carlos Solari", "11223344", "10/10/2000")
        self.assertEqual(paciente.obtener_dni(), "11223344")
        self.assertEqual(str(paciente), "Carlos Solari, 11223344, 10/10/2000")
