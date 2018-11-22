import socket
import threading
import os
import signal
import time
import Queue
import fcntl
import struct
import speech_processing
import json

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])
	
def socket_create():
	##Creating UDP socket to receive sensor data
	global sensor_data_socket 
	sensor_data_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	
	##Creating UDP socket to communicate with Unity
	global unity_socket
	unity_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	##Binding sensor data socket to IP address
	##HOST = "172.29.70.132" alternative
	HOST = get_ip_address('enp0s3')
	SENSOR_DATA_PORT = 10000
	SENSOR_DATA_ADDRESS = (HOST, SENSOR_DATA_PORT)
	sensor_data_socket.bind(SENSOR_DATA_ADDRESS)
	
	##Binding Unity socket to IP address
	UNITY_PORT = 10002
	UNITY_ADDRESS = (HOST, UNITY_PORT)
	unity_socket.bind(UNITY_ADDRESS)
	
def client_communicate():
	while True:
	##Receiving sensor data from Pi
		data,addr = sensor_data_socket.recvfrom(4096)
		##Send received data to Unity over socket after adding in Speech Recognition data
		if unityClientAddress is not None:
			
			print (data.decode()) ##Print the data for debugging purposes
			unity_socket.sendto(data, unityClientAddress)
		if not signal.is_set():
			##Send stop signal if no more data is needed now
			##Sending 3 to be safe
			for _ in range(3):
				sensor_data_socket.sendto("stop".encode(), addr)
		signal.wait()
		##Send start signal to collect more data
		for _ in range(3):
			sensor_data_socket.sendto("collect".encode(), addr)
			
def unity_communicate():
	global unityClientAddress
	unityClientAddress = None
	while True:
		##Get signal from Unity
		data,addr = unity_socket.recvfrom(4096)
		unityClientAddress = addr
		if data.decode() == "collect":
			signal.set()
		elif data.decode() == "stop":
			signal.clear()
	
	
def camera_communication():
	##Take camera data here
	print("test")
	
def speech_recognition():
	##Instantiate microphone and recognizer
	speech_processing.speech_initialize()
	##Do speech recognition here
	speech_processing.recognize()
	print(speech_processing.speechValue)
	
def main():
	##Create sockets
	socket_create()
	##Create signal
	global signal
	signal = threading.Event()
	signal.clear()
	##Define threads
	clientThread = threading.Thread(target = client_communicate)
	unityThread = threading.Thread(target = unity_communicate)
	speechRecognitionThread = threading.Thread(target = speech_recognition)
	##Close threads when main thread ends
	clientThread.daemon = True
	unityThread.daemon = True
	speechRecognitionThread.daemon = True
	##Start threads
	clientThread.start()
	unityThread.start()
	speechRecognitionThread.start()
	while True:
		time.sleep(0.01)
		
if __name__ == "__main__":
	main()