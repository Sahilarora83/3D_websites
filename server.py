#!/usr/bin/env python3
"""
Simple static file server with CORS support
"""

import http.server
import socketserver
import os

PORT = 8000
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class CORSRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, HEAD, OPTIONS, POST')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Range')
        self.send_header('Access-Control-Max-Age', '3600')
        self.end_headers()
    
    def end_headers(self):
        # Add CORS headers to all responses
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, HEAD, OPTIONS, POST')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Range')
        super().end_headers()
    
    def do_GET(self):
        # Serve files directly
        try:
            super().do_GET()
        except (ConnectionAbortedError, ConnectionResetError):
            pass
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BASE_DIR, **kwargs)
    
    def address_string(self):
        return self.client_address[0]

if __name__ == '__main__':
    os.chdir(BASE_DIR)
    
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), CORSRequestHandler) as httpd:
        print(f"✅ Server running at http://localhost:{PORT}")
        print(f"📁 Serving from: {BASE_DIR}")
        print("🌍 CORS enabled for all origins")
        print("Press Ctrl+C to stop")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n✋ Server stopped")

