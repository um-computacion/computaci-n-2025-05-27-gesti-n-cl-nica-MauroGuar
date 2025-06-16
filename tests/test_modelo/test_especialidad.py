import unittest
from src.clinica_gestion.modelo.especialidad import Especialidad

class TestEspecialidad(unittest.TestCase):

    def test_creacion_especialidad_y_obtener_nombre(self):
        especialidad = Especialidad("Cardiología", ["lunes", "miércoles"])
        self.assertEqual(especialidad.obtener_especialidad(), "Cardiología", "El nombre de la especialidad no es correcto.")

    def test_verificar_dia_atiende_sensible_mayusculas_minusculas(self):
        especialidad = Especialidad("Pediatría", ["martes", "jueves"])
        self.assertTrue(especialidad.verificar_dia("martes"), "Debería atender los martes.")
        self.assertTrue(especialidad.verificar_dia("Martes"), "Debería atender los Martes (insensible a mayúsculas).")
        self.assertTrue(especialidad.verificar_dia("JUEVES"), "Debería atender los JUEVES (insensible a mayúsculas).")

    def test_verificar_dia_no_atiende(self):
        especialidad = Especialidad("Dermatología", ["viernes"])
        self.assertFalse(especialidad.verificar_dia("lunes"), "No debería atender los lunes.")

    def test_verificar_dia_lista_dias_vacia(self):
        especialidad = Especialidad("Oftalmología", [])
        self.assertFalse(especialidad.verificar_dia("lunes"), "No debería atender ningún día si la lista está vacía.")

    def test_representacion_str_especialidad_con_dias(self):
        especialidad = Especialidad("Traumatología", ["lunes", "viernes"])
        self.assertEqual(str(especialidad), "Traumatología (Días: lunes, viernes)", "La representación str no es la esperada.")

    def test_representacion_str_especialidad_sin_dias(self):
        especialidad = Especialidad("Nutrición", [])
        self.assertEqual(str(especialidad), "Nutrición (Días: )", "La representación str para sin días no es la esperada.")

    def test_representacion_str_especialidad_un_dia(self):
        especialidad = Especialidad("Kinesiología", ["miércoles"])
        self.assertEqual(str(especialidad), "Kinesiología (Días: miércoles)", "La representación str para un día no es la esperada.")
