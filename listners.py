import threading
import win32api
import win32con
import send
import time
import mouse
import keyboard


relativeClients = {"R": "192.168.1.101"}
screen_width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
screen_height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
border_height = win32api.GetSystemMetrics(win32con.SM_CYBORDER)


# start listners
activeThreads = {}
rawMouseInput = threading.Thread(target=mouse.getMouseRawInput)
rawMouseInput.start()
activeThreads["rawMouseInput"] = rawMouseInput
mhook = mouse.listner()
khook = keyboard.listner()


def getEdge():
    while True:
        cursor_x, cursor_y = win32api.GetCursorPos()
        if cursor_x == 0:
            return "L"  # LEFT
        elif cursor_x == screen_width - 1:
            return "R"  # RIGHT
        elif cursor_y == 0:
            return "T"  # TOP
        elif cursor_y == screen_height - border_height:
            return "B"  # BOTTOM
        time.sleep(0.1)


def active(arg):
    if (arg["IP"] == send.HOSTIP):
        if (mhook._listner._running):
            mhook.unSuppress()
            khook.unSuppress()
        else:
            pass
    send.activeIP = arg["IP"]
    while True:
        Edge = getEdge()
        try:  # If client does not exist in relative borders
            send.activeIP = relativeClients[Edge]
            send.send(fn="active", IP=send.activeIP)
            mhook.suppress()
            khook.suppress()
            win32api.SetCursorPos((683, 384))
            break
        except:
            continue


if __name__ == "__main__":
    active({})
