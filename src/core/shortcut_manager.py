"""Shortcut manager module for managing keyboard shortcuts."""
import json
from pathlib import Path
from typing import Dict, Optional

DEFAULT_SHORTCUTS = {
    "1": "good",
    "2": "bad",
    "3": "interesting",
    "4": "review_later",
    "5": "favorite",
}


class ShortcutManager:
    """Manages keyboard shortcuts with JSON persistence."""
    
    def __init__(self, config_file: str = "config/shortcuts.json"):
        """
        Initialize the shortcut manager.
        
        Args:
            config_file: Path to the JSON file for storing shortcuts
        """
        self.config_file = Path(config_file)
        self.shortcuts: Dict[str, str] = {}
        self.load()
    
    def load(self):
        """Load shortcut configuration from file."""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.shortcuts = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.shortcuts = DEFAULT_SHORTCUTS.copy()
                self.save()
        else:
            self.shortcuts = DEFAULT_SHORTCUTS.copy()
            self.save()
    
    def save(self):
        """Save shortcut configuration to file."""
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.shortcuts, f, indent=2)
    
    def set_shortcut(self, key: str, tag: str):
        """
        Set a shortcut key mapping.
        
        Args:
            key: Keyboard key
            tag: Tag to associate with the key
        """
        self.shortcuts[key] = tag
        self.save()
    
    def get_tag(self, key: str) -> Optional[str]:
        """
        Get the tag for a shortcut key.
        
        Args:
            key: Keyboard key
            
        Returns:
            Tag associated with the key, or None if not found
        """
        return self.shortcuts.get(key)
    
    def get_all(self) -> Dict[str, str]:
        """
        Get all shortcut mappings.
        
        Returns:
            Dictionary of key-to-tag mappings
        """
        return self.shortcuts.copy()
