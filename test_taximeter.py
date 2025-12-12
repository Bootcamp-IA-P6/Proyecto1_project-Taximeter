import pytest
from taximeter import calculate_fare

def test_calculate_fare_basic():
    # 10s detenido, 20s en movimiento
    result = calculate_fare(10, 20)
    assert result == pytest.approx(10 * 0.02 + 20 * 0.05)

def test_calculate_fare_zero():
    result = calculate_fare(0, 0)
    assert result == 0

def test_calculate_fare_only_stopped():
    result = calculate_fare(15, 0)
    assert result == pytest.approx(15 * 0.02)

def test_calculate_fare_only_moving():
    result = calculate_fare(0, 30)
    assert result == pytest.approx(30 * 0.05)

def test_calculate_fare_large_values():
    result = calculate_fare(1000, 2000)
    assert result == pytest.approx(1000 * 0.02 + 2000 * 0.05)
