import sqlite3
import os

# Connect to the existing database
db_path = "todo_backend.db"  # Default SQLite path from the code
if os.path.exists(db_path):
    print(f"Found database at: {db_path}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check if the password column exists in user table
    cursor.execute("PRAGMA table_info(user)")
    user_columns = [column[1] for column in cursor.fetchall()]

    if 'password' not in user_columns:
        print("Adding password column to user table...")
        try:
            # Add password column to the user table
            cursor.execute("ALTER TABLE user ADD COLUMN password TEXT NOT NULL DEFAULT '';")
            conn.commit()
            print("Password column added successfully!")
        except sqlite3.Error as e:
            print(f"Error adding password column: {e}")
    else:
        print("Password column already exists in user table.")

    # Check if the priority and due_date columns exist in task table
    cursor.execute("PRAGMA table_info(task)")
    task_columns = [column[1] for column in cursor.fetchall()]

    if 'priority' not in task_columns:
        print("Adding priority column to task table...")
        try:
            # Add priority column to the task table
            cursor.execute("ALTER TABLE task ADD COLUMN priority TEXT DEFAULT 'medium';")
            conn.commit()
            print("Priority column added successfully!")
        except sqlite3.Error as e:
            print(f"Error adding priority column: {e}")
    else:
        print("Priority column already exists in task table.")

    if 'due_date' not in task_columns:
        print("Adding due_date column to task table...")
        try:
            # Add due_date column to the task table
            cursor.execute("ALTER TABLE task ADD COLUMN due_date TIMESTAMP DEFAULT NULL;")
            conn.commit()
            print("Due date column added successfully!")
        except sqlite3.Error as e:
            print(f"Error adding due_date column: {e}")
    else:
        print("Due date column already exists in task table.")

    # Close connection
    conn.close()
    print("Database migration completed.")
else:
    print(f"Database file not found at: {db_path}")
    print("This script assumes the database is stored locally as 'todo_backend.db'")