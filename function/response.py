import config
from function.renderfile import *

class Response:
	def __init__(self, path):

		self.file_buff = ''
		self.status = 200

		#if case below define some files to transfer normally

		# If you asked why also have ? symbol after the path, ex: /index.html?. 
		# Just because I added some "back" button to some page to return to last page and when click it
		# Client request path "/index.html?" not "/index.html"

		if path in ['/','/index.html','/index.html?']: #index here
			path = config.get_index
		elif path in ['/info.html','/info.html?']: #info page after login
			path = config.get_info
		elif path in ['/404.html','/404.html?']: #error page
			path = config.get_404
			self.status = 404							# change status code
		elif path in ['/files.html','/files.html?']: #files to download
			path = '/files.html'
			self.file_buff = renderfile('./dat').make_html_files()
		else:			#this path will check if some data request from client don't have /dat path, result is return to /dat/filehere
			if '/dat' not in path:
				path = '/dat' + path

		
		# Split path into array to get file name and file type
		self.locOf_file = path							
		file_info = path.split('/')[-1].split('.')		
		self.file_type = file_info[-1]		# Get file type from array


		#try to open file that provide above, if the file doesn't exist, return status code 404
		try:
			if(self.file_buff == ''):
				self.buffer = open(path[1:].replace("%20"," "),"rb")				# Get data buffer from file
		except:
			self.status = 404
			self.buffer = open(config.get_404[1:],"rb")

		#make header
		header = ""	
		header += "HTTP/1.1 404 NOT FOUND\n" if(self.status == 404) else "HTTP/1.1 200 OK\n"
		if self.file_type in ["html","txt"]:
			header += 'Content-Type: Text/%s\n'%self.file_type
		else:
			if self.file_type in ["png","ico","jpg"]:
				header += 'Content-Type: Image/%s\n'%self.file_type
			else:
				header += 'Content-Type: multipart/form-data\r\n'
		self.header = header
		print(f'-------------------\n [HEADER RESPONSE]\n {header}')

	def makeResponse(self):

		if(self.file_buff != ''):
			content = self.file_buff.encode('utf-8')
		else:
			content = self.buffer.read()

		if len(content) < config.buffer_size:

			self.header += "Content-Length: %d\r\n\r\n"%len(content)
			header = self.header.encode('utf-8') + content + "\r\n".encode('utf-8')
			print(f"-------------------\n [SEND RESPONSE]\n Transfer {self.locOf_file} with normal mode")
			return header
		else:
			self.header += "Transfer-Encoding: chunked\r\n\r\n"

		#render chunk
			BUFF_SIZE = config.buffer_size
			content = "".encode('utf-8')
			self.buffer.seek(0)
			L = self.buffer.read(BUFF_SIZE)
			while(len(L) == BUFF_SIZE):
				size = len(L)
				content += ("{:X}\r\n".format(size)).encode('utf-8')
				content += L 
				content += "\r\n".encode()
				L = self.buffer.read(BUFF_SIZE)
			size = len(L)
			content += ("{:X}\r\n".format(size)).encode('utf-8')
			content += L
			content += "\r\n0".encode('utf-8')
			self.chunkedcontent = content

		#send chunk
			header = self.header.encode('utf-8') + self.chunkedcontent + "\r\n\r\n".encode('utf-8')
			print(f"-------------------\n [SEND RESPONSE]\n Transfer {self.locOf_file} with chunked transfer encoding mode")
			return header
