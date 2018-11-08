import socket
import threading
import sys

def socket_create():
	##Creating UDP socket to receive sensor data
	global sensor_data_socket 
	sensor_data_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	
	##Creating UDP socket to communicate with Unity
	global unity_socket
	unity_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	##Binding sensor data socket to IP address
	HOST = "172.29.68.81"; 
	SENSOR_DATA_PORT = 10000
	SENSOR_DATA_ADDRESS = (HOST, SENSOR_DATA_PORT)
	sensor_data_socket.bind(SENSOR_DATA_ADDRESS)
	
	##Binding Unity socket to IP address
	HOST = "172.29.68.81"; 
	UNITY_PORT = 10002
	UNITY_ADDRESS = (HOST, UNITY_PORT)
	unity_socket.bind(UNITY_ADDRESS)
	
def pi_communicate():
	while True:
	##Receiving sensor data from Pi
		data,addr = sensor_data_socket.recvfrom(4096)
		##Data parsing can be done here
		print (data.decode())
		if not signal.is_set():
			##Send stop signal if no more data is needed now
			##Sending 3 to be safe
			for _ in range(3):
				sensor_data_socket.sendto("stop", addr)
		signal.wait()
		if signal.is_set():
			##Send start signal to collect more data
			for _ in range(3):
				sensor_data_socket.sendto("collect", addr)
	
	
def unity_communicate():
	while True:
		##Get signal from Unity
		data,addr = unity_socket.recvfrom(4096)
		if data.decode() == "collect":
			signal.set()
		elif data.decode() == "stop":
			signal.clear()
	##Send sensor data to Unity
	
def camera_communication():
	##Take camera data here
	print("test")
	
def main():
	socket_create()
	global signal
	signal = threading.Event()
	signal.clear()
	##Define threads
	piThread = threading.Thread(target = pi_communicate)
	unityThread = threading.Thread(target = unity_communicate)
	##Start threads
	piThread.start()
	unityThread.start()
	
	
if __name__ == "__main__":
	main()