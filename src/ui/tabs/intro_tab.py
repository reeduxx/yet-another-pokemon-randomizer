from PySide6.QtCore import Qt
from PySide6.QtGui import QIntValidator
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QVBoxLayout,
    QWidget,
)
from superqt import QRangeSlider


class IntroTab(QWidget):
    def __init__(self):
        super().__init__()
        self._create_widgets()
        self._build_ui()
        self._connect_signals()

    def _create_widgets(self):
        self.randomize_title_screen_mon_checkbox = QCheckBox(
            "Randomize title screen Pokémon"
        )
        self.randomize_title_screen_mon_mode_combobox = QComboBox()
        self.randomize_title_screen_mon_mode_combobox.addItem("First Pokémon")
        self.randomize_title_screen_mon_mode_combobox.addItem("All Pokémon")
        self.randomize_intro_mon_checkbox = QCheckBox("Randomize Oak's Pokémon")
        self.randomize_starting_pc_item_checkbox = QCheckBox(
            "Randomize starting PC item"
        )
        self.randomize_starting_money_checkbox = QCheckBox("Randomize starting money")

        self.randomize_title_screen_mon_checkbox.setToolTip(
            "Randomizes the Pokémon shown on the title screen. RGB only."
        )
        self.randomize_title_screen_mon_mode_combobox.setToolTip(
            "The mode used for randomizing the title screen Pokémon"
            "\n- First Pokémon: Randomizes only the first Pokémon shown"
            "\n- All Pokémon: Randomizes the entire list (16 Pokémon)"
        )
        self.randomize_intro_mon_checkbox.setToolTip(
            "Randomizes the Pokémon Oak displays during the introduction."
        )
        self.randomize_starting_pc_item_checkbox.setToolTip(
            "Randomizes the PC item the player starts with."
        )
        self.randomize_starting_money_checkbox.setToolTip(
            "Randomizes the amount of money the player starts with."
        )

        self.starting_money_min_edit = QLineEdit()
        self.starting_money_max_edit = QLineEdit()

        validator = QIntValidator(0, 999999)
        self.starting_money_min_edit.setValidator(validator)
        self.starting_money_max_edit.setValidator(validator)

        self.slider = QRangeSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(0, 999999)
        self.slider.setValue((0, 999999))

    def _build_ui(self):
        layout = QVBoxLayout(self)

        group = QGroupBox("Intro Randomization")
        group_layout = QVBoxLayout(group)

        combobox_row = QHBoxLayout()
        combobox_row.setSpacing(12)
        combobox_row.addWidget(self.randomize_title_screen_mon_checkbox)
        combobox_row.addWidget(self.randomize_title_screen_mon_mode_combobox)

        group_layout.addLayout(combobox_row)

        group_layout.addWidget(self.randomize_intro_mon_checkbox)
        group_layout.addWidget(self.randomize_starting_pc_item_checkbox)
        group_layout.addWidget(self.randomize_starting_money_checkbox)

        range_row = QHBoxLayout()
        range_row.addWidget(QLabel("Min"))
        range_row.addWidget(self.starting_money_min_edit)
        range_row.addWidget(self.slider)
        range_row.addWidget(QLabel("Max"))
        range_row.addWidget(self.starting_money_max_edit)

        group_layout.addLayout(range_row)
        layout.addWidget(group)
        layout.addStretch()

    def _connect_signals(self):
        self.randomize_title_screen_mon_checkbox.toggled.connect(
            self._update_title_screen_mon_enabled
        )
        self.randomize_starting_money_checkbox.toggled.connect(
            self._update_money_enabled
        )
        self.starting_money_min_edit.textChanged.connect(self._on_min_changed)
        self.starting_money_max_edit.textChanged.connect(self._on_max_changed)
        self.slider.valueChanged.connect(self._on_slider_changed)
        self._on_slider_changed()
        self._update_title_screen_mon_enabled(
            self.randomize_title_screen_mon_checkbox.isChecked()
        )
        self._update_money_enabled(self.randomize_starting_money_checkbox.isChecked())

    def _on_min_changed(self):
        text = self.starting_money_min_edit.text().strip()

        if not text:
            return

        min_val = int(text)
        _, max_val = self.slider.value()
        min_val = max(0, min(min_val, max_val))
        self.slider.setValue((min_val, max_val))

    def _on_max_changed(self):
        text = self.starting_money_max_edit.text().strip()

        if not text:
            return

        max_val = int(text)
        min_val, _ = self.slider.value()
        max_val = min(999999, max(min_val, max_val))
        self.slider.setValue((min_val, max_val))

    def _on_slider_changed(self):
        min_val, max_val = self.slider.value()

        self.starting_money_min_edit.blockSignals(True)
        self.starting_money_max_edit.blockSignals(True)

        self.starting_money_min_edit.setText(str(min_val))
        self.starting_money_max_edit.setText(str(max_val))

        self.starting_money_min_edit.blockSignals(False)
        self.starting_money_max_edit.blockSignals(False)

    def _update_title_screen_mon_enabled(self, checked: bool):
        self.randomize_title_screen_mon_mode_combobox.setEnabled(checked)

    def _update_money_enabled(self, checked: bool):
        self.starting_money_min_edit.setEnabled(checked)
        self.starting_money_max_edit.setEnabled(checked)
        self.slider.setEnabled(checked)

    def get_settings_patch(self) -> dict:
        title_screen_mon_enabled = self.randomize_title_screen_mon_checkbox.isChecked()
        money_enabled = self.randomize_starting_money_checkbox.isChecked()
        min_val, max_val = self.slider.value()

        return {
            "randomize_title_screen_mon": title_screen_mon_enabled,
            "randomize_title_screen_mon_mode": self.randomize_title_screen_mon_mode_combobox.currentText()
            if title_screen_mon_enabled
            else None,
            "randomize_intro_mon": self.randomize_intro_mon_checkbox.isChecked(),
            "randomize_starting_pc_item": self.randomize_starting_pc_item_checkbox.isChecked(),
            "randomize_starting_money": money_enabled,
            "starting_money_min": min_val if money_enabled else None,
            "starting_money_max": max_val if money_enabled else None,
        }
