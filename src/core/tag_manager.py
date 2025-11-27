"""Tag manager module for managing video tags."""
import json
from pathlib import Path
from typing import Dict, List


class TagManager:
    """Manages video tags with JSON persistence."""
    
    def __init__(self, data_file: str = "data/tags.json"):
        """
        Initialize the tag manager.
        
        Args:
            data_file: Path to the JSON file for storing tags
        """
        self.data_file = Path(data_file)
        self.tags: Dict[str, List[str]] = {}
        self.load()
    
    def load(self):
        """Load tag data from file."""
        if self.data_file.exists():
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    self.tags = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.tags = {}
    
    def save(self):
        """Save tag data to file."""
        self.data_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.tags, f, indent=2, ensure_ascii=False)
    
    def add_tag(self, video_path: str, tag: str):
        """
        Add a tag to a video.
        
        Args:
            video_path: Path to the video file
            tag: Tag to add
        """
        if video_path not in self.tags:
            self.tags[video_path] = []
        if tag not in self.tags[video_path]:
            self.tags[video_path].append(tag)
            self.save()
    
    def remove_tag(self, video_path: str, tag: str):
        """
        Remove a tag from a video.
        
        Args:
            video_path: Path to the video file
            tag: Tag to remove
        """
        if video_path in self.tags and tag in self.tags[video_path]:
            self.tags[video_path].remove(tag)
            self.save()
    
    def get_tags(self, video_path: str) -> List[str]:
        """
        Get all tags for a video.
        
        Args:
            video_path: Path to the video file
            
        Returns:
            List of tags for the video
        """
        return self.tags.get(video_path, [])
    
    def export(self, output_path: str):
        """
        Export tags to a JSON file.
        
        Args:
            output_path: Path to save the exported JSON
        """
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.tags, f, indent=2, ensure_ascii=False)
