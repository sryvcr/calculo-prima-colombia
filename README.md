# 🇨🇴 Cálculo de Prima de Servicios en Colombia

Este proyecto es una aplicación CLI en Python que calcula la Prima de Servicios en Colombia, teniendo en cuenta:

- Días efectivamente trabajados en el semestre (`primer_semestre` o `segundo_semestre`).
- Método de salario base (`actual` o `promedio`).
- Ausencias no remuneradas.
- Renta exenta del 25%.
- Retención en la fuente según el Artículo 383 del Estatuto Tributario.
- Resultados con exactitud de 2 decimales.
- La aplicación está dockerizada para que se ejecute fácilmente en cualquier entorno.

## 💭 Supuestos Realizados:
- Para calcular la prima se tiene en cuenta el año de la fecha de ingreso.
- Se asume que el año base para el cálculo de la prima es de 360 días, como se infiere de la fórmula `(Salario * Días Trabajados) / 360` proporcionada en el ejercicio.
- Se utiliza el valor de la UVT de **$47,065 COP** proporcionado en el ejercicio y la tabla de retención del Art. 383 E.T. vigente extraida de: https://www.itscontable.com/blog/retencion-en-la-fuente-de-asalariados-2025/.
- Para simplificar, y como lo permite el ejercicio, se omite el límite anual de 790 UVT para la renta exenta del 25%.
- Si las ausencias no corresponden al periodo o año en cuestión, no se toman en cuenta.

## 🖌️ Decisiones de Diseño:
- Se implementa una arquitectura limpia separando la lógica de negocio, presentación y utilidades para facilitar el mantenimiento y la escalabilidad.
- La estructura modular permite agregar nuevos métodos de cálculo o periodos sin afectar el resto del sistema.
- Se utiliza el tipo `Decimal` con precisión de 2 dígitos y redondeo hacia arriba, para asegurar en lo posible la exactitud en los cálculos financieros.

## 🏗️ Clases principales

Las clases y módulos principales son:
- _domain/models.py_: Define las entidades centrales, como `EmpleadoData`, que encapsula los datos y comportamientos relacionados para el cálculo de la prima, incluyendo salarios, ausencias y periodos de cálculo.
- _domain/services.py_: Contiene la lógica de negocio para el cálculo de la prima, renta exenta y retención en la fuente. Aquí se implementan los métodos que aplican las reglas legales y financieras, asegurando precisión y cumplimiento normativo.
    - La clase `PrimaCalculadora` (ubicada en `src/domain/services.py`) es el núcleo del cálculo de la prima de servicios. Su diseño encapsula toda la lógica necesaria para calcular la prima de un empleado en Colombia, siguiendo la normativa vigente y los supuestos del proyecto. Esta clase tiene las siguientes responsabilidades:
        - Calcular el salario base.
        - Determinar los días efectivamente trabajados en el semestre especificado.
        - Aplicar las ausencias no remuneradas dentro del periodo de cálculo.
        - Calcular la prima bruta utilizando la fórmula `(Salario * Días Trabajados) / 360`.
        - Calcular la renta exenta del 25%.
        - Aplicar la retención en la fuente según el Artículo 383 del Estatuto Tributario.
        - Proporcionar el resultado final de la prima con exactitud de 2 decimales.
        - Manejar posibles errores y excepciones durante el cálculo.
- _domain/constants.py_: Centraliza los valores constantes, como el valor de la UVT y los tramos de retención, facilitando su actualización.
- _domain/factories.py_: Implementa fábricas para construir instancias de entidades a partir de los datos de entrada (por ejemplo, desde archivos JSON), desacoplando la creación de objetos.
- _presentation/cli.py_: Gestiona la interfaz de línea de comandos, el parseo de argumentos y la interacción con el usuario, manteniendo la lógica de presentación desacoplada.
- _utils/converters.py_: Incluye funciones auxiliares para la conversión y validación de datos, como fechas y montos, asegurando que la información procesada sea consistente y válida.

## 📂 Estructura del proyecto
```bash
.
├──src/                       # Carpeta principal del proyecto, contiene el código fuente
│   ├── samples               # Archivos de ejemplo
│   │   ├── employee_1.json
│   │   └── employee_2.json
│   ├── domain                # Entidades y lógica de negocio
│   │   ├── constants.py
│   │   ├── factories.py
│   │   ├── models.py
│   │   └── services.py
│   ├── presentation          # Interfaces de usuario
│   │   └── cli.py
│   ├── utils                 # Utilidades y helpers
│   │   └── converters.py
│   └── main.py               # Funcion main() que orquesta la ejecución del código
├──tests/                     # Pruebas unitarias
│   ├── conftests.py
│   └── test_services.py
├── Dockerfile
├── Makefile
└── README.md
```

## 🚀 Ejecución
1. Construir la imagen Docker
    ```bash
    make build
    ```
2. Ejecutar la aplicación con un archivo JSON  
    Por defecto, el proyecto incluye dos archivos de ejemplo en la carpeta /app/data dentro del contenedor:

    - _employee_1.json_ (primer semestre sin ausencias ni retención).
    - _employee_2.json_ (segundo semestre con ausencias y retención).

    Ejemplo de ejecución:
    ```bash
    make run
    ```
    👉 Usa `/app/samples/employee_1.json` como archivo por defecto.  
    
    Si quieres usar otro archivo JSON ya incluido en la imagen:
    ```bash
    make run JSON_FILE=/app/samples/employee_2.json
    ```
3. (Opcional) Ejecutar tests unitarios
    ```bash
    make tests
    ```

## ➕ Agregar más archivos JSON
1. Crea un archivo en la carpeta src/samples/ con la misma estructura de los ejemplos:
    ```json
    {
        "nombre": "Juan Pérez",
        "fecha_ingreso": "2023-03-15",
        "salarios_mensuales": {
            "enero": 3000000,
            "febrero": 3000000,
            "marzo": 3000000,
            "abril": 3200000,
            "mayo": 3200000,
            "junio": 3200000,
            "julio": 3200000,
            "agosto": 3200000,
            "septiembre": 3500000,
            "octubre": 3500000,
            "noviembre": 3500000,
            "diciembre": 3500000
        },
        "periodo_calculo": "primer_semestre",
        "metodo_calculo_salario": "promedio",
        "ausencias_no_remuneradas": []
    }
    ```
2. Reconstruye la imagen para que el nuevo archivo quede dentro del contenedor:
    ```bash
    make build
    ```
3. Ejecuta usando la ruta interna del nuevo archivo:
    ```bash
    make run JSON_FILE=/app/samples/<nombre_del_archivo>.json
    ```

## 📊 Ejemplo de salida
```json
{
    "empleado": "Juan Pérez",
    "periodo_calculo": "primer_semestre",
    "salario_base_prima": 3100000.0,
    "dias_trabajados_semestre": 108,
    "prima_bruta": 930000.0,
    "renta_exenta_25_por_ciento": 232500.0,
    "base_gravable_impuesto": 697500.0,
    "impuesto_retenido": 0.0,
    "prima_neta": 930000.0
}
```

## 🛠️ Tecnologías utilizadas
- Python 3.11 para el desarrollo del CLI.
- Docker para portabilidad.
- Makefile para simplificar ejecución.
