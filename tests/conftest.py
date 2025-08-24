from datetime import date

import pytest

from domain.models import EmpleadoData


@pytest.fixture
def empleado_base():
    return EmpleadoData(
        nombre="John Doe",
        fecha_ingreso=date(2024, 1, 1),
        salarios_mensuales={
            "enero": 2000000,
            "febrero": 2000000,
            "marzo": 2000000,
            "abril": 2000000,
            "mayo": 2000000,
            "junio": 2000000,
            "julio": 2000000,
            "agosto": 2000000,
            "septiembre": 2000000,
            "octubre": 2000000,
            "noviembre": 2000000,
            "diciembre": 2000000,
        },
        periodo_calculo="primer_semestre",
        metodo_calculo_salario="actual",
        ausencias_no_remuneradas=[],
    )
