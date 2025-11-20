from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QFormLayout, QLineEdit, QPushButton, QMessageBox
)
from PySide6.QtCore import Qt


class ModifyGeometryDialog(QDialog):
    def __init__(self, carriageway_width):
        super().__init__()

        self.setWindowTitle("Modify Additional Geometry")
        self.setMinimumWidth(350)

        # Store base value
        self.carriageway_width = float(carriageway_width)
        self.overall_width = self.carriageway_width + 5.0

        layout = QVBoxLayout(self)

        # ---- Header ----
        header = QLabel(f"Overall Bridge Width = Carriageway Width + 5 = {self.overall_width:.1f} m")
        header.setStyleSheet("font-weight: bold; color: darkblue;")
        layout.addWidget(header)

        form = QFormLayout()
        layout.addLayout(form)

        # ---- Inputs ----
        self.in_spacing = QLineEdit()
        self.in_spacing.setPlaceholderText("Enter girder spacing (m)")

        self.in_girders = QLineEdit()
        self.in_girders.setPlaceholderText("Enter number of girders")

        self.in_overhang = QLineEdit()
        self.in_overhang.setPlaceholderText("Enter deck overhang (m)")

        form.addRow("Girder Spacing (m):", self.in_spacing)
        form.addRow("No. of Girders:", self.in_girders)
        form.addRow("Deck Overhang (m):", self.in_overhang)

        # Error label
        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: red;")
        layout.addWidget(self.error_label)

        # ---- Buttons ----
        btn_save = QPushButton("Save")
        btn_save.clicked.connect(self.on_save)
        layout.addWidget(btn_save)

        # ---- Connect signals ----
        self.in_spacing.textChanged.connect(self.update_from_spacing)
        self.in_girders.textChanged.connect(self.update_from_girders)
        self.in_overhang.textChanged.connect(self.update_from_overhang)

    # ======================================================
    # Calculation Logic
    # ======================================================

    def update_from_spacing(self):
        if not self.in_spacing.hasFocus():
            return
        try:
            spacing = float(self.in_spacing.text())
            overhang = float(self.in_overhang.text() or 0)

            if spacing <= 0 or spacing >= self.overall_width:
                self.error_label.setText("Invalid spacing value.")
                return
            self.error_label.setText("")

            # Compute number of girders
            n_float = (self.overall_width - overhang) / spacing
            n = max(1, round(n_float))

            # Adjust spacing to match integer girders
            spacing_exact = round((self.overall_width - overhang) / n, 1)

            self.in_girders.blockSignals(True)
            self.in_spacing.blockSignals(True)

            self.in_girders.setText(str(n))
            self.in_spacing.setText(str(spacing_exact))

            self.in_girders.blockSignals(False)
            self.in_spacing.blockSignals(False)

        except:
            return

    def update_from_girders(self):
        if not self.in_girders.hasFocus():
            return
        try:
            n = int(self.in_girders.text())
            overhang = float(self.in_overhang.text() or 0)

            if n < 1:
                self.error_label.setText("Number of girders must be ≥ 1.")
                return
            self.error_label.setText("")

            spacing = (self.overall_width - overhang) / n
            spacing = round(spacing, 1)

            if spacing <= 0 or spacing >= self.overall_width:
                self.error_label.setText("Computed spacing invalid.")
                return

            self.in_spacing.blockSignals(True)
            self.in_spacing.setText(str(spacing))
            self.in_spacing.blockSignals(False)

        except:
            return

    def update_from_overhang(self):
        if not self.in_overhang.hasFocus():
            return
        try:
            overhang = float(self.in_overhang.text())
            n = int(self.in_girders.text() or 1)

            if overhang < 0 or overhang >= self.overall_width:
                self.error_label.setText("Invalid overhang value.")
                return
            self.error_label.setText("")

            spacing = (self.overall_width - overhang) / n
            spacing = round(spacing, 1)

            self.in_spacing.blockSignals(True)
            self.in_spacing.setText(str(spacing))
            self.in_spacing.blockSignals(False)

        except:
            return

    def on_save(self):
        if self.error_label.text():
            QMessageBox.warning(self, "Invalid Input", "Fix all errors before saving.")
            return

        if not self.in_spacing.text() or not self.in_girders.text() or not self.in_overhang.text():
            QMessageBox.warning(self, "Missing Input", "Please fill all fields.")
            return

        self.accept()

    # ---- Export values ----
    def get_values(self):
        return {
            "spacing": float(self.in_spacing.text()),
            "girders": int(self.in_girders.text()),
            "overhang": float(self.in_overhang.text()),
            "overall_width": self.overall_width
        }
