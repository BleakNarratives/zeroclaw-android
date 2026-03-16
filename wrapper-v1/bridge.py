'#!/usr/bin/env python3
"""
zeroclaw → TCP Bridge
Listens to zeroclaw subscribe, pipes JSON deltas to localhost:8080
"""

import subprocess
import socket
import json
import sys
import signal
import time
from threading import Thread, Lock

class ZeroClawBridge:
    def __init__(self, host='127.0.0.1', port=8080):
        self.host = host
        self.port = port
        self.server_socket = None
        self.clients = []
        self.clients_lock = Lock()
        self.running = True
        
    def start_server(self):
        """Start TCP server listening for client connections"""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"[BRIDGE] Listening on {self.host}:{self.port}", file=sys.stderr)
        
        while self.running:
            try:
                client_socket, client_addr = self.server_socket.accept()
                print(f"[BRIDGE] Client connected: {client_addr}", file=sys.stderr)
                with self.clients_lock:
                    self.clients.append(client_socket)
            except OSError:
                break
    
def broadcast(self, data):
        """Send data to all connected clients"""
        with self.clients_lock:
            dead_clients = []
            for client in self.clients:
                try:
                    client.sendall(data.encode('utf-8') + b'\n')
                except (BrokenPipeError, ConnectionResetError):
                    dead_clients.append(client)
            
            for client in dead_clients:
                self.clients.remove(client)
                client.close()
    
def start_zeroclaw_subscribe(self):
        """Start zeroclaw subscribe subprocess and pipe output"""
        try:
            proc = subprocess.Popen(
                ['zeroclaw', 'subscribe'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                bufsize=1
            )
            print(f"[ZEROCLAW] Process started (PID: {proc.pid})", file=sys.stderr)
            
            for line in proc.stdout:
                if not self.running:
                    break
                
                line = line.strip()
                if line:
                    try:
                        # Validate it's JSON
                        json.loads(line)
                        self.broadcast(line)
                        print(f"[EVENT] {line[:80]}", file=sys.stderr)
                    except json.JSONDecodeError:
                        print(f"[ERROR] Invalid JSON: {line[:80]}", file=sys.stderr)
            
            proc.wait()
        except FileNotFoundError:
            print("[ERROR] zeroclaw not found in PATH", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"[ERROR] zeroclaw process error: {e}", file=sys.stderr)
            sys.exit(1)
    
def shutdown(self, signum=None, frame=None):
        """Graceful shutdown"""
        print("\n[BRIDGE] Shutting down...", file=sys.stderr)
        self.running = False
        with self.clients_lock:
            for client in self.clients:
                try:
                    client.close()
                except:
                    pass
        if self.server_socket:
            self.server_socket.close()
        sys.exit(0)
    
def run(self):
        """Start server and zeroclaw subscription threads"""
        signal.signal(signal.SIGINT, self.shutdown)
        signal.signal(signal.SIGTERM, self.shutdown)
        
        server_thread = Thread(target=self.start_server, daemon=False)
        zeroclaw_thread = Thread(target=self.start_zeroclaw_subscribe, daemon=False)
        
        server_thread.start()
        zeroclaw_thread.start()
        
        server_thread.join()
        zeroclaw_thread.join()

if __name__ == '__main__':
    bridge = ZeroClawBridge()
    bridge.run()'