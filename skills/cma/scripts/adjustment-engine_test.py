import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from importlib import import_module
adjustment_engine = import_module("adjustment-engine")


def test_aggressive_picks_high_when_favors_subject():
    """Aggressive + favors subject = top of range.
    Pool: $15K-$20K. Subject has pool, comp doesn't → positive adjustment to comp.
    Aggressive wants the highest positive adjustment."""
    result = adjustment_engine.pick_from_range(15_000, 20_000, 'aggressive', favor_subject=True)
    assert result == 20_000


def test_conservative_picks_low_when_favors_subject():
    """Conservative + favors subject = bottom of range."""
    result = adjustment_engine.pick_from_range(15_000, 20_000, 'conservative', favor_subject=True)
    assert result == 15_000


def test_aggressive_picks_low_when_against_subject():
    """Aggressive + against subject = smaller deduction.
    Subject has worse school district. Negative adjustment.
    Aggressive wants minimum negative."""
    result = adjustment_engine.pick_from_range(10_000, 20_000, 'aggressive', favor_subject=False)
    assert result == 10_000


def test_middle_is_midpoint():
    """Middle returns the midpoint regardless of favor direction."""
    result = adjustment_engine.pick_from_range(15_000, 20_000, 'middle', favor_subject=True)
    assert result == 17_500
    result = adjustment_engine.pick_from_range(15_000, 20_000, 'middle', favor_subject=False)
    assert result == 17_500


def test_low_equals_high():
    """If low == high (point value, not a range), return that value."""
    result = adjustment_engine.pick_from_range(7_500, 7_500, 'aggressive', favor_subject=True)
    assert result == 7_500
