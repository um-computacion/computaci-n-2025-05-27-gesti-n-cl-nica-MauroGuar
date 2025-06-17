class ClinicaException(Exception):
    """Clase base para excepciones de la clínica."""
    pass

class PacienteDuplicadoException(ClinicaException):
    """Excepción para cuando se intenta agregar un paciente con un DNI ya existente."""
    pass

class PacienteNoEncontradoException(ClinicaException):
    """Excepción para cuando no se encuentra un paciente con un DNI específico."""
    pass

class MedicoDuplicadoException(ClinicaException):
    """Excepción para cuando se intenta agregar un médico con una matrícula ya existente."""
    pass

class MedicoNoEncontradoException(ClinicaException):
    """Excepción para cuando no se encuentra un médico con una matrícula específica."""
    pass

class MedicoNoDisponibleException(ClinicaException):
    """Excepción para cuando un médico no está disponible en la fecha/hora solicitada."""
    pass

class TurnoOcupadoException(ClinicaException):
    """Excepción para cuando se intenta agendar un turno en un horario ya ocupado para el médico."""
    pass

class EspecialidadNoValidaParaDiaException(ClinicaException):
    """Excepción para cuando la especialidad del médico no es válida para el día solicitado."""
    pass

class RecetaInvalidaException(ClinicaException):
    """Excepción para errores relacionados con la emisión o validación de recetas."""
    pass
