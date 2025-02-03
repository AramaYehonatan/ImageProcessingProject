import cv2

SUCCESS = 1
FAIL = 0

class ImgProcHandler:
    def __init__(self,stream_url):
        self.stream_url = stream_url
        self.cap = None

    def FindBasket(self):
        print("TODO Find Basket")
        return

    def CamConnect(self):
        print("trying to connect to camera")
        self.cap = cv2.VideoCapture(self.stream_url)
        print("finished connecting to camera")
        if self.cap.isOpened():
            return SUCCESS
        else:
            return FAIL

    def Exit(self):
        if self.cap is not None:
            self.cap.release()
        cv2.destroyAllWindows()