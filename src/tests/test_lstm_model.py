from src.ai.lstm_model import build_model


def test_model_build():
    model = build_model((50,10))

    assert model is not None


def test_model_has_layers():
    model = build_model((50,10))

    assert len(model.layers) > 0