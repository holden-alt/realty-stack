"""
Realty Stack — Adjustment Engine

Picks adjustment values from rate ranges based on the aggressive/conservative
knob. Ensures consistent application across all line items in the CMA.
"""


def pick_from_range(low: float, high: float, knob: str,
                    favor_subject: bool = True) -> float:
    """
    Pick a value from a rate range based on the agg/cons knob position.

    Args:
        low: bottom of range
        high: top of range
        knob: 'aggressive' | 'conservative' | 'middle'
        favor_subject: True if the higher value of the range favors the subject
                       property's value (e.g., a $20K positive adjustment for subject's
                       pool is "favorable" — pushes adjusted value up). False if the
                       higher value works against the subject (e.g., a -$40K school
                       district adjustment is unfavorable).

    Returns the chosen value.
    """
    if low == high:
        return low

    if knob == 'middle':
        return (low + high) / 2

    if knob == 'aggressive':
        return high if favor_subject else low

    if knob == 'conservative':
        return low if favor_subject else high

    raise ValueError(f"Unknown knob position: {knob!r}. Must be 'aggressive', 'conservative', or 'middle'.")
