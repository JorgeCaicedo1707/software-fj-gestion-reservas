"""
reserva.py
Sistema Integral de Gestión de Clientes, Servicios y Reservas - Software FJ
Curso Programación 213023 - Grupo 213023_333
Responsable del módulo: Ronaldo Hoyos Acevedo (GitHub: Ronyhoyos30)

Contenido del módulo:
    - Reserva : une un Cliente con un Servicio durante una duración y controla su estado.
                Estados: PENDIENTE -> CONFIRMADA -> PROCESADA, o CANCELADA.
"""

# =====================================================================
# DEPENDENCIAS DEL GRUPO
# =====================================================================

from entidad import Entidad                             # Clase abstracta base (Jorge)
from cliente import Cliente                             # Clase Cliente (Jorge)
from servicios import Servicio                          # Clase abstracta Servicio (Ronaldo)
from excepciones import (                               # Excepciones personalizadas (Jorge)
    ServicioInvalidoError,                              # FJ-201: parámetro del servicio inválido
    ServicioNoDisponibleError,                          # FJ-202: servicio desactivado
    CalculoError,                                       # FJ-401: costo inconsistente
    ReservaInvalidaError,                               # FJ-301: datos de la reserva no válidos
    OperacionNoPermitidaError,                          # FJ-302: acción no permitida en el estado actual
)
from logger import registrar_evento, registrar_error    # Registro en logs/software_fj.log (Jorge)


# =====================================================================
# CLASE RESERVA
# =====================================================================

class Reserva(Entidad):
    """
    Reserva de un servicio por parte de un cliente.
    Integra Cliente + Servicio + duración + estado, y controla las transiciones de estado.
    """

    # Constantes de estado: evitan errores de escritura al comparar textos
    PENDIENTE = "PENDIENTE"                             # Recién creada, aún no confirmada
    CONFIRMADA = "CONFIRMADA"                           # Verificada: servicio disponible
    PROCESADA = "PROCESADA"                             # Cobrada: costo final calculado
    CANCELADA = "CANCELADA"                             # Anulada: ya no admite más operaciones

    def __init__(self, cliente, servicio, duracion):
        if not isinstance(cliente, Cliente):            # Debe recibirse un objeto Cliente real
            raise ReservaInvalidaError(f"Se esperaba un Cliente y se recibió {type(cliente).__name__}.")
        if not isinstance(servicio, Servicio):          # Debe recibirse un objeto Servicio real
            raise ReservaInvalidaError(f"Se esperaba un Servicio y se recibió {type(servicio).__name__}.")
        try:
            duracion = servicio.validar_parametros(duracion)  # Cada servicio valida su duración (polimorfismo)
        except ServicioInvalidoError as error:          # Si la duración no sirve para ese servicio...
            # ENCADENAMIENTO: el error del servicio se convierte en error de la reserva, sin perder la causa
            raise ReservaInvalidaError(f"Duración no válida para '{servicio.nombre}'.") from error
        super().__init__()                              # Solo si todo es válido se asigna un id (Entidad)
        self._cliente = cliente                         # Cliente que hace la reserva
        self._servicio = servicio                       # Servicio reservado
        self._duracion = duracion                       # Duración ya validada
        self._estado = Reserva.PENDIENTE                # Toda reserva nace pendiente
        self._costo_final = None                        # Se conoce solo al procesar
        registrar_evento(f"Reserva #{self.id} creada: {cliente.nombre} -> {servicio.nombre}")  # Evento al log

    # ----------------- Encapsulación: solo lectura -----------------

    @property
    def cliente(self):                                  # Cliente asociado
        return self._cliente

    @property
    def servicio(self):                                 # Servicio asociado
        return self._servicio

    @property
    def duracion(self):                                 # Duración validada
        return self._duracion

    @property
    def estado(self):                                   # Estado actual: no se puede asignar desde fuera
        return self._estado

    @property
    def costo_final(self):                              # Costo después de procesar (None si no se ha procesado)
        return self._costo_final

    # ----------------- Operaciones de la reserva -----------------

    def confirmar(self):
        """PENDIENTE -> CONFIRMADA. Usa try/except/else."""
        if self._estado != Reserva.PENDIENTE:           # Solo se confirma lo que está pendiente
            raise OperacionNoPermitidaError(
                f"No se puede confirmar la reserva #{self.id}: estado {self._estado}.")
        try:
            self._servicio.verificar_disponibilidad()   # ¿El servicio sigue activo?
        except ServicioNoDisponibleError as error:      # Si no lo está...
            # ENCADENAMIENTO: se informa a nivel de reserva conservando la causa
            raise OperacionNoPermitidaError(f"No se pudo confirmar la reserva #{self.id}.") from error
        else:                                           # Solo si NO hubo excepción en el try
            self._estado = Reserva.CONFIRMADA           # Cambia el estado
            registrar_evento(f"Reserva #{self.id} confirmada.")

    def cancelar(self):
        """PENDIENTE o CONFIRMADA -> CANCELADA."""
        if self._estado in (Reserva.CANCELADA, Reserva.PROCESADA):  # No se cancela lo ya cerrado
            raise OperacionNoPermitidaError(
                f"No se puede cancelar la reserva #{self.id}: estado {self._estado}.")
        self._estado = Reserva.CANCELADA                # Cambia el estado
        registrar_evento(f"Reserva #{self.id} cancelada.")

    def procesar(self, impuesto=0.0, descuento=0.0):
        """
        CONFIRMADA -> PROCESADA. Calcula y fija el costo final.
        Usa try/except/else/finally y encadenamiento de excepciones.
        Acepta las mismas variantes opcionales de calcular_costo (impuesto, descuento).
        """
        if self._estado != Reserva.CONFIRMADA:          # Solo se procesa lo confirmado
            raise OperacionNoPermitidaError(
                f"No se puede procesar la reserva #{self.id}: estado {self._estado}.")
        exito = False                                   # Bandera para el mensaje del bloque finally
        try:
            costo = self._servicio.calcular_costo(self._duracion, impuesto, descuento)  # POLIMORFISMO
        except (ServicioInvalidoError, ServicioNoDisponibleError, CalculoError) as error:  # Errores del servicio
            # ENCADENAMIENTO: error de reserva cuya causa es el error del servicio
            raise ReservaInvalidaError(f"No se pudo procesar la reserva #{self.id}.") from error
        else:                                           # Solo si el cálculo fue exitoso
            self._costo_final = costo                   # Se guarda el costo
            self._estado = Reserva.PROCESADA            # Cambia el estado
            exito = True
            return costo                                # Devuelve el costo a quien llamó
        finally:                                        # Se ejecuta SIEMPRE, con o sin error
            registrar_evento(f"Procesamiento de la reserva #{self.id} finalizado (exitoso={exito}).")

    # ----------------- Método abstracto heredado de Entidad -----------------

    def describir(self):                                # Implementa el método abstracto de Entidad
        costo = f" | costo ${self._costo_final:,.2f}" if self._costo_final is not None else ""
        return (f"Reserva #{self.id}: {self._cliente.nombre} -> {self._servicio.nombre} | "
                f"duración {self._duracion:g} | estado {self._estado}{costo}")


# =====================================================================
# PRUEBA RÁPIDA (solo corre si ejecutas este archivo directamente)
# La simulación oficial de las 12 operaciones va en main.py (Miguel Ángel).
# =====================================================================

if __name__ == "__main__":
    from servicios import ReservaSala                   # Servicio concreto para la prueba
    from excepciones import ReservaError                # Clase padre de los errores de reserva

    ana = Cliente("Ana Ruiz", "ana@mail.co", "3001234567")
    sala = ReservaSala("S1", "Sala Juntas", 50000, capacidad=10)

    r1 = Reserva(ana, sala, 3)                          # Caso válido completo
    r1.confirmar()
    print("Costo:", r1.procesar(0.19, 0.10))
    print(r1)

    casos = [
        ("Duración fuera de rango",  lambda: Reserva(ana, sala, 20)),
        ("Cliente que no es Cliente", lambda: Reserva("Ana", sala, 2)),
        ("Procesar sin confirmar",   lambda: Reserva(ana, sala, 2).procesar()),
        ("Cancelar dos veces",       lambda: [r.cancelar() for r in [Reserva(ana, sala, 2)] * 2]),
    ]
    for descripcion, operacion in casos:
        try:
            operacion()
        except ReservaError as error:                   # Captura toda la familia de errores de reserva
            registrar_error(error, contexto=descripcion)  # El log guarda también la causa encadenada
            causa = f" | causa: {type(error.__cause__).__name__}" if error.__cause__ else ""
            print(f"- {descripcion}: {error}{causa}")
