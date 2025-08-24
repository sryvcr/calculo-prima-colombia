from decimal import Decimal

UVT = Decimal("47065")  # Valor UVT 2025 extraido del pdf
PORCENTAJE_RENTA_EXENTA = Decimal("0.25")

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
