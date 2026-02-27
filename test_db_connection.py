# test_db_connection.py
"""
Test if database connection works
Run this to make sure PostgreSQL is set up correctly
"""

import psycopg2
from config import config

try:
    # Try to connect
    connection = psycopg2.connect(
        database="analytics",
        user="postgres",
        password="password",
        host="localhost",
        port="5432"
    )

    # Create cursor (tool to run commands)
    cursor = connection.cursor()

    # Run a test query
    cursor.execute("SELECT COUNT(*) FROM sales_daily;")
    count = cursor.fetchone()[0]

    print("Database connected successfully!")
    print(f"Found {count} rows in sales_daily table")

    # Close cleanly
    cursor.close()
    connection.close()

except Exception as e:
    print(f"Database connection failed: {e}")
    print("Make sure PostgreSQL is running and credentials are correct!")