import socket

##Creating UDP socket to receive sensor data
sensor_data_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

##Binding sensor data socket to IP address
HOST = "172.29.68.61"
SENSOR_DATA_PORT = 10000
SENSOR_DATA_ADDRESS = (HOST, SENSOR_DATA_PORT)
sensor_data_socket.bind(SENSOR_DATA_ADDRESS)


while True:
	##Receiving sensor data from Pi
	sensor_data_socket.sendto("send", SENSOR_DATA_ADDRESS)
	data,addr = sensor_data_socket.recvfrom(4096)
	print (data.decode())
	
	
	
	
	##Data parsing can be done here
	
	##Possibly collect camera data
	##Send sensor data to Unity