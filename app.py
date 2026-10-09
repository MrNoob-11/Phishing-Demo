from datetime import datetime
import os
import sys

def create_app():
    """Builds the Flask application after our search paths are injected."""
    # We move the flask import inside here so it doesn't crash on launch!
    from flask import Flask, render_template, request, jsonify
    
    app = Flask(__name__)

    @app.get("/")
    def home():
        return render_template("index.html")

    @app.post("/simulate")
    def simulate():
        data = request.get_json(silent=True) or {}
        if data.get("event") != "demo-submit":
            return jsonify(ok=False), 400

        email = str(data.get("email", "")).strip()
        if not email or len(email) > 254:
            return jsonify(ok=False, message="Enter a valid demo email."), 400

        timestamp = datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")
        print(f"\n[{timestamp}] CONSENTED DEMO SUBMISSION")
        print(f"Demo email: {email}")
        print("Password: NOT TRANSMITTED")
        print("-" * 40)

        return jsonify(ok=True, message="Demo complete. Password was not transmitted.")
        
    return app


def start_server():
    """Entry point for your global terminal shortcut command."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(base_dir)

    # Forcefully inject your hidden virtual environment paths BEFORE loading Flask
    venv_site_packages = os.path.join(base_dir, ".venv", "lib", "python3.14", "site-packages")
    if os.path.exists(venv_site_packages):
        sys.path.insert(0, venv_site_packages)
    
    # Safe to load now!
    app = create_app()
    print("Launching Flask Web Server...")
    app.run(host="127.0.0.1", port=5000, debug=False)

if __name__ == "__main__":
    start_server()

