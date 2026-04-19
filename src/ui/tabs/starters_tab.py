from PySide6.QtWidgets import (
    QCheckBox,
    QGroupBox,
    QVBoxLayout,
    QWidget,
)


class StartersTab(QWidget):
    def __init__(self):
        super().__init__()
        self._create_widgets()
        self._build_ui()
        self._connect_signals()

    def _create_widgets(self):
        self.randomize_starters_checkbox = QCheckBox("Randomize starters")
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
        group_layout.addWidget(self.synchronize_rival_starter_checkbox)
        group_layout.addWidget(self.correct_oak_starter_text_checkbox)

        layout.addWidget(group)
        layout.addStretch()

    def _connect_signals(self):
        self.randomize_starters_checkbox.toggled.connect(self._update_enabled)
        self._update_enabled(self.randomize_starters_checkbox.isChecked())

    def _update_enabled(self, checked: bool):
        self.synchronize_rival_starter_checkbox.setEnabled(checked)
        self.correct_oak_starter_text_checkbox.setEnabled(checked)

    def get_settings_patch(self) -> dict:
        starters_enabled = self.randomize_starters_checkbox.isChecked()

        return {
            "randomize_starters": starters_enabled,
            "synchronize_rival_starter": (
                starters_enabled and self.synchronize_rival_starter_checkbox.isChecked()
            ),
            "correct_oak_starter_text": (
                starters_enabled and self.correct_oak_starter_text_checkbox.isChecked()
            ),
        }
