import socket
import config
from function.response import *

#Get request from client
def getRequest(client):
	request = ''
	client.settimeout(1)

	try:
		#receive request
		request = client.recv(1024).decode()
		while (request):
			request += client.recv(1024).decode()
	except socket.timeout:
		#if timedout
		if not request:
			print("-------------------\n [SERVER]\n No request from client")
	finally:
		#parse the request for better using
		return RequestParse(request)

class RequestParse:
	def __init__(self, request):

		requestArray = request.split("\n")
		if request == "":
			self.empty = True	#if there is no request content
		else:
			self.empty = False
			self.method = requestArray[0].split(" ")[0]		#get method
			self.path = requestArray[0].split(" ")[1]		#get path
			self.content = requestArray[-1]					#get request content

#POST Method Parser
def postMethod(client, request):
	#scan login content or return info.html or return 404.html
	if(request.path in ['/info.html?','/info.html'] and request.content == "Username=%s&Password=%s"%(config.username,config.password)):
		client.sendall("HTTP/1.1 301 MOVED PERMANENTLY\nLOCATION: /info.html\n".encode('utf-8'))
		client.sendall(Response("/html/info.html").makeResponse())
		return
	else:
		client.sendall("HTTP/1.1 301 MOVED PERMANENTLY\nLOCATION: /404.html\n".encode('utf-8'))
		client.sendall(Response("/html/404.html").makeResponse())
		return


#GET method parser
def getMethod(client, request):

	#if not "GET" method, abort 
	if request.method != 'GET':
		return
	
	#input the file path to send to client
	client.sendall(Response(request.path).makeResponse())
	print(f"-------------------\n [SEND RESPONSE]\n Package for {Response(request.path).locOf_file} sent")