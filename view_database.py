import os
import sqlite3

def display_logs():
    """Queries the SQLite local database file and prints out all logs cleanly."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, "demo_database.db")
    
    if not os.path.exists(db_path):
        print("\n[DATABASE] No database file found yet. Submit a test form first!\n")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT id, timestamp, email, status FROM submissions")
        rows = cursor.fetchall()
        
        if not rows:
            print("\n[DATABASE] The database file exists but contains zero submission logs.\n")
            return
            
        print("\n" + "="*85)
        print(f"{'ID':<5} | {'TIMESTAMP (CDT/Z)':<25} | {'LOGGED EMAIL METRIC':<30} | {'STATUS'}")
        print("="*85)
        
        # THE FIX: Explicitly unpack the individual columns from the data row tuple
        for row in rows:
            sub_id, timestamp, email, status = row
            print(f"{sub_id:<5} | {timestamp:<25} | {email:<30} | {status}")
        print("="*85 + "\n")
        
    except sqlite3.OperationalError:
        print("\n[DATABASE ERROR] Submissions table does not exist inside the database file yet.\n")
    finally:
        conn.close()

if __name__ == "__main__":
    display_logs()

