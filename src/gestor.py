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

    def __init__(self):                                # Se ejecuta al crear el gestor
        # Las listas se guardan privadas (con __) para proteger los datos (encapsulación)
        self.__clientes = []                           # Lista vacía para almacenar objetos Cliente
        self.__servicios = []                          # Lista vacía para almacenar objetos Servicio
        self.__reservas = []                           # Lista vacía para almacenar objetos Reserva

    # ----------------- Encapsulación -----------------
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

    # ----------------- Operaciones de gestión -----------------
    def registrar_cliente(self, cliente):              # Agrega un cliente válido a la lista interna
        """Valida que sea un Cliente y lo guarda en la lista interna."""
        if not isinstance(cliente, Cliente):           # Verificamos que el objeto sí sea de la clase Cliente
            error = TypeError("Se esperaba un objeto del tipo Cliente.")   # Creamos el error
            registrar_error(error, contexto="GestorFJ.registrar_cliente")  # Guardamos el error en el log
            raise error                                # Se envía el error para avisar que el dato no sirve

        self.__clientes.append(cliente)                # Agregamos el cliente al final de la lista privada
        registrar_evento(f"GestorFJ: cliente '{cliente.nombre}' ({cliente.correo}) registrado.")  # Guardamos en el log
        return cliente                                 # Devolvemos el cliente registrado

    def buscar_cliente(self, dato_busqueda):           # Busca un cliente por correo, nombre o id
        """Busca un cliente en la lista y si no existe, lanza ClienteNoEncontradoError (FJ-102)."""
        # Si el dato es texto, le quitamos espacios y lo pasamos a minúsculas
        texto_buscado = dato_busqueda.strip().lower() if isinstance(dato_busqueda, str) else None

        for cliente in self.__clientes:                # Recorremos uno por uno los clientes guardados
            if (                                       # Comparamos el dato buscado con id, correo o nombre
                cliente.id == dato_busqueda
                or (texto_buscado is not None and cliente.correo == texto_buscado)
                or (texto_buscado is not None and cliente.nombre.lower() == texto_buscado)
            ):
                return cliente                         # Si coincide, devolvemos el objeto Cliente encontrado

        # Si termina el ciclo for y no encontró nada, preparamos la excepción FJ-102
        error = ClienteNoEncontradoError(              # Instanciamos el error personalizado (código FJ-102)
            f"No se encontró ningún cliente con el dato '{dato_busqueda}'."
        )
        registrar_error(error, contexto="GestorFJ.buscar_cliente")  # Registramos el error en el archivo de logs
        raise error                                    # Lanzamos la excepción FJ-102

    def agregar_servicio(self, servicio):              # Agrega un servicio válido al catálogo interno
        """Valida que sea un Servicio y lo guarda en la lista interna."""
        if not isinstance(servicio, Servicio):         # Verificamos que herede de la clase abstracta Servicio
            error = TypeError("Se esperaba un objeto de tipo Servicio.")  # Creamos el error
            registrar_error(error, contexto="GestorFJ.agregar_servicio")  # Guardamos el fallo en el log
            raise error                                # Lanzamos el error

        self.__servicios.append(servicio)              # Agregamos el servicio a la lista
        registrar_evento(f"GestorFJ: servicio '{servicio.nombre}' agregado.")  # Dejamos constancia en el log
        return servicio                                # Devolvemos el servicio agregado

    def crear_reserva(self, dato_cliente, servicio, duracion):  # Une cliente buscado, servicio y duración
        """Busca el cliente, crea la reserva y la guarda usando try/except/else/finally."""
        try:
            cliente = self.buscar_cliente(dato_cliente)  # Intentamos buscar el cliente y si no existe salta el error ClienteNoEncontradoError
            reserva = Reserva(cliente, servicio, duracion)  # Creamos la reserva con la clase de Ronaldo
        except ClienteNoEncontradoError as error_cliente:
            # Conectamos el error FJ-102 dentro de ReservaInvalidaError (FJ-301)
            error_reserva = ReservaInvalidaError(
                f"No se pudo crear la reserva: cliente '{dato_cliente}' no registrado."
            )
            registrar_error(error_cliente, contexto="GestorFJ.crear_reserva")  # Registramos la causa en el log
            raise error_reserva from error_cliente     # Lanzamos el error encadenado (raise ... from)
        else:                                          # Este bloque funciona solo si no hubo errores en el try
            self.__reservas.append(reserva)            # Guardamos la reserva en la lista interna
            registrar_evento(f"GestorFJ: reserva #{reserva.id} guardada en la lista.")  # Registramos
            return reserva                             # Devolvemos la reserva creada
        finally:                                       # Este bloque siempre se ejecuta haya error o no
            registrar_evento("GestorFJ: proceso de creación de reserva finalizado.")  # Cierre en el log


# ---------------------------------------------------------------------------
# PRUEBA RÁPIDA (solo corre si ejecutas este archivo directamente)
# ---------------------------------------------------------------------------
if __name__ == "__main__":                             # Solo se ejecuta si corres gestor.py directamente
    from servicios import ReservaSala                  # Importamos un servicio de prueba

    gestor_prueba = GestorFJ()                         # Creamos una instancia del gestor
    cli = Cliente("Angela Hoyos", "angela@mail.com", "3001112233")  # Creamos un cliente válido
    sal = ReservaSala("S9", "Sala Prueba", 40000, capacidad=8)      # Creamos una sala válida

    gestor_prueba.registrar_cliente(cli)               # Registramos el cliente en el gestor
    gestor_prueba.agregar_servicio(sal)                # Agregamos la sala al gestor
    res = gestor_prueba.crear_reserva("angela@mail.com", sal, 2)    # Creamos reserva buscando por correo
    print("Reserva creada:", res.describir())          # Mostramos la reserva creada

    try:                                               # Probamos buscar un cliente que no existe
        gestor_prueba.buscar_cliente("fantasma@mail.com")  # Debe lanzar ClienteNoEncontradoError (FJ-102)
    except ClienteNoEncontradoError as err:            # Atrapamos el error esperado
        print("Error capturado correctamente:", err)   # Imprimimos el mensaje con código [FJ-102]

