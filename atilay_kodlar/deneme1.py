from atilay import atilay
import time
master=atilay.set()



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

def red_status ():
    
        dosya = open("/home/rasp/atilay/red_status", "r")
        gorev = dosya.read()
        dosya.close()

        if gorev=="False":
            return False
        elif gorev=="True":
            return True



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


def ilerle (master, gorev):
    #lOnTutarli, lSagTutarli, lSolTutarli = tutarli()
    while gorev == False:
        
        for i in range(1000):
            
            atilay.ileri_geri(1200,master)
            time.sleep(0.5)
            atilay.bat_cik(1430,master)
            gorev=red_status
            if gorev:
                break
        
    
        #gorev = solkontrol(master, red_status())
    #atilay.ileri_geri()
    if gorev == False:
        gorev = don(master, 1)
    return gorev




dosya=open("/home/rasp/atilay/red_status","w")
dosya.write("False")
dosya.close()


dosya=open("/home/rasp/atilay/dip_cam_status","w")
dosya.write("False")
dosya.close()


sayac=0
while True:
	sayac+=1	
	gorev=don(master)
	if not gorev:
		gorev=ilerle(master,gorev)
	atilay.ileri_geri()
	
	while True:
		x,y=ortala(master)
		if x <50 and y <50:
			for i in range(60):
				atilay.bat_cik(1300,master)
				time.sleep(0.5)
			break
	atilay.bat_cik()
	time.sleep(0.5)
	atilay.ileri_geri(1200,master)
	
	if sayac>=500:
		break
