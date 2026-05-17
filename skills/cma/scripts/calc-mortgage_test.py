import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from importlib import import_module
calc_mortgage = import_module("calc-mortgage")


def test_standard_20pct_down_no_mip():
    """20% down → no MIP. $400K purchase, 6.5% rate, 30 yr."""
    result = calc_mortgage.calculate_mortgage(
        purchase_price=400_000,
        down_payment_pct=20,
        annual_interest_rate=6.5,
        loan_term_years=30,
        annual_property_tax_pct=1.5,
        annual_ho_insurance=1_800,
    )

    assert result['down_payment'] == 80_000
    assert result['loan_amount'] == 320_000
    assert result['monthly_mip'] == 0

    # P&I for $320K @ 6.5% / 30yr ≈ $2,022.62
    assert abs(result['monthly_principal_interest'] - 2_022.62) < 1.0

    # Property tax: 400,000 × 1.5% / 12 = $500/mo
    assert abs(result['monthly_property_tax'] - 500) < 0.01

    # HO insurance: $1,800 / 12 = $150/mo
    assert abs(result['monthly_ho_insurance'] - 150) < 0.01


def test_low_down_triggers_mip():
    """5% down → MIP applies."""
    result = calc_mortgage.calculate_mortgage(
        purchase_price=300_000,
        down_payment_pct=5,
        annual_interest_rate=6.5,
        loan_term_years=30,
        annual_property_tax_pct=1.5,
        annual_ho_insurance=1_200,
        annual_mip_pct=0.85,
    )

    # Loan: 300K - 15K = 285K
    assert result['loan_amount'] == 285_000

    # MIP: 285,000 × 0.85% / 12 = $201.875/mo
    assert abs(result['monthly_mip'] - 201.875) < 0.01


def test_cash_to_close_estimate():
    """Cash to close = down payment + roughly 3% of purchase price."""
    result = calc_mortgage.calculate_mortgage(
        purchase_price=400_000,
        down_payment_pct=20,
        annual_interest_rate=6.5,
        loan_term_years=30,
        annual_property_tax_pct=1.5,
        annual_ho_insurance=1_800,
    )
    # 80,000 + 12,000 (3% of 400K) = 92,000
    assert abs(result['cash_to_close_estimate'] - 92_000) < 0.01
