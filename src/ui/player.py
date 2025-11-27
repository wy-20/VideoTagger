"""Video player widget using VLC."""

import sys
from typing import Optional

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QSlider, QLabel, QFrame, QStyle
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal

try:
    import vlc
    VLC_AVAILABLE = True
except ImportError:
    VLC_AVAILABLE = False


class VideoPlayerWidget(QWidget):
    """Video player widget with VLC backend."""
    
    # Signals
    playback_started = pyqtSignal(str)  # Emitted when video starts playing
    playback_stopped = pyqtSignal()      # Emitted when playback stops
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_video: Optional[str] = None
        self.vlc_instance = None
        self.media_player = None
        self.is_paused = False
        
        self.init_vlc()
        self.init_ui()
        self.init_timer()
    
    def init_vlc(self):
        """Initialize VLC instance."""
        if not VLC_AVAILABLE:
            return
        
        try:
            # Create VLC instance with options for better compatibility
            self.vlc_instance = vlc.Instance('--no-xlib', '--quiet')
            self.media_player = self.vlc_instance.media_player_new()
        except Exception as e:
            print(f"VLC initialization error: {e}")
            self.vlc_instance = None
            self.media_player = None
    
    def init_ui(self):
        """Initialize the UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Video display frame
        self.video_frame = QFrame()
        self.video_frame.setStyleSheet("background-color: black;")
        self.video_frame.setMinimumSize(640, 360)
        layout.addWidget(self.video_frame, stretch=1)
        
        # Controls panel
        controls_layout = QVBoxLayout()
        
        # Progress slider
        progress_layout = QHBoxLayout()
        self.time_label = QLabel("00:00")
        self.progress_slider = QSlider(Qt.Orientation.Horizontal)
        self.progress_slider.setRange(0, 1000)
        self.progress_slider.sliderMoved.connect(self.on_slider_moved)
        self.progress_slider.sliderPressed.connect(self.on_slider_pressed)
        self.progress_slider.sliderReleased.connect(self.on_slider_released)
        self.duration_label = QLabel("00:00")
        
        progress_layout.addWidget(self.time_label)
        progress_layout.addWidget(self.progress_slider)
        progress_layout.addWidget(self.duration_label)
        controls_layout.addLayout(progress_layout)
        
        # Playback controls
        buttons_layout = QHBoxLayout()
        
        self.play_btn = QPushButton("▶")
        self.play_btn.setFixedWidth(50)
        self.play_btn.clicked.connect(self.toggle_play)
        
        self.stop_btn = QPushButton("⏹")
        self.stop_btn.setFixedWidth(50)
        self.stop_btn.clicked.connect(self.stop)
        
        self.volume_label = QLabel("🔊")
        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(80)
        self.volume_slider.setFixedWidth(100)
        self.volume_slider.valueChanged.connect(self.on_volume_changed)
        
        buttons_layout.addWidget(self.play_btn)
        buttons_layout.addWidget(self.stop_btn)
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.volume_label)
        buttons_layout.addWidget(self.volume_slider)
        
        controls_layout.addLayout(buttons_layout)
        layout.addLayout(controls_layout)
        
        # Status label
        self.status_label = QLabel("请选择视频")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)
        
        if not VLC_AVAILABLE:
            self.status_label.setText("VLC 未安装，请安装 python-vlc")
    
    def init_timer(self):
        """Initialize update timer."""
        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.update_ui)
        self.update_timer.start(200)  # Update every 200ms
        
        self.slider_being_dragged = False
    
    def play_video(self, video_path: str):
        """Play a video file.
        
        Args:
            video_path: Path to the video file
        """
        if not self.vlc_instance or not self.media_player:
            self.status_label.setText("VLC 未初始化")
            return
        
        self.current_video = video_path
        
        try:
            media = self.vlc_instance.media_new(video_path)
            self.media_player.set_media(media)
            
            # Embed VLC in Qt widget
            if sys.platform.startswith('linux'):
                self.media_player.set_xwindow(int(self.video_frame.winId()))
            elif sys.platform == 'win32':
                self.media_player.set_hwnd(int(self.video_frame.winId()))
            elif sys.platform == 'darwin':
                self.media_player.set_nsobject(int(self.video_frame.winId()))
            
            self.media_player.play()
            self.is_paused = False
            self.play_btn.setText("⏸")
            self.status_label.setText(f"正在播放: {video_path.split('/')[-1]}")
            
            # Apply current volume
            self.media_player.audio_set_volume(self.volume_slider.value())
            
            self.playback_started.emit(video_path)
        except Exception as e:
            self.status_label.setText(f"播放失败: {str(e)}")
    
    def toggle_play(self):
        """Toggle play/pause."""
        if not self.media_player:
            return
        
        if self.media_player.is_playing():
            self.media_player.pause()
            self.is_paused = True
            self.play_btn.setText("▶")
        else:
            self.media_player.play()
            self.is_paused = False
            self.play_btn.setText("⏸")
    
    def stop(self):
        """Stop playback."""
        if not self.media_player:
            return
        
        self.media_player.stop()
        self.is_paused = False
        self.play_btn.setText("▶")
        self.progress_slider.setValue(0)
        self.time_label.setText("00:00")
        self.status_label.setText("已停止")
        self.playback_stopped.emit()
    
    def on_slider_pressed(self):
        """Handle slider press."""
        self.slider_being_dragged = True
    
    def on_slider_released(self):
        """Handle slider release."""
        self.slider_being_dragged = False
        self.on_slider_moved(self.progress_slider.value())
    
    def on_slider_moved(self, position: int):
        """Handle slider movement.
        
        Args:
            position: Slider position (0-1000)
        """
        if not self.media_player:
            return
        
        # Convert slider position to percentage
        percentage = position / 1000.0
        self.media_player.set_position(percentage)
    
    def on_volume_changed(self, value: int):
        """Handle volume change.
        
        Args:
            value: Volume level (0-100)
        """
        if not self.media_player:
            return
        
        self.media_player.audio_set_volume(value)
        if value == 0:
            self.volume_label.setText("🔇")
        elif value < 50:
            self.volume_label.setText("🔉")
        else:
            self.volume_label.setText("🔊")
    
    def update_ui(self):
        """Update UI based on playback state."""
        if not self.media_player:
            return
        
        if self.slider_being_dragged:
            return
        
        # Update progress slider
        position = self.media_player.get_position()
        if position >= 0:
            self.progress_slider.setValue(int(position * 1000))
        
        # Update time labels
        time_ms = self.media_player.get_time()
        if time_ms >= 0:
            self.time_label.setText(self.format_time(time_ms))
        
        length_ms = self.media_player.get_length()
        if length_ms >= 0:
            self.duration_label.setText(self.format_time(length_ms))
    
    @staticmethod
    def format_time(milliseconds: int) -> str:
        """Format milliseconds to MM:SS or HH:MM:SS.
        
        Args:
            milliseconds: Time in milliseconds
            
        Returns:
            Formatted time string
        """
        seconds = milliseconds // 1000
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{secs:02d}"
        else:
            return f"{minutes:02d}:{secs:02d}"
    
    def get_current_video(self) -> Optional[str]:
        """Get currently playing video path.
        
        Returns:
            Current video path or None
        """
        return self.current_video
    
    def cleanup(self):
        """Clean up VLC resources."""
        if self.media_player:
            self.media_player.stop()
            self.media_player.release()
        if self.vlc_instance:
            self.vlc_instance.release()
