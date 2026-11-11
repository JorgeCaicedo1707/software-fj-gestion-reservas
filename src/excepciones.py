# -*- coding: utf-8 -*-
"""
Aquí se definen los errores propios de Software FJ. Todos parten de una
misma clase para poder reconocerlos en conjunto o manejar cada caso por separado.
"""


# ---------------------------------------------------------------------------
# 1. EXCEPCIÓN BASE
# ---------------------------------------------------------------------------
class SoftwareFJError(Exception):                      # Hereda de Exception para que Python la trate como un error normal
    """Error general del sistema, con un mensaje y un código identificador."""

    def __init__(self, mensaje, codigo="FJ-000"):      # Recibe el mensaje y un código (FJ-000 si nadie lo define)
        # La clase Exception conserva el mensaje para el manejo estándar de Python.
        super().__init__(mensaje)                      # Le pasamos el mensaje a la clase padre
        self.mensaje = mensaje                         # Guardamos el mensaje por si lo necesitamos aparte
        # El código ayuda a identificar y buscar este error en el registro.
        self.codigo = codigo                           # Guardamos el código del error

    def __str__(self):                                 # Define cómo se ve el error al imprimirlo
        return f"[{self.codigo}] {self.mensaje}"       # Queda así: [FJ-101] mensaje


# ---------------------------------------------------------------------------
# 2. ERRORES DE CLIENTE
# ---------------------------------------------------------------------------
class ClienteError(SoftwareFJError):                   # Familia de errores de clientes (hija del error base)
    """Clase que reúne los errores que pueden ocurrir con un cliente."""


class ClienteInvalidoError(ClienteError):              # Error para datos de cliente mal escritos
    """Se usa cuando alguno de los datos del cliente no cumple las reglas."""

    def __init__(self, mensaje):                       # Solo pide el mensaje, el código ya va fijo
        super().__init__(mensaje, codigo="FJ-101")     # Llama al padre con el código FJ-101


class ClienteNoEncontradoError(ClienteError):          # Error para cuando el cliente no existe
    """Indica que no se encontró el cliente solicitado."""

    def __init__(self, mensaje):                       # Solo pide el mensaje
        super().__init__(mensaje, codigo="FJ-102")     # Código fijo FJ-102


# ---------------------------------------------------------------------------
# 3. ERRORES DE SERVICIO
# ---------------------------------------------------------------------------
class ServicioError(SoftwareFJError):                  # Familia de errores de servicios
    """Clase que reúne los errores relacionados con los servicios."""


class ServicioInvalidoError(ServicioError):            # Error para datos de servicio incorrectos
    """Se presenta cuando los datos de un servicio no son válidos."""

    def __init__(self, mensaje):                       # Solo pide el mensaje
        super().__init__(mensaje, codigo="FJ-201")     # Código fijo FJ-201


class ServicioNoDisponibleError(ServicioError):        # Error para servicios desactivados
    """Señala que el servicio no está disponible para la reserva."""

    def __init__(self, mensaje):                       # Solo pide el mensaje
        super().__init__(mensaje, codigo="FJ-202")     # Código fijo FJ-202


# ---------------------------------------------------------------------------
# 4. ERRORES DE RESERVA
# ---------------------------------------------------------------------------
class ReservaError(SoftwareFJError):                   # Familia de errores de reservas
    """Clase que reúne los errores que pueden ocurrir con una reserva."""


class ReservaInvalidaError(ReservaError):              # Error para reservas con datos malos
    """Se usa cuando la información necesaria para una reserva no es válida."""

    def __init__(self, mensaje):                       # Solo pide el mensaje
        super().__init__(mensaje, codigo="FJ-301")     # Código fijo FJ-301


class OperacionNoPermitidaError(ReservaError):         # Error para acciones que el estado actual no deja hacer
    """Indica que la reserva no permite realizar la operación solicitada."""

    def __init__(self, mensaje):                       # Solo pide el mensaje
        super().__init__(mensaje, codigo="FJ-302")     # Código fijo FJ-302


# ---------------------------------------------------------------------------
# 5. ERRORES DE CÁLCULO
# ---------------------------------------------------------------------------
class CalculoError(SoftwareFJError):                   # Error para cuando un cálculo no da un resultado válido
    """Se presenta cuando no es posible obtener un cálculo válido."""

    def __init__(self, mensaje):                       # Solo pide el mensaje
        super().__init__(mensaje, codigo="FJ-401")     # Código fijo FJ-401


# ---------------------------------------------------------------------------
# 6. PRUEBA RÁPIDA DEL MÓDULO (solo se ejecuta si corres este archivo directamente)
# ---------------------------------------------------------------------------
if __name__ == "__main__":                             # Solo corre si ejecutamos este archivo solo, no al importarlo

    # --- Prueba A: try / except / else / finally ---
    try:                                               # Intentamos algo que sabemos que va a fallar
        # Se genera un error de prueba para revisar la jerarquía.
        raise ClienteInvalidoError("El correo 'abc' no tiene formato válido")  # Lanzamos el error a propósito
    except ClienteError as error:                      # Lo atrapamos con la clase padre (ClienteError)
        print("Capturado:", error)                     # Mostramos el error con su código
    else:
        # Este bloque solo se ejecutaría si el try terminara sin errores.
        print("Sin errores")                           # Aquí no entra porque sí hubo error
    finally:
        # Este bloque siempre se ejecuta, incluso cuando ocurre una excepción.
        print("Fin de la prueba A")                    # Esto siempre se imprime

    # --- Prueba B: encadenamiento con raise ... from ---
    try:                                               # Try de afuera: atrapa el error que nosotros creamos
        try:                                           # Try de adentro: atrapa el error original de Python
            # Se genera un error original que luego se convierte en CalculoError.
            costo = 100 / 0                            # Esto da ZeroDivisionError
        except ZeroDivisionError as original:          # Guardamos el error original en la variable "original"
            raise CalculoError("No se pudo calcular el costo de la reserva") from original  # Lanzamos el nuestro sin perder el original
    except SoftwareFJError as error:                   # Lo atrapamos con el error base del sistema
        print("Capturado:", error)                     # Mostramos el error nuestro
        # __cause__ permite consultar el error que inició el problema.
        print("Causa original:", repr(error.__cause__))  # Mostramos el error original que quedó encadenado
