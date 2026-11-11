# -*- coding: utf-8 -*-
"""
Aquí se definen los errores propios de Software FJ. Todos parten de una
misma clase para poder reconocerlos en conjunto o manejar cada caso por separado.
"""


# ---------------------------------------------------------------------------
# 1. EXCEPCIÓN BASE
# ---------------------------------------------------------------------------
class SoftwareFJError(Exception):
    """Error general del sistema, con un mensaje y un código identificador."""

    def __init__(self, mensaje, codigo="FJ-000"):
        # La clase Exception conserva el mensaje para el manejo estándar de Python.
        super().__init__(mensaje)
        self.mensaje = mensaje
        # El código ayuda a identificar y buscar este error en el registro.
        self.codigo = codigo

    def __str__(self):
        return f"[{self.codigo}] {self.mensaje}"


# ---------------------------------------------------------------------------
# 2. ERRORES DE CLIENTE
# ---------------------------------------------------------------------------
class ClienteError(SoftwareFJError):
    """Clase que reúne los errores que pueden ocurrir con un cliente."""


class ClienteInvalidoError(ClienteError):
    """Se usa cuando alguno de los datos del cliente no cumple las reglas."""

    def __init__(self, mensaje):
        super().__init__(mensaje, codigo="FJ-101")


class ClienteNoEncontradoError(ClienteError):
    """Indica que no se encontró el cliente solicitado."""

    def __init__(self, mensaje):
        super().__init__(mensaje, codigo="FJ-102")


# ---------------------------------------------------------------------------
# 3. ERRORES DE SERVICIO
# ---------------------------------------------------------------------------
class ServicioError(SoftwareFJError):
    """Clase que reúne los errores relacionados con los servicios."""


class ServicioInvalidoError(ServicioError):
    """Se presenta cuando los datos de un servicio no son válidos."""

    def __init__(self, mensaje):
        super().__init__(mensaje, codigo="FJ-201")


class ServicioNoDisponibleError(ServicioError):
    """Señala que el servicio no está disponible para la reserva."""

    def __init__(self, mensaje):
        super().__init__(mensaje, codigo="FJ-202")


# ---------------------------------------------------------------------------
# 4. ERRORES DE RESERVA
# ---------------------------------------------------------------------------
class ReservaError(SoftwareFJError):
    """Clase que reúne los errores que pueden ocurrir con una reserva."""


class ReservaInvalidaError(ReservaError):
    """Se usa cuando la información necesaria para una reserva no es válida."""

    def __init__(self, mensaje):
        super().__init__(mensaje, codigo="FJ-301")


class OperacionNoPermitidaError(ReservaError):
    """Indica que la reserva no permite realizar la operación solicitada."""

    def __init__(self, mensaje):
        super().__init__(mensaje, codigo="FJ-302")


# ---------------------------------------------------------------------------
# 5. ERRORES DE CÁLCULO
# ---------------------------------------------------------------------------
class CalculoError(SoftwareFJError):
    """Se presenta cuando no es posible obtener un cálculo válido."""

    def __init__(self, mensaje):
        super().__init__(mensaje, codigo="FJ-401")


# ---------------------------------------------------------------------------
# 6. PRUEBA RÁPIDA DEL MÓDULO (solo se ejecuta si corres este archivo directamente)
# ---------------------------------------------------------------------------
if __name__ == "__main__":

    # --- Prueba A: try / except / else / finally ---
    try:
        # Se genera un error de prueba para revisar la jerarquía.
        raise ClienteInvalidoError("El correo 'abc' no tiene formato válido")
    except ClienteError as error:
        print("Capturado:", error)
    else:
        # Este bloque solo se ejecutaría si el try terminara sin errores.
        print("Sin errores")
    finally:
        # Este bloque siempre se ejecuta, incluso cuando ocurre una excepción.
        print("Fin de la prueba A")

    # --- Prueba B: encadenamiento con raise ... from ---
    try:
        try:
            # Se genera un error original que luego se convierte en CalculoError.
            costo = 100 / 0
        except ZeroDivisionError as original:
            raise CalculoError("No se pudo calcular el costo de la reserva") from original
    except SoftwareFJError as error:
        print("Capturado:", error)
        # __cause__ permite consultar el error que inició el problema.
        print("Causa original:", repr(error.__cause__))
