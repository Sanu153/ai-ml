import os
import cv2
import mediapipe as mp
import time
import hand_tracking_module as htm
import numpy as np
import math

wCam, hCam = 640, 480
pTime = 0

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

folderPath = "hand_tracking/pics"
myList = sorted(os.listdir(folderPath))
print(myList)
overlayList = []
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)

detector = htm.handDetector(detectionCon=0.75)
tipIds =[4,8,12,16,20]

while True:
    sucess, img = cap.read()
    img = detector.findHands(img)
    lmlist = detector.findPosition(img,draw=False)
    if len(lmlist) != 0:
        fingers = []
        if lmlist[tipIds[0]][1] > lmlist[tipIds[0]-1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        for id in range(1,5):
            if lmlist[tipIds[id]][2] < lmlist[tipIds[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        totalFingers = fingers.count(1)
        
                
        h,w,c = overlayList[totalFingers-1].shape
        img[0:h, 0:w] = overlayList[totalFingers-1]

        cv2.rectangle(img, (20,255), (170,425), (0,255,0), cv2.FILLED)
        cv2.putText(img, str(totalFingers), (45,375),cv2.FONT_HERSHEY_PLAIN,10,(255,0,0),25)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    
    cv2.putText(img,f'FPS:{int(fps)}',(400,50), cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)
    cv2.imshow("Image", img)
    cv2.waitKey(1)