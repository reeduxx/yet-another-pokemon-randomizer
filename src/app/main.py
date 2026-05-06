"""
Application entry point.

Initializes the Qt application, creates the main window, and starts the event loop.
"""

import sys
from PySide6.QtWidgets import QApplication
from src.ui.main_window import MainWindow


def main() -> int:
    """
    Starts the application and runs the event loop.

    Returns:
        int: The application exit code returned by Qt.
    """
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
