#!/usr/bin/env python3
"""Video Tagger - A lightweight video tagging tool."""
import sys
from PyQt6.QtWidgets import QApplication
from src.ui.main_window import MainWindow


def main():
    """Main entry point."""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
