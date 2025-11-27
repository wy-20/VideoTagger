"""Tag manager module for managing video tags."""
import json
from pathlib import Path
from typing import Dict, List


class TagManager:
    """Manages tags for video files with JSON persistence."""
    
    def __init__(self, data_file: str = "data/tags.json"):
        """
        Initialize the TagManager.
        
        Args:
            data_file: Path to the JSON file for storing tags
        """
        self.data_file = Path(data_file)
        self.tags: Dict[str, List[str]] = {}
        self.load()
    
    def load(self):
        """Load tags from the data file."""
        if self.data_file.exists():
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    self.tags = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.tags = {}
    
    def save(self):
        """Save tags to the data file."""
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
            if not self.tags[video_path]:
                del self.tags[video_path]
            self.save()
    
    def toggle_tag(self, video_path: str, tag: str) -> bool:
        """
        Toggle a tag on a video (add if not present, remove if present).
        
        Args:
            video_path: Path to the video file
            tag: Tag to toggle
            
        Returns:
            True if tag was added, False if tag was removed
        """
        if video_path in self.tags and tag in self.tags[video_path]:
            self.remove_tag(video_path, tag)
            return False
        else:
            self.add_tag(video_path, tag)
            return True
    
    def clear_tags(self, video_path: str):
        """
        Remove all tags from a video.
        
        Args:
            video_path: Path to the video file
        """
        if video_path in self.tags:
            del self.tags[video_path]
            self.save()
    
    def has_tag(self, video_path: str, tag: str) -> bool:
        """
        Check if a video has a specific tag.
        
        Args:
            video_path: Path to the video file
            tag: Tag to check
            
        Returns:
            True if video has the tag, False otherwise
        """
        return video_path in self.tags and tag in self.tags[video_path]
    
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
            output_path: Path to the output JSON file
        """
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.tags, f, indent=2, ensure_ascii=False)
    
    def get_all_tags(self) -> Dict[str, List[str]]:
        """
        Get all video-tag mappings.
        
        Returns:
            Dictionary mapping video paths to their tags
        """
        return self.tags.copy()
