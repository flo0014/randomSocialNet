import sqlite3

def connect_to_database(db_path):
    try:
        # Connect to SQLite database. This will create a new database file if it doesn't exist.
        conn = sqlite3.connect(db_path)
        print("Successfully connected to SQLite database")
        return conn
    except sqlite3.Error as e:
        print("Error occurred while connecting to SQLite database:", e)
        return None

# Example usage:
if __name__ == "__main__":
    db_path = "../database/app_data.db"  # Replace with the actual path to your SQLite database file
    connection = connect_to_database(db_path)

    # Don't forget to close the connection when done
    if connection:
        connection.close()


def create_tables(conn):
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS MotsCles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        mot_cle TEXT NOT NULL UNIQUE
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Sources (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source TEXT NOT NULL,
        mot_cle_id INTEGER,
        FOREIGN KEY (mot_cle_id) REFERENCES MotsCles(id)
    );
    """)

    conn.commit()

# Creating tables on script run
if __name__ == '__main__':
    db_path = '../database/app_data.db'
    conn = connect_to_database(db_path)
    if conn:
        create_tables(conn)
        conn.close()
