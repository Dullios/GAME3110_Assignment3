import socket
import time
from _thread import *

sendToAddress = ()

def ConnectToServer(sock):
    msg = 'connect'
    print("Sending Connection...")
    sock.sendto(bytes(msg, 'utf8'), sendToAddress)

def heartbeat(sock):
    while True:
        msg = 'heartbeat'
        print("Sending Heartbeat...")
        sock.sendto(bytes(msg, 'utf8'), sendToAddress)
        time.sleep(3)

if __name__ == "__main__":
    ipAddress = '52.15.65.92'
    port = 12345
    sendToAddress = (ipAddress, port)

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('', port))
    ConnectToServer(s)
    start_new_thread(heartbeat, (s,))

    while True:
        time.sleep(1)