import pytest
from unittest.mock import patch
import string
import random
from simulation.utils import floor_ceiling_round, create_id, apply_random_modifier

def test_floor_ceiling_round():
    # Test for value within range
    assert floor_ceiling_round(50.4) == 50
    assert floor_ceiling_round(49.5) == 50
    assert floor_ceiling_round(50.6) == 51
    assert floor_ceiling_round(55) == 55

    # Test for value below range (after rounding)
    assert floor_ceiling_round(-10.7) == 0
    assert floor_ceiling_round(-0.6) == 0
    assert floor_ceiling_round(-0.4) == 0

    # Test for value above range (after rounding)
    assert floor_ceiling_round(150.3) == 100
    assert floor_ceiling_round(100.6) == 100

    # Edge cases
    assert floor_ceiling_round(0) == 0
    assert floor_ceiling_round(100) == 100
    assert floor_ceiling_round(99.6) == 100

@patch('random.choices')
def test_create_id(mock_choices):
    # Mock random.choices to return a predictable value
    mock_choices.return_value = ['A', 'B', 'C', 'D', 'E', 'F']
    
    # Generate ID
    generated_id = create_id()
    
    # Check if the generated ID matches the mocked value
    assert generated_id == 'ABCDEF'
    
    # Ensure random.choices is called with the correct arguments
    mock_choices.assert_called_with(string.ascii_uppercase, k=6)

@patch('random.choices')
def test_create_id_randomness(mock_choices):
    # Mock random.choices to return a different predictable value
    mock_choices.return_value = ['X', 'Y', 'Z', 'W', 'V', 'U']
    
    # Generate ID and check that it's the correct mocked value
    generated_id = create_id()
    assert generated_id == 'XYZWVU'

@patch('random.uniform')
def test_apply_random_modifier(mock_uniform):
    # Mock the random value returned by random.uniform(-1, 1)
    mock_uniform.return_value = 0.5  # Mock value for multiplier
    
    # Test for joy with randomize_radius = 10
    result = apply_random_modifier(50, 10)
    # Expected deviation = 0.5 * 10 = 5, so the result = 50 + 5 = 55
    assert result == 55
    
    # Test for clamping at 0 when value goes negative
    mock_uniform.return_value = -0.5
    result = apply_random_modifier(5, 10)  # Random multiplier = -0.5 (mocked), deviation = -5
    assert result == 0  # Result should be clamped to 0
    
    # Test for rounding behavior
    result = apply_random_modifier(49.6, 10)  # Random multiplier = -0.5, deviation = -5
    assert result == 45  # 49.6 - 5 = 44.6, rounded to 45
