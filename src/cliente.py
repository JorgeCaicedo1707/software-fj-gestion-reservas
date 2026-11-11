# -*- coding: utf-8 -*-
"""
En este módulo se crea la clase Cliente. Sus datos se guardan de forma
privada y se revisan antes de aceptar cada valor.
"""

# re permite comprobar que los datos tengan el formato esperado.
import re                                              # Módulo de expresiones regulares para validar texto

# Cliente hereda el identificador y la estructura común de Entidad.
from entidad import Entidad                            # Traemos la clase abstracta base
# Esta excepción se usa cuando falta un dato o su formato no es válido.
from excepciones import ClienteInvalidoError           # Traemos el error propio para clientes

# El nombre admite letras y espacios, y debe tener entre 3 y 60 caracteres.
PATRON_NOMBRE = re.compile(r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ ]{3,60}$")   # Solo letras (con tildes y ñ) y espacios
# El correo debe tener un usuario, un dominio y al menos una extensión.
PATRON_CORREO = re.compile(r"^[\w.+-]+@[\w-]+(\.[\w-]+)+$")      # usuario@dominio.extension
# Se acepta un celular colombiano de diez dígitos que comience por 3.
PATRON_TELEFONO = re.compile(r"^3\d{9}$")              # Empieza por 3 y tiene 10 dígitos en total


class Cliente(Entidad):                                # Cliente es hija de Entidad (herencia)
    """Representa a un cliente y valida sus datos al guardarlos."""

    def __init__(self, nombre=None, correo=None, telefono=None):  # Parámetros opcionales para poder detectar si faltan
        # Primero se obtiene el identificador heredado de Entidad.
        super().__init__()                             # Llamamos al constructor del padre para asignar el id
        # Se usan las propiedades para revisar cada dato antes de guardarlo.
        self.nombre = nombre                           # Pasa por el setter de nombre (se valida)
        self.correo = correo                           # Pasa por el setter de correo (se valida)
        self.telefono = telefono                       # Pasa por el setter de teléfono (se valida)

    # Nombre
    @property                                          # Lectura del nombre: cliente.nombre
    def nombre(self):
        """Devuelve el nombre que está guardado en el atributo privado."""
        return self.__nombre                           # Atributo privado (doble guion bajo = encapsulación)

    @nombre.setter                                     # Escritura del nombre con validación
    def nombre(self, valor):
        # El nombre es obligatorio y debe recibirse como texto.
        if valor is None:                              # Si no mandaron nada...
            raise ClienteInvalidoError("Falta el parámetro 'nombre'")  # ...avisamos que falta
        if not isinstance(valor, str):                 # Si no es texto (por ejemplo un número)...
            raise ClienteInvalidoError(f"El nombre debe ser texto, no {type(valor).__name__}")  # ...también es error
        valor = valor.strip()                          # Quitamos espacios sobrantes al inicio y al final
        # El patrón descarta nombres vacíos, muy largos o con símbolos y números.
        if not PATRON_NOMBRE.match(valor):             # Si no cumple el patrón del nombre...
            raise ClienteInvalidoError(f"Nombre inválido: '{valor}'")  # ...lo rechazamos
        # Se normaliza el nombre para que comience cada palabra con mayúscula.
        self.__nombre = valor.title()                  # Lo guardamos con formato Nombre Apellido

    # Correo
    @property                                          # Lectura del correo
    def correo(self):
        """Devuelve el correo guardado para el cliente."""
        return self.__correo                           # Devolvemos el correo privado

    @correo.setter                                     # Escritura del correo con validación
    def correo(self, valor):
        # El correo debe estar presente y cumplir el formato esperado.
        if valor is None:                              # Si no mandaron correo...
            raise ClienteInvalidoError("Falta el parámetro 'correo'")  # ...error de dato faltante
        if not isinstance(valor, str) or not PATRON_CORREO.match(valor.strip()):  # Si no es texto o no tiene formato de correo...
            raise ClienteInvalidoError(f"Correo inválido: '{valor}'")  # ...error de correo inválido
        # Se guarda en minúsculas para mantener un formato uniforme.
        self.__correo = valor.strip().lower()          # Guardamos el correo limpio y en minúsculas

    # Teléfono
    @property                                          # Lectura del teléfono
    def telefono(self):
        """Devuelve el número de teléfono guardado para el cliente."""
        return self.__telefono                         # Devolvemos el teléfono privado

    @telefono.setter                                   # Escritura del teléfono con validación
    def telefono(self, valor):
        # No se puede crear el cliente sin un número de teléfono.
        if valor is None:                              # Si no mandaron teléfono...
            raise ClienteInvalidoError("Falta el parámetro 'telefono'")  # ...error de dato faltante
        # Se convierte a texto para aceptar tanto números como cadenas.
        texto = str(valor).replace(" ", "")            # Pasamos a texto y quitamos los espacios
        # El patrón comprueba que sea un celular colombiano de diez dígitos.
        if not PATRON_TELEFONO.match(texto):           # Si no cumple el formato del celular...
            raise ClienteInvalidoError(f"Teléfono inválido: '{valor}'")  # ...lo rechazamos
        self.__telefono = texto                        # Si todo salió bien, lo guardamos

    # Descripción propia del cliente
    def describir(self):                               # Implementa el método abstracto que pide Entidad
        return f"Cliente #{self.id}: {self.nombre} | {self.correo} | Tel: {self.telefono}"  # Texto resumen del cliente


# ---------------------------------------------------------------------------
# PRUEBA RÁPIDA (solo corre si ejecutas este archivo directamente)
# ---------------------------------------------------------------------------
if __name__ == "__main__":                             # Solo corre si ejecutamos este archivo directamente
    # Los casos combinan datos correctos con algunos datos que deben rechazarse.
    casos = [                                          # Lista de (nombre, correo, teléfono) para probar
        ("jorge caicedo", "Jorge@Correo.com", "3001234567"),   # Válido: se normaliza nombre y correo
        ("Ana María Ruiz", "ana.ruiz@mail.co", 3109876543),    # Válido: el teléfono llega como número
        ("", "x@y.com", "3001234567"),                         # Inválido: nombre vacío
        ("Pedro Gómez", "pedro-correo.com", "3001234567"),     # Inválido: correo sin @
        ("Luis Pérez", "luis@mail.com", "12345"),              # Inválido: teléfono muy corto
        (None, "luis@mail.com", "3001234567"),                 # Inválido: falta el nombre
        ("Carla123", "carla@mail.com", "3001234567"),          # Inválido: el nombre tiene números
    ]
    for datos in casos:                                # Recorremos cada caso de prueba
        try:                                           # Intentamos crear el cliente
            cliente = Cliente(*datos)                  # El * desempaqueta la tupla en los 3 parámetros
        except ClienteInvalidoError as error:          # Si algún dato es inválido...
            print("RECHAZADO ->", error)               # ...mostramos el error y seguimos con el siguiente
        else:
            # Este bloque solo corre cuando los datos fueron aceptados.
            print("CREADO    ->", cliente)            # Mostramos el cliente creado
        finally:
            # Este aviso aparece al terminar cada caso, haya error o no.
            print("   (caso procesado)")               # Siempre se imprime
