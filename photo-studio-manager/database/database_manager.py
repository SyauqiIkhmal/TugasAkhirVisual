"""
Database Manager for Photo Studio Management System
Handles SQLite database operations and CRUD functionality
"""

import sqlite3
import os
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple
from contextlib import contextmanager

from models.database_models import Klien, Fotografer, Studio, Jadwal

class DatabaseManager:
    """Manages all database operations for the photo studio system"""
    
    def __init__(self, db_path: str = "photo_studio.db"):
        """Initialize database manager with database path"""
        self.db_path = db_path
        self.init_database()
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row  # Enable column access by name
            yield conn
        except sqlite3.Error as e:
            if conn:
                conn.rollback()
            raise e
        finally:
            if conn:
                conn.close()
    
    def init_database(self):
        """Initialize database and create tables"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Create tables
                cursor.execute(Klien.get_table_schema())
                cursor.execute(Fotografer.get_table_schema())
                cursor.execute(Studio.get_table_schema())
                cursor.execute(Jadwal.get_table_schema())
                
                # Create indexes for better performance
                cursor.execute("""
                    CREATE INDEX IF NOT EXISTS idx_jadwal_tanggal 
                    ON jadwal(tanggal_waktu)
                """)
                cursor.execute("""
                    CREATE INDEX IF NOT EXISTS idx_jadwal_klien 
                    ON jadwal(id_klien)
                """)
                cursor.execute("""
                    CREATE INDEX IF NOT EXISTS idx_jadwal_fotografer 
                    ON jadwal(id_fotografer)
                """)
                cursor.execute("""
                    CREATE INDEX IF NOT EXISTS idx_jadwal_studio 
                    ON jadwal(id_studio)
                """)
                
                conn.commit()
                print(f"Database initialized at: {os.path.abspath(self.db_path)}")
                
        except sqlite3.Error as e:
            print(f"Error initializing database: {e}")
            raise e
    
    # KLIEN CRUD OPERATIONS
    def create_klien(self, klien: Klien) -> int:
        """Create a new client and return the ID"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO klien (nama, nomor_hp, email, alamat)
                VALUES (?, ?, ?, ?)
            """, (klien.nama, klien.nomor_hp, klien.email, klien.alamat))
            conn.commit()
            return cursor.lastrowid
    
    def get_all_klien(self) -> List[Dict[str, Any]]:
        """Get all clients"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM klien ORDER BY nama")
            return [dict(row) for row in cursor.fetchall()]
    
    def get_klien_by_id(self, id_klien: int) -> Optional[Dict[str, Any]]:
        """Get client by ID"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM klien WHERE id_klien = ?", (id_klien,))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def update_klien(self, id_klien: int, klien: Klien) -> bool:
        """Update client information"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE klien SET nama = ?, nomor_hp = ?, email = ?, 
                alamat = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id_klien = ?
            """, (klien.nama, klien.nomor_hp, klien.email, klien.alamat, id_klien))
            conn.commit()
            return cursor.rowcount > 0
    
    def delete_klien(self, id_klien: int) -> bool:
        """Delete client (only if no scheduled sessions)"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            # Check if client has any scheduled sessions
            cursor.execute("SELECT COUNT(*) FROM jadwal WHERE id_klien = ?", (id_klien,))
            if cursor.fetchone()[0] > 0:
                return False  # Cannot delete client with existing schedules
            
            cursor.execute("DELETE FROM klien WHERE id_klien = ?", (id_klien,))
            conn.commit()
            return cursor.rowcount > 0
    
    def search_klien(self, search_term: str) -> List[Dict[str, Any]]:
        """Search clients by name or phone"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM klien 
                WHERE nama LIKE ? OR nomor_hp LIKE ?
                ORDER BY nama
            """, (f"%{search_term}%", f"%{search_term}%"))
            return [dict(row) for row in cursor.fetchall()]
    
    # FOTOGRAFER CRUD OPERATIONS
    def create_fotografer(self, fotografer: Fotografer) -> int:
        """Create a new photographer and return the ID"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO fotografer (nama, spesialisasi, nomor_hp)
                VALUES (?, ?, ?)
            """, (fotografer.nama, fotografer.spesialisasi, fotografer.nomor_hp))
            conn.commit()
            return cursor.lastrowid
    
    def get_all_fotografer(self) -> List[Dict[str, Any]]:
        """Get all photographers"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM fotografer ORDER BY nama")
            return [dict(row) for row in cursor.fetchall()]
    
    def update_fotografer(self, id_fotografer: int, fotografer: Fotografer) -> bool:
        """Update photographer information"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE fotografer SET nama = ?, spesialisasi = ?, nomor_hp = ?,
                updated_at = CURRENT_TIMESTAMP
                WHERE id_fotografer = ?
            """, (fotografer.nama, fotografer.spesialisasi, fotografer.nomor_hp, id_fotografer))
            conn.commit()
            return cursor.rowcount > 0
    
    def delete_fotografer(self, id_fotografer: int) -> bool:
        """Delete photographer (only if no scheduled sessions)"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM jadwal WHERE id_fotografer = ?", (id_fotografer,))
            if cursor.fetchone()[0] > 0:
                return False
            
            cursor.execute("DELETE FROM fotografer WHERE id_fotografer = ?", (id_fotografer,))
            conn.commit()
            return cursor.rowcount > 0
    
    # STUDIO CRUD OPERATIONS
    def create_studio(self, studio: Studio) -> int:
        """Create a new studio and return the ID"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO studio (nama_studio, lokasi, kapasitas)
                VALUES (?, ?, ?)
            """, (studio.nama_studio, studio.lokasi, studio.kapasitas))
            conn.commit()
            return cursor.lastrowid
    
    def get_all_studio(self) -> List[Dict[str, Any]]:
        """Get all studios"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM studio ORDER BY nama_studio")
            return [dict(row) for row in cursor.fetchall()]
    
    def update_studio(self, id_studio: int, studio: Studio) -> bool:
        """Update studio information"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE studio SET nama_studio = ?, lokasi = ?, kapasitas = ?,
                updated_at = CURRENT_TIMESTAMP
                WHERE id_studio = ?
            """, (studio.nama_studio, studio.lokasi, studio.kapasitas, id_studio))
            conn.commit()
            return cursor.rowcount > 0
    
    def delete_studio(self, id_studio: int) -> bool:
        """Delete studio (only if no scheduled sessions)"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM jadwal WHERE id_studio = ?", (id_studio,))
            if cursor.fetchone()[0] > 0:
                return False
            
            cursor.execute("DELETE FROM studio WHERE id_studio = ?", (id_studio,))
            conn.commit()
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
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO jadwal (id_klien, id_fotografer, id_studio, 
                tanggal_waktu, jenis_paket, status, catatan)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (jadwal.id_klien, jadwal.id_fotografer, jadwal.id_studio,
                  jadwal.tanggal_waktu, jadwal.jenis_paket, jadwal.status, jadwal.catatan))
            conn.commit()
            return True, "Schedule created successfully"
    
    def check_schedule_conflict(self, id_fotografer: int, id_studio: int, 
                              tanggal_waktu: datetime, exclude_session: int = None) -> str:
        """Check for scheduling conflicts"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Check photographer availability (2-hour buffer)
            time_start = tanggal_waktu - timedelta(hours=1)
            time_end = tanggal_waktu + timedelta(hours=1)
            
            query = """
                SELECT COUNT(*) FROM jadwal 
                WHERE id_fotografer = ? AND status = 'Booked'
                AND tanggal_waktu BETWEEN ? AND ?
            """
            params = [id_fotografer, time_start, time_end]
            
            if exclude_session:
                query += " AND id_sesi != ?"
                params.append(exclude_session)
            
            cursor.execute(query, params)
            if cursor.fetchone()[0] > 0:
                return "Fotografer sudah memiliki jadwal pada waktu tersebut"
            
            # Check studio availability
            query = """
                SELECT COUNT(*) FROM jadwal 
                WHERE id_studio = ? AND status = 'Booked'
                AND tanggal_waktu BETWEEN ? AND ?
            """
            params = [id_studio, time_start, time_end]
            
            if exclude_session:
                query += " AND id_sesi != ?"
                params.append(exclude_session)
            
            cursor.execute(query, params)
            if cursor.fetchone()[0] > 0:
                return "Studio sudah digunakan pada waktu tersebut"
            
            return ""  # No conflict
    
    def get_all_jadwal_with_details(self) -> List[Dict[str, Any]]:
        """Get all schedules with client, photographer, and studio details"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT j.*, k.nama as nama_klien, f.nama as nama_fotografer,
                       s.nama_studio, s.lokasi
                FROM jadwal j
                JOIN klien k ON j.id_klien = k.id_klien
                JOIN fotografer f ON j.id_fotografer = f.id_fotografer
                JOIN studio s ON j.id_studio = s.id_studio
                ORDER BY j.tanggal_waktu DESC
            """)
            return [dict(row) for row in cursor.fetchall()]
    
    def update_jadwal(self, id_sesi: int, jadwal: Jadwal) -> Tuple[bool, str]:
        """Update schedule with conflict checking"""
        conflict_msg = self.check_schedule_conflict(
            jadwal.id_fotografer, jadwal.id_studio, 
            jadwal.tanggal_waktu, id_sesi
        )
        
        if conflict_msg:
            return False, conflict_msg
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE jadwal SET id_klien = ?, id_fotografer = ?, id_studio = ?,
                tanggal_waktu = ?, jenis_paket = ?, status = ?, catatan = ?,
                updated_at = CURRENT_TIMESTAMP
                WHERE id_sesi = ?
            """, (jadwal.id_klien, jadwal.id_fotografer, jadwal.id_studio,
                  jadwal.tanggal_waktu, jadwal.jenis_paket, jadwal.status,
                  jadwal.catatan, id_sesi))
            conn.commit()
            return cursor.rowcount > 0, "Schedule updated successfully"
    
    def delete_jadwal(self, id_sesi: int) -> bool:
        """Delete schedule"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM jadwal WHERE id_sesi = ?", (id_sesi,))
            conn.commit()
            return cursor.rowcount > 0
    
    def get_upcoming_sessions(self, hours: int = 1) -> List[Dict[str, Any]]:
        """Get sessions starting within specified hours"""
        cutoff_time = datetime.now() + timedelta(hours=hours)
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT j.*, k.nama as nama_klien, f.nama as nama_fotografer,
                       s.nama_studio, s.lokasi
                FROM jadwal j
                JOIN klien k ON j.id_klien = k.id_klien
                JOIN fotografer f ON j.id_fotografer = f.id_fotografer
                JOIN studio s ON j.id_studio = s.id_studio
                WHERE j.tanggal_waktu <= ? AND j.status = 'Booked'
                AND j.tanggal_waktu >= datetime('now')
                ORDER BY j.tanggal_waktu
            """, (cutoff_time,))
            return [dict(row) for row in cursor.fetchall()]
    
    # DASHBOARD AND REPORTING
    def get_dashboard_stats(self) -> Dict[str, int]:
        """Get dashboard statistics"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
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
                WHERE strftime('%Y-%m', tanggal_waktu) = strftime('%Y-%m', 'now')
            """)
            stats['sesi_bulan_ini'] = cursor.fetchone()[0]
            
            return stats
    
    def get_monthly_report(self, year: int, month: int) -> List[Dict[str, Any]]:
        """Get monthly schedule report"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT j.*, k.nama as nama_klien, f.nama as nama_fotografer,
                       s.nama_studio, s.lokasi
                FROM jadwal j
                JOIN klien k ON j.id_klien = k.id_klien
                JOIN fotografer f ON j.id_fotografer = f.id_fotografer
                JOIN studio s ON j.id_studio = s.id_studio
                WHERE strftime('%Y', j.tanggal_waktu) = ? 
                AND strftime('%m', j.tanggal_waktu) = ?
                ORDER BY j.tanggal_waktu
            """, (str(year), f"{month:02d}"))
            return [dict(row) for row in cursor.fetchall()]