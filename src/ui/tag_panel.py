"""Tag panel widget for displaying and managing tags."""

from typing import List, Dict

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QGridLayout, QScrollArea, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal


class TagPanelWidget(QWidget):
    """Widget for displaying tags and tag controls."""
    
    # Signals
    tag_added = pyqtSignal(str)     # Emitted when a tag is added
    tag_removed = pyqtSignal(str)   # Emitted when a tag is removed
    export_requested = pyqtSignal()  # Emitted when export is requested
    settings_requested = pyqtSignal()  # Emitted when settings is requested
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.shortcuts: Dict[str, str] = {}
        self.current_tags: List[str] = []
        self.tag_buttons: Dict[str, QPushButton] = {}
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # Title
        title = QLabel("标签管理")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(title)
        
        # Current video tags section
        current_frame = QFrame()
        current_frame.setFrameShape(QFrame.Shape.StyledPanel)
        current_layout = QVBoxLayout(current_frame)
        
        current_title = QLabel("当前视频标签")
        current_title.setStyleSheet("font-weight: bold;")
        current_layout.addWidget(current_title)
        
        self.current_tags_label = QLabel("无")
        self.current_tags_label.setWordWrap(True)
        current_layout.addWidget(self.current_tags_label)
        
        layout.addWidget(current_frame)
        
        # Quick tag buttons section
        quick_frame = QFrame()
        quick_frame.setFrameShape(QFrame.Shape.StyledPanel)
        quick_layout = QVBoxLayout(quick_frame)
        
        quick_title = QLabel("快捷标签 (点击或使用快捷键)")
        quick_title.setStyleSheet("font-weight: bold;")
        quick_layout.addWidget(quick_title)
        
        # Scroll area for tag buttons
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        self.buttons_widget = QWidget()
        self.buttons_layout = QGridLayout(self.buttons_widget)
        self.buttons_layout.setSpacing(5)
        scroll.setWidget(self.buttons_widget)
        
        quick_layout.addWidget(scroll)
        layout.addWidget(quick_frame, stretch=1)
        
        # Action buttons
        actions_layout = QHBoxLayout()
        
        self.settings_btn = QPushButton("⚙ 设置")
        self.settings_btn.clicked.connect(self.settings_requested.emit)
        
        self.export_btn = QPushButton("📤 导出 JSON")
        self.export_btn.clicked.connect(self.export_requested.emit)
        
        actions_layout.addWidget(self.settings_btn)
        actions_layout.addWidget(self.export_btn)
        layout.addLayout(actions_layout)
    
    def set_shortcuts(self, shortcuts: Dict[str, str]):
        """Set shortcut mappings and update buttons.
        
        Args:
            shortcuts: Dictionary of key to tag mappings
        """
        self.shortcuts = shortcuts
        self.update_tag_buttons()
    
    def update_tag_buttons(self):
        """Update the tag buttons based on shortcuts."""
        # Clear existing buttons
        while self.buttons_layout.count():
            item = self.buttons_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        self.tag_buttons.clear()
        
        # Create buttons for each shortcut
        row = 0
        col = 0
        max_cols = 2
        
        for key, tag in sorted(self.shortcuts.items()):
            btn = QPushButton(f"[{key}] {tag}")
            btn.setToolTip(f"快捷键: {key}")
            btn.clicked.connect(lambda checked, t=tag: self.tag_added.emit(t))
            
            self.buttons_layout.addWidget(btn, row, col)
            self.tag_buttons[key] = btn
            
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
    
    def set_current_tags(self, tags: List[str]):
        """Set the current video's tags.
        
        Args:
            tags: List of tags
        """
        self.current_tags = tags
        if tags:
            # Create clickable tag display
            tags_text = ", ".join(tags)
            self.current_tags_label.setText(tags_text)
        else:
            self.current_tags_label.setText("无")
    
    def add_tag(self, tag: str):
        """Add a tag to current display.
        
        Args:
            tag: Tag to add
        """
        if tag not in self.current_tags:
            self.current_tags.append(tag)
            self.set_current_tags(self.current_tags)
    
    def remove_tag(self, tag: str):
        """Remove a tag from current display.
        
        Args:
            tag: Tag to remove
        """
        if tag in self.current_tags:
            self.current_tags.remove(tag)
            self.set_current_tags(self.current_tags)
    
    def clear_tags(self):
        """Clear current tags display."""
        self.current_tags = []
        self.current_tags_label.setText("无")
