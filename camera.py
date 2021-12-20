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
        self.drawColor = (255, 0, 255)
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

                    # Step3: Check which fingers are up
                    fingers = detector.fingersUp()
                    # cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR),
                    #               (255, 0, 255), 2)

                    if fingers[1] and fingers[2]:
                        if xp == 0 and yp == 0:
                            xp, yp = x1, y1
                        cv2.line(img, (xp, yp), (x1, y1), (0,0,0), self.eraserThickness)
                        cv2.line(imgCanvas, (xp, yp), (x1, y1), (0,0,0), self.eraserThickness)

                    # if drawing mode - index finger is up
                    if fingers[1] and fingers[2] == False:
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

            