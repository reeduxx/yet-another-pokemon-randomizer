from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
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
from src.ui.panels.actions_panel import ActionsPanel
from src.ui.panels.rom_panel import RomPanel
from src.ui.tabs.intro_tab import IntroTab
from src.ui.tabs.pokemon_tab import PokemonTab
from src.ui.tabs.starters_tab import StartersTab
from src.ui.tabs.trainers_tab import TrainersTab
from src.ui.tabs.wild_pokemon_tab import WildPokemonTab

ROM_FILE_FILTER = (
    "GB ROMs (*.gb);;"
    "GBC ROMs (*.gbc);;"
    "GBA ROMs (*.gba);;"
    "NDS ROMs (*.nds);;"
    "All Files (*)"
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Yet Another Pokémon Randomizer")
        self.setWindowIcon(QIcon("src/assets/icon.png"))
        self.resize(900, 600)
        self._create_widgets()
        self._create_menu_bar()
        self._build_ui()
        self._connect_signals()
        self._set_randomizer_controls_enabled(False)
        self.setStatusBar(QStatusBar(self))
        self.statusBar().showMessage("Ready")

    def _create_widgets(self):
        self.export_settings_button = QPushButton("Export Settings")
        self.reset_settings_button = QPushButton("Reset Settings")
        self.randomize_button = QPushButton("Randomize ROM")

        self.tabs = QTabWidget()

    def _create_menu_bar(self):
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("&File")
        self.open_rom_action = QAction("Open ROM...", self)
        self.open_rom_action.setShortcut("Ctrl+O")
        file_menu.addAction(self.open_rom_action)

        self.randomize_action = QAction("Randomize ROM", self)
        self.randomize_action.setShortcut("Ctrl+R")
        file_menu.addAction(self.randomize_action)

        file_menu.addSeparator()

        self.exit_action = QAction("Exit", self)
        file_menu.addAction(self.exit_action)

        settings_menu = menu_bar.addMenu("&Settings")
        self.export_settings_action = QAction("Export Settings", self)
        settings_menu.addAction(self.export_settings_action)

        self.import_settings_action = QAction("Import Settings", self)
        settings_menu.addAction(self.import_settings_action)

        help_menu = menu_bar.addMenu("&Help")
        self.about_action = QAction("About", self)
        help_menu.addAction(self.about_action)

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)

        root_layout = QVBoxLayout(central)
        root_layout.setContentsMargins(16, 16, 16, 16)
        root_layout.setSpacing(16)

        top_row = QHBoxLayout()
        top_row.setSpacing(16)

        self.rom_panel = RomPanel()
        self.actions_panel = ActionsPanel()

        top_row.addWidget(self.rom_panel, 1)
        top_row.addWidget(self.actions_panel, 1)

        self.intro_tab = IntroTab()
        self.starters_tab = StartersTab()
        self.pokemon_tab = PokemonTab()
        self.wild_pokemon_tab = WildPokemonTab()
        self.trainers_tab = TrainersTab()

        self.randomizer_tabs = [
            self.intro_tab,
            self.starters_tab,
            self.pokemon_tab,
            self.wild_pokemon_tab,
            self.trainers_tab,
        ]

        self.tabs.addTab(self.intro_tab, "Intro")
        self.tabs.addTab(self.starters_tab, "Starters")
        self.tabs.addTab(self.pokemon_tab, "Pokémon")
        self.tabs.addTab(self.wild_pokemon_tab, "Wild Pokémon")
        self.tabs.addTab(self.trainers_tab, "Trainers")

        root_layout.addLayout(top_row)
        root_layout.addWidget(self.tabs)

        button_row = QHBoxLayout()
        button_row.addWidget(self.export_settings_button)
        button_row.addWidget(self.reset_settings_button)
        button_row.addStretch()
        button_row.addWidget(self.randomize_button)
        root_layout.addLayout(button_row)

    def _connect_signals(self):
        self.open_rom_action.triggered.connect(self._browse_for_rom)
        self.randomize_action.triggered.connect(self._randomize_rom)
        self.exit_action.triggered.connect(self.close)
        self.actions_panel.browse_button.clicked.connect(self._browse_for_rom)
        self.randomize_button.clicked.connect(self._randomize_rom)

    def _browse_for_rom(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select ROM",
            "",
            ROM_FILE_FILTER,
        )

        if file_path:
            self.actions_panel.set_rom_path(file_path)
            self._detect_rom()

    def _detect_rom(self):
        rom_path = self.actions_panel.rom_path()

        if not rom_path:
            QMessageBox.warning(self, "No ROM", "Please choose a ROM first.")
            return

        try:
            result = detect_rom_file(rom_path)
        except Exception as e:
            QMessageBox.critical(self, "Detection failed", str(e))
            self._clear_rom_state()
            self.statusBar().showMessage("Detection failed")
            return

        self.rom_panel.set_rom_info(
            result.game_name, result.rom_identifier, result.language
        )
        self._set_randomizer_controls_enabled(True)
        self.intro_tab.set_gameboy_game(result.generation == 1)
        self.statusBar().showMessage("ROM detected successfully")

    def _build_settings(self) -> RandomizerSettings:
        data = {}

        for tab in self.randomizer_tabs:
            if hasattr(tab, "get_settings_patch"):
                data.update(tab.get_settings_patch())

        seed_text = self.actions_panel.seed_text()

        try:
            data["seed"] = int(seed_text) if seed_text else None
        except ValueError:
            raise ValueError("Seed must be a whole number.")

        return RandomizerSettings(**data)

    def _randomize_rom(self):
        rom_path = self.actions_panel.rom_path()

        if not rom_path:
            QMessageBox.warning(self, "No ROM", "Please choose a ROM first.")
            return

        try:
            settings = self._build_settings()
            settings.validate()
        except ValueError as e:
            QMessageBox.warning(self, "Invalid settings", str(e))
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

    def _set_randomizer_controls_enabled(self, enabled: bool) -> None:
        for tab in self.randomizer_tabs:
            tab.setEnabled(enabled)

        self.randomize_action.setEnabled(enabled)
        self.export_settings_action.setEnabled(enabled)
        self.import_settings_action.setEnabled(enabled)
        self.export_settings_button.setEnabled(enabled)
        self.reset_settings_button.setEnabled(enabled)
        self.randomize_button.setEnabled(enabled)

    def _clear_rom_state(self) -> None:
        self.actions_panel.clear_rom_path()
        self.rom_panel.clear()
        self._set_randomizer_controls_enabled(False)
