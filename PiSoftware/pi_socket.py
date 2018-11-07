import socket

##Creating UDP socket to send sensor data to server
sensor_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


##Sending signals through Pi socket
HOST = "172.29.68.61"
PORT = 10000
ADDRESS = (HOST, PORT)

##Send sensor data continuously until stop signal received
##Keep listening until program closed
while True:
	data,addr = sensor_socket.recvfrom(4096)
	if data == "stop":
		print (data)
	else:
		sensor_socket.sendto("sensor data", ADDRESS)