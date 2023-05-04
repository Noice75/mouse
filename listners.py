import threading
import win32api
import win32con
import send
import time
import mouse
import keyboard
import clipboard
import runtimeREF


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
activeThreads["rawMouseInput"] = rawMouseInput
activeThreads["onCopy"] = onCopy
mhook = mouse.listner()
khook = keyboard.listner()


def getEdge():
    while True:
        cursor_x, cursor_y = win32api.GetCursorPos()
        if cursor_x == 0:
            return "L", cursor_x, cursor_y  # LEFT
        elif cursor_x == screen_width - 1:
            return "R", cursor_x, cursor_y  # RIGHT
        elif cursor_y == 0:
            return "T", cursor_x, cursor_y  # TOP
        elif cursor_y == screen_height - border_height:
            return "B", cursor_x, cursor_y  # BOTTOM
        time.sleep(0.1)


def active(arg):
    if (arg["ACTIVEIP"] == runtimeREF.HOSTIP):
        if (mhook._listner._running):
            try:
                win32api.SetCursorPos((arg["Width"], 5))
            except:
                pass
            mhook.unSuppress()
            khook.unSuppress()
            print("Unsupressing")
        else:
            pass
    runtimeREF.ACTIVEIP = arg["ACTIVEIP"]
    print("StartingEDGE!")
    while True:
        Edge = getEdge()
        try:  # If client does not exist in relative borders
            runtimeREF.ACTIVEIP = relativeClients[Edge[0]]
            send.sendALL(fn=50, ACTIVEIP=runtimeREF.ACTIVEIP, Width=Edge[1], Height=Edge[2])
            print("Switching")
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
