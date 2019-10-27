"""
The DNS record updater server (which implements dynamic dns)!
It takes runs a python server which does 3 things:
	1. Gets a DNS change request from the user, after verifying the user's identity using TLS
	2. Sends the user's DNS change request to AWS.
	3. Notifies the user on the status of their DNS change request.
"""

from services.socket import Socket

Socket().openSocketServer()