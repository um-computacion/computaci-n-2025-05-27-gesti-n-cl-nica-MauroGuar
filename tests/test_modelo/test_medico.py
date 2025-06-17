import unittest
from src.clinica_gestion.modelo.medico import Medico
from src.clinica_gestion.modelo.especialidad import Especialidad

class TestMedico(unittest.TestCase):

    def test_creacion_medico_y_obtener_matricula(self):
        medico = Medico("Dr. Carlos Casas", "MAT123")
        self.assertEqual(medico.obtener_matricula(), "MAT123")

    def test_obtener_nombre(self):
        medico = Medico("Dr. Carlos Casas", "MAT123")
        self.assertEqual(medico.obtener_nombre(), "Dr. Carlos Casas")

    def test_obtener_matricula(self):
        medico = Medico("Dr. Mario Mendez", "MAT999")
        self.assertEqual(medico.obtener_matricula(), "MAT999")

    def test_obtener_especialidad(self):
        medico = Medico("Dr. Mario Mendez", "MAT999")
        especialidad_cardio = Especialidad("Cardiología", ["lunes", "miércoles"])
        especialidad_pedia = Especialidad("Pediatría", ["martes", "jueves"])
        medico.agregar_especialidad(especialidad_cardio)
        medico.agregar_especialidad(especialidad_pedia)
        self.assertIn(especialidad_cardio, medico.obtener_especialidades())
        self.assertIn(especialidad_pedia, medico.obtener_especialidades())


    def test_agregar_una_especialidad(self):
        medico = Medico("Dra. Ana Allen", "MAT456")
        especialidad_cardio = Especialidad("Cardiología", ["lunes", "miércoles"])
        medico.agregar_especialidad(especialidad_cardio)
        especialidades = medico.obtener_especialidades_para_dia("lunes")
        self.assertEqual(len(especialidades), 1)
        self.assertEqual(especialidades[0], "Cardiología")

    def test_agregar_multiples_especialidades(self):
        medico = Medico("Dr. Luis Luna", "MAT789")
        especialidad_pedia = Especialidad("Pediatría", ["martes", "jueves"])
        especialidad_derma = Especialidad("Dermatología", ["viernes"])
        medico.agregar_especialidad(especialidad_pedia)
        medico.agregar_especialidad(especialidad_derma)

        especialidades_martes = medico.obtener_especialidades_para_dia("martes")
        self.assertEqual(len(especialidades_martes), 1)
        self.assertEqual(especialidades_martes[0], "Pediatría")

        especialidades_viernes = medico.obtener_especialidades_para_dia("viernes")
        self.assertEqual(len(especialidades_viernes), 1)
        self.assertEqual(especialidades_viernes[0], "Dermatología")

    def test_obtener_especialidades_para_dia_disponible(self):
        medico = Medico("Dra. Laura Lee", "MAT101")
        especialidad_neuro = Especialidad("Neurología", ["lunes", "jueves"])
        medico.agregar_especialidad(especialidad_neuro)
        especialidades = medico.obtener_especialidades_para_dia("LUNES")
        self.assertEqual(len(especialidades), 1)
        self.assertEqual(especialidades[0], "Neurología")

    def test_obtener_especialidades_para_dia_no_disponible(self):
        medico = Medico("Dr. Pedro Paz", "MAT112")
        especialidad_trauma = Especialidad("Traumatología", ["miércoles"])
        medico.agregar_especialidad(especialidad_trauma)
        especialidades = medico.obtener_especialidades_para_dia("martes")
        self.assertEqual(especialidades, [])

    def test_obtener_especialidades_para_dia_sin_especialidades(self):
        medico = Medico("Dra. Sara Sol", "MAT113")
        especialidades = medico.obtener_especialidades_para_dia("lunes")
        self.assertEqual(especialidades, [])

    def test_obtener_especialidades_para_dia_multiples_especialidades_mismo_dia(self):
        medico = Medico("Dr. Max Power", "MAT007")
        especialidad_general = Especialidad("Medicina General", ["lunes", "martes"])
        especialidad_deportes = Especialidad("Medicina Deportiva", ["lunes", "miércoles"])
        medico.agregar_especialidad(especialidad_general)
        medico.agregar_especialidad(especialidad_deportes)
        especialidades = medico.obtener_especialidades_para_dia("lunes")
        self.assertEqual(len(especialidades), 2)
        self.assertIn("Medicina General", especialidades)
        self.assertIn("Medicina Deportiva", especialidades)

    def test_representacion_str_medico_sin_especialidades(self):
        medico = Medico("Dr. Hugo Huesos", "MAT221")
        self.assertEqual(str(medico), "Medico: Dr. Hugo Huesos, MAT221, Especialidades: Ninguna")

    def test_representacion_str_medico_con_una_especialidad(self):
        medico = Medico("Dra. Irene Irizarry", "MAT332")
        especialidad_endo = Especialidad("Endocrinología", ["martes", "viernes"])
        medico.agregar_especialidad(especialidad_endo)
        esperado = "Medico: Dra. Irene Irizarry, MAT332, Especialidades: [Endocrinología (Días: martes, viernes)]"
        self.assertEqual(str(medico), esperado)

    def test_representacion_str_medico_con_multiples_especialidades(self):
        medico = Medico("Dr. Jorge Jaramillo", "MAT443")
        especialidad1 = Especialidad("Oftalmología", ["lunes"])
        especialidad2 = Especialidad("Otorrinolaringología", ["jueves", "viernes"])
        medico.agregar_especialidad(especialidad1)
        medico.agregar_especialidad(especialidad2)
        esperado = "Medico: Dr. Jorge Jaramillo, MAT443, Especialidades: [Oftalmología (Días: lunes), Otorrinolaringología (Días: jueves, viernes)]"
        self.assertEqual(str(medico), esperado)
