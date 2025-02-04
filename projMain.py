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
Stream_url1 = "http://10.100.102.13:4747/video"
Stream_url2 = "http://10.100.102.17:4747/video"
#Stream_url = "http://192.168.1.133:4747/video"

#Global Variables
gui = None
imgProc = None
start_gui_ready_event = threading.Event()
game_gui_ready_event = threading.Event()


def FinishBootstrap():
    start_gui_ready_event.wait()
    if imgProc.CamConnect() == FAIL:
        print("Camera could not be connected.")
        Exit()
    gui.updateBootStrapWindow(CAMERA_CONNECTED)
    if imgProc.FindBasket() == FAIL:
        print("Basket could not be found.")
        Exit()
    gui.updateBootStrapWindow(BASKET_FOUND)
    return

def GameLoop():
    game_gui_ready_event.wait()
    while True :
        imgProc.SearchBall() #returns only after we have a ball... still don't know what this function returns
        imgProc.RecognizeThrow() #returns only after we have found a throw... still don't know what this function returns
        gui.UpdateScore(imgProc.IsScoreFound()) #returns 0 if no score, and the score if do score
        gui.updateGameWindow(0) #moving to the next player

def PromptPlayer():
    bg_thread = threading.Thread(target=GameLoop, daemon=True)
    bg_thread.start()
    gui.CreateGameWindow()
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
    imgProc = ImgProcHandler(Stream_url1,Stream_url2)
    gui = GuiHandler(PromptPlayer, Exit, start_gui_ready_event, game_gui_ready_event)
    Bootstrap()

if __name__ == "__main__":
    main()