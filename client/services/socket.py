import os, socket, ssl

class Socket():

    def sendRequestToServer(self):
        hostname = 'domcc3.com'
        port = 50
        context = self.__loadCertContext()

        # Create a TCP/IP socket, and then open it as a secure (TLS) socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            print('Connecting to %s on port %s.' % (hostname, port))
            ssock.connect((hostname, port))
            # Send data and look for the response
            authKey = 'AhwkreWoZOwke9Kwlepq'
            print('Sending %s' % authKey)
            ssock.sendall(str.encode(authKey))

            data = ssock.recv(1024)
            print('Received', repr(data.decode()))
            ssock.close()
    
    def __loadCertContext(self):
        # Set up the client's TLS parameters
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        context.verify_mode = ssl.CERT_REQUIRED
        # Load the server's public key
        context.load_verify_locations("./server.pem")
        return context