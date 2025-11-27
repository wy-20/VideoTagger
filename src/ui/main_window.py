"""Main window module for Video Tagger application."""
from pathlib import Path
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QListWidget, QPushButton, QFileDialog, QLabel,
    QSlider, QListWidgetItem, QSplitter
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QShortcut, QKeySequence
from PyQt6.QtMultimediaWidgets import QVideoWidget

from src.ui.player import QtPlayer
from src.ui.settings_dialog import SettingsDialog
from src.core.video_scanner import scan_videos
from src.core.tag_manager import TagManager
from src.core.shortcut_manager import ShortcutManager


class MainWindow(QMainWindow):
    """Main application window for Video Tagger."""
    
    def __init__(self):
        """Initialize the main window."""
        super().__init__()
        self.setWindowTitle("Video Tagger")
        self.setGeometry(100, 100, 1200, 700)
        
        # Initialize managers
        self.tag_manager = TagManager()
        self.shortcut_manager = ShortcutManager()
        self.videos = []
        self.current_video = None
        self.player = None
        self.shortcuts = []
        
        self.init_ui()
        self.setup_shortcuts()
        self.setup_timer()
    
    def init_ui(self):
        """Initialize the UI components."""
        central = QWidget()
        self.setCentralWidget(central)
        layout = QHBoxLayout(central)
        
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left panel: Playlist
        left_widget = QWidget()
        left_panel = QVBoxLayout(left_widget)
        
        self.folder_btn = QPushButton("📁 选择文件夹")
        self.folder_btn.clicked.connect(self.select_folder)
        
        self.playlist = QListWidget()
        self.playlist.itemDoubleClicked.connect(self.play_video)
        
        left_panel.addWidget(self.folder_btn)
        left_panel.addWidget(self.playlist)
        
        # Center panel: Video player
        center_widget = QWidget()
        center_layout = QVBoxLayout(center_widget)
        
        # Video widget
        self.video_widget = QVideoWidget()
        self.video_widget.setMinimumSize(640, 480)
        self.video_widget.setStyleSheet("background-color: black;")
        
        # Playback controls
        controls = QHBoxLayout()
        
        self.play_btn = QPushButton("▶️ 播放")
        self.play_btn.clicked.connect(self.toggle_play)
        
        self.progress = QSlider(Qt.Orientation.Horizontal)
        self.progress.setMaximum(1000)
        self.progress.sliderMoved.connect(self.seek_video)
        
        self.time_label = QLabel("00:00 / 00:00")
        
        self.volume = QSlider(Qt.Orientation.Horizontal)
        self.volume.setMaximum(100)
        self.volume.setValue(100)
        self.volume.setFixedWidth(100)
        self.volume.valueChanged.connect(self.change_volume)
        
        controls.addWidget(self.play_btn)
        controls.addWidget(self.progress, 1)
        controls.addWidget(self.time_label)
        controls.addWidget(QLabel("🔊"))
        controls.addWidget(self.volume)
        
        center_layout.addWidget(self.video_widget, 1)
        center_layout.addLayout(controls)
        
        # Right panel: Tag panel
        right_widget = QWidget()
        right_panel = QVBoxLayout(right_widget)
        
        right_panel.addWidget(QLabel("<b>当前视频标签</b>"))
        self.tag_label = QLabel("无")
        self.tag_label.setWordWrap(True)
        right_panel.addWidget(self.tag_label)
        
        right_panel.addWidget(QLabel("<b>快捷键标签</b>"))
        self.tag_buttons_layout = QVBoxLayout()
        right_panel.addLayout(self.tag_buttons_layout)
        self.update_tag_buttons()
        
        right_panel.addStretch()
        
        self.export_btn = QPushButton("📤 导出 JSON")
        self.export_btn.clicked.connect(self.export_tags)
        
        self.settings_btn = QPushButton("⚙️ 快捷键设置")
        self.settings_btn.clicked.connect(self.open_settings)
        
        right_panel.addWidget(self.export_btn)
        right_panel.addWidget(self.settings_btn)
        
        # Add widgets to splitter
        splitter.addWidget(left_widget)
        splitter.addWidget(center_widget)
        splitter.addWidget(right_widget)
        splitter.setSizes([200, 700, 200])
        
        layout.addWidget(splitter)
        
        # Initialize player
        self.player = QtPlayer(self.video_widget)
    
    def setup_shortcuts(self):
        """Set up keyboard shortcuts."""
        # Clear existing shortcuts
        for shortcut in self.shortcuts:
            shortcut.setEnabled(False)
            shortcut.deleteLater()
        self.shortcuts.clear()
        
        # Add tag shortcuts
        for key, tag in self.shortcut_manager.get_all().items():
            shortcut = QShortcut(QKeySequence(key), self)
            shortcut.activated.connect(
                lambda t=tag: self.add_tag_to_current(t)
            )
            self.shortcuts.append(shortcut)
        
        # Space bar for play/pause
        space_shortcut = QShortcut(QKeySequence("Space"), self)
        space_shortcut.activated.connect(self.toggle_play)
        self.shortcuts.append(space_shortcut)
    
    def setup_timer(self):
        """Set up timer for progress updates."""
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progress)
        self.timer.start(100)
    
    def update_tag_buttons(self):
        """Update tag buttons in the right panel."""
        # Clear existing buttons
        while self.tag_buttons_layout.count():
            item = self.tag_buttons_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Add new buttons
        for key, tag in self.shortcut_manager.get_all().items():
            btn = QPushButton(f"[{key}] {tag}")
            btn.clicked.connect(lambda checked, t=tag: self.add_tag_to_current(t))
            self.tag_buttons_layout.addWidget(btn)
    
    def select_folder(self):
        """Open folder selection dialog."""
        folder = QFileDialog.getExistingDirectory(self, "选择视频文件夹")
        if folder:
            self.videos = scan_videos(folder)
            self.update_playlist()
    
    def update_playlist(self):
        """Update the playlist display."""
        self.playlist.clear()
        for video in self.videos:
            item = QListWidgetItem(Path(video).name)
            item.setData(Qt.ItemDataRole.UserRole, video)
            tags = self.tag_manager.get_tags(video)
            if tags:
                item.setText(f"{Path(video).name} 🏷️ {', '.join(tags)}")
            self.playlist.addItem(item)
    
    def play_video(self, item):
        """Play the selected video."""
        video_path = item.data(Qt.ItemDataRole.UserRole)
        self.current_video = video_path
        if self.player:
            self.player.play(video_path)
            self.play_btn.setText("⏸️ 暂停")
        self.update_current_tags()
    
    def toggle_play(self):
        """Toggle play/pause state."""
        if self.player:
            self.player.pause()
            if self.player.is_paused:
                self.play_btn.setText("▶️ 播放")
            else:
                self.play_btn.setText("⏸️ 暂停")
    
    def seek_video(self, position):
        """Seek to a position in the video."""
        if self.player and self.player.duration > 0:
            self.player.seek(position / 1000 * self.player.duration)
    
    def change_volume(self, value):
        """Change the audio volume."""
        if self.player:
            self.player.set_volume(value)
    
    def update_progress(self):
        """Update the progress bar and time display."""
        if self.player and self.player.duration > 0:
            progress = int(self.player.position / self.player.duration * 1000)
            self.progress.blockSignals(True)
            self.progress.setValue(progress)
            self.progress.blockSignals(False)
            
            # Update time display
            current = self.format_time(self.player.position)
            total = self.format_time(self.player.duration)
            self.time_label.setText(f"{current} / {total}")
    
    def format_time(self, seconds: float) -> str:
        """Format seconds as time string."""
        m, s = divmod(int(seconds), 60)
        h, m = divmod(m, 60)
        if h > 0:
            return f"{h}:{m:02d}:{s:02d}"
        return f"{m:02d}:{s:02d}"
    
    def add_tag_to_current(self, tag: str):
        """Add a tag to the current video."""
        if self.current_video:
            self.tag_manager.add_tag(self.current_video, tag)
            self.update_current_tags()
            self.update_playlist()
    
    def update_current_tags(self):
        """Update the current video's tag display."""
        if self.current_video:
            tags = self.tag_manager.get_tags(self.current_video)
            self.tag_label.setText(', '.join(tags) if tags else '无')
    
    def export_tags(self):
        """Export tags to a JSON file."""
        path, _ = QFileDialog.getSaveFileName(
            self, "导出标签", "tags.json", "JSON Files (*.json)"
        )
        if path:
            self.tag_manager.export(path)
    
    def open_settings(self):
        """Open the settings dialog."""
        dialog = SettingsDialog(self.shortcut_manager, self)
        if dialog.exec():
            # Refresh shortcuts and buttons
            self.setup_shortcuts()
            self.update_tag_buttons()
