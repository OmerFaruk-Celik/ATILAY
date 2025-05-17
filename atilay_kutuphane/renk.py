import cv2
import cvzone
from cvzone.ColorModule import ColorFinder

#cap_dip = cv2.VideoCapture(0)#Dahili kamerayı kullanmak için
dip_cap = cv2.VideoCapture(0)
on_cap = cv2.VideoCapture(1)
renkAraligi = ColorFinder(False)
hsvaralik = {'hmin': 146, 'smin': 141, 'vmin':77,#Kırmızının değer aralığı min ve max şeklinde giriyoruz
           'hmax':179 ,'smax':255, 'vmax':255}

while True:#Bigisayar kamerasından sürekli olarak förüntü alabilmek için    
    
    dosya=open("/home/rasp/atilay/dip_status","r")
    dip_status=dosya.read()
    dosya.close()

    if dip_status=="True":
        ret, bilgisayarKamerasi = dip_cap.read()#Kamerayı oku 20 ms de 1 kare
    else:
        ret, bilgisayarKamerasi = on_cap.read()#Kamerayı oku 20 ms de 1 kare

    #ret, bilgisayarKamerasi = cap.read()#Kamerayı oku 20 ms de 1 kare
    #Görüntüyü bulanıklaştırmak etraftaki gölgelerden oluşabilecek renk bozulmasını önlemek için
    medianBlr = cv2.medianBlur(bilgisayarKamerasi,51,51)#Değerler tek sayı olmalı
    cam = cv2.flip(medianBlr,1)#Kameradan alınan görüntüyü aynalar
    imgColor, mask = renkAraligi.update(cam,hsvaralik)#maskeleme
    imgContours, contours = cvzone.findContours(cam, mask ,minArea = 40) #Maskelenecek azami piksel sayısı
    imgContours = cv2.resize(imgContours, (640, 480), None, 1, 1) #açılan pencereyi boyutlandırmak
    
    #cv2.imshow(' ImageColor', imgContours)#pencerenin ekranda görüntülenmesi
    #cv2.imshow(' original', cam)#pencerenin ekranda görüntülenmesi
    if cv2.waitKey(1) & 0xFF == ord('q'):#kaç ms de bir görüntü alınacağı, Belirlenen harf ile çıkış yapmak
        break 
cap.release()#kamerayı kapatmak
cv2.destroyAllWindows()#pencereleri kapatmak
