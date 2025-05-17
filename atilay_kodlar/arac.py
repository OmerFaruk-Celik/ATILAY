import time
from atilay import atilay
master=atilay.set(0)
time.sleep(2)
def mesafeyi_koru(master):
    while True:
        x, y0, y1=atilay.lidar("x"), atilay.lidar("y0"), atilay.lidar("y1")
        if y0<=50:
            atilay.yanla(1550,master)
        if y1<50:
            atilay.yanla(1450,master)

        if x<50:
            atilay.ileri_geri(1440,master)

def dip_cam():
    dosya = open("/home/rasp/atilay/dip_cam_status","r")
    status = dosya.read()
    dosya.close()
    if status == "False":
        return False
    elif status == "True":
        return True
    
    
def don(master,tekrar = 4,gorev=False):
    kontrol=0
        
    ilk_derece=atilay.pusula(master)
    while True:
        atilay.sag_sol(1530,master)
        son_derece=atilay.pusula(master)
        son_fark=abs(son_derece-ilk_derece)
        gorev = red_status()
        print("don fonksiyonu gorev=",gorev)
        if abs(son_fark>=90) or gorev == True:
                ilk_derece=atilay.pusula(master)
                kontrol+=1
                if kontrol>=tekrar or gorev==True:
                    atilay.sag_sol()
                    print("break yaptım")
                    time.sleep(1)
                    break
    return gorev

def red_status ():
    
        dosya = open("/home/rasp/atilay/red_status", "r")
        gorev = dosya.read()
        dosya.close()
        
        if gorev=="False":
            return False
        elif gorev=="True":
            return True
        
def tutarli ():
    lOnIlk, lSagIlk, lSolIlk = atilay.lidar("x") ,atilay.lidar("y0"), atilay.lidar("y1")
    lOnTutarli = False
    lSagTutarli = False # LİDARLARDAN ALINAN DEĞERİN BELİRLENEN ARALIKTA OLUP OLMADIĞINI
    lSolTutarli = False # KONTROL EDEN DEĞİŞKEN AYNI ZAMANDA PUSULA SETLEMEK İÇİN GEREKLİ
                    
    if  2 < lOnIlk < 500:
        lOnTutarli = True     
    elif lOnIlk > 500:
        lOnTutarli = False
                            
    if  2 < lSagIlk < 500:  # cm cinsinden yaparız ÇOK HASSAS OLURSA SORUN ÇIKABİLİR
        lSagTutarli = True # Oldu
    elif lSagIlk > 500:
        lSagTutarli = False
                            
    if  2 < lSolIlk < 500:
        lSolTutarli = True
    elif lSolIlk > 500:
        lSolTutarli = False
    return lOnTutarli, lSagTutarli, lSolTutarli

        # ORTALANIN İÇİNDE RED STATUS ÇALIŞMALI
def ortala (master,dip_cam=False):
    tekrar=0
    print("ortaladayim...")
    while tekrar <= 100:
        tekrar+=1
        try:
            x=int(atilay.piksel("x"))
            y=int(atilay.piksel("y"))
        except:
            print("int error...")
        if x>10:
                atilay.yanla(1520,master)
        elif x<-10:
                atilay.yanla(1480,master)
        if dip_cam:
            if y>10:
                atilay.ileri_geri(1510,master)
            elif x<-10:
                atilay.ileri_geri(1460,master)
    return x,y


def solkontrol (master, gorev):
    lOnTutarli, lSagTutarli, lSolTutarli = tutarli()
    while lSolTutarli == False or gorev == False:
        gorev = red_status()
        for i in range(100):
            atilay.yanla(1460,master)
        lOnTutarli, lSagTutarli, lSolTutarli = tutarli()

    atilay.yanla(1460,master)
    return gorev


def ilerle (master, gorev):
    lOnTutarli, lSagTutarli, lSolTutarli = tutarli()
    while lOnTutarli == False or gorev == False:
        atilay.bat_cik(1430,master)
        for i in range(100):
            atilay.ileri_geri(1530,master)
        
        lOnTutarli, lSagTutarli, lSolTutarli = tutarli()
    
        gorev = solkontrol(master, red_status())
    atilay.ileri_geri()
    if gorev == False:
        gorev = don(master, 1)
    return gorev

dongu = True
dosya=open("/home/rasp/atilay/on_cam","w")
dosya.write("True")
dosya.close()


dosya=open("/home/rasp/atilay/dip_cam","w")
dosya.write("False")
dosya.close()

dosya=open("/home/rasp/atilay/red_status","w")
dosya.write("False")
dosya.close()


dosya=open("/home/rasp/atilay/dip_cam_status","w")
dosya.write("False")
dosya.close()

atilay.servo(7,1190,master)

while dongu:
    atilay.bat_cik(1430,master)
    gorev = don(master)

    if gorev == False:
        gorev = ilerle(master, red_status())

    if gorev:
        dosya=open("/home/rasp/atilay/dip_cam","w")
        dosya.write("True")
        dosya.close()
        x,y = ortala(master)
        print("x :",x)
        if x <= 50:
            while True:
                atilay.ileri_geri(1510,master)
                x,y = ortala(master)
                status = dip_cam()
                if status:
                    print("status tayım",x,y)
                    dosya=open("/home/rasp/atilay/on_cam","w")
                    dosya.write("False")
                    dosya.close()
                    break
            while True:
                x,y = ortala(master,True)
                if x <= 20 and y <= 20:
                    zaman = 0
                    while True:
                        x,y = ortala(master,True)
                        time.sleep(0.5)
                        zaman = zaman + 1
                        atilay.bat_cik(1400,master)
                        if zaman >= 90:
                            zaman2 = 0
                            while True:
                                time.sleep(0.5)
                                zaman2 = zaman2 +1
                                atilay.bat_cik(1550,master)
                                if zaman2 >= (60):
                                    dongu = False
                                    break
                        break
                break
