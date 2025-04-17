import unittest
from unittest.mock import patch
from emotional_state import apply_random_modifier, EmotionalState  # replace with the actual module name

class TestEmotionalState(unittest.TestCase):
        
    def test_emotional_state_initialization(self):
        # Test for initialization without randomize_radius
        emotional_state = EmotionalState(joy=60, anger=20, anxiety=5, jealousy=10, curiosity=40)
        
        # No randomization, so values should be directly assigned
        self.assertEqual(emotional_state.joy, 60)
        self.assertEqual(emotional_state.anger, 20)
        self.assertEqual(emotional_state.anxiety, 5)
        self.assertEqual(emotional_state.jealousy, 10)
        self.assertEqual(emotional_state.curiosity, 40)
        
    @patch('random.uniform')
    def test_emotional_state_with_randomize_radius(self, mock_uniform):
        # Mock random.uniform to return 0.5
        mock_uniform.return_value = 0.5
        
        # Initialize with randomization radius
        emotional_state = EmotionalState(joy=60, anger=20, anxiety=5, jealousy=10, curiosity=40, randomize_radius=10)
        
        # Apply the random deviation (multiplier = 0.5, deviation = 0.5 * 10 = 5)
        self.assertEqual(emotional_state.joy, 65)  # joy should be 60 + 5 = 65
        self.assertEqual(emotional_state.anger, 25)  # anger should be 20 + 5 = 25
        self.assertEqual(emotional_state.anxiety, 10)  # anxiety should be 5 + 5 = 10
        self.assertEqual(emotional_state.jealousy, 15)  # jealousy should be 10 + 5 = 15
        self.assertEqual(emotional_state.curiosity, 45)  # curiosity should be 40 + 5 = 45
    
    def test_set_emotional_state(self):
        es = EmotionalState(joy=50, anger=10, anxiety=20, jealousy=5, curiosity=30)
        
        # Only update a few emotions
        es.set_emotional_state(joy=80, anxiety=5)

        self.assertEqual(es.joy, 80)
        self.assertEqual(es.anxiety, 5)
        self.assertEqual(es.anger, 10)      # unchanged
        self.assertEqual(es.jealousy, 5)    # unchanged
        self.assertEqual(es.curiosity, 30)  # unchanged


if __name__ == '__main__':
    unittest.main()
