import json
import argparse
from decimal import Decimal, getcontext, ROUND_HALF_UP
from datetime import date

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


# ------------------------------
# Utilidades
# ------------------------------
def convertir_a_decimal(valor: float | int | str) -> Decimal:
    """Convierte valores numéricos a Decimal"""
    return Decimal(str(valor))


# ------------------------------
# Cálculos principales
# ------------------------------
def calcular_dias_trabajados(
    periodo: str,
    fecha_ingreso: date,
    ausencias: list[date],
 ) -> int:
    """
    Calcula los días trabajados en el semestre, restando ausencias dentro del periodo.
    """
    if periodo == "primer_semestre":
        inicio = date(fecha_ingreso.year, 1, 1)
        fin = date(fecha_ingreso.year, 6, 30)
    elif periodo == "segundo_semestre":
        inicio = date(fecha_ingreso.year, 7, 1)
        fin = date(fecha_ingreso.year, 12, 31)
    else:
        raise ValueError("Periodo no válido")

    if fecha_ingreso > inicio:
        inicio = fecha_ingreso

    total_dias = (fin - inicio).days + 1  # se suma 1 para incluir el dia final
    ausencias_dias = sum(1 for ausencia in ausencias if inicio <= ausencia <= fin)

    return max(total_dias - ausencias_dias, 0)


def calcular_prima(data):
    return {}


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

    result = calcular_prima(data)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
