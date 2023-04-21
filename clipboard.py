import win32clipboard
import time
import send

currentClipboard = None


def setClipboard(arg):
    global currentClipboard
    if (send.activeIP == send.HOSTIP):
        return
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardText(arg["Text"])
    win32clipboard.CloseClipboard()
    currentClipboard = arg["Text"]


def getClipboard():
    win32clipboard.OpenClipboard()
    if win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_TEXT):
        data = win32clipboard.GetClipboardData()
    else:
        return None
    win32clipboard.CloseClipboard()
    return data


def onCopy():
    global currentClipboard
    while True:
        clipboardText = getClipboard()
        if (currentClipboard == clipboardText):
            time.sleep(1)
            continue
        else:
            send.send(fn=51, Text=clipboardText)
            currentClipboard = clipboardText
