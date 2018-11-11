using System;
using System.Net;
using System.Net.Sockets;
using System.Text;

class Program
{
    void sendSignal(string signal)
    {
        //Signal must be "collect" or "stop"

    }
    static void Main(string[] args)
    {
        //Creates socket and endpoint
        Socket unity_socket = new Socket(AddressFamily.InterNetwork, SocketType.Dgram, ProtocolType.Udp);

        IPAddress broadcast = IPAddress.Parse("172.29.69.39");
        IPEndPoint ep = new IPEndPoint(broadcast, 10002);
        /*Trigger Signal Here*/
        while (true) {
            byte[] sendbuf = Encoding.ASCII.GetBytes("testdata");
            unity_socket.SendTo(sendbuf, ep);
            Console.WriteLine("Message sent to the broadcast address");
        }
    }
}