import os, socket, ssl

class Socket():

    def sendRequestToServer(self):
        hostname = 'localhost'
        port = 50
        context = self.__loadCertContext()

        # Create a TCP/IP socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
            print('connecting to %s port %s' % (hostname, port))
            sock.connect((hostname, port))

            with context.wrap_socket(sock, server_hostname=hostname, server_side=False) as ssock:
                # Send data and look for the response
                authKey = 'AhwkreWoZOwke9Kwlepq'
                print('Sending %s' % authKey)
                ssock.sendall(str.encode(authKey))

                data = ssock.recv(1024)
                print('Received', repr(data.decode()))
                ssock.close()
                sock.close()
    
    def __loadCertContext(self):
        context = ssl.SSLContext(ssl.PROTOCOL_TLS)
        context.verify_mode = ssl.CERT_REQUIRED
        context.load_verify_locations(os.path.abspath(os.path.join(__file__ ,"../../../server/server.pem")))
        context.load_cert_chain('client.pem', 'client.key')

        return context