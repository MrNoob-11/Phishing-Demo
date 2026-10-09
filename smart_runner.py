import os
import sys
import time
import subprocess
import urllib.request
from urllib.error import URLError
import re

def main():
    processes = []
    project_dir = os.path.expanduser("~/Desktop/PhishingDemoFresh")
    
    try:
        os.chdir(project_dir)
        venv_python = os.path.join(project_dir, ".venv", "bin", "python")
        print("Inside the project folder!")
        
        print("Starting Flask as a module...")
        flask_proc = subprocess.Popen([venv_python, "-m", "flask", "run", "--port", "5000"])
        processes.append(flask_proc)
        
        print("Waiting for Flask to respond...")
        flask_ready = False
        for i in range(20):
            try:
                with urllib.request.urlopen("http://127.0.0.1:5000", timeout=1):
                    flask_ready = True
                    break
            except URLError:
                time.sleep(1)
                
        if flask_ready:
            print("Flask is online and ready!")
        else:
            print("Flask took too long to start.")
            flask_proc.terminate()
            sys.exit(1)
            
        print("Starting Cloudflare tunnel...")
        with open("/tmp/phishing-demo-cloudflared.log", "w") as log_file:
            pass
            
        log_handle = open("/tmp/phishing-demo-cloudflared.log", "a")
        cf_proc = subprocess.Popen(
            ["cloudflared", "tunnel", "--url", "http://127.0.0.1:5000"],
            stdout=log_handle,
            stderr=log_handle
        )
        processes.append(cf_proc)

        print("Waiting for Cloudflare URL...")
        public_url = None

        for i in range(30):
            time.sleep(1)
            if os.path.exists("/tmp/phishing-demo-cloudflared.log"):
                with open("/tmp/phishing-demo-cloudflared.log", "r") as log_file:
                    log_data = log_file.read()

                match = re.search(r"https://[a-zA-Z0-9-]+\.trycloudflare\.com", log_data)
                if match:
                    public_url = match.group(0)
                    break

        if public_url:
            print("\n========================================")
            print(f" Your Phishing Demo is live at:")
            print(f" {public_url}")
            print("========================================\n")
            
            print("Press Ctrl+C to stop the servers safely.")
            while True:
                time.sleep(1)
        else:
            print("Could not find Cloudflare URL in logs.")
            
    finally:
        print("\nStopping background servers cleanly...")
        for proc in processes:
            if proc.poll() is None:
                proc.terminate()
                proc.wait()
        print("All ports clean. Goodbye!")

if __name__ == "__main__":
    main()

