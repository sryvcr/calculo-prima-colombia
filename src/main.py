import json
import argparse
from decimal import getcontext, ROUND_HALF_UP

# ------------------------------
# Configuración de Decimal
# ------------------------------
getcontext().prec = 28  # Alta precisión
getcontext().rounding = ROUND_HALF_UP


def calcular_prima(data):
    return {}


def main():
    parser = argparse.ArgumentParser(
        description="Cálculo de Prima de Servicios en Colombia"
    )
    parser.add_argument("input_file", help="Archivo JSON con datos del empleado")
    args = parser.parse_args()

    with open(args.input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    result = calcular_prima(data)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
