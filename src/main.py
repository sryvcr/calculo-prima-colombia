from decimal import getcontext, ROUND_HALF_UP

from presentation.cli import cli

# Configuración de Decimal
getcontext().prec = 28  # Alta precisión
getcontext().rounding = ROUND_HALF_UP


def main():
    cli()


if __name__ == "__main__":
    main()
