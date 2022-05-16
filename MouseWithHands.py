###########################Wersja Python 3.7, na nowszych wersjach biblioteka autopy nie działa.
###########################
import cv2
import numpy as np
import MouseWithHandsLIB as mwhL
import time
import autopy
###########################
pTime = 0
szOkna, wysOkna = 640, 480
pX, pY = 0, 0
cX, cY = 0, 0
wyg = 7
klatkaR = 100
###########################
cap = cv2.VideoCapture(0) #wybór kamery, jesli kamera druga nalezy wpisać "1"
cap.set(3,szOkna)             #szerokość okna
cap.set(4,wysOkna)             #wysokosc okna
detector = mwhL.hDetect(maxHands =1)
szEkr, wysEkr = autopy.screen.size()

while True:
    success, img = cap.read()       #odczyt# z kamery
    img = detector.fHands(img)
    lmList, bbox  = detector.fPos(img)

    if len(lmList)!=0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]

    fingers = detector.fUp()
    cv2.rectangle(img, (klatkaR, klatkaR), (szOkna - klatkaR, wysOkna - klatkaR), (255, 0, 255), 2)


    #Klikanie LPM
    if fingers[1] == 1 and fingers[2] == 1:
        length, img, lineInfo = detector.fDist(8, 12, img)
        print(length)
        if length < 40:
            cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
            autopy.mouse.click()


    #poruszanie kursorem
    if fingers[1]==1 and fingers[2]==0 :
        x3 = np.interp(x1, (klatkaR,szOkna-klatkaR),(0,szEkr))
        y3 = np.interp(y1, (klatkaR, wysOkna-klatkaR), (0, wysEkr))
        cX = pX + (x3 - pX) / wyg
        cY = pY + (y3 - pY) / wyg
        autopy.mouse.move(szEkr - cX, cY)
        cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
        pX, pY = cX, cY


    #FrameRate
    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255,255,100), 2)
    #Display
    cv2.imshow("Image", img)        #Tytuł okienka
    cv2.waitKey(1)
