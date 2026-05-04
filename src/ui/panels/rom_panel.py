from PySide6.QtWidgets import QFormLayout, QGroupBox, QLabel


class RomPanel(QGroupBox):
    def __init__(self, parent=None):
        super().__init__("ROM Info", parent)
        self._create_widgets()
        self._build_ui()

    def _create_widgets(self):
        self.detected_game_label = QLabel("")
        self.rom_id_label = QLabel("")
        self.lang_label = QLabel("")

    def _build_ui(self):
        layout = QFormLayout(self)
        layout.addRow("Game:", self.detected_game_label)
        layout.addRow("ROM ID:", self.rom_id_label)
        layout.addRow("Language:", self.lang_label)

    def set_rom_info(self, game_name: str, rom_identifier: str, language: str) -> None:
        self.detected_game_label.setText(game_name)
        self.rom_id_label.setText(rom_identifier)
        self.lang_label.setText(language)

    def clear(self) -> None:
        self.detected_game_label.clear()
        self.rom_id_label.clear()
        self.lang_label.clear()
