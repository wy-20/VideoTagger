"""Playlist widget for displaying video files."""

from pathlib import Path
from typing import List, Optional

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QListWidget, QListWidgetItem,
    QPushButton, QLineEdit, QLabel, QHBoxLayout
)
from PyQt6.QtCore import Qt, pyqtSignal


class PlaylistWidget(QWidget):
    """Widget for displaying and managing the video playlist."""
    
    # Signals
    video_selected = pyqtSignal(str)  # Emitted when a video is selected
    folder_requested = pyqtSignal()   # Emitted when user wants to select a folder
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.videos: List[str] = []
        self.video_tags: dict = {}
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # Folder selection button
        self.folder_btn = QPushButton("📁 选择文件夹")
        self.folder_btn.clicked.connect(self.folder_requested.emit)
        layout.addWidget(self.folder_btn)
        
        # Search box
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("搜索视频...")
        self.search_input.textChanged.connect(self.filter_videos)
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)
        
        # Video count label
        self.count_label = QLabel("共 0 个视频")
        layout.addWidget(self.count_label)
        
        # Video list
        self.list_widget = QListWidget()
        self.list_widget.itemClicked.connect(self.on_item_clicked)
        self.list_widget.itemDoubleClicked.connect(self.on_item_clicked)
        layout.addWidget(self.list_widget)
    
    def set_videos(self, videos: List[str], tags: dict = None):
        """Set the list of videos to display.
        
        Args:
            videos: List of video file paths
            tags: Dictionary mapping video paths to their tags
        """
        self.videos = videos
        self.video_tags = tags or {}
        self.update_list()
    
    def update_list(self, filter_text: str = ""):
        """Update the list widget.
        
        Args:
            filter_text: Optional text to filter videos
        """
        self.list_widget.clear()
        filter_lower = filter_text.lower()
        
        visible_count = 0
        for video_path in self.videos:
            file_name = Path(video_path).name
            
            # Apply filter
            if filter_lower and filter_lower not in file_name.lower():
                continue
            
            # Get tags
            tags = self.video_tags.get(video_path, [])
            if tags:
                display_text = f"{file_name} [{', '.join(tags)}]"
            else:
                display_text = file_name
            
            item = QListWidgetItem(display_text)
            item.setData(Qt.ItemDataRole.UserRole, video_path)
            item.setToolTip(video_path)
            self.list_widget.addItem(item)
            visible_count += 1
        
        self.count_label.setText(f"共 {visible_count} 个视频")
    
    def filter_videos(self, text: str):
        """Filter videos by search text.
        
        Args:
            text: Search text
        """
        self.update_list(text)
    
    def on_item_clicked(self, item: QListWidgetItem):
        """Handle item click.
        
        Args:
            item: Clicked list item
        """
        video_path = item.data(Qt.ItemDataRole.UserRole)
        if video_path:
            self.video_selected.emit(video_path)
    
    def update_video_tags(self, video_path: str, tags: List[str]):
        """Update tags for a specific video.
        
        Args:
            video_path: Path to the video
            tags: New tags for the video
        """
        if tags:
            self.video_tags[video_path] = tags
        elif video_path in self.video_tags:
            del self.video_tags[video_path]
        
        # Refresh list
        current_filter = self.search_input.text()
        self.update_list(current_filter)
    
    def get_current_video(self) -> Optional[str]:
        """Get currently selected video path.
        
        Returns:
            Selected video path or None
        """
        current = self.list_widget.currentItem()
        if current:
            return current.data(Qt.ItemDataRole.UserRole)
        return None
    
    def select_video(self, video_path: str):
        """Select a video in the list.
        
        Args:
            video_path: Path to select
        """
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            if item.data(Qt.ItemDataRole.UserRole) == video_path:
                self.list_widget.setCurrentItem(item)
                break
