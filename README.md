#DNS Record Updater

The client has a dynamic IP address, but we still want to map it to a DNS record. Therefore, the client sends IP address advertisements to a server with a static IP address, which subsequently updates the AWS Route 53 DNS entry. The entire project uses python3.

##Working notes
-on the server:
	-API endpoint for client
		-receiving advertisement/API call
			-IP address
			-authentication key
		-verify the key
	-updating record set
		-authenticate to amazon
			-awscli
		-create XML structure
		-send the info through API call
		-receive confirmation
	-confirmation to client
		-update failed or succeeded

-structure of application
	-port
	-protocol - possibly use https, ftps, scp, or generic tls
	-keys/certificates