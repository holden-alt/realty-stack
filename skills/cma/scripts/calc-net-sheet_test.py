"""Tests for calc-net-sheet.py — Michigan net sheet at $549,900 (matches 6333 Blackmar)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from importlib import import_module
calc_net_sheet = import_module("calc-net-sheet")

MI_TITLE_INSURANCE_TIERS = [
    {'upper_bound': 100_000, 'rate_per_1000': 5.75},
    {'upper_bound': 500_000, 'rate_per_1000': 3.40},
    {'upper_bound': None,    'rate_per_1000': 2.50},
]


def test_blackmar_recommended_list_price():
    """At $549,900 sale price with default 6% commission, MI rates, no payoff."""
    result = calc_net_sheet.calculate_net_sheet(
        sale_price=549_900,
        commission_pct=6.0,
        admin_fee=495,
        title_fee=395,
        tax_proration=1_800,
        well_septic_inspection=500,
        state_transfer_tax_per_500=3.75,
        county_transfer_tax_per_500=0.55,
        title_insurance_tiers=MI_TITLE_INSURANCE_TIERS,
    )

    # Commission: 6% × $549,900 = $32,994
    assert result['line_items'][0]['name'] == 'Real Estate Commission'
    assert result['line_items'][0]['amount'] == 32_994.00

    # State transfer tax: ceil(549900/500) × 3.75 = 1100 × 3.75 = $4,125
    state_tax = next(li for li in result['line_items'] if 'State Transfer Tax' in li['name'])
    assert state_tax['amount'] == 4_125.00

    # County transfer tax: ceil(549900/500) × 0.55 = 1100 × 0.55 = $605
    county_tax = next(li for li in result['line_items'] if 'County Transfer Tax' in li['name'])
    assert county_tax['amount'] == 605.00

    # Title insurance: tier1 (100 × $5.75 = $575) + tier2 (400 × $3.40 = $1,360) +
    # tier3 (49.9 × $2.50 = $124.75) = $2,059.75
    title_ins = next(li for li in result['line_items'] if 'Title Insurance' in li['name'])
    assert abs(title_ins['amount'] - 2_059.75) < 0.01

    # Total: 32994 + 4125 + 605 + 2059.75 + 395 + 495 + 1800 + 500 = $42,973.75
    assert abs(result['total_costs'] - 42_973.75) < 0.01

    # Net to seller: 549900 - 42973.75 = $506,926.25
    assert abs(result['net_to_seller'] - 506_926.25) < 0.01


def test_transfer_tax_rounds_up_to_next_500():
    """549,901 (not on $500 boundary) should round to ceil(549901/500)=1100 × 3.75 = $4,125."""
    result = calc_net_sheet.calculate_net_sheet(
        sale_price=549_901,
        commission_pct=6.0,
        admin_fee=495, title_fee=395, tax_proration=1_800, well_septic_inspection=500,
        state_transfer_tax_per_500=3.75, county_transfer_tax_per_500=0.55,
        title_insurance_tiers=MI_TITLE_INSURANCE_TIERS,
    )
    state_tax = next(li for li in result['line_items'] if 'State Transfer Tax' in li['name'])
    assert state_tax['amount'] == 4_125.00


def test_title_insurance_single_tier():
    """At $50,000 sale price, only first tier applies."""
    result = calc_net_sheet.calculate_net_sheet(
        sale_price=50_000,
        commission_pct=6.0,
        admin_fee=495, title_fee=395, tax_proration=500, well_septic_inspection=0,
        state_transfer_tax_per_500=3.75, county_transfer_tax_per_500=0.55,
        title_insurance_tiers=MI_TITLE_INSURANCE_TIERS,
    )
    title_ins = next(li for li in result['line_items'] if 'Title Insurance' in li['name'])
    # 50 × $5.75 = $287.50
    assert abs(title_ins['amount'] - 287.50) < 0.01


def test_with_mortgage_payoff_and_concessions():
    """Optional mortgage payoff + buyer concessions add to costs and reduce net."""
    result = calc_net_sheet.calculate_net_sheet(
        sale_price=400_000,
        commission_pct=6.0,
        admin_fee=495, title_fee=395, tax_proration=1_500, well_septic_inspection=500,
        state_transfer_tax_per_500=3.75, county_transfer_tax_per_500=0.55,
        title_insurance_tiers=MI_TITLE_INSURANCE_TIERS,
        mortgage_payoff=180_000,
        buyer_concessions=8_000,
    )

    has_payoff = any('Mortgage Payoff' in li['name'] for li in result['line_items'])
    has_concessions = any('Buyer Concessions' in li['name'] for li in result['line_items'])
    assert has_payoff
    assert has_concessions

    payoff_li = next(li for li in result['line_items'] if 'Mortgage Payoff' in li['name'])
    conc_li = next(li for li in result['line_items'] if 'Buyer Concessions' in li['name'])
    assert payoff_li['amount'] == 180_000
    assert conc_li['amount'] == 8_000


def test_zero_sale_price_returns_zeros():
    """Edge case: $0 sale price should not error, just return zeros."""
    result = calc_net_sheet.calculate_net_sheet(
        sale_price=0,
        commission_pct=6.0,
        admin_fee=0, title_fee=0, tax_proration=0, well_septic_inspection=0,
        state_transfer_tax_per_500=3.75, county_transfer_tax_per_500=0.55,
        title_insurance_tiers=MI_TITLE_INSURANCE_TIERS,
    )
    assert result['net_to_seller'] == 0
    assert result['cost_pct_of_sale'] == 0
