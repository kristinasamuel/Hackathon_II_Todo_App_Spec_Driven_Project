import sqlite3
import os

# Connect to the existing database
db_path = "todo_backend.db"  # Default SQLite path from the code
if os.path.exists(db_path):
    print(f"Found database at: {db_path}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check if the password column exists
    cursor.execute("PRAGMA table_info(user)")
    columns = [column[1] for column in cursor.fetchall()]

    if 'password' not in columns:
        print("Adding password column to user table...")
        try:
            # Add password column to the user table
            cursor.execute("ALTER TABLE user ADD COLUMN password TEXT NOT NULL DEFAULT '';")
            conn.commit()
            print("Password column added successfully!")
        except sqlite3.Error as e:
            print(f"Error adding password column: {e}")
    else:
        print("Password column already exists.")

    # Close connection
    conn.close()
    print("Database migration completed.")
else:
    print(f"Database file not found at: {db_path}")
    print("This script assumes the database is stored locally as 'todo_backend.db'")