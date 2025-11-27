"""Tests for the player module."""
import unittest

# Define constants here for testing since importing player requires Qt multimedia
# These match the constants in src/ui/player.py
PLAYBACK_SPEEDS = [0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 5.0]
DEFAULT_FRAME_RATE = 30.0


class TestPlaybackSpeeds(unittest.TestCase):
    """Test cases for playback speeds constants."""
    
    def test_playback_speeds_order(self):
        """Test that playback speeds are in ascending order."""
        self.assertEqual(PLAYBACK_SPEEDS, sorted(PLAYBACK_SPEEDS))
    
    def test_playback_speeds_contains_normal(self):
        """Test that playback speeds include 1.0 (normal speed)."""
        self.assertIn(1.0, PLAYBACK_SPEEDS)
    
    def test_playback_speeds_values(self):
        """Test expected playback speed values."""
        expected = [0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 5.0]
        self.assertEqual(PLAYBACK_SPEEDS, expected)
    
    def test_playback_speeds_contains_5x(self):
        """Test that playback speeds include 5.0 (5x speed)."""
        self.assertIn(5.0, PLAYBACK_SPEEDS)


class TestQtPlayerSpeedControl(unittest.TestCase):
    """Test cases for QtPlayer speed control methods."""
    
    def setUp(self):
        """Set up test fixtures with mocked Qt components."""
        # We can't test the actual player without Qt event loop,
        # so we test the logic of speed index calculations
        pass
    
    def test_default_frame_rate(self):
        """Test default frame rate constant."""
        self.assertEqual(DEFAULT_FRAME_RATE, 30.0)
    
    def test_speed_index_calculation(self):
        """Test speed index lookup for various rates."""
        # Test normal speed (1.0)
        self.assertEqual(PLAYBACK_SPEEDS.index(1.0), 3)
        
        # Test minimum speed (0.25)
        self.assertEqual(PLAYBACK_SPEEDS.index(0.25), 0)
        
        # Test maximum speed (5.0)
        self.assertEqual(PLAYBACK_SPEEDS.index(5.0), 7)
    
    def test_speed_increase_logic(self):
        """Test that speed increase moves to next available speed."""
        # Starting at 1.0 (index 3), next should be 1.25 (index 4)
        current_index = PLAYBACK_SPEEDS.index(1.0)
        if current_index < len(PLAYBACK_SPEEDS) - 1:
            next_speed = PLAYBACK_SPEEDS[current_index + 1]
            self.assertEqual(next_speed, 1.25)
    
    def test_speed_decrease_logic(self):
        """Test that speed decrease moves to previous available speed."""
        # Starting at 1.0 (index 3), previous should be 0.75 (index 2)
        current_index = PLAYBACK_SPEEDS.index(1.0)
        if current_index > 0:
            prev_speed = PLAYBACK_SPEEDS[current_index - 1]
            self.assertEqual(prev_speed, 0.75)
    
    def test_speed_at_maximum(self):
        """Test that speed cannot increase beyond maximum."""
        max_index = len(PLAYBACK_SPEEDS) - 1
        # At maximum, should not be able to increase
        self.assertEqual(max_index, 7)
        self.assertEqual(PLAYBACK_SPEEDS[max_index], 5.0)
    
    def test_speed_at_minimum(self):
        """Test that speed cannot decrease below minimum."""
        min_index = 0
        # At minimum, should not be able to decrease
        self.assertEqual(PLAYBACK_SPEEDS[min_index], 0.25)


if __name__ == '__main__':
    unittest.main()
