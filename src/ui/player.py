"""MPV player wrapper for video playback."""
import mpv


class MpvPlayer:
    """MPV player wrapper class."""
    
    def __init__(self, wid: int):
        """
        Initialize the MPV player.
        
        Args:
            wid: Qt Widget's window ID for video output
        """
        self.player = mpv.MPV(
            wid=str(wid),
            vo='x11',           # Linux uses x11, Windows uses gpu
            hwdec='auto',       # Auto hardware decoding
            keep_open='yes',    # Keep open after playback
            osc=False,          # Disable mpv's on-screen controls
            input_default_bindings=False,  # Disable default key bindings
            input_vo_keyboard=False,
        )
        
        self._duration = 0
        self._position = 0
        
        # Monitor property changes
        @self.player.property_observer('duration')
        def on_duration(name, value):
            self._duration = value or 0
        
        @self.player.property_observer('time-pos')
        def on_position(name, value):
            self._position = value or 0
    
    def play(self, path: str):
        """
        Play a video file.
        
        Args:
            path: Path to the video file
        """
        self.player.play(path)
    
    def pause(self):
        """Toggle pause/play state."""
        self.player.pause = not self.player.pause
    
    def stop(self):
        """Stop playback."""
        self.player.stop()
    
    def seek(self, position: float):
        """
        Seek to a position in the video.
        
        Args:
            position: Position in seconds
        """
        self.player.seek(position, 'absolute')
    
    def set_volume(self, volume: int):
        """
        Set the volume level.
        
        Args:
            volume: Volume level (0-100)
        """
        self.player.volume = volume
    
    @property
    def duration(self) -> float:
        """Get video duration in seconds."""
        return self._duration
    
    @property
    def position(self) -> float:
        """Get current playback position in seconds."""
        return self._position
    
    @property
    def is_paused(self) -> bool:
        """Check if playback is paused."""
        return self.player.pause
    
    def quit(self):
        """Terminate the player."""
        self.player.terminate()
