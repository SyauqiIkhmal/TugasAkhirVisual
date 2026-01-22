"""
Schedule Management Widget for Photo Studio Management System
Provides comprehensive scheduling with conflict prevention
"""

import sys
import os
from datetime import datetime, timedelta
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                            QTableWidget, QTableWidgetItem, QHeaderView, QLabel,
                            QLineEdit, QDialog, QFormLayout, QDialogButtonBox,
                            QMessageBox, QFrame, QSplitter, QGroupBox, QComboBox,
                            QDateTimeEdit, QTextEdit, QTabWidget)
from PyQt5.QtCore import Qt, pyqtSignal, QDateTime
from PyQt5.QtGui import QIcon, QPalette, QColor, QFont

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.database_models import Jadwal, PAKET_JENIS


class JadwalFormDialog(QDialog):
    """Dialog for adding/editing schedule information"""
    
    def __init__(self, jadwal_data=None, db_manager=None, parent=None):
        super().__init__(parent)
        self.jadwal_data = jadwal_data
        self.db_manager = db_manager
        self.is_edit_mode = jadwal_data is not None
        self.setup_ui()
        
        if self.is_edit_mode:
            self.populate_fields()
    
    def setup_ui(self):
        """Setup dialog user interface"""
        self.setWindowTitle("Edit Jadwal" if self.is_edit_mode else "Tambah Jadwal Sesi")
        self.setModal(True)
        self.setFixedSize(500, 550)
        
        # Apply dark theme
        self.setStyleSheet("""
            QDialog {
                background-color: #2D2D2D;
                color: #FFFFFF;
            }
            QLabel {
                color: #FFFFFF;
                font-size: 12px;
            }
            QLineEdit, QComboBox, QDateTimeEdit, QTextEdit {
                background-color: #404040;
                color: #FFFFFF;
                border: 2px solid #505050;
                border-radius: 6px;
                padding: 8px;
                font-size: 12px;
            }
            QLineEdit:focus, QComboBox:focus, QDateTimeEdit:focus, QTextEdit:focus {
                border-color: #4A90E2;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 15px;
                border-left: 1px solid #505050;
                border-top-right-radius: 3px;
                border-bottom-right-radius: 3px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid none;
                border-right: 5px solid none;
                border-top: 5px solid #FFFFFF;
            }
            QDateTimeEdit::up-button, QDateTimeEdit::down-button {
                width: 16px;
                border: none;
                background: #505050;
            }
            QDateTimeEdit::up-button:hover, QDateTimeEdit::down-button:hover {
                background: #4A90E2;
            }
            QPushButton {
                background-color: #4A90E2;
                color: #FFFFFF;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #357ABD;
            }
            QPushButton:pressed {
                background-color: #2E6DA4;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Form fields
        form_layout = QFormLayout()
        form_layout.setSpacing(12)
        
        # Client selection
        self.klien_combo = QComboBox()
        self.load_klien_options()
        form_layout.addRow("Klien:", self.klien_combo)
        
        # Photographer selection
        self.fotografer_combo = QComboBox()
        self.load_fotografer_options()
        form_layout.addRow("Fotografer:", self.fotografer_combo)
        
        # Studio selection
        self.studio_combo = QComboBox()
        self.load_studio_options()
        form_layout.addRow("Studio:", self.studio_combo)
        
        # Date and time
        self.datetime_edit = QDateTimeEdit()
        self.datetime_edit.setDateTime(QDateTime.currentDateTime().addDays(1))
        self.datetime_edit.setDisplayFormat("yyyy-MM-dd hh:mm")
        self.datetime_edit.setCalendarPopup(True)
        form_layout.addRow("Tanggal & Waktu:", self.datetime_edit)
        
        # Package type
        self.paket_combo = QComboBox()
        self.paket_combo.addItems(PAKET_JENIS)
        form_layout.addRow("Jenis Paket:", self.paket_combo)
        
        # Status
        self.status_combo = QComboBox()
        self.status_combo.addItems(["Booked", "Selesai", "Batal"])
        form_layout.addRow("Status:", self.status_combo)
        
        # Notes
        self.catatan_edit = QTextEdit()
        self.catatan_edit.setMaximumHeight(80)
        self.catatan_edit.setPlaceholderText("Catatan tambahan untuk sesi foto...")
        form_layout.addRow("Catatan:", self.catatan_edit)
        
        layout.addLayout(form_layout)
        
        # Conflict warning label
        self.conflict_label = QLabel()
        self.conflict_label.setStyleSheet("""
            color: #F44336;
            font-weight: bold;
            background-color: #452B2B;
            border: 1px solid #F44336;
            border-radius: 4px;
            padding: 8px;
        """)
        self.conflict_label.hide()
        layout.addWidget(self.conflict_label)
        
        # Dialog buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.Save | QDialogButtonBox.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        
        # Connect signals for conflict checking
        self.datetime_edit.dateTimeChanged.connect(self.check_conflicts)
        self.fotografer_combo.currentIndexChanged.connect(self.check_conflicts)
        self.studio_combo.currentIndexChanged.connect(self.check_conflicts)
    
    def load_klien_options(self):
        """Load client options into combo box"""
        try:
            klien_list = self.db_manager.get_all_klien()
            self.klien_combo.clear()
            self.klien_combo.addItem("-- Pilih Klien --", None)
            for klien in klien_list:
                display_text = f"{klien['nama']} ({klien['nomor_hp']})"
                self.klien_combo.addItem(display_text, klien['id_klien'])
        except Exception as e:
            print(f"Error loading clients: {e}")
    
    def load_fotografer_options(self):
        """Load photographer options into combo box"""
        try:
            fotografer_list = self.db_manager.get_all_fotografer()
            self.fotografer_combo.clear()
            self.fotografer_combo.addItem("-- Pilih Fotografer --", None)
            for fotografer in fotografer_list:
                display_text = f"{fotografer['nama']} ({fotografer['spesialisasi']})"
                self.fotografer_combo.addItem(display_text, fotografer['id_fotografer'])
        except Exception as e:
            print(f"Error loading photographers: {e}")
    
    def load_studio_options(self):
        """Load studio options into combo box"""
        try:
            studio_list = self.db_manager.get_all_studio()
            self.studio_combo.clear()
            self.studio_combo.addItem("-- Pilih Studio --", None)
            for studio in studio_list:
                display_text = f"{studio['nama_studio']} - {studio['lokasi']} ({studio['kapasitas']} org)"
                self.studio_combo.addItem(display_text, studio['id_studio'])
        except Exception as e:
            print(f"Error loading studios: {e}")
    
    def check_conflicts(self):
        """Check for scheduling conflicts"""
        if not self.db_manager:
            return
            
        fotografer_id = self.fotografer_combo.currentData()
        studio_id = self.studio_combo.currentData()
        
        if fotografer_id and studio_id:
            selected_datetime = self.datetime_edit.dateTime().toPyDateTime()
            exclude_session = None
            if self.is_edit_mode and self.jadwal_data:
                exclude_session = self.jadwal_data.get('id_sesi')
            
            conflict_msg = self.db_manager.check_schedule_conflict(
                fotografer_id, studio_id, selected_datetime, exclude_session
            )
            
            if conflict_msg:
                self.conflict_label.setText(f"⚠️ KONFLIK: {conflict_msg}")
                self.conflict_label.show()
            else:
                self.conflict_label.hide()
    
    def populate_fields(self):
        """Populate form fields with existing data"""
        if self.jadwal_data:
            # Set client
            klien_id = self.jadwal_data.get('id_klien')
            for i in range(self.klien_combo.count()):
                if self.klien_combo.itemData(i) == klien_id:
                    self.klien_combo.setCurrentIndex(i)
                    break
            
            # Set photographer
            fotografer_id = self.jadwal_data.get('id_fotografer')
            for i in range(self.fotografer_combo.count()):
                if self.fotografer_combo.itemData(i) == fotografer_id:
                    self.fotografer_combo.setCurrentIndex(i)
                    break
            
            # Set studio
            studio_id = self.jadwal_data.get('id_studio')
            for i in range(self.studio_combo.count()):
                if self.studio_combo.itemData(i) == studio_id:
                    self.studio_combo.setCurrentIndex(i)
                    break
            
            # Set datetime
            tanggal_waktu_str = self.jadwal_data.get('tanggal_waktu')
            if tanggal_waktu_str:
                try:
                    if isinstance(tanggal_waktu_str, str):
                        dt = datetime.fromisoformat(tanggal_waktu_str.replace('Z', '+00:00'))
                    else:
                        dt = tanggal_waktu_str
                    self.datetime_edit.setDateTime(QDateTime.fromSecsSinceEpoch(int(dt.timestamp())))
                except:
                    pass
            
            # Set package
            jenis_paket = self.jadwal_data.get('jenis_paket', '')
            index = self.paket_combo.findText(jenis_paket)
            if index >= 0:
                self.paket_combo.setCurrentIndex(index)
            
            # Set status
            status = self.jadwal_data.get('status', 'Booked')
            index = self.status_combo.findText(status)
            if index >= 0:
                self.status_combo.setCurrentIndex(index)
            
            # Set notes
            self.catatan_edit.setPlainText(self.jadwal_data.get('catatan', ''))
    
    def get_jadwal_data(self):
        """Get schedule data from form"""
        return Jadwal(
            id_klien=self.klien_combo.currentData(),
            id_fotografer=self.fotografer_combo.currentData(),
            id_studio=self.studio_combo.currentData(),
            tanggal_waktu=self.datetime_edit.dateTime().toPyDateTime(),
            jenis_paket=self.paket_combo.currentText(),
            status=self.status_combo.currentText(),
            catatan=self.catatan_edit.toPlainText().strip()
        )
    
    def validate_input(self):
        """Validate form input"""
        if not self.klien_combo.currentData():
            QMessageBox.warning(self, "Validasi", "Klien harus dipilih!")
            return False
        
        if not self.fotografer_combo.currentData():
            QMessageBox.warning(self, "Validasi", "Fotografer harus dipilih!")
            return False
        
        if not self.studio_combo.currentData():
            QMessageBox.warning(self, "Validasi", "Studio harus dipilih!")
            return False
        
        if self.datetime_edit.dateTime() <= QDateTime.currentDateTime():
            QMessageBox.warning(self, "Validasi", "Tanggal dan waktu harus di masa depan!")
            return False
        
        if not self.paket_combo.currentText():
            QMessageBox.warning(self, "Validasi", "Jenis paket harus dipilih!")
            return False
        
        # Check for conflicts one more time
        if self.conflict_label.isVisible():
            reply = QMessageBox.question(
                self, "Konflik Jadwal",
                "Terdapat konflik jadwal. Apakah Anda yakin ingin melanjutkan?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if reply == QMessageBox.No:
                return False
        
        return True
    
    def accept(self):
        """Handle dialog acceptance"""
        if self.validate_input():
            super().accept()


class JadwalTable(QTableWidget):
    """Custom table widget for displaying schedules"""
    
    edit_requested = pyqtSignal(dict)
    delete_requested = pyqtSignal(int)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        """Setup table interface"""
        self.setColumnCount(9)
        self.setHorizontalHeaderLabels([
            "ID", "Tanggal/Waktu", "Klien", "Fotografer", "Studio", 
            "Paket", "Status", "Catatan", "Aksi"
        ])
        
        # Hide ID column
        self.setColumnHidden(0, True)
        
        # Style the table
        self.setStyleSheet("""
            QTableWidget {
                background-color: #404040;
                alternate-background-color: #454545;
                gridline-color: #505050;
                border: 1px solid #505050;
                border-radius: 8px;
                color: white;
                selection-background-color: #4A90E2;
            }
            QHeaderView::section {
                background-color: #4A90E2;
                color: white;
                padding: 10px;
                border: none;
                font-weight: bold;
                font-size: 12px;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #505050;
            }
            QTableWidget::item:selected {
                background-color: #4A90E2;
            }
            QPushButton {
                background-color: #4A90E2;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 4px 8px;
                margin: 1px;
                font-size: 10px;
            }
            QPushButton:hover {
                background-color: #357ABD;
            }
        """)
        
        # Configure table
        self.setAlternatingRowColors(True)
        self.setSelectionBehavior(QTableWidget.SelectRows)
        self.setSelectionMode(QTableWidget.SingleSelection)
        
        # Auto-resize columns
        header = self.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)  # DateTime
        header.setSectionResizeMode(2, QHeaderView.Stretch)  # Client
        header.setSectionResizeMode(3, QHeaderView.Stretch)  # Photographer
        header.setSectionResizeMode(4, QHeaderView.Stretch)  # Studio
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)  # Package
        header.setSectionResizeMode(6, QHeaderView.ResizeToContents)  # Status
        header.setSectionResizeMode(7, QHeaderView.Stretch)  # Notes
        header.setSectionResizeMode(8, QHeaderView.Fixed)  # Actions
        self.setColumnWidth(8, 100)
        
        # Hide vertical header
        self.verticalHeader().setVisible(False)
    
    def update_data(self, jadwal_list):
        """Update table with schedule data"""
        self.setRowCount(len(jadwal_list))
        
        for row, jadwal in enumerate(jadwal_list):
            # ID (hidden)
            self.setItem(row, 0, QTableWidgetItem(str(jadwal.get('id_sesi', ''))))
            
            # Format datetime
            tanggal_waktu = jadwal.get('tanggal_waktu', '')
            if tanggal_waktu:
                try:
                    if isinstance(tanggal_waktu, str):
                        dt = datetime.fromisoformat(tanggal_waktu.replace('Z', '+00:00'))
                    else:
                        dt = tanggal_waktu
                    formatted_dt = dt.strftime('%d/%m/%Y %H:%M')
                except:
                    formatted_dt = str(tanggal_waktu)
            else:
                formatted_dt = ''
            
            self.setItem(row, 1, QTableWidgetItem(formatted_dt))
            self.setItem(row, 2, QTableWidgetItem(jadwal.get('nama_klien', '')))
            self.setItem(row, 3, QTableWidgetItem(jadwal.get('nama_fotografer', '')))
            
            # Studio with location
            studio_info = f"{jadwal.get('nama_studio', '')} - {jadwal.get('lokasi', '')}"
            self.setItem(row, 4, QTableWidgetItem(studio_info))
            
            self.setItem(row, 5, QTableWidgetItem(jadwal.get('jenis_paket', '')))
            
            # Status with color coding
            status = jadwal.get('status', '')
            status_item = QTableWidgetItem(status)
            if status == 'Booked':
                status_item.setBackground(QColor('#4CAF50'))  # Green
            elif status == 'Selesai':
                status_item.setBackground(QColor('#2196F3'))  # Blue
            elif status == 'Batal':
                status_item.setBackground(QColor('#F44336'))  # Red
            status_item.setTextAlignment(Qt.AlignCenter)
            self.setItem(row, 6, status_item)
            
            # Notes (truncated)
            catatan = jadwal.get('catatan', '')
            if len(catatan) > 50:
                catatan = catatan[:50] + '...'
            self.setItem(row, 7, QTableWidgetItem(catatan))
            
            # Action buttons
            self.setup_action_buttons(row, jadwal)
    
    def setup_action_buttons(self, row, jadwal_data):
        """Setup action buttons for each row"""
        button_frame = QFrame()
        button_layout = QHBoxLayout(button_frame)
        button_layout.setContentsMargins(2, 2, 2, 2)
        button_layout.setSpacing(2)
        
        # Edit button
        edit_btn = QPushButton("Edit")
        edit_btn.clicked.connect(
            lambda: self.edit_requested.emit(jadwal_data)
        )
        button_layout.addWidget(edit_btn)
        
        # Delete button
        delete_btn = QPushButton("Hapus")
        delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #F44336;
            }
            QPushButton:hover {
                background-color: #D32F2F;
            }
        """)
        delete_btn.clicked.connect(
            lambda: self.delete_requested.emit(jadwal_data.get('id_sesi'))
        )
        button_layout.addWidget(delete_btn)
        
        self.setCellWidget(row, 8, button_frame)


class JadwalWidget(QWidget):
    """Main schedule management widget"""
    
    def __init__(self, db_manager, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.setup_ui()
        self.load_data()
    
    def setup_ui(self):
        """Setup widget user interface"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Header section
        header_layout = QHBoxLayout()
        
        title_label = QLabel("Manajemen Jadwal Sesi")
        title_label.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #FFFFFF;
        """)
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        layout.addLayout(header_layout)
        
        # Tab widget for different views
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #505050;
                background-color: #404040;
            }
            QTabBar::tab {
                background-color: #2D2D2D;
                color: #FFFFFF;
                padding: 10px 20px;
                border: 1px solid #505050;
                border-bottom: none;
            }
            QTabBar::tab:selected {
                background-color: #4A90E2;
            }
            QTabBar::tab:hover {
                background-color: #357ABD;
            }
        """)
        
        # All schedules tab
        all_tab = QWidget()
        all_layout = QVBoxLayout(all_tab)
        
        # Control panel for all schedules
        self.setup_control_panel(all_layout)
        
        # Table for all schedules
        self.setup_table(all_layout)
        
        self.tab_widget.addTab(all_tab, "Semua Jadwal")
        
        # Upcoming schedules tab
        upcoming_tab = QWidget()
        upcoming_layout = QVBoxLayout(upcoming_tab)
        
        upcoming_label = QLabel("Jadwal Mendatang (24 jam ke depan)")
        upcoming_label.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #FFFFFF;
            margin: 10px 0;
        """)
        upcoming_layout.addWidget(upcoming_label)
        
        self.upcoming_table = JadwalTable()
        upcoming_layout.addWidget(self.upcoming_table, 1)
        
        self.tab_widget.addTab(upcoming_tab, "Jadwal Mendatang")
        
        layout.addWidget(self.tab_widget)
    
    def setup_control_panel(self, parent_layout):
        """Setup control panel with search and buttons"""
        panel_frame = QFrame()
        panel_frame.setStyleSheet("""
            QFrame {
                background-color: #404040;
                border-radius: 10px;
                padding: 10px;
            }
        """)
        
        panel_layout = QHBoxLayout(panel_frame)
        panel_layout.setContentsMargins(15, 15, 15, 15)
        panel_layout.setSpacing(15)
        
        # Search section
        search_label = QLabel("Cari:")
        search_label.setStyleSheet("color: #FFFFFF; font-weight: bold;")
        panel_layout.addWidget(search_label)
        
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Cari berdasarkan klien, fotografer, atau studio...")
        self.search_edit.setStyleSheet("""
            QLineEdit {
                background-color: #505050;
                color: #FFFFFF;
                border: 2px solid #606060;
                border-radius: 6px;
                padding: 8px;
                font-size: 12px;
            }
            QLineEdit:focus {
                border-color: #4A90E2;
            }
        """)
        self.search_edit.textChanged.connect(self.on_search)
        panel_layout.addWidget(self.search_edit, 1)
        
        # Status filter
        self.status_filter = QComboBox()
        self.status_filter.addItems(["Semua Status", "Booked", "Selesai", "Batal"])
        self.status_filter.setStyleSheet("""
            QComboBox {
                background-color: #505050;
                color: #FFFFFF;
                border: 2px solid #606060;
                border-radius: 6px;
                padding: 8px;
                font-size: 12px;
                min-width: 120px;
            }
            QComboBox:focus {
                border-color: #4A90E2;
            }
        """)
        self.status_filter.currentTextChanged.connect(self.on_filter_change)
        panel_layout.addWidget(self.status_filter)
        
        # Action buttons
        self.add_btn = QPushButton("➕ Buat Jadwal")
        self.add_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45A049;
            }
        """)
        self.add_btn.clicked.connect(self.add_jadwal)
        panel_layout.addWidget(self.add_btn)
        
        self.refresh_btn = QPushButton("🔄 Refresh")
        self.refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #4A90E2;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #357ABD;
            }
        """)
        self.refresh_btn.clicked.connect(self.load_data)
        panel_layout.addWidget(self.refresh_btn)
        
        parent_layout.addWidget(panel_frame)
    
    def setup_table(self, parent_layout):
        """Setup schedule table"""
        self.table = JadwalTable()
        self.table.edit_requested.connect(self.edit_jadwal)
        self.table.delete_requested.connect(self.delete_jadwal)
        parent_layout.addWidget(self.table, 1)
    
    def load_data(self):
        """Load schedule data from database"""
        try:
            # Load all schedules
            jadwal_list = self.db_manager.get_all_jadwal_with_details()
            self.table.update_data(jadwal_list)
            
            # Load upcoming schedules
            upcoming_list = self.db_manager.get_upcoming_sessions(24)  # 24 hours
            self.upcoming_table.update_data(upcoming_list)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal memuat data jadwal: {str(e)}")
    
    def on_search(self, text):
        """Handle search functionality"""
        self.apply_filters()
    
    def on_filter_change(self):
        """Handle filter change"""
        self.apply_filters()
    
    def apply_filters(self):
        """Apply search and filter criteria"""
        try:
            search_text = self.search_edit.text().strip().lower()
            status_filter = self.status_filter.currentText()
            
            all_jadwal = self.db_manager.get_all_jadwal_with_details()
            filtered = []
            
            for jadwal in all_jadwal:
                # Apply status filter
                if status_filter != "Semua Status" and jadwal.get('status') != status_filter:
                    continue
                
                # Apply text search
                if search_text:
                    searchable_text = (
                        jadwal.get('nama_klien', '').lower() + ' ' +
                        jadwal.get('nama_fotografer', '').lower() + ' ' +
                        jadwal.get('nama_studio', '').lower() + ' ' +
                        jadwal.get('lokasi', '').lower() + ' ' +
                        jadwal.get('jenis_paket', '').lower()
                    )
                    if search_text not in searchable_text:
                        continue
                
                filtered.append(jadwal)
            
            self.table.update_data(filtered)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal memfilter data: {str(e)}")
    
    def add_jadwal(self):
        """Add new schedule"""
        # Check if we have the required data
        klien_count = len(self.db_manager.get_all_klien())
        fotografer_count = len(self.db_manager.get_all_fotografer())
        studio_count = len(self.db_manager.get_all_studio())
        
        if klien_count == 0:
            QMessageBox.warning(
                self, "Data Belum Lengkap",
                "Belum ada data klien. Tambahkan klien terlebih dahulu."
            )
            return
        
        if fotografer_count == 0:
            QMessageBox.warning(
                self, "Data Belum Lengkap",
                "Belum ada data fotografer. Tambahkan fotografer terlebih dahulu."
            )
            return
        
        if studio_count == 0:
            QMessageBox.warning(
                self, "Data Belum Lengkap",
                "Belum ada data studio. Tambahkan studio terlebih dahulu."
            )
            return
        
        dialog = JadwalFormDialog(db_manager=self.db_manager, parent=self)
        if dialog.exec_() == QDialog.Accepted:
            try:
                jadwal = dialog.get_jadwal_data()
                success, message = self.db_manager.create_jadwal(jadwal)
                
                if success:
                    QMessageBox.information(
                        self, "Sukses", 
                        "Jadwal sesi berhasil dibuat!"
                    )
                    self.load_data()
                else:
                    QMessageBox.warning(self, "Gagal", message)
                    
            except Exception as e:
                QMessageBox.critical(
                    self, "Error", 
                    f"Gagal membuat jadwal: {str(e)}"
                )
    
    def edit_jadwal(self, jadwal_data):
        """Edit existing schedule"""
        dialog = JadwalFormDialog(jadwal_data, self.db_manager, parent=self)
        if dialog.exec_() == QDialog.Accepted:
            try:
                updated_jadwal = dialog.get_jadwal_data()
                success, message = self.db_manager.update_jadwal(
                    jadwal_data['id_sesi'], updated_jadwal
                )
                
                if success:
                    QMessageBox.information(
                        self, "Sukses", 
                        "Jadwal sesi berhasil diperbarui!"
                    )
                    self.load_data()
                else:
                    QMessageBox.warning(self, "Gagal", message)
                    
            except Exception as e:
                QMessageBox.critical(
                    self, "Error", 
                    f"Gagal memperbarui jadwal: {str(e)}"
                )
    
    def delete_jadwal(self, jadwal_id):
        """Delete schedule"""
        try:
            # Confirm deletion
            reply = QMessageBox.question(
                self, "Konfirmasi Hapus",
                "Apakah Anda yakin ingin menghapus jadwal sesi ini?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                success = self.db_manager.delete_jadwal(jadwal_id)
                
                if success:
                    QMessageBox.information(
                        self, "Sukses", 
                        "Jadwal sesi berhasil dihapus!"
                    )
                    self.load_data()
                else:
                    QMessageBox.warning(
                        self, "Peringatan", 
                        "Gagal menghapus jadwal sesi."
                    )
                    
        except Exception as e:
            QMessageBox.critical(
                self, "Error", 
                f"Gagal menghapus jadwal: {str(e)}"
            )
