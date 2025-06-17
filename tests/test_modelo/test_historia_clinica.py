import unittest
from datetime import datetime
from src.clinica_gestion.modelo.paciente import Paciente
from src.clinica_gestion.modelo.medico import Medico
from src.clinica_gestion.modelo.especialidad import Especialidad
from src.clinica_gestion.modelo.turno import Turno
from src.clinica_gestion.modelo.receta import Receta
from src.clinica_gestion.modelo.historia_clinica import HistoriaClinica

class TestHistoriaClinica(unittest.TestCase):

    def setUp(self):
        self.paciente_hc = Paciente("Audrey Horne", "33445566", "01/12/1973")
        self.historia_clinica = HistoriaClinica(self.paciente_hc)

        self.medico1 = Medico("Dr. Albert Rosenfield", "MATFBI1")
        self.medico1.agregar_especialidad(Especialidad("Forense", ["lunes"]))

        self.medico2 = Medico("Dr. Will Hayward", "MAT002")
        self.medico2.agregar_especialidad(Especialidad("Clínica Médica", ["martes"]))

        self.turno1_dt = datetime(2025, 10, 6, 9, 0) # Lunes
        self.turno1 = Turno(self.paciente_hc, self.medico1, self.turno1_dt, "Forense")

        self.turno2_dt = datetime(2025, 10, 7, 11, 0) # Martes
        self.turno2 = Turno(self.paciente_hc, self.medico2, self.turno2_dt, "Clínica Médica")

        self.receta1 = Receta(self.paciente_hc, self.medico2, "Analgésicos")
        self.receta2 = Receta(self.paciente_hc, self.medico1, "Antibióticos")

    def test_creacion_historia_clinica(self):
        self.assertTrue(self.historia_clinica.__paciente__ is not None)
        self.assertEqual(len(self.historia_clinica.obtener_turnos()), 0)
        self.assertEqual(len(self.historia_clinica.obtener_recetas()), 0)

    def test_agregar_y_obtener_turnos(self):
        self.historia_clinica.agregar_turno(self.turno2)
        self.historia_clinica.agregar_turno(self.turno1)

        turnos = self.historia_clinica.obtener_turnos()
        self.assertEqual(len(turnos), 2)

    def test_obtener_turnos_devuelve_copia(self):
        self.historia_clinica.agregar_turno(self.turno1)
        turnos1 = self.historia_clinica.obtener_turnos()
        turnos1.append(self.turno2)

        turnos2 = self.historia_clinica.obtener_turnos()
        self.assertEqual(len(turnos2), 1)

    def test_agregar_y_obtener_recetas(self):
        self.historia_clinica.agregar_receta(self.receta1)
        self.historia_clinica.agregar_receta(self.receta2)

        recetas = self.historia_clinica.obtener_recetas()
        self.assertEqual(len(recetas), 2)

    def test_obtener_recetas_devuelve_copia(self):
        self.historia_clinica.agregar_receta(self.receta1)
        recetas1 = self.historia_clinica.obtener_recetas()
        receta_extra = Receta(self.paciente_hc, self.medico1, "Extra")
        recetas1.append(receta_extra)

        recetas2 = self.historia_clinica.obtener_recetas()
        self.assertEqual(len(recetas2), 1)

    def test_representacion_str_historia_clinica(self):
        self.historia_clinica.agregar_turno(self.turno1)
        self.historia_clinica.agregar_receta(self.receta1)

        representacion = str(self.historia_clinica)

        self.assertTrue(representacion.startswith("HistoriaClinica("))
        self.assertTrue(representacion.endswith(")"))

        self.assertIn(str(self.paciente_hc), representacion)

        self.assertIn("\n", representacion)
