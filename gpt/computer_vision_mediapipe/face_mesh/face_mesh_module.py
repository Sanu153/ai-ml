import cv2
import mediapipe as mp
import time

class FaceMeshDetector():
        def __init__(self,staticMode=False,maxFace=2,minDetectionCon=0.5,minTrackCon=0.5):
            self.staticMode = staticMode
            self.maxFace = maxFace
            self.minDetectionCon = minDetectionCon
            self.minTrackCon = minTrackCon
            self.mpDraw = mp.solutions.drawing_utils
            self.mpFaceMesh = mp.solutions.face_mesh
            self.faceMesh = self.mpFaceMesh.FaceMesh(max_num_faces=2)
            self.drawSpec = self.mpDraw.DrawingSpec(thickness=1, circle_radius=2)

        def findFaceMesh(self,img,draw=True):
            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            self.results = self.faceMesh.process(imgRGB)
            faces = []
            if self.results.multi_face_landmarks:
                for faceLms in self.results.multi_face_landmarks:
                    if draw:
                        self.mpDraw.draw_landmarks(img, faceLms, self.mpFaceMesh.FACEMESH_CONTOURS,self.drawSpec,self.drawSpec)
                    face = []
                    for id, lm in enumerate(faceLms.landmark):
                        ih, iw, ic = img.shape
                        x, y = int(lm.x*iw), int(lm.y*ih)
                        # cv2.putText(img, str(id), (x,y), cv2.FONT_HERSHEY_PLAIN, 1, (0,255,0), 1)
                        face.append([x,y])
                    faces.append([face])
            return img, faces

def main():
    cap = cv2.VideoCapture('video/4.mp4')
    # cap = cv2.VideoCapture(1)
    pTime = 0
    
    detector = FaceMeshDetector()
    while True:
        sucess, img = cap.read()
        img, faces = detector.findFaceMesh(img)
        print(len(faces))
        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime

        cv2.putText(img, f'FPS:{int(fps)}', (20,70), cv2.FONT_HERSHEY_PLAIN, 3, (0,255,0), 3)

        cv2.imshow("Image", img)
        cv2.waitKey(1)

if __name__ == "__main__":
    main()