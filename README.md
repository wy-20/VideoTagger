# Video Tagger

A lightweight video tagging tool built with PyQt6 and QtMultimedia for Linux, supporting customizable keyboard shortcuts and JSON export.

## Features

- **Folder Selection**: Browse and select folders containing video files
- **Video Scanning**: Recursively scan directories for video files (mp4, avi, mkv, mov, webm, flv, wmv)
- **Playlist View**: Display all videos in a list with file names and assigned tags
- **Video Playback**: Built-in player with play/pause, progress bar, and volume control
- **Tag Management**: Add tags to videos via keyboard shortcuts or button clicks
- **Customizable Shortcuts**: Configure keyboard shortcuts for quick tagging
- **JSON Export**: Export all tags in JSON format: `{video_path: [tag1, tag2, ...], ...}`
- **Persistent Storage**: Automatically save and restore tags between sessions

## Requirements

- Python 3.9+
- PyQt6

### Linux Dependencies

Install GStreamer plugins for video playback support:

```bash
# Ubuntu/Debian
sudo apt install gstreamer1.0-plugins-good gstreamer1.0-plugins-bad \
    gstreamer1.0-plugins-ugly gstreamer1.0-libav

# Fedora
sudo dnf install gstreamer1-plugins-good gstreamer1-plugins-bad-free \
    gstreamer1-plugins-ugly gstreamer1-libav

# Arch
sudo pacman -S gst-plugins-good gst-plugins-bad gst-plugins-ugly gst-libav
```

## Installation

```bash
# Clone the repository
git clone <repo_url>
cd video-tagger

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

```bash
# Activate virtual environment
source venv/bin/activate

# Run the application
python main.py
```

### Workflow

1. Click "📁 选择文件夹" to select a folder containing videos
2. Double-click a video in the playlist to start playback
3. Use keyboard shortcuts (1-5 by default) or buttons to add tags
4. Use "📤 导出 JSON" to export tags to a JSON file
5. Use "⚙️ 快捷键设置" to customize shortcut mappings

### Default Keyboard Shortcuts

| Key | Tag |
|-----|-----|
| 1 | good |
| 2 | bad |
| 3 | interesting |
| 4 | review_later |
| 5 | favorite |
| Space | Play/Pause |

## Project Structure

```
video-tagger/
├── main.py                 # Entry point
├── requirements.txt        # Dependencies
├── config/
│   └── shortcuts.json      # Shortcut configuration
├── data/
│   └── tags.json           # Tag data
├── src/
│   ├── ui/
│   │   ├── main_window.py  # Main window
│   │   ├── player.py       # QtMultimedia player
│   │   └── settings_dialog.py  # Settings dialog
│   ├── core/
│   │   ├── video_scanner.py    # Video scanning
│   │   ├── tag_manager.py      # Tag management
│   │   └── shortcut_manager.py # Shortcut management
│   └── utils/
│       └── file_utils.py   # File utilities
└── tests/
    ├── test_video_scanner.py
    ├── test_tag_manager.py
    └── test_shortcut_manager.py
```

## Export Format

Tags are exported as JSON in the following format:

```json
{
  "/path/to/video1.mp4": ["good", "favorite"],
  "/path/to/video2.mkv": ["bad"],
  "/path/to/video3.avi": ["interesting", "review_later"]
}
```

## Running Tests

```bash
python -m pytest tests/
```

## Troubleshooting

### Video not playing or no sound?

Install all GStreamer plugins:

```bash
sudo apt install gstreamer1.0-plugins-base gstreamer1.0-plugins-good \
    gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly \
    gstreamer1.0-libav gstreamer1.0-tools gstreamer1.0-alsa \
    gstreamer1.0-pulseaudio
```

### PyQt6 installation failed?

Try using pre-compiled wheels:

```bash
pip install --upgrade pip
pip install PyQt6 --only-binary :all:
```

Or use conda:

```bash
conda install -c conda-forge pyqt6
```

## License

MIT License
