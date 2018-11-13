using System;
using System.Net;
using System.Net.Sockets;
using System.Text;

class Program
{
    void sendSignal(string signal, Socket unity_socket, IPAddress broadcast, IPEndPoint ep)
    {
        //Signal must be "collect" or "stop"
        byte[] sendbuf = Encoding.ASCII.GetBytes(signal);
        //Send the signal three times to be sure
        for (int i = 0; i < 3; i++)
        {
            unity_socket.SendTo(sendbuf, ep);
        }
    }
    static void Main(string[] args)
    {
        //Creates socket and endpoint
        Socket unity_socket = new Socket(AddressFamily.InterNetwork, SocketType.Dgram, ProtocolType.Udp);

        IPAddress broadcast = IPAddress.Parse("192.168.1.230");
        IPEndPoint ep = new IPEndPoint(broadcast, 10002);
    }
}