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
    """Manages keyboard shortcut to tag mappings."""
    
    def __init__(self, config_file: str = "config/shortcuts.json"):
        """Initialize ShortcutManager.
        
        Args:
            config_file: Path to the JSON file for storing shortcuts
        """
        self.config_file = Path(config_file)
        self.shortcuts: Dict[str, str] = {}
        self.load()
    
    def load(self) -> None:
        """Load shortcuts from JSON file."""
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
    
    def save(self) -> None:
        """Save shortcuts to JSON file."""
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.shortcuts, f, indent=2)
    
    def set_shortcut(self, key: str, tag: str) -> None:
        """Set a shortcut key to tag mapping.
        
        Args:
            key: Keyboard key
            tag: Tag name to map to
        """
        self.shortcuts[key] = tag
        self.save()
    
    def remove_shortcut(self, key: str) -> bool:
        """Remove a shortcut mapping.
        
        Args:
            key: Keyboard key to remove
            
        Returns:
            True if removed, False if not found
        """
        if key in self.shortcuts:
            del self.shortcuts[key]
            self.save()
            return True
        return False
    
    def get_tag(self, key: str) -> Optional[str]:
        """Get tag for a shortcut key.
        
        Args:
            key: Keyboard key
            
        Returns:
            Tag name or None if not found
        """
        return self.shortcuts.get(key)
    
    def get_all(self) -> Dict[str, str]:
        """Get all shortcut mappings.
        
        Returns:
            Dictionary of key to tag mappings
        """
        return self.shortcuts.copy()
    
    def reset_to_defaults(self) -> None:
        """Reset shortcuts to default values."""
        self.shortcuts = DEFAULT_SHORTCUTS.copy()
        self.save()
