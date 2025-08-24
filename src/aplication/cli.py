import json
import argparse

from domain.factories import EmpleadoFactory
from domain.services import PrimaCalculadora


def cli():
    """
    Interfaz de línea de comandos para el cálculo de la prima de servicios.
    Lee un archivo JSON con los datos del empleado y muestra el resultado en
    formato JSON.
    """
    parser = argparse.ArgumentParser(
        description="Cálculo de Prima de Servicios en Colombia"
    )
    parser.add_argument("input_file", help="Archivo JSON con datos del empleado")
    args = parser.parse_args()

    with open(args.input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    empleado_data = EmpleadoFactory.from_dict(data)
    calculadora = PrimaCalculadora(empleado_data=empleado_data)
    resultado = calculadora.calcular()
    print(json.dumps(resultado.__dict__, indent=4, ensure_ascii=False, default=float))
