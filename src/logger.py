# -*- coding: utf-8 -*-
"""
Este módulo guarda en un archivo los eventos, advertencias y errores del sistema.
El archivo sirve para revisar lo ocurrido durante la ejecución.
"""

# logging permite guardar mensajes con distintos niveles de importancia.
import logging                                         # Módulo estándar de Python para registros (logs)
# os ayuda a crear la ruta y la carpeta del registro.
import os                                              # Para armar rutas y crear carpetas

# La carpeta principal del proyecto está un nivel arriba de src.
RUTA_PROYECTO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Subimos dos niveles desde este archivo
# Todos los mensajes se guardan en este archivo.
RUTA_LOG = os.path.join(RUTA_PROYECTO, "logs", "software_fj.log")  # Ruta final: proyecto/logs/software_fj.log


def configurar_logger(nombre="software_fj"):          # Prepara el logger una sola vez
    """Prepara el registro en archivo y evita agregar manejadores repetidos."""
    logger = logging.getLogger(nombre)                 # Pedimos (o creamos) el logger con ese nombre
    # Si ya está configurado, se devuelve para no escribir cada mensaje dos veces.
    if logger.handlers:                                # Si ya tiene un manejador puesto...
        return logger                                  # ...lo devolvemos tal cual
    # Se guardan mensajes desde DEBUG, incluidos INFO, WARNING y ERROR.
    logger.setLevel(logging.DEBUG)                     # Nivel más bajo: así se registra todo
    os.makedirs(os.path.dirname(RUTA_LOG), exist_ok=True)  # Creamos la carpeta logs si no existe
    # El manejador escribe el registro usando codificación UTF-8.
    manejador = logging.FileHandler(RUTA_LOG, encoding="utf-8")  # Manejador que escribe en el archivo
    # Cada línea muestra la fecha, el nivel y el contenido del mensaje.
    formato = logging.Formatter("%(asctime)s | %(levelname)-8s | %(message)s", "%Y-%m-%d %H:%M:%S")  # Formato de cada línea
    manejador.setFormatter(formato)                    # Le asignamos el formato al manejador
    logger.addHandler(manejador)                       # Conectamos el manejador al logger
    return logger                                      # Devolvemos el logger listo


# Logger único que usarán todos los módulos con: from logger import registrar_evento, registrar_error
_logger = configurar_logger()                          # Se crea una sola vez al importar el módulo


def registrar_evento(mensaje):                         # Para dejar constancia de algo que salió bien
    """Guarda información sobre una acción que se realizó correctamente."""
    _logger.info(mensaje)                              # Nivel INFO


def registrar_advertencia(mensaje):                    # Para avisos que conviene revisar
    """Guarda un aviso sobre una situación que conviene revisar."""
    _logger.warning(mensaje)                           # Nivel WARNING


def registrar_error(error, contexto=""):               # Para guardar errores con su contexto
    """Guarda el error y, si existe, la causa original que lo produjo."""
    # Se incluyen el tipo de error y su mensaje para facilitar la revisión.
    texto = f"[{type(error).__name__}] {error}"        # Ejemplo: [ClienteInvalidoError] [FJ-101] mensaje
    if contexto:                                       # Si nos dieron contexto (qué se estaba haciendo)...
        texto = f"{contexto} -> {texto}"               # ...lo ponemos al comienzo
    # Si el error se encadenó con raise from, también se registra su origen.
    causa = error.__cause__                            # Error original (si se usó raise ... from)
    if causa is not None:                              # Si existe una causa original...
        texto += f" | causa: {type(causa).__name__}: {causa}"  # ...la agregamos al mensaje
    _logger.error(texto)                               # Nivel ERROR


# ---------------------------------------------------------------------------
# PRUEBA RÁPIDA (solo corre si ejecutas este archivo directamente)
# ---------------------------------------------------------------------------
if __name__ == "__main__":                             # Solo corre si ejecutamos este archivo directamente
    from excepciones import CalculoError               # Importamos aquí porque solo se usa en la prueba

    registrar_evento("Prueba de logger: inicio")       # Escribimos un evento normal
    try:                                               # Try de afuera: captura nuestro error
        try:                                           # Try de adentro: captura el error de Python
            1 / 0                                      # Provoca ZeroDivisionError a propósito
        except ZeroDivisionError as original:          # Guardamos el error original
            raise CalculoError("No se pudo calcular el costo") from original  # Lo encadenamos con el nuestro
    except CalculoError as error:                      # Atrapamos el error nuestro
        registrar_error(error, contexto="Prueba de cálculo")  # Lo registramos con su causa
    registrar_advertencia("Prueba de advertencia")     # Escribimos una advertencia
    print("Log escrito en:", RUTA_LOG)                  # Mostramos dónde quedó el log
    with open(RUTA_LOG, encoding="utf-8") as archivo:  # Abrimos el log para leerlo
        print(archivo.read())                          # Lo imprimimos completo
