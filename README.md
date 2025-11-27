# Video Tagger

A lightweight video tagging tool built with PyQt6 and QtMultimedia for Linux, supporting customizable keyboard shortcuts and JSON export.

## Features

- **Folder Selection**: Browse and select folders containing video files
- **Video Scanning**: Recursively scan directories for video files (mp4, avi, mkv, mov, webm, flv, wmv)
- **Playlist View**: Display all videos in a list with file names and assigned tags
- **Video Playback**: Built-in player with play/pause, progress bar, and volume control
- **Playback Speed Control**: Adjust playback speed from 0.25x to 5.0x with keyboard shortcuts or dropdown
- **Frame-by-Frame Navigation**: Step through video one frame at a time with keyboard shortcuts or buttons
- **Frame Rate Control**: Adjust frame rate (1-120 fps) for precise frame-by-frame navigation
- **Video Navigation**: Navigate between videos in the playlist with keyboard shortcuts (P/N)
- **Tag Management**: Toggle tags on/off with keyboard shortcuts or button clicks
- **Tag Toggle Mode**: First press adds tag, second press removes it - buttons show active state
- **Clear All Tags**: One-click button to remove all tags from current video (with confirmation)
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

## Building Executable

The project supports building a standalone executable using Nuitka for Ubuntu 20.04 x64.

### Prerequisites

```bash
# Install system dependencies (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install -y patchelf ccache libgl1-mesa-dev

# Install Nuitka
pip install nuitka ordered-set zstandard
```

### Build Command

```bash
python -m nuitka \
    --standalone \
    --onefile \
    --enable-plugin=pyqt6 \
    --include-package=src \
    --include-package-data=src \
    --include-qt-plugins=platforms,multimedia,styles,iconengines,imageformats \
    --output-filename=VideoTagger \
    --output-dir=dist \
    main.py
```

The executable will be created at `dist/VideoTagger`.

### Automated Builds

GitHub Actions automatically builds the executable on:
- Push to `main` branch
- Pull requests to `main`
- Tag pushes (creates a release with the executable)

Download the latest build from the [Actions](../../actions) tab or [Releases](../../releases) page.

### Workflow

1. Click "📁 选择文件夹" to select a folder containing videos
2. Double-click a video in the playlist to start playback
3. Use keyboard shortcuts (1-5 by default) or buttons to add tags
4. Use "📤 导出 JSON" to export tags to a JSON file
5. Use "⚙️ 快捷键设置" to customize shortcut mappings

### Default Keyboard Shortcuts

| Key | Function |
|-----|----------|
| 1 | Toggle 'good' tag |
| 2 | Toggle 'bad' tag |
| 3 | Toggle 'interesting' tag |
| 4 | Toggle 'review_later' tag |
| 5 | Toggle 'favorite' tag |
| Space | Play/Pause |
| , (comma) | Previous frame |
| . (period) | Next frame |
| + or = | Increase playback speed |
| - | Decrease playback speed |
| P | Previous video |
| N | Next video |
| Ctrl+Shift+C | Clear all tags |

### Playback Controls

- **Frame-by-frame navigation**: Use `,` and `.` keys or the ⏮️/⏭️ buttons to step through video one frame at a time
- **Playback speed**: Adjust speed from 0.25x to 5.0x using the dropdown or +/- keys
- **Frame rate**: Adjust frame rate (1-120 fps) using the spinbox for precise frame-by-frame navigation
- **Video navigation**: Use `P` and `N` keys to navigate to previous/next video in the playlist
- **Tag toggle**: Press a tag shortcut to add the tag, press again to remove it
- **Clear all tags**: Remove all tags from current video with confirmation

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
