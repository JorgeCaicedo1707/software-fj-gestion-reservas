"""
servicios.py
Sistema Integral de Gestión de Clientes, Servicios y Reservas - Software FJ
Curso Programación 213023 - Grupo 213023_333
Responsable del módulo: Ronaldo Hoyos Acevedo (GitHub: Ronyhoyos30)

Contenido del módulo:
    - Servicio        : clase abstracta que define lo que todo servicio debe saber hacer.
    - ReservaSala     : servicio de reserva de salas (cobro por hora).
    - AlquilerEquipo  : servicio de alquiler de equipos (cobro por día y por unidad).
    - Asesoria        : servicio de asesoría especializada (cobro por hora según nivel).
"""

from abc import abstractmethod  # Decorador que obliga a las clases hijas a implementar un método
import math                     # Se usa math.isfinite() para detectar resultados infinitos o NaN


# =====================================================================
# DEPENDENCIAS DEL GRUPO (módulos de Jorge Caicedo en src/)
# =====================================================================

from excepciones import (                               # Módulo excepciones.py (Jorge Caicedo)
    ServicioInvalidoError,                              # Tarifa o parámetro inválido
    ServicioNoDisponibleError,                          # El servicio está desactivado
    CalculoError,                                       # Cálculo de costo inconsistente
)
from entidad import Entidad                             # Clase abstracta base del sistema (Jorge Caicedo)


# =====================================================================
# CLASE ABSTRACTA SERVICIO
# =====================================================================

class Servicio(Entidad):
    """
    Clase abstracta que representa cualquier servicio ofrecido por Software FJ.
    No se puede instanciar directamente: solo sus clases hijas.
    Obliga a cada hija a implementar: validar_parametros, calcular_costo y describir.
    """

    def __init__(self, identificador, nombre, tarifa, disponible=True):
        super().__init__()                              # Entidad asigna el id numérico automático (self.id)
        if not isinstance(identificador, str) or not identificador.strip():  # El código es obligatorio
            raise ServicioInvalidoError("El código del servicio es obligatorio y debe ser texto.")
        self._codigo = identificador.strip()            # Código propio del servicio, ej. "S1"
        self.nombre = nombre                            # Pasa por el setter de 'nombre' -> se valida
        self.tarifa = tarifa                            # Pasa por el setter de 'tarifa' -> se valida
        self._disponible = bool(disponible)             # Estado del servicio: True = se puede reservar

    # ----------------- Encapsulación: propiedades -----------------

    @property                                           # Lectura del nombre: servicio.nombre
    def nombre(self):
        return self._nombre                             # Devuelve el atributo protegido

    @nombre.setter                                      # Escritura del nombre con validación
    def nombre(self, valor):
        if not isinstance(valor, str) or not valor.strip():   # Debe ser texto y no estar vacío
            raise ServicioInvalidoError("El nombre del servicio es obligatorio y debe ser texto.")
        self._nombre = valor.strip()                    # Se guarda sin espacios sobrantes

    @property                                           # Lectura de la tarifa: servicio.tarifa
    def tarifa(self):
        return self._tarifa

    @tarifa.setter                                      # Escritura de la tarifa con validación
    def tarifa(self, valor):
        tarifa = self._convertir_numero(valor, "tarifa")  # Convierte a número (o lanza error encadenado)
        if tarifa <= 0:                                 # Una tarifa cero o negativa no tiene sentido comercial
            raise ServicioInvalidoError(f"La tarifa debe ser mayor que cero. Recibido: {valor}")
        self._tarifa = tarifa                           # Se guarda la tarifa ya validada

    @property                                           # Solo lectura del código: servicio.codigo
    def codigo(self):
        return self._codigo

    @property                                           # Solo lectura: no hay setter para 'disponible'
    def disponible(self):
        return self._disponible

    def activar(self):                                  # Habilita el servicio para nuevas reservas
        self._disponible = True

    def desactivar(self):                               # Deshabilita el servicio (mantenimiento, sin cupo...)
        self._disponible = False

    # ----------------- Métodos de apoyo comunes -----------------

    @staticmethod                                       # No usa 'self': es una utilidad de la clase
    def _convertir_numero(valor, campo):
        """Convierte 'valor' a float. Si falla, lanza ServicioInvalidoError encadenada al error original."""
        if valor is None:                               # Parámetro faltante
            raise ServicioInvalidoError(f"Falta el parámetro '{campo}'.")
        if isinstance(valor, bool):                     # True/False se convertirían a 1.0/0.0: se rechazan
            raise ServicioInvalidoError(f"'{campo}' no puede ser un valor lógico (True/False).")
        try:
            return float(valor)                         # Intenta la conversión ("3" -> 3.0, 2 -> 2.0)
        except (TypeError, ValueError) as error:        # "abc" da ValueError; [1, 2] da TypeError
            # ENCADENAMIENTO: se lanza un error del dominio conservando la causa técnica original
            raise ServicioInvalidoError(f"'{campo}' debe ser numérico. Recibido: {valor!r}") from error

    def verificar_disponibilidad(self):
        """Lanza ServicioNoDisponibleError si el servicio está desactivado."""
        if not self._disponible:                        # Si el servicio está desactivado...
            raise ServicioNoDisponibleError(f"El servicio '{self.nombre}' (id {self.codigo}) no está disponible.")

    def _aplicar_ajustes(self, costo_base, impuesto=0.0, descuento=0.0):
        """
        Aplica impuesto y descuento al costo base. Común a todos los servicios.
        impuesto y descuento se expresan como fracción: 0.19 = 19 %, 0.10 = 10 %.
        """
        impuesto = self._convertir_numero(impuesto, "impuesto")     # Valida tipo del impuesto
        descuento = self._convertir_numero(descuento, "descuento")  # Valida tipo del descuento
        if not 0 <= impuesto <= 1:                                  # Impuesto entre 0 % y 100 %
            raise CalculoError(f"Impuesto fuera de rango (0 a 1): {impuesto}")
        if not 0 <= descuento < 1:                                  # Descuento entre 0 % y menos de 100 %
            raise CalculoError(f"Descuento fuera de rango (0 a <1): {descuento}")
        total = costo_base * (1 + impuesto) * (1 - descuento)       # Primero impuesto, luego descuento
        if not math.isfinite(total) or total <= 0:                  # Detecta infinitos, NaN o totales no positivos
            raise CalculoError(f"Costo inconsistente calculado: {total}")
        return round(total, 2)                                      # Redondeo a 2 decimales (moneda)

    # ----------------- Métodos abstractos (polimorfismo) -----------------

    @abstractmethod
    def validar_parametros(self, duracion):
        """Valida la duración según las reglas de cada servicio. Retorna la duración como float."""

    @abstractmethod
    def calcular_costo(self, duracion, impuesto=0.0, descuento=0.0):
        """
        'Sobrecarga' simulada mediante parámetros opcionales. Variantes de llamada:
            calcular_costo(3)                 -> costo sin impuesto ni descuento
            calcular_costo(3, 0.19)           -> costo con impuesto
            calcular_costo(3, 0.19, 0.10)     -> costo con impuesto y descuento
            calcular_costo(3, descuento=0.1)  -> costo solo con descuento
        Python no admite dos métodos con el mismo nombre en una clase: el segundo
        reemplazaría al primero. Por eso la sobrecarga se simula con valores por defecto.
        """

    @abstractmethod
    def describir(self):
        """Retorna un texto descriptivo del servicio."""


# =====================================================================
# SERVICIO 1: RESERVA DE SALAS
# =====================================================================

class ReservaSala(Servicio):
    """Reserva de salas. Se cobra por hora. Duración permitida: 1 a 12 horas."""

    HORAS_MIN = 1                                       # Constante de clase: mínimo de horas reservables
    HORAS_MAX = 12                                      # Constante de clase: máximo (una jornada)

    def __init__(self, identificador, nombre, tarifa_hora, capacidad, disponible=True):
        super().__init__(identificador, nombre, tarifa_hora, disponible)  # Valida id, nombre y tarifa en Servicio
        capacidad = self._convertir_numero(capacidad, "capacidad")        # Valida que la capacidad sea numérica
        if capacidad <= 0 or not capacidad.is_integer():                  # Debe ser entero positivo (no 10.5 personas)
            raise ServicioInvalidoError(f"La capacidad debe ser un entero positivo. Recibido: {capacidad}")
        self._capacidad = int(capacidad)                                  # Se guarda como entero

    @property
    def capacidad(self):                                # Solo lectura de la capacidad
        return self._capacidad

    def validar_parametros(self, duracion):             # SOBRESCRIBE el método abstracto
        horas = self._convertir_numero(duracion, "duración en horas")     # Convierte o lanza error encadenado
        if not self.HORAS_MIN <= horas <= self.HORAS_MAX:                 # Verifica el rango permitido
            raise ServicioInvalidoError(
                f"Una sala se reserva entre {self.HORAS_MIN} y {self.HORAS_MAX} horas. Recibido: {horas}")
        return horas                                                      # Duración validada

    def calcular_costo(self, duracion, impuesto=0.0, descuento=0.0):      # SOBRESCRIBE: lógica propia de salas
        self.verificar_disponibilidad()                 # 1. ¿Se puede usar el servicio?
        horas = self.validar_parametros(duracion)       # 2. ¿La duración es válida?
        costo_base = self.tarifa * horas                # 3. Regla de negocio: tarifa por hora x horas
        return self._aplicar_ajustes(costo_base, impuesto, descuento)     # 4. Impuesto y descuento

    def describir(self):                                # SOBRESCRIBE: descripción propia de salas
        estado = "disponible" if self.disponible else "no disponible"
        return (f"[Sala {self.codigo}] {self.nombre} - capacidad {self.capacidad} personas - "
                f"${self.tarifa:,.0f}/hora - {estado}")


# =====================================================================
# SERVICIO 2: ALQUILER DE EQUIPOS
# =====================================================================

class AlquilerEquipo(Servicio):
    """Alquiler de equipos. Se cobra por día y por unidad. Duración permitida: 1 a 30 días."""

    DIAS_MIN = 1                                        # Mínimo un día de alquiler
    DIAS_MAX = 30                                       # Máximo un mes

    def __init__(self, identificador, nombre, tarifa_dia, tipo_equipo, cantidad=1, disponible=True):
        super().__init__(identificador, nombre, tarifa_dia, disponible)   # Validaciones comunes
        if not isinstance(tipo_equipo, str) or not tipo_equipo.strip():   # El tipo de equipo es obligatorio
            raise ServicioInvalidoError("El tipo de equipo es obligatorio.")
        self._tipo_equipo = tipo_equipo.strip()                           # Ej.: "Portátil", "Proyector"
        cantidad = self._convertir_numero(cantidad, "cantidad")           # Valida que sea numérica
        if cantidad <= 0 or not cantidad.is_integer():                    # Unidades enteras y positivas
            raise ServicioInvalidoError(f"La cantidad debe ser un entero positivo. Recibido: {cantidad}")
        self._cantidad = int(cantidad)

    @property
    def tipo_equipo(self):                              # Solo lectura del tipo de equipo
        return self._tipo_equipo

    @property
    def cantidad(self):                                 # Solo lectura de la cantidad
        return self._cantidad

    def validar_parametros(self, duracion):             # SOBRESCRIBE: aquí la duración son días
        dias = self._convertir_numero(duracion, "duración en días")
        if not self.DIAS_MIN <= dias <= self.DIAS_MAX:
            raise ServicioInvalidoError(
                f"Un equipo se alquila entre {self.DIAS_MIN} y {self.DIAS_MAX} días. Recibido: {dias}")
        if not dias.is_integer():                       # Se alquila por días completos
            raise ServicioInvalidoError(f"El alquiler es por días completos. Recibido: {dias}")
        return dias

    def calcular_costo(self, duracion, impuesto=0.0, descuento=0.0):      # SOBRESCRIBE: lógica de equipos
        self.verificar_disponibilidad()
        dias = self.validar_parametros(duracion)
        costo_base = self.tarifa * dias * self.cantidad # Regla: tarifa por día x días x unidades
        return self._aplicar_ajustes(costo_base, impuesto, descuento)

    def describir(self):
        estado = "disponible" if self.disponible else "no disponible"
        return (f"[Equipo {self.codigo}] {self.nombre} - {self.cantidad} x {self.tipo_equipo} - "
                f"${self.tarifa:,.0f}/día por unidad - {estado}")


# =====================================================================
# SERVICIO 3: ASESORÍA ESPECIALIZADA
# =====================================================================

class Asesoria(Servicio):
    """Asesoría especializada. Se cobra por hora con un factor según el nivel del asesor."""

    HORAS_MIN = 1                                       # Mínimo una hora de asesoría
    HORAS_MAX = 8                                       # Máximo una jornada laboral
    FACTORES_NIVEL = {"basico": 1.0, "avanzado": 1.3, "experto": 1.6}  # Recargo según nivel

    def __init__(self, identificador, nombre, tarifa_hora, especialidad, nivel="basico", disponible=True):
        super().__init__(identificador, nombre, tarifa_hora, disponible)
        if not isinstance(especialidad, str) or not especialidad.strip():
            raise ServicioInvalidoError("La especialidad de la asesoría es obligatoria.")
        self._especialidad = especialidad.strip()                         # Ej.: "Ciberseguridad"
        if not isinstance(nivel, str) or nivel.lower() not in self.FACTORES_NIVEL:  # Solo niveles definidos
            raise ServicioInvalidoError(
                f"Nivel inválido: {nivel!r}. Opciones: {', '.join(self.FACTORES_NIVEL)}")
        self._nivel = nivel.lower()                                       # Se normaliza a minúsculas

    @property
    def especialidad(self):
        return self._especialidad

    @property
    def nivel(self):
        return self._nivel

    def validar_parametros(self, duracion):             # SOBRESCRIBE: horas de asesoría
        horas = self._convertir_numero(duracion, "duración en horas")
        if not self.HORAS_MIN <= horas <= self.HORAS_MAX:
            raise ServicioInvalidoError(
                f"Una asesoría dura entre {self.HORAS_MIN} y {self.HORAS_MAX} horas. Recibido: {horas}")
        return horas

    def calcular_costo(self, duracion, impuesto=0.0, descuento=0.0):      # SOBRESCRIBE: lógica de asesorías
        self.verificar_disponibilidad()
        horas = self.validar_parametros(duracion)
        factor = self.FACTORES_NIVEL[self.nivel]        # Recargo por nivel del asesor
        costo_base = self.tarifa * horas * factor       # Regla: tarifa x horas x factor de nivel
        return self._aplicar_ajustes(costo_base, impuesto, descuento)

    def describir(self):
        estado = "disponible" if self.disponible else "no disponible"
        return (f"[Asesoría {self.codigo}] {self.nombre} - {self.especialidad} (nivel {self.nivel}) - "
                f"${self.tarifa:,.0f}/hora base - {estado}")


# =====================================================================
# PRUEBAS DEL MÓDULO (solo se ejecutan al correr este archivo directamente)
# La simulación oficial de las 10 operaciones va en main.py.
# =====================================================================

if __name__ == "__main__":

    print("=== 1. try/except: una clase abstracta no se puede instanciar ===")
    try:
        Servicio("S0", "Genérico", 1000)                # Debe fallar: Servicio es abstracta
    except TypeError as e:
        print("Correcto, se rechazó:", e)

    print("\n=== 2. try/except/else: creación válida de los tres servicios ===")
    try:
        sala = ReservaSala("S1", "Sala Juntas", 50000, capacidad=10)
        equipo = AlquilerEquipo("E1", "Kit presentación", 30000, "Proyector", cantidad=2)
        asesoria = Asesoria("A1", "Asesoría TI", 80000, "Ciberseguridad", nivel="experto")
    except ServicioInvalidoError as e:
        print("Error inesperado:", e)
    else:                                               # Solo se ejecuta si no hubo excepción
        for servicio in (sala, equipo, asesoria):       # POLIMORFISMO: misma llamada, comportamiento distinto
            print(servicio)

    print("\n=== 3. Polimorfismo + 'sobrecarga' de calcular_costo ===")
    for servicio, duracion in ((sala, 3), (equipo, 2), (asesoria, 2)):
        print(f"{servicio.nombre}: base={servicio.calcular_costo(duracion):,.2f} | "
              f"con IVA={servicio.calcular_costo(duracion, 0.19):,.2f} | "
              f"IVA y 10% dto={servicio.calcular_costo(duracion, 0.19, 0.10):,.2f}")

    print("\n=== 4. Casos inválidos (el programa no se detiene) ===")
    casos = [
        ("Tarifa negativa",          lambda: ReservaSala("S2", "Sala B", -100, 5)),
        ("Nombre vacío",             lambda: AlquilerEquipo("E2", "  ", 1000, "Portátil")),
        ("Nivel inexistente",        lambda: Asesoria("A2", "Asesoría", 1000, "Redes", "maestro")),
        ("Duración no numérica",     lambda: sala.calcular_costo("tres")),
        ("Duración fuera de rango",  lambda: asesoria.calcular_costo(10)),
        ("Días fraccionados",        lambda: equipo.calcular_costo(1.5)),
        ("Descuento de 150 %",       lambda: sala.calcular_costo(2, descuento=1.5)),
        ("Parámetro faltante",       lambda: sala.calcular_costo(None)),
    ]
    for descripcion, operacion in casos:
        try:
            operacion()
        except (ServicioInvalidoError, CalculoError, ServicioNoDisponibleError) as e:
            causa = f" | causa original: {type(e.__cause__).__name__}" if e.__cause__ else ""
            print(f"- {descripcion}: {type(e).__name__} -> {e}{causa}")

    print("\n=== 5. try/except/finally: servicio no disponible ===")
    sala.desactivar()                                   # Se simula sala en mantenimiento
    try:
        sala.calcular_costo(2)
    except ServicioNoDisponibleError as e:
        print("Rechazado:", e)
    finally:                                            # Siempre se ejecuta, haya o no error
        sala.activar()                                  # Se restablece el estado para no afectar otras pruebas
        print("Estado restablecido ->", sala)
