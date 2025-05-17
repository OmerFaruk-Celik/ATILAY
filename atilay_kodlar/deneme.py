import cv2
import numpy as np
import socket
from atilay import atilay
from time import sleep

# Motor kontrol ayarları
master = atilay.set(0)
atilay.arm(master)

# Sunucu bağlantı bilgileri
SERVER_IP = "192.168.7.45"
SERVER_PORT = 9999

def fire():
    print("fired")

def detect_squares_and_circles(image, detected_circles):
    # Kareleri tespit et
    detect_squares(image)
    
    # Çemberleri çerçeveye al
    center_x, center_y = image.shape[1] // 2, image.shape[0] // 2
    radius_small, radius_large = 50, 100
    draw_circles(image, center_x, center_y, radius_small, radius_large, detected_circles)

def detect_squares(image, canny_threshold1=50, canny_threshold2=150, blur_kernel=(5, 5), approx_epsilon=0.02):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, blur_kernel, 0)
    edges = cv2.Canny(blurred, canny_threshold1, canny_threshold2)

    try:
        contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    except ValueError:
        _, contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, approx_epsilon * cv2.arcLength(cnt, True), True)
        if len(approx) == 4 and cv2.isContourConvex(approx):
            cv2.drawContours(image, [approx], 0, (0, 255, 0), 2)
            cv2.putText(image, "Square", (approx[0][0][0], approx[0][0][1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

def draw_circles(image, center_x, center_y, radius_small, radius_large, detected_circles):
    # Küçük ve büyük daire yarıçapları
    kucukDaireYariCap = radius_small
    buyukDaireYariCap = radius_large

    miniDaireYariCap = 20

    # Küçük daireyi çizme
    cv2.circle(image, (center_x, center_y), miniDaireYariCap, (0, 255, 0), 2)

    if detected_circles is not None:
        detected_circles = np.uint16(np.around(detected_circles))
        sorted_circles = sorted(detected_circles[0], key=lambda circle: circle[2])
        x, y, r = sorted_circles[0]
        
        # Koordinat ve yarıçapları tamsayıya çevir
        x = int(x)
        y = int(y)
        r = int(r)
        
        cv2.circle(image, (x, y), r, (255, 0, 0), 2)

        outer_circle_left = (x - r, y)
        outer_circle_right = (x + r, y)

        if radius_small < np.sqrt((outer_circle_left[0] - center_x) ** 2 + (outer_circle_left[1] - center_y) ** 2) < radius_large \
            and radius_small < np.sqrt((outer_circle_right[0] - center_x) ** 2 + (outer_circle_right[1] - center_y) ** 2) < radius_large \
            and radius_small < r < radius_large:
            cv2.putText(image, "ATES!", (center_x - 100, center_y - 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            fire()

        else:
            if y > center_y + buyukDaireYariCap:
                cv2.putText(image, "Asagi Git", (center_x - 100, center_y + 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
                atilay.bat_cik(100, master)  # Yukarı çık
            elif y < center_y - buyukDaireYariCap:
                cv2.putText(image, "Yukari Git", (center_x + 100, center_y + 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
                atilay.bat_cik(50, master)  # Aşağı in
            if x > center_x + buyukDaireYariCap:
                cv2.putText(image, "Saga Git", (center_x + 50, center_y - 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                atilay.yanla(100, master)  # Sağa git
            elif x < center_x - buyukDaireYariCap:
                cv2.putText(image, "Sola Git", (center_x + 50, center_y - 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                atilay.yanla(50, master)  # Sola git
            if r > buyukDaireYariCap:
                cv2.putText(image, "Geri Git", (image.shape[1] - 200, image.shape[0] - 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
                atilay.ileri_geri(50, master)  # Geri git
            elif r < kucukDaireYariCap:
                cv2.putText(image, "Ileri Git", (image.shape[1] - 200, image.shape[0] - 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
                atilay.ileri_geri(100, master)  # İleri git

def process_frame(frame):
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    circles = cv2.HoughCircles(gray_frame, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=10, maxRadius=100)

    detect_squares_and_circles(frame, circles)

    return frame

def main():
    frame_count = 0

    # Socket bağlantısını oluştur
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_IP, SERVER_PORT))

    try:
        cap = cv2.VideoCapture(0)
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            processed_frame = process_frame(frame)

            # Görüntüyü sıkıştır ve boyutunu al
            encoded, buffer = cv2.imencode('.jpg', processed_frame)
            data = np.array(buffer)
            byte_data = data.tobytes()
            length = len(byte_data)
            
            # Paket boyutunu gönder
            client_socket.sendall(length.to_bytes(4, byteorder='big'))

            # Görüntü verisini gönder
            client_socket.sendall(byte_data)

            frame_count += 1

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    finally:
        cap.release()
        client_socket.close()
        cv2.destroyAllWindows()
        atilay.arm(master)
        atilay.sifirla()

if __name__ == "__main__":
    main()
