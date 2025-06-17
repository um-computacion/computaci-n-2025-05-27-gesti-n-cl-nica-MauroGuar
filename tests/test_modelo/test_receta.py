import unittest
from datetime import datetime
from src.clinica_gestion.modelo.paciente import Paciente
from src.clinica_gestion.modelo.medico import Medico
from src.clinica_gestion.modelo.especialidad import Especialidad
from src.clinica_gestion.modelo.receta import Receta

class TestReceta(unittest.TestCase):
    def setUp(self):
        self.paciente = Paciente("Laura Palmer", "26777888", "10/07/1972")

        self.medico = Medico("Dr. Jacoby", "MAT90210")
        self.especialidad_psiquiatria = Especialidad("Psiquiatría", ["lunes", "miércoles", "viernes"])
        self.medico.agregar_especialidad(self.especialidad_psiquiatria)

        self.medicamentos = ["Alprazolam 0.5mg", "Sertralina 50mg"]

        self.fecha = datetime(2025, 11, 21, 10, 30)

        self.receta = Receta(
            paciente=self.paciente,
            medico=self.medico,
            medicamentos=self.medicamentos,
            fecha=self.fecha
        )

    def test_representacion_str_receta(self):
        representacion = str(self.receta)

        self.assertTrue(representacion.startswith("Receta("))
        self.assertTrue(representacion.endswith(")"))

        self.assertIn(str(self.paciente), representacion)
        self.assertIn(str(self.medico), representacion)

        for medicamento in self.medicamentos:
            self.assertIn(medicamento, representacion)

        self.assertIn(str(self.fecha), representacion)

        self.assertIn("\n", representacion)

if __name__ == '__main__':
    unittest.main()
