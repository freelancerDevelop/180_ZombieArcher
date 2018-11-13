import socket

##Creating UDP socket to communicate with Unity
global unity_socket
unity_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
##Binding Unity socket to IP address
HOST = "172.29.70.132"
UNITY_PORT = 10002
UNITY_ADDRESS = (HOST, UNITY_PORT)
unity_socket.bind(UNITY_ADDRESS)
	
while True:
	data,addr = unity_socket.recvfrom(4096)
	print(data)
