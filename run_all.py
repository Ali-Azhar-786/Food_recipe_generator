# run_all.py
import os
import sys
import threading
import uvicorn
import subprocess
import time

# ── Configuration ───────────────────────────────────────────────
BACKEND_PORT = 8000
UVICORN_LOG_LEVEL = "info"   # can be "debug", "info", "warning"

def run_fastapi():
    """Run FastAPI server in background thread"""
    os.environ["UVICORN_LOG_LEVEL"] = UVICORN_LOG_LEVEL
    
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=BACKEND_PORT,
        reload=False,           # reload=False in production-like mode
        log_level=UVICORN_LOG_LEVEL,
        workers=1
    )

def wait_for_backend(max_wait=15):
    """Wait until backend is ready"""
    import requests
    
    url = f"http://127.0.0.1:{BACKEND_PORT}/health"
    for i in range(max_wait):
        try:
            r = requests.get(url, timeout=2)
            if r.status_code == 200:
                print(f"✓ Backend is ready after {i+1} seconds")
                return True
        except:
            pass
        time.sleep(1)
    
    print("✗ Backend did not start in time")
    return False

if __name__ == "__main__":
    print("Starting Food Recipe Generator...")
    print("Launching FastAPI backend in background...")
    
    # Start FastAPI in a separate thread
    backend_thread = threading.Thread(
        target=run_fastapi,
        daemon=True
    )
    backend_thread.start()
    
    # Give backend a moment to start
    time.sleep(2)
    
    if not wait_for_backend():
        print("\nWarning: Backend might be slow to start.")
        print("You can still try to use the app, but it may take a few more seconds.\n")
    
    print("\nLaunching Streamlit frontend...\n")
    
    # Launch Streamlit (this will take over the main thread)
    subprocess.run([
        sys.executable, "-m", "streamlit", "run",
        "streamlit_app.py",
        "--server.port=8501",
        "--server.headless=true"    # optional - cleaner in some environments
    ])