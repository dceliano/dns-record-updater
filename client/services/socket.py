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
            # Send request and look for the response
            request = '(Code for the request to update the DNS record)'
            print('Sending %s' % request)
            ssock.sendall(str.encode(request))
            data = ssock.recv(1024)
            print('Received', repr(data.decode()))
            ssock.close()
    
    def __loadCertContext(self):
        # Set up the client's TLS parameters
        context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile="../server.pem")
        context.load_cert_chain(certfile="../client.pem", keyfile="client.key")
        context.verify_mode = ssl.CERT_REQUIRED
        # Load the server's public key
        context.load_verify_locations('../server.pem')
        return context