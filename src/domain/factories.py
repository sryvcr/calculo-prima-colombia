from domain.models import EmpleadoData
from utils.converters import convertir_fecha_string_isoformat_a_date

class EmpleadoFactory:
    @staticmethod
    def from_dict(data: dict) -> EmpleadoData:
        return EmpleadoData(
            nombre=data["nombre"],
            fecha_ingreso=convertir_fecha_string_isoformat_a_date(
                fecha_str=data["fecha_ingreso"],
            ),
            salarios_mensuales=data["salarios_mensuales"],
            periodo_calculo=data["periodo_calculo"],
            metodo_calculo_salario=data["metodo_calculo_salario"],
            ausencias_no_remuneradas=[
                convertir_fecha_string_isoformat_a_date(fecha_str=ausencia)
                for ausencia in data.get("ausencias_no_remuneradas", [])
            ]
        )
