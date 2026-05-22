"""Application menu bar."""

from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenuBar


class MenuBar(QMenuBar):
    """Main application menu bar and actions."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._create_actions()
        self._build_menus()

    def _create_actions(self):
        """Create all menu actions used by the application."""
        self.open_rom_action = QAction("Open ROM...", self)
        self.open_rom_action.setShortcut("Ctrl+O")

        self.randomize_action = QAction("Randomize ROM", self)
        self.randomize_action.setShortcut("Ctrl+R")

        self.exit_action = QAction("Exit", self)

        self.export_settings_action = QAction("Export Settings", self)
        self.import_settings_action = QAction("Import Settings", self)

        self.about_action = QAction("About", self)

    def _build_menus(self):
        """Create menus and populate them with actions."""
        file_menu = self.addMenu("&File")
        file_menu.addAction(self.open_rom_action)
        file_menu.addAction(self.randomize_action)
        file_menu.addSeparator()
        file_menu.addAction(self.exit_action)

        settings_menu = self.addMenu("&Settings")
        settings_menu.addAction(self.export_settings_action)
        settings_menu.addAction(self.import_settings_action)

        help_menu = self.addMenu("&Help")
        help_menu.addAction(self.about_action)
