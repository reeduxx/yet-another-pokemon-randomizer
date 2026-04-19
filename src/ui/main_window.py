from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QFileDialog,
    QFormLayout,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QStatusBar,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)
from src.services.randomizer_service import (
    RandomizerSettings,
    detect_rom_file,
    randomize_rom_file,
)
from src.ui.tabs.intro_tab import IntroTab
from src.ui.tabs.starters_tab import StartersTab
from src.core.util import resolve_range


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Yet Another Pokémon Randomizer")
        self.setWindowIcon(QIcon("src/assets/icon.png"))
        self.resize(900, 600)
        self._create_widgets()
        self._build_ui()
        self._connect_signals()
        self._set_randomizer_controls_enabled(False)
        self.setStatusBar(QStatusBar(self))
        self.statusBar().showMessage("Ready")

    def _create_widgets(self):
        self.rom_path_edit = QLineEdit()
        self.rom_path_edit.setPlaceholderText("Select a ROM...")
        self.rom_path_edit.setReadOnly(True)

        self.detected_game_label = QLabel("")
        self.rom_id_label = QLabel("")
        self.lang_label = QLabel("")

        self.browse_button = QPushButton("Browse...")
        self.randomize_button = QPushButton("Randomize ROM")

        self.seed_edit = QLineEdit()
        self.seed_edit.setPlaceholderText("ex. 1234567890")

        self.tabs = QTabWidget()

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)

        root_layout = QVBoxLayout(central)
        root_layout.setContentsMargins(16, 16, 16, 16)
        root_layout.setSpacing(16)

        top_row = QHBoxLayout()
        top_row.setSpacing(16)

        rom_info_group = self._build_rom_info_group()
        actions_group = self._build_actions_group()

        top_row.addWidget(rom_info_group, 1)
        top_row.addWidget(actions_group, 1)

        self.intro_tab = IntroTab()
        self.starters_tab = StartersTab()

        self.tabs.addTab(self.intro_tab, "Intro")
        self.tabs.addTab(self.starters_tab, "Starters")

        root_layout.addLayout(top_row)
        root_layout.addWidget(self.tabs)
        # root_layout.addWidget(self.randomize_button)

    def _build_rom_info_group(self) -> QGroupBox:
        group = QGroupBox("Rom Info")
        layout = QFormLayout(group)
        layout.addRow("Game:", self.detected_game_label)
        layout.addRow("ROM ID:", self.rom_id_label)
        layout.addRow("Language:", self.lang_label)

        return group

    def _build_actions_group(self) -> QGroupBox:
        group = QGroupBox("Actions")
        layout = QGridLayout(group)
        layout.addWidget(QLabel("File"), 0, 0)
        layout.addWidget(self.rom_path_edit, 0, 1, 1, 1)
        layout.addWidget(self.browse_button, 0, 2)
        layout.addWidget(QLabel("Seed"), 1, 0)
        layout.addWidget(self.seed_edit, 1, 1, 1, 2)
        layout.addWidget(self.randomize_button, 2, 2)

        return group

    def _connect_signals(self):
        self.browse_button.clicked.connect(self._browse_for_rom)
        self.randomize_button.clicked.connect(self._randomize_rom)

    def _browse_for_rom(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select ROM",
            "",
            "GB ROMs (*.gb);;GBC ROMs (*.gbc);;GBA ROMs (*.gba);;NDS ROMs (*.nds);;All Files (*)",
        )

        if file_path:
            self.rom_path_edit.setText(file_path)
            self._detect_rom()
            self.statusBar().showMessage("ROM selected")

    def _detect_rom(self):
        rom_path = self.rom_path_edit.text().strip()

        if not rom_path:
            QMessageBox.warning(self, "No ROM", "Please choose a ROM first.")
            return

        try:
            result = detect_rom_file(rom_path)
        except Exception as e:
            QMessageBox.critical(self, "Detection failed", str(e))
            self.rom_path_edit.setText("")
            self.detected_game_label.setText("")
            self.rom_id_label.setText("")
            self.lang_label.setText("")
            self._set_randomizer_controls_enabled(False)
            self.statusBar().showMessage("Detection failed")
            return

        self.detected_game_label.setText(result.game_name)
        self.rom_id_label.setText(result.rom_identifier)
        self.lang_label.setText(result.language)
        self._set_randomizer_controls_enabled(True)
        self.statusBar().showMessage("ROM detected successfully")

    def _build_settings(self) -> RandomizerSettings:
        data = {}
        data.update(self.intro_tab.get_settings_patch())
        data.update(self.starters_tab.get_settings_patch())
        seed_text = self.seed_edit.text().strip()

        try:
            data["seed"] = int(seed_text) if seed_text else None
        except ValueError:
            raise ValueError("Seed must be a whole number.")

        return RandomizerSettings(**data)

    def _randomize_rom(self):
        rom_path = self.rom_path_edit.text().strip()

        if not rom_path:
            QMessageBox.warning(self, "No ROM", "Please choose a ROM first.")
            return

        try:
            settings = self._build_settings()
        except ValueError as e:
            QMessageBox.warning(self, "Invalid input", str(e))
            return

        if not self._validate_settings(settings):
            return

        if settings.randomize_starting_money:
            try:
                resolve_range(
                    default_min=0,
                    default_max=999999,
                    user_min=settings.starting_money_min,
                    user_max=settings.starting_money_max,
                )
            except ValueError as e:
                QMessageBox.warning(self, "Invalid money range", str(e))
                return

        try:
            output_path = randomize_rom_file(rom_path, settings)
        except Exception as e:
            QMessageBox.critical(self, "Randomization failed", str(e))
            self.statusBar().showMessage("Randomization failed")
            return

        self.statusBar().showMessage("Randomization complete")
        QMessageBox.information(
            self, "Done", f"Randomized ROM saved to:\n{output_path}"
        )

    def _validate_settings(self, settings: RandomizerSettings) -> bool:
        if not (
            settings.randomize_title_screen_mon
            or settings.randomize_intro_mon
            or settings.randomize_starting_pc_item
            or settings.randomize_starting_money
            or settings.randomize_starters
        ):
            QMessageBox.information(
                self, "No options selected", "Enable at least one randomization option."
            )

            return False

        return True

    def _set_randomizer_controls_enabled(self, enabled: bool) -> None:
        for i in range(self.tabs.count()):
            self.tabs.widget(i).setEnabled(enabled)

        self.randomize_button.setEnabled(enabled)
