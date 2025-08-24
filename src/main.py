import json
import argparse
from decimal import Decimal, getcontext, ROUND_HALF_UP
from dataclasses import dataclass
from datetime import date

# ------------------------------
# Configuración de Decimal
# ------------------------------
getcontext().prec = 28  # Alta precisión
getcontext().rounding = ROUND_HALF_UP


# ------------------------------
# Constantes
# ------------------------------
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


# ------------------------------
# Dataclasses
# ------------------------------
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


# ------------------------------
# Utilidades
# ------------------------------
def convertir_a_decimal(valor: float | int | str) -> Decimal:
    """Convierte valores numéricos a Decimal"""
    return Decimal(str(valor))


def convertir_fecha_string_isoformat_a_date(fecha_str: str) -> date:
    """Convierte una fecha en texto en formato ISO a un objeto date"""
    return date.fromisoformat(fecha_str)


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


def calcular_salario_base(
    metodo: str,
    salarios: dict[str, float],
    periodo: str
) -> Decimal:
    """Calcula el salario base de la prima según el método elegido."""
    meses_semestre = {
        "primer_semestre": [
            "enero", "febrero", "marzo", "abril", "mayo", "junio"
        ],
        "segundo_semestre": [
            "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
        ],
    }
    meses = meses_semestre[periodo]

    if metodo == "actual":
        return convertir_a_decimal(salarios[meses[-1]])
    elif metodo == "promedio":
        return (
            sum(convertir_a_decimal(salarios[mes]) for mes in meses)
            / convertir_a_decimal(len(meses))
        )
    else:
        raise ValueError("Método de cálculo de salario no válido")


def calcular_retencion_en_la_fuente(
    prima_bruta: Decimal
) -> tuple[Decimal, Decimal, Decimal]:
    """
    Calcula la retención en la fuente según Art. 383 E.T.

    Retorna: (renta exenta, base gravable, impuesto retenido).
    """
    renta_exenta = (prima_bruta * PORCENTAJE_RENTA_EXENTA).quantize(Decimal("0.01"))
    base_gravable = (prima_bruta - renta_exenta).quantize(Decimal("0.01"))
    base_uvt = base_gravable / UVT

    impuesto_uvt = convertir_a_decimal(0)
    for min_uvt, max_uvt, fijo_uvt, tarifa in RETENCION_TABLA:
        min_uvt, max_uvt = convertir_a_decimal(min_uvt), convertir_a_decimal(max_uvt)
        fijo_uvt, tarifa = convertir_a_decimal(fijo_uvt), convertir_a_decimal(tarifa)
        if base_uvt > min_uvt and base_uvt <= max_uvt:
            impuesto_uvt = fijo_uvt + (base_uvt - min_uvt) * tarifa
            break

    impuesto_retenido = (impuesto_uvt * UVT).quantize(Decimal("0.01"))
    return renta_exenta, base_gravable, impuesto_retenido


def calcular_prima_bruta(salario_base: Decimal, dias_trabajados: int) -> Decimal:
    """
    Calcula la prima bruta de un empleado aplicando la formula:
    (salario_base * dias_trabajados) / 360
    """
    return (
        salario_base * convertir_a_decimal(dias_trabajados) / convertir_a_decimal(360)
    ).quantize(Decimal("0.01"))


def calcular_prima_neta(prima_bruta: Decimal, impuesto: Decimal) -> Decimal:
    """
    Calcula la prima neta de un empleado de acuerdo a la diferencia
    entre la prima bruta y el impuesto retenido.
    """
    return (prima_bruta - impuesto).quantize(Decimal("0.01"))


def calcular_prima(empleado_data: EmpleadoData) -> PrimaInfo:
    """Realiza el cálculo completo de la prima."""
    nombre = empleado_data.nombre
    fecha_ingreso = convertir_fecha_string_isoformat_a_date(
        fecha_str=empleado_data.fecha_ingreso
    )
    salarios = empleado_data.salarios_mensuales
    periodo = empleado_data.periodo_calculo
    metodo = empleado_data.metodo_calculo_salario
    ausencias = [
        convertir_fecha_string_isoformat_a_date(fecha_str=ausencia)
        for ausencia in empleado_data.ausencias_no_remuneradas
    ]

    dias_trabajados = calcular_dias_trabajados(
        periodo=periodo,
        fecha_ingreso=fecha_ingreso,
        ausencias=ausencias,
    )
    salario_base = calcular_salario_base(
        metodo=metodo,
        salarios=salarios,
        periodo=periodo,
    )

    prima_bruta = calcular_prima_bruta(
        salario_base=salario_base,
        dias_trabajados=dias_trabajados,
    )
    renta_exenta, base_gravable, impuesto = calcular_retencion_en_la_fuente(
        prima_bruta=prima_bruta,
    )
    prima_neta = calcular_prima_neta(prima_bruta=prima_bruta, impuesto=impuesto)

    return PrimaInfo(
        empleado=nombre,
        periodo_calculo=periodo,
        salario_base_prima=salario_base.quantize(Decimal("0.01")),
        dias_trabajados_semestre=dias_trabajados,
        prima_bruta=prima_bruta,
        renta_exenta_25_por_ciento=renta_exenta,
        base_gravable_impuesto=base_gravable,
        impuesto_retenido=impuesto,
        prima_neta=prima_neta,
    )


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

    empleado_data = EmpleadoData(
        nombre=data["nombre"],
        fecha_ingreso=data["fecha_ingreso"],
        salarios_mensuales=data["salarios_mensuales"],
        periodo_calculo=data["periodo_calculo"],
        metodo_calculo_salario=data["metodo_calculo_salario"],
        ausencias_no_remuneradas=data.get("ausencias_no_remuneradas", [])
    )
    result = calcular_prima(empleado_data=empleado_data)
    print(json.dumps(result.__dict__, indent=4, ensure_ascii=False, default=float))


if __name__ == "__main__":
    main()
