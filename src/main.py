import json
import argparse
from decimal import getcontext, ROUND_HALF_UP

from domain.factories import EmpleadoFactory
from domain.services import PrimaCalculadora

# ------------------------------
# Configuración de Decimal
# ------------------------------
getcontext().prec = 28  # Alta precisión
getcontext().rounding = ROUND_HALF_UP


# ------------------------------
# CLI
# ------------------------------
def main():
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


if __name__ == "__main__":
    main()
