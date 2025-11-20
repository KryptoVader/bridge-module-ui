from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QGroupBox, QRadioButton, QHBoxLayout,
    QComboBox, QLineEdit, QPushButton, QTabWidget, QCheckBox, QFormLayout,
    QMessageBox, QSizePolicy, QFrame, QScrollArea
)
from PySide6.QtCore import Qt

from ui.db import DB
from ui.modify_geometry_dialog import ModifyGeometryDialog
from ui.custom_table_editor import CustomTableEditor


class BasicInputs(QWidget):
    def __init__(self):
        super().__init__()

        # =============================================================
        # MAIN LAYOUT + SCROLLABLE PAGE
        # =============================================================

        main_layout = QVBoxLayout(self)
        tabs = QTabWidget()
        main_layout.addWidget(tabs)

        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        tabs.addTab(scroll, "Basic Inputs")

        # Inner widget
        basic_tab = QWidget()
        scroll.setWidget(basic_tab)

        page_layout = QVBoxLayout(basic_tab)
        page_layout.setSpacing(25)
        page_layout.setContentsMargins(20, 20, 20, 20)

        # =============================================================
        # 1. TYPE OF STRUCTURE
        # =============================================================

        type_box = QGroupBox("Type of Structure")
        type_layout = QHBoxLayout()
        type_box.setLayout(type_layout)

        self.radio_highway = QRadioButton("Highway Bridge")
        self.radio_other = QRadioButton("Other Structure")
        self.radio_highway.setChecked(True)

        type_layout.addWidget(self.radio_highway)
        type_layout.addWidget(self.radio_other)

        page_layout.addWidget(type_box)

        self.type_warning = QLabel("")
        self.type_warning.setStyleSheet("color: red;")
        page_layout.addWidget(self.type_warning)

        # =============================================================
        # 2. PROJECT LOCATION — BIG, CLEAN, SCROLL-FRIENDLY
        # =============================================================

        self.chk_mode_name = QCheckBox("Enter Location Name")
        self.chk_mode_custom = QCheckBox("Tabulate Custom Loading Parameters")

        self.cmb_state = QComboBox()
        self.cmb_district = QComboBox()

        # Larger, premium UI comboboxes
        self.cmb_state.setFixedHeight(38)
        self.cmb_district.setFixedHeight(38)
        self.cmb_state.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.cmb_district.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        combo_style = """
        QComboBox {
            min-height: 38px;
            padding: 6px 8px;
            font-size: 13px;
        }
        QComboBox:disabled {
            background-color: #3b3b3b;
            color: #bdbdbd;
            border: 1px solid #666;
        }
        """
        self.cmb_state.setStyleSheet(combo_style)
        self.cmb_district.setStyleSheet(combo_style)

        # Environment labels
        self.lbl_wind = QLabel("Basic Wind Speed: -")
        self.lbl_seismic = QLabel("Seismic Zone: -")
        self.lbl_temp = QLabel("Temperature Range: -")

        for lbl in (self.lbl_wind, self.lbl_seismic, self.lbl_temp):
            lbl.setStyleSheet("color: #8ff78f; font-weight: 600; font-size: 12px;")

        self.btn_custom_table = QPushButton("Open Custom Table Editor")
        self.btn_custom_table.setEnabled(False)
        self.btn_custom_table.setFixedHeight(36)
        self.btn_custom_table.clicked.connect(self.open_custom_table_editor)

        # Group box container
        loc_box = QGroupBox("Project Location")
        loc_box.setMinimumHeight(380)                     # <-- BIG BLOCK
        loc_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        loc_box.setStyleSheet("QGroupBox { font-size: 15px; font-weight: bold; }")

        loc_layout = QVBoxLayout()
        loc_layout.setSpacing(15)
        loc_layout.setContentsMargins(14, 12, 14, 12)
        loc_box.setLayout(loc_layout)

        # Modes row
        mode_row = QHBoxLayout()
        mode_row.addWidget(self.chk_mode_name)
        mode_row.addWidget(self.chk_mode_custom)
        mode_row.addStretch()
        loc_layout.addLayout(mode_row)

        # Separator line
        line1 = QFrame()
        line1.setFrameShape(QFrame.HLine)
        line1.setStyleSheet("background-color: #444;")
        line1.setFixedHeight(1)
        loc_layout.addWidget(line1)

        # Form for state/district
        form_container = QWidget()
        form_container.setMinimumHeight(200)  # <-- plenty of space
        form_layout = QFormLayout(form_container)
        form_layout.setHorizontalSpacing(25)
        form_layout.setVerticalSpacing(15)
        form_layout.setContentsMargins(0, 0, 0, 0)

        # Placeholders before DB load
        self.cmb_state.addItem("Loading states…")
        self.cmb_state.setEnabled(False)

        self.cmb_district.addItem("Select state first")
        self.cmb_district.setEnabled(False)

        # Add rows
        form_layout.addRow("State:", self.cmb_state)
        form_layout.addRow("District:", self.cmb_district)
        loc_layout.addWidget(form_container)

        # Separator
        line2 = QFrame()
        line2.setFrameShape(QFrame.HLine)
        line2.setStyleSheet("background-color: #444;")
        line2.setFixedHeight(1)
        loc_layout.addWidget(line2)

        # Environment label block
        env_block = QVBoxLayout()
        env_block.setSpacing(6)
        env_block.addWidget(self.lbl_wind)
        env_block.addWidget(self.lbl_seismic)
        env_block.addWidget(self.lbl_temp)
        loc_layout.addLayout(env_block)

        # Custom table button right aligned
        btn_row = QHBoxLayout()
        btn_row.addStretch()
        btn_row.addWidget(self.btn_custom_table)
        loc_layout.addLayout(btn_row)

        self.btn_custom_table.clicked.connect(self.open_custom_dialog)

        page_layout.addWidget(loc_box)

        # =============================================================
        # 3. GEOMETRIC DETAILS
        # =============================================================

        geom_box = QGroupBox("Geometric Details")
        geom_form = QFormLayout()
        geom_form.setSpacing(15)
        geom_box.setLayout(geom_form)

        self.in_span = QLineEdit()
        self.in_cw = QLineEdit()
        self.in_fp = QComboBox()
        self.in_fp.addItems(["None", "Single-Sided", "Both Sides"])
        self.in_skew = QLineEdit()

        geom_form.addRow("Span (m):", self.in_span)
        geom_form.addRow("Carriageway Width (m):", self.in_cw)
        geom_form.addRow("Footpath:", self.in_fp)
        geom_form.addRow("Skew Angle (°):", self.in_skew)

        page_layout.addWidget(geom_box)

        self.err_span = QLabel("")
        self.err_span.setStyleSheet("color: red;")
        page_layout.addWidget(self.err_span)

        self.warn_skew = QLabel("")
        self.warn_skew.setStyleSheet("color: orange;")
        page_layout.addWidget(self.warn_skew)

        # =============================================================
        # 4. MATERIAL INPUTS
        # =============================================================

        mat_box = QGroupBox("Material Inputs")
        mat_form = QFormLayout()
        mat_form.setSpacing(15)
        mat_box.setLayout(mat_form)

        self.cmb_girder = QComboBox()
        self.cmb_girder.addItems(["E250", "E350", "E450"])

        self.cmb_cross = QComboBox()
        self.cmb_cross.addItems(["E250", "E350", "E450"])

        self.cmb_concrete = QComboBox()
        self.cmb_concrete.addItems(["M25", "M30", "M35", "M40", "M50", "M60"])

        mat_form.addRow("Girder Steel Grade:", self.cmb_girder)
        mat_form.addRow("Cross-Bracing Steel Grade:", self.cmb_cross)
        mat_form.addRow("Deck Concrete Grade:", self.cmb_concrete)

        page_layout.addWidget(mat_box)

        # =============================================================
        # 5. MODIFY GEOMETRY BUTTON
        # =============================================================

        self.btn_modify = QPushButton("Modify Additional Geometry")
        self.btn_modify.setFixedHeight(36)
        self.btn_modify.clicked.connect(self.open_modify_dialog)
        page_layout.addWidget(self.btn_modify)

        # Stretch pushes bottom items away from top
        page_layout.addStretch()

        # SIG/VAL
        self.radio_other.toggled.connect(self.on_structure_type_change)
        self.chk_mode_name.toggled.connect(self.toggle_location_modes)
        self.chk_mode_custom.toggled.connect(self.toggle_location_modes)

        self.in_span.textChanged.connect(self.validate_span)
        self.in_skew.textChanged.connect(self.validate_skew)

        # Load DB at end
        self.load_db()

    # ==============================================================  
    # Validation & Mode Switching
    # ==============================================================  

    def on_structure_type_change(self):
        if self.radio_other.isChecked():
            self.type_warning.setText("Other structures are not included. Inputs disabled.")
        else:
            self.type_warning.setText("")

    def toggle_location_modes(self):
        if self.chk_mode_name.isChecked():
            self.chk_mode_custom.setChecked(False)
            self.cmb_state.setEnabled(True)
            self.cmb_district.setEnabled(False)
            self.btn_custom_table.setEnabled(False)

        elif self.chk_mode_custom.isChecked():
            self.chk_mode_name.setChecked(False)
            self.cmb_state.setEnabled(False)
            self.cmb_district.setEnabled(False)
            self.btn_custom_table.setEnabled(True)

    def validate_span(self):
        try:
            value = float(self.in_span.text())
            if value < 20 or value > 45:
                self.err_span.setText("Outside the software range.")
            else:
                self.err_span.setText("")
        except:
            self.err_span.setText("")

    def validate_skew(self):
        try:
            skew = float(self.in_skew.text())
            if skew < -15 or skew > 15:
                self.warn_skew.setText("IRC 24 (2010) requires detailed analysis.")
            else:
                self.warn_skew.setText("")
        except:
            self.warn_skew.setText("")

    # ==============================================================  
    # DB LOADERS
    # ==============================================================  

    def on_state_changed(self, state):
        if not state or state.startswith("Select") or state.startswith("—"):
            self.cmb_district.blockSignals(True)
            self.cmb_district.clear()
            self.cmb_district.addItem("Select state first")
            self.cmb_district.setEnabled(False)
            self.cmb_district.blockSignals(False)
            return

        # Load districts
        self.cmb_district.blockSignals(True)
        self.cmb_district.clear()
        districts = self.db.get_districts(state) or []

        if districts:
            self.cmb_district.addItem("Select district...")
            self.cmb_district.addItems(districts)
            self.cmb_district.setEnabled(True)
        else:
            self.cmb_district.addItem("— No districts —")
            self.cmb_district.setEnabled(False)

        self.cmb_district.blockSignals(False)

    def on_district_changed(self, district):
        if not district or district.startswith("Select"):
            return

        data = self.db.get_location_data(district)
        if data:
            wind, zone, factor, tmax, tmin = data
            self.lbl_wind.setText(f"Basic Wind Speed: {wind} m/s")
            self.lbl_seismic.setText(f"Seismic Zone: {zone} | Factor: {factor}")
            self.lbl_temp.setText(f"Temperature Range: {tmin}°C – {tmax}°C")

    # ==============================================================  
    # CUSTOM TABLE EDITOR POPUP  
    # ==============================================================  

    def open_custom_table_editor(self):
        """Open the custom table editor dialog to input environmental parameters."""
        dialog = CustomTableEditor()
        if dialog.exec():
            values = dialog.get_values()
            # Update the environment labels with custom values
            self.lbl_wind.setText(f"Basic Wind Speed: {values['wind']} m/s")
            self.lbl_seismic.setText(f"Seismic Zone: {values['zone']} | Factor: {values['factor']}")
            self.lbl_temp.setText(f"Temperature Range: {values['tmin']}°C – {values['tmax']}°C")
            print("Custom parameters saved:", values)

    # ==============================================================  
    # MODIFY GEOMETRY POPUP  
    # ==============================================================  

    def open_modify_dialog(self):
        cw = self.in_cw.text()

        if not cw:
            QMessageBox.warning(self, "Missing Input", "Please enter Carriageway Width first.")
            return

        dialog = ModifyGeometryDialog(float(cw))
        if dialog.exec():
            values = dialog.get_values()
            print("Updated geometry:", values)

    # ==============================================================  
    # LOAD DB
    # ==============================================================  

    def load_db(self):
        self.db = DB()

        states = self.db.get_states() or []

        self.cmb_state.blockSignals(True)
        self.cmb_state.clear()
        if states:
            self.cmb_state.addItem("Select state...")
            self.cmb_state.addItems(states)
            self.cmb_state.setEnabled(True)
        else:
            self.cmb_state.addItem("— No states available —")
            self.cmb_state.setEnabled(False)
        self.cmb_state.blockSignals(False)

        # district default
        self.cmb_district.blockSignals(True)
        self.cmb_district.clear()
        self.cmb_district.addItem("Select state first")
        self.cmb_district.setEnabled(False)
        self.cmb_district.blockSignals(False)

        # signals - only disconnect if already connected
        self.cmb_state.currentTextChanged.connect(self.on_state_changed)
        self.cmb_district.currentTextChanged.connect(self.on_district_changed)

        self.toggle_location_modes()
    
    def open_custom_dialog(self):
        dialog = CustomTableEditor()
        if dialog.exec():
            values = dialog.get_values()

            # Update green labels
            self.lbl_wind.setText(f"Basic Wind Speed: {values['wind']} m/s")
            self.lbl_seismic.setText(f"Seismic Zone: {values['zone']} | Factor: {values['factor']}")
            self.lbl_temp.setText(f"Temperature Range: {values['tmin']}°C – {values['tmax']}°C")

            # Disable DB-driven values
            print("Custom parameters applied:", values)

