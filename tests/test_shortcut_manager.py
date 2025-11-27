"""Tests for the shortcut manager module."""
import json
import os
import tempfile
import unittest
from pathlib import Path

from src.core.shortcut_manager import ShortcutManager, DEFAULT_SHORTCUTS


class TestShortcutManager(unittest.TestCase):
    """Test cases for ShortcutManager class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.config_file = os.path.join(self.test_dir, 'config', 'shortcuts.json')
        self.manager = ShortcutManager(self.config_file)
    
    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_default_shortcuts(self):
        """Test that default shortcuts are loaded."""
        shortcuts = self.manager.get_all()
        self.assertEqual(shortcuts, DEFAULT_SHORTCUTS)
    
    def test_set_shortcut(self):
        """Test setting a new shortcut."""
        self.manager.set_shortcut('q', 'questionable')
        
        tag = self.manager.get_tag('q')
        self.assertEqual(tag, 'questionable')
    
    def test_get_tag(self):
        """Test getting a tag by key."""
        tag = self.manager.get_tag('1')
        self.assertEqual(tag, 'good')
    
    def test_get_tag_nonexistent(self):
        """Test getting a nonexistent tag."""
        tag = self.manager.get_tag('z')
        self.assertIsNone(tag)
    
    def test_remove_shortcut(self):
        """Test removing a shortcut."""
        self.manager.remove_shortcut('1')
        
        tag = self.manager.get_tag('1')
        self.assertIsNone(tag)
    
    def test_persistence(self):
        """Test that shortcuts are persisted to file."""
        self.manager.set_shortcut('q', 'questionable')
        
        # Create new manager instance
        new_manager = ShortcutManager(self.config_file)
        tag = new_manager.get_tag('q')
        self.assertEqual(tag, 'questionable')
    
    def test_reset_to_defaults(self):
        """Test resetting shortcuts to defaults."""
        self.manager.set_shortcut('q', 'questionable')
        self.manager.remove_shortcut('1')
        
        self.manager.reset_to_defaults()
        
        shortcuts = self.manager.get_all()
        self.assertEqual(shortcuts, DEFAULT_SHORTCUTS)
    
    def test_get_all(self):
        """Test getting all shortcuts."""
        shortcuts = self.manager.get_all()
        self.assertIsInstance(shortcuts, dict)
        self.assertEqual(len(shortcuts), 5)


if __name__ == '__main__':
    unittest.main()
