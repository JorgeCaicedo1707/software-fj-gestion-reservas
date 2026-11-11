# -*- coding: utf-8 -*-
"""Software FJ - Fase 4: doce simulaciones de integración.

Responsable del main.py: Miguel Ángel.
Ejecutar desde la carpeta principal: python3 main.py
"""

import os                                              # Para armar rutas de carpetas
import sys                                             # Para agregar src a las rutas donde Python busca módulos

# Los módulos del equipo están dentro de src.
RUTA_PROYECTO = os.path.dirname(os.path.abspath(__file__))  # Carpeta donde está este main.py
RUTA_SRC = os.path.join(RUTA_PROYECTO, "src")          # Carpeta src dentro del proyecto
if RUTA_SRC not in sys.path:                           # Si src todavía no está en la lista de búsqueda...
    sys.path.insert(0, RUTA_SRC)                       # ...la agregamos al principio para poder importar los módulos

from cliente import Cliente                            # Clase Cliente (Jorge)
from servicios import ReservaSala, AlquilerEquipo, Asesoria  # Los tres servicios (Ronaldo)
from reserva import Reserva                            # Clase Reserva (Ronaldo)
from excepciones import (                              # Errores propios que esperamos en las simulaciones
    ClienteInvalidoError,                              # FJ-101: datos de cliente inválidos
    ServicioInvalidoError,                             # FJ-201: datos de servicio inválidos
    ReservaInvalidaError,                              # FJ-301: reserva con datos inválidos
    OperacionNoPermitidaError,                         # FJ-302: acción no permitida en ese estado
)
from logger import registrar_evento, registrar_error, RUTA_LOG  # Funciones del log y la ruta del archivo


def ejecutar_simulacion(numero, descripcion, operacion, error_esperado=None):
    """Ejecuta una simulación aislada y registra su resultado en el log."""
    print(f"\n{numero:02d}. {descripcion}")             # Título de la simulación con número de dos dígitos
    try:                                               # Todo va en try para que un fallo no detenga el programa
        resultado = operacion()                        # Ejecutamos la operación que nos pasaron
    except Exception as error:                         # Si hubo cualquier error...
        registrar_error(error, contexto=f"Simulación {numero}: {descripcion}")  # ...lo guardamos en el log
        if error_esperado is not None and isinstance(error, error_esperado):   # Si era el error que esperábamos...
            print(f"   OK: error esperado controlado: {error}")  # ...la prueba salió bien
            if error.__cause__ is not None:            # Si el error tiene una causa encadenada (raise from)...
                print(f"   Causa original: {type(error.__cause__).__name__}: {error.__cause__}")  # ...la mostramos
            return True                                # La simulación fue correcta
        print(f"   FALLÓ: error inesperado: {type(error).__name__}: {error}")  # Era un error que no esperábamos
        return False                                   # La simulación falló
    else:                                              # Se ejecuta solo si no hubo error
        if error_esperado is not None:                 # Pero si esperábamos un error y no ocurrió...
            print("   FALLÓ: se esperaba un error, pero no ocurrió")  # ...eso también es un fallo
            registrar_evento(f"Simulación {numero}: FALLÓ, faltó el error esperado")  # Lo dejamos en el log
            return False                               # La simulación falló
        print(f"   OK: {resultado}")                   # Operación correcta: mostramos el resultado
        registrar_evento(f"Simulación {numero}: {descripcion} - correcta")  # Lo registramos en el log
        return True                                    # La simulación fue correcta
    finally:                                           # Siempre se ejecuta, haya error o no
        print(f"   Fin de simulación {numero}")        # Marca el final de cada simulación


def crear_y_procesar(cliente, servicio, duracion, impuesto=0.0, descuento=0.0):
    """Demuestra el ciclo PENDIENTE -> CONFIRMADA -> PROCESADA."""
    reserva = Reserva(cliente, servicio, duracion)     # Se crea la reserva (queda PENDIENTE)
    reserva.confirmar()                                # Pasa a CONFIRMADA
    reserva.procesar(impuesto=impuesto, descuento=descuento)  # Pasa a PROCESADA y calcula el costo
    return reserva                                     # Devolvemos la reserva para mostrarla


def cancelar_reserva(cliente, servicio, duracion):
    """Demuestra una cancelación válida de una reserva pendiente."""
    reserva = Reserva(cliente, servicio, duracion)     # Creamos la reserva
    reserva.cancelar()                                 # La cancelamos mientras está pendiente
    return reserva                                     # Devolvemos la reserva cancelada


def confirmar_servicio_inactivo(cliente, servicio):
    """Demuestra el error encadenado cuando un servicio no está disponible."""
    reserva = Reserva(cliente, servicio, 2)            # Reserva de 2 unidades de tiempo
    servicio.desactivar()                              # Desactivamos el servicio a propósito
    try:                                               # Intentamos confirmar con el servicio apagado
        reserva.confirmar()                            # Esto debe lanzar OperacionNoPermitidaError
    finally:                                           # Pase lo que pase...
        servicio.activar()  # Restaurar estado, incluso si confirmar() falla.


def procesar_sin_confirmar(cliente, servicio):
    """Demuestra una transición de estado no permitida."""
    reserva = Reserva(cliente, servicio, 2)            # La reserva queda PENDIENTE
    return reserva.procesar()                          # Procesar sin confirmar no está permitido


def cancelar_dos_veces(cliente, servicio):
    """Demuestra que una reserva cancelada no se puede cancelar nuevamente."""
    reserva = Reserva(cliente, servicio, 1)            # Creamos la reserva
    reserva.cancelar()                                 # Primera cancelación: válida
    reserva.cancelar()  # Debe generar OperacionNoPermitidaError.


def main():
    print("=== SOFTWARE FJ: 12 SIMULACIONES INTEGRADAS ===")  # Encabezado del programa
    registrar_evento("Inicio de las 12 simulaciones integradas de main.py")  # Marca el inicio en el log
    resultados = []                                    # Aquí guardamos True/False de cada simulación

    # Objetos compartidos para las operaciones de reserva.
    cliente = Cliente("Ana María Ruiz", "ana@mail.com", "3109876543")  # Cliente válido para las reservas
    sala = ReservaSala("S1", "Sala de estudio", 50000, capacidad=10)   # Servicio 1: sala por hora
    equipo = AlquilerEquipo("E1", "Kit de presentación", 30000, "Proyector", cantidad=2)  # Servicio 2: equipo por día
    asesoria = Asesoria("A1", "Asesoría TI", 80000, "Ciberseguridad", nivel="experto")    # Servicio 3: asesoría por hora

    # 1. Registro correcto de un cliente.
    resultados.append(ejecutar_simulacion(
        1, "Registro de cliente válido",
        lambda: cliente))                              # No hay error: solo mostramos el cliente

    # 2. Correo inválido: excepción personalizada de Jorge.
    resultados.append(ejecutar_simulacion(
        2, "Rechazo de correo inválido",
        lambda: Cliente("Pedro Gómez", "correo-sin-arroba", "3001234567"),  # Correo sin @
        ClienteInvalidoError))                         # Esperamos este error

    # 3. Teléfono inválido.
    resultados.append(ejecutar_simulacion(
        3, "Rechazo de teléfono inválido",
        lambda: Cliente("Laura Pérez", "laura@mail.com", "12345"),  # Teléfono muy corto
        ClienteInvalidoError))                         # Esperamos este error

    # 4. Crear y describir los tres servicios (polimorfismo).
    resultados.append(ejecutar_simulacion(
        4, "Creación de tres tipos de servicio",
        lambda: "\n       ".join(servicio.describir() for servicio in (sala, equipo, asesoria))))  # Cada servicio se describe a su manera

    # 5. Tarifa negativa: excepción de servicio.
    resultados.append(ejecutar_simulacion(
        5, "Rechazo de tarifa negativa",
        lambda: ReservaSala("S2", "Sala B", -100, capacidad=5),  # Tarifa negativa no es válida
        ServicioInvalidoError))                        # Esperamos este error

    # 6. Ciclo completo: crear, confirmar y procesar una sala.
    resultados.append(ejecutar_simulacion(
        6, "Reserva de sala confirmada y procesada (3 horas)",
        lambda: crear_y_procesar(cliente, sala, 3)))   # 3 horas de sala

    # 7. Ciclo completo: equipo, dos unidades, dos días.
    resultados.append(ejecutar_simulacion(
        7, "Reserva de equipo confirmada y procesada (2 días)",
        lambda: crear_y_procesar(cliente, equipo, 2))) # 2 días de equipo

    # 8. Ciclo completo: asesoría con impuesto y descuento.
    resultados.append(ejecutar_simulacion(
        8, "Reserva de asesoría procesada con IVA y descuento",
        lambda: crear_y_procesar(cliente, asesoria, 2, 0.19, 0.10)))  # IVA 19 % y descuento 10 %

    # 9. Cancelación permitida de una reserva pendiente.
    resultados.append(ejecutar_simulacion(
        9, "Cancelación válida de reserva pendiente",
        lambda: cancelar_reserva(cliente, sala, 2)))   # Cancelar estando pendiente sí se permite

    # 10. Duración inválida: excepción de reserva encadenada a la de servicio.
    resultados.append(ejecutar_simulacion(
        10, "Rechazo de reserva con duración fuera de rango",
        lambda: Reserva(cliente, sala, 20),            # 20 horas supera el máximo de la sala
        ReservaInvalidaError))                         # Esperamos este error

    # 11. Confirmar con servicio desactivado: error encadenado.
    resultados.append(ejecutar_simulacion(
        11, "Rechazo de confirmación con servicio no disponible",
        lambda: confirmar_servicio_inactivo(cliente, sala),  # Servicio apagado a propósito
        OperacionNoPermitidaError))                    # Esperamos este error

    # 12. No se puede procesar una reserva pendiente.
    resultados.append(ejecutar_simulacion(
        12, "Rechazo de procesamiento sin confirmar",
        lambda: procesar_sin_confirmar(cliente, sala), # Procesar sin haber confirmado
        OperacionNoPermitidaError))                    # Esperamos este error

    correctas = sum(resultados)                        # Contamos las simulaciones que dieron True
    print(f"\n=== RESUMEN: {correctas}/12 simulaciones correctas ===")  # Resumen final
    print(f"Archivo de registro: {RUTA_LOG}")          # Dónde quedó el log
    registrar_evento(f"Fin de simulaciones integradas: {correctas}/12 correctas")  # Cierre en el log


if __name__ == "__main__":                             # Solo corre si ejecutamos este archivo directamente
    main()                                             # Arranca las simulaciones
