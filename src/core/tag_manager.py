"""Tag manager module for managing video tags."""

import json
from pathlib import Path
from typing import Dict, List


class TagManager:
    """Manages video tags with JSON persistence."""
    
    def __init__(self, data_file: str = "data/tags.json"):
        """Initialize TagManager.
        
        Args:
            data_file: Path to the JSON file for storing tags
        """
        self.data_file = Path(data_file)
        self.tags: Dict[str, List[str]] = {}
        self.load()
    
    def load(self) -> None:
        """Load tags from JSON file."""
        if self.data_file.exists():
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    self.tags = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.tags = {}
    
    def save(self) -> None:
        """Save tags to JSON file."""
        self.data_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.tags, f, indent=2, ensure_ascii=False)
    
    def add_tag(self, video_path: str, tag: str) -> bool:
        """Add a tag to a video.
        
        Args:
            video_path: Path to the video file
            tag: Tag to add
            
        Returns:
            True if tag was added, False if already exists
        """
        if video_path not in self.tags:
            self.tags[video_path] = []
        if tag not in self.tags[video_path]:
            self.tags[video_path].append(tag)
            self.save()
            return True
        return False
    
    def remove_tag(self, video_path: str, tag: str) -> bool:
        """Remove a tag from a video.
        
        Args:
            video_path: Path to the video file
            tag: Tag to remove
            
        Returns:
            True if tag was removed, False if not found
        """
        if video_path in self.tags and tag in self.tags[video_path]:
            self.tags[video_path].remove(tag)
            if not self.tags[video_path]:
                del self.tags[video_path]
            self.save()
            return True
        return False
    
    def get_tags(self, video_path: str) -> List[str]:
        """Get all tags for a video.
        
        Args:
            video_path: Path to the video file
            
        Returns:
            List of tags for the video
        """
        return self.tags.get(video_path, []).copy()
    
    def set_tags(self, video_path: str, tags: List[str]) -> None:
        """Set all tags for a video.
        
        Args:
            video_path: Path to the video file
            tags: List of tags to set
        """
        if tags:
            self.tags[video_path] = list(set(tags))
        elif video_path in self.tags:
            del self.tags[video_path]
        self.save()
    
    def get_all_videos(self) -> List[str]:
        """Get all video paths that have tags.
        
        Returns:
            List of video paths with tags
        """
        return list(self.tags.keys())
    
    def export(self, output_path: str) -> None:
        """Export tags to a JSON file.
        
        Args:
            output_path: Path to the output JSON file
        """
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.tags, f, indent=2, ensure_ascii=False)
    
    def clear(self) -> None:
        """Clear all tags."""
        self.tags = {}
        self.save()
