from decimal import Decimal
from datetime import date

from domain.services import PrimaCalculadora


def test_prima_bruta_sin_ausencias(empleado_base):
    calculadora = PrimaCalculadora(empleado_base)
    resultado = calculadora.calcular()
    assert resultado.prima_bruta == Decimal("1011111.11")
    assert resultado.dias_trabajados_semestre == 182


def test_prima_bruta_con_ausencias(empleado_base):
    empleado_base.ausencias_no_remuneradas = [date(2024, 1, 2), date(2024, 2, 15)]
    calculadora = PrimaCalculadora(empleado_base)
    resultado = calculadora.calcular()
    assert resultado.dias_trabajados_semestre == 180
    assert resultado.prima_bruta == Decimal("1000000.00")


def test_salario_base_promedio(empleado_base):
    empleado_base.metodo_calculo_salario = "promedio"
    calculadora = PrimaCalculadora(empleado_base)
    resultado = calculadora.calcular()
    assert resultado.salario_base_prima == Decimal("2000000.00")


def test_retencion_aplicada(empleado_base):
    empleado_base.salarios_mensuales = {
        "enero": 18000000,
        "febrero": 18000000,
        "marzo": 18000000,
        "abril": 18000000,
        "mayo": 18000000,
        "junio": 18000000,
        "julio": 18000000,
        "agosto": 18000000,
        "septiembre": 18000000,
        "octubre": 18000000,
        "noviembre": 18000000,
        "diciembre": 18000000,
    }
    empleado_base.periodo_calculo = "segundo_semestre"
    empleado_base.metodo_calculo_salario = "actual"

    calculadora = PrimaCalculadora(empleado_base)
    resultado = calculadora.calcular()
    assert resultado.impuesto_retenido == Decimal("461476.75")
    assert resultado.prima_bruta > resultado.prima_neta
    assert resultado.prima_bruta - resultado.impuesto_retenido == resultado.prima_neta
