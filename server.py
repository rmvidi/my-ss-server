#!/usr/bin/python

# -------------------
# HTTP Handler
# -------------------
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Kung WebSocket path (huwag sagutin dito)
        if self.path == "/ws":
            self.send_response(426)  # Upgrade Required
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"This endpoint is for WebSocket only.\n")
            return

        # Normal GET logic
        key = self.path
        value = cache.get(key)
        if value is None:
            value = f"Data for {key}"
            cache.put(key, value)

        self.send_response(200)
        self.send_header('Content-type', 'text/plain; charset=utf-8')
        self.end_headers()

        try:
            self.wfile.write(value.encode('utf-8'))
        except BrokenPipeError:
            print(f"Client disconnected before receiving response for {key}")

# -------------------
# WebSocket Handler
# -------------------
async def ws_handler(websocket, path):
    print(f"New WebSocket connection: {path}")
    try:
        async for message in websocket:
            print(f"Received: {message}")
            await websocket.send(f"Echo: {message}")
    except websockets.exceptions.ConnectionClosed:
        print("WebSocket client disconnected")

def start_websocket(local_ip):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    ws_server = websockets.serve(ws_handler, "0.0.0.0", 8765)
    loop.run_until_complete(ws_server)
    print("WebSocket server running at:")
    print(f" - ws://localhost:8765/ws")
    print(f" - ws://{local_ip}:8765/ws  (for other devices in Wi-Fi)")
    loop.run_forever()

from http.server import BaseHTTPRequestHandler
from lru_cache import LRUCache

# Gumawa ng cache instance
cache = LRUCache(capacity=5)

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Kung path ay /ws → huwag i-handle, sabihan lang
        if self.path == "/ws":
            self.send_response(426)  # Upgrade Required
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            try:
                self.wfile.write(b"This endpoint is for WebSocket only.\n")
            except BrokenPipeError:
                pass
            return

        # Normal GET logic
        key = self.path
        value = cache.get(key)
        if value is None:
            value = f"Data for {key}"
            cache.put(key, value)

        # Send response headers
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()

        # Write response safely
        try:
            self.wfile.write(value.encode("utf-8"))
        except BrokenPipeError:
            print(f"Client disconnected before receiving response for {key}")

