"""Tests for the finance.calculator module."""

from decimal import Decimal

import pytest
from fools.finance import calculator


def test_calc_compound_result_no_monthly() -> None:
    """Test case for a compound result with no monthly contribution."""
    init_value = Decimal(100)
    percent_rate = Decimal(0.05)
    years = 3

    result = Decimal(115.7625)

    assert result == pytest.approx(  # pyright: ignore[reportUnknownMemberType]
        calculator.calc_compound_result(init_value, percent_rate, years)
    )


def test_calc_compound_result_with_monthly() -> None:
    """Test case for a compound result with a regular monthly contribution."""
    init_value = Decimal(100)
    percent_rate = Decimal(0.05)
    years = 3
    monthly_contribution = Decimal(10)

    result = Decimal(502.6555)

    assert result == pytest.approx(  # pyright: ignore[reportUnknownMemberType]
        calculator.calc_compound_result(
            init_value, percent_rate, years, monthly_contribution
        )
    )


def test_calc_monthly_target() -> None:
    """Test how much per month to reach 100k in 10 years."""
    desired_target = Decimal(100000)
    percent_rate = Decimal(0.1)
    years = 10

    # expected_result = Decimal(475.3439)
    monthly_result = calculator.calc_monthly_target(
        desired_target, percent_rate, years
    )
    compound_result = calculator.calc_compound_result(
        Decimal(0), percent_rate, years, monthly_result
    )
    assert desired_target == pytest.approx(compound_result)  # pyright: ignore[reportUnknownMemberType]


def test_calc_investment_time() -> None:
    """Test how long to invest for to reach a desired value."""
    desired_value = Decimal(100000)
    percent_rate = Decimal(0.1)
    initial_value = Decimal(0)
    monthly_contribution = Decimal(1000)

    years = calculator.calc_investment_time(
        desired_value, percent_rate, initial_value, monthly_contribution
    )
    compound_result = calculator.calc_compound_result(
        initial_value, percent_rate, years, monthly_contribution
    )
    compound_result_before = calculator.calc_compound_result(
        initial_value, percent_rate, years - 1, monthly_contribution
    )
    assert (
        compound_result >= desired_value
        and compound_result_before < desired_value
    )


def test_deflate_value() -> None:
    """Test how much currency is worth in the past."""
    value = Decimal(100)
    inflation_rate = Decimal(0.1)
    years = 10

    actual_value = Decimal(38.5543)
    result = calculator.deflate_value(value, inflation_rate, years)

    assert actual_value == pytest.approx(result)  # pyright: ignore[reportUnknownMemberType]
    # Check if function is reversible
    assert result * (1 + inflation_rate) ** years == pytest.approx(value)  # pyright: ignore[reportUnknownMemberType]
