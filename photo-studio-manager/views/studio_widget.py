"""
Studio Management Widget for Photo Studio Management System
Provides CRUD operations for studio data with modern interface
"""

import sys
import os
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                            QTableWidget, QTableWidgetItem, QHeaderView, QLabel,
                            QLineEdit, QDialog, QFormLayout, QDialogButtonBox,
                            QMessageBox, QFrame, QSplitter, QGroupBox, QSpinBox)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon, QPalette, QColor

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.database_models import Studio


class StudioFormDialog(QDialog):
    """Dialog for adding/editing studio information"""
    
    def __init__(self, studio_data=None, parent=None):
        super().__init__(parent)
        self.studio_data = studio_data
        self.is_edit_mode = studio_data is not None
        self.setup_ui()
        
        if self.is_edit_mode:
            self.populate_fields()
    
    def setup_ui(self):
        """Setup dialog user interface"""
        self.setWindowTitle("Edit Studio" if self.is_edit_mode else "Tambah Studio")
        self.setModal(True)
        self.setFixedSize(400, 300)
        
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
            QLineEdit, QSpinBox {
                background-color: #404040;
                color: #FFFFFF;
                border: 2px solid #505050;
                border-radius: 6px;
                padding: 8px;
                font-size: 12px;
            }
            QLineEdit:focus, QSpinBox:focus {
                border-color: #4A90E2;
            }
            QSpinBox::up-button, QSpinBox::down-button {
                subcontrol-origin: border;
                width: 16px;
                border: none;
                background: #505050;
            }
            QSpinBox::up-button:hover, QSpinBox::down-button:hover {
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
        
        self.nama_studio_edit = QLineEdit()
        self.nama_studio_edit.setPlaceholderText("Masukkan nama studio")
        form_layout.addRow("Nama Studio:", self.nama_studio_edit)
        
        self.lokasi_edit = QLineEdit()
        self.lokasi_edit.setPlaceholderText("Masukkan lokasi studio")
        form_layout.addRow("Lokasi:", self.lokasi_edit)
        
        self.kapasitas_spin = QSpinBox()
        self.kapasitas_spin.setRange(1, 100)
        self.kapasitas_spin.setSuffix(" orang")
        self.kapasitas_spin.setValue(10)
        form_layout.addRow("Kapasitas:", self.kapasitas_spin)
        
        layout.addLayout(form_layout)
        
        # Dialog buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.Save | QDialogButtonBox.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        
        # Set focus to first field
        self.nama_studio_edit.setFocus()
    
    def populate_fields(self):
        """Populate form fields with existing data"""
        if self.studio_data:
            self.nama_studio_edit.setText(self.studio_data.get('nama_studio', ''))
            self.lokasi_edit.setText(self.studio_data.get('lokasi', ''))
            self.kapasitas_spin.setValue(self.studio_data.get('kapasitas', 10))
    
    def get_studio_data(self):
        """Get studio data from form"""
        return Studio(
            nama_studio=self.nama_studio_edit.text().strip(),
            lokasi=self.lokasi_edit.text().strip(),
            kapasitas=self.kapasitas_spin.value()
        )
    
    def validate_input(self):
        """Validate form input"""
        if not self.nama_studio_edit.text().strip():
            QMessageBox.warning(self, "Validasi", "Nama studio harus diisi!")
            return False
        
        if not self.lokasi_edit.text().strip():
            QMessageBox.warning(self, "Validasi", "Lokasi studio harus diisi!")
            return False
        
        if self.kapasitas_spin.value() <= 0:
            QMessageBox.warning(self, "Validasi", "Kapasitas harus lebih dari 0!")
            return False
        
        return True
    
    def accept(self):
        """Handle dialog acceptance"""
        if self.validate_input():
            super().accept()


class StudioTable(QTableWidget):
    """Custom table widget for displaying studios"""
    
    edit_requested = pyqtSignal(dict)
    delete_requested = pyqtSignal(int)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        """Setup table interface"""
        self.setColumnCount(5)
        self.setHorizontalHeaderLabels([
            "ID", "Nama Studio", "Lokasi", "Kapasitas", "Aksi"
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
                padding: 12px 8px;
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
                padding: 6px 12px;
                margin: 2px;
                font-size: 11px;
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
        header.setSectionResizeMode(1, QHeaderView.Stretch)  # Studio name column
        header.setSectionResizeMode(2, QHeaderView.Stretch)  # Location
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # Capacity
        header.setSectionResizeMode(4, QHeaderView.Fixed)  # Actions
        self.setColumnWidth(4, 120)
        
        # Hide vertical header
        self.verticalHeader().setVisible(False)
    
    def update_data(self, studio_list):
        """Update table with studio data"""
        self.setRowCount(len(studio_list))
        
        for row, studio in enumerate(studio_list):
            # ID (hidden)
            self.setItem(row, 0, QTableWidgetItem(str(studio.get('id_studio', ''))))
            
            # Studio info
            self.setItem(row, 1, QTableWidgetItem(studio.get('nama_studio', '')))
            self.setItem(row, 2, QTableWidgetItem(studio.get('lokasi', '')))
            
            # Format capacity with unit
            kapasitas = studio.get('kapasitas', 0)
            capacity_text = f"{kapasitas} orang"
            capacity_item = QTableWidgetItem(capacity_text)
            capacity_item.setTextAlignment(Qt.AlignCenter)
            self.setItem(row, 3, capacity_item)
            
            # Action buttons
            self.setup_action_buttons(row, studio)
    
    def setup_action_buttons(self, row, studio_data):
        """Setup action buttons for each row"""
        button_frame = QFrame()
        button_layout = QHBoxLayout(button_frame)
        button_layout.setContentsMargins(4, 4, 4, 4)
        button_layout.setSpacing(4)
        
        # Edit button
        edit_btn = QPushButton("Edit")
        edit_btn.clicked.connect(
            lambda: self.edit_requested.emit(studio_data)
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
            lambda: self.delete_requested.emit(studio_data.get('id_studio'))
        )
        button_layout.addWidget(delete_btn)
        
        self.setCellWidget(row, 4, button_frame)


class StudioWidget(QWidget):
    """Main studio management widget"""
    
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
        
        title_label = QLabel("Manajemen Studio")
        title_label.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #FFFFFF;
        """)
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        layout.addLayout(header_layout)
        
        # Control panel
        self.setup_control_panel(layout)
        
        # Table
        self.setup_table(layout)
    
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
        self.search_edit.setPlaceholderText("Cari berdasarkan nama studio atau lokasi...")
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
        
        # Action buttons
        self.add_btn = QPushButton("➕ Tambah Studio")
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
        self.add_btn.clicked.connect(self.add_studio)
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
        """Setup studio table"""
        self.table = StudioTable()
        self.table.edit_requested.connect(self.edit_studio)
        self.table.delete_requested.connect(self.delete_studio)
        parent_layout.addWidget(self.table, 1)
    
    def load_data(self):
        """Load studio data from database"""
        try:
            studio_list = self.db_manager.get_all_studio()
            self.table.update_data(studio_list)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal memuat data studio: {str(e)}")
    
    def on_search(self, text):
        """Handle search functionality"""
        try:
            if text.strip():
                # Simple search implementation - filter by name or location
                all_studio = self.db_manager.get_all_studio()
                filtered = [s for s in all_studio 
                           if text.lower() in s.get('nama_studio', '').lower() or 
                              text.lower() in s.get('lokasi', '').lower()]
                self.table.update_data(filtered)
            else:
                self.load_data()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal melakukan pencarian: {str(e)}")
    
    def add_studio(self):
        """Add new studio"""
        dialog = StudioFormDialog(parent=self)
        if dialog.exec_() == QDialog.Accepted:
            try:
                studio = dialog.get_studio_data()
                studio_id = self.db_manager.create_studio(studio)
                
                QMessageBox.information(
                    self, "Sukses", 
                    f"Studio '{studio.nama_studio}' berhasil ditambahkan!"
                )
                self.load_data()
                
            except Exception as e:
                QMessageBox.critical(
                    self, "Error", 
                    f"Gagal menambahkan studio: {str(e)}"
                )
    
    def edit_studio(self, studio_data):
        """Edit existing studio"""
        dialog = StudioFormDialog(studio_data, parent=self)
        if dialog.exec_() == QDialog.Accepted:
            try:
                updated_studio = dialog.get_studio_data()
                success = self.db_manager.update_studio(
                    studio_data['id_studio'], updated_studio
                )
                
                if success:
                    QMessageBox.information(
                        self, "Sukses", 
                        f"Data studio '{updated_studio.nama_studio}' berhasil diperbarui!"
                    )
                    self.load_data()
                else:
                    QMessageBox.warning(
                        self, "Peringatan", 
                        "Tidak ada perubahan data yang disimpan."
                    )
                    
            except Exception as e:
                QMessageBox.critical(
                    self, "Error", 
                    f"Gagal memperbarui studio: {str(e)}"
                )
    
    def delete_studio(self, studio_id):
        """Delete studio"""
        try:
            # Get studio name for confirmation
            studio_data = None
            all_studio = self.db_manager.get_all_studio()
            for s in all_studio:
                if s.get('id_studio') == studio_id:
                    studio_data = s
                    break
            
            if not studio_data:
                QMessageBox.warning(self, "Error", "Studio tidak ditemukan!")
                return
            
            # Confirm deletion
            reply = QMessageBox.question(
                self, "Konfirmasi Hapus",
                f"Apakah Anda yakin ingin menghapus studio '{studio_data['nama_studio']}'?\n\n"
                "PERINGATAN: Studio tidak dapat dihapus jika memiliki jadwal aktif.",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                success = self.db_manager.delete_studio(studio_id)
                
                if success:
                    QMessageBox.information(
                        self, "Sukses", 
                        f"Studio '{studio_data['nama_studio']}' berhasil dihapus!"
                    )
                    self.load_data()
                else:
                    QMessageBox.warning(
                        self, "Peringatan", 
                        "Studio tidak dapat dihapus karena memiliki jadwal sesi yang terdaftar. "
                        "Hapus atau batalkan jadwal terlebih dahulu."
                    )
                    
        except Exception as e:
            QMessageBox.critical(
                self, "Error", 
                f"Gagal menghapus studio: {str(e)}"
            )
