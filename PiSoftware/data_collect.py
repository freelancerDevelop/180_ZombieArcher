import socket
import threading
import time

def socket_create():
	##Creating UDP socket to send sensor data to server
	global sensor_socket
	sensor_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def data_collect():
	##Sending signals through Pi socket
	HOST = "172.29.68.81"
	PORT = 10000
	ADDRESS = (HOST, PORT)
	##Start sequence to establish connection
	for _ in range(3):
		sensor_socket.sendto("connect", ADDRESS)
	##Send sensor data until stop/start signal received
	##Keep listening until program closed
	while True:
		signal.wait() ## Holds here until start signal received
		if signal.is_set():
			sensor_socket.sendto("sensor data", ADDRESS)
		
def get_signal():
	##Grabs cue from Unity to start or stop taking sensor data
	global sensor_socket
	global signal
	while True:
		data,addr = sensor_socket.recvfrom(4096)
		if data == "collect":
			signal.set()
		elif data == "stop":
			signal.clear()
		print(data)
		data = None
		
def main():
	socket_create()
	global signal
	signal = threading.Event()
	signal.clear()
	sendDataThread = threading.Thread(target = data_collect)
	getSignalThread = threading.Thread(target = get_signal)
	sendDataThread.start()
	getSignalThread.start()
	
if __name__ == "__main__":
	main()