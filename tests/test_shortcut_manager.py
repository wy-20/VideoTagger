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
        self.config_file = os.path.join(self.test_dir, 'shortcuts.json')
        self.manager = ShortcutManager(self.config_file)
    
    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.test_dir)
    
    def test_default_shortcuts(self):
        """Test that default shortcuts are loaded."""
        self.assertEqual(self.manager.get_all(), DEFAULT_SHORTCUTS)
    
    def test_set_shortcut(self):
        """Test setting a new shortcut."""
        self.manager.set_shortcut('a', 'awesome')
        self.assertEqual(self.manager.get_tag('a'), 'awesome')
    
    def test_get_tag(self):
        """Test getting a tag by key."""
        self.assertEqual(self.manager.get_tag('1'), 'good')
    
    def test_get_tag_nonexistent(self):
        """Test getting a tag for a non-existent key."""
        self.assertIsNone(self.manager.get_tag('z'))
    
    def test_persistence(self):
        """Test that shortcuts are persisted to file."""
        self.manager.set_shortcut('a', 'awesome')
        
        # Create a new manager instance
        new_manager = ShortcutManager(self.config_file)
        self.assertEqual(new_manager.get_tag('a'), 'awesome')
    
    def test_get_all_returns_copy(self):
        """Test that get_all returns a copy."""
        shortcuts = self.manager.get_all()
        shortcuts['test'] = 'value'
        self.assertIsNone(self.manager.get_tag('test'))


if __name__ == '__main__':
    unittest.main()
