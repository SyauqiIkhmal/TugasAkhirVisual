"""
Database configuration for Photo Studio Management System
Configure MySQL connection settings for Laragon
"""

import os

# MySQL Database Configuration for Laragon
DATABASE_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '',  # Default Laragon MySQL password is empty
    'database': 'photo_studio_db',
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_unicode_ci',
    'autocommit': True,
    'raise_on_warnings': False,
    'use_unicode': True
}

# Alternative configuration if you have different settings
# Uncomment and modify if needed:
"""
DATABASE_CONFIG = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root', 
    'password': 'your_password_here',
    'database': 'photo_studio_db',
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_unicode_ci',
    'autocommit': True,
    'raise_on_warnings': True,
    'use_unicode': True
}
"""

# Test connection function
def test_connection():
    """Test the database connection"""
    import mysql.connector
    from mysql.connector import Error
    
    try:
        # Test connection without specifying database first
        test_config = DATABASE_CONFIG.copy()
        database_name = test_config.pop('database')
        
        connection = mysql.connector.connect(**test_config)
        if connection.is_connected():
            print("✅ MySQL connection successful!")
            
            # Create database if it doesn't exist
            cursor = connection.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
            print(f"✅ Database '{database_name}' ready!")
            
            cursor.close()
            connection.close()
            return True
            
    except Error as e:
        print(f"❌ Error connecting to MySQL: {e}")
        return False

if __name__ == "__main__":
    test_connection()