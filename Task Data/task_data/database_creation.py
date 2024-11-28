import sqlite3

def setup_database():
    conn = sqlite3.connect('vikings.db')
    cursor = conn.cursor()
    
    # Create table for characters
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS characters (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        actor TEXT,
        photo_url TEXT
    )
    ''')
    
    # Create table for NFL stats
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS nfl_players (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        position TEXT,
        stats TEXT,
        photo_url TEXT
    )
    ''')
    
    conn.commit()
    conn.close()

# Example usage
setup_database()
