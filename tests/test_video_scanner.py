"""Tests for video_scanner module."""

import os
import tempfile
import unittest
from pathlib import Path

from src.core.video_scanner import scan_videos, format_duration, VIDEO_EXTENSIONS


class TestVideoScanner(unittest.TestCase):
    """Test cases for video_scanner module."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        
        # Create test video files (empty files with video extensions)
        self.test_files = [
            "video1.mp4",
            "video2.avi",
            "video3.mkv",
            "document.txt",
            "image.png",
        ]
        
        for filename in self.test_files:
            path = Path(self.temp_dir) / filename
            path.touch()
        
        # Create a subdirectory with a video
        subdir = Path(self.temp_dir) / "subdir"
        subdir.mkdir()
        (subdir / "subvideo.mp4").touch()
    
    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_scan_videos_recursive(self):
        """Test scanning videos recursively."""
        videos = scan_videos(self.temp_dir, recursive=True)
        
        # Should find 4 video files (3 in root + 1 in subdir)
        self.assertEqual(len(videos), 4)
        
        # Check that all are video files
        for video in videos:
            ext = Path(video).suffix.lower()
            self.assertIn(ext, VIDEO_EXTENSIONS)
    
    def test_scan_videos_non_recursive(self):
        """Test scanning videos non-recursively."""
        videos = scan_videos(self.temp_dir, recursive=False)
        
        # Should find only 3 video files in root
        self.assertEqual(len(videos), 3)
    
    def test_scan_videos_sorted(self):
        """Test that results are sorted alphabetically."""
        videos = scan_videos(self.temp_dir, recursive=False)
        
        self.assertEqual(videos, sorted(videos))
    
    def test_scan_videos_empty_folder(self):
        """Test scanning an empty folder."""
        empty_dir = Path(self.temp_dir) / "empty"
        empty_dir.mkdir()
        
        videos = scan_videos(str(empty_dir))
        self.assertEqual(videos, [])
    
    def test_scan_videos_nonexistent_folder(self):
        """Test scanning a nonexistent folder."""
        videos = scan_videos("/nonexistent/folder")
        self.assertEqual(videos, [])
    
    def test_scan_videos_absolute_paths(self):
        """Test that returned paths are absolute."""
        videos = scan_videos(self.temp_dir)
        
        for video in videos:
            self.assertTrue(Path(video).is_absolute())


class TestFormatDuration(unittest.TestCase):
    """Test cases for format_duration function."""
    
    def test_format_seconds(self):
        """Test formatting seconds."""
        self.assertEqual(format_duration(5), "00:05")
        self.assertEqual(format_duration(59), "00:59")
    
    def test_format_minutes(self):
        """Test formatting minutes."""
        self.assertEqual(format_duration(60), "01:00")
        self.assertEqual(format_duration(125), "02:05")
    
    def test_format_hours(self):
        """Test formatting hours."""
        self.assertEqual(format_duration(3600), "01:00:00")
        self.assertEqual(format_duration(3665), "01:01:05")
    
    def test_format_zero(self):
        """Test formatting zero."""
        self.assertEqual(format_duration(0), "00:00")
    
    def test_format_negative(self):
        """Test formatting negative values."""
        self.assertEqual(format_duration(-10), "00:00")


if __name__ == "__main__":
    unittest.main()
