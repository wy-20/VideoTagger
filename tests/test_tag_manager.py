"""Tests for tag_manager module."""

import json
import tempfile
import unittest
from pathlib import Path

from src.core.tag_manager import TagManager


class TestTagManager(unittest.TestCase):
    """Test cases for TagManager class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.test_file = Path(self.temp_dir) / "test_tags.json"
        self.manager = TagManager(str(self.test_file))
    
    def tearDown(self):
        """Clean up test fixtures."""
        if self.test_file.exists():
            self.test_file.unlink()
        Path(self.temp_dir).rmdir()
    
    def test_add_tag(self):
        """Test adding a tag to a video."""
        result = self.manager.add_tag("/video/test.mp4", "good")
        self.assertTrue(result)
        self.assertEqual(self.manager.get_tags("/video/test.mp4"), ["good"])
    
    def test_add_duplicate_tag(self):
        """Test adding a duplicate tag returns False."""
        self.manager.add_tag("/video/test.mp4", "good")
        result = self.manager.add_tag("/video/test.mp4", "good")
        self.assertFalse(result)
        self.assertEqual(self.manager.get_tags("/video/test.mp4"), ["good"])
    
    def test_add_multiple_tags(self):
        """Test adding multiple tags to a video."""
        self.manager.add_tag("/video/test.mp4", "good")
        self.manager.add_tag("/video/test.mp4", "favorite")
        tags = self.manager.get_tags("/video/test.mp4")
        self.assertEqual(len(tags), 2)
        self.assertIn("good", tags)
        self.assertIn("favorite", tags)
    
    def test_remove_tag(self):
        """Test removing a tag from a video."""
        self.manager.add_tag("/video/test.mp4", "good")
        self.manager.add_tag("/video/test.mp4", "bad")
        
        result = self.manager.remove_tag("/video/test.mp4", "good")
        self.assertTrue(result)
        self.assertEqual(self.manager.get_tags("/video/test.mp4"), ["bad"])
    
    def test_remove_nonexistent_tag(self):
        """Test removing a tag that doesn't exist."""
        result = self.manager.remove_tag("/video/test.mp4", "nonexistent")
        self.assertFalse(result)
    
    def test_get_tags_empty(self):
        """Test getting tags for a video without tags."""
        tags = self.manager.get_tags("/video/nonexistent.mp4")
        self.assertEqual(tags, [])
    
    def test_set_tags(self):
        """Test setting all tags for a video."""
        self.manager.set_tags("/video/test.mp4", ["tag1", "tag2", "tag3"])
        tags = self.manager.get_tags("/video/test.mp4")
        self.assertEqual(len(tags), 3)
    
    def test_set_empty_tags_removes_video(self):
        """Test that setting empty tags removes the video entry."""
        self.manager.add_tag("/video/test.mp4", "good")
        self.manager.set_tags("/video/test.mp4", [])
        self.assertEqual(self.manager.get_tags("/video/test.mp4"), [])
        self.assertNotIn("/video/test.mp4", self.manager.tags)
    
    def test_persistence(self):
        """Test that tags are persisted to file."""
        self.manager.add_tag("/video/test.mp4", "good")
        
        # Create a new manager with the same file
        new_manager = TagManager(str(self.test_file))
        self.assertEqual(new_manager.get_tags("/video/test.mp4"), ["good"])
    
    def test_export(self):
        """Test exporting tags to a file."""
        self.manager.add_tag("/video/test1.mp4", "good")
        self.manager.add_tag("/video/test2.mp4", "bad")
        
        export_file = Path(self.temp_dir) / "export.json"
        self.manager.export(str(export_file))
        
        with open(export_file, 'r', encoding='utf-8') as f:
            exported = json.load(f)
        
        self.assertIn("/video/test1.mp4", exported)
        self.assertIn("/video/test2.mp4", exported)
        
        export_file.unlink()
    
    def test_get_all_videos(self):
        """Test getting all videos with tags."""
        self.manager.add_tag("/video/test1.mp4", "good")
        self.manager.add_tag("/video/test2.mp4", "bad")
        
        videos = self.manager.get_all_videos()
        self.assertEqual(len(videos), 2)
        self.assertIn("/video/test1.mp4", videos)
        self.assertIn("/video/test2.mp4", videos)
    
    def test_clear(self):
        """Test clearing all tags."""
        self.manager.add_tag("/video/test1.mp4", "good")
        self.manager.add_tag("/video/test2.mp4", "bad")
        
        self.manager.clear()
        
        self.assertEqual(self.manager.tags, {})
        self.assertEqual(self.manager.get_all_videos(), [])


if __name__ == "__main__":
    unittest.main()
