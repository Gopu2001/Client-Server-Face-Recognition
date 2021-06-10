import socket
import os
from imageClassifier import Rekognize

rek = Rekognize()

server_host = '10.0.0.40'
server_port = 65432
host = '10.0.0.5'
port = server_port
buffer_size = 4096
separator = "<SEPARATOR>"
folder = "Images/"

while True:
	s = socket.socket()
	s.bind((server_host,server_port))

	s.listen(5)
	print(f"Listening as {server_host}:{server_port}")
	client_socket, address = s.accept()
	print(f"{address[0]}:{address[1]} is connected")

	received = client_socket.recv(buffer_size).decode()
	filename, filesize = received.split(separator)
	filename = os.path.basename(filename)
	filesize = int(filesize)

	with open(folder + filename, "wb") as f:
		while True:
			bytes_read = client_socket.recv(buffer_size)
			if not bytes_read:
				break
			f.write(bytes_read)

	client_socket.close()
	s.close()

	name = rek.classify(folder + filename)
	s = socket.socket()

	print(f"Connection to {host}:{port}")
	s.connect((host, port))
	print(f"Found {name} in {filename}")
	s.send(name.encode())
	s.close()
