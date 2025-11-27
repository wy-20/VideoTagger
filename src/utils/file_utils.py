"""File utility functions."""
import os
from pathlib import Path
from typing import Optional


def get_file_size(file_path: str) -> int:
    """
    Get the size of a file in bytes.
    
    Args:
        file_path: Path to the file
        
    Returns:
        File size in bytes, or 0 if file doesn't exist
    """
    try:
        return os.path.getsize(file_path)
    except OSError:
        return 0


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human-readable format.
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Human-readable size string
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} PB"


def ensure_directory(directory: str) -> bool:
    """
    Ensure a directory exists, creating it if necessary.
    
    Args:
        directory: Path to the directory
        
    Returns:
        True if directory exists or was created, False on error
    """
    try:
        Path(directory).mkdir(parents=True, exist_ok=True)
        return True
    except OSError:
        return False


def get_file_extension(file_path: str) -> str:
    """
    Get the file extension (lowercase, without dot).
    
    Args:
        file_path: Path to the file
        
    Returns:
        File extension in lowercase
    """
    return Path(file_path).suffix.lower().lstrip('.')


def is_video_file(file_path: str) -> bool:
    """
    Check if a file is a supported video file.
    
    Args:
        file_path: Path to the file
        
    Returns:
        True if file is a supported video format
    """
    video_extensions = {'mp4', 'avi', 'mkv', 'mov', 'webm', 'flv', 'wmv'}
    return get_file_extension(file_path) in video_extensions
