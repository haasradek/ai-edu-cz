#!/usr/bin/env python3
"""Spustí AI-EDU-CZ dashboard. Otevři http://localhost:8765"""
import subprocess, sys, webbrowser, time

print("\n  🤖 AI-EDU-CZ Mission Control")
print("  ─────────────────────────────")
print("  http://localhost:8765\n")

proc = subprocess.Popen(
    [sys.executable, "-m", "uvicorn", "server.main:app",
     "--host", "localhost", "--port", "8765"],
    cwd=str(__import__('pathlib').Path(__file__).parent)
)
time.sleep(1.5)
webbrowser.open("http://localhost:8765")
try:
    proc.wait()
except KeyboardInterrupt:
    proc.terminate()
    print("\n  Dashboard zastaven.")
