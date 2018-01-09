# echo_server.py
import socket
from Settings import Settings

sett = Settings().settings

host = ''        # Symbolic name meaning all available interfaces
port = sett["port"]     # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(1)
while True:
    conn, addr = s.accept()
    print('Connected by', addr)
    data = conn.recv(1048576)
    print(data)
    conn.close()