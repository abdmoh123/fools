"""Typer commands for finance related stuff."""

from decimal import Decimal
from typing import Annotated

import typer
from fools.finance.calculator import (
    calc_compound_result,
    calc_debt_monthly_payments,
    calc_debt_payoff_years,
    calc_investment_time,
    calc_monthly_target,
    deflate_value,
)

app = typer.Typer()


@app.command()
def compound(
    initial_value: Annotated[float, typer.Argument()],
    percent_rate: Annotated[float, typer.Argument()],
    years: Annotated[int, typer.Argument()],
    monthly_contribution: Annotated[float, typer.Option()] = 0,
) -> None:
    """Compound interest calculator command."""
    print(
        calc_compound_result(
            Decimal(initial_value),
            Decimal(percent_rate),
            years,
            Decimal(monthly_contribution),
        )
    )


@app.command()
def monthly_target(
    desired_target: Annotated[float, typer.Argument()],
    percent_rate: Annotated[float, typer.Argument()],
    years: Annotated[int, typer.Argument()],
    initial_value: Annotated[float, typer.Option()] = 0,
) -> None:
    """Minimum monthly contributions target calculator command."""
    print(
        calc_monthly_target(
            Decimal(desired_target),
            Decimal(percent_rate),
            years,
            Decimal(initial_value),
        )
    )


@app.command()
def investment_time(
    desired_value: Annotated[float, typer.Argument()],
    percent_rate: Annotated[float, typer.Argument()],
    initial_value: Annotated[float, typer.Argument()],
    monthly_contribution: Annotated[float, typer.Option()] = 0,
) -> None:
    """Calculate how long to reach a desired target."""
    print(
        calc_investment_time(
            Decimal(desired_value),
            Decimal(percent_rate),
            Decimal(initial_value),
            Decimal(monthly_contribution),
        )
    )


@app.command()
def deflate(
    value: Annotated[float, typer.Argument()],
    inflation_rate: Annotated[float, typer.Argument()],
    years: Annotated[int, typer.Argument()],
) -> None:
    """Deflates the current value of money to its past value."""
    print(deflate_value(Decimal(value), Decimal(inflation_rate), years))


@app.command()
def payoff_years(
    initial_debt: Annotated[float, typer.Argument()],
    inflation_rate: Annotated[float, typer.Argument()],
    monthly_payment: Annotated[float, typer.Argument()],
) -> None:
    """Calculate how many years it will take to pay off a debt."""
    print(
        calc_debt_payoff_years(
            Decimal(initial_debt),
            Decimal(inflation_rate),
            Decimal(monthly_payment),
        )
    )


@app.command()
def payoff_monthly(
    initial_debt: Annotated[float, typer.Argument()],
    inflation_rate: Annotated[float, typer.Argument()],
    years: Annotated[int, typer.Argument()],
) -> None:
    """Calculate monthly payment required to pay off debt."""
    print(
        calc_debt_monthly_payments(
            Decimal(initial_debt), Decimal(inflation_rate), years
        )
    )
