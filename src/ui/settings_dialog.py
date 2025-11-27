"""Settings dialog for shortcut configuration."""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTableWidget, 
    QTableWidgetItem, QPushButton, QLineEdit, QLabel,
    QHeaderView, QMessageBox
)
from PyQt6.QtCore import Qt


class SettingsDialog(QDialog):
    """Dialog for configuring keyboard shortcuts."""
    
    def __init__(self, shortcut_manager, parent=None):
        """
        Initialize the settings dialog.
        
        Args:
            shortcut_manager: ShortcutManager instance
            parent: Parent widget
        """
        super().__init__(parent)
        self.shortcut_manager = shortcut_manager
        self.setWindowTitle("快捷键设置")
        self.setMinimumSize(400, 300)
        self.init_ui()
        self.load_shortcuts()
    
    def init_ui(self):
        """Initialize the UI components."""
        layout = QVBoxLayout(self)
        
        # Shortcut table
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["快捷键", "标签"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.table)
        
        # Add new shortcut section
        add_layout = QHBoxLayout()
        add_layout.addWidget(QLabel("新快捷键:"))
        self.key_input = QLineEdit()
        self.key_input.setMaxLength(1)
        self.key_input.setMaximumWidth(50)
        add_layout.addWidget(self.key_input)
        
        add_layout.addWidget(QLabel("标签:"))
        self.tag_input = QLineEdit()
        add_layout.addWidget(self.tag_input)
        
        self.add_btn = QPushButton("添加")
        self.add_btn.clicked.connect(self.add_shortcut)
        add_layout.addWidget(self.add_btn)
        layout.addLayout(add_layout)
        
        # Button row
        btn_layout = QHBoxLayout()
        
        self.delete_btn = QPushButton("删除选中")
        self.delete_btn.clicked.connect(self.delete_selected)
        btn_layout.addWidget(self.delete_btn)
        
        self.reset_btn = QPushButton("恢复默认")
        self.reset_btn.clicked.connect(self.reset_defaults)
        btn_layout.addWidget(self.reset_btn)
        
        btn_layout.addStretch()
        
        self.save_btn = QPushButton("保存")
        self.save_btn.clicked.connect(self.save_and_close)
        btn_layout.addWidget(self.save_btn)
        
        self.cancel_btn = QPushButton("取消")
        self.cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(self.cancel_btn)
        
        layout.addLayout(btn_layout)
    
    def load_shortcuts(self):
        """Load shortcuts into the table."""
        shortcuts = self.shortcut_manager.get_all()
        self.table.setRowCount(len(shortcuts))
        
        for row, (key, tag) in enumerate(shortcuts.items()):
            key_item = QTableWidgetItem(key)
            key_item.setFlags(key_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.table.setItem(row, 0, key_item)
            self.table.setItem(row, 1, QTableWidgetItem(tag))
    
    def add_shortcut(self):
        """Add a new shortcut."""
        key = self.key_input.text().strip()
        tag = self.tag_input.text().strip()
        
        if not key or not tag:
            QMessageBox.warning(self, "警告", "请输入快捷键和标签")
            return
        
        # Check if key already exists
        for row in range(self.table.rowCount()):
            if self.table.item(row, 0).text() == key:
                QMessageBox.warning(self, "警告", f"快捷键 '{key}' 已存在")
                return
        
        # Add to table
        row = self.table.rowCount()
        self.table.insertRow(row)
        key_item = QTableWidgetItem(key)
        key_item.setFlags(key_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        self.table.setItem(row, 0, key_item)
        self.table.setItem(row, 1, QTableWidgetItem(tag))
        
        # Clear inputs
        self.key_input.clear()
        self.tag_input.clear()
    
    def delete_selected(self):
        """Delete selected shortcuts."""
        selected_rows = set()
        for item in self.table.selectedItems():
            selected_rows.add(item.row())
        
        for row in sorted(selected_rows, reverse=True):
            self.table.removeRow(row)
    
    def reset_defaults(self):
        """Reset shortcuts to defaults."""
        reply = QMessageBox.question(
            self, "确认", "确定要恢复默认快捷键设置吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.shortcut_manager.reset_to_defaults()
            self.load_shortcuts()
    
    def save_and_close(self):
        """Save shortcuts and close dialog."""
        # Clear existing shortcuts
        self.shortcut_manager.shortcuts.clear()
        
        # Save from table
        for row in range(self.table.rowCount()):
            key = self.table.item(row, 0).text()
            tag = self.table.item(row, 1).text()
            if key and tag:
                self.shortcut_manager.shortcuts[key] = tag
        
        self.shortcut_manager.save()
        self.accept()
