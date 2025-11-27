"""Main window module for Video Tagger application."""
from pathlib import Path
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QListWidget, QPushButton, QFileDialog, QLabel,
    QSlider, QListWidgetItem, QSplitter, QComboBox, QMessageBox,
    QSpinBox
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QShortcut, QKeySequence
from PyQt6.QtMultimediaWidgets import QVideoWidget

from src.ui.player import QtPlayer, PLAYBACK_SPEEDS, DEFAULT_FRAME_RATE
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
        
        # Frame step buttons
        self.prev_frame_btn = QPushButton("⏮️")
        self.prev_frame_btn.setToolTip("上一帧 (,)")
        self.prev_frame_btn.setFixedWidth(40)
        self.prev_frame_btn.clicked.connect(self.step_backward)
        
        self.play_btn = QPushButton("▶️ 播放")
        self.play_btn.clicked.connect(self.toggle_play)
        
        self.next_frame_btn = QPushButton("⏭️")
        self.next_frame_btn.setToolTip("下一帧 (.)")
        self.next_frame_btn.setFixedWidth(40)
        self.next_frame_btn.clicked.connect(self.step_forward)
        
        self.progress = QSlider(Qt.Orientation.Horizontal)
        self.progress.setMaximum(1000)
        self.progress.sliderMoved.connect(self.seek_video)
        
        self.time_label = QLabel("00:00 / 00:00")
        
        # Speed control
        self.speed_combo = QComboBox()
        for speed in PLAYBACK_SPEEDS:
            self.speed_combo.addItem(f"{speed}x", speed)
        self.speed_combo.setCurrentIndex(PLAYBACK_SPEEDS.index(1.0))
        self.speed_combo.currentIndexChanged.connect(self.change_speed)
        self.speed_combo.setFixedWidth(70)
        self.speed_combo.setToolTip("播放速度 (+/-)")
        
        # Frame rate control
        self.frame_rate_label = QLabel("帧率:")
        self.frame_rate_spinbox = QSpinBox()
        self.frame_rate_spinbox.setMinimum(1)
        self.frame_rate_spinbox.setMaximum(120)
        self.frame_rate_spinbox.setValue(int(DEFAULT_FRAME_RATE))
        self.frame_rate_spinbox.setSuffix(" fps")
        self.frame_rate_spinbox.setToolTip("视频帧率 (用于逐帧导航)")
        self.frame_rate_spinbox.setFixedWidth(80)
        self.frame_rate_spinbox.valueChanged.connect(self.change_frame_rate)
        
        self.volume = QSlider(Qt.Orientation.Horizontal)
        self.volume.setMaximum(100)
        self.volume.setValue(100)
        self.volume.setFixedWidth(100)
        self.volume.valueChanged.connect(self.change_volume)
        
        controls.addWidget(self.prev_frame_btn)
        controls.addWidget(self.play_btn)
        controls.addWidget(self.next_frame_btn)
        controls.addWidget(self.progress, 1)
        controls.addWidget(self.time_label)
        controls.addWidget(self.speed_combo)
        controls.addWidget(self.frame_rate_label)
        controls.addWidget(self.frame_rate_spinbox)
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
        
        # Clear all tags button
        self.clear_tags_btn = QPushButton("🗑️ 清除所有标签")
        self.clear_tags_btn.setToolTip("清除当前视频所有标签 (Ctrl+Shift+C)")
        self.clear_tags_btn.clicked.connect(self.clear_all_tags)
        right_panel.addWidget(self.clear_tags_btn)
        
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
        
        # Add tag shortcuts (toggle mode)
        for key, tag in self.shortcut_manager.get_all().items():
            shortcut = QShortcut(QKeySequence(key), self)
            shortcut.activated.connect(
                lambda t=tag: self.toggle_tag_on_current(t)
            )
            self.shortcuts.append(shortcut)
        
        # Space bar for play/pause
        space_shortcut = QShortcut(QKeySequence("Space"), self)
        space_shortcut.activated.connect(self.toggle_play)
        self.shortcuts.append(space_shortcut)
        
        # Frame-by-frame shortcuts
        prev_frame_shortcut = QShortcut(QKeySequence(","), self)
        prev_frame_shortcut.activated.connect(self.step_backward)
        self.shortcuts.append(prev_frame_shortcut)
        
        next_frame_shortcut = QShortcut(QKeySequence("."), self)
        next_frame_shortcut.activated.connect(self.step_forward)
        self.shortcuts.append(next_frame_shortcut)
        
        # Speed control shortcuts
        speed_up_shortcut = QShortcut(QKeySequence("+"), self)
        speed_up_shortcut.activated.connect(self.increase_speed)
        self.shortcuts.append(speed_up_shortcut)
        
        speed_up_equals = QShortcut(QKeySequence("="), self)
        speed_up_equals.activated.connect(self.increase_speed)
        self.shortcuts.append(speed_up_equals)
        
        speed_down_shortcut = QShortcut(QKeySequence("-"), self)
        speed_down_shortcut.activated.connect(self.decrease_speed)
        self.shortcuts.append(speed_down_shortcut)
        
        # Clear all tags shortcut
        clear_tags_shortcut = QShortcut(QKeySequence("Ctrl+Shift+C"), self)
        clear_tags_shortcut.activated.connect(self.clear_all_tags)
        self.shortcuts.append(clear_tags_shortcut)
        
        # Video navigation shortcuts
        prev_video_shortcut = QShortcut(QKeySequence("P"), self)
        prev_video_shortcut.activated.connect(self.play_previous_video)
        self.shortcuts.append(prev_video_shortcut)
        
        next_video_shortcut = QShortcut(QKeySequence("N"), self)
        next_video_shortcut.activated.connect(self.play_next_video)
        self.shortcuts.append(next_video_shortcut)
    
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
        
        # Store button references for state updates
        self.tag_buttons = {}
        
        # Add new buttons
        for key, tag in self.shortcut_manager.get_all().items():
            btn = QPushButton(f"[{key}] {tag}")
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, t=tag: self.toggle_tag_on_current(t))
            self.tag_buttons_layout.addWidget(btn)
            self.tag_buttons[tag] = btn
        
        # Update button states based on current video
        self.update_tag_button_states()
    
    def update_tag_button_states(self):
        """Update tag button checked states based on current video tags."""
        if not hasattr(self, 'tag_buttons'):
            return
        
        current_tags = []
        if self.current_video:
            current_tags = self.tag_manager.get_tags(self.current_video)
        
        for tag, btn in self.tag_buttons.items():
            btn.setChecked(tag in current_tags)
    
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
        self.update_tag_button_states()
    
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
            self.update_tag_button_states()
    
    def toggle_tag_on_current(self, tag: str):
        """Toggle a tag on the current video (add if not present, remove if present)."""
        if self.current_video:
            self.tag_manager.toggle_tag(self.current_video, tag)
            self.update_current_tags()
            self.update_playlist()
            self.update_tag_button_states()
    
    def clear_all_tags(self):
        """Clear all tags from the current video."""
        if not self.current_video:
            return
        
        current_tags = self.tag_manager.get_tags(self.current_video)
        if not current_tags:
            return
        
        reply = QMessageBox.question(
            self, "确认清除",
            "确定要清除当前视频的所有标签吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.tag_manager.clear_tags(self.current_video)
            self.update_current_tags()
            self.update_playlist()
            self.update_tag_button_states()
    
    def step_forward(self):
        """Step video forward by one frame."""
        if self.player:
            self.player.step_forward()
            if self.player.is_paused:
                self.play_btn.setText("▶️ 播放")
    
    def step_backward(self):
        """Step video backward by one frame."""
        if self.player:
            self.player.step_backward()
            if self.player.is_paused:
                self.play_btn.setText("▶️ 播放")
    
    def change_speed(self, index):
        """Change playback speed from combo box."""
        if self.player and index >= 0:
            speed = self.speed_combo.itemData(index)
            self.player.set_playback_rate(speed)
    
    def increase_speed(self):
        """Increase playback speed."""
        if self.player:
            self.player.increase_speed()
            self._update_speed_combo()
    
    def decrease_speed(self):
        """Decrease playback speed."""
        if self.player:
            self.player.decrease_speed()
            self._update_speed_combo()
    
    def _update_speed_combo(self):
        """Update speed combo box to reflect current playback rate."""
        if self.player:
            current_rate = self.player.playback_rate
            for i in range(self.speed_combo.count()):
                if self.speed_combo.itemData(i) == current_rate:
                    self.speed_combo.blockSignals(True)
                    self.speed_combo.setCurrentIndex(i)
                    self.speed_combo.blockSignals(False)
                    break
    
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
    
    def change_frame_rate(self, value: int):
        """Change the frame rate for frame-by-frame navigation."""
        if self.player:
            self.player.set_frame_rate(float(value))
    
    def _get_current_video_index(self) -> int:
        """Get the current video index in the playlist."""
        if self.current_video:
            try:
                return self.videos.index(self.current_video)
            except ValueError:
                pass
        return -1
    
    def _navigate_to_video(self, index: int):
        """Navigate to a video at the specified index in the playlist."""
        if 0 <= index < len(self.videos):
            self.playlist.setCurrentRow(index)
            item = self.playlist.item(index)
            if item:
                self.play_video(item)
    
    def play_previous_video(self):
        """Play the previous video in the playlist."""
        if not self.videos:
            return
        current_row = self._get_current_video_index()
        if current_row > 0:
            self._navigate_to_video(current_row - 1)
    
    def play_next_video(self):
        """Play the next video in the playlist."""
        if not self.videos:
            return
        current_row = self._get_current_video_index()
        if current_row < len(self.videos) - 1:
            self._navigate_to_video(current_row + 1)
