"""Panel containing ROM selection and randomization actions."""

from PySide6.QtWidgets import QGridLayout, QGroupBox, QLabel, QLineEdit, QPushButton


class ActionsPanel(QGroupBox):
    """UI panel for ROM selection and seed configuration."""

    def __init__(self, parent=None):
        super().__init__("Actions", parent)
        self._create_widgets()
        self._build_ui()

    def _create_widgets(self):
        """Create panel widgets."""
        self.rom_path_edit = QLineEdit()
        self.rom_path_edit.setPlaceholderText("Select a ROM...")
        self.rom_path_edit.setReadOnly(True)

        self.browse_button = QPushButton("Browse...")

        self.seed_edit = QLineEdit()
        self.seed_edit.setPlaceholderText("ex. 1234567890")

    def _build_ui(self):
        """Build the panel layout."""
        layout = QGridLayout(self)
        layout.addWidget(QLabel("File"), 0, 0)
        layout.addWidget(self.rom_path_edit, 0, 1, 1, 1)
        layout.addWidget(self.browse_button, 0, 2)
        layout.addWidget(QLabel("Seed"), 1, 0)
        layout.addWidget(self.seed_edit, 1, 1, 1, 2)

    def rom_path(self) -> str:
        """Return the currently selected ROM path."""
        return self.rom_path_edit.text().strip()

    def set_rom_path(self, path: str) -> None:
        """Set the displayed ROM path.

        Args:
            path: ROM file path to display.
        """
        self.rom_path_edit.setText(path)

    def clear_rom_path(self) -> None:
        """Clear the displayed ROM path."""
        self.rom_path_edit.clear()

    def seed_text(self) -> str:
        """Return the entered seed text.

        Returns:
            The current seed text entered by the user.
        """
        return self.seed_edit.text().strip()
