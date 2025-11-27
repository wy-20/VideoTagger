"""QtMultimedia player wrapper module."""
from PyQt6.QtCore import QUrl
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget


# Default frame rate assumption when video metadata is unavailable
DEFAULT_FRAME_RATE = 30.0

# Available playback speeds
PLAYBACK_SPEEDS = [0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 5.0]


class QtPlayer:
    """QtMultimedia player wrapper class for video playback."""
    
    def __init__(self, video_widget: QVideoWidget):
        """
        Initialize the QtPlayer.
        
        Args:
            video_widget: QVideoWidget instance for video output
        """
        self.player = QMediaPlayer()
        self.audio = QAudioOutput()
        self.player.setAudioOutput(self.audio)
        self.player.setVideoOutput(video_widget)
        
        self._duration = 0
        self._playback_rate = 1.0
        self._frame_rate = DEFAULT_FRAME_RATE
        
        # Connect duration changed signal
        self.player.durationChanged.connect(self._on_duration_changed)
    
    def _on_duration_changed(self, duration: int):
        """
        Handle duration change event.
        
        Args:
            duration: Duration in milliseconds
        """
        self._duration = duration / 1000  # Convert to seconds
    
    def play(self, path: str):
        """
        Play a video file.
        
        Args:
            path: Path to the video file
        """
        self.player.setSource(QUrl.fromLocalFile(path))
        self.player.play()
    
    def pause(self):
        """Toggle pause/play state."""
        if self.player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.player.pause()
        else:
            self.player.play()
    
    def stop(self):
        """Stop playback."""
        self.player.stop()
    
    def seek(self, position: float):
        """
        Seek to a position in the video.
        
        Args:
            position: Position in seconds
        """
        self.player.setPosition(int(position * 1000))
    
    def set_volume(self, volume: int):
        """
        Set the audio volume.
        
        Args:
            volume: Volume level (0-100)
        """
        self.audio.setVolume(volume / 100)
    
    @property
    def duration(self) -> float:
        """Get video duration in seconds."""
        return self._duration
    
    @property
    def position(self) -> float:
        """Get current playback position in seconds."""
        return self.player.position() / 1000
    
    @property
    def is_paused(self) -> bool:
        """Check if playback is paused."""
        return self.player.playbackState() != QMediaPlayer.PlaybackState.PlayingState
    
    @property
    def playback_rate(self) -> float:
        """Get current playback rate."""
        return self._playback_rate
    
    def set_playback_rate(self, rate: float):
        """
        Set the playback speed.
        
        Args:
            rate: Playback rate (e.g., 0.5, 1.0, 2.0)
        """
        self._playback_rate = rate
        self.player.setPlaybackRate(rate)
    
    def increase_speed(self):
        """Increase playback speed to next available speed level."""
        current_index = self._get_speed_index()
        if current_index < len(PLAYBACK_SPEEDS) - 1:
            self.set_playback_rate(PLAYBACK_SPEEDS[current_index + 1])
    
    def decrease_speed(self):
        """Decrease playback speed to previous available speed level."""
        current_index = self._get_speed_index()
        if current_index > 0:
            self.set_playback_rate(PLAYBACK_SPEEDS[current_index - 1])
    
    def _get_speed_index(self) -> int:
        """Get the index of current speed in PLAYBACK_SPEEDS list."""
        try:
            return PLAYBACK_SPEEDS.index(self._playback_rate)
        except ValueError:
            # Find closest speed
            for i, speed in enumerate(PLAYBACK_SPEEDS):
                if speed >= self._playback_rate:
                    return i
            return len(PLAYBACK_SPEEDS) - 1
    
    def step_forward(self):
        """Step forward one frame."""
        if self.player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.player.pause()
        frame_duration_ms = 1000 / self._frame_rate
        new_position = self.player.position() + int(frame_duration_ms)
        if new_position <= self._duration * 1000:
            self.player.setPosition(new_position)
    
    def step_backward(self):
        """Step backward one frame."""
        if self.player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.player.pause()
        frame_duration_ms = 1000 / self._frame_rate
        new_position = max(0, self.player.position() - int(frame_duration_ms))
        self.player.setPosition(new_position)
    
    @property
    def frame_rate(self) -> float:
        """Get current frame rate."""
        return self._frame_rate
    
    def set_frame_rate(self, rate: float):
        """
        Set the frame rate for frame-by-frame navigation.
        
        Args:
            rate: Frame rate in frames per second
        """
        if rate > 0:
            self._frame_rate = rate
