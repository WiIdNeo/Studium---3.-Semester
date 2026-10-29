import socket
import time

HOST = "127.0.0.1"
PORT = 5000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    i = 0
    while True:
        s.sendall(f"Hallo Server! Nachricht {i}\n".encode())
        i += 1
        time.sleep(1)