from src.trading.risk_management import calculate_position


def test_position_size_positive():

    size = calculate_position(
        1000,
        0.02,
        0.01
    )

    assert size > 0