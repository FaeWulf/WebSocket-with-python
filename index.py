# I know my code stuff suck :), my only purpose to make it "suck" is to avoid spoon-feeding
# you will have to search and research a hell lot :). Thank me later...

import socket
import config
from function.MethodParse import *

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

server.bind((config.host, config.port))
server.listen(5)
print("-------------------\n [SERVER]\n Listening on: %s:%d"%(config.host,config.port))

while 1:

	#Server things
	(client, address) = server.accept()

	print(f"-------------------\n [SERVER]\n {address} sent request to server.")

	#Get request
	request = getRequest(client)

	if not request.empty: 
		print(f"-------------------\n [LISTENED REQUEST]\n Request catched: %s with %s has content %s\n"%(request.method, request.path, request.content))
		if request.method == "POST":
			postMethod(client, request)
		else:
			getMethod(client, request)

	# shutdown, do not client.close()
	client.shutdown(socket.SHUT_RD)
	print("\n--------[Request done]--------\n\n")
	
client.close()
