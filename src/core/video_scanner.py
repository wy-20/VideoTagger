"""Video scanner module for scanning video files in directories."""

import os
from pathlib import Path
from typing import List

VIDEO_EXTENSIONS = {'.mp4', '.avi', '.mkv', '.mov', '.webm', '.flv', '.wmv'}


def scan_videos(folder_path: str, recursive: bool = True) -> List[str]:
    """Scan folder for all video files.
    
    Args:
        folder_path: Path to the folder to scan
        recursive: If True, scan subdirectories recursively
        
    Returns:
        List of absolute paths to video files, sorted alphabetically
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


def get_video_duration(video_path: str) -> float:
    """Get duration of a video file in seconds.
    
    Note: This requires VLC to be installed. Returns 0 if duration cannot be determined.
    
    Args:
        video_path: Path to the video file
        
    Returns:
        Duration in seconds, or 0 if cannot be determined
    """
    try:
        import vlc
        instance = vlc.Instance('--no-xlib')
        media = instance.media_new(video_path)
        media.parse()
        duration_ms = media.get_duration()
        return duration_ms / 1000.0 if duration_ms > 0 else 0
    except Exception:
        return 0


def format_duration(seconds: float) -> str:
    """Format duration in seconds to HH:MM:SS or MM:SS format.
    
    Args:
        seconds: Duration in seconds
        
    Returns:
        Formatted duration string
    """
    if seconds <= 0:
        return "00:00"
    
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    else:
        return f"{minutes:02d}:{secs:02d}"
