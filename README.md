# Video Tagger - 视频标签工具

一个轻量级的视频标签工具，支持在 Linux 端使用，用于给视频文件添加自定义标签，支持快捷键操作和 JSON 导出。

## ✨ 功能特性

- 📁 **文件夹选择** - 通过文件选择对话框选择目标文件夹
- 🎬 **视频扫描** - 递归扫描文件夹下的视频文件（mp4, avi, mkv, mov, webm, flv, wmv）
- 📋 **播放列表** - 以列表形式展示所有视频，显示文件名和已标记的标签
- ▶️ **视频播放** - 内置 VLC 播放器，支持播放/暂停、进度条、音量控制
- 🏷️ **标签添加** - 通过快捷键或按钮为当前视频添加预定义标签
- ⌨️ **快捷键配置** - 用户可自定义快捷键与标签的映射关系
- 📤 **标签导出** - 导出为 JSON 格式，支持选择导出路径
- 💾 **标签持久化** - 自动保存标签数据，下次打开时恢复

## 🛠️ 技术栈

- **UI 框架**: PyQt6
- **视频播放**: python-vlc (libVLC 绑定)
- **数据存储**: JSON 文件

## 📦 安装

### 系统要求

- Python 3.9+
- Linux (Ubuntu/Debian/Fedora/Arch)

### 安装 VLC

```bash
# Ubuntu/Debian
sudo apt install vlc libvlc-dev

# Fedora
sudo dnf install vlc vlc-devel

# Arch Linux
sudo pacman -S vlc
```

### 安装 Python 依赖

```bash
# 克隆项目
git clone https://github.com/wy-20/VideoTagger.git
cd VideoTagger

# 安装依赖
pip install -r requirements.txt
```

## 🚀 运行

```bash
python main.py
```

## 📖 使用说明

### 基本操作

1. **选择文件夹** - 点击"选择文件夹"按钮，选择包含视频文件的目录
2. **选择视频** - 在左侧播放列表中点击视频开始播放
3. **添加标签** - 使用快捷键（默认 1-5）或点击右侧标签按钮为视频添加标签
4. **导出标签** - 点击"导出 JSON"按钮，选择保存路径

### 默认快捷键

| 快捷键 | 标签 |
|--------|------|
| 1 | good |
| 2 | bad |
| 3 | interesting |
| 4 | review_later |
| 5 | favorite |
| Space | 播放/暂停 |

### 自定义快捷键

1. 点击"设置"按钮打开设置对话框
2. 在表格中编辑快捷键和对应的标签
3. 点击"保存"应用更改

## 📂 项目结构

```
video-tagger/
├── main.py                 # 入口文件
├── requirements.txt        # 依赖
├── config/
│   └── shortcuts.json      # 快捷键配置
├── data/
│   └── tags.json           # 标签数据
├── src/
│   ├── ui/
│   │   ├── main_window.py  # 主窗口
│   │   ├── playlist.py     # 播放列表组件
│   │   ├── player.py       # 播放器组件
│   │   ├── tag_panel.py    # 标签面板
│   │   └── settings_dialog.py  # 设置对话框
│   ├── core/
│   │   ├── video_scanner.py    # 视频扫描
│   │   ├── tag_manager.py      # 标签管理
│   │   └── shortcut_manager.py # 快捷键管理
│   └── utils/
│       └── file_utils.py   # 文件工具
└── tests/
    ├── test_tag_manager.py
    ├── test_shortcut_manager.py
    └── test_video_scanner.py
```

## 📊 导出数据格式

标签导出为 JSON 格式：

```json
{
  "/path/to/video1.mp4": ["good", "favorite"],
  "/path/to/video2.mkv": ["bad"],
  "/path/to/video3.avi": ["interesting", "review_later"]
}
```

## 🧪 运行测试

```bash
python -m pytest tests/ -v
```

或使用 unittest：

```bash
python -m unittest discover tests/
```

## 📝 许可证

MIT License
