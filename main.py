#!/usr/bin/env python3
"""
Video Tagger - A lightweight video tagging tool.

A PyQt6-based application for tagging video files with customizable
keyboard shortcuts and JSON export support.
"""
import sys
from PyQt6.QtWidgets import QApplication
from src.ui.main_window import MainWindow


def main():
    """Main entry point for the application."""
    app = QApplication(sys.argv)
    app.setApplicationName("Video Tagger")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
