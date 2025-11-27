"""Settings dialog for configuring shortcuts."""

from typing import Dict

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QTableWidget, QTableWidgetItem, QLineEdit,
    QHeaderView, QMessageBox
)
from PyQt6.QtCore import Qt


class SettingsDialog(QDialog):
    """Dialog for configuring keyboard shortcuts."""
    
    def __init__(self, shortcuts: Dict[str, str], parent=None):
        super().__init__(parent)
        self.shortcuts = shortcuts.copy()
        self.setWindowTitle("快捷键设置")
        self.setMinimumSize(400, 400)
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI."""
        layout = QVBoxLayout(self)
        
        # Instructions
        instructions = QLabel(
            "配置快捷键与标签的映射关系。\n"
            "在表格中编辑快捷键和对应的标签名称。"
        )
        instructions.setWordWrap(True)
        layout.addWidget(instructions)
        
        # Shortcuts table
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["快捷键", "标签"])
        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.populate_table()
        layout.addWidget(self.table)
        
        # Add/Remove buttons
        edit_layout = QHBoxLayout()
        
        self.add_btn = QPushButton("添加")
        self.add_btn.clicked.connect(self.add_shortcut)
        
        self.remove_btn = QPushButton("删除选中")
        self.remove_btn.clicked.connect(self.remove_shortcut)
        
        self.reset_btn = QPushButton("重置默认")
        self.reset_btn.clicked.connect(self.reset_defaults)
        
        edit_layout.addWidget(self.add_btn)
        edit_layout.addWidget(self.remove_btn)
        edit_layout.addWidget(self.reset_btn)
        layout.addLayout(edit_layout)
        
        # Dialog buttons
        buttons_layout = QHBoxLayout()
        
        self.cancel_btn = QPushButton("取消")
        self.cancel_btn.clicked.connect(self.reject)
        
        self.save_btn = QPushButton("保存")
        self.save_btn.clicked.connect(self.save_and_accept)
        
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.cancel_btn)
        buttons_layout.addWidget(self.save_btn)
        layout.addLayout(buttons_layout)
    
    def populate_table(self):
        """Populate table with current shortcuts."""
        self.table.setRowCount(len(self.shortcuts))
        
        for row, (key, tag) in enumerate(sorted(self.shortcuts.items())):
            key_item = QTableWidgetItem(key)
            tag_item = QTableWidgetItem(tag)
            self.table.setItem(row, 0, key_item)
            self.table.setItem(row, 1, tag_item)
    
    def add_shortcut(self):
        """Add a new shortcut row."""
        row = self.table.rowCount()
        self.table.insertRow(row)
        self.table.setItem(row, 0, QTableWidgetItem(""))
        self.table.setItem(row, 1, QTableWidgetItem(""))
        self.table.setCurrentCell(row, 0)
    
    def remove_shortcut(self):
        """Remove selected shortcut row."""
        current_row = self.table.currentRow()
        if current_row >= 0:
            self.table.removeRow(current_row)
    
    def reset_defaults(self):
        """Reset to default shortcuts."""
        from src.core.shortcut_manager import DEFAULT_SHORTCUTS
        
        reply = QMessageBox.question(
            self,
            "确认重置",
            "确定要重置为默认快捷键设置吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.shortcuts = DEFAULT_SHORTCUTS.copy()
            self.populate_table()
    
    def save_and_accept(self):
        """Save shortcuts and close dialog."""
        self.shortcuts = {}
        
        for row in range(self.table.rowCount()):
            key_item = self.table.item(row, 0)
            tag_item = self.table.item(row, 1)
            
            if key_item and tag_item:
                key = key_item.text().strip()
                tag = tag_item.text().strip()
                
                if key and tag:
                    self.shortcuts[key] = tag
        
        self.accept()
    
    def get_shortcuts(self) -> Dict[str, str]:
        """Get the configured shortcuts.
        
        Returns:
            Dictionary of key to tag mappings
        """
        return self.shortcuts
