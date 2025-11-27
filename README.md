# Video Tagger

A lightweight video tagging tool for Linux, supporting custom tags, keyboard shortcuts, and JSON export.

## Features

- 📁 Select folders and scan for video files (mp4, avi, mkv, mov, webm, flv, wmv)
- 📋 Display all videos as a playlist
- ▶️ Built-in video player with mpv backend
- 🏷️ Add tags to videos via shortcuts or buttons
- ⌨️ Customizable keyboard shortcuts
- 📤 Export tags to JSON format

## Requirements

- Python 3.10+
- PyQt6
- python-mpv
- mpv (system library)

## Installation

### Install system dependencies

```bash
# Ubuntu/Debian
sudo apt install mpv libmpv-dev

# Fedora
sudo dnf install mpv mpv-libs-devel

# Arch Linux
sudo pacman -S mpv
```

### Install Python dependencies

```bash
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

### Keyboard Shortcuts

| Key | Tag |
|-----|-----|
| 1 | good |
| 2 | bad |
| 3 | interesting |
| 4 | review_later |
| 5 | favorite |
| Space | Play/Pause |

## Export Format

Tags are exported as JSON in the following format:

```json
{
  "/path/to/video1.mp4": ["good", "favorite"],
  "/path/to/video2.mkv": ["bad"],
  "/path/to/video3.avi": ["interesting", "review_later"]
}
```

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
│   │   └── player.py       # mpv player wrapper
│   ├── core/
│   │   ├── video_scanner.py    # Video file scanning
│   │   ├── tag_manager.py      # Tag management
│   │   └── shortcut_manager.py # Shortcut management
│   └── utils/
└── tests/
    ├── test_video_scanner.py
    ├── test_tag_manager.py
    └── test_shortcut_manager.py
```

## Running Tests

```bash
python -m pytest tests/
```

## License

MIT License
