"""Starter randomization settings tab."""

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
from src.randomizers.engine.type_trios import TYPE_TRIOS, TYPE_TRIOS_BY_NAME

BST_MIN = 175
BST_MAX = 590
BST_STEP = 5


class StartersTab(QWidget):
    """Tab containing starter randomization settings."""

    def __init__(self):
        super().__init__()
        self._create_widgets()
        self._build_ui()
        self._connect_signals()

    def _create_widgets(self):
        self.randomize_starters_checkbox = QCheckBox("Randomize starters")
        self.use_type_trio_checkbox = QCheckBox("Use type trio rules")
        self.type_trio_combobox = QComboBox()

        for trio in TYPE_TRIOS:
            self.type_trio_combobox.addItem(trio.display_name)

        self.bst_min_edit = QLineEdit()
        self.bst_max_edit = QLineEdit()

        validator = QIntValidator(175, 590)
        self.bst_min_edit.setValidator(validator)
        self.bst_max_edit.setValidator(validator)

        self.slider = QRangeSlider(Qt.Orientation.Horizontal)
        self.slider.setSingleStep(5)
        self.slider.setPageStep(5)
        self.slider.setRange(175, 590)
        self.slider.setValue((175, 590))

        self.synchronize_rival_starter_checkbox = QCheckBox("Synchronize rival starter")
        self.correct_oak_starter_text_checkbox = QCheckBox("Correct Oak starter text")

        self.synchronize_rival_starter_checkbox.setToolTip(
            "If checked, the rival will choose one of the randomized player options."
        )
        self.correct_oak_starter_text_checkbox.setToolTip(
            "Corrects Prof. Oak's text to reflect the correct randomized species."
        )

    def _build_ui(self):
        layout = QVBoxLayout(self)

        group = QGroupBox("Starters Randomization")
        group_layout = QVBoxLayout(group)

        group_layout.addWidget(self.randomize_starters_checkbox)

        combobox_row = QHBoxLayout()
        combobox_row.setSpacing(12)
        combobox_row.addWidget(self.use_type_trio_checkbox)
        combobox_row.addWidget(self.type_trio_combobox)
        group_layout.addLayout(combobox_row)

        range_row = QHBoxLayout()
        range_row.setSpacing(12)
        range_row.addWidget(QLabel("Min BST"))
        range_row.addWidget(self.bst_min_edit)
        range_row.addWidget(self.slider)
        range_row.addWidget(QLabel("Max BST"))
        range_row.addWidget(self.bst_max_edit)
        group_layout.addLayout(range_row)

        group_layout.addWidget(self.synchronize_rival_starter_checkbox)
        group_layout.addWidget(self.correct_oak_starter_text_checkbox)

        layout.addWidget(group)
        layout.addStretch()

    def _connect_signals(self):
        """Connect widget signals and initialize dependent UI state."""
        self.randomize_starters_checkbox.toggled.connect(self._update_enabled)
        self.use_type_trio_checkbox.toggled.connect(self._update_enabled)
        self.bst_min_edit.textChanged.connect(self._on_min_changed)
        self.bst_max_edit.textChanged.connect(self._on_max_changed)
        self.slider.valueChanged.connect(self._on_slider_changed)
        self._on_slider_changed()
        self._update_enabled(self.randomize_starters_checkbox.isChecked())

    def _snap_bst_value(self, value: int) -> int:
        """Clamp and round a BST value to the configured slider step.

        Args:
            value: BST value to normalize.

        Returns:
            Clamped and rounded BST value.
        """
        value = max(BST_MIN, min(value, BST_MAX))
        return round(value / BST_STEP) * BST_STEP

    def _on_min_changed(self):
        text = self.bst_min_edit.text().strip()

        if not text:
            return

        min_val = self._snap_bst_value(int(text))
        _, max_val = self.slider.value()
        min_val = max(BST_MIN, min(min_val, max_val))
        self.slider.setValue((min_val, max_val))

    def _on_max_changed(self):
        text = self.bst_max_edit.text().strip()

        if not text:
            return

        max_val = self._snap_bst_value(int(text))
        min_val, _ = self.slider.value()
        max_val = min(BST_MAX, max(min_val, max_val))
        self.slider.setValue((min_val, max_val))

    def _on_slider_changed(self):
        min_val, max_val = self.slider.value()
        min_val = self._snap_bst_value(min_val)
        max_val = self._snap_bst_value(max_val)

        if (min_val, max_val) != self.slider.value():
            self.slider.blockSignals(True)
            self.slider.setValue((min_val, max_val))
            self.slider.blockSignals(False)

        self.bst_min_edit.blockSignals(True)
        self.bst_max_edit.blockSignals(True)
        self.bst_min_edit.setText(str(min_val))
        self.bst_max_edit.setText(str(max_val))
        self.bst_min_edit.blockSignals(False)
        self.bst_max_edit.blockSignals(False)

    def _update_enabled(self, checked: bool):
        """Enable/disable dependent starter options.

        Args:
            checked: Whether starter randomization is enabled.
        """
        self.use_type_trio_checkbox.setEnabled(checked)
        self.type_trio_combobox.setEnabled(
            checked and self.use_type_trio_checkbox.isChecked()
        )
        self.bst_min_edit.setEnabled(checked)
        self.bst_max_edit.setEnabled(checked)
        self.slider.setEnabled(checked)
        self.synchronize_rival_starter_checkbox.setEnabled(checked)
        self.correct_oak_starter_text_checkbox.setEnabled(checked)

    def get_settings_patch(self) -> dict:
        """Return the settings contributed by this tab.

        Returns:
            Dictionary containing starter randomization settings.
        """
        starters_enabled = self.randomize_starters_checkbox.isChecked()
        selected_trio_name = self.type_trio_combobox.currentText()
        min_val, max_val = self.slider.value()

        return {
            "randomize_starters": starters_enabled,
            "use_type_trio": (
                starters_enabled and self.use_type_trio_checkbox.isChecked()
            ),
            "type_trio": TYPE_TRIOS_BY_NAME.get(selected_trio_name)
            if self.use_type_trio_checkbox.isChecked()
            else None,
            "starter_bst_min": min_val if starters_enabled else None,
            "starter_bst_max": max_val if starters_enabled else None,
            "synchronize_rival_starter": (
                starters_enabled and self.synchronize_rival_starter_checkbox.isChecked()
            ),
            "correct_oak_starter_text": (
                starters_enabled and self.correct_oak_starter_text_checkbox.isChecked()
            ),
        }
