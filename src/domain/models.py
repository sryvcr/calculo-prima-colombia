from decimal import Decimal
from dataclasses import dataclass
from datetime import date


@dataclass
class EmpleadoData:
    nombre: str
    fecha_ingreso: date
    salarios_mensuales: dict[str, Decimal]
    periodo_calculo: str
    metodo_calculo_salario: str
    ausencias_no_remuneradas: list[date]


@dataclass
class PrimaInfo:
    empleado: str
    periodo_calculo: str
    salario_base_prima: Decimal
    dias_trabajados_semestre: int
    prima_bruta: Decimal
    renta_exenta_25_por_ciento: Decimal
    base_gravable_impuesto: Decimal
    impuesto_retenido: Decimal
    prima_neta: Decimal
