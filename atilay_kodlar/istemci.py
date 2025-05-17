import time
def gonder(g):

	import time
	import socket

	HOST = '192.168.100.2'  # Coral'ın IP adresi
	PORT = 9990  # Sunucu tarafındaki port numarası

	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.connect((HOST, PORT))
		with open('/home/rasp/atilay/'+g, 'rb') as f:
			data = f.read()
			s.sendall(data)
			print('Dosya başarıyla gönderildi.')
			s.close()

for i in range(2):
	time.sleep(2)
	if i==0:
		gonder(g="ip")
	if i==1:
		gonder(g="state")
