import socket
import cv2

# Bilgisayarınızın IP adresi ve portu
SERVER_IP = "192.168.7.48"
SERVER_PORT = 9999

# Socket oluşturma
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
client_socket.connect((SERVER_IP, SERVER_PORT))

# VideoCapture ile kameradan görüntü alıyoruz
cap = cv2.VideoCapture(0)

try:
    while True:
        # Kamera çerçevesi oku
        ret, frame = cap.read()
        if not ret:
            print("Kamera çerçevesi alınamadı.")
            break
        
        # Görüntüyü sıkıştır ve gönder
        _, buffer = cv2.imencode('.jpg', frame)
        message = buffer.tobytes()
        
        # Paket boyutunu gönder
        client_socket.sendall(len(message).to_bytes(4, byteorder='big'))
        
        # Görüntü verisini gönder
        client_socket.sendall(message)
finally:
    cap.release()
    client_socket.close()
