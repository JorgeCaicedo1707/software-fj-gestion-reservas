# -*- coding: utf-8 -*-
"""
En este módulo se crea la clase GestorFJ. Administra las listas internas
de clientes, servicios y reservas sin utilizar base de datos.
"""

# Se importan las clases desde la carpeta src
from cliente import Cliente                            # Traemos la clase Cliente (Jorge)
from servicios import Servicio                          # Traemos la clase base Servicio (Ronaldo)
from reserva import Reserva                            # Traemos la clase Reserva (Ronaldo)
from excepciones import (                              # Traemos los errores propios del sistema (Jorge)
    ClienteNoEncontradoError,                          # FJ-102: cuando el cliente no está en la lista
    ReservaInvalidaError,                              # FJ-301: cuando falla la creación de la reserva
)
from logger import registrar_evento, registrar_error   # Funciones para escribir en logs/software_fj.log


# ------------------------------------------------------
# CLASE GESTOR PRINCIPAL
# ------------------------------------------------------
class GestorFJ:                                        # Clase encargada de administrar las listas del sistema
    """Guarda y gestiona las listas internas de clientes, servicios y reservas."""

    def __init__(self):                                # Constructor: se ejecuta al crear el gestor
        # Las listas se guardan privadas (con __) para proteger los datos (encapsulación)
        self.__clientes = []                           # Lista vacía para almacenar objetos Cliente
        self.__servicios = []                          # Lista vacía para almacenar objetos Servicio
        self.__reservas = []                           # Lista vacía para almacenar objetos Reserva

    # ----------------- encapsulación -----------------
    @property                                          # Permite leer gestor.clientes como un atributo
    def clientes(self):
        """Devuelve una copia de la lista de clientes registrados."""
        return list(self.__clientes)                   # Retornamos una copia para que no la modifiquen desde fuera

    @property                                          # Permite leer gestor.servicios como un atributo
    def servicios(self):
        """Devuelve una copia de la lista de servicios disponibles."""
        return list(self.__servicios)                  # Retornamos una copia de la lista de servicios

    @property                                          # Permite leer gestor.reservas como un atributo
    def reservas(self):
        """Devuelve una copia de la lista de reservas creadas."""
        return list(self.__reservas)                   # Retornamos una copia de la lista de reservas
