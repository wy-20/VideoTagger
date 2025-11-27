"""Video scanner module for scanning video files in a directory."""
import os
from pathlib import Path
from typing import List

VIDEO_EXTENSIONS = {'.mp4', '.avi', '.mkv', '.mov', '.webm', '.flv', '.wmv'}


def scan_videos(folder_path: str, recursive: bool = True) -> List[str]:
    """
    Scan a folder for video files.
    
    Args:
        folder_path: Path to the folder to scan
        recursive: Whether to scan subdirectories
        
    Returns:
        List of absolute paths to video files
    """
    videos = []
    path = Path(folder_path)
    
    if not path.exists() or not path.is_dir():
        return videos
    
    if recursive:
        for file in path.rglob('*'):
            if file.suffix.lower() in VIDEO_EXTENSIONS:
                videos.append(str(file.absolute()))
    else:
        for file in path.iterdir():
            if file.is_file() and file.suffix.lower() in VIDEO_EXTENSIONS:
                videos.append(str(file.absolute()))
    
    return sorted(videos)
