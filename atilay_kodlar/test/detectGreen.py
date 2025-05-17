import cv2
import numpy as np
from atilay import atilay
master=atilay.set(0)
atilay.arm(master)


def fire():
    atilay.ates()
    print("ATEŞ!")

def bat_cikF_yukari():
    atilay.bat_cik(100,master)
    #print("Yukarı git!")

def bat_cikF_asagi():
    atilay.bat_cik(60,master)
    #print("Aşağı git!")

def yanla_sola():
    atilay.yanla(90,master)
    #print("Sola git!")

def yanla_saga():
    atilay.yanla(60,master)
    #print("Sağa git!")

def ileri():
    atilay.ileri_geri(100,master)
    #print("İleri git!")

def geri():
    #atilay.ileri_geri(65,master)
    print("Geri git!")

def draw_ates_text(image, center_x, center_y):
    cv2.putText(image, "ATES!", (center_x - 100, center_y - 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    fire()

def draw_movement_text(image, x_diff, y_diff, center_x, center_y, radius_small, radius_large):
    if abs(x_diff) < radius_small and abs(y_diff) < radius_small:
        draw_ates_text(image, center_x, center_y)
    else:
        if y_diff > radius_large:
            cv2.putText(image, "Yukarı Git", (center_x - 100, center_y + 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
            bat_cikF_asagi()
        elif y_diff < -radius_large:
            cv2.putText(image, "Aşağı Git", (center_x + 100, center_y + 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
            bat_cikF_yukari()

        if x_diff > radius_large:
            cv2.putText(image, "Sağa Git", (center_x + 50, center_y - 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            yanla_saga()
        elif x_diff < -radius_large:
            cv2.putText(image, "Sola Git", (center_x + 50, center_y - 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            yanla_sola()
        
        # İleri veya geri gitme talimatı ekleme
        if abs(x_diff) > radius_large or abs(y_diff) > radius_large:
            cv2.putText(image, "Geri Git", (image.shape[1] - 200, image.shape[0] - 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
            geri()
        elif abs(x_diff) < radius_small and abs(y_diff) < radius_small:
            cv2.putText(image, "İleri Git", (image.shape[1] - 200, image.shape[0] - 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
            ileri()

def send_frame_to_socket(frame, ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    result, frame = cv2.imencode('.jpg', frame)
    data = frame.tobytes()
    sock.sendall(data)
    sock.close()

# Kameradan görüntü yakalama ve işleme
webcam = cv2.VideoCapture(0)

if not webcam.isOpened():
    print("Kameraya bağlanılamadı.")
    exit()

atilay.kilitle()
while True:
    alt=atilay.lidar_alt()
    on=atilay.lidar_on()
    sol=atilay.lidar_sol()
    gx,gy,gz=atilay.hareket()
    ret, frame = webcam.read()
    print(gz)
    if not ret:
        print("Görüntü alınamadı.")
        break
    if sol <30:
        atilay.yanla(100,master)

    if sol>560:
        atilay.yanla(40,master)

    if on<50:
        atilay.sag_sol(90,master)


    if alt <20:
        atilay.bat_cik(95,master)


    if alt>130:
        atilay.bat_cik(70,master)
 
    # Kameradan gelen görüntüyü yatayda ters çevirme (ayna etkisi)
    frame = cv2.flip(frame, 1)

    # Ekranın merkezini ve aralıkları belirleme
    height, width = frame.shape[:2]
    center_x = width // 2
    center_y = height // 2
    radius_small = 50
    radius_large = 100

    # Renk filtresi için HSV renk uzayına dönüştürme
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_green = np.array([28, 93, 0], dtype=np.uint8)  # Koyu yeşil alt sınır
    upper_green = np.array([96, 255, 143], dtype=np.uint8)  # Koyu yeşil üst sınır
    mask = cv2.inRange(hsv, lower_green, upper_green)

    # Maske ve median blur uygulama
    masked_frame = cv2.bitwise_and(frame, frame, mask=mask)
    medianBlr = cv2.medianBlur(mask, 21)
    medianBlrOrg = cv2.medianBlur(frame, 21)

    # Kontur algılama
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        # Eşik değeri
        min_area = 500  # Minimum alan eşiği

        for contour in contours:
            area = cv2.contourArea(contour)
            if area > min_area:
                # En büyük konturu seçme
                largest_contour = contour
                M = cv2.moments(largest_contour)
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])
                else:
                    cx, cy = 0, 0

                cv2.circle(frame, (cx, cy), 5, (0, 255, 255), -1)  # Kontur merkezini çiz

                # Tolerans aralığı
                tolerance = 20

                # Yeşil alan merkezi kontrolü
                x_diff = cx - center_x
                y_diff = cy - center_y
                draw_movement_text(frame, x_diff, y_diff, center_x, center_y, radius_small, radius_large)

                # Merkez koordinatlarını dosyalara yazma
                with open('/home/rasp/atilay/x', 'w') as f_x, open('/home/rasp/atilay/y', 'w') as f_y:
                    f_x.write(str(cx))
                    f_y.write(str(cy))

    # Görüntüyü belirtilen IP adresine ve porta gönderme
    #send_frame_to_socket(frame, '192.168.7.48', 9999)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

webcam.release()
cv2.destroyAllWindows()
