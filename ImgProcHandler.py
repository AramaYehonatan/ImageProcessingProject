import cv2

SUCCESS = 1
FAIL = 0

class ImgProcHandler:
    def __init__(self,stream_url1 = None ,stream_url2 = None):
        self.stream_url1 = stream_url1
        self.stream_url2 = stream_url2
        self.cap1 = None
        self.cap2 = None

    def SearchBall(self):
        print("TODO Search Ball")
        return

    def RecognizeThrow(self):
        print("TODO Recognize Throw")
        return

    def IsScoreFound(self):
        print("TODO Is Score Found")
        return

    def FindBasket(self):
        print("TODO Find Basket")
        return SUCCESS

    def CamConnect(self):
        if self.stream_url1 is not None:
            print("trying to connect to camera1")
            self.cap1 = cv2.VideoCapture(self.stream_url1)
            print("finished connecting to camera1")
            if not self.cap1.isOpened():
                return FAIL

        if self.stream_url2 is not None:
            print("trying to connect to camera2")
            self.cap2 = cv2.VideoCapture(self.stream_url2)
            print("finished connecting to camera2")
            if not self.cap2.isOpened():
                return FAIL
        return SUCCESS

    def Exit(self):
        if self.cap1 is not None:
            self.cap1.release()
        if self.cap2 is not None:
            self.cap2.release()
        cv2.destroyAllWindows()