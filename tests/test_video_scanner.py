"""Tests for the video scanner module."""
import os
import tempfile
import unittest
from pathlib import Path

from src.core.video_scanner import scan_videos, VIDEO_EXTENSIONS


class TestVideoScanner(unittest.TestCase):
    """Test cases for video_scanner module."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        
        # Create test video files
        self.video_files = ['video1.mp4', 'video2.mkv', 'video3.avi']
        for video in self.video_files:
            Path(self.test_dir, video).touch()
        
        # Create a subdirectory with videos
        self.sub_dir = Path(self.test_dir, 'subdir')
        self.sub_dir.mkdir()
        Path(self.sub_dir, 'sub_video.mp4').touch()
        
        # Create non-video files
        Path(self.test_dir, 'document.txt').touch()
        Path(self.test_dir, 'image.jpg').touch()
    
    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.test_dir)
    
    def test_scan_videos_recursive(self):
        """Test recursive video scanning."""
        videos = scan_videos(self.test_dir, recursive=True)
        self.assertEqual(len(videos), 4)  # 3 in root + 1 in subdir
    
    def test_scan_videos_non_recursive(self):
        """Test non-recursive video scanning."""
        videos = scan_videos(self.test_dir, recursive=False)
        self.assertEqual(len(videos), 3)  # Only files in root
    
    def test_scan_videos_filters_non_video(self):
        """Test that non-video files are filtered out."""
        videos = scan_videos(self.test_dir)
        for video in videos:
            self.assertTrue(
                Path(video).suffix.lower() in VIDEO_EXTENSIONS,
                f"Non-video file found: {video}"
            )
    
    def test_scan_empty_directory(self):
        """Test scanning an empty directory."""
        empty_dir = tempfile.mkdtemp()
        try:
            videos = scan_videos(empty_dir)
            self.assertEqual(len(videos), 0)
        finally:
            os.rmdir(empty_dir)
    
    def test_scan_nonexistent_directory(self):
        """Test scanning a non-existent directory."""
        videos = scan_videos('/nonexistent/path')
        self.assertEqual(len(videos), 0)
    
    def test_results_are_sorted(self):
        """Test that results are sorted."""
        videos = scan_videos(self.test_dir, recursive=False)
        self.assertEqual(videos, sorted(videos))


if __name__ == '__main__':
    unittest.main()
