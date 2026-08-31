import os
import subprocess
import sys
import time


def main():
  port = os.environ.get("PORT", "8080")

  print("Starting FastAPI backend on port 8001...")
  fastapi_process = subprocess.Popen([
      sys.executable,
      "-m",
      "uvicorn",
      "app.main:app",
      "--host",
      "127.0.0.1",
      "--port",
      "8001",
  ])

  # Wait 3 seconds for FastAPI to fully initialize and bind to the port
  time.sleep(3)

  print(f"Starting Streamlit frontend on port {port}...")
  streamlit_process = subprocess.Popen([
      sys.executable,
      "-m",
      "streamlit",
      "run",
      "app.py",
      f"--server.port={port}",
      "--server.address=0.0.0.0",
      "--server.headless=true",
  ])

  try:
    streamlit_process.wait()
  except KeyboardInterrupt:
    fastapi_process.terminate()
    streamlit_process.terminate()


if __name__ == "__main__":
  main()
