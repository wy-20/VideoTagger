"""Tests for the tag manager module."""
import json
import os
import tempfile
import unittest
from pathlib import Path

from src.core.tag_manager import TagManager


class TestTagManager(unittest.TestCase):
    """Test cases for TagManager class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.data_file = os.path.join(self.test_dir, 'tags.json')
        self.manager = TagManager(self.data_file)
    
    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.test_dir)
    
    def test_add_tag(self):
        """Test adding a tag to a video."""
        video_path = '/path/to/video.mp4'
        self.manager.add_tag(video_path, 'good')
        self.assertIn('good', self.manager.get_tags(video_path))
    
    def test_add_duplicate_tag(self):
        """Test that duplicate tags are not added."""
        video_path = '/path/to/video.mp4'
        self.manager.add_tag(video_path, 'good')
        self.manager.add_tag(video_path, 'good')
        self.assertEqual(self.manager.get_tags(video_path).count('good'), 1)
    
    def test_remove_tag(self):
        """Test removing a tag from a video."""
        video_path = '/path/to/video.mp4'
        self.manager.add_tag(video_path, 'good')
        self.manager.remove_tag(video_path, 'good')
        self.assertNotIn('good', self.manager.get_tags(video_path))
    
    def test_get_tags_empty(self):
        """Test getting tags for a video with no tags."""
        tags = self.manager.get_tags('/nonexistent/video.mp4')
        self.assertEqual(tags, [])
    
    def test_persistence(self):
        """Test that tags are persisted to file."""
        video_path = '/path/to/video.mp4'
        self.manager.add_tag(video_path, 'good')
        
        # Create a new manager instance
        new_manager = TagManager(self.data_file)
        self.assertIn('good', new_manager.get_tags(video_path))
    
    def test_export(self):
        """Test exporting tags to JSON."""
        video_path = '/path/to/video.mp4'
        self.manager.add_tag(video_path, 'good')
        self.manager.add_tag(video_path, 'favorite')
        
        export_path = os.path.join(self.test_dir, 'export.json')
        self.manager.export(export_path)
        
        with open(export_path, 'r', encoding='utf-8') as f:
            exported = json.load(f)
        
        self.assertIn(video_path, exported)
        self.assertEqual(set(exported[video_path]), {'good', 'favorite'})


if __name__ == '__main__':
    unittest.main()
