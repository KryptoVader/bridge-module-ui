from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit,
    QPushButton, QLabel, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QDoubleValidator, QIntValidator


class CustomTableEditor(QDialog):
    """
    Popup dialog to enter custom environmental parameters:
    - Basic Wind Speed
    - Seismic Zone
    - Seismic Factor
    - Max Temperature
    - Min Temperature
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Custom Loading Parameters")
        self.setMinimumWidth(350)

        layout = QVBoxLayout(self)

        form = QFormLayout()
        layout.addLayout(form)

        # Inputs
        self.in_wind = QLineEdit()
        self.in_zone = QLineEdit()
        self.in_factor = QLineEdit()
        self.in_tmax = QLineEdit()
        self.in_tmin = QLineEdit()

        # Validators
        double_valid = QDoubleValidator(0.0, 500.0, 2)
        int_valid = QIntValidator(1, 5)

        self.in_wind.setValidator(double_valid)
        self.in_factor.setValidator(double_valid)
        self.in_tmax.setValidator(double_valid)
        self.in_tmin.setValidator(double_valid)
        self.in_zone.setValidator(int_valid)  # zone: 1–5

        form.addRow("Basic Wind Speed (m/s):", self.in_wind)
        form.addRow("Seismic Zone (1–5):", self.in_zone)
        form.addRow("Seismic Factor:", self.in_factor)
        form.addRow("Max Temperature (°C):", self.in_tmax)
        form.addRow("Min Temperature (°C):", self.in_tmin)

        # Error label
        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: red;")
        layout.addWidget(self.error_label)

        # Save button
        self.btn_save = QPushButton("Save")
        self.btn_save.clicked.connect(self.on_save)
        layout.addWidget(self.btn_save)

    def on_save(self):
        if (not self.in_wind.text()
            or not self.in_zone.text()
            or not self.in_factor.text()
            or not self.in_tmax.text()
            or not self.in_tmin.text()):
            self.error_label.setText("All fields are required.")
            return

        # Basic value integrity checks
        try:
            if float(self.in_wind.text()) <= 0:
                self.error_label.setText("Wind speed must be positive.")
                return
        except:
            self.error_label.setText("Invalid wind value.")
            return

        self.accept()  # close popup

    def get_values(self):
        return {
            "wind": float(self.in_wind.text()),
            "zone": int(self.in_zone.text()),
            "factor": float(self.in_factor.text()),
            "tmax": float(self.in_tmax.text()),
            "tmin": float(self.in_tmin.text())
        }
