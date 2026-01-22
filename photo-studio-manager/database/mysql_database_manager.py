"""
MySQL Database Manager for Photo Studio Management System
Handles MySQL database operations and CRUD functionality for Laragon
"""

import mysql.connector
from mysql.connector import Error
import os
import sys
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple
from contextlib import contextmanager

# Add parent directory to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from config.database import DATABASE_CONFIG
from models.database_models import Klien, Fotografer, Studio, Jadwal

class MySQLDatabaseManager:
    """Manages all MySQL database operations for the photo studio system"""
    
    def __init__(self):
        """Initialize MySQL database manager"""
        self.config = DATABASE_CONFIG
        self.init_database()
    
    @contextmanager
    def get_connection(self):
        """Context manager for MySQL database connections"""
        connection = None
        try:
            connection = mysql.connector.connect(**self.config)
            yield connection
        except Error as e:
            if connection:
                connection.rollback()
            raise e
        finally:
            if connection and connection.is_connected():
                connection.close()
    
    def init_database(self):
        """Initialize MySQL database and create tables"""
        try:
            with self.get_connection() as connection:
                cursor = connection.cursor()
                
                # Create tables with MySQL syntax
                self.create_klien_table(cursor)
                self.create_fotografer_table(cursor)
                self.create_studio_table(cursor)
                self.create_jadwal_table(cursor)
                
                # Create indexes for better performance
                self.create_indexes(cursor)
                
                connection.commit()
                print(f"MySQL database initialized successfully!")
                print(f"Database: {self.config['database']} on {self.config['host']}:{self.config['port']}")
                
        except Error as e:
            print(f"Error initializing MySQL database: {e}")
            raise e
    
    def create_klien_table(self, cursor):
        """Create clients table"""
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS klien (
                id_klien INT AUTO_INCREMENT PRIMARY KEY,
                nama VARCHAR(255) NOT NULL,
                nomor_hp VARCHAR(20) NOT NULL,
                email VARCHAR(255),
                alamat TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                INDEX idx_nama (nama),
                INDEX idx_nomor_hp (nomor_hp)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
    
    def create_fotografer_table(self, cursor):
        """Create photographers table"""
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS fotografer (
                id_fotografer INT AUTO_INCREMENT PRIMARY KEY,
                nama VARCHAR(255) NOT NULL,
                spesialisasi VARCHAR(100) NOT NULL,
                nomor_hp VARCHAR(20) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                INDEX idx_nama (nama),
                INDEX idx_spesialisasi (spesialisasi)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
    
    def create_studio_table(self, cursor):
        """Create studios table"""
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS studio (
                id_studio INT AUTO_INCREMENT PRIMARY KEY,
                nama_studio VARCHAR(255) NOT NULL,
                lokasi VARCHAR(255) NOT NULL,
                kapasitas INT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                INDEX idx_nama_studio (nama_studio),
                INDEX idx_lokasi (lokasi)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
    
    def create_jadwal_table(self, cursor):
        """Create schedules table"""
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS jadwal (
                id_sesi INT AUTO_INCREMENT PRIMARY KEY,
                id_klien INT NOT NULL,
                id_fotografer INT NOT NULL,
                id_studio INT NOT NULL,
                tanggal_waktu DATETIME NOT NULL,
                jenis_paket VARCHAR(100) NOT NULL,
                status ENUM('Booked', 'Selesai', 'Batal') NOT NULL DEFAULT 'Booked',
                catatan TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (id_klien) REFERENCES klien(id_klien) ON DELETE CASCADE,
                FOREIGN KEY (id_fotografer) REFERENCES fotografer(id_fotografer) ON DELETE CASCADE,
                FOREIGN KEY (id_studio) REFERENCES studio(id_studio) ON DELETE CASCADE,
                INDEX idx_tanggal_waktu (tanggal_waktu),
                INDEX idx_status (status),
                INDEX idx_klien (id_klien),
                INDEX idx_fotografer (id_fotografer),
                INDEX idx_studio (id_studio)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
    
    def create_indexes(self, cursor):
        """Create additional indexes for performance"""
        indexes = [
            "CREATE INDEX IF NOT EXISTS idx_jadwal_date_status ON jadwal(tanggal_waktu, status)",
            "CREATE INDEX IF NOT EXISTS idx_jadwal_photographer_date ON jadwal(id_fotografer, tanggal_waktu)",
            "CREATE INDEX IF NOT EXISTS idx_jadwal_studio_date ON jadwal(id_studio, tanggal_waktu)"
        ]
        
        for index_sql in indexes:
            try:
                cursor.execute(index_sql)
            except Error:
                # Index might already exist, ignore error
                pass
    
    # KLIEN CRUD OPERATIONS
    def create_klien(self, klien: Klien) -> int:
        """Create a new client and return the ID"""
        with self.get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO klien (nama, nomor_hp, email, alamat)
                VALUES (%s, %s, %s, %s)
            """, (klien.nama, klien.nomor_hp, klien.email, klien.alamat))
            connection.commit()
            return cursor.lastrowid
    
    def get_all_klien(self) -> List[Dict[str, Any]]:
        """Get all clients"""
        with self.get_connection() as connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM klien ORDER BY nama")
            return cursor.fetchall()
    
    def get_klien_by_id(self, id_klien: int) -> Optional[Dict[str, Any]]:
        """Get client by ID"""
        with self.get_connection() as connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM klien WHERE id_klien = %s", (id_klien,))
            return cursor.fetchone()
    
    def update_klien(self, id_klien: int, klien: Klien) -> bool:
        """Update client information"""
        with self.get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("""
                UPDATE klien SET nama = %s, nomor_hp = %s, email = %s, 
                alamat = %s WHERE id_klien = %s
            """, (klien.nama, klien.nomor_hp, klien.email, klien.alamat, id_klien))
            connection.commit()
            return cursor.rowcount > 0
    
    def delete_klien(self, id_klien: int) -> bool:
        """Delete client (only if no scheduled sessions)"""
        with self.get_connection() as connection:
            cursor = connection.cursor()
            # Check if client has any scheduled sessions
            cursor.execute("SELECT COUNT(*) FROM jadwal WHERE id_klien = %s", (id_klien,))
            if cursor.fetchone()[0] > 0:
                return False  # Cannot delete client with existing schedules
            
            cursor.execute("DELETE FROM klien WHERE id_klien = %s", (id_klien,))
            connection.commit()
            return cursor.rowcount > 0
    
    def search_klien(self, search_term: str) -> List[Dict[str, Any]]:
        """Search clients by name or phone"""
        with self.get_connection() as connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT * FROM klien 
                WHERE nama LIKE %s OR nomor_hp LIKE %s
                ORDER BY nama
            """, (f"%{search_term}%", f"%{search_term}%"))
            return cursor.fetchall()
    
    # FOTOGRAFER CRUD OPERATIONS
    def create_fotografer(self, fotografer: Fotografer) -> int:
        """Create a new photographer and return the ID"""
        with self.get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO fotografer (nama, spesialisasi, nomor_hp)
                VALUES (%s, %s, %s)
            """, (fotografer.nama, fotografer.spesialisasi, fotografer.nomor_hp))
            connection.commit()
            return cursor.lastrowid
    
    def get_all_fotografer(self) -> List[Dict[str, Any]]:
        """Get all photographers"""
        with self.get_connection() as connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM fotografer ORDER BY nama")
            return cursor.fetchall()
    
    def update_fotografer(self, id_fotografer: int, fotografer: Fotografer) -> bool:
        """Update photographer information"""
        with self.get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("""
                UPDATE fotografer SET nama = %s, spesialisasi = %s, nomor_hp = %s
                WHERE id_fotografer = %s
            """, (fotografer.nama, fotografer.spesialisasi, fotografer.nomor_hp, id_fotografer))
            connection.commit()
            return cursor.rowcount > 0
    
    def delete_fotografer(self, id_fotografer: int) -> bool:
        """Delete photographer (only if no scheduled sessions)"""
        with self.get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM jadwal WHERE id_fotografer = %s", (id_fotografer,))
            if cursor.fetchone()[0] > 0:
                return False
            
            cursor.execute("DELETE FROM fotografer WHERE id_fotografer = %s", (id_fotografer,))
            connection.commit()
            return cursor.rowcount > 0
    
    # STUDIO CRUD OPERATIONS
    def create_studio(self, studio: Studio) -> int:
        """Create a new studio and return the ID"""
        with self.get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO studio (nama_studio, lokasi, kapasitas)
                VALUES (%s, %s, %s)
            """, (studio.nama_studio, studio.lokasi, studio.kapasitas))
            connection.commit()
            return cursor.lastrowid
    
    def get_all_studio(self) -> List[Dict[str, Any]]:
        """Get all studios"""
        with self.get_connection() as connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM studio ORDER BY nama_studio")
            return cursor.fetchall()
    
    def update_studio(self, id_studio: int, studio: Studio) -> bool:
        """Update studio information"""
        with self.get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("""
                UPDATE studio SET nama_studio = %s, lokasi = %s, kapasitas = %s
                WHERE id_studio = %s
            """, (studio.nama_studio, studio.lokasi, studio.kapasitas, id_studio))
            connection.commit()
            return cursor.rowcount > 0
    
    def delete_studio(self, id_studio: int) -> bool:
        """Delete studio (only if no scheduled sessions)"""
        with self.get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM jadwal WHERE id_studio = %s", (id_studio,))
            if cursor.fetchone()[0] > 0:
                return False
            
            cursor.execute("DELETE FROM studio WHERE id_studio = %s", (id_studio,))
            connection.commit()
            return cursor.rowcount > 0
    
    # JADWAL CRUD OPERATIONS
    def create_jadwal(self, jadwal: Jadwal) -> Tuple[bool, str]:
        """Create a new schedule with conflict checking"""
        # Check for conflicts
        conflict_msg = self.check_schedule_conflict(
            jadwal.id_fotografer, jadwal.id_studio, 
            jadwal.tanggal_waktu, jadwal.id_sesi
        )
        
        if conflict_msg:
            return False, conflict_msg
        
        with self.get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO jadwal (id_klien, id_fotografer, id_studio, 
                tanggal_waktu, jenis_paket, status, catatan)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (jadwal.id_klien, jadwal.id_fotografer, jadwal.id_studio,
                  jadwal.tanggal_waktu, jadwal.jenis_paket, jadwal.status, jadwal.catatan))
            connection.commit()
            return True, "Schedule created successfully"
    
    def check_schedule_conflict(self, id_fotografer: int, id_studio: int, 
                              tanggal_waktu: datetime, exclude_session: int = None) -> str:
        """Check for scheduling conflicts"""
        with self.get_connection() as connection:
            cursor = connection.cursor()
            
            # Check photographer availability (2-hour buffer)
            time_start = tanggal_waktu - timedelta(hours=1)
            time_end = tanggal_waktu + timedelta(hours=1)
            
            query = """
                SELECT COUNT(*) FROM jadwal 
                WHERE id_fotografer = %s AND status = 'Booked'
                AND tanggal_waktu BETWEEN %s AND %s
            """
            params = [id_fotografer, time_start, time_end]
            
            if exclude_session:
                query += " AND id_sesi != %s"
                params.append(exclude_session)
            
            cursor.execute(query, params)
            if cursor.fetchone()[0] > 0:
                return "Fotografer sudah memiliki jadwal pada waktu tersebut"
            
            # Check studio availability
            query = """
                SELECT COUNT(*) FROM jadwal 
                WHERE id_studio = %s AND status = 'Booked'
                AND tanggal_waktu BETWEEN %s AND %s
            """
            params = [id_studio, time_start, time_end]
            
            if exclude_session:
                query += " AND id_sesi != %s"
                params.append(exclude_session)
            
            cursor.execute(query, params)
            if cursor.fetchone()[0] > 0:
                return "Studio sudah digunakan pada waktu tersebut"
            
            return ""  # No conflict
    
    def get_all_jadwal_with_details(self) -> List[Dict[str, Any]]:
        """Get all schedules with client, photographer, and studio details"""
        with self.get_connection() as connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT j.*, k.nama as nama_klien, f.nama as nama_fotografer,
                       s.nama_studio, s.lokasi
                FROM jadwal j
                JOIN klien k ON j.id_klien = k.id_klien
                JOIN fotografer f ON j.id_fotografer = f.id_fotografer
                JOIN studio s ON j.id_studio = s.id_studio
                ORDER BY j.tanggal_waktu DESC
            """)
            return cursor.fetchall()
    
    def update_jadwal(self, id_sesi: int, jadwal: Jadwal) -> Tuple[bool, str]:
        """Update schedule with conflict checking"""
        conflict_msg = self.check_schedule_conflict(
            jadwal.id_fotografer, jadwal.id_studio, 
            jadwal.tanggal_waktu, id_sesi
        )
        
        if conflict_msg:
            return False, conflict_msg
        
        with self.get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("""
                UPDATE jadwal SET id_klien = %s, id_fotografer = %s, id_studio = %s,
                tanggal_waktu = %s, jenis_paket = %s, status = %s, catatan = %s
                WHERE id_sesi = %s
            """, (jadwal.id_klien, jadwal.id_fotografer, jadwal.id_studio,
                  jadwal.tanggal_waktu, jadwal.jenis_paket, jadwal.status,
                  jadwal.catatan, id_sesi))
            connection.commit()
            return cursor.rowcount > 0, "Schedule updated successfully"
    
    def delete_jadwal(self, id_sesi: int) -> bool:
        """Delete schedule"""
        with self.get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM jadwal WHERE id_sesi = %s", (id_sesi,))
            connection.commit()
            return cursor.rowcount > 0
    
    def get_upcoming_sessions(self, hours: int = 24) -> List[Dict[str, Any]]:
        """Get sessions starting within specified hours"""
        cutoff_time = datetime.now() + timedelta(hours=hours)
        with self.get_connection() as connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT j.*, k.nama as nama_klien, f.nama as nama_fotografer,
                       s.nama_studio, s.lokasi
                FROM jadwal j
                JOIN klien k ON j.id_klien = k.id_klien
                JOIN fotografer f ON j.id_fotografer = f.id_fotografer
                JOIN studio s ON j.id_studio = s.id_studio
                WHERE j.tanggal_waktu <= %s AND j.status = 'Booked'
                AND j.tanggal_waktu >= NOW()
                ORDER BY j.tanggal_waktu
            """, (cutoff_time,))
            return cursor.fetchall()
    
    # DASHBOARD AND REPORTING
    def get_dashboard_stats(self) -> Dict[str, int]:
        """Get dashboard statistics"""
        with self.get_connection() as connection:
            cursor = connection.cursor()
            
            stats = {}
            
            # Total clients
            cursor.execute("SELECT COUNT(*) FROM klien")
            stats['total_klien'] = cursor.fetchone()[0]
            
            # Total photographers
            cursor.execute("SELECT COUNT(*) FROM fotografer")
            stats['total_fotografer'] = cursor.fetchone()[0]
            
            # Total studios
            cursor.execute("SELECT COUNT(*) FROM studio")
            stats['total_studio'] = cursor.fetchone()[0]
            
            # Sessions by status
            cursor.execute("SELECT COUNT(*) FROM jadwal WHERE status = 'Booked'")
            stats['sesi_booked'] = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM jadwal WHERE status = 'Selesai'")
            stats['sesi_selesai'] = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM jadwal WHERE status = 'Batal'")
            stats['sesi_batal'] = cursor.fetchone()[0]
            
            # This month's sessions
            cursor.execute("""
                SELECT COUNT(*) FROM jadwal 
                WHERE YEAR(tanggal_waktu) = YEAR(NOW()) 
                AND MONTH(tanggal_waktu) = MONTH(NOW())
            """)
            stats['sesi_bulan_ini'] = cursor.fetchone()[0]
            
            return stats
    
    def get_monthly_report(self, year: int, month: int) -> List[Dict[str, Any]]:
        """Get monthly schedule report"""
        with self.get_connection() as connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT j.*, k.nama as nama_klien, f.nama as nama_fotografer,
                       s.nama_studio, s.lokasi
                FROM jadwal j
                JOIN klien k ON j.id_klien = k.id_klien
                JOIN fotografer f ON j.id_fotografer = f.id_fotografer
                JOIN studio s ON j.id_studio = s.id_studio
                WHERE YEAR(j.tanggal_waktu) = %s 
                AND MONTH(j.tanggal_waktu) = %s
                ORDER BY j.tanggal_waktu
            """, (year, month))
            return cursor.fetchall()