# Photo Studio Management System

A comprehensive photo studio management system built with Python, PyQt5, and SQLite. This application provides a modern, user-friendly interface for managing clients, photographers, studios, and photo session schedules.

## Features

### ✅ Implemented
- **Modern Dark Theme UI** with responsive sidebar navigation
- **Client Management** - Full CRUD operations with search functionality
- **Dashboard** - Real-time statistics and recent sessions overview
- **Database** - Automatic SQLite database creation with proper relationships
- **Modular Architecture** - Clean separation of models, views, and database layers

### 🚧 Ready for Implementation
- **Photographer Management** - Manage photographer profiles and specializations
- **Studio Management** - Studio locations, capacity, and availability tracking
- **Session Scheduling** - Advanced booking system with conflict prevention
- **Reporting System** - PDF and Excel export capabilities
- **Search & Notifications** - Quick search and upcoming session alerts

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Setup Instructions

1. **Clone or Download** the project to your local machine

2. **Navigate to the project directory**
   ```bash
   cd photo-studio-manager
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**
   ```bash
   python main.py
   ```

## Project Structure

```
photo-studio-manager/
├── models/
│   └── database_models.py      # Data models and table schemas
├── views/
│   ├── main_window.py         # Main application window
│   ├── dashboard_widget.py    # Dashboard with statistics
│   ├── klien_widget.py        # Client management interface
│   ├── fotografer_widget.py   # Photographer management (placeholder)
│   ├── studio_widget.py       # Studio management (placeholder)
│   ├── jadwal_widget.py       # Schedule management (placeholder)
│   └── laporan_widget.py      # Reporting module (placeholder)
├── database/
│   └── database_manager.py    # Database operations and CRUD
├── resources/
│   ├── icons/                 # Application icons
│   └── styles/                # Additional stylesheets
├── requirements.txt           # Python dependencies
├── main.py                   # Application entry point
└── README.md                 # This file
```

## Database Schema

The application uses SQLite with the following tables:

### Klien (Clients)
- `id_klien` (Primary Key)
- `nama` (Name)
- `nomor_hp` (Phone/WhatsApp)
- `email`
- `alamat` (Address)
- `created_at`, `updated_at`

### Fotografer (Photographers)
- `id_fotografer` (Primary Key)
- `nama` (Name)
- `spesialisasi` (Specialization)
- `nomor_hp` (Phone)
- `created_at`, `updated_at`

### Studio
- `id_studio` (Primary Key)
- `nama_studio` (Studio Name)
- `lokasi` (Location)
- `kapasitas` (Capacity)
- `created_at`, `updated_at`

### Jadwal (Schedule)
- `id_sesi` (Primary Key)
- `id_klien` (Foreign Key)
- `id_fotografer` (Foreign Key)
- `id_studio` (Foreign Key)
- `tanggal_waktu` (Date & Time)
- `jenis_paket` (Package Type)
- `status` (Booked/Selesai/Batal)
- `catatan` (Notes)
- `created_at`, `updated_at`

## Usage

### Dashboard
- View real-time statistics
- Monitor recent sessions
- Track business metrics

### Client Management
- Add new clients with contact information
- Edit existing client details
- Search clients by name or phone number
- Delete clients (with validation)

### Data Management
- Automatic database creation on first run
- Data validation and error handling
- Referential integrity protection

## Technical Details

### Architecture
- **MVC Pattern** - Separation of models, views, and controllers
- **Object-Oriented Design** - Clean, maintainable code structure
- **Context Managers** - Safe database connection handling
- **Signal-Slot Pattern** - Event-driven UI interactions

### Key Technologies
- **PyQt5** - Modern cross-platform GUI framework
- **SQLite** - Lightweight, embedded database
- **Python 3.7+** - Modern Python features and type hints

### Performance Features
- **Database Indexing** - Optimized query performance
- **Connection Pooling** - Efficient database access
- **Lazy Loading** - On-demand data loading
- **Auto-refresh** - Real-time data updates

## Development Status

This is a foundational implementation with a fully functional client management system and modern UI framework. The architecture is designed to easily accommodate the remaining features:

- All database schemas are defined and ready
- UI framework supports all planned modules
- Core functionality patterns are established
- Placeholder widgets are ready for implementation

## Future Enhancements

- **Advanced Scheduling** - Calendar view and drag-and-drop booking
- **Photo Gallery** - Session photo management
- **Financial Tracking** - Payment and invoice management  
- **Multi-user Support** - User roles and permissions
- **Cloud Sync** - Backup and synchronization features
- **Mobile App** - Companion mobile application

## Contributing

This project follows clean code principles and modular design. When contributing:

1. Follow the existing code structure
2. Add proper error handling
3. Include appropriate docstrings
4. Test all functionality
5. Maintain the dark theme consistency

## License

This project is available for educational and commercial use. Feel free to modify and distribute according to your needs.

## Support

For questions or issues:
- Check the code comments for implementation details
- Review the database schema documentation
- Test with sample data to understand functionality

---

**Version**: 1.0.0
**Last Updated**: October 2025
**Status**: Foundation Complete - Ready for Feature Development