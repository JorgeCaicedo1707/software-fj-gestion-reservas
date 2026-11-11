# -*- coding: utf-8 -*-
"""
Este módulo define la clase base Entidad para los elementos del sistema.
Como es abstracta, cada clase hija debe implementar su propia descripción.
"""

# ABC y abstractmethod permiten definir una clase abstracta y sus requisitos.
from abc import ABC, abstractmethod


class Entidad(ABC):
    """Base común que asigna un identificador a cada objeto del sistema."""

    # Este contador pertenece a la clase y se comparte entre sus objetos.
    _contador = 0

    def __init__(self):
        # Cada objeto nuevo recibe el siguiente número disponible.
        Entidad._contador += 1
        self._id = Entidad._contador

    @property
    def id(self):
        """Permite consultar el identificador sin modificarlo directamente."""
        return self._id

    @abstractmethod
    def describir(self):
        """Cada clase concreta define la información que mostrará de sí misma."""

    def __str__(self):
        # Al convertir el objeto en texto, se usa la descripción de su clase hija.
        return self.describir()


# ---------------------------------------------------------------------------
# PRUEBA RÁPIDA (solo corre si ejecutas este archivo directamente)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    try:
        # Esta clase no se puede crear directamente porque es abstracta.
        Entidad()
    except TypeError as error:
        print("Correcto, no se puede instanciar:", error)
