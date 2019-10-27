import os, socket, ssl
from services.aws_cli import AwsCli

class Socket: 

    def openSocketServer(self):
        server_address = ('localhost', 50)
        context = self.__loadCertContext()

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind(server_address)
            sock.listen(0)
            print('Server listening on %s:%s' % server_address)
            
            while True: # Always have server waiting for a connection
                client_conn, client_address = sock.accept()
                host = client_address[0]
                print('Connection from', client_address[0])

                with ssl.wrap_socket(client_conn, server_side=True, certfile='server.pem', keyfile='server.key') as ssock:
                    data = ssock.recv(1024)
                    authKey = data.decode()
                    recordSetNameToUpdate = 'nicky.domcc3.com' # TODO: this should come in as a property from data.decode() to make app more generic
                    print('Received authKey: ', authKey)

                    if self.__authenticateClientRequest(authKey):
                        msg = self.__updateAWSResourceRecord(host, recordSetNameToUpdate)
                        ssock.sendall(str.encode(msg))
                    else:
                        ssock.sendall(b'Error: Invalid Auth')
                    
                    ssock.close()
                    
            sock.close()

    def __loadCertContext(self):
        context = ssl.SSLContext(ssl.PROTOCOL_TLS)
        context.verify_mode = ssl.CERT_REQUIRED

        return context

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