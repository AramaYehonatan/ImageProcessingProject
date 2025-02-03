import threading
from GUIHandler import GuiHandler
from ImgProcHandler import ImgProcHandler

#Defines
SUCCESS = 1
FAIL = 0
CAMERA_CONNECTED = 1
CAMERA_DISCONNECTED = 2
BASKET_FOUND = 3
BASKET_NOT_FOUND = 4
Stream_url = "http://192.168.1.133:4747/video"

#Global Variables
gui = None
imgProc = None

def FinishBootstrap():
    if imgProc.CamConnect() == FAIL:
        print("Camera could not be connected.")
        Exit()
    gui.updateBootStrapWindow(CAMERA_CONNECTED)
    if imgProc.FindBasket() == FAIL:
        print("Basket could not be found.")
        Exit()
    gui.updateBootStrapWindow(BASKET_FOUND)
    return

def PromptPlayer():
    print("TODO Prompt Player")
    return

def Exit():
    gui.Exit()
    imgProc.Exit()
    return

def Bootstrap():
    bg_thread = threading.Thread(target=FinishBootstrap, daemon=True)
    bg_thread.start()
    gui.CreateStartWindow()

def main():
    global gui
    global imgProc
    imgProc = ImgProcHandler(Stream_url)
    gui = GuiHandler(PromptPlayer, Exit)
    Bootstrap()

if __name__ == "__main__":
    main()