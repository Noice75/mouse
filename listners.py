import threading
import win32api
import win32con
import send
import time
import mouse
import keyboard
import clipboard
import runtimeREF
import httpServer


relativeClients = {"T": "192.168.1.105"}
screen_width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
screen_height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
border_height = win32api.GetSystemMetrics(win32con.SM_CYBORDER)


# start listners
activeThreads = {}
rawMouseInput = threading.Thread(target=mouse.getMouseRawInput)
rawMouseInput.start()
onCopy = threading.Thread(target=clipboard.onCopy)
onCopy.start()
httpServerRef = threading.Thread(target=httpServer.startServer)
httpServerRef.start()
activeThreads["rawMouseInput"] = rawMouseInput
activeThreads["onCopy"] = onCopy
activeThreads["httpServerRef"] = httpServerRef
mhook = mouse.listner()
khook = keyboard.listner()


def getEdge():
    currentEdge = None
    while True:
        try:
            cursor_x, cursor_y = win32api.GetCursorPos()
            if cursor_x == 0:
                currentEdge = "L" # LEFT
            elif cursor_x == screen_width - 1:
                currentEdge =  "R" # RIGHT
            elif cursor_y == 0:
                currentEdge =  "T" # TOP
            elif cursor_y == screen_height - border_height:
                currentEdge =  "B" # BOTTOM
            if(currentEdge != None and relativeClients[currentEdge] in runtimeREF.clients): # If client is online
                return currentEdge, cursor_x, cursor_y
            else:
                currentEdge = None
            time.sleep(0.1)
        except:
            time.sleep(0.1)
            continue


def active(arg):
    if (arg["ACTIVEIP"] == runtimeREF.HOSTIP):
        if (mhook._listner._running):
            try:
                win32api.SetCursorPos((arg["Width"], 5))
            except:
                pass
            mhook.unSuppress()
            khook.unSuppress()
        else:
            pass
    runtimeREF.ACTIVEIP = arg["ACTIVEIP"]
    while True:
        Edge = getEdge()
        try:  # If client does not exist in relative borders
            runtimeREF.ACTIVEIP = relativeClients[Edge[0]]
            send.sendALL(fn=50, ACTIVEIP=runtimeREF.ACTIVEIP, Width=Edge[1], Height=Edge[2])
            mhook.suppress()
            khook.suppress()
            win32api.SetCursorPos((683, 384))
            break
        except:
            continue

def setActiveIP(arg):
    runtimeREF.ACTIVEIP = arg["ACTIVEIP"]
    if(runtimeREF.ACTIVEIP != runtimeREF.HOSTIP):
        mhook.suppress()
        khook.suppress()
        win32api.SetCursorPos((683, 384))
    print(runtimeREF.ACTIVEIP)


if __name__ == "__main__":
    print(getEdge())
