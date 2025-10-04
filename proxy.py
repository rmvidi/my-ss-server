import socket
import threading

def handle_client(client_socket):
    request = client_socket.recv(4096)

    # Parse HTTP request (kunin host)
    try:
        first_line = request.split(b'\n')[0]
        url = first_line.split(b' ')[1]
        http_pos = url.find(b"://")
        if http_pos != -1:
            url = url[(http_pos+3):]
        port_pos = url.find(b":")
        path_pos = url.find(b"/")
        if path_pos == -1:
            path_pos = len(url)

        webserver = ""
        port = 80

        if port_pos == -1 or path_pos < port_pos:
            port = 80
            webserver = url[:path_pos]
        else:
            port = int((url[(port_pos+1):])[:path_pos-port_pos-1])
            webserver = url[:port_pos]

        # Connect to target webserver
        proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        proxy_socket.connect((webserver.decode(), port))
        proxy_socket.send(request)

        while True:
            data = proxy_socket.recv(4096)
            if len(data) > 0:
                client_socket.send(data)
            else:
                break

        proxy_socket.close()
        client_socket.close()
    except Exception as e:
        print("Error:", e)
        client_socket.close()

def start_proxy(host="0.0.0.0", port=8080):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(10)
    print(f"[*] Proxy server listening on {host}:{port}")

    while True:
        client_socket, addr = server.accept()
        print(f"[*] Received connection from {addr}")
        handler = threading.Thread(target=handle_client, args=(client_socket,))
        handler.start()

if __name__ == "__main__":
    start_proxy()
