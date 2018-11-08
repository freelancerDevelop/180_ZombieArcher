## ZombieArcher

ZombieArcher is a video game designed for UCLA's Capstone Couse EE 180D.

The designers are Sidharth Bambah, Sparsh Gauba, Andrew Juarez, and Mohamed Shatela.


### Main Components:
1) Unity Game
2) Raspberry Pi Sensor Software
3) Python Server

#### How to Run Python Server:
1. Define host IP address
2. Run with:

	```python
	python3 data_collect.py
	```
	
#### How to Run Raspberry Pi Sensor Software:
1. Define server IP address
2. Copy file pi_socket.py to Raspberry Pi and connect necessary hardware (BerryIMU)
3. Run program on Pi with:
	
	```python
	python3 server.py
	```
	
Note: It is **critical** to start server before Pi software to properly initialize
the UDP sockets.

Known Issues
1. Server and Raspberry Pi software cannot be closed with Ctrl-C. Must do a hard shutdown.