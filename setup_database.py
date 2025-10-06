#!/usr/bin/env python3
"""
Database Management Script untuk Attendance System
- Setup database baru
- Upgrade database yang sudah ada
- Check dan repair database
"""

import mysql.connector
from mysql.connector import Error
from config.database import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME
from src.models import init_database

def create_database():
    """Create database if not exists"""
    try:
        # Connect to MySQL server (without specifying database)
        connection = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD
        )
        
        cursor = connection.cursor()
        
        # Create database if not exists
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        print(f"✅ Database '{DB_NAME}' created successfully!")
        
        cursor.close()
        connection.close()
        
        return True
        
    except Error as e:
        print(f"❌ Error creating database: {e}")
        return False

def check_database_exists():
    """Check if database exists"""
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD
        )
        
        cursor = connection.cursor()
        cursor.execute("SHOW DATABASES")
        databases = [db[0] for db in cursor.fetchall()]
        
        cursor.close()
        connection.close()
        
        return DB_NAME in databases
        
    except Error as e:
        print(f"❌ Error checking database: {e}")
        return False

def check_table_exists():
    """Check if attendance table exists"""
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        
        cursor = connection.cursor()
        cursor.execute("SHOW TABLES LIKE 'attendance'")
        result = cursor.fetchone()
        
        cursor.close()
        connection.close()
        
        return result is not None
        
    except Error as e:
        print(f"❌ Error checking table: {e}")
        return False

def get_table_columns():
    """Get existing columns in attendance table"""
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        
        cursor = connection.cursor()
        cursor.execute("""
            SELECT COLUMN_NAME 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_SCHEMA = %s AND TABLE_NAME = 'attendance'
        """, (DB_NAME,))
        
        existing_columns = [row[0] for row in cursor.fetchall()]
        
        cursor.close()
        connection.close()
        
        return existing_columns
        
    except Error as e:
        print(f"❌ Error getting table columns: {e}")
        return []

def upgrade_database():
    """Upgrade database dengan menambahkan kolom foto"""
    print("🔄 Checking and upgrading database schema...")
    
    try:
        existing_columns = get_table_columns()
        
        if not existing_columns:
            print("❌ No attendance table found. Please run setup first.")
            return False
        
        connection = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        
        cursor = connection.cursor()
        
        # Add photo_data column if not exists
        if 'photo_data' not in existing_columns:
            cursor.execute("""
                ALTER TABLE attendance 
                ADD COLUMN photo_data LONGBLOB NULL
            """)
            print("✅ Added photo_data column")
        else:
            print("ℹ️  photo_data column already exists")
        
        # Add photo_filename column if not exists
        if 'photo_filename' not in existing_columns:
            cursor.execute("""
                ALTER TABLE attendance 
                ADD COLUMN photo_filename VARCHAR(255) NULL
            """)
            print("✅ Added photo_filename column")
        else:
            print("ℹ️  photo_filename column already exists")
        
        # Add confidence_score column if not exists
        if 'confidence_score' not in existing_columns:
            cursor.execute("""
                ALTER TABLE attendance 
                ADD COLUMN confidence_score VARCHAR(10) NULL
            """)
            print("✅ Added confidence_score column")
        else:
            print("ℹ️  confidence_score column already exists")
        
        connection.commit()
        cursor.close()
        connection.close()
        
        print("✅ Database upgrade completed successfully!")
        return True
        
    except Error as e:
        print(f"❌ Error upgrading database: {e}")
        return False

def setup_database():
    """Setup complete database"""
    print("🚀 Setting up database...")
    
    # Step 1: Create database
    if not create_database():
        print("❌ Failed to create database!")
        return False
    
    # Step 2: Create tables
    if not init_database():
        print("❌ Failed to create tables!")
        return False
    
    print("✅ Database setup completed successfully!")
    return True

def check_and_setup():
    """Check database status and setup/upgrade as needed"""
    print("=== Database Management System ===")
    print("🔍 Checking database status...")
    
    # Check if database exists
    if not check_database_exists():
        print(f"📝 Database '{DB_NAME}' does not exist. Creating new database...")
        return setup_database()
    
    print(f"✅ Database '{DB_NAME}' exists")
    
    # Check if table exists
    if not check_table_exists():
        print("📝 Attendance table does not exist. Creating tables...")
        if not init_database():
            print("❌ Failed to create tables!")
            return False
        print("✅ Tables created successfully!")
    
    print("✅ Attendance table exists")
    
    # Check and upgrade schema
    existing_columns = get_table_columns()
    required_columns = ['photo_data', 'photo_filename', 'confidence_score']
    missing_columns = [col for col in required_columns if col not in existing_columns]
    
    if missing_columns:
        print(f"📝 Missing columns detected: {missing_columns}")
        print("🔄 Upgrading database schema...")
        return upgrade_database()
    else:
        print("✅ Database schema is up to date!")
        print(f"📊 Current columns: {existing_columns}")
        return True

def main():
    """Main function with menu"""
    import sys
    
    if len(sys.argv) > 1:
        action = sys.argv[1].lower()
        
        if action == 'setup':
            setup_database()
        elif action == 'upgrade':
            upgrade_database()
        elif action == 'check':
            check_and_setup()
        else:
            print("Usage: python setup_database.py [setup|upgrade|check]")
    else:
        # Interactive mode
        print("=== Database Management ===")
        print("1. Auto Check & Setup")
        print("2. Force New Setup")
        print("3. Force Upgrade")
        print("4. Exit")
        
        choice = input("Choose option (1-4): ").strip()
        
        if choice == '1':
            check_and_setup()
        elif choice == '2':
            setup_database()
        elif choice == '3':
            upgrade_database()
        elif choice == '4':
            print("Goodbye!")
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()