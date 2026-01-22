"""
Main Application Window for Photo Studio Management System
Modern PyQt5 interface with sidebar navigation and stacked widgets
"""

import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QPushButton, QStackedWidget, QLabel,
                            QFrame, QSizePolicy, QScrollArea)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QFont, QIcon, QPalette, QColor

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.mysql_database_manager import MySQLDatabaseManager
from views.dashboard_widget import DashboardWidget
from views.klien_widget import KlienWidget
from views.fotografer_widget import FotograferWidget
from views.studio_widget import StudioWidget
from views.jadwal_widget import JadwalWidget
from views.laporan_widget import LaporanWidget


class ModernButton(QPushButton):
    """Custom modern button with hover effects"""
    
    def __init__(self, text, icon_path=None, parent=None):
        super().__init__(text, parent)
        self.setMinimumHeight(50)
        self.setCursor(Qt.PointingHandCursor)
        self.is_active = False
        
        # Set button style
        self.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                color: #FFFFFF;
                text-align: left;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: 500;
                border-radius: 8px;
                margin: 2px 10px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.1);
            }
            QPushButton:pressed {
                background-color: rgba(255, 255, 255, 0.2);
            }
        """)
    
    def set_active(self, active=True):
        """Set button as active/inactive"""
        self.is_active = active
        if active:
            self.setStyleSheet(self.styleSheet() + """
                QPushButton {
                    background-color: rgba(74, 144, 226, 0.8);
                    color: #FFFFFF;
                }
            """)
        else:
            # Reset to default style
            self.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    border: none;
                    color: #FFFFFF;
                    text-align: left;
                    padding: 10px 20px;
                    font-size: 14px;
                    font-weight: 500;
                    border-radius: 8px;
                    margin: 2px 10px;
                }
                QPushButton:hover {
                    background-color: rgba(255, 255, 255, 0.1);
                }
                QPushButton:pressed {
                    background-color: rgba(255, 255, 255, 0.2);
                }
            """)


class SidebarWidget(QWidget):
    """Modern sidebar navigation widget"""
    
    page_changed = pyqtSignal(int)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_button = None
        self.setup_ui()
    
    def setup_ui(self):
        """Setup sidebar user interface"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Header section
        header_frame = QFrame()
        header_frame.setFixedHeight(80)
        header_frame.setStyleSheet("background-color: rgba(0, 0, 0, 0.1); border-radius: 0px;")
        
        header_layout = QVBoxLayout(header_frame)
        header_layout.setContentsMargins(20, 10, 20, 10)
        
        title_label = QLabel("Photo Studio\nManager")
        title_label.setStyleSheet("""
            color: #FFFFFF;
            font-size: 18px;
            font-weight: bold;
            line-height: 1.2;
        """)
        title_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(title_label)
        
        layout.addWidget(header_frame)
        
        # Navigation buttons
        self.nav_layout = QVBoxLayout()
        self.nav_layout.setContentsMargins(0, 20, 0, 0)
        self.nav_layout.setSpacing(5)
        
        # Menu items
        menu_items = [
            ("📊 Dashboard", 0),
            ("👥 Klien", 1),
            ("📸 Fotografer", 2),
            ("🏢 Studio", 3),
            ("📅 Jadwal", 4),
            ("📋 Laporan", 5),
        ]
        
        self.buttons = []
        for text, page_index in menu_items:
            button = ModernButton(text)
            button.clicked.connect(lambda checked, idx=page_index: self.change_page(idx))
            self.buttons.append(button)
            self.nav_layout.addWidget(button)
        
        # Set dashboard as active by default
        self.buttons[0].set_active(True)
        self.current_button = self.buttons[0]
        
        layout.addLayout(self.nav_layout)
        layout.addStretch()
        
        # Footer
        footer_label = QLabel("v1.0.0")
        footer_label.setStyleSheet("""
            color: rgba(255, 255, 255, 0.6);
            font-size: 12px;
            padding: 10px 20px;
        """)
        footer_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(footer_label)
    
    def change_page(self, page_index):
        """Change active page and button state"""
        # Reset previous button
        if self.current_button:
            self.current_button.set_active(False)
        
        # Set new active button
        self.current_button = self.buttons[page_index]
        self.current_button.set_active(True)
        
        # Emit signal to change page
        self.page_changed.emit(page_index)


class MainWindow(QMainWindow):
    """Main application window with modern interface"""
    
    def __init__(self):
        super().__init__()
        
        # Initialize MySQL database
        self.db_manager = MySQLDatabaseManager()
        
        # Setup window
        self.setup_window()
        self.setup_ui()
        self.setup_notifications()
        
        # Show maximized
        self.showMaximized()
    
    def setup_window(self):
        """Setup main window properties"""
        self.setWindowTitle("Photo Studio Management System")
        self.setMinimumSize(1200, 800)
        
        # Set application icon (if available)
        # self.setWindowIcon(QIcon("resources/icons/app_icon.png"))
        
        # Apply dark theme
        self.apply_dark_theme()
    
    def apply_dark_theme(self):
        """Apply modern dark theme to the application"""
        dark_palette = QPalette()
        
        # Window colors
        dark_palette.setColor(QPalette.Window, QColor(45, 45, 45))
        dark_palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
        
        # Base colors
        dark_palette.setColor(QPalette.Base, QColor(35, 35, 35))
        dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        
        # Text colors
        dark_palette.setColor(QPalette.Text, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
        
        # Button colors
        dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
        
        # Highlight colors
        dark_palette.setColor(QPalette.Highlight, QColor(74, 144, 226))
        dark_palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
        
        # Disabled colors
        dark_palette.setColor(QPalette.Disabled, QPalette.Text, QColor(127, 127, 127))
        dark_palette.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(127, 127, 127))
        
        self.setPalette(dark_palette)
        
        # Set global stylesheet
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2D2D2D;
            }
            QWidget {
                background-color: #2D2D2D;
                color: #FFFFFF;
            }
            QFrame {
                background-color: #2D2D2D;
                border: none;
            }
            QScrollArea {
                background-color: #2D2D2D;
                border: none;
            }
            QScrollBar:vertical {
                background-color: #404040;
                width: 12px;
                border: none;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background-color: #606060;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #707070;
            }
        """)
    
    def setup_ui(self):
        """Setup main user interface"""
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create main layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create sidebar
        self.sidebar = SidebarWidget()
        self.sidebar.setFixedWidth(250)
        self.sidebar.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 #4A90E2, stop:1 #357ABD);
        """)
        self.sidebar.page_changed.connect(self.change_page)
        main_layout.addWidget(self.sidebar)
        
        # Create content area
        content_frame = QFrame()
        content_frame.setStyleSheet("""
            background-color: #353535;
            border-left: 2px solid #404040;
        """)
        
        content_layout = QVBoxLayout(content_frame)
        content_layout.setContentsMargins(0, 0, 0, 0)
        
        # Create stacked widget for pages
        self.stacked_widget = QStackedWidget()
        content_layout.addWidget(self.stacked_widget)
        
        # Add pages
        self.setup_pages()
        
        main_layout.addWidget(content_frame, 1)
    
    def setup_pages(self):
        """Setup all application pages"""
        try:
            # Dashboard
            self.dashboard_widget = DashboardWidget(self.db_manager)
            self.stacked_widget.addWidget(self.dashboard_widget)
            
            # Klien management
            self.klien_widget = KlienWidget(self.db_manager)
            self.stacked_widget.addWidget(self.klien_widget)
            
            # Fotografer management
            self.fotografer_widget = FotograferWidget(self.db_manager)
            self.stacked_widget.addWidget(self.fotografer_widget)
            
            # Studio management
            self.studio_widget = StudioWidget(self.db_manager)
            self.stacked_widget.addWidget(self.studio_widget)
            
            # Jadwal management
            self.jadwal_widget = JadwalWidget(self.db_manager)
            self.stacked_widget.addWidget(self.jadwal_widget)
            
            # Laporan
            self.laporan_widget = LaporanWidget(self.db_manager)
            self.stacked_widget.addWidget(self.laporan_widget)
            
        except ImportError as e:
            # Create placeholder widgets if specific widgets aren't available yet
            for i in range(6):
                placeholder = QLabel(f"Page {i} - Under Development")
                placeholder.setAlignment(Qt.AlignCenter)
                placeholder.setStyleSheet("""
                    font-size: 24px;
                    color: #888888;
                    background-color: #353535;
                """)
                self.stacked_widget.addWidget(placeholder)
    
    def setup_notifications(self):
        """Setup notification system for upcoming sessions"""
        self.notification_timer = QTimer()
        self.notification_timer.timeout.connect(self.check_upcoming_sessions)
        self.notification_timer.start(300000)  # Check every 5 minutes
    
    def check_upcoming_sessions(self):
        """Check for upcoming sessions and show notifications"""
        try:
            upcoming_sessions = self.db_manager.get_upcoming_sessions(1)  # 1 hour ahead
            
            if upcoming_sessions:
                from PyQt5.QtWidgets import QMessageBox
                
                session_names = [
                    f"{session['nama_klien']} - {session['nama_fotografer']} - {session['nama_studio']}"
                    for session in upcoming_sessions
                ]
                
                QMessageBox.information(
                    self,
                    "Jadwal Mendatang",
                    f"Ada {len(upcoming_sessions)} sesi pemotretan dalam 1 jam ke depan:\n\n" +
                    "\n".join(session_names)
                )
        except Exception as e:
            print(f"Error checking upcoming sessions: {e}")
    
    def change_page(self, page_index):
        """Change the current page"""
        self.stacked_widget.setCurrentIndex(page_index)
        
        # Refresh dashboard if switching to it
        if page_index == 0 and hasattr(self, 'dashboard_widget'):
            try:
                self.dashboard_widget.refresh_stats()
            except:
                pass
    
    def closeEvent(self, event):
        """Handle application close event"""
        # Clean up resources
        if hasattr(self, 'notification_timer'):
            self.notification_timer.stop()
        
        event.accept()


def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    app.setApplicationName("Photo Studio Manager")
    app.setApplicationVersion("1.0.0")
    
    # Set application font
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()