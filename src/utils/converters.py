from decimal import Decimal
from datetime import date


def convertir_a_decimal(valor: float | int | str) -> Decimal:
    """Convierte valores numéricos a Decimal"""
    return Decimal(str(valor))


def convertir_fecha_string_isoformat_a_date(fecha_str: str) -> date:
    """Convierte una fecha en texto en formato ISO a un objeto date"""
    return date.fromisoformat(fecha_str)
