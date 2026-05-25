"""Calculators relating to finance."""


def calc_compound_result(
    initial_value: float,
    percent_rate: float,
    years: int,
    monthly_contribution: float = 0,
) -> float:
    """Calculate the compound result of an investment.

    Args:
        initial_value: The initial value of the investment
        percent_rate: The percent rate of the investment
        years: The number of years to calculate the result for
        monthly_contribution: The monthly contribution to the investment

    Returns:
        The compound result of the investment
    """
    # Quick and fast calculation if no monthly deposits are made
    if monthly_contribution == 0:
        return initial_value * (1 + percent_rate) ** years

    # The nested loop gives a more granular and accurate result
    current_value = initial_value
    for _ in range(years):
        for __ in range(12):
            current_value = (current_value + monthly_contribution) * (
                1 + (percent_rate / 12)
            )

    return current_value


def calc_monthly_target(
    desired_target: float,
    percent_rate: float,
    years: int,
    initial_value: float = 0,
) -> float:
    """Calculate how much you need to pay monthly to reach a desired target.

    Args:
        desired_target: The desired value to reach
        percent_rate: The yearly interest rate of the account (e.g. 0.05 for 5%)
        years: The number of years to reach the desired value
        initial_value: The initial value in the account, defaults to 0
    Returns:
        The amount of money to pay per month in order to reach the desired value
    """
    if initial_value > desired_target:
        return 0

    compounding_rate = 1 + percent_rate
    constant: float = desired_target / (compounding_rate)
    inital_value_effect: float = initial_value * (compounding_rate) ** (
        years - 1
    )

    years_effect: float = 0
    for i in range(years):
        years_effect += compounding_rate**i

    return ((constant - inital_value_effect) / years_effect) / 12


def calc_investment_time(
    desired_value: float,
    percent_rate: float,
    initial_value: float,
    monthly_contribution: float = 0,
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
    years: int = 0
    current_value: float = initial_value
    while current_value < desired_value:
        current_value = calc_compound_result(
            initial_value,
            percent_rate,
            years=1,
            monthly_contribution=monthly_contribution,
        )
        years += 1

    return years


def deflate_value(value: float, inflation_rate: float, years: int) -> float:
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
