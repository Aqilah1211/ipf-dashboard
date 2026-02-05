#!/usr/bin/env python3
"""
Simple HTTP Server untuk IFP Monitoring Dashboard
Jalankan: python run_server.py
Atau: python -m http.server 8000

Akses: http://localhost:8000/Monitoring.html
"""

import http.server
import socketserver
import os
import sys
from pathlib import Path

PORT = 8000

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Serve files dengan default ke Monitoring.html"""
    
    def end_headers(self):
        # Prevent caching untuk development
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

def start_server():
    """Start HTTP server di port 8000"""
    # Change to script directory
    script_dir = Path(__file__).parent.absolute()
    os.chdir(script_dir)
    
    handler = MyHTTPRequestHandler
    try:
        with socketserver.TCPServer(("", PORT), handler) as httpd:
            print(f"✅ Server running at http://localhost:{PORT}")
            print(f"📂 Serving from: {script_dir}")
            print(f"🌐 Dashboard: http://localhost:{PORT}/Monitoring.html")
            print(f"⏹️  Press Ctrl+C to stop\n")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n✓ Server stopped")
        sys.exit(0)
    except OSError as e:
        if e.errno == 48:  # Port already in use (macOS)
            print(f"❌ Port {PORT} already in use. Try another port or stop the other process.")
        else:
            print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    start_server()
