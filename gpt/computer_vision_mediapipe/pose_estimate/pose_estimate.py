import cv2
import time
import pose_estimate_module as pem

# cap = cv2.VideoCapture('video/5.mp4')
cap = cv2.VideoCapture(0)
pTime = 0
detector = pem.poseDetector()
while True:
    sucess, img = cap.read()
    img = detector.findPose(img)
    lmList = detector.findPosition(img, draw=False)
    # cv2.circle(img, (lmList[14][1], lmList[14][2]), 15,(0,0,255),cv2.FILLED)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img,str(int(fps)),(70,50), cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)
    
    cv2.imshow("Image", img)
    cv2.waitKey(10)