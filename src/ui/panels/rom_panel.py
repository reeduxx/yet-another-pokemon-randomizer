"""Panel displaying detected ROM information."""

from PySide6.QtWidgets import QFormLayout, QGroupBox, QLabel


class RomPanel(QGroupBox):
    """UI panel displaying information about the loaded ROM."""

    def __init__(self, parent=None):
        super().__init__("ROM Info", parent)
        self._create_widgets()
        self._build_ui()

    def _create_widgets(self):
        """Create panel widgets."""
        self.detected_game_label = QLabel("")
        self.rom_id_label = QLabel("")
        self.lang_label = QLabel("")

    def _build_ui(self):
        """Build the panel layout."""
        layout = QFormLayout(self)
        layout.addRow("Game:", self.detected_game_label)
        layout.addRow("ROM ID:", self.rom_id_label)
        layout.addRow("Language:", self.lang_label)

    def set_rom_info(self, game_name: str, rom_identifier: str, language: str) -> None:
        """Update the displayed ROM information.

        Args:
            game_name: Display name of the detected game.
            rom_identifier: ROM identifier or game code.
            language: Detected ROM language.
        """
        self.detected_game_label.setText(game_name)
        self.rom_id_label.setText(rom_identifier)
        self.lang_label.setText(language)

    def clear(self) -> None:
        """Clear all displayed ROM information."""
        self.detected_game_label.clear()
        self.rom_id_label.clear()
        self.lang_label.clear()
