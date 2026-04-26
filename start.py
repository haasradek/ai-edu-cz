#!/usr/bin/env python3
"""Spustí AI-EDU-CZ dashboard — automaticky uvolní port 8765."""
import subprocess, sys, webbrowser, time

PORT = 8765

def free_port():
    """Zabije cokoliv co běží na portu 8765."""
    r = subprocess.run(
        ['powershell', '-Command',
         f'$p=(Get-NetTCPConnection -LocalPort {PORT} -ErrorAction SilentlyContinue).OwningProcess;'
         f'if($p){{Stop-Process -Id $p -Force;Write-Host "Uvolnen port {PORT}"}}'],
        capture_output=True, text=True
    )
    if 'Uvolnen' in r.stdout:
        print(f"  ↯ Uvolněn port {PORT} (starý server zastaven)")
        time.sleep(0.8)

print("\n  AI-EDU-CZ Mission Control")
print("  ─────────────────────────")
print(f"  http://localhost:{PORT}\n")

free_port()

proc = subprocess.Popen(
    [sys.executable, "-m", "uvicorn", "server.main:app",
     "--host", "localhost", f"--port", str(PORT)],
    cwd=str(__import__('pathlib').Path(__file__).parent)
)
time.sleep(1.5)
webbrowser.open(f"http://localhost:{PORT}")
try:
    proc.wait()
except KeyboardInterrupt:
    proc.terminate()
    print("\n  Dashboard zastaven.")
