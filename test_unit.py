import pytest
import time
from tax import Trip

# ---------------------------
# TEST Trip.calculate_fare()
# ---------------------------
def test_calculate_fare_basic():
    trip = Trip(stopped_rate=0.02, moving_rate=0.05)
    trip.stopped_time = 10
    trip.moving_time = 20
    assert trip.calculate_fare() == pytest.approx(10*0.02 + 20*0.05)


def test_calculate_fare_zero():
    trip = Trip(stopped_rate=0.02, moving_rate=0.05)
    trip.stopped_time = 0
    trip.moving_time = 0
    assert trip.calculate_fare() == pytest.approx(0)


def test_calculate_fare_only_stopped():
    trip = Trip(stopped_rate=0.02, moving_rate=0.05)
    trip.stopped_time = 15
    trip.moving_time = 0
    assert trip.calculate_fare() == pytest.approx(15*0.02)


def test_calculate_fare_only_moving():
    trip = Trip(stopped_rate=0.02, moving_rate=0.05)
    trip.stopped_time = 0
    trip.moving_time = 30
    assert trip.calculate_fare() == pytest.approx(30*0.05)


def test_calculate_fare_large_values():
    trip = Trip(stopped_rate=0.02, moving_rate=0.05)
    trip.stopped_time = 1000
    trip.moving_time = 2000
    assert trip.calculate_fare() == pytest.approx(1000*0.02 + 2000*0.05)


# ---------------------------
# TEST cambio de estado
# ---------------------------
def test_change_state_accumulates_time():
    trip = Trip(stopped_rate=0.02, moving_rate=0.05)

    # Simula 5 segundos detenidos
    trip.state_start_time = time.time() - 5
    trip.change_state("moving")
    assert trip.stopped_time == pytest.approx(5, rel=0.01)
    assert trip.state == "moving"

    # Simula 3 segundos en movimiento
    trip.state_start_time = time.time() - 3
    trip.change_state("stopped")
    assert trip.moving_time == pytest.approx(3, rel=0.01)
    assert trip.state == "stopped"


# ---------------------------
# TEST finalizar viaje
# ---------------------------
def test_finish_trip_accumulates_time():
    trip = Trip(stopped_rate=0.02, moving_rate=0.05)

    # 4 segundos detenidos
    trip.state_start_time = time.time() - 4
    trip.change_state("moving")

    # 6 segundos en movimiento
    trip.state_start_time = time.time() - 6
    total = trip.finish()

    assert trip.stopped_time == pytest.approx(4, rel=0.01)
    assert trip.moving_time == pytest.approx(6, rel=0.01)
    assert total == pytest.approx(4*0.02 + 6*0.05)









