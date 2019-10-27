"""
The DNS record updater server (which implements dynamic dns)!
It takes runs a python server which does 3 things:
	1. Gets a DNS change request from the user, after verifying the user's identity using TLS
	2. Sends the user's DNS change request to AWS.
	3. Notifies the user on the status of their DNS change request.
"""
import socket
import ssl
import subprocess

# context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
# context.load_cert_chain(certfile="cert.pem")

server_address = ('0.0.0.0', 50)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
    print('Server listening on %s:%s' % server_address)
    sock.bind(server_address)
    sock.listen(5)
    while True:
        #Wait for a connection
        connection, client_address = sock.accept()
    	# sslsoc = context.wrap_socket(newsocket, server_side=True)
    	# request = sslsoc.read()
    	# print(request)
        print('Received connection from', client_address)
        connection.sendall(b"You have successfully authenticated. Type your new IP Address: ")
        # Receive the data
        while True:
            data = connection.recv(1024)
            if not data:
                break
            else:
                print ('Received "%s"' % data.decode())
        # Clean up the connection
        connection.close()

ip_address = "4.4.4.4"
update_string_json = """{
    "HostedZoneId": "Z7B5GAEZJQY49",
    "ChangeBatch": {
        "Comment": "Test - batch",
        "Changes": [
            {
                "Action": "UPSERT",
                "ResourceRecordSet": {
                    "Name": "nicky.domcc3.com",
                    "Type": "A",
                    "TTL": 300,
                  "ResourceRecords": [
                    {
                      "Value": "%s"
                    }
                  ]
                }
            }
        ]
    }
}""" % ip_address
# change_id = "/change/CWJXCGIWWEQT8"

update_command = "aws route53 change-resource-record-sets --cli-input-json '{}'".format(update_string_json)
# get_status_command = "aws route53 get-change --id {}".format(change_id)

print(update_command)

#Actually update the AWS record
# subprocess.call(update_command, shell=True) #might need to verify there is no shell injection
