import os
import subprocess
import sys


def main():
  port = os.environ.get("PORT", "8000")

  print("Starting FastAPI backend...")
  fastapi_process = subprocess.Popen([
      sys.executable,
      "-m",
      "uvicorn",
      "app.main:app",
      "--host",
      "127.0.0.1",
      "--port",
      "8000",
  ])

  print(f"Starting Streamlit frontend on port {port}...")
  # Use sys.executable to run streamlit as a module (-m streamlit)
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
