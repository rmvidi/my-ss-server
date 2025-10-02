import socket

HOST = '0.0.0.0'  # Makikinig sa lahat ng network interfaces
PORT = 12345      # Pwede mong palitan ng kahit anong libre na port

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f'Server listening on {HOST}:{PORT}')
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        conn.sendall(b'Hello from server!')
