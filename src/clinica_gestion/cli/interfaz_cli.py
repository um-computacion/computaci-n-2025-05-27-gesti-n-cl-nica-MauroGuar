from src.clinica_gestion.modelo.clinica import Clinica
from src.clinica_gestion.modelo.especialidad import Especialidad
from src.clinica_gestion.modelo.excepciones import ClinicaException

class CLI:
    def __init__(self, clinica: Clinica = Clinica()):
        self.__clinica__ = clinica

    def mostrar_menu_principal(self):
        print("\n--- Menú Clínica ---")
        print("1. Agregar Paciente")
        print("2. Agregar Médico")
        print("3. Agendar Turno")
        print("4. Agregar Especialidad a Médico Existente")
        print("5. Emitir Receta")
        print("6. Ver Historia Clínica de Paciente")
        print("7. Listar Turnos")
        print("8. Listar Pacientes")
        print("9. Listar Médicos")
        print("0. Salir")

    def iniciar(self):
        while True:
            self.mostrar_menu_principal()
            opcion = input("Seleccione una opción: ")

            try:
                if opcion == '1':
                    self._opcion_agregar_paciente()
                elif opcion == '2':
                    self._opcion_agregar_medico()
                elif opcion == '3':
                    self._opcion_agendar_turno()
                elif opcion == '4':
                    self._opcion_agregar_especialidad_a_medico()
                elif opcion == '5':
                    self._opcion_emitir_receta()
                elif opcion == '6':
                    self._opcion_ver_historia_clinica()
                elif opcion == '7':
                    self._opcion_listar_turnos()
                elif opcion == '8':
                    self._opcion_listar_pacientes()
                elif opcion == '9':
                    self._opcion_listar_medicos()
                elif opcion == '0':
                    print("¡Hasta luego!")
                    break
                else:
                    print("Opción no válida. Intente de nuevo.")
            except ClinicaException as e:
                print(f"Error de la clínica: {e}")
            except ValueError as e:
                print(f"Error de valor: {e}")
            except TypeError as e:
                print(f"Error de tipo: {e}")
            except Exception as e:
                print(f"Ha ocurrido un error inesperado: {e}")

            input("\nPresione Enter para continuar...")


    def _opcion_agregar_paciente(self):
        print("\n--- Agregar Nuevo Paciente ---")
        nombre = input("Nombre completo del paciente: ")
        dni = input("DNI del paciente (solo números): ")
        fecha_nacimiento = input("Fecha de nacimiento (DD/MM/AAAA): ")

        from src.clinica_gestion.modelo.paciente import Paciente
        nuevo_paciente = Paciente(nombre, dni, fecha_nacimiento)
        self.__clinica__.agregar_paciente(nuevo_paciente)
        print(f"Paciente {nombre} (DNI: {dni}) agregado exitosamente.")

    def _opcion_listar_pacientes(self):
        print("\n--- Listado de Pacientes ---")
        pacientes = self.__clinica__.obtener_pacientes()
        if not pacientes:
            print("No hay pacientes registrados.")
            return
        for p in pacientes:
            print(p)


    def _opcion_agregar_medico(self):
        print("\n--- Agregar Nuevo Médico ---")
        nombre = input("Nombre completo del médico: ")
        matricula = input("Matrícula del médico: ")

        from src.clinica_gestion.modelo.medico import Medico
        nuevo_medico = Medico(nombre, matricula)

        while True:
            agregar_esp = input("¿Desea agregar una especialidad a este médico? (s/n): ").lower()
            if agregar_esp != 's':
                break

            nombre_esp = input("Nombre de la especialidad: ")
            dias_str = input("Días de atención para esta especialidad (ej: lunes,martes,viernes): ")
            lista_dias = [dia.strip().lower() for dia in dias_str.split(',')]

            dias_validos = []
            for dia in lista_dias:
                if dia in Clinica.DIAS_SEMANA_ES: # Usamos la lista de Clinica
                    dias_validos.append(dia)
                else:
                    print(f"Advertencia: Día '{dia}' no reconocido y será ignorado.")

            if not dias_validos:
                print("No se ingresaron días válidos para la especialidad. No se agregará.")
                continue

            especialidad = Especialidad(nombre_esp, dias_validos)
            nuevo_medico.agregar_especialidad(especialidad)
            print(f"Especialidad '{nombre_esp}' agregada al Dr. {nombre}.")

        self.__clinica__.agregar_medico(nuevo_medico)
        print(f"Médico {nombre} (Matrícula: {matricula}) agregado exitosamente.")


    def _opcion_listar_medicos(self):
        print("\n--- Listado de Médicos ---")
        medicos = self.__clinica__.obtener_medicos()
        if not medicos:
            print("No hay médicos registrados.")
            return
        for m in medicos:
            print(f"- {m.obtener_nombre()} (Matrícula: {m.obtener_matricula()})")
            especialidades_medico = m.obtener_especialidades()
            if especialidades_medico:
                print(f"    Especialidades: {[str(esp) for esp in especialidades_medico]}".replace("'", ""))
            else:
                print("  Especialidades: Ninguna")


    def _opcion_agregar_especialidad_a_medico(self):
        print("\n--- Agregar Especialidad a Médico Existente ---")
        matricula = input("Ingrese la matrícula del médico: ")

        medico = self.__clinica__.obtener_medico_por_matricula(matricula) # Lanza excepción si no existe
        print(f"Médico encontrado: {medico.obtener_nombre()}")

        nombre_esp = input("Nombre de la nueva especialidad: ")
        dias_str = input("Días de atención para esta especialidad (ej: lunes,martes,viernes): ")
        lista_dias = [dia.strip().lower() for dia in dias_str.split(',')]

        dias_validos = []
        for dia in lista_dias:
            if dia in Clinica.DIAS_SEMANA_ES:
                dias_validos.append(dia)
            else:
                print(f"Advertencia: Día '{dia}' no reconocido y será ignorado.")

        if not dias_validos:
            print("No se ingresaron días válidos para la especialidad. No se agregará.")
            return

        especialidad = Especialidad(nombre_esp, dias_validos)
        medico.agregar_especialidad(especialidad)
        print(f"Especialidad '{nombre_esp}' agregada exitosamente al Dr./Dra. {medico.obtener_nombre()}.")


    def _opcion_agendar_turno(self):
        print("\n--- Agendar Nuevo Turno ---")
        dni_paciente = input("DNI del paciente: ")
        matricula_medico = input("Matrícula del médico: ")
        fecha_hora_str = input("Fecha y hora del turno (YYYY-MM-DD HH:MM): ")
        nombre_especialidad = input("Especialidad deseada para el turno: ")

        turno_agendado = self.__clinica__.agendar_turno(
            dni_paciente,
            matricula_medico,
            fecha_hora_str,
            nombre_especialidad
        )
        print("\n¡Turno agendado exitosamente!\n")
        print(f"Turno:\n{turno_agendado}")


    def _opcion_listar_turnos(self):
        print("\n--- Listado de Turnos Agendados ---")
        turnos = self.__clinica__.obtener_turnos()
        if not turnos:
            print("No hay turnos agendados.")
            return
        for t in turnos:
            print(t)


    def _opcion_emitir_receta(self):
        print("\n--- Emitir Nueva Receta ---")
        dni_paciente = input("DNI del paciente: ")
        matricula_medico = input("Matrícula del médico que emite: ")

        medicamentos = []
        print("Ingrese los medicamentos (deje vacío y presione Enter para finalizar):")
        while True:
            medicamento = input(f"Medicamento {len(medicamentos) + 1}: ")
            if not medicamento:
                break
            medicamentos.append(medicamento)

        if not medicamentos:
            print("No se ingresaron medicamentos. No se emitirá la receta.")
            return

        receta_emitida = self.__clinica__.emitir_receta(
            dni_paciente,
            matricula_medico,
            medicamentos
        )
        print("\n¡Receta emitida exitosamente!\n")
        print(f"Receta: {receta_emitida}")


    def _opcion_ver_historia_clinica(self):
        print("\n--- Ver Historia Clínica ---")
        dni_paciente = input("DNI del paciente: ")

        historia_clinica = self.__clinica__.obtener_historia_clinica(dni_paciente)
        print("\n------------------------------------")
        print(historia_clinica)
        print("------------------------------------")
