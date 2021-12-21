import cv2
import threading
import numpy as np
import HandTrackingModule as htm
######################
imgCanvas = np.zeros((480, 640, 3), np.uint8)
########################
class RecordingThread (threading.Thread):
    def __init__(self, name, camera):
        threading.Thread.__init__(self)
        self.brushThickness = 5
        self.eraserThickness = 50
        
        # self.colorList=[(255,0,0),(0,255,0),(0,0,255)]
        # self.currColor=1
        self.drawColor = (0,0,255)
        
        self.name = name
        self.isRunning = True

        self.cap = camera
        
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        self.out = cv2.VideoWriter('./static/video.avi',fourcc, 20.0, (640,480))

    def run(self):
        xp, yp = 0, 0
        
        detector = htm.handDetector(maxHands=1)
        # imgCanvas = np.zeros((480, 640, 3), np.uint8)
        while self.isRunning:
            ret, frame = self.cap.read()
            img = detector.findHands(frame)
            lmList, bbox = detector.findPosition(img)
            if ret:
                if len(lmList) != 0:
                    x1, y1 = lmList[8][1:]
                    x2, y2 = lmList[12][1:]
                    # print(x1,y1)
                    # Step3: Check which fingers are up
                    fingers = detector.fingersUp()
                    # cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR),
                    #               (255, 0, 255), 2)
                    # if fingers[0] and not(fingers[1] or fingers[2] or fingers[3] or fingers[4]):
                    #     while(fingers[0]):
                    #         ret, frame = self.cap.read()
                    #         img = detector.findHands(frame)
                    #         lmList, bbox = detector.findPosition(img)
                    #         fingers = detector.fingersUp()
                            
                    #         self.out.write(img)
                    #     print("color change")
                    #     self.currColor =(self.currColor+1)%3
                    #     self.drawColor=self.colorList[self.currColor]
                    if 0<=y1<=25 and 20<=x1<=50:
                        self.drawColor=(255,0,0)
                    elif 0<=y1<=25 and 70<=x1<=100:
                        self.drawColor=(0,255,0)
                    elif 0<=y1<=25 and 120<=x1<=150:
                        self.drawColor=(0,0,255)
                    if fingers[1] and fingers[2] and fingers[3] and fingers[4]:
                        if xp == 0 and yp == 0:
                            xp, yp = x1, y1
                        print("erasing Mode")
                        # cv2.line(img, (xp, yp), (x1, y1), (0,0,0), self.eraserThickness)
                        cv2.line(imgCanvas, (xp, yp), (x1, y1), (0,0,0), self.eraserThickness)

                    # if drawing mode - index finger is up
                    elif fingers[1] and not(fingers[0] or fingers[2] or fingers[3] or fingers[4]):
                        # cv2.circle(img, (x1,y1), 15, drawColor, cv2.FILLED)
                        
                        print("Drawing Mode")

                        if xp == 0 and yp == 0:
                            xp, yp = x1, y1

                        # if self.drawColor == (0, 0, 0):
                        #     cv2.line(img, (xp, yp), (x1, y1), self.drawColor, self.eraserThickness)
                        #     cv2.line(imgCanvas, (xp, yp), (x1, y1), self.drawColor, self.eraserThickness)
                        # else:
                        cv2.line(img, (xp, yp), (x1, y1), self.drawColor, self.brushThickness)
                        cv2.line(imgCanvas, (xp, yp), (x1, y1), self.drawColor, self.brushThickness)

                        xp, yp = x1, y1
                    else:
                        xp, yp = 0, 0
                imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
                _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
                imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
                img = cv2.bitwise_and(img, imgInv)
                img = cv2.bitwise_or(img, imgCanvas)
                img=cv2.flip(img,1)
                img = cv2.rectangle(img, (580,10), (600,25), (255,0,0), 15)
                img = cv2.rectangle(img, (530,10), (550,25), (0,255,0), 15)
                img = cv2.rectangle(img, (480,10), (500,25), (0,0,255), 15)

                self.out.write(img)

        self.out.release()

    def stop(self):
        self.isRunning = False

    def __del__(self):
        self.out.release()

class VideoCamera(object):
    def __init__(self):
        # Open a camera
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, 640)
        self.cap.set(4, 480)
        # Initialize video recording environment
        self.is_record = False
        self.out = None

        # Thread for recording
        self.recordingThread = None
    
    def __del__(self):
        self.cap.release()
    
    def get_frame(self):
        ret, frame = self.cap.read()

        if ret:
            
            frame=cv2.bitwise_or(frame, imgCanvas)
            frame=cv2.flip(frame,1)
            frame = cv2.rectangle(frame, (580,10), (600,25), (255,0,0), 15)
            frame = cv2.rectangle(frame, (530,10), (550,25), (0,255,0), 15)
            frame = cv2.rectangle(frame, (480,10), (500,25), (0,0,255), 15)
            ret, jpeg = cv2.imencode('.jpg', frame)

            # Record video
            # if self.is_record:
            #     if self.out == None:
            #         fourcc = cv2.VideoWriter_fourcc(*'MJPG')
            #         self.out = cv2.VideoWriter('./static/video.avi',fourcc, 20.0, (640,480))
                
            #     ret, frame = self.cap.read()
            #     if ret:
            #         self.out.write(frame)
            # else:
            #     if self.out != None:
            #         self.out.release()
            #         self.out = None  

            return jpeg.tobytes()
      
        else:
            return None

    def start_record(self):
        self.is_record = True
        self.recordingThread = RecordingThread("Video Recording Thread", self.cap)
        self.recordingThread.start()

    def stop_record(self):
        self.is_record = False

        if self.recordingThread != None:
            self.recordingThread.stop()

            