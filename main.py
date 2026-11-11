# -*- coding: utf-8 -*-
"""Software FJ - Fase 4: doce simulaciones de integración.

Responsable del main.py: Miguel Ángel.
Ejecutar desde la carpeta principal: python3 main.py
"""

import os
import sys

# Los módulos del equipo están dentro de src.
RUTA_PROYECTO = os.path.dirname(os.path.abspath(__file__))
RUTA_SRC = os.path.join(RUTA_PROYECTO, "src")
if RUTA_SRC not in sys.path:
    sys.path.insert(0, RUTA_SRC)

from cliente import Cliente
from servicios import ReservaSala, AlquilerEquipo, Asesoria
from reserva import Reserva
from excepciones import (
    ClienteInvalidoError,
    ServicioInvalidoError,
    ReservaInvalidaError,
    OperacionNoPermitidaError,
)
from logger import registrar_evento, registrar_error, RUTA_LOG


def ejecutar_simulacion(numero, descripcion, operacion, error_esperado=None):
    """Ejecuta una simulación aislada y registra su resultado en el log."""
    print(f"\n{numero:02d}. {descripcion}")
    try:
        resultado = operacion()
    except Exception as error:
        registrar_error(error, contexto=f"Simulación {numero}: {descripcion}")
        if error_esperado is not None and isinstance(error, error_esperado):
            print(f"   OK: error esperado controlado: {error}")
            if error.__cause__ is not None:
                print(f"   Causa original: {type(error.__cause__).__name__}: {error.__cause__}")
            return True
        print(f"   FALLÓ: error inesperado: {type(error).__name__}: {error}")
        return False
    else:
        if error_esperado is not None:
            print("   FALLÓ: se esperaba un error, pero no ocurrió")
            registrar_evento(f"Simulación {numero}: FALLÓ, faltó el error esperado")
            return False
        print(f"   OK: {resultado}")
        registrar_evento(f"Simulación {numero}: {descripcion} - correcta")
        return True
    finally:
        print(f"   Fin de simulación {numero}")


def crear_y_procesar(cliente, servicio, duracion, impuesto=0.0, descuento=0.0):
    """Demuestra el ciclo PENDIENTE -> CONFIRMADA -> PROCESADA."""
    reserva = Reserva(cliente, servicio, duracion)
    reserva.confirmar()
    reserva.procesar(impuesto=impuesto, descuento=descuento)
    return reserva


def cancelar_reserva(cliente, servicio, duracion):
    """Demuestra una cancelación válida de una reserva pendiente."""
    reserva = Reserva(cliente, servicio, duracion)
    reserva.cancelar()
    return reserva


def confirmar_servicio_inactivo(cliente, servicio):
    """Demuestra el error encadenado cuando un servicio no está disponible."""
    reserva = Reserva(cliente, servicio, 2)
    servicio.desactivar()
    try:
        reserva.confirmar()
    finally:
        servicio.activar()  # Restaurar estado, incluso si confirmar() falla.


def procesar_sin_confirmar(cliente, servicio):
    """Demuestra una transición de estado no permitida."""
    reserva = Reserva(cliente, servicio, 2)
    return reserva.procesar()


def cancelar_dos_veces(cliente, servicio):
    """Demuestra que una reserva cancelada no se puede cancelar nuevamente."""
    reserva = Reserva(cliente, servicio, 1)
    reserva.cancelar()
    reserva.cancelar()  # Debe generar OperacionNoPermitidaError.


def main():
    print("=== SOFTWARE FJ: 12 SIMULACIONES INTEGRADAS ===")
    registrar_evento("Inicio de las 12 simulaciones integradas de main.py")
    resultados = []

    # Objetos compartidos para las operaciones de reserva.
    cliente = Cliente("Ana María Ruiz", "ana@mail.com", "3109876543")
    sala = ReservaSala("S1", "Sala de estudio", 50000, capacidad=10)
    equipo = AlquilerEquipo("E1", "Kit de presentación", 30000, "Proyector", cantidad=2)
    asesoria = Asesoria("A1", "Asesoría TI", 80000, "Ciberseguridad", nivel="experto")

    # 1. Registro correcto de un cliente.
    resultados.append(ejecutar_simulacion(
        1, "Registro de cliente válido",
        lambda: cliente))

    # 2. Correo inválido: excepción personalizada de Jorge.
    resultados.append(ejecutar_simulacion(
        2, "Rechazo de correo inválido",
        lambda: Cliente("Pedro Gómez", "correo-sin-arroba", "3001234567"),
        ClienteInvalidoError))

    # 3. Teléfono inválido.
    resultados.append(ejecutar_simulacion(
        3, "Rechazo de teléfono inválido",
        lambda: Cliente("Laura Pérez", "laura@mail.com", "12345"),
        ClienteInvalidoError))

    # 4. Crear y describir los tres servicios (polimorfismo).
    resultados.append(ejecutar_simulacion(
        4, "Creación de tres tipos de servicio",
        lambda: "\n       ".join(servicio.describir() for servicio in (sala, equipo, asesoria))))

    # 5. Tarifa negativa: excepción de servicio.
    resultados.append(ejecutar_simulacion(
        5, "Rechazo de tarifa negativa",
        lambda: ReservaSala("S2", "Sala B", -100, capacidad=5),
        ServicioInvalidoError))

    # 6. Ciclo completo: crear, confirmar y procesar una sala.
    resultados.append(ejecutar_simulacion(
        6, "Reserva de sala confirmada y procesada (3 horas)",
        lambda: crear_y_procesar(cliente, sala, 3)))

    # 7. Ciclo completo: equipo, dos unidades, dos días.
    resultados.append(ejecutar_simulacion(
        7, "Reserva de equipo confirmada y procesada (2 días)",
        lambda: crear_y_procesar(cliente, equipo, 2)))

    # 8. Ciclo completo: asesoría con impuesto y descuento.
    resultados.append(ejecutar_simulacion(
        8, "Reserva de asesoría procesada con IVA y descuento",
        lambda: crear_y_procesar(cliente, asesoria, 2, 0.19, 0.10)))

    # 9. Cancelación permitida de una reserva pendiente.
    resultados.append(ejecutar_simulacion(
        9, "Cancelación válida de reserva pendiente",
        lambda: cancelar_reserva(cliente, sala, 2)))

    # 10. Duración inválida: excepción de reserva encadenada a la de servicio.
    resultados.append(ejecutar_simulacion(
        10, "Rechazo de reserva con duración fuera de rango",
        lambda: Reserva(cliente, sala, 20),
        ReservaInvalidaError))

    # 11. Confirmar con servicio desactivado: error encadenado.
    resultados.append(ejecutar_simulacion(
        11, "Rechazo de confirmación con servicio no disponible",
        lambda: confirmar_servicio_inactivo(cliente, sala),
        OperacionNoPermitidaError))

    # 12. No se puede procesar una reserva pendiente.
    resultados.append(ejecutar_simulacion(
        12, "Rechazo de procesamiento sin confirmar",
        lambda: procesar_sin_confirmar(cliente, sala),
        OperacionNoPermitidaError))

    correctas = sum(resultados)
    print(f"\n=== RESUMEN: {correctas}/12 simulaciones correctas ===")
    print(f"Archivo de registro: {RUTA_LOG}")
    registrar_evento(f"Fin de simulaciones integradas: {correctas}/12 correctas")


if __name__ == "__main__":
    main()
