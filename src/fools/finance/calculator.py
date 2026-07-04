"""Calculators relating to finance."""

from decimal import Decimal


def calc_compound_result(
    initial_value: Decimal,
    percent_rate: Decimal,
    years: int,
    monthly_contribution: Decimal | None = None,
) -> Decimal:
    """Calculate the compound result of an investment.

    Args:
        initial_value: The initial value of the investment
        percent_rate: The percent rate of the investment
        years: The number of years to calculate the result for
        monthly_contribution: The monthly contribution to the investment

    Returns:
        The compound result of the investment
    """
    if monthly_contribution is None:
        monthly_contribution = Decimal(0)

    # Quick and fast calculation if no monthly deposits are made
    if monthly_contribution == 0:
        return initial_value * (1 + percent_rate) ** years

    percent_multiplier: Decimal = (1 + percent_rate) ** (
        Decimal(1) / Decimal(12)
    )

    # The nested loop gives a more granular and accurate result
    current_value = initial_value
    for _ in range(years):
        for __ in range(12):
            current_value = (
                current_value * percent_multiplier + monthly_contribution
            )
    return current_value


def calc_monthly_target(
    desired_target: Decimal,
    percent_rate: Decimal,
    years: int,
    initial_value: Decimal | None = None,
) -> Decimal:
    """Calculate how much you need to pay monthly to reach a desired target.

    Args:
        desired_target: The desired value to reach
        percent_rate: The yearly interest rate of the account (e.g. 0.05 for 5%)
        years: The number of years to reach the desired value
        initial_value: The initial value in the account, defaults to 0
    Returns:
        The amount of money to pay per month in order to reach the desired value
    """
    if initial_value is None:
        initial_value = Decimal(0)

    if initial_value > desired_target:
        return Decimal(0)

    monthly_multiplier = (1 + percent_rate) ** (Decimal(1) / Decimal(12))

    growth_factor = monthly_multiplier ** (years * 12)
    result_without_contributions = initial_value * growth_factor
    difference = desired_target - result_without_contributions
    if difference <= 0:
        return Decimal(0)
    return difference * (monthly_multiplier - 1) / (growth_factor - 1)


def calc_investment_time(
    desired_value: Decimal,
    percent_rate: Decimal,
    initial_value: Decimal,
    monthly_contribution: Decimal | None = None,
) -> int:
    """Calculate how long to reach a desired target.

    Args:
        desired_value: The desired value to reach
        percent_rate: The yearly interest rate of the account (e.g. 0.05 for 5%)
        initial_value: The initial value in the account
        monthly_contribution: The monthly addition to the account, defaults to 0

    Returns:
        The number of years to reach the desired value
    """
    if monthly_contribution is None:
        monthly_contribution = Decimal(0)

    years: int = -1
    current_value = initial_value
    while current_value < desired_value:
        years += 1
        current_value = calc_compound_result(
            initial_value,
            percent_rate,
            years,
            monthly_contribution=monthly_contribution,
        )

    return years


def deflate_value(
    value: Decimal, inflation_rate: Decimal, years: int
) -> Decimal:
    """Reverses compound interest to give the value of money in the past.

    Useful for calculating how your invested money in the future will be worth
    in the present.

    Args:
        value: The value to deflate
        inflation_rate: The yearly inflation rate
        years: The number of years to go back

    Returns:
        The deflated value
    """
    return value / (1 + inflation_rate) ** years


def calc_debt_payoff_years(
    initial_debt: Decimal, inflation_rate: Decimal, monthly_payment: Decimal
) -> Decimal:
    """Calculate how many years it will take to pay off a debt.

    Args:
        initial_debt: The initial debt value
        inflation_rate: The yearly interest rate of the debt (e.g. 0.05 for 5%)
        monthly_payment: The monthly payment amount

    Returns:
        The number of years to pay off the debt (rounded up), can return
        infinity if the monthly payment is not enough
    """
    # Check if the monthly payment is enough to even pay off the debt
    monthly_rate = (1 + inflation_rate) ** (Decimal(1) / Decimal(12)) - 1
    if monthly_payment <= initial_debt * monthly_rate:
        return Decimal("inf")

    years = 0
    current_debt = initial_debt
    while current_debt > 0:
        years += 1
        current_debt = calc_compound_result(
            initial_debt,
            inflation_rate,
            years,
            monthly_contribution=-monthly_payment,
        )

    return Decimal(years)


def calc_debt_monthly_payments(
    initial_debt: Decimal, inflation_rate: Decimal, years: int
) -> Decimal:
    """Calculate monthly payment required to pay off debt.

    Given an initial debt, a yearly inflation rate and the number of years to
    pay off the debt.

    Args:
        initial_debt: The initial debt value
        inflation_rate: The yearly interest rate of the debt (e.g. 0.05 for 5%)
        years: The number of years to pay off the debt

    Returns:
        The monthly payment needed to pay off the debt
    """
    monthly_multiplier = (1 + inflation_rate) ** (Decimal(1) / Decimal(12))
    growth_factor = monthly_multiplier ** (years * 12)

    # Standard amortisation formula
    return (
        initial_debt
        * (monthly_multiplier - 1)
        * growth_factor
        / (growth_factor - 1)
    )
