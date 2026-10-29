import socket

HOST = "127.0.0.1"
PORT = 5000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen()
    print(f"Server läuft auf {HOST}:{PORT}")

    while True:
        conn, addr = s.accept()
        print(f"Verbunden mit {addr}")
        with conn:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                print("Empfangen:", data.decode().strip())
        print("Verbindung getrennt, warte auf neuen Client...")