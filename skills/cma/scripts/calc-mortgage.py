"""
Realty Stack — Buyer Mortgage Calculator

Zillow-style mortgage calculator. Takes researched rates as input
(mortgage rate, area property tax %, area HO insurance estimate).
Used by /cma skill in buyer mode.
"""


def calculate_principal_interest(loan_amount: float, annual_rate: float,
                                   loan_term_years: int) -> float:
    """Standard amortization formula: P × (r(1+r)^n) / ((1+r)^n - 1)."""
    if loan_amount <= 0:
        return 0.0
    monthly_rate = (annual_rate / 100) / 12
    n_payments = loan_term_years * 12
    if monthly_rate == 0:
        return loan_amount / n_payments
    factor = (1 + monthly_rate) ** n_payments
    return loan_amount * (monthly_rate * factor) / (factor - 1)


def calculate_mortgage(
    purchase_price: float,
    down_payment_pct: float,
    annual_interest_rate: float,
    loan_term_years: int,
    annual_property_tax_pct: float,
    annual_ho_insurance: float,
    annual_mip_pct: float = 0.85,
    other_monthly_costs: float = 0,
) -> dict:
    """Compute a Zillow-style mortgage breakdown for a buyer."""
    down_payment = purchase_price * (down_payment_pct / 100)
    loan_amount = purchase_price - down_payment

    pi = calculate_principal_interest(loan_amount, annual_interest_rate, loan_term_years)
    monthly_tax = (purchase_price * (annual_property_tax_pct / 100)) / 12
    monthly_ins = annual_ho_insurance / 12

    # MIP applies when LTV > 80% (down payment < 20%)
    if down_payment_pct < 20:
        monthly_mip = (loan_amount * (annual_mip_pct / 100)) / 12
    else:
        monthly_mip = 0.0

    total_monthly = pi + monthly_tax + monthly_ins + monthly_mip + other_monthly_costs

    # Cash to close estimate: down payment + ~3% of purchase price
    cash_to_close = down_payment + (purchase_price * 0.03)

    return {
        'down_payment': down_payment,
        'loan_amount': loan_amount,
        'monthly_principal_interest': pi,
        'monthly_property_tax': monthly_tax,
        'monthly_ho_insurance': monthly_ins,
        'monthly_mip': monthly_mip,
        'monthly_other': other_monthly_costs,
        'monthly_payment_total': total_monthly,
        'cash_to_close_estimate': cash_to_close,
    }
