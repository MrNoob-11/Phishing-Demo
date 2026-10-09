import os
import sys
import time
import subprocess
import urllib.request
from urllib.error import URLError
import re

def main():
    # 1. We create an empty list to keep track of our background processes
    processes = []
    
    project_dir = os.path.expanduser("~/Desktop/PhishingDemoFresh")
    
    # 2. Wrap the core logic in a try block so we can catch the Ctrl+C shutdown
    try:
        os.chdir(project_dir)
        venv_python = os.path.join(project_dir, ".venv", "bin", "python")
        print("Inside the project folder!")
        
        print("Starting Flask as a module...")
        # Make sure this line is fully spelled out without the '$' truncation:
        flask_proc = subprocess.Popen([venv_python, "-m", "flask", "run", "--port", "5000"])
        processes.append(flask_proc) # Save Flask process handle to our list
        
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
            
        # 3. Add the missing Cloudflare process launcher step!
        print("Starting Cloudflare tunnel...")
        with open("/tmp/phishing-demo-cloudflared.log", "w") as log_file:
            pass  # Truncates old logs
            
        log_handle = open("/tmp/phishing-demo-cloudflared.log", "a")
        cf_proc = subprocess.Popen(
            ["cloudflared", "tunnel", "--url", "http://127.0.0.1:5000"],
            stdout=log_handle,
            stderr=log_handle
        )
        processes.append(cf_proc) # Save Cloudflare process handle to our list

        print("Waiting for Cloudflare URL...")
        public_url = None

        for i in range(30):
            time.sleep(1)
            if os.path.exists("/tmp/phishing-demo-cloudflared.log"):
                # Make sure this line is fully spelled out:
                with open("/tmp/phishing-demo-cloudflared.log", "r") as log_file:
                    log_data = log_file.read()

                # Make sure this regex line is fully spelled out:
                match = re.search(r"https://[a-zA-Z0-9-]+\.trycloudflare\.com", log_data)
                if match:
                    public_url = match.group(0)
                    break

        if public_url:
            print("\n========================================")
            print(f" Your Phishing Demo is live at:")
            print(f" {public_url}")
            print("========================================\n")
            
            # 4. The Keep-Alive Infinite Loop that anchors your background tasks
            print("Press Ctrl+C to stop the servers safely.")
            while True:
                time.sleep(1)
        else:
            print("Could not find Cloudflare URL in logs.")
            
    # 5. The safety net that runs automatically when the script ends or you hit Ctrl+C
    finally:
        print("\nStopping background servers cleanly...")
        for proc in processes:
            if proc.poll() is None:  # If the server process is still active
                proc.terminate()    # Tell it to shut down
                proc.wait()         # Wait for it to close completely to free the port
        print("All ports clean. Goodbye!")

if __name__ == "__main__":
    main()

