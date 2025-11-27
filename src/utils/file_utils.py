"""File utility functions."""

import os
from pathlib import Path
from typing import Optional


def get_file_name(path: str) -> str:
    """Get file name from path.
    
    Args:
        path: Full file path
        
    Returns:
        File name without directory
    """
    return Path(path).name


def get_file_extension(path: str) -> str:
    """Get file extension from path.
    
    Args:
        path: Full file path
        
    Returns:
        File extension (lowercase, including dot)
    """
    return Path(path).suffix.lower()


def ensure_directory(path: str) -> None:
    """Ensure directory exists, create if not.
    
    Args:
        path: Directory path
    """
    Path(path).mkdir(parents=True, exist_ok=True)


def get_app_data_dir() -> str:
    """Get application data directory.
    
    Returns:
        Path to application data directory
    """
    # Use XDG_DATA_HOME on Linux, fallback to ~/.local/share
    xdg_data = os.environ.get('XDG_DATA_HOME', os.path.expanduser('~/.local/share'))
    app_dir = os.path.join(xdg_data, 'video-tagger')
    ensure_directory(app_dir)
    return app_dir


def get_config_dir() -> str:
    """Get application config directory.
    
    Returns:
        Path to application config directory
    """
    # Use XDG_CONFIG_HOME on Linux, fallback to ~/.config
    xdg_config = os.environ.get('XDG_CONFIG_HOME', os.path.expanduser('~/.config'))
    config_dir = os.path.join(xdg_config, 'video-tagger')
    ensure_directory(config_dir)
    return config_dir
