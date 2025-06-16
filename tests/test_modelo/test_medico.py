import unittest
from src.clinica_gestion.modelo.medico import Medico
from src.clinica_gestion.modelo.especialidad import Especialidad

class TestMedico(unittest.TestCase):

    def test_creacion_medico_y_obtener_matricula(self):
        medico = Medico("Dr. Carlos Casas", "MAT123")
        self.assertEqual(medico.obtener_matricula(), "MAT123")

    def test_agregar_una_especialidad(self):
        medico = Medico("Dra. Ana Allen", "MAT456")
        especialidad_cardio = Especialidad("Cardiología", ["lunes", "miércoles"])
        medico.agregar_especialidad(especialidad_cardio)
        self.assertEqual(medico.obtener_especialidad_para_dia("lunes"), "Cardiología")

    def test_agregar_multiples_especialidades(self):
        medico = Medico("Dr. Luis Luna", "MAT789")
        especialidad_pedia = Especialidad("Pediatría", ["martes", "jueves"])
        especialidad_derma = Especialidad("Dermatología", ["viernes"])
        medico.agregar_especialidad(especialidad_pedia)
        medico.agregar_especialidad(especialidad_derma)
        self.assertEqual(medico.obtener_especialidad_para_dia("martes"), "Pediatría")
        self.assertEqual(medico.obtener_especialidad_para_dia("viernes"), "Dermatología")

    def test_obtener_especialidad_para_dia_disponible(self):
        medico = Medico("Dra. Laura Lee", "MAT101")
        especialidad_neuro = Especialidad("Neurología", ["lunes", "jueves"])
        medico.agregar_especialidad(especialidad_neuro)
        self.assertEqual(medico.obtener_especialidad_para_dia("LUNES"), "Neurología")

    def test_obtener_especialidad_para_dia_no_disponible(self):
        medico = Medico("Dr. Pedro Paz", "MAT112")
        especialidad_trauma = Especialidad("Traumatología", ["miércoles"])
        medico.agregar_especialidad(especialidad_trauma)
        self.assertIsNone(medico.obtener_especialidad_para_dia("martes"))

    def test_obtener_especialidad_para_dia_sin_especialidades(self):
        medico = Medico("Dra. Sara Sol", "MAT113")
        self.assertIsNone(medico.obtener_especialidad_para_dia("lunes"))

    def test_obtener_especialidad_para_dia_multiples_especialidades_mismo_dia_devuelve_primera(self):
        medico = Medico("Dr. Max Power", "MAT007")
        especialidad_general = Especialidad("Medicina General", ["lunes", "martes"])
        especialidad_deportes = Especialidad("Medicina Deportiva", ["lunes", "miércoles"])
        medico.agregar_especialidad(especialidad_general)
        medico.agregar_especialidad(especialidad_deportes)
        self.assertEqual(medico.obtener_especialidad_para_dia("lunes"), "Medicina General")


    def test_representacion_str_medico_sin_especialidades(self):
        medico = Medico("Dr. Hugo Huesos", "MAT221")
        self.assertEqual(str(medico), "Medico: Dr. Hugo Huesos, Matrícula: MAT221, Especialidades: Ninguna")

    def test_representacion_str_medico_con_una_especialidad(self):
        medico = Medico("Dra. Irene Irizarry", "MAT332")
        especialidad_endo = Especialidad("Endocrinología", ["martes", "viernes"])
        medico.agregar_especialidad(especialidad_endo)
        esperado = "Medico: Dra. Irene Irizarry, Matrícula: MAT332, Especialidades: [Endocrinología (Días: martes, viernes)]"
        self.assertEqual(str(medico), esperado)

    def test_representacion_str_medico_con_multiples_especialidades(self):
        medico = Medico("Dr. Jorge Jaramillo", "MAT443")
        especialidad1 = Especialidad("Oftalmología", ["lunes"])
        especialidad2 = Especialidad("Otorrinolaringología", ["jueves", "viernes"])
        medico.agregar_especialidad(especialidad1)
        medico.agregar_especialidad(especialidad2)
        esperado = "Medico: Dr. Jorge Jaramillo, Matrícula: MAT443, Especialidades: [Oftalmología (Días: lunes), Otorrinolaringología (Días: jueves, viernes)]"
        self.assertEqual(str(medico), esperado)
