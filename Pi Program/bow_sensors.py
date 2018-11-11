import socket
import threading
import time
from IMU import berryIMU

def socket_create():
	##Creating UDP socket to send sensor data to server
	global sensor_socket
	sensor_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def data_collect():
	##Sending signals through Pi socket
	HOST = "192.168.1.230"
	PORT = 10000
	ADDRESS = (HOST, PORT)
	##Start sequence to establish connection
	for _ in range(3):
		sensor_socket.sendto("connect".encode(), ADDRESS)
	##Send sensor data until stop/start signal received
	##Keep listening until program closed
	berryIMU.collect(sensor_socket, ADDRESS, signal)
		
def get_signal():
	##Grabs cue from Unity to start or stop taking sensor data
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
	##Generate signal
	global signal
	signal = threading.Event()
	signal.clear()
	##Define threads
	sendDataThread = threading.Thread(target = data_collect)
	getSignalThread = threading.Thread(target = get_signal)
	##Kill threads when main thread dies
	sendDataThread.daemon = True
	getSignalThread.daemon = True
	##Start threads
	sendDataThread.start()
	getSignalThread.start()
	while True:
		time.sleep(0.01)

if __name__ == "__main__":
	main()