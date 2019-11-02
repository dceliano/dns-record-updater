import os, socket, ssl
from services.aws_cli import AwsCli

class Socket:
    def openSocketServer(self):
        server_address = ('0.0.0.0', 50)
        context = self.__loadCertContext()

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind(server_address)
            sock.listen(0)
            print('Server listening on %s:%s' % server_address)
            
            while True: # Always have the server waiting for a connection
                client_conn, client_address = sock.accept()
                host = client_address[0]
                print("Client connected: {}:{}".format(host, client_address[1]))

                with context.wrap_socket(client_conn, server_side=True) as ssock:
                    # We only reach here if the mutual authentication succeeded.
                    print("TLS connection established.")
                    data = ssock.recv(1024)
                    authKey = data.decode()
                    recordSetNameToUpdate = 'nicky.domcc3.com' # TODO: this should come in as a property from data.decode() to make app more generic
                    print('Received Request:', authKey)
                    msg = self.__updateAWSResourceRecord(host, recordSetNameToUpdate)
                    ssock.sendall(str.encode(msg))
                    ssock.close()
            sock.close()

    def __loadCertContext(self):
        # Set up the server's TLS parameters
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.verify_mode = ssl.CERT_REQUIRED
        context.load_cert_chain(certfile='../server.pem', keyfile='server.key')
        # Load the client's public key
        context.load_verify_locations(cafile='../client.pem')
        return context

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