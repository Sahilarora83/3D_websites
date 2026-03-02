#!/usr/bin/env python3
"""
HTTP server that handles Next.js image optimization API requests
"""

import http.server
import socketserver
import urllib.parse
import os
import mimetypes

PORT = 8000
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Parse the request URL
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path
        query = parsed_url.query
        
        # Handle Next.js image optimization API requests
        if path == '/_next/image/' or path == '/_next/image':
            params = urllib.parse.parse_qs(query)
            if 'url' in params:
                # Decode the image URL
                image_url = urllib.parse.unquote(params['url'][0])
                
                # Remove leading slash if present
                if image_url.startswith('/'):
                    image_url = image_url[1:]
                
                # Build the full file path
                file_path = os.path.join(BASE_DIR, image_url)
                
                # Security check: ensure the file is within the base directory
                real_path = os.path.realpath(file_path)
                base_real_path = os.path.realpath(BASE_DIR)
                
                if not real_path.startswith(base_real_path):
                    print(f"[SECURITY] Access denied: {real_path}")
                    self.send_response(403)
                    self.send_header('Content-Type', 'text/plain')
                    self.end_headers()
                    return
                
                # Check if file exists
                if os.path.exists(real_path) and os.path.isfile(real_path):
                    try:
                        with open(real_path, 'rb') as f:
                            content = f.read()
                        
                        # Set appropriate content type
                        mime_type, _ = mimetypes.guess_type(real_path)
                        if mime_type is None:
                            mime_type = 'application/octet-stream'
                        
                        self.send_response(200)
                        self.send_header('Content-Type', mime_type)
                        self.send_header('Content-Length', len(content))
                        self.send_header('Cache-Control', 'public, max-age=31536000')
                        self.end_headers()
                        self.wfile.write(content)
                        print(f"[OK] /_next/image/ -> {image_url} ({len(content)} bytes)")
                        return
                    except Exception as e:
                        print(f"[ERROR] Reading file {real_path}: {e}")
                        self.send_response(500)
                        self.send_header('Content-Type', 'text/plain')
                        self.end_headers()
                        return
                else:
                    print(f"[NOT_FOUND] {image_url} - {real_path}")
                    self.send_response(404)
                    self.send_header('Content-Type', 'text/plain')
                    self.end_headers()
                    return
        
        # For all other requests, use the default handler
        try:
            super().do_GET()
        except (ConnectionAbortedError, ConnectionResetError):
            # Ignore errors caused by the browser disconnecting early (e.g., during page refresh)
            pass
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BASE_DIR, **kwargs)
    
    def address_string(self):
        # Prevent reverse DNS lookups which cause massive delays
        return self.client_address[0]

    def log_message(self, format, *args):
        # Mute normal GET request logs to keep terminal clean (optional)
        # print(f"[{self.client_address[0]}] {format % args}")
        pass

    def log_error(self, format, *args):
        # Mute standard 404 errors
        if "404" in str(args) or "File not found" in format % args:
            return
        super().log_error(format, *args)

class QuietThreadingTCPServer(socketserver.ThreadingTCPServer):
    def handle_error(self, request, client_address):
        # Suppress standard "ConnectionAbortedError" and "ConnectionResetError" spam 
        # that happens when a browser cancels a loading image
        import sys
        err = sys.exc_info()[1]
        if isinstance(err, (ConnectionAbortedError, ConnectionResetError)):
            return
        super().handle_error(request, client_address)

if __name__ == '__main__':
    os.chdir(BASE_DIR)
    handler = CustomHTTPRequestHandler
    
    # Enable threading to handle parallel browser requests instantly
    QuietThreadingTCPServer.allow_reuse_address = True
    with QuietThreadingTCPServer(("", PORT), handler) as httpd:
        print(f"Server running at http://localhost:{PORT}")
        print(f"Serving files from: {BASE_DIR}")
        print("Fast Multi-threaded Mode: ON")
        print("Hit Ctrl+C to stop the server")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped")
