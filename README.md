# Software FJ: gestión de clientes, servicios y reservas

Este proyecto corresponde a la Fase 4 del curso Programación (213023) de la UNAD, Grupo 333. La aplicación permite registrar clientes, ofrecer servicios y administrar reservas sin utilizar una base de datos. Los datos se manejan con objetos y listas; el archivo de logs deja constancia de las operaciones y los errores.

## Integrantes y responsabilidades

| Integrante | Usuario de GitHub | Trabajo asignado |
|---|---|---|
| Jorge Leonardo Caicedo Reina | JorgeCaicedo1707 | Excepciones, entidad, cliente y logger |
| Ronaldo Hoyoa Acevedo | Ronyhoyos30 | Servicios y reservas |
| Miguel Ángel González Murillo | miguelgonzalezm16 | main.py con las 12 simulaciones |
| Todos | - | README e informe en PDF |

## Organización del proyecto

- main.py: ejecuta las 12 simulaciones de integración (se ejecuta desde la carpeta principal).
- src/excepciones.py: errores propios de la aplicación.
- src/entidad.py: clase base abstracta.
- src/cliente.py: cliente y validación de sus datos.
- src/servicios.py: clase Servicio y tipos de servicio.
- src/reserva.py: creación y procesamiento de reservas.
- src/logger.py: registro de eventos y errores.
- logs/software_fj.log: registro que se crea al ejecutar la aplicación.

## Ejecución

Desde la carpeta principal del repositorio se ejecuta el comando `python main.py`. Se requiere Python 3.10 o una versión posterior. El proyecto utiliza módulos incluidos en Python y no necesita instalar paquetes adicionales.

## Ideas aplicadas

- **Abstracción:** `Entidad` reúne características comunes y obliga a sus clases hijas a definir una descripción.
- **Herencia y polimorfismo:** los clientes, servicios y reservas comparten la estructura general de `Entidad`, y cada tipo define su comportamiento particular.
- **Encapsulación:** los datos se guardan como atributos privados y se revisan mediante propiedades.
- **Excepciones:** los errores tienen clases propias y códigos para poder identificarlos. Las simulaciones muestran el uso de `try`, `except`, `else`, `finally` y el encadenamiento de errores con `raise ... from`.
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

Cada integrante trabajó en una rama propia (jorge-caicedo, Ronaldo-Hoyos y Miguel-Gonzalez). Los cambios se integraron a `main` mediante pull requests, con commits que indican qué se agregó o corrigió. Las tareas y su avance se organizaron mediante issues en GitHub.
