import json
import argparse
from decimal import Decimal, getcontext, ROUND_HALF_UP

# ------------------------------
# Configuración de Decimal
# ------------------------------
getcontext().prec = 28  # Alta precisión
getcontext().rounding = ROUND_HALF_UP


# ------------------------------
# Constantes
# ------------------------------
UVT = Decimal("49000")  # Valor UVT 2025 extraido del pdf

# Tabla Art. 383 E.T. (retención en la fuente)
# Formato: (mínimo UVT, máximo UVT, fijo UVT, tarifa marginal)
# Extraida de: https://www.itscontable.com/blog/retencion-en-la-fuente-de-asalariados-2025/
RETENCION_TABLA = [
    (0, 95, 0, 0.0),
    (95, 150, 0, 0.19),
    (150, 360, 10.45, 0.28),
    (360, 640, 69.295, 0.33),
    (640, 945, 162.085, 0.35),
    (945, 2300, 268.7, 0.37),
    (2300, float("inf"), 770.72, 0.39),
]


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
