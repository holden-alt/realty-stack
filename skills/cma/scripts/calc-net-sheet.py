"""
Realty Stack — Net Sheet Calculator

Parameterized seller net sheet math. Takes researched state/county rates
as input; does not hardcode any state-specific values. Used by /cma skill.
"""
import math


def calculate_title_insurance(price: float, tiers: list[dict]) -> float:
    """
    Calculate owner's title insurance per a graduated tier schedule.

    tiers is an ordered list of {'upper_bound': float | None, 'rate_per_1000': float}.
    The last tier's upper_bound is None (unlimited / top tier).
    """
    if price <= 0:
        return 0.0

    cost = 0.0
    remaining = price
    lower_bound = 0.0

    for tier in tiers:
        if remaining <= 0:
            break
        upper = tier['upper_bound']
        if upper is None:
            cost += (remaining / 1000) * tier['rate_per_1000']
            break
        else:
            tier_size = upper - lower_bound
            in_this_tier = min(remaining, tier_size)
            cost += (in_this_tier / 1000) * tier['rate_per_1000']
            remaining -= in_this_tier
            lower_bound = upper

    return cost


def calculate_transfer_tax(price: float, rate_per_500: float) -> float:
    """
    State or county transfer tax. Statutorily rounds UP to next $500 increment
    before applying the rate (per MCL 207.502 in MI; similar in many states).
    """
    if price <= 0:
        return 0.0
    return math.ceil(price / 500) * rate_per_500


def calculate_net_sheet(
    sale_price: float,
    commission_pct: float,
    admin_fee: float,
    title_fee: float,
    tax_proration: float,
    well_septic_inspection: float,
    state_transfer_tax_per_500: float,
    county_transfer_tax_per_500: float,
    title_insurance_tiers: list[dict],
    mortgage_payoff: float = 0.0,
    buyer_concessions: float = 0.0,
) -> dict:
    """
    Compute a Michigan-format seller net sheet. All state-specific rates are
    passed in as parameters (researched per invocation) — no hardcoded
    state math. Returns structured breakdown.
    """
    if sale_price <= 0:
        return {
            'sale_price': 0,
            'line_items': [],
            'total_costs': 0,
            'net_to_seller': 0,
            'cost_pct_of_sale': 0,
        }

    commission = sale_price * (commission_pct / 100)
    state_tax = calculate_transfer_tax(sale_price, state_transfer_tax_per_500)
    county_tax = calculate_transfer_tax(sale_price, county_transfer_tax_per_500)
    title_ins = calculate_title_insurance(sale_price, title_insurance_tiers)

    line_items = [
        {'name': 'Real Estate Commission',
         'detail': f'{commission_pct:.1f}% × ${sale_price:,.0f}',
         'amount': commission},
        {'name': 'State Transfer Tax',
         'detail': f'${state_transfer_tax_per_500:.2f} per $500',
         'amount': state_tax},
        {'name': 'County Transfer Tax',
         'detail': f'${county_transfer_tax_per_500:.2f} per $500',
         'amount': county_tax},
        {'name': "Owner's Title Insurance",
         'detail': 'State graduated rate',
         'amount': title_ins},
        {'name': 'Title Company Closing Fee',
         'detail': 'Flat fee',
         'amount': title_fee},
        {'name': 'Brokerage Admin Fee',
         'detail': 'Flat fee',
         'amount': admin_fee},
        {'name': 'Property Tax Proration',
         'detail': 'Estimated',
         'amount': tax_proration},
    ]

    if well_septic_inspection > 0:
        line_items.append({
            'name': 'Well/Septic Inspection',
            'detail': 'Customary rural',
            'amount': well_septic_inspection,
        })

    if buyer_concessions > 0:
        line_items.append({
            'name': 'Buyer Concessions',
            'detail': 'Negotiated credit',
            'amount': buyer_concessions,
        })

    if mortgage_payoff > 0:
        line_items.append({
            'name': 'Mortgage Payoff',
            'detail': 'Existing loan',
            'amount': mortgage_payoff,
        })

    total_costs = sum(li['amount'] for li in line_items)
    net = sale_price - total_costs
    cost_pct = (total_costs / sale_price * 100) if sale_price > 0 else 0

    return {
        'sale_price': sale_price,
        'line_items': line_items,
        'total_costs': total_costs,
        'net_to_seller': net,
        'cost_pct_of_sale': cost_pct,
    }
