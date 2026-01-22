"""
Client Management Widget for Photo Studio Management System
Provides CRUD operations for client data with modern interface
"""

import sys
import os
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                            QTableWidget, QTableWidgetItem, QHeaderView, QLabel,
                            QLineEdit, QDialog, QFormLayout, QDialogButtonBox,
                            QMessageBox, QFrame, QSplitter, QGroupBox)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon, QPalette, QColor

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.database_models import Klien


class KlienFormDialog(QDialog):
    """Dialog for adding/editing client information"""
    
    def __init__(self, klien_data=None, parent=None):
        super().__init__(parent)
        self.klien_data = klien_data
        self.is_edit_mode = klien_data is not None
        self.setup_ui()
        
        if self.is_edit_mode:
            self.populate_fields()
    
    def setup_ui(self):
        """Setup dialog user interface"""
        self.setWindowTitle("Edit Klien" if self.is_edit_mode else "Tambah Klien")
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
            QLineEdit {
                background-color: #404040;
                color: #FFFFFF;
                border: 2px solid #505050;
                border-radius: 6px;
                padding: 8px;
                font-size: 12px;
            }
            QLineEdit:focus {
                border-color: #4A90E2;
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
        
        self.nama_edit = QLineEdit()
        self.nama_edit.setPlaceholderText("Masukkan nama lengkap klien")
        form_layout.addRow("Nama:", self.nama_edit)
        
        self.hp_edit = QLineEdit()
        self.hp_edit.setPlaceholderText("Contoh: 081234567890")
        form_layout.addRow("Nomor HP/WA:", self.hp_edit)
        
        self.email_edit = QLineEdit()
        self.email_edit.setPlaceholderText("email@example.com")
        form_layout.addRow("Email:", self.email_edit)
        
        self.alamat_edit = QLineEdit()
        self.alamat_edit.setPlaceholderText("Alamat lengkap klien")
        form_layout.addRow("Alamat:", self.alamat_edit)
        
        layout.addLayout(form_layout)
        
        # Dialog buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.Save | QDialogButtonBox.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        
        # Set focus to first field
        self.nama_edit.setFocus()
    
    def populate_fields(self):
        """Populate form fields with existing data"""
        if self.klien_data:
            self.nama_edit.setText(self.klien_data.get('nama', ''))
            self.hp_edit.setText(self.klien_data.get('nomor_hp', ''))
            self.email_edit.setText(self.klien_data.get('email', ''))
            self.alamat_edit.setText(self.klien_data.get('alamat', ''))
    
    def get_klien_data(self):
        """Get client data from form"""
        return Klien(
            nama=self.nama_edit.text().strip(),
            nomor_hp=self.hp_edit.text().strip(),
            email=self.email_edit.text().strip(),
            alamat=self.alamat_edit.text().strip()
        )
    
    def validate_input(self):
        """Validate form input"""
        if not self.nama_edit.text().strip():
            QMessageBox.warning(self, "Validasi", "Nama klien harus diisi!")
            return False
        
        if not self.hp_edit.text().strip():
            QMessageBox.warning(self, "Validasi", "Nomor HP/WA harus diisi!")
            return False
        
        return True
    
    def accept(self):
        """Handle dialog acceptance"""
        if self.validate_input():
            super().accept()


class KlienTable(QTableWidget):
    """Custom table widget for displaying clients"""
    
    edit_requested = pyqtSignal(dict)
    delete_requested = pyqtSignal(int)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        """Setup table interface"""
        self.setColumnCount(6)
        self.setHorizontalHeaderLabels([
            "ID", "Nama", "Nomor HP/WA", "Email", "Alamat", "Aksi"
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
        header.setSectionResizeMode(1, QHeaderView.Stretch)  # Name column
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)  # Phone
        header.setSectionResizeMode(3, QHeaderView.Stretch)  # Email
        header.setSectionResizeMode(4, QHeaderView.Stretch)  # Address
        header.setSectionResizeMode(5, QHeaderView.Fixed)  # Actions
        self.setColumnWidth(5, 120)
        
        # Hide vertical header
        self.verticalHeader().setVisible(False)
    
    def update_data(self, klien_list):
        """Update table with client data"""
        self.setRowCount(len(klien_list))
        
        for row, klien in enumerate(klien_list):
            # ID (hidden)
            self.setItem(row, 0, QTableWidgetItem(str(klien.get('id_klien', ''))))
            
            # Client info
            self.setItem(row, 1, QTableWidgetItem(klien.get('nama', '')))
            self.setItem(row, 2, QTableWidgetItem(klien.get('nomor_hp', '')))
            self.setItem(row, 3, QTableWidgetItem(klien.get('email', '')))
            self.setItem(row, 4, QTableWidgetItem(klien.get('alamat', '')))
            
            # Action buttons
            self.setup_action_buttons(row, klien)
    
    def setup_action_buttons(self, row, klien_data):
        """Setup action buttons for each row"""
        button_frame = QFrame()
        button_layout = QHBoxLayout(button_frame)
        button_layout.setContentsMargins(4, 4, 4, 4)
        button_layout.setSpacing(4)
        
        # Edit button
        edit_btn = QPushButton("Edit")
        edit_btn.clicked.connect(
            lambda: self.edit_requested.emit(klien_data)
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
            lambda: self.delete_requested.emit(klien_data.get('id_klien'))
        )
        button_layout.addWidget(delete_btn)
        
        self.setCellWidget(row, 5, button_frame)


class KlienWidget(QWidget):
    """Main client management widget"""
    
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
        
        title_label = QLabel("Manajemen Klien")
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
        self.search_edit.setPlaceholderText("Cari berdasarkan nama atau nomor HP...")
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
        self.add_btn = QPushButton("➕ Tambah Klien")
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
        self.add_btn.clicked.connect(self.add_klien)
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
        """Setup client table"""
        self.table = KlienTable()
        self.table.edit_requested.connect(self.edit_klien)
        self.table.delete_requested.connect(self.delete_klien)
        parent_layout.addWidget(self.table, 1)
    
    def load_data(self):
        """Load client data from database"""
        try:
            klien_list = self.db_manager.get_all_klien()
            self.table.update_data(klien_list)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal memuat data klien: {str(e)}")
    
    def on_search(self, text):
        """Handle search functionality"""
        try:
            if text.strip():
                results = self.db_manager.search_klien(text.strip())
                self.table.update_data(results)
            else:
                self.load_data()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal melakukan pencarian: {str(e)}")
    
    def add_klien(self):
        """Add new client"""
        dialog = KlienFormDialog(parent=self)
        if dialog.exec_() == QDialog.Accepted:
            try:
                klien = dialog.get_klien_data()
                klien_id = self.db_manager.create_klien(klien)
                
                QMessageBox.information(
                    self, "Sukses", 
                    f"Klien '{klien.nama}' berhasil ditambahkan!"
                )
                self.load_data()
                
            except Exception as e:
                QMessageBox.critical(
                    self, "Error", 
                    f"Gagal menambahkan klien: {str(e)}"
                )
    
    def edit_klien(self, klien_data):
        """Edit existing client"""
        dialog = KlienFormDialog(klien_data, parent=self)
        if dialog.exec_() == QDialog.Accepted:
            try:
                updated_klien = dialog.get_klien_data()
                success = self.db_manager.update_klien(
                    klien_data['id_klien'], updated_klien
                )
                
                if success:
                    QMessageBox.information(
                        self, "Sukses", 
                        f"Data klien '{updated_klien.nama}' berhasil diperbarui!"
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
                    f"Gagal memperbarui klien: {str(e)}"
                )
    
    def delete_klien(self, klien_id):
        """Delete client"""
        try:
            # Get client name for confirmation
            klien_data = self.db_manager.get_klien_by_id(klien_id)
            if not klien_data:
                QMessageBox.warning(self, "Error", "Klien tidak ditemukan!")
                return
            
            # Confirm deletion
            reply = QMessageBox.question(
                self, "Konfirmasi Hapus",
                f"Apakah Anda yakin ingin menghapus klien '{klien_data['nama']}'?\n\n"
                "PERINGATAN: Klien tidak dapat dihapus jika memiliki jadwal aktif.",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                success = self.db_manager.delete_klien(klien_id)
                
                if success:
                    QMessageBox.information(
                        self, "Sukses", 
                        f"Klien '{klien_data['nama']}' berhasil dihapus!"
                    )
                    self.load_data()
                else:
                    QMessageBox.warning(
                        self, "Peringatan", 
                        "Klien tidak dapat dihapus karena memiliki jadwal sesi yang terdaftar. "
                        "Hapus atau batalkan jadwal terlebih dahulu."
                    )
                    
        except Exception as e:
            QMessageBox.critical(
                self, "Error", 
                f"Gagal menghapus klien: {str(e)}"
            )