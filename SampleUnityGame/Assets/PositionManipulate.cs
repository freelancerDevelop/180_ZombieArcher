using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;
using System.Text;
using System.Net;
using System.Net.Sockets;
using Newtonsoft.Json.Linq;

public class PositionManipulate : MonoBehaviour {
	//Variable Definitions
	private string HOST = "172.29.70.132"; //Must change this each time
	int PORT = 10002;
	UdpClient unity_socket;
	IPEndPoint ep;
	
	private void sendSignal(string signal) {
		Byte[] message = Encoding.ASCII.GetBytes(signal);
		//Send signal three times to be safe
		for (int i = 0; i < 3; i++) {
			unity_socket.Send(message, message.Length);
			Debug.Log("Sent Signal");
		}
	}
	
	private void createSocket() {
		unity_socket = new UdpClient();
		unity_socket.Connect(IPAddress.Parse(HOST), PORT);
		ep = new IPEndPoint(IPAddress.Parse(HOST), PORT);
	}
	
	private string getResponse() {
		Byte[] response = unity_socket.Receive(ref ep);
		string responseAsString = System.Text.Encoding.ASCII.GetString(response);
		return responseAsString;
	}
	
	private void moveBow(JObject coordinates) {
		float smooth = 5.0f;
		float tiltAngle = 60.0f;
		// Smoothly tilts a transform towards a target rotation.
        float tiltAroundX = coordinates["x-angle"].Value<float>();
        float tiltAroundY = coordinates["y-angle"].Value<float>();
		Debug.Log(tiltAroundX);
        Quaternion target = Quaternion.Euler(tiltAroundX, tiltAroundY, 0);

        // Dampen towards the target rotation
        transform.rotation = Quaternion.Slerp(transform.rotation, target,  Time.deltaTime * smooth);
	}
	

	// Use this for initialization
	void Start () {
		//Create socket
		createSocket();
		sendSignal("collect");
	}
	
	// Update is called once per frame
	void Update () {
		string responseAsString = getResponse();
		JObject coordinates = JObject.Parse(responseAsString);
		moveBow(coordinates);
	}
}
