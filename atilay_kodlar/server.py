import  cv2, imutils, socket
import numpy as np
import time
import base64
import netifaces as ni
import os
time.sleep(3)

ip = ni.ifaddresses('usb0')[ni.AF_INET][0]['addr']
dosya=open("/home/rasp/atilay/ip","w")
dosya.write(ip)
dosya.close()
os.system("python3 /home/rasp/atilay/istemci.py &")


BUFF_SIZE = 65536
server_socket=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE)
host_name=socket.gethostname()
host_ip = ip #"192.168.100.2"#socket.gethostbyname(host_name)
port = 9999
socket_address = (host_ip,port)
server_socket.bind(socket_address)
print("listening at:",socket_address)

vid = cv2.VideoCapture(0)
fps,st,frames_to_count,cnt = (0,0,20,0)


while True:

	msg,client_addr = server_socket.recvfrom(BUFF_SIZE)
	print("GOT connection from ",client_addr)	
	#print(msg)

	WIDTH=640
	while(vid.isOpened()):
		_,frame=vid.read()
		#frame = imutils.resize(frame,width=WIDTH)
		frame=cv2.resize(frame,(400,400))
		encoded,buffer = cv2.imencode(".jpg",frame,[cv2.IMWRITE_JPEG_QUALITY,80])
		message = base64.b64encode(buffer)
		server_socket.sendto(message,client_addr)
		packet,_ =  server_socket.recvfrom(BUFF_SIZE)
		if packet[0]!=110:
			x=""
			y=""
			x_state=True
			y_state=False
			carpan=1
			for indis,s in enumerate(packet):
				if s!=32 and x_state:
					if s==45 and indis==0:
						carpan=-1
					else:
						x+=str(s-48)
				if s==32:
					x_state=False
					y_state=True
					x=int(x)*carpan
					carpan=1
				if s!=32 and y_state:
					if s==45:
						carpan=-1
					else:
						y+=str(s-48)
			y=int(y)*carpan
			dosya=open("/home/rasp/atilay/x","w")
			dosya.write(str(x))
			dosya.close()
			dosya=open("/home/rasp/atilay/y","w")
			dosya.write(str(y))
			dosya.close()
			print("x :",x," y :",y)			
			
			
		key = cv2.waitKey(1) & 0xFF
		if key == ord("q"):
			server_socket.close()
			break
