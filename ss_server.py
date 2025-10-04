import socket
import threading
from Crypto.Cipher import ChaCha20
from Crypto.Random import get_random_bytes
from lru_cache import LRUCache

HOST = '0.0.0.0'
PORT = 8388
KEY = b'0123456789ABCDEF0123456789ABCDEF'  # 32 bytes
CACHE_CAPACITY = 10
cache = LRUCache(capacity=CACHE_CAPACITY)

def handle_client(conn, addr):
    print(f"[+] New connection from {addr}")
    
    # Generate random nonce per session
    nonce = get_random_bytes(12)
    cipher_enc = ChaCha20.new(key=KEY, nonce=nonce)
    cipher_dec = ChaCha20.new(key=KEY, nonce=nonce)
    
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            # Decrypt incoming data
            decrypted = cipher_dec.decrypt(data)
            
            # Cache the message (optional)
            cache.put(addr, decrypted)
            
            # Encrypt response and send back
            response = cipher_enc.encrypt(decrypted)
            conn.sendall(response)
    except Exception as e:
        print(f"[!] Connection error: {e}")
    finally:
        conn.close()
        print(f"[-] Connection closed {addr}")

def start_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(5)
    print(f"Server running on {HOST}:{PORT} ...")
    
    while True:
        conn, addr = s.accept()
        t = threading.Thread(target=handle_client, args=(conn, addr))
        t.start()

if __name__ == "__main__":
    start_server()
