# Documentación del Sistema de Gestión de una Clínica

## Cómo Ejecutar el Sistema

Para inicializar el sistema, se debe ejecutar el archivo app.py utilizando python:

```bash
python app.py
```

## Cómo Ejecutar las Pruebas

Para ejecutar **todas** las pruebas, se debe utilizar el siguiente comando:
```bash
python -m unittest discover tests
```

Para ejecutar las pruebas de un **archivo específico**, se debe utilizar el nombre del módulo y archivo como en el siguiente ejemplo:
```bash
python -m unittest tests.test_cli.test_interfaz_cli
```

## Explicación de diseño general

El diseño general del sistema consta de la parte del código principal (en el módulo "src") y la parte de las pruebas de ese código (en el módulo "tests").

A su vez, src se divide en:

- `src/clinica_gestion`: el módulo principal donde se alberga el código fuente de la aplicación.
- `src/clinica_gestion/modelo`: contiene las clases principales de la gestión de la clínica en sí (no el CLI).
- `src/clinica_gestion/cli`: contiene las clases relacionadas al manejo de la interfaz de usuario (CLI).
- `src/clinica_gestion/modelo/Clinica`: la clase central del manejo del sistema. Se encarga de acciones como registro de nuevos pacientes y médicos, agenda de turnos, emisión de resetas, etc.

Y tests se divide en:

- `tests/test_modelo`: alberga los archivos de tests para las clases de modelo en src.
- `tests/test_cli`: alberga los archivos de tests para las clases de cli en src.

Cabe aclarar que las excepciones personalizadas se encuientran en `src/clinica_gestion/modelo/excepciones.py`.

Finalmente, la entrada principal del sistema se realiza mediante el archivo `app.py` en la raíz del proyecto. Este se encarga de ejecutar el CLI, que a su vez se encarga de la inicialización y manejo de todas las clases del sistema.
