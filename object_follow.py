#!/usr/bin/python3

from PIL import Image
from PIL import ImageColor

file = open("kils.jpg","rb");
im = Image.open(file,"r");
im_hsv = im.convert("HSV");
hsv_data = list(im_hsv.getdata());

x_size = im.width;
y_size = im.height;

x_cor=0;
y_cor=0;

x = -1;
y = -1;

x_start = -1;
x_end = -1;

y_start = -1;
y_end = -1;

value = 0;

area = [];

for i in range(0,99) :
	area.append([]);
	for j in range(0,99) :
		area[i].append(0);

for x in hsv_data :
	if((((x[1]*360)/255) < 3 and ((x[2]*360)/255) > 99) and ((int((x[0]*360)/255) >= 179 and int((x[0]*360)/255) <= 181) or (int((x[0]*360)/255) >= 299 and int((x[0]*360)/255) <= 301))) :
		area[int((100*x_cor)/x_size)-1][int((100*y_cor)/y_size)-1] += 1;
	x_cor += 1;
	if(x_cor == x_size) :
		y_cor += 1;
		x_cor = 0;

for i in range(0,99) :
	for j in range(0,99) :
		if(area[i][j] > 0) :
			if(y_start == -1) :
				y_start = i;
			else :
				y_end = i;
			if(x_start == -1 or x_start > j) :
				x_start = j;
				k = 98;
				while (k > j):
					if(area[i][k] > 0) :
						if(x_end < k) :
							x_end = k;
							break;
					k -= 1;
				break;

x = int((x_start + x_end) / 2);
y = int((y_start + y_end) / 2);

print("x = " + str(x) + " y = " + str(y));

area[y][x] = -2;

for i in range(0,99) :
	print(area[i]);