import socket
import os
import subprocess
import time

subprocess.Popen("python3.5 Video_detection_send.py".split())

separator = '<SEPARATOR>'
buffer_size = 4096

host = '10.0.0.40'
port = 65432
server_host = '10.0.0.5'
server_port = port
folder = "Images/"

while True:
        try:
                filename = os.listdir(folder)[0]
                filesize = os.path.getsize(folder + filename)
                time.sleep(1)
                s = socket.socket()

                #print(f"Connection to {host}:{port}")
                s.connect((host, port))
                #print("CONNECTION SUCCESS!")

                s.send(f"{filename}{separator}{filesize}".encode())
                with open(folder + filename, "rb") as f:
                        while True:
                                bytes_read = f.read(buffer_size)
                                if not bytes_read:
                                        break
                                s.sendall(bytes_read)

                s.close()

                s = socket.socket()
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.bind((server_host, server_port))
                s.listen(5)
                #print(f"Listening as {server_host}:{server_port}")
                client_socket, address = s.accept()
                #print(f"{address[0]}:{address[1]} is connected")

                name = client_socket.recv(buffer_size).decode()
                print(f"I see {name.upper()}")
                os.remove(folder + filename)
        except IndexError:
                print(".", end="", flush=True)
