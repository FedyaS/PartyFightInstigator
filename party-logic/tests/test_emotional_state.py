import pytest
from unittest.mock import patch
from simulation.emotional_state import apply_random_modifier, EmotionalState

def test_emotional_state_initialization():
    # Test for initialization without randomize_radius
    emotional_state = EmotionalState(joy=60, anger=20, anxiety=5, jealousy=10, curiosity=40)
    
    # No randomization, so values should be directly assigned
    assert emotional_state.joy == 60
    assert emotional_state.anger == 20
    assert emotional_state.anxiety == 5
    assert emotional_state.jealousy == 10
    assert emotional_state.curiosity == 40
    
@patch('random.uniform')
def test_emotional_state_with_randomize_radius(mock_uniform):
    # Mock random.uniform to return 0.5
    mock_uniform.return_value = 0.5
    
    # Initialize with randomization radius
    emotional_state = EmotionalState(joy=60, anger=20, anxiety=5, jealousy=10, curiosity=40, randomize_radius=10)
    
    # Apply the random deviation (multiplier = 0.5, deviation = 0.5 * 10 = 5)
    assert emotional_state.joy == 65  # joy should be 60 + 5 = 65
    assert emotional_state.anger == 25  # anger should be 20 + 5 = 25
    assert emotional_state.anxiety == 10  # anxiety should be 5 + 5 = 10
    assert emotional_state.jealousy == 15  # jealousy should be 10 + 5 = 15
    assert emotional_state.curiosity == 45  # curiosity should be 40 + 5 = 45

def test_set_emotional_state():
    es = EmotionalState(joy=50, anger=10, anxiety=20, jealousy=5, curiosity=30)
    
    # Only update a few emotions
    es.set_emotional_state(joy=80, anxiety=5)

    assert es.joy == 80
    assert es.anxiety == 5
    assert es.anger == 10      # unchanged
    assert es.jealousy == 5    # unchanged
    assert es.curiosity == 30  # unchanged
