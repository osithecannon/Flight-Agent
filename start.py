import os
import subprocess
import sys


def main():
  port = os.environ.get("PORT", "8000")

  # Start FastAPI in the background using uvicorn
  print("Starting FastAPI backend...")
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

  # Start Streamlit on the main port required by Railway
  print(f"Starting Streamlit frontend on port {port}...")
  streamlit_process = subprocess.Popen([
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
