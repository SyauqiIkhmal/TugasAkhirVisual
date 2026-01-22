"""
Dashboard Widget for Photo Studio Management System
Displays summary statistics and recent activities
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QFrame, QGridLayout, QScrollArea, QTableWidget,
                            QTableWidgetItem, QHeaderView)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QPalette, QColor
from datetime import datetime


class StatCard(QFrame):
    """Modern statistics card widget"""
    
    def __init__(self, title, value, icon="📊", color="#4A90E2", parent=None):
        super().__init__(parent)
        self.setup_ui(title, value, icon, color)
    
    def setup_ui(self, title, value, icon, color):
        """Setup card user interface"""
        self.setFixedHeight(120)
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {color};
                border-radius: 12px;
                border: none;
                margin: 5px;
            }}
            QLabel {{
                background-color: transparent;
                border: none;
                color: white;
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(5)
        
        # Icon and title row
        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(0, 0, 0, 0)
        
        icon_label = QLabel(icon)
        icon_label.setStyleSheet("font-size: 24px;")
        top_layout.addWidget(icon_label)
        
        top_layout.addStretch()
        
        title_label = QLabel(title)
        title_label.setStyleSheet("""
            font-size: 12px;
            font-weight: 500;
            color: rgba(255, 255, 255, 0.9);
        """)
        title_label.setAlignment(Qt.AlignRight)
        top_layout.addWidget(title_label)
        
        layout.addLayout(top_layout)
        
        # Value
        self.value_label = QLabel(str(value))
        self.value_label.setStyleSheet("""
            font-size: 32px;
            font-weight: bold;
            color: white;
        """)
        self.value_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.value_label)
        
        layout.addStretch()
    
    def update_value(self, value):
        """Update the card value"""
        self.value_label.setText(str(value))


class RecentSessionsTable(QTableWidget):
    """Table showing recent sessions"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        """Setup table interface"""
        self.setColumnCount(5)
        self.setHorizontalHeaderLabels([
            "Tanggal", "Klien", "Fotografer", "Studio", "Status"
        ])
        
        # Style the table
        self.setStyleSheet("""
            QTableWidget {
                background-color: #404040;
                alternate-background-color: #454545;
                gridline-color: #505050;
                border: 1px solid #505050;
                border-radius: 8px;
                color: white;
            }
            QHeaderView::section {
                background-color: #4A90E2;
                color: white;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #505050;
            }
            QTableWidget::item:selected {
                background-color: #4A90E2;
            }
        """)
        
        # Configure table
        self.setAlternatingRowColors(True)
        self.setSelectionBehavior(QTableWidget.SelectRows)
        self.setSelectionMode(QTableWidget.SingleSelection)
        
        # Auto-resize columns
        header = self.horizontalHeader()
        header.setStretchLastSection(True)
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        
        # Hide vertical header
        self.verticalHeader().setVisible(False)
    
    def update_sessions(self, sessions):
        """Update table with session data"""
        self.setRowCount(len(sessions))
        
        for row, session in enumerate(sessions):
            # Format date
            try:
                date_obj = datetime.fromisoformat(session['tanggal_waktu'].replace('Z', '+00:00'))
                date_str = date_obj.strftime('%d/%m/%Y %H:%M')
            except:
                date_str = str(session.get('tanggal_waktu', ''))
            
            # Set table items
            self.setItem(row, 0, QTableWidgetItem(date_str))
            self.setItem(row, 1, QTableWidgetItem(session.get('nama_klien', '')))
            self.setItem(row, 2, QTableWidgetItem(session.get('nama_fotografer', '')))
            self.setItem(row, 3, QTableWidgetItem(session.get('nama_studio', '')))
            
            # Status with color
            status_item = QTableWidgetItem(session.get('status', ''))
            status = session.get('status', '')
            if status == 'Booked':
                status_item.setBackground(QColor('#4CAF50'))
            elif status == 'Selesai':
                status_item.setBackground(QColor('#2196F3'))
            elif status == 'Batal':
                status_item.setBackground(QColor('#F44336'))
            
            self.setItem(row, 4, status_item)


class DashboardWidget(QWidget):
    """Main dashboard widget"""
    
    def __init__(self, db_manager, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.setup_ui()
        self.refresh_stats()
        
        # Setup auto-refresh timer
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.refresh_stats)
        self.refresh_timer.start(60000)  # Refresh every minute
    
    def setup_ui(self):
        """Setup dashboard user interface"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Header
        header_layout = QHBoxLayout()
        
        title_label = QLabel("Dashboard")
        title_label.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #FFFFFF;
            margin-bottom: 10px;
        """)
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        # Current time label
        self.time_label = QLabel()
        self.time_label.setStyleSheet("""
            font-size: 14px;
            color: #CCCCCC;
        """)
        header_layout.addWidget(self.time_label)
        
        layout.addLayout(header_layout)
        
        # Statistics cards
        self.setup_stat_cards(layout)
        
        # Recent sessions section
        self.setup_recent_sessions(layout)
        
        # Update time
        self.update_time()
        time_timer = QTimer()
        time_timer.timeout.connect(self.update_time)
        time_timer.start(1000)  # Update every second
    
    def setup_stat_cards(self, parent_layout):
        """Setup statistics cards"""
        cards_frame = QFrame()
        cards_frame.setStyleSheet("background-color: transparent; border: none;")
        
        cards_layout = QGridLayout(cards_frame)
        cards_layout.setSpacing(10)
        cards_layout.setContentsMargins(0, 0, 0, 0)
        
        # Create cards
        self.cards = {
            'klien': StatCard("Total Klien", "0", "👥", "#4A90E2"),
            'fotografer': StatCard("Fotografer", "0", "📸", "#FF9800"),
            'studio': StatCard("Studio", "0", "🏢", "#9C27B0"),
            'booked': StatCard("Sesi Aktif", "0", "📅", "#4CAF50"),
            'selesai': StatCard("Selesai", "0", "✅", "#2196F3"),
            'batal': StatCard("Dibatal", "0", "❌", "#F44336"),
        }
        
        # Add cards to grid
        cards_layout.addWidget(self.cards['klien'], 0, 0)
        cards_layout.addWidget(self.cards['fotografer'], 0, 1)
        cards_layout.addWidget(self.cards['studio'], 0, 2)
        cards_layout.addWidget(self.cards['booked'], 1, 0)
        cards_layout.addWidget(self.cards['selesai'], 1, 1)
        cards_layout.addWidget(self.cards['batal'], 1, 2)
        
        parent_layout.addWidget(cards_frame)
    
    def setup_recent_sessions(self, parent_layout):
        """Setup recent sessions section"""
        # Section header
        section_header = QLabel("Jadwal Sesi Terbaru")
        section_header.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #FFFFFF;
            margin: 20px 0 10px 0;
        """)
        parent_layout.addWidget(section_header)
        
        # Recent sessions table
        self.recent_table = RecentSessionsTable()
        self.recent_table.setMaximumHeight(300)
        parent_layout.addWidget(self.recent_table)
    
    def update_time(self):
        """Update current time display"""
        current_time = datetime.now().strftime("%d %B %Y, %H:%M:%S")
        self.time_label.setText(current_time)
    
    def refresh_stats(self):
        """Refresh dashboard statistics"""
        try:
            # Get statistics from database
            stats = self.db_manager.get_dashboard_stats()
            
            # Update cards
            self.cards['klien'].update_value(stats.get('total_klien', 0))
            self.cards['fotografer'].update_value(stats.get('total_fotografer', 0))
            self.cards['studio'].update_value(stats.get('total_studio', 0))
            self.cards['booked'].update_value(stats.get('sesi_booked', 0))
            self.cards['selesai'].update_value(stats.get('sesi_selesai', 0))
            self.cards['batal'].update_value(stats.get('sesi_batal', 0))
            
            # Update recent sessions
            recent_sessions = self.db_manager.get_all_jadwal_with_details()[:10]  # Get last 10
            self.recent_table.update_sessions(recent_sessions)
            
        except Exception as e:
            print(f"Error refreshing dashboard: {e}")
            # Set default values on error
            for card in self.cards.values():
                card.update_value("0")
    
    def showEvent(self, event):
        """Handle widget show event"""
        super().showEvent(event)
        self.refresh_stats()
    
    def closeEvent(self, event):
        """Handle widget close event"""
        if hasattr(self, 'refresh_timer'):
            self.refresh_timer.stop()
        event.accept()