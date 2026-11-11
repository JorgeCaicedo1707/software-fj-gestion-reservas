# -*- coding: utf-8 -*-
"""
En este módulo se crea la clase Cliente. Sus datos se guardan de forma
privada y se revisan antes de aceptar cada valor.
"""

# re permite comprobar que los datos tengan el formato esperado.
import re

# Cliente hereda el identificador y la estructura común de Entidad.
from entidad import Entidad
# Esta excepción se usa cuando falta un dato o su formato no es válido.
from excepciones import ClienteInvalidoError

# El nombre admite letras y espacios, y debe tener entre 3 y 60 caracteres.
PATRON_NOMBRE = re.compile(r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ ]{3,60}$")
# El correo debe tener un usuario, un dominio y al menos una extensión.
PATRON_CORREO = re.compile(r"^[\w.+-]+@[\w-]+(\.[\w-]+)+$")
# Se acepta un celular colombiano de diez dígitos que comience por 3.
PATRON_TELEFONO = re.compile(r"^3\d{9}$")


class Cliente(Entidad):
    """Representa a un cliente y valida sus datos al guardarlos."""

    def __init__(self, nombre=None, correo=None, telefono=None):
        # Primero se obtiene el identificador heredado de Entidad.
        super().__init__()
        # Se usan las propiedades para revisar cada dato antes de guardarlo.
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

    # Nombre
    @property
    def nombre(self):
        """Devuelve el nombre que está guardado en el atributo privado."""
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        # El nombre es obligatorio y debe recibirse como texto.
        if valor is None:
            raise ClienteInvalidoError("Falta el parámetro 'nombre'")
        if not isinstance(valor, str):
            raise ClienteInvalidoError(f"El nombre debe ser texto, no {type(valor).__name__}")
        valor = valor.strip()
        # El patrón descarta nombres vacíos, muy largos o con símbolos y números.
        if not PATRON_NOMBRE.match(valor):
            raise ClienteInvalidoError(f"Nombre inválido: '{valor}'")
        # Se normaliza el nombre para que comience cada palabra con mayúscula.
        self.__nombre = valor.title()

    # Correo
    @property
    def correo(self):
        """Devuelve el correo guardado para el cliente."""
        return self.__correo

    @correo.setter
    def correo(self, valor):
        # El correo debe estar presente y cumplir el formato esperado.
        if valor is None:
            raise ClienteInvalidoError("Falta el parámetro 'correo'")
        if not isinstance(valor, str) or not PATRON_CORREO.match(valor.strip()):
            raise ClienteInvalidoError(f"Correo inválido: '{valor}'")
        # Se guarda en minúsculas para mantener un formato uniforme.
        self.__correo = valor.strip().lower()

    # Teléfono
    @property
    def telefono(self):
        """Devuelve el número de teléfono guardado para el cliente."""
        return self.__telefono

    @telefono.setter
    def telefono(self, valor):
        # No se puede crear el cliente sin un número de teléfono.
        if valor is None:
            raise ClienteInvalidoError("Falta el parámetro 'telefono'")
        # Se convierte a texto para aceptar tanto números como cadenas.
        texto = str(valor).replace(" ", "")
        # El patrón comprueba que sea un celular colombiano de diez dígitos.
        if not PATRON_TELEFONO.match(texto):
            raise ClienteInvalidoError(f"Teléfono inválido: '{valor}'")
        self.__telefono = texto

    # Descripción propia del cliente
    def describir(self):
        return f"Cliente #{self.id}: {self.nombre} | {self.correo} | Tel: {self.telefono}"


# ---------------------------------------------------------------------------
# PRUEBA RÁPIDA (solo corre si ejecutas este archivo directamente)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # Los casos combinan datos correctos con algunos datos que deben rechazarse.
    casos = [
        ("jorge caicedo", "Jorge@Correo.com", "3001234567"),
        ("Ana María Ruiz", "ana.ruiz@mail.co", 3109876543),
        ("", "x@y.com", "3001234567"),
        ("Pedro Gómez", "pedro-correo.com", "3001234567"),
        ("Luis Pérez", "luis@mail.com", "12345"),
        (None, "luis@mail.com", "3001234567"),
        ("Carla123", "carla@mail.com", "3001234567"),
    ]
    for datos in casos:
        try:
            cliente = Cliente(*datos)
        except ClienteInvalidoError as error:
            print("RECHAZADO ->", error)
        else:
            # Este bloque solo corre cuando los datos fueron aceptados.
            print("CREADO    ->", cliente)
        finally:
            # Este aviso aparece al terminar cada caso, haya error o no.
            print("   (caso procesado)")
