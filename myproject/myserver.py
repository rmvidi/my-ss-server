import socket

HOST = '0.0.0.0'  # Makikinig sa lahat ng n>
PORT = 12345      # Pwede mong palitan ng k>

with socket.socket(socket.AF_INET, socket.S>
    s.bind((HOST, PORT))
    s.listen()
    print(f'Server listening on {HOST}:{POR>
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        conn.sendall(b'Hello from server!')
