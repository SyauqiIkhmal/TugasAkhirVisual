#!/usr/bin/env python3
"""
Add sample data to the Photo Studio Management System database
This script populates the database with sample clients, photographers, studios, and schedules
"""

import sys
import os
from datetime import datetime, timedelta
import random

# Add current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from database.mysql_database_manager import MySQLDatabaseManager
from models.database_models import Klien, Fotografer, Studio, Jadwal

def add_sample_data():
    """Add comprehensive sample data to the database"""
    print("Adding sample data to Photo Studio Management System...")
    
    # Initialize MySQL database manager
    db_manager = MySQLDatabaseManager()
    
    # Sample clients
    print("\nAdding sample clients...")
    clients = [
        {"nama": "Ahmad Wijaya", "nomor_hp": "081234567890", "email": "ahmad.wijaya@email.com", "alamat": "Jl. Sudirman No. 123, Jakarta"},
        {"nama": "Siti Nurhaliza", "nomor_hp": "081234567891", "email": "siti.nurhaliza@email.com", "alamat": "Jl. Thamrin No. 456, Jakarta"},
        {"nama": "Budi Santoso", "nomor_hp": "081234567892", "email": "budi.santoso@email.com", "alamat": "Jl. Gatot Subroto No. 789, Jakarta"},
        {"nama": "Dewi Lestari", "nomor_hp": "081234567893", "email": "dewi.lestari@email.com", "alamat": "Jl. Kuningan No. 321, Jakarta"},
        {"nama": "Eko Prasetyo", "nomor_hp": "081234567894", "email": "eko.prasetyo@email.com", "alamat": "Jl. Kemang No. 654, Jakarta"},
        {"nama": "Fitri Handayani", "nomor_hp": "081234567895", "email": "fitri.handayani@email.com", "alamat": "Jl. Pondok Indah No. 987, Jakarta"},
        {"nama": "Gunawan Susanto", "nomor_hp": "081234567896", "email": "gunawan.susanto@email.com", "alamat": "Jl. Senayan No. 147, Jakarta"},
        {"nama": "Hani Puspita", "nomor_hp": "081234567897", "email": "hani.puspita@email.com", "alamat": "Jl. Menteng No. 258, Jakarta"},
    ]
    
    client_ids = []
    for client_data in clients:
        klien = Klien(**client_data)
        klien_id = db_manager.create_klien(klien)
        client_ids.append(klien_id)
        print(f"  Added client: {client_data['nama']}")
    
    # Sample photographers
    print("\nAdding sample photographers...")
    photographers = [
        {"nama": "Maya Photographer", "spesialisasi": "Wedding", "nomor_hp": "082134567890"},
        {"nama": "Reza Studio", "spesialisasi": "Portrait", "nomor_hp": "082134567891"},
        {"nama": "Linda Creative", "spesialisasi": "Fashion", "nomor_hp": "082134567892"},
        {"nama": "Anton Photography", "spesialisasi": "Corporate", "nomor_hp": "082134567893"},
        {"nama": "Sari Visual", "spesialisasi": "Family", "nomor_hp": "082134567894"},
        {"nama": "Denny Captures", "spesialisasi": "Event", "nomor_hp": "082134567895"},
        {"nama": "Rina Moments", "spesialisasi": "Prewedding", "nomor_hp": "082134567896"},
    ]
    
    photographer_ids = []
    for photographer_data in photographers:
        fotografer = Fotografer(**photographer_data)
        fotografer_id = db_manager.create_fotografer(fotografer)
        photographer_ids.append(fotografer_id)
        print(f"  Added photographer: {photographer_data['nama']} ({photographer_data['spesialisasi']})")
    
    # Sample studios
    print("\nAdding sample studios...")
    studios = [
        {"nama_studio": "Studio Utama", "lokasi": "Jakarta Pusat", "kapasitas": 20},
        {"nama_studio": "Studio Mini", "lokasi": "Jakarta Selatan", "kapasitas": 8},
        {"nama_studio": "Studio Premium", "lokasi": "Jakarta Barat", "kapasitas": 30},
        {"nama_studio": "Studio Outdoor", "lokasi": "Jakarta Timur", "kapasitas": 15},
        {"nama_studio": "Studio Classic", "lokasi": "Jakarta Utara", "kapasitas": 12},
        {"nama_studio": "Studio Modern", "lokasi": "Tangerang", "kapasitas": 25},
    ]
    
    studio_ids = []
    for studio_data in studios:
        studio = Studio(**studio_data)
        studio_id = db_manager.create_studio(studio)
        studio_ids.append(studio_id)
        print(f"  Added studio: {studio_data['nama_studio']} - {studio_data['lokasi']} ({studio_data['kapasitas']} capacity)")
    
    # Sample schedules
    print("\nAdding sample schedules...")
    package_types = ["Wedding", "Prewedding", "Portrait", "Family", "Corporate", "Product", "Event", "Fashion", "Graduation", "Birthday"]
    statuses = ["Booked", "Selesai", "Batal"]
    
    schedules = []
    
    # Create schedules for the past month (some completed, some cancelled)
    for i in range(15):
        days_ago = random.randint(1, 30)
        schedule_datetime = datetime.now() - timedelta(days=days_ago, hours=random.randint(8, 18))
        
        schedules.append({
            "id_klien": random.choice(client_ids),
            "id_fotografer": random.choice(photographer_ids),
            "id_studio": random.choice(studio_ids),
            "tanggal_waktu": schedule_datetime,
            "jenis_paket": random.choice(package_types),
            "status": random.choice(["Selesai", "Batal"]),
            "catatan": f"Sesi foto {random.choice(['indoor', 'outdoor', 'studio'])} dengan durasi {random.randint(2, 6)} jam"
        })
    
    # Create schedules for the future (all booked)
    for i in range(20):
        days_ahead = random.randint(1, 60)
        schedule_datetime = datetime.now() + timedelta(days=days_ahead, hours=random.randint(8, 18))
        
        schedules.append({
            "id_klien": random.choice(client_ids),
            "id_fotografer": random.choice(photographer_ids),
            "id_studio": random.choice(studio_ids),
            "tanggal_waktu": schedule_datetime,
            "jenis_paket": random.choice(package_types),
            "status": "Booked",
            "catatan": f"Booking untuk {random.choice(['pernikahan', 'ulang tahun', 'wisuda', 'family gathering', 'corporate event'])}"
        })
    
    # Add some schedules for tomorrow and next few days
    for i in range(5):
        days_ahead = random.randint(0, 3)
        schedule_datetime = datetime.now() + timedelta(days=days_ahead, hours=random.randint(9, 17))
        
        schedules.append({
            "id_klien": random.choice(client_ids),
            "id_fotografer": random.choice(photographer_ids),
            "id_studio": random.choice(studio_ids),
            "tanggal_waktu": schedule_datetime,
            "jenis_paket": random.choice(package_types),
            "status": "Booked",
            "catatan": "Sesi foto mendatang - pastikan semua peralatan siap"
        })
    
    # Add schedules to database
    for schedule_data in schedules:
        jadwal = Jadwal(**schedule_data)
        success, message = db_manager.create_jadwal(jadwal)
        if success:
            print(f"  Added schedule: {schedule_data['jenis_paket']} on {schedule_data['tanggal_waktu'].strftime('%d/%m/%Y %H:%M')} - {schedule_data['status']}")
        else:
            # Try with different time if conflict
            schedule_data['tanggal_waktu'] += timedelta(hours=2)
            jadwal = Jadwal(**schedule_data)
            success, message = db_manager.create_jadwal(jadwal)
            if success:
                print(f"  Added schedule (adjusted): {schedule_data['jenis_paket']} on {schedule_data['tanggal_waktu'].strftime('%d/%m/%Y %H:%M')} - {schedule_data['status']}")
    
    print(f"\n✅ Sample data added successfully!")
    print(f"   - {len(clients)} clients")
    print(f"   - {len(photographers)} photographers") 
    print(f"   - {len(studios)} studios")
    print(f"   - {len(schedules)} schedules")
    
    # Display some statistics
    stats = db_manager.get_dashboard_stats()
    print(f"\n📊 Current Database Statistics:")
    print(f"   - Total Clients: {stats.get('total_klien', 0)}")
    print(f"   - Total Photographers: {stats.get('total_fotografer', 0)}")
    print(f"   - Total Studios: {stats.get('total_studio', 0)}")
    print(f"   - Booked Sessions: {stats.get('sesi_booked', 0)}")
    print(f"   - Completed Sessions: {stats.get('sesi_selesai', 0)}")
    print(f"   - Cancelled Sessions: {stats.get('sesi_batal', 0)}")
    print(f"   - This Month's Sessions: {stats.get('sesi_bulan_ini', 0)}")
    
    print(f"\n🎉 You can now explore all features of the Photo Studio Management System!")
    print(f"   • View and manage clients, photographers, and studios")
    print(f"   • Create and manage photo session schedules with conflict detection")
    print(f"   • Generate comprehensive reports in PDF and Excel formats")
    print(f"   • Monitor upcoming sessions and business statistics")

if __name__ == "__main__":
    add_sample_data()