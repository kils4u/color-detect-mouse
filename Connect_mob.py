#!/usr/bin/python3
import socket

class CreateServer :
	def __init__(self) :
		self.port = 8520

	def Connect(self) :
		try :
			serverSock = socket.socket()
			serverSock.bind(("192.168.0.101",self.port))
			serverSock.listen(5)
			print("on listen")
			sock,addr = serverSock.accept()
			print("got Connect")
			i = 1
			while 1:
				data = sock.recv(1)
				if(data == b'\xff') :
					file = "tmp_" + str(i) + ".jpg"
					im = open(file,"wb")
					count = 0
					while (data != b'') :
						if(data == b'\xff') :
							data += sock.recv(1)
							if(data == b'\xff\xd8') :
								count += 1
								print("data : ", data , "  count : ",count)
							elif(data == b'\xff\xd9') :
								count -= 1
								print("data : ", data , "  count : ",count)
								if(not count) :
									print("image close")
									im.write(data)
									im.close()
									break
						im.write(data)
						data = sock.recv(1)
						if(data == b'') :
							break
					i += 1
		except Exception as e:
			print("Error : ",e)

a = CreateServer()
a.Connect()