import pytest
from app.core.humanizer import Humanizer

@pytest.fixture
def humanizer():
    return Humanizer()

def test_randomize_amount(humanizer):
    amount = humanizer.randomize_amount(1.0)
    assert 0.98 <= amount <= 1.02