"""Tests for shortcut_manager module."""

import json
import tempfile
import unittest
from pathlib import Path

from src.core.shortcut_manager import ShortcutManager, DEFAULT_SHORTCUTS


class TestShortcutManager(unittest.TestCase):
    """Test cases for ShortcutManager class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.test_file = Path(self.temp_dir) / "test_shortcuts.json"
        self.manager = ShortcutManager(str(self.test_file))
    
    def tearDown(self):
        """Clean up test fixtures."""
        if self.test_file.exists():
            self.test_file.unlink()
        Path(self.temp_dir).rmdir()
    
    def test_default_shortcuts_loaded(self):
        """Test that default shortcuts are loaded on new file."""
        self.assertEqual(self.manager.shortcuts, DEFAULT_SHORTCUTS)
    
    def test_set_shortcut(self):
        """Test setting a new shortcut."""
        self.manager.set_shortcut("q", "quality")
        self.assertEqual(self.manager.get_tag("q"), "quality")
    
    def test_set_shortcut_override(self):
        """Test that setting a shortcut overrides existing."""
        self.manager.set_shortcut("1", "new_tag")
        self.assertEqual(self.manager.get_tag("1"), "new_tag")
    
    def test_get_tag(self):
        """Test getting a tag by shortcut key."""
        tag = self.manager.get_tag("1")
        self.assertEqual(tag, "good")
    
    def test_get_tag_nonexistent(self):
        """Test getting a tag for nonexistent key."""
        tag = self.manager.get_tag("nonexistent")
        self.assertIsNone(tag)
    
    def test_remove_shortcut(self):
        """Test removing a shortcut."""
        result = self.manager.remove_shortcut("1")
        self.assertTrue(result)
        self.assertIsNone(self.manager.get_tag("1"))
    
    def test_remove_nonexistent_shortcut(self):
        """Test removing a nonexistent shortcut."""
        result = self.manager.remove_shortcut("nonexistent")
        self.assertFalse(result)
    
    def test_get_all(self):
        """Test getting all shortcuts."""
        all_shortcuts = self.manager.get_all()
        self.assertEqual(all_shortcuts, DEFAULT_SHORTCUTS)
        
        # Verify it's a copy
        all_shortcuts["x"] = "test"
        self.assertNotIn("x", self.manager.shortcuts)
    
    def test_reset_to_defaults(self):
        """Test resetting to default shortcuts."""
        self.manager.set_shortcut("x", "custom")
        self.manager.remove_shortcut("1")
        
        self.manager.reset_to_defaults()
        
        self.assertEqual(self.manager.shortcuts, DEFAULT_SHORTCUTS)
        self.assertIsNone(self.manager.get_tag("x"))
    
    def test_persistence(self):
        """Test that shortcuts are persisted to file."""
        self.manager.set_shortcut("x", "custom")
        
        # Create a new manager with the same file
        new_manager = ShortcutManager(str(self.test_file))
        self.assertEqual(new_manager.get_tag("x"), "custom")


if __name__ == "__main__":
    unittest.main()
