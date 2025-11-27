"""QtMultimedia player wrapper module."""
from PyQt6.QtCore import QUrl
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget


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
