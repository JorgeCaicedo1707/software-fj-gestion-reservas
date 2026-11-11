# Software FJ: gestión de clientes, servicios y reservas

Este proyecto corresponde a la Fase 4 del curso Programación (213023) de la UNAD. La aplicación permitirá registrar clientes, ofrecer servicios y administrar reservas sin utilizar una base de datos. Los datos se manejarán con objetos y listas; el archivo de logs se usará para dejar constancia de las operaciones y los errores.

## Integrantes y responsabilidades

| Integrante | Usuario de GitHub | Trabajo asignado |
|---|---|---|
| Jorge Leonardo Caicedo Reina | JorgeCaicedo1707 | Excepciones, entidad, cliente, logger e integración de las simulaciones |
| Ronaldo Hoyoa Acevedo | Ronyhoyos30 | Servicios y reservas |
| Ambos | — | Simulaciones, README e informe en PDF |

## Organización del proyecto

```text
src/
  excepciones.py   Errores propios de la aplicación
  entidad.py       Clase base abstracta
  cliente.py       Cliente y validación de sus datos
  servicios.py     Clase Servicio y tipos de servicio
  reserva.py       Creación y procesamiento de reservas
  logger.py        Registro de eventos y errores
  main.py          Simulaciones de las operaciones del sistema
logs/
  software_fj.log  Registro que se crea al ejecutar la aplicación
```

Los archivos de servicios, reservas y simulaciones se completarán durante la integración del trabajo asignado a los integrantes.

## Ejecución

Cuando estén integrados todos los módulos, se podrá ejecutar la aplicación desde la carpeta `src`:

```text
python main.py
```

Se requiere Python 3.10 o una versión posterior. El proyecto utiliza módulos incluidos en Python y no necesita instalar paquetes adicionales.

## Ideas aplicadas

- **Abstracción:** `Entidad` reúne características comunes y obliga a sus clases hijas a definir una descripción.
- **Herencia y polimorfismo:** los clientes, servicios y reservas compartirán la estructura general de `Entidad`, y cada tipo definirá su comportamiento particular.
- **Encapsulación:** los datos personales del cliente se guardan como atributos privados y se revisan mediante propiedades.
- **Excepciones:** los errores tienen clases propias y códigos para poder identificarlos. Las simulaciones mostrarán el uso de `try`, `except`, `else`, `finally` y el encadenamiento de errores.
- **Registro:** las operaciones importantes, advertencias y errores se guardan en `logs/software_fj.log`.

## Códigos de error

| Código | Excepción | Uso |
|---|---|---|
| FJ-101 | `ClienteInvalidoError` | Los datos del cliente faltan o no cumplen el formato esperado. |
| FJ-102 | `ClienteNoEncontradoError` | No se encuentra el cliente solicitado. |
| FJ-201 | `ServicioInvalidoError` | Los datos de un servicio no son válidos. |
| FJ-202 | `ServicioNoDisponibleError` | El servicio no se puede reservar. |
| FJ-301 | `ReservaInvalidaError` | Los datos necesarios para crear la reserva no son válidos. |
| FJ-302 | `OperacionNoPermitidaError` | La reserva no permite realizar la acción solicitada. |
| FJ-401 | `CalculoError` | El costo u otro cálculo no produce un resultado válido. |

## Trabajo en equipo

Cada integrante trabajará en la rama acordada para su parte. Los cambios se integrarán a `main` mediante pull requests, con commits que indiquen qué se agregó o corrigió. Las tareas y su avance se pueden organizar mediante issues en GitHub.
