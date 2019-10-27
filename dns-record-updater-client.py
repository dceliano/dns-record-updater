"""
The DNS record updater client, which sends update requests to the server!
"""
import socket
import ssl
import subprocess

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 50)
print('connecting to %s port %s' % server_address)
sock.connect(server_address)

# Send data and look for the response
message = b'4.4.4.4'
print('sending "%s"' % message.decode())
sock.sendall(message)

print('closing socket')
sock.close()