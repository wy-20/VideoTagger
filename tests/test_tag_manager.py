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
        self.data_file = os.path.join(self.test_dir, 'data', 'tags.json')
        self.manager = TagManager(self.data_file)
    
    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_add_tag(self):
        """Test adding a tag to a video."""
        video_path = '/path/to/video.mp4'
        self.manager.add_tag(video_path, 'good')
        
        tags = self.manager.get_tags(video_path)
        self.assertEqual(tags, ['good'])
    
    def test_add_multiple_tags(self):
        """Test adding multiple tags to a video."""
        video_path = '/path/to/video.mp4'
        self.manager.add_tag(video_path, 'good')
        self.manager.add_tag(video_path, 'favorite')
        
        tags = self.manager.get_tags(video_path)
        self.assertEqual(set(tags), {'good', 'favorite'})
    
    def test_add_duplicate_tag(self):
        """Test that duplicate tags are not added."""
        video_path = '/path/to/video.mp4'
        self.manager.add_tag(video_path, 'good')
        self.manager.add_tag(video_path, 'good')
        
        tags = self.manager.get_tags(video_path)
        self.assertEqual(tags, ['good'])
    
    def test_remove_tag(self):
        """Test removing a tag from a video."""
        video_path = '/path/to/video.mp4'
        self.manager.add_tag(video_path, 'good')
        self.manager.add_tag(video_path, 'favorite')
        self.manager.remove_tag(video_path, 'good')
        
        tags = self.manager.get_tags(video_path)
        self.assertEqual(tags, ['favorite'])
    
    def test_remove_last_tag_removes_video(self):
        """Test that removing the last tag removes the video entry."""
        video_path = '/path/to/video.mp4'
        self.manager.add_tag(video_path, 'good')
        self.manager.remove_tag(video_path, 'good')
        
        self.assertNotIn(video_path, self.manager.tags)
    
    def test_get_tags_empty(self):
        """Test getting tags for a video with no tags."""
        tags = self.manager.get_tags('/nonexistent/video.mp4')
        self.assertEqual(tags, [])
    
    def test_persistence(self):
        """Test that tags are persisted to file."""
        video_path = '/path/to/video.mp4'
        self.manager.add_tag(video_path, 'good')
        
        # Create new manager instance
        new_manager = TagManager(self.data_file)
        tags = new_manager.get_tags(video_path)
        self.assertEqual(tags, ['good'])
    
    def test_export(self):
        """Test exporting tags to a file."""
        video_path = '/path/to/video.mp4'
        self.manager.add_tag(video_path, 'good')
        self.manager.add_tag(video_path, 'favorite')
        
        export_path = os.path.join(self.test_dir, 'export.json')
        self.manager.export(export_path)
        
        with open(export_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.assertEqual(data[video_path], ['good', 'favorite'])
    
    def test_get_all_tags(self):
        """Test getting all video-tag mappings."""
        self.manager.add_tag('/path/to/video1.mp4', 'good')
        self.manager.add_tag('/path/to/video2.mp4', 'bad')
        
        all_tags = self.manager.get_all_tags()
        self.assertEqual(len(all_tags), 2)
        self.assertIn('/path/to/video1.mp4', all_tags)
        self.assertIn('/path/to/video2.mp4', all_tags)
    
    def test_toggle_tag_add(self):
        """Test toggling a tag adds it when not present."""
        video_path = '/path/to/video.mp4'
        result = self.manager.toggle_tag(video_path, 'good')
        
        self.assertTrue(result)
        self.assertEqual(self.manager.get_tags(video_path), ['good'])
    
    def test_toggle_tag_remove(self):
        """Test toggling a tag removes it when present."""
        video_path = '/path/to/video.mp4'
        self.manager.add_tag(video_path, 'good')
        result = self.manager.toggle_tag(video_path, 'good')
        
        self.assertFalse(result)
        self.assertEqual(self.manager.get_tags(video_path), [])
    
    def test_toggle_tag_multiple(self):
        """Test toggling tags multiple times."""
        video_path = '/path/to/video.mp4'
        
        # First toggle adds the tag
        self.manager.toggle_tag(video_path, 'good')
        self.assertTrue(self.manager.has_tag(video_path, 'good'))
        
        # Second toggle removes the tag
        self.manager.toggle_tag(video_path, 'good')
        self.assertFalse(self.manager.has_tag(video_path, 'good'))
        
        # Third toggle adds it back
        self.manager.toggle_tag(video_path, 'good')
        self.assertTrue(self.manager.has_tag(video_path, 'good'))
    
    def test_clear_tags(self):
        """Test clearing all tags from a video."""
        video_path = '/path/to/video.mp4'
        self.manager.add_tag(video_path, 'good')
        self.manager.add_tag(video_path, 'favorite')
        self.manager.add_tag(video_path, 'interesting')
        
        self.manager.clear_tags(video_path)
        
        self.assertEqual(self.manager.get_tags(video_path), [])
        self.assertNotIn(video_path, self.manager.tags)
    
    def test_clear_tags_nonexistent(self):
        """Test clearing tags from a video with no tags."""
        video_path = '/path/to/video.mp4'
        # Should not raise an error
        self.manager.clear_tags(video_path)
        self.assertEqual(self.manager.get_tags(video_path), [])
    
    def test_has_tag(self):
        """Test checking if a video has a specific tag."""
        video_path = '/path/to/video.mp4'
        self.manager.add_tag(video_path, 'good')
        
        self.assertTrue(self.manager.has_tag(video_path, 'good'))
        self.assertFalse(self.manager.has_tag(video_path, 'bad'))
    
    def test_has_tag_nonexistent_video(self):
        """Test has_tag returns False for nonexistent video."""
        self.assertFalse(self.manager.has_tag('/nonexistent/video.mp4', 'good'))


if __name__ == '__main__':
    unittest.main()
