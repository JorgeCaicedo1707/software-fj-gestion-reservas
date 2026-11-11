# -*- coding: utf-8 -*-
"""
Este módulo define la clase base Entidad para los elementos del sistema.
Como es abstracta, cada clase hija debe implementar su propia descripción.
"""

# ABC y abstractmethod permiten definir una clase abstracta y sus requisitos.
from abc import ABC, abstractmethod                    # Traemos las herramientas para hacer clases abstractas


class Entidad(ABC):                                    # Hereda de ABC, por eso no se puede instanciar sola
    """Base común que asigna un identificador a cada objeto del sistema."""

    # Este contador pertenece a la clase y se comparte entre sus objetos.
    _contador = 0                                      # Arranca en cero y sube con cada objeto creado

    def __init__(self):                                # Constructor que usan las clases hijas con super()
        # Cada objeto nuevo recibe el siguiente número disponible.
        Entidad._contador += 1                         # Sumamos uno al contador compartido
        self._id = Entidad._contador                   # Ese número queda como id del objeto

    @property                                          # Permite leer el id como si fuera un atributo (objeto.id)
    def id(self):
        """Permite consultar el identificador sin modificarlo directamente."""
        return self._id                                # Devolvemos el id guardado

    @abstractmethod                                    # Obliga a las hijas a escribir su propio describir()
    def describir(self):
        """Cada clase concreta define la información que mostrará de sí misma."""

    def __str__(self):                                 # Se usa cuando hacemos print(objeto)
        # Al convertir el objeto en texto, se usa la descripción de su clase hija.
        return self.describir()                        # Reutilizamos describir() de la hija


# ---------------------------------------------------------------------------
# PRUEBA RÁPIDA (solo corre si ejecutas este archivo directamente)
# ---------------------------------------------------------------------------
if __name__ == "__main__":                             # Solo corre si ejecutamos este archivo directamente
    try:                                               # Probamos algo que debe fallar
        # Esta clase no se puede crear directamente porque es abstracta.
        Entidad()                                      # Intentar crear una clase abstracta da TypeError
    except TypeError as error:                         # Atrapamos ese TypeError
        print("Correcto, no se puede instanciar:", error)  # Confirmamos que la protección funciona
