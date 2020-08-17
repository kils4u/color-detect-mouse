#!/usr/bin/python3
import socket
from PIL import Image
from threading import Thread

old_x = -1;
old_y = -1;
new_x = -1;
new_y = -1;

canTrack = True;

class CreateServer :
	def __init__(self) :
		self.port = 8520

	def Connect(self) :
		global canTrack;
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
									im.close();
									if(canTrack) :
										canTrack = False;
										im = open(file,"rb");
										track = object_track(im);
										track.start();
									break
						im.write(data)
						data = sock.recv(1)
						if(data == b'') :
							break
					i += 1
		except Exception as e:
			print("Error : ",e)



class object_track(Thread) :
	def __init__(self,file) :
		Thread.__init__(self);
		self.file = file;
		self.im = Image.open(file,"r");
		im_hsv = self.im.convert("HSV");
		self.hsv_data = list(im_hsv.getdata());
		self.x_size = self.im.width;
		self.y_size = self.im.height;
		self.x_cor=0;
		self.y_cor=0;
		self.x = -1;
		self.y = -1;
		self.x_start = -1;
		self.x_end = -1;
		self.y_start = -1;
		self.y_end = -1;
		self.area = [];
		for i in range(0,99) :
			self.area.append([]);
			for j in range(0,99) :
				self.area[i].append(0);

	def run(self) :
		global old_x;
		global old_y;
		global new_x;
		global new_y;
		global canTrack;

		for x in self.hsv_data :
			if((((x[1]*360)/255) < 3 and ((x[2]*360)/255) > 99) and ((int((x[0]*360)/255) >= 179 and int((x[0]*360)/255) <= 181) or (int((x[0]*360)/255) >= 299 and int((x[0]*360)/255) <= 301))) :
				self.area[int((100*self.x_cor)/self.x_size)-1][int((100*self.y_cor)/self.y_size)-1] += 1;
			self.x_cor += 1;
			if(self.x_cor == self.x_size) :
				self.y_cor += 1;
				self.x_cor = 0;
		for i in range(0,99) :
			for j in range(0,99) :
				if(self.area[i][j] > 0) :
					if(self.y_start == -1) :
						self.y_start = i;
					else :
						self.y_end = i;
					if(self.x_start == -1 or self.x_start > j) :
						self.x_start = j;
						k = 98;
						while (k > j):
							if(self.area[i][k] > 0) :
								if(self.x_end < k) :
									self.x_end = k;
									break;
							k -= 1;
						break;

		new_x = int((self.x_start + self.x_end) / 2);
		new_y = int((self.y_start + self.y_end) / 2);

		print("new_x = " + str(new_x) + "  new_y = " + str(new_y));
		canTrack = True;


a = CreateServer()
a.Connect()