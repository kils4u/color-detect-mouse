#!/usr/bin/python3
import socket
from PIL import Image
from threading import Thread
from pynput.mouse import Controller;

old_x = -1;
old_y = -1;
new_x = -1;
new_y = -1;

mouse = Controller();

canTrack = True;

class CreateServer :
	def __init__(self) :
		self.port = 8520

	def Connect(self) :
		global canTrack;
		try :
			serverSock = socket.socket()
			serverSock.bind(("192.168.43.138",self.port))
			serverSock.listen(5)
			print("on listen")
			sock,addr = serverSock.accept()
			print("got Connect")
			i = 1
			while 1:
				self.count = 0
				self.data = sock.recv(1)
				if(self.data == b'\xff') :
					file = "tmp.jpg"
					im = open(file,"wb")
					while (self.data != b'') :
						if(self.data == b'\xff') :
							self.data += sock.recv(1)
							if(self.data == b'\xff\xd8') :
								if(self.count !=0 and self.count != 1 ) :
									self.data = "";
									self.data = sock.recv(1);
									continue;
								else :
									self.count += 1
								# print("self.data : ", self.data , "  count : ",self.count)
							elif(self.data == b'\xff\xd9') :
								if(self.count != 2 and self.count != 3) :
									self.data = "";
									self.data = sock.recv(1);
									continue;
								else :
									self.count += 1
								# print("self.data : ", self.data , "  count : ",self.count)
								if(self.count == 4) :
									# print("image close")
									im.write(self.data)
									self.data="";
									im.close();
									if(canTrack) :
										canTrack = False;
										try :
											img = Image.open(file,"r");
											track = object_track(img.convert("HSV"),img.width,img.height);
											track.start();
											img.close();
										except Exception as e :
											print("Error : ",e);
											canTrack = True;
									break
						im.write(self.data)
						self.data="";
						self.data = sock.recv(1)
						if(self.data==b'') :
							break
					i += 1
		except Exception as e:
			print("Error : ",e)



class object_track(Thread) :
	def __init__(self,data,width,height) :
		Thread.__init__(self);
		im_hsv = data;
		self.hsv_data = list(im_hsv.getdata());
		self.x_size = width;
		self.y_size = height;
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

		if(new_x != -1 and new_y != -1) :
			if(old_x != -1 and old_y != -1) :
				diff_x = (new_x - old_x)*11;
				diff_y = (new_y - old_y)*19;
				print("diff_x = " + str(diff_x) + "  diff_y = " + str(diff_y));				
				mouse.move(diff_y, diff_x);
			else :
				old_x = new_x;
				old_y = new_y;
				
		else :
			old_x = -1;
			old_y = -1;

		print("new_x = " + str(new_x) + "  new_y = " + str(new_y));
		canTrack = True;


a = CreateServer()
a.Connect()