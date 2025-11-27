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
    
    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_scan_empty_directory(self):
        """Test scanning an empty directory."""
        result = scan_videos(self.test_dir)
        self.assertEqual(result, [])
    
    def test_scan_directory_with_videos(self):
        """Test scanning a directory with video files."""
        # Create test video files
        video_files = ['test1.mp4', 'test2.avi', 'test3.mkv']
        for name in video_files:
            Path(self.test_dir, name).touch()
        
        result = scan_videos(self.test_dir)
        self.assertEqual(len(result), 3)
        
        # Check all files are found
        result_names = [Path(p).name for p in result]
        for name in video_files:
            self.assertIn(name, result_names)
    
    def test_scan_ignores_non_video_files(self):
        """Test that non-video files are ignored."""
        # Create mixed files
        Path(self.test_dir, 'video.mp4').touch()
        Path(self.test_dir, 'document.txt').touch()
        Path(self.test_dir, 'image.jpg').touch()
        
        result = scan_videos(self.test_dir)
        self.assertEqual(len(result), 1)
        self.assertTrue(result[0].endswith('.mp4'))
    
    def test_scan_recursive(self):
        """Test recursive directory scanning."""
        # Create subdirectory structure
        subdir = Path(self.test_dir, 'subdir')
        subdir.mkdir()
        
        Path(self.test_dir, 'root.mp4').touch()
        Path(subdir, 'nested.mp4').touch()
        
        result = scan_videos(self.test_dir, recursive=True)
        self.assertEqual(len(result), 2)
    
    def test_scan_non_recursive(self):
        """Test non-recursive directory scanning."""
        # Create subdirectory structure
        subdir = Path(self.test_dir, 'subdir')
        subdir.mkdir()
        
        Path(self.test_dir, 'root.mp4').touch()
        Path(subdir, 'nested.mp4').touch()
        
        result = scan_videos(self.test_dir, recursive=False)
        self.assertEqual(len(result), 1)
        self.assertTrue(result[0].endswith('root.mp4'))
    
    def test_scan_nonexistent_directory(self):
        """Test scanning a nonexistent directory."""
        result = scan_videos('/nonexistent/path')
        self.assertEqual(result, [])
    
    def test_case_insensitive_extensions(self):
        """Test that file extensions are case insensitive."""
        Path(self.test_dir, 'video1.MP4').touch()
        Path(self.test_dir, 'video2.Mp4').touch()
        Path(self.test_dir, 'video3.mp4').touch()
        
        result = scan_videos(self.test_dir)
        self.assertEqual(len(result), 3)
    
    def test_video_extensions_constant(self):
        """Test that all expected extensions are supported."""
        expected = {'.mp4', '.avi', '.mkv', '.mov', '.webm', '.flv', '.wmv'}
        self.assertEqual(VIDEO_EXTENSIONS, expected)


if __name__ == '__main__':
    unittest.main()
