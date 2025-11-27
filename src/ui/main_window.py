"""Main window for Video Tagger application."""

import sys
from pathlib import Path
from typing import Dict

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QFileDialog, QMessageBox, QSplitter, QStatusBar
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QShortcut, QKeySequence

from src.core.video_scanner import scan_videos
from src.core.tag_manager import TagManager
from src.core.shortcut_manager import ShortcutManager
from src.ui.playlist import PlaylistWidget
from src.ui.player import VideoPlayerWidget
from src.ui.tag_panel import TagPanelWidget
from src.ui.settings_dialog import SettingsDialog


class MainWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Video Tagger - 视频标签工具")
        self.setGeometry(100, 100, 1200, 700)
        
        # Initialize managers
        self.tag_manager = TagManager()
        self.shortcut_manager = ShortcutManager()
        
        self.videos = []
        self.current_video = None
        self.shortcuts_map: Dict[str, QShortcut] = {}
        
        self.init_ui()
        self.setup_shortcuts()
        self.update_status("就绪")
    
    def init_ui(self):
        """Initialize the UI."""
        central = QWidget()
        self.setCentralWidget(central)
        
        # Main layout with splitter
        main_layout = QHBoxLayout(central)
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left panel: Playlist
        self.playlist_widget = PlaylistWidget()
        self.playlist_widget.video_selected.connect(self.on_video_selected)
        self.playlist_widget.folder_requested.connect(self.select_folder)
        self.playlist_widget.setMaximumWidth(350)
        self.playlist_widget.setMinimumWidth(200)
        
        # Center panel: Video player
        self.player_widget = VideoPlayerWidget()
        
        # Right panel: Tag panel
        self.tag_panel = TagPanelWidget()
        self.tag_panel.tag_added.connect(self.add_tag_to_current)
        self.tag_panel.tag_removed.connect(self.remove_tag_from_current)
        self.tag_panel.export_requested.connect(self.export_tags)
        self.tag_panel.settings_requested.connect(self.show_settings)
        self.tag_panel.setMaximumWidth(300)
        self.tag_panel.setMinimumWidth(200)
        
        # Update tag panel with shortcuts
        self.tag_panel.set_shortcuts(self.shortcut_manager.get_all())
        
        # Add widgets to splitter
        splitter.addWidget(self.playlist_widget)
        splitter.addWidget(self.player_widget)
        splitter.addWidget(self.tag_panel)
        
        # Set initial sizes (left:center:right ratio)
        splitter.setSizes([250, 600, 250])
        
        main_layout.addWidget(splitter)
        
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
    
    def setup_shortcuts(self):
        """Setup keyboard shortcuts for tagging."""
        # Clear existing shortcuts
        for shortcut in self.shortcuts_map.values():
            shortcut.setEnabled(False)
            shortcut.deleteLater()
        self.shortcuts_map.clear()
        
        # Create shortcuts from config
        for key, tag in self.shortcut_manager.get_all().items():
            try:
                shortcut = QShortcut(QKeySequence(key), self)
                shortcut.activated.connect(
                    lambda t=tag: self.add_tag_to_current(t)
                )
                self.shortcuts_map[key] = shortcut
            except Exception as e:
                print(f"Error creating shortcut for key '{key}': {e}")
        
        # Spacebar for play/pause
        space_shortcut = QShortcut(QKeySequence(Qt.Key.Key_Space), self)
        space_shortcut.activated.connect(self.player_widget.toggle_play)
        self.shortcuts_map["Space"] = space_shortcut
    
    def select_folder(self):
        """Open folder selection dialog."""
        folder = QFileDialog.getExistingDirectory(
            self, 
            "选择视频文件夹",
            "",
            QFileDialog.Option.ShowDirsOnly
        )
        
        if folder:
            self.load_folder(folder)
    
    def load_folder(self, folder_path: str):
        """Load videos from a folder.
        
        Args:
            folder_path: Path to the folder
        """
        self.update_status(f"正在扫描: {folder_path}")
        
        self.videos = scan_videos(folder_path)
        
        # Get tags for all videos
        video_tags = {}
        for video in self.videos:
            tags = self.tag_manager.get_tags(video)
            if tags:
                video_tags[video] = tags
        
        self.playlist_widget.set_videos(self.videos, video_tags)
        self.update_status(f"已加载 {len(self.videos)} 个视频")
    
    def on_video_selected(self, video_path: str):
        """Handle video selection.
        
        Args:
            video_path: Path to the selected video
        """
        self.current_video = video_path
        self.player_widget.play_video(video_path)
        self.update_current_tags()
        self.update_status(f"正在播放: {Path(video_path).name}")
    
    def add_tag_to_current(self, tag: str):
        """Add a tag to the current video.
        
        Args:
            tag: Tag to add
        """
        if not self.current_video:
            self.update_status("请先选择视频")
            return
        
        if self.tag_manager.add_tag(self.current_video, tag):
            self.update_current_tags()
            self.update_playlist_tags()
            self.update_status(f"已添加标签: {tag}")
        else:
            self.update_status(f"标签已存在: {tag}")
    
    def remove_tag_from_current(self, tag: str):
        """Remove a tag from the current video.
        
        Args:
            tag: Tag to remove
        """
        if not self.current_video:
            self.update_status("请先选择视频")
            return
        
        if self.tag_manager.remove_tag(self.current_video, tag):
            self.update_current_tags()
            self.update_playlist_tags()
            self.update_status(f"已删除标签: {tag}")
        else:
            self.update_status(f"标签不存在: {tag}")
    
    def update_current_tags(self):
        """Update the tag display for current video."""
        if self.current_video:
            tags = self.tag_manager.get_tags(self.current_video)
            self.tag_panel.set_current_tags(tags)
        else:
            self.tag_panel.clear_tags()
    
    def update_playlist_tags(self):
        """Update tags in the playlist display."""
        if self.current_video:
            tags = self.tag_manager.get_tags(self.current_video)
            self.playlist_widget.update_video_tags(self.current_video, tags)
    
    def export_tags(self):
        """Export tags to JSON file."""
        path, _ = QFileDialog.getSaveFileName(
            self,
            "导出标签",
            "tags.json",
            "JSON Files (*.json);;All Files (*)"
        )
        
        if path:
            try:
                self.tag_manager.export(path)
                self.update_status(f"标签已导出到: {path}")
                QMessageBox.information(
                    self,
                    "导出成功",
                    f"标签数据已成功导出到:\n{path}"
                )
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "导出失败",
                    f"导出失败: {str(e)}"
                )
    
    def show_settings(self):
        """Show settings dialog."""
        dialog = SettingsDialog(self.shortcut_manager.get_all(), self)
        
        if dialog.exec():
            new_shortcuts = dialog.get_shortcuts()
            
            # Update shortcut manager
            for key in list(self.shortcut_manager.shortcuts.keys()):
                if key not in new_shortcuts:
                    self.shortcut_manager.remove_shortcut(key)
            
            for key, tag in new_shortcuts.items():
                self.shortcut_manager.set_shortcut(key, tag)
            
            # Refresh UI
            self.tag_panel.set_shortcuts(self.shortcut_manager.get_all())
            self.setup_shortcuts()
            self.update_status("快捷键设置已更新")
    
    def update_status(self, message: str):
        """Update status bar message.
        
        Args:
            message: Status message
        """
        self.status_bar.showMessage(message)
    
    def closeEvent(self, event):
        """Handle window close event."""
        self.player_widget.cleanup()
        event.accept()
