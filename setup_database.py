#!/usr/bin/env python3
"""
Setup script untuk database attendance system
Jalankan script ini untuk membuat database dan tabel yang diperlukan
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
        print(f"Database '{DB_NAME}' created successfully!")
        
        cursor.close()
        connection.close()
        
        return True
        
    except Error as e:
        print(f"Error creating database: {e}")
        return False

def setup_database():
    """Setup complete database"""
    print("=== Database Setup ===")
    
    # Step 1: Create database
    if not create_database():
        print("Failed to create database!")
        return False
    
    # Step 2: Create tables
    if not init_database():
        print("Failed to create tables!")
        return False
    
    print("Database setup completed successfully!")
    return True

if __name__ == "__main__":
    setup_database()