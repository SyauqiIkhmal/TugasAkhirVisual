"""
Photographer Management Widget for Photo Studio Management System
Provides CRUD operations for photographer data with modern interface
"""

import sys
import os
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                            QTableWidget, QTableWidgetItem, QHeaderView, QLabel,
                            QLineEdit, QDialog, QFormLayout, QDialogButtonBox,
                            QMessageBox, QFrame, QSplitter, QGroupBox, QComboBox)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon, QPalette, QColor

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.database_models import Fotografer


class FotograferFormDialog(QDialog):
    """Dialog for adding/editing photographer information"""
    
    SPECIALIZATIONS = [
        "Wedding", "Portrait", "Fashion", "Product", "Event", 
        "Corporate", "Family", "Nature", "Street", "Fine Art"
    ]
    
    def __init__(self, fotografer_data=None, parent=None):
        super().__init__(parent)
        self.fotografer_data = fotografer_data
        self.is_edit_mode = fotografer_data is not None
        self.setup_ui()
        
        if self.is_edit_mode:
            self.populate_fields()
    
    def setup_ui(self):
        """Setup dialog user interface"""
        self.setWindowTitle("Edit Fotografer" if self.is_edit_mode else "Tambah Fotografer")
        self.setModal(True)
        self.setFixedSize(400, 280)
        
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
            QLineEdit, QComboBox {
                background-color: #404040;
                color: #FFFFFF;
                border: 2px solid #505050;
                border-radius: 6px;
                padding: 8px;
                font-size: 12px;
            }
            QLineEdit:focus, QComboBox:focus {
                border-color: #4A90E2;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 15px;
                border-left-width: 1px;
                border-left-color: #505050;
                border-left-style: solid;
                border-top-right-radius: 3px;
                border-bottom-right-radius: 3px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid none;
                border-right: 5px solid none;
                border-top: 5px solid #FFFFFF;
                width: 0;
                height: 0;
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
        self.nama_edit.setPlaceholderText("Masukkan nama fotografer")
        form_layout.addRow("Nama:", self.nama_edit)
        
        self.spesialisasi_combo = QComboBox()
        self.spesialisasi_combo.addItems(self.SPECIALIZATIONS)
        self.spesialisasi_combo.setEditable(True)
        form_layout.addRow("Spesialisasi:", self.spesialisasi_combo)
        
        self.hp_edit = QLineEdit()
        self.hp_edit.setPlaceholderText("Contoh: 081234567890")
        form_layout.addRow("Nomor HP:", self.hp_edit)
        
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
        if self.fotografer_data:
            self.nama_edit.setText(self.fotografer_data.get('nama', ''))
            spesialisasi = self.fotografer_data.get('spesialisasi', '')
            index = self.spesialisasi_combo.findText(spesialisasi)
            if index >= 0:
                self.spesialisasi_combo.setCurrentIndex(index)
            else:
                self.spesialisasi_combo.setCurrentText(spesialisasi)
            self.hp_edit.setText(self.fotografer_data.get('nomor_hp', ''))
    
    def get_fotografer_data(self):
        """Get photographer data from form"""
        return Fotografer(
            nama=self.nama_edit.text().strip(),
            spesialisasi=self.spesialisasi_combo.currentText().strip(),
            nomor_hp=self.hp_edit.text().strip()
        )
    
    def validate_input(self):
        """Validate form input"""
        if not self.nama_edit.text().strip():
            QMessageBox.warning(self, "Validasi", "Nama fotografer harus diisi!")
            return False
        
        if not self.spesialisasi_combo.currentText().strip():
            QMessageBox.warning(self, "Validasi", "Spesialisasi harus diisi!")
            return False
        
        if not self.hp_edit.text().strip():
            QMessageBox.warning(self, "Validasi", "Nomor HP harus diisi!")
            return False
        
        return True
    
    def accept(self):
        """Handle dialog acceptance"""
        if self.validate_input():
            super().accept()


class FotograferTable(QTableWidget):
    """Custom table widget for displaying photographers"""
    
    edit_requested = pyqtSignal(dict)
    delete_requested = pyqtSignal(int)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        """Setup table interface"""
        self.setColumnCount(5)
        self.setHorizontalHeaderLabels([
            "ID", "Nama", "Spesialisasi", "Nomor HP", "Aksi"
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
        header.setSectionResizeMode(2, QHeaderView.Stretch)  # Specialization
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # Phone
        header.setSectionResizeMode(4, QHeaderView.Fixed)  # Actions
        self.setColumnWidth(4, 120)
        
        # Hide vertical header
        self.verticalHeader().setVisible(False)
    
    def update_data(self, fotografer_list):
        """Update table with photographer data"""
        self.setRowCount(len(fotografer_list))
        
        for row, fotografer in enumerate(fotografer_list):
            # ID (hidden)
            self.setItem(row, 0, QTableWidgetItem(str(fotografer.get('id_fotografer', ''))))
            
            # Photographer info
            self.setItem(row, 1, QTableWidgetItem(fotografer.get('nama', '')))
            self.setItem(row, 2, QTableWidgetItem(fotografer.get('spesialisasi', '')))
            self.setItem(row, 3, QTableWidgetItem(fotografer.get('nomor_hp', '')))
            
            # Action buttons
            self.setup_action_buttons(row, fotografer)
    
    def setup_action_buttons(self, row, fotografer_data):
        """Setup action buttons for each row"""
        button_frame = QFrame()
        button_layout = QHBoxLayout(button_frame)
        button_layout.setContentsMargins(4, 4, 4, 4)
        button_layout.setSpacing(4)
        
        # Edit button
        edit_btn = QPushButton("Edit")
        edit_btn.clicked.connect(
            lambda: self.edit_requested.emit(fotografer_data)
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
            lambda: self.delete_requested.emit(fotografer_data.get('id_fotografer'))
        )
        button_layout.addWidget(delete_btn)
        
        self.setCellWidget(row, 4, button_frame)


class FotograferWidget(QWidget):
    """Main photographer management widget"""
    
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
        
        title_label = QLabel("Manajemen Fotografer")
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
        self.search_edit.setPlaceholderText("Cari berdasarkan nama atau spesialisasi...")
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
        self.add_btn = QPushButton("➕ Tambah Fotografer")
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
        self.add_btn.clicked.connect(self.add_fotografer)
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
        """Setup photographer table"""
        self.table = FotograferTable()
        self.table.edit_requested.connect(self.edit_fotografer)
        self.table.delete_requested.connect(self.delete_fotografer)
        parent_layout.addWidget(self.table, 1)
    
    def load_data(self):
        """Load photographer data from database"""
        try:
            fotografer_list = self.db_manager.get_all_fotografer()
            self.table.update_data(fotografer_list)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal memuat data fotografer: {str(e)}")
    
    def on_search(self, text):
        """Handle search functionality"""
        try:
            if text.strip():
                # Simple search implementation - filter by name or specialization
                all_fotografer = self.db_manager.get_all_fotografer()
                filtered = [f for f in all_fotografer 
                           if text.lower() in f.get('nama', '').lower() or 
                              text.lower() in f.get('spesialisasi', '').lower()]
                self.table.update_data(filtered)
            else:
                self.load_data()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal melakukan pencarian: {str(e)}")
    
    def add_fotografer(self):
        """Add new photographer"""
        dialog = FotograferFormDialog(parent=self)
        if dialog.exec_() == QDialog.Accepted:
            try:
                fotografer = dialog.get_fotografer_data()
                fotografer_id = self.db_manager.create_fotografer(fotografer)
                
                QMessageBox.information(
                    self, "Sukses", 
                    f"Fotografer '{fotografer.nama}' berhasil ditambahkan!"
                )
                self.load_data()
                
            except Exception as e:
                QMessageBox.critical(
                    self, "Error", 
                    f"Gagal menambahkan fotografer: {str(e)}"
                )
    
    def edit_fotografer(self, fotografer_data):
        """Edit existing photographer"""
        dialog = FotograferFormDialog(fotografer_data, parent=self)
        if dialog.exec_() == QDialog.Accepted:
            try:
                updated_fotografer = dialog.get_fotografer_data()
                success = self.db_manager.update_fotografer(
                    fotografer_data['id_fotografer'], updated_fotografer
                )
                
                if success:
                    QMessageBox.information(
                        self, "Sukses", 
                        f"Data fotografer '{updated_fotografer.nama}' berhasil diperbarui!"
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
                    f"Gagal memperbarui fotografer: {str(e)}"
                )
    
    def delete_fotografer(self, fotografer_id):
        """Delete photographer"""
        try:
            # Get photographer name for confirmation
            fotografer_data = None
            all_fotografer = self.db_manager.get_all_fotografer()
            for f in all_fotografer:
                if f.get('id_fotografer') == fotografer_id:
                    fotografer_data = f
                    break
            
            if not fotografer_data:
                QMessageBox.warning(self, "Error", "Fotografer tidak ditemukan!")
                return
            
            # Confirm deletion
            reply = QMessageBox.question(
                self, "Konfirmasi Hapus",
                f"Apakah Anda yakin ingin menghapus fotografer '{fotografer_data['nama']}'?\n\n"
                "PERINGATAN: Fotografer tidak dapat dihapus jika memiliki jadwal aktif.",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                success = self.db_manager.delete_fotografer(fotografer_id)
                
                if success:
                    QMessageBox.information(
                        self, "Sukses", 
                        f"Fotografer '{fotografer_data['nama']}' berhasil dihapus!"
                    )
                    self.load_data()
                else:
                    QMessageBox.warning(
                        self, "Peringatan", 
                        "Fotografer tidak dapat dihapus karena memiliki jadwal sesi yang terdaftar. "
                        "Hapus atau batalkan jadwal terlebih dahulu."
                    )
                    
        except Exception as e:
            QMessageBox.critical(
                self, "Error", 
                f"Gagal menghapus fotografer: {str(e)}"
            )
