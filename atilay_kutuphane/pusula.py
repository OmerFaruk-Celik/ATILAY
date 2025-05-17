def pusula(connection=set()):
        sayi=0
        toplam=0
        while sayi<2:

                import numpy as np
                msg = connection.recv_match(type='RAW_IMU', blocking=True)
                #xmag = msg#.ymag#.yacc#.zacc#.xacc

                if msg != None:
                        sayi+=1

                        if np.rad2deg(np.arctan2(msg.ymag,msg.xmag))<0:
                                d=360+np.rad2deg(np.arctan2(msg.ymag,msg.xmag))
                        else:
                                d=np.rad2deg(np.arctan2(msg.ymag,msg.xmag))
                toplam+=d
                if sayi>=2:
                        ort=toplam/2
                        break
        return ort

