import socket

class Socket(object):

    def sendRequestToServer():
        server_address = ('localhost', 50)
        # Create a TCP/IP socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
            print('connecting to %s port %s' % server_address)
            sock.connect(server_address)
            
            # Send data and look for the response
            authKey = 'AhwkreWoZOwke9Kwlepq'
            print('Sending %s' % authKey)
            sock.sendall(str.encode(authKey))

            data = sock.recv(1024)
            print('Received', repr(data.decode()))
            sock.close()