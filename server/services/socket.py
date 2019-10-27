import socket
# import ssl
from services.aws_cli import AwsCli

class Socket: 

    def openSocketServer(self):
        server_address = ('localhost', 50)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            print('Server listening on %s:%s' % server_address)
            # TODO: build in SSL connection
                # context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
                # context.load_cert_chain(certfile="cert.pem")
                # sslsoc = context.wrap_socket(newsocket, server_side=True)
                # request = sslsoc.read()
            sock.bind(server_address)
            sock.listen(0)
            
            while True: # Always have server waiting for a connection
                connection, client_address = sock.accept()
                host = client_address[0]
                print('Connection from', client_address[0])

                data = connection.recv(1024)
                authKey = data.decode()
                recordSetNameToUpdate = 'nicky.domcc3.com' # TODO: this should come in as a property from data.decode() to make app more generic
                print('Received authKey: ', authKey)
                if self.__authenticateClientRequest(authKey):
                    msg = self.__updateAWSResourceRecord(host, recordSetNameToUpdate)
                    connection.sendall(str.encode(msg))
                else:
                    connection.sendall(b'Error: Invalid Auth')
                
                connection.close()

    def __authenticateClientRequest(self, authKey):
        # TODO: verify client's public key to server's private key
        return True

    def __updateAWSResourceRecord(self, host, recordSetName):
        currentResourceRecordValue = AwsCli.getRecorceRecordValueByRecordSetName(recordSetName)

        if currentResourceRecordValue != host:
            resp = AwsCli.updateResourceRecord(host)
            if resp == True:
                return 'Resource Record has been successfully set to %s' % host
            else: 
                return 'Error: Unable to set Resource Record to %s' % host
        else:
            return 'Resoruce Record IP already set to %s' % host