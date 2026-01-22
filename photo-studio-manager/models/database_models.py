"""
Database models for Photo Studio Management System
Defines the structure and relationships between entities
"""

from datetime import datetime
from typing import Dict, Any, List, Optional

class BaseModel:
    """Base class for all database models"""
    
    def __init__(self):
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary"""
        return {key: value for key, value in self.__dict__.items() 
                if not key.startswith('_')}
    
    def from_dict(self, data: Dict[str, Any]):
        """Update model from dictionary"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)

class Klien(BaseModel):
    """Client model"""
    
    def __init__(self, id_klien: int = None, nama: str = "", 
                 nomor_hp: str = "", email: str = "", alamat: str = ""):
        super().__init__()
        self.id_klien = id_klien
        self.nama = nama
        self.nomor_hp = nomor_hp
        self.email = email
        self.alamat = alamat
    
    @staticmethod
    def get_table_schema() -> str:
        """Get SQL table creation schema"""
        return """
        CREATE TABLE IF NOT EXISTS klien (
            id_klien INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT NOT NULL,
            nomor_hp TEXT NOT NULL,
            email TEXT,
            alamat TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """

class Fotografer(BaseModel):
    """Photographer model"""
    
    def __init__(self, id_fotografer: int = None, nama: str = "", 
                 spesialisasi: str = "", nomor_hp: str = ""):
        super().__init__()
        self.id_fotografer = id_fotografer
        self.nama = nama
        self.spesialisasi = spesialisasi
        self.nomor_hp = nomor_hp
    
    @staticmethod
    def get_table_schema() -> str:
        """Get SQL table creation schema"""
        return """
        CREATE TABLE IF NOT EXISTS fotografer (
            id_fotografer INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT NOT NULL,
            spesialisasi TEXT NOT NULL,
            nomor_hp TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """

class Studio(BaseModel):
    """Studio model"""
    
    def __init__(self, id_studio: int = None, nama_studio: str = "", 
                 lokasi: str = "", kapasitas: int = 0):
        super().__init__()
        self.id_studio = id_studio
        self.nama_studio = nama_studio
        self.lokasi = lokasi
        self.kapasitas = kapasitas
    
    @staticmethod
    def get_table_schema() -> str:
        """Get SQL table creation schema"""
        return """
        CREATE TABLE IF NOT EXISTS studio (
            id_studio INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_studio TEXT NOT NULL,
            lokasi TEXT NOT NULL,
            kapasitas INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """

class Jadwal(BaseModel):
    """Schedule model"""
    
    STATUS_CHOICES = ["Booked", "Selesai", "Batal"]
    
    def __init__(self, id_sesi: int = None, id_klien: int = None, 
                 id_fotografer: int = None, id_studio: int = None,
                 tanggal_waktu: datetime = None, jenis_paket: str = "",
                 status: str = "Booked", catatan: str = ""):
        super().__init__()
        self.id_sesi = id_sesi
        self.id_klien = id_klien
        self.id_fotografer = id_fotografer
        self.id_studio = id_studio
        self.tanggal_waktu = tanggal_waktu or datetime.now()
        self.jenis_paket = jenis_paket
        self.status = status if status in self.STATUS_CHOICES else "Booked"
        self.catatan = catatan
    
    @staticmethod
    def get_table_schema() -> str:
        """Get SQL table creation schema"""
        return """
        CREATE TABLE IF NOT EXISTS jadwal (
            id_sesi INTEGER PRIMARY KEY AUTOINCREMENT,
            id_klien INTEGER NOT NULL,
            id_fotografer INTEGER NOT NULL,
            id_studio INTEGER NOT NULL,
            tanggal_waktu TIMESTAMP NOT NULL,
            jenis_paket TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Booked',
            catatan TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (id_klien) REFERENCES klien (id_klien),
            FOREIGN KEY (id_fotografer) REFERENCES fotografer (id_fotografer),
            FOREIGN KEY (id_studio) REFERENCES studio (id_studio),
            CHECK (status IN ('Booked', 'Selesai', 'Batal'))
        )
        """

# Package type options for the application
PAKET_JENIS = [
    "Wedding", "Prewedding", "Portrait", "Family", "Corporate", 
    "Product", "Event", "Fashion", "Graduation", "Birthday"
]