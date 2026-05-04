from PySide6.QtWidgets import QGridLayout, QGroupBox, QLabel, QLineEdit, QPushButton


class ActionsPanel(QGroupBox):
    def __init__(self, parent=None):
        super().__init__("Actions", parent)
        self._create_widgets()
        self._build_ui()

    def _create_widgets(self):
        self.rom_path_edit = QLineEdit()
        self.rom_path_edit.setPlaceholderText("Select a ROM...")
        self.rom_path_edit.setReadOnly(True)

        self.browse_button = QPushButton("Browse...")

        self.seed_edit = QLineEdit()
        self.seed_edit.setPlaceholderText("ex. 1234567890")

    def _build_ui(self):
        layout = QGridLayout(self)
        layout.addWidget(QLabel("File"), 0, 0)
        layout.addWidget(self.rom_path_edit, 0, 1, 1, 1)
        layout.addWidget(self.browse_button, 0, 2)
        layout.addWidget(QLabel("Seed"), 1, 0)
        layout.addWidget(self.seed_edit, 1, 1, 1, 2)

    def rom_path(self) -> str:
        return self.rom_path_edit.text().strip()

    def set_rom_path(self, path: str) -> None:
        self.rom_path_edit.setText(path)

    def clear_rom_path(self) -> None:
        self.rom_path_edit.clear()

    def seed_text(self) -> str:
        return self.seed_edit.text().strip()
