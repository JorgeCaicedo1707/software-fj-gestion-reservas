# -*- coding: utf-8 -*-
"""
Este módulo guarda en un archivo los eventos, advertencias y errores del sistema.
El archivo sirve para revisar lo ocurrido durante la ejecución.
"""

# logging permite guardar mensajes con distintos niveles de importancia.
import logging
# os ayuda a crear la ruta y la carpeta del registro.
import os

# La carpeta principal del proyecto está un nivel arriba de src.
RUTA_PROYECTO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Todos los mensajes se guardan en este archivo.
RUTA_LOG = os.path.join(RUTA_PROYECTO, "logs", "software_fj.log")


def configurar_logger(nombre="software_fj"):
    """Prepara el registro en archivo y evita agregar manejadores repetidos."""
    logger = logging.getLogger(nombre)
    # Si ya está configurado, se devuelve para no escribir cada mensaje dos veces.
    if logger.handlers:
        return logger
    # Se guardan mensajes desde DEBUG, incluidos INFO, WARNING y ERROR.
    logger.setLevel(logging.DEBUG)
    os.makedirs(os.path.dirname(RUTA_LOG), exist_ok=True)
    # El manejador escribe el registro usando codificación UTF-8.
    manejador = logging.FileHandler(RUTA_LOG, encoding="utf-8")
    # Cada línea muestra la fecha, el nivel y el contenido del mensaje.
    formato = logging.Formatter("%(asctime)s | %(levelname)-8s | %(message)s", "%Y-%m-%d %H:%M:%S")
    manejador.setFormatter(formato)
    logger.addHandler(manejador)
    return logger


# Logger único que usarán todos los módulos con: from logger import registrar_evento, registrar_error
_logger = configurar_logger()


def registrar_evento(mensaje):
    """Guarda información sobre una acción que se realizó correctamente."""
    _logger.info(mensaje)


def registrar_advertencia(mensaje):
    """Guarda un aviso sobre una situación que conviene revisar."""
    _logger.warning(mensaje)


def registrar_error(error, contexto=""):
    """Guarda el error y, si existe, la causa original que lo produjo."""
    # Se incluyen el tipo de error y su mensaje para facilitar la revisión.
    texto = f"[{type(error).__name__}] {error}"
    if contexto:
        texto = f"{contexto} -> {texto}"
    # Si el error se encadenó con raise from, también se registra su origen.
    causa = error.__cause__
    if causa is not None:
        texto += f" | causa: {type(causa).__name__}: {causa}"
    _logger.error(texto)


# ---------------------------------------------------------------------------
# PRUEBA RÁPIDA (solo corre si ejecutas este archivo directamente)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    from excepciones import CalculoError

    registrar_evento("Prueba de logger: inicio")
    try:
        try:
            1 / 0
        except ZeroDivisionError as original:
            raise CalculoError("No se pudo calcular el costo") from original
    except CalculoError as error:
        registrar_error(error, contexto="Prueba de cálculo")
    registrar_advertencia("Prueba de advertencia")
    print("Log escrito en:", RUTA_LOG)
    with open(RUTA_LOG, encoding="utf-8") as archivo:
        print(archivo.read())
